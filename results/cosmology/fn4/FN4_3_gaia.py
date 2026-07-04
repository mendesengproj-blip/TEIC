"""FN4_3_gaia.py -- DEV screening across the Chae+2023 wide-binary regime.

Charter FN4-3.  Chae (arXiv:2309.08160): 26,615 Gaia DR3 binaries, separations
200-30000 au (= 0.001-0.145 pc), MOND anomaly at s >~ 2 kau, gamma = 1.43 +/- 0.06.
This script verifies the separation regime, computes the DEV screening / residual
boost there, and quantifies the tension with Chae's positive detection.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fn4_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent


def main():
    s_au = np.logspace(np.log10(c.CHAE_S_MIN_AU), np.log10(c.CHAE_S_MAX_AU), 300)
    s_pc = s_au * c.AU / c.PC
    s = s_au * c.AU
    M = 1.5

    S = c.screening(s)                  # de-screening factor (tiny here)
    bM = c.boost_mond(s, M)
    bD = c.boost_dev(s, M)
    # fraction of MOND boost DEV keeps; 0 where there is no MOND boost (bM~1)
    recovered = np.where(bM - 1.0 > 1e-6, (bD - 1.0) / (bM - 1.0), 0.0)

    # checkpoints
    pts = {}
    for s_a in [200, 2000, 7031, 10000, 30000]:  # incl r_MOND~7031 au
        ss = s_a * c.AU
        pts[f"{s_a}au"] = {
            "s_pc": float(ss / c.PC),
            "s_over_lambda": float(ss / c.LAMBDA_A),
            "screening_S": float(c.screening(ss)),
            "boost_DEV": float(c.boost_dev(ss, M)),
            "boost_MOND": float(c.boost_mond(ss, M)),
            "MOND_boost_recovered": (
                float((c.boost_dev(ss, M) - 1) / (c.boost_mond(ss, M) - 1))
                if c.boost_mond(ss, M) - 1 > 1e-6 else 0.0),
        }

    # DEV vs Chae: Chae's gamma=1.43; DEV predicts the EFE plateau ONLY if unscreened.
    # In the Chae band DEV is screened -> predicted gamma ~ 1 (Newton).
    chae_mid = 0.5 * (c.CHAE_S_MIN_AU + c.CHAE_S_MAX_AU) * c.AU
    gamma_dev_chae = float(c.boost_dev(chae_mid, M))      # ~1.00x
    gamma_mond_chae = float(c.boost_mond(chae_mid, M))    # ~1.36x
    # tension: how many sigma is Chae's gamma=1.43 from the DEV (Newton) prediction
    tension_sigma = (c.CHAE_GAMMA - gamma_dev_chae) / c.CHAE_GAMMA_ERR

    payload = {
        "chae_sample": {
            "ref": "arXiv:2309.08160 (Chae 2023)",
            "N_binaries": 26615, "within_pc": 200,
            "sep_range_au": [c.CHAE_S_MIN_AU, c.CHAE_S_MAX_AU],
            "sep_range_pc": [c.CHAE_S_MIN_AU*c.AU/c.PC, c.CHAE_S_MAX_AU*c.AU/c.PC],
            "anomaly_onset_au": c.CHAE_S_ANOMALY_AU,
            "gamma": c.CHAE_GAMMA, "gamma_err": c.CHAE_GAMMA_ERR,
        },
        "lambda_A_pc": c.LAMBDA_A_PC,
        "chae_max_sep_over_lambda": float(c.CHAE_S_MAX_AU*c.AU / c.LAMBDA_A),
        "r_MOND_au": float(c.mond_radius(1.0)/c.AU),
        "checkpoints": pts,
        "DEV_prediction_in_chae_band": {
            "gamma_DEV": gamma_dev_chae, "gamma_MOND": gamma_mond_chae,
            "regime": "deeply screened: S << 1 -> DEV ~ Newton",
        },
        "tension_with_chae_sigma": float(tension_sigma),
        "is_chae_the_right_test": (
            "YES as a discriminator (DEV->Newton vs MOND->boost differ maximally "
            "here), but it probes the SCREENED PLATEAU, not the 17 pc transition"),
    }
    (OUT / "FN4_3_gaia.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("FN4-3  DEV screening across the Chae+2023 regime")
    print("=" * 74)
    print(f"  Chae range: {c.CHAE_S_MIN_AU:.0f}-{c.CHAE_S_MAX_AU:.0f} au = "
          f"{c.CHAE_S_MIN_AU*c.AU/c.PC:.4f}-{c.CHAE_S_MAX_AU*c.AU/c.PC:.4f} pc")
    print(f"  widest Chae binary / lambda_A = "
          f"{c.CHAE_S_MAX_AU*c.AU/c.LAMBDA_A:.4f}  (<< 1 -> deeply screened)")
    print(f"  r_MOND(1 Msun) = {c.mond_radius(1.0)/c.AU:.0f} au (MOND onset)\n")
    print(f"  {'s [au]':>8} {'s/lambda':>9} {'S(r)':>8} {'boost_DEV':>10} "
          f"{'boost_MOND':>11} {'%recov':>7}")
    for k, d in pts.items():
        print(f"  {k:>8} {d['s_over_lambda']:>9.5f} {d['screening_S']:>8.5f} "
              f"{d['boost_DEV']:>10.4f} {d['boost_MOND']:>11.4f} "
              f"{100*d['MOND_boost_recovered']:>6.2f}%")
    print(f"\n  DEV predicts gamma ~ {gamma_dev_chae:.3f} (Newton) in the Chae band.")
    print(f"  Chae measures gamma = {c.CHAE_GAMMA} +/- {c.CHAE_GAMMA_ERR}")
    print(f"  -> tension with DEV's Newtonian prediction: {tension_sigma:.1f} sigma")
    print(f"  saved {OUT/'FN4_3_gaia.json'}")

    make_figure(s_pc, S, bM, bD, recovered)
    return payload


def make_figure(s_pc, S, bM, bD, recovered):
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    ax[0].semilogx(s_pc, bM, color="C3", lw=2, ls="--", label="MOND boost ($\\sim$1.36)")
    ax[0].semilogx(s_pc, bD, color="C2", lw=2.6, label="DEV boost (screened $\\to$1)")
    ax[0].axhline(1.0, color="C0", lw=1.5, label="Newton")
    ax[0].axhspan(c.CHAE_GAMMA - c.CHAE_GAMMA_ERR, c.CHAE_GAMMA + c.CHAE_GAMMA_ERR,
                  color="orange", alpha=0.35,
                  label=f"Chae $\\gamma={c.CHAE_GAMMA}\\pm{c.CHAE_GAMMA_ERR}$")
    ax[0].axvline(c.mond_radius(1.0)/c.PC, color="purple", ls=":", lw=1,
                  label="$r_{MOND}\\approx$7000 au")
    ax[0].set_xlabel("separation s [pc]"); ax[0].set_ylabel("$g/g_N$ boost ($\\gamma$)")
    ax[0].set_title("FN4-3: in Chae's band DEV $\\approx$ Newton, Chae sees $\\gamma=1.43$")
    ax[0].legend(fontsize=7, loc="center left")

    ax[1].loglog(s_pc, 100*np.clip(recovered, 1e-3, 1), color="C2", lw=2.6,
                 label="% of MOND boost kept by DEV")
    ax[1].loglog(s_pc, 100*S, color="grey", lw=1.4, ls=":",
                 label="screening $S=1-e^{-s/\\lambda_A}$ [%]")
    ax[1].axhline(100, color="C3", lw=1.2, ls="--", label="full MOND (100%)")
    ax[1].set_xlabel("separation s [pc]")
    ax[1].set_ylabel("fraction of MOND boost recovered [%]")
    ax[1].set_title(f"FN4-3: DEV keeps <1% of MOND boost across Chae's range\n"
                    f"(widest binary = {c.CHAE_S_MAX_AU*c.AU/c.LAMBDA_A:.1%} of $\\lambda_A$)")
    ax[1].legend(fontsize=7, loc="upper left")

    fig.suptitle("FN4-3  Chae+2023 binaries (0.001-0.145 pc) lie DEEP inside the DEV "
                 "screened zone $\\Rightarrow$ DEV predicts Newton, in tension with "
                 "$\\gamma=1.43$", fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "FN4_3_gaia.png", dpi=130)
    print(f"  saved {OUT/'FN4_3_gaia.png'}")


if __name__ == "__main__":
    main()
