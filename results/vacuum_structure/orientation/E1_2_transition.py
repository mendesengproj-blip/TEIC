"""E1_2_transition.py -- locate and characterise the causal-vacuum ordering
transition, reusing the 20-seed E1-1 measurement (no new Monte-Carlo).

Charter: E1_ORIENTATION.md (E1-2).  Runs because E1-1 found an ordered phase.
E1-1 already swept J finely across the transition and recorded, per (model, J),
the order parameter m = |<n>| (or |<e^{i phi}>|), the susceptibility
chi = N(<m^2>-<m>^2), and the long-range correlation C(infinity) = C_long.
This script distils those into the transition observables and figure:

  * order parameter m(J): zero (~1/sqrt(N)) below J_c, lifting above;
  * susceptibility chi(J): peak locates J_c;
  * C_long(J) vs m(J)^2: the Mermin clustering test of genuine LRO;
  * J_c from the chi peak and from the exp->const crossover of C(r).

Reads E1_1_correlations.json; writes E1_2_transition.json + .png.  No physics
interpretation token in the generator; this is pure re-analysis of E1-1 data.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent
MODELS = ("U(1)", "O(3)")


def main():
    src = json.loads((OUT / "E1_1_correlations.json").read_text())
    R = src["results"]
    N = src["graph_stats"]["mean_n"]
    baseline = 1.0 / np.sqrt(N)
    Js = sorted(float(j) for j in R["U(1)"].keys())

    out = {"baseline_1_over_sqrtN": baseline, "mean_n": N, "models": {}}
    print("=" * 72)
    print(f"E1-2 -- causal-vacuum ordering transition  (1/sqrt(N) baseline={baseline:.3f})")
    print("=" * 72)
    for model in MODELS:
        m = np.array([R[model][str(J)]["m"] for J in Js])
        chi = np.array([R[model][str(J)]["chi"] for J in Js])
        Clong = np.array([R[model][str(J)]["C_long"] for J in Js])
        winners = [R[model][str(J)]["fit"]["winner"] for J in Js]

        jc_chi = Js[int(np.argmax(chi))]
        # ordering onset: first J where m exceeds 5x the disordered baseline
        onset = next((J for J, mm in zip(Js, m) if mm > 5 * baseline), None)
        exp_Js = [J for J, w in zip(Js, winners) if w == "exp"]
        const_Js = [J for J, w in zip(Js, winners) if w == "const"]
        jc_cross = (0.5 * (max(exp_Js) + min(J for J in const_Js if J > max(exp_Js)))
                    if exp_Js and const_Js
                    and any(J > max(exp_Js) for J in const_Js) else None)
        # genuine-LRO check: |C_long - m^2|/m^2 in the ordered phase
        lro = [(J, Clong[i], m[i] ** 2,
                abs(Clong[i] - m[i] ** 2) / m[i] ** 2 if m[i] > 0 else np.nan)
               for i, J in enumerate(Js) if winners[i] == "const"]

        out["models"][model] = {
            "J": Js, "m": m.tolist(), "chi": chi.tolist(), "C_long": Clong.tolist(),
            "winners": winners, "Jc_chi_peak": jc_chi, "Jc_crossover": jc_cross,
            "ordering_onset_J": onset, "chi_max": float(chi.max()),
            "lro_C_long_vs_m2": [{"J": J, "C_long": cl, "m2": m2, "rel": rel}
                                 for J, cl, m2, rel in lro]}
        print(f"\n  {model}:  J_c(chi-peak)={jc_chi}  J_c(crossover)~{jc_cross}  "
              f"onset(m>5/sqrtN)={onset}  chi_max={chi.max():.2f}")
        print("    J      m       chi      C_long   m^2     C(r)")
        for i, J in enumerate(Js):
            print(f"   {J:5.2f}  {m[i]:.3f}  {chi[i]:7.3f}  {Clong[i]:.3f}  "
                  f"{m[i]**2:.3f}  {winners[i]}")

    # ---- figure ----
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))
    for model, col in zip(MODELS, ("tab:blue", "tab:red")):
        d = out["models"][model]
        J = np.array(d["J"])
        ax = axes[0]
        ax.plot(J, d["m"], "o-", color=col, label=f"m {model}")
        ax.plot(J, np.sqrt(np.clip(d["C_long"], 0, None)), "x--", color=col,
                alpha=0.6, label=f"sqrt(C_long) {model}")
        ax.axvline(d["Jc_chi_peak"], color=col, ls=":", lw=1)
    axes[0].axhline(baseline, color="0.6", lw=0.8, ls="--",
                    label=r"$1/\sqrt{N}$ baseline")
    axes[0].set_xscale("log"); axes[0].set_xlabel("J (= 1/T)")
    axes[0].set_ylabel("order parameter")
    axes[0].set_title("m(J): disordered (~1/sqrt N) -> ordered; sqrt(C_long)=m")
    axes[0].legend(fontsize=8)
    axes[0].grid(alpha=0.2)
    for model, col in zip(MODELS, ("tab:blue", "tab:red")):
        d = out["models"][model]
        axes[1].plot(d["J"], d["chi"], "s-", color=col, label=f"chi {model}")
        axes[1].axvline(d["Jc_chi_peak"], color=col, ls=":", lw=1,
                        label=f"J_c({model})={d['Jc_chi_peak']}")
    axes[1].set_xscale("log"); axes[1].set_xlabel("J (= 1/T)")
    axes[1].set_ylabel("susceptibility chi")
    axes[1].set_title("chi(J) peaks at J_c")
    axes[1].legend(fontsize=8)
    axes[1].grid(alpha=0.2)
    fig.suptitle("E1-2: causal-vacuum ordering transition (re-analysis of 20-seed "
                 "E1-1 data)", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E1_2_transition.png", dpi=130)
    print(f"\nsaved {OUT/'E1_2_transition.png'}")

    out["source"] = "E1_1_correlations.json (20 seeds)"
    (OUT / "E1_2_transition.json").write_text(json.dumps(out, indent=2, default=float))
    print(f"saved {OUT/'E1_2_transition.json'}")


if __name__ == "__main__":
    main()
