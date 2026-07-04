"""chain.py -- Longest causal chain (the "chain" formulation of proper time).

The length of the longest chain between two events is the height of the causal
poset restricted to their Alexandrov interval.  In the continuum it tracks the
longest timelike geodesic, hence proper time.

This module is part of the DATA GENERATOR: no relativistic formula here.

Two implementations:
  * longest_chain_2d  -- O(n log n) via reduction to a longest increasing
    subsequence in light-cone coordinates (valid only in 1+1D).
  * longest_chain_dag -- O(n^2) dynamic programming over the causal order
    (any dimension; used for 1+3D and as a cross-check in 2D).
"""

from __future__ import annotations

import bisect

import numpy as np

from causal_core import causal_matrix


def lightcone_coords(pts):
    """Map 1+1D events (t, x) to null coordinates (u, v) = (t - x, t + x).

    In these coordinates p precedes q  <=>  u_q > u_p AND v_q > v_p.
    """
    pts = np.asarray(pts, dtype=float)
    u = pts[:, 0] - pts[:, 1]
    v = pts[:, 0] + pts[:, 1]
    return u, v


def longest_chain_2d(pts):
    """Longest causal chain length among 1+1D events, via LIS in (u, v).

    Sort by u (break ties by v), then the longest chain is the longest strictly
    increasing subsequence in v.  Returns the number of events in the chain.
    """
    pts = np.asarray(pts, dtype=float)
    if len(pts) == 0:
        return 0
    u, v = lightcone_coords(pts)
    order = np.lexsort((v, u))  # primary u, secondary v
    vs = v[order]
    us = u[order]

    # Strictly-increasing LIS on v, but only across strictly increasing u.
    # Because causal precedence needs BOTH u and v strictly greater, we must not
    # chain two events with equal u.  Sorting by u then taking a strictly
    # increasing subsequence in v handles equal-u ties correctly only if we also
    # forbid equal u; with continuous (Poisson) coordinates ties have measure
    # zero, so a strict LIS on v after the lexsort is exact a.s.
    tails = []  # tails[k] = smallest possible tail v of an increasing subseq of length k+1
    for val in vs:
        i = bisect.bisect_left(tails, val)
        if i == len(tails):
            tails.append(val)
        else:
            tails[i] = val
    _ = us  # kept for clarity; ties are measure-zero for Poisson sprinkles
    return len(tails)


def longest_chain_dag(pts):
    """Longest causal chain length in any dimension, O(n^2) DP.

    Events are processed in time order; dp[j] = longest chain ending at j.
    Returns the number of events in the longest chain.
    """
    pts = np.asarray(pts, dtype=float)
    n = len(pts)
    if n == 0:
        return 0
    order = np.argsort(pts[:, 0])
    P = pts[order]
    C = causal_matrix(P)  # C[i, j] = i precedes j (i < j in time after sort)
    dp = np.ones(n, dtype=int)
    for j in range(n):
        preds = np.nonzero(C[:, j])[0]
        if preds.size:
            dp[j] = 1 + dp[preds].max()
    return int(dp.max())
