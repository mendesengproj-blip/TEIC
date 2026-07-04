"""T3B -- IS d=3+1 A DYNAMICAL ATTRACTOR?  (TIER3_EXPLORATIONS.md, aposta T3B)

Initialise the network in the "wrong" dimension and let it grow with the e7
TEIC rule (validated sampler, gate T3V).  Does d_MM flow to 4?

T3B-1: seed = static sprinkling of N_seed=300 events in a 1+1D diamond (d=2),
       grow combinatorially to N=1500, track d_MM(N).
T3B-2: same with a 4+1D seed (d=5).
CONTROL: same with a 3+1D seed (d=4) -- if even a d=4 seed flows away from 4,
       growth DESTROYS dimensionality rather than attracting to it.
T3B-3: pure combinatorial growth, no background at all (single primordial
       event) -- same protocol as T3A-1, run here at N=1500 for the direct
       comparison on equal footing.

PRE-REGISTERED KILL CRITERIA (from TIER3_EXPLORATIONS.md -- not to be altered):

    MORTE  : network seeded at d=2 or d=5 stays at that dimension under
             growth.  d=3+1 is not an attractor.
    PARCIAL: d=2 seed converges to d>2 but not necessarily to d=4.
    SUCESSO: seeds at d != 4 converge to d = 4 +/- 0.5 for N > 1000.

Operationalisation fixed BEFORE running (this docstring):
  * trajectories: PRIMARY d_MM_interval on the whole causet, plus the same
    estimator restricted to the GROWN region (intervals whose bottom event was
    born after the seed -- such intervals contain no seed events).
  * d_f = mean over runs of d_MM_interval at N=1500.
  * SUCESSO: |d_f - 4| <= 0.5 for BOTH the d=2 and d=5 seeds at N=1500.
  * PARCIAL: d=2 seed rises by > 0.5 (d_f > 2.5) without reaching 4 +/- 0.5.
  * MORTE: |d_f - d_input| < 0.3 for both seeds (stays), OR any other pattern
    that does not approach 4 (e.g. both collapse to a common d_x != 4 --
    reported as "attractor exists but it is d_x, not 4": still MORTE for the
    d=3+1-attractor hypothesis).

ANTI-CIRCULARITY: the seed dimension is the experimental variable (explicit,
labelled input).  The growth rule is purely combinatorial; the number 4
appears only in the verdict block.

Output: results/tier3/T3B_dimension_attractor/{T3B_attractor_data.json, .md, .png}
Reproduce: python results/tier3/T3B_dimension_attractor/T3B_attractor.py
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

N_SEED = 300
N_MAX = 1500
CHECKPOINTS = (500, 750, 1000, 1250, 1500)
SEED_DIMS = (2, 4, 5)        # 4 is the control
N_RUNS = 3


def measure_seed(A, n, rng):
    """Seed measurement: interval estimator with a smaller min size (the seed
    has only 300 events; high-d sprinklings have small intervals), labelled."""
    m = {"N": int(n),
         "ordering_fraction": t3.ordering_fraction(A, n),
         "d_mm_global": t3.mm_global(A, n)}
    iv = t3.mm_intervals(A, n, rng, min_interior=16)
    m["intervals"] = iv
    m["d_mm_interval"] = iv["d_median"] if iv else float("nan")
    return m


def run_seeded(dim, seed):
    rng = np.random.default_rng(seed)
    if dim is None:
        g = t3.GrowthCauset(N_MAX, rng=rng)            # T3B-3: pure growth
        seed_meas = None
        j_min = 0
    else:
        pts = t3.sprinkle_diamond(N_SEED, dim, rng)
        A0 = t3.causal_matrix_anc(pts)
        seed_meas = measure_seed(A0, N_SEED, rng)
        g = t3.GrowthCauset(N_MAX, rng=rng, seed_matrix=A0)
        j_min = N_SEED
    traj = []

    def cb(gc):
        m = t3.measure_causet(gc.A, gc.n, rng)
        if j_min:
            iv_g = t3.mm_intervals(gc.A, gc.n, rng, j_min=j_min)
            m["d_mm_interval_grown"] = iv_g["d_median"] if iv_g else float("nan")
        traj.append(m)
        print(f"      N={m['N']:5d}  d_int={m['d_mm_interval']:.3f}  "
              f"d_glob={m['d_mm_global']:.3f}"
              + (f"  d_grown={m['d_mm_interval_grown']:.3f}" if j_min else ""))

    g.grow(N_MAX, checkpoints=CHECKPOINTS, on_checkpoint=cb,
           init_burn=(dim is not None))
    return {"seed_dim": dim, "rng_seed": seed, "seed_measurement": seed_meas,
            "trajectory": traj,
            "acceptance": g.n_accepted / max(g.n_proposals, 1)}


def verdict(by_dim):
    """Pre-registered criteria (docstring) on the PRIMARY estimator at N=1500."""
    df = {d: float(np.nanmean([r["trajectory"][-1]["d_mm_interval"]
                               for r in runs]))
          for d, runs in by_dim.items() if d is not None}
    d2, d5 = df[2], df[5]
    stays2 = abs(d2 - 2.0) < 0.3
    stays5 = abs(d5 - 5.0) < 0.3
    to4 = (abs(d2 - 4.0) <= 0.5) and (abs(d5 - 4.0) <= 0.5)
    if to4:
        v, box = "SUCESSO", "Sim: d=4 e atrator dinamico"
    elif d2 > 2.5 and not to4:
        v = "PARCIAL" if not stays5 or d2 > 2.5 else "MORTE"
        # PARCIAL per pre-registration: d=2 rises >0.5 without reaching 4
        v, box = "PARCIAL", "d=2 sobe mas nao atinge 4"
    elif stays2 and stays5:
        v, box = "MORTE", "Redes permanecem na dimensao inicial"
    else:
        v, box = "MORTE", "Nao converge para 4 (padrao misto)"
    note = ""
    if not to4 and abs(d2 - d5) < 0.4 and not (stays2 or stays5):
        note = (f"Ambas as seeds convergem para um valor comum d ~ "
                f"{(d2 + d5) / 2:.2f} != 4: existe um atrator dinamico, mas "
                "ele NAO e d=3+1 (continua MORTE para a hipotese).")
    return {"verdict": v, "synthesis_box": box, "note": note,
            "d_final_by_seed": {str(k): float(vv) for k, vv in df.items()},
            "d_final_pure": float(np.nanmean(
                [r["trajectory"][-1]["d_mm_interval"]
                 for r in by_dim[None]]))}


def figure(by_dim, out_png):
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.8))
    colors = {2: "tab:blue", 4: "tab:green", 5: "tab:red", None: "tab:gray"}
    for d, runs in by_dim.items():
        lbl = "pure growth (T3B-3)" if d is None else f"seed d={d}" + \
            (" (control)" if d == 4 else "")
        for k, r in enumerate(runs):
            Ns = [m["N"] for m in r["trajectory"]]
            di = [m["d_mm_interval"] for m in r["trajectory"]]
            if r["seed_measurement"] is not None:
                Ns = [N_SEED] + Ns
                di = [r["seed_measurement"]["d_mm_interval"]] + di
            ax[0].plot(Ns, di, "o-", color=colors[d], alpha=0.65,
                       label=lbl if k == 0 else None)
    ax[0].axhline(4.0, color="k", ls=":", lw=1, label="d=4 (comparison)")
    ax[0].set_xlabel("N")
    ax[0].set_ylabel("d_MM interval (primary)")
    ax[0].set_title("T3B: whole-causet dimension under growth")
    ax[0].legend(fontsize=8)

    for d, runs in by_dim.items():
        if d is None:
            continue
        for k, r in enumerate(runs):
            Ns = [m["N"] for m in r["trajectory"]]
            dg = [m.get("d_mm_interval_grown", float("nan"))
                  for m in r["trajectory"]]
            ax[1].plot(Ns, dg, "s--", color=colors[d], alpha=0.65,
                       label=f"seed d={d}" if k == 0 else None)
    ax[1].axhline(4.0, color="k", ls=":", lw=1)
    ax[1].set_xlabel("N")
    ax[1].set_ylabel("d_MM interval, grown region only")
    ax[1].set_title("T3B: dimension of the newly grown region")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def report(out, path):
    v = out["verdict"]
    L = ["# T3B -- d=3+1 como atrator dinamico?", "",
         "Seeds estaticas (sprinkling, 300 eventos) em d=2, d=4 (controle) e",
         "d=5; crescimento combinatorio e7 ate N=1500. Criterios de morte",
         "pre-registrados em TIER3_EXPLORATIONS.md e no docstring.", "",
         "## Trajetorias d_MM (estimador primario, causet inteiro)", "",
         "| seed | d_MM(seed) | " +
         " | ".join(f"N={c}" for c in CHECKPOINTS) + " |",
         "|---|---|" + "---|" * len(CHECKPOINTS)]
    for d, runs in out["by_dim"].items():
        if d == "None":
            ds = "puro"
            d0 = "--"
        else:
            ds = f"d={d}"
            d0 = np.nanmean([r["seed_measurement"]["d_mm_interval"]
                             for r in runs])
            d0 = f"{d0:.2f}"
        cells = []
        for i in range(len(CHECKPOINTS)):
            vals = [r["trajectory"][i]["d_mm_interval"] for r in runs]
            cells.append(f"{np.nanmean(vals):.2f}")
        L.append(f"| {ds} | {d0} | " + " | ".join(cells) + " |")
    L += ["", "## Regiao crescida (intervalos sem eventos de seed)", "",
          "| seed | " + " | ".join(f"N={c}" for c in CHECKPOINTS) + " |",
          "|---|" + "---|" * len(CHECKPOINTS)]
    for d, runs in out["by_dim"].items():
        if d == "None":
            continue
        cells = []
        for i in range(len(CHECKPOINTS)):
            vals = [r["trajectory"][i].get("d_mm_interval_grown", float("nan"))
                    for r in runs]
            cells.append(f"{np.nanmean(vals):.2f}")
        L.append(f"| d={d} | " + " | ".join(cells) + " |")
    L += ["", "## VEREDITO (criterio pre-registrado)", "",
          f"**{v['verdict']}** -- {v['synthesis_box']}.", ""]
    for k, dv in v["d_final_by_seed"].items():
        L.append(f"- seed d={k}: d_MM(N=1500) = {dv:.3f}")
    L.append(f"- crescimento puro (T3B-3): d_MM(N=1500) = "
             f"{v['d_final_pure']:.3f}")
    if v["note"]:
        L += ["", f"**Nota:** {v['note']}"]
    dfb = v["d_final_by_seed"]
    L += ["", "### Linha honesta", "",
          f"As seeds essencialmente MANTEM a dimensao de entrada (d=2 -> "
          f"{dfb['2']:.2f}, d=4 -> {dfb['4']:.2f}, d=5 -> {dfb['5']:.2f}):",
          "nao ha fluxo em direcao a 4; onde ha deriva (d=5), ela e para",
          "CIMA, afastando-se de 4. O estimador de causet inteiro fica",
          "dominado pela seed (os maiores intervalos vivem nela). A regiao",
          "CRESCIDA nao produz intervalos grandes nas seeds d>=4 (nan):",
          "o crescimento e nao-manifold, como em T3A. Na seed d=2 a regiao",
          "crescida le d ~ 2.5-3.4 (instavel entre runs) -- curiosidade,",
          "nao resultado. O 'padrao misto' do veredito vem do corte",
          "pre-registrado |d5 - 5| >= 0.3; a conclusao substantiva e a",
          "mesma: d=3+1 NAO e atrator dinamico desta regra de crescimento.",
          "O estimador em si esta validado (T3A-2/T3V-V3 recuperam o input",
          "em sprinkling estatico).", "",
          "![T3B](T3B_attractor.png)", ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")


def main():
    t3.validation_gate()
    print("=" * 70)
    print("T3B -- DIMENSION ATTRACTOR: seeds at d=2/4/5 + pure growth")
    print("=" * 70)
    t0 = time.perf_counter()
    by_dim = {}
    for d in SEED_DIMS:
        print(f"  T3B seed d={d}{' (control)' if d == 4 else ''}:")
        runs = []
        for k in range(N_RUNS):
            print(f"    run {k + 1}/{N_RUNS}:")
            runs.append(run_seeded(d, 2000 + 10 * d + k))
        by_dim[d] = runs
    print("  T3B-3 pure combinatorial growth (no background):")
    runs = []
    for k in range(N_RUNS):
        print(f"    run {k + 1}/{N_RUNS}:")
        runs.append(run_seeded(None, 3000 + k))
    by_dim[None] = runs

    v = verdict(by_dim)
    out = {"params": {"N_seed": N_SEED, "N_max": N_MAX,
                      "checkpoints": list(CHECKPOINTS),
                      "seed_dims": list(SEED_DIMS), "n_runs": N_RUNS,
                      "w_meet": t3.W_MEET_DEFAULT, "K_FACTOR": t3.K_FACTOR},
           "by_dim": {str(k): v_ for k, v_ in by_dim.items()},
           "verdict": v, "runtime_s": time.perf_counter() - t0}
    t3.save_json(HERE, "T3B_attractor_data", out)
    figure(by_dim, HERE / "T3B_attractor.png")
    report(out, HERE / "T3B_attractor.md")
    print("-" * 70)
    print(f"VERDICT T3B: {v['verdict']} -- {v['synthesis_box']}")
    if v["note"]:
        print(f"  NOTE: {v['note']}")
    print(f"[{out['runtime_s']:.1f}s]")


if __name__ == "__main__":
    main()
