"""causal_core.py -- Causal network primitives for the TEIC pipeline.

This module is part of the DATA GENERATOR. It must contain NO special- or
general-relativistic formula (no Lorentz factor, no sqrt(1-beta^2), no metric
dilation factor). It only knows:

    * how to sprinkle events (Poisson process or regular lattice),
    * the bare causal relation of flat Minkowski space (light cones),
    * how to extract the Alexandrov interval (causal diamond) between two events.

Everything relativistic lives in validation.py and is only used for COMPARISON.

Conventions
-----------
An event is a row ``(t, x1, ..., xs)`` with one time coordinate and ``s`` spatial
coordinates.  Signature ``(-,+,...,+)``.  Event ``p`` causally precedes ``q`` iff

    dt = q[0]-p[0] > 0   and   dt^2 - |dx|^2 > 0 .
"""

from __future__ import annotations

import numpy as np


# --------------------------------------------------------------------------- #
# Sprinkling
# --------------------------------------------------------------------------- #
def sprinkle_box(rho, bounds, rng):
    """Poisson sprinkle events uniformly in an axis-aligned box.

    Parameters
    ----------
    rho : float
        Sprinkling density (expected events per unit coordinate volume).
    bounds : sequence of (lo, hi)
        One (lo, hi) pair per coordinate, time first.
    rng : numpy.random.Generator

    Returns
    -------
    (n, D) float array of event coordinates, D = len(bounds).
    """
    bounds = np.asarray(bounds, dtype=float)
    vol = np.prod(bounds[:, 1] - bounds[:, 0])
    n = rng.poisson(rho * vol)
    pts = rng.uniform(bounds[:, 0], bounds[:, 1], size=(n, bounds.shape[0]))
    return pts


def lattice_box(spacing, bounds):
    """Regular hyper-cubic lattice of events in a box (the anisotropic control).

    The lattice density matches rho = spacing**(-D) so it can be compared with a
    Poisson sprinkle of the same density.
    """
    bounds = np.asarray(bounds, dtype=float)
    axes = [np.arange(lo, hi, spacing) for lo, hi in bounds]
    grids = np.meshgrid(*axes, indexing="ij")
    return np.stack([g.ravel() for g in grids], axis=1)


# --------------------------------------------------------------------------- #
# Causal relation (bare Minkowski light cones -- no dilation formula here)
# --------------------------------------------------------------------------- #
def interval2(p, q):
    """Squared invariant interval dt^2 - |dx|^2 for p->q (broadcasts over arrays)."""
    d = np.asarray(q) - np.asarray(p)
    return d[..., 0] ** 2 - np.sum(d[..., 1:] ** 2, axis=-1)


def precedes(p, q):
    """True iff event p causally precedes event q in flat space."""
    dt = q[0] - p[0]
    return bool(dt > 0 and dt * dt > np.sum((np.asarray(q[1:]) - np.asarray(p[1:])) ** 2))


def causal_to(pts, base, future=True):
    """Boolean mask: which ``pts`` are in the future (or past) light cone of ``base``.

    future=True  -> base precedes pts
    future=False -> pts precede base
    """
    pts = np.asarray(pts, dtype=float)
    base = np.asarray(base, dtype=float)
    if future:
        dt = pts[:, 0] - base[0]
        dx2 = np.sum((pts[:, 1:] - base[1:]) ** 2, axis=1)
    else:
        dt = base[0] - pts[:, 0]
        dx2 = np.sum((base[1:] - pts[1:]) ** 2 if pts.ndim == 1
                     else (base[1:] - pts[:, 1:]) ** 2, axis=-1)
    return (dt > 0) & (dt * dt > dx2)


def alexandrov_interval(pts, A, B):
    """Indices of events in the Alexandrov interval (causal diamond) A < x < B.

    I.e. events in the future of A and in the past of B.
    """
    pts = np.asarray(pts, dtype=float)
    in_future_A = causal_to(pts, A, future=True)
    in_past_B = causal_to(pts, B, future=False)
    return np.nonzero(in_future_A & in_past_B)[0]


def causal_matrix(pts):
    """Strict causal order relation as a boolean matrix C[i, j] = (i precedes j).

    O(n^2) -- intended for small sets (chain extraction, unit tests).
    """
    pts = np.asarray(pts, dtype=float)
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    return (dt > 0) & (dt * dt > dx2)
