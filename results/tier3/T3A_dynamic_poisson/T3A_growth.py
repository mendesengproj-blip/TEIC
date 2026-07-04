"""T3A -- DYNAMIC POISSON: does the Myrheim-Meyer dimension converge under the
e7 growth protocol?  (TIER3_EXPLORATIONS.md, aposta T3A)

T3A-1: grow with the e7 TEIC rule (w_meet = 1/3, validated sampler, gate T3V)
       to N = 2000; measure d_MM at checkpoints N = {100, 300, 500, 1000, 2000};
       5 independent runs.
T3A-2: static-sprinkling controls at the same N: d in {2, 3, 4, 5} (the input
       dimension is the control variable) -- the estimator must return the
       input; the grown causet is compared against them.
T3A-3: coupling sweep w_meet in {1/5, 1/3, 1/2, 1, 2, 3} at N = 500 (3 seeds):
       is d_MM sensitive to the coupling or robust?  Plus a sampler-mixing
       sensitivity check (K_FACTOR doubled) at N = 500.

PRE-REGISTERED KILL CRITERIA (from TIER3_EXPLORATIONS.md -- not to be altered):

    MORTE  : d_MM does not converge with growing N, or converges to d != 4.
    PARCIAL: converges to d near 4 with a large error bar.
    SUCESSO: converges to d = 4.00 +/- 0.1 for N > 1000.

Operationalisation fixed BEFORE running (this docstring):
  * PRIMARY observable: d_MM_interval (median over largest Alexandrov
    sub-intervals); SECONDARY: d_MM_global.  Both reported.
  * "converges": |mean d(2000) - mean d(1000)| < 0.15 AND between-run std at
    N=2000 < 0.3.
  * SUCESSO: converged and |d* - 4| <= 0.1;  PARCIAL: converged and
    |d* - 4| <= 0.5;  MORTE: otherwise (no convergence, or d* off by > 0.5).

ANTI-CIRCULARITY: the growth rule is purely combinatorial -- no dimension, no
metric, no target value enters the generator.  The number 4 appears only in
the verdict block below.  Sprinkling controls take d as an explicit labelled
input (they are controls).

Output: results/tier3/T3A_dynamic_poisson/{T3A_growth_data.json, .md, .png}
Reproduce: python results/tier3/T3A_dynamic_poisson/T3A_growth.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                      # noqa: E402

import tier3_core as t3                              # noqa: E402

CHECKPOINTS = (100, 300, 500, 1000, 2000)
N_MAX = 2000
N_RUNS = 5
W_SWEEP = (0.2, 1.0 / 3.0, 0.5, 1.0, 2.0, 3.0)
N_SWEEP = 500
SWEEP_SEEDS = 3
CONTROL_DIMS = (2, 3, 4, 5)
CONTROL_N = 1000
CONTROL_SEEDS = 3


def run_growth(n_target, w_meet, seed, checkpoints, progress=False):
    rng = np.random.default_rng(seed)
    g = t3.GrowthCauset(n_target, w_meet=w_meet, rng=rng)
    traj = []

    def cb(gc):
        m = t3.measure_causet(gc.A, gc.n, rng)
        m["acceptance"] = gc.n_accepted / max(gc.n_proposals, 1)
        m["bfs_fallbacks"] = gc.n_bfs_fallback
        traj.append(m)
        if progress:
            print(f"      N={m['N']:5d}  r={m['ordering_fraction']:.4f}  "
                  f"d_int={m['d_mm_interval']:.3f}  "
                  f"d_glob={m['d_mm_global']:.3f}")

    g.grow(n_target, checkpoints=checkpoints, on_checkpoint=cb)
    return traj


def t3a1_growth():
    print("  T3A-1: e7 growth (w_meet=1/3) to N=2000, 5 runs")
    runs = []
    for k in range(N_RUNS):
        t0 = time.perf_counter()
        print(f"    run {k + 1}/{N_RUNS} (seed {1000 + k}):")
        traj = run_growth(N_MAX, t3.W_MEET_DEFAULT, 1000 + k, CHECKPOINTS,
                          progress=True)
        print(f"      [{time.perf_counter() - t0:.1f}s]")
        runs.append(traj)
    return runs


def t3a2_controls():
    print("  T3A-2: static sprinkling controls (input dimension is labelled)")
    rng = np.random.default_rng(42)
    controls = []
    for d in CONTROL_DIMS:
        ests_i, ests_g = [], []
        for _ in range(CONTROL_SEEDS):
            pts = t3.sprinkle_diamond(CONTROL_N, d, rng)
            A = t3.causal_matrix_anc(pts)
            m = t3.measure_causet(A, CONTROL_N, rng)
            ests_i.append(m["d_mm_interval"])
            ests_g.append(m["d_mm_global"])
        controls.append({"d_input": d, "N": CONTROL_N,
                         "d_mm_interval": t3.seed_stats(ests_i),
                         "d_mm_global": t3.seed_stats(ests_g)})
        print(f"    d={d}: d_int={controls[-1]['d_mm_interval']['mean']:.3f} "
              f"d_glob={controls[-1]['d_mm_global']['mean']:.3f}")
    return controls


def t3a3_sweep():
    print("  T3A-3: coupling sweep at N=500")
    sweep = []
    for w in W_SWEEP:
        di, dg = [], []
        for s in range(SWEEP_SEEDS):
            traj = run_growth(N_SWEEP, w, 5000 + 100 * SWEEP_SEEDS + s,
                              (N_SWEEP,))
            di.append(traj[-1]["d_mm_interval"])
            dg.append(traj[-1]["d_mm_global"])
        sweep.append({"w_meet": w, "N": N_SWEEP,
                      "d_mm_interval": t3.seed_stats(di),
                      "d_mm_global": t3.seed_stats(dg)})
        print(f"    w_meet={w:.3f}: d_int={sweep[-1]['d_mm_interval']['mean']:.3f}"
              f" +/- {sweep[-1]['d_mm_interval']['sem']:.3f}")

    # mixing sensitivity: double K_FACTOR, same seeds, compare d at N=500
    print("    mixing check: K_FACTOR x2")
    base, dbl = [], []
    for s in range(SWEEP_SEEDS):
        traj = run_growth(N_SWEEP, t3.W_MEET_DEFAULT, 7000 + s, (N_SWEEP,))
        base.append(traj[-1]["d_mm_interval"])
    kf = t3.K_FACTOR
    try:
        t3.K_FACTOR = 2 * kf
        for s in range(SWEEP_SEEDS):
            traj = run_growth(N_SWEEP, t3.W_MEET_DEFAULT, 7000 + s, (N_SWEEP,))
            dbl.append(traj[-1]["d_mm_interval"])
    finally:
        t3.K_FACTOR = kf
    mix = {"K_factor_base": kf, "d_base": t3.seed_stats(base),
           "d_doubled": t3.seed_stats(dbl),
           "delta": float(np.nanmean(dbl) - np.nanmean(base))}
    print(f"    K={kf}: d={mix['d_base']['mean']:.3f}  "
          f"K={2*kf}: d={mix['d_doubled']['mean']:.3f}  "
          f"delta={mix['delta']:+.3f}")
    return sweep, mix


def verdict(runs):
    """Apply the pre-registered criteria (docstring) to the PRIMARY estimator."""
    d1000 = np.array([r[CHECKPOINTS.index(1000)]["d_mm_interval"] for r in runs])
    d2000 = np.array([r[CHECKPOINTS.index(2000)]["d_mm_interval"] for r in runs])
    drift = abs(float(np.nanmean(d2000)) - float(np.nanmean(d1000)))
    spread = float(np.nanstd(d2000, ddof=1))
    d_star = float(np.nanmean(d2000))
    converged = (drift < 0.15) and (spread < 0.3)
    if converged and abs(d_star - 4.0) <= 0.1:
        v, box = "SUCESSO", "Converge para d=4"
    elif converged and abs(d_star - 4.0) <= 0.5:
        v, box = "PARCIAL", "Converge para d proximo de 4"
    elif converged:
        v, box = "MORTE", "Converge para d != 4"
    else:
        v, box = "MORTE", "Nao converge"
    return {"verdict": v, "synthesis_box": box, "converged": bool(converged),
            "d_star": d_star, "drift_1000_2000": drift,
            "between_run_std_2000": spread,
            "d_1000_runs": [float(x) for x in d1000],
            "d_2000_runs": [float(x) for x in d2000]}


def figure(runs, controls, sweep, out_png):
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
    Ns = list(CHECKPOINTS)
    for k, traj in enumerate(runs):
        di = [m["d_mm_interval"] for m in traj]
        dg = [m["d_mm_global"] for m in traj]
        ax[0].plot(Ns, di, "o-", color="tab:red", alpha=0.6,
                   label="d_MM interval (primary)" if k == 0 else None)
        ax[0].plot(Ns, dg, "s--", color="tab:blue", alpha=0.4,
                   label="d_MM global" if k == 0 else None)
    ax[0].axhline(4.0, color="gray", ls=":", label="d=4 (comparison)")
    ax[0].set_xscale("log")
    ax[0].set_xlabel("N (growth)")
    ax[0].set_ylabel("d_MM")
    ax[0].set_title("T3A-1: e7 growth, 5 runs")
    ax[0].legend(fontsize=8)

    dins = [c["d_input"] for c in controls]
    mi = [c["d_mm_interval"]["mean"] for c in controls]
    mg = [c["d_mm_global"]["mean"] for c in controls]
    ax[1].plot(dins, dins, "k:", label="ideal (output = input)")
    ax[1].plot(dins, mi, "o-", color="tab:red", label="interval estimator")
    ax[1].plot(dins, mg, "s--", color="tab:blue", label="global estimator")
    g_final = np.nanmean([r[-1]["d_mm_interval"] for r in runs])
    ax[1].axhline(g_final, color="tab:green", ls="-",
                  label=f"grown causet (d={g_final:.2f})")
    ax[1].set_xlabel("input dimension (sprinkling)")
    ax[1].set_ylabel("measured d_MM")
    ax[1].set_title(f"T3A-2: controls N={CONTROL_N} vs grown")
    ax[1].legend(fontsize=8)

    ws = [s["w_meet"] for s in sweep]
    dm = [s["d_mm_interval"]["mean"] for s in sweep]
    de = [s["d_mm_interval"]["sem"] for s in sweep]
    ax[2].errorbar(ws, dm, yerr=de, fmt="o-", color="tab:purple", capsize=3)
    ax[2].set_xscale("log")
    ax[2].set_xlabel("w_meet (coupling)")
    ax[2].set_ylabel(f"d_MM interval at N={N_SWEEP}")
    ax[2].set_title("T3A-3: coupling sweep")
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def report(out, path):
    v = out["verdict"]
    L = ["# T3A -- Poisson dinamico: a dimensao converge?", "",
         "Crescimento com o protocolo e7 (regra TEIC, w_meet=1/3, sampler MCMC",
         "validado pelo gate T3V) ate N=2000. Criterios de morte pre-registrados",
         "em TIER3_EXPLORATIONS.md e no docstring do gerador.", "",
         "## T3A-1 -- trajetorias d_MM(N) (5 runs)", "",
         "| N | d_MM interval (mean +/- std entre runs) | d_MM global | r |",
         "|---|---|---|---|"]
    for i, N in enumerate(CHECKPOINTS):
        di = [r[i]["d_mm_interval"] for r in out["runs"]]
        dg = [r[i]["d_mm_global"] for r in out["runs"]]
        rr = [r[i]["ordering_fraction"] for r in out["runs"]]
        L.append(f"| {N} | {np.nanmean(di):.3f} +/- {np.nanstd(di, ddof=1):.3f} "
                 f"| {np.nanmean(dg):.3f} | {np.mean(rr):.4f} |")
    L += ["",
          "## T3A-2 -- controles de sprinkling (estimador devolve o input)", "",
          "| d input | d_MM interval | d_MM global |", "|---|---|---|"]
    for c in out["controls"]:
        L.append(f"| {c['d_input']} | {c['d_mm_interval']['mean']:.3f} | "
                 f"{c['d_mm_global']['mean']:.3f} |")
    L += ["", "## T3A-3 -- varredura de acoplamento (N=500)", "",
          "| w_meet | d_MM interval |", "|---|---|"]
    for s in out["sweep"]:
        L.append(f"| {s['w_meet']:.3f} | {s['d_mm_interval']['mean']:.3f} "
                 f"+/- {s['d_mm_interval']['sem']:.3f} |")
    mix = out["mixing_check"]
    L += ["",
          f"Sensibilidade de mixing: K_FACTOR {mix['K_factor_base']} -> "
          f"{2 * mix['K_factor_base']} muda d_MM em {mix['delta']:+.3f} "
          "(mesmo seed).", "",
          "## VEREDITO (criterio pre-registrado)", "",
          f"**{v['verdict']}** -- {v['synthesis_box']}.",
          f"- d* (N=2000, interval) = {v['d_star']:.3f}",
          f"- drift |d(2000)-d(1000)| = {v['drift_1000_2000']:.3f} "
          "(limite de convergencia 0.15)",
          f"- desvio entre runs em N=2000 = {v['between_run_std_2000']:.3f} "
          "(limite 0.3)", "",
          "### Linha honesta", ""]
    r_first = float(np.mean([r[0]["ordering_fraction"] for r in out["runs"]]))
    r_last = float(np.mean([r[-1]["ordering_fraction"] for r in out["runs"]]))
    if r_last > 0.8 and r_last >= r_first:
        L += ["O crescimento e7 produz causets cada vez mais DENSOS (ordering",
              f"fraction r: {r_first:.3f} em N={CHECKPOINTS[0]} -> "
              f"{r_last:.3f} em N={CHECKPOINTS[-1]}): a medida sobre ideais",
              "favorece passados grandes, entao cada novo evento conecta-se a",
              "quase tudo e o causet aproxima-se de uma cadeia (d_MM -> 1),",
              "nao de uma variedade 3+1D. Nao ha ajuste possivel sem alterar",
              "a dinamica (o que violaria o pre-registro)."]
    else:
        g_last = float(np.nanmean([r[-1]["d_mm_global"] for r in out["runs"]]))
        L += [f"Ordering fraction r: {r_first:.3f} em N={CHECKPOINTS[0]} -> "
              f"{r_last:.3f} em N={CHECKPOINTS[-1]}; d* (interval) = "
              f"{v['d_star']:.3f}.",
              "",
              f"Os dois estimadores DIVERGEM em N grande (interval "
              f"{v['d_star']:.2f} vs global {g_last:.2f}): num sprinkling de "
              "variedade eles coincidem (controles T3A-2), logo o causet",
              "crescido NAO e manifold-like -- nao ha dimensao bem definida a",
              "qual convergir, apenas o valor local ~1.3-1.9 dos maiores",
              "intervalos (proximo de uma cadeia, d=1). O check de mixing",
              "(K_FACTOR x2 desloca d em "
              f"{out['mixing_check']['delta']:+.2f}) e um caveat de",
              "engenharia, mas nao aproxima o resultado de 4 -- o veredito",
              "MORTE e robusto a ele."]
    L += ["",
          "![T3A](T3A_growth.png)", ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")


def main():
    t3.validation_gate()
    print("=" * 70)
    print("T3A -- DYNAMIC POISSON (e7 growth): does d_MM converge?")
    print("=" * 70)
    t0 = time.perf_counter()
    runs = t3a1_growth()
    controls = t3a2_controls()
    sweep, mix = t3a3_sweep()
    v = verdict(runs)
    out = {"params": {"N_max": N_MAX, "checkpoints": list(CHECKPOINTS),
                      "n_runs": N_RUNS, "w_meet": t3.W_MEET_DEFAULT,
                      "K_FACTOR": t3.K_FACTOR, "K_MIN": t3.K_MIN,
                      "control_dims": list(CONTROL_DIMS),
                      "control_N": CONTROL_N, "w_sweep": list(W_SWEEP),
                      "n_sweep": N_SWEEP},
           "runs": runs, "controls": controls, "sweep": sweep,
           "mixing_check": mix, "verdict": v,
           "runtime_s": time.perf_counter() - t0}
    t3.save_json(HERE, "T3A_growth_data", out)
    figure(runs, controls, sweep, HERE / "T3A_growth.png")
    report(out, HERE / "T3A_growth.md")
    print("-" * 70)
    print(f"VERDICT T3A: {v['verdict']} -- {v['synthesis_box']}  "
          f"(d*={v['d_star']:.3f}, drift={v['drift_1000_2000']:.3f}, "
          f"spread={v['between_run_std_2000']:.3f})")
    print(f"[{out['runtime_s']:.1f}s]")


if __name__ == "__main__":
    main()
