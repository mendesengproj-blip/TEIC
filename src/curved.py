"""curved.py -- Sprinkling on fixed curved backgrounds (generator module).

Anti-circularity design (see PROMPT.md sec.3):

  * The CAUSAL RELATION is always the bare 45-degree Minkowski light cone.  We use
    conformally-flat coordinates, in which light cones of any 2D metric are exactly
    those of flat space, so causal_core.precedes / alexandrov_interval apply unchanged.
  * The METRIC enters ONLY through the proper-volume element used to set the local
    sprinkling density.  That is the fixed background geometry we test counting
    against -- it is an input, not the answer.
  * This module NEVER takes the square root of g_tt.  The dilation factor sqrt(g_tt)
    (special- and general-relativistic) lives exclusively in validation.py.  Proper
    time is recovered here only by counting, via volume.tau_from_count.

Backgrounds provided:
  * 2D constant curvature (de Sitter R>0 / anti-de Sitter R<0)  -- Tasks A & B.
  * 2D radial Schwarzschild slice in tortoise coordinates       -- Task C.
"""

from __future__ import annotations

import numpy as np
from scipy.optimize import brentq


# --------------------------------------------------------------------------- #
# 2D constant curvature (conformally flat: ds^2 = Omega^2 (-dt^2 + dx^2))
# --------------------------------------------------------------------------- #
def omega2_const_curv(t, x, R):
    """Proper-volume element Omega^2 of the 2D constant-curvature metric.

    Omega = 1 / (1 + (R/8)(x^2 - t^2))  ->  Ricci scalar = R (verified in e4).
    This is the metric, not a dilation formula: no square root is taken.
    """
    denom = 1.0 + (R / 8.0) * (np.asarray(x) ** 2 - np.asarray(t) ** 2)
    return 1.0 / denom ** 2


def sprinkle_const_curv(rho, R, t_bounds, x_bounds, rng, omega2_max=None):
    """Inhomogeneous Poisson sprinkle at proper density rho on 2D constant curvature.

    Implemented by thinning: oversprinkle a homogeneous Poisson process at the
    peak coordinate density rho * omega2_max, then keep each candidate with
    probability Omega^2 / omega2_max.  The kept set is an exact Poisson process
    with intensity rho * Omega^2 (proper density rho).
    """
    t_bounds = np.asarray(t_bounds, float)
    x_bounds = np.asarray(x_bounds, float)
    if omega2_max is None:
        # sample the box on a grid to bound Omega^2 from above (with margin)
        tt = np.linspace(*t_bounds, 64)
        xx = np.linspace(*x_bounds, 64)
        TT, XX = np.meshgrid(tt, xx)
        vals = omega2_const_curv(TT, XX, R)
        omega2_max = float(np.nanmax(vals)) * 1.05
        if not np.isfinite(omega2_max) or omega2_max <= 0:
            raise ValueError("Omega^2 diverges in the requested box (coordinate "
                             "singularity); shrink the box for this R.")
    area = (t_bounds[1] - t_bounds[0]) * (x_bounds[1] - x_bounds[0])
    n = rng.poisson(rho * omega2_max * area)
    cand = np.column_stack([
        rng.uniform(t_bounds[0], t_bounds[1], n),
        rng.uniform(x_bounds[0], x_bounds[1], n),
    ])
    keep = rng.uniform(0, 1, n) < omega2_const_curv(cand[:, 0], cand[:, 1], R) / omega2_max
    return cand[keep]


def geodesic_tau_const_curv(T, R):
    """Exact proper time of the timelike geodesic between tips (-T/2,0) and (T/2,0).

    The geodesic stays on x=0 by reflection symmetry, so
        tau = \\int_{-T/2}^{T/2} Omega(t,0) dt = \\int dt / (1 - (R/8) t^2).
    Closed form: (8/R)^{1/2} artanh( sqrt(R/8) * T/2 ) * 2   for R>0, and the
    analytic continuation (arctan) for R<0.  Computed here by stable elementary
    functions.  NOTE: this is reference GEOMETRY of the background, used as the
    independent variable tau; it is not applied to any counting estimator.
    """
    a = R / 8.0
    half = T / 2.0
    if abs(a) < 1e-14:
        return float(T)
    if a > 0:
        k = np.sqrt(a)
        return float(2.0 * np.arctanh(k * half) / k)
    k = np.sqrt(-a)
    return float(2.0 * np.arctan(k * half) / k)


# --------------------------------------------------------------------------- #
# 2D Schwarzschild radial slice in tortoise coordinates (Task C)
# --------------------------------------------------------------------------- #
def rstar_of_r(r, M):
    """Tortoise coordinate r* = r + 2M ln(r/(2M) - 1), for r > 2M."""
    return r + 2.0 * M * np.log(r / (2.0 * M) - 1.0)


def r_of_rstar(rstar, M):
    """Invert the tortoise coordinate (scalar), r > 2M, by bracketed root find."""
    f = lambda r: rstar_of_r(r, M) - rstar
    lo = 2.0 * M * (1.0 + 1e-9)
    hi = 4.0 * M  # start strictly above the horizon to avoid log(0)
    while f(hi) < 0:
        hi *= 2.0
    return brentq(f, lo, hi, xtol=1e-12, rtol=1e-12)


def _r_interp(rstar_bounds, M, n=4096):
    """Fast vectorised inverse r(r*) on a range, via a monotone forward grid.

    r*(r) is monotone increasing for r>2M, so we tabulate r -> r* (cheap, closed
    form) on a fine r grid covering the requested r* range and interpolate.
    """
    lo, hi = float(rstar_bounds[0]), float(rstar_bounds[1])
    r_lo = r_of_rstar(lo, M)
    r_hi = r_of_rstar(hi, M)
    r_grid = np.linspace(r_lo * (1 - 1e-9), r_hi * (1 + 1e-9), n)
    rs_grid = rstar_of_r(r_grid, M)
    return lambda rstar: np.interp(rstar, rs_grid, r_grid)


def omega2_schwarzschild(rstar, M, r_of=None):
    """Proper-volume element Omega^2 = g_tt = (1 - 2M/r) on the radial slice.

    In tortoise coordinates ds^2 = (1 - 2M/r)(-dt^2 + dr*^2), conformally flat, so
    light cones are 45 degrees.  Returns (1 - 2M/r); NO square root (that would be
    the redshift, which lives only in validation.py).  ``r_of`` is an optional fast
    inverse-tortoise interpolator (see _r_interp); otherwise a per-point root find
    is used.
    """
    rstar = np.atleast_1d(np.asarray(rstar, float))
    if r_of is not None:
        r = r_of(rstar)
    else:
        r = np.array([r_of_rstar(rs, M) for rs in rstar])
    return 1.0 - 2.0 * M / r


def sprinkle_schwarzschild(rho, M, t_bounds, rstar_bounds, rng):
    """Inhomogeneous Poisson sprinkle at proper density rho on the radial slice."""
    t_bounds = np.asarray(t_bounds, float)
    rstar_bounds = np.asarray(rstar_bounds, float)
    r_of = _r_interp(rstar_bounds, M)
    rs_grid = np.linspace(*rstar_bounds, 256)
    omega2_max = float(omega2_schwarzschild(rs_grid, M, r_of).max()) * 1.02
    area = (t_bounds[1] - t_bounds[0]) * (rstar_bounds[1] - rstar_bounds[0])
    n = rng.poisson(rho * omega2_max * area)
    cand_t = rng.uniform(t_bounds[0], t_bounds[1], n)
    cand_rs = rng.uniform(rstar_bounds[0], rstar_bounds[1], n)
    w = omega2_schwarzschild(cand_rs, M, r_of) / omega2_max
    keep = rng.uniform(0, 1, n) < w
    return np.column_stack([cand_t[keep], cand_rs[keep]])
