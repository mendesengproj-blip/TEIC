"""SU6 -- creation by collision: does a Skyrmion (B != 0) emerge from a SU(2) collision?

T3D4 collided two scalar chains in compact U(1) and produced a transient vortex but no
robust spontaneous winding.  Here we repeat with the chiral SU(2) field: two
counter-propagating chains, embedded in SU(2) with a TRANSVERSE (non-Abelian) tilt that
breaks the sigma_3 plane (a pure sigma_3/Abelian collision has B == 0 identically -- SU5),
giving pi_3 winding a fair chance.  We evolve with the full sigma + Skyrme action and
measure, in the LATE window, the topological charge B over 20 seeds.

Decisive observable: |B| in the late window.  If |B| ~ 1 emerges and persists -> a
Skyrmion was created from a causal-lattice collision.  If |B| stays ~ 0 -> the hedgehog
is a stable STATIC soliton (SU3) but is NOT spontaneously created by this collision
(Verdict C), as for the U(1) vortex.

ANTI-CIRCULARITY: quaternions only; "proton"/"baryon" are names; B is the determinant.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_dbi"))
import dbi_core as dbi  # noqa: E402  (two_packets)

N_SEEDS = 20
L = 12.0
N = 25
# The collision must evolve long enough for the chains to meet (~150 steps); with the
# costly FD-Skyrme force that is intractable over 20 seeds, so the collision is run with
# the FAST analytic sigma force (e_sk=0).  Rationale: the decisive question is whether
# pi_3 winding (B != 0) is spontaneously GENERATED; the Skyrme term (SU5) only
# STABILISES a B that already formed -- it cannot create winding that the collision does
# not produce.  If B stays ~0 in the sigma collision, no Skyrmion is created.
E_SK = 0.0
AMP = 2.5


def initial_collision(xs, rng):
    """Two counter-propagating scalar chains theta(x) embedded in SU(2), with a seed-
    dependent transverse tilt so the configuration is genuinely non-Abelian (axis varies
    in space, not fixed along sigma_3).  Returns (U, w) with w the angular velocity from
    the chains' motion."""
    dx = float(xs[1] - xs[0])
    th1d, vth1d = dbi.two_packets(xs, AMP, x0=4.0, w=1.6, noise=0.0, rng=rng)
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    th = np.repeat(np.repeat(th1d[:, None], N, 1)[:, :, None], N, 2)
    vth = np.repeat(np.repeat(vth1d[:, None], N, 1)[:, :, None], N, 2)
    # transverse tilt: the rotation axis rotates with a seed-random transverse pattern
    # (breaks the Abelian sigma_3 plane so B can be nonzero)
    kx = rng.uniform(0.4, 0.9); ky = rng.uniform(0.4, 0.9)
    tilt = 0.8
    axis = np.stack([tilt * np.sin(ky * Y), tilt * np.sin(kx * X + 0.5 * Z),
                     np.ones_like(X)], axis=-1)
    U = s.q_from_axis_angle(axis, th)
    # body angular velocity from the chain velocity (w ~ d/dt of the angle)
    nhat = axis / np.sqrt(np.sum(axis ** 2, -1, keepdims=True))
    w = vth[..., None] * nhat
    return s.q_normalize(U), w, dx


def run_seed(seed):
    rng = np.random.default_rng(1000 + seed)
    xs = np.linspace(-L / 2, L / 2, N)
    U, w, dx = initial_collision(xs, rng)
    dt = 0.06 * dx
    B_series = [s.baryon_number(U, dx)]
    E_series = [s.chiral_energy(U, dx, E_SK)[2] + s.kinetic_energy(w, dx)]
    # evolve long enough to collide (~150 steps); sample B in blocks
    for blk in range(10):
        U, w, hist = s.chiral_evolve(U, w, dx, dt, 15, E_SK, clamp_boundary=True,
                                     record_B=True)
        B_series.append(hist[-1][1])
        E_series.append(hist[-1][0])
    late = B_series[-3:]
    return {"seed": seed, "B_series": B_series, "B_late_mean": float(np.mean(late)),
            "B_late_absmax": float(np.max(np.abs(late))),
            "B_traj_absmax": float(np.max(np.abs(B_series))),
            "E_first": E_series[0], "E_last": E_series[-1]}


def main():
    results = [run_seed(k) for k in range(N_SEEDS)]
    late_absmax = [r["B_late_absmax"] for r in results]
    traj_absmax = [r["B_traj_absmax"] for r in results]
    n_skyrmion = sum(1 for v in late_absmax if v > 0.5)   # |B|>0.5 ~ a winding object
    n_transient = sum(1 for v in traj_absmax if v > 0.5)  # transient winding ever seen
    frac = n_skyrmion / N_SEEDS
    max_over_seeds = float(np.max(late_absmax))
    max_traj = float(np.max(traj_absmax))
    mean_absmax = float(np.mean(late_absmax))

    created = frac >= 0.5
    verdict = "SIM" if created else "NAO"

    payload = {"n_seeds": N_SEEDS, "L": L, "N": N, "e_sk": E_SK, "amp": AMP,
               "results": results,
               "late_absmax_per_seed": late_absmax,
               "traj_absmax_per_seed": traj_absmax,
               "fraction_late_|B|>0.5": frac,
               "n_seeds_transient_|B|>0.5": n_transient,
               "max_late_|B|_over_seeds": max_over_seeds,
               "max_trajectory_|B|_over_seeds": max_traj,
               "mean_late_absmax": mean_absmax,
               "skyrmion_created": bool(created),
               "verdict": verdict}
    s.save_json("SU6_collision", payload)

    print("=" * 70)
    print("SU6 -- CREATION BY COLLISION (20 seeds)")
    print("=" * 70)
    print("seed  B_late_mean  B_late|max|  B_traj|max|  E_first -> E_last")
    for r in results:
        print(f"{r['seed']:>4} {r['B_late_mean']:+11.3f} {r['B_late_absmax']:11.3f} "
              f"{r['B_traj_absmax']:11.3f}   {r['E_first']:7.1f} -> {r['E_last']:7.1f}")
    print("-" * 70)
    print(f"fraction late |B|>0.5: {frac:.2f}   max late |B|: {max_over_seeds:.3f}")
    print(f"seeds with transient |B|>0.5: {n_transient}/{N_SEEDS}   "
          f"max trajectory |B|: {max_traj:.3f}")
    print(f"VERDICT: Skyrmion created by collision: {verdict}")
    return payload


if __name__ == "__main__":
    main()
