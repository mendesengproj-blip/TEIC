"""B2 -- primary Ubler+2017 (KMOS3D) bTFR data, converted to Delta log(v).

Source: Ubler H. et al. 2017, ApJ 842, 121 (arXiv:1703.04321), Table 2 and text
(values fetched from the paper, NOT estimated):
  baryonic TFR fixed slope a = 3.75 (Lelli et al. 2016), reference velocity v_ref = 242 km/s
  zero-point (log M_bar at v_ref):  b(z~0.9) = 10.68 +- 0.04 ,  b(z~2.3) = 10.85 +- 0.05
  offset to local (Lelli+2016): Db_bTFR(z~0.9) = -0.44 ,  Db_bTFR(z~2.3) = -0.27
  internal evolution z~0.9 -> z~2.3:  Db = +0.17 dex
  abstract: "negative evolution of the stellar and baryonic TFR zero-points from z=0 to
  z~0.9 ... positive evolution of the baryonic TFR zero-point from z~0.9 to z~2.3."

Conversion to the DEV variable Delta log(v) at FIXED baryonic mass.  On log M_bar =
a (log v - log v_ref) + b, fixed M gives Delta log v = -Db / a.  A NEGATIVE mass-zero-point
offset Db<0 (less baryonic mass at fixed v) <=> POSITIVE Delta log v (faster rotation at
fixed mass).

Two comparisons:
  (i) to-local offsets -> Delta log v at each z relative to z=0 (the DEV variable), BUT
      systematics-dominated (Ubler: including disturbed/dispersion-dominated galaxies makes
      the z=0->high-z evolution "insignificant");
  (ii) internal z~0.9->z~2.3 change -> the ROBUST quantity (free of local-comparison
      systematics).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parent
A_SLOPE = 3.75
V_REF = 242.0

# primary values (arXiv:1703.04321)
B_Z09, SIG_B_Z09 = 10.68, 0.04
B_Z23, SIG_B_Z23 = 10.85, 0.05
DB_LOCAL_Z09 = -0.44       # b(z~0.9) - b_local
DB_LOCAL_Z23 = -0.27       # b(z~2.3) - b_local
DB_INTERNAL = +0.17        # b(z~2.3) - b(z~0.9)


def dlogv_from_db(db):
    return -db / A_SLOPE


def main():
    # (i) to-local -> Delta log v(z) [DEV variable]; stat error from the high-z b fit
    obs = {
        "z~0.9": {"z": 0.9, "Db_to_local": DB_LOCAL_Z09,
                  "dlogv": dlogv_from_db(DB_LOCAL_Z09),
                  "sigma_stat": SIG_B_Z09 / A_SLOPE},
        "z~2.3": {"z": 2.3, "Db_to_local": DB_LOCAL_Z23,
                  "dlogv": dlogv_from_db(DB_LOCAL_Z23),
                  "sigma_stat": SIG_B_Z23 / A_SLOPE},
    }
    # (ii) internal robust change in Delta log v from z~0.9 to z~2.3
    sig_internal_b = np.hypot(SIG_B_Z09, SIG_B_Z23)
    internal = {"Db_internal": DB_INTERNAL,
                "d(dlogv)_internal": dlogv_from_db(DB_INTERNAL),  # change in Delta log v
                "sigma": sig_internal_b / A_SLOPE}

    payload = {
        "source": "Ubler et al. 2017, ApJ 842 121 (arXiv:1703.04321), Table 2",
        "bTFR_slope": A_SLOPE, "v_ref_km_s": V_REF,
        "zero_points": {"b_z0.9": [B_Z09, SIG_B_Z09], "b_z2.3": [B_Z23, SIG_B_Z23]},
        "to_local_offsets_Db": {"z0.9": DB_LOCAL_Z09, "z2.3": DB_LOCAL_Z23},
        "observed_dlogv_to_local": obs,
        "internal_evolution": internal,
        "caveats": [
            "to-local offsets are SYSTEMATICS-DOMINATED (sample selection; Ubler note the "
            "z=0->high-z evolution can be 'insignificant' if disturbed/dispersion-dominated "
            "galaxies are included); stat errors below are lower bounds on the true error.",
            "the INTERNAL z~0.9->z~2.3 change is the robust, systematics-controlled quantity.",
            "MASS BIAS: KMOS3D is massive disks (log M* > ~10.5), HIGH surface brightness, "
            "i.e. the HIGH-acceleration (Newtonian) regime -- where the DEV a0(z) signal is "
            "intrinsically weak. The DEV/SPARC calibration is LOW-mass, deep-MOND galaxies.",
        ],
    }
    (OUT / "B2_data.json").write_text(json.dumps(payload, indent=2))

    print("=" * 70)
    print("B2 -- Ubler+2017 bTFR data -> Delta log(v)  (a=3.75, v_ref=242 km/s)")
    print("=" * 70)
    print(f"zero-points: b(z~0.9)={B_Z09}+-{SIG_B_Z09}  b(z~2.3)={B_Z23}+-{SIG_B_Z23}")
    print(f"to-local Db: z~0.9={DB_LOCAL_Z09}  z~2.3={DB_LOCAL_Z23}  (internal +{DB_INTERNAL})")
    print("-> Delta log(v) at fixed M_bar = -Db/a:")
    for k, o in obs.items():
        print(f"   {k}: Delta log v = {o['dlogv']:+.4f} +- {o['sigma_stat']:.4f} (stat only)")
    print(f"internal change z~0.9->z~2.3: d(Delta log v) = {internal['d(dlogv)_internal']:+.4f}"
          f" +- {internal['sigma']:.4f}  (ROBUST; v at fixed M DECREASES with z)")
    print("CAVEAT: massive HIGH-acceleration sample -> weak DEV signal; to-local is "
          "systematics-dominated.")
    return payload


if __name__ == "__main__":
    main()
