"""E7_gate.py -- validation gates G1, G2 for the E7_COULOMB_PHASE campaign.

The charter requires that BEFORE measuring any physics we reproduce the already-
established E5 results with the SAME engine we will use for the Wilson-loop
measurement. We REUSE the E5 engine (e5_core / e5_fast) and the E5 gate functions
verbatim -- this campaign does not rebuild the motor.

  G1  gauge invariance: a random local gauge transform leaves every plaquette
      holonomy invariant to machine precision, on (a) the regular 4D/3D lattice and
      (b) the causal-set DIAMOND plaquettes (the construction E7 actually measures).
  G2  4D U(1) transition: the regular-lattice specific-heat proxy peaks near the
      known beta_c ~ 1.01 (E5-V found 1.00).

If either gate fails: STOP, do not measure Wilson loops with an unvalidated engine.
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

from e5_core import causal_diamond_plaquettes              # noqa: E402
from E5V_gate import gate_G1, scan_specific_heat           # noqa: E402  (reuse E5 gate)
from orientation_core import causal_link_graph             # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box                       # noqa: E402


def diamond_gauge_invariance(L_box=5.0, rho=0.5, seed=0):
    """G1 on the causal diamonds: per-node gauge transform theta_(a,b) += lam[b]-lam[a]
    (edge a<b) must leave the diamond plaquette holonomies invariant."""
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    L, pl, ps = causal_diamond_plaquettes(g, max_per_pair=2, seed=seed)
    edges = g.edges
    theta = rng.uniform(-np.pi, np.pi, L)
    hol0 = (ps * theta[pl]).sum(axis=1)
    lam = rng.uniform(-np.pi, np.pi, g.n)
    theta2 = theta + (lam[edges[:, 1]] - lam[edges[:, 0]])
    hol1 = (ps * theta2[pl]).sum(axis=1)
    max_dcos = float(np.max(np.abs(np.cos(hol1) - np.cos(hol0))))
    return max_dcos, g.n, int(pl.shape[0])


def main():
    t0 = time.time()
    out = {}

    # ---- G1: gauge invariance, regular lattices (reuse E5 gate_G1) ----
    g1_4d = gate_G1((3, 3, 3, 3))
    g1_3d = gate_G1((4, 4, 4))
    # ---- G1: gauge invariance on the causal diamonds ----
    g1_diam, ndiam, npl = diamond_gauge_invariance()
    G1_pass = (g1_4d < 1e-10) and (g1_3d < 1e-10) and (g1_diam < 1e-10)
    out["G1_gauge_invariance"] = {"max_dcos_4D": g1_4d, "max_dcos_3D": g1_3d,
                                  "max_dcos_diamond": g1_diam,
                                  "diamond_n_events": ndiam, "diamond_n_plaq": npl,
                                  "pass": bool(G1_pass)}
    print(f"G1 gauge invariance: 4D={g1_4d:.1e} 3D={g1_3d:.1e} "
          f"diamond={g1_diam:.1e} (n={ndiam}, plaq={npl}) -> "
          f"{'PASS' if G1_pass else 'FAIL'}", flush=True)

    # ---- G2: 4D U(1) transition near beta_c~1.01 (reuse E5 scan) ----
    betas = np.array([0.2, 0.5, 0.7, 0.85, 1.0, 1.1, 1.25, 1.5, 1.8])
    meanP4, C4, Np4 = scan_specific_heat((4, 4, 4, 4), betas)
    pk4 = int(np.argmax(C4)); beta_pk4 = float(betas[pk4])
    G2_pass = 0.85 <= beta_pk4 <= 1.20
    out["G2_4D"] = {"betas": betas.tolist(), "mean_plaq": meanP4.tolist(),
                    "specific_heat": C4.tolist(), "peak_beta": beta_pk4,
                    "N_plaq": Np4, "pass": bool(G2_pass)}
    print(f"G2 4D U(1): specific-heat peak at beta={beta_pk4:.2f} "
          f"(known beta_c~1.01; E5-V found 1.00) -> {'PASS' if G2_pass else 'FAIL'}",
          flush=True)

    all_pass = G1_pass and G2_pass
    out["all_pass"] = bool(all_pass)
    out["runtime_s"] = time.time() - t0
    (HERE / "E7_gate.json").write_text(json.dumps(out, indent=2))
    print(f"\nGATE {'PASSED' if all_pass else 'FAILED'} -- "
          f"{'E7 Wilson measurement may run' if all_pass else 'STOP: engine not validated'} "
          f"({out['runtime_s']:.0f}s)")


if __name__ == "__main__":
    main()
