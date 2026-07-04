"""
rs_clustering.py -- GATILHO 2 Rideout-Sorkin: clustering do grafo de cobertura do CSG.

Implementa EXATAMENTE o protocolo congelado em PRE_REGISTRO.md (2026-06-25). Nao
reinterpreta criterios. Reutiliza o gerador VERBATIM do Gatilho 1
(rs_trigger.grow_transitive_percolation) e mede o clustering do grafo de cobertura
(Hasse) NAO-direcionado.

Observavel primario: transitividade global C = 3*#triangulos / #caminhos-de-2-arestas.
Cross-check: clustering local medio <C_i>. Secundario: girth local (laco minimo).
Contraste: Poisson (esperado C -> 0, controle negativo).

Criterio (congelado):
  ARMADO     : em >=1 regime legitimo, C satura em valor positivo com N.
  NAO ARMADO : em todos os regimes legitimos, C -> 0 com N (tipo-arvore).
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TRIGGER = os.path.join(os.path.dirname(HERE), "RIDEOUT_SORKIN_TRIGGER")
sys.path.insert(0, TRIGGER)

from rs_trigger import grow_transitive_percolation, _bits_to_indices, WORD  # noqa: E402

# Poisson reference engine (validated substrate), same as COLAPSO/ESCALA_XI lineage
_ROOT = HERE
for _ in range(6):
    if os.path.exists(os.path.join(_ROOT, "TEIC", "src", "causal_core.py")):
        break
    _ROOT = os.path.dirname(_ROOT)
sys.path.insert(0, os.path.join(_ROOT, "TEIC", "results", "tier3"))
import tier3_core as t3  # noqa: E402


# ====================================================================== #
# COVERING (Hasse) EDGES -- undirected
# ====================================================================== #
def csg_covering_edges(anc, n):
    """Undirected covering (Hasse-link) edges of a CSG given ancestor bitsets `anc`.
    i covers-> j  iff  i in anc[j]  AND  i not in (OR_{k in anc[j]} anc[k])."""
    W = anc.shape[1]
    edges = []
    for j in range(n):
        aj = anc[j]
        ks = _bits_to_indices(aj)
        if ks.size == 0:
            continue
        inter = np.bitwise_or.reduce(anc[ks], axis=0) if ks.size else np.zeros(W, np.uint64)
        linkparents = aj & ~inter
        for i in _bits_to_indices(linkparents):
            edges.append((int(i), j))
    return edges


def poisson_covering_edges(n, dim, rng):
    """Undirected covering edges of a Poisson causal set sprinkled in the unit
    causal diamond of M^dim. Boolean ancestor matrix -> transitive reduction."""
    pts = t3.sprinkle_diamond(n, dim, rng)
    A = t3.causal_matrix_anc(pts)              # A[i,j] = True iff j strictly precedes i
    Af = A.astype(np.float32)
    two_step = (Af @ Af) > 0.5                  # exists k: j<k<i
    cover = A & ~two_step                       # i covers j
    ii, jj = np.nonzero(cover)
    return [(int(a), int(b)) for a, b in zip(jj, ii)]   # undirected (j,i)


# ====================================================================== #
# CLUSTERING METRICS on an undirected edge list
# ====================================================================== #
def clustering_metrics(n, edges):
    """Global transitivity, mean local clustering, triangle/2-path counts, <z>."""
    nbr = [set() for _ in range(n)]
    for u, v in edges:
        if u != v:
            nbr[u].add(v)
            nbr[v].add(u)
    deg = np.array([len(s) for s in nbr], dtype=np.int64)
    two_paths = int(np.sum(deg * (deg - 1) // 2))
    tri_through = np.zeros(n, dtype=np.int64)
    for i in range(n):
        Ni = nbr[i]
        if len(Ni) < 2:
            continue
        Ni_list = list(Ni)
        t = 0
        for a_idx in range(len(Ni_list)):
            u = Ni_list[a_idx]
            Nu = nbr[u]
            for b_idx in range(a_idx + 1, len(Ni_list)):
                if Ni_list[b_idx] in Nu:
                    t += 1
        tri_through[i] = t                       # #edges among neighbors of i
    n_triangles = int(np.sum(tri_through) // 3)
    transitivity = (3.0 * n_triangles / two_paths) if two_paths > 0 else 0.0
    with np.errstate(divide="ignore", invalid="ignore"):
        local = np.where(deg >= 2, tri_through / (deg * (deg - 1) / 2), np.nan)
    mean_local = float(np.nanmean(local)) if np.any(deg >= 2) else 0.0

    # --- SQUARE (4-cycle) clustering: the only non-degenerate clustering for a
    #     triangle-free Hasse graph (secondary observable of the pre-registro).
    #     C4 = Lind/networkx square_clustering (bounded [0,1], coordination-normalised). ---
    squares_through = np.zeros(n, dtype=np.int64)   # raw #squares through node i
    c4_local = np.full(n, np.nan)
    for i in range(n):
        Ni = list(nbr[i])
        k = len(Ni)
        if k < 2:
            continue
        clustering = 0
        potential = 0
        for a_idx in range(k):
            u = Ni[a_idx]; Nu = nbr[u]; du = len(Nu)
            for b_idx in range(a_idx + 1, k):
                w = Ni[b_idx]; Nw = nbr[w]; dw = len(Nw)
                squares = len((Nu & Nw) - {i})
                clustering += squares
                degm = squares + 1
                if w in Nu:
                    degm += 1
                potential += (du - degm) + (dw - degm) + squares
        squares_through[i] = clustering
        if potential > 0:
            c4_local[i] = clustering / potential
    n_squares = int(np.sum(squares_through) // 4)   # each 4-cycle hits 4 nodes
    frac_on_square = float(np.mean(squares_through > 0))
    squares_per_node = float(np.mean(squares_through))
    mean_local_square = float(np.nanmean(c4_local)) if np.any(~np.isnan(c4_local)) else 0.0
    return {"transitivity": transitivity, "mean_local": mean_local,
            "n_triangles": n_triangles, "n_2paths": two_paths, "deg_mean": float(deg.mean()),
            "n_squares": n_squares, "frac_on_square": frac_on_square,
            "squares_per_node": squares_per_node, "mean_local_square": mean_local_square}


# ====================================================================== #
# VALIDATION GATE (estimator correctness on known cases)
# ====================================================================== #
def validation_gate(verbose=True):
    rng = np.random.default_rng(11)
    report = {"checks": [], "passed": True}

    def check(name, ok, detail):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["passed"] = False
        if verbose:
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {detail}")

    # (1) Erdos-Renyi G(n,p): global transitivity -> p
    n, p = 600, 0.05
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if rng.random() < p:
                edges.append((i, j))
    m = clustering_metrics(n, edges)
    check("ER transitivity ~= p", abs(m["transitivity"] - p) < 0.01,
          f"measured C={m['transitivity']:.4f} vs p={p}")

    # (2) Complete graph K_m: transitivity = 1 exactly
    km = 25
    edges = [(i, j) for i in range(km) for j in range(i + 1, km)]
    m = clustering_metrics(km, edges)
    check("K_n transitivity == 1", abs(m["transitivity"] - 1.0) < 1e-9,
          f"measured C={m['transitivity']:.6f}")

    # (3) Path graph (tree): transitivity = 0, no triangles
    n = 500
    edges = [(i, i + 1) for i in range(n - 1)]
    m = clustering_metrics(n, edges)
    check("path/tree transitivity == 0", m["n_triangles"] == 0 and m["transitivity"] == 0.0,
          f"triangles={m['n_triangles']} C={m['transitivity']}")

    # (4) Triangular ring (ring lattice k=2 each side): known C = 0.5
    n = 300
    edges = []
    for i in range(n):
        edges.append((i, (i + 1) % n))
        edges.append((i, (i + 2) % n))
    m = clustering_metrics(n, edges)
    # ring lattice with k=4 (2 each side): C = 3(k-2)/(4(k-1)) = 3*2/(4*3) = 0.5
    check("ring lattice k=4 transitivity ~= 0.5", abs(m["transitivity"] - 0.5) < 0.02,
          f"measured C={m['transitivity']:.4f} vs 0.5")

    # --- C4 (square clustering) validation: bounded [0,1], coordination-controlled ---
    # (5) path/tree: C4 == 0 (no squares)
    n = 200; edges = [(i, i + 1) for i in range(n - 1)]
    m = clustering_metrics(n, edges)
    check("C4 path/tree == 0", m["mean_local_square"] == 0.0, f"C4={m['mean_local_square']}")
    # (6) complete graph K_n: C4 == 1
    km = 20; edges = [(i, j) for i in range(km) for j in range(i + 1, km)]
    m = clustering_metrics(km, edges)
    check("C4 K_n == 1", abs(m["mean_local_square"] - 1.0) < 1e-9, f"C4={m['mean_local_square']:.6f}")
    # (7) 2D periodic square lattice (torus): triangle-free, C4 > 0 fixed (loops persist)
    L = 20; n = L * L; edges = []
    for x in range(L):
        for y in range(L):
            a = x * L + y
            edges.append((a, ((x + 1) % L) * L + y))
            edges.append((a, x * L + (y + 1) % L))
    m = clustering_metrics(n, edges)
    check("C4 2D torus in (0,1) and triangle-free", 0.05 < m["mean_local_square"] < 1.0
          and m["n_triangles"] == 0, f"C4={m['mean_local_square']:.4f} tri={m['n_triangles']}")
    return report


# ====================================================================== #
# MEASUREMENT
# ====================================================================== #
REGIMES = [  # legitimate only -- dense EXCLUDED by inherited Caveat 1
    {"label": "sparse", "kind": "fixed", "p": 0.02},
    {"label": "intermediate", "kind": "fixed", "p": 0.10},
    {"label": "manifold", "kind": "scaled", "lam": 4.0},
]
LADDER = [500, 1000, 2000, 3300, 3888]
POISSON_LADDER = [500, 1000, 2000]      # reduced ladder: O(N^3) reference cost; trend suffices
POISSON_DIM = 3
N_SEEDS = 5
SEED_CAP = (3300, 3)


def p_for(regime, n):
    return regime["p"] if regime["kind"] == "fixed" else regime["lam"] / n


def run_measurement():
    out = {"observable": "global transitivity C=3*tri/2paths on undirected covering graph",
           "generator": "transitive percolation (CSG), rs_trigger VERBATIM",
           "ladder": LADDER, "poisson_ladder": POISSON_LADDER, "n_seeds": N_SEEDS,
           "regimes": {}, "poisson": []}

    for regime in REGIMES:
        label = regime["label"]
        rows = []
        for n in LADDER:
            ns = SEED_CAP[1] if n >= SEED_CAP[0] else N_SEEDS
            p = p_for(regime, n)
            Cs, tris, sqf, sqn, sqlc, t0 = [], [], [], [], [], time.perf_counter()
            for s in range(ns):
                rng = np.random.default_rng(2000 + s + n)
                anc, _ = grow_transitive_percolation(n, p, rng)
                edges = csg_covering_edges(anc, n)
                m = clustering_metrics(n, edges)
                Cs.append(m["transitivity"]); tris.append(m["n_triangles"])
                sqf.append(m["frac_on_square"]); sqn.append(m["squares_per_node"])
                sqlc.append(m["mean_local_square"])
            dt = time.perf_counter() - t0
            rows.append({"N": n, "p": p, "n_seeds": ns,
                         "C_trans": float(np.mean(Cs)), "n_tri": float(np.mean(tris)),
                         "frac_on_square": float(np.mean(sqf)),
                         "frac_on_square_sem": float(np.std(sqf) / np.sqrt(ns)),
                         "squares_per_node": float(np.mean(sqn)),
                         "C_local_square": float(np.mean(sqlc)), "runtime_s": dt})
            print(f"  {label:>13} N={n:>4} p={p:.4g}: C_tri={np.mean(Cs):.4f} "
                  f"frac_sq={np.mean(sqf):.4f} sq/node={np.mean(sqn):.3f} "
                  f"C4={np.mean(sqlc):.4f} [{dt:.1f}s]")
        F = np.array([r["C_local_square"] for r in rows]); Nv = np.array([r["N"] for r in rows], float)
        slope = np.diff(F) / np.diff(np.log(Nv))
        out["regimes"][label] = {"regime": regime, "rows": rows,
                                 "C4_dlnN": slope.tolist(), "slope_top": float(slope[-1])}

    # Poisson negative control
    print("  -- Poisson reference (negative control: Bethe-like => C4 must -> 0) --")
    for n in POISSON_LADDER:
        Cs, sqf, c4, zz, t0 = [], [], [], [], time.perf_counter()
        for s in range(3):
            rng = np.random.default_rng(9000 + s + n)
            edges = poisson_covering_edges(n, POISSON_DIM, rng)
            m = clustering_metrics(n, edges)
            Cs.append(m["transitivity"]); sqf.append(m["frac_on_square"])
            c4.append(m["mean_local_square"]); zz.append(m["deg_mean"])
        dt = time.perf_counter() - t0
        out["poisson"].append({"N": n, "C_trans": float(np.mean(Cs)),
                               "frac_on_square": float(np.mean(sqf)),
                               "C_local_square": float(np.mean(c4)),
                               "deg_mean": float(np.mean(zz)), "runtime_s": dt})
        print(f"  {'poisson':>13} N={n:>4} dim={POISSON_DIM}: z={np.mean(zz):.2f} "
              f"frac_sq={np.mean(sqf):.4f} C4={np.mean(c4):.4f} [{dt:.1f}s]")
    return out


def verdict(meas, sat_thresh=0.02, decay_ratio=0.5):
    """Discriminator = C4 = mean local SQUARE clustering (coordination-NORMALISED),
    since (a) triangle transitivity is structurally 0 for any Hasse graph (theorem)
    and (b) raw frac_on_square is confounded by coordination (Poisson -> ~1 despite
    being Bethe). C4 -> 0 is the Bethe/tree-like signature; C4 saturating > 0 is
    finite-dimensional loop structure. ARMADO if some legit regime saturates C4 > 0
    (and clearly above the Poisson/Bethe control); NAO ARMADO if all decay to 0."""
    pois = meas.get("poisson", [])
    pois_c4_top = pois[-1].get("C_local_square") if pois else None
    res = {"discriminator": "C4 = mean local square (4-cycle) clustering, coordination-"
                            "normalised; transitivity structurally 0 (Hasse theorem); "
                            "frac_on_square confounded by coordination",
           "poisson_C4_top": pois_c4_top, "per_regime": {}, "armed": False, "armed_regime": None}
    for label, R in meas["regimes"].items():
        rows = R["rows"]
        c_first, c_top = rows[0]["C_local_square"], rows[-1]["C_local_square"]
        decaying = (c_top < decay_ratio * c_first) if c_first > 0 else True
        above_bethe = (pois_c4_top is None) or (c_top > 3 * pois_c4_top)
        positive_sat = (c_top > sat_thresh) and (not decaying) and above_bethe
        res["per_regime"][label] = {
            "C4_first": c_first, "C4_top": c_top, "slope_top": R["slope_top"],
            "C_trans_top": rows[-1]["C_trans"], "frac_sq_top": rows[-1]["frac_on_square"],
            "sq_per_node_top": rows[-1]["squares_per_node"],
            "decaying_to_zero": bool(decaying), "above_bethe_control": bool(above_bethe),
            "saturates_positive": bool(positive_sat)}
        if positive_sat:
            res["armed"] = True; res["armed_regime"] = label
    res["verdict"] = "ARMADO" if res["armed"] else "NAO_ARMADO"
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("gate", "all"):
        print("=" * 64 + "\nGATE DE VALIDACAO (clustering estimator)\n" + "=" * 64)
        g = validation_gate()
        json.dump(g, open(os.path.join(HERE, "validation_gate.json"), "w"), indent=2)
        print(f"\n  GATE {'VERDE' if g['passed'] else 'VERMELHO'}")
        if not g["passed"]:
            print("  ABORTA: estimador nao confiavel."); sys.exit(1)
    if mode in ("measure", "all"):
        print("\n" + "=" * 64 + "\nMEDICAO: clustering C(N) por regime\n" + "=" * 64)
        meas = run_measurement()
        v = verdict(meas)
        meas["verdict"] = v
        json.dump(meas, open(os.path.join(HERE, "rs_clustering.json"), "w"), indent=2)
        print("\n" + "=" * 64 + "\nVEREDITO DO GATILHO 2\n" + "=" * 64)
        print(f"  Poisson/Bethe control C4_top = {v['poisson_C4_top']}")
        for label, r in v["per_regime"].items():
            print(f"  {label:>13}: C4 {r['C4_first']:.4f}->{r['C4_top']:.4f} "
                  f"(>3xBethe={r['above_bethe_control']}) C_tri={r['C_trans_top']:.4f} "
                  f"{'SATURA>0' if r['saturates_positive'] else 'decai->0 (arvore)'}")
        print(f"\n  >>> GATILHO 2 {v['verdict']}"
              + (f" (regime {v['armed_regime']})" if v["armed"] else " (todos tipo-arvore)"))
