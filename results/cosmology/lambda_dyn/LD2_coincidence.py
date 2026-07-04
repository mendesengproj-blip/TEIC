"""LD2 -- the coincidence problem and the effective equation of state.

Two diagnostics, both reading the LD1 tracking exponent p:

(A) COINCIDENCE ("why now"): in LCDM, Lambda=const so Omega_Lambda(z) was tiny in
    the past and -> 1 in the future; today (Omega_Lambda ~ Omega_m) is a special
    epoch.  Everpresent Lambda tracks rho_crit (LD1: p ~ 1), so Omega_Lambda stays
    O(1) at ALL epochs -> no special 'now'.  We compute Omega_Lambda(z) for both
    and report over how many e-folds each stays O(1) (0.1 < Omega_Lambda < 0.9).

(B) EFFECTIVE w from the tracking ENVELOPE: w_eff = -1 - (1/3) dln rho_Lambda/dlna
    with rho_Lambda ~ rho_crit^p.  HONESTY: everpresent Lambda enters Einstein's
    equations as a genuine cosmological-constant term at EACH instant (w = -1
    instantaneously); its MAGNITUDE does a stochastic walk whose RMS envelope
    tracks rho_crit.  So this 'w_eff' is the apparent EoS of the slowly-drifting
    ENVELOPE, NOT a fluid w -- it is the quantity the everpresent-Lambda
    literature (Zwane-Afshordi-Sorkin 2018) fits to data and finds can deviate
    from -1.  We report it as a diagnostic, explicitly NOT as 'the field has
    w != -1'.

Background is imported flat-LCDM E(z) (declared); rho_crit = E^2.  This is a
consistency diagnostic, not a self-consistent stochastic solve.
"""

import json
import os

import numpy as np

from ld_core import E, rho_crit, OMEGA_M, OMEGA_L

HERE = os.path.dirname(os.path.abspath(__file__))

P_TRACK = 1.107          # from LD1
OMEGA_L0 = OMEGA_L       # everpresent normalised to match Omega_Lambda(0)=0.69


def omega_lambda_lcdm(z):
    rho_L = OMEGA_L0
    rho_m = OMEGA_M * (1.0 + z) ** 3
    return rho_L / (rho_L + rho_m)


def omega_lambda_everpresent(z, p=P_TRACK):
    # rho_Lambda tracks rho_crit^p, normalised so Omega_Lambda(0)=OMEGA_L0.
    rho_L = OMEGA_L0 * (rho_crit(z) / rho_crit(0.0)) ** p
    rho_m = OMEGA_M * (1.0 + z) ** 3
    return rho_L / (rho_L + rho_m)


def w_eff_envelope(z, p=P_TRACK, dz=1e-3):
    # w = -1 - (1/3) dln rho_L / dln a ; rho_L ~ rho_crit^p ; a=1/(1+z)
    lnrho = lambda zz: p * np.log(rho_crit(zz))
    dlnrho_dz = (lnrho(z + dz) - lnrho(z - dz)) / (2 * dz)
    dlna_dz = -1.0 / (1.0 + z)
    dlnrho_dlna = dlnrho_dz / dlna_dz
    return -1.0 - dlnrho_dlna / 3.0


def efolds_order1(omega_fn, z_hi=1000.0, n=4000):
    """Number of e-folds in ln(1+z) over which 0.1 < Omega_Lambda < 0.9."""
    zs = np.expm1(np.linspace(0, np.log(1 + z_hi), n))
    om = np.array([omega_fn(z) for z in zs])
    mask = (om > 0.1) & (om < 0.9)
    lna = np.log(1 + zs)
    if not mask.any():
        return 0.0
    return float(lna[mask].max() - lna[mask].min())


def run():
    zs = [0.0, 0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1000.0]
    rows = []
    for z in zs:
        rows.append(
            {
                "z": float(z),
                "omega_L_lcdm": float(omega_lambda_lcdm(z)),
                "omega_L_everpresent": float(omega_lambda_everpresent(z)),
                "w_eff_envelope": float(w_eff_envelope(z)) if z > 0 else float(w_eff_envelope(1e-4)),
            }
        )
    ef_lcdm = efolds_order1(omega_lambda_lcdm)
    ef_ever = efolds_order1(omega_lambda_everpresent)
    return rows, ef_lcdm, ef_ever


if __name__ == "__main__":
    rows, ef_lcdm, ef_ever = run()
    print("  z       Omega_L(LCDM)  Omega_L(ever)  w_eff(envelope)")
    for r in rows:
        print(f"  {r['z']:7.1f}   {r['omega_L_lcdm']:.4f}        "
              f"{r['omega_L_everpresent']:.4f}        {r['w_eff_envelope']:+.3f}")
    print(f"\ne-folds with 0.1<Omega_L<0.9 (coincidence window):")
    print(f"  LCDM (Lambda=const):     {ef_lcdm:.2f}  (narrow -> 'now' is special)")
    print(f"  everpresent (tracking):  {ef_ever:.2f}  (wide -> no special epoch)")
    print(f"\nw_eff(z=0) from envelope = {rows[0]['w_eff_envelope']:+.3f}")
    print("  (instantaneous term is w=-1 by construction; envelope drift gives the")
    print("   apparent EoS the everpresent-Lambda literature fits -- NOT a fluid w)")

    payload = {
        "description": "Coincidence-problem dissolution + envelope effective w "
        "for everpresent Lambda.",
        "p_track": P_TRACK,
        "omega_m": OMEGA_M,
        "omega_L0": OMEGA_L0,
        "rows": rows,
        "efolds_order1_lcdm": ef_lcdm,
        "efolds_order1_everpresent": ef_ever,
        "w_eff_envelope_z0": rows[0]["w_eff_envelope"],
        "honesty": "w_eff is the apparent EoS of the slowly-drifting RMS envelope; "
        "everpresent Lambda is instantaneously a true cosmological-constant term "
        "(w=-1). Background imported (flat LCDM). Consistency diagnostic only.",
    }
    with open(os.path.join(HERE, "LD2_coincidence.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote LD2_coincidence.json")
