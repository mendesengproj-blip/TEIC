"""C3_scale.py -- the DBI saturation scale X0 = (Dtheta/Dtau)^2_max from the network.

BRIDGE / COEFFICIENTS, task C3.  Independent of R1-R3 / e6-e11.  No SR/GR formula,
no fit to data; the DEV does not enter here at all.

Context.  The minimal action's saturated (non-linear) sector is the DBI-like term
rho*sqrt(1 - X/X0) found by the NL/DBI work: the square root is forced by the
light cone in field space.  Its scale X0 is the kinetic density at which the field
saturates.  The conjecture (BRIDGE_COEFFICIENTS.md, C3) is that X0 is the field-
space light cone: the largest |Dtheta/Dtau| the discrete network can represent.

On a single link, X = (Dtheta/Dtau)^2.  Dtheta across a link is bounded by the
field's coherent variation Dtheta_max (a property of the field, not the geometry);
Dtau is bounded BELOW by the smallest causal link the network supports, Dtau_min.
Hence

    X0 = (Dtheta_max / Dtau_min)^2          (the field-space light cone)

C3 MEASURES Dtau_min(rho).  NOTE the subtlety this measurement exposes: the
smallest causal link is NOT the lattice-discreteness length rho^{-1/D}.  The region
{0 < Dt^2 - Dx^2 < eps} is a thin sliver hugging the light cone whose box measure
vanishes LINEARLY in eps in EVERY dimension, so with N ~ rho events the minimum
proper time scales as

    Dtau_min ~ rho^{-1/2}      (dimension-INDEPENDENT; light-cone sliver, not rho^{-1/D})

and therefore  X0 ∝ rho^{+1}  in both 1+1D and 3+1D.  The field-dependent factor
Dtheta_max is left explicit and honest.  The exponent p in X0 ∝ rho^p is what is
fit below; p ~ 1 (UV / granularity origin) is the prediction, NOT the cosmological
2/D scaling first guessed.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from causal_core import sprinkle_box           # noqa: E402

OUT = Path(__file__).resolve().parent


def nearest_future_dtau(pts, bounds, margin_frac=0.25):
    """For each BULK event, the proper time Dtau to its nearest future neighbour.

    The nearest future timelike neighbour is ALWAYS a covering relation (no event
    can sit causally between an event and its proper-time-closest future event),
    so this is the granularity end of the link Dtau distribution -- the discreteness
    scale -- obtained in O(n_bulk * n) without the O(n^3) covering-relation matmul.
    """
    pts = np.asarray(pts, dtype=float)
    bounds = np.asarray(bounds, dtype=float)
    D = pts.shape[1]
    lo = bounds[:, 0] + margin_frac * (bounds[:, 1] - bounds[:, 0])
    hi = bounds[:, 1] - margin_frac * (bounds[:, 1] - bounds[:, 0])
    bulk = np.nonzero(np.all((pts >= lo) & (pts <= hi), axis=1))[0]
    out = []
    for idx in bulk:
        p = pts[idx]
        d = pts - p
        dt = d[:, 0]
        dx2 = np.sum(d[:, 1:] ** 2, axis=1) if D > 1 else np.zeros(len(pts))
        s2 = dt * dt - dx2
        fut = (dt > 0) & (s2 > 0)
        if not np.any(fut):
            continue
        out.append(np.sqrt(s2[fut].min()))
    return np.asarray(out)


def link_dtau_scale(D, rho, extent, n_real, seed0):
    """Characteristic nearest-future link proper-time scales at a given density."""
    bounds = [[0.0, extent]] * D
    dtaus = []
    for s in range(n_real):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, bounds, rng)
        if len(pts) < 5:
            continue
        dtaus.append(nearest_future_dtau(pts, bounds))
    dtaus = np.concatenate(dtaus)
    return {
        "rho": rho,
        "n_links": int(len(dtaus)),
        "dtau_p05": float(np.percentile(dtaus, 5)),
        "dtau_p25": float(np.percentile(dtaus, 25)),
        "dtau_median": float(np.percentile(dtaus, 50)),
        "dtau_mean": float(dtaus.mean()),
    }


def fit_powerlaw(rhos, scales):
    """Fit log(scale) = a + p*log(rho); return exponent p and intercept a."""
    lr = np.log(np.asarray(rhos))
    ls = np.log(np.asarray(scales))
    p, a = np.polyfit(lr, ls, 1)
    pred = a + p * lr
    ss_res = np.sum((ls - pred) ** 2)
    ss_tot = np.sum((ls - ls.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return float(p), float(a), float(r2)


def run_dim(D, rhos, extent, n_real, seed0):
    rows = [link_dtau_scale(D, r, extent, n_real, seed0 + 100 * k)
            for k, r in enumerate(rhos)]
    out = {"D": D, "rhos": list(rhos), "rows": rows}
    for key, name in [("dtau_p05", "p05"), ("dtau_median", "median"),
                      ("dtau_mean", "mean")]:
        scales = [r[key] for r in rows]
        p, a, r2 = fit_powerlaw(rhos, scales)
        out[f"fit_{name}"] = {"q_exponent_dtau": p, "intercept": a, "r2": r2,
                              "X0_exponent_p_eq_-2q": -2 * p}
    out["theory_q_lightcone_sliver"] = -0.5      # rho^{-1/2}, dimension-independent
    out["theory_X0_exponent"] = 1.0              # X0 ∝ rho^{+1}
    out["naive_q_eq_-1overD"] = -1.0 / D         # the lattice guess the data REJECTS
    return out


def main():
    results = {}
    # 1+1D: theory q = -1/2  (Dtau_min ~ rho^{-1/2}); X0 ∝ rho^{1}
    results["d2"] = run_dim(2, rhos=[80, 160, 320, 640, 1280], extent=5.0,
                            n_real=16, seed0=10000)
    # 3+1D: theory q = -1/2 (Dtau_min ~ rho^{-1/2}, DIMENSION-INDEPENDENT light-cone
    # sliver -- see module docstring); X0 ∝ rho^{1}.  [Corrected: an earlier comment here
    # read q=-1/4, X0∝rho^{1/2}; the 20-seed audit (AB1) measured p=1.00+/-0.02 in 3+1D,
    # confirming p=1 in BOTH dimensions.  The recorded theory_X0_exponent=1.0 was always
    # correct; only this comment was wrong.]
    results["d4"] = run_dim(4, rhos=[4, 8, 16, 32, 64], extent=5.0,
                            n_real=12, seed0=20000)
    results["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "C3_scale_data.json").write_text(json.dumps(results, indent=2))

    print("=" * 72)
    print("C3 -- DBI SCALE X0 = (Dtheta/Dtau)^2_max ;  link Dtau granularity vs rho")
    print("=" * 72)
    for dk, lab in [("d2", "1+1D"), ("d4", "3+1D")]:
        r = results[dk]
        print(f"\n{lab}:  theory (light-cone sliver) Dtau_min ~ rho^({r['theory_q_lightcone_sliver']:.3f})"
              f"  ->  X0 ~ rho^({r['theory_X0_exponent']:.3f})  "
              f"[naive lattice rho^({r['naive_q_eq_-1overD']:.3f}) REJECTED]")
        print("   rho     p05      median     mean")
        for row in r["rows"]:
            print(f"  {row['rho']:5.0f}  {row['dtau_p05']:7.4f}  "
                  f"{row['dtau_median']:8.4f}  {row['dtau_mean']:8.4f}")
        for name in ("p05", "median", "mean"):
            f = r[f"fit_{name}"]
            print(f"   fit[{name:>6}]: Dtau ~ rho^({f['q_exponent_dtau']:+.3f}) "
                  f"(r2={f['r2']:.4f})  =>  X0 ~ rho^({f['X0_exponent_p_eq_-2q']:+.3f})")
    print("\n(written C3_scale_data.json)")
    return results


if __name__ == "__main__":
    main()
