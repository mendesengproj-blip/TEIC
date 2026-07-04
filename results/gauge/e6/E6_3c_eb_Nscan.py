"""E6_3c_eb_Nscan.py -- B-type fraction vs network size N (reviewer robustness).

E6_3b established frac_B_type=0.0000 across nine sprinklings up to N=626. A reviewer
asks whether the exactly-zero magnetic (B-type) fraction is stable as N grows, or a
finite-size effect. This scans the SAME E/B classifier (height-2 causal diamonds,
e6_bd_core) at target sizes N ~ 200, 500, 1000, 2000 and reports, for each, the
pooled B-type fraction and a one-sided Wilson 95% UPPER bound (0 successes in P
plaquettes => upper limit ~ 3/P). Nothing relativistic enters: only the causal order
and the area-bivector signature classification.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E5 = HERE.parent / "e5"; ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(E5)); sys.path.insert(0, str(ORI))
from e5_core import causal_diamond_plaquettes              # noqa: E402
from orientation_core import causal_link_graph             # noqa: E402
ROOT = HERE.parents[2]; sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box                       # noqa: E402
from e6_bd_core import (plaquette_vertices, plaquette_bivectors,   # noqa: E402
                        lorentzian_weights)


def wilson_upper(k, n, z=1.96):
    """One-sided Wilson upper bound for a binomial proportion (k successes / n)."""
    if n == 0:
        return float("nan")
    p = k / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return float((centre + half) / denom)


def measure(rho, L_box, seed):
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    _, pl, ps = causal_diamond_plaquettes(g, max_per_pair=3, seed=seed)
    verts = plaquette_vertices(g.edges, pl, ps)
    _, e2, b2 = plaquette_bivectors(pts, verts)
    nB = int(np.sum(b2 > e2))
    return int(g.n), int(pl.shape[0]), nB


def main():
    t0 = time.time()
    rho = 1.0
    # target N ~ rho * L^4  ->  L = (N/rho)^(1/4)
    targets = [200, 500, 1000, 2000]
    seeds = (1, 2, 3)
    rows = []
    for Ntar in targets:
        L = (Ntar / rho) ** 0.25
        Ns, Ptot, nB_tot = [], 0, 0
        for s in seeds:
            n, P, nB = measure(rho, L, 100 + s)
            Ns.append(n); Ptot += P; nB_tot += nB
        fB = nB_tot / Ptot if Ptot else float("nan")
        hi = wilson_upper(nB_tot, Ptot)
        rows.append(dict(N_target=Ntar, N_mean=float(np.mean(Ns)), L_box=L,
                         n_seeds=len(seeds), plaquettes=Ptot, nB=nB_tot,
                         frac_B_type=fB, wilson_hi_95=hi))
        print(f"  N~{Ntar:5d} (N_mean={np.mean(Ns):7.1f})  P={Ptot:7d}  "
              f"nB={nB_tot}  fB={fB:.4f}  Wilson-hi={hi:.2e}", flush=True)
    out = dict(rho=rho, rows=rows,
               all_zero=bool(all(r["nB"] == 0 for r in rows)),
               runtime_s=time.time() - t0)
    (HERE / "E6_3c_eb_Nscan.json").write_text(json.dumps(out, indent=2))
    print(f"\nall fB exactly zero: {out['all_zero']}")
    print(f"runtime {out['runtime_s']:.0f}s -> E6_3c_eb_Nscan.json")


if __name__ == "__main__":
    main()
