"""FR2 -- exchange endpoint = rigid spatial half-turn endpoint, up to one
GLOBAL isospin conjugation: an EXACT identity for hedgehogs (pre-registered
< 1e-12), tested at machine precision via analytic evaluation.

The rigid half-turn about z maps x -> R_z(pi)^{-1} x. For the hedgehog,
U0(R x - c) = D U0(x - R^{-1} c) D^dagger with D the SU(2) lift of R; applied
to the pair, the rigid endpoint equals the exchange endpoint conjugated by the
single global element D(pi) = lift of R_z(pi) (quaternion (0,0,0,1)).
Both sign lifts and both conjugation directions are tested; the matching one
is reported (sign conventions only).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import fr_core as fc

D_SEP = 8.0


def main():
    X, Y, Z, dx = fc.grid()
    c1 = (0.5 * D_SEP, 0.0, 0.0)
    c2 = (-0.5 * D_SEP, 0.0, 0.0)

    # exchange endpoint: positions swapped, orientations fixed, SAME factor order
    U_exch = fc.pair(X, Y, Z, c2, c1)

    # rigid endpoint: the s=0 pair evaluated at R_z(pi)^{-1} x = (-x, -y, z)
    U_rigid = fc.pair(-X, -Y, Z, c1, c2)

    Dz = np.array([0.0, 0.0, 0.0, 1.0])            # lift of R_z(pi): exp(i pi sz/2)
    candidates = {
        "D U_exch D^-1": fc.conj_global(U_exch, Dz),
        "D^-1 U_exch D": fc.conj_global(U_exch, fc.s2.q_conj(Dz)),
        "U_exch (no conj)": U_exch,
    }
    errors = {}
    for name, V in candidates.items():
        emax, emean = fc.qdist(U_rigid, V)
        errors[name] = {"max": emax, "mean": emean}
    best = min(errors, key=lambda k: errors[k]["max"])

    payload = {"separation": D_SEP,
               "errors": errors, "matching_form": best,
               "machine_precision": bool(errors[best]["max"] < 1e-12),
               "pre_registered": "exact identity < 1e-12 with ONE global "
                                 "isospin conjugation D(pi)"}
    fc.save_json("FR2_rigid.json", payload)
    print(json.dumps(payload, indent=2, default=str))


if __name__ == "__main__":
    main()
