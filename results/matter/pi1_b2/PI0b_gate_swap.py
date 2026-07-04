"""PI0b -- gate addendum: the SWAP-topology calibrator. Declared AFTER the
raw PI3 surprise and BEFORE running (order of events documented honestly).

WHY. PI3 measured the exchange loop at class 0 (stable, all engineering
green) against the FR/Williams expectation 1. Analysis found a hole in PI0:
the exchange preimage is a SINGLE curve winding the s-circle TWICE (the
strands swap) -- the first multi-winding case, never covered by the gate.
The constant-vector reference framing is validated only on winding-1
topology; on a framed double cover it can shift the Z2 reading by one unit
(the classical framed-transfer anomaly).

THE CALIBRATOR (class known analytically, swap topology guaranteed):
the axially-symmetric B=2 field with doubled azimuth, under the global
target-rotation 2pi loop. Its true class is B mod 2 = 0 (precomposition
with a degree-B map multiplies the suspended Hopf generator by B -- standard
suspension algebra, no FR input). Its preimage strands sit at azimuths
phi0 and phi0+pi and rotate by -pi s each: at s=1 they SWAP -- a single
winding-2 curve, the same topology class as the exchange loop.

PRE-REGISTERED READING (fixed before running):
  g5 = 0  -> the parity measurement is faithful on swap topology
             => PI3's raw 0 stands => FR identification FAILS on the network.
  g5 = 1  -> the framed-transfer anomaly is real (eps = 1 on this topology)
             => exchange class corrected to 0 XOR 1 = 1 => FR CONFIRMED,
             conditioned on the anomaly being uniform on the topology type
             (both curves are two-strand half-turn helices; stated openly).
Engineering: comps must be 1 (swap), chains closed, 3 regular values agree.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pi1_core as pc
from pi1_core import s2

L, N, NS = 16.0, 37, 48


def main():
    X, Y, Z, dx = pc.spatial_grid(L, N)
    W = pc.axial_b2(X, Y, Z)
    B = s2.baryon_number(W, dx)
    print(f"axial field: B = {B:.4f} (must be ~2)", flush=True)

    print("g5: target-rotation 2pi loop on axial B=2 (KNOWN class 0; "
          "swap topology)", flush=True)
    loop = pc.loop_target_rotation(W, NS)
    r = pc.z2_class_multi(loop, "g5-swap")

    swap_topology = all(d["n_components"] == 1 for d in r["details"])
    out = {
        "baryon_number": B,
        "g5": r,
        "swap_topology_confirmed": bool(swap_topology),
        "known_true_class": 0,
        "eps_anomaly": (None if r["value"] is None
                        else int(r["value"] != 0)),
    }
    pc.save_json("PI0b_gate_swap.json", out)
    print(json.dumps({"g5_class": r["value"], "stable": r["stable"],
                      "swap_topology": swap_topology,
                      "eps_anomaly": out["eps_anomaly"]}, indent=2))


if __name__ == "__main__":
    main()
