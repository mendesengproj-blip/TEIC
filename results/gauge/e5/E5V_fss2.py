"""E5V_fss2.py -- G3 finite-size scaling with the VALIDATED fast engine, at volumes
the pure-Python engine could not reach.

Physics of the discriminator (corrected): at a genuine (first-order) transition the
specific heat PER PLAQUETTE grows ~linearly with volume (phase coexistence /
bimodal plaquette distribution near beta_c, Var(mean cos) stays O(1)); at a smooth
crossover it stays roughly constant (Var ~ 1/N by the central limit). So:
  4D U(1) (transition at beta_c~1.01): C/N_plaq should GROW with volume.
  3D U(1) (confines at all beta, Polyakov, no transition): C/N_plaq ~ constant.
This is the clean G3 that the tiny 3^4/4^4 volumes could not resolve.

C/N_plaq = beta^2 * N_plaq * Var(<cos theta_P>_config).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e5_core import regular_lattice  # noqa: E402
from e5_fast import FastU1Gauge      # noqa: E402


def peak_C_per_plaq(shape, betas, n_seeds=2, n_burn=200, n_meas=150, seed0=0):
    L, pl, ps = regular_lattice(shape)
    Nplaq = pl.shape[0]
    Cpp = np.zeros(len(betas))
    for ib, beta in enumerate(betas):
        mc = []
        for s in range(n_seeds):
            g = FastU1Gauge(L, pl, ps, beta=beta, seed=seed0 + 100 * ib + s)
            g.equilibrate(n_burn)
            mc.append(g.measure_plaq(n_meas))
        mc = np.concatenate(mc)
        Cpp[ib] = beta ** 2 * Nplaq * mc.var()
    j = int(np.argmax(Cpp))
    return float(Cpp[j]), float(betas[j]), Nplaq


def main():
    t0 = time.time()
    betas4 = np.array([0.95, 1.0, 1.05, 1.10, 1.15])
    betas3 = np.array([1.0, 1.5, 2.0, 2.5])

    rows4, rows3 = [], []
    print("4D U(1) -- C/N_plaq at peak vs volume (expect GROWTH = transition):")
    for shp in [(4, 4, 4, 4), (5, 5, 5, 5), (6, 6, 6, 6)]:
        c, b, Np = peak_C_per_plaq(shp, betas4)
        rows4.append({"shape": shp, "N_plaq": Np, "C_per_plaq_peak": c, "peak_beta": b})
        print(f"  {shp}: N_plaq={Np:5d}  C/N_plaq={c:.3e} at beta={b:.2f}", flush=True)

    print("3D U(1) -- C/N_plaq at peak vs volume (expect ~CONSTANT = crossover):")
    for shp in [(6, 6, 6), (8, 8, 8), (10, 10, 10)]:
        c, b, Np = peak_C_per_plaq(shp, betas3)
        rows3.append({"shape": shp, "N_plaq": Np, "C_per_plaq_peak": c, "peak_beta": b})
        print(f"  {shp}: N_plaq={Np:5d}  C/N_plaq={c:.3e} at beta={b:.2f}", flush=True)

    # trends: slope of log(C/N_plaq) vs log(N_plaq)
    def slope(rows):
        x = np.log(np.array([r["N_plaq"] for r in rows]))
        y = np.log(np.array([r["C_per_plaq_peak"] for r in rows]))
        return float(np.polyfit(x, y, 1)[0])
    s4 = slope(rows4); s3 = slope(rows3)

    # 4D transition: C/N_plaq grows (slope > +0.15); 3D crossover: ~flat/decreasing
    G3_pass = (s4 > 0.15) and (s4 > s3 + 0.3)
    verdict = (f"G3 {'PASS' if G3_pass else 'INCONCLUSIVE/FAIL'}: "
               f"4D C/N_plaq trend dln/dlnN = {s4:+.2f} "
               f"({'grows -> transition' if s4 > 0.15 else 'does not grow'}); "
               f"3D trend = {s3:+.2f} ({'flat/decreasing -> crossover' if s3 < s4 - 0.3 else 'not clearly distinct'}).")

    out = {"betas_4D": betas4.tolist(), "betas_3D": betas3.tolist(),
           "rows_4D": rows4, "rows_3D": rows3,
           "slope_4D": s4, "slope_3D": s3,
           "G3_pass": bool(G3_pass), "verdict": verdict,
           "runtime_s": time.time() - t0}
    (HERE / "E5V_fss2.json").write_text(json.dumps(out, indent=2))
    print("\n" + verdict)
    print(f"runtime {out['runtime_s']:.0f}s -> E5V_fss2.json")


if __name__ == "__main__":
    main()
