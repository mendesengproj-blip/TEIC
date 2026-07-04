"""cdt_substrate.py -- adaptador: 1-esqueleto do CDT 3D (F1b) como Graph do TEIC.

Campanha CDT_TEIC_FERRO. Importa o motor CDT 3D JA VALIDADO E GATEADO de F1b
(TEORIA_CDT/F1b_acao/f1b_cdt3d.py) SEM modificacao, e o entrega como o `Graph` que o
orientation_core do TEIC consome -- exatamente como xi_suite entrega sprinkles de Poisson.

Anti-contaminacao (charter TEORIA_CDT): a regra e' unidirecional -- TEORIA_CDT nao importa
TEIC. AQUI e' TEIC que importa o motor CDT como SUBSTRATO (igual importa causal_core), sem
tocar na geometria. A aresta do CDT ja' e' [External] por F1b; nada "escala emergiu" aqui.

O grafo entregue = 1-esqueleto da triangulacao (vertices + arestas), o MESMO objeto usado
para medir <z>/C4 em CDT_VIABILIDADE e em F1b. O campo de orientacao n in S^2 vivera' nos
VERTICES (pre-registro sec 3.1).
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
# TEIC root (para orientation_core) e TEORIA_CDT/F1b_acao (para o motor)
TEIC_ROOT = HERE.parents[2]
CDT_DIR = TEIC_ROOT.parents[0] / "TEORIA_CDT" / "F1b_acao"
sys.path.insert(0, str(CDT_DIR))
sys.path.insert(0, str(TEIC_ROOT / "results" / "vacuum_structure" / "orientation"))

from f1b_cdt3d import CDT3D            # noqa: E402  (motor CDT 3D, F1b, intacto)
from f1b_dH import equilibrate         # noqa: E402  (equilibra geometria fase estendida)
from orientation_core import Graph     # noqa: E402  (container de grafo do TEIC)


def cdt_skeleton_graph(g_cdt):
    """Extrai o 1-esqueleto (vertices+arestas) da triangulacao CDT como Graph do TEIC.

    Retorna (Graph, times, frac_links_spatial). `times` = rotulo de fatia por no'
    (a unica coordenada natural do CDT, usada so' para diagnostico, NAO p/ Fourier)."""
    vids = sorted(g_cdt.vt.keys())
    remap = {v: i for i, v in enumerate(vids)}
    edges = []
    n_spatial = 0
    for e in g_cdt.edge_set.items:
        u, w = tuple(e)
        edges.append((remap[u], remap[w]))
        if g_cdt.vt[u] == g_cdt.vt[w]:
            n_spatial += 1
    edges = np.asarray(edges, dtype=np.int64)
    times = np.array([g_cdt.vt[v] for v in vids], dtype=np.int64)
    G = Graph(len(vids), edges)
    frac_spatial = n_spatial / max(1, len(edges))
    return G, times, frac_spatial


def build_cdt(k0, Vt, seed, T=10, therm=140, decorrelate=40):
    """Equilibra a geometria CDT 3D PURA (sem semente) na fase estendida e congela o
    1-esqueleto. `decorrelate` = sweeps extra apos a calibracao p/ snapshots independentes.

    Retorna (Graph, times, info). info: N3, N0, z_mean, conn_frac, frac_links_spatial, k3.
    A geometria NAO e' modificada (so' MC de Pachner puro de F1b)."""
    g_cdt, k3 = equilibrate(k0, T, Vt, seed, therm=therm)
    eps = 0.0012
    # decorrelacao extra (snapshot independente por seed) mantendo volume travado
    gain = 0.4 * eps
    for _ in range(decorrelate):
        g_cdt.sweep(k0, k3, eps, Vt, n_steps=Vt)
        k3 += gain * (g_cdt.N3 - Vt)
    assert len(g_cdt.check_manifold()) == 0, "geometria CDT quebrou (nao deveria)"
    G, times, frac_sp = cdt_skeleton_graph(g_cdt)
    info = {
        "k0": k0, "Vt": Vt, "T": T, "seed": seed,
        "N3": int(g_cdt.N3), "N0": int(g_cdt.N0),
        "z_mean": float(G.degree.mean()), "z_max": int(G.degree.max()),
        "conn_frac": float(G.connected_fraction()),
        "frac_links_spatial": float(frac_sp),
        "n_colors": int(G.n_colors), "k3": float(k3),
    }
    return G, times, info


if __name__ == "__main__":
    # smoke: constroi um substrato pequeno e reporta as estatisticas do 1-esqueleto
    for k0 in (1.0, 3.0):
        G, times, info = build_cdt(k0, Vt=1500, seed=11, therm=60, decorrelate=10)
        # checa coloracao propria (pre-requisito do Metropolis colorido)
        bad = sum(1 for a, b in G.edges if G.colors[a] == G.colors[b])
        print(f"k0={k0}: N0(nos)={info['N0']} N3={info['N3']} <z>={info['z_mean']:.1f} "
              f"z_max={info['z_max']} conn={info['conn_frac']:.2f} "
              f"frac_spatial={info['frac_links_spatial']:.2f} colours={info['n_colors']} "
              f"colour_violations={bad}")
