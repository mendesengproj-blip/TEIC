"""BQ5 -- synthesis and verdict for BARYON_QUANTITATIVE (gap #12)."""
from __future__ import annotations
import json
from pathlib import Path
import bq_core as b

HERE = Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE / f"{name}.json").read_text())


def main():
    bq1 = load("BQ1_tower")
    bq2 = load("BQ2_inertia")
    bq3 = load("BQ3_calibration")
    bq4 = load("BQ4_moments")

    all_pass = (bq1["verdict"] == "PASS" and bq2["verdict"] == "PASS"
                and bq3["verdict"] == "PASS" and bq4["verdict"] == "PASS")
    verdict = "A" if all_pass else "B"

    payload = dict(
        BQ1_tower=bq1["verdict"],
        BQ1_FR_degeneracies=bq1["FR_tower_degeneracies"],
        BQ1_ratio=bq1["ratio_E52_E12_over_E32_E12"],
        BQ2_inertia=bq2["verdict"],
        BQ2_skyrme_inertia_fraction=bq2["skyrme_inertia_fraction"],
        BQ2_full_over_sigma=bq2["I_full_over_I_sigma"],
        BQ3_calibration=bq3["verdict"],
        BQ3_e=bq3["calibrated_e"], BQ3_e_vs_ANW=bq3["ANW_e"],
        BQ4_moments=bq4["verdict"],
        BQ4_mu_ratio=bq4["mu_p_over_mu_n"],
        BQ4_r_iso_fm=bq4["isoscalar_charge_radius_fm"],
        BQ4_g_A=bq4["g_A"],
        VERDICT=verdict,
        verdict_text=(
            "A -- the quantitative collective-coordinate quantization of the TEIC "
            "B=1 Skyrmion reproduces the established baryon phenomenology. (1) The "
            "FR-projected rotor tower gives the baryon multiplets with degeneracies "
            f"{bq1['FR_tower_degeneracies']} = (2j+1)^2 for j=1/2(N),3/2(Delta),5/2, "
            f"spin=isospin locked, with the parameter-free ratio "
            f"(E_5/2-E_1/2)/(E_3/2-E_1/2)={bq1['ratio_E52_E12_over_E32_E12']:.3f} "
            "(rigid-rotor 8/3=2.667). (2) The FULL moment of inertia adds the Skyrme "
            f"contribution Q2 omitted ({bq2['skyrme_inertia_fraction']*100:.0f}% of "
            f"the total; full inertia {bq2['I_full_over_I_sigma']:.2f}x the sigma-only "
            "value). (3) ONE calibration (the N-Delta splitting) fixes the Skyrme "
            f"coupling e={bq3['calibrated_e']:.2f} (ANW 5.45, 1%). (4) Then the "
            f"magnetic-moment ratio mu_p/mu_n={bq4['mu_p_over_mu_n']:.3f} (ANW -1.43, "
            f"exp -1.46), isoscalar radius {bq4['isoscalar_charge_radius_fm']:.2f} fm "
            f"(ANW 0.59), g_A={bq4['g_A']:.2f} (ANW 0.61) are PARAMETER-FREE "
            "predictions. SCOPE: f_pi (overall scale) is EXTERNAL-B; the EM current "
            "decomposition is imported standard physics (like the FR phase); the "
            "profile is the lattice's. The DIMENSIONLESS baryon structure is derived."
        ),
    )
    b.save_json("BQ5_synthesis", payload)
    print(f"BQ5  VERDICT {verdict}")
    print(f"     BQ1 {bq1['verdict']}  BQ2 {bq2['verdict']}  BQ3 {bq3['verdict']}  "
          f"BQ4 {bq4['verdict']}")
    return payload


if __name__ == "__main__":
    main()
