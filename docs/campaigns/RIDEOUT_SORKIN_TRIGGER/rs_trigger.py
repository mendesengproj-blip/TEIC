"""
rs_trigger.py — GATILHO de coordenação do crescimento sequencial (Rideout-Sorkin).

Mede APENAS <z>(N) = coordenacao media do grafo de Hasse (relacoes de cobertura),
com o MESMO estimador da ESCALA_XI (orientation_core.causal_link_graph +
Graph.degree.mean() = 2*#links/N), sobre causal sets CRESCIDOS pela dinamica de
percolacao transitiva (subfamilia canonica de Rideout-Sorkin / Barak-Erdos).

GUARD ANTI-CIRCULARIDADE: nenhuma escala metrica, coordenada de espaco-tempo, ou
expressao relativistica entra no gerador. So a constante adimensional p e a ordem
de nascimento (rotulo). z e puramente combinatorio.

NAO roda ferromagneto, NAO mede xi, NAO constroi a campanha completa.
"""

import json
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# bits empacotados em uint64
WORD = 64


# ====================================================================== #
# GERADOR: percolacao transitiva (CSG classico, subfamilia t_n = t^n)
# ====================================================================== #

def _pack_width(n):
    return (n + WORD - 1) // WORD


def grow_transitive_percolation(n, p, rng):
    """Cresce um causal set de tamanho n por percolacao transitiva.

    Para cada par em ordem de nascimento i<j, sorteia aresta direta i->j com
    probabilidade p (independente). A ordem causal e o fecho transitivo.

    Retorna o fecho como bitsets de ANCESTRAIS: anc[j] (W,) uint64 com bit i ligado
    sse i precede j (i strictly < j na ordem causal). Tambem retorna #arestas diretas.

    Construcao incremental e exata: anc[j] = OR_{p in pais diretos}(anc[p] | onehot(p)).
    """
    W = _pack_width(n)
    anc = np.zeros((n, W), dtype=np.uint64)
    n_direct = 0
    # onehot pre-computado: bit i -> (word, mask)
    word_of = np.arange(n) // WORD
    mask_of = (np.uint64(1) << (np.arange(n) % WORD).astype(np.uint64))

    for j in range(1, n):
        # pais diretos: cada i<j independente com prob p
        draws = rng.random(j) < p
        parents = np.nonzero(draws)[0]
        n_direct += parents.size
        if parents.size == 0:
            continue
        # OR dos ancestrais dos pais + os proprios pais
        acc = np.bitwise_or.reduce(anc[parents], axis=0)
        # liga o bit de cada pai (onehot)
        # agrupa por palavra
        pw = word_of[parents]
        pm = mask_of[parents]
        # acumula mascaras por palavra
        np.bitwise_or.at(acc, pw, pm)
        anc[j] = acc
    return anc, n_direct


# ====================================================================== #
# ESTIMADOR: coordenacao do grafo de Hasse (= ESCALA_XI)
# ====================================================================== #

def hasse_links_count(anc, n):
    """#links (relacoes de cobertura) do causal set dado pelos ancestrais 'anc'.

    i e link-pai de j  <=>  i in anc[j]  E  i NAO esta em (OR_{k in anc[j]} anc[k]).
    O segundo termo = elementos que tem um intermediario estrito ate j (i.e. existe k
    com i<k<j). Isto e exatamente L = C & ~(C@C) restrito a coluna j.
    """
    total_links = 0
    W = anc.shape[1]
    for j in range(n):
        aj = anc[j]
        # indices k em anc[j]
        ks = _bits_to_indices(aj)
        if ks.size == 0:
            continue
        inter = np.bitwise_or.reduce(anc[ks], axis=0) if ks.size else np.zeros(W, np.uint64)
        linkparents = aj & ~inter
        total_links += _popcount(linkparents)
    return total_links


def _bits_to_indices(bitrow):
    """Indices dos bits ligados num bitset (W,) uint64."""
    out = []
    for w, word in enumerate(bitrow):
        if word == 0:
            continue
        base = w * WORD
        x = int(word)
        while x:
            b = (x & -x).bit_length() - 1
            out.append(base + b)
            x &= x - 1
    return np.asarray(out, dtype=np.int64)


def _popcount(bitrow):
    # popcount vetorizado em uint64 via tabela de bytes
    b = bitrow.view(np.uint8)
    return int(_BYTE_POPCOUNT[b].sum())


_BYTE_POPCOUNT = np.array([bin(i).count("1") for i in range(256)], dtype=np.int64)


def ordering_fraction(anc, n):
    """Fracao de pares relacionados = #relacoes / C(n,2)."""
    rel = sum(_popcount(anc[j]) for j in range(n))
    return rel / (n * (n - 1) / 2) if n > 1 else 0.0


def n_minimal(anc, n):
    """#elementos sem ancestrais (minimais)."""
    return sum(1 for j in range(n) if _popcount(anc[j]) == 0)


def z_mean_hasse(anc, n):
    return 2.0 * hasse_links_count(anc, n) / n if n else 0.0


# ====================================================================== #
# GATE DE VALIDACAO
# ====================================================================== #

def validation_gate(verbose=True):
    """Reproduz propriedades documentadas da percolacao transitiva."""
    rng = np.random.default_rng(7)
    report = {"checks": [], "passed": True}

    def check(name, ok, detail):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["passed"] = False
        if verbose:
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {detail}")

    # (1) e (2): formas fechadas para minimais e arestas diretas
    for (n, p) in [(200, 0.05), (400, 0.10)]:
        n_seeds = 200
        mins, edges = [], []
        for s in range(n_seeds):
            anc, nd = grow_transitive_percolation(n, p, np.random.default_rng(100 + s))
            mins.append(n_minimal(anc, n))
            edges.append(nd)
        exp_min = (1 - (1 - p) ** n) / p
        exp_edge = p * n * (n - 1) / 2
        m_mean, m_sem = np.mean(mins), np.std(mins) / np.sqrt(n_seeds)
        e_mean, e_sem = np.mean(edges), np.std(edges) / np.sqrt(n_seeds)
        check(f"E[#minimais] n={n} p={p}",
              abs(m_mean - exp_min) <= 3 * max(m_sem, 1e-9),
              f"medido {m_mean:.2f}+-{m_sem:.2f} vs fechado {exp_min:.2f}")
        check(f"E[#arestas diretas] n={n} p={p}",
              abs(e_mean - exp_edge) <= 3 * max(e_sem, 1e-9),
              f"medido {e_mean:.1f}+-{e_sem:.1f} vs fechado {exp_edge:.1f}")

    # (3) idempotencia/aciclicidade: anc[j] nunca contem indice >= j (DAG por ordem)
    anc, _ = grow_transitive_percolation(300, 0.1, rng)
    dag_ok = True
    for j in range(300):
        ks = _bits_to_indices(anc[j])
        if ks.size and ks.max() >= j:
            dag_ok = False
            break
    check("aciclicidade/DAG (ancestrais < j)", dag_ok, "nenhum ancestral com indice >= j")

    # idempotencia do fecho: se i in anc[j] e k in anc[i] entao k in anc[j]
    trans_ok = True
    anc, _ = grow_transitive_percolation(150, 0.15, np.random.default_rng(3))
    for j in range(150):
        ks = _bits_to_indices(anc[j])
        for i in ks:
            if not _subset(anc[i], anc[j]):
                trans_ok = False
                break
        if not trans_ok:
            break
    check("fecho transitivo idempotente", trans_ok, "anc[i] subset anc[j] para i in anc[j]")

    # (4) percolacao: fracao de ordenacao cresce com N a p fixo
    p = 0.05
    fr = []
    for n in [200, 800, 1600]:
        vals = [ordering_fraction(grow_transitive_percolation(n, p, np.random.default_rng(50 + s))[0], n)
                for s in range(5)]
        fr.append(np.mean(vals))
    check("percolacao: fracao de ordenacao cresce com N (p fixo)",
          fr[0] < fr[1] < fr[2], f"order_frac(N) = {[round(x,3) for x in fr]} @ p={p}")

    return report


def _subset(a, b):
    return bool(np.all((a & ~b) == 0))


# ====================================================================== #
# MEDICAO CENTRAL
# ====================================================================== #

REGIMES = [
    {"label": "sparse_fixed", "kind": "fixed", "p": 0.02},
    {"label": "intermediate_fixed", "kind": "fixed", "p": 0.10},
    {"label": "dense_fixed", "kind": "fixed", "p": 0.40},
    {"label": "manifold_scaled", "kind": "scaled", "lam": 4.0},  # p = lam/N
]
LADDER = [500, 1000, 2000, 3300, 3888]
N_SEEDS = 5


def p_for(regime, n):
    if regime["kind"] == "fixed":
        return regime["p"]
    return regime["lam"] / n


def run_measurement(ladder=LADDER, n_seeds=N_SEEDS, seed_n_cap=None):
    out = {"estimator": "z_mean = 2*#hasse_links/N (= ESCALA_XI causal_link_graph)",
           "generator": "transitive percolation (CSG / Rideout-Sorkin subfamily t_n=t^n)",
           "anti_circularity": "dimensionless p + birth order only; no metric scale",
           "ladder": ladder, "n_seeds": n_seeds, "regimes": {}}
    for regime in REGIMES:
        label = regime["label"]
        rows = []
        for n in ladder:
            ns = n_seeds
            if seed_n_cap and n >= seed_n_cap[0]:
                ns = seed_n_cap[1]
            p = p_for(regime, n)
            zs, ofs, nd = [], [], []
            t0 = time.perf_counter()
            for s in range(ns):
                rng = np.random.default_rng(1000 + s + n)
                anc, n_direct = grow_transitive_percolation(n, p, rng)
                zs.append(z_mean_hasse(anc, n))
                ofs.append(ordering_fraction(anc, n))
                nd.append(n_direct)
            dt = time.perf_counter() - t0
            rows.append({"N": n, "p": p, "n_seeds": ns,
                         "z_mean": float(np.mean(zs)), "z_sem": float(np.std(zs) / np.sqrt(ns)),
                         "order_frac": float(np.mean(ofs)),
                         "n_direct": float(np.mean(nd)), "runtime_s": dt})
            print(f"  {label:>18} N={n:>4} p={p:.4g}: z={np.mean(zs):7.3f}"
                  f" of={np.mean(ofs):.3f} [{dt:.1f}s, {ns} seeds]")
        # expoente local d<z>/d ln N nos dois maiores N
        z = np.array([r["z_mean"] for r in rows])
        Nv = np.array([r["N"] for r in rows], float)
        local_exp = np.diff(z) / np.diff(np.log(Nv))
        out["regimes"][label] = {"regime": regime, "rows": rows,
                                 "local_dz_dlnN": local_exp.tolist(),
                                 "local_exp_top": float(local_exp[-1])}
    return out


# ====================================================================== #
# VEREDITO
# ====================================================================== #

def verdict(meas, rel_slope_thresh=0.05):
    """ARMADO se ALGUM regime satura (expoente local no topo ~0).
    Criterio operacional: expoente local relativo (d<z>/dlnN) / z_top < rel_slope_thresh
    E nao-crescente (a inclinacao no topo <= inclinacao anterior).
    """
    res = {"per_regime": {}, "armed": False, "armed_regime": None}
    for label, R in meas["regimes"].items():
        rows = R["rows"]
        z_top = rows[-1]["z_mean"]
        slope_top = R["local_exp_top"]
        slopes = R["local_dz_dlnN"]
        rel = slope_top / z_top if z_top else 0.0
        decreasing = len(slopes) >= 2 and slopes[-1] <= slopes[-2] + 1e-9
        saturates = (rel < rel_slope_thresh) and decreasing
        res["per_regime"][label] = {
            "z_top": z_top, "slope_top": slope_top, "rel_slope_top": rel,
            "decreasing": decreasing, "saturates": saturates,
            "z_first": rows[0]["z_mean"], "ratio_top_first": z_top / rows[0]["z_mean"]}
        if saturates:
            res["armed"] = True
            res["armed_regime"] = label
    res["verdict"] = "ARMADO" if res["armed"] else "NAO_ARMADO"
    return res


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode in ("gate", "all"):
        print("=" * 64)
        print("GATE DE VALIDACAO (percolacao transitiva)")
        print("=" * 64)
        gate = validation_gate()
        json.dump(gate, open(os.path.join(HERE, "validation_gate.json"), "w"), indent=2)
        print(f"\n  GATE {'VERDE' if gate['passed'] else 'VERMELHO'}")
        if not gate["passed"]:
            print("  ABORTA: medicao nao confiavel sem gate verde.")
            sys.exit(1)

    if mode in ("measure", "all"):
        print("\n" + "=" * 64)
        print("MEDICAO CENTRAL: <z>(N) por regime")
        print("=" * 64)
        # cap seeds no topo para o regime denso ser viavel
        meas = run_measurement(seed_n_cap=(3300, 3))
        v = verdict(meas)
        meas["verdict"] = v
        json.dump(meas, open(os.path.join(HERE, "rs_trigger.json"), "w"), indent=2)
        print("\n" + "=" * 64)
        print("VEREDITO DO GATILHO")
        print("=" * 64)
        for label, r in v["per_regime"].items():
            print(f"  {label:>18}: z {r['z_first']:.2f}->{r['z_top']:.2f}"
                  f" (x{r['ratio_top_first']:.2f}) slope_top={r['slope_top']:+.2f}"
                  f" rel={r['rel_slope_top']:.3f} {'SATURA' if r['saturates'] else 'cresce'}")
        print(f"\n  >>> {v['verdict']}"
              + (f" (regime {v['armed_regime']})" if v["armed"] else " (todos divergem)"))
