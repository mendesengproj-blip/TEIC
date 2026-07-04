"""VS4b -- deterministic energy scan along a configuration-space path
(replaces the resolution-limited 3D cooling spot-check of VS4 part B).

The VS4 cooling check at dx=0.5 was unusable: even the GROUND hedgehog
unwinds (B 0.91 -> 0.00) -- the known coarse-lattice B leak (SU3 used
dx=0.33; SU9 records ~4% B error at N=51).  Instead of flow, scan the energy
along the per-site GEODESIC path on S^3 between two B=1 configurations:

    U_s(x) = U_g(x) * exp(s * log(U_g(x)^{-1} U_e(x))),   s in [0, 1],

from the relaxed ground hedgehog (s=0) to the wide +2pi excursion hedgehog
(s=1), at dx = 1/3 (the SU3 resolution, B well-resolved).  If E(s) rises
MONOTONICALLY from ground to excursion (no interior minimum), there is no
second basin along this natural path -- the excursion is a hillside of the
single ground basin, confirming part A beyond the strict radial ansatz
(weakly: one path, not all of configuration space; stated honestly).

Also records B(s): the path stays in the B=1 sector throughout (geodesic
interpolation between same-sector configs cannot jump winding unless it
passes a singular point; B(s) is measured, not assumed).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s    # noqa: E402

OUTDIR = Path(__file__).resolve().parent
E_SK = 4.0
PI = np.pi
N, L = 37, 12.0          # dx = 1/3 -- SU3's resolution class


def q_exp_vec(v):
    """exp of a pure-imaginary quaternion 3-vector field v -> unit quaternion."""
    ang = np.linalg.norm(v, axis=-1)
    out = np.zeros(v.shape[:-1] + (4,))
    out[..., 0] = np.cos(ang)
    safe = np.where(ang > 1e-300, ang, 1.0)
    out[..., 1:] = v * (np.sin(ang) / safe)[..., None]
    out[ang == 0, 1:] = 0.0
    return out


def main():
    xs = np.linspace(-L / 2, L / 2, N)
    dx = float(xs[1] - xs[0])
    r, dr = s.radial_grid(rmax=14.0, n=360)
    rmax = r[-1]

    # ground: the relaxed stationary profile (re-derived here, deterministic)
    F0 = PI * np.exp(-r / (0.25 * rmax)); F0[0] = PI; F0[-1] = 0.0
    Fg, E2g, E4g = s.radial_relax(r, dr, E_SK, F0=F0, maxiter=8000)
    U_g = s.hedgehog_field(xs, xs, xs, profile=s.profile_from_radial(Fg, r))

    # excursion: +2pi bump on the base profile.  Geometry constraint (learned
    # from the first run, B=-1.36): the bump must DECAY WELL INSIDE the box
    # half-width L/2=6, or the boundary truncates the extra winding and B is
    # garbage.  Centre 0.15*rmax=2.1, sigma 0.08*rmax=1.1 (>=3 lattice points
    # per sigma at dx=1/3; F(L/2) ~ base only).
    base = PI * np.exp(-r / (0.25 * rmax))
    Fe = base + 2.0 * PI * np.exp(-((r - 0.15 * rmax) ** 2)
                                  / (2 * (0.08 * rmax) ** 2))
    Fe[0] = PI; Fe[-1] = 0.0
    U_e = s.hedgehog_field(xs, xs, xs, profile=s.profile_from_radial(Fe, r))

    print(f"N={N} dx={dx:.3f}  B(ground)={s.baryon_number(U_g, dx):+.3f}  "
          f"B(excursion)={s.baryon_number(U_e, dx):+.3f}")

    # per-site geodesic tangent: v = log(U_g^{-1} U_e)
    D = s.q_mul(s.q_conj(U_g), U_e)
    v = s.q_log_vec(D)

    rows = []
    for sfrac in np.linspace(0.0, 1.0, 21):
        U = s.q_normalize(s.q_mul(U_g, q_exp_vec(sfrac * v)))
        E2, E4, Et = s.chiral_energy(U, dx, E_SK)
        B = s.baryon_number(U, dx)
        rows.append({"s": float(sfrac), "E": float(Et), "B": float(B)})
        print(f"  s={sfrac:4.2f}  E={Et:10.2f}  B={B:+.3f}")

    E = np.array([d["E"] for d in rows])
    interior_min = bool(np.any((E[1:-1] < E[:-2]) & (E[1:-1] < E[2:])
                               & (E[1:-1] < E[0] - 1e-6)))
    monotone_up = bool(np.all(np.diff(E) > -1e-6 * max(E.max(), 1)))
    print(f"\nmonotone uphill ground->excursion: {monotone_up}  "
          f"interior minimum below ground: {interior_min}")

    payload = {"params": {"N": N, "L": L, "dx": dx, "e_sk": E_SK},
               "ground_mass_radial": E2g + E4g,
               "path": rows, "monotone_up": monotone_up,
               "interior_minimum": interior_min}
    (OUTDIR / "VS4b_path_scan.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print("saved VS4b_path_scan.json")


if __name__ == "__main__":
    main()
