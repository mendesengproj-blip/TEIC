"""focused_knn.py -- decisive FSS of the ONLY fixed-point lever (k-NN cap k=3).

The full campaign showed the k-NN cap is the only substrate that holds coordination z
fixed (-> a fixed J_c, ~0.68).  Its xi/L was ~constant, which is AMBIGUOUS: a genuine
2nd-order fixed point has xi/L CROSSING at J_c (curves for different L intersect:
below J_c xi/L falls with L, above it rises), whereas an ordered-phase plateau has
xi/L ~ const trivially (LRO = system-spanning order for any model).

This run scans a fine J grid around J_c with higher statistics and 5 sizes, and asks:
  (1) do the xi/L(J) curves CROSS at a single J_c (RG fixed point)?  -> criticality
  (2) does U4(J) cross at the same J_c?
  (3) chi_max ~ N^x: mean-field FSS gives x~0.5, 3D-Heisenberg x~0.66, volume x~1.
The 3D periodic lattice (validate_positive.json) is the criticality anchor.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xi_suite import build_knn_cap, measure_point  # noqa: E402
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402


def main():
    t0 = time.time()
    rho, k = 2.0, 3
    Ls = [4.0, 4.8, 5.6, 6.4, 7.2]
    Js = [0.40, 0.50, 0.58, 0.64, 0.68, 0.72, 0.78, 0.88, 1.00]
    cfg = dict(n_burn=400, n_meas=100, meas_every=2)
    n_seeds = 8
    sizes = []
    for L in Ls:
        clouds = [sprinkle_box(rho, [(0.0, L)] * 4, np.random.default_rng(1000 + s))
                  for s in range(n_seeds)]
        graphs = [build_knn_cap(pts, k) for pts in clouds]
        rows = [measure_point(graphs, J, L_s=L, **cfg) for J in Js]
        chi = [r["chi"] for r in rows]
        Jc = Js[int(np.argmax(chi))]
        zc = rows[0]["z_mean"]
        sizes.append({"L": L, "L_s": L, "N_mean": rows[0]["N_mean"], "z_mean": zc,
                      "Jc": Jc, "rows": rows})
        print(f"  L={L:.1f} N~{rows[0]['N_mean']:.0f} z={zc:.1f} Jc={Jc:.2f} "
              f"chi_max={max(chi):.2f}", flush=True)

    # tables
    print("\n  xi/L (rows=J, cols=L):")
    print("   J     " + "  ".join(f"L={L}" for L in Ls))
    for j, J in enumerate(Js):
        v = [sizes[i]["rows"][j]["xi_over_L"] for i in range(len(Ls))]
        print(f"  {J:.2f}  " + "  ".join(f"{x:.3f}" for x in v))
    print("\n  U4 (rows=J, cols=L):")
    for j, J in enumerate(Js):
        v = [sizes[i]["rows"][j]["U4"] for i in range(len(Ls))]
        print(f"  {J:.2f}  " + "  ".join(f"{x:.3f}" for x in v))

    Ns = np.array([s["N_mean"] for s in sizes])
    chi_max = np.array([max(r["chi"] for r in s["rows"]) for s in sizes])
    x_N = float(np.polyfit(np.log(Ns), np.log(np.maximum(chi_max, 1e-9)), 1)[0])
    print(f"\n  chi_max ~ N^{x_N:.3f}  (MF~0.5, 3D-crit~0.66, volume~1.0)")

    out = {"lever": "focused_knn_k3", "k": k, "rho": rho, "Ls": Ls, "Js": Js,
           "cfg": cfg, "n_seeds": n_seeds, "sizes": sizes,
           "chi_max_exponent_in_N": x_N, "runtime_s": time.time() - t0}
    (HERE / "focused_knn.json").write_text(json.dumps(out, indent=2))
    print(f"\nruntime {out['runtime_s']:.1f}s -> focused_knn.json")


if __name__ == "__main__":
    main()
