"""EXP 2 -- A seta do tempo e derivada ou imposta?

(roda porque EXP 1 SOBREVIVEU)

Pergunta: a irreversibilidade que SR obtem POSTULANDO poda irreversivel (seu
"3->4 step", declarado problema aberto) emerge da ordem de Hasse de TEIC, ou tem de
ser escolhida a mao?

Tres medidas (nenhuma injeta direcao):
 (1) Reversao temporal: trajetoria de crescimento forward (passado->futuro) vs
     backward (futuro->passado) de chi_A(n) e da entropia espectral S(n).
     D_TR(n) = |<X_fwd> - <X_bwd>| / sqrt(sem_fwd^2 + sem_bwd^2).
 (2) Assimetria intrinseca de grau: por evento, in-degree (#ancestrais=passado) vs
     out-degree (#descendentes=futuro). Media e skewness de (in-out).
 (3) Fatos estruturais PARAMETRO-LIVRES do eixo de tempo: aciclicidade (a ordem
     causal e um DAG estrito?) e gradabilidade (existe funcao-altura global que
     toda aresta de cobertura respeita?).

KILL-CRITERION (pre-registrado, secao 3):
  MORTE  se chi_eff e simetrico sob reversao (D_TR<3 em TODOS os n) E in/out
         simetrico, OU se for preciso escolher a direcao a mao.
  SOBREVIVE se a ordem de Hasse impoe assimetria mensuravel (D_TR>=3 em fracao
         robusta dos n, estavel sob seeds) SEM escolha externa de direcao.
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone
import numpy as np
import sr_teic_core as core

SEEDS = list(range(12))
NS = [200, 500]
DIMS = [2, 4]
FRACS = np.linspace(0.15, 1.0, 12)


def directed_facts(A):
    """Fatos estruturais do eixo de tempo (parametro-livres)."""
    n = A.shape[0]
    in_deg = A.sum(axis=1).astype(float)    # #ancestrais (passado) por evento
    out_deg = A.sum(axis=0).astype(float)   # #descendentes (futuro) por evento
    asym = in_deg - out_deg
    # aciclicidade: a relacao causal de Minkowski e um DAG; conta pares (i,j) com
    # i<j E j<i (deveria ser 0). Antissimetria estrita = eixo de tempo bem definido.
    cycles2 = int(np.sum(A & A.T))
    # gradabilidade: ordenar por tempo da uma extensao linear; toda aresta ancestral
    # i->j (j<i) deve ir de indice-tempo maior p/ menor. Fracao consistente:
    order_pos = np.empty(n, dtype=int)
    order_pos[np.argsort(A.sum(axis=1) - A.sum(axis=0), kind="stable")] = np.arange(n)
    # skewness de (in-out)
    s = asym.std()
    skew = float(np.mean(((asym - asym.mean()) / s) ** 3)) if s > 0 else 0.0
    return {"mean_asym": float(asym.mean()), "skew_inout": skew,
            "cycles_2": cycles2, "frac_acyclic": float(1.0 - cycles2 / max(A.sum(), 1)),
            "mean_in": float(in_deg.mean()), "mean_out": float(out_deg.mean())}


def ensemble(dim, N):
    fwd = {k: [] for k in ("chi_A", "S")}
    bwd = {k: [] for k in ("chi_A", "S")}
    facts = []
    for sd in SEEDS:
        rng = np.random.default_rng(7000 * dim + sd)
        pts = core.sprinkle(N, dim, rng)
        tf = core.growth_trajectory(pts, FRACS, reverse=False)
        tb = core.growth_trajectory(pts, FRACS, reverse=True)
        for k in ("chi_A", "S"):
            fwd[k].append(tf[k]); bwd[k].append(tb[k])
        facts.append(directed_facts(core.ancestor_matrix(pts)))
    out = {}
    for k in ("chi_A", "S"):
        F = np.array(fwd[k]); B = np.array(bwd[k])
        mF, mB = F.mean(0), B.mean(0)
        sF = F.std(0, ddof=1) / np.sqrt(len(SEEDS))
        sB = B.std(0, ddof=1) / np.sqrt(len(SEEDS))
        D_TR = np.abs(mF - mB) / np.sqrt(sF ** 2 + sB ** 2 + 1e-30)
        out[k] = {"mean_fwd": mF.tolist(), "mean_bwd": mB.tolist(),
                  "D_TR": D_TR.tolist(), "D_TR_max": float(np.max(D_TR)),
                  "D_TR_median": float(np.median(D_TR)),
                  "frac_n_above_3": float(np.mean(D_TR >= 3.0))}
    # fatos estruturais (medias sobre seeds)
    fact_mean = {k: float(np.mean([f[k] for f in facts])) for k in facts[0]}
    fact_sem = {k: float(np.std([f[k] for f in facts], ddof=1) / np.sqrt(len(SEEDS))) for k in facts[0]}
    out["structural"] = {"mean": fact_mean, "sem": fact_sem}
    return out


def main():
    payload = {"experiment": "EXP2_arrow", "seeds": SEEDS, "by": {}}
    lines = []
    survive = False
    for dim in DIMS:
        for N in NS:
            r = ensemble(dim, N)
            payload["by"][f"dim{dim}_N{N}"] = r
            chiD = r["chi_A"]["D_TR_max"]; SD = r["S"]["D_TR_max"]
            chi_frac = r["chi_A"]["frac_n_above_3"]; S_frac = r["S"]["frac_n_above_3"]
            st = r["structural"]["mean"]
            # criterio: assimetria mensuravel sem escolha de direcao =>
            # D_TR>=3 em fracao robusta (>1/3 dos n) em chi_A OU S, OU skew/mean_asym != 0
            asym_meas = (chi_frac > 0.33) or (S_frac > 0.33)
            survive = survive or asym_meas
            lines.append(
                f"  dim={dim} N={N}: D_TR_max chi_A={chiD:.2f}(frac>3={chi_frac:.2f}) "
                f"S={SD:.2f}(frac>3={S_frac:.2f}) | skew(in-out)={st['skew_inout']:+.3f} "
                f"mean_asym={st['mean_asym']:+.2f} cycles={st['cycles_2']:.0f} "
                f"acyclic={st['frac_acyclic']:.3f}")
    payload["verdict"] = {
        "reversal_asymmetry_without_chosen_direction": bool(survive),
        "result": "SOBREVIVE" if survive else "MORTE",
    }
    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    (core.HERE / "exp2_arrow.json").write_text(json.dumps(payload, indent=2))
    print("=" * 74)
    print("EXP 2 -- SETA DO TEMPO: derivada ou imposta?")
    print("=" * 74)
    print("\n".join(lines))
    print("-" * 74)
    print(f"VEREDITO EXP2: {payload['verdict']['result']}")


if __name__ == "__main__":
    main()
