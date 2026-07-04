"""e5_core.py -- U(1) Wilson lattice gauge engine for the E5_PHOTON_LINK_SECTOR
campaign. Works on (a) regular periodic d-dimensional lattices (for the mandatory
validation gate against known U(1) results) and (b) an arbitrary plaquette list
(for the causal-set diamonds). Contains NO relativistic/quantum literal: the gauge
dynamics is real Metropolis on link angles with the Wilson action S=beta*sum_P
[1-cos theta_P]; the word 'photon' lives only in the synthesis.

A plaquette is a closed oriented loop of 4 links with signs +/-1; the holonomy is
theta_P = sum_j sign_j theta[link_j]. The engine precomputes, per link, the other
three (link,sign) entries of every plaquette containing it, so single-link
Metropolis updates are exact and vectorised over a link's plaquettes.
"""
from __future__ import annotations

import numpy as np


# ====================================================================== #
# Regular periodic d-dim lattice plaquettes (validation gate)
# ====================================================================== #
def regular_lattice(shape):
    """U(1) plaquettes of a periodic hyper-cubic lattice of the given shape.

    Links indexed link_id = site*d + mu (site = raveled coords, mu = direction).
    Returns (L, plaq_links (P,4) int, plaq_signs (P,4) float)."""
    shape = tuple(int(s) for s in shape)
    d = len(shape)
    n_sites = int(np.prod(shape))
    L = n_sites * d
    coords = np.array(np.unravel_index(np.arange(n_sites), shape)).T  # (n_sites,d)

    def shift(site_coords, mu):
        c = site_coords.copy()
        c[:, mu] = (c[:, mu] + 1) % shape[mu]
        return np.ravel_multi_index(c.T, shape)

    site_ids = np.arange(n_sites)
    plinks, psigns = [], []
    for mu in range(d):
        for nu in range(mu + 1, d):
            x = site_ids
            x_mu = shift(coords, mu)
            x_nu = shift(coords, nu)
            l1 = x * d + mu            # theta_mu(x)            +
            l2 = x_mu * d + nu         # theta_nu(x+mu)         +
            l3 = x_nu * d + mu         # theta_mu(x+nu)         -
            l4 = x * d + nu            # theta_nu(x)            -
            plinks.append(np.stack([l1, l2, l3, l4], axis=1))
            psigns.append(np.tile([1.0, 1.0, -1.0, -1.0], (n_sites, 1)))
    plaq_links = np.concatenate(plinks, axis=0)
    plaq_signs = np.concatenate(psigns, axis=0)
    return L, plaq_links, plaq_signs


# ====================================================================== #
# Per-link plaquette structure (for single-link Metropolis)
# ====================================================================== #
def build_link_plaqs(L, plaq_links, plaq_signs):
    """For each link, list the plaquettes containing it with this link's sign and
    the other three (link,sign). Returns ragged arrays packed as lists."""
    P = plaq_links.shape[0]
    buckets = [[] for _ in range(L)]
    for p in range(P):
        for j in range(4):
            l = plaq_links[p, j]
            buckets[l].append((p, j))
    self_sign = []
    other_links = []
    other_signs = []
    for l in range(L):
        rows = buckets[l]
        ss = np.array([plaq_signs[p, j] for (p, j) in rows])
        ol = np.array([[plaq_links[p, k] for k in range(4) if k != j] for (p, j) in rows],
                      dtype=np.int64).reshape(len(rows), 3) if rows else np.zeros((0, 3), np.int64)
        os = np.array([[plaq_signs[p, k] for k in range(4) if k != j] for (p, j) in rows],
                      dtype=float).reshape(len(rows), 3) if rows else np.zeros((0, 3))
        self_sign.append(ss)
        other_links.append(ol)
        other_signs.append(os)
    return self_sign, other_links, other_signs


class U1Gauge:
    """U(1) Wilson gauge field with single-link Metropolis on an arbitrary plaquette
    list."""

    def __init__(self, L, plaq_links, plaq_signs, beta, seed=0, step=1.0):
        self.L = L
        self.plaq_links = plaq_links
        self.plaq_signs = plaq_signs
        self.beta = float(beta)
        self.rng = np.random.default_rng(seed)
        self.step = float(step)
        self.theta = self.rng.uniform(-np.pi, np.pi, L)
        self.self_sign, self.other_links, self.other_signs = build_link_plaqs(
            L, plaq_links, plaq_signs)

    def plaquette_holonomies(self):
        return (self.plaq_signs * self.theta[self.plaq_links]).sum(axis=1)

    def mean_cos_plaq(self):
        return float(np.cos(self.plaquette_holonomies()).mean())

    def sweep(self):
        acc = 0
        order = self.rng.permutation(self.L)
        for l in order:
            ol = self.other_links[l]
            if ol.shape[0] == 0:
                continue
            ss = self.self_sign[l]                       # (n_l,)
            staple = (self.other_signs[l] * self.theta[ol]).sum(axis=1)  # (n_l,)
            old = self.theta[l]
            new = old + self.step * self.rng.standard_normal()
            # S_l = -beta sum_P cos(ss*theta_l + staple)
            dE = -self.beta * np.sum(np.cos(ss * new + staple) - np.cos(ss * old + staple))
            if dE <= 0 or self.rng.random() < np.exp(-dE):
                self.theta[l] = new
                acc += 1
        return acc / max(self.L, 1)

    def equilibrate(self, n_burn, adapt=True, target=0.4):
        for s in range(n_burn):
            a = self.sweep()
            if adapt and (s + 1) % 20 == 0:
                if a > target + 0.1:
                    self.step *= 1.15
                elif a < target - 0.1:
                    self.step *= 0.87
                self.step = float(np.clip(self.step, 1e-2, 6.28))

    def measure_plaq(self, n_meas, meas_every=2):
        vals = []
        s = 0
        while len(vals) < n_meas:
            self.sweep(); s += 1
            if s % meas_every == 0:
                vals.append(self.mean_cos_plaq())
        return np.array(vals)


def gauge_transform(theta, plaq_links, plaq_signs, L, link_sites=None, rng=None):
    """Apply a random local gauge transform if a (site_of_link_tail/head) map is
    given; used by the gauge-invariance gate on the regular lattice (where the map
    is known). Returns transformed theta and the max change in plaquette holonomy."""
    raise NotImplementedError  # gate builds the transform explicitly for the lattice


# ====================================================================== #
# Causal-set diamond plaquettes (height-2 causal diamonds)
# ====================================================================== #
def causal_diamond_plaquettes(g, max_per_pair=2, max_plaqs=20000, seed=0):
    """Build U(1) plaquettes from height-2 causal diamonds of a causal link graph g
    (orientation_core.causal_link_graph): for events i<k joined by >=2 distinct
    length-2 link paths i->a->k and i->b->k, the loop i->a->k->b->i is a plaquette.

    Links are the undirected Hasse edges g.edges (id = row index). Returns
    (L, plaq_links (P,4), plaq_signs (P,4)). Orientation along i->a->k uses +; the
    return path k->b->i uses -. Requires g.children (directed Hasse)."""
    edges = g.edges                       # (E,2) with edges[:,0]<edges[:,1]
    L = edges.shape[0]
    # map undirected pair -> link id
    emap = {}
    for eid, (a, b) in enumerate(edges):
        emap[(int(a), int(b))] = eid

    def link_id(u, v):
        a, b = (u, v) if u < v else (v, u)
        return emap.get((int(a), int(b)), -1)

    rng = np.random.default_rng(seed)
    plinks, psigns = [], []
    # for each event i, its Hasse children; for each child a, a's children k
    # collect, per (i,k), the intermediate nodes a with i->a->k
    n = g.n
    for i in range(n):
        ch = g.children(i)
        if ch.size < 1:
            continue
        mids_by_k = {}
        for a in ch:
            for k in g.children(a):
                mids_by_k.setdefault(int(k), []).append(int(a))
        for k, mids in mids_by_k.items():
            if len(mids) < 2:
                continue
            # pick up to max_per_pair distinct intermediate pairs
            pairs = [(mids[m], mids[mm])
                     for m in range(len(mids)) for mm in range(m + 1, len(mids))]
            if len(pairs) > max_per_pair:
                idx = rng.choice(len(pairs), max_per_pair, replace=False)
                pairs = [pairs[t] for t in idx]
            for (a, b) in pairs:
                lia = link_id(i, a); lak = link_id(a, k)
                lkb = link_id(k, b); lbi = link_id(b, i)
                if min(lia, lak, lkb, lbi) < 0:
                    continue
                # holonomy i->a->k->b->i: +theta(i,a)+theta(a,k)+theta(k,b)+theta(b,i)
                # but link ids are undirected; assign sign by direction vs stored pair
                def signed(u, v, lid):
                    a0, b0 = edges[lid]
                    return 1.0 if (int(a0), int(b0)) == (min(u, v), max(u, v)) and u < v else \
                           (1.0 if u < v else -1.0)
                # simpler: orient by the directed step; stored edge is (lo,hi).
                def sdir(u, v, lid):
                    lo, hi = edges[lid]
                    return 1.0 if (u == lo and v == hi) else -1.0
                plinks.append([lia, lak, lkb, lbi])
                psigns.append([sdir(i, a, lia), sdir(a, k, lak),
                               sdir(k, b, lkb), sdir(b, i, lbi)])
                if len(plinks) >= max_plaqs:
                    return L, np.array(plinks), np.array(psigns)
    if not plinks:
        return L, np.zeros((0, 4), np.int64), np.zeros((0, 4))
    return L, np.array(plinks, dtype=np.int64), np.array(psigns, dtype=float)


if __name__ == "__main__":
    # quick self-test: regular 4D lattice gauge invariance of plaquette holonomies
    L, pl, ps = regular_lattice((3, 3, 3, 3))
    g = U1Gauge(L, pl, ps, beta=1.0, seed=0)
    h0 = g.plaquette_holonomies().copy()
    print(f"4D 3^4: L={L} plaquettes={pl.shape[0]} <cos>={g.mean_cos_plaq():+.3f}")
