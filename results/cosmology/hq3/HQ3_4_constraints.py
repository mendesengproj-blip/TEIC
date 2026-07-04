"""HQ3_4_constraints.py -- cross-constraints on the m_A PTA interpretation.

Charter HQ3-4.  Checks that an m_A whose f_GW is in the PTA band does not violate
existing bounds:

  1. BBN (Delta N_eff): the PROPAGATING SGWB radiated by m_A is a generous ceiling
     ~Psi_c^2; integrated it is far below the Delta N_eff < 0.3 bound (no extra
     radiation).  The KR line carries no propagating energy either.
  2. CMB: integrated Omega_GW h^2 << 1e-5 -> no spectral distortion.
  3. Lyman-alpha (inherited from FM4/FN3): m_A as 100% DM survives only at the top of
     the window (~2e-21 floor > Paper II ceiling 1.2e-22) -> for in-band masses m_A is
     SUBDOMINANT, which lowers the KR amplitude proportionally.
  4. Soliton-excluded window 1.3e-21 - 1.4e-20 eV: the in-band Paper II masses
     (<=1.2e-22 eV) sit BELOW it -> not affected.

Writes a JSON ledger + figure.  All bounds COMPARISON ONLY.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import hq3_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent
LYMAN_100PCT_FLOOR_EV = 2.0e-21      # FM4/FN3: m_A as 100% DM needs m >~ this


def main():
    # in-band representative masses
    masses = [4.14e-24, 1e-23, 3e-23, 1e-22, c.M_A_CEIL]

    # 1+2. radiated SGWB ceiling -> Delta N_eff.  Integrate ~ Psi_c^2 over ~1 e-fold.
    omega_gw_ceiling = max(float(c.omega_gw_propagating_bound(m)) for m in masses)
    omega_gw_h2_integrated = omega_gw_ceiling * c.H_LITTLE ** 2     # one decade, ceiling
    dNeff = float(c.delta_neff_from_omega_gw(omega_gw_h2_integrated))
    bbn_ok = dNeff < 0.3
    cmb_ok = omega_gw_h2_integrated < 1e-5

    # 3. Lyman-alpha: which in-band masses can be 100% DM?
    lyman = {f"{m:.2e}": bool(m >= LYMAN_100PCT_FLOOR_EV) for m in masses}
    any_100pct = any(lyman.values())

    # 4. soliton-excluded window
    soliton = {f"{m:.2e}": c.in_soliton_excluded(m) for m in masses}
    any_excluded = any(soliton.values())

    payload = {
        "bbn": {"omega_gw_ceiling": omega_gw_ceiling,
                "omega_gw_h2_integrated_ceiling": omega_gw_h2_integrated,
                "delta_Neff": dNeff, "bound": 0.3, "ok": bbn_ok},
        "cmb": {"omega_gw_h2_integrated": omega_gw_h2_integrated, "bound": 1e-5,
                "ok": cmb_ok},
        "lyman_alpha": {"floor_100pct_DM_eV": LYMAN_100PCT_FLOOR_EV,
                        "paper_II_ceiling_eV": c.M_A_CEIL,
                        "can_be_100pct_DM_in_band": lyman, "any": any_100pct,
                        "implication": "in-band masses are SUBDOMINANT DM -> KR "
                                       "amplitude scales down by the m_A fraction"},
        "soliton_excluded": {"window_eV": list(c.SOLITON_EXCL_EV),
                             "in_band_masses_excluded": soliton, "any": any_excluded},
        "all_ok": bbn_ok and cmb_ok and not any_excluded,
        "note": "all bounds COMPARISON ONLY; m_A from Paper II",
    }
    (OUT / "HQ3_4_constraints.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("HQ3-4  cross-constraints on the m_A PTA interpretation")
    print("=" * 74)
    print(f"  1. BBN  : radiated Omega_GW ceiling = {omega_gw_ceiling:.2e}, "
          f"Delta N_eff = {dNeff:.2e}  -> {'OK' if bbn_ok else 'VIOLATION'} (<0.3)")
    print(f"  2. CMB  : Omega_GW h^2 integrated = {omega_gw_h2_integrated:.2e}  "
          f"-> {'OK' if cmb_ok else 'VIOLATION'} (<1e-5)")
    print(f"  3. Lyman-alpha: 100%-DM floor {LYMAN_100PCT_FLOOR_EV:.1e} eV > "
          f"Paper II ceiling {c.M_A_CEIL:.1e} eV")
    print("       -> in-band m_A is SUBDOMINANT DM (KR amplitude scales with fraction)")
    print(f"  4. soliton-excluded {c.SOLITON_EXCL_EV[0]:.1e}-{c.SOLITON_EXCL_EV[1]:.1e} "
          f"eV: in-band masses excluded? {any_excluded}  (expect False)")
    print(f"  ALL constraints OK (excl. Lyman subdominance): {payload['all_ok']}")
    print(f"  saved {OUT/'HQ3_4_constraints.json'}")

    make_figure()
    return payload


def make_figure():
    fig, ax = plt.subplots(figsize=(9.2, 4.6))
    mm = np.logspace(np.log10(c.M_A_FLOOR), np.log10(1e-20), 400)

    # band-producing mass range (orange), Paper II window (grey), soliton-excluded (red)
    lo_b, hi_b = c.band_mass_window()
    ax.axvspan(lo_b, hi_b, color="orange", alpha=0.12, label="f_GW in NANOGrav band")
    ax.axvspan(c.M_A_FLOOR, c.M_A_CEIL, color="grey", alpha=0.10, label="Paper II window")
    ax.axvspan(*c.SOLITON_EXCL_EV, color="red", alpha=0.12, label="soliton-excluded")
    ax.axvline(LYMAN_100PCT_FLOOR_EV, color="purple", ls="--", lw=1.4,
               label=r"Lyman-$\alpha$ 100%-DM floor (2e-21 eV)")

    # the overlap (testable PTA window) highlighted
    ov = c.overlap_with_paper_II()
    if ov:
        ax.axvspan(ov[0], ov[1], color="green", alpha=0.18,
                   label=f"PTA-testable overlap {ov[0]:.1e}-{ov[1]:.1e} eV")

    ax.set_xscale("log")
    ax.set_yticks([])
    ax.set_xlabel(r"$m_A$ [eV]")
    ax.set_title("HQ3-4: in-band Paper II masses are below the soliton-excluded window;\n"
                 "as 100% DM they fail Lyman-$\\alpha$ (so subdominant), but no hard bound is violated")
    ax.legend(fontsize=8, loc="upper right", ncol=1)
    ax.set_xlim(c.M_A_FLOOR, 1e-20)
    fig.tight_layout()
    fig.savefig(OUT / "HQ3_4_constraints.png", dpi=130)
    print(f"  saved {OUT/'HQ3_4_constraints.png'}")


if __name__ == "__main__":
    main()
