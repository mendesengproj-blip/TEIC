"""F_LENSING -- DEV gravitational slip vs current weak-lensing precision.

DEV (future DEV-V extension, DEV_bridge_future.md) predicts a gravitational slip
eta = Phi/Psi with eta - 1 in [2.2%, 6.7%] -- and, in the extended theory, a DIRECTIONAL
(anisotropic) slip aligned with the local density gradient, largest at filament/cluster
edges.  Current weak-lensing surveys constrain ISOTROPIC modified-gravity parameters at
the ~10-30% level (KiDS-1000, Heymans+2021; DES Y3, DES+2021; E_G statistic, Reyes+2010 ~
0.39 +- 0.06, consistent with GR).  A 2-7% slip is therefore WELL inside current error
bars -> CONSISTENT but UNTESTED.  Euclid (~1% slip precision) is the discriminating test;
the specific DEV-V *directional* slip is not even targeted by existing isotropic analyses.

ANTI-CIRCULARITY: the prediction band is the DEV's; the current precision is a cited
order-of-magnitude (we do not fabricate a specific eta measurement).
"""

from __future__ import annotations

import json
from pathlib import Path

# DEV prediction band (fractional slip eta-1)
ETA_PRED_LOW = 0.022
ETA_PRED_HIGH = 0.067
# current weak-lensing precision on isotropic slip-type parameters (order of magnitude)
CURRENT_PRECISION = 0.20      # ~10-30%; cited (KiDS-1000, DES Y3, E_G)
EUCLID_PRECISION = 0.01       # ~1% (forecast)
REFS = ["Heymans et al. 2021 (KiDS-1000)", "DES Collaboration 2021 (DES Y3)",
        "Reyes et al. 2010 (E_G ~ 0.39 +- 0.06, consistent with GR)"]


def main():
    pred_mid = 0.5 * (ETA_PRED_LOW + ETA_PRED_HIGH)
    # current data cannot distinguish the predicted band from GR (eta-1 = 0)
    distinguishable_now = ETA_PRED_LOW > CURRENT_PRECISION
    distinguishable_euclid = ETA_PRED_LOW > EUCLID_PRECISION
    # consistent: the predicted band lies within the current error band around GR
    consistent_now = ETA_PRED_HIGH < CURRENT_PRECISION + 0.05   # band inside ~current bar

    verdict = "CONSISTENTE (mas nao testado)" if consistent_now else "TENSAO"

    payload = {
        "eta_minus_1_pred_band": [ETA_PRED_LOW, ETA_PRED_HIGH],
        "eta_pred_mid": pred_mid,
        "current_WL_precision_on_slip": CURRENT_PRECISION,
        "euclid_precision_forecast": EUCLID_PRECISION,
        "refs": REFS,
        "distinguishable_with_current_data": bool(distinguishable_now),
        "distinguishable_with_euclid": bool(distinguishable_euclid),
        "consistent_with_current_data": bool(consistent_now),
        "verdict": verdict,
        "note": ("A 2.2-6.7% slip is inside current weak-lensing error bars (~10-30% on "
                 "isotropic slip-type parameters; E_G consistent with GR), so it is "
                 "CONSISTENT but NOT YET TESTED. Euclid (~1%) is the discriminating "
                 "instrument. Moreover the DEV-V slip is DIRECTIONAL (anisotropic, "
                 "filament/edge-aligned) -- a signature existing isotropic analyses do "
                 "not target. Non-discriminating with present data."),
    }
    (Path(__file__).resolve().parent / "F_LENSING.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("F_LENSING -- gravitational slip: DEV prediction vs weak-lensing precision")
    print("=" * 74)
    print(f"DEV prediction: eta - 1 in [{ETA_PRED_LOW:.1%}, {ETA_PRED_HIGH:.1%}]")
    print(f"current WL precision on slip: ~{CURRENT_PRECISION:.0%}  (KiDS-1000, DES Y3, E_G)")
    print(f"Euclid forecast: ~{EUCLID_PRECISION:.0%}")
    for r in REFS:
        print(f"   - {r}")
    print(f"distinguishable now: {distinguishable_now}   with Euclid: {distinguishable_euclid}")
    print("-" * 74)
    print(f"VERDICT: {verdict}")
    print("  (a few-% slip is inside current error bars; Euclid is the real test;")
    print("   the DEV-V slip is directional, not targeted by isotropic analyses)")
    return payload


if __name__ == "__main__":
    main()
