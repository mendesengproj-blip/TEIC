"""B3b -- Stage 0 + Stage 1 (BLOCKING GATES): does the future-cone 2-complex of B3
support a genuine gauge field?  Closure (d^2 = dd = 0) + gauge-invariance, with the
mandatory positive control (4D lattice = Maxwell) and the B3 kinematic null.

Pre-registration: docs/campaigns/FOTON_B3B4/PRE_REGISTRO_B3b (the B3b charter).  Per the
user's decision (jun/2026) ONLY the blocking gates run here: Stage 0 (validated
reconstruction) + Stage 1 (gauge).  Polarisation (Stage 2) and dispersion (Stage 3)
are NOT measured -- if the gauge gate fails, nothing downstream runs.  STOP at the
first verdict.

What this decides
-----------------
The B3 cell is the ordered quad (i,k,j,l): i,j spacelike-incomparable, k,l in their
common future.  Its FOUR sides are causal RELATIONS i<k, j<k, i<l, j<l -- which are NOT
in general Hasse LINKS (covering relations).  The E5/E6 gauge complex (causal_diamond_
plaquettes, height_h_plaquettes) is built ENTIRELY from Hasse links: that is the link
sector whose gauge field E6_1 validated.  So the structural questions are:

  (A) Closure  ddtheta = 0:  with F = dtheta on the cell complex and G the node
      coboundary, gauge invariance is  B G = 0  (every plaquette boundary is a node
      cycle).  For a 4-loop i->k->j->l->i this telescopes to zero BY CONSTRUCTION --
      so we ALSO run it on the B3 KINEMATIC NULL (random apices).  If the null gives
      the SAME machine-zero, the dd=0 / gauge-invariance "pass" is non-discriminating:
      it is automatic for any set of closed quads, signal or noise.  (Lesson B3/B4:
      a pass that the null reproduces is not evidence.)

  (B) Hasse-link membership:  what fraction of the cells' sides are actually links of
      the Hasse graph (= the gauge substrate E6_1 used)?  If ~0, the future-cone cells
      do not live on the link sector at all -- they are a DIFFERENT (relation) complex.

  (C) Mode counting (rank-nullity), signal vs null:  gauge modes = rank G, physical
      (transverse) = rank B.  Does the causal signal carry a richer/different physical
      sector than the kinematic null?

Positive control (Stage 0, MANDATORY): the SAME incidence/coboundary machinery on a
regular 4D lattice must reproduce Maxwell: B G = 0 to ~1e-16 and gauge fraction
(N_sites-1)/L.  If it fails, the reconstruction is untrustworthy and nothing else
counts (INVALID).

c, omega, dispersion: NEVER inserted (A1 guard).  This stage touches no relativistic
literal -- only incidence/coboundary linear algebra and the embedding causal order.

Run:  python docs/campaigns/FOTON_B3B4/b3b_closure.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
E5 = ROOT / "results" / "gauge" / "e5"
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
for p in (str(HERE), str(E5), str(ORI), str(ROOT / "src")):
    if p not in sys.path:
        sys.path.insert(0, p)

from b3_future_cone import future_cone_cells                  # noqa: E402  (REUSE B3)
from e5_core import regular_lattice                           # noqa: E402  (Maxwell control)
from orientation_core import causal_link_graph               # noqa: E402
from causal_core import sprinkle_box                          # noqa: E402

RHO = 2.0                                                      # match B3/E6 density


# ====================================================================== #
# Generic incidence (B) + node coboundary (G) for a list of 4-vertex loops
# ====================================================================== #
def loop_incidence(cells):
    """Given an (P,4) array of cyclic vertex quads (v0,v1,v2,v3) describing the loop
    v0->v1->v2->v3->v0, build:
      B : (P, L) signed plaquette-incidence on the UNIQUE undirected edges,
      G : (L, N) node coboundary (G[e,lo]=-1, G[e,hi]=+1 for stored edge (lo,hi)),
      edges : (L,2) int (lo<hi).
    Sign of an edge in a plaquette = +1 if the traversal goes lo->hi, else -1.
    (Identical convention to E6_1_gauge_structure / e5_core; closure B G = 0 is then a
    PURE combinatorial cycle property -- true for any genuine 4-loop, signal or null.)
    """
    cells = np.asarray(cells, np.int64)
    P = cells.shape[0]
    # collect directed traversal steps (v_c -> v_{c+1})
    steps = []  # (p, u, v)
    for p in range(P):
        q = cells[p]
        for c in range(4):
            u, v = int(q[c]), int(q[(c + 1) % 4])
            if u != v:
                steps.append((p, u, v))
    # unique undirected edges
    emap = {}
    edges = []
    for _, u, v in steps:
        key = (u, v) if u < v else (v, u)
        if key not in emap:
            emap[key] = len(edges)
            edges.append(key)
    L = len(edges)
    nodes = sorted({n for e in edges for n in e})
    nmap = {nd: i for i, nd in enumerate(nodes)}
    N = len(nodes)
    B = np.zeros((P, L))
    for p, u, v in steps:
        lo, hi = (u, v) if u < v else (v, u)
        eid = emap[(lo, hi)]
        B[p, eid] += 1.0 if u < v else -1.0          # +1 if step goes lo->hi
    G = np.zeros((L, N))
    for eid, (lo, hi) in enumerate(edges):
        G[eid, nmap[lo]] -= 1.0
        G[eid, nmap[hi]] += 1.0
    return B, G, np.array(edges, np.int64), N, L


def gauge_metrics(B, G, label, n_random=1000, seed=0):
    """Closure, gauge-invariance and mode counting for an incidence/coboundary pair.

    dd / closure :  max|B G|        (exact zero <=> every plaquette boundary is a cycle)
    dS/S         :  S=1/2 th^T M th, M=B^T B, gauge shift th->th+G chi over n_random
                    (chi, th) draws; reports max relative change (machine zero <=> dd=0).
    modes        :  rank B (physical/transverse), rank G (gauge), ker B, harmonic.
    """
    P, L = B.shape
    N = G.shape[1]
    M = B.T @ B
    ddBG = float(np.max(np.abs(B @ G))) if (P and L and N) else 0.0
    # numerical gauge-shift test dS/S
    rng = np.random.default_rng(seed)
    worst = 0.0
    for _ in range(n_random):
        th = rng.standard_normal(L)
        chi = rng.standard_normal(N)
        S0 = 0.5 * th @ (M @ th)
        thp = th + G @ chi
        S1 = 0.5 * thp @ (M @ thp)
        if S0 > 1e-12:
            worst = max(worst, abs(S1 - S0) / S0)
    tol = 1e-8
    rank_B = int(np.linalg.matrix_rank(B, tol=tol)) if (P and L) else 0
    rank_G = int(np.linalg.matrix_rank(G, tol=tol)) if (L and N) else 0
    ker_B = L - rank_B
    harmonic = ker_B - rank_G
    return {
        "label": label, "P": int(P), "L": int(L), "N": int(N),
        "closure_ddBG": ddBG,
        "gauge_dS_over_S_max": float(worst),
        "rank_B_physical": rank_B, "rank_G_gauge": rank_G,
        "ker_B": int(ker_B), "harmonic": int(harmonic),
        "gauge_fraction": float(rank_G / L) if L else float("nan"),
        "physical_fraction": float(rank_B / L) if L else float("nan"),
    }


# ====================================================================== #
# Stage 0 -- positive control: 4D lattice incidence must reproduce Maxwell
# ====================================================================== #
def lattice_incidence(shape):
    """Build B,G for the regular d-dim lattice from e5_core.regular_lattice, with the
    link tail/head reconstructed from link_id = site*d + mu.  Returns same tuple as
    loop_incidence so gauge_metrics applies unchanged."""
    L, pl, ps = regular_lattice(shape)
    shape = tuple(int(s) for s in shape)
    d = len(shape)
    n_sites = int(np.prod(shape))
    coords = np.array(np.unravel_index(np.arange(n_sites), shape)).T   # (n_sites,d)
    # tail/head node for every link id = site*d + mu
    tail = np.empty(L, np.int64)
    head = np.empty(L, np.int64)
    for s in range(n_sites):
        for mu in range(d):
            c = coords[s].copy()
            c[mu] = (c[mu] + 1) % shape[mu]
            lid = s * d + mu
            tail[lid] = s
            head[lid] = int(np.ravel_multi_index(c, shape))
    P = pl.shape[0]
    B = np.zeros((P, L))
    for p in range(P):
        for j in range(4):
            B[p, pl[p, j]] += ps[p, j]
    G = np.zeros((L, n_sites))
    for lid in range(L):
        G[lid, tail[lid]] -= 1.0
        G[lid, head[lid]] += 1.0
    return B, G, None, n_sites, L


# ====================================================================== #
# Hasse-link membership of B3 cell edges (the gauge-substrate diagnostic)
# ====================================================================== #
def hasse_membership(cells, g):
    """Fraction of the cells' undirected sides that are Hasse LINKS of g (= the gauge
    substrate E5/E6 use).  cells = (P,4) quads (i,k,j,l) -> sides {i,k},{k,j},{j,l},{l,i}.
    Also returns the fraction of CELLS all four of whose sides are links."""
    link_set = set()
    for a, b in g.edges:
        link_set.add((int(a), int(b)))            # edges stored lo<hi
    cells = np.asarray(cells, np.int64)
    side_hit = 0
    side_tot = 0
    full_cells = 0
    for q in cells:
        i, k, j, l = (int(x) for x in q)
        sides = [(i, k), (k, j), (j, l), (l, i)]
        hits = 0
        for u, v in sides:
            if u == v:
                continue
            lo, hi = (u, v) if u < v else (v, u)
            side_tot += 1
            if (lo, hi) in link_set:
                side_hit += 1
                hits += 1
        if hits == 4:
            full_cells += 1
    return {
        "side_link_fraction": float(side_hit / side_tot) if side_tot else float("nan"),
        "n_sides": int(side_tot),
        "cells_all4_links_fraction": float(full_cells / len(cells)) if len(cells) else float("nan"),
        "n_cells": int(len(cells)),
    }


CELL_CAP = 1500          # cap cells so dense incidence/SVD stays feasible (memory+time)


def build_cells(pts, anchor, seed, null=False):
    """B3 future-cone cells (anchor='spacelike') or the kinematic null (random apices),
    plus the Hasse link graph g for membership checks."""
    g, C = causal_link_graph(pts, return_relation=True)
    V = future_cone_cells(C, anchor=anchor, seed=seed,
                          max_pairs=CELL_CAP, max_cells=CELL_CAP)
    if null and V.shape[0]:
        rng = np.random.default_rng(7 * seed + 1)
        Vn = V.copy()
        Vn[:, 1] = rng.integers(0, g.n, size=V.shape[0])   # random apex k
        Vn[:, 3] = rng.integers(0, g.n, size=V.shape[0])   # random apex l
        V = Vn
    return V, g


def main():
    t0 = time.time()
    print("=" * 78)
    print("B3b -- Stage 0 (positive control + null) + Stage 1 (gauge closure)  [BLOCKING]")
    print("=" * 78)

    out = {"campaign": "FOTON_B3B4", "experiment": "B3b_closure_gauge",
           "rho": RHO, "stages_run": "0+1 (gauge gate only; 2/3 not run)"}

    # ---------- Stage 0: positive control (4D lattice = Maxwell) ----------
    Bl, Gl, _, Nl, Ll = lattice_incidence((4, 4, 4, 4))
    ctrl = gauge_metrics(Bl, Gl, "lattice_4D_Maxwell", n_random=200, seed=1)
    expected_gauge = (Nl - 1) / Ll       # connected lattice: rank G = N_sites - 1
    ctrl["expected_gauge_modes"] = int(Nl - 1)
    ctrl["expected_gauge_fraction"] = float(expected_gauge)
    ctrl_pass = (ctrl["closure_ddBG"] < 1e-9
                 and abs(ctrl["rank_G_gauge"] - (Nl - 1)) <= 1)
    out["stage0_positive_control"] = ctrl
    out["stage0_control_pass"] = bool(ctrl_pass)
    print(f"  [Stage0 lattice 4^4]  L={Ll} N={Nl}  ddBG={ctrl['closure_ddBG']:.2e}  "
          f"dS/S={ctrl['gauge_dS_over_S_max']:.2e}  gauge={ctrl['rank_G_gauge']}"
          f"(exp {Nl-1})  phys={ctrl['rank_B_physical']}  -> "
          f"{'PASS' if ctrl_pass else 'FAIL'}", flush=True)

    if not ctrl_pass:
        out["verdict_tag"] = "INVALID"
        out["verdict"] = ("INVALID: the incidence/coboundary machinery does NOT reproduce "
                          "4D Maxwell (closure or gauge-mode count wrong); reconstruction "
                          "untrustworthy, no gauge claim on B3 cells is valid.")
        _finish(out, t0)
        return 0

    # ---------- Stage 1: closure + gauge on B3 cells vs kinematic null ----------
    Ns = [400, 800]
    sig_rows, null_rows, hasse_rows = [], [], []
    for N in Ns:
        L = (N / RHO) ** 0.25
        rng = np.random.default_rng(100 + N)
        pts = sprinkle_box(RHO, [(0.0, L)] * 4, rng)
        Vs, g = build_cells(pts, "spacelike", seed=1, null=False)
        Vn, _ = build_cells(pts, "spacelike", seed=1, null=True)
        Bs, Gs, _, _, _ = loop_incidence(Vs)
        Bn, Gn, _, _, _ = loop_incidence(Vn)
        ms = gauge_metrics(Bs, Gs, f"spacelike_N{N}", n_random=400, seed=2)
        mn = gauge_metrics(Bn, Gn, f"null_N{N}", n_random=400, seed=3)
        hm = hasse_membership(Vs, g)
        print(f"             (cells: signal P={Vs.shape[0]} null P={Vn.shape[0]})",
              flush=True)
        ms["N"] = N; mn["N"] = N; hm["N"] = N
        sig_rows.append(ms); null_rows.append(mn); hasse_rows.append(hm)
        print(f"  [Stage1 N={N:4d}] SIGNAL ddBG={ms['closure_ddBG']:.2e} "
              f"dS/S={ms['gauge_dS_over_S_max']:.2e} gauge_frac={ms['gauge_fraction']:.3f} "
              f"phys_frac={ms['physical_fraction']:.3f} | side_link_frac="
              f"{hm['side_link_fraction']:.4f} all4={hm['cells_all4_links_fraction']:.4f}",
              flush=True)
        print(f"             NULL   ddBG={mn['closure_ddBG']:.2e} "
              f"dS/S={mn['gauge_dS_over_S_max']:.2e} gauge_frac={mn['gauge_fraction']:.3f} "
              f"phys_frac={mn['physical_fraction']:.3f}", flush=True)

    out["stage1_signal"] = sig_rows
    out["stage1_null"] = null_rows
    out["stage1_hasse"] = hasse_rows

    # ---------- verdict ----------
    sig = sig_rows[-1]; nul = null_rows[-1]; hm = hasse_rows[-1]
    closure_ok = sig["closure_ddBG"] < 1e-9 and sig["gauge_dS_over_S_max"] < 1e-9
    # is the closure/gauge "pass" reproduced by the kinematic null? (=> non-discriminating)
    null_also_passes = nul["closure_ddBG"] < 1e-9 and nul["gauge_dS_over_S_max"] < 1e-9
    # do the cells live on the gauge (Hasse-link) substrate at all?
    on_substrate = hm["side_link_fraction"] > 0.5     # majority of sides are links
    # does the causal signal carry a physical sector the null lacks?
    phys_gap = sig["physical_fraction"] - nul["physical_fraction"]

    if not closure_ok:
        tag = "MORTE_B3b_NOGAUGE"
        verdict = (
            f"MORTE (closure fails): the future-cone 2-complex does NOT close "
            f"(ddBG={sig['closure_ddBG']:.2e} or dS/S={sig['gauge_dS_over_S_max']:.2e} "
            f"above machine zero); dd != 0 means no gauge field. Future-cone cells are "
            f"spacelike structure without gauge character. Photon channel -> [FRONTEIRA].")
    elif null_also_passes and not on_substrate:
        tag = "MORTE_B3b_NOGAUGE"
        verdict = (
            f"MORTE (gauge gate non-discriminating + off-substrate): closure ddBG="
            f"{sig['closure_ddBG']:.2e} and gauge dS/S={sig['gauge_dS_over_S_max']:.2e} are "
            f"machine zero -- BUT this is AUTOMATIC for any set of closed quads: the B3 "
            f"KINEMATIC NULL (random apices) gives the SAME machine zero "
            f"(ddBG={nul['closure_ddBG']:.2e}, dS/S={nul['gauge_dS_over_S_max']:.2e}). The "
            f"closure/gauge-invariance 'pass' carries no information (lesson B3/B4: a pass "
            f"the null reproduces is not evidence). Decisively, only "
            f"{100*hm['side_link_fraction']:.1f}% of the cells' sides are Hasse LINKS "
            f"({100*hm['cells_all4_links_fraction']:.1f}% of cells have all four sides as "
            f"links): the future-cone cells do NOT live on the link sector whose gauge "
            f"field E6_1 validated -- they are a relation complex, not the gauge complex. "
            f"The future-cone construction does not furnish a genuine gauge 2-complex; "
            f"frac_B=0.84 was spacelike structure, not a photon. Channel 'cones futuros' "
            f"-> [FRONTEIRA]; B4 Bianchi-I genuine = the last door. Stages 2/3 NOT run "
            f"(blocked by the gate, as pre-registered).")
    elif on_substrate and phys_gap > 0.05:
        tag = "GATE_GREEN_B3b"
        verdict = (
            f"GATE GREEN (proceed to Stage 2): closure exact (ddBG={sig['closure_ddBG']:.2e}, "
            f"dS/S={sig['gauge_dS_over_S_max']:.2e}); {100*hm['side_link_fraction']:.1f}% of "
            f"sides are Hasse links (on the gauge substrate) and the causal signal carries a "
            f"physical sector the null lacks (phys_frac {sig['physical_fraction']:.3f} vs "
            f"{nul['physical_fraction']:.3f}, gap {phys_gap:.3f}). The future-cone 2-complex "
            f"supports a non-trivial gauge redundancy. Stage 2 (polarisation lock to k-hat) "
            f"is now warranted.")
    else:
        tag = "MORTE_B3b_NOGAUGE"
        verdict = (
            f"MORTE (ambiguous gauge content, conservative branch): closure holds "
            f"(ddBG={sig['closure_ddBG']:.2e}) but is reproduced by the null and the cells "
            f"are largely off the Hasse-link substrate (side_link_frac="
            f"{hm['side_link_fraction']:.3f}) with no clear physical-sector gap over the null "
            f"(phys_gap={phys_gap:.3f}). Per the golden rule (doubt -> conservative), the "
            f"future-cone construction does not establish a genuine gauge field. "
            f"Channel -> [FRONTEIRA]. Stages 2/3 NOT run.")

    out["verdict_tag"] = tag
    out["verdict"] = verdict
    out["closure_ok"] = bool(closure_ok)
    out["null_also_passes"] = bool(null_also_passes)
    out["on_hasse_substrate"] = bool(on_substrate)
    out["physical_fraction_gap_signal_minus_null"] = float(phys_gap)
    _finish(out, t0)
    return 0


def _finish(out, t0):
    out["runtime_s"] = time.time() - t0
    (HERE / "b3b_closure.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"VERDICT [{out['verdict_tag']}]:\n{out['verdict']}")
    print(f"[{out['runtime_s']:.0f}s] -> b3b_closure.json")


if __name__ == "__main__":
    raise SystemExit(main())
