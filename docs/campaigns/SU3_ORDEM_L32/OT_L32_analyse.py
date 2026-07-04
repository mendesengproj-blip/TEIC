#!/usr/bin/env python3
"""Post-analysis for SU3_ORDEM_L32: combine the PT L=32 production run with the
PT L=16 gate and the OT (L<=24) reference to map the verdict onto A/B/C/D.

Decisive observables (charter PRE_REGISTRO sec 5):
  L32-1  bimodality / dip depth of P(b) at the pseudo-critical slot  (decisive)
  L32-2  latent heat magnitude (peak separation) if bimodal          (strong vs weak)
  L32-3  chi_max exponent -- here a protocol-internal 2-point PT slope (16->32)
  L32-4  U4 dip trend vs OT (comparable: PT U4(16)=0.563 ~ OT 0.565)
PT health (charter sec 6.1): min swap rate, round-trips.
"""
import os, sys, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OT = os.path.abspath(os.path.join(HERE, "..", "SU3_ORDEM_TRANSICAO", "OT_transition_order.json"))

# OT reference (canonical Metropolis, L<=24)
OT_U4 = {8: 0.618, 12: 0.580, 16: 0.565, 20: 0.522, 24: 0.485}
OT_CHI = {8: 2.4514744242351085, 12: 9.595521512136344, 16: 29.203691147703523,
          20: 69.82034484876864, 24: 125.6081542663167}
OT_X = 3.633801645877652


def load(path):
    with open(path) as f:
        return json.load(f)


def best_run_summary(payload):
    """Return the per-run analysis dict averaged across seeds, plus the raw runs."""
    return payload["summary"], payload["runs"]


def main():
    prod = load(os.path.join(HERE, "prod_l32.json"))
    gate = load(os.path.join(HERE, "gate_l16.json"))
    s32, runs32 = best_run_summary(prod)
    s16, runs16 = best_run_summary(gate)

    chi16 = s16["chi_max_mean"]; chi32 = s32["chi_max_mean"]
    u4_16 = s16["U4_at_chi_max_mean"]; u4_32 = s32["U4_at_chi_max_mean"]
    Jc32 = s32["Jc_mean"]
    dip32 = s32["dip_depth_mean"]
    min_swap = s32["min_swap_rate_min"]; rt = s32["up_crossings_min"]

    x_pt = np.log(chi32 / chi16) / np.log(32.0 / 16.0)

    print("="*70)
    print("SU3_ORDEM_L32  --  verdict analysis")
    print("="*70)
    print(f"PT chi_max:   L=16 {chi16:.2f}   L=32 {chi32:.2f}   "
          f"2-point PT exponent x(16->32) = {x_pt:.2f}")
    print(f"   (OT 5-point exponent over L=8..24 = {OT_X:.2f}; volume law x=3; 2nd-order x=gamma/nu<2)")
    print(f"PT U4 at peak: L=16 {u4_16:.3f} (OT 0.565)   L=32 {u4_32:.3f} "
          f"(OT L=24 was {OT_U4[24]:.3f})")
    print(f"   U4 trend: {'DEEPENS below OT-L24 (1st-order trend)' if u4_32 < OT_U4[24] else 'SATURATES/rises (toward 2nd order)'}")
    print(f"PT dip depth @ J_c={Jc32:.3f}:  {dip32:.3f}   "
          f"({'BIMODAL' if dip32 > 0.15 else 'flat/unimodal'})")
    print(f"PT health:  min swap rate = {min_swap:.2f}   round-trips = {rt}")
    print("-"*70)

    # ---- verdict mapping (charter sec 5/6/7) -------------------------------
    pt_dead = (min_swap < 0.10) or (rt < 1)
    if pt_dead:
        verdict = ("D (FRONTEIRA TECNICA): PT health insufficient at L=32 "
                   f"(min_swap={min_swap:.2f}, round-trips={rt}). The barrier, if "
                   "present, is not crossed with desktop statistics. Requires "
                   "L>=48 with multicanonical/Wang-Landau on a cluster.")
    elif dip32 > 0.15:
        # bimodal -> 1st order; latent heat magnitude separates strong/weak
        kind = "FORTE" if dip32 > 0.50 else "FRACA"   # proxy; refine with peak gap
        verdict = (f"{'A' if kind=='FORTE' else 'B'} (1st ORDER {kind}): P(b) at J_c is "
                   f"bimodal (dip={dip32:.2f}). Latent heat {'resolved' if kind=='FORTE' else 'small'}.")
    else:
        # no resolvable barrier: continuous OR weak-below-resolution
        if u4_32 < OT_U4[24] and x_pt > 2.3:
            verdict = ("D/B border (UNRESOLVED, leans weak-1st): no double peak at "
                       f"L=32 (dip={dip32:.2f}) but U4 keeps deepening and chi exponent "
                       f"x={x_pt:.2f}>2. Barrier below desktop resolution -> frontier; "
                       "weak-1st remains the more likely reading, continuous not excluded.")
        else:
            verdict = ("C (CONTINUOUS / 2nd order with finite-size): no double peak, "
                       f"U4 {'saturating' if u4_32>=OT_U4[24] else 'deepening'}, "
                       f"chi exponent x={x_pt:.2f}. Reverts OT's weak-1st reading.")
    print("VERDICT:", verdict)
    print("="*70)

    out = {
        "chi16": chi16, "chi32": chi32, "x_pt_2pt": float(x_pt), "OT_x_5pt": OT_X,
        "u4_16": u4_16, "u4_32": u4_32, "OT_U4_L24": OT_U4[24],
        "Jc32": Jc32, "dip32": dip32, "min_swap": min_swap, "round_trips": rt,
        "pt_dead": bool(pt_dead), "verdict": verdict,
    }
    with open(os.path.join(HERE, "L32_verdict.json"), "w") as f:
        json.dump(out, f, indent=2)

    # ---- figure: P(b) at pseudo-critical slot + neighbours ----------------
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        run = runs32[0]
        if "b_samples" in run:
            ladder = np.array(run["ladder"])
            chi = np.array(run["chi"]); kstar = int(np.argmax(chi))
            fig, ax = plt.subplots(1, 2, figsize=(11, 4))
            for k in [kstar-1, kstar, kstar+1]:
                if 0 <= k < len(ladder):
                    b = np.array(run["b_samples"][k])
                    if b.size:
                        ax[0].hist(b, bins=30, density=True, histtype="step",
                                   label=f"J={ladder[k]:.3f}"+(" (Jc)" if k==kstar else ""))
            ax[0].set_xlabel("overlap density  b = U / n_edges")
            ax[0].set_ylabel("P(b)"); ax[0].set_title(f"L=32 energy histogram (dip={dip32:.2f})")
            ax[0].legend(fontsize=8)
            ax[1].plot(ladder, chi, "o-")
            ax[1].axvline(ladder[kstar], ls="--", c="grey")
            ax[1].set_xlabel("J"); ax[1].set_ylabel("chi"); ax[1].set_title("susceptibility vs J")
            fig.tight_layout()
            fig.savefig(os.path.join(HERE, "L32_histogram.png"), dpi=110)
            print("figure -> L32_histogram.png")
    except Exception as e:
        print("figure skipped:", e)


if __name__ == "__main__":
    main()
