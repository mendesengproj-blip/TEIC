"""SU7 -- spin-1/2: does a 2pi rotation send the Skyrmion state to MINUS itself?

The topological prerequisite is real: pi_4(SU(2)) = Z_2, so a 2pi spatial rotation of a
B=1 Skyrmion traces a NON-contractible loop in configuration space (Finkelstein-Rubinstein).
This is what ALLOWS half-integer spin -- the deepest reason a soliton can be a fermion.

But the SIGN flip |psi> -> -|psi> is a QUANTUM statement about the wavefunction on
configuration space; it requires quantising the collective (rotational) coordinate.  A
CLASSICAL field configuration is unchanged by a 2pi rotation (it returns to ITSELF, with
field overlap +1).  We therefore:

  1. rotate the hedgehog field spatially by alpha in [0, 2pi] and measure the normalised
     field overlap O(alpha) = <U(0), U(alpha)> -- classically O(2pi) = +1 (no sign);
  2. confirm the configuration-space loop is the non-trivial pi_4 = Z_2 element via the
     SU(2) ISOROTATION that a spatial 2pi rotation induces on the hedgehog (the hedgehog
     locks isospin to space, so a 2pi spatial rotation = a 2pi isorotation = the SU(2)
     element exp(i 2pi n.sigma/... ) = -1, the double cover);
  3. report HONESTLY: the classical field gives +1 (boson-like); the -1 sign is a
     quantum FR phase the classical lattice cannot certify.  SU7 = NAO (not verified).

ANTI-CIRCULARITY: "spin"/"fermion"/"proton" are names; the rotation is a geometric
transform of the quaternion field; the overlap and the SU(2) trace are real.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402


def converged_profile():
    r, dr = s.radial_grid(rmax=14.0, n=360)
    F, E2, E4 = s.radial_relax(r, dr, 2.0)
    return s.profile_from_radial(F, r)


def rotate_field_z(U, xs, alpha):
    """Rigidly rotate the hedgehog field by angle alpha about the z-axis in SPACE: the
    field is resampled at the rotated coordinates U_rot(x) = U(R_z(-alpha) x).  (For the
    hedgehog the spatial rotation also rotates rhat, locking iso to space.)"""
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    ca, sa = np.cos(alpha), np.sin(alpha)
    Xr = ca * X + sa * Y
    Yr = -sa * X + ca * Y
    # trilinear resample of each quaternion component at (Xr,Yr,Z)
    return _resample(U, xs, Xr, Yr, Z)


def _resample(U, xs, Xr, Yr, Zr):
    L = xs[-1] - xs[0]; N = len(xs); dx = xs[1] - xs[0]
    def idx(c):
        f = (c - xs[0]) / dx
        i0 = np.clip(np.floor(f).astype(int), 0, N - 2)
        return i0, f - i0
    ix, fx = idx(Xr); iy, fy = idx(Yr); iz, fz = idx(Zr)
    out = np.zeros_like(U)
    for dxk, wx in ((0, 1 - fx), (1, fx)):
        for dyk, wy in ((0, 1 - fy), (1, fy)):
            for dzk, wz in ((0, 1 - fz), (1, fz)):
                w = (wx * wy * wz)[..., None]
                out += w * U[ix + dxk, iy + dyk, iz + dzk]
    return s.q_normalize(out)


def field_overlap(Ua, Ub):
    """Normalised field overlap <Ua,Ub> = mean of the 4D dot product over sites (=+1 if
    identical, sign-sensitive)."""
    return float(np.mean(np.sum(Ua * Ub, axis=-1)))


def main():
    prof = converged_profile()
    L = 14.0; N = 41
    xs = np.linspace(-L / 2, L / 2, N)
    U0 = s.hedgehog_field(xs, xs, xs, profile=prof)

    alphas = np.linspace(0, 2 * np.pi, 13)
    overlaps = [field_overlap(U0, rotate_field_z(U0, xs, a)) for a in alphas]
    overlap_2pi = overlaps[-1]
    classical_returns_plus = abs(overlap_2pi - 1.0) < 0.05    # classical: +1, no sign

    # The induced ISOROTATION of a 2pi spatial rotation on the hedgehog is the SU(2)
    # element exp(i 2pi (z-axis).sigma /2)?  A 2pi rotation in SO(3) lifts to -1 in SU(2):
    # quaternion of a 2pi rotation about z = (cos(pi), 0,0, sin(pi)) = (-1,0,0,0) = -identity.
    iso_2pi = s.q_from_axis_angle(np.array([0.0, 0.0, 1.0]), np.pi)   # half-angle pi
    iso_trace = float(s.half_trace(iso_2pi))                           # = cos(pi) = -1
    double_cover_minus1 = abs(iso_trace + 1.0) < 1e-12

    payload = {
        "alphas": alphas.tolist(), "field_overlaps": overlaps,
        "overlap_at_2pi": overlap_2pi,
        "classical_field_returns_+state": bool(classical_returns_plus),
        "pi4_SU2": "Z_2 (a 2pi rotation is the non-trivial class -> half-integer spin ALLOWED)",
        "su2_double_cover_2pi_rotation": {"half_trace": iso_trace,
                                          "is_minus_identity": bool(double_cover_minus1)},
        "spin_half_verified": False,
        "honest_note": (
            "The SU(2) double cover gives -1 for a 2pi rotation (the topological "
            "prerequisite for spin-1/2 is present: pi_4(SU(2))=Z_2). But the classical "
            "field configuration returns to +itself under a 2pi spatial rotation "
            "(overlap +1): the |psi> -> -|psi> sign is a QUANTUM Finkelstein-Rubinstein "
            "phase on the quantised collective coordinate, which a classical lattice "
            "field theory cannot produce. Spin-1/2 is ALLOWED and topologically natural, "
            "but NOT verified here."),
        "verdict": "NAO",
    }
    s.save_json("SU7_spin", payload)

    print("=" * 70)
    print("SU7 -- SPIN-1/2 via 2pi ROTATION")
    print("=" * 70)
    print("alpha/pi :", [round(a / np.pi, 2) for a in alphas])
    print("overlap  :", [round(o, 3) for o in overlaps])
    print(f"classical field overlap at 2pi = {overlap_2pi:+.4f} (-> returns to +state)")
    print(f"SU(2) double cover: 1/2Tr(2pi rotation) = {iso_trace:+.3f} "
          f"(= -1, the -identity)")
    print("-" * 70)
    print("pi_4(SU(2)) = Z_2: spin-1/2 is ALLOWED (topological prerequisite present).")
    print("Classical field returns to +itself; the -sign is a QUANTUM FR phase.")
    print("VERDICT: spin-1/2 (2pi -> -state) NAO verificavel classicamente")
    return payload


if __name__ == "__main__":
    main()
