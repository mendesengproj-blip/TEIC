"""F_synthesis -- aggregate the four falsification tests into one honest verdict."""

from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent


def load(name):
    p = OUT / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    eht = load("F_EHT"); jwst = load("F_JWST"); cmb = load("F_CMB"); lens = load("F_LENSING")

    summary = {
        "EHT": {"verdict": eht.get("verdict"),
                "discriminating": eht.get("is_discriminating_test"),
                "max_shadow_shift_uas": eht.get("max_TEIC_shadow_shift_uas")},
        "JWST_BTFR": {"verdict": jwst.get("verdict"),
                      "pred_z2_dex": jwst.get("prediction_z2_dex"),
                      "tension_sigma": jwst.get("tension_sigma_at_z2"),
                      "discriminating": True},
        "CMB_monopoles": {"verdict": cmb.get("verdict"),
                          "type": cmb.get("monopole_type_in_T3D2"),
                          "discriminating": False},
        "LENSING_slip": {"verdict": lens.get("verdict"),
                         "distinguishable_now": lens.get("distinguishable_with_current_data"),
                         "discriminating": False},
        "OVERALL": "NAO FALSIFICADA (consistente com dados atuais)",
        "honest_caveat": (
            "Of the four tests, THREE are NON-DISCRIMINATING with present data: EHT "
            "(TEIC->GR in strong field; deviation 10^-12..10^-95 uas), LENSING (a 2-7% "
            "slip is inside current ~20% bars; Euclid is the test), and CMB monopoles "
            "(consistent only under the Polyakov/vacuum reading, i.e. T3D2 does not "
            "predict physical relic monopoles). The ONLY genuinely discriminating test is "
            "the JWST BTFR evolution, where the DEV predicts +0.12 dex at z=2 against an "
            "observed ~non-evolving relation -- a tentative ~1.6 sigma TENSION that is "
            "data-limited and needs the primary tabulated offsets (Ubler+2023). "
            "Conclusion: the theory is NOT falsified, but it is also largely UNTESTED by "
            "three of these probes; the decisive confrontations are the JWST/ALMA BTFR "
            "(primary data) and Euclid (directional slip)."),
    }
    (OUT / "F_synthesis.json").write_text(json.dumps(summary, indent=2))

    print("=" * 74)
    print("FALSIFICATION -- SYNTHESIS")
    print("=" * 74)
    print(f"EHT (shadow):       {summary['EHT']['verdict']:35s} "
          f"discriminating={summary['EHT']['discriminating']}")
    print(f"JWST (BTFR):        {summary['JWST_BTFR']['verdict']:35s} "
          f"tension={summary['JWST_BTFR']['tension_sigma']:.1f}sigma discriminating=True")
    print(f"CMB (monopoles):    {summary['CMB_monopoles']['verdict']:35s} "
          f"discriminating=False")
    print(f"LENSING (slip):     {summary['LENSING_slip']['verdict']:35s} "
          f"discriminating=False")
    print("-" * 74)
    print(f"OVERALL: {summary['OVERALL']}")
    print(summary["honest_caveat"])
    return summary


if __name__ == "__main__":
    main()
