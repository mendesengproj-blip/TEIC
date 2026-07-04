"""F_EHT -- test the TEIC/DEV quartic-operator correction against the EHT black-hole shadow.

Published data (external; the theory is TESTED against them, not fitted):
  M87*  (EHT 2019, ApJL 875 L6, arXiv:1906.11243):
        crescent diameter theta_obs = 42 +- 3 uas,  M = (6.5 +- 0.7)e9 Msun, d = 16.8 Mpc
  Sgr A* (EHT 2022 / arXiv:2311.08680):
        theta_obs = 51.8 +- 2.3 uas,  M ~ 4.0e6 Msun, d = 8.15 kpc

TEIC/DEV prediction.  C4/AB1 measured the geometric quartic coefficient
C_q = -(1/24) n_links <Dtau (e.e)^2>  <0 at 9-17 sigma (a DBI-type, sign-definite lattice
number -- NOT itself a physical shadow deviation).  The physical question is how large a
fractional change delta_TEIC the quartic/DBI sector makes to the photon sphere.

Two honest suppression estimates (no fitting):
  (A) DEV / low-acceleration scale.  The modified-gravity sector departs from GR only at
      LOW acceleration a < a0 ~ 1.2e-10 m/s^2 (the MOND-like scale; a0 is MEASURED, not
      derived -- DEV_bridge_future.md, paper main.tex). The fractional deviation scales
      as ~ a0/a.  At a BH photon sphere a >> a0, so delta ~ a0/a is astronomically small.
      (Structural: the F^2/quartic terms are INERT where F=0; the photon sphere is the
      deep-GR, high-curvature regime -- the OPPOSITE of where the DEV modifies gravity.)
  (B) Planck suppression.  A higher-derivative operator suppressed by M_Pl gives a
      fractional deviation ~ (l_Pl / r_ph)^2.

Both give |delta_TEIC| many orders of magnitude below the EHT error bars.  Verdict:
CONSISTENT, but NON-DISCRIMINATING -- EHT cannot test the TEIC quartic sector because the
theory reduces to GR in the strong-field regime.  (The prompt's intro figure of "5-10%"
is NOT supported by either suppression; it would require an unsuppressed operator, which
contradicts both the Planck scale and the "inert where F=0" structure.)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

# --- physical constants (SI) ------------------------------------------------ #
G = 6.674e-11
c = 2.998e8
Msun = 1.989e30
Mpc = 3.086e22
kpc = 3.086e19
l_Pl = 1.616e-35
a0_MOND = 1.2e-10                       # MEASURED acceleration scale (not derived)
RAD_TO_UAS = (180.0 / np.pi) * 3600.0 * 1e6

# --- published EHT data (cited) --------------------------------------------- #
TARGETS = {
    "M87*": {"M_Msun": 6.5e9, "d_m": 16.8 * Mpc, "theta_obs": 42.0, "sigma_obs": 3.0,
             "ref": "EHT 2019, ApJL 875 L6 (arXiv:1906.11243)"},
    "SgrA*": {"M_Msun": 4.0e6, "d_m": 8.15 * kpc, "theta_obs": 51.8, "sigma_obs": 2.3,
              "ref": "EHT 2022 (arXiv:2311.08680)"},
}


def shadow_diameter_uas(M_Msun, d_m):
    """Schwarzschild shadow ANGULAR DIAMETER = 2 * 3sqrt(3) GM/(c^2 d)  [uas]."""
    GMc2 = G * M_Msun * Msun / c ** 2          # gravitational radius [m]
    r_shadow = 3.0 * np.sqrt(3.0) * GMc2       # shadow radius [m]
    return 2.0 * r_shadow / d_m * RAD_TO_UAS, GMc2


def main():
    rows = []
    for name, t in TARGETS.items():
        theta_gr, GMc2 = shadow_diameter_uas(t["M_Msun"], t["d_m"])
        r_ph = 3.0 * GMc2                       # Schwarzschild photon sphere [m]
        a_ph = G * t["M_Msun"] * Msun / r_ph ** 2   # Newtonian accel at photon sphere
        # (A) DEV / low-acceleration suppression: fractional deviation ~ a0/a_ph
        delta_DEV = a0_MOND / a_ph
        # (B) Planck suppression: ~ (l_Pl / r_ph)^2
        delta_Pl = (l_Pl / r_ph) ** 2
        # convert fractional deviations to a shadow-diameter shift (uas)
        dtheta_DEV = delta_DEV * theta_gr
        dtheta_Pl = delta_Pl * theta_gr
        consistent = dtheta_DEV < t["sigma_obs"] and dtheta_Pl < t["sigma_obs"]
        rows.append({
            "target": name, "ref": t["ref"],
            "theta_GR_uas": theta_gr, "theta_obs_uas": t["theta_obs"],
            "sigma_obs_uas": t["sigma_obs"],
            "r_photon_m": r_ph, "a_photon_m_s2": a_ph,
            "delta_DEV_frac (a0/a)": delta_DEV, "dtheta_DEV_uas": dtheta_DEV,
            "delta_Planck_frac": delta_Pl, "dtheta_Planck_uas": dtheta_Pl,
            "within_error_bars": bool(consistent),
        })

    # the GR baseline already matches EHT to ~1 sigma; the TEIC correction is negligible
    gr_ok = all(abs(r["theta_GR_uas"] - r["theta_obs_uas"]) < 2 * r["sigma_obs_uas"]
                for r in rows)
    max_dtheta = max(max(r["dtheta_DEV_uas"], r["dtheta_Planck_uas"]) for r in rows)
    discriminating = max_dtheta > 0.1 * min(r["sigma_obs_uas"] for r in rows)
    verdict = "CONSISTENTE" if not discriminating else "TENSAO/FALSIFICADO"

    payload = {"targets": rows, "a0_MOND_m_s2": a0_MOND,
               "GR_matches_EHT_2sigma": bool(gr_ok),
               "max_TEIC_shadow_shift_uas": max_dtheta,
               "is_discriminating_test": bool(discriminating),
               "verdict": verdict,
               "note": ("TEIC/DEV -> GR in the strong-field (high-acceleration, F=0) "
                        "regime; the quartic/DBI deviation at a BH photon sphere is "
                        "10^-12 (a0/a) to 10^-95 (Planck) of the shadow size, i.e. "
                        "12-95 orders of magnitude below the EHT error bars. CONSISTENT "
                        "but NON-DISCRIMINATING: EHT cannot test the TEIC quartic sector. "
                        "The '5-10%' figure in the prompt intro is not supported by any "
                        "suppression scale and is inconsistent with the 'inert where F=0' "
                        "structure of the bridge.")}
    import json
    (Path(__file__).resolve().parent / "F_EHT.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("F_EHT -- black-hole shadow: TEIC quartic correction vs EHT")
    print("=" * 74)
    for r in rows:
        print(f"\n{r['target']}  [{r['ref']}]")
        print(f"  shadow diameter: GR = {r['theta_GR_uas']:.1f} uas   "
              f"obs = {r['theta_obs_uas']:.1f} +- {r['sigma_obs_uas']:.1f} uas")
        print(f"  photon sphere: r_ph = {r['r_photon_m']:.2e} m   "
              f"a_ph = {r['a_photon_m_s2']:.2e} m/s^2  (a0 = {a0_MOND:.1e})")
        print(f"  delta_TEIC (DEV, a0/a)   = {r['delta_DEV_frac (a0/a)']:.2e}  "
              f"-> shadow shift {r['dtheta_DEV_uas']:.2e} uas")
        print(f"  delta_TEIC (Planck)      = {r['delta_Planck_frac']:.2e}  "
              f"-> shadow shift {r['dtheta_Planck_uas']:.2e} uas")
        print(f"  within error bars (<{r['sigma_obs_uas']} uas): {r['within_error_bars']}")
    print("-" * 74)
    print(f"GR matches EHT to 2sigma: {gr_ok}   max TEIC shift = {max_dtheta:.2e} uas")
    print(f"discriminating test: {discriminating}")
    print(f"VERDICT: {verdict} (non-discriminating: TEIC -> GR in strong field)")
    return payload


if __name__ == "__main__":
    main()
