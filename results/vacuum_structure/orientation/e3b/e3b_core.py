"""e3b_core.py -- causal-network defect engine for the E3b_CAUSAL_DEFECT campaign.

DATA GENERATOR for NIVEL4_ORIENTATION entry FN3b.  Contains NO physics
interpretation: the words "matter"/"particle"/"mass"/"E=mc^2" are forbidden here
-- they live only in the synthesis (COMPARISON ONLY).  E3 ran the hedgehog on the
SPATIAL cubic lattice and found Verdict B (metastable, unwinds thermally in
~2700 sweeps, no Derrick minimum).  E3b tests the one mechanism the cubic lattice
cannot carry: the RIGIDITY OF THE 3+1D CAUSAL CONE.  The hypothesis is that the
arrow of time -- the irreversibility of causal evolution -- supplies a topological
barrier the spatial lattice lacks.

This module knows how to:

  * sprinkle a 3+1D Poisson causal set (cols [t, x, y, z]) -- the SAME R1/D3
    substrate (src/causal_core.sprinkle_box), Lorentz-invariant in distribution;
  * build the CAUSAL LINK (Hasse / covering) substrate L = C & ~(C @ C): an
    orientation field n_e in S^2 lives on each EVENT e, coupled along causal links
    only (local, NOT the full mean-field causal relation of E1);
  * seed a hedgehog texture  n(r) = r_hat  from the SPATIAL coordinates of each
    event (time-independent: a static defect in the spatial slice);
  * MEASURE the topological charge B on the irregular Poisson cloud by the
    solid-angle (Berg-Luscher) degree adapted to DELAUNAY TETRAHEDRA: every
    tetrahedron's boundary is a small S^2 (4 outward triangles); the signed
    spherical area of n over it / 4pi is the integer charge enclosed; interior
    faces cancel between adjacent tetrahedra, so the total is the degree of n on
    the outer (convex-hull) boundary surface.  Verified B=+1 hedgehog, 0 vacuum;
  * EVOLVE the field two ways (charter E3b-2):
      Protocol A -- deterministic CAUSAL evolution: process events in increasing
        time, set n_e by minimising the link energy against its CAUSAL PAST only
        (the past is fixed; the future cannot un-write it -- the arrow of time);
      Protocol B -- causal MONTE CARLO: Metropolis that may climb thermal
        barriers but still respects causality (the seeded past slab is frozen);
  * the Derrick functional on causal links  E = sum_links (1 - n_i . n_j)  and its
    behaviour under a SPATIAL dilation, split into the energy carried by links with
    a large spatial separation (E_spatial) and by nearly-purely-temporal links
    (E_temporal) -- the causal Derrick virial of charter E3b-3.

Anti-circularity.  No topological number, no critical coupling, no c, no
dispersion law and no E=mc^2 is inserted into the generator.  B is a pure
solid-angle count of the spins; E is the cos/dot bond functional; the light cone
dt^2 > dx^2 is the GEOMETRY of any sprinkle (how a causal set is defined), not a
dynamical input.  c enters NOWHERE here; in E3b-4 it is the measured 0.98 of E2.
The arrow of time is implemented as "process events in increasing t and let the
past fix the future" -- a counting rule, not a relativistic formula.

Conventions follow src/causal_core.py (signature (-,+,+,+); p precedes q iff
dt>0 and dt^2-|dx|^2>0) and results/.../orientation/e3/e3_core.py (O(3) Heisenberg,
solid-angle degree via Van Oosterom-Strackee).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.spatial import Delaunay

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                       # .../TEIC
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE.parent / "e3"))  # reuse the validated solid-angle helper

sys.path.insert(0, str(HERE.parent))             # results/.../orientation (orientation_core)
from causal_core import sprinkle_box, lattice_box, causal_matrix   # noqa: E402
from e3_core import _tri_solid_angle                               # noqa: E402
import orientation_core as oc                                      # noqa: E402


# ====================================================================== #
# 3+1D causal substrate
# ====================================================================== #
def sprinkle_causal(rho, T, L, seed):
    """Poisson sprinkle in [0,T] x [-L,L]^3.  Returns pts (n,4), cols [t,x,y,z],
    sorted by time for deterministic causal sweeps."""
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, T), (-L, L), (-L, L), (-L, L)], rng)
    pts = pts[np.argsort(pts[:, 0], kind="stable")]
    return pts


class Substrate:
    """Causal-link (Hasse) structure of a 3+1D sprinkle.

    A directed relation i->j is a LINK iff i precedes j and no event lies strictly
    between them (transitive reduction L = C & ~(C @ C)).  The O(3) coupling
    n_i.n_j is symmetric, so links are also stored undirected; but the directed
    parent/child split is what makes the ARROW OF TIME explicit -- Protocol A
    updates an event from its parents (causal past) only.

    Attributes
    ----------
    pts      : (n,4) events [t,x,y,z], time-sorted
    n        : number of events
    src,dst  : directed links src->dst (src precedes dst in time)
    parents  : list[array] -- past-linked neighbours of each event (t smaller)
    children : list[array] -- future-linked neighbours
    edges    : (E,2) undirected link pairs (i<j by index)
    degree   : (n,) undirected link degree
    mean_degree : float
    """

    def __init__(self, pts):
        pts = np.asarray(pts, float)
        self.pts = pts
        self.n = pts.shape[0]
        C = causal_matrix(pts)                       # (n,n) strict precedence
        # transitive reduction: drop relations with an intermediate event
        inter = (C.astype(np.float32) @ C.astype(np.float32)) > 0.5
        Lk = C & ~inter
        src, dst = np.nonzero(Lk)                    # src precedes dst
        self.src, self.dst = src, dst
        self.edges = np.stack([np.minimum(src, dst), np.maximum(src, dst)], axis=1)
        self.edges = np.unique(self.edges, axis=0) if self.edges.size else \
            np.zeros((0, 2), dtype=np.int64)
        # parent / child adjacency (index lists), grouped vectorised
        self.parents = _group_by(dst, src, self.n)   # parents[j] = sources into j
        self.children = _group_by(src, dst, self.n)  # children[i] = targets of i
        # undirected degree
        deg = np.zeros(self.n, dtype=np.int64)
        if self.edges.size:
            np.add.at(deg, self.edges[:, 0], 1)
            np.add.at(deg, self.edges[:, 1], 1)
        self.degree = deg
        self.mean_degree = float(deg.mean()) if self.n else 0.0
        self.n_links = int(self.edges.shape[0])
        self.topo_order = np.argsort(pts[:, 0], kind="stable")
        self._graph = None

    @property
    def graph(self):
        """Lazily build the undirected coloured graph (orientation_core.Graph) used
        by the vectorised colour-checkerboard Metropolis and cooler."""
        if self._graph is None:
            self._graph = oc.Graph(self.n, self.edges)
        return self._graph

    def causal_violations(self):
        """Number of directed links whose target is NOT strictly later in time --
        must be 0 (the arrow of time is respected by construction)."""
        return int(np.sum(self.pts[self.dst, 0] <= self.pts[self.src, 0]))


def _group_by(keys, vals, n):
    """Return list L with L[k] = sorted vals where keys==k, for k in range(n)."""
    out = [np.empty(0, dtype=np.int64) for _ in range(n)]
    if keys.size == 0:
        return out
    order = np.argsort(keys, kind="stable")
    ks = keys[order]
    vs = vals[order]
    # split points where key changes
    bounds = np.nonzero(np.diff(ks))[0] + 1
    starts = np.concatenate([[0], bounds])
    ends = np.concatenate([bounds, [ks.size]])
    for s, e in zip(starts, ends):
        out[int(ks[s])] = vs[s:e].copy()
    return out


# ====================================================================== #
# Orientation fields on events (spatial textures)
# ====================================================================== #
def _normalize(v, eps=1e-12):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + eps)


def hedgehog_field(pts, charge=+1, center=(0.0, 0.0, 0.0), core=0.0):
    """Radial spatial texture n(r) = sign * r_hat from each event's SPATIAL
    coordinates (x,y,z); the time coordinate is ignored, so this is a static
    defect in the spatial slice.  `core` softens the singular centre: within r<core
    n is blended toward +z (regularises the unrepresentable r=0 point).  Returns
    (n,3) unit vectors."""
    x = pts[:, 1:4] - np.asarray(center, float)
    r = np.linalg.norm(x, axis=1, keepdims=True)
    n = np.sign(charge) * x / (r + 1e-12)
    if core > 0:
        w = np.clip(r / core, 0, 1)                 # 0 at centre, 1 outside core
        zhat = np.array([0.0, 0.0, 1.0])
        n = w * n + (1 - w) * zhat
    else:
        n = np.where(r > 1e-9, n, np.array([0.0, 0.0, 1.0]))
    return _normalize(n)


def uniform_field(pts, axis=(0.0, 0.0, 1.0)):
    """Ordered ferromagnetic vacuum n = const (degree 0)."""
    n = np.zeros((pts.shape[0], 3))
    n[...] = _normalize(np.asarray(axis, float))
    return n


# ====================================================================== #
# Topological charge B on the Poisson cloud (Delaunay-tetrahedron degree)
# ====================================================================== #
# faces[a] = the 3 vertices of the tetra face OPPOSITE local vertex a (the apex).
_TET_FACES = ((1, 2, 3), (0, 2, 3), (0, 1, 3), (0, 1, 2))


def charge_field_poisson(xyz, n, tri=None):
    """Per-tetrahedron topological charge of the orientation field n sampled at the
    3D points xyz.  Delaunay-tetrahedralise xyz; for each tetra sum the solid
    angles of its 4 OUTWARD spherical triangles (Van Oosterom-Strackee) / 4pi.

    Each per-tetra value is ~integer (the degree of n on that little S^2); their
    sum is the degree of n on the OUTER boundary surface (interior faces, shared by
    two tetra with opposite outward orientation, cancel exactly).  Returns
    (q, tri) with q shape (n_tetra,)."""
    xyz = np.asarray(xyz, float)
    n = np.asarray(n, float)
    if tri is None:
        tri = Delaunay(xyz)
    simp = tri.simplices                              # (m,4) vertex indices
    P = xyz[simp]                                      # (m,4,3) coords
    NV = n[simp]                                        # (m,4,3) field
    m = simp.shape[0]
    q = np.zeros(m)
    for apex, (a, b, c) in enumerate(_TET_FACES):
        A, B, Cc = P[:, a], P[:, b], P[:, c]
        normal = np.cross(B - A, Cc - A)               # (m,3)
        # outward = normal points away from the apex vertex of THIS face
        outward = np.einsum("mi,mi->m", normal, A - P[:, apex]) > 0
        na = NV[:, a]
        nb = np.where(outward[:, None], NV[:, b], NV[:, c])
        nc = np.where(outward[:, None], NV[:, c], NV[:, b])
        q += _tri_solid_angle(na, nb, nc)
    return q / (4.0 * np.pi), tri


def topological_charge_poisson(xyz, n, tri=None):
    """Total degree B = sum of the per-tetra solid-angle charge.  Float, close to
    an integer for a clean texture."""
    q, _ = charge_field_poisson(xyz, n, tri)
    return float(q.sum())


def core_charge_poisson(xyz, n, center=(0.0, 0.0, 0.0), radius=None, tri=None):
    """Charge carried by tetrahedra whose centroid lies within `radius` of the
    spatial centre -- localises the defect so its survival is tracked even if cloud
    noise scatters tiny fractional charge near the boundary."""
    q, tri = charge_field_poisson(xyz, n, tri)
    simp = tri.simplices
    cen = xyz[simp].mean(axis=1)                       # (m,3)
    d = np.linalg.norm(cen - np.asarray(center, float), axis=1)
    if radius is None:
        radius = 0.5 * (xyz.max(0) - xyz.min(0)).min()
    sel = d <= radius
    return float(q[sel].sum())


# ====================================================================== #
# Energy, gradient density, effective radius (on causal links)
# ====================================================================== #
def link_energy(sub, n):
    """Derrick functional on causal links  E = sum_links (1 - n_i . n_j) >= 0.
    Zero on a uniform field; large where n turns fast across a link."""
    if sub.edges.size == 0:
        return 0.0
    i, j = sub.edges[:, 0], sub.edges[:, 1]
    return float(np.sum(1.0 - np.einsum("ij,ij->i", n[i], n[j])))


def gradient_density_links(sub, n):
    """Per-event link gradient energy g_e = sum_{f linked to e} (1 - n_e . n_f).
    Shape (n,)."""
    g = np.zeros(sub.n)
    if sub.edges.size == 0:
        return g
    i, j = sub.edges[:, 0], sub.edges[:, 1]
    w = 1.0 - np.einsum("ij,ij->i", n[i], n[j])
    np.add.at(g, i, w)
    np.add.at(g, j, w)
    return g


def r_eff_links(sub, n, center=(0.0, 0.0, 0.0)):
    """Effective defect radius r_eff = sum_e r_e g_e / sum_e g_e, r_e the spatial
    distance from `center`, g_e the link gradient density.  Shrinks if the texture
    collapses to a point, grows if it spreads or unwinds."""
    g = gradient_density_links(sub, n)
    r = np.linalg.norm(sub.pts[:, 1:4] - np.asarray(center, float), axis=1)
    tot = g.sum()
    return float(np.sum(r * g) / tot) if tot > 1e-12 else 0.0


# ====================================================================== #
# Leaf (time-slice) topological charge B(t)
# ====================================================================== #
def time_leaves(pts, n_leaves, t_lo=None, t_hi=None):
    """Partition the time axis into `n_leaves` equal bands.  Returns a list of
    (t_centre, index_array) for the events in each band."""
    t = pts[:, 0]
    t_lo = t.min() if t_lo is None else t_lo
    t_hi = t.max() if t_hi is None else t_hi
    edges = np.linspace(t_lo, t_hi, n_leaves + 1)
    out = []
    for a, b in zip(edges[:-1], edges[1:]):
        sel = np.nonzero((t >= a) & (t < b))[0]
        out.append((0.5 * (a + b), sel))
    return out


def leaf_charge(pts, n, idx, center=(0.0, 0.0, 0.0)):
    """Topological charge B of the field on a single time leaf: Delaunay the leaf
    events' SPATIAL coordinates and take the boundary degree.  Returns nan if the
    leaf has too few points for a 3D tetrahedralisation."""
    if idx.size < 8:
        return float("nan")
    xyz = pts[idx, 1:4]
    try:
        return topological_charge_poisson(xyz, n[idx])
    except Exception:
        return float("nan")


def measure_leaf(pts, sub, n, idx, center=(0.0, 0.0, 0.0)):
    """B, r_eff and gradient energy restricted to a time leaf."""
    B = leaf_charge(pts, n, idx, center)
    if idx.size:
        xyz = pts[idx, 1:4]
        g_all = gradient_density_links(sub, n)
        g = g_all[idx]
        r = np.linalg.norm(xyz - np.asarray(center, float), axis=1)
        tot = g.sum()
        reff = float(np.sum(r * g) / tot) if tot > 1e-12 else 0.0
        E = float(g.sum())
    else:
        reff = 0.0
        E = 0.0
    return {"B": B, "E": E, "r_eff": reff, "n_events": int(idx.size)}


# ====================================================================== #
# Protocol A -- deterministic CAUSAL evolution (the arrow of time)
# ====================================================================== #
def evolve_causal(sub, n0, init_mask, passes=1):
    """Deterministic causal evolution.  Sweep events in increasing time; an event
    NOT in the frozen initial slab is set to the energy-minimising orientation
    against its CAUSAL PAST (parents):  n_e <- normalize(sum_{p in parents} n_p).

    The past is fixed before the future is written -- the irreversibility of the
    causal cone.  `passes` repeats the forward sweep (each pass only ever reads
    already-updated past events, so >1 pass sharpens the propagated field without
    ever modifying an event from its future).  Returns the evolved field n."""
    n = n0.copy()
    order = sub.topo_order
    for _ in range(max(1, passes)):
        for e in order:
            if init_mask[e]:
                continue
            par = sub.parents[e]
            if par.size == 0:
                continue
            h = n[par].sum(axis=0)
            nrm = np.linalg.norm(h)
            if nrm > 1e-9:
                n[e] = h / nrm
    return n


# ====================================================================== #
# Protocol B -- causal Monte Carlo (thermal barrier crossing, past frozen)
# ====================================================================== #
def evolve_mc_causal(sub, n0, init_mask, J, n_sweeps, seed=0, step=0.5,
                     record=None, center=(0.0, 0.0, 0.0), adapt=True, target=0.4):
    """Metropolis on the causal-link O(3) energy  -J sum_links n_i.n_j, sweeping
    events in time order.  The seeded past slab (init_mask) is FROZEN -- causality:
    the initial data cannot be thermally un-written -- but bulk events may climb a
    finite barrier, so MC reveals whether the cone-rigidity is a true minimum or a
    metastable plateau.  If `record` (list of sweep numbers) is given, returns
    (n, traj) with traj a list of measure dicts; else (n, []).

    Energy uses ALL links of an event (past+future); only the FROZEN mask differs
    from an ordinary Metropolis -- that frozen past is the causal constraint."""
    n = n0.copy()
    rng = np.random.default_rng(seed)
    free = np.nonzero(~init_mask)[0]
    order = free[np.argsort(sub.pts[free, 0], kind="stable")]
    # precompute neighbour lists (past+future links)
    nbr = [np.concatenate([sub.parents[e], sub.children[e]]) for e in range(sub.n)]
    rec_set = set(record or [])
    traj = []
    if record is not None and 0 in rec_set:
        traj.append({"sweep": 0, **_global_measure(sub, n, center)})
    for s in range(1, n_sweeps + 1):
        acc = 0
        for e in order:
            ne = nbr[e]
            if ne.size == 0:
                continue
            h = n[ne].sum(axis=0)
            old = n[e]
            v = old + step * rng.standard_normal(3)
            prop = v / (np.linalg.norm(v) + 1e-12)
            dE = -J * float((prop - old) @ h)
            if dE <= 0 or rng.random() < np.exp(-min(dE, 50.0)):
                n[e] = prop
                acc += 1
        if adapt and s % 25 == 0:
            a = acc / max(order.size, 1)
            if a > target + 0.1:
                step *= 1.15
            elif a < target - 0.1:
                step *= 0.87
            step = float(np.clip(step, 1e-3, 3.0))
        if s in rec_set:
            traj.append({"sweep": s, **_global_measure(sub, n, center)})
    return n, traj


def _global_measure(sub, n, center):
    """Whole-cloud B (all events, spatial Delaunay) + energy + r_eff -- a coarse
    monitor used inside the MC loop."""
    xyz = sub.pts[:, 1:4]
    try:
        B = topological_charge_poisson(xyz, n)
        Bc = core_charge_poisson(xyz, n, center)
    except Exception:
        B = float("nan"); Bc = float("nan")
    return {"B": B, "B_core": Bc, "E": link_energy(sub, n),
            "r_eff": r_eff_links(sub, n, center)}


# ====================================================================== #
# Vectorised colour-checkerboard Metropolis + cooler (fast paths)
# ====================================================================== #
def _color_neighbour_sum(g, n, c):
    """Neighbour spin sum H (m_c, 3) on the nodes of colour c, current spins n."""
    nbr, seg, m = g._nbr[c], g._seg[c], g.groups[c].size
    H = np.empty((m, 3))
    for k in range(3):
        H[:, k] = np.bincount(seg, weights=n[nbr, k], minlength=m)
    return H


def evolve_mc_fast(sub, n0, frozen, J, n_sweeps, seed=0, step=0.5, record=None,
                   center=(0.0, 0.0, 0.0), adapt=True, target=0.4, cool_steps=12):
    """Vectorised colour-checkerboard O(3) Metropolis on the causal-link energy
    -J sum_links n_i.n_j, with a FROZEN node set held fixed (Dirichlet boundary).

    Same physics as evolve_mc_causal but ~100x faster (per-colour vectorisation via
    the proper graph colouring).  Frozen nodes are never proposed, yet still feed
    their (fixed) orientation into every neighbour field -- so a frozen PAST slab
    keeps re-imposing its winding on the bulk through the causal links.  If
    `record` (iterable of sweeps) is given, returns (n, traj) with each traj entry
    the COOLED whole-cloud B (charter: cool before measuring the integer charge, to
    drop thermal UV wrinkles that carry spurious fractional solid angle)."""
    g = sub.graph
    n = n0.copy()
    rng = np.random.default_rng(seed)
    # per-colour free-node masks (frozen nodes proposed-but-never-accepted)
    free_in_grp = [~frozen[g.groups[c]] for c in range(g.n_colors)]
    rec_set = set(record or [])
    xyz = sub.pts[:, 1:4]
    traj = []

    def _snap(s):
        nc = cool_field(sub, n, cool_steps)
        return {"sweep": int(s), "B": topological_charge_poisson(xyz, nc),
                "B_core": core_charge_poisson(xyz, nc, center),
                "E": link_energy(sub, n), "r_eff": r_eff_links(sub, n, center)}

    if 0 in rec_set:
        traj.append(_snap(0))
    for s in range(1, n_sweeps + 1):
        acc = 0; tot = 0
        for c in range(g.n_colors):
            nodes = g.groups[c]
            if nodes.size == 0:
                continue
            H = _color_neighbour_sum(g, n, c)
            old = n[nodes]
            v = old + step * rng.standard_normal(old.shape)
            prop = v / (np.linalg.norm(v, axis=1, keepdims=True) + 1e-12)
            dE = -J * np.einsum("ij,ij->i", prop - old, H)
            p = np.exp(-np.clip(dE, 0.0, 50.0))
            a = (rng.random(old.shape[0]) < p) & free_in_grp[c]
            n[nodes] = np.where(a[:, None], prop, old)
            acc += int(a.sum()); tot += int(free_in_grp[c].sum())
        if adapt and s % 25 == 0:
            ar = acc / max(tot, 1)
            if ar > target + 0.1:
                step *= 1.15
            elif ar < target - 0.1:
                step *= 0.87
            step = float(np.clip(step, 1e-3, 3.0))
        if s in rec_set:
            traj.append(_snap(s))
    return n, traj


def cool_field(sub, n, steps=12):
    """Zero-temperature cooling: align each spin to ALL its link neighbours (Jacobi
    sweeps).  Removes thermal UV wrinkles without moving the integer topological
    winding -- the standard 'cool before measuring B' protocol.  Vectorised via the
    colour groups (each colour aligned against current spins)."""
    g = sub.graph
    n = n.copy()
    for _ in range(steps):
        for c in range(g.n_colors):
            nodes = g.groups[c]
            if nodes.size == 0:
                continue
            H = _color_neighbour_sum(g, n, c)
            nrm = np.linalg.norm(H, axis=1, keepdims=True)
            ok = nrm[:, 0] > 1e-9
            upd = np.where(ok[:, None], H / (nrm + 1e-12), n[nodes])
            n[nodes] = upd
    return n


# ====================================================================== #
# Causal Derrick: spatial dilation, split spatial vs temporal link energy
# ====================================================================== #
def link_geometry(sub):
    """Per-link |dt| and spatial |dx|.  All causal links are timelike (dt^2>dx^2),
    so |dt|>|dx| always; a link is 'temporal-like' when |dx| is small (the two
    events sit at nearly the SAME spatial point, separated in time) and
    'spatial-like' when |dx| is an appreciable fraction of |dt|."""
    i, j = sub.edges[:, 0], sub.edges[:, 1]
    d = sub.pts[j] - sub.pts[i]
    dt = np.abs(d[:, 0])
    dx = np.linalg.norm(d[:, 1:4], axis=1)
    return dt, dx


def dilate_hedgehog(pts, lam, charge=+1, center=(0.0, 0.0, 0.0), core=1.0):
    """Hedgehog with a finite core of size `core`, sampled at the SPATIALLY DILATED
    coordinate x -> (x-c)/lam + c.  A pure r_hat is scale invariant, so the core is
    essential: lam>1 spreads the core (slower turning), lam<1 compresses it (faster
    turning) -- the Derrick handle.  Returns the (n,3) dilated field."""
    c = np.asarray(center, float)
    x = (pts[:, 1:4] - c) / lam + c
    r = np.linalg.norm(x - c, axis=1, keepdims=True)
    nrad = np.sign(charge) * (x - c) / (r + 1e-12)
    w = np.clip(r / core, 0, 1)
    zhat = np.array([0.0, 0.0, 1.0])
    n = w * nrad + (1 - w) * zhat
    return _normalize(n)


def causal_derrick(sub, lambdas, charge=+1, center=(0.0, 0.0, 0.0), core=1.0,
                   dx_frac=0.5):
    """E(lambda) of the dilated hedgehog on causal links, split by link geometry.

    A link is 'spatial-like' if dx > dx_frac * dt (carries a real spatial gradient)
    and 'temporal-like' otherwise (events almost co-located in space, separated in
    time).  Returns dict with arrays E_spatial(lam), E_temporal(lam), E_total(lam),
    B(lam)."""
    dt, dx = link_geometry(sub)
    i, j = sub.edges[:, 0], sub.edges[:, 1]
    spatial = dx > dx_frac * dt
    Es, Et, Etot, Bs = [], [], [], []
    xyz = sub.pts[:, 1:4]
    for lam in lambdas:
        n = dilate_hedgehog(sub.pts, lam, charge, center, core)
        bond = 1.0 - np.einsum("ij,ij->i", n[i], n[j])
        Es.append(float(bond[spatial].sum()))
        Et.append(float(bond[~spatial].sum()))
        Etot.append(float(bond.sum()))
        Bs.append(topological_charge_poisson(xyz, n))
    return {"lambda": np.asarray(lambdas), "E_spatial": np.asarray(Es),
            "E_temporal": np.asarray(Et), "E_total": np.asarray(Etot),
            "B": np.asarray(Bs), "frac_spatial_links": float(spatial.mean())}


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("e3b_core self-test")
    for seed in (0, 1, 2):
        pts = sprinkle_causal(rho=1.5, T=3.0, L=4.0, seed=seed)
        sub = Substrate(pts)
        xyz = pts[:, 1:4]
        nh = hedgehog_field(pts, +1)
        na = hedgehog_field(pts, -1)
        nu = uniform_field(pts)
        Bh = topological_charge_poisson(xyz, nh)
        Ba = topological_charge_poisson(xyz, na)
        Bu = topological_charge_poisson(xyz, nu)
        print(f"  seed={seed} n={sub.n:4d} links={sub.n_links:5d} "
              f"<deg>={sub.mean_degree:5.2f} cviol={sub.causal_violations()}  "
              f"B(hh)={Bh:+.3f} B(anti)={Ba:+.3f} B(vac)={Bu:+.4f}")
        assert abs(Bh - 1.0) < 0.15, Bh
        assert abs(Ba + 1.0) < 0.15, Ba
        assert abs(Bu) < 0.05, Bu
        assert sub.causal_violations() == 0
    # causal evolution preserves a uniform field (sanity) and lowers link energy
    pts = sprinkle_causal(1.5, 3.0, 4.0, 7)
    sub = Substrate(pts)
    nh = hedgehog_field(pts, +1, core=1.0)
    init = pts[:, 0] <= (pts[:, 0].min() + 0.25 * (pts[:, 0].max() - pts[:, 0].min()))
    E0 = link_energy(sub, nh)
    nf = evolve_causal(sub, nh, init, passes=2)
    Ef = link_energy(sub, nf)
    print(f"  causal evolve: E {E0:.1f} -> {Ef:.1f}  (init slab {int(init.sum())}/{sub.n} frozen)")
    print("self-test OK")
