"""HQ3_2_amplitude.py -- amplitude of the m_A signal vs NANOGrav.

Charter HQ3-2.  Two physically distinct amplitudes, kept separate:

  (a) the KHMELNITSKY-RUBAKOV monochromatic metric oscillation Psi_c = pi G rho/omega^2
      -- the real PTA observable for a DM condensate (a LINE at f_GW).  Compared with
      the NANOGrav broadband strain h_c(f_GW) at the same frequency.

  (b) the PROPAGATING stochastic GW background radiated by the condensate -- an
      order-of-magnitude UPPER BOUND (Psi_c^2), shown to be astronomically below the
      NANOGrav Omega_GW ~ 1e-8.  A homogeneous condensate radiates no on-shell graviton.

Scans the masses inside the band-overlap.  Reports Psi_c (first-principles + KR
literature), the strain ratio to NANOGrav, and the SGWB Omega_GW comparison.  Also
folds in the FM4/FN3 result that for most of the window m_A is SUBDOMINANT DM
(frac<1), which lowers Psi_c proportionally.  m_A not adjusted; A_yr COMPARISON ONLY.
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
# masses inside the band-overlap, plus the window edges for context
MASSES = [4.14e-24, 5e-24, 1e-23, 3e-23, 1e-22, c.M_A_CEIL]      # eV


def main():
    rows = []
    for m in MASSES:
        fgw = float(c.f_gw(m))
        psi_fp = float(c.kr_psi_amplitude(m))                    # frac=1 (100% local DM)
        psi_lit = float(c.kr_psi_literature(m))
        hc_ng = float(c.nanograv_hc(fgw))
        ratio = float(c.kr_signal_vs_nanograv(m))                # Psi_c / h_c(f_GW)
        omega_gw_prop = float(c.omega_gw_propagating_bound(m))   # SGWB upper bound
        rows.append({"m_eV": m, "f_GW_Hz": fgw,
                     "Psi_c_firstprinciples": psi_fp, "Psi_c_literature": psi_lit,
                     "nanograv_hc_at_fGW": hc_ng, "strain_ratio_Psi_over_hc": ratio,
                     "omega_gw_propagating_bound": omega_gw_prop})

    ng_omega = float(c.nanograv_omega_gw())                      # ~8e-9 at 1/yr

    payload = {
        "rows": rows,
        "nanograv_omega_gw_at_fyr": ng_omega,
        "nanograv_A_yr": c.NG_A_YR,
        "rho_local_GeVcm3": c.RHO_LOCAL_GEVCM3,
        "interpretation": {
            "KR_line": "Psi_c is the MONOCHROMATIC PTA observable; compare to h_c(f_GW)",
            "SGWB": "omega_gw_propagating_bound is a generous CEILING on the radiated "
                    "stochastic background; the true value is far below.",
        },
        "verdict_inputs": {
            "max_strain_ratio_in_band": max(r["strain_ratio_Psi_over_hc"] for r in rows),
            "max_omega_gw_prop_in_band": max(r["omega_gw_propagating_bound"] for r in rows),
            "nanograv_omega_gw": ng_omega,
        },
        "note": "m_A from Paper II; NANOGrav numbers COMPARISON ONLY; not adjusted",
    }
    (OUT / "HQ3_2_amplitude.json").write_text(json.dumps(payload, indent=2))

    print("=" * 78)
    print("HQ3-2  amplitude of the m_A signal vs NANOGrav (A_yr = 2.4e-15)")
    print("=" * 78)
    print("  (a) Khmelnitsky-Rubakov LINE signal  Psi_c = pi G rho/omega^2")
    print(f"  {'m_A [eV]':>10} {'f_GW [Hz]':>11} {'Psi_c(fp)':>11} {'Psi_c(lit)':>11}"
          f" {'h_c,NG':>10} {'Psi/h_c':>9}")
    for r in rows:
        print(f"  {r['m_eV']:>10.2e} {r['f_GW_Hz']:>11.3e} "
              f"{r['Psi_c_firstprinciples']:>11.2e} {r['Psi_c_literature']:>11.2e} "
              f"{r['nanograv_hc_at_fGW']:>10.2e} {r['strain_ratio_Psi_over_hc']:>9.2e}")
    print("\n  (b) PROPAGATING stochastic background (upper bound) vs NANOGrav:")
    print(f"      max Omega_GW(m_A) ceiling in band = "
          f"{payload['verdict_inputs']['max_omega_gw_prop_in_band']:.2e}")
    print(f"      NANOGrav Omega_GW(1/yr)           = {ng_omega:.2e}")
    print(f"      ratio (m_A / NANOGrav)            = "
          f"{payload['verdict_inputs']['max_omega_gw_prop_in_band']/ng_omega:.2e}  (<<1)")
    print(f"  saved {OUT/'HQ3_2_amplitude.json'}")

    make_figure(rows, ng_omega)
    return payload


def make_figure(rows, ng_omega):
    fig, ax = plt.subplots(1, 2, figsize=(13, 5.0))

    mm = np.logspace(np.log10(4.14e-24), np.log10(c.M_A_CEIL), 200)
    # LEFT: KR line amplitude vs NANOGrav broadband strain
    ax[0].loglog(mm, c.kr_psi_amplitude(mm), color="crimson", lw=2.2,
                 label=r"$\Psi_c=\pi G\rho/\omega^2$ (first-principles, 100% local DM)")
    ax[0].loglog(mm, c.kr_psi_literature(mm), color="orange", lw=1.4, ls="--",
                 label=r"$\Psi_c$ (KR literature $\sim$2e-15)")
    # subdominant case: frac=0.1 (FM4/FN3 -- m_A is subdominant for much of the window)
    ax[0].loglog(mm, c.kr_psi_amplitude(mm, frac=0.1), color="crimson", lw=1.0, ls=":",
                 label=r"$\Psi_c$ if m_A = 10% of local DM (FM4/FN3)")
    ax[0].loglog(mm, c.nanograv_hc(c.f_gw(mm)), color="navy", lw=1.8,
                 label=r"NANOGrav $h_c(f_{\rm GW})$ broadband")
    for r in rows:
        ax[0].plot(r["m_eV"], r["Psi_c_firstprinciples"], "o",
                   color="crimson", markeredgecolor="k", ms=6, zorder=5)
    ax[0].set_xlabel(r"$m_A$ [eV]"); ax[0].set_ylabel(r"strain amplitude $\Psi_c$ / $h_c$")
    ax[0].set_title("HQ3-2a: KR monochromatic line vs NANOGrav strain")
    ax[0].legend(fontsize=7.5, loc="lower left")

    # RIGHT: propagating SGWB Omega_GW comparison (bar-style)
    ax[1].axhline(ng_omega, color="navy", lw=2.0,
                  label=f"NANOGrav $\\Omega_{{GW}}(1/yr)\\approx${ng_omega:.0e}")
    omg = c.omega_gw_propagating_bound(mm)
    ax[1].loglog(mm, omg, color="crimson", lw=2.2,
                 label=r"$\Omega_{GW}$ radiated by m_A (generous ceiling $\sim\Psi_c^2$)")
    ax[1].set_xlabel(r"$m_A$ [eV]"); ax[1].set_ylabel(r"$\Omega_{GW}$")
    ax[1].set_ylim(1e-40, 1e-5)
    ax[1].set_title("HQ3-2b: propagating SGWB -- m_A is NOT the NANOGrav background")
    ax[1].legend(fontsize=8, loc="lower left")

    fig.suptitle("HQ3-2: m_A gives a near-threshold PTA LINE (left) but a negligible "
                 "propagating background (right)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "HQ3_2_amplitude.png", dpi=130)
    print(f"  saved {OUT/'HQ3_2_amplitude.png'}")


if __name__ == "__main__":
    main()
