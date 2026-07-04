"""SC3 -- the emergent coefficient: constancy in g, scaling with granularity.

Two measurements (pre-registered expectations in parentheses):
  1. c_K(g) plateau: the commutator coefficient extracted at several g is
     constant as g->0 (the operator coefficient is well-defined; departure ~g^2).
  2. granularity scaling: c_K(a) ~ a^4 per link (slope 4 in log-log), and the
     emergent Skyrme LENGTH lambda_Sk^2 = (c_K per unit K)/(c_2 per unit TrG)
     = a^2/120 (slope 2): the stabiliser length scale IS the granularity.

Cross-relation hook (Ataque 6): the same granularity scale that fixes G ~ 1/K
(D3D audit) fixes lambda_Sk = a/sqrt(120) -- one scale, two sectors.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sc_core as sc

N_DIR = 200_000
N_SEEDS = 20
G_LIST = [0.02, 0.05, 0.1, 0.2, 0.4]
A_LIST = [0.25, 0.5, 1.0, 2.0, 4.0]
_, _, K_B_UNIT = sc.invariants(sc.config_B(1.0))        # = 6 per unit g^4


def c_K(g, a_link, dirs):
    """Commutator coefficient from the A/B residual difference (per unit K)."""
    rA = sc.quartic_residual(sc.config_A(g), dirs, a_link) / g ** 4
    rB = sc.quartic_residual(sc.config_B(g), dirs, a_link) / g ** 4
    return (rB - rA) / K_B_UNIT


def main():
    # ---- 1. plateau in g (a=1), 20 seeds ----------------------------------- #
    plateau = []
    for g in G_LIST:
        vals = []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(3000 + seed)
            dirs = sc.isotropic_directions(N_DIR, rng)
            vals.append(c_K(g, 1.0, dirs))
        plateau.append(sc.seed_stats(vals))
    pred_cK_a1 = 1.0 / 2880.0

    # ---- 2. scaling with the link scale a (g small fixed), 20 seeds -------- #
    scaling = []
    for a in A_LIST:
        g = 0.05 / a                       # keep a*g fixed -> same numerical regime
        vals = []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(4000 + seed)
            dirs = sc.isotropic_directions(N_DIR, rng)
            vals.append(c_K(g, a, dirs))
        scaling.append(sc.seed_stats(vals))
    loga = np.log(A_LIST)
    logc = np.log([s["mean"] for s in scaling])
    slope_cK = float(np.polyfit(loga, logc, 1)[0])

    # lambda_Sk^2 = c_K / c_2 with c_2 = a^2/24 per unit TrG (per link)
    lam2 = [s["mean"] / (a ** 2 / 24.0) for s, a in zip(scaling, A_LIST)]
    slope_lam2 = float(np.polyfit(loga, np.log(lam2), 1)[0])
    pred_lam2_over_a2 = 1.0 / 120.0

    payload = {
        "params": {"n_dirs": N_DIR, "n_seeds": N_SEEDS, "g_list": G_LIST,
                   "a_list": A_LIST},
        "plateau_g": {"g": G_LIST, "c_K": plateau,
                      "predicted_a1": pred_cK_a1},
        "scaling_a": {"a": A_LIST, "c_K": scaling,
                      "slope_loglog": slope_cK, "predicted_slope": 4.0,
                      "lambda_Sk2_over_a2": [l / a ** 2 for l, a in
                                             zip(lam2, A_LIST)],
                      "predicted_lambda_Sk2_over_a2": pred_lam2_over_a2,
                      "slope_lambda2": slope_lam2,
                      "predicted_slope_lambda2": 2.0},
        "cross_relation_note": (
            "lambda_Sk = a/sqrt(120): the emergent Skyrme length is the "
            "granularity. The same scale enters G ~ 1/K (D3D). Dimensionless "
            "cross-ratio for Ataque 6: lambda_Sk^2 * K_rigidity ~ const."),
    }
    sc.save_json("SC3_coefficient.json", payload)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    means = [s["mean"] for s in plateau]
    sems = [s["sem"] for s in plateau]
    ax1.errorbar(G_LIST, means, yerr=sems, fmt="o-", color="tab:blue")
    ax1.axhline(pred_cK_a1, color="k", ls=":", label="predicted a$^4$/2880")
    ax1.set_xscale("log")
    ax1.set_xlabel("g")
    ax1.set_ylabel(r"$c_K$ (a=1)")
    ax1.set_title("commutator coefficient: plateau in g")
    ax1.legend(fontsize=8)

    ax2.errorbar(A_LIST, [s["mean"] for s in scaling],
                 yerr=[s["sem"] for s in scaling], fmt="o", color="tab:blue",
                 label=f"$c_K(a)$, slope {slope_cK:.3f} (pred 4)")
    aa = np.linspace(min(A_LIST), max(A_LIST), 50)
    ax2.plot(aa, aa ** 4 / 2880.0, "k:", label="a$^4$/2880")
    ax2.set_xscale("log")
    ax2.set_yscale("log")
    ax2.set_xlabel("link scale a (granularity)")
    ax2.set_ylabel(r"$c_K$")
    ax2.set_title(f"$\\lambda^2_{{Sk}}/a^2$ = {np.mean([l/a**2 for l, a in zip(lam2, A_LIST)]):.5f} "
                  f"(pred 1/120 = {1/120:.5f})")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SC3_coefficient.png", dpi=150)

    print(json.dumps({"plateau_means": means,
                      "scaling_slope": slope_cK,
                      "lambda2_over_a2": payload["scaling_a"]["lambda_Sk2_over_a2"],
                      "slope_lambda2": slope_lam2}, indent=2))


if __name__ == "__main__":
    main()
