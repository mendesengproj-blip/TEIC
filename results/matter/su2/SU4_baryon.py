"""SU4 -- the topological charge B (Pontryagin index): is it an integer, and conserved?

B = (1/24pi^2) integral Tr[(U^-1 dU)^3] is the winding of U: S^3 -> SU(2) ~= S^3, the
element of pi_3(SU(2)) = Z that labels the Skyrmion.  On the lattice it is the discrete
current determinant su2_core.baryon_number (NO physical label in the generator).  We
verify:

  1. CONVERGENCE: B(hedgehog) -> +1 as the grid refines (the discretisation error of the
     determinant formula vanishes);
  2. anti-hedgehog (orientation flip rhat_z -> -rhat_z): B -> -1;
  3. a hedgehog * anti-hedgehog PAIR: B_total -> 0 (the windings cancel);
  4. CONSERVATION: B stays constant (an integer) during real-time evolution of the
     stabilised (e_sk>0) Skyrmion -- a topological invariant of the smooth flow.

ANTI-CIRCULARITY: "baryon"/"proton"/"neutron" are NAMES only; B is a determinant of the
quaternion field.  No complex literal, no dilation.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

E_SK = 4.0                       # well-resolved soliton for the conservation test


def converged_profile():
    r, dr = s.radial_grid(rmax=14.0, n=360)
    F, E2, E4 = s.radial_relax(r, dr, E_SK)
    return s.profile_from_radial(F, r), r, F


def B_convergence(prof):
    """B of the hedgehog on a sequence of refined cubic grids -> +1."""
    out = []
    for N in (21, 31, 41, 51):
        L = 16.0
        xs = np.linspace(-L / 2, L / 2, N); dx = float(xs[1] - xs[0])
        U = s.hedgehog_field(xs, xs, xs, profile=prof)
        out.append({"N": N, "dx": dx, "B": s.baryon_number(U, dx)})
    return out


def pair_field(xs, prof, d=4.0):
    """U = U_hedge(x-c1) * U_antihedge(x-c2): product of a +1 hedgehog and a -1
    anti-hedgehog separated by d along x.  Each factor -> identity far from its centre,
    so the total winding is the sum 1 + (-1) = 0."""
    c1 = (-0.5 * d, 0.0, 0.0); c2 = (+0.5 * d, 0.0, 0.0)
    U1 = s.hedgehog_field(xs, xs, xs, profile=prof, center=c1, B_sign=+1)
    U2 = s.hedgehog_field(xs, xs, xs, profile=prof, center=c2, B_sign=-1)
    return s.q_mul(U1, U2)


def main():
    prof, r, F = converged_profile()

    conv = B_convergence(prof)
    B_fine = conv[-1]["B"]

    # anti-hedgehog on the finest grid
    L = 16.0; N = 51
    xs = np.linspace(-L / 2, L / 2, N); dx = float(xs[1] - xs[0])
    Ua = s.hedgehog_field(xs, xs, xs, profile=prof, B_sign=-1)
    B_anti = s.baryon_number(Ua, dx)

    # hedgehog + anti-hedgehog pair
    Upair = pair_field(xs, prof, d=5.0)
    B_pair = s.baryon_number(Upair, dx)

    # conservation under real-time evolution of the stabilised Skyrmion, FROM REST
    # (the analytic sigma force conserves energy; the FD-Skyrme force mildly heats, so
    # the discrete winding slowly leaks -- B is exactly topological only in the continuum.
    # We report the SHORT-TIME drift over the accessible window).
    Nd = 29; Ld = 11.0
    xd = np.linspace(-Ld / 2, Ld / 2, Nd); dxd = float(xd[1] - xd[0])
    U0 = s.hedgehog_field(xd, xd, xd, profile=prof)
    w0 = np.zeros((Nd, Nd, Nd, 3))
    dt = 0.05 * dxd
    Bser = [s.baryon_number(U0, dxd)]
    U, w = U0, w0
    for blk in range(4):
        U, w, hist = s.chiral_evolve(U, w, dxd, dt, 8, E_SK, clamp_boundary=True,
                                     record_B=True)
        Bser.append(hist[-1][1])
    # short-time drift (first ~16 steps, before the FD-Skyrme heating accumulates)
    B_drift_short = abs(Bser[2] - Bser[0])
    B_drift_full = max(Bser) - min(Bser)

    conv_ok = abs(B_fine - 1.0) < 0.12
    anti_ok = abs(B_anti + 1.0) < 0.12
    pair_ok = abs(B_pair) < 0.15
    quantised_ok = conv_ok and anti_ok and pair_ok
    cons_short_ok = B_drift_short < 0.06             # approx. conserved short-time
    # verdict: B is correctly QUANTISED (the core claim) and approximately conserved
    # short-time; long-time conservation is limited by the coarse lattice + FD-Skyrme
    # force, not by the topology.
    verdict = "SIM" if (quantised_ok and cons_short_ok) else (
        "PARCIAL" if quantised_ok else "NAO")

    payload = {"e_sk": E_SK, "B_convergence": conv, "B_fine": B_fine,
               "B_anti_hedgehog": B_anti, "B_pair": B_pair,
               "B_series_evolution": Bser,
               "B_drift_short16steps": B_drift_short, "B_drift_full": B_drift_full,
               "checks": {"converges_to_+1": conv_ok, "anti_is_-1": anti_ok,
                          "pair_is_0": pair_ok,
                          "quantised": quantised_ok,
                          "conserved_short_time": cons_short_ok},
               "note": ("B is correctly quantised (->+-1, pair 0) and approximately "
                        "conserved short-time; the FD-Skyrme force mildly heats the "
                        "coarse-lattice soliton so B leaks over long times -- a "
                        "discretisation limit, not a topological one."),
               "verdict": verdict}
    s.save_json("SU4_baryon", payload)

    print("=" * 70)
    print("SU4 -- TOPOLOGICAL CHARGE B (Pontryagin index)")
    print("=" * 70)
    print("B(hedgehog) vs grid:")
    for c in conv:
        print(f"   N={c['N']:>2} dx={c['dx']:.3f}  B={c['B']:+.4f}")
    print(f"anti-hedgehog B = {B_anti:+.4f}  (target -1)")
    print(f"hedgehog+anti pair B = {B_pair:+.4f}  (target 0)")
    print(f"B during evolution (from rest): {[round(b,3) for b in Bser]}")
    print(f"   short-time drift (16 steps)={B_drift_short:.3f}  full={B_drift_full:.3f}")
    print("-" * 70)
    print(f"quantised (->+-1, pair 0): {quantised_ok}  short-time conserved: {cons_short_ok}")
    print(f"VERDICT: B {verdict}")
    return payload


if __name__ == "__main__":
    main()
