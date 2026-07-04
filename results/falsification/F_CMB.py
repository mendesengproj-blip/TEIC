"""F_CMB -- are T3D2's lattice monopoles Polyakov (vacuum instantons) or Dirac (relic
particles)?  Confront with the Parker bound.

T3D2 measured a monopole density rho_M ~ 0.41 (charged cubes per cube) in the compact-U(1)
vacuum of the 3D causal lattice.  Two readings:

  (A) PHYSICAL RELIC PARTICLES.  If rho_M counted real magnetic monopoles at the lattice
      (Planck) scale, the mass density would be ~ rho_M * rho_Planck -- absurdly above the
      Parker bound (~1e-19 g/cm^3 ~ 1e-16 kg/m^3).  We compute the ratio: it is ~1e112,
      i.e. GROSSLY FALSIFIED.  This very absurdity is the proof that the lattice monopoles
      are NOT physical relic particles.
  (B) POLYAKOV INSTANTONS (vacuum effect).  In compact U(1) gauge theory the monopoles are
      Euclidean tunnelling events (monopole-instantons) that disorder the vacuum, give the
      photon a mass and confine -- a Coulomb-gas / condensate property of the VACUUM, not a
      density of asymptotic particles.  The Parker bound (which constrains relic monopole
      PARTICLES moving through galactic B-fields) does not apply.  T3D2's "monopole plasma"
      is exactly this: the compact-U(1) (Polyakov) vacuum, NOT a relic abundance.

Honest verdict: CONSISTENT under (B), the correct reading of compact-U(1) lattice
monopoles -- with the explicit caveat that this means T3D2 does NOT predict a physical
relic-monopole abundance; the "plasma" is a vacuum/lattice phenomenon.  (Were they
physical particles, the theory would be falsified by ~112 orders of magnitude.)

ANTI-CIRCULARITY: rho_M is from T3D2 (lattice); the Parker bound and rho_Planck are cited
external numbers.  No fitting.
"""

from __future__ import annotations

import json
from pathlib import Path

# constants
m_Pl = 2.176e-8          # kg
l_Pl = 1.616e-35         # m
RHO_M_LATTICE = 0.41     # T3D2, charged cubes per cube
PARKER_BOUND_kg_m3 = 1e-16   # ~1e-19 g/cm^3 -> kg/m^3 (cited)


def main():
    rho_Planck = m_Pl / l_Pl ** 3                      # kg/m^3
    rho_A = RHO_M_LATTICE * rho_Planck                 # interpretation A: physical relics
    over_parker = rho_A / PARKER_BOUND_kg_m3

    payload = {
        "rho_M_lattice": RHO_M_LATTICE,
        "rho_Planck_kg_m3": rho_Planck,
        "interpretation_A_relic_density_kg_m3": rho_A,
        "parker_bound_kg_m3": PARKER_BOUND_kg_m3,
        "A_over_parker": over_parker,
        "interpretation_A_verdict": "GROSSLY FALSIFIED (~1e112 over Parker) -> NOT physical relics",
        "monopole_type_in_T3D2": "Polyakov (compact-U(1) monopole-instantons; vacuum/condensate)",
        "interpretation_B_constrained_by_parker": False,
        "verdict": "CONSISTENTE",
        "note": ("The compact-U(1) lattice monopoles of T3D2 are Polyakov instantons "
                 "(Euclidean tunnelling events disordering the vacuum / generating the "
                 "photon mass / confining), NOT asymptotic relic particles, so the Parker "
                 "bound does not apply -> CONSISTENT. Caveat: this means T3D2's monopole "
                 "plasma is a vacuum phenomenon, NOT a prediction of relic monopoles; the "
                 "absurd interpretation-A overshoot (~1e112) confirms they cannot be "
                 "physical particles."),
    }
    (Path(__file__).resolve().parent / "F_CMB.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("F_CMB -- monopoles: Polyakov (vacuum) vs Dirac (relic) and the Parker bound")
    print("=" * 74)
    print(f"rho_M (T3D2 lattice)      = {RHO_M_LATTICE}")
    print(f"rho_Planck                = {rho_Planck:.2e} kg/m^3")
    print(f"(A) as physical relics    = {rho_A:.2e} kg/m^3")
    print(f"    Parker bound          = {PARKER_BOUND_kg_m3:.0e} kg/m^3")
    print(f"    overshoot             = {over_parker:.1e}x  -> GROSSLY FALSIFIED")
    print(f"(B) Polyakov instantons   = vacuum effect, NOT relic particles")
    print(f"    constrained by Parker = False")
    print("-" * 74)
    print("VERDICT: CONSISTENTE (Polyakov reading); T3D2 monopoles are a vacuum/lattice")
    print("         phenomenon, NOT a physical relic-monopole prediction.")
    return payload


if __name__ == "__main__":
    main()
