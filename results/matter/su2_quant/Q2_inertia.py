"""Q2 -- rotational inertia tensor and the (un-constrained) spin spectrum.

I_ab = integral Tr[xi_a^dag xi_b] d^3x = 2 sum_sites (xi_a . xi_b) dx^3 (the zero modes
of Q1).  For the hedgehog (SO(3)-symmetric) it must be spherical, I_ab = I delta_ab.
With I, the rigid-rotor (collective-coordinate) spectrum is

    E_j = j(j+1) / (2I) ,   j = 0, 1/2, 1, 3/2, ...

(no Finkelstein-Rubinstein constraint yet; that selects half-integer j in Q4).

ANTI-CIRCULARITY: I_ab is a real overlap integral of quaternion tangents; "spin j" is a
label of the rotor spectrum, used in COMPARISON ONLY notes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2q_core as q   # noqa: E402


def main():
    U0, dx, M, E2, E4, xs = q.skyrmion(e_sk=4.0, N=41, L=16.0)
    I, xis = q.inertia_tensor(U0, dx)
    diag = np.diag(I)
    offdiag = I - np.diag(diag)
    I_mean = float(np.mean(diag))
    diag_spread = float((np.max(diag) - np.min(diag)) / I_mean)
    offdiag_rel = float(np.max(np.abs(offdiag)) / I_mean)
    spherical = bool(diag_spread < 0.05 and offdiag_rel < 0.05)

    js = [0.0, 0.5, 1.0, 1.5, 2.0]
    spectrum = {f"j={j}": j * (j + 1) / (2 * I_mean) for j in js}

    payload = {"e_sk": 4.0, "M_Sk": M,
               "inertia_tensor": I.tolist(), "I_diag": diag.tolist(),
               "I_mean": I_mean, "diag_spread": diag_spread,
               "offdiag_rel": offdiag_rel, "spherical": spherical,
               "spectrum_E_j": spectrum,
               "E_half": 0.5 * 1.5 / (2 * I_mean),
               "verdict": "SIM" if spherical else "NAO"}
    q.save_json("Q2_inertia", payload)

    print("=" * 70)
    print("Q2 -- ROTATIONAL INERTIA TENSOR AND SPIN SPECTRUM")
    print("=" * 70)
    print("inertia tensor I_ab:")
    for row in I:
        print("   ", np.round(row, 4))
    print(f"I (mean diag) = {I_mean:.3f}   diag spread = {diag_spread:.2e}   "
          f"offdiag/I = {offdiag_rel:.2e}")
    print(f"spherical (I_ab = I delta_ab): {'SIM' if spherical else 'NAO'}")
    print("rotor spectrum E_j = j(j+1)/(2I):")
    for j in js:
        print(f"   j={j}:  E = {j*(j+1)/(2*I_mean):.5f}")
    print("-" * 70)
    print(f"VERDICT: I spherical, spectrum computed: {'SIM' if spherical else 'NAO'}")
    return payload


if __name__ == "__main__":
    main()
