"""SC2 -- the decisive constant-field test: does the commutator (Skyrme) piece
appear in the quartic residual of the SU(2) link cosine?

Pre-registered predictions (BRIDGE_SU2_COEFF.md, written before this ran):

  config A (abelian-like, K=0):     c_x=c_y=c_z=g(1,0,0)   -> 3S-2K = 27 g^4
  config B (hedgehog-like, K=6g^4): c_mu = g e_mu           -> 3S-2K = 15 g^4

  Poisson (isotropic) measure: r4(B)/r4(A) = 15/27 = 5/9 = 0.5556  (Skyrme present)
  cubic 3-axis measure:        r4(B)/r4(A) = 1.0000 exactly        (K-blind control)
  commutator coefficient:      c_K = (r4(B)-r4(A)) g^4... = +a^4/2880 (stabilising sign)

  DEATH CRITERION: Poisson ratio = 1.0 too  ->  quartic purely symmetric, verdict C.

r4 = per-link mean of [E_link - a^2|l_e|^2/8] / g^4, the quadratic term subtracted
sample-by-sample (exact), so only the quartic average fluctuates. 20 seeds.
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

A_LINK = 1.0
G_SMALL = 0.05          # quartic regime: g^6 corrections ~ g^2 = 2.5e-3 relative
N_DIR = 200_000
N_SEEDS = 20
GRID_G = [0.02, 0.05, 0.1, 0.2, 0.4, 0.8]   # plateau scan (feeds SC3)


def residuals_for_seed(rng, g):
    dirs = sc.isotropic_directions(N_DIR, rng)
    CA, CB = sc.config_A(g), sc.config_B(g)
    r4A = sc.quartic_residual(CA, dirs, A_LINK) / g ** 4
    r4B = sc.quartic_residual(CB, dirs, A_LINK) / g ** 4
    return r4A, r4B


def main():
    # ---- Poisson measure, 20 seeds ----------------------------------------- #
    rAs, rBs = [], []
    for seed in range(N_SEEDS):
        rng = np.random.default_rng(1000 + seed)
        rA, rB = residuals_for_seed(rng, G_SMALL)
        rAs.append(rA)
        rBs.append(rB)
    stA, stB = sc.seed_stats(rAs), sc.seed_stats(rBs)
    ratio = np.array(rBs) / np.array(rAs)
    st_ratio = sc.seed_stats(ratio)

    # ---- cubic 3-axis control (deterministic) ------------------------------ #
    CA, CB = sc.config_A(G_SMALL), sc.config_B(G_SMALL)
    r4A_cub = sc.quartic_residual(CA, sc.CUBIC_AXES, A_LINK) / G_SMALL ** 4
    r4B_cub = sc.quartic_residual(CB, sc.CUBIC_AXES, A_LINK) / G_SMALL ** 4

    # ---- commutator coefficient -------------------------------------------- #
    # r4 = -(a^4/(384*15)) (3S-2K)/g^4 with S,K per config; K_A=0, K_B=6g^4:
    # c_K = (r4B - r4A) * g^4 / K_B  (predicted +a^4/2880 = +3.472e-4 at a=1)
    _, _, KB = sc.invariants(sc.config_B(1.0))      # K_B per unit g^4 = 6
    cK = (np.array(rBs) - np.array(rAs)) / KB
    st_cK = sc.seed_stats(cK)

    # ---- predictions -------------------------------------------------------- #
    pred_rA = -(A_LINK ** 4 / (384.0 * 15.0)) * 27.0
    pred_rB = -(A_LINK ** 4 / (384.0 * 15.0)) * 15.0
    pred_cK = A_LINK ** 4 / 2880.0
    pred_cub = -(A_LINK ** 4 / 384.0)               # cubic: mean over 3 axes of G_ii^2 = g^4

    # ---- plateau scan in g (single seed batch, for the figure / SC3) -------- #
    rng = np.random.default_rng(99)
    dirs = sc.isotropic_directions(N_DIR, rng)
    plateau = {"g": GRID_G, "r4A": [], "r4B": []}
    for g in GRID_G:
        plateau["r4A"].append(sc.quartic_residual(sc.config_A(g), dirs, A_LINK) / g ** 4)
        plateau["r4B"].append(sc.quartic_residual(sc.config_B(g), dirs, A_LINK) / g ** 4)

    verdict_skyrme = abs(st_ratio["mean"] - 5.0 / 9.0) < 5 * st_ratio["sem"] + 5e-3
    verdict_blind = abs(r4B_cub / r4A_cub - 1.0) < 1e-12
    death = abs(st_ratio["mean"] - 1.0) < 3 * st_ratio["sem"]

    payload = {
        "params": {"a_link": A_LINK, "g": G_SMALL, "n_dirs": N_DIR,
                   "n_seeds": N_SEEDS},
        "poisson": {
            "r4_A": stA, "r4_B": stB,
            "ratio_B_over_A": st_ratio,
            "predicted_ratio": 5.0 / 9.0,
            "predicted_r4_A": pred_rA, "predicted_r4_B": pred_rB,
        },
        "cubic_control": {
            "r4_A": r4A_cub, "r4_B": r4B_cub,
            "ratio_B_over_A": r4B_cub / r4A_cub,
            "predicted_ratio": 1.0, "predicted_r4": pred_cub,
        },
        "commutator_coefficient": {
            "c_K": st_cK, "predicted": pred_cK,
            "sign": "stabilising (positive)" if st_cK["mean"] > 0 else "NEGATIVE",
        },
        "plateau_scan": plateau,
        "verdict": {
            "skyrme_present_poisson": bool(verdict_skyrme),
            "cubic_K_blind": bool(verdict_blind),
            "death_criterion_activated": bool(death),
        },
    }
    sc.save_json("SC2_constant_field.json", payload)

    # ---- figure -------------------------------------------------------------- #
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    x = np.arange(2)
    width = 0.35
    ax1.bar(x - width / 2, [stA["mean"], r4A_cub], width,
            yerr=[stA["sem"], 0], label="config A (K=0)", color="tab:gray")
    ax1.bar(x + width / 2, [stB["mean"], r4B_cub], width,
            yerr=[stB["sem"], 0], label="config B (K=6g$^4$)", color="tab:blue")
    ax1.axhline(pred_rA, color="tab:gray", ls=":", lw=1)
    ax1.axhline(pred_rB, color="tab:blue", ls=":", lw=1)
    ax1.set_xticks(x, ["Poisson (isotropic)", "cubic 3-axis"])
    ax1.set_ylabel(r"$r_4$ = quartic residual / $g^4$ per link")
    ax1.set_title(f"B/A: Poisson {st_ratio['mean']:.4f} (pred 5/9={5/9:.4f}); "
                  f"cubic {r4B_cub/r4A_cub:.4f} (pred 1)")
    ax1.legend(fontsize=8)

    ax2.plot(plateau["g"], np.abs(plateau["r4A"]), "o-", color="tab:gray",
             label="|r4| config A")
    ax2.plot(plateau["g"], np.abs(plateau["r4B"]), "s-", color="tab:blue",
             label="|r4| config B")
    ax2.axhline(abs(pred_rA), color="tab:gray", ls=":", lw=1)
    ax2.axhline(abs(pred_rB), color="tab:blue", ls=":", lw=1)
    ax2.set_xscale("log")
    ax2.set_xlabel("g (current magnitude)")
    ax2.set_ylabel(r"$|r_4|$")
    ax2.set_title("quartic plateau (g$\\to$0) and g$^6$ departure")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SC2_constant_field.png", dpi=150)

    print(json.dumps({k: payload[k] for k in
                      ("poisson", "cubic_control", "commutator_coefficient",
                       "verdict")}, indent=2))


if __name__ == "__main__":
    main()
