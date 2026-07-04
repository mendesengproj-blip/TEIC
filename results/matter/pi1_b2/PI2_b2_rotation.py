"""PI2 -- B=2: the spin spectrum of the composite. Pre-registered
(MATTER_PI1_B2.md):

  2pi rotation of ONE soliton of the pair (about its own center): class 1
  2pi rigid rotation of the WHOLE pair (about the midpoint):      class 0
      (degree-B map: rotation-loop class = B mod 2 = 0 -- the B=2
       composite is bosonic)

KILL: (one, pair) != (1, 0) -- composite spin spectrum inconsistent.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc

L, N, NS, D_SEP = 24.0, 41, 48, 6.0


def main():
    X, Y, Z, _ = pc.spatial_grid(L, N)
    print("PI2: 2pi rotation of one soliton (predict 1)", flush=True)
    r_one = pc.z2_class_multi(
        pc.loop_rotation_one_b2(X, Y, Z, NS, d=D_SEP, turns=1), "one")
    print("PI2: 2pi rigid rotation of the pair (predict 0)", flush=True)
    r_pair = pc.z2_class_multi(
        pc.loop_rotation_pair_b2(X, Y, Z, NS, d=D_SEP), "pair")

    verdict = {"class_one_soliton_2pi": r_one["value"],
               "class_whole_pair_2pi": r_pair["value"],
               "predicted": {"one": 1, "pair": 0},
               "death": not (r_one["value"] == 1 and r_pair["value"] == 0)}
    pc.save_json("PI2_b2_rotation.json",
                 {"rot_one": r_one, "rot_pair": r_pair, "verdict": verdict})
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()
