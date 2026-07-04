"""pi1_core.py -- the Pontryagin-Thom Z2 invariant of loops of Skyrme fields.

MATTER_PI1_B2 campaign (charter: MATTER_PI1_B2.md, pre-registered before any
run). Continues MATTER_FR_EXCHANGE: converts the imported homotopy step
(exchange ~ 2pi-rotation in pi_1 of the B=2 configuration space; Williams 1970)
into a MEASUREMENT.

THE INVARIANT. A based loop U_s(x) of B-sector fields (vacuum at infinity)
defines a map of the 4D domain (s, x) -> S^3. pi_1(Maps_B) = pi_4(S^3) = Z2
(imported, textbook: Pontryagin; Whitehead), and the complete invariant is
Pontryagin-Thom: the preimage of a regular value y in S^3 is a closed framed
1-manifold in 4D (framing = pullback of a basis of T_y S^3 by the
differential); in 4D circles neither knot nor link, so the class is the TOTAL
FRAMING TWIST PARITY (pi_1(SO(3)) = Z2), summed over components, relative to
the constant-frame reference (validated by the PI0 gate: contractible loops
must measure 0).

IMPLEMENTATION. The 4D grid (s periodic) is cut into Kuhn-Freudenthal
4-simplices (24 per hypercube); on each simplex the field is interpolated
affinely; the preimage of the ray {t*y} is a segment (5 eqs, 6 unknowns,
1D kernel); segments chain across shared tetrahedral faces into closed
curves; each segment carries the exact affine differential, from which the
actual framing is solved; the twist is lifted continuously through SO(3)
(quaternion lift, sign-continuity) and the endpoint sign gives the parity.

Engineering checks (pre-registered): all chains must CLOSE; no preimage cell
on the spatial boundary; consecutive frame rotations < 90 deg; class stable
across 3 regular values and (gate) one grid refinement.

ANTI-CIRCULARITY: no SR/GR formula, no quantum phase; pure real quaternion
arithmetic (su2_core) and topology. Nothing here feeds R1-R3.
"""

from __future__ import annotations

import itertools
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "fr_exchange"))
import su2_core as s2          # noqa: E402
import fr_core as fc           # noqa: E402

OUT = Path(__file__).resolve().parent

# ---- pre-registered parameters (MATTER_PI1_B2.md) ---------------------------
REGULAR_VALUES = [
    np.array([0.05, 0.70, -0.50, 0.50]),
    np.array([-0.20, 0.40, 0.65, -0.55]),
    np.array([0.10, -0.60, 0.45, 0.60]),
]
REGULAR_VALUES = [y / np.linalg.norm(y) for y in REGULAR_VALUES]
SLERP_MAX_DIST = 0.5          # closing segment valid only below this
FRAME_DOT_MIN = np.sqrt(0.5)  # consecutive frame quaternion dot (90 deg)
FILTER_SAFETY = 1.5

# fixed generic constant vectors for the reference framing
_REF = np.array([[0.213, -0.842, 0.391, 0.302],
                 [0.516, 0.297, -0.331, 0.732],
                 [-0.644, 0.118, 0.605, 0.456]])


# =========================================================================== #
# Field loops (analytic; fr_core profile F = pi exp(-r/2))
# =========================================================================== #
def spatial_grid(L, N):
    x = np.linspace(-L / 2, L / 2, N)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    return X, Y, Z, float(x[1] - x[0])


def hedgehog(X, Y, Z, center=(0.0, 0.0, 0.0)):
    return fc.hedgehog_at(X, Y, Z, center)


def hedgehog_rotz(X, Y, Z, center, theta):
    """U0 rotated spatially by theta about the z-axis THROUGH ITS OWN CENTER:
    U(x) = U0(R(-theta)(x - c) + c - c) evaluated at rotated relative coords."""
    cx, cy, cz = center
    Xr, Yr = X - cx, Y - cy
    c, s = np.cos(theta), np.sin(theta)
    Xq = c * Xr + s * Yr          # R(-theta) applied to relative coords
    Yq = -s * Xr + c * Yr
    return fc.hedgehog_at(Xq + cx, Yq + cy, Z, (cx, cy, cz))


def q_slerp(U1, U0, t):
    """Pointwise geodesic U1 * (U1^{-1} U0)^t on S^3 (valid: nowhere antipodal)."""
    w = s2.q_normalize(s2.q_mul(s2.q_conj(U1), U0))
    a0 = np.clip(w[..., 0], -1.0, 1.0)
    ang = np.arccos(a0)
    nv = np.linalg.norm(w[..., 1:], axis=-1)
    axis = np.where(nv[..., None] > 1e-14, w[..., 1:] / np.maximum(nv, 1e-300)[..., None], 0.0)
    wt = np.empty_like(w)
    wt[..., 0] = np.cos(t * ang)
    wt[..., 1:] = np.sin(t * ang)[..., None] * axis
    return s2.q_mul(U1, wt)


def loop_constant(X, Y, Z, n_s):
    U0 = hedgehog(X, Y, Z)
    return np.broadcast_to(U0, (n_s,) + U0.shape).copy()


def loop_translation(X, Y, Z, n_s, radius=1.0):
    """Center moves on a circle through the origin (based, exactly closed,
    contractible: shrink the radius)."""
    out = np.empty((n_s,) + X.shape + (4,))
    for k, t in enumerate(np.linspace(0.0, 1.0, n_s, endpoint=False)):
        c = (radius * (1.0 - np.cos(2 * np.pi * t)), radius * np.sin(2 * np.pi * t), 0.0)
        out[k] = hedgehog(X, Y, Z, c)
    return out


def loop_rotation_b1(X, Y, Z, n_s, turns=1):
    """U0(R_z(2 pi turns s) x): exactly closed each turn."""
    out = np.empty((n_s,) + X.shape + (4,))
    for k, t in enumerate(np.linspace(0.0, 1.0, n_s, endpoint=False)):
        out[k] = hedgehog_rotz(X, Y, Z, (0.0, 0.0, 0.0), 2 * np.pi * turns * t)
    return out


def pair_field(X, Y, Z, c1, c2):
    return s2.q_mul(hedgehog(X, Y, Z, c1), hedgehog(X, Y, Z, c2))


def loop_rotation_one_b2(X, Y, Z, n_s, d=6.0, turns=1):
    """Soliton 1 (at +d/2 x) rotates 2 pi turns about z through its center;
    soliton 2 fixed. Exactly closed."""
    c1, c2 = (d / 2, 0.0, 0.0), (-d / 2, 0.0, 0.0)
    out = np.empty((n_s,) + X.shape + (4,))
    for k, t in enumerate(np.linspace(0.0, 1.0, n_s, endpoint=False)):
        U1 = hedgehog_rotz(X, Y, Z, c1, 2 * np.pi * turns * t)
        out[k] = s2.q_mul(U1, hedgehog(X, Y, Z, c2))
    return out


def loop_rotation_pair_b2(X, Y, Z, n_s, d=6.0):
    """The WHOLE pair field rotated rigidly by 2 pi about the z-axis through
    the midpoint (centers orbit; exactly closed at s=1)."""
    c10, c20 = (d / 2, 0.0, 0.0), (-d / 2, 0.0, 0.0)
    out = np.empty((n_s,) + X.shape + (4,))
    for k, t in enumerate(np.linspace(0.0, 1.0, n_s, endpoint=False)):
        th = 2 * np.pi * t
        cs, sn = np.cos(th), np.sin(th)
        Xq = cs * X + sn * Y
        Yq = -sn * X + cs * Y
        out[k] = pair_field(Xq, Yq, Z, c10, c20)
    return out


def loop_exchange_b2(X, Y, Z, n_path, n_close, d=6.0, traversals=1):
    """FR1 exchange path (centers half-turn about midpoint, orientations
    fixed) + slerp closing segment U(1) -> U(0). Returns (loop, closure_max)."""
    base = pair_field(X, Y, Z, (d / 2, 0.0, 0.0), (-d / 2, 0.0, 0.0))
    frames = []
    for _ in range(traversals):
        for t in np.linspace(0.0, 1.0, n_path, endpoint=False):
            ang = np.pi * t
            c1 = (0.5 * d * np.cos(ang), 0.5 * d * np.sin(ang), 0.0)
            c2 = (-c1[0], -c1[1], 0.0)
            frames.append(pair_field(X, Y, Z, c1, c2))
        # end of one traversal: swapped product; close back to base by slerp
        end = pair_field(X, Y, Z, (-d / 2, 0.0, 0.0), (d / 2, 0.0, 0.0))
        closure = float(np.max(np.sqrt(np.sum((end - base) ** 2, axis=-1))))
        for t in np.linspace(0.0, 1.0, n_close, endpoint=False):
            frames.append(q_slerp(end, base, t))
    return np.stack(frames), closure


def axial_b2(X, Y, Z):
    """Axially-symmetric B=2 field: U = (cos F(r), sin F(r) nhat(theta, 2 phi)),
    nhat = (sin th cos 2phi, sin th sin 2phi, cos th) -- the doubled-azimuth
    degree-2 map. Smooth on the axis (sin th = 0 kills the 2phi ambiguity)."""
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    rs = np.where(r > 0, r, 1.0)
    F = np.pi * np.exp(-r / fc.PROFILE_W)
    cth = Z / rs
    sth = np.sqrt(np.maximum(1.0 - cth ** 2, 0.0))
    phi = np.arctan2(Y, X)
    U = np.empty(X.shape + (4,))
    U[..., 0] = np.cos(F)
    sF = np.sin(F)
    U[..., 1] = sF * sth * np.cos(2 * phi)
    U[..., 2] = sF * sth * np.sin(2 * phi)
    U[..., 3] = sF * cth
    U[r == 0, 1:] = 0.0
    U[r == 0, 0] = np.cos(np.pi)
    return s2.q_normalize(U)


def axial_bn(X, Y, Z, n):
    """Axially-symmetric degree-n field: U = (cos F(r), sin F(r) nhat(th, n phi)),
    nhat = (sin th cos n phi, sin th sin n phi, cos th). Generalises axial_b2
    (n=2). Baryon number = n; smooth on the axis (sin th = 0 kills the n phi
    ambiguity). Added for FQ2 (FQ2_PI1_B3_CALIBRATOR.md); axial_b2 untouched."""
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    rs = np.where(r > 0, r, 1.0)
    F = np.pi * np.exp(-r / fc.PROFILE_W)
    cth = Z / rs
    sth = np.sqrt(np.maximum(1.0 - cth ** 2, 0.0))
    phi = np.arctan2(Y, X)
    U = np.empty(X.shape + (4,))
    U[..., 0] = np.cos(F)
    sF = np.sin(F)
    U[..., 1] = sF * sth * np.cos(n * phi)
    U[..., 2] = sF * sth * np.sin(n * phi)
    U[..., 3] = sF * cth
    U[r == 0, 1:] = 0.0
    U[r == 0, 0] = np.cos(np.pi)
    return s2.q_normalize(U)


def preimage_windings(segments, ns, match_tol=1e-5):
    """Per-component s-winding number of the preimage curves. Reuses the
    mutual-nearest-neighbour endpoint matching of chain_components (cKDTree on
    the periodic-s R^5 embedding), then walks each closed component summing the
    signed s-step with periodic unwrapping; winding = round(sum / ns).

    Returns a list of integer windings (one per component). The FQ2 gate
    (FQ2_PI1_B3_CALIBRATOR.md) requires one component of winding 3 for the
    B=3 triple-cover calibrator. Additive; does not touch chain_components."""
    from scipy.spatial import cKDTree
    n = len(segments)
    if n == 0:
        return []
    pts = np.empty((2 * n, 5))
    s_of = np.empty(2 * n)
    for sid, seg in enumerate(segments):
        pts[2 * sid] = _embed(seg["p0"], ns)
        pts[2 * sid + 1] = _embed(seg["p1"], ns)
        s_of[2 * sid] = seg["p0"][0]
        s_of[2 * sid + 1] = seg["p1"][0]
    tree = cKDTree(pts)
    dist, idx = tree.query(pts, k=4)
    nearest = np.full(2 * n, -1, dtype=int)
    for e in range(2 * n):
        for j in range(4):
            cand = int(idx[e, j])
            if cand == e or cand // 2 == e // 2:
                continue
            if dist[e, j] < match_tol:
                nearest[e] = cand
            break
    partner = np.full(2 * n, -1, dtype=int)
    for e in range(2 * n):
        m = nearest[e]
        if m >= 0 and nearest[m] == e:
            partner[e] = m

    def wrap(d):
        if d > ns / 2.0:
            d -= ns
        elif d < -ns / 2.0:
            d += ns
        return d

    windings = []
    used = set()
    for sid0 in range(n):
        if sid0 in used:
            continue
        start = 2 * sid0
        e = start
        s_cur = s_of[e]
        total = 0.0
        broken = False
        while True:
            other = e ^ 1                       # cross the segment
            total += wrap(s_of[other] - s_cur)
            s_cur = s_of[other]
            used.add(other // 2)
            nxt = partner[other]                # hop to the mated endpoint
            if nxt < 0:
                broken = True
                break
            total += wrap(s_of[nxt] - s_cur)
            s_cur = s_of[nxt]
            if nxt == start:
                break
            e = nxt
        windings.append(None if broken else int(round(total / ns)))
    return windings


def loop_target_rotation(W, n_s):
    """U_s = q(s) W q(s)^dag with q(s) = (cos pi s, 0, 0, sin pi s): the global
    target (isospin) 2pi-rotation loop, exactly closed (q(1) = -1 acts
    trivially by conjugation). For a degree-B field the class is B mod 2
    (precomposition multiplies the suspended Hopf class by the degree)."""
    out = np.empty((n_s,) + W.shape)
    for k, t in enumerate(np.linspace(0.0, 1.0, n_s, endpoint=False)):
        q = np.zeros(W.shape[:-1] + (4,))
        q[..., 0] = np.cos(np.pi * t)
        q[..., 3] = np.sin(np.pi * t)
        out[k] = s2.q_mul(s2.q_mul(q, W), s2.q_conj(q))
    return out


# =========================================================================== #
# Pontryagin-Thom machinery
# =========================================================================== #
_PERMS = list(itertools.permutations(range(4)))   # 24 Kuhn simplices / cube


def _candidate_cells(V, y):
    """Boolean mask over 4-cells: min corner |V - y| <= safety * sum of
    per-axis max edge jumps in the cell (Lipschitz bound; misses are caught
    by the chain-closure check)."""
    D = np.sqrt(np.sum((V - y) ** 2, axis=-1))          # (ns, nx, ny, nz)

    def cellify(A, off):
        """Restrict shifted array to the cell grid (ns, nx-1, ny-1, nz-1)."""
        B = np.roll(A, -off[0], axis=0)
        sl = tuple(slice(o, B.shape[1 + i] - 1 + o) for i, o in enumerate(off[1:]))
        return B[(slice(None),) + sl]

    corners = list(itertools.product((0, 1), repeat=4))
    Dmin = None
    for off in corners:
        c = cellify(D, off)
        Dmin = c if Dmin is None else np.minimum(Dmin, c)

    jump = 0.0
    for ax in range(4):
        dV = np.sqrt(np.sum((np.roll(V, -1, axis=0) - V) ** 2, axis=-1)) if ax == 0 \
            else np.sqrt(np.sum((np.diff(V, axis=ax)) ** 2, axis=-1))
        # max of this axis's edges over the cell
        Jmax = None
        for off in corners:
            if off[ax] == 1:
                continue                                  # edge starts at off[ax]=0
            if ax == 0:
                c = cellify(dV, off)
            else:
                # dV already shorter along ax; treat as field on edge grid
                off2 = list(off)
                B = np.roll(dV, -off2[0], axis=0)
                sl = []
                for i, o in enumerate(off2[1:]):
                    n_edge = B.shape[1 + i]
                    n_cell = V.shape[1 + i] - 1
                    if i == ax - 1:
                        sl.append(slice(0, n_cell))       # one edge per cell along ax
                    else:
                        sl.append(slice(o, n_cell + o))
                c = B[(slice(None),) + tuple(sl)]
            Jmax = c if Jmax is None else np.maximum(Jmax, c)
        jump = jump + Jmax
    return Dmin <= FILTER_SAFETY * jump


def _simplex_segment(P, V, y):
    """Preimage of the ray {t y, t>0} in one affine 4-simplex.

    P: (5,4) vertex domain coords; V: (5,4) vertex values.
    Solve sum b_i V_i = t y, sum b_i = 1, b_i >= 0, t > 0.
    Returns (p_start, p_end, A_lin, t_mid) or None.
    """
    M = np.zeros((5, 6))
    M[:4, :5] = V.T
    M[:4, 5] = -y
    M[4, :5] = 1.0
    rhs = np.array([0.0, 0.0, 0.0, 0.0, 1.0])
    # particular + null direction
    zp, *_ = np.linalg.lstsq(M, rhs, rcond=None)
    _, sing, Vt = np.linalg.svd(M)
    if sing[-1] > 1e-9 * sing[0]:
        null = Vt[-1]
    else:
        return None                                       # degenerate simplex
    # residual check (system must be consistent)
    if np.linalg.norm(M @ zp - rhs) > 1e-8:
        return None
    lo, hi = -np.inf, np.inf
    for i in range(5):                                    # b_i >= 0
        a, b = zp[i], null[i]
        if abs(b) < 1e-14:
            if a < -1e-12:
                return None
            continue
        bound = -a / b
        if b > 0:
            lo = max(lo, bound)
        else:
            hi = min(hi, bound)
    # t > 0
    a, b = zp[5], null[5]
    if abs(b) < 1e-14:
        if a <= 0:
            return None
    else:
        bound = -a / b
        if b > 0:
            lo = max(lo, bound)
        else:
            hi = min(hi, bound)
    if not (lo < hi - 1e-12):
        return None
    z0, z1 = zp + lo * null, zp + hi * null
    p0 = z0[:5] @ P
    p1 = z1[:5] @ P
    if np.linalg.norm(p1 - p0) < 1e-12:
        return None
    # affine differential dU/dp on the simplex
    Ep = (P[1:] - P[0]).T                                 # 4x4
    Ev = (V[1:] - V[0]).T
    try:
        A = Ev @ np.linalg.inv(Ep)
    except np.linalg.LinAlgError:
        return None
    t_mid = 0.5 * (z0[5] + z1[5])
    return p0, p1, A, t_mid


def extract_preimage(Vfield, y):
    """All preimage segments of the loop field Vfield (ns, nx, ny, nz, 4).

    Domain coords are index coords (s, i, j, k); s is periodic with period ns.
    Returns (segments, boundary_touch). Each segment: dict with p0, p1, A, t.
    """
    ns = Vfield.shape[0]
    mask = _candidate_cells(Vfield, y)
    cells = np.argwhere(mask)
    corners = list(itertools.product((0, 1), repeat=4))
    segments = []
    boundary_touch = False
    nx, ny, nz = Vfield.shape[1] - 1, Vfield.shape[2] - 1, Vfield.shape[3] - 1
    for (cs, ci, cj, ck) in cells:
        # gather the 16 corner values once
        cv = {}
        for off in corners:
            s_idx = (cs + off[0]) % ns
            cv[off] = Vfield[s_idx, ci + off[1], cj + off[2], ck + off[3]]
        for perm in _PERMS:
            offs = [np.zeros(4, dtype=int)]
            for ax in perm:
                offs.append(offs[-1] + np.eye(4, dtype=int)[ax])
            P = np.array([[cs, ci, cj, ck]] * 5, dtype=float) + np.array(offs)
            V = np.array([cv[tuple(o)] for o in offs])
            seg = _simplex_segment(P, V, y)
            if seg is None:
                continue
            p0, p1, A, t = seg
            segments.append({"p0": p0, "p1": p1, "A": A, "t": t})
            # boundary contact: preimage point on the spatial box face
            for p in (p0, p1):
                if (min(p[1], p[2], p[3]) < 1e-9 or
                        p[1] > nx + 1 - 1e-9 or p[2] > ny + 1 - 1e-9 or
                        p[3] > nz + 1 - 1e-9):
                    boundary_touch = True
    return segments, boundary_touch


def _embed(p, ns):
    """Endpoint -> R^5 with the periodic s-axis embedded on a circle so that
    periodic closeness = Euclidean closeness (radius scaled to preserve
    local distances)."""
    R = ns / (2.0 * np.pi)
    ang = 2.0 * np.pi * p[0] / ns
    return np.array([R * np.cos(ang), R * np.sin(ang), p[1], p[2], p[3]])


def chain_components(segments, ns, match_tol=1e-5):
    """Chain segments into closed curves by MUTUAL nearest-neighbour matching
    of endpoints (cKDTree). True mates (the same face point seen from the two
    adjacent simplices) agree to ~1e-10; everything else is orders of
    magnitude farther, so mutual-NN within match_tol is unambiguous. Any
    unpaired endpoint = chain break.

    Returns (components, all_closed).
    """
    from scipy.spatial import cKDTree
    n = len(segments)
    pts = np.empty((2 * n, 5))
    for sid, seg in enumerate(segments):
        pts[2 * sid] = _embed(seg["p0"], ns)
        pts[2 * sid + 1] = _embed(seg["p1"], ns)
    tree = cKDTree(pts)
    # nearest OTHER endpoint, excluding self and the same segment's two ends
    # (NB: with coincident points the self index is NOT guaranteed first)
    dist, idx = tree.query(pts, k=4)
    nearest = np.full(2 * n, -1, dtype=int)
    for e in range(2 * n):
        for j in range(4):
            cand = int(idx[e, j])
            if cand == e or cand // 2 == e // 2:
                continue
            if dist[e, j] < match_tol:
                nearest[e] = cand
            break                          # nearest valid candidate decides
    partner = np.full(2 * n, -1, dtype=int)
    for e in range(2 * n):
        m = nearest[e]
        if m >= 0 and nearest[m] == e:     # mutual
            partner[e] = m
    all_closed = bool(np.all(partner >= 0))
    used = set()
    components = []
    for sid0 in range(n):
        if sid0 in used:
            continue
        comp = [sid0]
        used.add(sid0)
        closed = False
        cur = 2 * sid0 + 1                 # walk out of p1 of the seed
        while True:
            nxt_end = partner[cur]
            if nxt_end < 0:
                break                      # broken chain
            sid = nxt_end // 2
            if sid == sid0:
                closed = True
                break
            if sid in used:
                break                      # malformed (degree > 1 somewhere)
            used.add(sid)
            comp.append(sid)
            cur = nxt_end ^ 1              # leave by the segment's other end
        components.append({"segs": comp, "closed": closed})
    all_closed = all_closed and all(c["closed"] for c in components)
    return components, all_closed


def _frame_of_segment(seg, y, fbasis):
    """Orthonormal actual frame (4x3) of the normal space, from the affine
    differential: solve dU_hat(v_a) = f_a with v_a orthogonal to the tangent."""
    T = seg["p1"] - seg["p0"]
    T = T / np.linalg.norm(T)
    Py = np.eye(4) - np.outer(y, y)
    dU = Py @ seg["A"] / max(seg["t"], 1e-12)
    B = fbasis.T @ dU                                     # 3x4 (rows: f_a . dU)
    Msys = np.vstack([B, T[None, :]])                     # 4x4
    try:
        Vsol = np.linalg.solve(Msys, np.vstack([np.eye(3), np.zeros((1, 3))]))
    except np.linalg.LinAlgError:
        return None, T
    # Gram-Schmidt the columns against T then each other
    F = []
    for a in range(3):
        v = Vsol[:, a] - (Vsol[:, a] @ T) * T
        for u in F:
            v = v - (v @ u) * u
        n = np.linalg.norm(v)
        if n < 1e-12:
            return None, T
        F.append(v / n)
    return np.column_stack(F), T


def _reference_frame(T, ref=_REF):
    """Gram-Schmidt of fixed generic vectors against the tangent."""
    F = []
    for a in range(3):
        v = ref[a] - (ref[a] @ T) * T
        for u in F:
            v = v - (v @ u) * u
        n = np.linalg.norm(v)
        if n < 1e-10:
            return None
        F.append(v / n)
    return np.column_stack(F)


def _rot_to_quat(R):
    """SO(3) matrix -> unit quaternion (standard, sign ambiguous)."""
    tr = np.trace(R)
    if tr > 0:
        w = np.sqrt(1.0 + tr) / 2.0
        x = (R[2, 1] - R[1, 2]) / (4 * w)
        y = (R[0, 2] - R[2, 0]) / (4 * w)
        z = (R[1, 0] - R[0, 1]) / (4 * w)
    else:
        i = int(np.argmax(np.diag(R)))
        j, k = (i + 1) % 3, (i + 2) % 3
        s = np.sqrt(max(1.0 + R[i, i] - R[j, j] - R[k, k], 1e-15)) * 2
        q = [0.0, 0.0, 0.0, 0.0]
        q[0] = (R[k, j] - R[j, k]) / s
        q[i + 1] = s / 4
        q[j + 1] = (R[j, i] + R[i, j]) / s
        q[k + 1] = (R[k, i] + R[i, k]) / s
        w, x, y, z = q
    v = np.array([w, x, y, z])
    return v / np.linalg.norm(v)


def component_parity(segments, comp, y, fbasis, ref=_REF):
    """Z2 framing twist of one closed component; returns (parity, min_dot)
    or (None, reason) on engineering failure."""
    frames = []
    for sid in comp["segs"]:
        Fact, T = _frame_of_segment(segments[sid], y, fbasis)
        if Fact is None:
            return None, "singular framing solve"
        Fref = _reference_frame(T, ref)
        if Fref is None:
            return None, "degenerate reference frame"
        R = Fref.T @ Fact                                 # 3x3
        if np.linalg.det(R) < 0:
            R = np.diag([1.0, 1.0, -1.0]) @ R             # constant left shift
        frames.append(R)
    # continuous quaternion lift around the cycle
    q0 = _rot_to_quat(frames[0])
    q_prev = q0
    min_dot = 1.0
    for R in frames[1:] + [frames[0]]:
        q = _rot_to_quat(R)
        d = float(np.dot(q, q_prev))
        if d < 0:
            q = -q
            d = -d
        min_dot = min(min_dot, d)
        q_prev = q
    # after full cycle q_prev is the continuous lift back at frame[0]
    parity = 0 if np.dot(q_prev, q0) > 0 else 1
    return parity, min_dot


JITTER = 1e-6    # generic-position tie-break (e.g. the exactly-constant loop
                 # makes simplex systems rank-deficient); 5 orders below the
                 # per-cell field variation and 3 above the rank tolerance --
                 # topologically null, numerically decisive.


def z2_class(Vfield, y, fbasis=None):
    """The Pontryagin-Thom Z2 class of the loop field. Returns a result dict."""
    rng = np.random.default_rng(421)
    Vfield = Vfield + JITTER * rng.standard_normal(Vfield.shape)
    if fbasis is None:
        # fixed orthonormal basis of y-perp
        fb = []
        for e in np.eye(4):
            v = e - (e @ y) * y
            for u in fb:
                v = v - (v @ u) * u
            n = np.linalg.norm(v)
            if n > 1e-6:
                fb.append(v / n)
            if len(fb) == 3:
                break
        fbasis = np.column_stack(fb)
    ns = Vfield.shape[0]
    segments, boundary = extract_preimage(Vfield, y)
    comps, all_closed = chain_components(segments, ns)
    parities, dots = [], []
    fail = None
    for c in comps:
        p, info = component_parity(segments, c, y, fbasis)
        if p is None:
            fail = info
            break
        parities.append(p)
        dots.append(info)
    ok = all_closed and not boundary and fail is None
    return {
        "class": int(sum(parities) % 2) if ok else None,
        "n_segments": len(segments),
        "n_components": len(comps),
        "component_parities": parities,
        "all_chains_closed": bool(all_closed),
        "boundary_touch": bool(boundary),
        "min_frame_dot": float(min(dots)) if dots else None,
        "frame_dot_ok": bool(dots and min(dots) >= FRAME_DOT_MIN),
        "failure": fail,
        "ok": bool(ok and dots and min(dots) >= FRAME_DOT_MIN),
    }


def z2_class_multi(Vfield, label=""):
    """Class for the 3 pre-registered regular values; stability is criterion g2."""
    results = []
    for y in REGULAR_VALUES:
        r = z2_class(Vfield, y)
        results.append(r)
        print(f"  [{label}] y={np.round(y, 2)}  class={r['class']}  "
              f"segs={r['n_segments']} comps={r['n_components']} "
              f"closed={r['all_chains_closed']} mindot="
              f"{None if r['min_frame_dot'] is None else round(r['min_frame_dot'], 3)}",
              flush=True)
    classes = [r["class"] for r in results]
    stable = len(set(classes)) == 1 and classes[0] is not None
    return {"classes": classes, "stable": bool(stable),
            "value": classes[0] if stable else None,
            "details": results}


def save_json(name, payload):
    payload = dict(payload)
    payload["_meta"] = {"campaign": "MATTER_PI1_B2",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "numpy": np.__version__}
    (OUT / name).write_text(json.dumps(payload, indent=2))
