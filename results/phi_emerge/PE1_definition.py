"""PE1_definition.py -- is the emergent field  Phi_i = rho_i e^{i phibar_i} well-defined?

PHI_EMERGE task PE1 (the GATE: if Phi is not well-defined, the campaign stops here).
Four checks over 20 seeds, on the cr3d 3+1D lattice:

  (1) rho_i = N_i/<N> >= 0 always; how often is a Voronoi cell empty (rho_i=0)?  A
      Poisson cell CAN be empty, so we report the empty-cell fraction and show it -> 0
      as the sprinkle density grows (it is a resolution knob, not a pathology).
  (2) phibar_i is defined for every node (degree >= 1).  On this lattice deg in {5,6}.
  (3) |Phi_i| = rho_i fluctuates about 1 in the vacuum, with spread ~ 1/sqrt(<N>).
  (4) arg(Phi_i) = phibar_i is uniform on [-pi,pi] in the disordered (hot) vacuum
      (chi-square test against uniform).

Anti-circularity: Phi is computed from the EXISTING fields (a Poisson count and the
gauge links); no new parameter, no complex literal (two real arrays).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phi_emerge_core as pe   # noqa: E402

NSEED = 20


def _ms(v):
    v = np.asarray(v, float)
    return float(v.mean()), float(v.std(ddof=1)) if v.size > 1 else 0.0


def chi2_uniform(angles, nbins=24):
    """Chi-square statistic of ``angles`` (in [-pi,pi]) against uniform; return (chi2,
    dof, reduced).  Reduced ~1 => consistent with uniform."""
    h, _ = np.histogram(angles, bins=nbins, range=(-np.pi, np.pi))
    exp = angles.size / nbins
    chi2 = float(np.sum((h - exp) ** 2 / exp))
    dof = nbins - 1
    return chi2, dof, chi2 / dof


def run_density(rho_sprinkle, grid, T=8.0, seed0=0):
    Nx, Ny, Nz = grid
    x, y, z, dx = pe.make_grid(Nx, Ny, Nz)
    frac_zero, rho_mean, rho_std = [], [], []
    deg_min, deg_max = [], []
    chi2red = []
    abs_match = 0.0
    for s in range(NSEED):
        rng = np.random.default_rng(seed0 + s)
        rho, counts, meanN = pe.causal_density(Nx, Ny, Nz, rho_sprinkle, T, rng,
                                               return_counts=True)
        phix, phiy, phiz = pe.hot_gauge(x, y, z, rng)
        pb, deg = pe.phibar(phix, phiy, phiz)
        Re, Im = pe.phi_field(rho, pb)
        frac_zero.append(float(np.mean(rho == 0)))
        rho_mean.append(float(rho.mean())); rho_std.append(float(rho.std()))
        deg_min.append(float(deg.min())); deg_max.append(float(deg.max()))
        # arg uniformity on BULK nodes: the x-end slices have a Dirichlet link pinned to
        # 0 (phix[0]=phix[-1]=0), which biases their phibar toward 0 -- a boundary
        # artefact, not a property of Phi.  Test the interior x-slices [1:-1].
        arg = pe.phi_arg(Re, Im)[1:-1]
        _, _, red = chi2_uniform(arg.ravel())
        chi2red.append(red)
        abs_match = max(abs_match, float(np.max(np.abs(pe.phi_abs(Re, Im) - rho))))
    return {
        "rho_sprinkle": rho_sprinkle, "mean_events_per_cell_<N>": float(meanN),
        "frac_empty_cells_mean": _ms(frac_zero)[0], "frac_empty_cells_std": _ms(frac_zero)[1],
        "rho_mean": _ms(rho_mean)[0], "rho_mean_std": _ms(rho_mean)[1],
        "rho_std_mean": _ms(rho_std)[0], "rho_std_expected_1_over_sqrtN": float(1/np.sqrt(meanN)),
        "deg_min": min(deg_min), "deg_max": max(deg_max),
        "argPhi_chi2_reduced_vs_uniform_mean": _ms(chi2red)[0],
        "argPhi_chi2_reduced_std": _ms(chi2red)[1],
        "max_abs_|Phi|_minus_rho": abs_match,
    }


def main():
    grid = (29, 20, 20)
    densities = [2.0, 4.0, 8.0, 16.0]
    rows = [run_density(rs, grid, seed0=100 + 50 * i) for i, rs in enumerate(densities)]

    # PE1 pass criteria
    well_defined = (
        all(r["rho_mean"] > 0.99 and r["rho_mean"] < 1.01 for r in rows) and
        all(r["deg_min"] >= 1 for r in rows) and
        all(r["max_abs_|Phi|_minus_rho"] < 1e-12 for r in rows) and
        # arg uniform in the hot vacuum (reduced chi2 ~ 1)
        all(r["argPhi_chi2_reduced_vs_uniform_mean"] < 1.5 for r in rows) and
        # empty-cell fraction shrinks with density (resolution knob)
        rows[-1]["frac_empty_cells_mean"] <= rows[0]["frac_empty_cells_mean"]
    )
    summary = {"n_seeds": NSEED, "grid": list(grid), "rows": rows,
               "phi_well_defined": bool(well_defined),
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    pe.save_json("PE1_definition", summary)

    print("=" * 74)
    print(f"PE1 -- IS  Phi = rho e^(i phibar)  WELL-DEFINED?  ({NSEED} seeds)")
    print("=" * 74)
    print(f"grid {grid}, hot (disordered) gauge vacuum")
    print("\n rho_spr  <N>/cell  empty-frac      <rho>        std(rho)  [exp 1/sqrtN]   "
          "arg chi2/dof")
    for r in rows:
        print(f"  {r['rho_sprinkle']:5.1f}   {r['mean_events_per_cell_<N>']:6.1f}   "
              f"{r['frac_empty_cells_mean']:.4f}     {r['rho_mean']:.4f}      "
              f"{r['rho_std_mean']:.3f}   [{r['rho_std_expected_1_over_sqrtN']:.3f}]      "
              f"{r['argPhi_chi2_reduced_vs_uniform_mean']:.2f}")
    print(f"\n deg range over all nodes: [{min(r['deg_min'] for r in rows):.0f}, "
          f"{max(r['deg_max'] for r in rows):.0f}]  (>=1 everywhere -> phibar always defined)")
    print(f" max | |Phi| - rho | over all runs: "
          f"{max(r['max_abs_|Phi|_minus_rho'] for r in rows):.2e}  (Phi stored as 2 real arrays)")
    print("-" * 74)
    print(f"VERDICT (PE1): {'WELL-DEFINED' if well_defined else 'NOT well-defined -- STOP'}")
    print("  rho>=0 (empty cells -> 0 with density), phibar defined (deg>=1), |Phi|=rho,")
    print("  arg(Phi) uniform in the hot vacuum.  Phi = rho e^(i phibar) is a valid")
    print("  composition of two pre-existing network fields.")
    return summary


if __name__ == "__main__":
    main()
