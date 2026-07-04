"""e1 -- R1: time dilation (Special Relativity) emerges from causal counting.

Two complementary tests, both on the bare causal network (no relativistic formula
in the generator):

PANEL A -- Dilation.  Events A=(0,0), B=(T, beta*T): a clock moving at velocity beta
for coordinate time T.  Measure proper time from the Alexandrov interval A<x<B by
(i) the longest causal chain L and (ii) the volume estimator sqrt(2N/rho).  Both
should follow the invariant tau(beta)/tau(0)=sqrt(1-beta^2).

PANEL B -- Lorentz invariance (the decisive isotropy test).  Hold the INVARIANT
proper time tau0 fixed and vary the boost via rapidity phi: B=(tau0 cosh phi,
tau0 sinh phi), so the interval (0,0)->B always has invariant proper time tau0
(hyperbolic identity cosh^2-sinh^2=1 -- pure geometry, no dilation formula).  A
Lorentz-invariant counting must give a CONSTANT count; a random Poisson network
does (Lorentz-invariant in distribution), a regular LATTICE does not -- its count
swings with direction.  This is the clean way the lattice "fails".

sqrt(1-beta^2) is imported from validation.py for COMPARISON only.

Verdict: PROVADO / PARCIAL / NEGATIVO / INCONCLUSIVO.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval, lattice_box, sprinkle_box  # noqa: E402
from chain import longest_chain_2d  # noqa: E402
from repro import FIGS, rng, save_run  # noqa: E402
from validation import lorentz_proper_time_ratio  # noqa: E402 (COMPARISON ONLY)
from volume import tau_from_count  # noqa: E402

SEED = 20240601
T = 10.0
RHO = 6.0
N_REAL = 250
BETAS = np.linspace(0.0, 0.9, 19)

# Panel B: fixed invariant proper time, boost parametrised by rapidity.
TAU0 = 6.0
RAPIDITIES = np.linspace(0.0, 3.0, 16)   # beta = tanh(phi) up to ~0.995


def _bounds(A, B, pad=1.0):
    t0, t1 = sorted([A[0], B[0]])
    cx = 0.5 * (A[1] + B[1])
    half = 0.5 * abs(B[0] - A[0]) + abs(B[1] - A[1]) + pad
    return [(t0 - pad, t1 + pad), (cx - half, cx + half)]


def _interval(pts, A, B):
    idx = alexandrov_interval(pts, A, B)
    return np.vstack([A, pts[idx], B]), len(idx)


# ---- Panel A: dilation vs beta -------------------------------------------- #
def panelA(g):
    chain_p, count_p = [], []
    for b in BETAS:
        A, B = np.array([0.0, 0.0]), np.array([T, b * T])
        Ls, Ns = [], []
        for _ in range(N_REAL):
            pts = sprinkle_box(RHO, _bounds(A, B), g)
            sub, n = _interval(pts, A, B)
            Ls.append(longest_chain_2d(sub))
            Ns.append(n)
        chain_p.append(np.mean(Ls))
        count_p.append(np.mean(Ns))
    return np.array(chain_p, float), np.array(count_p, float)


# ---- Panel B: Lorentz invariance at fixed tau0 ---------------------------- #
def panelB(g):
    mean_p, cv_lat, betas = [], [], []
    lat_counts = []
    for phi in RAPIDITIES:
        A = np.array([0.0, 0.0])
        B = np.array([TAU0 * np.cosh(phi), TAU0 * np.sinh(phi)])  # invariant tau0
        betas.append(np.tanh(phi))
        # Poisson: average count (mean is the Lorentz invariant rho*tau0^2/2)
        ns = []
        for _ in range(N_REAL):
            pts = sprinkle_box(RHO, _bounds(A, B), g)
            _, n = _interval(pts, A, B)
            ns.append(n)
        mean_p.append(np.mean(ns))
        # Lattice: deterministic count
        spacing = RHO ** -0.5
        pts = lattice_box(spacing, _bounds(A, B))
        _, nlat = _interval(pts, A, B)
        lat_counts.append(nlat)
    return np.array(betas), np.array(mean_p, float), np.array(lat_counts, float)


def main():
    g = rng(SEED)
    chain_p, count_p = panelA(g)
    betasB, count_p_fixed, count_lat_fixed = panelB(g)

    ref = lorentz_proper_time_ratio(BETAS)  # comparison only
    chain_p_n = chain_p / chain_p[0]
    tau_vol_p = tau_from_count(count_p, RHO, 2)
    tau_vol_p_n = tau_vol_p / tau_vol_p[0]

    corr = lambda a: float(np.corrcoef(a, ref)[0, 1])
    c_chain = corr(chain_p_n)
    c_vol = corr(tau_vol_p_n)
    dev_chain = float(np.mean(np.abs(chain_p_n - ref)))
    dev_vol = float(np.mean(np.abs(tau_vol_p_n - ref)))

    # Invariance: spread of the count at fixed tau0 (coefficient of variation).
    expected_count = RHO * 0.5 * TAU0 ** 2
    cv_poisson = float(np.std(count_p_fixed) / np.mean(count_p_fixed))
    cv_lattice = float(np.std(count_lat_fixed) / np.mean(count_lat_fixed))

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    bb = np.linspace(0, 0.9, 200)
    ax[0].plot(bb, lorentz_proper_time_ratio(bb), "k-", lw=1.5, label=r"$\sqrt{1-\beta^2}$ (SR)")
    ax[0].plot(BETAS, chain_p_n, "o", ms=5, label=f"chain (corr {c_chain:.4f})")
    ax[0].plot(BETAS, tau_vol_p_n, "s", ms=4, mfc="none", label=f"volume (corr {c_vol:.4f})")
    ax[0].set_title("(A) Random network: dilation emerges")
    ax[0].set_xlabel(r"$\beta$"); ax[0].set_ylabel(r"$\tau(\beta)/\tau(0)$"); ax[0].legend()

    ax[1].axhline(expected_count, color="k", ls="--", lw=1, label=r"invariant $\rho\,\tau_0^2/2$")
    ax[1].plot(betasB, count_p_fixed, "o-", label=f"Poisson (CV {cv_poisson:.1%})")
    ax[1].plot(betasB, count_lat_fixed, "^-", color="crimson", label=f"lattice (CV {cv_lattice:.0%})")
    ax[1].set_title(r"(B) Fixed invariant $\tau_0$: Lorentz invariance")
    ax[1].set_xlabel(r"$\beta=\tanh\phi$"); ax[1].set_ylabel("count in interval"); ax[1].legend()
    fig.tight_layout()
    fig.savefig(FIGS / "e1_special_relativity.png", dpi=130)

    poisson_dilation_ok = c_chain > 0.99 and c_vol > 0.99 and dev_chain < 0.03
    lattice_breaks = cv_lattice > 5 * cv_poisson
    verdict = "PROVADO" if (poisson_dilation_ok and lattice_breaks) else "PARCIAL"

    summary = {
        "corr_chain": c_chain, "corr_volume": c_vol,
        "mean_abs_dev_chain": dev_chain, "mean_abs_dev_volume": dev_vol,
        "fixed_tau_cv_poisson": cv_poisson, "fixed_tau_cv_lattice": cv_lattice,
        "expected_fixed_count": expected_count, "verdict": verdict,
    }
    save_run("e1_special_relativity", SEED,
             {"T": T, "rho": RHO, "n_real": N_REAL, "betas": BETAS.tolist(),
              "tau0": TAU0, "rapidities": RAPIDITIES.tolist()},
             arrays={"betas": BETAS, "chain_poisson": chain_p, "count_poisson": count_p,
                     "betasB": betasB, "count_p_fixed": count_p_fixed,
                     "count_lat_fixed": count_lat_fixed, "ref": ref},
             summary=summary)

    print("=" * 70)
    print("R1 -- EMERGENCE OF SPECIAL RELATIVITY")
    print("=" * 70)
    print("(A) Dilation vs sqrt(1-beta^2):")
    print(f"    chain : corr={c_chain:.4f}  mean|dev|={dev_chain:.3%}")
    print(f"    volume: corr={c_vol:.4f}  mean|dev|={dev_vol:.3%}")
    print("(B) Lorentz invariance at fixed invariant proper time tau0=%.1f:" % TAU0)
    print(f"    expected count = rho*tau0^2/2 = {expected_count:.1f}")
    print(f"    Poisson count CV = {cv_poisson:.1%}  (invariant)")
    print(f"    lattice count CV = {cv_lattice:.0%}  (direction-dependent -> breaks SR)")
    print("-" * 70)
    print(f"VERDICT: {verdict}")
    return summary


if __name__ == "__main__":
    main()
