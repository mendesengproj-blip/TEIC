"""KR2 -- confront the m_A KR line with PUBLISHED PTA direct-search limits.

PRE-REGISTERED KILL CRITERION (written before running)
------------------------------------------------------
The m_A KR line is a falsifiable prediction in the PTA band.  Define
    f_max(m) = max ULDM fraction allowed by the published PTA gravitational
               direct search at mass m  (rho_limit / rho_local).

  DEATH (m_A as DM ruled out by PTA):
      the published gravitational search excludes f_frac = 1 (i.e. f_max(m) < 1)
      across the ENTIRE HQ3 overlap window AND m_A is required to be ~100% DM
      there  -> the line should have been seen; m_A=CDM falsified in the band.

  PARTIAL (constraint, no death):
      f_max(m) < 1 over only PART of the window, OR an independent bound (Lyman-a)
      already forces m_A subdominant so the PTA non-detection is consistent.

  CONSISTENT (no constraint bites):
      f_max(m) >= 1 across the window (even 100% local-DM ULDM is allowed) ->
      current PTA searches do not yet probe the m_A line; future probe only.

Independent cross-check imported (NOT from this network):
    Fuzzy-DM structure bounds (Lyman-a / high-z) require m >~ 1e-21 eV for ULDM
    to be ~100% of DM.  In the PTA band (m <~ 1e-22 eV) m_A MUST be subdominant.
    => the physically relevant question is whether PTA constrains the SUBDOMINANT
    fraction better than Lyman-a does.
"""

import json
import os

import numpy as np

from kr_pta_core import (
    ppta_fraction_limit,
    ppta_rho_limit,
    f_signal,
    M_A_PTA_LO,
    M_A_PTA_HI,
    RHO_LOCAL,
    PPTA_RHO_LIMIT_AT_1e23,
)

HERE = os.path.dirname(os.path.abspath(__file__))

# fuzzy-DM 100%-of-DM lower bound (Lyman-a / high-z), literature: m >~ 1e-21 eV
FUZZY_DM_100PCT_LOWER_EV = 1e-21


def run():
    masses = np.geomspace(M_A_PTA_LO, M_A_PTA_HI, 25)
    rows = []
    for m in masses:
        fmax = ppta_fraction_limit(m)
        rows.append(
            {
                "m_eV": float(m),
                "f_Hz": float(f_signal(m)),
                "ppta_rho_limit_GeVcm3": float(ppta_rho_limit(m)),
                "ppta_fraction_limit": float(fmax),
                "excludes_100pct_DM": bool(fmax < 1.0),
                "lyman_alpha_allows_100pct": bool(m >= FUZZY_DM_100PCT_LOWER_EV),
            }
        )
    # where does PPTA reach f_max = 1?
    m_cross = 1e-23 * np.sqrt(1.0 / (PPTA_RHO_LIMIT_AT_1e23 / RHO_LOCAL))
    excluded_anywhere = any(r["excludes_100pct_DM"] for r in rows)
    return rows, m_cross, excluded_anywhere


if __name__ == "__main__":
    rows, m_cross, excluded_anywhere = run()
    print("  m_A [eV]    rho_lim[GeV/cm3]  f_max(PPTA)  excl.100%?")
    for r in rows[::3]:
        print(
            f"  {r['m_eV']:.2e}    {r['ppta_rho_limit_GeVcm3']:.2e}        "
            f"{r['ppta_fraction_limit']:.1f}        "
            f"{'YES' if r['excludes_100pct_DM'] else 'no'}"
        )
    print()
    print(f"PPTA reaches f_max=1 (100% local DM) at m ~ {m_cross:.2e} eV "
          f"(below window low edge {M_A_PTA_LO:.2e})")
    print(f"100%-ULDM excluded ANYWHERE in the HQ3 overlap window? {excluded_anywhere}")
    print(f"Lyman-a forces m_A subdominant for m < {FUZZY_DM_100PCT_LOWER_EV:.0e} eV "
          f"(= the whole PTA band)")

    # verdict logic
    if excluded_anywhere and all(
        not r["lyman_alpha_allows_100pct"] for r in rows
    ):
        # PTA would need to exclude 100% across window AND m_A required 100% there
        verdict = "DEATH"
    elif excluded_anywhere:
        verdict = "PARTIAL"
    else:
        verdict = "CONSISTENT"
    print(f"\nKILL-CRITERION VERDICT: {verdict}")

    payload = {
        "description": "Confrontation of the m_A KR line with published PTA "
        "gravitational direct-search limits.",
        "ppta_benchmark": {
            "ref": "Porayko et al. (PPTA) 2018, arXiv:1810.03227",
            "rho_limit_GeVcm3_at_1e-23eV": PPTA_RHO_LIMIT_AT_1e23,
            "note": "gravitational/universal KR signal; rho<6 at m<=1e-23 eV (95%)",
        },
        "lyman_alpha_100pct_lower_eV": FUZZY_DM_100PCT_LOWER_EV,
        "rho_local_GeVcm3": RHO_LOCAL,
        "m_fmax_eq_1_eV": float(m_cross),
        "excluded_100pct_anywhere_in_window": bool(excluded_anywhere),
        "verdict": verdict,
        "rows": rows,
    }
    with open(os.path.join(HERE, "KR2_confront.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote KR2_confront.json")
