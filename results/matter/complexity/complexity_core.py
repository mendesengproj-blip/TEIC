"""complexity_core.py -- shared engine for the MATTER_COMPLEXITY campaign (CC1-CC6).

Tests the founding TEIC hypothesis:  mass  is the causal cost of displacement,
and that cost  is the internal topological complexity  N  of a causal structure.

    photon  : every causal tick = 1 external displacement      (N = 0, v = 1)
    massive : N internal ticks before 1 external displacement  (N loops, v < 1)

This module builds causal STRUCTURES with a CONTROLLED first Betti number N (the
number of independent undirected cycles of the structure's graph), embeds them in
a Poisson causal network, and measures their displacement cost by COUNTING events.
It modifies nothing in R1-R3 / e6-e11 / D1-D3 / M1-S1; it reuses only the bare
Poisson generator of src/causal_core.py.

ANTI-CIRCULARITY (this file is scanned by tests/test_no_circularity.py, which walks
results/matter/ recursively):
  * Mass, energy, momentum, force, F=ma, E=mc^2, Klein-Gordon, Dirac NEVER enter a
    generator.  Every "cost" below is an integer count of events / causal links.
  * No special-/general-relativistic dilation formula.  Boosts are pure coordinate
    maps written in RAPIDITY form (cosh/sinh); the factor 1/sqrt(1-beta^2) is never
    written.  (cosh(phi) equals it for beta=tanh(phi), but we never insert the sqrt.)
  * No complex numbers (no quantum phase).

The cycle = causal "diamond"
----------------------------
A directed causal order is acyclic (no closed timelike curve), so a "loop" cannot be
a directed cycle.  The causally admissible cycle is the DIAMOND: an event that splits
into two spacelike-separated branch events that re-merge.  Its UNDIRECTED graph has
one independent cycle (Betti += 1).  It advances coordinate time but returns the
centroid to the same x -- exactly "an internal update that does not translate".

What is genuinely MEASURED vs what is DEFINITIONAL
--------------------------------------------------
  * Kinematic cost C(N) = (coordinate ticks)/(displacement) = 1 + N/n_ext is EXACT
    by construction -- it is the operational definition realised, not a discovery.
  * Proper time tau(N) = the LONGEST CAUSAL CHAIN through the structure embedded in a
    Poisson medium is genuinely MEASURED (it depends on the random sprinkle; it has
    seed-to-seed error bars).  tau is a combinatorial invariant of the causal set, so
    it is the Lorentz-invariant "rest cost".  The campaign's real question is whether
    tau(N) is proportional to N and whether it behaves like a rest mass.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

from causal_core import sprinkle_box  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

# Canonical complexity ladder for the whole campaign.
N_LADDER = [0, 1, 3, 10, 30, 100]
SEEDS = range(20)


# --------------------------------------------------------------------------- #
# Structure builder (pure topology + geometry -- NO physics inserted)
# --------------------------------------------------------------------------- #
def build_structure(N, n_ext=12, branch_w=0.3, ext_dx=1.0):
    """Build a causal structure with internal complexity (first Betti number) = N.

    The worldline runs forward in coordinate time.  N "diamonds" (internal cycles)
    are distributed as evenly as possible among ``n_ext`` external translation steps.

      * diamond  : split S -> {B+, B-} -> merge M.  dt(S->M)=1, net dx=0.  +1 cycle.
      * ext step : a single near-null link, dt=1, dx=ext_dx.  0 cycles, +dx.

    Returns a dict with
      events   : (V,2) array of (t,x) coordinates
      edges    : (E,2) int array of directed causal links (i precedes j)
      internal : (E,) bool, True for links inside a diamond (no external translation)
      diamonds : list of (S,Bp,Bm,M) event-index tuples (one per cycle)
      betti, n_ext, dx_total, dt_total
    """
    events = []
    edges = []
    internal = []
    diamonds = []

    def add(t, x):
        events.append((t, x))
        return len(events) - 1

    t, x = 0.0, 0.0
    prev = add(t, x)
    diamonds_left = N
    for k in range(n_ext):
        # spread the remaining diamonds over the remaining external steps
        d_here = diamonds_left // (n_ext - k)
        diamonds_left -= d_here
        for _ in range(d_here):
            s = prev
            bp = add(t + 0.5, x + branch_w)
            bm = add(t + 0.5, x - branch_w)
            m = add(t + 1.0, x)
            edges += [(s, bp), (s, bm), (bp, m), (bm, m)]
            internal += [True, True, True, True]
            diamonds.append((s, bp, bm, m))
            t += 1.0
            prev = m
        nx = add(t + 1.0, x + ext_dx)         # external translation step (near-null)
        edges.append((prev, nx))
        internal.append(False)
        t += 1.0
        x += ext_dx
        prev = nx

    events = np.asarray(events, dtype=float)
    edges = np.asarray(edges, dtype=int)
    internal = np.asarray(internal, dtype=bool)
    return dict(events=events, edges=edges, internal=internal, diamonds=diamonds,
                betti=betti(len(events), edges), N=N, n_ext=n_ext,
                branch_w=branch_w, ext_dx=ext_dx,
                dx_total=float(x), dt_total=float(t))


def betti(n_vertices, edges):
    """First Betti number of the UNDIRECTED graph: E - V + (connected components).

    Pure counting -- no geometry, no physics.  For a tree it is 0; each independent
    cycle adds 1.  This is N_interno.
    """
    edges = np.asarray(edges, dtype=int)
    parent = list(range(n_vertices))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for i, j in edges:
        ri, rj = find(int(i)), find(int(j))
        if ri != rj:
            parent[ri] = rj
    comps = len({find(v) for v in range(n_vertices)})
    return int(len(edges) - n_vertices + comps)


# --------------------------------------------------------------------------- #
# Kinematics of the structure (counting only)
# --------------------------------------------------------------------------- #
def v_eff(struct):
    """Effective translation speed of the centroid = displacement / coordinate time.

    v_eff = n_ext*ext_dx / (N + n_ext).  For N=0 this is ext_dx/1 = 1 (the photon).
    """
    return struct["dx_total"] / struct["dt_total"]


def cost_kinematic(struct):
    """C(N) = coordinate ticks per unit displacement = dt_total / dx_total.

    Exact by construction: C = 1 + N/n_ext (an AFFINE law).  This is the operational
    definition of "causal cost of displacement", realised -- not an emergent discovery.
    """
    return struct["dt_total"] / struct["dx_total"]


# --------------------------------------------------------------------------- #
# Longest causal chain (proper time) -- the genuinely MEASURED quantity
# --------------------------------------------------------------------------- #
def longest_chain(pts):
    """Length (number of links) of the longest causal chain in a small causal set.

    Topological-sort dynamic program over the strict causal order of ``pts``.  This
    is the causal-set proper-time estimator (Myrheim-Meyer): the longest chain in a
    causal diamond grows with the diamond's proper time.  It is a COMBINATORIAL
    INVARIANT of the order -- frame independent -- and uses no metric dilation.
    """
    pts = np.asarray(pts, dtype=float)
    n = len(pts)
    if n == 0:
        return 0
    order = np.argsort(pts[:, 0])
    t = pts[:, 0]
    x = pts[:, 1:]
    best = np.ones(n, dtype=int)            # chain length ending at each event (>=1)
    for a in range(n):
        i = order[a]
        dt = t[i] - t[order[:a]]
        dx2 = np.sum((x[i] - x[order[:a]]) ** 2, axis=1)
        anc = order[:a][(dt > 0) & (dt * dt > dx2)]
        if anc.size:
            best[i] = 1 + best[anc].max()
    return int(best.max())


def proper_time(struct, rho, rng, pad=0.15):
    """Measured proper time tau of the structure = sum of longest chains through its
    diamonds, each realised by a Poisson sprinkle of density ``rho``.

    Only the TIMELIKE internal diamonds accrue proper time; the near-null external
    steps contribute ~0 (a null worldline has zero proper time).  So tau counts
    exactly the internal causal updates -- the candidate for the rest mass m c^2.
    Returns chain links summed over the N diamonds (0 for the photon N=0).
    """
    ev = struct["events"]
    total = 0
    for (s, bp, bm, m) in struct["diamonds"]:
        A, B = ev[s], ev[m]
        box = [(A[0] - pad, B[0] + pad),
               (min(ev[bp][1], ev[bm][1]) - pad, max(ev[bp][1], ev[bm][1]) + pad)]
        pts = sprinkle_box(rho, box, rng)
        # keep only events inside the causal diamond A < y < B
        if len(pts):
            dtA = pts[:, 0] - A[0]
            dx2A = (pts[:, 1] - A[1]) ** 2
            fa = (dtA > 0) & (dtA * dtA > dx2A)
            dtB = B[0] - pts[:, 0]
            dx2B = (pts[:, 1] - B[1]) ** 2
            fb = (dtB > 0) & (dtB * dtB > dx2B)
            pts = pts[fa & fb]
        # include the diamond's own endpoints so an empty sprinkle still gives 1 link
        core = np.vstack([A, B, pts]) if len(pts) else np.vstack([A, B])
        total += longest_chain(core)
    return int(total)


# --------------------------------------------------------------------------- #
# Coordinate maps (pure geometry -- NOT dilation formulas).  Rapidity form only.
# --------------------------------------------------------------------------- #
def boost(struct, rapidity):
    """Return a copy of the structure with all events Lorentz-boosted by ``rapidity``.

        t' = t cosh phi + x sinh phi ,   x' = x cosh phi + t sinh phi

    cosh^2 - sinh^2 = 1, so this is a pure coordinate relabelling (no dilation
    factor 1/sqrt(1-beta^2) appears).  Edges / diamonds / Betti are unchanged: the
    causal order is invariant.  beta = tanh(phi) is the corresponding velocity.
    """
    ch, sh = np.cosh(rapidity), np.sinh(rapidity)
    ev = struct["events"]
    t, x = ev[:, 0], ev[:, 1]
    out = ev.copy()
    out[:, 0] = ch * t + sh * x
    out[:, 1] = sh * t + ch * x
    new = dict(struct)
    new["events"] = out
    return new


# --------------------------------------------------------------------------- #
# Radial Poisson solver for the gravity link CC5 (D3 machinery, pure numpy)
# --------------------------------------------------------------------------- #
def radial_grid(L, n_bins, r_min=1.0):
    """Log-spaced radial grid on [r_min, L] in d=3 (shell measure ~ r^2 dr)."""
    edges = np.geomspace(r_min, L, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    shell_vol = (edges[1:] ** 3 - edges[:-1] ** 3) / 3.0
    return edges, centers, shell_vol


def _radial_laplacian(centers, shell_vol, K):
    n = centers.size
    dr = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H = K * vbar / dr ** 2
    Lap = np.zeros((n, n))
    for e in range(n - 1):
        Lap[e, e] += H[e]
        Lap[e + 1, e + 1] += H[e]
        Lap[e, e + 1] -= H[e]
        Lap[e + 1, e] -= H[e]
    return Lap


def radial_source_core(centers, shell_vol, r_core, w_source):
    """Normalised finite source core of total deposited weight ``w_source`` (NO G).

    ``w_source`` is a dimensionless causal-density weight; here it will be set to the
    structure's complexity (loops / proper time), never to a mass.
    """
    mask = centers < r_core
    s = np.where(mask, shell_vol, 0.0)
    s = s / s.sum()
    return w_source * s


def radial_solve(centers, shell_vol, q, K):
    """Exact equilibrium field theta of the quadratic gradient action (= discrete
    Poisson) with a neutralising background and gauge sum_i theta_i V_i = 0."""
    Lap = _radial_laplacian(centers, shell_vol, K)
    lam = q.sum() / shell_vol.sum()
    rhs = q - lam * shell_vol
    theta, *_ = np.linalg.lstsq(Lap, rhs, rcond=None)
    theta = theta - (theta * shell_vol).sum() / shell_vol.sum()
    return theta


def fit_amplitude(centers, theta, r_lo, r_hi):
    """Fit theta = A/r + C on [r_lo, r_hi]; return (A, C).  A is the 1/r amplitude."""
    use = (centers >= r_lo) & (centers <= r_hi)
    if use.sum() < 4:
        return float("nan"), float("nan")
    X = np.vstack([1.0 / centers[use], np.ones(use.sum())]).T
    coef, *_ = np.linalg.lstsq(X, theta[use], rcond=None)
    return float(coef[0]), float(coef[1])


# --------------------------------------------------------------------------- #
# Statistics + IO
# --------------------------------------------------------------------------- #
def seed_stats(values):
    """mean / std / sem of per-seed scalars (NaNs dropped)."""
    a = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if a.size == 0:
        return {"mean": float("nan"), "std": float("nan"), "sem": float("nan"), "n": 0}
    std = float(a.std(ddof=1)) if a.size > 1 else 0.0
    return {"mean": float(a.mean()), "std": std,
            "sem": std / np.sqrt(a.size) if a.size > 1 else 0.0, "n": int(a.size)}


def power_fit(N, C):
    """Fit log(C-C0) ~ p log N for N>0 after removing the N=0 intercept C0.

    Returns the power-law exponent p of (C - C0) vs N.  Reported alongside a direct
    linear and quadratic fit so the functional form is not assumed.
    """
    N = np.asarray(N, dtype=float)
    C = np.asarray(C, dtype=float)
    C0 = C[N == 0][0] if np.any(N == 0) else 0.0
    pos = N > 0
    dC = C[pos] - C0
    ok = dC > 0
    if ok.sum() < 2:
        return float("nan"), C0
    p = float(np.polyfit(np.log(N[pos][ok]), np.log(dC[ok]), 1)[0])
    return p, float(C0)


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    # self-test: Betti = N, v_eff(0) = 1, proper time grows with N
    for N in N_LADDER:
        s = build_structure(N)
        rng = np.random.default_rng(0)
        tau = proper_time(s, rho=60.0, rng=rng)
        print(f"N={N:4d}  Betti={s['betti']:4d}  v_eff={v_eff(s):.4f}  "
              f"C={cost_kinematic(s):.4f}  tau(rho=60)={tau}")
