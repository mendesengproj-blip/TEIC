"""EXP 1 -- Saturacao espontanea (teste de morte precoce).

Pergunta: rodando a rede causal de TEIC SEM nenhum criterio de colapso embutido,
chi_eff = lambda_max/N atinge regime de saturacao por conta propria conforme a
rede cresce em ordem de Hasse?

KILL-CRITERION (pre-registrado em PRE_REGISTRO.md, secao 2):
  MORTE  se NENHUMA ordem-parametro (chi_A, chi_L, chi_BD) satura em NENHUM N.
  SOBREVIVE se >=1 satura (cauda <10%, N-estavel <15%, chi_plato > 2/N) em >=1 N.

Nada ajustado. Reusa sr_teic_core (que reusa tier3_core/c5_core validados).
"""
from __future__ import annotations
import json, platform, sys
from datetime import datetime, timezone
import numpy as np
import sr_teic_core as core

SEEDS = list(range(8))                      # fixas e registradas
NS = [50, 100, 200, 500]
DIMS = [2, 4]
FRACS = np.linspace(0.15, 1.0, 12)          # prefixos de crescimento causal
PARAMS = ("chi_A", "chi_L", "chi_BD")       # ordens-parametro candidatas


def run_dim(dim):
    """Ensemble de trajetorias de crescimento; medias por N; teste de plato."""
    per_N = {}
    for N in NS:
        trajs = []
        for sd in SEEDS:
            rng = np.random.default_rng(1000 * dim + sd)
            pts = core.sprinkle(N, dim, rng)
            trajs.append(core.growth_trajectory(pts, FRACS))
        # alinhar por fracao (n pode variar 1 evento entre seeds; usa a media)
        nmean = np.mean([t["n"] for t in trajs], axis=0)
        agg = {"n": nmean}
        for key in ("chi_A", "R", "chi_L", "chi_BD", "S"):
            stack = np.array([t[key] for t in trajs])
            agg[key + "_mean"] = stack.mean(axis=0)
            agg[key + "_sem"] = stack.std(axis=0, ddof=1) / np.sqrt(len(SEEDS))
        per_N[N] = agg
    return per_N


def evaluate(per_N):
    """Aplica o teste de plato pre-registrado a cada ordem-parametro e N, e a
    estabilidade-N entre N=200 e N=500."""
    res = {}
    for p in PARAMS:
        res[p] = {"by_N": {}}
        for N in NS:
            pt = core.plateau_test(per_N[N]["n"], per_N[N][p + "_mean"], N)
            res[p]["by_N"][N] = pt
        # estabilidade-N (200 vs 500): |chi(500)-chi(200)|/chi(200) < 0.15
        c200 = res[p]["by_N"][200]["plateau"]
        c500 = res[p]["by_N"][500]["plateau"]
        nstab = abs(c500 - c200) / c200 if c200 > 1e-12 else np.inf
        res[p]["nstab_200_500"] = float(nstab)
        res[p]["nstab_ok"] = bool(nstab < 0.15)
        # SOBREVIVE se algum N satisfaz (drift_ok & above_floor) E nstab_ok
        saturates = [N for N in NS
                     if res[p]["by_N"][N]["drift_ok"] and res[p]["by_N"][N]["above_floor"]]
        res[p]["saturating_N"] = saturates
        res[p]["survives"] = bool(saturates and res[p]["nstab_ok"])
    return res


def main():
    payload = {"experiment": "EXP1_saturation", "seeds": SEEDS, "Ns": NS,
               "dims": DIMS, "fracs": FRACS.tolist(), "by_dim": {}}
    verdict_lines = []
    any_survive = False
    for dim in DIMS:
        per_N = run_dim(dim)
        ev = evaluate(per_N)
        # serializar trajetorias (medias) + avaliacao
        payload["by_dim"][dim] = {
            "trajectories": {str(N): {k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                      for k, v in per_N[N].items()} for N in NS},
            "evaluation": ev,
        }
        for p in PARAMS:
            surv = ev[p]["survives"]
            any_survive = any_survive or surv
            plat500 = ev[p]["by_N"][500]["plateau"]
            dr500 = ev[p]["by_N"][500]["tail_drift"]
            verdict_lines.append(
                f"  dim={dim} {p:6s}: plateau(N=500)={plat500:.3f} drift={dr500:.3f} "
                f"nstab={ev[p]['nstab_200_500']:.3f} satN={ev[p]['saturating_N']} "
                f"-> {'SOBREVIVE' if surv else 'nao satura'}")
    payload["verdict"] = {
        "any_order_parameter_saturates": bool(any_survive),
        "result": "SOBREVIVE" if any_survive else "MORTE",
    }
    payload["_meta"] = {"timestamp": datetime.now(timezone.utc).isoformat(),
                        "python": sys.version.split()[0], "numpy": np.__version__,
                        "platform": platform.platform()}
    out = core.HERE / "exp1_saturation.json"
    out.write_text(json.dumps(payload, indent=2))
    print("=" * 72)
    print("EXP 1 -- SATURACAO ESPONTANEA")
    print("=" * 72)
    print("\n".join(verdict_lines))
    print("-" * 72)
    print(f"VEREDITO EXP1: {payload['verdict']['result']}  "
          f"(>=1 ordem-parametro satura: {any_survive})")
    print(f"JSON -> {out.name}")


if __name__ == "__main__":
    main()
