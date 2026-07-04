"""KR1 -- the m_A Khmelnitsky-Rubakov line across the PTA band.

Maps the Paper II m_A window into the observable KR signal (frequency,
characteristic strain, timing-residual amplitude) assuming the line carries a
fraction f_frac of the local DM density.  No PTA limit yet (that is KR2); this
task just builds the signal the m_A WOULD produce, so KR2's confrontation is
transparent.
"""

import json
import os

import numpy as np

from kr_pta_core import (
    f_signal,
    h_c,
    timing_residual_s,
    RHO_LOCAL,
    M_A_SPARC_LOWER,
    M_A_PTA_LO,
    M_A_PTA_HI,
    PTA_F_LO,
    PTA_F_HI,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def run():
    masses = np.geomspace(M_A_PTA_LO, M_A_PTA_HI, 25)
    rows = []
    for m in masses:
        rows.append(
            {
                "m_eV": float(m),
                "f_Hz": float(f_signal(m)),
                "in_pta_band": bool(PTA_F_LO <= f_signal(m) <= PTA_F_HI),
                "h_c_frac1": float(h_c(m, RHO_LOCAL)),  # 100% local DM
                "timing_residual_ns_frac1": float(timing_residual_s(m, RHO_LOCAL) * 1e9),
            }
        )
    return rows


if __name__ == "__main__":
    rows = run()
    print(f"m_A window for KR-PTA overlap: [{M_A_PTA_LO:.2e}, {M_A_PTA_HI:.2e}] eV")
    print(f"SPARC lower bound on m_A (Paper II): {M_A_SPARC_LOWER:.2e} eV")
    print(f"PTA band: f in [{PTA_F_LO:.1e}, {PTA_F_HI:.1e}] Hz\n")
    print("  m_A [eV]     f [Hz]     in-band   h_c(f=1)   dt(f=1) [ns]")
    for r in rows[::3]:
        print(
            f"  {r['m_eV']:.2e}  {r['f_Hz']:.2e}   "
            f"{'yes' if r['in_pta_band'] else 'no ':3s}    "
            f"{r['h_c_frac1']:.2e}  {r['timing_residual_ns_frac1']:.2f}"
        )

    payload = {
        "description": "m_A KR line across the PTA band (signal model only).",
        "model": "Khmelnitsky-Rubakov 2014 (arXiv:1309.5888), Eqs 12/21/22.",
        "rho_local_GeVcm3": RHO_LOCAL,
        "m_A_window_eV": [M_A_PTA_LO, M_A_PTA_HI],
        "m_A_sparc_lower_eV": M_A_SPARC_LOWER,
        "pta_band_Hz": [PTA_F_LO, PTA_F_HI],
        "rows": rows,
    }
    with open(os.path.join(HERE, "KR1_signal.json"), "w") as f:
        json.dump(payload, f, indent=2)
    print("\nwrote KR1_signal.json")
