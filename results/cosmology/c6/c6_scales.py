"""c6_scales.py -- vortex scales for C6_QUANTIZED_VORTICES (C6-3).

ANALYTIC scale calculator for the C6 investigation: IF the m_A coherent condensate
of FM4 admits the Madelung velocity v = (hbar/m_A) grad(theta) (C6-1/C6-2, candidate
1), then its U(1) vortices carry the quantized circulation

    circ = closed-loop integral of v.dl = n * h / m_A          (n integer)

This module computes, with hbar EXTERNAL (declared input) and m_A from the Paper II
window (NOT refitted here), the two physical scales of such vortices:

  * the de Broglie / healing core radius     xi = hbar / (m_A v)
    (the fuzzy-DM granule size; equals the Compton length lambda_C = hbar/(m_A c)
     blown up by c/v -- so it is c/v ~ 1500x LARGER than the FN4 screening scale
     lambda_A = 17.3 pc, which is the Compton length at v=c);

  * the inter-vortex separation in a halo rotating at Omega = v_rot/R, from the
    Feynman rotating-superfluid vortex areal density
        n_v = 2 Omega / (h/m_A)   ->   d_v = n_v^(-1/2).

Comparison anchors: lambda_A = 17.3 pc (FN4 MOND screening, = hbar/(m_A c) at floor),
globular-cluster scale (~pc-tens of pc), kpc halo substructure.

Anti-circularity: hbar and m_A are DECLARED INPUTS (hbar external, m_A from Paper II);
no observational structure value is inserted.  This tests CONSISTENCY of the vortex
scale with known hbar, not a derivation of hbar.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent

# ---- declared external constants (SI) ----
HBAR = 1.054571817e-34      # J*s          (EXTERNAL input -- not derived by TEIC)
HBAR_EV_S = 6.582119569e-16  # eV*s
H_PLANCK = 2 * np.pi * HBAR  # J*s
C_SI = 2.99792458e8          # m/s
EV_TO_KG = 1.782661921e-36   # kg per eV/c^2
PC_M = 3.0856775815e16       # m per parsec
KPC_M = 1e3 * PC_M
KMS = 1e3                    # m/s per km/s

# ---- Paper II vector-mass window (declared input, NOT refitted) ----
M_A_FLOOR = 3.7e-25          # eV  (Paper II lower bound; gives lambda_A = 17.3 pc)
M_A_TOP = 1.2e-22            # eV  (Paper II upper bound)
M_A_GRID = np.array([3.7e-25, 1e-24, 1e-23, 1e-22, 1.2e-22])  # eV

# FN4 anchor
LAMBDA_A_PC = 17.3           # pc  (FN4 MOND screening scale = hbar/(m_A c) at floor)


def compton_pc(m_eV):
    """Reduced Compton length lambda_C = hbar/(m_A c) in pc (= FN4 lambda_A at floor)."""
    m_kg = m_eV * EV_TO_KG
    return HBAR / (m_kg * C_SI) / PC_M


def healing_core_pc(m_eV, v_kms):
    """de Broglie / healing vortex-core radius xi = hbar/(m_A v) in pc."""
    m_kg = m_eV * EV_TO_KG
    v = v_kms * KMS
    return HBAR / (m_kg * v) / PC_M


def debroglie_pc(m_eV, v_kms):
    """Full de Broglie wavelength lambda_dB = h/(m_A v) = 2 pi xi in pc."""
    return 2 * np.pi * healing_core_pc(m_eV, v_kms)


def circulation_quantum(m_eV):
    """Quantum of circulation kappa_circ = h/m_A in m^2/s (one winding, n=1)."""
    m_kg = m_eV * EV_TO_KG
    return H_PLANCK / m_kg


def intervortex_sep_pc(m_eV, v_rot_kms, R_kpc):
    """Inter-vortex separation d_v in pc for a halo rotating at Omega = v_rot/R.
    Feynman density n_v = 2 Omega/(h/m_A); d_v = n_v^(-1/2)."""
    omega = (v_rot_kms * KMS) / (R_kpc * KPC_M)        # 1/s
    kappa = circulation_quantum(m_eV)                  # m^2/s
    n_v = 2 * omega / kappa                            # 1/m^2
    d_v = n_v ** -0.5                                  # m
    return d_v / PC_M, n_v


def n_vortices(m_eV, v_rot_kms, R_kpc):
    """Number of vortices threading a halo of radius R (area pi R^2)."""
    _, n_v = intervortex_sep_pc(m_eV, v_rot_kms, R_kpc)
    area = np.pi * (R_kpc * KPC_M) ** 2
    return n_v * area


# representative SPARC-like galaxies (v_flat, halo radius)
GALAXIES = {
    "dwarf (v=50, R=5 kpc)":        dict(v=50.0, R=5.0),
    "median SPARC (v=120, R=15 kpc)": dict(v=120.0, R=15.0),
    "massive spiral (v=200, R=30 kpc)": dict(v=200.0, R=30.0),
}
V_VIR = 200.0   # km/s typical virial velocity for the healing-core scale


def main():
    out = {"inputs": {"hbar_Js": HBAR, "m_A_window_eV": [M_A_FLOOR, M_A_TOP],
                      "lambda_A_pc": LAMBDA_A_PC, "v_vir_kms": V_VIR},
           "per_mass": [], "intervortex": []}

    print("=" * 72)
    print("C6-3  VORTEX SCALES  (hbar EXTERNAL, m_A from Paper II)")
    print("=" * 72)
    print(f"\nCheck: lambda_C(m_A=floor={M_A_FLOOR:.2e} eV) = {compton_pc(M_A_FLOOR):.2f} pc "
          f"  (FN4 lambda_A = {LAMBDA_A_PC} pc -- must match)")

    print("\n--- core / de Broglie scales at v_vir = 200 km/s ---")
    print(f"{'m_A [eV]':>12} {'lambda_C [pc]':>14} {'xi_core [pc]':>14} "
          f"{'lambda_dB [pc]':>15} {'kappa_circ[m2/s]':>17}")
    for m in M_A_GRID:
        lc = compton_pc(m)
        xi = healing_core_pc(m, V_VIR)
        ldb = debroglie_pc(m, V_VIR)
        kc = circulation_quantum(m)
        out["per_mass"].append(dict(m_eV=float(m), lambda_C_pc=lc, xi_core_pc=xi,
                                    lambda_dB_pc=ldb, kappa_circ_m2s=kc))
        print(f"{m:>12.2e} {lc:>14.4g} {xi:>14.4g} {ldb:>15.4g} {kc:>17.4g}")

    print("\n--- inter-vortex separation d_v in rotating halos ---")
    for gname, g in GALAXIES.items():
        print(f"\n  {gname}:  Omega = {g['v']}/{g['R']} kpc")
        print(f"    {'m_A [eV]':>12} {'d_v [pc]':>12} {'d_v [kpc]':>10} "
              f"{'N_vort':>12} {'d_v/lambda_A':>13}")
        for m in M_A_GRID:
            dv_pc, _ = intervortex_sep_pc(m, g["v"], g["R"])
            nv = n_vortices(m, g["v"], g["R"])
            out["intervortex"].append(dict(galaxy=gname, m_eV=float(m),
                                           d_v_pc=dv_pc, N_vort=float(nv),
                                           dv_over_lambdaA=dv_pc / LAMBDA_A_PC))
            print(f"    {m:>12.2e} {dv_pc:>12.4g} {dv_pc/1e3:>10.3g} "
                  f"{nv:>12.3g} {dv_pc/LAMBDA_A_PC:>13.4g}")

    (HERE / "C6_3_scales.json").write_text(json.dumps(out, indent=2))
    print(f"\nwrote {HERE/'C6_3_scales.json'}")
    make_figure(out)


def make_figure(out):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"(figure skipped: {e})")
        return

    m = np.array([d["m_eV"] for d in out["per_mass"]])
    xi = np.array([d["xi_core_pc"] for d in out["per_mass"]])
    ldb = np.array([d["lambda_dB_pc"] for d in out["per_mass"]])
    lc = np.array([d["lambda_C_pc"] for d in out["per_mass"]])

    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    ax.loglog(m, lc, "s--", color="0.5", label=r"$\lambda_C=\hbar/m_Ac$ (FN4 screening)")
    ax.loglog(m, xi, "o-", color="C0", label=r"$\xi=\hbar/m_Av$ (vortex core, $v=200$ km/s)")
    ax.loglog(m, ldb, "^-", color="C1", label=r"$\lambda_{dB}=h/m_Av$ (de Broglie)")

    # inter-vortex for median galaxy
    med = [d for d in out["intervortex"] if d["galaxy"].startswith("median")]
    mm = np.array([d["m_eV"] for d in med])
    dv = np.array([d["d_v_pc"] for d in med])
    ax.loglog(mm, dv, "D-", color="C3", label=r"$d_v$ (inter-vortex, median SPARC halo)")

    # reference scales (horizontal bands)
    for y, lab, col in [(17.3, r"$\lambda_A=17.3$ pc (FN4)", "0.3"),
                        (10.0, "globular cluster ~10 pc", "0.6"),
                        (1000.0, "1 kpc (halo substructure)", "green")]:
        ax.axhline(y, ls=":", color=col, lw=1)
        ax.text(m.min() * 1.1, y * 1.15, lab, fontsize=8, color=col)

    ax.axvspan(M_A_FLOOR, M_A_TOP, alpha=0.07, color="purple")
    ax.text(M_A_FLOOR * 1.3, xi.max() * 0.5, "Paper II window", fontsize=8,
            color="purple", rotation=90, va="top")

    ax.set_xlabel(r"$m_A$ [eV]")
    ax.set_ylabel("comoving / physical scale [pc]")
    ax.set_title("C6 vortex scales vs $m_A$ (Paper II window)\n"
                 r"physical quantization $\oint v\cdot dl = n\,h/m_A$, $\hbar$ external")
    ax.legend(fontsize=8, loc="upper right")
    ax.grid(True, which="both", alpha=0.2)
    fig.tight_layout()
    fig.savefig(HERE / "C6_3_scales.png", dpi=130)
    print(f"wrote {HERE/'C6_3_scales.png'}")


if __name__ == "__main__":
    main()
