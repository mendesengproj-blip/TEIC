"""e2 -- R2: causal-diamond volume law and the dimension estimator.

Part 1 (analytic, sympy): derive the flat causal-diamond volume from first
principles by stacking spatial slices,
    d=2 : Vol = (1/2) tau^2
    d=4 : Vol = (pi/24) tau^4 .
No relativity is assumed -- only the light-cone geometry of the interval.

Part 2 (numeric): sprinkle at density rho, vary tau, and fit
    <N>(tau) = C * tau^p .
Expect p=2, C=rho/2 in 1+1D and p=4, C=rho*pi/24 in 1+3D.  The fitted exponent
IS the Myrheim-Meyer spacetime dimension, measured purely by counting.

Verdict: PROVADO / PARCIAL / NEGATIVO / INCONCLUSIVO.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval, sprinkle_box  # noqa: E402
from repro import FIGS, rng, save_run  # noqa: E402

SEED = 314159
RHO = {2: 50.0, 4: 50.0}
N_REAL = {2: 300, 4: 120}
TAUS = np.linspace(1.5, 5.0, 10)


def analytic_volumes():
    """Symbolically derive diamond volumes by integrating spatial slices."""
    t, tau, r = sp.symbols("t tau r", positive=True)
    half = tau / 2
    # slice radius is min(t, tau-t); integrate over the two halves and double.
    # d=2: spatial slice is an interval of length 2*radius
    vol2 = 2 * sp.integrate(2 * t, (t, 0, half))
    # d=4: spatial slice is a 3-ball of radius=radius, volume (4/3) pi r^3
    vol4 = 2 * sp.integrate(sp.Rational(4, 3) * sp.pi * t ** 3, (t, 0, half))
    return sp.simplify(vol2), sp.simplify(vol4)


def _bounds(tau, s):
    return [(0.0, tau)] + [(-tau / 2, tau / 2)] * s


def mean_count(tau, d, g):
    s = d - 1
    A = np.zeros(d)
    B = np.zeros(d); B[0] = tau
    ns = []
    for _ in range(N_REAL[d]):
        pts = sprinkle_box(RHO[d], _bounds(tau, s), g)
        ns.append(len(alexandrov_interval(pts, A, B)))
    return np.mean(ns)


def fit_powerlaw(taus, counts):
    """Fit log N = log C + p log tau; return (p, C)."""
    p, logC = np.polyfit(np.log(taus), np.log(counts), 1)
    return p, np.exp(logC)


def main():
    g = rng(SEED)
    vol2, vol4 = analytic_volumes()

    results = {}
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    for k, d in enumerate((2, 4)):
        counts = np.array([mean_count(tau, d, g) for tau in TAUS])
        p, C = fit_powerlaw(TAUS, counts)
        C_expected = RHO[d] * (0.5 if d == 2 else np.pi / 24)
        results[d] = {"exponent": float(p), "coef": float(C),
                      "exponent_expected": float(d),
                      "coef_expected": float(C_expected)}
        ax[k].loglog(TAUS, counts, "o", label="measured <N>")
        ax[k].loglog(TAUS, C * TAUS ** p, "-",
                     label=f"fit: p={p:.3f}, C={C:.3f}")
        ax[k].set_title(f"d={d}: expect p={d}, C={C_expected:.3f}")
        ax[k].set_xlabel(r"$\tau$"); ax[k].set_ylabel(r"$\langle N\rangle$"); ax[k].legend()
    fig.tight_layout()
    fig.savefig(FIGS / "e2_dimension_volume.png", dpi=130)

    ok = True
    for d in (2, 4):
        r = results[d]
        ok &= abs(r["exponent"] - d) < 0.05
        ok &= abs(r["coef"] / r["coef_expected"] - 1) < 0.05
    verdict = "PROVADO" if ok else "PARCIAL"

    summary = {"analytic_vol2": str(vol2), "analytic_vol4": str(vol4),
               "fits": results, "verdict": verdict}
    save_run("e2_dimension_volume", SEED,
             {"rho": RHO, "n_real": N_REAL, "taus": TAUS.tolist()},
             summary=summary)

    print("=" * 70)
    print("R2 -- VOLUME LAW AND DIMENSION ESTIMATOR")
    print("=" * 70)
    print(f"Analytic: Vol_2(tau) = {vol2}   Vol_4(tau) = {vol4}")
    for d in (2, 4):
        r = results[d]
        print(f"d={d}: exponent {r['exponent']:.3f} (expect {d}), "
              f"coef {r['coef']:.3f} (expect {r['coef_expected']:.3f})")
    print("-" * 70)
    print(f"VERDICT: {verdict}")
    return summary


if __name__ == "__main__":
    main()
