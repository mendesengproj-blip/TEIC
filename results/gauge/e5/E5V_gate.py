"""E5V_gate.py -- mandatory validation gate for the U(1) gauge engine (e5_core),
pre-registered in E5_PHOTON_LINK_SECTOR.md. The SAME machinery used on the causal
set must first reproduce known U(1) lattice-gauge results on regular lattices:

  G1 gauge invariance : a random local gauge transform leaves every plaquette
                        holonomy invariant to machine precision.
  G2 4D transition    : 4D U(1) Wilson gauge theory has a deconfinement transition
                        near beta_c ~ 1.01; the specific-heat proxy peaks there.
  G3 3D contrast      : 3D U(1) confines at all beta (Polyakov), with no comparable
                        deconfinement peak -- the engine must distinguish 3D from 4D.

If any gate fails, no causal-set number is trustworthy and E5-1 must not run.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e5_core import regular_lattice, U1Gauge  # noqa: E402


def gate_G1(shape, beta=1.0, seed=0):
    """Gauge invariance: theta_mu(x) -> theta_mu(x) + lam(x+mu) - lam(x) must leave
    all plaquette holonomies unchanged."""
    shape = tuple(shape); d = len(shape)
    n_sites = int(np.prod(shape))
    L, pl, ps = regular_lattice(shape)
    g = U1Gauge(L, pl, ps, beta=beta, seed=seed)
    h0 = g.plaquette_holonomies().copy()
    rng = np.random.default_rng(seed + 1)
    lam = rng.uniform(-np.pi, np.pi, n_sites)
    coords = np.array(np.unravel_index(np.arange(n_sites), shape)).T
    theta = g.theta.copy()
    for mu in range(d):
        c = coords.copy(); c[:, mu] = (c[:, mu] + 1) % shape[mu]
        x_mu = np.ravel_multi_index(c.T, shape)
        link_ids = np.arange(n_sites) * d + mu
        theta[link_ids] += lam[x_mu] - lam[np.arange(n_sites)]
    g.theta = theta
    h1 = g.plaquette_holonomies()
    # holonomies are mod 2pi; compare cos to be safe
    max_dcos = float(np.max(np.abs(np.cos(h1) - np.cos(h0))))
    return max_dcos


def scan_specific_heat(shape, betas, n_seeds=2, n_burn=150, n_meas=80, seed0=0):
    """Specific-heat proxy C(beta) = beta^2 * N_plaq * Var(<cos theta_P>) and the
    mean plaquette, seed-averaged, on a regular lattice."""
    L, pl, ps = regular_lattice(shape)
    Nplaq = pl.shape[0]
    meanP = np.zeros(len(betas)); C = np.zeros(len(betas))
    for ib, beta in enumerate(betas):
        mc_all = []
        for s in range(n_seeds):
            g = U1Gauge(L, pl, ps, beta=beta, seed=seed0 + 100 * ib + s)
            g.equilibrate(n_burn)
            vals = g.measure_plaq(n_meas)
            mc_all.append(vals)
        mc_all = np.concatenate(mc_all)
        meanP[ib] = mc_all.mean()
        C[ib] = beta ** 2 * Nplaq * mc_all.var()
    return meanP, C, Nplaq


def main():
    t0 = time.time()
    out = {}

    # ---- G1: gauge invariance (4D and 3D) ----
    g1_4d = gate_G1((3, 3, 3, 3))
    g1_3d = gate_G1((4, 4, 4))
    G1_pass = (g1_4d < 1e-10) and (g1_3d < 1e-10)
    out["G1_gauge_invariance"] = {"max_dcos_4D": g1_4d, "max_dcos_3D": g1_3d,
                                  "pass": bool(G1_pass)}
    print(f"G1 gauge invariance: max|dcos| 4D={g1_4d:.1e} 3D={g1_3d:.1e} -> "
          f"{'PASS' if G1_pass else 'FAIL'}", flush=True)

    # ---- G2: 4D U(1) transition near beta_c~1.01 ----
    betas = np.array([0.2, 0.5, 0.7, 0.85, 1.0, 1.1, 1.25, 1.5, 1.8])
    meanP4, C4, Np4 = scan_specific_heat((4, 4, 4, 4), betas)
    pk4 = int(np.argmax(C4)); beta_pk4 = float(betas[pk4])
    G2_pass = 0.85 <= beta_pk4 <= 1.20
    out["G2_4D"] = {"betas": betas.tolist(), "mean_plaq": meanP4.tolist(),
                    "specific_heat": C4.tolist(), "peak_beta": beta_pk4,
                    "N_plaq": Np4, "pass": bool(G2_pass)}
    print(f"G2 4D U(1): specific-heat peak at beta={beta_pk4:.2f} "
          f"(known beta_c~1.01) -> {'PASS' if G2_pass else 'FAIL'}", flush=True)

    # ---- G3: 3D U(1) contrast (confines; no comparable deconfinement peak) ----
    meanP3, C3, Np3 = scan_specific_heat((6, 6, 6), betas)
    pk3 = float(C3.max())
    # normalise peak heights per plaquette for a fair 3D-vs-4D comparison
    peak4_pp = C4.max() / Np4
    peak3_pp = C3.max() / Np3
    G3_pass = peak4_pp > 1.3 * peak3_pp   # 4D transition sharper than 3D crossover
    out["G3_3D"] = {"betas": betas.tolist(), "mean_plaq": meanP3.tolist(),
                    "specific_heat": C3.tolist(), "N_plaq": Np3,
                    "peak4_per_plaq": float(peak4_pp), "peak3_per_plaq": float(peak3_pp),
                    "pass": bool(G3_pass)}
    print(f"G3 3D contrast: peak/plaq 4D={peak4_pp:.3e} vs 3D={peak3_pp:.3e} "
          f"(4D should be sharper) -> {'PASS' if G3_pass else 'FAIL'}", flush=True)

    all_pass = G1_pass and G2_pass and G3_pass
    out["all_pass"] = bool(all_pass)
    out["runtime_s"] = time.time() - t0
    (HERE / "E5V_gate.json").write_text(json.dumps(out, indent=2))
    print(f"\nGATE {'PASSED' if all_pass else 'FAILED'} "
          f"-- {'E5-1 may run' if all_pass else 'STOP: engine not validated'} "
          f"({out['runtime_s']:.0f}s)")


if __name__ == "__main__":
    main()
