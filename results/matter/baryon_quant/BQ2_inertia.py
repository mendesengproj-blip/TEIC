"""BQ2 -- the FULL moment of inertia (sigma + Skyrme), correcting Q2.

Q2 measured I = 312.7 from the 3D zero-mode overlap 2 int xi.xi -- the SIGMA-model
inertia ONLY.  The Skyrme 4-derivative term also contributes to the rotational
inertia (the rotor stiffens).  BQ2:

  (G0) cross-check the sigma integrand: the lattice 3D zero-mode I_sigma must equal
       the radial integral (16 pi/3) int r^2 sin^2 F dr from the SAME profile;
  (1)  measure the Skyrme contribution fraction f_Sk = Lhat_Skyrme/Lhat (a pure
       number of the universal profile, from the ANW-validated reduced solver);
  (2)  report the corrected full inertia and the downstream correction to the
       rotor energies E_{1/2} = 3/(8 I) and the N-Delta splitting 3/(2 I).

PRE-REGISTERED KILL: if the reduced-solver profile disagrees with the lattice
profile's sigma-inertia by >5% the engines are inconsistent -> STOP.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "su2"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "su2_quant"))
import su2_core as s
import su2q_core as q
import bq_core as b

PI = np.pi


def main():
    # --- G0: lattice 3D zero-mode sigma-inertia (Q2 setup, e_sk=4) ---
    U0, dx, M, E2, E4, xs = q.skyrmion(e_sk=4.0, N=41, L=16.0, rmax=14.0, nr=360)
    I3d, _ = q.inertia_tensor(U0, dx)
    I_sigma_lattice = float(np.mean(np.diag(I3d)))

    # same lattice profile -> radial sigma-inertia (16 pi/3) int r^2 sin^2 F dr
    r, dr = s.radial_grid(rmax=14.0, n=360)
    F_lat, _, _ = s.radial_relax(r, dr, 4.0)
    s2 = np.sin(F_lat) ** 2
    I_sigma_radial = float((16.0 * PI / 3.0) * np.sum(r ** 2 * s2) * dr)
    g0_rel = abs(I_sigma_lattice - I_sigma_radial) / I_sigma_radial
    g0_ok = g0_rel < 0.05

    # --- Skyrme inertia fraction from the ANW-validated reduced universal profile ---
    Fr, x, dxr, Ehat = b.relax_profile()
    Lhat, Lsig, Lsky = b.inertia_integral(Fr, x, dxr)
    f_Sk = Lsky / Lhat                      # Skyrme fraction (pure number)
    ratio_sky_sig = Lsky / Lsig             # full = sigma * (1 + this)

    # full inertia in lattice units = sigma-lattice * (1 + Lsky/Lsig)
    I_full_lattice = I_sigma_lattice * (1.0 + ratio_sky_sig)

    # downstream corrections (lattice units)
    E_half_sigma_only = 3.0 / (8.0 * I_sigma_lattice)     # what Q2 would give
    E_half_full = 3.0 / (8.0 * I_full_lattice)            # corrected
    split_sigma_only = 3.0 / (2.0 * I_sigma_lattice)
    split_full = 3.0 / (2.0 * I_full_lattice)

    payload = dict(
        I_sigma_lattice_3d_zeromode=I_sigma_lattice,
        I_sigma_radial_integral=I_sigma_radial,
        G0_sigma_crosscheck_rel=g0_rel, G0_ok=bool(g0_ok),
        Lhat_total=Lhat, Lhat_sigma=Lsig, Lhat_skyrme=Lsky,
        skyrme_inertia_fraction=f_Sk,
        skyrme_over_sigma=ratio_sky_sig,
        I_full_over_I_sigma=1.0 + ratio_sky_sig,
        I_full_lattice=I_full_lattice,
        E_half_sigma_only_Q2=E_half_sigma_only,
        E_half_full_corrected=E_half_full,
        E_half_correction_factor=E_half_full / E_half_sigma_only,
        NDelta_split_sigma_only=split_sigma_only,
        NDelta_split_full=split_full,
        note=("Q2's inertia was sigma-only; the Skyrme term adds "
              f"{ratio_sky_sig*100:.0f}% -> full inertia is {1+ratio_sky_sig:.3f}x "
              "larger, so the rotor energies (and N-Delta splitting in lattice "
              f"units) are {E_half_full/E_half_sigma_only:.3f}x smaller than Q2."),
        verdict="PASS" if g0_ok else "STOP",
    )
    b.save_json("BQ2_inertia", payload)
    print(f"BQ2  G0 sigma cross-check: lattice {I_sigma_lattice:.2f} vs radial "
          f"{I_sigma_radial:.2f}  ({g0_rel*100:.1f}%)  ok={g0_ok}")
    print(f"     Skyrme inertia fraction = {f_Sk:.3f}  (full inertia "
          f"{1+ratio_sky_sig:.3f}x the sigma-only Q2 value)")
    print(f"     => rotor energies {E_half_full/E_half_sigma_only:.3f}x smaller; "
          f"full I (lattice units) = {I_full_lattice:.1f}")
    return payload


if __name__ == "__main__":
    main()
