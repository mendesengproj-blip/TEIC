"""PI3 -- B=2: the FR theorem becomes a measurement. Pre-registered
(MATTER_PI1_B2.md):

  exchange loop (FR1 half-turn path + slerp closing segment): class 1
  exchange traversed twice:                                   class 0

  => [exchange] = [2pi rotation of one soliton] = 1 in Z2: the imported
     homotopy step (Williams 1970) becomes a MEASURED equality of classes.

Engineering (pre-registered): the slerp closing segment is valid only if the
max pointwise distance U(1) <-> U(0) is < 0.5 (far from antipodal).

KILL: (exchange, exchange^2) != (1, 0) -- exchange is NOT homotopic to the
2pi rotation on the network; the FR theorem does not apply to this substrate.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc

L, N, D_SEP = 24.0, 41, 6.0
N_PATH, N_CLOSE = 48, 8


def main():
    X, Y, Z, _ = pc.spatial_grid(L, N)
    print("PI3: exchange loop (predict 1)", flush=True)
    loop1, closure = pc.loop_exchange_b2(X, Y, Z, N_PATH, N_CLOSE, d=D_SEP,
                                         traversals=1)
    slerp_valid = closure < pc.SLERP_MAX_DIST
    print(f"  closure max |U(1)-U(0)| = {closure:.4f} "
          f"(slerp valid: {slerp_valid})", flush=True)
    r_ex = pc.z2_class_multi(loop1, "exch")
    del loop1

    print("PI3: exchange traversed twice (predict 0)", flush=True)
    loop2, _ = pc.loop_exchange_b2(X, Y, Z, N_PATH, N_CLOSE, d=D_SEP,
                                   traversals=2)
    r_ex2 = pc.z2_class_multi(loop2, "exch^2")
    del loop2

    verdict = {"closure_max": closure, "slerp_valid": bool(slerp_valid),
               "class_exchange": r_ex["value"],
               "class_exchange_squared": r_ex2["value"],
               "predicted": {"exchange": 1, "exchange^2": 0},
               "death": not (slerp_valid and r_ex["value"] == 1
                             and r_ex2["value"] == 0)}
    pc.save_json("PI3_b2_exchange.json",
                 {"exchange": r_ex, "exchange_squared": r_ex2,
                  "verdict": verdict})
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()
