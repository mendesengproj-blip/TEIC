"""FN3_4_constraints.py -- observational constraints on the m_A relic.

Charter FN3-4.  For each (m_A, f_A) test point: (1) Omega <= 0.12 (no DM over-
production); (2) Lyman-alpha at k~3/Mpc (the FM4-4 wall); (3) subdominance before
matter-radiation equality (m_A must not dominate at z>z_eq); (4) the ULDM Jeans
mass vs observed z~0 structure.  Builds the allowed region in (m_A, f_A).

Reuses the FM4 Lyman-alpha transfer (anti-circular: bound is COMPARISON ONLY).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fn3_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent
MASSES = [c.M_A_FLOOR, 1e-24, 1e-23, 1e-22]
F_AS = [1e15, 1e16, 1e17, 1e18]
LYA_FLOOR = c.lyman_safe_100pct_floor()              # ~2e-21 eV for 100% DM


def main():
    # (1) Lyman-alpha: at the 0.12-contour f_A, m_A is ~100% of DM -> use frac = Omega/0.12
    lya_rows = []
    for m in MASSES:
        f012 = c.f_A_for_target(m)
        frac = 1.0                                    # at the contour it IS 100% of DM
        supp = c.lyman_suppression(m, frac)
        lya_rows.append({"m_eV": m, "frac_at_contour": frac,
                         "P_supp_k3": float(supp),
                         "lya_safe": bool(supp >= 0.95)})

    # (2) which f_A keeps Omega <= 0.12 (no overproduction) at each mass
    overprod = {}
    for m in MASSES:
        overprod[f"{m:.2e}"] = {f"{f:.0e}": bool(c.omega_canonical(m, f) > 0.12)
                                for f in F_AS}

    # (3) subdominance before equality: rho_mA(z_eq)/rho_DM(z_eq).  Cold m_A redshifts
    #     as DM (a^-3) once oscillating; onset a_osc << a_eq for all our masses, so by
    #     z_eq it already tracks DM -- its fraction of DM is just Omega_mA/0.12, the
    #     SAME at all z after onset.  Report a_osc << a_eq as the subdominance check.
    a_eq = 1.0 / (1.0 + c.Z_EQ)
    sub_rows = []
    for m in MASSES:
        a_osc = c.a_osc_of(m)
        sub_rows.append({"m_eV": m, "a_osc": float(a_osc), "a_eq": float(a_eq),
                         "oscillating_before_eq": bool(a_osc < a_eq)})

    # (4) Jeans mass vs z~0 structure (dwarf-galaxy halos ~1e8-1e9 Msun observed)
    jeans_rows = [{"m_eV": m, "M_J_Msun": float(c.jeans_mass_Msun(m)),
                   "suppresses_observed_dwarfs": bool(c.jeans_mass_Msun(m) > 1e9)}
                  for m in MASSES]

    payload = {
        "lyman_alpha": lya_rows, "lya_safe_floor_eV": LYA_FLOOR,
        "overproduction_Omega_gt_012": overprod,
        "subdominance_before_eq": sub_rows,
        "jeans_mass": jeans_rows,
        "paper_II_window_eV": [c.M_A_FLOOR, c.M_A_CEIL],
        "key_conflict": ("100%-DM relic (Omega=0.12) at Paper II masses (<=1.2e-22 eV) "
                         "is below the Lyman-alpha 100%-DM floor (~2e-21 eV) -> excluded "
                         "as dominant DM; survives only as a subdominant fraction."),
    }
    (OUT / "FN3_4_constraints.json").write_text(json.dumps(payload, indent=2))

    print("=" * 76)
    print("FN3-4  observational constraints on the m_A relic")
    print("=" * 76)
    print("  Lyman-alpha (m_A as 100% of DM, P-suppression at k=3/Mpc; need >=0.95):")
    for r in lya_rows:
        print(f"    m_A={r['m_eV']:>8.2e} eV: P_supp={r['P_supp_k3']:.3f}  "
              f"-> {'SAFE' if r['lya_safe'] else 'EXCLUDED as 100% DM'}")
    print(f"  Lyman-alpha 100%-DM floor: m_A >= {LYA_FLOOR:.1e} eV "
          f"(above the Paper II ceiling {c.M_A_CEIL:.1e} eV)")
    print("\n  Subdominance before equality (a_osc << a_eq = {:.2e}):".format(a_eq))
    for r in sub_rows:
        print(f"    m_A={r['m_eV']:>8.2e} eV: a_osc={r['a_osc']:.2e}  "
              f"oscillating(cold) before eq: {r['oscillating_before_eq']}")
    print("\n  ULDM Jeans mass (suppresses halos below M_J):")
    for r in jeans_rows:
        print(f"    m_A={r['m_eV']:>8.2e} eV: M_J={r['M_J_Msun']:.2e} Msun  "
              f"{'-> suppresses observed dwarfs' if r['suppresses_observed_dwarfs'] else 'OK'}")
    print(f"\n  KEY CONFLICT: {payload['key_conflict']}")
    print(f"  saved {OUT/'FN3_4_constraints.json'}")

    make_figure(lya_rows)
    return payload


def make_figure(lya_rows):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))

    # left: allowed region in (m_A, f_A).  Bands: Omega=0.12 contour, overproduction,
    # Lyman-alpha exclusion of the 100%-DM contour at Paper II masses.
    mm = np.logspace(np.log10(c.M_A_FLOOR), np.log10(c.M_A_CEIL), 80)
    f012 = c.f_A_for_target(mm)
    ax[0].fill_between(mm, f012, 1e19, color="red", alpha=0.12,
                       label="Omega > 0.12 (overproduced)")
    ax[0].fill_between(mm, 1e14, f012, color="green", alpha=0.10,
                       label="Omega < 0.12 (subdominant, allowed)")
    ax[0].loglog(mm, f012, "k-", lw=2, label="Omega = 0.12 (100% DM)")
    # the 100% DM line is Lyman-alpha-excluded across the whole window (m<2e-21)
    ax[0].loglog(mm, f012, "x", color="red", ms=4, markevery=8,
                 label="...but Lyman-alpha-excluded as 100% DM")
    ax[0].axhline(1e17, color="blue", ls=":", lw=1, label="GUT scale 1e17 GeV")
    ax[0].set_xlabel("m_A [eV]"); ax[0].set_ylabel("f_A [GeV]")
    ax[0].set_ylim(1e14, 1e19)
    ax[0].set_title("FN3-4: allowed (m_A, f_A) region")
    ax[0].legend(fontsize=7, loc="lower left")

    # right: Lyman-alpha P-suppression for 100% DM vs mass; floor at 2e-21
    mlya = np.logspace(np.log10(c.M_A_FLOOR), np.log10(5e-21), 120)
    supp = [c.lyman_suppression(m, 1.0) for m in mlya]
    ax[1].semilogx(mlya, supp, "b-", lw=1.5)
    ax[1].axhline(0.95, color="k", ls="--", lw=1, label="Lyman-alpha limit (0.95)")
    ax[1].axvspan(c.M_A_FLOOR, c.M_A_CEIL, color="grey", alpha=0.15,
                  label="Paper II window")
    ax[1].axvline(LYA_FLOOR, color="red", ls=":", lw=1.5,
                  label="100%-DM safe floor ~2e-21 eV")
    ax[1].set_xlabel("m_A [eV]"); ax[1].set_ylabel("P(k=3/Mpc) for 100% DM")
    ax[1].set_ylim(0, 1.05)
    ax[1].set_title("FN3-4: Lyman-alpha excludes 100%-DM at Paper II masses")
    ax[1].legend(fontsize=7, loc="lower right")

    fig.suptitle("FN3-4: Omega~0.12 is reachable, but as 100% DM it is Lyman-alpha-excluded "
                 "at Paper II masses (the FM4 wall) -> m_A is subdominant DM", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "FN3_4_constraints.png", dpi=130)
    print(f"  saved {OUT/'FN3_4_constraints.png'}")


if __name__ == "__main__":
    main()
