"""B3 -- future-lightcone-intersection 2-cells: a spacelike (magnetic) sector?

Campaign FOTON_B3B4 (Fase 2, Frente B, photon critical path).  E6/E6b/E6c showed the
causal-DIAMOND 2-complex of a flat Poisson causet is essentially 100% electric, and
spatial curvature only opens the magnetic sector at PLANCKIAN curvature (E6c:
frac_B 0.0026 flat -> 0.0117 at R_hat=2; <0.01 at low curvature R_hat>=8).

B3 tests a genuinely NEW 2-cell construction: instead of a causal diamond (anchored on
a TIMELIKE pair i<k, dominated by the timelike extent => electric), anchor the cell on
a SPACELIKE pair (i,j incomparable) with a common future apex.  The base i-j edge is
spacelike, so the area bivector can carry O(1) magnetic A^{ij} content.

CELL = (i, k, j, l): i,j incomparable (spacelike-separated), and k,l two distinct events
in the MINIMAL common future (i<k, j<k, i<l, j<l).  The ordered quadrilateral i->k->j->l
is a closed 2-cell; its area bivector is classified by polygon_bivectors (REUSED verbatim
from E6 -- the same E/B split e2=sum(A^0i)^2, b2=sum(A^ij)^2).

GATE (anti-circular): a control cell anchored on a TIMELIKE pair (i<j, plus two common
future apices) must reproduce the diamond's electric dominance (frac_B ~ E6b ~ 0).  No
phase inserted; the bivector is real embedding geometry.  Under the A1 guard.

Run:  python docs/campaigns/FOTON_B3B4/b3_future_cone.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
E6 = ROOT / "results" / "gauge" / "e6"
E6B = ROOT / "results" / "gauge" / "e6b"
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
for p in (str(E6), str(E6B), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from e6b_diamond_height_core import polygon_bivectors           # noqa: E402  (REUSE E/B split)
from orientation_core import causal_link_graph                  # noqa: E402
from causal_core import sprinkle_box                            # noqa: E402

RHO = 2.0                                                       # match E6/E6b density


def _wilson(k, n, z=1.96):
    """Wilson score interval for a binomial fraction k/n."""
    if n == 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return p, (c - h) / d, (c + h) / d


def future_cone_cells(C, max_pairs=6000, max_apices=2, anchor="spacelike", seed=0,
                      max_cells=20000):
    """Build 2-cells anchored on event pairs sharing a common future.

    C : (n,n) bool strict causal order, C[i,j] = i precedes j.
    anchor='spacelike' : i,j INCOMPARABLE (not C[i,j] and not C[j,i]) -- the B3 cell.
    anchor='timelike'  : i<j (C[i,j]) -- the GATE control (must read electric).
    For each anchor pair, take up to max_apices events in the common future
    {k : both i<k and j<k}; restrict to the MINIMAL future (smallest temporal index,
    i.e. nearest apices) for a compact cell.  Cell = ordered quad (i,k,j,l).
    Returns an (P,4) int vertex array.
    """
    n = C.shape[0]
    rng = np.random.default_rng(seed)
    future = C                                                  # future[a] = events after a
    cells = []
    order = rng.permutation(n)
    npair = 0
    for ii in range(n):
        i = int(order[ii])
        fi = future[i]                                          # bool (n,) i < *
        for j in range(i + 1, n):
            if anchor == "spacelike":
                if C[i, j] or C[j, i]:
                    continue                                    # must be incomparable
            else:  # timelike control
                if not C[i, j]:
                    continue
            common = np.nonzero(fi & future[j])[0]              # common future of i,j
            if common.size < 2:
                continue
            # minimal (nearest) apices: the two with the fewest ancestors among `common`
            # (proxy for "first layer" of the common future) -- cheap: lowest index works
            # since pts are time-sorted upstream; pick 2 distinct.
            ap = common[:max_apices] if common.size >= max_apices else common
            if ap.size < 2:
                continue
            k, l = int(ap[0]), int(ap[1])
            cells.append((i, k, j, l))
            npair += 1
            if len(cells) >= max_cells or npair >= max_pairs:
                break
        if len(cells) >= max_cells or npair >= max_pairs:
            break
    return np.array(cells, dtype=np.int64) if cells else np.zeros((0, 4), np.int64)


def measure(pts, anchor, seed, null=False):
    """Measure frac_B for the anchored cells.  If null=True, replace the genuine
    common-future apices with RANDOM events: this is the TAUTOLOGY CONTROL.  If the
    spacelike result is real gauge structure (the causal common-future matters), the
    null frac_B should differ; if it stays ~equal, the magnetic dominance is a pure
    kinematic artefact of anchoring on a spacelike base, NOT emergent gauge content."""
    g, C = causal_link_graph(pts, return_relation=True)
    V = future_cone_cells(C, anchor=anchor, seed=seed)
    P = int(V.shape[0])
    if P == 0:
        return {"P": 0, "frac_B": float("nan"), "n": int(g.n)}
    if null:
        # keep the anchor pair (i,j) = columns 0,2; randomise the apices (cols 1,3)
        rng = np.random.default_rng(7 * seed + 1)
        Vn = V.copy()
        Vn[:, 1] = rng.integers(0, g.n, size=P)
        Vn[:, 3] = rng.integers(0, g.n, size=P)
        V = Vn
    _, e2, b2 = polygon_bivectors(pts, V)
    nB = int(np.sum(b2 > e2))
    p, lo, hi = _wilson(nB, P)
    return {"P": P, "n_B": nB, "frac_B": p, "wilson_lo": lo, "wilson_hi": hi,
            "mean_e2": float(np.mean(e2)), "mean_b2": float(np.mean(b2)),
            "mean_b2_over_e2": float(np.mean(b2) / (np.mean(e2) + 1e-300)),
            "n": int(g.n)}


def main():
    t0 = time.time()
    print("=" * 78)
    print("B3 -- future-cone-intersection 2-cells: spacelike (magnetic) sector at LOW curvature?")
    print("=" * 78)

    # LOW curvature = flat Minkowski (R_hat=inf, the observable-universe regime).
    Ns = [400, 800, 1500]
    rows = {"spacelike": [], "timelike_gate": [], "spacelike_null": []}
    spec = [("timelike", "timelike_gate", False),
            ("spacelike", "spacelike", False),
            ("spacelike", "spacelike_null", True)]
    for N in Ns:
        L = (N / RHO) ** 0.25
        for anchor, key, null in spec:
            accP, accB = 0, 0
            for seed in (1, 2, 3):
                rng = np.random.default_rng(100 * seed + N)
                pts = sprinkle_box(RHO, [(0.0, L)] * 4, rng)
                r = measure(pts, anchor, seed, null=null)
                if r["P"] > 0:
                    accP += r["P"]; accB += r["n_B"]
            p, lo, hi = _wilson(accB, accP)
            row = {"N": N, "P_tot": accP, "nB_tot": accB, "frac_B": p,
                   "wilson_lo": lo, "wilson_hi": hi}
            rows[key].append(row)
            lbl = anchor + ("-NULL" if null else "")
            print(f"  [{lbl:14s}] N={N:5d}: P={accP:6d} frac_B={p:.5f} "
                  f"[{lo:.5f},{hi:.5f}]", flush=True)

    # ---- gate: timelike-anchored control must be electric (frac_B small) ----
    gate_fracs = [r["frac_B"] for r in rows["timelike_gate"]]
    gate_ok = all(f < 0.05 for f in gate_fracs)     # control stays electric-dominated
    sp = rows["spacelike"][-1]                       # largest N
    nullr = rows["spacelike_null"][-1]
    sp_lo = sp["wilson_lo"]
    sp_fracs = [r["frac_B"] for r in rows["spacelike"]]
    n_stable = bool(max(sp_fracs) - min(sp_fracs) < 0.02 or sp_fracs[-1] >= sp_fracs[0])
    # ---- TAUTOLOGY CONTROL: is the magnetic dominance from the causal common-future,
    #      or merely from anchoring on a spacelike base?  If the null (random apices)
    #      reproduces frac_B, the result is kinematic, NOT emergent gauge content.
    null_gap = abs(sp["frac_B"] - nullr["frac_B"])
    is_tautology = bool(null_gap < 0.05)            # null ~ signal => no gauge content

    if not gate_ok:
        tag = "INVALID"
        verdict = (f"INVALID: the timelike-anchored gate is not electric-dominated "
                   f"(frac_B={gate_fracs}); the cell construction or E/B split is suspect.")
    elif is_tautology:
        tag = "DEATH_B3_TAUTOLOGY"
        verdict = (
            f"DEATH (tautology exposed): the spacelike-anchored cells DO carry a large "
            f"magnetic fraction (frac_B={sp['frac_B']:.3f}), but the NULL control with RANDOM "
            f"apices gives the SAME frac_B={nullr['frac_B']:.3f} (gap {null_gap:.3f} < 0.05). "
            f"The magnetic dominance is therefore a KINEMATIC ARTEFACT of anchoring the cell "
            f"on a spacelike base (i,j incomparable => the i-j diagonal is spacelike => b2>e2 "
            f"by geometry), NOT emergent gauge content sourced by the causal common-future. "
            f"A magnetic photon needs the cell's magnetic content to come from the causal "
            f"structure, which it does not here. Direction B (this construction) does not "
            f"furnish a genuine magnetic sector; the honest E6/E6b/E6c diamonds remain the "
            f"faithful gauge plaquettes (electric). [FRONTIER] stands.")
    elif n_stable and sp_lo > 0.01:
        tag = "SUCCESS_B3_CANDIDATE"
        verdict = (
            f"SUCCESS (candidate, needs gauge-invariance follow-up): future-cone cells carry "
            f"frac_B={sp['frac_B']:.3f} (Wilson-lo {sp_lo:.3f}) at LOW curvature, N-stable, AND "
            f"the causal common-future MATTERS (null with random apices gives "
            f"frac_B={nullr['frac_B']:.3f}, gap {null_gap:.3f} > 0.05 -- not a kinematic "
            f"tautology). This is a real candidate for a magnetic sector on the bare flat "
            f"causet. BEFORE any paper: must verify (i) the cells form a connected gauge "
            f"2-complex and (ii) a gauge-invariant action -- not done here. Promising, not "
            f"yet the photon.")
    else:
        tag = "DEATH_B3"
        verdict = (f"DEATH: spacelike-anchored future-cone cells are electric at low curvature "
                   f"(frac_B={sp['frac_B']:.4f}, Wilson-lo {sp_lo:.4f} <= 0.01). Direction B "
                   f"exhausted; magnetic photon stays [FRONTIER].")

    out = {"campaign": "FOTON_B3B4", "experiment": "B3_future_cone", "rho": RHO,
           "low_curvature": "flat Minkowski (R_hat=inf)", "rows": rows,
           "gate_timelike_electric": gate_ok, "spacelike_N_stable": n_stable,
           "tautology_null_gap": null_gap, "is_tautology": is_tautology,
           "verdict": verdict, "verdict_tag": tag, "runtime_s": time.time() - t0}
    (HERE / "b3_future_cone.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"VERDICT [{tag}]:\n{verdict}")
    print(f"[{out['runtime_s']:.0f}s] -> b3_future_cone.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
