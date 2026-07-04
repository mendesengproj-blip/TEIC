"""FN4_4_forecast.py -- forecast for testing the lambda_A = 17.3 pc transition.

Charter FN4-4.  (1) N of tracers needed for a 3-sigma detection of the screening
transition; (2) the structural obstacle: bound binaries are tidally disrupted at
the Jacobi radius r_J ~ 1.7 pc, far inside lambda_A = 17.3 pc, so the transition
regime s ~ 10-100 pc cannot be probed with BOUND binaries at all; (3) v~(s) for
DEV vs MOND over [1,100] pc marking where the divergence is observable.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import fn4_core as c  # noqa: E402

OUT = Path(__file__).resolve().parent

# Chae sensitivity anchor: sigma_gamma = K / sqrt(N), with K calibrated so that
# N=26615 binaries give sigma_gamma=0.06 (his reported error).
K_GAMMA = c.CHAE_GAMMA_ERR * np.sqrt(26615)


def n_for_3sigma(delta_gamma, n_bins=2):
    """N (per bin) of tracers to detect a contrast delta_gamma at 3 sigma, given
    sigma_gamma = K/sqrt(N) per bin and a 2-bin (above/below lambda_A) comparison:
    sigma_contrast = K*sqrt(2/N)  ->  N = 2*(3K/delta_gamma)^2."""
    return 2.0 * (3.0 * K_GAMMA / delta_gamma) ** 2


def main():
    # the transition contrast DEV predicts: gamma drops from the plateau (above
    # lambda_A) to ~1 (below).  Use boost gamma = (v~)^2.
    M = 1.5
    gamma_above = float(c.boost_dev(50 * c.PC, M))   # ~plateau ~1.35
    gamma_below = float(c.boost_dev(5 * c.PC, M))     # screened, near 1.04
    delta_gamma_transition = gamma_above - gamma_below

    # alternative: the sub-pc discriminator (DEV~Newton vs MOND~1.36) where Chae works
    delta_gamma_subpc = float(c.boost_mond(0.05 * c.PC, M) - c.boost_dev(0.05 * c.PC, M))

    N_transition = n_for_3sigma(delta_gamma_transition)
    N_subpc = n_for_3sigma(delta_gamma_subpc)

    # structural obstacle
    r_J = c.R_JACOBI_PC
    obstacle = {
        "jacobi_radius_pc": r_J,
        "lambda_A_pc": c.LAMBDA_A_PC,
        "ratio_lambda_over_rJ": c.LAMBDA_A_PC / r_J,
        "verdict": ("bound binaries disrupted beyond r_J~1.7 pc (Jiang & Tremaine "
                    "2010); the 5-50 pc transition regime is 3-30x wider than r_J -> "
                    "NOT accessible to bound binaries; needs comoving/dissolving pairs"),
    }

    payload = {
        "sensitivity_anchor": {"K_gamma": float(K_GAMMA),
                               "from": "Chae sigma_gamma=0.06 at N=26615"},
        "transition_test": {
            "gamma_above_lambda": gamma_above, "gamma_below_lambda": gamma_below,
            "delta_gamma": delta_gamma_transition,
            "N_pairs_for_3sigma": float(N_transition)},
        "subpc_discriminator": {
            "delta_gamma": delta_gamma_subpc,
            "N_binaries_for_3sigma": float(N_subpc),
            "note": "DEV(Newton) vs MOND(1.36) at sub-pc; data ALREADY exist (Chae)"},
        "structural_obstacle": obstacle,
        "surveys": {
            "Gaia_DR4_2026": "deeper bound-binary census but still <~1-2 pc (tidal cap)",
            "comoving_pairs_DR3_DR4": "6D phase-space pairs to 10-100 pc exist but mix "
                                      "bound + dissolving -> 3D velocity not orbital",
            "4MOST_WEAVE": "high-res RV to sharpen plane-of-sky velocities sub-pc",
            "Roman_2027": "fainter/farther binaries, sub-pc statistics"},
    }
    (OUT / "FN4_4_forecast.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("FN4-4  forecast: testing the lambda_A = 17.3 pc transition")
    print("=" * 74)
    print(f"  sensitivity K_gamma = {K_GAMMA:.2f}  (sigma_gamma = K/sqrt(N))\n")
    print(f"  Jacobi radius r_J = {r_J} pc << lambda_A = {c.LAMBDA_A_PC} pc")
    print(f"  -> transition regime (5-50 pc) is {c.LAMBDA_A_PC/r_J:.0f}x wider than r_J")
    print(f"  -> BOUND binaries cannot reach it (tidally disrupted)\n")
    print(f"  Transition test (gamma {gamma_below:.3f}->{gamma_above:.3f}, "
          f"d_gamma={delta_gamma_transition:.3f}):")
    print(f"    N ~ {N_transition:.0f} comoving pairs spanning 5-50 pc for 3 sigma")
    print(f"    BUT such pairs are unbound/dissolving -> velocities not orbital\n")
    print(f"  Sub-pc discriminator (DEV~Newton vs MOND~1.36, d_gamma="
          f"{delta_gamma_subpc:.3f}):")
    print(f"    N ~ {N_subpc:.0f} bound binaries for 3 sigma -- ALREADY in hand (Chae 26615)")
    print(f"  saved {OUT/'FN4_4_forecast.json'}")

    make_figure(M)
    return payload


def make_figure(M):
    s_pc = np.logspace(0.0, 2.0, 400)
    s = s_pc * c.PC
    vM = c.vtilde_mond(s, M)
    vD = c.vtilde_dev(s, M)

    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    ax[0].semilogx(s_pc, vM, color="C3", lw=2, ls="--", label="MOND")
    ax[0].semilogx(s_pc, vD, color="C2", lw=2.6, label="DEV (screened)")
    ax[0].axhline(1.0, color="C0", lw=1.3, label="Newton")
    ax[0].axvspan(0.0, c.R_JACOBI_PC, color="green", alpha=0.10,
                  label=f"bound binaries (s<$r_J$={c.R_JACOBI_PC} pc)")
    ax[0].axvspan(c.R_JACOBI_PC, 100, color="red", alpha=0.06,
                  label="unbound / dissolving pairs only")
    ax[0].axvline(c.LAMBDA_A_PC, color="k", ls="-.", lw=1.2,
                  label=f"$\\lambda_A$={c.LAMBDA_A_PC} pc")
    ax[0].set_xlabel("separation s [pc]"); ax[0].set_ylabel("$\\tilde v$")
    ax[0].set_title("FN4-4: the 17 pc transition sits in the unbound-pair regime")
    ax[0].legend(fontsize=7, loc="center right")

    # N vs delta_gamma curve
    dg = np.linspace(0.02, 0.5, 200)
    N = n_for_3sigma(dg)
    ax[1].loglog(dg, N, color="navy", lw=2.2)
    # mark the two tests
    M_ = 1.5
    dgt = float(c.boost_dev(50*c.PC, M_) - c.boost_dev(5*c.PC, M_))
    dgs = float(c.boost_mond(0.05*c.PC, M_) - c.boost_dev(0.05*c.PC, M_))
    ax[1].scatter([dgt], [n_for_3sigma(dgt)], color="C3", zorder=5,
                  label=f"17 pc transition ($\\Delta\\gamma$={dgt:.2f})\nN$\\approx${n_for_3sigma(dgt):.0f} (unbound pairs)")
    ax[1].scatter([dgs], [n_for_3sigma(dgs)], color="C2", zorder=5,
                  label=f"sub-pc discriminator ($\\Delta\\gamma$={dgs:.2f})\nN$\\approx${n_for_3sigma(dgs):.0f} (have it)")
    ax[1].axhline(26615, color="grey", ls=":", lw=1, label="Chae N=26615")
    ax[1].set_xlabel("contrast $\\Delta\\gamma$ to detect")
    ax[1].set_ylabel("N tracers for 3$\\sigma$")
    ax[1].set_title("FN4-4: N for 3$\\sigma$ (anchored to Chae sensitivity)")
    ax[1].legend(fontsize=7, loc="upper right")

    fig.suptitle("FN4-4  The clean $\\lambda_A=17.3$ pc transition is inaccessible to "
                 "bound binaries (tidal $r_J\\approx1.7$ pc); the sharp test is the "
                 "sub-pc discriminator", fontsize=10.5)
    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(OUT / "FN4_4_forecast.png", dpi=130)
    print(f"  saved {OUT/'FN4_4_forecast.png'}")


if __name__ == "__main__":
    main()
