"""HQ2_4_sigma8.py -- sigma8 with G_eff(z)/G_N = Z(z) from critical softening.

Charter: HQ2_CRITICAL_FERROMAGNET.md (HQ2-4).  Runs only because HQ2-2 was
positive.  Solves the linear growth ODE with the scale-INDEPENDENT effective
gravity Z(z)=(m(J(z))/m_sat)^2 (Route B), the SAME modified-growth equation used
in FM1 (k-independent mu here, since Z depends on J(z) not k):

    D'' + (2 + dlnH/dlna) D' - 1.5 Om(a) mu(a) D = 0 ,   mu(a) = Z(J(z)/J_c).

Because mu is k-independent, sigma8(HQ2) = sigma8(LCDM) * D_HQ2(0)/D_LCDM(0).

Pre-registered SUCCESS: sigma8(HQ2) < 0.83 AND closer to KiDS (0.766 -> sigma8~0.75)
than LCDM.  Death: sigma8(HQ2) ~ sigma8(LCDM), unmoved.

We report (a) the FIDUCIAL run at the constancy-of-c bound J0/J_c from HQ2-3
(physical), and (b) a scan over J0/J_c to show that sigma8 only moves toward KiDS
in the regime J0/J_c ~ O(1) that HQ2-3 already excluded.

LCDM anchors are COMPARISON ONLY (Planck sigma8=0.811, Om=0.315; KiDS S8=0.766).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import hq2_core as hc  # noqa: E402

OUT = Path(__file__).resolve().parent
OM = 0.315                     # Planck matter fraction (COMPARISON anchor)
SIGMA8_LCDM = 0.811            # Planck LCDM (COMPARISON anchor)
KIDS_S8, KIDS_ERR = 0.766, 0.020
SIGMA8_KIDS = KIDS_S8 / np.sqrt(OM / 0.3)     # ~0.748


def Z_of(JoJc):
    return float(np.clip(hc.m_of_J_meanfield(JoJc) ** 2, 0.0, 1.0))


def growth_D0(mu_of_a, Om=OM, a_i=1e-3):
    """Linear growth factor D(a=1) for a k-independent mu(a)=G_eff/G_N."""
    OL = 1.0 - Om

    def E2(a):
        return Om / a ** 3 + OL

    def Om_a(a):
        return Om / a ** 3 / E2(a)

    def dlnH_dlna(a):
        return -1.5 * Om / a ** 3 / E2(a)

    def rhs(N, y):
        D, Dp = y
        a = np.exp(N)
        return [Dp, -(2.0 + dlnH_dlna(a)) * Dp + 1.5 * Om_a(a) * mu_of_a(a) * D]

    sol = solve_ivp(rhs, [np.log(a_i), 0.0], [a_i, a_i], method="RK45",
                    rtol=1e-8, atol=1e-12, dense_output=True)
    return float(sol.y[0, -1])


def sigma8_for(J0_over_Jc):
    """sigma8(HQ2) for an assumed today's J0/J_c, via the growth-factor ratio."""
    def mu(a):
        z = 1.0 / a - 1.0
        return Z_of(hc.J_over_Jc_of_z(z, J0_over_Jc))
    D_hq2 = growth_D0(mu)
    D_lcdm = growth_D0(lambda a: 1.0)
    return SIGMA8_LCDM * D_hq2 / D_lcdm, D_hq2 / D_lcdm


def main():
    g2 = OUT / "HQ2_2_geff.json"
    if not g2.exists() or not json.loads(g2.read_text()).get("positive"):
        print("HQ2-2 not positive -- HQ2-4 must not run.  Aborting.")
        return 1
    print("=" * 72)
    print("HQ2-4 -- sigma8 with G_eff(z)/G_N = Z(z) (critical softening, Route B)")
    print("=" * 72)
    print(f"  LCDM anchor sigma8={SIGMA8_LCDM}  Om={OM}  "
          f"KiDS sigma8~{SIGMA8_KIDS:.3f} (S8={KIDS_S8})")

    # fiducial J0/Jc from HQ2-3 constancy-of-c bound (alpha, eps=1e-6)
    h3 = json.loads((OUT / "HQ2_3_cosmology.json").read_text())
    J0_fid = h3["constancy_bounds"]["alpha (1e-6)"]["J0_over_Jc_min"]
    if not np.isfinite(J0_fid):
        J0_fid = 1e6
    s8_fid, ratio_fid = sigma8_for(J0_fid)
    print(f"\n  FIDUCIAL (constancy-of-c bound J0/Jc={J0_fid:.3g}):")
    print(f"    growth ratio D_HQ2/D_LCDM = {ratio_fid:.6f}")
    print(f"    sigma8(HQ2) = {s8_fid:.4f}   vs LCDM {SIGMA8_LCDM}  vs KiDS {SIGMA8_KIDS:.3f}")

    # scan over J0/Jc
    print(f"\n  scan over J0/Jc (today):")
    print(f"  {'J0/Jc':>8} {'D_HQ2/D_LCDM':>13} {'sigma8(HQ2)':>12} "
          f"{'closer to KiDS?':>16}")
    scan = []
    for J0 in [1.05, 1.2, 1.5, 2.0, 3.0, 5.0, 10.0, 100.0, 1e3, J0_fid]:
        s8, ratio = sigma8_for(J0)
        closer = abs(s8 - SIGMA8_KIDS) < abs(SIGMA8_LCDM - SIGMA8_KIDS)
        scan.append({"J0_over_Jc": float(J0), "ratio": ratio, "sigma8": s8,
                     "closer_to_kids": bool(closer)})
        print(f"  {J0:8.3g} {ratio:13.5f} {s8:12.4f} {str(closer):>16}")

    # verdict
    # success needs sigma8(HQ2)<0.83 AND closer to KiDS than LCDM AT THE PHYSICAL
    # (constancy-bound) J0/Jc.  At fiducial Z~1 so sigma8~LCDM -> not closer.
    fid_closer = abs(s8_fid - SIGMA8_KIDS) < abs(SIGMA8_LCDM - SIGMA8_KIDS) - 1e-4
    success = bool(s8_fid < 0.83 and fid_closer)
    # where would it become closer? smallest J0/Jc that is also c-allowed (none)
    print("-" * 72)
    print(f"  at the physical J0/Jc: sigma8(HQ2)={s8_fid:.4f} "
          f"(LCDM {SIGMA8_LCDM}); closer to KiDS than LCDM: {fid_closer}")
    print(f"  sigma8 only moves toward KiDS for J0/Jc ~ O(1), which HQ2-3 excludes "
          f"(would imply |Delta c/c| ~ O(1)).")
    verdict = ("SUCCESS" if success else
               "DEATH -- sigma8(HQ2) ~ sigma8(LCDM); the suppression that could "
               "lower sigma8 lives only in the c-forbidden near-critical regime.")
    print(f"\n  HQ2-4 VERDICT: {verdict}")
    print("=" * 72)

    # figure
    fig, ax = plt.subplots(figsize=(8.5, 5.5))
    J0a = np.array([r["J0_over_Jc"] for r in scan])
    s8a = np.array([r["sigma8"] for r in scan])
    o = np.argsort(J0a)
    ax.semilogx(J0a[o], s8a[o], "o-", color="tab:red", label="sigma8(HQ2)")
    ax.axhline(SIGMA8_LCDM, color="tab:blue", ls="--", label=f"LCDM {SIGMA8_LCDM}")
    ax.axhspan(SIGMA8_KIDS - 0.02, SIGMA8_KIDS + 0.02, color="tab:green",
               alpha=0.25, label=f"KiDS ~{SIGMA8_KIDS:.3f}")
    ax.axvline(J0_fid, color="k", ls=":", lw=1,
               label=f"c-bound J0/Jc={J0_fid:.2g}")
    ax.set_xlabel("J0 / J_c (today)"); ax.set_ylabel("sigma8")
    ax.set_title("HQ2-4: sigma8 reaches KiDS only in the c-forbidden J0/Jc~O(1) regime")
    ax.legend(fontsize=8); ax.grid(alpha=0.25, which="both")
    fig.tight_layout()
    fig.savefig(OUT / "HQ2_4_sigma8.png", dpi=130)
    print(f"saved {OUT/'HQ2_4_sigma8.png'}")

    payload = {"task": "HQ2-4", "Om": OM, "sigma8_LCDM": SIGMA8_LCDM,
               "sigma8_KiDS": SIGMA8_KIDS, "KiDS_S8": KIDS_S8,
               "J0_over_Jc_fiducial": J0_fid, "sigma8_HQ2_fiducial": s8_fid,
               "growth_ratio_fiducial": ratio_fid, "scan": scan,
               "success": success, "verdict": verdict}
    (OUT / "HQ2_4_sigma8.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'HQ2_4_sigma8.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
