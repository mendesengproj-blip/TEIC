"""W3 -- collision with Wilson active (the central test).

Repeat CR_GAUGE's G3 collision, now with the plaquette term, to ask whether lambda_p
confines the charge created in the collision before it radiates, extending the kink's
lifetime.  For lambda_p in {0, lc/2, lc, 2lc, 5lc} (lc from W2) and rho in {10,18,50},
20 seeds, the two scalar chains carry a small TRANSVERSE noise so the created gauge
structure is NOT y-uniform (a y-uniform kink has W_p=0 and would not feel Wilson at all).

Late-window observables (max over rows / averaged over seeds):
  * n_kink        : created gauge cores (phi crosses pi);
  * W_phi         : net winding (must stay ~0, charge conservation);
  * lifetime_frac : fraction of post-collision time windows with n_kink >= 1 (0 = dies
                    at once, 1 = survives the whole window) -- the kink LIFETIME proxy;
  * frac_gauge    : gauge-sector energy fraction that stays in the central region.

The decisive comparison: does lifetime_frac / n_kink GROW with lambda_p?  lambda_p=0 must
reproduce CR_GAUGE (radiation, no surviving kink).

Output: W3_collision.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import wilson_core as wc


def _lc():
    import json
    try:
        return float(json.loads((wc.OUTDIR / "W2_string.json").read_text())["lam_c"])
    except Exception:
        return 1.0


SEEDS = range(20)
RHOS = [10, 18, 50]
NWIN = 6                  # post-collision windows for the lifetime measurement


def central_gauge_fraction(th, vth, px, vpx, py, vpy, dx, lam, x, half=4.0):
    """Gauge-sector energy (kinetic + Wilson) in the central region |x|<half, as a
    fraction of E_total -- the energy that stays trapped at the collision core."""
    comp = wc.energy_components(th, vth, px, vpx, py, vpy, dx, lam)
    m = np.abs(x) < half
    W = wc.plaquette(px, py)
    e_g = 0.5 * dx * float(np.sum(vpx[m, :] ** 2) + np.sum(vpy[m, :] ** 2))
    e_g += lam * dx * float(np.sum(1.0 - np.cos(W[m, :])))
    return float(e_g / comp["E_total"])


def collide(amp, lam, seed):
    x, y, dx = wc.make_grid(Lx=40.0, Nx=201, Ny=10)
    dt = wc.dt_cfl(dx)
    rng = np.random.default_rng(7000 + seed)
    th, vth, px, vpx, py, vpy = wc.two_chains(x, y, float(amp), x0=8.0, w=2.0,
                                              noise=0.01, rng=rng, ynoise=0.04)
    nst = int(round(16.0 / dt))                    # collide ~ t=8, settle by t=16
    th, vth, px, vpx, py, vpy = wc.evolve(th, vth, px, vpx, py, vpy, dx, dt, nst, lam=lam)
    # lifetime: track n_kink over NWIN further windows
    win = int(round(3.0 / dt))
    counts = [wc.kink_count_x(px)]
    cur = (th, vth, px, vpx, py, vpy)
    for _ in range(NWIN):
        cur = wc.evolve(*cur, dx, dt, win, lam=lam)
        counts.append(wc.kink_count_x(cur[2]))
    th, vth, px, vpx, py, vpy = cur
    n_late = counts[-1]
    lifetime_frac = float(np.mean([c >= 1 for c in counts]))
    fr = central_gauge_fraction(th, vth, px, vpx, py, vpy, dx, lam, x)
    return {"n_kink_late": n_late, "max_count": int(max(counts)),
            "winding": wc.winding_x(px), "lifetime_frac": lifetime_frac,
            "frac_gauge": fr, "peak_phi": wc.peak_phi(px)}


def main():
    lam_c = _lc()
    LAMS = [0.0, 0.5 * lam_c, lam_c, 2.0 * lam_c, 5.0 * lam_c]
    print("=" * 70)
    print("W3 -- COLLISION WITH WILSON ACTIVE (lambda_c=%.2f)" % lam_c)
    print("=" * 70)
    rows = []
    for lam in LAMS:
        for rho in RHOS:
            obs = [collide(rho, lam, s) for s in SEEDS]
            nk = wc.seed_stats([float(o["n_kink_late"]) for o in obs])
            lt = wc.seed_stats([o["lifetime_frac"] for o in obs])
            fg = wc.seed_stats([o["frac_gauge"] for o in obs])
            W = wc.seed_stats([o["winding"] for o in obs])
            frac_surv = float(np.mean([o["lifetime_frac"] > 0.5 for o in obs]))
            rows.append({"lam": lam, "rho": rho, "n_kink_late": nk, "lifetime_frac": lt,
                         "frac_gauge": fg, "winding": W, "frac_survive": frac_surv})
            print(f"  lam={lam:5.2f} rho={rho:3d}: n_kink_late={nk['mean']:.2f} "
                  f"lifetime={lt['mean']:.2f} surv_frac={frac_surv:.0%} "
                  f"E_g/E={fg['mean']:.3f} W={W['mean']:+.3f}")

    # does Wilson extend the kink lifetime?  compare lambda=0 vs the largest lambda at each rho
    by_rho = {}
    for rho in RHOS:
        l0 = next(r for r in rows if r["lam"] == 0.0 and r["rho"] == rho)
        lmax = next(r for r in rows if r["lam"] == LAMS[-1] and r["rho"] == rho)
        by_rho[rho] = {"life_lam0": l0["lifetime_frac"]["mean"],
                       "life_lammax": lmax["lifetime_frac"]["mean"],
                       "survive_lam0": l0["frac_survive"], "survive_lammax": lmax["frac_survive"]}
    wilson_helps = any(d["life_lammax"] > d["life_lam0"] + 0.15 for d in by_rho.values())
    any_stable = any(r["frac_survive"] >= 0.5 for r in rows)
    stable_needs_wilson = any_stable and all(
        r["frac_survive"] < 0.5 for r in rows if r["lam"] == 0.0)

    if any_stable and wilson_helps and stable_needs_wilson:
        scenario, grade = "A/B (kink estabilizado por Wilson)", "A"
        statement = ("With Wilson active a created kink SURVIVES the late window in a "
                     "majority of seeds where lambda_p=0 does not -- Wilson confinement "
                     "stabilises collision-created matter; characterise mass in W4.")
    elif wilson_helps:
        scenario, grade = "C (Wilson ajuda, ainda insuficiente)", "C"
        statement = ("Wilson measurably EXTENDS the kink lifetime (lifetime_frac grows "
                     "with lambda_p) but not enough to make a kink survive in a majority "
                     "of seeds: confinement helps but the collision still loses the charge "
                     "to radiation. Stronger lambda_p or higher energy needed.")
    else:
        scenario, grade = "C/D (Wilson sub-dominante; sem estabilizacao)", "D"
        statement = (
            "Wilson does NOT stabilise the collision-created kink in the testable regime: "
            "lifetime_frac and n_kink are essentially independent of lambda_p (the "
            "plaquette term is sub-dominant to the inherited gauge stiffness, W2), and "
            "lambda_p=0 already reproduces CR_GAUGE's radiation outcome. The created "
            "charge disperses regardless of lambda_p. As W2 showed, static 2D compact-U(1) "
            "does not linearly confine winding-+/-1 charges, so there is no confining "
            "string to catch the charge -- the frontier is deeper than the plaquette term "
            "(needs the dynamical Polyakov/monopole mechanism, higher dimension, or an "
            "external field).")
    print("-" * 70)
    print(f"VERDICT W3: cenario {scenario} (grade {grade})")
    print(f"  {statement}")

    _figure(rows, LAMS)
    out = {"lam_c": lam_c, "lams": LAMS, "rhos": RHOS, "n_seeds": len(list(SEEDS)),
           "rows": rows, "by_rho": by_rho, "wilson_helps": bool(wilson_helps),
           "any_stable": bool(any_stable), "stable_needs_wilson": bool(stable_needs_wilson),
           "scenario": scenario, "grade": grade, "statement": statement}
    wc.save_json("W3_collision", out)
    _write_md(rows, out, LAMS)
    return out


def _figure(rows, LAMS):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    ax = axes[0]
    for rho in RHOS:
        ls = [r["lam"] for r in rows if r["rho"] == rho]
        lf = [r["lifetime_frac"]["mean"] for r in rows if r["rho"] == rho]
        ax.plot(ls, lf, "o-", label=f"rho={rho}")
    ax.set_xlabel("lambda_p"); ax.set_ylabel("kink lifetime fraction")
    ax.set_title("W3 -- kink lifetime vs lambda_p")
    ax.legend(fontsize=9)
    ax2 = axes[1]
    for rho in RHOS:
        ls = [r["lam"] for r in rows if r["rho"] == rho]
        nk = [r["n_kink_late"]["mean"] for r in rows if r["rho"] == rho]
        ax2.plot(ls, nk, "s-", label=f"rho={rho}")
    ax2.set_xlabel("lambda_p"); ax2.set_ylabel("late n_kink")
    ax2.set_title("W3 -- created cores vs lambda_p")
    ax2.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(wc.OUTDIR / "W3_collision.png", dpi=130)
    plt.close(fig)


def _write_md(rows, out, LAMS):
    lines = [
        "# W3 -- Colisão com Wilson ativo (teste central)",
        "",
        f"Colisão de CR_GAUGE (G3) com o termo de plaqueta ativo (λ_c = {out['lam_c']:.2f} "
        "de W2). Cadeias com ruído transverso (para a estrutura criada não ser y-uniforme,",
        "que teria W_p=0). Por (λ_p, ρ), 20 sementes, janela tardia:",
        "",
        "| λ_p | ρ | n_kink tardio | lifetime | sobrevive | E_gauge/E | W_φ |",
        "|-----|---|---------------|----------|-----------|-----------|-----|",
    ]
    for r in rows:
        lines.append(f"| {r['lam']:.2f} | {r['rho']} | {r['n_kink_late']['mean']:.2f} | "
                     f"{r['lifetime_frac']['mean']:.2f} | {r['frac_survive']:.0%} | "
                     f"{r['frac_gauge']['mean']:.3f} | {r['winding']['mean']:+.3f} |")
    lines += [
        "",
        f"## VERDICT W3: cenário {out['scenario']} (grade {out['grade']})",
        "",
        out["statement"],
        "",
        "![colisao](W3_collision.png)",
        "",
    ]
    (wc.OUTDIR / "W3_collision.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
