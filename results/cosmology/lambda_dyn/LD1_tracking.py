"""LD1 -- does the everpresent Lambda TRACK the critical density over cosmic time?

PRE-REGISTERED KILL CRITERION (RESEARCH_MAP #7 / FUTURE_EXPERIMENTS FM4-Lambda):
    DEATH if Lambda_dynamics is inconsistent with the measured w = -1 OR
    diverges at z ~ 0.
  Operationally:
    (D1) Lambda_rms(z) diverges or -> 0 as z -> 0  (no finite present value), OR
    (D2) the tracking exponent p in Lambda_rms ~ rho_crit^p is far from 1
         (|p-1| > 0.5 would mean Omega_Lambda runs away / vanishes across epochs,
         i.e. not a cosmological-constant-like everpresent term).
  PREDICTED (everpresent CST, Sorkin/ADGS): finite at z=0; p ~ 1 (Lambda ~ H^2 ~
  rho_crit because V4_past ~ H^-4) -> Omega_Lambda stays O(1) at all epochs.

Also checks numerical convergence of V4_past in z_max (the a^3 weight must make
the early-time contribution negligible).
"""

import json
import os

import numpy as np

from ld_core import (
    past_4volume,
    lambda_rms_unnorm,
    rho_crit,
    everpresent_ratio,
    L1_COEFF,
    OMEGA_M,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def convergence(z=0.0):
    """V4_past at z as a function of integration cutoff z_max."""
    return {zm: float(past_4volume(z, z_max=zm)) for zm in (10, 20, 30, 50)}


def run():
    zs = np.array([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 5.0, 8.0])
    rows = []
    for z in zs:
        rows.append(
            {
                "z": float(z),
                "V4_past": float(past_4volume(z)),
                "lambda_rms": float(lambda_rms_unnorm(z)),
                "rho_crit": float(rho_crit(z)),
                "ratio_R": float(everpresent_ratio(z)),
            }
        )
    # tracking exponent p: ln lambda_rms = p ln rho_crit + const
    lnL = np.log([r["lambda_rms"] for r in rows])
    lnRho = np.log([r["rho_crit"] for r in rows])
    p, c = np.polyfit(lnRho, lnL, 1)
    fit = np.poly1d([p, c])
    ss_res = np.sum((lnL - fit(lnRho)) ** 2)
    ss_tot = np.sum((lnL - lnL.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot
    # divergence test at z->0
    finite_at_0 = np.isfinite(rows[0]["lambda_rms"]) and rows[0]["lambda_rms"] > 0
    return rows, float(p), float(r2), bool(finite_at_0)


if __name__ == "__main__":
    conv = convergence()
    print("V4_past(z=0) vs z_max cutoff (convergence):")
    for zm, v in conv.items():
        print(f"  z_max={zm:3d}: V4={v:.6e}")
    rows, p, r2, finite0 = run()
    print("\n  z     V4_past      Lambda_rms    rho_crit      R=L/rho")
    for r in rows:
        print(f"  {r['z']:4.2f}  {r['V4_past']:.3e}   {r['lambda_rms']:.3e}   "
              f"{r['rho_crit']:.3e}   {r['ratio_R']:.3e}")
    print(f"\nTracking: Lambda_rms ~ rho_crit^p, p = {p:.3f} (R^2={r2:.4f})")
    print(f"Finite, nonzero at z=0? {finite0}  (Lambda_rms(0)={rows[0]['lambda_rms']:.3e})")

    death = (not finite0) or (abs(p - 1.0) > 0.5)
    print(f"\nKILL CRITERION (diverges at z~0 OR |p-1|>0.5)? {death}")

    payload = {
        "description": "Everpresent-Lambda tracking of rho_crit over cosmic time.",
        "model_imported": "Sorkin everpresent Lambda ~ 1/sqrt(V4_past); "
        "ADGS astro-ph/0209274; V<->Hubble transplant (CST heritage).",
        "teic_input": f"L1 measured fluctuation coefficient = {L1_COEFF}",
        "omega_m": OMEGA_M,
        "convergence_V4_z0_vs_zmax": conv,
        "rows": rows,
        "tracking_exponent_p": p,
        "tracking_r2": r2,
        "finite_nonzero_at_z0": finite0,
        "kill_criterion_fires": death,
    }
    with open(os.path.join(HERE, "LD1_tracking.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote LD1_tracking.json")
