"""CC4 -- is the internal complexity N conserved under perturbation?

A structure of N internal cycles, when jostled by the causal medium, either keeps
its N (a conserved quantity -> a candidate quantum number / identity through motion)
or loses cycles (complexity is dynamical -> the analogue of pair production /
annihilation).  Both outcomes are physically meaningful; we MEASURE which happens.

PERTURBATION (the causal-medium kick that drives CC2's embedding): each structure
event is displaced by a random medium fluctuation of amplitude delta in (t, x), plus
a deterministic shear from the D3 theta-gradient (a linear compressive bias toward a
source).  We sweep delta from 0 up past the diamond half-width branch_w.

EFFECTIVE COMPLEXITY after perturbation = number of diamonds whose cycle SURVIVES,
i.e. whose causal relations still hold:
    S < B+,  S < B-,  B+ < M,  B- < M,  and  B+, B- mutually spacelike.
If a kick makes the two branches causally related (one precedes the other) the
diamond collapses to a chain and the cycle is destroyed (Betti drops).  This is pure
causal-order bookkeeping -- no physics inserted.

Output: CC4_conservation.{md,json,png}.
"""

from __future__ import annotations

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import complexity_core as cc

N_TEST = [3, 10, 30]
BRANCH_W = 0.3
DELTAS = np.array([0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.45, 0.60]) * BRANCH_W
SEEDS = range(20)
GRAD = 0.04          # deterministic theta-gradient shear coefficient (compressive)


def _precedes(a, b):
    dt = b[0] - a[0]
    return dt > 0 and dt * dt > (b[1] - a[1]) ** 2


def _spacelike(a, b):
    dt = abs(a[0] - b[0])
    return dt * dt < (a[1] - b[1]) ** 2


def perturb(struct, delta, rng):
    """Return perturbed event coordinates: random medium kick (amplitude delta) plus a
    deterministic theta-gradient shear (compresses x toward the worldline centre)."""
    ev = struct["events"].copy()
    x0 = ev[:, 1].mean()
    ev[:, 0] += delta * rng.standard_normal(len(ev))
    ev[:, 1] += delta * rng.standard_normal(len(ev)) - GRAD * (ev[:, 1] - x0)
    return ev


def surviving_cycles(struct, ev):
    """Number of diamonds whose cycle survives in the perturbed coordinates."""
    n = 0
    for (s, bp, bm, m) in struct["diamonds"]:
        S, Bp, Bm, M = ev[s], ev[bp], ev[bm], ev[m]
        ok = (_precedes(S, Bp) and _precedes(S, Bm) and
              _precedes(Bp, M) and _precedes(Bm, M) and _spacelike(Bp, Bm))
        n += int(ok)
    return n


def main():
    print("=" * 70)
    print("CC4 -- CONSERVATION OF INTERNAL COMPLEXITY N UNDER PERTURBATION")
    print("=" * 70)
    table = {}
    for N in N_TEST:
        s = cc.build_structure(N, branch_w=BRANCH_W)
        per_delta = []
        for delta in DELTAS:
            surv = []
            for seed in SEEDS:
                rng = np.random.default_rng(4000 + seed + int(delta * 1e4))
                surv.append(surviving_cycles(s, perturb(s, delta, rng)))
            st = cc.seed_stats(surv)
            per_delta.append(st)
        table[N] = per_delta
        frac0 = per_delta[0]["mean"] / N
        # critical delta: first where mean surviving < 0.95 N
        dc = None
        for delta, st in zip(DELTAS, per_delta):
            if st["mean"] < 0.95 * N:
                dc = float(delta); break
        print(f"  N={N:3d}: surviving at delta=0 -> {per_delta[0]['mean']:.1f}/{N} "
              f"(frac {frac0:.2f}); delta_c(95%) = "
              f"{'none' if dc is None else f'{dc:.3f}'}")

    # conservation regime: at the smallest non-zero delta, is N preserved?
    small = DELTAS[1]
    si = 1
    preserved = all(table[N][si]["mean"] > 0.97 * N for N in N_TEST)
    # breaking regime: at the largest delta, is there significant loss?
    breaks = all(table[N][-1]["mean"] < 0.85 * N for N in N_TEST)

    if preserved and breaks:
        verdict, grade = "CONSERVADO (perturbacao pequena) / QUEBRA (grande)", "A"
        statement = ("N is CONSERVED for small medium kicks (>97%% of cycles survive at "
                     "delta=%.3f, ~%.0f%% of the diamond half-width) -- the complexity is "
                     "a topologically stable quantity, an identity carried through motion. "
                     "For large kicks (delta ~ branch_w) cycles are destroyed (>15%% lost), "
                     "the analogue of pair annihilation. Both regimes are present, exactly "
                     "the expected behaviour." % (small, 100 * small / BRANCH_W))
    elif preserved:
        verdict, grade = "CONSERVADO", "B"
        statement = ("N is conserved for the perturbations tested; no clean breaking "
                     "regime was reached at the largest delta.")
    else:
        verdict, grade = "NAO CONSERVADO", "C"
        statement = ("Even small perturbations destroy cycles -- the constructed "
                     "complexity is fragile, not a robust conserved number.")
    print("-" * 70)
    print(f"VERDICT CC4: {verdict}  (grade {grade})")
    print(f"  {statement}")

    _figure(table)
    out = {"N_test": N_TEST, "branch_w": BRANCH_W, "gradient_shear": GRAD,
           "deltas": DELTAS.tolist(), "n_seeds": len(list(SEEDS)),
           "surviving": {str(N): [{"delta": float(d), **st}
                                   for d, st in zip(DELTAS, table[N])] for N in N_TEST},
           "preserved_small": bool(preserved), "breaks_large": bool(breaks),
           "verdict": verdict, "grade": grade, "statement": statement}
    cc.save_json("CC4_conservation", out)
    _write_md(table, out)
    return out


def _figure(table):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    for N in N_TEST:
        m = np.array([st["mean"] for st in table[N]])
        e = np.array([st["sem"] for st in table[N]])
        ax.errorbar(DELTAS / BRANCH_W, m / N, yerr=e / N, fmt="o-", capsize=3,
                    label=f"N={N}")
    ax.axhline(1.0, color="k", lw=0.8, ls="--")
    ax.set_xlabel("perturbation amplitude  delta / branch_w")
    ax.set_ylabel("fraction of cycles surviving  (effective N / N)")
    ax.set_title("CC4 -- conservation of internal complexity under perturbation")
    ax.legend()
    fig.tight_layout()
    fig.savefig(cc.OUTDIR / "CC4_conservation.png", dpi=130)
    plt.close(fig)


def _write_md(table, out):
    lines = [
        "# CC4 -- Conservação da complexidade interna N",
        "",
        "Uma estrutura de N ciclos, sob perturbação do meio causal, ou mantém N (número",
        "conservado → identidade através do movimento) ou perde ciclos (complexidade",
        "dinâmica → análogo a produção/aniquilação de pares). Medimos qual ocorre.",
        "",
        "Perturbação: kick aleatório do meio (amplitude δ em t,x) + cisalhamento",
        f"determinístico do gradiente de θ (coef {out['gradient_shear']}). Meia-largura",
        f"do diamante branch_w = {out['branch_w']}.",
        "",
        "Fração de ciclos sobreviventes (N_efetivo / N):",
        "",
        "| δ/branch_w | " + " | ".join(f"N={N}" for N in out["N_test"]) + " |",
        "|" + "---|" * (len(out["N_test"]) + 1),
    ]
    for i, d in enumerate(DELTAS):
        cells = " | ".join(f"{table[N][i]['mean']/N:.2f}" for N in out["N_test"])
        lines.append(f"| {d/BRANCH_W:.2f} | {cells} |")
    lines += [
        "",
        f"- preservado para perturbação pequena: **{out['preserved_small']}**",
        f"- quebra para perturbação grande: **{out['breaks_large']}**",
        "",
        f"## VERDICT CC4: {out['verdict']}  (grade {out['grade']})",
        "",
        out["statement"],
        "",
        "![conservacao](CC4_conservation.png)",
        "",
    ]
    (cc.OUTDIR / "CC4_conservation.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
