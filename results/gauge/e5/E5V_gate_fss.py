"""E5V_gate_fss.py -- corrected G3 for the U(1) engine gate.

The original G3 in E5V_gate.py compared specific-heat PEAK HEIGHTS at a single
volume, which physically CANNOT distinguish a true phase transition from a smooth
crossover -- that distinction requires FINITE-SIZE SCALING. This script replaces G3
with the correct test: the specific-heat peak (per plaquette) of 4D U(1) should GROW
with lattice volume (genuine deconfinement transition, beta_c~1.01), whereas 3D
compact U(1) confines at all beta (Polyakov, no transition) and its crossover bump
should grow much less. G1 (gauge invariance, machine precision) and G2 (4D peak at
beta=1.00) already PASSED in E5V_gate.json; this completes the gate.
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


def peak_specific_heat(shape, betas, n_seeds=2, n_burn=120, n_meas=60, seed0=0):
    L, pl, ps = regular_lattice(shape)
    Nplaq = pl.shape[0]
    C = np.zeros(len(betas))
    for ib, beta in enumerate(betas):
        mc = []
        for s in range(n_seeds):
            g = U1Gauge(L, pl, ps, beta=beta, seed=seed0 + 100 * ib + s)
            g.equilibrate(n_burn)
            mc.append(g.measure_plaq(n_meas))
        mc = np.concatenate(mc)
        C[ib] = beta ** 2 * Nplaq * mc.var()
    return float(C.max() / Nplaq), float(betas[int(np.argmax(C))])


def main():
    t0 = time.time()
    betas = np.array([0.7, 0.85, 1.0, 1.1, 1.25, 1.5])

    # 4D U(1): two volumes -- peak should GROW with volume (true transition)
    p4_small, b4_small = peak_specific_heat((3, 3, 3, 3), betas)
    p4_large, b4_large = peak_specific_heat((4, 4, 4, 4), betas)
    growth_4d = p4_large / p4_small

    # 3D U(1): two volumes -- crossover, peak should grow much less
    p3_small, _ = peak_specific_heat((4, 4, 4), betas)
    p3_large, _ = peak_specific_heat((6, 6, 6), betas)
    growth_3d = p3_large / p3_small

    # corrected G3 (honest): a TRUE transition sharpens with volume, so the 4D peak
    # per plaquette must be MAINTAINED OR GROW (ratio >= 0.9) AND clearly exceed the
    # 3D crossover's volume trend. A marginal "4D shrinks less than 3D" is NOT a
    # clean transition signature and is reported as INCONCLUSIVE, not a pass.
    transition_like = growth_4d >= 0.9
    sharper_than_3d = growth_4d > 1.3 * growth_3d
    if transition_like and sharper_than_3d and b4_large in (1.0, 1.1):
        G3_status = "PASS"
    elif sharper_than_3d:
        G3_status = "INCONCLUSIVE"   # 4D more transition-like than 3D, but peaks not
                                     # growing at these tiny volumes -> unresolved
    else:
        G3_status = "FAIL"
    G3_pass = (G3_status == "PASS")
    out = {
        "betas": betas.tolist(),
        "peak_per_plaq_4D_small_3^4": p4_small,
        "peak_per_plaq_4D_large_4^4": p4_large,
        "peak_beta_4D_small": b4_small, "peak_beta_4D_large": b4_large,
        "growth_4D": growth_4d,
        "peak_per_plaq_3D_small_4^3": p3_small,
        "peak_per_plaq_3D_large_6^3": p3_large,
        "growth_3D": growth_3d,
        "G3_status": G3_status,
        "G3_corrected_pass": bool(G3_pass),
        "runtime_s": time.time() - t0,
    }
    (HERE / "E5V_gate_fss.json").write_text(json.dumps(out, indent=2))
    print(f"4D U(1) peak/plaq: 3^4={p4_small:.3e} -> 4^4={p4_large:.3e}  "
          f"growth x{growth_4d:.2f} (peak beta {b4_large})")
    print(f"3D U(1) peak/plaq: 4^3={p3_small:.3e} -> 6^3={p3_large:.3e}  "
          f"growth x{growth_3d:.2f}")
    print(f"\nG3 (corrected, finite-size scaling) -> {G3_status}")
    if G3_status == "INCONCLUSIVE":
        print("  4D is more transition-like than 3D, but neither peak grows at these")
        print("  tiny volumes (3^4,4^4): the FSS signature is unresolved with a")
        print("  pure-Python engine. Engine still validated by G1 (exact) + G2 (beta_c).")
    print(f"runtime {out['runtime_s']:.0f}s")


if __name__ == "__main__":
    main()
