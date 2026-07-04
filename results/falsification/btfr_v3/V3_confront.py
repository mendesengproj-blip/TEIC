"""V3_confront.py -- FALSIFICATION_BTFR_V3: published a0(z) (MUSE-DARK III,
Ciocan et al. 2026, A&A 708 A112, arXiv:2604.22613) vs the pre-registered
prediction Delta log v = (1/4) log10[H(z)/H0]  (i.e. a0 ~ H(z)).

Deterministic arithmetic on PUBLISHED numbers -- no simulation, no free
parameter, no seed. H(z) flat LCDM, Om = 0.30 +/- 0.02 (H0 cancels).

Decision rules R1-R4 pre-registered in FALSIFICATION_BTFR_V3.md. The anchor
matrix is declared there; A3 (the paper's own a0(0) from the same MCMC as
a0|z~1) is CORRELATED with the numerator -- reported as a consistency note,
not an independent tension. z_eff of the full-sample a0|z~1 is bracketed
[0.85, 1.0] (median of 0.33<z<1.44, mass-complete; the paper labels it z~1).
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
OM = 0.30
DOM = 0.02

# ---- published numbers (sources in FALSIFICATION_BTFR_V3.md) ----------------
A0_Z1 = (2.38, 0.11)            # MUSE-DARK III full sample 0.33<z<1.44 (sym. err)
A0_BINS = {"low~0.5": 1.99, "high~1.3": 2.71}      # binned endpoints (Fig. 3)
A1_FIT = (1.59, 0.105)          # linear coefficient a0(z)=a0(0)+a1 z
A0_OWN = (1.00, 0.04)           # the paper's own a0(0) (same MCMC -> correlated)
ANCHORS = {
    "A1_SPARC_McGaugh16": (1.20, 0.26, 0.0),       # (a0, err, z_anchor)
    "A2_MIGHTEE_Varasteanu25": (1.69, 0.13, 0.04),
    "A3_own_fit_CORRELATED": (1.00, 0.04, 0.0),
}
Z_EFF = [0.85, 1.00]            # bracket for the full-sample effective z


def E(z, om=OM):
    return np.sqrt(om * (1 + z) ** 3 + (1 - om))


def pred_dlogv(z_hi, z_lo=0.0, om=OM):
    return 0.25 * np.log10(E(z_hi, om) / E(z_lo, om))


def slog_err(val, err):
    """sigma of log10(val) from symmetric absolute err."""
    return err / (val * np.log(10.0))


def main():
    out = {"published": {"a0_z1": A0_Z1, "a1_fit": A1_FIT, "a0_own": A0_OWN,
                         "anchors": ANCHORS, "bins": A0_BINS, "z_eff": Z_EFF}}

    # R3 -- amplitude: obs Delta log v vs predicted, per anchor x z_eff
    r3 = {}
    for name, (a_loc, e_loc, z_loc) in ANCHORS.items():
        obs = 0.25 * np.log10(A0_Z1[0] / a_loc)
        sob = 0.25 * np.sqrt(slog_err(*A0_Z1) ** 2 + slog_err(a_loc, e_loc) ** 2)
        rows = {}
        for zf in Z_EFF:
            pred = pred_dlogv(zf, z_loc)
            pred_lo = pred_dlogv(zf, z_loc, OM - DOM)
            pred_hi = pred_dlogv(zf, z_loc, OM + DOM)
            rows[zf] = {"pred": float(pred),
                        "pred_om_band": [float(pred_lo), float(pred_hi)],
                        "deviation_sigma": float((obs - pred) / sob)}
        r3[name] = {"obs_dlogv": float(obs), "obs_err": float(sob), "vs": rows}
    out["R3_amplitude"] = r3
    indep = ["A1_SPARC_McGaugh16", "A2_MIGHTEE_Varasteanu25"]
    spread = np.std([r3[k]["obs_dlogv"] for k in r3], ddof=1)
    out["R3_anchor_spread_dex"] = float(spread)
    out["R3_consistent_2sigma_independent_anchor"] = bool(any(
        abs(r3[k]["vs"][zf]["deviation_sigma"]) < 2.0
        for k in indep for zf in Z_EFF))

    # R4 -- form: measured a1 vs a0~H secant slope per anchor
    r4 = {}
    for name, (a_loc, e_loc, z_loc) in ANCHORS.items():
        a1_H = a_loc * (E(1.0) - E(z_loc)) / (1.0 - z_loc)
        r4[name] = {"a1_H_secant_0_to_1": float(a1_H),
                    "ratio_measured_over_H": float(A1_FIT[0] / a1_H),
                    "tension_sigma_stat": float(
                        (A1_FIT[0] - a1_H)
                        / np.hypot(A1_FIT[1], e_loc * (E(1.0) - E(z_loc))))}
    out["R4_form"] = r4
    # form sanity: linear fit extrapolated to z=1.44 vs measured top bin;
    # and a0~H from SPARC anchor at z=1.44 vs the same bin
    z_top = 1.3
    out["R4_sanity"] = {
        "linear_fit_at_1.44": float(A0_OWN[0] + A1_FIT[0] * 1.44),
        "top_bin_measured(z~1.3)": A0_BINS["high~1.3"],
        "a0H_SPARC_at_1.3": float(ANCHORS["A1_SPARC_McGaugh16"][0] * E(z_top)),
    }

    # R2 -- direction (published, restated): a1 > 0 at a1/err sigma
    out["R2_direction_sigma"] = float(A1_FIT[0] / A1_FIT[1])
    # R1 -- kill executability: no qualifying z>=2 sample published (jun/2026)
    out["R1_kill"] = {"qualifying_sample_exists": False, "triggered": False,
                      "note": "F1 criterion unchanged; sign of available "
                              "right-regime signal is OPPOSITE to death "
                              "(dlogv > 0)"}

    out["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                    "numpy": np.__version__, "Om": [OM, DOM],
                    "deterministic": True}
    (HERE / "V3_confront_data.json").write_text(json.dumps(out, indent=2))

    # ---- figure -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
    zz = np.linspace(0, 1.6, 200)
    for a_loc, lab, c in [(1.20, "a₀∝H (âncora SPARC 1.20)", "tab:red"),
                          (1.69, "a₀∝H (âncora MIGHTEE 1.69)", "tab:green"),
                          (1.00, "a₀∝H (âncora própria 1.00)", "tab:gray")]:
        ax1.plot(zz, a_loc * E(zz), c=c, lw=1.4, label=lab)
    ax1.plot(zz, A0_OWN[0] + A1_FIT[0] * zz, "k--", lw=1.6,
             label="fit linear Ciocan+26")
    ax1.errorbar([0.925], [A0_Z1[0]], yerr=[[A0_Z1[1]]], xerr=[[0.075]],
                 fmt="o", color="tab:purple", ms=7, capsize=3,
                 label=r"$a_0|_{z\sim1}$ = 2.38")
    ax1.scatter([0.5, 1.3], [A0_BINS["low~0.5"], A0_BINS["high~1.3"]],
                marker="s", color="tab:blue", zorder=5, label="bins (extremos)")
    ax1.errorbar([0.0], [1.20], yerr=[[0.26]], fmt="*", ms=12, color="tab:red")
    ax1.errorbar([0.04], [1.69], yerr=[[0.13]], fmt="*", ms=12, color="tab:green")
    ax1.set_xlabel("z"); ax1.set_ylabel(r"$a_0$ [$10^{-10}$ m s$^{-2}$]")
    ax1.set_title("a₀(z): medido vs a₀∝H(z)"); ax1.legend(fontsize=7)

    names = list(r3.keys())
    obs = [r3[k]["obs_dlogv"] for k in names]
    err = [r3[k]["obs_err"] for k in names]
    ax2.errorbar(range(len(names)), obs, yerr=err, fmt="o", ms=7, capsize=4,
                 color="tab:purple", label="observado (z~1)")
    band = [pred_dlogv(Z_EFF[0]), pred_dlogv(Z_EFF[1])]
    ax2.axhspan(band[0], band[1], color="tab:orange", alpha=0.35,
                label=f"previsto ¼log[H/H₀], z_eff∈[{Z_EFF[0]},{Z_EFF[1]}]")
    ax2.axhline(0.0, color="k", lw=1.2, label="ΛCDM (=0)")
    ax2.set_xticks(range(len(names)))
    ax2.set_xticklabels(["SPARC", "MIGHTEE", "própria\n(correl.)"], fontsize=8)
    ax2.set_ylabel(r"$\Delta\log v$ a $M_b$ fixa (dex)")
    ax2.set_title("amplitude: a previsão dentro do leque de âncoras")
    ax2.legend(fontsize=7)
    fig.tight_layout()
    fig.savefig(HERE / "V3_confront.png", dpi=150)

    print(json.dumps({k: out[k] for k in
                      ["R1_kill", "R2_direction_sigma", "R3_amplitude",
                       "R3_anchor_spread_dex",
                       "R3_consistent_2sigma_independent_anchor",
                       "R4_form", "R4_sanity"]}, indent=2))


if __name__ == "__main__":
    main()
