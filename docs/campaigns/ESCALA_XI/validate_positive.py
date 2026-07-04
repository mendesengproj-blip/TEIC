"""validate_positive.py -- POSITIVE CONTROL for the Campaign XI estimator.

Runs the SAME suite (xi_2nd from S(k), U4, chi) on the O(3) Heisenberg model on a
periodic 3D cubic lattice -- a substrate with a textbook 2nd-order transition
(T_c/J ~ 1.443, i.e. J_c ~ 0.693) and a genuinely diverging xi.  If xi_2nd/L CROSSES
across sizes near J_c and U4 crosses, the estimator can see a real divergence and a
null on the causal substrate is meaningful.  If it canNOT, the estimator is too blunt
and the whole campaign's null would be an artefact -- so this gate runs FIRST.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from xi_suite import build_lattice_3d, measure_point  # noqa: E402


def main():
    t0 = time.time()
    ms = [6, 8, 10, 12]
    Js = [0.45, 0.55, 0.62, 0.66, 0.69, 0.72, 0.78, 0.90, 1.10]
    cfg = dict(n_burn=400, n_meas=80, meas_every=2)
    n_seeds = 4
    sizes = []
    for m in ms:
        graphs = [build_lattice_3d(m) for _ in range(n_seeds)]  # deterministic graph; seeds differ in MC
        rows = [measure_point(graphs, J, L_s=float(m), **cfg) for J in Js]
        chi = [r["chi"] for r in rows]
        Jc = Js[int(np.argmax(chi))]
        zc = rows[int(np.argmin([abs(r["J"] - Jc) for r in rows]))]["z_mean"]
        sizes.append({"m": m, "L": float(m), "L_s": float(m), "N": m ** 3,
                      "N_mean": float(m ** 3), "z_mean": zc, "Jc": Jc, "rows": rows})
        xol = [r["xi_over_L"] for r in rows]
        u4 = [r["U4"] for r in rows]
        chi = [r["chi"] for r in rows]
        jc = Js[int(np.argmax(chi))]
        print(f"  m={m:2d} N={m**3:4d}  Jc(chi)={jc:.2f}  "
              f"xi/L: {min(xol):.3f}-{max(xol):.3f}  U4: {min(u4):.2f}-{max(u4):.2f}  "
              f"chi_max={max(chi):.2f}", flush=True)

    # crossing check: at the largest J below ordering, does xi/L grow with m near Jc?
    # Report xi/L(m) at each J so the crossing is visible.
    print("\n  xi/L table (rows=J, cols=m):")
    print("   J     " + "  ".join(f"m={m}" for m in ms))
    for j, J in enumerate(Js):
        vals = [sizes[i]["rows"][j]["xi_over_L"] for i in range(len(ms))]
        print(f"  {J:.2f}  " + "  ".join(f"{v:.3f}" for v in vals))
    print("\n  U4 table (rows=J, cols=m):")
    for j, J in enumerate(Js):
        vals = [sizes[i]["rows"][j]["U4"] for i in range(len(ms))]
        print(f"  {J:.2f}  " + "  ".join(f"{v:.3f}" for v in vals))

    out = {"control": "O3_periodic_lattice_3D",
           # analyse-compatible lever schema (identical pipeline as the campaign)
           "lever": "POSITIVE_CONTROL_lattice3d", "external_scale": None,
           "dim": 3, "Ls": [float(m) for m in ms], "Js": Js,
           "ms": ms, "cfg": cfg, "n_seeds": n_seeds, "sizes": sizes,
           "runtime_s": time.time() - t0}
    (HERE / "validate_positive.json").write_text(json.dumps(out, indent=2))
    print(f"\nruntime {out['runtime_s']:.1f}s -> validate_positive.json")


if __name__ == "__main__":
    main()
