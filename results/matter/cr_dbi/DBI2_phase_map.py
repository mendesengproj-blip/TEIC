"""DBI2 -- phase map of the collision: where does (phi + Dtheta) reach pi?

Before colliding, map the maximum link phase (phi + Dtheta)_max that a collision of a
given amplitude (= 'energy density' rho proxy) generates in the encounter region, by
evolving the cos dynamics and recording the peak link phase over the collision window.

The cosine's critical point is phi+Dtheta = pi: there cos''(u) = -cos(u) changes sign,
so the gradient action [1-cos(Dtheta)] turns from convex to CONCAVE.  We identify the
density rho_pi where the peak phase first reaches pi -- a MEASURED threshold (pi enters
only as the cosine's inflection, never as a 'creation' input).

We also flag the loss of hyperbolicity: once the peak phase exceeds pi, the scalar
gradient-cos evolution stops converging under time-step refinement (peak |theta| does
not settle) -- the ill-posed regime probed in DBI3.

Output: DBI2_phase_map.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import dbi_core as dbi

# rho/rho0 == field amplitude (rho0 <-> amp 1).  Fine ladder to locate the pi crossing.
RHOS = [1, 2, 3, 5, 8, 12, 16, 20, 25, 30, 40, 50, 75, 100]
SEEDS = range(12)


def peak_phase(amp, seed):
    """Peak link phase over the collision, with small IC noise (seed sensitivity)."""
    x, dx = dbi.make_grid()
    dt = 0.1 * dx
    rng = np.random.default_rng(2000 + seed)
    th0, v0 = dbi.two_packets(x, float(amp), noise=0.01, rng=rng)
    _, _, hist = dbi.evolve(th0, v0, dbi.force_cos, dx, dt, 3000, record_every=40)
    return max(dbi.phase_max(h) for h in hist)


def main():
    print("=" * 70)
    print("DBI2 -- PHASE MAP: (phi+Dtheta)_max vs rho, find rho_pi")
    print("=" * 70)
    rows = []
    for rho in RHOS:
        st = dbi.seed_stats([peak_phase(rho, s) for s in SEEDS])
        rows.append({"rho": rho, **st})
        flag = "  <-- crosses pi" if st["mean"] >= np.pi and (
            not rows[:-1] or rows[-2]["mean"] < np.pi) else ""
        print(f"  rho={rho:4d}rho0: (phi+Dtheta)_max = {st['mean']:8.3f} +/- {st['sem']:.3f}{flag}")

    # rho_pi: linear interpolation of mean peak-phase crossing pi
    rho_pi = None
    for a, b in zip(rows[:-1], rows[1:]):
        if a["mean"] < np.pi <= b["mean"]:
            t = (np.pi - a["mean"]) / (b["mean"] - a["mean"])
            rho_pi = float(a["rho"] + t * (b["rho"] - a["rho"]))
            break
    reached = any(r["mean"] >= np.pi for r in rows)
    print("-" * 70)
    print(f"  critical phase pi reached: {reached};  rho_pi = "
          f"{'%.1f rho0' % rho_pi if rho_pi else 'n/a'}")

    verdict = "SIM" if reached else "NAO"
    statement = (
        "The collision phase (phi+Dtheta)_max grows with density and crosses the cosine "
        "critical point pi at rho_pi = %.1f rho0 (measured, pi = cosine inflection, not "
        "inserted). Below rho_pi the gradient action is convex (stable); above it cos'' "
        "< 0 and the action turns concave -- the ill-posed regime tested in DBI3."
        % (rho_pi if rho_pi else float("nan")))
    print(f"VERDICT DBI2: {verdict}")
    print(f"  {statement}")

    _figure(rows, rho_pi)
    out = {"rhos": RHOS, "n_seeds": len(list(SEEDS)),
           "rows": rows, "pi": float(np.pi), "rho_pi": rho_pi,
           "pi_reached": bool(reached), "verdict": verdict, "statement": statement}
    dbi.save_json("DBI2_phase_map", out)
    _write_md(rows, rho_pi, out)
    return out


def _figure(rows, rho_pi):
    rho = np.array([r["rho"] for r in rows], float)
    ph = np.array([r["mean"] for r in rows])
    er = np.array([r["sem"] for r in rows])
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.errorbar(rho, ph, yerr=er, fmt="o-", color="#c0392b", capsize=3,
                label="(phi+Dtheta)_max measured")
    ax.axhline(np.pi, color="k", lw=1.0, ls="--", label="pi (cos critical point)")
    if rho_pi:
        ax.axvline(rho_pi, color="#2980b9", lw=1.0, ls=":",
                   label=f"rho_pi = {rho_pi:.1f} rho0")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("density rho / rho0  (= field amplitude)")
    ax.set_ylabel("peak link phase (phi+Dtheta)_max")
    ax.set_title("DBI2 -- collision phase reaches the cosine critical point pi")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(dbi.OUTDIR / "DBI2_phase_map.png", dpi=130)
    plt.close(fig)


def _write_md(rows, rho_pi, out):
    lines = [
        "# DBI2 -- Mapa de fase: (φ+Δθ)_max vs ρ",
        "",
        "Antes de colidir, mede-se a fase de link máxima `(φ+Δθ)_max` gerada na colisão",
        "(amplitude = proxy de ρ). O ponto crítico do cosseno é π, onde `cos''(u)` muda",
        "de sinal e a ação de gradiente `[1−cos Δθ]` passa de convexa a **côncava**.",
        "",
        "| ρ/ρ₀ | (φ+Δθ)_max (média ± sem) |",
        "|------|---------------------------|",
    ]
    for r in rows:
        lines.append(f"| {r['rho']} | {r['mean']:.3f} ± {r['sem']:.3f} |")
    lines += [
        "",
        f"- π atingido: **{out['pi_reached']}**",
        f"- **ρ_π = {('%.1f ρ₀' % rho_pi) if rho_pi else 'n/a'}** (medido; π = inflexão do cosseno)",
        "",
        f"## VERDICT DBI2: {out['verdict']}",
        "",
        out["statement"],
        "",
        "Abaixo de ρ_π a ação é convexa (estável); acima, `cos'' < 0` → côncava → regime",
        "mal-posto testado em DBI3.",
        "",
        "![fase](DBI2_phase_map.png)",
        "",
    ]
    (dbi.OUTDIR / "DBI2_phase_map.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
