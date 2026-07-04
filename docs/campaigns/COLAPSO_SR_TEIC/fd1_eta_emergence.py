"""FD1 (ramo dormente EXP3) -- eta emerge ou e calibrado?

Roda como NOVA investigacao da SATURACAO (EXP1 sobreviveu standalone), nao como
reabertura da seta (EXP2 morto). Kill-criterion congelado em PRE_REGISTRO.md (EXP3,
secao 4) ANTES de qualquer dado -- reusado, nao reescrito.

Pergunta: o limiar eta tem um valor NATURAL e robusto na rede causal, ou e livre
(como a SR admite)?

Protocolo (PRE_REGISTRO EXP3): procurar transicao de fase espontanea variando um
controle interno e detectar onde o comportamento muda. O controle SR-fiel e a
PERCOLACAO DE LIGACAO do grafo causal (SR secao 5.5: chi_eff>=eta corresponde ao
surgimento do gigante componente; p_c.N=1+sqrt(eta)). Mede-se, ao reter cada aresta
causal com probabilidade p (varrendo p):
  (a) fracao do gigante componente G(p)         -> limiar de percolacao
  (b) susceptibilidade chi_perc(p) = <s^2>/<s>  (clusters finitos) -> PICO no p_c
  (c) rigidez espectral R(p) = (lmax-l2)/lmax    -> o sinal de colapso da SR
O eta_emergente = p_c (cego). So DEPOIS compara-se com SR (0.1, 0.99) e p_c=0.2488.

KILL-CRITERION (congelado):
  MORTE  se sem ponto critico (pico de susceptibilidade < 2x o fundo), OU
         eta_emergente muda > +-20% sob variacao +-10% da acao (eps do BD; densidade).
  SOBREVIVE se ha eta_emergente robusto (<+-20%) com pico de susceptibilidade >= 2x.

Pura medida sobre o grafo causal validado; nenhuma dinamica nova.
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone
import numpy as np
import sr_teic_core as core

SEEDS = list(range(12))
# CONTROLE CORRIGIDO (1a rodada confundida: edge-fraction p tinha p_c na borda da
# grade porque o grafo causal e DENSO ~N^2/4 -> percola em p->0). O invariante
# SR-fiel e o GRAU MEDIO retido k = p*<k_full> (SR: p_c.N=1+sqrt(eta), grau O(1)).
# Varre-se k de 0.2 a 6 (cobre o limiar ER k~1 com folga, interior).
KGRID = np.linspace(0.2, 6.0, 30)       # grau medio retido (x-axis fisico)
DIMS = [2, 4]
N_MAIN = 300                            # tamanho principal
PERC_SUSC_MIN = 2.0                     # pico >= 2x fundo (pre-registrado)
ROBUST_TOL = 0.20                       # +-20% (pre-registrado)


def giant_and_susc(adj_bool):
    """Fracao do maior componente e susceptibilidade de percolacao (<s^2>/<s> sobre
    clusters FINITOS, excluindo o gigante) via union-find."""
    n = adj_bool.shape[0]
    parent = np.arange(n)

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    ii, jj = np.where(np.triu(adj_bool, 1))
    for a, b in zip(ii, jj):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    roots = np.array([find(k) for k in range(n)])
    _, sizes = np.unique(roots, return_counts=True)
    gmax = sizes.max()
    finite = sizes[sizes < gmax] if (sizes == gmax).sum() == 1 else sizes[sizes < gmax]
    if finite.size == 0:
        susc = 0.0
    else:
        susc = float((finite ** 2).sum() / finite.sum())
    return gmax / n, susc


def rigidity(adj_w):
    """R = (lmax - l2)/lmax do grafo retido (operador de colapso = adjacencia)."""
    if adj_w.sum() == 0:
        return 0.0
    ev = np.linalg.eigvalsh(adj_w)
    lmax, l2 = ev[-1], ev[-2]
    return float((lmax - l2) / lmax) if lmax > 1e-9 else 0.0


def sweep(dim, N, eps_density_seed_offset=0):
    """Varre o GRAU MEDIO retido k; retorna G(k), susc(k), R(k) medias sobre seeds.
    Para cada rede, p = k/<k_full> (clampeado em [0,1]); retem arestas com prob p."""
    G = np.zeros((len(SEEDS), len(KGRID)))
    S = np.zeros_like(G)
    R = np.zeros_like(G)
    for si, sd in enumerate(SEEDS):
        rng = np.random.default_rng(50000 * dim + sd + eps_density_seed_offset)
        pts = core.sprinkle(N, dim, rng)
        A = core.ancestor_matrix(pts)
        Asym = (A | A.T)
        np.fill_diagonal(Asym, False)
        ii, jj = np.where(np.triu(Asym, 1))
        m = len(ii)
        k_full = 2.0 * m / N                    # grau medio do grafo causal cheio
        rperc = np.random.default_rng(99 * sd + 7)
        u = rperc.random(m)
        for ki, kk in enumerate(KGRID):
            p = min(kk / k_full, 1.0)            # fracao p p/ atingir grau medio kk
            keep = u < p
            adj = np.zeros((N, N), dtype=bool)
            adj[ii[keep], jj[keep]] = True
            adj[jj[keep], ii[keep]] = True
            g, susc = giant_and_susc(adj)
            G[si, ki] = g
            S[si, ki] = susc
            R[si, ki] = rigidity(adj.astype(float))
    return G.mean(0), S.mean(0), R.mean(0)


def find_kc(susc):
    """k_c = grau medio no pico de susceptibilidade; razao pico/fundo; idx."""
    ipk = int(np.argmax(susc))
    kc = float(KGRID[ipk])
    bg = float(np.median(susc[susc < np.percentile(susc, 50)])) if susc.size else 0.0
    ratio = float(susc[ipk] / bg) if bg > 1e-9 else float("inf")
    return kc, ratio, ipk


def main():
    payload = {"experiment": "FD1_eta_emergence", "seeds": SEEDS,
               "kgrid": KGRID.tolist(), "by": {}}
    lines, kcs = [], {}
    for dim in DIMS:
        G, S, R = sweep(dim, N_MAIN)
        kc, ratio, ipk = find_kc(S)
        kcs[dim] = kc
        payload["by"][f"dim{dim}_main"] = {
            "G": G.tolist(), "susc": S.tolist(), "R": R.tolist(),
            "kc": kc, "susc_peak_ratio": ratio,
            "R_at_kc": float(R[ipk]), "G_at_kc": float(G[ipk])}
        lines.append(f"  dim={dim} N={N_MAIN}: k_c(pico susc)={kc:.2f}  "
                     f"pico/fundo={ratio:.1f}x  R(k_c)={R[ipk]:.3f}  G(k_c)={G[ipk]:.2f}")
    # ---- robustez +-10% da densidade (controle interno real da rede causal) ----
    robust = {}
    for dim in DIMS:
        kc_lo, _, _ = find_kc(sweep(dim, int(N_MAIN * 0.9))[1])   # -10% densidade
        kc_hi, _, _ = find_kc(sweep(dim, int(N_MAIN * 1.1))[1])   # +10% densidade
        base = kcs[dim]
        dev = max(abs(kc_lo - base), abs(kc_hi - base)) / base if base > 0 else float("inf")
        robust[dim] = {"kc_-10%": kc_lo, "kc_base": base, "kc_+10%": kc_hi,
                       "max_rel_dev": float(dev), "robust_ok": bool(dev < ROBUST_TOL)}
        lines.append(f"  dim={dim} robustez +-10% densidade: k_c {kc_lo:.2f}/{base:.2f}/"
                     f"{kc_hi:.2f}  dev={dev*100:.1f}%  {'OK' if dev<ROBUST_TOL else 'FALHA'}")
    payload["robustness"] = robust
    # ---- veredito (kill-criterion congelado) ----
    crit_peak = all(payload["by"][f"dim{d}_main"]["susc_peak_ratio"] >= PERC_SUSC_MIN for d in DIMS)
    crit_robust = all(robust[d]["robust_ok"] for d in DIMS)
    survives = bool(crit_peak and crit_robust)
    payload["verdict"] = {"susceptibility_peak_ge_2x": bool(crit_peak),
                          "kc_robust_within_20pct": bool(crit_robust),
                          "result": "SOBREVIVE" if survives else "MORTE"}
    # comparacao POS-DICAO: SR p_c.N=1+sqrt(eta) => k_c=1+sqrt(eta) => eta=(k_c-1)^2
    eta_implied = {str(d): float((kcs[d] - 1.0) ** 2) for d in DIMS}
    payload["postdiction"] = {
        "kc_measured": {str(d): kcs[d] for d in DIMS},
        "eta_implied_(kc-1)^2": eta_implied,
        "SR_relation": "p_c*N = 1+sqrt(eta)  ->  k_c = 1+sqrt(eta)  ->  eta=(k_c-1)^2",
        "SR_eta_macro": 0.1, "SR_eta_nisq": 0.99, "ER_generic_kc": 1.0,
        "note": "POS-DICAO (numeros da SR ja expostos no prompt). k_c~1 = limiar ER "
                "generico (qualquer grafo) -> NAO pina eta especifico de TEIC; "
                "reproduz a relacao de consistencia da SR sem deriva-la."}
    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    (core.HERE / "fd1_eta.json").write_text(json.dumps(payload, indent=2))
    print("=" * 76)
    print("FD1 (EXP3 dormente) -- eta emerge ou e calibrado?")
    print("=" * 76)
    print("\n".join(lines))
    print("-" * 76)
    print(f"k_c medido (cego): " + "  ".join(f"dim{d}={kcs[d]:.2f}" for d in DIMS)
          + "   (limiar ER generico ~1)")
    print(f"POS-DICAO: eta=(k_c-1)^2 = " + "  ".join(f"dim{d}={eta_implied[str(d)]:.3f}" for d in DIMS)
          + "   vs SR eta_macro=0.1 / eta_nisq=0.99")
    print(f"VEREDITO FD1: {payload['verdict']['result']}  "
          f"(pico>=2x: {crit_peak}; robusto<20%: {crit_robust})")


if __name__ == "__main__":
    main()
