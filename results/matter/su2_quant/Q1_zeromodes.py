"""Q1 -- rotational zero modes of the Skyrmion (mandatory gate).

The Skyrmion's orientation is a collective coordinate: rotating it costs ZERO energy.
For the SU3 hedgehog U_0, a global SU(2) rotation U -> A U_0 A^dag has identical energy
(an exact symmetry of the lattice chiral action, since 1/2 Tr and the current cross-
products are conjugation invariant).  The three generators give three zero modes

    xi_a(x) = d/d(angle) [A U_0 A^dag]|_0 = [T_a, U_0],   T_a = (0, e_a/2) ,

tangent to S^3 at every site.  We verify:
  1. E[A U_0 A^dag] = E[U_0] to < 0.1% (the prompt's gate; here ~ machine precision);
  2. xi_a is tangent (xi_a . U_0 = 0) and matches the finite-difference derivative;
  3. the three modes are orthogonal with a common norm (-> spherical inertia, Q2).

ANTI-CIRCULARITY: A are unit quaternions (su2_core, no Pauli/complex); the angle is a
real geometric rotation angle.  "spin"/"angular momentum" only in COMPARISON ONLY notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2q_core as q   # noqa: E402
import su2_core as s    # noqa: E402

E_SK = 4.0


def main():
    U0, dx, M, E2, E4, xs = q.skyrmion(e_sk=E_SK, N=41, L=16.0)

    # 1) energy invariance under finite rotations about each axis
    inv = []
    for a in range(3):
        for angle in (0.3, 0.7, 1.5):
            UR = q.iso_rotate(U0, q.rotation_quat(a, angle))
            ER = s.chiral_energy(UR, dx, E_SK)[2]
            inv.append({"axis": a, "angle": angle, "E": ER,
                        "rel_diff": abs(ER - M) / M})
    max_rel = max(d["rel_diff"] for d in inv)
    energy_ok = max_rel < 1e-3

    # 2) zero modes: tangency and finite-difference match
    xis = [q.zero_mode(U0, a) for a in range(3)]
    tangency = [float(np.max(np.abs(np.sum(xi * U0, axis=-1)))) for xi in xis]
    fd_err = []
    h = 1e-5
    for a in range(3):
        UR = q.iso_rotate(U0, q.rotation_quat(a, h))
        xi_fd = (UR - U0) / h
        fd_err.append(float(np.max(np.abs(xi_fd - xis[a]))))
    tangency_ok = max(tangency) < 1e-12
    fd_ok = max(fd_err) < 1e-4

    # 3) orthogonality / common norm (overlap matrix = inertia tensor / convention)
    G = np.zeros((3, 3))
    for a in range(3):
        for b in range(3):
            G[a, b] = q.mode_overlap(xis[a], xis[b], dx)
    diag = np.diag(G)
    offdiag_max = float(np.max(np.abs(G - np.diag(diag))))
    diag_spread = float((np.max(diag) - np.min(diag)) / np.mean(diag))
    ortho_ok = offdiag_max / np.mean(diag) < 0.05 and diag_spread < 0.05

    n_modes = 3
    all_ok = energy_ok and tangency_ok and fd_ok and ortho_ok
    payload = {"e_sk": E_SK, "M_Sk": M, "n_zero_modes": n_modes,
               "energy_invariance_max_rel_diff": max_rel,
               "energy_invariance_ok": bool(energy_ok),
               "tangency_max": max(tangency), "tangency_ok": bool(tangency_ok),
               "finite_diff_err_max": max(fd_err), "fd_ok": bool(fd_ok),
               "overlap_matrix": G.tolist(), "diag": diag.tolist(),
               "offdiag_max": offdiag_max, "diag_spread": diag_spread,
               "orthogonal_common_norm": bool(ortho_ok),
               "verdict": "SIM" if all_ok else "NAO"}
    q.save_json("Q1_zeromodes", payload)

    print("=" * 70)
    print("Q1 -- ROTATIONAL ZERO MODES (gate)")
    print("=" * 70)
    print(f"Skyrmion mass M_Sk = {M:.3f}  (e_sk={E_SK})")
    print(f"1 energy invariance E[A U A^dag]=E[U]: max rel diff = {max_rel:.2e} "
          f"-> {'OK' if energy_ok else 'FAIL'}")
    print(f"2 tangency xi.U=0: max = {max(tangency):.2e} -> {'OK' if tangency_ok else 'FAIL'}")
    print(f"  finite-diff match: max err = {max(fd_err):.2e} -> {'OK' if fd_ok else 'FAIL'}")
    print(f"3 overlap (inertia) diag = {np.round(diag,3)}  offdiag_max={offdiag_max:.2e}")
    print(f"  orthogonal + common norm -> {'OK' if ortho_ok else 'FAIL'}")
    print("-" * 70)
    print(f"VERDICT: {n_modes} zero modes verified: {'SIM' if all_ok else 'NAO'}")
    return payload


if __name__ == "__main__":
    main()
