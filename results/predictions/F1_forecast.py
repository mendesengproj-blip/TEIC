"""F1 -- forecast of the decisive BTFR test (the riskiest prediction).

Signal: Delta log10(v_flat) = (1/4) log10[H(z)/H0]  (flat LCDM, H0=67, Om=0.30+-0.02;
same convention as results/falsification/btfr_v2/B1_prediction.py -- H0 cancels).

Question answered here: at which z, with how many galaxies, and below what systematic
floor does the prediction become decisively testable against LCDM (Delta = 0)?

Error model for a future sample of low-mass gas-rich rotators in the low-acceleration
regime (the regime where the prediction applies -- B5 caveat of FALSIFICATION_BTFR_V2):

  per-galaxy scatter in log10 v_flat at fixed M_b:
      sigma_gal in {0.05 (SPARC-quality), 0.10 (realistic high-z), 0.15 (conservative)}
  zero-point systematics (pressure support, beam smearing, M_b calibration) that do
  NOT average down with N:
      sigma_sys in {0.02 (optimistic future), 0.04 (state of the art)}

  sigma_tot(N) = sqrt(sigma_gal^2 / N + sigma_sys^2)
  significance  S(z, N) = signal(z) / sigma_tot(N)
  ceiling       S_max(z) = signal(z) / sigma_sys   (N -> infinity)

COMPARISON ONLY note: this is a prediction/forecast script (lives under results/),
not a generator; H(z) belongs here by construction.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from astropy.cosmology import FlatLambdaCDM

OUT = Path(__file__).resolve().parent

H0 = 67.0
OM, OM_SIG = 0.30, 0.02
SIGMA_GAL = [0.05, 0.10, 0.15]
SIGMA_SYS = [0.02, 0.04]
Z_TABLE = [1.0, 1.5, 2.0, 2.5, 3.0]
TARGETS = [3.0, 5.0]

# Ubler+2017 (KMOS3D) points from FALSIFICATION_BTFR_V2 B2 -- WRONG REGIME
# (massive, high-acceleration); statistical floor sigma_b / a (a = 3.75).
KMOS3D = [
    {"z": 0.9, "dlogv": 0.1173, "err": 0.04 / 3.75},
    {"z": 2.3, "dlogv": 0.0720, "err": 0.05 / 3.75},
]


def signal(z, Om=OM):
    c = FlatLambdaCDM(H0=H0, Om0=Om)
    return 0.25 * np.log10(c.H(z).value / c.H(0).value)


def n_required(sig, sigma_gal, sigma_sys, target):
    """Galaxies needed so that signal/sigma_tot >= target; None if unreachable."""
    var_needed = (sig / target) ** 2 - sigma_sys**2
    if var_needed <= 0:
        return None  # systematic ceiling below target
    return int(np.ceil(sigma_gal**2 / var_needed))


def main():
    rows = []
    for z in Z_TABLE:
        s = float(signal(z))
        row = {"z": z, "signal_dex": round(s, 4),
               "S_max": {str(ss): round(s / ss, 2) for ss in SIGMA_SYS}}
        for ss in SIGMA_SYS:
            for sg in SIGMA_GAL:
                for t in TARGETS:
                    key = f"N({t:.0f}sigma, sig_gal={sg}, sig_sys={ss})"
                    row[key] = n_required(s, sg, ss, t)
        rows.append(row)

    payload = {
        "cosmology": {"H0": H0, "Om": OM, "Om_sigma": OM_SIG},
        "prediction": "Delta log10(v_flat) = (1/4) log10[H(z)/H0]; LCDM predicts 0",
        "regime": "low-mass gas-rich rotators, a <~ a0 (B5 caveat respected)",
        "error_model": {"sigma_gal": SIGMA_GAL, "sigma_sys": SIGMA_SYS,
                        "sigma_tot": "sqrt(sigma_gal^2/N + sigma_sys^2)"},
        "table": rows,
        "kill_criterion": (
            "If a sample of >=25 low-mass gas-rich rotators at z>=2 in the "
            "low-acceleration regime, with zero-point systematics <=0.03 dex, "
            "measures Delta log v_flat <= 0 (non-evolving or decreasing), the "
            "prediction -- and with it the galactic sector of the theory -- is "
            "falsified. Conversely, Delta log v > 0 at >=5 sigma in that regime "
            "falsifies LCDM's null evolution."
        ),
    }
    (OUT / "F1_forecast.json").write_text(json.dumps(payload, indent=2))

    # ---- figure -------------------------------------------------------------
    zs = np.linspace(0.0, 3.2, 161)
    sig = signal(zs)
    sig_lo, sig_hi = signal(zs, OM - OM_SIG), signal(zs, OM + OM_SIG)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))

    ax1.fill_between(zs, sig_lo, sig_hi, color="tab:blue", alpha=0.25,
                     label=r"DEV: $\frac{1}{4}\log[H(z)/H_0]$ ($\Omega_m$ band)")
    ax1.plot(zs, sig, color="tab:blue")
    ax1.axhline(0.0, color="k", lw=1, ls="--", label=r"$\Lambda$CDM (null)")
    for ss, ls in zip(SIGMA_SYS, [":", "-."]):
        ax1.axhline(ss, color="gray", lw=1, ls=ls,
                    label=fr"syst. floor $\sigma_{{\rm sys}}={ss}$ dex")
    for p in KMOS3D:
        ax1.errorbar(p["z"], p["dlogv"], yerr=p["err"], fmt="s", color="0.55",
                     capsize=3)
    ax1.annotate("KMOS$^{3D}$ (massive, high-acc:\nwrong regime)", xy=(0.95, 0.118),
                 fontsize=8, color="0.4")
    ax1.set_xlabel("z")
    ax1.set_ylabel(r"$\Delta\log_{10} v_{\rm flat}$ [dex] at fixed $M_b$")
    ax1.set_title("The riskiest prediction vs the null")
    ax1.legend(fontsize=7.5, loc="upper left")

    for sg, c in zip(SIGMA_GAL, ["tab:green", "tab:orange", "tab:red"]):
        ns = [n_required(float(signal(z)), sg, 0.02, 3.0) for z in zs]
        ns = [n if n is not None else np.nan for n in ns]
        ax2.plot(zs, ns, color=c, label=fr"$\sigma_{{\rm gal}}={sg}$ dex")
    ax2.set_yscale("log")
    ax2.set_ylim(1, 3e3)
    ax2.set_xlim(0.5, 3.2)
    ax2.set_xlabel("z")
    ax2.set_ylabel(r"$N$ galaxies for $3\sigma$ ($\sigma_{\rm sys}=0.02$)")
    ax2.set_title("Sample size needed (JWST/ALMA regime)")
    ax2.axvspan(2.0, 3.2, color="tab:blue", alpha=0.08)
    ax2.annotate("decisive window", xy=(2.25, 1.5), fontsize=9, color="tab:blue")
    ax2.legend(fontsize=8)

    fig.tight_layout()
    fig.savefig(OUT / "F1_forecast.png", dpi=150)

    # console summary
    print("z      signal   S_max(0.04)  S_max(0.02)  N3sig(0.10,0.02)")
    for r in rows:
        print(f"{r['z']:.1f}   {r['signal_dex']:+.4f}   "
              f"{r['S_max']['0.04']:>6.2f}      {r['S_max']['0.02']:>6.2f}      "
              f"{r['N(3sigma, sig_gal=0.1, sig_sys=0.02)']}")


if __name__ == "__main__":
    main()
