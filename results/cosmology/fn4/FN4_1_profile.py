"""FN4_1_profile.py -- analytic screened-MOND profile g_DEV(r).

Charter FN4-1.  M = 1 Msun, a0 = 1.2e-10 m/s^2, lambda_A = 17.3 pc (fixed).
Computes g_N, g_MOND, g_DEV and the boost g/g_N over r in [0.1, 1000] pc, locates
the transition at r = lambda_A, and writes json + a two-panel figure.
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
M = 1.0  # Msun


def main():
    r_pc = np.logspace(np.log10(0.1), np.log10(1000.0), 400)
    r = r_pc * c.PC

    gN = c.g_newton(r, M)
    gM = c.g_mond(r, M)
    gD = c.g_dev(r, M)
    S = c.screening(r)
    bD = c.boost_dev(r, M)
    bM = c.boost_mond(r, M)

    # checkpoint table (charter asks for S at 0.05 pc and 17 pc explicitly)
    checkpoints = {}
    for tag, rp in [("0.05pc_Chae", 0.05), ("1.7pc_Jacobi", c.R_JACOBI_PC),
                    ("17.3pc_lambdaA", c.LAMBDA_A_PC), ("100pc", 100.0),
                    ("1000pc", 1000.0)]:
        rr = rp * c.PC
        checkpoints[tag] = {
            "r_pc": rp,
            "screening_S": float(c.screening(rr)),
            "boost_DEV": float(c.boost_dev(rr, M)),
            "boost_MOND": float(c.boost_mond(rr, M)),
            "vtilde_DEV": float(c.vtilde_dev(rr, M)),
            "vtilde_MOND": float(c.vtilde_mond(rr, M)),
        }

    payload = {
        "params": {"M_msun": M, "a0": c.A0, "lambda_A_pc": c.LAMBDA_A_PC,
                   "g_ext_over_a0": c.G_EXT / c.A0,
                   "gamma_plateau": float(c.nu_rar(c.G_EXT / c.A0)),
                   "r_MOND_pc": float(c.mond_radius(M) / c.PC)},
        "checkpoints": checkpoints,
        "transition_pc": c.LAMBDA_A_PC,
        "S_at_lambda": float(c.screening(c.LAMBDA_A)),
        "note": "g_DEV = g_N*[1+(nu_eff-1)*(1-exp(-r/lambda_A))]; EFE-capped nu_eff",
    }
    (OUT / "FN4_1_profile.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("FN4-1  screened-MOND profile  g_DEV(r)   (M = 1 Msun)")
    print("=" * 74)
    print(f"  lambda_A = {c.LAMBDA_A_PC} pc   r_MOND = {c.mond_radius(M)/c.PC:.4f} pc"
          f"   gamma_plateau = {c.nu_rar(c.G_EXT/c.A0):.3f}")
    print(f"  {'r [pc]':>10} {'S(r)':>8} {'g_DEV/g_N':>10} {'g_MOND/g_N':>11}")
    for tag, d in checkpoints.items():
        print(f"  {d['r_pc']:>10.3f} {d['screening_S']:>8.4f} "
              f"{d['boost_DEV']:>10.4f} {d['boost_MOND']:>11.4f}   {tag}")
    print(f"\n  S(lambda_A) = {payload['S_at_lambda']:.4f}  (= 1 - 1/e, the transition)")
    print(f"  saved {OUT/'FN4_1_profile.json'}")

    make_figure(r_pc, gN, gM, gD, S, bD, bM)
    return payload


def make_figure(r_pc, gN, gM, gD, S, bD, bM):
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    # left: accelerations
    ax[0].loglog(r_pc, gN, color="C0", lw=2, label="Newton  $g_N=GM/r^2$")
    ax[0].loglog(r_pc, gM, color="C3", lw=2, ls="--", label="MOND (EFE)  $g_N\\,\\nu$")
    ax[0].loglog(r_pc, gD, color="C2", lw=2.5, label="DEV (screened)  $g_{DEV}$")
    ax[0].axhline(c.A0, color="grey", ls=":", lw=1, label="$a_0$")
    ax[0].axvline(c.LAMBDA_A_PC, color="k", ls="-.", lw=1.2,
                  label=f"$\\lambda_A={c.LAMBDA_A_PC}$ pc")
    ax[0].axvline(c.mond_radius(1.0)/c.PC, color="purple", ls=":", lw=1,
                  label=f"$r_{{MOND}}={c.mond_radius(1.0)/c.PC:.3f}$ pc")
    ax[0].axvspan(c.CHAE_S_MIN_AU*c.AU/c.PC, c.CHAE_S_MAX_AU*c.AU/c.PC,
                  color="orange", alpha=0.15, label="Chae+2023 binaries")
    ax[0].set_xlabel("separation r [pc]"); ax[0].set_ylabel("acceleration [m/s$^2$]")
    ax[0].set_title("FN4-1: $g_{DEV}$ tracks Newton below $\\lambda_A$, MOND above")
    ax[0].legend(fontsize=7, loc="lower left")

    # right: boost factor g/g_N
    ax[1].semilogx(r_pc, bM, color="C3", lw=2, ls="--", label="MOND boost  $g/g_N$")
    ax[1].semilogx(r_pc, bD, color="C2", lw=2.5, label="DEV boost (screened)")
    ax[1].semilogx(r_pc, S, color="grey", lw=1.2, ls=":",
                   label="screening $S(r)=1-e^{-r/\\lambda_A}$")
    ax[1].axhline(1.0, color="C0", lw=1.2, label="Newton (no boost)")
    ax[1].axvline(c.LAMBDA_A_PC, color="k", ls="-.", lw=1.2,
                  label=f"$\\lambda_A={c.LAMBDA_A_PC}$ pc")
    ax[1].axvspan(c.CHAE_S_MIN_AU*c.AU/c.PC, c.CHAE_S_MAX_AU*c.AU/c.PC,
                  color="orange", alpha=0.15, label="Chae+2023 (deeply screened)")
    ax[1].set_xlabel("separation r [pc]"); ax[1].set_ylabel("$g/g_N$  (boost)")
    ax[1].set_ylim(0.0, 1.45)
    ax[1].set_title("FN4-1: MOND boost screened away for $r<\\lambda_A=17.3$ pc")
    ax[1].legend(fontsize=7, loc="center left")

    fig.suptitle("FN4-1  DEV screened MOND: exclusive prediction = Newtonian gravity "
                 "below the m_A correlation length $\\lambda_A=17.3$ pc", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FN4_1_profile.png", dpi=130)
    print(f"  saved {OUT/'FN4_1_profile.png'}")


if __name__ == "__main__":
    main()
