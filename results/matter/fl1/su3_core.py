"""su3_core.py -- SU(3) engine for the FL1_SU3_FOUNDATION campaign.

Asks whether colour (SU(3)) and a confining defect can emerge from the SAME 3+1D
Poisson causal lattice that already produced SU(2) (the Skyrmion).  Phase A only:
define the field, prove the minimal action is positive semi-definite, and verify
that causal locality is preserved.

WHY A GENUINELY NEW ENGINE.  SU(2) was carried by UNIT QUATERNIONS -- four real
numbers, no complex literal -- because SU(2) ~= S^3 is a real division algebra.
SU(3) has no such shortcut: the faithful minimal carrier is COMPLEX 3x3 matrices
with the eight Gell-Mann generators.  This module therefore does NOT import
su2_core or orientation_core; it owns its own data structures (3x3 complex arrays,
the structure constants f^{abc}, d^{abc}).  It reuses only causal_core, the
substrate primitive shared by every TEIC campaign, so that the SU(3) field is
tested on EXACTLY the causal network that hosted SU(2).

ANTI-CIRCULARITY.  The complex matrices and the constants f,d ARE the definition of
the group SU(3); they are mathematics, not a physics input.  No QCD number ever
enters Phases A-C: no quark mass, no string tension sigma, no measured alpha_s, no
hadron mass.  Such numbers are used ONLY in Phase D for qualitative comparison and
appear ONLY inside blocks labelled "COMPARISON ONLY".  The Skyrme/commutator
operator is never inserted as a fit target -- every gate MEASURES first and checks
the pre-registered prediction afterwards.

Conventions.
  * Generators: the 8 Gell-Mann matrices lambda_a, normalised Tr(lambda_a lambda_b)
    = 2 delta_ab.  An su(3) element ("current") is a Hermitian traceless 3x3 matrix
    X = sum_a phi_a lambda_a; its real coordinate vector is phi_a = (1/2)Tr(X
    lambda_a).  Inner product <X,Y> = (1/2)Tr(X Y) = phi.psi (the Killing form,
    up to scale).
  * Link variable: U = exp(i X) in SU(3) (X Hermitian traceless => U unitary,
    det U = exp(i Tr X) = 1).
  * Wilson plaquette holonomy W = Ua Ub Uc^dag Ud^dag; plaquette action density
    s_p = 1 - (1/3) Re Tr(W) in [0, 2].
  * Currents matrix for the quartic analysis: c_mu (mu = x,y,z) are three su(3)
    elements; M = sum_mu c_mu^2; the Skyrme/commutator invariant is
    K = - sum_{mu,nu} Tr([c_mu,c_nu]^2) >= 0.
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402  (the shared substrate primitive)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

N = 3  # SU(3)
PI = np.pi


# =========================================================================== #
# PART 0 -- the Lie algebra su(3): Gell-Mann generators and structure constants
# =========================================================================== #
def _gell_mann():
    """The 8 Gell-Mann matrices (3x3 complex), Tr(lambda_a lambda_b) = 2 delta_ab."""
    l = np.zeros((8, 3, 3), dtype=complex)
    # SU(3) GROUP-DEF COMPLEX -- the imaginary entries below ARE the definition of
    # the Gell-Mann generators of su(3); they are group theory, not an injected
    # phase/dilation.  (anti-circularity exception, see tests/test_no_circularity.py)
    l[0] = [[0, 1, 0], [1, 0, 0], [0, 0, 0]]
    l[1] = [[0, -1j, 0], [1j, 0, 0], [0, 0, 0]]
    l[2] = [[1, 0, 0], [0, -1, 0], [0, 0, 0]]
    l[3] = [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
    l[4] = [[0, 0, -1j], [0, 0, 0], [1j, 0, 0]]
    l[5] = [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
    l[6] = [[0, 0, 0], [0, 0, -1j], [0, 1j, 0]]
    l[7] = np.array([[1, 0, 0], [0, 1, 0], [0, 0, -2]]) / np.sqrt(3.0)
    # END SU(3) GROUP-DEF COMPLEX
    return l


GELL_MANN = _gell_mann()


def structure_constants():
    """Totally antisymmetric f^{abc} and symmetric d^{abc} from the Gell-Mann basis:
        [l_a, l_b] = 2i f^{abc} l_c ,   {l_a, l_b} = (4/3) delta_ab I + 2 d^{abc} l_c .
    Both extracted by projection f = (1/4i) Tr([l_a,l_b] l_c),
    d = (1/4) Tr({l_a,l_b} l_c).  Returned as (8,8,8) real arrays."""
    l = GELL_MANN
    f = np.zeros((8, 8, 8))
    d = np.zeros((8, 8, 8))
    for a in range(8):
        for b in range(8):
            comm = l[a] @ l[b] - l[b] @ l[a]
            anti = l[a] @ l[b] + l[b] @ l[a]
            for c in range(8):
                # SU(3) GROUP-DEF COMPLEX -- f = (1/4i)Tr([l_a,l_b] l_c) is the
                # projection that DEFINES the structure constants of su(3).
                f[a, b, c] = (np.trace(comm @ l[c]) / (4j)).real
                # END SU(3) GROUP-DEF COMPLEX
                d[a, b, c] = (np.trace(anti @ l[c]) / 4.0).real
    return f, d


def algebra_from_coords(phi):
    """su(3) element X = sum_a phi_a lambda_a from a real 8-vector (or (...,8) array).
    X is Hermitian and traceless by construction."""
    phi = np.asarray(phi, dtype=float)
    return np.tensordot(phi, GELL_MANN, axes=([-1], [0]))


def coords_from_algebra(X):
    """phi_a = (1/2) Tr(X lambda_a) -- the real coordinates of a Hermitian su(3) X."""
    return 0.5 * np.real(np.einsum("...ij,aji->...a", X, GELL_MANN))


# =========================================================================== #
# PART 1 -- the group SU(3): exponential, products, random Haar elements
# =========================================================================== #
def su3_exp(X):
    """U = exp(i X) for a Hermitian (su(3)) matrix X, via eigendecomposition
    (exact, no truncation).  Works on a single 3x3 or a stack (...,3,3)."""
    w, V = np.linalg.eigh(X)                       # X = V diag(w) V^dag
    # SU(3) GROUP-DEF COMPLEX -- exp(i*eigenvalue) IS the Lie-algebra->group
    # exponential map of su(3)->SU(3); it is the group structure, not a phase put in
    # by hand to manufacture the action positivity that Phase A measures.
    phase = np.exp(1j * w)
    # END SU(3) GROUP-DEF COMPLEX
    return (V * phase[..., None, :]) @ np.conjugate(np.swapaxes(V, -1, -2))


def su3_from_coords(phi):
    """Link variable U = exp(i phi_a lambda_a) directly from real coordinates."""
    return su3_exp(algebra_from_coords(phi))


def dagger(U):
    return np.conjugate(np.swapaxes(U, -1, -2))


def su3_random(n, rng):
    """n Haar-distributed SU(3) matrices.  QR of a complex Gaussian gives a Haar
    U(3); the diagonal-phase fix makes it uniform, then dividing by det^{1/3}
    projects onto SU(3).  Returns (n,3,3) complex."""
    # SU(3) GROUP-DEF COMPLEX -- a complex Gaussian is the standard carrier of the
    # Haar measure on U(3)/SU(3); the imaginary part is the group's own geometry.
    Z = (rng.standard_normal((n, 3, 3)) + 1j * rng.standard_normal((n, 3, 3))) / np.sqrt(2.0)
    # END SU(3) GROUP-DEF COMPLEX
    Q, R = np.linalg.qr(Z)
    ph = np.diagonal(R, axis1=-2, axis2=-1)
    ph = ph / np.abs(ph)
    Q = Q * ph[:, None, :]
    det = np.linalg.det(Q)
    Q = Q * (det ** (-1.0 / 3.0))[:, None, None]
    return Q


def su3_defects(n, rng, scale=1.0):
    """n SU(3) matrices drawn near identity at a controllable algebra scale (for
    adversarial action tests that probe the small- and moderate-angle regime where
    the cosine quartic lives).  phi ~ scale * N(0,1)^8."""
    phi = scale * rng.standard_normal((n, 8))
    return su3_from_coords(phi)


def is_su3(U, tol=1e-9):
    """(unitarity_err, det_err) maxima over a stack: |U U^dag - I| and |det U - 1|."""
    eye = np.broadcast_to(np.eye(3), U.shape)
    unit = np.max(np.abs(U @ dagger(U) - eye))
    det = np.max(np.abs(np.linalg.det(U) - 1.0))
    return float(unit), float(det)


# =========================================================================== #
# PART 2 -- Wilson plaquette holonomy and the minimal (Wilson) action
# =========================================================================== #
def plaquette(Ua, Ub, Uc, Ud):
    """Oriented holonomy W = Ua Ub Uc^dag Ud^dag around a plaquette."""
    return Ua @ Ub @ dagger(Uc) @ dagger(Ud)


def wilson_density(W):
    """Plaquette action density s_p = 1 - (1/3) Re Tr(W) in [0, 2].  Positive
    semi-definite: eigenvalues of W in SU(3) lie on the unit circle, so
    Re Tr(W) = sum_k cos(theta_k) <= 3, with equality iff W = I."""
    tr = np.trace(W, axis1=-2, axis2=-1)
    return 1.0 - np.real(tr) / 3.0


def wilson_action(Ws, lam=1.0):
    return lam * float(np.sum(wilson_density(Ws)))


def gauge_transform_plaquette(W, g):
    """Conjugation W -> g W g^dag (the residual action of a site gauge transform on
    a closed loop).  Re Tr(W) -- hence wilson_density -- is invariant."""
    return g @ W @ dagger(g)


# =========================================================================== #
# PART 3 -- chiral currents and the leading quartic invariants (SU(3) Skyrme)
# =========================================================================== #
# c_mu (mu = 0,1,2 ~ x,y,z) are su(3) currents (Hermitian traceless 3x3).  The
# link cosine 1 - (1/3)Re Tr(exp(i a (e.C))) expands as
#     (a^2 / 6) Tr((e.C)^2)  -  (a^4 / 72) Tr((e.C)^4)  + ...
# so the QUADRATIC (sigma) density is +Tr((e.C)^2) >= 0 and the QUARTIC density is
# -Tr((e.C)^4) <= 0 -- the SD4 sign theorem, now for SU(3): Tr of an even power of a
# Hermitian matrix is sum_k lambda_k^{2m} >= 0, group-independently.

def contract_direction(C, e):
    """e.C = sum_mu e_mu c_mu for a unit 3-vector e and currents C (3,3,3)."""
    return np.tensordot(e, C, axes=([0], [0]))


def sigma_density_dir(C, e):
    """Quadratic (sigma) density along link direction e: Tr((e.C)^2) >= 0."""
    X = contract_direction(C, e)
    return float(np.real(np.trace(X @ X)))


def quartic_density_dir(C, e):
    """Net leading quartic density along e (the cosine's 4th term, sign included):
    -Tr((e.C)^4) <= 0.  Returns -Tr(X^4)."""
    X = contract_direction(C, e)
    X2 = X @ X
    return float(-np.real(np.trace(X2 @ X2)))


def skyrme_invariant(C):
    """K = - sum_{mu,nu} Tr([c_mu,c_nu]^2) >= 0 (commutator/Skyrme operator) and
    TrM2 = Tr(M^2), M = sum_mu c_mu^2 (symmetric core-cost invariant)."""
    K = 0.0
    M = np.zeros((3, 3), dtype=complex)
    for mu in range(3):
        M = M + C[mu] @ C[mu]
        for nu in range(3):
            comm = C[mu] @ C[nu] - C[nu] @ C[mu]
            K += -np.real(np.trace(comm @ comm))
    TrM2 = float(np.real(np.trace(M @ M)))
    return float(K), TrM2


def quartic_isotropic_mean_formula(C):
    """Pre-registered identity for the isotropic average of Tr((e.C)^4) over e in S^2:
        <Tr((e.C)^4)>_e = (1/15) (3 TrM2 - K/2),
    derived from <e_mu e_nu e_rho e_sig> = (delta..delta + 2 perms)/15 and
    sum Tr(c_mu c_nu c_mu c_nu) = TrM2 - K/2.  Returns the formula value."""
    K, TrM2 = skyrme_invariant(C)
    return (3.0 * TrM2 - 0.5 * K) / 15.0


def quartic_isotropic_mean_exact(C):
    """The SAME isotropic average computed EXACTLY (no sampling) from the rank-4
    moment <e_a e_b e_c e_d> = (delta_ab delta_cd + delta_ac delta_bd +
    delta_ad delta_bc)/15:
        <Tr((e.C)^4)> = (1/15) sum_{a,b} [Tr(c_a c_a c_b c_b)
                        + Tr(c_a c_b c_a c_b) + Tr(c_a c_b c_b c_a)].
    Used to verify quartic_isotropic_mean_formula to machine precision."""
    s = 0.0
    for a in range(3):
        for b in range(3):
            ca, cb = C[a], C[b]
            s += np.real(np.trace(ca @ ca @ cb @ cb))      # delta_ab delta_cd
            s += np.real(np.trace(ca @ cb @ ca @ cb))      # delta_ac delta_bd
            s += np.real(np.trace(ca @ cb @ cb @ ca))      # delta_ad delta_bc
    return float(s / 15.0)


def random_currents(rng, scale=1.0):
    """Three independent su(3) currents with phi ~ scale * N(0,1)^8 (generic, non-
    Abelian).  Returns C as (3,3,3) complex (axis 0 = mu)."""
    phi = scale * rng.standard_normal((3, 8))
    return algebra_from_coords(phi)


# =========================================================================== #
# PART 4 -- the causal substrate: SU(3) links on the Poisson Hasse diagram
# =========================================================================== #
def causal_links(pts):
    """Covering relations (irreducible causal links) of a 3+1D event set: i -> j iff
    i precedes j (timelike, future-directed) with no k strictly between.  Returns an
    (L,2) int array.  Identical transitive reduction used by SU(2)'s substrate, so
    the SU(3) field sits on EXACTLY the same causal network."""
    t = pts[:, 0]
    dt = t[None, :] - t[:, None]                        # dt[i,j] = t_j - t_i
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=2)
    rel = (dt > 0) & (dt * dt > dx2)                    # i precedes j (timelike)
    relf = rel.astype(np.float32)
    two_step = (relf @ relf) > 0.5                      # exists k: i < k < j
    link = rel & ~two_step
    return np.argwhere(link)


def links_are_causal(pts, links):
    """Fraction of links that are genuine future-directed timelike relations
    (dt > 0 and dt^2 > |dx|^2).  Must be 1.0 for causal locality to hold."""
    i, j = links[:, 0], links[:, 1]
    dt = pts[j, 0] - pts[i, 0]
    dx2 = np.sum((pts[j, 1:] - pts[i, 1:]) ** 2, axis=1)
    causal = (dt > 0) & (dt * dt > dx2)
    return float(np.mean(causal)), causal


def find_diamond_loops(links, max_loops=2000):
    """Smallest closed loops of a CAUSAL SET (Hasse diagram): the 4-element diamond
    i -> j -> l and i -> k -> l with j, k incomparable.  A transitively reduced
    causal order has NO chordal triangles (the chord i->l is a removed transitive
    relation), so the diamond is the natural minimal Wilson plaquette here.  Returns
    up to max_loops quadruples (i,j,k,l); the oriented holonomy is the loop
    i -> j -> l -> k -> i = U_ij U_jl U_kl^dag U_ik^dag."""
    succ = {}
    for a, b in links:
        succ.setdefault(int(a), set()).add(int(b))
    out = []
    for i, s in succ.items():
        s = sorted(s)
        for ji in range(len(s)):
            for ki in range(ji + 1, len(s)):
                j, k = s[ji], s[ki]
                common = succ.get(j, set()) & succ.get(k, set())
                for l in common:
                    out.append((i, j, k, l))
                    if len(out) >= max_loops:
                        return np.array(out, dtype=int)
    return np.array(out, dtype=int) if out else np.zeros((0, 4), dtype=int)


# =========================================================================== #
# PART 5 -- graph substrate (Phase B): cubic anchor + causal Hasse diagram
# =========================================================================== #
# Neutral graph helpers (NO SU(3) here -- pure combinatorics).  Reimplemented
# natively rather than importing orientation_core, so su3_core is a self-contained
# SU(3) engine; only causal_core (the shared substrate primitive) is reused.

class Graph:
    """Undirected graph with the structures the vectorised Metropolis needs:
    CSR adjacency, a greedy proper colouring, and per-colour segment arrays for
    bincount neighbour sums.  A directed children-CSR + time order are attached for
    causal (longest-chain) distances when built from a sprinkling."""

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
        self._segments()

    def _build_csr(self):
        n, e = self.n, self.edges
        deg = np.zeros(n, dtype=np.int64)
        if e.size:
            np.add.at(deg, np.concatenate([e[:, 0], e[:, 1]]), 1)
        self.indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(deg, out=self.indptr[1:])
        self.indices = np.empty(int(self.indptr[-1]), dtype=np.int64)
        cur = self.indptr[:-1].copy()
        for a, b in e:
            self.indices[cur[a]] = b; cur[a] += 1
            self.indices[cur[b]] = a; cur[b] += 1
        self.degree = deg

    def neighbours(self, i):
        return self.indices[self.indptr[i]:self.indptr[i + 1]]

    def _colour(self):
        order = np.argsort(-self.degree, kind="stable")
        colors = np.full(self.n, -1, dtype=np.int64)
        for v in order:
            used = {int(colors[u]) for u in self.neighbours(v) if colors[u] >= 0}
            c = 0
            while c in used:
                c += 1
            colors[v] = c
        self.colors = colors
        self.n_colors = int(colors.max()) + 1 if self.n else 0

    def _segments(self):
        self.groups, self._nbr, self._seg = [], [], []
        for c in range(self.n_colors):
            nodes = np.nonzero(self.colors == c)[0]
            self.groups.append(nodes)
            degs = self.degree[nodes]
            nbr = (np.concatenate([self.neighbours(v) for v in nodes])
                   if nodes.size else np.zeros(0, dtype=np.int64))
            self._nbr.append(nbr.astype(np.int64))
            self._seg.append(np.repeat(np.arange(nodes.size), degs).astype(np.int64))

    def _attach_directed(self, src, dst, tcoord):
        n = self.n
        outdeg = np.bincount(src, minlength=n)
        self.ch_indptr = np.zeros(n + 1, dtype=np.int64)
        np.cumsum(outdeg, out=self.ch_indptr[1:])
        self.ch_indices = np.empty(int(self.ch_indptr[-1]), dtype=np.int64)
        cur = self.ch_indptr[:-1].copy()
        for k in np.argsort(src, kind="stable"):
            a = src[k]; self.ch_indices[cur[a]] = dst[k]; cur[a] += 1
        self.topo_order = np.argsort(tcoord, kind="stable")

    def children(self, i):
        return self.ch_indices[self.ch_indptr[i]:self.ch_indptr[i + 1]]


def lattice_periodic(shape):
    """Periodic hyper-cubic lattice graph (literature anchor)."""
    shape = tuple(int(s) for s in shape)
    n = int(np.prod(shape))
    idx = np.arange(n).reshape(shape)
    edges = [np.stack([idx.ravel(), np.roll(idx, -1, axis=ax).ravel()], axis=1)
             for ax in range(len(shape))]
    g = Graph(n, np.concatenate(edges, axis=0))
    g.shape = shape
    return g


def causal_link_graph(pts):
    """Hasse diagram (covering relations) of a sprinkled 3+1D causal set, as an
    undirected Graph with a directed children-CSR + time order attached for
    longest-chain (causal proper-time) distances.  Same substrate as SU(2)."""
    links = causal_links(pts)
    g = Graph(len(pts), links)
    g.n_links = int(len(links))
    if len(links):
        g._attach_directed(links[:, 0], links[:, 1], pts[:, 0])
    return g


def bfs_distances(graph, source, r_max):
    """Hop distance from source, capped at r_max; -1 beyond reach."""
    from collections import deque
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


def longest_chain_from(graph, source, r_max=None):
    """Longest directed-path (causal proper-time) distance from source to its
    future; -1 for events not in the future.  DAG longest path via time order."""
    n = graph.n
    dist = np.full(n, -1, dtype=np.int64)
    dist[source] = 0
    topo = graph.topo_order
    pos = int(np.nonzero(topo == source)[0][0])
    cap = r_max if r_max is not None else n
    for u in topo[pos:]:
        du = dist[u]
        if du < 0 or du >= cap:
            continue
        for v in graph.children(u):
            if du + 1 > dist[v]:
                dist[v] = du + 1
    return dist


# =========================================================================== #
# PART 6 -- the SU(3) principal-chiral spin model (Phase B Monte Carlo)
# =========================================================================== #
# Site field U_i in SU(3); energy  E = -J sum_{<ij>} (1/3) Re Tr(U_i U_j^dag).
# This is the matrix generalisation of E1's O(3) model E = -J sum n_i.n_j: the
# scalar overlap n_i.n_j is replaced by the SU(3)xSU(3)-invariant (1/3)Re Tr(U_i
# U_j^dag) in [-1/3, 1], = 1 iff U_i = U_j.  KEY IDENTITY: flatten each U into the
# real 18-vector v = (1/sqrt3)[Re(U).ravel(), Im(U).ravel()].  Then v is a UNIT
# 18-vector (v.v = (1/3)Tr(U U^dag) = 1) and v_i . v_j = (1/3) Re Tr(U_i U_j^dag).
# So the model is literally an O(18) Heisenberg model CONSTRAINED to the 8-dim
# SU(3) submanifold of S^17 -- the order parameter m = |mean_i v_i| has the same
# 1/sqrt(N) disordered baseline as O(3), and C(r) plateau = m^2 (Mermin clustering).
# Ordering breaks SU(3)xSU(3) -> diagonal SU(3).

def u_to_vec(U):
    """18-vector v (real) for a stack of SU(3) matrices: v.v = 1, v_i.v_j = overlap."""
    flat = U.reshape(U.shape[:-2] + (9,))
    return np.concatenate([flat.real, flat.imag], axis=-1) / np.sqrt(3.0)


class SU3ChiralModel:
    """Vectorised colour-Metropolis for the SU(3) principal-chiral field.

    Proposal: U_i' = R_i U_i with R_i = exp(i step * phi.lambda), phi ~ N(0,1)^8
    (a random SU(3) rotation near identity at scale `step`).  Local energy change
    dE = -J (v_i' - v_i).H_i, H_i = sum_{j~i} v_j the 18-vector neighbour field
    (segment-summed by colour).  Adaptive step targets ~0.4 acceptance, exactly as
    E1's O(3) updater."""

    def __init__(self, graph, J, seed=0, step=0.4, init=None):
        self.g = graph
        self.J = float(J)
        self.rng = np.random.default_rng(seed)
        self.step = float(step)
        if init == "ordered":
            self.U = np.broadcast_to(np.eye(3, dtype=complex),
                                     (graph.n, 3, 3)).copy()
        else:
            self.U = su3_random(graph.n, self.rng)
        self.v = u_to_vec(self.U)

    def _color_field(self, c):
        nbr, seg, m = self.g._nbr[c], self.g._seg[c], self.g.groups[c].size
        H = np.empty((m, 18))
        for k in range(18):
            H[:, k] = np.bincount(seg, weights=self.v[nbr, k], minlength=m)
        return H

    def _propose_accept(self, c, H):
        nodes = self.g.groups[c]
        m = nodes.size
        phi = self.step * self.rng.standard_normal((m, 8))
        R = su3_from_coords(phi)
        Uprop = R @ self.U[nodes]
        vprop = u_to_vec(Uprop)
        dE = -self.J * np.sum((vprop - self.v[nodes]) * H, axis=1)
        p = np.exp(-np.clip(dE, 0.0, 50.0))            # =1 when dE<=0 (auto-accept)
        acc = self.rng.random(m) < p
        self.U[nodes[acc]] = Uprop[acc]
        self.v[nodes[acc]] = vprop[acc]
        return int(acc.sum())

    def sweep(self):
        acc = 0
        for c in range(self.g.n_colors):
            if self.g.groups[c].size == 0:
                continue
            acc += self._propose_accept(c, self._color_field(c))
        return acc / max(self.g.n, 1)

    def equilibrate(self, n_burn, adapt=True, target=0.4):
        for s in range(n_burn):
            a = self.sweep()
            if adapt and (s + 1) % 25 == 0:
                if a > target + 0.1:
                    self.step *= 1.15
                elif a < target - 0.1:
                    self.step *= 0.87
                self.step = float(np.clip(self.step, 1e-3, 3.0))

    def order_parameter(self):
        """m = |mean_i v_i| = sqrt(Tr(M M^dag)/3), M = mean_i U_i.  In [1/sqrt(N), 1]."""
        return float(np.linalg.norm(self.v.mean(axis=0)))

    def energy_per_link(self):
        """E/(#links) = -J <(1/3)Re Tr(U_i U_j^dag)> over edges (intensive)."""
        e = self.g.edges
        if e.shape[0] == 0:
            return 0.0
        overlap = np.sum(self.v[e[:, 0]] * self.v[e[:, 1]], axis=1)
        return float(-self.J * np.mean(overlap))

    def corr_arrays(self):
        """18 per-node arrays a_k with s_i.s_j = sum_k a_k(i) a_k(j) (the overlap)."""
        return [self.v[:, k] for k in range(18)]


# ---- correlation accumulator (C(r) = <overlap> by graph distance) ----------- #
class CorrelationAccumulator:
    """C(r) = <(1/3)Re Tr(U_0 U_r^dag)> over (source, distance-r) shells & samples."""

    def __init__(self, sources, dist_list, r_max):
        self.sources = sources
        self.dist_list = dist_list
        self.r_max = r_max
        self.sum_c = np.zeros(r_max + 1)
        self.sum_w = np.zeros(r_max + 1)

    def add(self, model):
        arrs = model.corr_arrays()
        for s, dist in zip(self.sources, self.dist_list):
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


def _r2(y, yhat):
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0


def fit_forms(r, C, sigma=None, r_lo=2, floor_abs=0.02):
    """Classify C(r) as 'exp' (disordered, finite xi), 'power' (critical r^-eta), or
    'const' (long-range order, C_long = plateau = m^2).  Same robust plateau+R^2
    classifier as E1 (orientation_core.fit_forms): LRO if the outer-half plateau
    C_long > 0.05 and flat (C_long/C_mid > 0.85); else the straighter of exp/power."""
    FLAT_RATIO, C_LONG_MIN = 0.85, 0.05
    r = np.asarray(r, float); C = np.asarray(C, float)
    ss = None if sigma is None else np.asarray(sigma, float)
    rmax = r.max() if r.size else 0.0
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
    C_mid = float(C[int(np.argmin(np.abs(r - r_mid)))])
    flat_ratio = C_long / C_mid if C_mid > 1e-9 else 0.0
    is_flat = (C_long > C_LONG_MIN) and (flat_ratio > FLAT_RATIO)
    floor = floor_abs
    if ss is not None:
        win0 = (r >= r_lo) & np.isfinite(C)
        if win0.any():
            floor = max(floor_abs, 4.0 * float(np.median(ss[win0])))
    sel = (r >= r_lo) & (C > floor) & np.isfinite(C)
    out = {"n_points": int(sel.sum()), "C_long": C_long, "C_mid": C_mid,
           "flat_ratio": float(flat_ratio)}
    if sel.sum() >= 3:
        rr, cc = r[sel], C[sel]
        logc = np.log(cc)
        be = np.polyfit(rr, logc, 1)
        xi = -1.0 / be[0] if be[0] < 0 else np.inf
        R2_exp = _r2(cc, np.exp(be[1] + be[0] * rr))
        bp = np.polyfit(np.log(rr), logc, 1)
        R2_pow = _r2(cc, np.exp(bp[1] + bp[0] * np.log(rr)))
        out["exp"] = {"xi": float(xi), "R2": R2_exp}
        out["power"] = {"eta": float(-bp[0]), "R2": R2_pow}
    else:
        out["exp"] = {"xi": float("nan"), "R2": float("nan")}
        out["power"] = {"eta": float("nan"), "R2": float("nan")}
        R2_exp = R2_pow = float("nan")
    out["const"] = {"C0": C_long}
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


# =========================================================================== #
# PART 7 -- chiral colour defect (Phase C): the SU(3) Skyrmion + stability
# =========================================================================== #
# Vacuum space of the ordered phase = SU(3)xSU(3)/SU(3)_diag ~= SU(3); a static
# field is a map S^3 -> SU(3) with topological charge B in pi_3(SU(3)) = Z.  The
# B=1 colour Skyrmion is the SU(2) hedgehog embedded in an SU(2) subgroup of SU(3)
# (standard: the minimal SU(3) Skyrmion lives in an SU(2) subgroup; the inclusion
# SU(2)->SU(3) is an isomorphism on pi_3).  Energy = principal-chiral E2 (2-deriv,
# collapses alone by Derrick) + the EXTERNAL Skyrme stabiliser E4 (4-deriv).  E4 is
# added EXPLICITLY and flagged as external: Phase A proved (K <= 6 TrM^2, sign
# theorem) that Skyrme dominance does NOT emerge from the cosine action by itself,
# exactly as for SU(2) -- so a non-cosine core cost is a declared input, not hidden.

def su3_log(U):
    """Anti-Hermitian su(3) logarithm of a stack of SU(3) matrices: U = exp(L),
    L = V diag(i*theta) V^dag with theta in (-pi, pi] the eigenphases.  Pure group
    geometry (the inverse of su3_exp)."""
    w, V = np.linalg.eig(U)
    theta = np.angle(w)                                # eigenphases in (-pi, pi]
    # L = V diag(i theta) V^{-1}; for unitary U, V^{-1} = V^dag up to numerical drift
    Vinv = np.linalg.inv(V)
    # SU(3) GROUP-DEF COMPLEX -- diag(i*theta) is the su(3) logarithm (inverse of the
    # group exponential); structural group geometry, not an injected phase.
    return (V * (1j * theta)[..., None, :]) @ Vinv
    # END SU(3) GROUP-DEF COMPLEX


def project_to_su3(M):
    """Nearest SU(3) matrix to an arbitrary 3x3 (polar/SVD projection): the unitary
    factor of M, with det fixed to 1.  Used after trilinear resampling (dilation)
    and after additive noise, the SU(3) analogue of renormalising a spin to S^2."""
    Uu, _, Vh = np.linalg.svd(M)
    W = Uu @ Vh
    det = np.linalg.det(W)
    return W * (det ** (-1.0 / 3.0))[..., None, None]


def grid_axes(L, half_width=2.5):
    """Cubic coordinate axis in [-half_width, half_width] with L points, spacing dx."""
    x = np.linspace(-half_width, half_width, L)
    return x, float(x[1] - x[0])


def embedded_hedgehog(L, half_width=2.5, profile=None, charge=+1, w_core=0.9):
    """B=1 colour Skyrmion: SU(2) hedgehog U2 = cosF + i sinF (rhat.sigma) embedded
    in the upper-left 2x2 block of SU(3) (lower-right = 1).  profile F(r): default
    F = pi exp(-r/w_core), F(0)=pi, F(inf)->0 (=> B=+1).  charge=-1 flips rhat_z."""
    x, dx = grid_axes(L, half_width)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    rs = np.where(r > 0, r, 1.0)
    rx, ry, rz = X / rs, Y / rs, Z / rs
    rx[r == 0] = ry[r == 0] = rz[r == 0] = 0.0
    if charge < 0:
        rz = -rz
    F = (profile(r) if profile is not None else PI * np.exp(-r / w_core))
    a0 = np.cos(F); s = np.sin(F)
    a1, a2, a3 = s * rx, s * ry, s * rz
    U = np.zeros(X.shape + (3, 3), dtype=complex)
    # SU(3) GROUP-DEF COMPLEX -- the 2x2 block is the SU(2) hedgehog group element
    # U2 = a0 I + i(a1 s1 + a2 s2 + a3 s3) embedded in SU(3); structural, not a phase.
    U[..., 0, 0] = a0 + 1j * a3
    U[..., 0, 1] = a2 + 1j * a1
    U[..., 1, 0] = -a2 + 1j * a1
    U[..., 1, 1] = a0 - 1j * a3
    # END SU(3) GROUP-DEF COMPLEX
    U[..., 2, 2] = 1.0
    return U, dx


def _right_links(U):
    """R_i = U_x^dag U_{x+i} for i = x,y,z (forward periodic difference)."""
    Ud = dagger(U)
    return [Ud @ np.roll(U, -1, axis=ax) for ax in range(3)]


def chiral_energy(U, dx, e_sk):
    """(E2, E4, E_total) of the SU(3) chiral field on the cubic lattice.
        E2 = (2/dx^2) sum_x sum_i [1 - (1/3) Re Tr(U_x^dag U_{x+i})]   (principal chiral)
        E4 = e_sk * sum_x sum_{i<j} -Tr([a_i, a_j]^2),  a_i = su3_log(R_i)/dx  (Skyrme)
    integrated with the volume element dx^3.  E2 >= 0; E4 >= 0 (commutator of anti-
    Hermitian currents).  e_sk is the EXTERNAL Skyrme weight (declared input)."""
    Rs = _right_links(U)
    vol = dx ** 3
    e2 = 0.0
    for R in Rs:
        tr = np.real(np.trace(R, axis1=-2, axis2=-1))
        e2 += np.sum(1.0 - tr / 3.0)
    E2 = (2.0 / dx ** 2) * e2 * vol
    a = [su3_log(R) / dx for R in Rs]                   # su(3) currents
    E4 = 0.0
    if e_sk:
        for i in range(3):
            for j in range(i + 1, 3):
                comm = a[i] @ a[j] - a[j] @ a[i]
                E4 += np.sum(-np.real(np.trace(comm @ comm, axis1=-2, axis2=-1)))
        E4 = e_sk * E4 * vol
    return float(E2), float(E4), float(E2 + E4)


_B_PREF = -1.0 / (24.0 * PI ** 2)   # sign calibrated so F(0)=pi hedgehog -> B=+1


def baryon_number(U, dx):
    """Topological charge B = (1/24pi^2) sum_x eps^{ijk} Tr(a_i a_j a_k) dx^3, with
    a_i = su3_log(R_i)/dx the su(3) currents (the dx^3 cancels the three 1/dx).  The
    Pontryagin index of U: S^3 -> SU(3); integer for a closed configuration.  Sign
    convention calibrated so the F(0)=pi hedgehog returns B=+1 (verified in __main__)."""
    Rs = _right_links(U)
    a = [su3_log(R) for R in Rs]                        # = a_i * dx (dx^3 cancels)
    ax_, ay_, az_ = a
    # eps^{ijk} Tr(a_i a_j a_k) = Tr(a_x[a_y,a_z]) + cyclic = 3 Tr(a_x[a_y,a_z])
    comm = ay_ @ az_ - az_ @ ay_
    dens = 3.0 * np.real(np.trace(ax_ @ comm, axis1=-2, axis2=-1))
    return _B_PREF * float(np.sum(dens))


def dilate_field(U, lam):
    """Scale transform U_lam(x) = U((x-c)/lam + c) by trilinear resampling on the
    cubic grid (coords clamped), re-projected to SU(3).  lam>1 spreads, lam<1
    compresses -- the Derrick dilation, SU(3) analogue of e3_core.dilate."""
    L = U.shape[0]
    c = (L - 1) / 2.0
    g = np.arange(L)
    X, Y, Z = np.meshgrid(g, g, g, indexing="ij")
    src = np.stack([np.clip((X - c) / lam + c, 0, L - 1),
                    np.clip((Y - c) / lam + c, 0, L - 1),
                    np.clip((Z - c) / lam + c, 0, L - 1)], axis=-1)
    i0 = np.floor(src).astype(int)
    i1 = np.minimum(i0 + 1, L - 1)
    f = src - i0
    out = np.zeros_like(U)
    for a, b, cc in [(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                     (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]:
        ii = np.where(a, i1[..., 0], i0[..., 0])
        jj = np.where(b, i1[..., 1], i0[..., 1])
        kk = np.where(cc, i1[..., 2], i0[..., 2])
        wx = f[..., 0] if a else 1 - f[..., 0]
        wy = f[..., 1] if b else 1 - f[..., 1]
        wz = f[..., 2] if cc else 1 - f[..., 2]
        out += (wx * wy * wz)[..., None, None] * U[ii, jj, kk]
    return project_to_su3(out)


def derrick_curve(U, dx, e_sk, lambdas):
    """E2(lam), E4(lam), E_total(lam), B(lam) of the dilated colour Skyrmion.  A
    genuine interior minimum of E_total(lam) (only possible with e_sk>0) proves
    Derrick stability; monotone decrease toward lam->0 (e_sk=0) is collapse."""
    E2s, E4s, Ets, Bs = [], [], [], []
    for lam in lambdas:
        Ul = dilate_field(U, lam)
        E2, E4, Et = chiral_energy(Ul, dx, e_sk)
        E2s.append(E2); E4s.append(E4); Ets.append(Et); Bs.append(baryon_number(Ul, dx))
    return (np.array(E2s), np.array(E4s), np.array(Ets), np.array(Bs))


def add_su3_noise(U, amp, rng):
    """Multiply each site by a random near-identity SU(3) of algebra scale `amp`
    (thermal wrinkles), re-projected.  The E3/E3b thermal robustness perturbation."""
    phi = amp * rng.standard_normal(U.shape[:3] + (8,))
    R = su3_from_coords(phi)
    return project_to_su3(R @ U)


def relax_chiral_flow(U, dx, e_sk, n_steps, rate=0.1, record_every=10):
    """Overdamped gradient flow minimising E2 (analytic principal-chiral staple)
    with the Skyrme term measured alongside: U_x <- project_SU3(U_x + rate * S_x),
    S_x = sum_i (U_{x+i} + U_{x-i}) the neighbour staple (ambient -grad of E2).  Open
    boundaries.  Returns (history of (t, E2, E4, B), final U).  Like e3 relax_gradient;
    the SIZE-stabilising role of E4 is shown by derrick_curve (E2-flow alone shrinks)."""
    U = U.copy()
    hist = []
    E2, E4, _ = chiral_energy(U, dx, e_sk)
    hist.append((0, E2, E4, baryon_number(U, dx)))
    for t in range(1, n_steps + 1):
        S = np.zeros_like(U)
        for ax in range(3):
            S = S + np.roll(U, -1, axis=ax) + np.roll(U, +1, axis=ax)
        U = project_to_su3(U + rate * S)
        if t % record_every == 0 or t == n_steps:
            E2, E4, _ = chiral_energy(U, dx, e_sk)
            hist.append((t, E2, E4, baryon_number(U, dx)))
    return hist, U


# ---- rigorous radial Derrick test (1D), the honest stability arbiter -------- #
# The B=1 colour Skyrmion is the embedded SU(2) hedgehog, so under the hedgehog
# ansatz U = (cos F + i sin F rhat.sigma) (upper-left block) the 3D energy reduces to
# the standard radial functional (reimplemented natively; the embedding justifies the
# SU(2) form -- verified by the lattice B above):
#   E2 = 4pi int r^2 [ F'^2 + 2 sin^2 F / r^2 ] dr
#   E4 = 4pi e_sk int     [ sin^2 F (2 F'^2 + sin^2 F / r^2) ] dr
# Derrick scaling x->x/lam: E2 -> lam E2, E4 -> E4/lam.  e_sk>0 gives an interior
# minimum lam* = sqrt(E4/E2) (STABLE soliton, evading the lattice cutoff artefact);
# e_sk=0 gives E(lam)=lam E2, monotone -> lam->0 (COLLAPSE, Derrick's theorem).

def radial_grid(rmax=10.0, n=600):
    r = np.linspace(0.0, rmax, n + 1)[1:]
    return r, float(r[1] - r[0])


def radial_energy(F, r, dr, e_sk):
    Fp = np.gradient(F, dr)
    s2 = np.sin(F) ** 2
    E2 = 4.0 * PI * float(np.sum(r ** 2 * (Fp ** 2 + 2.0 * s2 / r ** 2)) * dr)
    E4 = 4.0 * PI * e_sk * float(np.sum(s2 * (2.0 * Fp ** 2 + s2 / r ** 2)) * dr)
    return E2, E4


def radial_relax(r, dr, e_sk, maxiter=3000):
    """Minimise E2+E4 with F(0)=pi, F(rmax)=0 fixed (L-BFGS-B over interior nodes).
    Returns (F, E2, E4).  With e_sk>0 the Skyrme term sets a finite size; with
    e_sk=0 the minimiser drives the profile to collapse (E2->0 size->0)."""
    from scipy.optimize import minimize
    F0 = PI * np.exp(-r / (0.25 * r[-1]))
    F0[0] = PI; F0[-1] = 0.0

    def assemble(x):
        F = np.empty_like(F0); F[0] = PI; F[-1] = 0.0; F[1:-1] = x
        return F

    def obj(x):
        F = assemble(x)
        E2, E4 = radial_energy(F, r, dr, e_sk)
        return E2 + E4

    res = minimize(obj, F0[1:-1], method="L-BFGS-B",
                   options={"maxiter": maxiter, "ftol": 1e-13})
    F = assemble(res.x)
    E2, E4 = radial_energy(F, r, dr, e_sk)
    return F, E2, E4


def radial_derrick_curve(F, r, dr, e_sk, lambdas):
    """E(lam) = lam E2 + E4/lam for a profile F (exact Derrick scaling).  Interior
    minimum iff e_sk>0."""
    E2, E4 = radial_energy(F, r, dr, e_sk)
    return np.array([lam * E2 + E4 / lam for lam in lambdas]), E2, E4


# =========================================================================== #
# PART 8 -- gauge sector (Phase C): SU(3) Wilson loops and the static potential
# =========================================================================== #
# Link field U_mu(x) in SU(3) on a periodic 4D lattice; Wilson action
# S = beta sum_plaq [1 - (1/3) Re Tr(W_plaq)] (the minimal action of Phase A).
# Confinement test: the static colour charge-anticharge potential V(r) from
# rectangular Wilson loops W(r,t); V(r) ~ sigma r (linear) = confinement.  beta is
# the bare coupling (scanned, NOT a QCD input); sigma is MEASURED, never inserted.

def gauge_init(L, rng, hot=True):
    """4D link field U[mu, x,y,z,t, 3,3].  hot=random SU(3); cold=identity."""
    shape = (4, L, L, L, L)
    if hot:
        return su3_random(int(np.prod(shape)), rng).reshape(shape + (3, 3))
    eye = np.broadcast_to(np.eye(3, dtype=complex), shape + (3, 3))
    return eye.copy()


def _shift(A, mu, sign):
    """Roll the link/site field by one site in direction mu (sign +1 = forward)."""
    return np.roll(A, -sign, axis=mu)


def staple_sum(U, mu):
    """Sum of the 6 staples around link U_mu(x): A_mu(x) = sum_{nu != mu} [
        U_nu(x) U_mu(x+nu) U_nu(x+mu)^dag                          (upper)
      + U_nu(x-nu)^dag U_mu(x-nu) U_nu(x-nu+mu) ]                  (lower)
    so that Re Tr(U_mu A_mu^dag) = sum of the 6 plaquettes touching the link.  Fully
    vectorised over the lattice with np.roll."""
    Umu = U[mu]
    A = np.zeros_like(Umu)
    for nu in range(4):
        if nu == mu:
            continue
        Unu = U[nu]
        Umu_pnu = _shift(Umu, nu, +1)
        Unu_pmu = _shift(Unu, mu, +1)
        upper = Unu @ Umu_pnu @ dagger(Unu_pmu)
        Unu_mnu = _shift(Unu, nu, -1)
        Umu_mnu = _shift(Umu, nu, -1)
        Unu_mnu_pmu = _shift(Unu_mnu, mu, +1)
        lower = dagger(Unu_mnu) @ Umu_mnu @ Unu_mnu_pmu
        A = A + upper + lower
    return A


def plaquette_average(U):
    """Mean plaquette (1/3)Re Tr(W) over all planes and sites (in [-?,1]); the action
    density is beta*(1 - this)*(#plaquettes)."""
    tot, npl = 0.0, 0
    for mu in range(4):
        for nu in range(mu + 1, 4):
            W = (U[mu] @ _shift(U[nu], mu, +1)
                 @ dagger(_shift(U[mu], nu, +1)) @ dagger(U[nu]))
            tot += np.sum(np.real(np.trace(W, axis1=-2, axis2=-1)) / 3.0)
            npl += U[mu][..., 0, 0].size
    return tot / npl


def gauge_metropolis_sweep(U, beta, rng, step, n_hit=2):
    """One Metropolis sweep over all links (4 directions x 2 parities), proposing
    U_mu' = R U_mu with R a near-identity SU(3) of scale `step`; accept by
    dS = -(beta/3) Re Tr((U_mu' - U_mu) A_mu^dag).  Returns acceptance fraction."""
    L = U.shape[1]
    g = np.arange(L)
    I, J, K, T = np.meshgrid(g, g, g, g, indexing="ij")
    parity = (I + J + K + T) % 2
    acc_tot = cnt_tot = 0
    for mu in range(4):
        A = staple_sum(U, mu)
        for par in (0, 1):
            mask = parity == par
            for _ in range(n_hit):
                Uold = U[mu][mask]
                Amask = A[mask]
                R = su3_from_coords(step * rng.standard_normal((Uold.shape[0], 8)))
                Uprop = R @ Uold
                dtr = np.real(np.trace((Uprop - Uold) @ dagger(Amask),
                                       axis1=-2, axis2=-1))
                dS = -(beta / 3.0) * dtr
                p = np.exp(-np.clip(dS, 0.0, 50.0))
                a = rng.random(Uold.shape[0]) < p
                newblk = np.where(a[:, None, None], Uprop, Uold)
                blk = U[mu][mask]
                blk[a] = newblk[a]
                U[mu][mask] = blk
                acc_tot += int(a.sum()); cnt_tot += a.size
    return acc_tot / max(cnt_tot, 1)


def wilson_loop(U, mu, nu, r, t):
    """Planar rectangular Wilson loop <(1/3)Re Tr> of size r (dir mu) x t (dir nu),
    averaged over all sites.  Built by walking r links in +mu, t in +nu, back."""
    Umu, Unu = U[mu], U[nu]
    # product_{k=0..r-1} U_mu(x + k*mu)
    Pmu = np.broadcast_to(np.eye(3, dtype=complex), Umu.shape).copy()
    for k in range(r):
        Pmu = Pmu @ _roll_n(Umu, mu, k)
    # product_{k=0..t-1} U_nu(x + r*mu + k*nu)
    Pnu = np.broadcast_to(np.eye(3, dtype=complex), Unu.shape).copy()
    base_nu = _roll_n(Unu, mu, r)
    for k in range(t):
        Pnu = Pnu @ _roll_n(base_nu, nu, k)
    # product back along mu at height t: U_mu(x + k*mu + t*nu)^dag (reverse order)
    Pmu_top = np.broadcast_to(np.eye(3, dtype=complex), Umu.shape).copy()
    base_mu_top = _roll_n(Umu, nu, t)
    for k in range(r):
        Pmu_top = Pmu_top @ _roll_n(base_mu_top, mu, k)
    # product back along nu at x: U_nu(x + k*nu)^dag (reverse)
    Pnu_left = np.broadcast_to(np.eye(3, dtype=complex), Unu.shape).copy()
    for k in range(t):
        Pnu_left = Pnu_left @ _roll_n(Unu, nu, k)
    W = Pmu @ Pnu @ dagger(Pmu_top) @ dagger(Pnu_left)
    return float(np.mean(np.real(np.trace(W, axis1=-2, axis2=-1)) / 3.0))


def _roll_n(field, axis, n):
    """field shifted so that entry at x holds the original value at x + n*e_axis."""
    return np.roll(field, -n, axis=axis) if n else field


def measure_wilson_loops(U, r_max, t_max):
    """All space-time Wilson loops W(r,t), averaged over the 3 spatial mu and site.
    Returns dict W[(r,t)] = mean loop value.  t is the (4th) Euclidean-time axis."""
    out = {}
    nu = 3                                              # time direction
    for r in range(1, r_max + 1):
        for t in range(1, t_max + 1):
            vals = [wilson_loop(U, mu, nu, r, t) for mu in range(3)]
            out[(r, t)] = float(np.mean(vals))
    return out


def static_potential(loops, r_max, t_max, w_floor=2e-3):
    """V(r) from the t-decay of the loop tower: W(r,t) ~ exp(-V(r) t), so
    V(r) = slope of -ln W(r,t) vs t.  Fitted over the t-range where W stays above
    w_floor (small loops are reliable, large ones drown in noise) -- far more robust
    than a single large-t ratio.  Returns (r_array, V_array).  Confinement: V(r)
    grows ~linearly with r; Coulomb/deconfined: V(r) flattens."""
    rs, Vs = [], []
    for r in range(1, r_max + 1):
        ts, lw = [], []
        for t in range(1, t_max + 1):
            w = loops.get((r, t))
            if w is not None and w > w_floor:
                ts.append(t); lw.append(-np.log(w))
        if len(ts) >= 2:
            slope = float(np.polyfit(ts, lw, 1)[0])
            rs.append(r); Vs.append(slope)
    return np.array(rs, float), np.array(Vs, float)


def creutz_ratio(loops, r):
    """Creutz ratio chi(r,r) = -ln[W(r,r)W(r-1,r-1)/(W(r-1,r)W(r,r-1))] -> the string
    tension sigma (area-law coefficient) as r grows.  chi>0 = area law = confinement;
    chi->0 = no confinement.  Returns nan if any needed loop is in the noise."""
    try:
        wrr = loops[(r, r)]; wmm = loops[(r - 1, r - 1)]
        wrm = loops[(r, r - 1)]; wmr = loops[(r - 1, r)]
        val = (wrr * wmm) / (wrm * wmr)
        if val <= 0:
            return float("nan")
        return float(-np.log(val))
    except (KeyError, ZeroDivisionError):
        return float("nan")


# =========================================================================== #
# IO
# =========================================================================== #
def seed_stats(values):
    v = np.asarray(values, dtype=float)
    return {"mean": float(np.mean(v)),
            "sem": float(np.std(v, ddof=1) / np.sqrt(len(v))) if len(v) > 1 else 0.0,
            "min": float(np.min(v)), "max": float(np.max(v)),
            "n_seeds": int(len(v))}


def save_json(name, payload, phase="A"):
    payload = dict(payload)
    payload["_meta"] = {
        "campaign": "FL1_SU3_FOUNDATION",
        "phase": phase,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
    }
    path = OUTDIR / name
    path.write_text(json.dumps(payload, indent=2))
    return path


# =========================================================================== #
# smoke tests
# =========================================================================== #
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    print("=" * 70)
    print("su3_core smoke tests")
    print("=" * 70)

    # 1) Gell-Mann normalisation Tr(l_a l_b) = 2 delta_ab -----------------------
    G = np.einsum("aij,bji->ab", GELL_MANN, GELL_MANN).real
    print(f"Tr(l_a l_b) = 2 delta : max err {np.max(np.abs(G - 2*np.eye(8))):.2e}")

    # 2) structure constants: known f_123 = 1, f_458 = sqrt3/2, d_118 = 1/sqrt3 -
    f, d = structure_constants()
    print(f"f_123 = {f[0,1,2]:+.4f} (exp +1)   f_458 = {f[3,4,7]:+.4f} (exp {np.sqrt(3)/2:+.4f})")
    print(f"d_118 = {d[0,0,7]:+.4f} (exp {1/np.sqrt(3):+.4f})  f antisym err "
          f"{np.max(np.abs(f + np.swapaxes(f,0,1))):.1e}")

    # 3) group axioms: random SU(3) is unitary, det 1, closed under product ------
    U = su3_random(2000, rng)
    print(f"random SU(3)    : unit err {is_su3(U)[0]:.2e}  det err {is_su3(U)[1]:.2e}")
    UV = U[:-1] @ U[1:]
    print(f"closure (U V)   : unit err {is_su3(UV)[0]:.2e}  det err {is_su3(UV)[1]:.2e}")

    # 4) Wilson density positivity on random plaquettes --------------------------
    A, B, Cc, D = (su3_random(5000, rng) for _ in range(4))
    W = plaquette(A, B, Cc, D)
    s = wilson_density(W)
    print(f"Wilson density  : min {s.min():+.3e}  max {s.max():.3f}  (>=0 required)")

    # 5) quartic isotropic identity: direct MC average vs formula ----------------
    C = random_currents(rng, scale=0.7)
    e = rng.standard_normal((200000, 3)); e /= np.linalg.norm(e, axis=1, keepdims=True)
    X = np.einsum("ne,eij->nij", e, C)
    X2 = X @ X
    tr4 = np.real(np.einsum("nij,nji->n", X2, X2))
    print(f"<TrX^4> MC = {tr4.mean():.5f}  formula = {quartic_isotropic_mean_formula(C):.5f}")
    Ksk, TrM2 = skyrme_invariant(C)
    print(f"K = {Ksk:.4f}  TrM2 = {TrM2:.4f}  K/TrM2 = {Ksk/TrM2:.4f} (bound 6)")

    # 6) Phase B engine: overlap identity + ordering on a small cubic lattice ----
    Ua = su3_random(500, rng); Ub = su3_random(500, rng)
    va, vb = u_to_vec(Ua), u_to_vec(Ub)
    overlap_vec = np.sum(va * vb, axis=1)
    overlap_tr = np.real(np.einsum("nij,nij->n", Ua, np.conjugate(Ub))) / 3.0
    print(f"v_i.v_j = (1/3)ReTr(U_i U_j^dag): max err "
          f"{np.max(np.abs(overlap_vec - overlap_tr)):.2e}  (self v.v={float(np.sum(va[0]**2)):.4f})")
    g = lattice_periodic((6, 6, 6))
    for J, tag in [(0.2, "hot"), (2.0, "cold")]:
        mdl = SU3ChiralModel(g, J=J, seed=1)
        mdl.equilibrate(400, adapt=True)
        ms = [mdl.order_parameter() for _ in range(60) if not mdl.sweep()] or [mdl.order_parameter()]
        print(f"cubic 6^3 J={J:.1f} ({tag}): m={np.mean(ms):.3f} "
              f"(baseline 1/sqrtN={1/np.sqrt(g.n):.3f})  step={mdl.step:.3f}")

    # 7) Phase C chiral defect: B=+1 for embedded hedgehog, Derrick with/without E4
    print("-" * 70)
    U, dx = embedded_hedgehog(21, half_width=2.6, w_core=0.8)
    B = baryon_number(U, dx)
    Ua, _ = embedded_hedgehog(21, half_width=2.6, w_core=0.8, charge=-1)
    Ba = baryon_number(Ua, dx)
    print(f"colour Skyrmion B = {B:+.4f}  (target +1)   anti: B = {Ba:+.4f}  (target -1)")
    # rigorous radial Derrick: one relaxed profile, stabiliser on vs off.
    r, dr = radial_grid(rmax=10.0, n=600)
    Fsk, E2s, E4s = radial_relax(r, dr, e_sk=0.5)
    lam_star = float(np.sqrt(E4s / E2s))
    lams = np.array([0.1, 0.2, lam_star, 0.6, 1.0, 2.0, 4.0])
    E_on, _, _ = radial_derrick_curve(Fsk, r, dr, 0.5, lams)     # E4 present
    E_off = lams * E2s                                            # E4 = 0 (same F)
    print(f"radial e_sk=0.5: E2={E2s:.1f} E4={E4s:.1f}>0  lam*={lam_star:.2f}  "
          f"M=2sqrt(E2E4)={2*np.sqrt(E2s*E4s):.1f}")
    print(f"  Derrick E4-on : argmin lam={lams[np.argmin(E_on)]:.2f} interior, "
          f"E(lam->0)={0.1*E2s+E4s/0.1:.0f} rises => STABLE")
    print(f"  Derrick E4-off: argmin lam={lams[np.argmin(E_off)]:.2f} (=0.1, ->0) "
          f"=> COLLAPSE (Derrick)")

    # 8) Phase C gauge: plaquette equilibration + a Wilson loop at strong coupling
    print("-" * 70)
    Ug = gauge_init(6, np.random.default_rng(0), hot=True)
    for _ in range(40):
        acc = gauge_metropolis_sweep(Ug, beta=5.0, rng=np.random.default_rng(_), step=0.3)
    P = plaquette_average(Ug)
    w11 = wilson_loop(Ug, 0, 3, 1, 1)
    print(f"gauge 6^4 beta=5.0: <plaq>={P:.3f}  W(1,1)={w11:.3f}  acc={acc:.2f}")
