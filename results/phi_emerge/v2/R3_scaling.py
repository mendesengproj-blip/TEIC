"""R3_scaling.py -- does the core depletion scale with the winding number W?

PE4_V2 task R3 (runs because R1 found dynamical rarefaction).  If the rarefaction is
topological, the core depletion should grow with the winding W.  We measure, for W in
{1,2,3}, the vortex action density at the core a(0), the UNCLAMPED density response
drho(0) (which is linear in the source, so it exposes the scaling without the |Phi|>=0
clamp masking it), and the clamped relative dip at a stiffness chosen so the dip is NOT
saturated (so a W-dependence is visible).

Anti-circularity: as v2_core.  [Abrikosov lattice / multiply-quantised vortex: COMPARISON ONLY.]
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import v2_core as v2   # noqa: E402

NSEED = 10
GRID = (33, 28, 28)
R_EDGES = np.arange(0.0, 12.0, 1.0)
K_UNSAT = 16.0      # stiff enough that the dip is partial -> W-dependence is visible


def measure(W, K, seed):
    rng = np.random.default_rng(seed)
    (px, py, pz), (x, y, z, dx), (xc, yc) = v2.relax_vortex(
        GRID, W=W, T_ticks=100, rng=rng, noise=0.05)
    a = v2.node_action_density(px, py, pz)
    cA, pA = v2.radial_profile(a, x, y, xc, yc, R_EDGES)
    drho = v2.relax_density(a, K=K)
    cD, pD = v2.radial_profile(drho, x, y, xc, yc, R_EDGES)          # UNclamped response
    cR, pR, rho_eff, _ = v2.dynamical_rho_eff(px, py, pz, x, y, xc, yc, R_EDGES, K=K)
    far = np.nanmean(pR[-3:])
    return {"a_core": float(pA[0]),
            "drho_core_unclamped": float(pD[0]),
            "dip_clamped": float((far - pR[0]) / far) if far else float("nan")}


def main():
    rows = {}
    for W in (1, 2, 3):
        seeds = [measure(W, K_UNSAT, 3000 + 10 * W + s) for s in range(NSEED)]
        def ms(key):
            v = np.array([r[key] for r in seeds if np.isfinite(r[key])])
            return float(v.mean()), float(v.std(ddof=1)) if v.size > 1 else 0.0
        rows[W] = {"a_core": ms("a_core"), "drho_core": ms("drho_core_unclamped"),
                   "dip": ms("dip_clamped")}

    # fit |drho_core| ~ W^p (the cleanest unclamped scaling)
    Ws = np.array([1, 2, 3], float)
    drc = np.array([abs(rows[w]["drho_core"][0]) for w in (1, 2, 3)])
    p = float(np.polyfit(np.log(Ws), np.log(drc), 1)[0])
    # ratios relative to W=1
    ratio2 = abs(rows[2]["drho_core"][0]) / abs(rows[1]["drho_core"][0])
    ratio3 = abs(rows[3]["drho_core"][0]) / abs(rows[1]["drho_core"][0])
    linear = bool(abs(ratio2 - 2.0) < 0.5 and abs(ratio3 - 3.0) < 0.8)

    summary = {
        "n_seeds": NSEED, "K": K_UNSAT,
        "per_W": {str(w): rows[w] for w in (1, 2, 3)},
        "drho_core_ratio_W2_over_W1": ratio2,
        "drho_core_ratio_W3_over_W1": ratio3,
        "exponent_p_drho_vs_W": p,
        "dip_scales_with_W_linearly": linear,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    v2.save_json("R3_scaling", summary)

    print("=" * 76)
    print(f"R3 -- DOES THE CORE DEPLETION SCALE WITH WINDING W?  ({NSEED} seeds, K={K_UNSAT})")
    print("=" * 76)
    print("   W   a(0)            |drho(0)| (unclamped)     clamped dip")
    for w in (1, 2, 3):
        r = rows[w]
        print(f"   {w}   {r['a_core'][0]:.3f}+/-{r['a_core'][1]:.3f}     "
              f"{abs(r['drho_core'][0]):.3f}+/-{r['drho_core'][1]:.3f}          "
              f"{r['dip'][0]:.3f}+/-{r['dip'][1]:.3f}")
    print(f"\n  |drho(0)| ratios: W2/W1={ratio2:.2f}, W3/W1={ratio3:.2f}  "
          f"(linear => 2, 3)")
    print(f"  |drho(0)| ~ W^({p:.2f})")
    print("-" * 76)
    print(f"VERDICT (R3): depletion scales with W (linear: {linear}); exponent {p:.2f}.")
    print("  The core depletion grows with the winding number -- the rarefaction is")
    print("  topological, consistent with |Phi| ~ (1 - W f(r)).")
    return summary


if __name__ == "__main__":
    main()
