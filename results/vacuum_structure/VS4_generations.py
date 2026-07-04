"""VS4 -- does the B=1 sector have MULTIPLE stable configurations with
different energies (a 'three generations' degeneracy)?

Charter: VACUUM_STRUCTURE.md (VS4).  The three SM generations have identical
quantum numbers and different masses.  In topological language: are there
several distinct local minima of the energy in the SAME topological sector
B=1?

Probe (the rigorous, cheap one first):

  (A) RADIAL BASIN SCAN.  Within the hedgehog ansatz U = exp(i F(r) rhat.s),
      B=1 is enforced by the boundary conditions F(0)=pi, F(inf)=0 ONLY --
      the interior profile is free, including non-monotonic excursions
      F -> 3pi -> pi etc. (same winding, different path).  Relax 10 widely
      different initial profiles (widths x{0.3..3}, linear ramp, plateau
      core, +2pi excursions at three radii, oscillating) with the analytic-
      gradient L-BFGS minimiser (su2_core.radial_relax, the SU3 machinery).
      If the B=1 sector has excited stationary profiles, some initial
      conditions relax into them; if all 10 land on ONE mass, the radial
      sector has a single basin.

  (B) 3D LATTICE SPOT-CHECK (beyond the hedgehog ansatz, limited).  Embed
      (i) the ground profile and (ii) the most distinct relaxed profile of
      (A) -- or, if (A) is single-basin, the strongest excursion initial
      condition -- on the 33^3 lattice and cool with the full 3D chiral
      force (sigma analytic + Skyrme stencil).  Verify both keep B=1 and
      flow toward the same energy (or not).

Honest scope: (A) is exhaustive only WITHIN the hedgehog ansatz; (B) probes
non-radial escape weakly (cooling, no long dynamics).  Non-hedgehog B=1
saddle configurations (rational-map deformations) are beyond this probe and
are recorded as the residual if the kill fires.

Kill criterion (pre-registered): only one stable configuration with B=1 --
every initial profile relaxes to the same mass (within the resolution
tolerance); no generational degeneracy in this sector.

Anti-circularity: no SM masses or mixing inserted; 'generation' is a name.
Deterministic initial data; e_sk = 4 (the SU3 reference), radial grid
rmax=14, n=360 (the SU3 grid).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s    # noqa: E402

OUTDIR = Path(__file__).resolve().parent
E_SK = 4.0
PI = np.pi


def initial_profiles(r):
    """10 widely different B=1 initial profiles (F(0)=pi, F(inf)=0)."""
    rmax = r[-1]
    profs = {}
    for w_frac in (0.075, 0.25, 0.75):                       # widths x ~0.3..3
        profs[f"exp_w{w_frac}"] = PI * np.exp(-r / (w_frac * rmax))
    profs["linear_ramp"] = PI * np.clip(1.0 - r / (0.6 * rmax), 0.0, 1.0)
    plateau = np.where(r < 0.25 * rmax, PI,
                       PI * np.exp(-(r - 0.25 * rmax) / (0.1 * rmax)))
    profs["plateau_core"] = plateau
    base = PI * np.exp(-r / (0.25 * rmax))
    for rc_frac in (0.15, 0.35, 0.6):                        # +2pi excursions
        bump = 2.0 * PI * np.exp(-((r - rc_frac * rmax) ** 2)
                                 / (2 * (0.06 * rmax) ** 2))
        profs[f"excursion_r{rc_frac}"] = base + bump
    profs["oscillating"] = base * (1.0 + 0.8 * np.sin(6.0 * PI * r / rmax)
                                   * np.exp(-r / (0.5 * rmax)))
    profs["wide_then_kink"] = PI / (1.0 + (r / (0.2 * rmax)) ** 4)
    return profs


def radial_winding(F):
    """(F(0)-F(inf))/pi -- the hedgehog B within the ansatz."""
    return float((F[0] - F[-1]) / PI)


def relax_to_virial(r, dr, F0, max_rounds=8, tol=0.02):
    """L-BFGS relax + Derrick-rescale loop.  A TRUE stationary point of the
    Skyrme functional must satisfy the virial E2 = E4 (Derrick); an optimiser
    stall does not.  After each relax, rescale the profile by the Derrick
    optimum lambda* = sqrt(E4/E2) (which strictly lowers the energy unless
    E2=E4) and re-relax, until |E2/E4 - 1| < tol or rounds exhausted.
    Returns (F, E2, E4, converged_flag, n_rounds)."""
    F = F0.copy()
    for k in range(max_rounds):
        F, E2, E4 = s.radial_relax(r, dr, E_SK, F0=F, maxiter=8000)
        ratio = E2 / E4
        if abs(ratio - 1.0) < tol:
            return F, E2, E4, True, k + 1
        lam = np.sqrt(E4 / E2)                     # Derrick rescale
        F = np.interp(r / lam, r, F, left=PI, right=0.0)
        F[0] = PI; F[-1] = 0.0
    return F, E2, E4, False, max_rounds


def part_A():
    r, dr = s.radial_grid(rmax=14.0, n=360)
    profs = initial_profiles(r)
    rows = []
    relaxed = {}
    print("(A) radial basin scan (e_sk=%.1f, %d initial profiles, "
          "virial-enforced):" % (E_SK, len(profs)))
    for name, F0 in profs.items():
        F0 = F0.copy(); F0[0] = PI; F0[-1] = 0.0
        E2i, E4i = s.radial_energy(F0, r, dr, E_SK)
        F, E2, E4, conv, k = relax_to_virial(r, dr, F0)
        M = E2 + E4
        rows.append({"profile": name, "E_init": E2i + E4i, "mass": M,
                     "E2": E2, "E4": E4, "virial": E2 / E4,
                     "stationary": conv, "rounds": k,
                     "B_radial": radial_winding(F),
                     "max_excursion": float(F.max())})
        relaxed[name] = F
        print(f"  {name:16s} E_init={E2i+E4i:9.1f} -> M={M:8.3f}  "
              f"E2/E4={E2/E4:6.3f}  stationary={conv}  rounds={k}  "
              f"B={radial_winding(F):+.2f}")
    good = [d for d in rows if d["stationary"]]
    masses = np.array([d["mass"] for d in good])
    rel_spread = (float(masses.max() - masses.min()) / float(masses.min())
                  if len(masses) else float("nan"))
    print(f"  stationary endpoints: {len(good)}/{len(rows)}  "
          f"mass range [{masses.min():.3f}, {masses.max():.3f}]  "
          f"spread={rel_spread:.3%}")
    msort = np.sort(masses)
    gaps = np.diff(msort)
    n_clusters = 1 + int(np.sum(gaps > 0.05 * msort[:-1]))   # >5% jumps
    print(f"  distinct stationary masses (>5% gaps): {n_clusters}")
    return r, dr, rows, relaxed, n_clusters, rel_spread


def part_B(r, relaxed, rows):
    """3D cooling spot-check beyond the strict ansatz: the STATIONARY ground
    profile vs a WIDE +2pi excursion (all features >= 3 lattice points so B
    is resolved; the VS4 first run showed narrow cores alias to B~0).

    Cooling rate 0.002: stability-tested (0.05 and 0.01 DIVERGE at dx~0.5,
    e_sk=4 -- the first VS4 run's E explosion was that instability, not
    physics; documented in VS4_generations.md)."""
    N, L = 25, 12.0
    xs = np.linspace(-L / 2, L / 2, N)
    dx = float(xs[1] - xs[0])
    good = [d for d in rows if d["stationary"]]
    ground_name = min(good, key=lambda d: d["mass"])["profile"]
    rmax = r[-1]
    base = PI * np.exp(-r / (0.25 * rmax))
    wide_exc = base + 2.0 * PI * np.exp(-((r - 0.35 * rmax) ** 2)
                                        / (2 * (0.15 * rmax) ** 2))
    cases = {
        "ground": s.profile_from_radial(relaxed[ground_name], r),
        "excursion_wide": s.profile_from_radial(wide_exc, r),
    }
    out = {}
    n_iter, rate = 400, 0.002
    print("\n(B) 3D lattice cooling spot-check (N=%d, %d iters, rate=%g):"
          % (N, n_iter, rate))
    for name, prof in cases.items():
        U = s.hedgehog_field(xs, xs, xs, profile=prof)
        B0 = s.baryon_number(U, dx)
        E2i, E4i, Ei = s.chiral_energy(U, dx, E_SK)
        t0 = time.time()
        U, hist = s.chiral_cool(U, dx, E_SK, n_iter=n_iter, rate=rate)
        Bf = s.baryon_number(U, dx)
        E2, E4, Et = s.chiral_energy(U, dx, E_SK)
        monotone = bool(np.all(np.diff(hist) < 1e-6 * max(abs(hist[0]), 1)))
        out[name] = {"B_init": float(B0), "B_final": float(Bf),
                     "E_init": float(Ei), "E_final": float(Et),
                     "E_monotone_down": monotone, "E_track": hist[::40]}
        print(f"  {name:14s} B: {B0:+.3f} -> {Bf:+.3f}   "
              f"E: {Ei:9.2f} -> {Et:9.2f}  monotone_down={monotone}  "
              f"({time.time()-t0:.0f}s)")
    return out


def main():
    r, dr, rows, relaxed, n_clusters, rel_spread = part_A()
    b3d = part_B(r, relaxed, rows)

    payload = {"params": {"e_sk": E_SK, "radial_grid": [14.0, 360]},
               "radial_scan": rows,
               "n_clusters": n_clusters, "rel_mass_spread": rel_spread,
               "lattice_3d": b3d}
    (OUTDIR / "VS4_generations.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print("\nsaved VS4_generations.json")


if __name__ == "__main__":
    main()
