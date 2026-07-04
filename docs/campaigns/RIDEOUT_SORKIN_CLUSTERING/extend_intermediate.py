"""
extend_intermediate.py -- PARTE 1: fechar a fronteira do regime 'intermediate'.

Estende o ladder de N APENAS no regime intermediate (p=0.10), mesmo gerador e
estimador C4 do Gatilho 2 (rs_clustering VERBATIM), para distinguir 'plato genuino
em C4>0' de 'decaimento lento ainda nao convergido'. Diagnostico = expoente local
d(C4)/d(ln N) nos pontos altos.

Criterio (pre-registrado em PARTE 1, nao ajustar depois):
  - exp local negativo e NAO indo a zero  -> decaimento confirmado (morte 3/3 limpa)
  - exp local -> 0 e C4 estabiliza em C4>0 -> plato genuino (fronteira 1/3, nao morte limpa)
  - ambiguo                                -> nao resolvido; reportar N necessario
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "RIDEOUT_SORKIN_TRIGGER"))
from rs_trigger import grow_transitive_percolation  # noqa: E402
import rs_clustering as rc  # noqa: E402

P = 0.10
EXT_LADDER = [6000, 8000, 12000, 16000]
N_SEEDS = 3                       # matches SEED_CAP top-of-ladder of Gatilho 2
# original measured points (from rs_clustering.json), intermediate regime
ORIG = [(500, 0.0200), (1000, 0.0195), (2000, 0.0197), (3300, 0.0192), (3888, 0.0190)]


def run():
    rows = []
    for n in EXT_LADDER:
        c4s, zs, tris, t0 = [], [], [], time.perf_counter()
        for s in range(N_SEEDS):
            rng = np.random.default_rng(2000 + s + n)   # same seeding scheme as Gatilho 2
            anc, _ = grow_transitive_percolation(n, P, rng)
            edges = rc.csg_covering_edges(anc, n)
            m = rc.clustering_metrics(n, edges)
            c4s.append(m["mean_local_square"]); zs.append(m["deg_mean"]); tris.append(m["n_triangles"])
        dt = time.perf_counter() - t0
        rows.append({"N": n, "p": P, "n_seeds": N_SEEDS,
                     "C4": float(np.mean(c4s)), "C4_sem": float(np.std(c4s) / np.sqrt(N_SEEDS)),
                     "z": float(np.mean(zs)), "n_tri": float(np.mean(tris)), "runtime_s": dt})
        print(f"  intermediate N={n:>5}: C4={np.mean(c4s):.4f}+-{np.std(c4s)/np.sqrt(N_SEEDS):.4f} "
              f"z={np.mean(zs):.2f} tri={np.mean(tris):.0f} [{dt:.1f}s]")

    # full curve (orig + extension) and local exponents on the TOP segment
    full = [{"N": n, "C4": c} for n, c in ORIG] + [{"N": r["N"], "C4": r["C4"]} for r in rows]
    Nv = np.array([d["N"] for d in full], float)
    C4 = np.array([d["C4"] for d in full], float)
    slope = np.diff(C4) / np.diff(np.log(Nv))        # d C4 / d ln N
    top_slopes = slope[-4:]                            # over the extended high-N segment
    # relative slope at the very top: |dC4/dlnN| / C4
    rel_top = abs(slope[-1]) / C4[-1]

    # decision logic (pre-registered)
    mean_top = float(np.mean(top_slopes))
    # 'going to zero': top-segment slopes small in magnitude AND not systematically negative-growing
    small = abs(mean_top) < 0.001                      # |dC4/dlnN| < 1e-3 over top segment
    # is the high-N C4 stable within stat error? compare last two extended points
    last_two_consistent = abs(rows[-1]["C4"] - rows[-2]["C4"]) < 2 * (rows[-1]["C4_sem"] + rows[-2]["C4_sem"])
    plateau = small and last_two_consistent and C4[-1] > 0.01
    decaying = (mean_top < -0.001) and not last_two_consistent

    if plateau:
        verdict = "PLATO_GENUINO"
    elif decaying:
        verdict = "DECAIMENTO_CONFIRMADO"
    else:
        verdict = "NAO_RESOLVIDO"

    out = {"regime": "intermediate", "p": P, "ext_ladder": EXT_LADDER, "n_seeds": N_SEEDS,
           "orig_points": [{"N": n, "C4": c} for n, c in ORIG], "ext_rows": rows,
           "full_curve": full, "local_slopes_dC4_dlnN": slope.tolist(),
           "top_segment_slopes": top_slopes.tolist(), "mean_top_slope": mean_top,
           "rel_slope_top": float(rel_top), "C4_top": float(C4[-1]),
           "last_two_consistent_within_2sem": bool(last_two_consistent),
           "verdict": verdict}
    json.dump(out, open(os.path.join(HERE, "extend_intermediate.json"), "w"), indent=2)
    print(f"\n  full C4 curve (N -> C4): "
          + ", ".join(f"{d['N']}:{d['C4']:.4f}" for d in full))
    print(f"  local d(C4)/d(lnN), top segment: {[round(x,5) for x in top_slopes]}")
    print(f"  mean top slope = {mean_top:.5f}  rel_top = {rel_top:.4f}")
    print(f"  last two extended points consistent within 2*SEM: {last_two_consistent}")
    print(f"\n  >>> INTERMEDIATE FRONTEIRA: {verdict}")
    return out


if __name__ == "__main__":
    run()
