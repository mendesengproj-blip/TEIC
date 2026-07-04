"""P2_numeric.py -- Effective causal density rho(r) around a mass, by counting.

BRIDGE investigation (independent of R1-R3 / e6-e11; nothing here modifies them).

What this measures
------------------
We sprinkle the 2D radial Schwarzschild slice in tortoise coordinates at *uniform
proper density* rho0 (exactly the generator used by R3 / e3 -- the metric enters
only as the proper-volume sprinkling weight Omega^2 = (1-2M/r); it is NEVER
square-rooted in the generator).  For a static observer at radius r we measure, BY
COUNTING ONLY, the proper time it assigns to a fixed coordinate-time interval dt:

    tau_meas(r) = sqrt(2 N / rho0)          (volume.tau_from_count, d=2)

This is R3's measurement.  The static-observer clock rate that emerges is

    (dtau/dt)(r) = tau_meas(r) / dt   ->   sqrt(1 - 2M/r)   (R3, PROVADO).

The EFFECTIVE CAUSAL DENSITY relevant to the TEIC<->DEV bridge is the number of
network events per unit of the observer's *proper time*, i.e. the inverse clock
rate (how many far-frame causal slices stream past the slow clock per unit of its
own proper time):

    rho_eff(r) / rho0  ==  dt / dtau   =   1 / (dtau/dt)   ->   1/sqrt(1-2M/r)
                                                            ~  1 + M/r  (weak field).

ANTI-CIRCULARITY.  G, GM/r, the potential Phi, and the redshift sqrt(1-2M/r) are
NEVER used to GENERATE anything here.  rho_eff is built purely from counted
tau_meas.  The closed forms sqrt(1-2M/r) and 1/sqrt(1-2M/r) appear ONLY in the
final comparison block (validation.py, COMPARISON ONLY), to score the result.

Verdict logic (P2 death criterion): if rho_eff/rho0 scales as 1 + c*(M/r) with
c ~ 1 -> P2 PASSES (rho(r) derived within CST/Schwarzschild).  Otherwise the
"effective density" does not have the bridge form and P2 fails.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval  # noqa: E402
from curved import rstar_of_r, sprinkle_schwarzschild  # noqa: E402
from repro import rng  # noqa: E402
from volume import tau_from_count  # noqa: E402
from validation import schwarzschild_redshift  # noqa: E402 (COMPARISON ONLY)

OUT = Path(__file__).resolve().parent

SEED = 31415926
M = 1.0
RHO = 4000.0
N_REAL = 60
RADII = np.array([3.0, 4.0, 6.0, 10.0, 20.0, 40.0, 80.0, 160.0])
DELTAS = np.array([0.8, 1.2, 1.6, 2.0])   # small coordinate-time separations


def measure_clock_rate(r_obs, g):
    """Static-observer dtau/dt at radius r_obs by COUNTING (R3 estimator)."""
    x0 = rstar_of_r(r_obs, M)
    taus = []
    for dt in DELTAS:
        t1, t2 = -dt / 2, dt / 2
        A = np.array([t1, x0]); B = np.array([t2, x0])
        pad = 0.05 * dt
        t_bounds = (t1 - pad, t2 + pad)
        rstar_bounds = (x0 - dt / 2 - pad, x0 + dt / 2 + pad)
        ns = [len(alexandrov_interval(
                  sprinkle_schwarzschild(RHO, M, t_bounds, rstar_bounds, g), A, B))
              for _ in range(N_REAL)]
        taus.append(tau_from_count(np.mean(ns), RHO, 2))
    taus = np.array(taus)
    # slope of tau_meas vs dt through the origin (least squares)
    return float(np.sum(DELTAS * taus) / np.sum(DELTAS ** 2))


def main():
    g = rng(SEED)

    clock_rate = np.array([measure_clock_rate(r, g) for r in RADII])  # dtau/dt
    rho_eff = 1.0 / clock_rate                                        # rho_eff/rho0

    # ---- comparison only (never fed back into a generator) ----
    gr_rate = schwarzschild_redshift(RADII, M)          # sqrt(1-2M/r)
    gr_rho = 1.0 / gr_rate                              # 1/sqrt(1-2M/r)
    x = M / RADII                                       # weak-field variable

    # consistency with R3: counted clock rate vs sqrt(1-2M/r)
    r3_corr = float(np.corrcoef(clock_rate, gr_rate)[0, 1])
    r3_max_err = float(np.max(np.abs(clock_rate - gr_rate) / gr_rate))

    # Primary test (P2 death criterion): does the counted rho_eff match the CST
    # prediction 1/sqrt(1-2M/r) across all radii?
    pred_corr = float(np.corrcoef(rho_eff, gr_rho)[0, 1])
    pred_max_err = float(np.max(np.abs(rho_eff - gr_rho) / gr_rho))

    # Weak-field leading coefficient.  1/sqrt(1-2x) = 1 + 1*x + 1.5*x^2 + ...,
    # so the per-point apparent slope (rho_eff-1)/x = 1 + 1.5 x + O(x^2) must
    # descend to 1 as r grows.  The strong-field points (x up to 0.33) carry the
    # full higher-order tail and confirm the EXACT form 1/sqrt(1-2M/r); they are
    # not used to read the leading slope.  We report the apparent slope at the two
    # largest radii to expose the trend -> 1.
    slope_per_point = (rho_eff - 1.0) / x
    c_far = float(slope_per_point[-1])          # largest r: closest to pure 1
    c_far2 = float(slope_per_point[-2])

    # P2 death criterion (prompt): does the count scale as the CST prediction
    # 1/sqrt(1-2M/r), with leading weak-field coefficient -> 1 ?
    passes = (r3_corr > 0.999 and pred_max_err < 0.03 and abs(c_far - 1.0) < 0.1)
    verdict = "PASSA" if passes else "FALHA"

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    rr = np.linspace(2.7, 41, 300)
    ax[0].plot(rr, 1.0 / schwarzschild_redshift(rr, M), "k-", lw=1.5,
               label=r"$1/\sqrt{1-2M/r}$ (CST/GR)")
    ax[0].plot(rr, 1.0 + M / rr, "0.6", ls="--", lw=1.0, label=r"$1+M/r$ (weak field)")
    ax[0].plot(RADII, rho_eff, "o", ms=7, label="counting estimate")
    ax[0].set_title(r"(P2) effective causal density $\rho_{\rm eff}(r)/\rho_0$")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$\rho_{\rm eff}/\rho_0$"); ax[0].legend()

    ax[1].plot(gr_rho, rho_eff, "o", ms=7)
    lim = [gr_rho.min() * 0.99, gr_rho.max() * 1.01]
    ax[1].plot(lim, lim, "k--", lw=1, label="y=x")
    ax[1].set_title(f"counting vs CST  (corr {pred_corr:.4f}, "
                    f"max err {pred_max_err:.1%})")
    ax[1].set_xlabel(r"$1/\sqrt{1-2M/r}$"); ax[1].set_ylabel("counting estimate")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "P2_numeric.png", dpi=130)

    summary = {
        "what": "rho_eff(r)/rho0 = 1/(dtau/dt), dtau/dt measured by counting (R3 estimator)",
        "M": M, "rho0": RHO, "n_real": N_REAL,
        "radii": RADII.tolist(),
        "clock_rate_counted": clock_rate.tolist(),
        "clock_rate_GR_sqrt(1-2M/r)": gr_rate.tolist(),
        "rho_eff_over_rho0_counted": rho_eff.tolist(),
        "rho_eff_over_rho0_CST_1/sqrt(1-2M/r)": gr_rho.tolist(),
        "R3_consistency_corr": r3_corr,
        "R3_consistency_max_rel_err": r3_max_err,
        "weakfield_apparent_slope_per_point": slope_per_point.tolist(),
        "weakfield_apparent_slope_largest_r": c_far,
        "weakfield_apparent_slope_2nd_largest_r": c_far2,
        "pure_prediction_leading_slope": 1.0,
        "rho_eff_corr": pred_corr,
        "rho_eff_max_rel_err": pred_max_err,
        "verdict": verdict,
        "seed": SEED,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "P2_numeric_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("P2 -- EFFECTIVE CAUSAL DENSITY rho_eff(r) BY COUNTING (Schwarzschild)")
    print("=" * 72)
    print("rho_eff/rho0 = 1/(dtau/dt);  dtau/dt counted (no sqrt in generator)")
    for r, cr, re_, gr in zip(RADII, clock_rate, rho_eff, gr_rho):
        print(f"  r={r:5.1f}:  dtau/dt(count)={cr:.4f}   "
              f"rho_eff/rho0={re_:.4f}   CST 1/sqrt={gr:.4f}")
    print("-" * 72)
    print(f"R3 consistency : clock-rate corr {r3_corr:.5f}, max err {r3_max_err:.2%}")
    print(f"vs CST 1/sqrt  : corr {pred_corr:.5f}, max rel err {pred_max_err:.2%}")
    print(f"weak-field lead: apparent slope (rho_eff-1)/(M/r) -> 1 as r grows")
    print(f"                 r={RADII[-2]:.0f}: {c_far2:.3f}   "
          f"r={RADII[-1]:.0f}: {c_far:.3f}   (pure leading = 1)")
    print(f"VERDICT (P2)   : {verdict}")
    return summary


if __name__ == "__main__":
    main()
