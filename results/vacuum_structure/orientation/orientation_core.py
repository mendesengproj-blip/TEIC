"""orientation_core.py -- spin-model Monte-Carlo engine for E1_ORIENTATION.

DATA GENERATOR for the NIVEL4_ORIENTATION programme.  Contains NO relativistic
formula and NO physics interpretation: the words "photon"/"magnon" are forbidden
here -- they live only in the synthesis (COMPARISON ONLY).  This module knows:

  * how to build graphs --
      - 1D ring, 2D / 3D periodic hyper-cubic lattices (the literature anchors
        used by the E1-V gate), and
      - the CAUSAL LINK GRAPH (Hasse diagram = irreducible causal relation) of a
        3+1D Poisson sprinkle (the substrate of the physical measurement);
  * two classical spin models on an arbitrary graph G=(V,E) --
      XY / U(1)   : spin = angle theta_i,    E = -J sum_{(ij) in E} cos(theta_i-theta_j)
      O(3)/Heisenb: spin = unit vector n_i,  E = -J sum_{(ij) in E} n_i . n_j
  * a graph-coloured, fully vectorised Metropolis updater at coupling J (= 1/T,
    with beta := 1 absorbed -- J large = low T = rigid, J small = high T = hot);
  * the orientation correlation  C(r) = <s(0).s(r)>  binned by graph (link)
    distance r (BFS hops in the undirected link graph).

Anti-circularity.  The generator uses only the graph and the cos/dot energy; no
critical temperature, no dispersion relation, no complex literals are inserted.
The correlation is real arithmetic: <cos(theta_i-theta_j)> = <cos cos + sin sin>.

Conventions for the causal substrate follow src/causal_core.py: an event is a row
(t, x1, x2, x3), signature (-,+,+,+); p precedes q iff dt>0 and dt^2-|dx|^2>0.
"""
from __future__ import annotations

import sys
from collections import deque
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box, causal_matrix  # noqa: E402


# ======================================================================== #
# Graph container + builders
# ======================================================================== #
class Graph:
    """Undirected graph with the structures the vectorised Metropolis needs.

    Attributes
    ----------
    n        : number of nodes
    edges    : (E,2) int array, unordered pairs with edges[:,0] < edges[:,1]
    indptr,
    indices  : CSR adjacency (each undirected edge stored in BOTH directions)
    colors   : (n,) int greedy proper colouring (no two neighbours share a colour)
    groups   : list of (m_c,) node-index arrays, one per colour
    seg, nbr : per-colour segment structures for bincount neighbour sums:
               for colour c, ``_nbr[c]`` are the (flattened) neighbour node ids of
               the colour's nodes and ``_seg[c]`` is the local 0..m_c-1 id telling
               bincount which colour-node each neighbour belongs to.
    """

    def __init__(self, n, edges):
        edges = np.asarray(edges, dtype=np.int64).reshape(-1, 2)
        if edges.size:
            lo = np.minimum(edges[:, 0], edges[:, 1])
            hi = np.maximum(edges[:, 0], edges[:, 1])
            keep = lo != hi
            pairs = np.unique(np.stack([lo[keep], hi[keep]], axis=1), axis=0)
        else:
            pairs = np.zeros((0, 2), dtype=np.int64)
        self.n = int(n)
        self.edges = pairs
        self._build_csr()
        self._colour()
        self._build_colour_segments()

    # ------------------------------------------------------------------ #
    def _build_csr(self):
        n, e = self.n, self.edges
        deg = np.zeros(n, dtype=np.int64)
        if e.size:
            both = np.concatenate([e[:, 0], e[:, 1]])
            np.add.at(deg, both, 1)
        self.indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(deg, out=self.indptr[1:])
        self.indices = np.empty(int(self.indptr[-1]), dtype=np.int64)
        cursor = self.indptr[:-1].copy()
        for a, b in e:
            self.indices[cursor[a]] = b
            cursor[a] += 1
            self.indices[cursor[b]] = a
            cursor[b] += 1
        self.degree = deg

    def neighbours(self, i):
        return self.indices[self.indptr[i]:self.indptr[i + 1]]

    # ------------------------------------------------------------------ #
    def _colour(self):
        """Greedy proper colouring, highest-degree-first (Welsh-Powell-ish)."""
        order = np.argsort(-self.degree, kind="stable")
        colors = np.full(self.n, -1, dtype=np.int64)
        for v in order:
            used = set()
            for u in self.neighbours(v):
                cu = colors[u]
                if cu >= 0:
                    used.add(int(cu))
            c = 0
            while c in used:
                c += 1
            colors[v] = c
        self.colors = colors
        self.n_colors = int(colors.max()) + 1 if self.n else 0

    def _build_colour_segments(self):
        self.groups, self._nbr, self._seg = [], [], []
        for c in range(self.n_colors):
            nodes = np.nonzero(self.colors == c)[0]
            self.groups.append(nodes)
            degs = self.degree[nodes]
            nbr = np.concatenate(
                [self.neighbours(v) for v in nodes]) if nodes.size else \
                np.zeros(0, dtype=np.int64)
            seg = np.repeat(np.arange(nodes.size), degs)
            self._nbr.append(nbr.astype(np.int64))
            self._seg.append(seg.astype(np.int64))

    # ------------------------------------------------------------------ #
    def connected_fraction(self):
        return float(np.mean(self.degree > 0)) if self.n else 0.0

    # ---- directed (causal) structure for longest-chain distances ------ #
    def _attach_directed(self, src, dst, tcoord):
        """Store a children CSR (i->j with i before j) and a topological order."""
        n = self.n
        outdeg = np.bincount(src, minlength=n)
        self.ch_indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(outdeg, out=self.ch_indptr[1:])
        self.ch_indices = np.empty(int(self.ch_indptr[-1]), dtype=np.int64)
        cursor = self.ch_indptr[:-1].copy()
        order_by_src = np.argsort(src, kind="stable")
        for k in order_by_src:
            a, b = src[k], dst[k]
            self.ch_indices[cursor[a]] = b
            cursor[a] += 1
        self.topo_order = np.argsort(tcoord, kind="stable")   # time order
        self.tcoord = np.asarray(tcoord, float)

    def children(self, i):
        return self.ch_indices[self.ch_indptr[i]:self.ch_indptr[i + 1]]


def longest_chain_from(graph, source, r_max=None):
    """Longest-chain (causal proper-time) distance from `source` to each event in
    its future.  Returns int array dist (n,): dist[source]=0, dist[descendant]=
    longest number of links on a directed path source->...->descendant, and -1 for
    events that are not in the future of `source`.  DAG longest path via the stored
    topological (time) order; O(V+E)."""
    n = graph.n
    dist = np.full(n, -1, dtype=np.int64)
    dist[source] = 0
    # position of each node in topological order, to iterate only forward
    topo = graph.topo_order
    pos_src = int(np.nonzero(topo == source)[0][0])
    cap = r_max if r_max is not None else n
    for u in topo[pos_src:]:
        du = dist[u]
        if du < 0 or du >= cap:
            continue
        for v in graph.children(u):
            if du + 1 > dist[v]:
                dist[v] = du + 1
    return dist


def ring_1d(n):
    i = np.arange(n)
    return Graph(n, np.stack([i, (i + 1) % n], axis=1))


def lattice_periodic(shape):
    """Periodic hyper-cubic lattice graph of the given shape (any dimension)."""
    shape = tuple(int(s) for s in shape)
    n = int(np.prod(shape))
    idx = np.arange(n).reshape(shape)
    edges = []
    for ax in range(len(shape)):
        nb = np.roll(idx, -1, axis=ax)
        edges.append(np.stack([idx.ravel(), nb.ravel()], axis=1))
    g = Graph(n, np.concatenate(edges, axis=0))
    g.shape = shape
    return g


def causal_link_graph(pts, return_relation=False):
    """Hasse diagram (links = covering relations) of a sprinkled causal set.

    A directed relation i->j is a LINK iff i precedes j and no event k satisfies
    i < k < j.  Transitive reduction:  L = C and not (C @ C).  Returned as an
    undirected Graph (the n_i.n_j coupling is symmetric).
    """
    C = causal_matrix(pts)                      # (n,n) strict precedence
    n = C.shape[0]
    # boolean "exists intermediate" = (C @ C) > 0, done as float32 matmul
    inter = (C.astype(np.float32) @ C.astype(np.float32)) > 0.5
    L = C & ~inter
    src, dst = np.nonzero(L)                     # directed link i->j (i precedes j)
    edges = np.stack([src, dst], axis=1)
    g = Graph(n, edges)
    g.n_links = int(edges.shape[0])
    # directed (time-ordered) children CSR for longest-chain distances, plus the
    # topological (time) order -- pts[:,0] is the time coordinate.
    g._attach_directed(src, dst, np.asarray(pts)[:, 0])
    if return_relation:
        return g, C
    return g


# ======================================================================== #
# Spin models
# ======================================================================== #
class SpinModel:
    """Common Metropolis driver; subclasses supply the spin algebra."""

    def __init__(self, graph, J, seed=0, step=None):
        self.g = graph
        self.J = float(J)
        self.rng = np.random.default_rng(seed)
        self.step = self._default_step() if step is None else float(step)
        self._init_state()

    # ---- to be provided by subclasses -------------------------------- #
    def _default_step(self):
        raise NotImplementedError

    def _init_state(self):
        raise NotImplementedError

    def _color_field(self, c):
        """Neighbour field on the nodes of colour c, from CURRENT spins."""
        raise NotImplementedError

    def _propose_and_accept(self, c, H):
        """Propose new spins on colour c, accept by Metropolis; return n_accept."""
        raise NotImplementedError

    # ---- driver ------------------------------------------------------ #
    def sweep(self):
        acc = 0
        for c in range(self.g.n_colors):
            if self.g.groups[c].size == 0:
                continue
            H = self._color_field(c)
            acc += self._propose_and_accept(c, H)
        return acc / max(self.g.n, 1)

    def equilibrate(self, n_burn, adapt=True, target=0.4):
        """Burn-in; optionally adapt the proposal step toward `target` accept."""
        for s in range(n_burn):
            a = self.sweep()
            if adapt and (s + 1) % 25 == 0:
                if a > target + 0.1:
                    self.step *= 1.15
                elif a < target - 0.1:
                    self.step *= 0.87
                self.step = float(np.clip(self.step, 1e-3, 6.28))

    # ---- observables (subclass supplies the per-node spin algebra) --- #
    def order_parameter(self):
        raise NotImplementedError

    def corr_arrays(self):
        """Return per-node arrays a,b,.. so that s_i.s_j = sum_k a_k(i) a_k(j)."""
        raise NotImplementedError


class XYModel(SpinModel):
    """U(1) / XY model: spin = angle theta_i in (-pi, pi]."""

    def _default_step(self):
        return 1.0

    def _init_state(self):
        self.theta = self.rng.uniform(-np.pi, np.pi, self.g.n)

    def _color_field(self, c):
        nbr, seg, m = self.g._nbr[c], self.g._seg[c], self.g.groups[c].size
        ct, st = np.cos(self.theta), np.sin(self.theta)
        Hx = np.bincount(seg, weights=ct[nbr], minlength=m)
        Hy = np.bincount(seg, weights=st[nbr], minlength=m)
        return Hx, Hy

    def _propose_and_accept(self, c, H):
        Hx, Hy = H
        nodes = self.g.groups[c]
        th = self.theta[nodes]
        prop = th + self.step * self.rng.standard_normal(th.size)
        dE = -self.J * ((np.cos(prop) - np.cos(th)) * Hx +
                        (np.sin(prop) - np.sin(th)) * Hy)
        p = np.exp(-np.clip(dE, 0.0, 50.0))        # =1 when dE<=0 (auto-accept)
        acc = self.rng.random(th.size) < p
        self.theta[nodes] = np.where(acc, prop, th)
        return int(acc.sum())

    def order_parameter(self):
        return float(np.hypot(np.cos(self.theta).mean(), np.sin(self.theta).mean()))

    def corr_arrays(self):
        return [np.cos(self.theta), np.sin(self.theta)]


class O3Model(SpinModel):
    """O(3) / Heisenberg model: spin = unit vector n_i in S^2."""

    def _default_step(self):
        return 0.7

    def _init_state(self):
        v = self.rng.standard_normal((self.g.n, 3))
        self.n = v / np.linalg.norm(v, axis=1, keepdims=True)

    def _color_field(self, c):
        nbr, seg, m = self.g._nbr[c], self.g._seg[c], self.g.groups[c].size
        H = np.empty((m, 3))
        for k in range(3):
            H[:, k] = np.bincount(seg, weights=self.n[nbr, k], minlength=m)
        return H

    def _propose_and_accept(self, c, H):
        nodes = self.g.groups[c]
        old = self.n[nodes]
        v = old + self.step * self.rng.standard_normal(old.shape)
        prop = v / np.linalg.norm(v, axis=1, keepdims=True)
        dE = -self.J * np.sum((prop - old) * H, axis=1)
        p = np.exp(-np.clip(dE, 0.0, 50.0))        # =1 when dE<=0 (auto-accept)
        acc = self.rng.random(old.shape[0]) < p
        self.n[nodes] = np.where(acc[:, None], prop, old)
        return int(acc.sum())

    def order_parameter(self):
        return float(np.linalg.norm(self.n.mean(axis=0)))

    def corr_arrays(self):
        return [self.n[:, 0], self.n[:, 1], self.n[:, 2]]


MODELS = {"U(1)": XYModel, "O(3)": O3Model}


# ======================================================================== #
# Correlation C(r) by graph distance
# ======================================================================== #
def bfs_distances(graph, source, r_max):
    """Graph (hop) distance from `source` to every node, capped at r_max.

    Returns an int array dist (n,), with -1 for nodes farther than r_max or
    unreachable.
    """
    dist = np.full(graph.n, -1, dtype=np.int64)
    dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft()
        du = dist[u]
        if du >= r_max:
            continue
        for v in graph.neighbours(u):
            if dist[v] < 0:
                dist[v] = du + 1
                q.append(v)
    return dist


def pick_sources(graph, n_sources, rng):
    cand = np.nonzero(graph.degree > 0)[0]
    if cand.size == 0:
        return np.zeros(0, dtype=np.int64)
    if cand.size <= n_sources:
        return cand
    return rng.choice(cand, size=n_sources, replace=False)


def precompute_source_distances(graph, sources, r_max):
    return [bfs_distances(graph, int(s), r_max) for s in sources]


class CorrelationAccumulator:
    """Accumulates C(r) = <s_i . s_j> over (source, distance-r) shells & samples."""

    def __init__(self, sources, dist_list, r_max):
        self.sources = sources
        self.dist_list = dist_list
        self.r_max = r_max
        self.sum_c = np.zeros(r_max + 1)
        self.sum_w = np.zeros(r_max + 1)

    def add(self, model):
        arrs = model.corr_arrays()          # list of per-node arrays
        for s, dist in zip(self.sources, self.dist_list):
            # s_i . s_source  for every node i
            dot = np.zeros(model.g.n)
            for a in arrs:
                dot += a * a[s]
            mask = dist >= 0
            r = dist[mask]
            self.sum_c += np.bincount(r, weights=dot[mask], minlength=self.r_max + 1)
            self.sum_w += np.bincount(r, minlength=self.r_max + 1)

    def result(self):
        with np.errstate(invalid="ignore", divide="ignore"):
            C = self.sum_c / self.sum_w
        r = np.arange(self.r_max + 1)
        good = self.sum_w > 0
        return r[good], C[good], self.sum_w[good]


def measure_correlation(model, n_burn, n_meas, meas_every=2, n_sources=24,
                        r_max=None, adapt=True):
    """Equilibrate then accumulate C(r) over n_meas samples.  Returns r, C, counts,
    plus the time series of the order parameter (for an equilibration check)."""
    g = model.g
    if r_max is None:
        r_max = 24
    sources = pick_sources(g, n_sources, model.rng)
    dist_list = precompute_source_distances(g, sources, r_max)
    model.equilibrate(n_burn, adapt=adapt)
    acc = CorrelationAccumulator(sources, dist_list, r_max)
    m_series = []
    taken = 0
    s = 0
    while taken < n_meas:
        model.sweep()
        s += 1
        if s % meas_every == 0:
            acc.add(model)
            m_series.append(model.order_parameter())
            taken += 1
    r, C, w = acc.result()
    return r, C, w, np.array(m_series)


# ======================================================================== #
# Transverse structure factor S(k) (Goldstone gaplessness / spatial stiffness)
# ======================================================================== #
def transverse_components(model):
    """Return a list of per-node TRANSVERSE spin-fluctuation arrays (orthogonal to
    the instantaneous mean orientation).  For XY: one array (the angle deviation
    projected transverse).  For O(3): two arrays spanning the tangent plane.

    Transverse = the Goldstone directions; their structure factor probes the soft
    (gapless) modes, not the massive amplitude direction.
    """
    if isinstance(model, XYModel):
        th = model.theta
        mbar = np.arctan2(np.sin(th).mean(), np.cos(th).mean())
        d = (th - mbar + np.pi) % (2 * np.pi) - np.pi    # wrapped deviation
        return [d - d.mean()]
    elif isinstance(model, O3Model):
        n = model.n
        mvec = n.mean(axis=0)
        mhat = mvec / (np.linalg.norm(mvec) + 1e-12)
        # build an orthonormal transverse frame (e1,e2) perpendicular to mhat
        a = np.array([1.0, 0.0, 0.0]) if abs(mhat[0]) < 0.9 else np.array([0, 1.0, 0])
        e1 = a - mhat * (a @ mhat)
        e1 /= np.linalg.norm(e1) + 1e-12
        e2 = np.cross(mhat, e1)
        return [n @ e1, n @ e2]
    raise TypeError("unknown model")


def structure_factor(comp_list, xs, kmags, n_dirs=3):
    """Transverse structure factor S(k) = <|sum_i s_perp,i e^{-i k.x_i}|^2> / N,
    averaged over transverse components, over the n_dirs spatial axes, and over the
    supplied list of equilibrium samples.

    Parameters
    ----------
    comp_list : list over samples; each entry is the list returned by
                transverse_components (per-sample, per-component node arrays).
    xs        : (N, d_space) spatial coordinates of the events (time column dropped).
    kmags     : 1D array of wavenumber magnitudes to probe.
    n_dirs    : number of spatial axes to average over (<= d_space).

    Returns S(k) array aligned with kmags (real arithmetic: cos/sin sums).
    """
    xs = np.asarray(xs, float)
    N = xs.shape[0]
    d_space = xs.shape[1]
    n_dirs = min(n_dirs, d_space)
    S = np.zeros(len(kmags))
    cnt = 0
    for comps in comp_list:
        for s_perp in comps:
            for ax in range(n_dirs):
                phase_arg = np.outer(kmags, xs[:, ax])      # (K, N)
                re = np.cos(phase_arg) @ s_perp
                im = np.sin(phase_arg) @ s_perp
                S += (re ** 2 + im ** 2) / N
                cnt += 1
    return S / max(cnt, 1)


# ======================================================================== #
# Fitting C(r) to the three competing forms
# ======================================================================== #
def _r2(y, yhat):
    ss_res = np.sum((y - yhat) ** 2)
    ss_tot = np.sum((y - y.mean()) ** 2)
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def fit_forms(r, C, sigma=None, r_lo=2, floor_abs=0.02):
    """Classify C(r) as exponential, power law, or constant (long-range order).

    The classification is physically robust rather than a brittle AIC race, which
    is unstable when C(r) is short-ranged (few points above the noise floor) or a
    near-flat power law (eta ~ 0) is indistinguishable from a constant by chi^2:

      C_long  = long-distance plateau value, the weighted mean of C over the outer
                half of the curve (the estimator of C(infinity); for true LRO this
                equals m^2, the Mermin clustering value -- checked in the gate).
      flat    = the curve has stopped decaying: C_long / C_mid > FLAT_RATIO, where
                C_mid is C at ~0.4 r_max.

    Decision:
      * LRO / 'const'   if C_long > C_LONG_MIN AND flat;
      * otherwise fit exp (log C vs r) and power (log C vs log r) over the window
        r>=r_lo, C>floor, and take whichever is straighter (higher R^2):
        'exp'   -> finite correlation length xi (short-range / disordered),
        'power' -> scale-free decay r^{-eta} (critical / KT / quasi-LRO).

    Anti-circularity: only the measured curve is used; no critical temperature or
    target exponent enters.  Returns parameters + R^2 for both forms and C_long.
    """
    FLAT_RATIO = 0.85
    C_LONG_MIN = 0.05
    r = np.asarray(r, float)
    C = np.asarray(C, float)
    ss = None if sigma is None else np.asarray(sigma, float)
    rmax = r.max() if r.size else 0.0

    # ---- plateau value C_long and mid value C_mid (full curve) ----
    outer = r >= max(r_lo, 0.5 * rmax)
    if outer.any():
        if ss is None:
            C_long = float(np.mean(C[outer]))
        else:
            wv = 1.0 / np.maximum(ss[outer], 1e-6) ** 2
            C_long = float(np.sum(wv * C[outer]) / np.sum(wv))
    else:
        C_long = float(C[-1]) if C.size else 0.0
    r_mid = max(r_lo, round(0.4 * rmax))
    mid_idx = int(np.argmin(np.abs(r - r_mid)))
    C_mid = float(C[mid_idx])
    flat_ratio = C_long / C_mid if C_mid > 1e-9 else 0.0
    is_flat = (C_long > C_LONG_MIN) and (flat_ratio > FLAT_RATIO)

    # ---- shape-fit window ----
    floor = floor_abs
    if ss is not None:
        win0 = (r >= r_lo) & np.isfinite(C)
        if win0.any():
            floor = max(floor_abs, 4.0 * float(np.median(ss[win0])))
    sel = (r >= r_lo) & (C > floor) & np.isfinite(C)

    out = {"n_points": int(sel.sum()), "C_long": C_long, "C_mid": C_mid,
           "flat_ratio": float(flat_ratio), "floor": float(floor)}

    if sel.sum() >= 3:
        rr, cc = r[sel], C[sel]
        logc = np.log(cc)
        be = np.polyfit(rr, logc, 1)               # logC = be0*r + be1
        xi = -1.0 / be[0] if be[0] < 0 else np.inf
        Ce = np.exp(be[1] + be[0] * rr)
        R2_exp = _r2(cc, Ce)
        bp = np.polyfit(np.log(rr), logc, 1)       # logC = bp0*logr + bp1
        eta = -bp[0]
        Cp = np.exp(bp[1] + bp[0] * np.log(rr))
        R2_pow = _r2(cc, Cp)
        out["exp"] = {"xi": float(xi), "amp": float(np.exp(be[1])), "R2": R2_exp}
        out["power"] = {"eta": float(eta), "amp": float(np.exp(bp[1])), "R2": R2_pow}
    else:
        out["exp"] = {"xi": float("nan"), "amp": float("nan"), "R2": float("nan")}
        out["power"] = {"eta": float("nan"), "amp": float("nan"), "R2": float("nan")}
        R2_exp = R2_pow = float("nan")
    out["const"] = {"C0": C_long}

    # ---- decision ----
    if is_flat:
        winner = "const"
    elif sel.sum() < 3:
        winner = "insufficient"
    elif R2_exp >= R2_pow:
        winner = "exp"
    else:
        winner = "power"
    out["winner"] = winner
    out["is_flat_plateau"] = bool(is_flat)
    return out


# ======================================================================== #
# 1D XY transfer-matrix exact correlation (quantitative gate anchor)
# ======================================================================== #
def xy_1d_exact_corr(J, r):
    """Exact equilibrium correlation of the 1D classical XY chain with energy
    -J sum cos(dtheta):  C(r) = (I1(J)/I0(J))**r.  COMPARISON ONLY anchor."""
    from scipy.special import i0, i1
    ratio = i1(J) / i0(J)
    return ratio ** np.asarray(r, float)


# ======================================================================== #
# Self-test
# ======================================================================== #
if __name__ == "__main__":
    print("orientation_core self-test")
    # graph builders
    g1 = ring_1d(12)
    assert g1.degree.min() == 2 and g1.degree.max() == 2
    g2 = lattice_periodic((6, 6))
    assert g2.degree.min() == 4 and g2.degree.max() == 4
    g3 = lattice_periodic((4, 4, 4))
    assert g3.degree.min() == 6 and g3.degree.max() == 6
    # proper colouring check on the causal graph
    rng = np.random.default_rng(0)
    pts = sprinkle_box(40.0, [(0, 3.0), (0, 3.0), (0, 3.0), (0, 3.0)], rng)
    gc = causal_link_graph(pts)
    bad = 0
    for a, b in gc.edges:
        if gc.colors[a] == gc.colors[b]:
            bad += 1
    print(f"  causal graph: n={gc.n} links={gc.n_links} colours={gc.n_colors} "
          f"conn_frac={gc.connected_fraction():.2f} colour_violations={bad}")
    assert bad == 0
    # quick 1D XY run vs exact (loose, short run)
    g = ring_1d(2000)
    m = XYModel(g, J=2.0, seed=1)
    r, C, w, ms = measure_correlation(m, n_burn=400, n_meas=120, n_sources=40,
                                      r_max=10)
    exact = xy_1d_exact_corr(2.0, r)
    print("  1D XY J=2  r, C_mc, C_exact:")
    for rr_, cm, ce in list(zip(r, C, exact))[:8]:
        print(f"    r={rr_:2d}  mc={cm:+.3f}  exact={ce:+.3f}")
    fit = fit_forms(r, C)
    print(f"  fit winner (1D XY, expect exp): {fit['winner']}")
    print("self-test OK")
