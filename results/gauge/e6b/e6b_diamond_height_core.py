"""e6b_diamond_height_core.py -- height-h causal-diamond gauge plaquettes (2h-gons).

E6 (E6_3b) found that the smallest gauge plaquette -- a HEIGHT-2 causal diamond
i->a->k->b->i (two ascending Hasse paths of LINK length 2 between a tip pair i<k) --
is ALWAYS E-type (timelike area bivector): every such diamond contains the timelike
past-tip->future-tip extent, so b2<e2 and the magnetic (spacelike) sector is empty.
The B-type fraction was 0.0000 across 9 sprinklings.

A 4-link plaquette can only be height-2 (or a height-1 K_{2,2} box): every 4-cycle in
a Hasse diagram has min->max longest-chain length <= 2 (see E6b_literature.md). To probe
height h>=3 we must use a LARGER plaquette. The natural generalisation of "two length-2
ascending paths between a tip pair" is:

    HEIGHT-h DIAMOND PLAQUETTE = a 2h-gon, the closed loop formed by TWO vertex-disjoint
    ascending Hasse (covering-relation) paths of LINK length h between a tip pair i<k:
        path1: i = v0 -< v1 -< ... -< v_{h-1} -< vh = k
        path2: i = u0 -< u1 -< ... -< u_{h-1} -< uh = k     (interiors disjoint)
    cyclic vertex order  i, v1, ..., v_{h-1}, k, u_{h-1}, ..., u1   (2h vertices).
    h=2 reproduces EXACTLY the E6 height-2 diamond 4-gon.

The E/B PHYSICS IS REUSED VERBATIM from e6_bd_core: a cell is B-type iff its area
bivector A^{mu nu} = 1/2 sum_c x_c ^ x_{c+1} has b2=sum_{i<j}(A^{ij})^2 > e2=sum_i(A^{0i})^2.
The ONLY generalisation is the cyclic area sum over 2h vertices instead of 4 (same
formula, more terms); `polygon_bivectors` below delegates to e6_bd_core for the 4-gon
case and a self-test asserts byte-for-byte agreement, so no E/B physics is reimplemented.

NO relativistic literal is inserted: the E/B split uses only the embedding time column
(the sprinkling's own causal/time direction), identical to E6.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E6 = HERE.parent / "e6"
E5 = HERE.parent / "e5"
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
ROOT = HERE.parents[2]
for p in (str(HERE), str(E6), str(E5), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from e6_bd_core import plaquette_bivectors, lorentzian_weights  # noqa: E402  (REUSE)


# ====================================================================== #
# Area bivector of a 2h-gon and the E/B (Minkowski) split  -- REUSE of E6
# ====================================================================== #
def polygon_bivectors(pts, verts):
    """Area bivector + electric/magnetic split for plaquettes with m vertices each.

    `verts` is an (P, m) int array (all P polygons share the SAME m within a call --
    true for a fixed height h, where m=2h). Returns (A, e2, b2) with EXACTLY the E6
    definition generalised to m vertices:
        A^{mu nu} = 1/2 sum_{c=0..m-1} (x_c ^ x_{c+1 mod m})    (translation-invariant)
        e2 = sum_i (A^{0i})^2   (timelike/electric),  b2 = sum_{i<j} (A^{ij})^2 (magnetic)
    For m=4 this is byte-for-byte e6_bd_core.plaquette_bivectors (asserted in self-test)."""
    verts = np.asarray(verts, np.int64)
    if verts.shape[1] == 4:
        return plaquette_bivectors(pts, verts)        # exact E6 path, no reimplementation
    X = np.asarray(pts, float)[verts]                 # (P, m, D)
    P, m, D = X.shape
    A = np.zeros((P, D, D))
    for c in range(m):
        xa = X[:, c, :]
        xb = X[:, (c + 1) % m, :]
        A += 0.5 * (xa[:, :, None] * xb[:, None, :] - xa[:, None, :] * xb[:, :, None])
    e2 = np.sum(A[:, 0, 1:] ** 2, axis=1)
    iu = np.triu_indices(D - 1, k=1)
    sub = A[:, 1:, 1:]
    b2 = np.sum(sub[:, iu[0], iu[1]] ** 2, axis=1)
    return A, e2, b2


# ====================================================================== #
# Ascending Hasse paths of fixed link length h between a tip pair
# ====================================================================== #
def _enumerate_paths_from(g, src, h, max_paths, rng):
    """Up to `max_paths` ascending covering-paths of LINK length exactly h starting at
    `src`, grouped by endpoint. Returns dict endpoint -> list of vertex tuples
    (len h+1, src first). Bounded DFS: at each node its children are visited in random
    order and the per-source path budget caps the cost (unbiased reservoir-free sample
    of the shallow paths). Children CSR comes from g (orientation_core)."""
    paths_by_end = {}
    budget = [max_paths]
    stack_path = [int(src)]

    def dfs(node, depth):
        if budget[0] <= 0:
            return
        if depth == h:
            end = node
            paths_by_end.setdefault(end, []).append(tuple(stack_path))
            budget[0] -= 1
            return
        ch = g.children(node)
        if ch.size == 0:
            return
        if ch.size > 1:
            ch = ch[rng.permutation(ch.size)]
        for c in ch:
            if budget[0] <= 0:
                return
            stack_path.append(int(c))
            dfs(int(c), depth + 1)
            stack_path.pop()

    dfs(int(src), 0)
    return paths_by_end


def _disjoint_pairs(paths, max_pairs, rng):
    """From a list of equal-length paths sharing endpoints (src, end), yield up to
    `max_pairs` pairs (p1, p2) whose INTERIORS are vertex-disjoint (endpoints shared).
    Greedy over a random order; cheap and unbiased enough for a fraction estimate."""
    n = len(paths)
    if n < 2:
        return []
    order = rng.permutation(n)
    out = []
    for ii in range(n):
        a = paths[order[ii]]
        ia = set(a[1:-1])
        for jj in range(ii + 1, n):
            b = paths[order[jj]]
            if ia.isdisjoint(b[1:-1]):
                out.append((a, b))
                if len(out) >= max_pairs:
                    return out
    return out


def height_h_plaquettes(g, h, max_plaqs=6000, max_sources=600,
                        paths_per_source=60, max_pairs_per_pair=3, seed=0):
    """Collect 2h-gon plaquette vertex-lists for height-h diamonds of the causal link
    graph g. Returns an (P, 2h) int array of cyclic vertex orderings.

    For each of up to `max_sources` randomly chosen events i (with children), enumerate
    up to `paths_per_source` ascending length-h covering-paths grouped by endpoint k;
    for each tip pair (i,k) with >=2 interior-disjoint paths, form up to
    `max_pairs_per_pair` plaquettes. Stops at `max_plaqs`. h=2 reproduces the E6
    height-2 diamonds (validated against E6_3b numbers)."""
    rng = np.random.default_rng(seed)
    n = g.n
    have_children = np.array([g.children(i).size > 0 for i in range(n)])
    sources = np.nonzero(have_children)[0]
    if sources.size == 0:
        return np.zeros((0, 2 * h), np.int64)
    if sources.size > max_sources:
        sources = rng.choice(sources, max_sources, replace=False)
    else:
        sources = rng.permutation(sources)

    plaqs = []
    for i in sources:
        if len(plaqs) >= max_plaqs:
            break
        pend = _enumerate_paths_from(g, int(i), h, paths_per_source, rng)
        for k, plist in pend.items():
            if len(plist) < 2:
                continue
            for (p1, p2) in _disjoint_pairs(plist, max_pairs_per_pair, rng):
                # cyclic order: i, v1..v_{h-1}, k, u_{h-1}..u1   (2h vertices)
                cyc = list(p1[:-1]) + list(p2[::-1][:-1])
                plaqs.append(cyc)
                if len(plaqs) >= max_plaqs:
                    break
            if len(plaqs) >= max_plaqs:
                break
    if not plaqs:
        return np.zeros((0, 2 * h), np.int64)
    return np.array(plaqs, dtype=np.int64)


# ====================================================================== #
# Self-test: h=2 path reproduces e6_bd_core exactly; geometry sanity
# ====================================================================== #
if __name__ == "__main__":
    rng = np.random.default_rng(0)
    # (1) polygon_bivectors on 4-gons == e6_bd_core.plaquette_bivectors (identical physics)
    pts = rng.standard_normal((20, 4))
    verts4 = rng.integers(0, 20, size=(50, 4))
    A1, e1, b1 = polygon_bivectors(pts, verts4)
    A2, e2, b2 = plaquette_bivectors(pts, verts4)
    assert np.allclose(A1, A2) and np.allclose(e1, e2) and np.allclose(b1, b2)
    print("OK  polygon_bivectors(4-gon) == e6_bd_core.plaquette_bivectors")

    # (2) a known SPACELIKE square (purely spatial loop) must be B-type, and a known
    #     TIMELIKE square (a 0-1 plane loop) must be E-type -- sign convention sanity.
    space_sq = np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0]], float)
    _, es, bs = polygon_bivectors(space_sq, np.array([[0, 1, 2, 3]]))
    time_sq = np.array([[0, 0, 0, 0], [1, 0, 0, 0], [1, 1, 0, 0], [0, 1, 0, 0]], float)
    _, et, bt = polygon_bivectors(time_sq, np.array([[0, 1, 2, 3]]))
    assert bs[0] > es[0] and bt[0] < et[0]
    print(f"OK  spacelike square b2>e2 ({bs[0]:.2f}>{es[0]:.2f}); "
          f"timelike square e2>b2 ({et[0]:.2f}>{bt[0]:.2f})")

    # (3) height-2 plaquettes on a small causal sprinkle: must be ALL E-type (E6 result)
    from causal_core import sprinkle_box
    from orientation_core import causal_link_graph
    p = sprinkle_box(0.7, [(0.0, 5.0)] * 4, np.random.default_rng(1))
    g = causal_link_graph(p)
    V2 = height_h_plaquettes(g, 2, max_plaqs=3000, seed=1)
    _, e, b = polygon_bivectors(p, V2)
    fracB = float(np.mean(b > e)) if V2.shape[0] else float("nan")
    print(f"OK  h=2 plaquettes: N={g.n} P={V2.shape[0]} frac_B={fracB:.4f} "
          f"(E6 expects 0.0000)")
    print("self-test OK")
