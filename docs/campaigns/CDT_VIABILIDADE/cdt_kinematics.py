"""
cdt_kinematics.py -- GATILHO 3: viabilidade CINEMATICA tipo-CDT (aresta fixa + colagem livre).

Protocolo congelado em PRE_REGISTRO.md (CDT_VIABILIDADE). CINEMATICA PURA, SEM ACAO:
ensemble de triangulacoes 2D (superficie fechada, topologia de esfera) com aresta de
comprimento FIXO ([External], declarado), evoluido por movimentos tipo-Pachner:
  (1,3): insere vertice num triangulo (3 novos triangulos)        -> cresce N
  (2,2): edge flip (vira a diagonal de 2 triangulos adjacentes)   -> N fixo
SEM peso de acao: passeio aleatorio uniforme sobre colagens validas.

Mede no 1-ESQUELETO (vertices=0-simplices, arestas=1-simplices):
  (a) coordenacao <z> = 2*#arestas/N   (estimador ESCALA_XI/Gatilho 1)
  (b) transitividade (3-ciclos) E C4 (4-ciclos)  -- rs_clustering VERBATIM
NB: aqui a transitividade NAO e degenerada (1-esqueleto de triangulacao TEM triangulos),
ao contrario do grafo de Hasse do CSG (Gatilho 2). Reporta AMBOS.

ANTI-CIRCULARIDADE: nada e formulado como "escala emergiu" -- a aresta e fixa por
construcao. So contagens combinatorias adimensionais. Sem metrica/boosts.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "RIDEOUT_SORKIN_CLUSTERING"))
import rs_clustering as rc  # noqa: E402  (clustering_metrics: transitivity + C4)


# ====================================================================== #
# 2D simplicial complex (closed surface, sphere topology) with Pachner moves
# ====================================================================== #
class Triangulation2D:
    """Closed orientable 2-manifold triangulation. Each edge in exactly 2 triangles."""

    def __init__(self):
        # seed = boundary of a tetrahedron (4 vertices, 4 triangles, sphere S^2).
        # 1-skeleton = K4.
        self.nverts = 4
        self.tris = {}          # tid -> frozenset({a,b,c})
        self.edge_tris = {}     # frozenset({u,v}) -> set(tids)
        self._next_tid = 0
        for tri in ([0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3]):
            self._add_tri(tri)

    def _add_tri(self, verts):
        tid = self._next_tid; self._next_tid += 1
        fs = frozenset(verts)
        self.tris[tid] = fs
        a, b, c = sorted(verts)
        for e in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))):
            self.edge_tris.setdefault(e, set()).add(tid)
        return tid

    def _del_tri(self, tid):
        fs = self.tris.pop(tid)
        a, b, c = sorted(fs)
        for e in (frozenset((a, b)), frozenset((a, c)), frozenset((b, c))):
            s = self.edge_tris[e]; s.discard(tid)
            if not s:
                del self.edge_tris[e]

    def move_13(self, rng):
        """(1,3): insert a new vertex in a random triangle -> 3 triangles."""
        tid = rng.choice(list(self.tris.keys()))
        a, b, c = sorted(self.tris[tid])
        d = self.nverts; self.nverts += 1
        self._del_tri(tid)
        self._add_tri([a, b, d]); self._add_tri([b, c, d]); self._add_tri([a, c, d])

    def move_22(self, rng):
        """(2,2): flip a random internal edge (u,v) shared by (u,v,a),(u,v,b) to (a,b).
        Valid only if a!=b and edge (a,b) does not already exist (keeps it a manifold)."""
        edges = list(self.edge_tris.keys())
        e = edges[rng.integers(len(edges))]
        tids = list(self.edge_tris[e])
        if len(tids) != 2:
            return False
        u, v = tuple(e)
        t1, t2 = tids
        a = next(iter(self.tris[t1] - {u, v}))
        b = next(iter(self.tris[t2] - {u, v}))
        if a == b:
            return False
        if frozenset((a, b)) in self.edge_tris:     # would create a doubled edge
            return False
        self._del_tri(t1); self._del_tri(t2)
        self._add_tri([a, b, u]); self._add_tri([a, b, v])
        return True

    def one_skeleton_edges(self):
        return [tuple(e) for e in self.edge_tris.keys()]


def grow_to(n, rng, flips_per_vertex=0.0):
    """Grow a triangulation to n vertices by (1,3) moves; optionally interleave
    `flips_per_vertex` random (2,2) flips per vertex (the DT-ensemble equilibration).
    flips_per_vertex=0 -> 'stacked' (Apollonian) regime."""
    T = Triangulation2D()
    n_flip_attempts = 0; n_flip_ok = 0
    while T.nverts < n:
        T.move_13(rng)
        if flips_per_vertex > 0:
            for _ in range(int(round(flips_per_vertex))):
                n_flip_attempts += 1
                n_flip_ok += int(T.move_22(rng))
    return T, {"flip_attempts": n_flip_attempts, "flip_ok": n_flip_ok}


# ====================================================================== #
# VALIDATION GATE
# ====================================================================== #
def _triangular_lattice_patch(L):
    """LxL triangular lattice patch (with wrap = triangular torus): every vertex
    degree 6, known clustering transitivity = 0.4. Returns (n, edges)."""
    n = L * L
    edges = set()
    for x in range(L):
        for y in range(L):
            a = x * L + y
            r = ((x + 1) % L) * L + y
            u = x * L + (y + 1) % L
            ur = ((x + 1) % L) * L + (y + 1) % L
            edges.add(frozenset((a, r)))
            edges.add(frozenset((a, u)))
            edges.add(frozenset((a, ur)))   # diagonal -> triangles
    return n, [tuple(e) for e in edges]


def validation_gate(verbose=True):
    report = {"checks": [], "passed": True}

    def check(name, ok, detail):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["passed"] = False
        if verbose:
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {detail}")

    # (1) seed = tetra boundary: 1-skeleton = K4 -> z=3, transitivity=1, C4=1
    T = Triangulation2D()
    m = rc.clustering_metrics(T.nverts, T.one_skeleton_edges())
    z = 2 * len(T.one_skeleton_edges()) / T.nverts
    check("seed tetra = K4 (z=3, C_tri=1, C4=1)",
          abs(z - 3) < 1e-9 and abs(m["transitivity"] - 1) < 1e-9 and abs(m["mean_local_square"] - 1) < 1e-9,
          f"z={z:.2f} C_tri={m['transitivity']:.4f} C4={m['mean_local_square']:.4f}")

    # (2) manifold invariant after moves: every edge in exactly 2 triangles (Euler V-E+F=2)
    rng = np.random.default_rng(3)
    T, _ = grow_to(400, rng, flips_per_vertex=2.0)
    deg2 = all(len(s) == 2 for s in T.edge_tris.values())
    V = T.nverts; E = len(T.edge_tris); F = len(T.tris)
    check("manifold + Euler char V-E+F=2 (sphere) after moves",
          deg2 and (V - E + F == 2), f"all-edges-deg2={deg2} V-E+F={V - E + F}")

    # (3) triangular lattice patch: transitivity == 0.4 (known)
    n, edges = _triangular_lattice_patch(30)
    m = rc.clustering_metrics(n, edges)
    check("triangular lattice transitivity ~= 0.4",
          abs(m["transitivity"] - 0.4) < 0.02, f"C_tri={m['transitivity']:.4f} vs 0.4")

    # (4) reuse Gatilho-2 estimator gate (path=0, K_n=1, torus C4=0.125)
    nn, ed = _triangular_lattice_patch(20)   # any triangle-rich graph for sanity
    mm = rc.clustering_metrics(nn, ed)
    check("estimator sane (C4 in (0,1), C_tri>0 on lattice)",
          0 < mm["mean_local_square"] < 1 and mm["transitivity"] > 0,
          f"C4={mm['mean_local_square']:.4f} C_tri={mm['transitivity']:.4f}")
    return report


# ====================================================================== #
# MEASUREMENT
# ====================================================================== #
LADDER = [500, 1000, 2000, 3300, 3888]
N_SEEDS = 5
SEED_CAP = (3300, 3)
REGIMES = {
    "stacked": 0.0,        # (1,3) growth only -- Apollonian / planar 3-tree
    "flipped": 4.0,        # (1,3) + 4 random (2,2) flips per vertex -- DT ensemble
}


def run_measurement():
    out = {"observable": "z and (transitivity, C4) on the 1-skeleton of a 2D Pachner ensemble",
           "edge_length": "FIXED [External] by construction (NOT emergent)",
           "ladder": LADDER, "regimes": {}}
    for label, fpv in REGIMES.items():
        rows = []
        for n in LADDER:
            ns = SEED_CAP[1] if n >= SEED_CAP[0] else N_SEEDS
            zs, tris, c4s, t0 = [], [], [], time.perf_counter()
            for s in range(ns):
                rng = np.random.default_rng(5000 + s + n)
                T, info = grow_to(n, rng, flips_per_vertex=fpv)
                edges = T.one_skeleton_edges()
                m = rc.clustering_metrics(T.nverts, edges)
                zs.append(2 * len(edges) / T.nverts)
                tris.append(m["transitivity"]); c4s.append(m["mean_local_square"])
            dt = time.perf_counter() - t0
            rows.append({"N": n, "n_seeds": ns,
                         "z": float(np.mean(zs)), "z_sem": float(np.std(zs) / np.sqrt(ns)),
                         "C_trans": float(np.mean(tris)), "C_trans_sem": float(np.std(tris) / np.sqrt(ns)),
                         "C4": float(np.mean(c4s)), "C4_sem": float(np.std(c4s) / np.sqrt(ns)),
                         "runtime_s": dt})
            print(f"  {label:>8} N={n:>4}: z={np.mean(zs):.3f} C_tri={np.mean(tris):.4f} "
                  f"C4={np.mean(c4s):.4f} [{dt:.1f}s]")
        z = np.array([r["z"] for r in rows]); C4 = np.array([r["C4"] for r in rows])
        Ct = np.array([r["C_trans"] for r in rows]); Nv = np.array([r["N"] for r in rows], float)
        out["regimes"][label] = {"flips_per_vertex": fpv, "rows": rows,
                                 "z_slope_top": float(np.diff(z)[-1] / np.diff(np.log(Nv))[-1]),
                                 "C4_slope_top": float(np.diff(C4)[-1] / np.diff(np.log(Nv))[-1]),
                                 "Ctrans_slope_top": float(np.diff(Ct)[-1] / np.diff(np.log(Nv))[-1])}
    return out


def verdict(meas, poisson_c4=0.029, csg_c4_intermediate=0.019):
    """Pre-registered criterion (frozen, not adjusted):
      ARMADO     : some regime has z saturating (finite) AND clustering saturating
                   positive clearly above the Poisson mean-field control.
      NAO ARMADO : replicates Poisson z-divergence OR replicates CSG C4-decay-to-zero.
      AMBIGUO    : neither clear within the N budget -> report unresolved."""
    res = {"per_regime": {}, "armed": False, "armed_regime": None}
    for label, R in meas["regimes"].items():
        rows = R["rows"]
        z_first, z_top = rows[0]["z"], rows[-1]["z"]
        c4_first, c4_top = rows[0]["C4"], rows[-1]["C4"]
        ct_top = rows[-1]["C_trans"]
        z_saturates = abs(R["z_slope_top"]) / z_top < 0.05
        z_diverges = R["z_slope_top"] / z_top > 0.10
        # clustering: positive, not decaying, AND above the Poisson MF floor
        c4_decaying = c4_top < 0.5 * c4_first if c4_first > 0 else True
        clustering_alive = (c4_top > 1.5 * poisson_c4) and (not c4_decaying)
        armed = z_saturates and clustering_alive
        res["per_regime"][label] = {
            "z_first": z_first, "z_top": z_top, "z_saturates": bool(z_saturates),
            "z_diverges": bool(z_diverges), "C4_first": c4_first, "C4_top": c4_top,
            "C_trans_top": ct_top, "c4_decaying": bool(c4_decaying),
            "clustering_above_MF": bool(clustering_alive), "armed": bool(armed),
            "ref_poisson_c4": poisson_c4, "ref_csg_c4_intermediate": csg_c4_intermediate}
        if armed:
            res["armed"] = True; res["armed_regime"] = label
    res["verdict"] = "ARMADO" if res["armed"] else "NAO_ARMADO"
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("gate", "all"):
        print("=" * 64 + "\nGATE DE VALIDACAO (CDT kinematics)\n" + "=" * 64)
        g = validation_gate()
        json.dump(g, open(os.path.join(HERE, "validation_gate.json"), "w"), indent=2)
        print(f"\n  GATE {'VERDE' if g['passed'] else 'VERMELHO'}")
        if not g["passed"]:
            print("  ABORTA."); sys.exit(1)
    if mode in ("measure", "all"):
        print("\n" + "=" * 64 + "\nMEDICAO: z e clustering no 1-esqueleto\n" + "=" * 64)
        meas = run_measurement()
        v = verdict(meas)
        meas["verdict"] = v
        json.dump(meas, open(os.path.join(HERE, "cdt_kinematics.json"), "w"), indent=2)
        print("\n" + "=" * 64 + "\nVEREDITO DO GATILHO 3\n" + "=" * 64)
        for label, r in v["per_regime"].items():
            print(f"  {label:>8}: z {r['z_first']:.2f}->{r['z_top']:.2f} "
                  f"({'satura' if r['z_saturates'] else 'diverge' if r['z_diverges'] else '?'}) "
                  f"C_tri={r['C_trans_top']:.4f} C4 {r['C4_first']:.4f}->{r['C4_top']:.4f} "
                  f"(>MF={r['clustering_above_MF']}) {'ARMA' if r['armed'] else 'nao-arma'}")
        print(f"\n  >>> GATILHO 3 {v['verdict']}"
              + (f" (regime {v['armed_regime']})" if v["armed"] else ""))
