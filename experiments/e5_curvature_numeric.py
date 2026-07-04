"""e5 -- Task B: numeric curvature test (decides the chain-vs-volume question).

Task A (e4) proved analytically that the VOLUME estimator, inverted with the flat
law, deviates from the geodesic proper time as
    tau_vol/tau_geo = 1 - R tau^2/96 + ...      (Ricci-scalar convention).
The CHAIN estimator tracks the longest timelike geodesic; whether its normalisation
picks up its OWN curvature correction is an empirical question.  Here we measure the
curvature response of BOTH estimators by high-density sprinkling on 2D constant-
curvature backgrounds (de Sitter R>0 and anti-de Sitter R<0).

Generator stays bare: conformally-flat coordinates => 45-degree light cones; the
metric enters only as the proper-volume sprinkling density (curved.sprinkle_const_curv).
The geodesic proper time tau_geo between the tips is known in closed form
(curved.geodesic_tau_const_curv) and is the independent variable.

For each (R, tau_geo) we form, from the Alexandrov interval between the tips,
    tau_vol  = sqrt(2 N / rho)
    tau_chain = L / (c2 * sqrt(rho))            (c2 calibrated at R=0)
and fit the relative deviation  (tau_est/tau_geo - 1)  as a function of  R*tau_geo^2.
The leading slopes are the curvature coefficients:
    volume slope  -> compare with Task A's -1/96  (validation of e4),
    chain slope   -> the unknown; if != volume slope the formulations DIVERGE.

Verdict: PROVADO (divergence) / equivalence / INCONCLUSIVO (slopes within error of
each other or of zero).
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

from causal_core import alexandrov_interval  # noqa: E402
from chain import longest_chain_2d  # noqa: E402
from curved import geodesic_tau_const_curv, sprinkle_const_curv  # noqa: E402
from repro import FIGS, rng, save_run  # noqa: E402
from volume import tau_from_count  # noqa: E402

SEED = 1618033
RHO = 3000.0
N_REAL = 80
N_CALIB = 200
T_VALUES = np.array([3.0, 4.0, 5.0, 6.0])        # coordinate tip separations
R_VALUES = np.array([-0.10, -0.05, 0.0, 0.05, 0.10])  # Ricci scalar (dS and AdS)
T_CALIB = np.array([3.0, 4.0, 5.0, 6.0])         # flat-space chain calibration


def _measure(T, R, g):
    """Mean interval count <N> and mean longest-chain length <L> for tips +-T/2."""
    A = np.array([-T / 2, 0.0]); B = np.array([T / 2, 0.0])
    pad = 0.15
    t_bounds = (-T / 2 - pad, T / 2 + pad)
    x_bounds = (-T / 2 - pad, T / 2 + pad)
    Ns, Ls = [], []
    for _ in range(N_REAL):
        pts = sprinkle_const_curv(RHO, R, t_bounds, x_bounds, g)
        idx = alexandrov_interval(pts, A, B)
        sub = np.vstack([A, pts[idx], B])
        Ns.append(len(idx))
        Ls.append(longest_chain_2d(sub))
    return np.mean(Ns), np.mean(Ls)


def calibrate_c2(g):
    """Chain normalisation c2 such that L = c2 sqrt(rho) tau_geo at R=0."""
    ratios = []
    for T in T_CALIB:
        for _ in range(N_CALIB // len(T_CALIB)):
            A = np.array([-T / 2, 0.0]); B = np.array([T / 2, 0.0])
            pad = 0.15
            pts = sprinkle_const_curv(RHO, 0.0, (-T / 2 - pad, T / 2 + pad),
                                      (-T / 2 - pad, T / 2 + pad), g)
            idx = alexandrov_interval(pts, A, B)
            sub = np.vstack([A, pts[idx], B])
            L = longest_chain_2d(sub)
            ratios.append(L / (np.sqrt(RHO) * T))   # tau_geo = T at R=0
    return float(np.mean(ratios))


def main():
    g = rng(SEED)
    c2 = calibrate_c2(g)

    rows = []   # (R, tau_geo, x=R*tau^2, dev_vol, dev_chain)
    for R in R_VALUES:
        for T in T_VALUES:
            tau_geo = geodesic_tau_const_curv(T, R)
            N, L = _measure(T, R, g)
            tau_vol = tau_from_count(N, RHO, 2)
            tau_chain = L / (c2 * np.sqrt(RHO))
            rows.append((R, tau_geo, R * tau_geo ** 2,
                         tau_vol / tau_geo - 1.0, tau_chain / tau_geo - 1.0))
    rows = np.array(rows)
    xR = rows[:, 2]
    dev_vol = rows[:, 3]
    dev_chain = rows[:, 4]

    # Fit relative deviation = slope * (R tau^2) + quad*(R tau^2)^2
    def fit(dev):
        c = np.polyfit(xR, dev, 2)   # [quad, slope, intercept]
        return float(c[1]), float(c[0]), float(c[2])
    slope_vol, quad_vol, int_vol = fit(dev_vol)
    slope_chain, quad_chain, int_chain = fit(dev_chain)

    predicted_vol_slope = -1.0 / 96.0   # from Task A (e4)

    # rough uncertainty on slopes from residual scatter
    def slope_err(dev, slope, quad, intc):
        pred = quad * xR ** 2 + slope * xR + intc
        resid = dev - pred
        s = np.std(resid)
        sxx = np.sum((xR - xR.mean()) ** 2)
        return float(s / np.sqrt(sxx))
    err_vol = slope_err(dev_vol, slope_vol, quad_vol, int_vol)
    err_chain = slope_err(dev_chain, slope_chain, quad_chain, int_chain)

    sep = abs(slope_vol - slope_chain)
    sep_sigma = sep / np.hypot(err_vol, err_chain)

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(7.2, 5.2))
    xs = np.linspace(xR.min(), xR.max(), 100)
    ax.axhline(0, color="0.7", lw=0.8)
    ax.plot(xR, dev_vol, "o", color="tab:blue", label="volume estimator")
    ax.plot(xR, dev_chain, "s", color="tab:red", label="chain estimator")
    ax.plot(xs, quad_vol * xs ** 2 + slope_vol * xs + int_vol, "-", color="tab:blue",
            label=f"vol slope {slope_vol:+.4f} (A: {predicted_vol_slope:+.4f})")
    ax.plot(xs, quad_chain * xs ** 2 + slope_chain * xs + int_chain, "-", color="tab:red",
            label=f"chain slope {slope_chain:+.4f}")
    ax.plot(xs, predicted_vol_slope * xs, "k--", lw=1, label="Task A prediction")
    ax.set_xlabel(r"$R\,\tau^2$")
    ax.set_ylabel(r"$\tau_{\rm est}/\tau_{\rm geo} - 1$")
    ax.set_title("Curvature response of the two proper-time formulations")
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIGS / "e5_curvature_numeric.png", dpi=130)

    vol_matches_A = abs(slope_vol - predicted_vol_slope) < 3 * err_vol + 0.003
    diverge = sep_sigma > 3 and sep > 0.003
    if diverge:
        verdict = "PROVADO: chain and volume formulations DIVERGE in curved space"
    elif sep_sigma < 2:
        verdict = "EQUIVALENCIA/INCONCLUSIVO: slopes statistically indistinguishable"
    else:
        verdict = "PARCIAL: marginal separation"

    summary = {
        "c2_calibration": c2,
        "volume_slope_measured": slope_vol, "volume_slope_err": err_vol,
        "volume_slope_predicted_taskA": predicted_vol_slope,
        "chain_slope_measured": slope_chain, "chain_slope_err": err_chain,
        "slope_separation": sep, "separation_sigma": sep_sigma,
        "volume_matches_taskA": bool(vol_matches_A),
        "verdict": verdict,
    }
    save_run("e5_curvature_numeric", SEED,
             {"rho": RHO, "n_real": N_REAL, "T_values": T_VALUES.tolist(),
              "R_values": R_VALUES.tolist()},
             arrays={"R": rows[:, 0], "tau_geo": rows[:, 1], "Rtau2": xR,
                     "dev_vol": dev_vol, "dev_chain": dev_chain},
             summary=summary)

    print("=" * 70)
    print("TASK B -- NUMERIC CURVATURE TEST (decides chain vs volume)")
    print("=" * 70)
    print(f"chain calibration c2 = {c2:.4f}  (rho={RHO}, n_real={N_REAL})")
    print(f"volume slope : {slope_vol:+.5f} +/- {err_vol:.5f}   "
          f"(Task A predicts {predicted_vol_slope:+.5f})")
    print(f"chain  slope : {slope_chain:+.5f} +/- {err_chain:.5f}")
    print(f"separation   : {sep:.5f}  ({sep_sigma:.1f} sigma)")
    print(f"volume matches Task A: {vol_matches_A}")
    print("-" * 70)
    print(f"VERDICT: {verdict}")
    return summary


if __name__ == "__main__":
    main()
