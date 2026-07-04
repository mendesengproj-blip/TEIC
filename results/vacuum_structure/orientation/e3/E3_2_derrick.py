"""E3_2_derrick.py -- Derrick's virial theorem on the causal lattice.

Charter E3-2.  Derrick's criterion: a static texture is stable only if its energy
E(lambda) under a scale transform n -> n((x-c)/lambda + c) has an INTERIOR
minimum at lambda* ~ 1 (energy rises for BOTH compression lambda<1 and dilation
lambda>1).  A monotone E(lambda) means Derrick is active and the defect is not a
soliton.

Three measurements:

  D1  E(lambda) of the hedgehog, FLAT metric, refined at L = 32, 48, 64.  The
      continuum O(3) hedgehog in 3D is scale-MARGINAL (E independent of lambda);
      the lattice can only add a UV wall.  We locate lambda* and test whether the
      minimum is interior (two-sided) or just a compression wall.

  D2  The artefact-free Derrick scaling: E(hedgehog) vs L.  For a scale-marginal
      texture E grows LINEARLY with the box (E ~ a L, no intrinsic length); a
      genuine soliton would saturate to a finite E.  Linear fit => marginal.

  D3  Curvature test (charter mechanism 2): repeat E(lambda) with a radial weight
      w(x) = 1 + alpha/r (COMPARISON-ONLY proxy for a curved metric theta~M/r
      sourced by the defect).  If curvature turns the monotone/marginal curve
      into one with an interior minimum, mechanism 2 is confirmed.

Anti-circularity: no stabilising term is added to the generator; w is an explicit
labelled proxy probed only here.  Derrick is scored exactly as the textbook test.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e3_core as e3  # noqa: E402

OUT = Path(__file__).resolve().parent
LAMBDAS = np.array([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.85, 1.0, 1.2, 1.5,
                    2.0, 3.0, 5.0, 8.0, 10.0])
REFINE_L = [32, 48, 64]
ALPHAS = [3.0, 6.0, 12.0]


def interior_minimum(lams, E, margin=0.05):
    """Return (has_interior_min, lambda_star, left_rise, right_rise).  A genuine
    CONFINING (soliton) minimum requires E to rise by >margin on BOTH the
    compression (lambda<1) and dilation (lambda>1) sides.  A pure UV wall (E rises
    only for lambda<1, flat for lambda>1) is the scale-MARGINAL signature and is
    NOT an interior minimum."""
    j = int(np.argmin(E))
    lam_star = float(lams[j])
    emin = E[j]
    left = (E[0] - emin) / emin
    right = (E[-1] - emin) / emin
    has = (j != 0) and (j != len(E) - 1) and (left > margin) and (right > margin)
    return has, lam_star, float(left), float(right)


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3-2 -- Derrick virial on the lattice (E(lambda), refinement, curvature)")
    print("=" * 72)

    # ---- D1: E(lambda) flat metric, refined ---------------------------- #
    d1 = {}
    print("  D1  E(lambda), flat metric:")
    for L in REFINE_L:
        nh = e3.hedgehog(L, +1)
        E, B = e3.derrick_curve(nh, LAMBDAS)
        E = E / E[np.argmin(np.abs(LAMBDAS - 1.0))]     # normalise to E(1)=1
        has_int, lstar, lr, rr = interior_minimum(LAMBDAS, E)
        d1[L] = {"E_over_E1": E.tolist(), "B": B.tolist(),
                 "interior_min": bool(has_int), "lambda_star": lstar,
                 "left_rise": lr, "right_rise": rr}
        print(f"      L={L}: lambda*={lstar:.2f}  interior_min={has_int}  "
              f"compress_rise(L)={lr:+.2f}  dilate_rise(R)={rr:+.2f}")

    # ---- D2: E vs L scaling (artefact-free) ---------------------------- #
    print("  D2  E(hedgehog) vs L (marginal <=> linear):")
    Ls = [16, 24, 32, 48, 64, 80]
    EL = [e3.gradient_energy(e3.hedgehog(L, +1)) for L in Ls]
    a, b = np.polyfit(Ls, EL, 1)
    yhat = a * np.array(Ls) + b
    r2 = 1 - np.sum((np.array(EL) - yhat) ** 2) / np.sum((np.array(EL) - np.mean(EL)) ** 2)
    # also fit a saturating form E = Einf*(1 - c/L)? compare: linear R^2 near 1 => marginal
    print(f"      E = {a:.3f}*L + {b:.1f}   R^2(linear)={r2:.5f}  "
          f"(R^2~1 => scale-marginal, E grows with box)")
    d2 = {"L": Ls, "E": EL, "slope": float(a), "intercept": float(b),
          "r2_linear": float(r2), "marginal": bool(r2 > 0.999)}

    # ---- D3: curvature weight ------------------------------------------ #
    print("  D3  E(lambda) with curvature weight w=1+alpha/r:")
    L = 48
    nh = e3.hedgehog(L, +1)
    d3 = {}
    for alpha in ALPHAS:
        w = e3.radial_weight(L, alpha=alpha)
        E, _ = e3.derrick_curve(nh, LAMBDAS, weight=w)
        E = E / E[np.argmin(np.abs(LAMBDAS - 1.0))]
        has_int, lstar, lr, rr = interior_minimum(LAMBDAS, E)
        d3[alpha] = {"E_over_E1": E.tolist(), "interior_min": bool(has_int),
                     "lambda_star": lstar, "left_rise": lr, "right_rise": rr}
        print(f"      alpha={alpha:5.1f}: lambda*={lstar:.2f}  interior_min={has_int}"
              f"  compress_rise={lr:+.2f}  dilate_rise={rr:+.2f}")

    flat_has_min = any(d1[L]["interior_min"] for L in REFINE_L)
    curv_has_min = any(d3[a]["interior_min"] for a in ALPHAS)
    curvature_changes = curv_has_min and not flat_has_min

    print("-" * 72)
    print(f"  flat metric interior minimum:      {flat_has_min}")
    print(f"  curvature induces interior minimum:{curv_has_min}  "
          f"(changes result: {curvature_changes})")
    print(f"  E vs L marginal (linear):          {d2['marginal']} "
          f"(slope={d2['slope']:.2f})")
    print("=" * 72)

    payload = {"D1_flat": d1, "D2_scaling": d2, "D3_curvature": d3,
               "lambdas": LAMBDAS.tolist(), "alphas": ALPHAS,
               "flat_interior_min": bool(flat_has_min),
               "curvature_interior_min": bool(curv_has_min),
               "curvature_changes_result": bool(curvature_changes),
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E3_2_derrick.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3_2_derrick.json'}  ({payload['runtime_s']:.0f}s)")

    # ---- figure -------------------------------------------------------- #
    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    ax = axes[0]
    for L in REFINE_L:
        ax.plot(LAMBDAS, d1[L]["E_over_E1"], "o-", ms=3, label=f"L={L}")
    ax.axvline(1, color="k", ls=":", lw=0.6)
    ax.set_xscale("log"); ax.set_xlabel("scale factor lambda")
    ax.set_ylabel("E(lambda)/E(1)")
    ax.set_title("D1: Derrick curve (flat)\nwall at lambda<1, flat for lambda>1 "
                 "= marginal")
    ax.legend(fontsize=8); ax.grid(alpha=0.25)

    ax = axes[1]
    ax.plot(Ls, EL, "ko-", ms=4)
    ax.plot(Ls, yhat, "r--", lw=1, label=f"E={a:.2f}L{b:+.1f} (R2={r2:.4f})")
    ax.set_xlabel("lattice size L"); ax.set_ylabel("E(hedgehog)")
    ax.set_title("D2: E ~ L (linear) => scale-marginal,\nno intrinsic soliton size")
    ax.legend(fontsize=8); ax.grid(alpha=0.25)

    ax = axes[2]
    for alpha in ALPHAS:
        ax.plot(LAMBDAS, d3[alpha]["E_over_E1"], "o-", ms=3, label=f"alpha={alpha:g}")
    ax.axvline(1, color="k", ls=":", lw=0.6)
    ax.set_xscale("log"); ax.set_xlabel("scale factor lambda")
    ax.set_ylabel("E(lambda)/E(1)")
    ax.set_title("D3: with curvature weight w=1+alpha/r\n(interior minimum?)")
    ax.legend(fontsize=8); ax.grid(alpha=0.25)
    fig.suptitle("E3-2: Derrick virial test for the hedgehog defect", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3_2_derrick.png", dpi=130)
    print(f"saved {OUT/'E3_2_derrick.png'}")


if __name__ == "__main__":
    main()
