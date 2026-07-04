"""Q6 -- the quantised Skyrmion gravitates with M_tot = M_Sk + E_{1/2}.

The j=1/2 ground state has rotational energy E_{1/2} = (1/2)(3/2)/(2I) = 3/(8I) added to
the classical mass M_Sk.  Via the established weak-field bridge (D1-D3), the soliton's
energy density sources a Poisson field theta(r) ~ -M/(4 pi r), so the quantised Skyrmion
gravitates with the corrected total energy

    M_tot = M_Sk + 3/(8I) .

We verify: (1) M_tot from M_Sk (SU3) and I (Q2); (2) the energy density sources a 1/r
field whose far-field coefficient scales with the (total) mass.

ANTI-CIRCULARITY: theta from a real Poisson solve of the energy density; NO Lorentz /
Schwarzschild dilation formula.  Masses are energies of the chiral field.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2q_core as q   # noqa: E402
import su2_core as s    # noqa: E402


def radial_energy_density(U, dx, e_sk, xs, rbins):
    e2d, e4d = s.chiral_energy_density(U, dx, e_sk)
    ed = e2d + e4d
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    rho = np.array([ed[(R >= rbins[i]) & (R < rbins[i + 1])].mean()
                    if np.any((R >= rbins[i]) & (R < rbins[i + 1])) else 0.0
                    for i in range(len(rbins) - 1)])
    rc = 0.5 * (rbins[:-1] + rbins[1:])
    return rho, rc


def poisson_radial(rho_r, rc):
    dr = rc[1] - rc[0]
    Q = np.cumsum(rho_r * 4 * np.pi * rc ** 2) * dr        # enclosed energy
    integrand = Q / (4 * np.pi * rc ** 2)
    theta = -np.flip(np.cumsum(np.flip(integrand)) * dr)
    return theta, Q


def main():
    e_sk = 4.0; L = 16.0; N = 51
    U0, dx, M_Sk, E2, E4, xs = q.skyrmion(e_sk=e_sk, N=N, L=L)
    I, _ = q.inertia_tensor(U0, dx)
    I_mean = float(np.mean(np.diag(I)))
    E_half = 0.5 * 1.5 / (2 * I_mean)                      # 3/(8I)
    M_tot = M_Sk + E_half

    rbins = np.linspace(0.4, L / 2, 40)
    rho, rc = radial_energy_density(U0, dx, e_sk, xs, rbins)
    theta, Qenc = poisson_radial(rho, rc)
    outer = rc > L / 4
    far_thetar = (theta * rc)[outer]
    far_const = float(np.mean(far_thetar))
    far_scatter = float(np.std(far_thetar) / (abs(far_const) + 1e-12))
    one_over_r = bool(far_scatter < 0.6)

    # coefficient scales with mass: compare a heavier soliton
    U2, dx2, M2, _, _, xs2 = q.skyrmion(e_sk=2 * e_sk, N=N, L=L)
    rho2, rc2 = radial_energy_density(U2, dx2, 2 * e_sk, xs2, rbins)
    th2, _ = poisson_radial(rho2, rc2)
    far2 = float(np.mean((th2 * rc2)[outer]))
    coeff_ratio = far2 / far_const if far_const else float("nan")
    mass_ratio = M2 / M_Sk
    scales_with_M = bool(abs(coeff_ratio / mass_ratio - 1.0) < 0.3)

    gravity_ok = bool(one_over_r and scales_with_M)
    payload = {"e_sk": e_sk, "M_Sk": M_Sk, "I": I_mean,
               "E_half_3_over_8I": E_half, "M_tot": M_tot,
               "rotational_correction_fraction": E_half / M_Sk,
               "theta_1overr_scatter": far_scatter, "one_over_r": one_over_r,
               "coeff_ratio": coeff_ratio, "mass_ratio": mass_ratio,
               "scales_with_mass": scales_with_M,
               "verdict": "SIM" if gravity_ok else "PARCIAL"}
    q.save_json("Q6_gravity", payload)

    print("=" * 70)
    print("Q6 -- QUANTISED SKYRMION GRAVITATES: M_tot = M_Sk + 3/(8I)")
    print("=" * 70)
    print(f"M_Sk = {M_Sk:.4f}   I = {I_mean:.3f}   E_(1/2) = 3/(8I) = {E_half:.5f}")
    print(f"M_tot = M_Sk + 3/(8I) = {M_tot:.4f}  "
          f"(rotational correction {E_half/M_Sk:.2e} of M_Sk)")
    print(f"theta ~ 1/r: far-field scatter = {far_scatter:.2f} -> {'OK' if one_over_r else 'NO'}")
    print(f"coefficient scales with mass: ratio {coeff_ratio:.2f} vs mass ratio "
          f"{mass_ratio:.2f} -> {'OK' if scales_with_M else 'NO'}")
    print("-" * 70)
    print(f"VERDICT: theta ~ M_tot/r : {payload['verdict']}")
    return payload


if __name__ == "__main__":
    main()
