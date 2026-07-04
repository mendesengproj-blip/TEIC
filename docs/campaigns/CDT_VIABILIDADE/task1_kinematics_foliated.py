"""
task1_kinematics_foliated.py — fecha o gatilho cinemático MEDINDO <z> e C4 no
1-esqueleto do CDT 2D FOLIADO de F1 (TEORIA_CDT), com os MESMOS estimadores dos
Gatilhos 1/2 (rs_clustering.clustering_metrics), e o TESTE DE TRIVIALIDADE de C4
(vs triangulação 2D genérica não-foliada).

Reuso (não reimplementação):
  - motor foliado validado: TEORIA_CDT/F1_acao/f1_cdt2d.py (gate G1: d_H=2)
  - estimador VERBATIM: RIDEOUT_SORKIN_CLUSTERING/rs_clustering.clustering_metrics
  - controle genérico não-foliado: cdt_kinematics.Triangulation2D (regime flipped/DT)
  - referências Poisson/CSG: cdt_kinematics.json / SYNTHESIS da fila

Anti-contaminação: rs_clustering/cdt_kinematics entram como ESTIMADOR/CONTROLE
(ferramenta de medição e benchmark), nunca como dado físico importado.
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)  # cdt_kinematics
sys.path.insert(0, os.path.join(HERE, "..", "RIDEOUT_SORKIN_CLUSTERING"))  # rs_clustering
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..",
                                "TEORIA_CDT", "F1_acao"))  # f1_cdt2d

import rs_clustering as rc          # noqa: E402
import cdt_kinematics as ck         # noqa: E402
from f1_cdt2d import CDT2D, UP, DOWN  # noqa: E402


# ---------------------------------------------------------------------------
# Reconstrução do 1-esqueleto (grafo de vértices) a partir da triângulo-adjacência
# ---------------------------------------------------------------------------
class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def _edge_corners(typ, which):
    """Para um triângulo de tipo `typ`, e a aresta `which` in {'C','L','R'},
    devolve (corner_baixo/esq, corner_cima/dir). Convenção:
      UP   corners: 0=esq-baixo,1=dir-baixo,2=ápice-cima
      DOWN corners: 0=esq-cima,1=dir-cima,2=ápice-baixo
    Tipo-tempo (L,R): devolve (corner_no_slice_baixo, corner_no_slice_cima).
    Espacial (C): devolve (corner_esq, corner_dir)."""
    if typ == UP:
        return {'C': (0, 1), 'L': (0, 2), 'R': (1, 2)}[which]
    else:  # DOWN: ápice (corner 2) está no slice BAIXO; 0,1 no slice cima
        return {'C': (0, 1), 'L': (2, 0), 'R': (2, 1)}[which]


def build_one_skeleton(g):
    """Devolve (nverts, edges) do 1-esqueleto + dict de validação."""
    N = g.N
    dsu = DSU(3 * N)

    def corner(i, c):
        return 3 * i + c

    for i in range(N):
        ti = g.typ[i]
        # aresta tipo-tempo R: compartilhada com j=nbR[i] (que é o L de j)
        j = int(g.nbR[i])
        tj = g.typ[j]
        ilo, iup = _edge_corners(ti, 'R')
        jlo, jup = _edge_corners(tj, 'L')
        dsu.union(corner(i, ilo), corner(j, jlo))   # ambos no slice baixo
        dsu.union(corner(i, iup), corner(j, jup))   # ambos no slice cima
        # aresta espacial C: compartilhada com k=nbC[i]
        k = int(g.nbC[i])
        tk = g.typ[k]
        il, ir = _edge_corners(ti, 'C')
        kl, kr = _edge_corners(tk, 'C')
        dsu.union(corner(i, il), corner(k, kl))     # esq<->esq
        dsu.union(corner(i, ir), corner(k, kr))     # dir<->dir

    # remapeia raízes para ids 0..V-1
    roots = {}
    vid = np.empty(3 * N, dtype=np.int64)
    for s in range(3 * N):
        r = dsu.find(s)
        if r not in roots:
            roots[r] = len(roots)
        vid[s] = roots[r]
    V = len(roots)

    # arestas: cada triângulo tem 3 arestas (C,L,R) -> par de vértices
    eset = set()
    for i in range(N):
        ti = g.typ[i]
        for which in ('C', 'L', 'R'):
            a, b = _edge_corners(ti, which)
            u = int(vid[3 * i + a]); w = int(vid[3 * i + b])
            if u != w:
                eset.add((u, w) if u < w else (w, u))
    edges = list(eset)
    val = dict(V=V, V_expected=int(g.ell.sum()),
               E=len(edges), E_expected=int(3 * N // 2),
               z_mean=round(2 * len(edges) / V, 4))
    return V, edges, val


# ---------------------------------------------------------------------------
# medição no CDT FOLIADO
# ---------------------------------------------------------------------------
def measure_foliated(Vtarget_verts, T, n_seeds=4, equil=1200, eps=0.02):
    lam = math.log(2.0)
    ell0 = Vtarget_verts // T
    Vt = 2 * ell0 * T  # triângulos
    zs, c4s, trs, valid = [], [], [], []
    for s in range(n_seeds):
        g = CDT2D(T, ell0, seed=100 + s)
        for _ in range(equil):
            g.sweep(lam, eps, Vt, ell_min=3)
        V, edges, val = build_one_skeleton(g)
        valid.append(val)
        m = rc.clustering_metrics(V, edges)
        zs.append(m['deg_mean']); c4s.append(m['mean_local_square'])
        trs.append(m['transitivity'])
    return dict(z=float(np.mean(zs)), z_sem=float(np.std(zs) / math.sqrt(n_seeds)),
                C4=float(np.mean(c4s)), C4_sem=float(np.std(c4s) / math.sqrt(n_seeds)),
                C_trans=float(np.mean(trs)),
                val_sample=valid[0])


def measure_generic_nonfoliated(Vtarget, n_seeds=4, flips_per_vertex=4.0):
    """Controle: triangulação 2D GENÉRICA (esfera, Pachner livre, SEM folheação)."""
    c4s, zs, trs = [], [], []
    for s in range(n_seeds):
        rng = np.random.default_rng(7000 + s)
        Tr, _ = ck.grow_to(Vtarget, rng, flips_per_vertex=flips_per_vertex)
        m = rc.clustering_metrics(Tr.nverts, Tr.one_skeleton_edges())
        c4s.append(m['mean_local_square']); zs.append(m['deg_mean'])
        trs.append(m['transitivity'])
    return dict(z=float(np.mean(zs)), C4=float(np.mean(c4s)),
                C4_sem=float(np.std(c4s) / math.sqrt(n_seeds)),
                C_trans=float(np.mean(trs)))


def gate_reconstruction():
    """Valida a reconstrução do 1-esqueleto: V==Σℓ, E==3N/2, z==6."""
    g = CDT2D(8, 8, seed=1)
    # mexe um pouco para não testar só o regular
    lam = math.log(2)
    for _ in range(200):
        g.sweep(lam, 0.05, g.N, ell_min=3)
    V, edges, val = build_one_skeleton(g)
    ok = (val['V'] == val['V_expected'] and val['E'] == val['E_expected']
          and abs(val['z_mean'] - 6.0) < 1e-9)
    return ok, val


if __name__ == "__main__":
    print("=== TAREFA 1 — <z> e C4 no CDT 2D FOLIADO (gatilho cinemático) ===\n")

    # gate de engenharia da reconstrução
    ok, val = gate_reconstruction()
    print(f"[gate reconstrução 1-esqueleto] V={val['V']}(esp {val['V_expected']}) "
          f"E={val['E']}(esp {val['E_expected']}) z={val['z_mean']} -> "
          f"{'OK' if ok else 'FALHOU'}")
    if not ok:
        print("Reconstrução incorreta — abortando."); sys.exit(1)

    ladder_V = [500, 1000, 2000]
    res = {"observable": "z, C4 no 1-esqueleto do CDT 2D FOLIADO (motor F1)",
           "estimador": "rs_clustering.clustering_metrics (VERBATIM Gatilhos 1/2)",
           "edge_length": "FIXED [External]", "ladder_V": ladder_V,
           "foliated": [], "generic_nonfoliated": [],
           "refs": {"poisson_C4": "0.029-0.054 (decaindo)", "csg_C4": "0.019",
                    "flipped_DT_C4": "~0.145-0.148", "lattice2D_C4": 0.125}}

    print("\n  CDT FOLIADO (motor F1):")
    for V in ladder_V:
        T = max(8, int(round(math.sqrt(V))))
        r = measure_foliated(V, T)
        r['V'] = V
        res['foliated'].append(r)
        print(f"    V={V:>4}: z={r['z']:.3f}±{r['z_sem']:.3f}  C4={r['C4']:.4f}±{r['C4_sem']:.4f}  "
              f"C_tri={r['C_trans']:.4f}")

    print("\n  CONTROLE genérico NÃO-foliado (triangulação Pachner livre):")
    for V in ladder_V:
        r = measure_generic_nonfoliated(V)
        r['V'] = V
        res['generic_nonfoliated'].append(r)
        print(f"    V={V:>4}: z={r['z']:.3f}  C4={r['C4']:.4f}±{r['C4_sem']:.4f}  C_tri={r['C_trans']:.4f}")

    # TESTE DE TRIVIALIDADE: C4 foliado indistinguível do genérico?
    fol = res['foliated'][-1]; gen = res['generic_nonfoliated'][-1]
    dC4 = abs(fol['C4'] - gen['C4'])
    err = math.sqrt(fol['C4_sem']**2 + gen['C4_sem']**2)
    trivial = dC4 < 3 * err
    res['triviality_test'] = dict(
        foliated_C4=round(fol['C4'], 4), generic_C4=round(gen['C4'], 4),
        diff=round(dC4, 4), combined_3sem=round(3 * err, 4),
        C4_trivial_in_class=bool(trivial))
    print(f"\n  [TESTE DE TRIVIALIDADE C4] foliado={fol['C4']:.4f} vs genérico={gen['C4']:.4f} "
          f"| Δ={dC4:.4f} vs 3σ={3*err:.4f} -> "
          f"{'C4 TRIVIAL nesta classe' if trivial else 'C4 informativo (foliação muda C4)'}")

    # veredito do gatilho — qualificado pelo teste de trivialidade
    z_sat = all(abs(r['z'] - 6.0) < 0.05 for r in res['foliated'])
    if trivial:
        verdict = ("NÃO RESOLVIDO POR ESTE DISCRIMINADOR — C4 é trivial nesta classe "
                   "(toda triangulação 2D dá C4~0.145, foliada ou não) e <z>->6 é "
                   "identidade de Euler. Requer estimador alternativo (proposto na síntese, "
                   "não implementado nesta tarefa).")
    else:
        verdict = ("C4 informativo: a foliação muda C4 vs triangulação genérica. "
                   f"<z> satura={z_sat}, C4 satura não-trivial -> avaliar ARMADO/NÃO-ARMADO.")
    res['verdict'] = verdict
    res['z_saturates_6'] = bool(z_sat)
    print(f"\n  >>> VEREDITO DO GATILHO (qualificado): {verdict}")

    out = os.path.join(HERE, "task1_foliated_kinematics.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, indent=2, ensure_ascii=False)
    print(f"\n[escrito: {out}]")
