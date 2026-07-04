"""Summary figure for BARYON_QUANTITATIVE (gap #12).

Left : the FR-projected rotor tower E_j vs j(j+1) (N, Delta, j=5/2) with the
       (2j+1)^2 degeneracies; the pure-number slope is the rigid-rotor law.
Right: parameter-free predictions vs ANW vs experiment (mu_p/mu_n, isoscalar
       radius, g_A) and the calibrated coupling e.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent


def load(n):
    return json.loads((HERE / f"{n}.json").read_text())


def main():
    bq1, bq3, bq4 = load("BQ1_tower"), load("BQ3_calibration"), load("BQ4_moments")
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.4))

    # --- left: rotor tower ---
    jjp1 = np.array(bq1["j_j_plus_1"])
    E = np.array(bq1["FR_level_energies"])
    deg = bq1["FR_tower_degeneracies"]
    labels = ["N (j=½)", "Δ (j=3/2)", "j=5/2"]
    xline = np.linspace(0, jjp1[-1] * 1.05, 50)
    slope = E[-1] / jjp1[-1]
    ax1.plot(xline, slope * xline, "--", color="gray", lw=1,
             label="rigid rotor $E\\propto j(j{+}1)$")
    ax1.scatter(jjp1, E, s=70, color="C0", zorder=3)
    for j, e, lab, d in zip(jjp1, E, labels, deg):
        ax1.annotate(f"{lab}\n$(2j{{+}}1)^2={d}$", (j, e),
                     textcoords="offset points", xytext=(8, -6), fontsize=8)
    ax1.set_xlabel("$j(j{+}1)$")
    ax1.set_ylabel("$E_j - E_{1/2}$  (transfer units)")
    ax1.set_title(f"FR baryon tower — ratio "
                  f"$(E_{{5/2}}{{-}}E_{{1/2}})/(E_{{3/2}}{{-}}E_{{1/2}})$"
                  f"={bq1['ratio_E52_E12_over_E32_E12']:.3f} (8/3={8/3:.3f})")
    ax1.legend(fontsize=8, loc="upper left")

    # --- right: observables vs ANW vs exp ---
    names = ["$\\mu_p/\\mu_n$\n(/-1)", "$r_{iso}$ [fm]", "$g_A$", "$e$/5"]
    ours = [-bq4["mu_p_over_mu_n"], bq4["isoscalar_charge_radius_fm"],
            bq4["g_A"], bq3["calibrated_e"] / 5.0]
    anw = [1.43, 0.59, 0.61, 5.45 / 5.0]
    exp = [1.46, 0.81, 1.267, np.nan]
    x = np.arange(len(names)); w = 0.27
    ax2.bar(x - w, ours, w, label="TEIC (BQ)", color="C0")
    ax2.bar(x, anw, w, label="ANW", color="C1")
    ax2.bar(x + w, exp, w, label="experiment", color="C2")
    ax2.set_xticks(x); ax2.set_xticklabels(names, fontsize=8)
    ax2.set_title("Parameter-free predictions (1 calibration: N–Δ → e)")
    ax2.legend(fontsize=8)
    ax2.axhline(0, color="k", lw=0.5)

    fig.suptitle("BQ (#12) — quantitative collective-coordinate quantization of the "
                 "B=1 Skyrmion", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.96))
    out = HERE / "BQ_summary.png"
    fig.savefig(out, dpi=130)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
