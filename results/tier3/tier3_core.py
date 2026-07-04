"""tier3_core.py -- shared engine for the TIER3 exploratory campaign (T3A/T3B/T3C).

Pre-registered kill criteria live in TIER3_EXPLORATIONS.md (repo root) and in each
task generator's docstring.  THIS FILE FIXES, BEFORE ANY CAMPAIGN CELL RUNS:

  * the growth dynamics: the e7 TEIC rule (a member of the GENERAL Rideout-Sorkin
    / CSG family parametrized by n_components; audited in e7_growth_dynamics.py).
    At each step the new event's past-set I is drawn with
        P(I) propto w(I),   w(I) = w_meet if I has >= 2 connected components
                            else 1            (n_components as in e7).
    Default coupling w_meet = 1/3 (e7's canonical T3 value).

  * the sampler: exact enumeration of order ideals (e7's transition_table) is
    impossible beyond N ~ 10 (ideal counting is #P-hard), so each growth step
    draws I by a LAZY Metropolis toggle chain on the lattice of order ideals
    of the current causet, warm-started from the previous step's choice, with
    K = max(K_MIN, K_FACTOR * n) proposals per step (laziness 1/2: each
    proposal holds with probability 1/2, guaranteeing aperiodicity -- without
    it the chain is periodic on small ideal lattices, caught by gate V2).
    The chain target is exactly P(I) propto w(I): the toggle proposal is
    symmetric, so Metropolis acceptance min(1, w(I')/w(I)) gives the e7
    distribution in stationarity.
    The sampler is validated against e7's EXACT enumeration at small N by
    T3V_validation.py (engineering gate -- if it fails, NO campaign runs).
    K_FACTOR may be raised to pass the gate; it is fixed BEFORE any physics run.

  * the dimension estimator (Myrheim-Meyer): ordering fraction
        r = 2 R / (N (N-1))      (fraction of unordered pairs that are related)
    inverted through the flat-interval expectation
        f(d) = Gamma(d+1) Gamma(d/2) / (2 Gamma(3d/2)),
    checks: f(1) = 1 (chain), f(2) = 1/2, f(4) = 0.1.
    PRIMARY observable: median d_MM over the largest Alexandrov sub-intervals
    of the causet (the estimator's valid domain is an interval).  SECONDARY:
    global d_MM of the whole set.  Both always reported; verdicts use PRIMARY.

ANTI-CIRCULARITY: no d=4 target, no hbar, no Planck scale, no relativistic
dilation formula anywhere in generator code.  Target dimensions enter only
verdict / comparison code.  Sprinkling takes an explicit background dimension
as INPUT only in (a) estimator controls and (b) T3B seeds, where the background
IS the experimental variable -- both labelled as such.  Scanned by
tests/test_no_circularity.py.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
from scipy.optimize import brentq
from scipy.special import gammaln

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

TIER3_DIR = Path(__file__).resolve().parent

# Sampler constants -- fixed before any physics run (see module docstring).
W_MEET_DEFAULT = 1.0 / 3.0
K_FACTOR = 12         # MCMC proposals per growth step = max(K_MIN, K_FACTOR*n);
K_MIN = 128           # the chain is lazy (1/2), so effective moves are K/2
INIT_BURN_FACTOR = 20  # extra burn-in proposals (x n) when starting from a seed


# ============================================================================
# Growth engine: e7 TEIC rule, MCMC over order ideals, scalable to N ~ 2000
# ============================================================================
class GrowthCauset:
    """Causet grown by the e7 TEIC rule with an MCMC ideal sampler.

    Representation: A[i, j] = True  iff  j strictly precedes i (ancestor
    matrix, transitive by construction -- a new event's ancestor set is the
    chosen ideal, which is downward closed).

    Incremental component bookkeeping (exact, with BFS fallback):
      the Metropolis weight only depends on ncomp(I).  For an ideal I of a
      causet, the neighbours (comparable elements) of x in I are exactly
      anc(x): if x is addable, anc(x) subseteq I and no descendant of x can be
      in I; if x in I, anc(x) subseteq I and removability requires no
      descendant in I.  Hence:
        add x   : anc empty -> ncomp+1; anc(x) connected as a sub-poset
                  ("past_connected") -> ncomp unchanged; else BFS recount.
        remove x: anc empty -> ncomp-1; past_connected -> unchanged
                  (the attachment blob anc(x) stays connected); else BFS.
      past_connected[x] is computed once at x's birth.  The BFS fallback is
      exact; V0 in T3V_validation.py audits this bookkeeping against full
      recounts.
    """

    def __init__(self, n_max, w_meet=W_MEET_DEFAULT, rng=None, seed_matrix=None):
        self.n_max = int(n_max)
        self.w_meet = float(w_meet)
        self.rng = rng if rng is not None else np.random.default_rng()
        self.A = np.zeros((self.n_max, self.n_max), dtype=bool)
        self.anc_count = np.zeros(self.n_max, dtype=np.int64)
        self.past_connected = np.zeros(self.n_max, dtype=bool)
        self.cur = np.zeros(self.n_max, dtype=bool)   # MCMC state: current ideal
        self.ncomp = 0                                 # components of cur
        self.n_bfs_fallback = 0
        self.n_proposals = 0
        self.n_accepted = 0

        if seed_matrix is None:
            # pure growth: a single primordial event with empty past
            self.n = 1
            self.past_connected[0] = True
        else:
            S = np.asarray(seed_matrix, dtype=bool)
            ns = S.shape[0]
            if ns > self.n_max:
                raise ValueError("seed larger than n_max")
            # transitivity check: ancestor-of-ancestor must be ancestor
            via = (S @ S.astype(np.int64)) > 0
            if (via & ~S).any():
                raise ValueError("seed matrix is not transitive")
            self.A[:ns, :ns] = S
            self.n = ns
            self.anc_count[:ns] = S.sum(axis=1)
            for x in range(ns):
                m = S[x, :ns]
                self.past_connected[x] = (self._ncomp_of_mask_static(
                    self.A, ns, m) <= 1)

    # -- component counting --------------------------------------------------
    @staticmethod
    def _ncomp_of_mask_static(A, n, mask):
        """Exact number of connected components of the comparability graph
        induced on ``mask`` (BFS with vectorised frontier expansion)."""
        active = mask.copy()
        count = 0
        while True:
            start = np.argmax(active)
            if not active[start]:
                break
            count += 1
            visited = np.zeros(n, dtype=bool)
            visited[start] = True
            frontier = np.array([start])
            while frontier.size:
                nb = A[frontier, :n].any(axis=0) | A[:n, frontier].any(axis=1)
                nb &= active & ~visited
                visited |= nb
                frontier = np.flatnonzero(nb)
            active &= ~visited
        return count

    def _ncomp_full(self):
        return self._ncomp_of_mask_static(self.A, self.n, self.cur[:self.n])

    # -- MCMC over ideals ----------------------------------------------------
    def _run_chain(self, K):
        """K lazy Metropolis toggle proposals on the ideal lattice (in place).

        Laziness: x is drawn from [0, 2n); x >= n is a hold (probability 1/2),
        which makes the chain aperiodic (without it, small ideal lattices give
        a periodic chain -- e.g. a single event toggles deterministically)."""
        n = self.n
        A = self.A
        cur = self.cur
        anc_count = self.anc_count
        past_conn = self.past_connected
        w_meet = self.w_meet
        xs = self.rng.integers(0, 2 * n, size=K)
        us = self.rng.random(K)
        ncomp = self.ncomp
        accepted = 0
        bfs = 0
        for t in range(K):
            x = xs[t]
            if x >= n:
                continue
            if cur[x]:
                # removable iff no descendant of x is in the ideal
                if np.any(A[:n, x] & cur[:n]):
                    continue
                if anc_count[x] == 0:
                    nc2 = ncomp - 1
                elif past_conn[x]:
                    nc2 = ncomp
                else:
                    cur[x] = False
                    nc2 = self._ncomp_of_mask_static(A, n, cur[:n])
                    cur[x] = True
                    bfs += 1
                w_old = w_meet if ncomp >= 2 else 1.0
                w_new = w_meet if nc2 >= 2 else 1.0
                if w_new >= w_old or us[t] < w_new / w_old:
                    cur[x] = False
                    ncomp = nc2
                    accepted += 1
            else:
                # addable iff anc(x) subseteq ideal
                if np.any(A[x, :n] & ~cur[:n]):
                    continue
                if anc_count[x] == 0:
                    nc2 = ncomp + 1
                elif past_conn[x]:
                    nc2 = ncomp
                else:
                    cur[x] = True
                    nc2 = self._ncomp_of_mask_static(A, n, cur[:n])
                    cur[x] = False
                    bfs += 1
                w_old = w_meet if ncomp >= 2 else 1.0
                w_new = w_meet if nc2 >= 2 else 1.0
                if w_new >= w_old or us[t] < w_new / w_old:
                    cur[x] = True
                    ncomp = nc2
                    accepted += 1
        self.ncomp = ncomp
        self.n_proposals += K
        self.n_accepted += accepted
        self.n_bfs_fallback += bfs

    def step_grow(self):
        """One growth step: mix the ideal chain, then birth event n with the
        current ideal as its past-set."""
        n = self.n
        if n >= self.n_max:
            raise RuntimeError("n_max reached")
        self._run_chain(max(K_MIN, K_FACTOR * n))
        ideal = self.cur[:n].copy()
        self.A[n, :n] = ideal
        self.anc_count[n] = int(ideal.sum())
        # anc(new) = ideal whose ncomp we track exactly: connected iff ncomp<=1
        self.past_connected[n] = (self.ncomp <= 1)
        # warm start for the next step: the new event joins the ideal; it is
        # comparable to every element of the old ideal, so everything merges.
        self.cur[n] = True
        self.ncomp = 1
        self.n = n + 1

    def grow(self, n_target, checkpoints=(), on_checkpoint=None,
             init_burn=False, progress=False):
        if init_burn:
            self._run_chain(INIT_BURN_FACTOR * max(self.n, 8))
        cps = set(int(c) for c in checkpoints)
        t0 = time.perf_counter()
        while self.n < n_target:
            self.step_grow()
            if self.n in cps and on_checkpoint is not None:
                on_checkpoint(self)
            if progress and self.n % 250 == 0:
                print(f"      n={self.n:5d}  [{time.perf_counter()-t0:7.1f}s]  "
                      f"acc={self.n_accepted/max(self.n_proposals,1):.3f}  "
                      f"bfs={self.n_bfs_fallback}")
        return self


# ============================================================================
# Myrheim-Meyer dimension estimator
# ============================================================================
def f_mm(d):
    """Expected ordering fraction (unordered pairs) of a flat d-dim interval."""
    d = np.asarray(d, dtype=float)
    return np.exp(gammaln(d + 1) + gammaln(d / 2)
                  - np.log(2.0) - gammaln(1.5 * d))


def mm_dimension(r):
    """Invert f(d) = r for the Myrheim-Meyer spacetime dimension d."""
    if not np.isfinite(r) or r <= 0:
        return float("nan")
    if r >= 1.0:
        return 1.0
    lo, hi = 0.5, 16.0
    if r > f_mm(lo):
        return float(lo)
    if r < f_mm(hi):
        return float("nan")
    return float(brentq(lambda d: f_mm(d) - r, lo, hi, xtol=1e-10))


def ordering_fraction(A, n):
    if n < 2:
        return float("nan")
    R = int(A[:n, :n].sum())
    return 2.0 * R / (n * (n - 1))


def mm_global(A, n):
    return mm_dimension(ordering_fraction(A, n))


def mm_intervals(A, n, rng, n_pairs=4000, min_interior=32, top_k=24, j_min=0):
    """PRIMARY estimator: median d_MM over the largest Alexandrov intervals.

    Samples related pairs (i, j) with j strictly preceding i (and j >= j_min,
    used by T3B to restrict to the grown region), keeps the ``top_k`` largest
    interior sizes >= ``min_interior``, and measures the ordering fraction
    INSIDE each interval -- the estimator's valid domain.
    """
    M = A[:n, :n]
    if j_min > 0:
        M = M.copy()
        M[:, :j_min] = False
    rows = np.flatnonzero(M.any(axis=1))
    if rows.size == 0:
        return None
    seen = set()
    cand = []
    for i in rng.choice(rows, size=min(n_pairs, 20 * rows.size)):
        anc = np.flatnonzero(M[i])
        j = int(rng.choice(anc))
        if (int(i), j) in seen:
            continue
        seen.add((int(i), j))
        interior = A[:n, j] & A[i, :n]          # c with j < c < i
        m = int(interior.sum())
        if m >= min_interior:
            cand.append((m, int(i), j))
    if not cand:
        return None
    cand.sort(reverse=True)
    dims, sizes = [], []
    for m, i, j in cand[:top_k]:
        S = np.flatnonzero(A[:n, j] & A[i, :n])
        sub = A[np.ix_(S, S)]
        r = 2.0 * int(sub.sum()) / (m * (m - 1))
        d = mm_dimension(r)
        if np.isfinite(d):
            dims.append(d)
            sizes.append(m)
    if not dims:
        return None
    dims = np.asarray(dims)
    return {"d_median": float(np.median(dims)),
            "d_mean": float(dims.mean()),
            "d_q25": float(np.percentile(dims, 25)),
            "d_q75": float(np.percentile(dims, 75)),
            "n_intervals": int(dims.size),
            "interval_sizes": [int(s) for s in sizes]}


def measure_causet(A, n, rng, j_min=0):
    """Standard TIER3 measurement bundle at a checkpoint."""
    r = ordering_fraction(A, n)
    out = {"N": int(n), "ordering_fraction": float(r),
           "d_mm_global": mm_global(A, n)}
    iv = mm_intervals(A, n, rng, j_min=j_min)
    out["intervals"] = iv
    out["d_mm_interval"] = iv["d_median"] if iv else float("nan")
    return out


# ============================================================================
# Static sprinkling into a d-dimensional causal diamond (controls + T3B seeds)
# ============================================================================
# NOTE: the background dimension here is an explicit INPUT -- used only for
# estimator controls (T3A-2) and for T3B initial conditions, where the input
# dimension is the experimental variable.  Never used by the growth rule.
def sprinkle_diamond(n_events, dim, rng):
    """n_events uniform points in the unit causal diamond of M^dim.

    Diamond between bottom (t=0, x=0) and top (t=1, x=0): a point is inside
    iff |x| < t and |x| < 1 - t.  Returns (n_events, dim) array, time first.
    """
    s = dim - 1
    pts = np.empty((0, dim))
    while pts.shape[0] < n_events:
        batch = max(4 * (n_events - pts.shape[0]), 256)
        t = rng.uniform(0, 1, batch)
        x = rng.uniform(-0.5, 0.5, (batch, s))
        rr = np.sqrt(np.sum(x * x, axis=1)) if s else np.zeros(batch)
        keep = (rr < t) & (rr < 1 - t)
        pts = np.vstack([pts, np.column_stack([t[keep], x[keep]])])
    return pts[:n_events]


def causal_matrix_anc(pts):
    """Ancestor matrix A[i, j] = True iff j strictly precedes i (Minkowski)."""
    pts = np.asarray(pts, dtype=float)
    dt = pts[:, 0][:, None] - pts[:, 0][None, :]      # t_i - t_j
    dx2 = np.sum((pts[:, None, 1:] - pts[None, :, 1:]) ** 2, axis=-1)
    return (dt > 0) & (dt * dt > dx2)


# ============================================================================
# Statistics + IO (campaign conventions)
# ============================================================================
def seed_stats(values):
    a = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if a.size == 0:
        return {"mean": float("nan"), "std": float("nan"),
                "sem": float("nan"), "n": 0}
    std = float(a.std(ddof=1)) if a.size > 1 else 0.0
    return {"mean": float(a.mean()), "std": std,
            "sem": std / np.sqrt(a.size) if a.size > 1 else 0.0,
            "n": int(a.size)}


def save_json(directory, name, payload):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def validation_gate():
    """Campaigns call this before running: the sampler gate must have passed."""
    p = TIER3_DIR / "T3V_validation" / "T3V_data.json"
    if not p.exists():
        sys.exit("GATE: T3V_validation has not been run -- run "
                 "results/tier3/T3V_validation.py first.")
    data = json.loads(p.read_text(encoding="utf-8"))
    if not data.get("passed", False):
        sys.exit("GATE: T3V_validation FAILED -- the MCMC sampler does not "
                 "reproduce the e7 dynamics; campaigns must not run.")
    return data


if __name__ == "__main__":
    # smoke test: grow a small causet, measure it
    rng = np.random.default_rng(0)
    g = GrowthCauset(220, rng=rng)
    t0 = time.perf_counter()
    g.grow(200)
    dt = time.perf_counter() - t0
    m = measure_causet(g.A, g.n, rng)
    print(f"grown N=200 in {dt:.2f}s  acc={g.n_accepted/g.n_proposals:.3f}  "
          f"bfs_fallbacks={g.n_bfs_fallback}")
    print(f"r={m['ordering_fraction']:.4f}  d_global={m['d_mm_global']:.3f}  "
          f"d_interval={m['d_mm_interval']:.3f}")
    print(f"f(1)={f_mm(1):.6f} (want 1)  f(2)={f_mm(2):.6f} (want 0.5)  "
          f"f(4)={f_mm(4):.6f} (want 0.1)")
