"""E6_1_gauge_structure.py -- does the link sector carry genuine gauge structure?

Pre-registered in E6_BD_GAUGE.md (gate H1 + the mode-counting that the orientation
sector of E4 lacked). NON-COMPACT (Gaussian) Maxwell on the causal set: a 1-cochain
theta_l on each causal link, field strength F_P = (d theta)_P around each causal
diamond, action S = (1/2) sum_P F_P^2 = (1/2) theta^T M theta with M = B^T B (B the
plaquette-incidence matrix). This is exact linear algebra -- no Monte Carlo, no
dispersion law inserted.

What it decides (the structural question E4 could not give the orientation Goldstone):
  H1  gauge invariance: a gauge shift theta -> theta + G lam (G the node coboundary)
      must leave every F_P invariant, i.e. B G = 0 and M G = 0 (gauge modes are exact
      zero modes). PASS is structural and decisive.
  mode counting: dim ker(B) = gauge modes (im G, dim = rank G) + harmonic modes;
      the propagating ("physical/transverse") modes = rank(B). A genuine gauge field
      has a large gauge redundancy (rank G = #nodes - #components) removed, leaving
      the transverse physical sector -- the structure a photon needs and the
      orientation Goldstone (E4: two internal scalars, NO gauge redundancy) lacked.

It does NOT decide H2 (the relativistic dispersion omega=ck), which needs the
Lorentzian electric/magnetic structure -- the hard, open part, reported honestly.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E5 = HERE.parent / "e5"
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
sys.path.insert(0, str(E5))
sys.path.insert(0, str(ORI))
from e5_core import causal_diamond_plaquettes   # noqa: E402
from orientation_core import causal_link_graph   # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box             # noqa: E402


def build_incidence(g, plaq_links, plaq_signs):
    """B: (P, L) plaquette-incidence; G: (L, N) node coboundary for link (a<b):
    G[l,a]=-1, G[l,b]=+1 (so theta -> theta + G lam is the gauge shift)."""
    L = g.edges.shape[0]
    P = plaq_links.shape[0]
    B = np.zeros((P, L))
    for p in range(P):
        for j in range(4):
            B[p, plaq_links[p, j]] += plaq_signs[p, j]
    N = g.n
    G = np.zeros((L, N))
    for l, (a, b) in enumerate(g.edges):
        G[l, a] -= 1.0
        G[l, b] += 1.0
    return B, G


def main():
    t0 = time.time()
    rho, L_box = 0.5, 4.6
    rng = np.random.default_rng(1)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    Lk, pl, ps = causal_diamond_plaquettes(g, max_per_pair=3, seed=1)
    L = g.edges.shape[0]; N = g.n; P = pl.shape[0]
    B, G = build_incidence(g, pl, ps)
    M = B.T @ B

    # H1: gauge invariance -- B G = 0 and M G = 0 (gauge shifts are exact zero modes)
    rng2 = np.random.default_rng(2)
    lam = rng2.standard_normal(N)
    shift = G @ lam
    h1_BG = float(np.max(np.abs(B @ G)))
    h1_Mshift = float(np.max(np.abs(M @ shift)))
    H1_pass = h1_BG < 1e-9 and h1_Mshift < 1e-7

    # mode counting (rank-nullity)
    tol = 1e-8
    rank_B = int(np.linalg.matrix_rank(B, tol=tol))
    rank_G = int(np.linalg.matrix_rank(G, tol=tol))
    ker_B = L - rank_B
    gauge_modes = rank_G                 # dim of pure-gauge subspace (im G)
    harmonic = ker_B - gauge_modes       # topological (cohomology) zero modes
    physical = rank_B                    # propagating / transverse sector
    gauge_frac = gauge_modes / L

    verdict = (
        f"GAUGE STRUCTURE CONFIRMED: H1 gauge invariance exact "
        f"(|BG|={h1_BG:.0e}, |M*gauge|={h1_Mshift:.0e}); of L={L} link d.o.f., "
        f"{gauge_modes} are pure gauge ({100*gauge_frac:.0f}%, = #nodes-#comp), "
        f"{harmonic} harmonic/topological, and {physical} are physical (transverse) "
        f"propagating modes. The link sector carries the genuine gauge redundancy a "
        f"photon needs -- exactly the structure the orientation Goldstone sector (E4) "
        f"LACKED (there the 2 modes were internal scalars with NO gauge redundancy). "
        f"H2 (relativistic dispersion omega=ck of the physical modes) needs the "
        f"Lorentzian electric/magnetic construction and remains the open hard part."
        if H1_pass else
        f"H1 FAILED (|BG|={h1_BG:.0e}): the action is not gauge-invariant as built; "
        f"diagnose the plaquette/coboundary sign convention before proceeding."
    )
    tag = "GAUGE_STRUCTURE_OK" if H1_pass else "H1_FAIL"

    out = {
        "config": {"rho": rho, "L_box": L_box},
        "N_nodes": N, "L_links": L, "P_plaquettes": P,
        "H1_BG_maxabs": h1_BG, "H1_M_gauge_maxabs": h1_Mshift, "H1_pass": bool(H1_pass),
        "rank_B": rank_B, "rank_G": rank_G,
        "gauge_modes": gauge_modes, "harmonic_modes": harmonic,
        "physical_modes": physical, "gauge_fraction": gauge_frac,
        "verdict": verdict, "verdict_tag": tag,
        "runtime_s": time.time() - t0,
    }
    (HERE / "E6_1_gauge_structure.json").write_text(json.dumps(out, indent=2))
    print(f"N={N} links={L} plaquettes={P}")
    print(f"H1 gauge invariance: |BG|={h1_BG:.1e}, |M*gauge|={h1_Mshift:.1e} -> "
          f"{'PASS' if H1_pass else 'FAIL'}")
    print(f"modes: gauge={gauge_modes} ({100*gauge_frac:.0f}%)  harmonic={harmonic}  "
          f"physical(transverse)={physical}")
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.0f}s -> E6_1_gauge_structure.json")


if __name__ == "__main__":
    main()
