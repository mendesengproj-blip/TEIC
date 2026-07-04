"""B1 -- DEV BTFR-evolution prediction with astropy, propagated uncertainty.

Delta log10(v_flat) = (1/4) log10[ H(z)/H0 ],  flat LCDM (H0=67, Om=0.3).

Note: in flat LCDM, H(z)/H0 = sqrt(Om(1+z)^3 + OL) is INDEPENDENT of H0, so the H0 +-1
uncertainty CANCELS in the ratio and propagates to ZERO. The real theory-side uncertainty
comes from Om; we propagate Om = 0.30 +- 0.02 (a conservative band bracketing Planck
0.315 +- 0.007 and older 0.30).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from astropy.cosmology import FlatLambdaCDM

OUT = Path(__file__).resolve().parent
ZS = [0.0, 0.5, 0.9, 1.5, 2.0, 2.3, 3.0]
H0 = 67.0
OM = 0.30
OM_SIG = 0.02


def delta_logv(z, Om, H0=67.0):
    c = FlatLambdaCDM(H0=H0, Om0=Om)
    return 0.25 * np.log10(c.H(z).value / c.H(0).value)


def main():
    rows = []
    for z in ZS:
        d0 = delta_logv(z, OM)
        d_lo = delta_logv(z, OM - OM_SIG)
        d_hi = delta_logv(z, OM + OM_SIG)
        # H0 propagation: identically zero (ratio independent of H0) -- demonstrate
        d_H0p = delta_logv(z, OM, H0=68.0)
        sigma_Om = 0.5 * abs(d_hi - d_lo)
        rows.append({"z": z, "delta_logv": d0,
                     "sigma_from_Om": sigma_Om,
                     "delta_logv_H0_68": d_H0p,
                     "H0_propagation_error": abs(d_H0p - d0)})
    payload = {"cosmology": {"H0": H0, "Om": OM, "Om_sigma": OM_SIG},
               "note_H0_cancels": "H(z)/H0 is independent of H0 in flat LCDM; "
                                  "H0 uncertainty propagates to zero.",
               "predictions": rows,
               "anchor_z0.9": delta_logv(0.9, OM),
               "anchor_z2.3": delta_logv(2.3, OM)}
    (OUT / "B1_prediction.json").write_text(json.dumps(payload, indent=2))

    print("=" * 70)
    print("B1 -- DEV prediction  Delta log(v) = (1/4) log10[H(z)/H0]")
    print("=" * 70)
    print(f"flat LCDM H0={H0}, Om={OM} +- {OM_SIG}")
    print(f"{'z':>5} {'Delta_logv':>11} {'sigma(Om)':>10} {'err(H0+1)':>10}")
    for r in rows:
        print(f"{r['z']:5.1f} {r['delta_logv']:+11.4f} {r['sigma_from_Om']:10.4f} "
              f"{r['H0_propagation_error']:10.1e}")
    print("-" * 70)
    print("H0 +-1 propagates to ~0 (ratio independent of H0); Om dominates the band.")
    return payload


if __name__ == "__main__":
    main()
