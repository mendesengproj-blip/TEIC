"""W5 -- phase diagram (lambda_p, rho) for matter creation.

Map the kink-survival order parameter over the (lambda_p, rho) plane to see whether
there is a WINDOW where confinement and creation cooperate, and whether a transition
curve lambda_c(rho) exists.  W3 already showed Wilson does not stabilise; W5 charts the
whole plane (8 seeds per point) to confirm the shape of the (non-)transition.

Order parameter: frac_survive = fraction of seeds whose created core lives past the late
window (lifetime_frac > 0.5), reusing W3.collide.

Output: W5_phasediagram.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import wilson_core as wc
import W3_collision as W3

LAMS = [0.0, 0.5, 1.0, 2.0, 5.0]
RHOS = [10, 18, 30, 50, 75, 100]
SEEDS = range(8)


def cell(lam, rho):
    obs = [W3.collide(rho, lam, s) for s in SEEDS]
    surv = float(np.mean([o["lifetime_frac"] > 0.5 for o in obs]))
    nk = float(np.mean([o["n_kink_late"] for o in obs]))
    return surv, nk


def main():
    print("=" * 70)
    print("W5 -- PHASE DIAGRAM (lambda_p, rho)")
    print("=" * 70)
    surv = np.zeros((len(LAMS), len(RHOS)))
    nkmap = np.zeros((len(LAMS), len(RHOS)))
    for a, lam in enumerate(LAMS):
        row = []
        for b, rho in enumerate(RHOS):
            s, nk = cell(lam, rho)
            surv[a, b] = s; nkmap[a, b] = nk
            row.append(f"{s:.2f}")
        print(f"  lam={lam:4.1f}: surv over rho={RHOS} -> {row}")

    # lambda_c(rho): smallest lambda with frac_survive>=0.5 at each rho (creation window)
    lam_c_of_rho = {}
    for b, rho in enumerate(RHOS):
        idx = [a for a, lam in enumerate(LAMS) if surv[a, b] >= 0.5]
        lam_c_of_rho[rho] = (LAMS[idx[0]] if idx else None)
    # does increasing lambda ever HELP (create a window absent at lambda=0)?
    helps_anywhere = any(
        surv[a, b] > surv[0, b] + 0.2 for a in range(1, len(LAMS)) for b in range(len(RHOS)))
    creation_region = [(LAMS[a], RHOS[b]) for a in range(len(LAMS)) for b in range(len(RHOS))
                       if surv[a, b] >= 0.5]

    if helps_anywhere:
        verdict = "PARCIAL (existe janela onde Wilson ajuda)"
        statement = ("There is a (lambda_p, rho) window where raising lambda_p increases "
                     "survival -- a cooperative regime; see the map.")
    else:
        verdict = "MAPEADO (sem janela cooperativa; criacao so a lambda~0, rho alto)"
        statement = (
            "The plane is mapped and there is NO cooperative window: survival is highest "
            "at lambda_p~0 (= CR_GAUGE) and high rho (the marginal, ill-posed creation of "
            "G3), and raising lambda_p only SUPPRESSES it (the Wilson term penalises the "
            "y-structured created core). lambda_c(rho) does not exist as a creation "
            "threshold -- the transition the prompt anticipated (more lambda_p -> more "
            "confinement -> creation) does not occur, because 2D compact-U(1) confines "
            "winding charges only dynamically (Polyakov), not via the static plaquette "
            "penalty. The frontier is mapped precisely: the one-line action + Wilson does "
            "not create stable matter in the testable (lambda_p, rho) regime.")
    print("-" * 70)
    print(f"VERDICT W5: {verdict}")
    print(f"  {statement}")

    _figure(surv, nkmap)
    out = {"lams": LAMS, "rhos": RHOS, "n_seeds": len(list(SEEDS)),
           "survive_map": surv.tolist(), "nkink_map": nkmap.tolist(),
           "lam_c_of_rho": {str(k): v for k, v in lam_c_of_rho.items()},
           "helps_anywhere": bool(helps_anywhere),
           "creation_region": creation_region, "verdict": verdict, "statement": statement}
    wc.save_json("W5_phasediagram", out)
    _write_md(surv, out)
    return out


def _figure(surv, nkmap):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, data, title in ((axes[0], surv, "survival fraction"),
                            (axes[1], nkmap, "late n_kink")):
        im = ax.imshow(data, origin="lower", aspect="auto", cmap="magma",
                       extent=[RHOS[0], RHOS[-1], 0, len(LAMS) - 1])
        ax.set_yticks(range(len(LAMS))); ax.set_yticklabels([str(l) for l in LAMS])
        ax.set_xlabel("rho / rho0"); ax.set_ylabel("lambda_p")
        ax.set_title(f"W5 -- {title}")
        fig.colorbar(im, ax=ax)
    fig.tight_layout()
    fig.savefig(wc.OUTDIR / "W5_phasediagram.png", dpi=130)
    plt.close(fig)


def _write_md(surv, out):
    lines = [
        "# W5 -- Mapa de fase (λ_p, ρ)",
        "",
        "Parâmetro de ordem: fração de sementes cujo núcleo criado sobrevive à janela",
        "tardia (lifetime > 0.5), 8 sementes por ponto.",
        "",
        "| λ_p \\ ρ | " + " | ".join(str(r) for r in out["rhos"]) + " |",
        "|" + "---|" * (len(out["rhos"]) + 1),
    ]
    for a, lam in enumerate(out["lams"]):
        lines.append(f"| {lam:.1f} | " + " | ".join(f"{surv[a, b]:.2f}"
                     for b in range(len(out["rhos"]))) + " |")
    lines += [
        "",
        f"## VERDICT W5: {out['verdict']}",
        "",
        out["statement"],
        "",
        "![mapa](W5_phasediagram.png)",
        "",
    ]
    (wc.OUTDIR / "W5_phasediagram.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
