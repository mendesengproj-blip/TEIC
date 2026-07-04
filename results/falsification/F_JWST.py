"""F_JWST -- test the DEV BTFR-evolution prediction against high-z rotation data.

DEV prediction (the modified-gravity programme TEIC welds to; a0 ~ cH is a MEASURED
coincidence, not derived -- paper main.tex, DEV_bridge_future.md). If the MONDian
acceleration scale tracks the Hubble rate, a0(z) ~ c H(z), the baryonic Tully-Fisher
relation (BTFR, v^4 = G a0 M_b) shifts with redshift by

    Delta log10(v_flat) = (1/4) log10[ H(z) / H0 ] .

LCDM predicts NO BTFR evolution (a0 = const). The two are distinguishable -> falsifiable.

We compute Delta log(v) for LCDM H(z) = H0 sqrt(Om (1+z)^3 + OL).  For the DATA we do NOT
fabricate a tabulated offset: the robust, citable observational picture is that the
BARYONIC TFR is approximately NON-EVOLVING out to z ~ 1-2.5 within uncertainties
(e.g. Ubler et al. 2017, KMOS3D, ApJ 842 121: stellar-TFR zeropoint evolves, baryonic
TFR consistent with no evolution; Ubler+2023 arXiv:2302.06647; Nestor Shachar+2023
arXiv:2304.05339). We therefore confront the prediction with an observed offset
consistent with ~0 at the ~0.05-0.10 dex (systematics-dominated) level, and report the
tension HONESTLY as tentative / data-limited -- the definitive test needs the primary
tabulated BTFR offsets.

ANTI-CIRCULARITY: H(z) is standard LCDM; the prediction is computed, not fitted; the
observational value is flagged as a literature-consensus range, NOT a measurement we made.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

# --- standard LCDM (Planck 2018: Om=0.315, OL=0.685) ------------------------ #
OM = 0.315
OL = 0.685
ZS = [0.5, 1.0, 2.0, 3.0]


def H_ratio(z):
    return np.sqrt(OM * (1 + z) ** 3 + OL)


def delta_logv(z):
    return 0.25 * np.log10(H_ratio(z))


# --- observational landscape (CITED, not measured here) --------------------- #
# Robust qualitative result: the baryonic TFR is ~non-evolving out to z~1-2.5 within
# uncertainties. We represent it as offset_obs(z) = 0 with a systematics-dominated
# uncertainty band; the definitive comparison requires the primary tabulated offsets.
OBS_OFFSET = 0.0
OBS_SIGMA = 0.075          # representative ~0.05-0.10 dex systematics band (NOT a fit)
OBS_REFS = ["Ubler et al. 2017, ApJ 842 121 (KMOS3D): baryonic TFR ~ non-evolving",
            "Ubler et al. 2023, arXiv:2302.06647",
            "Nestor Shachar et al. 2023, arXiv:2304.05339"]


def main():
    pred = {f"z={z}": delta_logv(z) for z in ZS}
    # tension at the canonical z=2 anchor
    pred_z2 = delta_logv(2.0)
    tension_sigma = abs(pred_z2 - OBS_OFFSET) / OBS_SIGMA

    if tension_sigma < 1.0:
        verdict = "CONSISTENTE"
    elif tension_sigma < 3.0:
        verdict = "TENSAO (tentativa, limitada por dados)"
    else:
        verdict = "FALSIFICADO"

    payload = {
        "cosmology": {"Om": OM, "OL": OL},
        "prediction_Delta_log_v_dex": pred,
        "prediction_z2_dex": pred_z2,
        "observed_offset_dex": OBS_OFFSET,
        "observed_sigma_dex": OBS_SIGMA,
        "observed_is_literature_consensus_not_our_measurement": True,
        "observed_refs": OBS_REFS,
        "tension_sigma_at_z2": tension_sigma,
        "verdict": verdict,
        "caveat": ("Observed offset is a literature-consensus band (BTFR ~ non-evolving), "
                   "NOT a value we measured; systematics (pressure support, beam "
                   "smearing, sample selection) dominate. A definitive verdict requires "
                   "the primary tabulated BTFR offsets of Ubler+2023. This is the only "
                   "GENUINELY DISCRIMINATING test of the four (EHT/lensing are in the "
                   "GR/untested regime)."),
        "note_LCDM": "LCDM predicts zero BTFR evolution; DEV predicts the dex shifts above.",
    }
    (Path(__file__).resolve().parent / "F_JWST.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("F_JWST -- BTFR evolution: DEV prediction vs high-z rotation data")
    print("=" * 74)
    print(f"LCDM (Om={OM}, OL={OL}):  Delta log10(v) = (1/4) log10[H(z)/H0]")
    for z in ZS:
        print(f"  z={z}:  H(z)/H0 = {H_ratio(z):.3f}   Delta log(v) = {delta_logv(z):+.4f} dex")
    print("-" * 74)
    print("Observed (literature consensus, NOT measured here):")
    print(f"  BTFR ~ non-evolving: offset = {OBS_OFFSET:+.3f} +- {OBS_SIGMA:.3f} dex "
          f"(systematics-dominated)")
    for r in OBS_REFS:
        print(f"   - {r}")
    print(f"DEV prediction at z=2: {pred_z2:+.4f} dex")
    print(f"tension at z=2: {tension_sigma:.1f} sigma")
    print(f"VERDICT: {verdict}")
    print("  (data-limited; needs primary tabulated offsets for a definitive verdict)")
    return payload


if __name__ == "__main__":
    main()
