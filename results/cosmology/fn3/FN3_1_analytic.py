"""FN3_1_analytic.py -- analytic relic density Omega_{m_A} h^2(m_A, f_A).

Charter FN3-1.  Scans m_A in {3.7e-25, 1e-24, 1e-23, 1e-22} eV (all inside the Paper
II vector window) x f_A in {1e15, 1e16, 1e17, 1e18} GeV.  Writes the grid + the
0.12 contour (f_A that gives Omega_DM h^2 at each mass) and a figure.

Headline = canonical ULDM closed form (prompt FN3-1 step 3).  First-principles
entropy estimate reported alongside as an independent cross-check (carries the O(1)
onset/g_* ambiguity).  Nothing fit to CMB: m_A from Paper II, f_A scanned.
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
MASSES = [c.M_A_FLOOR, 1e-24, 1e-23, 1e-22]          # eV (Paper II window)
F_AS = [1e15, 1e16, 1e17, 1e18]                      # GeV


def main():
    grid_canon = {}
    grid_fp = {}
    for m in MASSES:
        grid_canon[f"{m:.2e}"] = [float(c.omega_canonical(m, f)) for f in F_AS]
        grid_fp[f"{m:.2e}"] = [float(c.omega_firstprinciples(m, f)) for f in F_AS]

    # f_A that yields Omega=0.12 at each mass (the 0.12 contour)
    f_contour = {f"{m:.2e}": float(c.f_A_for_target(m)) for m in MASSES}

    # is there ANY grid point within a factor 10 of 0.12?  (death-criterion check)
    all_vals = np.array([v for row in grid_canon.values() for v in row])
    within_factor10 = bool(np.any((all_vals > 0.012) & (all_vals < 1.2)))
    # the contour f_A range across the window
    fc = np.array(list(f_contour.values()))

    payload = {
        "masses_eV": MASSES, "f_A_GeV": F_AS,
        "grid_canonical_Omega_h2": grid_canon,
        "grid_firstprinciples_Omega_h2": grid_fp,
        "f_A_for_Omega012_GeV": f_contour,
        "f_A_contour_min_GeV": float(fc.min()), "f_A_contour_max_GeV": float(fc.max()),
        "any_point_within_factor10_of_012": within_factor10,
        "paper_II_window_eV": [c.M_A_FLOOR, c.M_A_CEIL],
        "note": "canonical = prompt standard form; firstprinciples = entropy cross-check (O(1))",
    }
    (OUT / "FN3_1_analytic.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("FN3-1  analytic relic density  Omega_{m_A} h^2 (canonical closed form)")
    print("=" * 74)
    header = "  m_A [eV] \\ f_A [GeV]  " + "".join(f"{f:>11.0e}" for f in F_AS)
    print(header)
    for m in MASSES:
        row = grid_canon[f"{m:.2e}"]
        print(f"  {m:>9.2e}        " + "".join(f"{v:>11.2e}" for v in row))
    print("\n  f_A giving Omega h^2 = 0.12 at each mass (the 0.12 contour):")
    for m in MASSES:
        print(f"    m_A={m:>9.2e} eV -> f_A = {f_contour[f'{m:.2e}']:.2e} GeV")
    print(f"\n  0.12 contour spans f_A = {fc.min():.2e} - {fc.max():.2e} GeV "
          f"across the Paper II window")
    print(f"  any grid point within x10 of 0.12: {within_factor10}")
    print(f"  saved {OUT/'FN3_1_analytic.json'}")

    make_figure(grid_canon, f_contour)
    return payload


def make_figure(grid_canon, f_contour):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))

    # left: Omega vs m_A, one curve per f_A, with 0.12 line
    mm = np.logspace(np.log10(c.M_A_FLOOR), np.log10(1e-22), 100)
    for f in F_AS:
        ax[0].loglog(mm, c.omega_canonical(mm, f), label=f"f_A = {f:.0e} GeV")
    ax[0].axhline(c.OMEGA_DM_H2, color="k", ls="--", lw=1.5, label="Omega_DM h^2 = 0.12")
    ax[0].axvspan(c.M_A_FLOOR, c.M_A_CEIL, color="grey", alpha=0.12,
                  label="Paper II window")
    ax[0].set_xlabel("m_A [eV]"); ax[0].set_ylabel("Omega_{m_A} h^2")
    ax[0].set_ylim(1e-8, 1e6)
    ax[0].set_title("FN3-1: relic density vs (m_A, f_A)")
    ax[0].legend(fontsize=7, loc="upper left")

    # right: the 0.12 contour in the (m_A, f_A) plane
    mc = np.array(MASSES)
    fc = np.array([f_contour[f"{m:.2e}"] for m in MASSES])
    ax[1].loglog(mc, fc, "o-", color="crimson", label="Omega h^2 = 0.12 (need this f_A)")
    ax[1].axhspan(1e15, 1e18, color="green", alpha=0.08, label="scanned f_A range")
    ax[1].axhline(1e17, color="green", ls=":", lw=1, label="GUT scale ~1e17 GeV")
    # Stueckelberg f_A = m_A/e (e~0.3): astronomically small -> off plot, annotate
    ax[1].set_xlabel("m_A [eV]"); ax[1].set_ylabel("f_A [GeV]")
    ax[1].set_ylim(1e14, 1e19)
    ax[1].set_title("FN3-1: f_A required for Omega=0.12")
    ax[1].annotate("Stueckelberg f_A=m_A/e ~ 1e-31 GeV\n(48 orders below: relic negligible)",
                   xy=(mc[1], 2e14), fontsize=7, color="navy")
    ax[1].legend(fontsize=7, loc="upper right")

    fig.suptitle("FN3-1: misalignment relic of m_A -- Omega~0.12 reachable at f_A~1e17 GeV "
                 "(GUT scale), not at the Stueckelberg scale", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FN3_1_analytic.png", dpi=130)
    print(f"  saved {OUT/'FN3_1_analytic.png'}")


if __name__ == "__main__":
    main()
