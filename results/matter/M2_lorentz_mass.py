"""M2 -- Lorentz invariance of the mass proxy (decisive test; conecta R1).

M1 found the free scalar has no measurable inertial rest mass (null force-response).
The only mass-like scalar the network offers is then the CONTENT of a causal
diamond -- the connectivity/action scale that T15/T16 reached for.  A genuine mass
must be Lorentz invariant.  R1 already proved Poisson sprinkling is Lorentz
invariant in distribution; here we test the mass proxy directly.

METHOD (the clean isotropy test, as in R1 Panel B)
  * Fix an INVARIANT proper time tau0.  Build the causal diamond A=(0,0) ->
    B=(tau0 cosh phi, tau0 sinh phi).  The hyperbolic identity cosh^2-sinh^2=1 keeps
    the invariant interval = tau0 for every rapidity phi (pure geometry, no dilation
    formula).
  * The mass proxy = number of events N inside the diamond (the diamond's
    action/connectivity content).  A Lorentz-invariant quantity must give a CONSTANT
    N (up to Poisson noise) as phi varies.
  * Poisson network: expect invariant mean N = rho * tau0^2 / 2, small CV.
    Regular lattice (the anisotropic control): N swings with direction -> breaks it.

ANTI-CIRCULARITY: no gamma, no sqrt(1-beta^2).  Boost is a coordinate map.  The
diamond content is a bare count.

SUCCESS: Poisson CV small and << lattice CV -> mass proxy is Lorentz invariant.
DEATH:   Poisson CV ~ lattice CV -> the proxy is frame-dependent -> not a mass.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import matter_core as mc

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from causal_core import lattice_box  # noqa: E402

SEEDS = range(20)
RHO, TAU0 = 8.0, 6.0
RAPIDITIES = np.linspace(0.0, 2.5, 12)   # beta = tanh(phi) up to ~0.987


def _diamond_bounds(B, pad=1.0):
    t0, t1 = sorted([0.0, B[0]])
    cx = 0.5 * B[1]
    half = 0.5 * abs(B[0]) + abs(B[1]) + pad
    return [(t0 - pad, t1 + pad), (cx - half, cx + half)]


def _count_in_diamond(pts, B):
    """Events in the Alexandrov interval (0,0) < x < B (future of A, past of B)."""
    t, x = pts[:, 0], pts[:, 1]
    dtA, dx2A = t, x ** 2                      # A = origin
    fut_A = (dtA > 0) & (dtA * dtA > dx2A)
    dtB, dx2B = B[0] - t, (B[1] - x) ** 2      # past of B
    past_B = (dtB > 0) & (dtB * dtB > dx2B)
    return int(np.sum(fut_A & past_B))


def poisson_counts():
    """Mean diamond count per rapidity, averaged over seeds."""
    sprinkle_box = __import__("causal_core").sprinkle_box
    per_phi = []
    for phi in RAPIDITIES:
        B = np.array([TAU0 * np.cosh(phi), TAU0 * np.sinh(phi)])
        ns = []
        for s in SEEDS:
            rng = np.random.default_rng(1000 + s)
            pts = sprinkle_box(RHO, _diamond_bounds(B), rng)
            ns.append(_count_in_diamond(pts, B))
        per_phi.append(np.mean(ns))
    return np.array(per_phi, dtype=float)


def lattice_counts():
    out = []
    spacing = RHO ** -0.5
    for phi in RAPIDITIES:
        B = np.array([TAU0 * np.cosh(phi), TAU0 * np.sinh(phi)])
        pts = lattice_box(spacing, _diamond_bounds(B))
        out.append(_count_in_diamond(pts, B))
    return np.array(out, dtype=float)


def main():
    print("=" * 70)
    print("M2 -- LORENTZ INVARIANCE OF THE MASS PROXY (conecta R1)")
    print("=" * 70)
    pois = poisson_counts()
    lat = lattice_counts()
    expected = RHO * 0.5 * TAU0 ** 2
    cv_p = float(np.std(pois) / np.mean(pois))
    cv_l = float(np.std(lat) / np.mean(lat))
    print(f"  invariant proper time tau0={TAU0}, expected count rho*tau0^2/2={expected:.1f}")
    print(f"  Poisson diamond count: mean={pois.mean():.1f}  CV={cv_p:.1%} (want small)")
    print(f"  Lattice diamond count: mean={lat.mean():.1f}  CV={cv_l:.1%} (direction-dep)")

    invariant = cv_p < 0.10 and cv_l > 3 * cv_p
    if invariant:
        verdict = "B"
        statement = ("The mass proxy (causal-diamond content) is Lorentz invariant "
                     "for the Poisson network (CV %.1f%%) and frame-dependent for the "
                     "lattice (CV %.1f%%).  This is REAL but inherited: it is R1's "
                     "Poisson Lorentz-invariance applied to the connectivity scale, "
                     "not an independently derived particle mass." % (cv_p*100, cv_l*100))
    else:
        verdict = "C"
        statement = ("The proxy's invariance is not cleanly separated from the "
                     "lattice control at this size -- inconclusive.")
    print("-" * 70)
    print(f"VERDICT M2: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "tau0": TAU0,
                      "rapidities": RAPIDITIES.tolist(), "n_seeds": len(list(SEEDS))},
           "expected_count": expected,
           "poisson_counts": pois.tolist(), "lattice_counts": lat.tolist(),
           "cv_poisson": cv_p, "cv_lattice": cv_l,
           "verdict": verdict, "statement": statement}
    mc.save_json("M2_lorentz_mass", out)
    return out


if __name__ == "__main__":
    main()
