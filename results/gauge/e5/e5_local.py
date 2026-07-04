"""e5_local.py -- LORENTZ-INVARIANT local causal graph for controlled-geometry FSS.

The confound in E5-1 was that a Poisson causal set in a growing box has a mean
degree that GROWS with box size (each event's light cone captures more events), so
the diamond plaquette count exploded faster than the volume and the finite-size
scaling did not compare like with like.

Fix: keep only causal links with proper time tau_ij <= tau_max. Proper time is a
LORENTZ SCALAR, so this cutoff is Lorentz-invariant -- it does not select a frame
(unlike a coordinate-time or distance cutoff). With tau_max fixed, a bulk event
links only to events within a fixed proper-time neighbourhood whose expected count
is rho * Vol(causal diamond of height tau_max) = constant. Growing the box at fixed
(rho, tau_max) then holds the LOCAL geometry (mean degree, diamonds per link) fixed
while N grows -- a clean FSS.

Provides a graph object compatible with e5_core.causal_diamond_plaquettes
(.n, .edges, .children).
"""
from __future__ import annotations

import numpy as np


class LocalCausalGraph:
    def __init__(self, pts, tau_max):
        self.pts = np.asarray(pts, float)
        self.n = self.pts.shape[0]
        self.tau_max = float(tau_max)
        self._build()

    def _build(self):
        pts = self.pts
        n = self.n
        t = pts[:, 0]
        x = pts[:, 1:]
        src, dst = [], []
        # O(n^2): for each i, find j in its future within proper time tau_max
        for i in range(n):
            dt = t - t[i]
            future = dt > 0
            dx2 = np.sum((x - x[i]) ** 2, axis=1)
            tau2 = dt ** 2 - dx2
            sel = future & (tau2 > 0) & (tau2 <= self.tau_max ** 2)
            j = np.nonzero(sel)[0]
            src.extend([i] * j.size)
            dst.extend(j.tolist())
        src = np.asarray(src, dtype=np.int64)
        dst = np.asarray(dst, dtype=np.int64)
        self._src, self._dst = src, dst
        # undirected edges, lo<hi, unique
        lo = np.minimum(src, dst); hi = np.maximum(src, dst)
        if lo.size:
            self.edges = np.unique(np.stack([lo, hi], axis=1), axis=0)
        else:
            self.edges = np.zeros((0, 2), dtype=np.int64)
        # children CSR (i -> j, i before j)
        outdeg = np.bincount(src, minlength=n)
        self.ch_indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(outdeg, out=self.ch_indptr[1:])
        self.ch_indices = np.empty(int(self.ch_indptr[-1]), dtype=np.int64)
        cursor = self.ch_indptr[:-1].copy()
        order = np.argsort(src, kind="stable")
        for k in order:
            a = src[k]
            self.ch_indices[cursor[a]] = dst[k]
            cursor[a] += 1
        # undirected degree
        deg = np.zeros(n, dtype=np.int64)
        if self.edges.size:
            np.add.at(deg, self.edges[:, 0], 1)
            np.add.at(deg, self.edges[:, 1], 1)
        self.degree = deg
        self.n_links = self.edges.shape[0]

    def children(self, i):
        return self.ch_indices[self.ch_indptr[i]:self.ch_indptr[i + 1]]

    def mean_degree(self):
        return float(self.degree.mean()) if self.n else 0.0
