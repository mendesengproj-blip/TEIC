"""HQ2_1_jeff.py -- c_eff(J) near J_c by TWO anti-circular routes.

Charter: HQ2_CRITICAL_FERROMAGNET.md (HQ2-1).  Runs only after HQ2-V passed.
Question: does the effective wave speed c_eff(J) DECREASE as J -> J_c (softening,
J_eff < J) -- the premise of G_eff < G_N?

ROUTE A (literal, BD / E2 motor).  c_BD from the BD symbol dispersion omega = c k
on a Poisson causal set.  The operator is built from the causal ORDER MATRIX only;
J is NOT an input, so c_BD is J-independent BY CONSTRUCTION.  This is the prompt's
literal death channel: "c_eff constant in J -> Verdict C".

ROUTE B (generous, E1 stiffness motor).  Give the hypothesis its best shot: the
mean-field spin stiffness rho_s(J) ~ m(J)^2 of the causal O(3) ferromagnet (E1-3
found flat/non-local S(k), so the softening stiffness is the squared ordered
moment).  c_eff^2(J)/c0^2 = (m(J)/m_sat)^2.  m(J) measured fresh, 20 seeds, at the
charter J set {1.02,1.05,1.1,1.2,1.5} J_c plus deep-ordered anchors.

Pre-registered: Route A -> c_eff constant; Route B -> c_eff decreases toward J_c.
Death criterion (Route A): c_eff(J->J_c+) = c0, no softening.
Anti-circularity: G_N/c never inserted as constants; m(J) is a measured ratio.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import hq2_core as hc  # noqa: E402

OUT = Path(__file__).resolve().parent
JC = hc.JC["O(3)"]
# charter J set (just above J_c, softening regime) + deep-ordered anchors for c0
J_OVER_JC_SOFT = [1.02, 1.05, 1.1, 1.2, 1.5]
J_OVER_JC_REF = [2.0, 5.0]
J_OVER_JC = J_OVER_JC_SOFT + J_OVER_JC_REF
JS = [round(r * JC, 5) for r in J_OVER_JC]
N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 20
N_BURN = 1500
N_MEAS = 150


def gate_passed():
    p = OUT / "HQ2V_gate.json"
    if not p.exists():
        return False
    return bool(json.loads(p.read_text()).get("passed"))


def main():
    if not gate_passed():
        print("HQ2-V gate has NOT passed -- HQ2-1 must not run.  Aborting.")
        return 1
    t0 = time.time()
    print("=" * 72)
    print(f"HQ2-1 -- c_eff(J) near J_c={JC}  (seeds={N_SEEDS})")
    print(f"  J/J_c={J_OVER_JC}  J={JS}")
    print("=" * 72)

    # ---- ROUTE A: BD photon speed (E2 motor), J-blind by construction ----
    print("\nROUTE A (BD / E2 motor) -- the operator has NO J input:")
    cA, devA, winA, nkA = hc.bd_photon_speed(n_seeds=8)
    print(f"  c_BD = {cA:.4f}  (fit winner={winA}, dev={devA:.1f}%, {nkA} k found)")
    print(f"  -> J appears nowhere in B_eps; c_BD(J)=c_BD for ALL J (constant).")

    # ---- ROUTE B: m(J) -> stiffness softening ----
    print("\nROUTE B (E1 stiffness) -- m(J), 20 seeds:")
    mvals = {J: [] for J in JS}
    chivals = {J: [] for J in JS}
    ns = []
    for seed in range(N_SEEDS):
        g, sources, dist_list = hc.build_seed(seed)
        ns.append(g.n)
        for J in JS:
            _, _, _, mm, msd, chi = hc.run_o3(g, sources, dist_list, J, seed,
                                              n_burn=N_BURN, n_meas=N_MEAS)
            mvals[J].append(mm)
            chivals[J].append(chi)
        print(f"  seed {seed:2d}: n={g.n}  ({time.time()-t0:.0f}s)")

    m_sat = hc.M_SAT
    c0 = hc.C0_PHOTON
    rows = []
    for r_jc, J in zip(J_OVER_JC, JS):
        m_arr = np.array(mvals[J])
        m_mean = float(m_arr.mean())
        m_err = float(m_arr.std() / np.sqrt(N_SEEDS))
        # Route B: c_eff = c0 * m/m_sat  (so (c_eff/c0)^2 = (m/m_sat)^2 = Z_B)
        ceff = c0 * m_mean / m_sat
        ceff_err = c0 * m_err / m_sat
        rows.append({"J": J, "J_over_Jc": r_jc, "m": m_mean, "m_err": m_err,
                     "chi": float(np.mean(chivals[J])),
                     "c_eff_B": ceff, "c_eff_B_err": ceff_err,
                     "c_eff_A": cA})
        print(f"  J/Jc={r_jc:4.2f} J={J:7.4f}  m={m_mean:.4f}+-{m_err:.4f}  "
              f"c_eff_B={ceff:.4f}  (c_eff_A={cA:.4f} const)")

    # ---- does c_eff decrease toward J_c? (within the softening set) ----
    soft = [r for r in rows if r["J_over_Jc"] in J_OVER_JC_SOFT]
    soft = sorted(soft, key=lambda d: d["J_over_Jc"])
    cB_soft = [r["c_eff_B"] for r in soft]
    # monotone increasing with J/Jc means: smaller toward J_c (softening)
    routeB_softens = cB_soft[0] < cB_soft[-1]
    cB_min = min(cB_soft)
    cB_at_Jc = cB_soft[0]          # J/Jc=1.02, closest to J_c
    # Route A: constant (no J dependence by construction)
    routeA_constant = True

    print("-" * 72)
    print(f"  ROUTE A: c_eff constant in J -> {routeA_constant} "
          f"(c_BD={cA:.4f}, J-blind operator)")
    print(f"  ROUTE B: c_eff decreases toward J_c -> {routeB_softens} "
          f"(c_eff(1.02 J_c)={cB_at_Jc:.4f} < c_eff(1.5 J_c)={cB_soft[-1]:.4f})")
    print(f"  c_eff(J_c)/c0  Route B = {cB_at_Jc/c0:.4f} ; Route A = {cA/c0:.4f}")
    print("=" * 72)

    # ---- figure ----
    fig, ax = plt.subplots(figsize=(8, 5.5))
    rj = np.array([r["J_over_Jc"] for r in rows])
    cB = np.array([r["c_eff_B"] for r in rows])
    cBe = np.array([r["c_eff_B_err"] for r in rows])
    order = np.argsort(rj)
    ax.errorbar(rj[order], cB[order], yerr=cBe[order], fmt="o-", color="tab:red",
                capsize=3, label="Route B: $c_{eff}\\propto m(J)$ (stiffness)")
    ax.axhline(cA, color="tab:blue", ls="-", lw=1.5,
               label=f"Route A: $c_{{BD}}$={cA:.3f} (J-blind, E2)")
    ax.axhline(c0, color="0.5", ls="--", lw=1, label=f"$c_0$={c0} (photon, E2)")
    ax.axvline(1.0, color="k", ls=":", lw=1, label="$J_c$")
    ax.set_xlabel("J / J_c"); ax.set_ylabel("effective wave speed $c_{eff}$")
    ax.set_title("HQ2-1: c_eff(J) near J_c -- Route A constant, Route B softens")
    ax.legend(fontsize=9); ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(OUT / "HQ2_1_jeff.png", dpi=130)
    print(f"saved {OUT/'HQ2_1_jeff.png'}")

    payload = {
        "task": "HQ2-1", "Jc_O3": JC, "n_seeds": N_SEEDS,
        "mean_n": float(np.mean(ns)), "c0": c0, "m_sat": m_sat,
        "J_over_Jc": J_OVER_JC, "J_over_Jc_soft": J_OVER_JC_SOFT, "Js": JS,
        "route_A": {"c_BD": cA, "dev_pct": devA, "winner": winA, "n_k_found": nkA,
                    "J_blind": True, "constant_in_J": True},
        "route_B": {"rows": rows, "c_eff_Jc": cB_at_Jc, "c_eff_min": cB_min,
                    "softens_toward_Jc": bool(routeB_softens)},
        "rows": rows,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "HQ2_1_jeff.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'HQ2_1_jeff.json'}  ({payload['runtime_s']:.0f}s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
