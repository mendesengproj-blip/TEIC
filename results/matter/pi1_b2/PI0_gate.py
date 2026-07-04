"""PI0 -- engineering gate for the Pontryagin-Thom Z2 machinery. RUNS FIRST.

Pre-registered (MATTER_PI1_B2.md). The gate validates the MACHINERY on loops
whose class is known a priori; it makes no physics verdict.

  g1  constant loop U_s = U0 (B=1):              class 0 (stable over 3 y)
  g1b translation loop (center on a circle,
      exactly closed, manifestly contractible):  class 0
  g2  (built into every measurement) class identical for 3 regular values
  g3  all preimage chains close; no boundary contact; frame dots >= sqrt(.5)
  g4  B=1 rotation loop class UNCHANGED under grid refinement N=33 -> 41
      (the value itself is judged in PI1, not here)

KILL (pre-registered): any of g1/g1b nonzero, instability across regular
values, unclosed chains after refinement, or boundary contact
=> MACHINERY DEAD -- campaign aborted with no physics verdict.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc

L_B1, N_B1, N_REF = 12.0, 33, 41
NS_CONST, NS_LOOP = 12, 32


def main():
    out = {}
    print("g1: constant loop (predict 0)", flush=True)
    X, Y, Z, dx = pc.spatial_grid(L_B1, N_B1)
    r = pc.z2_class_multi(pc.loop_constant(X, Y, Z, NS_CONST), "const")
    out["g1_constant"] = r

    print("g1b: translation loop (contractible; predict 0)", flush=True)
    r2 = pc.z2_class_multi(pc.loop_translation(X, Y, Z, NS_LOOP), "trans")
    out["g1b_translation"] = r2

    print("g4: rotation loop, base grid N=33", flush=True)
    r3 = pc.z2_class_multi(pc.loop_rotation_b1(X, Y, Z, NS_LOOP, turns=1), "rotN33")
    out["g4_rotation_N33"] = r3

    print("g4: rotation loop, refined grid N=41", flush=True)
    Xr, Yr, Zr, _ = pc.spatial_grid(L_B1, N_REF)
    r4 = pc.z2_class_multi(pc.loop_rotation_b1(Xr, Yr, Zr, NS_LOOP, turns=1), "rotN41")
    out["g4_rotation_N41"] = r4

    def ok_engineering(res):
        return all(d["ok"] for d in res["details"]) and res["stable"]

    gate = {
        "g1_zero": r["value"] == 0,
        "g1b_zero": r2["value"] == 0,
        "g2_stability_all": all(x["stable"] for x in (r, r2, r3, r4)),
        "g3_engineering_all": all(ok_engineering(x) for x in (r, r2, r3, r4)),
        "g4_refinement_stable": (r3["value"] is not None
                                 and r3["value"] == r4["value"]),
    }
    gate["MACHINERY_VALID"] = all(gate.values())
    out["gate"] = gate
    pc.save_json("PI0_gate.json", out)
    print(json.dumps(gate, indent=2))


if __name__ == "__main__":
    main()
