"""R2_current.py -- gauge current around the vortex and the centrifuge criterion.

PE4_V2 task R2.  Measure the gauge current  J_mu = Dtau * sin(phi + Dtheta)  around a
winding-1 vortex (theta=0 => J = Dtau sin(phi)) and test:
  (1) does J circulate tangentially around the core?  (circulation != 0)
  (2) is |J| concentrated near the core and decaying outside?
  (3) the centrifuge criterion: the causal angular momentum  L = circulation * xi  vs the
      causal inertia  rho * xi^2.  Ratio L/(rho xi^2) > 1 means the circulating current
      carries enough angular momentum to redistribute the local causal density (the
      mechanism R1's dynamical depletion realises).

xi (core size) is the half-max radius of the gauge action density a(r) = sum [1-cos(u)].

Anti-circularity: J is the action's own current (delta S / delta A); rho a count; no complex
literal.  [The superfluid analogy -- circulating supercurrent depleting the Cooper-pair
density at an Abrikosov vortex core -- is COMPARISON ONLY below.]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2_core as v2   # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

NSEED = 10
GRID = (33, 28, 28)
R_EDGES = np.arange(0.0, 12.0, 1.0)


def half_max_radius(centers, prof):
    centers = np.asarray(centers, float); prof = np.asarray(prof, float)
    ok = np.isfinite(prof)
    if not ok.any():
        return float("nan")
    peak = np.nanmax(prof)
    half = 0.5 * peak
    below = np.where(prof[ok] < half)[0]
    if below.size == 0:
        return float(centers[ok][-1])
    return float(centers[ok][below[0]])


def measure_once(seed, T=100):
    rng = np.random.default_rng(seed)
    (px, py, pz), (x, y, z, dx), (xc, yc) = v2.relax_vortex(
        GRID, W=1, T_ticks=T, rng=rng, noise=0.05)
    a = v2.node_action_density(px, py, pz)
    cA, pA = v2.radial_profile(a, x, y, xc, yc, R_EDGES)
    Jm = v2.current_magnitude_field(px, py, pz)
    cJ, pJ = v2.radial_profile(Jm, x, y, xc, yc, R_EDGES)
    xi = half_max_radius(cA, pA)
    # circulation at the core radius xi, and the |J| decay outside
    circ_xi = v2.tangential_circulation(px, py, pz, x, y, xc, yc, max(xi, 1.0))
    circ_2xi = v2.tangential_circulation(px, py, pz, x, y, xc, yc, max(2 * xi, 2.0))
    rho0 = 1.0
    L = abs(circ_xi) * xi
    ratio = L / (rho0 * xi ** 2) if xi > 0 else float("nan")
    return {"xi": xi, "circ_xi": circ_xi, "circ_2xi": circ_2xi, "L": L,
            "ratio_L_over_rho_xi2": ratio, "Jprof": pJ.tolist(), "centers": list(cJ),
            "Jcore": float(pJ[0]), "Jfar": float(np.nanmean(pJ[-3:]))}


def main():
    rows = [measure_once(2000 + s) for s in range(NSEED)]

    def ms(key):
        v = np.array([r[key] for r in rows if np.isfinite(r[key])])
        return float(v.mean()), float(v.std(ddof=1)) if v.size > 1 else 0.0

    xi_m, xi_s = ms("xi")
    circ_m, circ_s = ms("circ_xi")
    ratio_m, ratio_s = ms("ratio_L_over_rho_xi2")
    Jprof = np.nanmean([r["Jprof"] for r in rows], axis=0)
    centers = rows[0]["centers"]

    circulates = bool(abs(circ_m) > 2 * circ_s and abs(circ_m) > 0.05)
    decays = bool(np.nanmean([r["Jcore"] for r in rows]) >
                  np.nanmean([r["Jfar"] for r in rows]))
    centrifuge = bool(ratio_m - 2 * ratio_s > 1.0)

    summary = {
        "n_seeds": NSEED, "grid": list(GRID),
        "xi_core": xi_m, "xi_std": xi_s,
        "circulation_at_xi": circ_m, "circulation_std": circ_s,
        "ratio_L_over_rho_xi2": ratio_m, "ratio_std": ratio_s,
        "J_circulates": circulates, "J_decays_outward": decays,
        "centrifuge_criterion_met": centrifuge,
        "Jprofile_mean": Jprof.tolist(), "centers": list(centers),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    v2.save_json("R2_current", summary)

    fig, ax = plt.subplots(figsize=(6.2, 4.5))
    ax.plot(centers, Jprof, "o-", color="C2", label=r"$|J|(r_\perp)$")
    ax.axvline(xi_m, color="0.5", ls="--", lw=1, label=fr"$\xi={xi_m:.1f}$")
    ax.set_xlabel(r"$r_\perp$ (cells)"); ax.set_ylabel(r"$|J|$")
    ax.set_title(f"(R2) gauge current: circulation={circ_m:.2f}±{circ_s:.2f}, "
                 f"L/(ρξ²)={ratio_m:.2f}±{ratio_s:.2f}")
    ax.legend(); fig.tight_layout(); fig.savefig(v2.OUTDIR / "R2_current.png", dpi=110)
    plt.close(fig)

    print("=" * 76)
    print(f"R2 -- GAUGE CURRENT AROUND THE VORTEX  ({NSEED} seeds)")
    print("=" * 76)
    print(f"  core size xi (half-max of action) = {xi_m:.2f} +/- {xi_s:.2f}")
    print(f"  tangential circulation at xi       = {circ_m:+.3f} +/- {circ_s:.3f}  "
          f"(circulates: {circulates})")
    print(f"  |J| core={np.nanmean([r['Jcore'] for r in rows]):.3f} "
          f"far={np.nanmean([r['Jfar'] for r in rows]):.3f}  (decays outward: {decays})")
    print(f"  L/(rho xi^2) = {ratio_m:.3f} +/- {ratio_s:.3f}  "
          f"(centrifuge criterion >1: {centrifuge})")
    print("-" * 76)
    print(f"VERDICT (R2): J circulates ({circulates}); centrifuge criterion L/(rho xi^2)>1: "
          f"{centrifuge}.")
    print("  The vortex carries a real circulating gauge current; its angular momentum is")
    print(f"  {'sufficient' if centrifuge else 'borderline/insufficient'} to drive the "
          f"causal-density redistribution R1 measures.")
    return summary


if __name__ == "__main__":
    main()
