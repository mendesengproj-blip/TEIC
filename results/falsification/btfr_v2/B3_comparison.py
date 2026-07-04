"""B3 -- direct comparison DEV vs Ubler+2017 vs LCDM(=0), tension in sigma + figure.

Two comparisons (B2): (i) to-local Delta log v at each z (DEV variable, systematics-dominated);
(ii) the ROBUST internal z~0.9->z~2.3 change.  We report tension vs DEV and vs LCDM for both.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    HAVE_MPL = True
except Exception:
    HAVE_MPL = False


def main():
    B1 = json.loads((OUT / "B1_prediction.json").read_text())
    B2 = json.loads((OUT / "B2_data.json").read_text())

    dev = {r["z"]: r["delta_logv"] for r in B1["predictions"]}
    dev_09, dev_23 = dev[0.9], dev[2.3]
    obs = B2["observed_dlogv_to_local"]
    o09, o23 = obs["z~0.9"], obs["z~2.3"]
    internal = B2["internal_evolution"]

    # (i) to-local tensions (stat errors only -- LOWER BOUND on true error)
    def tens(obsval, sig, model):
        return abs(obsval - model) / sig
    tl = {
        "z~0.9": {"obs": o09["dlogv"], "sig": o09["sigma_stat"], "DEV": dev_09,
                  "tension_DEV": tens(o09["dlogv"], o09["sigma_stat"], dev_09),
                  "tension_LCDM": tens(o09["dlogv"], o09["sigma_stat"], 0.0)},
        "z~2.3": {"obs": o23["dlogv"], "sig": o23["sigma_stat"], "DEV": dev_23,
                  "tension_DEV": tens(o23["dlogv"], o23["sigma_stat"], dev_23),
                  "tension_LCDM": tens(o23["dlogv"], o23["sigma_stat"], 0.0)},
    }
    # (ii) internal robust change
    dev_change = dev_23 - dev_09
    obs_change = internal["d(dlogv)_internal"]
    sig_change = internal["sigma"]
    internal_cmp = {
        "obs_change": obs_change, "sigma": sig_change,
        "DEV_change": dev_change, "LCDM_change": 0.0,
        "tension_DEV": abs(obs_change - dev_change) / sig_change,
        "tension_LCDM": abs(obs_change - 0.0) / sig_change,
        "trend_opposite_to_DEV": bool(obs_change * dev_change < 0),
    }

    payload = {"to_local": tl, "internal": internal_cmp,
               "dev_09": dev_09, "dev_23": dev_23,
               "summary": {
                   "to_local_favours_evolution_over_LCDM": bool(
                       tl["z~0.9"]["tension_LCDM"] > tl["z~0.9"]["tension_DEV"]),
                   "internal_trend_opposite_to_DEV": internal_cmp["trend_opposite_to_DEV"],
                   "internal_tension_DEV_sigma": internal_cmp["tension_DEV"],
                   "internal_tension_LCDM_sigma": internal_cmp["tension_LCDM"],
               }}
    (OUT / "B3_comparison.json").write_text(json.dumps(payload, indent=2))

    if HAVE_MPL:
        zs = np.linspace(0, 2.6, 100)
        from astropy.cosmology import FlatLambdaCDM
        c = FlatLambdaCDM(H0=67, Om0=0.30)
        dev_curve = 0.25 * np.log10(c.H(zs).value / c.H(0).value)
        fig, ax = plt.subplots(figsize=(7.5, 5.2))
        ax.plot(zs, dev_curve, "b-", lw=2, label=r"DEV: $\frac{1}{4}\log[H(z)/H_0]$")
        ax.axhline(0, color="k", lw=1.2, ls="--", label=r"$\Lambda$CDM (no evolution)")
        ax.errorbar([0.9, 2.3], [o09["dlogv"], o23["dlogv"]],
                    yerr=[o09["sigma_stat"], o23["sigma_stat"]], fmt="rs", ms=9,
                    capsize=4, label="Ubler+2017 (to local, stat err)")
        ax.annotate("internal trend\n(robust): DECREASES",
                    xy=(1.6, 0.095), fontsize=9, color="darkred")
        ax.set_xlabel("redshift z"); ax.set_ylabel(r"$\Delta\log_{10}(v_{\rm flat})$ [dex]")
        ax.set_title("BTFR evolution: DEV prediction vs Ubler+2017 (KMOS3D)")
        ax.legend(loc="upper left"); ax.set_xlim(-0.05, 2.6)
        fig.savefig(OUT / "B3_comparison.png", dpi=130, bbox_inches="tight")

    print("=" * 72)
    print("B3 -- DEV vs Ubler+2017 vs LCDM")
    print("=" * 72)
    print(f"DEV: z~0.9 = {dev_09:+.4f}   z~2.3 = {dev_23:+.4f}   (change {dev_change:+.4f})")
    print("\n(i) to-local offsets (DEV variable; stat errors are a LOWER bound):")
    for k, t in tl.items():
        print(f"  {k}: obs={t['obs']:+.4f}+-{t['sig']:.4f}  "
              f"tension vs DEV={t['tension_DEV']:.1f}sig  vs LCDM={t['tension_LCDM']:.1f}sig")
    print("\n(ii) internal z~0.9->z~2.3 change (ROBUST):")
    print(f"  observed = {obs_change:+.4f}+-{sig_change:.4f}   DEV = {dev_change:+.4f}   LCDM = 0")
    print(f"  tension vs DEV = {internal_cmp['tension_DEV']:.1f}sig   "
          f"vs LCDM = {internal_cmp['tension_LCDM']:.1f}sig")
    print(f"  trend OPPOSITE to DEV: {internal_cmp['trend_opposite_to_DEV']} "
          f"(DEV predicts increase; observed decreases)")
    return payload


if __name__ == "__main__":
    main()
