"""PI1 -- B=1: the suspension acts. Pre-registered (MATTER_PI1_B2.md):

  2pi spatial rotation of the hedgehog: class 1 (generator; suspended Hopf)
  4pi rotation (loop traversed twice):  class 0 (2-torsion)

KILL: (2pi, 4pi) != (1, 0) -- the suspension structure does not act on the
network fields; the whole FR route is wrong for this network.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc

L, N = 12.0, 33
NS_2PI, NS_4PI = 32, 64


def main():
    X, Y, Z, _ = pc.spatial_grid(L, N)
    print("PI1: 2pi rotation (predict 1)", flush=True)
    r2pi = pc.z2_class_multi(pc.loop_rotation_b1(X, Y, Z, NS_2PI, turns=1), "2pi")
    print("PI1: 4pi rotation (predict 0)", flush=True)
    r4pi = pc.z2_class_multi(pc.loop_rotation_b1(X, Y, Z, NS_4PI, turns=2), "4pi")

    verdict = {"class_2pi": r2pi["value"], "class_4pi": r4pi["value"],
               "predicted": {"2pi": 1, "4pi": 0},
               "death": not (r2pi["value"] == 1 and r4pi["value"] == 0)}
    pc.save_json("PI1_b1_rotation.json",
                 {"rot_2pi": r2pi, "rot_4pi": r4pi, "verdict": verdict})
    print(json.dumps(verdict, indent=2))


if __name__ == "__main__":
    main()
