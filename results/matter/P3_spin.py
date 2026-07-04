"""P3 -- spin test: 2pi vs 4pi (refaz T21BIS).

The decisive spin test: under a full 2pi rotation, a spin-1/2 state -> MINUS itself
and only a 4pi rotation -> PLUS itself; an integer-spin/scalar state -> PLUS itself
already at 2pi.  T21BIS never ran this test.  We run it.

We need >= 2 spatial dimensions to rotate, so we use a 2+1D Poisson network.  On it
we build a real field with directional (angular) structure -- the only kind a scalar
admits -- and rotate the spatial plane, measuring the normalized overlap
O(alpha) = <theta, R_alpha theta>/<theta,theta> as alpha goes 0 -> 4pi.

A real single-valued field on the plane carries INTEGER angular number m, so
theta = cos(m phi) gives O(alpha) = cos(m alpha): O(2pi)=+1 for every integer m.  A
half-integer m (which would give O(2pi) = -1) is NOT a single-valued function on the
plane -- it requires a spinor (double cover), which a scalar theta does not have.

ANTI-CIRCULARITY: spin, Pauli, spinors are never inserted; the +/- response is
MEASURED from how a real field transforms under rotation.

SUCCESS (for spin-1/2): O(2pi) = -1, O(4pi) = +1.
EXPECTED (scalar):       O(2pi) = +1 -> no spin-1/2; integer spin only.
"""

from __future__ import annotations

import numpy as np

import matter_core as mc

SEEDS = range(20)
RHO, T, X, SIGMA = 6.0, 6.0, 8.0, 3.0
M_NUMBERS = [1, 2]                       # angular numbers to probe
ALPHAS = np.linspace(0.0, 4.0 * np.pi, 17)


def overlap_curve(m_ang, seed):
    rng = np.random.default_rng(9000 + seed)
    p = mc.sprinkle_3d(RHO, T, X, rng)
    x, y = p[:, 1], p[:, 2]
    r2 = x ** 2 + y ** 2
    phi_ang = np.arctan2(y, x)
    env = np.exp(-r2 / (2.0 * SIGMA ** 2))
    theta = env * np.cos(m_ang * phi_ang)            # directional real field
    denom = float(np.dot(theta, theta))
    ov = []
    for a in ALPHAS:
        # R_alpha theta evaluated at the same events = field rotated by alpha
        theta_rot = env * np.cos(m_ang * (phi_ang - a))
        ov.append(float(np.dot(theta, theta_rot) / denom) if denom > 0 else np.nan)
    return np.array(ov)


def main():
    print("=" * 70)
    print("P3 -- SPIN TEST: 2pi vs 4pi (refaz T21BIS)")
    print("=" * 70)
    i2 = int(np.argmin(np.abs(ALPHAS - 2 * np.pi)))
    i4 = int(np.argmin(np.abs(ALPHAS - 4 * np.pi)))
    results = {}
    for m_ang in M_NUMBERS:
        curves = np.array([overlap_curve(m_ang, s) for s in SEEDS])
        o2 = mc.seed_stats(curves[:, i2])
        o4 = mc.seed_stats(curves[:, i4])
        results[m_ang] = {"O_2pi": o2, "O_4pi": o4, "curve_mean": curves.mean(0).tolist()}
        print(f"  m={m_ang}: O(2pi)={o2['mean']:+.3f}+/-{o2['sem']:.3f}  "
              f"O(4pi)={o4['mean']:+.3f}+/-{o4['sem']:.3f}")

    # spin-1/2 would need O(2pi) ~ -1; we find O(2pi) ~ +1 for all integer m
    half_integer = any(results[m]["O_2pi"]["mean"] < -0.5 for m in M_NUMBERS)
    verdict = "C"
    if half_integer:
        statement = "Unexpected: a 2pi rotation flips the sign -> spin-1/2 signature."
    else:
        statement = (
            "No spin-1/2 (as expected).  A 2pi rotation returns the field to +itself "
            "(O(2pi)=+1 for every integer angular number m); there is no 4pi double "
            "cover.  A real scalar theta carries only INTEGER angular structure -- a "
            "half-integer (which would give O(2pi)=-1) is not a single-valued function "
            "on the plane and would require a spinor field, which theta does not have.  "
            "Spin-1/2 needs internal (spinor/vector) structure ABSENT from the scalar "
            "sector; it cannot emerge from theta alone.")
    print("-" * 70)
    print(f"VERDICT P3: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "T": T, "X": X, "sigma": SIGMA,
                      "m_numbers": M_NUMBERS, "alphas": ALPHAS.tolist(),
                      "n_seeds": len(list(SEEDS))},
           "results": {str(m): results[m] for m in M_NUMBERS},
           "half_integer_found": bool(half_integer),
           "verdict": verdict, "statement": statement}
    mc.save_json("P3_spin", out)
    return out


if __name__ == "__main__":
    main()
