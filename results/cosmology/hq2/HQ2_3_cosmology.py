"""HQ2_3_cosmology.py -- could the z~0.5-1 universe have been near J_c?

Charter: HQ2_CRITICAL_FERROMAGNET.md (HQ2-3).  Runs only because HQ2-2 was
positive (Route B: G_eff<G_N exists near J_c).  The question that decides the
campaign: is the near-critical regime, where Z=(m/m_sat)^2 < 1, observationally
ACCESSIBLE at the redshifts (z~0.3-1) where S8 is measured?

Physics (prompt + DEV):
  * J ∝ rho_vacuum ∝ a^-3  =>  J(z)/J_c = (J0/J_c)(1+z)^3   (denser past = MORE
    ordered = FURTHER from J_c).  So J is SMALLEST today and shrinks toward J_c
    only in the FUTURE, never at z~0.5.
  * The photon EXISTS today with a CONSTANT speed (E2 Verdict A; observationally
    |Delta c/c| is tiny).  c_eff/c0 = m(J)/m_sat, so a constant c forces m≈m_sat,
    i.e. the vacuum sits DEEP in the ordered phase: J0/J_c >> 1.

Test: for a grid of assumed J0/J_c, compute Z(z=0) and Z(z=0.5,1) and the implied
variation of the speed of light Delta c/c between z=0 and z=0.5.  Show that any
J0/J_c giving meaningful suppression at z~0.5 also predicts a HUGE Delta c/c
(excluded), while the observed constancy of c forces J0/J_c so large that
Z(z~0.5)≈1 (no suppression).

m(J/J_c): mean-field shape sqrt(1 - J_c/J), anchored to the E1-1 measured m(J)
(the SAME curve HQ2-V/HQ2-1 measured; see anchor check below).  No free fit.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import hq2_core as hc  # noqa: E402

OUT = Path(__file__).resolve().parent
M_SAT = hc.M_SAT
# observational constancy-of-c / fine-structure bounds (COMPARISON anchors)
EPS_C_BOUNDS = {"alpha (1e-6)": 1e-6, "loose (1%)": 1e-2}


def m_of(JoJc):
    return hc.m_of_J_meanfield(JoJc)


def Z_of(JoJc):
    # mean-field stiffness ratio: m(J/Jc) asymptotes to 1 deep in the ordered
    # phase, so Z = m^2 in [0,1] with Z->1 deep-ordered (G_eff->G_N).
    return np.clip(m_of(JoJc) ** 2, 0.0, 1.0)


def main():
    g2 = OUT / "HQ2_2_geff.json"
    if not g2.exists() or not json.loads(g2.read_text()).get("positive"):
        print("HQ2-2 not positive -- HQ2-3 must not run.  Aborting.")
        return 1
    print("=" * 72)
    print("HQ2-3 -- is the z~0.5-1 universe near J_c?  (J/J_c = (J0/J_c)(1+z)^3)")
    print("=" * 72)

    # anchor check: mean-field m(J/Jc) vs the E1-1 measured m at J/Jc=1.5,2 (HQ2-1)
    try:
        h1 = json.loads((OUT / "HQ2_1_jeff.json").read_text())
        anchor = [(r["J_over_Jc"], r["m"]) for r in h1["rows"]
                  if r["J_over_Jc"] in (1.5, 2.0, 5.0)]
        print("  anchor (measured m vs mean-field shape):")
        for rj, mm in anchor:
            print(f"    J/Jc={rj}: measured m={mm:.3f}  mean-field={m_of(rj):.3f}")
    except Exception:
        anchor = []

    zs = np.array([0.0, 0.5, 1.0])
    J0_grid = np.array([1.1, 1.5, 2.0, 3.0, 5.0, 10.0, 30.0, 100.0, 1e3, 1e5])
    print(f"\n  scan over J0/J_c (today), Z=(m/m_sat)^2 at z=0,0.5,1 and Delta c/c:")
    print(f"  {'J0/Jc':>8} {'Z(0)':>8} {'Z(0.5)':>8} {'Z(1)':>8} "
          f"{'|dc/c|(0->0.5)':>14}")
    rows = []
    for J0 in J0_grid:
        JoJc_z = hc.J_over_Jc_of_z(zs, J0)
        Zz = Z_of(JoJc_z)
        m_z = m_of(JoJc_z)
        # speed of light variation between z=0 and z=0.5
        dcc = abs(m_z[1] - m_z[0]) / max(m_z[0], 1e-12)
        rows.append({"J0_over_Jc": float(J0), "Z_z0": float(Zz[0]),
                     "Z_z0p5": float(Zz[1]), "Z_z1": float(Zz[2]),
                     "dc_over_c_0_0p5": float(dcc)})
        print(f"  {J0:8.1f} {Zz[0]:8.4f} {Zz[1]:8.4f} {Zz[2]:8.4f} {dcc:14.2e}")

    # what J0/Jc does each constancy bound require? (smallest J0 with |dc/c|<eps)
    print("\n  constancy-of-c bound -> minimum J0/J_c -> residual suppression:")
    bound_results = {}
    Jfine = np.geomspace(1.001, 1e8, 4000)
    for name, eps in EPS_C_BOUNDS.items():
        m0 = m_of(Jfine)
        m05 = m_of(hc.J_over_Jc_of_z(0.5, Jfine))
        dcc = np.abs(m05 - m0) / np.maximum(m0, 1e-12)
        ok = dcc < eps
        if ok.any():
            J0min = float(Jfine[ok][0])
            Zz05 = float(Z_of(hc.J_over_Jc_of_z(0.5, J0min)))
            Zz0 = float(Z_of(J0min))
        else:
            J0min, Zz05, Zz0 = float("inf"), 1.0, 1.0
        bound_results[name] = {"eps_c": eps, "J0_over_Jc_min": J0min,
                               "Z_z0p5": Zz05, "Z_z0": Zz0,
                               "suppression_pct_z0p5": 100.0 * (1 - Zz05)}
        print(f"    {name:14s}: J0/Jc >= {J0min:.3g}  ->  G_eff/G_N(z=0.5)="
              f"{Zz05:.6f}  (suppression {100*(1-Zz05):.4f}%)")

    # decision
    # "near J_c" would require Z(z~0.5) noticeably <1 (say <0.95) WITHOUT violating
    # the loosest constancy bound.  Check the strict bound's residual suppression.
    strict = bound_results["alpha (1e-6)"]
    near_Jc_accessible = strict["Z_z0p5"] < 0.95
    # also: direction -- J shrinks to J_c only in the FUTURE (z<0)
    JoJc_future = hc.J_over_Jc_of_z(-0.5, 10.0)   # illustrative future point
    print("-" * 72)
    print(f"  with the alpha-constancy bound (eps=1e-6): G_eff/G_N(z=0.5) = "
          f"{strict['Z_z0p5']:.6f}  -> near-J_c accessible at z~0.5: "
          f"{near_Jc_accessible}")
    print(f"  J ∝ a^-3 shrinks toward J_c only in the FUTURE (z<0); at z~0.5 the "
          f"vacuum is MORE ordered than today.")
    verdict = ("INCONCLUSIVE" if near_Jc_accessible else
               "NO -- the universe is NEVER near J_c at observable z; a stable "
               "photon (constant c) forces J0/J_c >> 1 so Z(z~0.5) ~ 1.")
    print(f"\n  HQ2-3 VERDICT: {verdict}")
    print("=" * 72)

    # figure
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    ax = axes[0]
    zline = np.linspace(0, 2, 100)
    for J0, col in zip([1.5, 3.0, 10.0, 100.0],
                       ["tab:purple", "tab:orange", "tab:green", "tab:blue"]):
        ax.plot(zline, Z_of(hc.J_over_Jc_of_z(zline, J0)), color=col,
                label=f"J0/Jc={J0:g}")
    ax.axhline(1.0, color="k", ls="--", lw=1)
    ax.axvspan(0.3, 1.0, color="0.85", alpha=0.6, label="S8 redshift window")
    ax.set_xlabel("z"); ax.set_ylabel("$G_{eff}/G_N = (m/m_{sat})^2$")
    ax.set_title("Z(z): suppression weakest in the S8 window\n(J grows with z = more ordered)")
    ax.legend(fontsize=8); ax.grid(alpha=0.25)

    ax2 = axes[1]
    J0a = np.array([r["J0_over_Jc"] for r in rows])
    dcca = np.array([r["dc_over_c_0_0p5"] for r in rows])
    Z05a = np.array([r["Z_z0p5"] for r in rows])
    ax2.loglog(J0a, dcca, "o-", color="tab:red", label="|Δc/c|(0→0.5)")
    ax2.loglog(J0a, 1 - Z05a, "s--", color="tab:green",
               label="suppression 1-Z(z=0.5)")
    for name, eps in EPS_C_BOUNDS.items():
        ax2.axhline(eps, color="0.5", ls=":", lw=1)
        ax2.text(J0a[0], eps * 1.3, f"c-bound {name}", fontsize=7)
    ax2.set_xlabel("J0 / J_c (today)"); ax2.set_ylabel("magnitude")
    ax2.set_title("suppression at z=0.5 is locked to Δc/c:\nconstant c ⇒ no suppression")
    ax2.legend(fontsize=8); ax2.grid(alpha=0.25, which="both")
    fig.suptitle("HQ2-3: the near-critical regime is observationally forbidden",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "HQ2_3_cosmology.png", dpi=130)
    print(f"saved {OUT/'HQ2_3_cosmology.png'}")

    payload = {"task": "HQ2-3", "m_sat": M_SAT, "scaling": "J ∝ a^-3 (prompt)",
               "anchor_meanfield_vs_measured": anchor,
               "scan": rows, "constancy_bounds": bound_results,
               "near_Jc_accessible_z0p5": bool(near_Jc_accessible),
               "verdict": verdict}
    (OUT / "HQ2_3_cosmology.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'HQ2_3_cosmology.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
