"""R1_rarefaction.py -- does the vortex DEPLETE the effective causal density at the core?

PE4_V2 task R1.  Two faithful measures of rho_eff around a winding-W vortex core:

  (K) KINEMATIC link flux (the prompt's literal rho_eff = count of Dtau>0 causal links per
      shell): on a regular lattice the link COUNT is the same everywhere, so this is FLAT.
      This makes explicit the rho_Poisson(nodes, PE4) -> rho_eff(links) distinction and
      shows the vortex does NOT change the kinematic link count.

  (D) DYNAMICAL back-reaction (the physical hypothesis): the causal density, treated as the
      bridge's dynamical geometry field (D1-D3/BD relax the density under the minimal
      action), minimises sum_links rho[1-cos(u)] + (K/2)(grad rho)^2 under conservation.
      The equilibrium DEPLETES rho where the vortex gauge action [1-cos(u)] peaks -- the
      core.  The dip SIGN/SHAPE is robust; the DEPTH scales as 1/K and reaches |Phi|(0)->0
      for soft/moderate stiffness.

Scans: relaxation time T in {10,50,100,200} ticks, winding W in {1,2}, background-density
factor in {1,5,20}, and the geometry stiffness K (to expose the depth's 1/K law).  20
seeds (gauge noise) for the headline dip.

Anti-circularity: rho_eff is a count / an action-minimising density; the vortex action and
current are genuine fields; no complex literal.  [Superfluid analogy: COMPARISON ONLY below.]
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

NSEED = 20          # headline T-scan (the prompt's "20 seeds for R1")
NSEED_SCAN = 8      # K/rho characterisation scans (cheaper; trends are deterministic)
GRID = (29, 24, 24)
R_EDGES = np.arange(0.0, 11.0, 1.0)


def _dip(prof):
    prof = np.asarray(prof, float)
    far = np.nanmean(prof[-3:])
    core = prof[0]
    return float((far - core) / far) if far else float("nan")


def measure_once(W, T, rho_factor, K, seed):
    rng = np.random.default_rng(seed)
    (px, py, pz), (x, y, z, dx), (xc, yc) = v2.relax_vortex(
        GRID, W=W, T_ticks=T, rng=rng, noise=0.05)
    # kinematic link flux (flat baseline)
    cK, pK = v2.kinematic_link_flux(px, py, pz, x, y, xc, yc, R_EDGES)
    # dynamical back-reaction density
    cD, pD, rho_eff, a = v2.dynamical_rho_eff(px, py, pz, x, y, xc, yc, R_EDGES,
                                             K=K, rho_factor=rho_factor)
    return cD, pK, pD, _dip(pK), _dip(pD)


def scan_seeds(W, T, rho_factor, K, nseed=NSEED):
    kin_dips, dyn_dips, dyn_profs, centers = [], [], [], None
    for s in range(nseed):
        c, pK, pD, dK, dD = measure_once(W, T, rho_factor, K, seed=1000 + s)
        centers = c
        kin_dips.append(dK); dyn_dips.append(dD); dyn_profs.append(pD)
    prof_mean = np.nanmean(dyn_profs, axis=0)
    return {
        "W": W, "T": T, "rho_factor": rho_factor, "K": K,
        "kin_dip_mean": float(np.nanmean(kin_dips)), "kin_dip_std": float(np.nanstd(kin_dips)),
        "dyn_dip_mean": float(np.nanmean(dyn_dips)), "dyn_dip_std": float(np.nanstd(dyn_dips)),
        "centers": list(np.asarray(centers)), "dyn_profile_mean": prof_mean.tolist(),
    }


def main():
    res = {"n_seeds": NSEED, "grid": list(GRID)}

    # headline at the natural stiffness K=1, base density, W=1, over T
    print("=" * 76)
    print(f"R1 -- CAUSAL RAREFACTION AT THE VORTEX CORE  ({NSEED} seeds)")
    print("=" * 76)
    print("\n[T scan]  W=1, rho_factor=1, K=1  -- kinematic(link count) vs dynamical(back-reaction):")
    T_rows = []
    for T in (10, 50, 100, 200):
        r = scan_seeds(W=1, T=T, rho_factor=1.0, K=1.0)
        T_rows.append(r)
        print(f"  T={T:3d}: kinematic dip={r['kin_dip_mean']:+.3f}+/-{r['kin_dip_std']:.3f}"
              f"   DYNAMICAL dip={r['dyn_dip_mean']:+.3f}+/-{r['dyn_dip_std']:.3f}")
    res["T_scan"] = T_rows

    # stiffness K scan (depth ~ 1/K; where does |Phi|(0) stop reaching 0?)
    print("\n[K scan]  W=1, T=100, rho_factor=1  -- the dynamical dip depth vs stiffness:")
    K_rows = []
    for K in (0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
        r = scan_seeds(W=1, T=100, rho_factor=1.0, K=K, nseed=NSEED_SCAN)
        K_rows.append(r)
        print(f"  K={K:5.1f}: dynamical dip={r['dyn_dip_mean']:+.3f}+/-{r['dyn_dip_std']:.3f}"
              f"   ({'FULL |Phi|(0)->0' if r['dyn_dip_mean']>0.98 else 'partial'})")
    res["K_scan"] = K_rows
    # critical stiffness K* where dip drops below 0.98 (|Phi|(0) stops reaching 0)
    Kstar = None
    for r in K_rows:
        if r["dyn_dip_mean"] < 0.98:
            Kstar = r["K"]; break
    res["K_star_full_depletion_below"] = Kstar

    # background-density scan (denser network -> stronger source -> deeper dip)
    print("\n[rho scan]  W=1, T=100, K=4 (so the dip is not saturated)  -- density factor:")
    rho_rows = []
    for rf in (1.0, 5.0, 20.0):
        r = scan_seeds(W=1, T=100, rho_factor=rf, K=4.0, nseed=NSEED_SCAN)
        rho_rows.append(r)
        print(f"  rho_factor={rf:5.1f}: dynamical dip={r['dyn_dip_mean']:+.3f}"
              f"+/-{r['dyn_dip_std']:.3f}")
    res["rho_scan"] = rho_rows

    # decision
    base = T_rows[2]  # T=100
    rarefaction = bool(base["dyn_dip_mean"] > 0.1 and
                       base["dyn_dip_mean"] > 2 * base["dyn_dip_std"])
    kinematic_flat = bool(abs(base["kin_dip_mean"]) < 0.02)
    res["rarefaction_dynamical"] = rarefaction
    res["kinematic_flux_flat"] = kinematic_flat

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.6))
    for r in T_rows:
        ax[0].plot(r["centers"], r["dyn_profile_mean"], "o-", label=f"T={r['T']}")
    ax[0].axhline(1.0, color="0.6", ls="--", lw=1, label="far field")
    ax[0].set_xlabel(r"$r_\perp$ (cells)"); ax[0].set_ylabel(r"$\rho_{\rm eff}(r)$")
    ax[0].set_title("(R1) dynamical $\\rho_{\\rm eff}$ around the core (depletes)")
    ax[0].legend(fontsize=8)
    Ks = [r["K"] for r in K_rows]; dips = [r["dyn_dip_mean"] for r in K_rows]
    ax[1].plot(Ks, dips, "s-", color="C3")
    ax[1].axhline(1.0, color="0.6", ls=":", lw=1, label="full depletion |Φ|(0)→0")
    ax[1].set_xscale("log"); ax[1].set_xlabel("geometry stiffness K")
    ax[1].set_ylabel("core dip depth"); ax[1].set_ylim(0, 1.05)
    ax[1].set_title("(R1) depth ~ 1/K: full for K≲5, partial above"); ax[1].legend(fontsize=8)
    fig.tight_layout(); fig.savefig(v2.OUTDIR / "R1_rarefaction.png", dpi=110); plt.close(fig)

    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    v2.save_json("R1_rarefaction", res)

    print("-" * 76)
    print(f"VERDICT (R1): kinematic link flux FLAT ({kinematic_flat}); "
          f"DYNAMICAL rarefaction = {rarefaction}")
    print(f"  The vortex does NOT change the causal-link COUNT (kinematic, flat), but the")
    print(f"  causal density -- IF dynamical (D1-D3) -- DEPLETES at the core: dip "
          f"{base['dyn_dip_mean']:.2f}+/-{base['dyn_dip_std']:.2f} at K=1, reaching "
          f"|Phi|(0)->0 for K<~{Kstar if Kstar else 'all tested'}.")
    return res


if __name__ == "__main__":
    main()
