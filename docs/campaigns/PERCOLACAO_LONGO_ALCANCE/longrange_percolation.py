"""
longrange_percolation.py -- 3a FAMILIA: percolacao de longo alcance sobre a ordem causal.

Gatilho cinematico barato (so <z> e C4), na mesma linhagem dos Gatilhos 1-3
(RIDEOUT_SORKIN_TRIGGER / RIDEOUT_SORKIN_CLUSTERING / CDT_VIABILIDADE). NAO roda
ferromagneto, NAO mede xi.

SUBSTRATO (reutilizado VERBATIM):
  * sprinkling de Poisson .................. causal_core.sprinkle_box (ESCALA_XI)
  * ordem causal + tempo-proprio ........... causal_core.causal_matrix (Minkowski nu)
  * estimador <z> e C4 ..................... rs_clustering.clustering_metrics (Gatilho 2)

REGRA DE CONEXAO (a UNICA novidade): dois eventos causais i<j conectam (aresta
nao-direcionada) com probabilidade
        p(dtau) = min(1, (dtau/dtau0)^(-sigma))
com dtau = tempo-proprio invariante e dtau0 = rho^(-1/d) ([External], escala de
discretude do sprinkling). sigma adimensional, varrido.

ANTI-CIRCULARIDADE: nenhuma escala metrica/dilatacao/Tc entra. O sorteio por par
u_ij e chaveado pela IDENTIDADE dos nos (invariante sob boost), nunca por coordenada
-> grafo Lorentz-invariante por construcao (verificado no gate item 5).
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

# --- localizar a raiz TEIC e importar os modulos reutilizados VERBATIM ---
_ROOT = HERE
for _ in range(6):
    if os.path.exists(os.path.join(_ROOT, "src", "causal_core.py")):
        break
    _ROOT = os.path.dirname(_ROOT)
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, os.path.join(_ROOT, "docs", "campaigns", "RIDEOUT_SORKIN_CLUSTERING"))

from causal_core import sprinkle_box, causal_matrix          # noqa: E402
from rs_clustering import clustering_metrics                  # noqa: E402  (VERBATIM Gatilho 2)

DIM = 3            # 2+1D Minkowski (t,x,y)
# Caixa fixa, larga-e-baixa (T < L): reduz a fracao de pares causais do cubo
# (que em 2+1D e causalmente denso, z~0.3N) para a faixa O(10) onde o estimador
# square-clustering VERBATIM e tratavel. T_box, L_box sao [External] (geometria do
# sprinkling, ja externa desde a ESCALA_XI), como o diamante da RS-CLUSTERING.
T_BOX = 1.0
L_BOX = 3.0
BOUNDS = [(0.0, T_BOX), (0.0, L_BOX), (0.0, L_BOX)]
VOL = T_BOX * L_BOX * L_BOX


# ====================================================================== #
# TEMPO-PROPRIO INVARIANTE entre pares causais (sem dilatacao)
# ====================================================================== #
def causal_proper_time(pts):
    """(C, tau): C[i,j]=i precede j (causal_matrix VERBATIM); tau[i,j]=sqrt(interval^2)
    para os pares causais (inf nos demais). So cones de Minkowski nus."""
    pts = np.asarray(pts, float)
    C = causal_matrix(pts)                         # VERBATIM do substrato
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    s2 = dt * dt - dx2
    tau = np.where(C, np.sqrt(np.maximum(s2, 0.0)), np.inf)
    return C, tau


# ====================================================================== #
# GRAFO DE PERCOLACAO DE LONGO ALCANCE
# ====================================================================== #
def longrange_edges(pts, sigma, dtau0, rng):
    """Lista de arestas (nao-direcionada) da regra de longo alcance.

    Para cada par causal i<j: p = min(1,(tau_ij/dtau0)^(-sigma)); conecta se u_ij<p.
    u_ij sorteado UMA vez por par no triangulo superior por IDENTIDADE de no
    (invariante sob boost). Retorna (edges, info)."""
    C, tau = causal_proper_time(pts)
    n = C.shape[0]
    # pares causais (qualquer direcao) colapsados ao triangulo superior {i<j}
    pair = C | C.T
    iu = np.triu_indices(n, k=1)
    causal_up = pair[iu]                            # bool nos pares {i<j} causalmente ligados
    src = iu[0][causal_up]
    dst = iu[1][causal_up]
    # tau e definido (finito) so na direcao causal; min() colapsa a direcao certa
    t_ij = np.minimum(tau[src, dst], tau[dst, src])
    p = np.minimum(1.0, (t_ij / dtau0) ** (-sigma))
    # u_ij chaveado por identidade do par (i<j) -> um sorteio por par, frame-invariante
    u = rng.random(src.shape[0])
    keep = u < p
    edges = list(zip(src[keep].tolist(), dst[keep].tolist()))
    info = {"n": int(n), "n_causal_pairs": int(src.shape[0]),
            "n_edges": int(keep.sum()), "dtau0": float(dtau0),
            "tau_min": float(t_ij.min()) if t_ij.size else 0.0,
            "tau_max": float(t_ij.max()) if t_ij.size else 0.0}
    return edges, info, (src, dst, t_ij)


def random_control_edges(src, dst, n_edges, rng):
    """Controle de triviality (gate 4): mesmo POOL de pares causais, mesma contagem
    de arestas, sorteadas UNIFORMEMENTE (sem decaimento por Delta-tau)."""
    m = src.shape[0]
    if n_edges >= m:
        idx = np.arange(m)
    else:
        idx = rng.choice(m, size=n_edges, replace=False)
    return list(zip(src[idx].tolist(), dst[idx].tolist()))


# ====================================================================== #
# BOOST (so para o gate de invariancia -- NUNCA no gerador de fisica)
# ====================================================================== #
def boost(pts, eta, axis=0):
    """Boost de Lorentz de rapidez eta no eixo espacial `axis` (0->x). x'^0,x'^axis
    misturados; demais espaciais inalterados. Probe de invariancia apenas."""
    pts = np.asarray(pts, float).copy()
    ch, sh = np.cosh(eta), np.sinh(eta)
    t = pts[:, 0].copy()
    x = pts[:, 1 + axis].copy()
    pts[:, 0] = ch * t - sh * x
    pts[:, 1 + axis] = -sh * t + ch * x
    return pts


# ====================================================================== #
# GATE DE VALIDACAO
# ====================================================================== #
def dtau0_for(rho):
    """Escala de discretude [External]: rho^(-1/d)."""
    return rho ** (-1.0 / DIM)


def validation_gate(verbose=True):
    report = {"checks": [], "passed": True}

    def check(name, ok, detail):
        report["checks"].append({"name": name, "ok": bool(ok), "detail": detail})
        if not ok:
            report["passed"] = False
        if verbose:
            print(f"  [{'OK' if ok else 'FAIL'}] {name}: {detail}")

    # substrato de teste (rho pequeno -> gate barato)
    n_target = 700.0
    rho = n_target / VOL
    rng = np.random.default_rng(7)
    pts = sprinkle_box(rho, BOUNDS, rng)
    n = pts.shape[0]
    dtau0 = dtau0_for(rho)

    # (1) sigma grande -> esparso (z baixo, saturante)
    e_hi, info_hi, _ = longrange_edges(pts, sigma=6.0, dtau0=dtau0,
                                       rng=np.random.default_rng(1))
    m_hi = clustering_metrics(n, e_hi)
    # (2) sigma->0 -> denso (quase todos os pares causais)
    e_lo, info_lo, _ = longrange_edges(pts, sigma=0.5, dtau0=dtau0,
                                       rng=np.random.default_rng(2))
    m_lo = clustering_metrics(n, e_lo)
    frac_lo = info_lo["n_edges"] / info_lo["n_causal_pairs"]
    # NB: a faixa dinamica tau/dtau0 ~ T*rho^(1/d) e modesta numa caixa, logo o
    # limite esparso e SUAVE (sigma=6 ainda retem cauda); o gate exige apenas que o
    # esparso fique CLARAMENTE abaixo do denso (ratio<0.5), nao um corte abrupto.
    check("sigma=6 esparso (z claramente < z denso)",
          m_hi["deg_mean"] < 0.5 * m_lo["deg_mean"],
          f"z(sig6)={m_hi['deg_mean']:.2f}  z(sig0.5)={m_lo['deg_mean']:.2f}  "
          f"ratio={m_hi['deg_mean']/max(m_lo['deg_mean'],1e-9):.3f}")
    check("sigma=0.5 conecta a MAIORIA dos pares causais (extremo denso/MF)",
          frac_lo > 0.6,
          f"frac arestas/pares-causais = {frac_lo:.3f}  z={m_lo['deg_mean']:.1f}")

    # (3) cross-check do estimador: clustering_metrics deg_mean == 2*E/N
    z_direct = 2.0 * len(e_hi) / n
    check("cross-check <z> = 2*E/N (estimador VERBATIM)",
          abs(m_hi["deg_mean"] - z_direct) < 1e-9,
          f"clustering_metrics={m_hi['deg_mean']:.9f} vs 2E/N={z_direct:.9f}")

    # (4) triviality do C4: family vs controle aleatorio de mesma densidade
    sig_mid = 3.0
    e_mid, info_mid, pool = longrange_edges(pts, sigma=sig_mid, dtau0=dtau0,
                                            rng=np.random.default_rng(3))
    src, dst, _ = pool
    m_mid = clustering_metrics(n, e_mid)
    c4_fam = []
    c4_rnd = []
    for s in range(4):
        e_f, info_f, pool_f = longrange_edges(pts, sigma=sig_mid, dtau0=dtau0,
                                              rng=np.random.default_rng(30 + s))
        c4_fam.append(clustering_metrics(n, e_f)["mean_local_square"])
        e_r = random_control_edges(pool_f[0], pool_f[1], info_f["n_edges"],
                                   np.random.default_rng(300 + s))
        c4_rnd.append(clustering_metrics(n, e_r)["mean_local_square"])
    c4_fam_m, c4_rnd_m = float(np.mean(c4_fam)), float(np.mean(c4_rnd))
    # gate aqui apenas verifica que C4 NAO e trivialmente identico ao controle
    # (i.e. a estrutura de decaimento por dtau MUDA o C4) -- direcao registrada
    check("C4 nao-trivial: familia difere do controle de mesma densidade",
          abs(c4_fam_m - c4_rnd_m) > 0.2 * max(c4_rnd_m, 1e-6),
          f"C4_fam(sig3)={c4_fam_m:.4f}  C4_rnd={c4_rnd_m:.4f}")

    # (5) INVARIANCIA DE LORENTZ: boost -> mesmo grafo (mesmas arestas)
    eta = 0.8
    ptsb = boost(pts, eta, axis=0)
    # mesmo sorteio (mesma seed) em ambos os referenciais; u chaveado por identidade
    e0, i0, _ = longrange_edges(pts, sigma=sig_mid, dtau0=dtau0,
                                rng=np.random.default_rng(99))
    eb, ib, _ = longrange_edges(ptsb, sigma=sig_mid, dtau0=dtau0,
                                rng=np.random.default_rng(99))
    set0 = set(map(tuple, (sorted(e) for e in e0)))
    setb = set(map(tuple, (sorted(e) for e in eb)))
    edges_identical = (set0 == setb)
    m0 = clustering_metrics(n, e0)
    mb = clustering_metrics(n, eb)
    check("invariancia de Lorentz: arestas BIT-identicas sob boost",
          edges_identical,
          f"|E0|={len(e0)} |Eb|={len(eb)} simdif={len(set0 ^ setb)}")
    check("invariancia de Lorentz: <z> e C4 identicos sob boost",
          abs(m0["deg_mean"] - mb["deg_mean"]) < 1e-9
          and abs(m0["mean_local_square"] - mb["mean_local_square"]) < 1e-9,
          f"z {m0['deg_mean']:.6f}/{mb['deg_mean']:.6f} "
          f"C4 {m0['mean_local_square']:.6f}/{mb['mean_local_square']:.6f}")

    report["aux"] = {"c4_family_sig3": c4_fam_m, "c4_random_control_sig3": c4_rnd_m,
                     "z_sig6": m_hi["deg_mean"], "z_sig0.5": m_lo["deg_mean"],
                     "frac_dense": frac_lo, "N_test": n}
    return report


# ====================================================================== #
# MEDICAO CENTRAL: scan de sigma x ladder de N
# ====================================================================== #
SIGMAS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0, 8.0]   # 11: + ancora esparsa
LADDER = [500, 800, 1500, 2200, 3000]
N_SEEDS = 5
SEED_CAP = (2200, 3)           # topo: menos seeds (custo O(N^2) + square-clustering)


def n_cap_for(sigma):
    """Cap de N por sigma: o square-clustering VERBATIM custa ~N*z^2 e z cresce com N
    no regime denso (sigma<d). Mantem cada (sigma) com >=3 pontos de ladder p/ o
    expoente local, capando so o extremo denso caro. Decisao-relevante (sigma>=2.5)
    roda o ladder completo ate 3000."""
    if sigma <= 1.0:
        return 1500
    if sigma <= 2.0:
        return 2200
    return 3000


def run_measurement(sigmas=SIGMAS, ladder=LADDER, n_seeds=N_SEEDS):
    out = {"family": "long-range percolation over causal order",
           "rule": "p(dtau)=min(1,(dtau/dtau0)^-sigma), dtau0=rho^(-1/d) [External]",
           "dim": DIM, "T_box": T_BOX, "L_box": L_BOX, "sigmas": sigmas, "ladder": ladder,
           "n_seeds": n_seeds, "estimator": "rs_clustering.clustering_metrics VERBATIM",
           "by_sigma": {}}
    for sigma in sigmas:
        rows = []
        ncap = n_cap_for(sigma)
        for n_target in ladder:
            if n_target > ncap:
                continue                              # cap denso (custo do square-clustering)
            ns = SEED_CAP[1] if n_target >= SEED_CAP[0] else n_seeds
            rho = n_target / VOL                      # N ~ rho*VOL
            dtau0 = dtau0_for(rho)
            zs, c4s, ctris, fracs, npairs, t0 = [], [], [], [], [], time.perf_counter()
            for s in range(ns):
                rng_pts = np.random.default_rng(10_000 + s + n_target)
                pts = sprinkle_box(rho, BOUNDS, rng_pts)
                n = pts.shape[0]
                edges, info, _ = longrange_edges(
                    pts, sigma, dtau0, np.random.default_rng(20_000 + s + n_target))
                m = clustering_metrics(n, edges)
                zs.append(m["deg_mean"]); c4s.append(m["mean_local_square"])
                ctris.append(m["transitivity"])
                fracs.append(info["n_edges"] / max(info["n_causal_pairs"], 1))
                npairs.append(n)
            dt = time.perf_counter() - t0
            rows.append({"N_target": n_target, "N_mean": float(np.mean(npairs)),
                         "rho": rho, "dtau0": dtau0, "n_seeds": ns,
                         "z_mean": float(np.mean(zs)), "z_sem": float(np.std(zs) / np.sqrt(ns)),
                         "C4": float(np.mean(c4s)), "C4_sem": float(np.std(c4s) / np.sqrt(ns)),
                         "C_trans": float(np.mean(ctris)),
                         "edge_frac": float(np.mean(fracs)), "runtime_s": dt})
            print(f"  sigma={sigma:>4}  N~{n_target:>4}: z={np.mean(zs):8.3f} "
                  f"C4={np.mean(c4s):.4f} frac={np.mean(fracs):.3f} [{dt:.1f}s, {ns}s]")
        # expoentes locais nos dois maiores N efetivamente medidos
        z = np.array([r["z_mean"] for r in rows])
        c4 = np.array([r["C4"] for r in rows])
        Nv = np.array([r["N_mean"] for r in rows], float)
        z_slope = (np.diff(z) / np.diff(np.log(Nv))).tolist() if len(rows) > 1 else []
        c4_slope = (np.diff(c4) / np.diff(np.log(Nv))).tolist() if len(rows) > 1 else []
        out["by_sigma"][f"{sigma}"] = {
            "sigma": sigma, "rows": rows,
            "z_dlnN": z_slope, "c4_dlnN": c4_slope,
            "z_slope_top": z_slope[-1] if z_slope else float("nan"),
            "c4_slope_top": c4_slope[-1] if c4_slope else float("nan")}
    return out


# ====================================================================== #
# VEREDITO (criterios congelados no PRE_REGISTRO Secao 5)
# ====================================================================== #
def verdict(meas, z_rel_thresh=0.05, c4_sat_thresh=0.02, c4_decay_ratio=0.5):
    res = {"per_sigma": {}, "window_sigmas": [],
           "z_saturates_sigmas": [], "c4_positive_sigmas": []}
    for key, R in meas["by_sigma"].items():
        rows = R["rows"]
        z_top = rows[-1]["z_mean"]; z_first = rows[0]["z_mean"]
        c4_top = rows[-1]["C4"]; c4_first = rows[0]["C4"]
        z_slope = R["z_slope_top"]
        c4_slope = R["c4_slope_top"]
        z_rel = (z_slope / z_top) if z_top else 0.0
        z_dec = (len(R["z_dlnN"]) < 2) or (R["z_dlnN"][-1] <= R["z_dlnN"][-2] + 1e-9)
        z_sat = (z_rel < z_rel_thresh) and z_dec
        c4_nondecay = (c4_top >= c4_decay_ratio * c4_first) if c4_first > 0 else False
        c4_pos = (c4_top > c4_sat_thresh) and c4_nondecay
        both = bool(z_sat and c4_pos)
        res["per_sigma"][key] = {
            "sigma": R["sigma"], "z_first": z_first, "z_top": z_top,
            "z_slope_top": z_slope, "z_rel_slope": z_rel, "z_saturates": bool(z_sat),
            "c4_first": c4_first, "c4_top": c4_top, "c4_slope_top": c4_slope,
            "c4_positive_sat": bool(c4_pos), "window": both}
        if z_sat:
            res["z_saturates_sigmas"].append(R["sigma"])
        if c4_pos:
            res["c4_positive_sigmas"].append(R["sigma"])
        if both:
            res["window_sigmas"].append(R["sigma"])
    res["verdict"] = "JANELA_ENCONTRADA" if res["window_sigmas"] else "SEM_JANELA"
    return res


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"
    if mode in ("gate", "all"):
        print("=" * 66 + "\nGATE DE VALIDACAO (percolacao de longo alcance)\n" + "=" * 66)
        g = validation_gate()
        json.dump(g, open(os.path.join(HERE, "validation_gate.json"), "w"), indent=2)
        print(f"\n  GATE {'VERDE' if g['passed'] else 'VERMELHO'}")
        if not g["passed"]:
            print("  ABORTA: sem leitura fisica sem gate verde.")
            sys.exit(1)
    if mode in ("measure", "all"):
        print("\n" + "=" * 66 + "\nMEDICAO CENTRAL: scan de sigma x N\n" + "=" * 66)
        meas = run_measurement()
        v = verdict(meas)
        meas["verdict"] = v
        json.dump(meas, open(os.path.join(HERE, "longrange.json"), "w"), indent=2)
        print("\n" + "=" * 66 + "\nVEREDITO\n" + "=" * 66)
        for key, r in v["per_sigma"].items():
            tag = "JANELA" if r["window"] else (
                "z-sat" if r["z_saturates"] else ("C4>0" if r["c4_positive_sat"] else "--"))
            print(f"  sigma={r['sigma']:>4}: z {r['z_first']:7.2f}->{r['z_top']:7.2f} "
                  f"(slope/z={r['z_rel_slope']:+.3f} {'SAT' if r['z_saturates'] else 'div'}) "
                  f"| C4 {r['c4_first']:.4f}->{r['c4_top']:.4f} "
                  f"({'pos' if r['c4_positive_sat'] else 'decai/0'}) [{tag}]")
        print(f"\n  z satura em sigma = {v['z_saturates_sigmas']}")
        print(f"  C4>0     em sigma = {v['c4_positive_sigmas']}")
        print(f"  JANELA   em sigma = {v['window_sigmas']}")
        print(f"\n  >>> VEREDITO: {v['verdict']}")
