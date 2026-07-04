"""wilson_core.py -- Wilson-loop / plaquette primitives for the BRIDGE/WILSON task.

Independent of R1-R3 and e6-e11; modifies nothing in the main pipeline.  Continues
BRIDGE_COEFFICIENTS.md, whose C4 found that the link action sum_links cos(.) produces
NO Maxwell term F_mn F^mn -- because a single link carries only the local phase
phi = A_mu e^mu.  F_mn = d_mu A_nu - d_nu A_mu needs the phase summed AROUND a loop
(a plaquette).  This module supplies the holonomy machinery; W1 verifies it gives F.

ANTI-CIRCULARITY.  F^2 is never written down.  We compute only the loop phase
W = sum of link phases = closed line integral of A; that W -> F by Stokes is the
content to be VERIFIED (W1) and coarse-grained (W2), not assumed.  No SR/GR dilation
factor, no GM/r, no DEV here.

Conventions: event x = (t, x1, ...), signature (+,-,...).  A_mu(x) is a covariant
covector field (a python callable x->A).  Link phase of p->q is the line integral
    phi = INT_0^1 A_mu(p + s(q-p)) (q-p)^mu ds        (plain component contraction).
"""

from __future__ import annotations

import numpy as np

# Gauss-Legendre nodes/weights on [0,1] (high order -> line integral ~ exact, so the
# only residual in W/area is the finite-loop curvature of F, which -> 0 as area -> 0).
_GL_X, _GL_W = np.polynomial.legendre.leggauss(8)
_GL_X = 0.5 * (_GL_X + 1.0)
_GL_W = 0.5 * _GL_W


def link_phase(A, p, q):
    """phi = INT A_mu dx^mu along the straight link p->q (Gauss-Legendre, ~exact)."""
    p = np.asarray(p, float); q = np.asarray(q, float)
    e = q - p
    s = 0.0
    for xi, wi in zip(_GL_X, _GL_W):
        s += wi * np.dot(A(p + xi * e), e)
    return float(s)


def loop_holonomy(A, verts):
    """Wilson loop W = sum of link phases around the closed polygon verts[0..n-1]."""
    verts = [np.asarray(v, float) for v in verts]
    n = len(verts)
    return float(sum(link_phase(A, verts[a], verts[(a + 1) % n]) for a in range(n)))


def area_bivector(verts):
    """Oriented area bivector Omega^{mu nu} = 1/2 sum_a (Va^mu Vb^nu - Va^nu Vb^mu).

    Translation-invariant for a closed loop.  In 1+1D Omega^{tx} is the signed area.
    """
    verts = [np.asarray(v, float) for v in verts]
    n = len(verts)
    D = verts[0].shape[0]
    Om = np.zeros((D, D))
    for a in range(n):
        Va, Vb = verts[a], verts[(a + 1) % n]
        Om += np.outer(Va, Vb) - np.outer(Vb, Va)
    return 0.5 * Om


def F_from_A(A, x, eps=1e-5):
    """Field tensor F_{mu nu} = d_mu A_nu - d_nu A_mu by central differences.

    Used ONLY as the continuum reference to score W against (it is the thing W must
    reproduce); it is never inserted into any action.
    """
    x = np.asarray(x, float)
    D = x.shape[0]
    dA = np.zeros((D, D))          # dA[mu, nu] = d_mu A_nu
    for mu in range(D):
        xp = x.copy(); xp[mu] += eps
        xm = x.copy(); xm[mu] -= eps
        dA[mu] = (np.asarray(A(xp)) - np.asarray(A(xm))) / (2 * eps)
    return dA - dA.T               # F_{mu nu}


def stokes_W(F, Om):
    """Predicted holonomy for constant F over a loop of area bivector Om: 1/2 F:Om."""
    return 0.5 * float(np.tensordot(F, Om, axes=2))


def F_sq(F):
    """F_{mu nu} F^{mu nu} with signature (+,-,...): raise both indices with eta."""
    D = F.shape[0]
    eta = np.diag([1.0] + [-1.0] * (D - 1))
    Fup = eta @ F @ eta            # F^{mu nu}
    return float(np.tensordot(F, Fup, axes=2))


# --------------------------------------------------------------------------- #
# Causal-loop construction from a sprinkling (genuine causal links)
# --------------------------------------------------------------------------- #
def causal_diamond_loops(pts, max_per_base=6, n_bases=None, rng=None):
    """Yield minimal causal-diamond loops i -> j -> l <- k <- i from a sprinkle.

    For a base event i, its nearest future neighbours (by proper time) are the small
    covering links; two of them j,k that are mutually spacelike, sharing a near
    common future event l, bound a small causal plaquette (loop i,j,l,k).  Small
    loops => area -> 0 => clean Stokes limit.  Returns list of vertex-quadruples.
    """
    pts = np.asarray(pts, float)
    n, D = pts.shape
    idx = np.arange(n)
    if n_bases is not None and n_bases < n:
        rng = rng or np.random.default_rng(0)
        idx = rng.choice(n, size=n_bases, replace=False)
    loops = []
    for i in idx:
        p = pts[i]
        d = pts - p
        dt = d[:, 0]
        dx2 = np.sum(d[:, 1:] ** 2, axis=1)
        s2 = dt * dt - dx2
        fut = np.nonzero((dt > 0) & (s2 > 0))[0]
        if fut.size < 3:
            continue
        order = fut[np.argsort(s2[fut])]            # nearest future first
        near = order[: min(len(order), max_per_base + 2)]
        made = 0
        for a in range(len(near)):
            for b in range(a + 1, len(near)):
                j, k = near[a], near[b]
                djk = pts[k] - pts[j]
                if djk[0] ** 2 - np.sum(djk[1:] ** 2) > 0:
                    continue                         # j,k causally related -> skip
                # nearest common future event l of both j and k
                for l in order:
                    if l == j or l == k:
                        continue
                    dlj = pts[l] - pts[j]; dlk = pts[l] - pts[k]
                    if (dlj[0] > 0 and dlj[0] ** 2 - np.sum(dlj[1:] ** 2) > 0 and
                            dlk[0] > 0 and dlk[0] ** 2 - np.sum(dlk[1:] ** 2) > 0):
                        loops.append((pts[i], pts[j], pts[l], pts[k]))
                        made += 1
                        break
                if made >= max_per_base:
                    break
            if made >= max_per_base:
                break
    return loops
