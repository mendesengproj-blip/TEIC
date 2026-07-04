"""FR3 -- spatial rotations act on the network Skyrmion through the double
cover: U0(R(theta) x) = D(theta) U0(x) D(theta)^dagger pointwise, with D(theta)
the CONTINUOUS lift; the lift path ends at D(2pi) = -identity (W = 1 antipodal
crossing -- the invariant MATTER_SU2_QUANT's FR machinery counts).

Measured content: at each sampled theta the identity holds at machine
precision for the lift branch CONTINUOUS with the previous step (the other
sign also satisfies the conjugation identity -- conjugation kills the sign --
but breaks continuity of the path in SU(2); continuity is what forces the
path to end at the antipode). Pre-registered: identity < 1e-12 at every theta;
q(2pi) = (-1,0,0,0); W = 1.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fr_core as fc
from fr_core import s2

THETAS = np.linspace(0.0, 2.0 * np.pi, 17)


def main():
    X, Y, Z, dx = fc.grid()
    U_base = fc.hedgehog_at(X, Y, Z, (0.0, 0.0, 0.0))

    rows = []
    q_prev = np.array([1.0, 0.0, 0.0, 0.0])
    crossings = 0
    for th in THETAS:
        c, s = np.cos(th), np.sin(th)
        Xr, Yr = c * X + s * Y, -s * X + c * Y          # R(theta)^{-1} x
        U_rot = fc.hedgehog_at(Xr, Yr, Z, (0.0, 0.0, 0.0))
        q = np.array([np.cos(th / 2.0), 0.0, 0.0, np.sin(th / 2.0)])
        # continuous branch: pick the sign closest to the previous step
        if np.dot(q, q_prev) < 0:
            q = -q
        err = fc.qdist(U_rot, fc.conj_global(U_base, q))[0]
        # antipodal-crossing counter (equator a0 = 0, the W of SU2_QUANT)
        if q_prev[0] > 0 >= q[0] or q_prev[0] >= 0 > q[0]:
            crossings += 1
        rows.append({"theta_over_pi": th / np.pi, "q0": float(q[0]),
                     "identity_err_max": err})
        q_prev = q

    q_end = q_prev
    payload = {
        "path": rows,
        "worst_identity_error": float(max(r["identity_err_max"] for r in rows)),
        "q_end": [float(v) for v in q_end],
        "q_end_is_minus_identity": bool(
            abs(q_end[0] + 1.0) < 1e-12 and np.max(np.abs(q_end[1:])) < 1e-12),
        "antipodal_crossings_W": crossings,
        "pre_registered": {"identity": "<1e-12", "q_end": [-1, 0, 0, 0],
                           "W": 1},
    }
    fc.save_json("FR3_doublecover.json", payload)
    print(json.dumps({k: payload[k] for k in
                      ("worst_identity_error", "q_end",
                       "q_end_is_minus_identity", "antipodal_crossings_W")},
                     indent=2))


if __name__ == "__main__":
    main()
