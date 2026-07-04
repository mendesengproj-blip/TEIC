"""FN4_2_velocity.py -- predicted velocity statistic v~(s) for DEV vs MOND vs Newton.

Charter FN4-2.  v~ = v_obs/v_Newton = sqrt(g_eff/g_N).  s in [1, 100] pc.  Shows the
DEV curve diverging from MOND below lambda_A = 17.3 pc (DEV -> Newton, MOND stays
boosted), and where that divergence is maximal.  Also reports a population-averaged
<v~>(s) over an Opik separation law and a 0.5-2 Msun mass range.
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


def population_average(s_pc, masses=(0.5, 1.0, 1.5, 2.0), efe=True):
    """<v~>(s) averaged over total masses (flat-ish IMF proxy)."""
    s = s_pc * c.PC
    dev = np.mean([c.vtilde_dev(s, m, efe) for m in masses], axis=0)
    mond = np.mean([c.vtilde_mond(s, m, efe) for m in masses], axis=0)
    return dev, mond


def main():
    s_pc = np.logspace(0.0, 2.0, 400)  # 1 -> 100 pc
    s = s_pc * c.PC
    M = 1.5  # representative total binary mass

    vN = np.ones_like(s_pc)
    vM = c.vtilde_mond(s, M)
    vD = c.vtilde_dev(s, M)
    vD_pop, vM_pop = population_average(s_pc)

    # divergence DEV vs MOND
    diff = vM - vD
    i_max = int(np.argmax(diff))
    s_maxdiff = float(s_pc[i_max])
    diff_max = float(diff[i_max])

    # fraction of the MOND boost recovered by DEV at key separations
    def recover(rp):
        rr = rp * c.PC
        return float((c.vtilde_dev(rr, M) - 1) / (c.vtilde_mond(rr, M) - 1))

    table = {}
    for rp in [1.0, 1.7, 5.0, 10.0, 17.3, 30.0, 50.0, 100.0]:
        rr = rp * c.PC
        table[f"{rp}pc"] = {
            "vtilde_DEV": float(c.vtilde_dev(rr, M)),
            "vtilde_MOND": float(c.vtilde_mond(rr, M)),
            "divergence": float(c.vtilde_mond(rr, M) - c.vtilde_dev(rr, M)),
            "MOND_boost_recovered_by_DEV": recover(rp),
        }

    payload = {
        "params": {"M_msun": M, "a0": c.A0, "lambda_A_pc": c.LAMBDA_A_PC,
                   "gamma_plateau": float(c.nu_rar(c.G_EXT / c.A0))},
        "max_divergence_DEV_vs_MOND": {"s_pc": s_maxdiff, "delta_vtilde": diff_max},
        "table": table,
        "note": "v~=sqrt(boost); divergence = v~_MOND - v~_DEV; DEV->1 below lambda_A",
    }
    (OUT / "FN4_2_velocity.json").write_text(json.dumps(payload, indent=2))

    print("=" * 74)
    print("FN4-2  velocity statistic  v~(s) = v_obs/v_Newton   (M = 1.5 Msun)")
    print("=" * 74)
    print(f"  {'s [pc]':>8} {'v~_Newton':>10} {'v~_DEV':>8} {'v~_MOND':>8} "
          f"{'MOND-DEV':>9} {'%boost rec.':>11}")
    for rp in [1.0, 1.7, 5.0, 10.0, 17.3, 30.0, 50.0, 100.0]:
        d = table[f"{rp}pc"]
        print(f"  {rp:>8.1f} {1.0:>10.4f} {d['vtilde_DEV']:>8.4f} "
              f"{d['vtilde_MOND']:>8.4f} {d['divergence']:>9.4f} "
              f"{100*d['MOND_boost_recovered_by_DEV']:>10.1f}%")
    print(f"\n  max DEV-vs-MOND divergence: delta_v~ = {diff_max:.4f} at s = {s_maxdiff:.2f} pc")
    print(f"  saved {OUT/'FN4_2_velocity.json'}")

    make_figure(s_pc, vN, vM, vD, vD_pop, vM_pop, s_maxdiff)
    return payload


def make_figure(s_pc, vN, vM, vD, vD_pop, vM_pop, s_maxdiff):
    fig, ax = plt.subplots(1, 2, figsize=(12.5, 5.0))

    for a in ax:
        a.axvline(c.LAMBDA_A_PC, color="k", ls="-.", lw=1.2,
                  label=f"$\\lambda_A={c.LAMBDA_A_PC}$ pc")
        a.axvline(c.R_JACOBI_PC, color="brown", ls=":", lw=1.4,
                  label=f"Jacobi $r_J={c.R_JACOBI_PC}$ pc (binaries unbind)")

    ax[0].semilogx(s_pc, vN, color="C0", lw=2, label="Newton  $\\tilde v=1$")
    ax[0].semilogx(s_pc, vM, color="C3", lw=2, ls="--", label="MOND (EFE)")
    ax[0].semilogx(s_pc, vD, color="C2", lw=2.6, label="DEV (screened)")
    ax[0].fill_between(s_pc, vD, vM, color="C2", alpha=0.12,
                       label="exclusive DEV$-$MOND gap")
    ax[0].axvspan(c.R_JACOBI_PC, 100, color="green", alpha=0.05)
    ax[0].set_xlabel("projected separation s [pc]")
    ax[0].set_ylabel("$\\tilde v = v_{obs}/v_{Newton}$")
    ax[0].set_title("FN4-2: DEV $\\to$ Newton below $\\lambda_A$, MOND stays boosted")
    ax[0].legend(fontsize=7, loc="center left")

    # right: population-averaged + divergence
    ax[1].semilogx(s_pc, vM_pop, color="C3", lw=2, ls="--",
                   label="$\\langle\\tilde v\\rangle$ MOND (0.5-2 M$_\\odot$)")
    ax[1].semilogx(s_pc, vD_pop, color="C2", lw=2.6,
                   label="$\\langle\\tilde v\\rangle$ DEV")
    ax[1].semilogx(s_pc, vM - vD, color="navy", lw=1.6,
                   label="divergence $\\tilde v_{MOND}-\\tilde v_{DEV}$")
    ax[1].axvline(s_maxdiff, color="navy", ls=":", lw=1,
                  label=f"max divergence @ {s_maxdiff:.1f} pc")
    ax[1].set_xlabel("projected separation s [pc]")
    ax[1].set_ylabel("$\\langle\\tilde v\\rangle$  /  divergence")
    ax[1].set_title("FN4-2: where DEV and standard MOND differ most")
    ax[1].legend(fontsize=7, loc="center left")

    fig.suptitle("FN4-2  Exclusive signature: below $\\lambda_A=17.3$ pc the DEV "
                 "velocity boost is screened to Newton while MOND is not", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "FN4_2_velocity.png", dpi=130)
    print(f"  saved {OUT/'FN4_2_velocity.png'}")


if __name__ == "__main__":
    main()
