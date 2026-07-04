"""e6_bd_core.py -- the BD-gauge LORENTZIAN operator (indefinite E^2-B^2 signature).

Built for E6_BD_GAUGE_LORENTZIAN (gate H2 of E6_BD_GAUGE.md). The naive non-compact
Maxwell action S=(1/2) sum_P F_P^2 (E6-1/E6-2) is positive-definite (Euclidean), so its
symbol is minimised at omega~0 -- no photon (E6-2: H2 FAIL). The Lorentzian operator
this module builds carries an INDEFINITE signature: each causal-diamond plaquette is
classified E-type (timelike area bivector, A^{0i}-dominant -> electric) or B-type
(spacelike bivector, A^{ij}-dominant -> magnetic) FROM ITS AREA BIVECTOR, and the two
enter the quadratic form with OPPOSITE signs:

    S_L = sum_P w_P F_P^2 ,   F_P = (d theta)_P ,   w_P ~ (b_P^2 - e_P^2),

so   S_L ~ integral (B^2 - E^2) ~ F_{mu nu} F^{mu nu}   in the continuum, which VANISHES
on the radiation shell omega=|k| (|E|=|B|). The operator is M_L = B^T diag(w) B.

KEY FACT (gauge invariance is automatic, ANY weights). F_P=(d theta)_P is gauge
invariant because d^2=0: a gauge shift theta->theta+G lam has B(G lam)=0 (BG=0 is exactly
the discrete d^2=0). Hence M_L (G lam) = B^T W (B G) lam = 0 for ANY diagonal W, even
indefinite. So the indefinite signature does NOT break gauge invariance -- the central
worry of a Lorentzian construction is structurally answered. H1 is checked numerically
anyway (machine precision).

NO relativistic literal is inserted: the bivector E/B split uses only the embedding
coordinates' time column (the sprinkling's own causal/time direction); c is NOT inserted
-- it is read off as the slope of the symbol's zero crossing in H2.

The same machinery runs on a regular 4D lattice (clean (mu,nu)-plane plaquettes, exact
E/B split) as the mandatory validation that the operator+symbol method recovers ck where
Maxwell is known, isolating any causal-set failure as non-locality rather than method.
"""
from __future__ import annotations

import numpy as np


# ====================================================================== #
# Incidence (B) and node coboundary (G)
# ====================================================================== #
def build_incidence(edges, plaq_links, plaq_signs, n_nodes):
    """B: (P,L) plaquette-incidence (F_P = (B theta)_P); G: (L,N) node coboundary
    (theta -> theta + G lam is the gauge shift). G[l,a]=-1, G[l,b]=+1 for link a<b."""
    L = edges.shape[0]
    P = plaq_links.shape[0]
    B = np.zeros((P, L))
    for p in range(P):
        for j in range(4):
            B[p, plaq_links[p, j]] += plaq_signs[p, j]
    G = np.zeros((L, n_nodes))
    for l, (a, b) in enumerate(edges):
        G[l, a] -= 1.0
        G[l, b] += 1.0
    return B, G


# ====================================================================== #
# Plaquette vertices (cyclic) from the signed link list
# ====================================================================== #
def plaquette_vertices(edges, plaq_links, plaq_signs):
    """Recover the 4 vertices of each plaquette in cyclic order from its signed links.

    Each link l stores the undirected pair (lo,hi)=edges[l]. The plaquette's j-th link
    with sign s is traversed lo->hi if s>0 else hi->lo; the four directed steps chain
    into a closed cycle v0->v1->v2->v3->v0. We return the ordered head vertices, which
    are a valid cyclic ordering for the polygon area bivector. Orientation independent
    of the (arbitrary) starting link only up to a global +/- of the bivector, which does
    not affect the E/B classification (it uses squares of bivector components)."""
    P = plaq_links.shape[0]
    verts = np.zeros((P, 4), dtype=np.int64)
    for p in range(P):
        for j in range(4):
            lo, hi = edges[plaq_links[p, j]]
            head = hi if plaq_signs[p, j] > 0 else lo
            verts[p, j] = head
    return verts


# ====================================================================== #
# Area bivector and the electric/magnetic (Minkowski) split
# ====================================================================== #
def plaquette_bivectors(pts, plaq_verts):
    """Oriented area bivector A^{mu nu} = 1/2 sum_c (x_c ^ x_{c+1}) of each plaquette
    (cyclic over its 4 vertices); translation-invariant. pts has the time column first
    (signature -+++). Returns:
      A     : (P, D, D) antisymmetric bivectors,
      e2    : (P,) electric content  sum_i (A^{0i})^2  (time-space components),
      b2    : (P,) magnetic content  sum_{i<j} (A^{ij})^2  (space-space components).
    The Minkowski self-norm of the bivector is proportional to (b2 - e2): timelike
    (electric) bivectors have b2<e2, spacelike (magnetic) have b2>e2."""
    X = np.asarray(pts, float)[plaq_verts]          # (P,4,D)
    P, _, D = X.shape
    A = np.zeros((P, D, D))
    for c in range(4):
        xa = X[:, c, :]
        xb = X[:, (c + 1) % 4, :]
        A += 0.5 * (xa[:, :, None] * xb[:, None, :] - xa[:, None, :] * xb[:, :, None])
    e2 = np.sum(A[:, 0, 1:] ** 2, axis=1)           # A^{0i}, i=1..D-1
    iu = np.triu_indices(D - 1, k=1)
    sub = A[:, 1:, 1:]
    b2 = np.sum(sub[:, iu[0], iu[1]] ** 2, axis=1)  # A^{ij}, 1<=i<j
    return A, e2, b2


def lorentzian_weights(e2, b2, mode="norm", eps=1e-12):
    """Indefinite plaquette weights for S_L = sum_P w_P F_P^2.
      mode='norm'  : w_P = (b2-e2)/(b2+e2)  in [-1,1] -- normalised Minkowski signature
                     of the area bivector (Lorentz-natural, bounded; the principal op).
      mode='sharp' : w_P = +1 if b2>e2 (B-type) else -1 (E-type) -- hard E/B split.
      mode='raw'   : w_P = (b2-e2)               -- unnormalised (over-weights big cells).
      mode='euclid': w_P = +1                     -- the E6-2 naive action (control)."""
    e2 = np.asarray(e2, float); b2 = np.asarray(b2, float)
    if mode == "norm":
        return (b2 - e2) / (b2 + e2 + eps)
    if mode == "sharp":
        return np.where(b2 > e2, 1.0, -1.0)
    if mode == "raw":
        return b2 - e2
    if mode == "euclid":
        return np.ones_like(e2)
    raise ValueError(f"unknown mode {mode}")


def build_operator(edges, plaq_links, plaq_signs, pts, n_nodes, mode="norm"):
    """Assemble the BD-gauge operator M_L = B^T diag(w) B with Lorentzian weights.
    Returns (M_L, B, G, w, e2, b2)."""
    B, G = build_incidence(edges, plaq_links, plaq_signs, n_nodes)
    verts = plaquette_vertices(edges, plaq_links, plaq_signs)
    _, e2, b2 = plaquette_bivectors(pts, verts)
    w = lorentzian_weights(e2, b2, mode=mode)
    M_L = B.T @ (w[:, None] * B)
    return M_L, B, G, w, e2, b2


# ====================================================================== #
# Plane-wave 1-form probe and the operator symbol
# ====================================================================== #
def transverse_pols(kdir):
    """Two spatial unit vectors orthogonal to spatial kdir (3D)."""
    k = np.asarray(kdir, float)
    k = k / (np.linalg.norm(k) + 1e-12)
    a = np.array([1.0, 0, 0]) if abs(k[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = a - k * (a @ k); e1 /= np.linalg.norm(e1) + 1e-12
    e2 = np.cross(k, e1)
    return e1, e2


def plane_wave_theta(edges, pts, kvec, omega, eps_spatial):
    """theta_l = (eps . dx_space) cos(k . xmid_space - omega tmid), eps spatial. The
    natural line integral A_mu dx^mu of a transverse spatial plane wave; no metric
    inserted. (Identical convention to E6-2 so the comparison is apples-to-apples.)"""
    a = edges[:, 0]; b = edges[:, 1]
    dx = pts[b, 1:] - pts[a, 1:]
    xmid = 0.5 * (pts[a, 1:] + pts[b, 1:])
    tmid = 0.5 * (pts[a, 0] + pts[b, 0])
    amp = dx @ eps_spatial
    phase = xmid @ kvec - omega * tmid
    return amp * np.cos(phase)


def symbol(M, theta):
    d = float(theta @ theta)
    return float(theta @ (M @ theta) / d) if d > 0 else np.nan


def zero_crossing(omegas, lam):
    """First sign change of lam(omega) from + to - (or - to +) by linear interpolation.
    The indefinite symbol crosses zero on the light cone (B^2=E^2); we return the omega
    of the first crossing, or nan if lam keeps one sign over the scan."""
    lam = np.asarray(lam, float); om = np.asarray(omegas, float)
    s = np.sign(lam)
    idx = np.nonzero(s[:-1] * s[1:] < 0)[0]
    if idx.size == 0:
        return np.nan
    i = idx[0]
    l0, l1 = lam[i], lam[i + 1]
    o0, o1 = om[i], om[i + 1]
    return float(o0 + (o1 - o0) * (-l0) / (l1 - l0 + 1e-30))
