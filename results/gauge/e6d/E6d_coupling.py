"""E6d_coupling.py -- does ferromagnet<->gauge coupling AMPLIFY E6c's magnetic sector?

Pre-registered question (E6d_ORIENTATION_GAUGE_COUPLING): on E6c's CURVED substrate
(de Sitter R̂=2, h=4), where the bare gauge bivector already gives a B-type (magnetic)
fraction ≈1.17%, does coupling the ordered orientation ferromagnet (E1, O(3) field n⃗∈S²)
to the gauge bivector via Φ=A+λ(n⃗_i×n⃗_j)·ê_z push frac_B from ~1% toward O(1)?

The coupling is realised EXACTLY inside E6's geometric E/B classifier by augmenting the 5D
de Sitter embedding with internal axes λ(n·e1, n·e2) (see e6d_coupling_core docstring): the
internal–internal bivector component equals ½λ²Σ(n×n')·ê_z (the prompt's coupling), the
internal axes are spacelike so they feed the magnetic channel, and λ=0 returns E6c
bit-for-bit. polygon_bivectors / height_h_plaquettes / de Sitter geometry all REUSED VERBATIM.

GATES (pre-registered):
  G0 : λ=0 on the curved substrate reproduces E6c's frac_B (≈0.0117 pooled)  [bit-for-bit].
  G1 : λ=0, any J reproduces E6c (the coupling-OFF control).
  G2 : λ>0 with a DISORDERED ferromagnet (J<J_c, |M|≈0) gives ≈ G1 -- i.e. the effect (if
       any) REQUIRES ordering; a rise driven by disorder is a spacelike-noise artefact.

KILL CRITERION (verbatim):
  SUCCESS      : frac_B > 0.05 AND grows with λ on the curved ordered substrate (J>J_c)
                 -> coupling amplifies E6c's signal; next step = measure the symbol λ(k,ω).
  DEATH        : frac_B < 0.02 across the WHOLE (λ,J) sweep even on the curved substrate
                 -> coupling does NOT amplify; document what it DOES produce.
  INCONCLUSIVE : frac_B grows but stays in [0.02, 0.05] -> partial; report values + how
                 much more λ would be needed.

Result goes to RESEARCH_MAP.md, NOT to a paper. Does NOT modify E6/E6b/E6c.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e6d_coupling_core import (build_substrate, equilibrate_orientation,      # noqa: E402
                               measure_coupled_fraction, polygon_bivectors,
                               R_HAT_SUBSTRATE, H_DIAMOND)

LAMBDAS = [0.0, 0.1, 0.5, 1.0, 2.0]
J_C = 0.05                       # critical coupling on the R̂=2 causal graph (M≈0.43)
J_PHASES = {"disordered": 0.02,  # |M|≈0.02  -> G2 control (coupling must NOT amplify here)
            "J_c": 0.05,         # |M|≈0.43  critical ferromagnet
            "2J_c": 0.10}        # |M|≈0.80  deep-ordered ferromagnet
NS = [1000, 2000]
SEEDS = [1, 2, 3]
N_BURN = 500
SUCCESS_THR = 0.05
DEATH_THR = 0.02


def _wilson(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    den = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return float(max(0.0, (centre - half) / den)), float((centre + half) / den)


def run_all():
    runs = []
    for N in NS:
        for seed in SEEDS:
            pc, pe, g, V, info = build_substrate(N, seed, R_hat=R_HAT_SUBSTRATE, h=H_DIAMOND)
            # E6c geometric baseline on THIS substrate (λ=0, no orientation):
            _, e2b, b2b = polygon_bivectors(pe, V)
            frac_e6c = float(np.mean(b2b > e2b)) if V.shape[0] else float("nan")
            for phase, J in J_PHASES.items():
                n, M, ez = equilibrate_orientation(g, J, seed=seed, n_burn=N_BURN)
                for lam in LAMBDAS:
                    P, nB, frac, me2, mb2 = measure_coupled_fraction(pe, n, ez, lam, V)
                    runs.append({"N_target": N, "N": int(g.n), "seed": seed,
                                 "R_dS": info["R_dS"], "phase": phase, "J": J, "M": M,
                                 "lam": lam, "P": P, "n_B": nB, "frac_B": frac,
                                 "mean_e2": me2, "mean_b2": mb2, "frac_e6c": frac_e6c})
                    print(f"N~{N} s{seed} {phase:>10}(M={M:.2f}) λ={lam:3.1f} "
                          f"P={P:5d} nB={nB:4d} fracB={frac:.5f} b2/e2={mb2/me2 if me2 else float('nan'):.3f}")
    return runs


def aggregate(runs):
    agg = {}
    for N in NS:
        for phase in J_PHASES:
            for lam in LAMBDAS:
                sub = [r for r in runs if r["N_target"] == N and r["phase"] == phase
                       and r["lam"] == lam and r["P"] > 0]
                key = f"{N}_{phase}_{lam}"
                if not sub:
                    agg[key] = {"N": N, "phase": phase, "lam": lam, "P_tot": 0,
                                "frac_B": float("nan")}
                    continue
                P_tot = sum(r["P"] for r in sub)
                nB_tot = sum(r["n_B"] for r in sub)
                frac = nB_tot / P_tot
                lo, hi = _wilson(nB_tot, P_tot)
                me2 = np.mean([r["mean_e2"] for r in sub])
                mb2 = np.mean([r["mean_b2"] for r in sub])
                agg[key] = {"N": N, "phase": phase, "lam": lam, "M": float(np.mean([r["M"] for r in sub])),
                            "P_tot": P_tot, "nB_tot": nB_tot, "frac_B": frac,
                            "binom_err": float(np.sqrt(frac * (1 - frac) / P_tot)) if P_tot else float("nan"),
                            "wilson_lo": lo, "wilson_hi": hi,
                            "frac_e6c": float(np.mean([r["frac_e6c"] for r in sub])),
                            "mean_b2_over_e2": float(mb2 / me2) if me2 else float("nan")}
    return agg


def make_figure(agg, verdict_tag):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    colors = {"disordered": "#888888", "J_c": "#d1495b", "2J_c": "#1f77b4"}
    for phase in J_PHASES:
        las, fr, er, rat = [], [], [], []
        for lam in LAMBDAS:
            a = agg[f"{2000}_{phase}_{lam}"]
            if a.get("P_tot", 0) == 0:
                continue
            las.append(lam); fr.append(a["frac_B"]); er.append(a["binom_err"])
            rat.append(a["mean_b2_over_e2"])
        M = agg[f"{2000}_{phase}_{LAMBDAS[-1]}"].get("M", float("nan"))
        ax1.errorbar(las, fr, yerr=er, marker="o", color=colors[phase], capsize=3,
                     lw=1.7, label=f"{phase} (|M|≈{M:.2f})")
        ax2.plot(las, rat, marker="s", color=colors[phase], lw=1.7, label=f"{phase}")
    ax1.axhline(SUCCESS_THR, ls="--", c="green", lw=1, label="success (0.05)")
    ax1.axhline(DEATH_THR, ls="--", c="red", lw=1, label="death floor (0.02)")
    ax1.axhline(0.0117, ls=":", c="purple", lw=1, label="E6c baseline (0.0117)")
    ax1.set_xlabel("coupling  λ")
    ax1.set_ylabel("B-type (magnetic) fraction  frac_B")
    ax1.set_title(f"Coupled magnetic fraction vs λ on E6c curved substrate (R̂=2, h=4, N≈2000)\n[{verdict_tag}]")
    ax1.set_yscale("log"); ax1.set_ylim(8e-3, 1.0)
    ax1.legend(fontsize=8); ax1.grid(alpha=0.3)
    ax2.set_xlabel("coupling  λ")
    ax2.set_ylabel("mean  b²/e²  (per-cell magnetic content)")
    ax2.set_title("Per-cell magnetic content vs λ")
    ax2.axhline(1.0, ls=":", c="grey", lw=1); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "E6d_coupling.png", dpi=130)
    plt.close(fig)


def verdict(agg, runs):
    """Pre-registered verdict + gate checks on the best-sampled N=2000 cells.

    Crucial discriminator: SUCCESS requires the frac_B rise to be SOURCED BY ORDER
    (G2: disordered control must NOT amplify). A rise driven by disorder is a
    spacelike-noise artefact (any random internal field inflates b²), which the gate rejects.
    """
    # ---- G0/G1: λ=0 reproduces E6c geometric fraction BIT-FOR-BIT, per run ----
    lam0 = [r for r in runs if r["lam"] == 0.0 and r["P"] > 0]
    gate_G0 = all(abs(r["frac_B"] - r["frac_e6c"]) < 1e-12 for r in lam0)
    # G1: at λ=0 the phase (J) is irrelevant (orientation OFF) -> identical fraction per (N,seed)
    gate_G1 = True
    for N in NS:
        for seed in SEEDS:
            vals = [r["frac_B"] for r in lam0 if r["N_target"] == N and r["seed"] == seed]
            if vals and (max(vals) - min(vals)) > 1e-12:
                gate_G1 = False
    # G2: λ>0 DISORDERED must stay near the λ=0 baseline (the coupling needs ORDER).
    base = agg["2000_disordered_0.0"]["frac_B"]
    dis_max = max(agg[f"2000_disordered_{lam}"]["frac_B"] for lam in LAMBDAS if lam > 0)
    gate_G2 = dis_max < max(2 * base, base + 0.01)     # disordered must not amplify materially

    # ---- ORDER-DEPENDENCE: at fixed λ, does MORE order give MORE magnetic (hypothesis)
    #      or LESS (anti-amplification)? Compare disordered vs J_c vs 2J_c at λ=2. ----
    at = lambda ph, lam: agg[f"2000_{ph}_{lam}"]["frac_B"]
    order_trend_lam2 = {ph: at(ph, 2.0) for ph in J_PHASES}            # disordered>J_c>2J_c?
    order_suppresses = (at("disordered", 2.0) > at("J_c", 2.0) > at("2J_c", 2.0))
    ord_all = [agg[f"2000_{ph}_{lam}"] for ph in ("J_c", "2J_c") for lam in LAMBDAS]
    max_ord_all = max(c["frac_B"] for c in ord_all)
    grows_ordered = all(at("2J_c", LAMBDAS[i]) <= at("2J_c", LAMBDAS[i + 1]) + 1e-9
                        for i in range(len(LAMBDAS) - 1))

    gates = {"G0_lam0_eq_E6c_bitwise": bool(gate_G0), "G1_lam0_phase_indep": bool(gate_G1),
             "G2_disordered_no_amplify": bool(gate_G2),
             "G2_detail": {"baseline_frac": base, "disordered_max_frac": dis_max},
             "order_dependence_at_lam2": order_trend_lam2,
             "more_order_LESS_magnetic": bool(order_suppresses)}

    if max_ord_all > SUCCESS_THR and grows_ordered and gate_G2:
        tag = "SUCCESS"
        v = (f"SUCCESS: on the curved ORDERED substrate the coupling amplifies the magnetic "
             f"sector past 0.05 (max frac_B={max_ord_all:.4f}) growing with λ, AND the "
             f"disordered control stays flat (G2 PASS) -- the effect REQUIRES ferromagnetic "
             f"order. Next: measure the coupled symbol λ(k,ω).")
    elif not gate_G2 and order_suppresses:
        # The amplification HYPOTHESIS is falsified: frac_B does rise with λ, but it is a
        # disorder-sourced spacelike-noise artefact, and ORDER SUPPRESSES it.
        tag = "DEATH"
        v = (f"DEATH — amplification hypothesis FALSIFIED. frac_B does rise with λ (up to "
             f"{agg['2000_disordered_2.0']['frac_B']:.3f} at λ=2), exceeding 0.05, BUT: "
             f"(i) the rise is driven by DISORDER, not order — G2 FAILS (disordered λ=2 "
             f"frac_B={at('disordered',2.0):.3f} ≫ baseline {base:.4f}); (ii) ferromagnetic "
             f"ORDER SUPPRESSES it (λ=2: disordered {at('disordered',2.0):.3f} > J_c "
             f"{at('J_c',2.0):.3f} > 2J_c {at('2J_c',2.0):.3f}). The ordered condensate does "
             f"NOT amplify E6c's curvature signal — it weakens it. What the coupling 'produces' "
             f"is spacelike NOISE from incoherent orientation texture (any random internal "
             f"field inflates b²); coherent (ordered) texture sweeps LESS internal area, so "
             f"more order = less magnetic. The Meissner-style amplification is not realised.")
    elif max_ord_all < DEATH_THR:
        tag = "DEATH"
        v = (f"DEATH: across the WHOLE (λ,J) sweep on the curved substrate frac_B stays below "
             f"0.02 (max {max_ord_all:.4f}). The coupling adds no usable magnetic 2-cell content.")
    else:
        tag = "INCONCLUSIVE"
        order_word = ("sourced by ORDER (G2 holds)" if gate_G2 else
                      "driven by DISORDER not order (G2 FAILS) — a spacelike-noise artefact")
        v = (f"INCONCLUSIVE: coupling moves frac_B (max ordered {max_ord_all:.4f} vs baseline "
             f"{base:.4f}); rise is {order_word}. Reported with the measured λ-response.")
    return tag, v, gates


def main():
    t0 = time.time()
    runs = run_all()
    agg = aggregate(runs)
    tag, v, gates = verdict(agg, runs)
    make_figure(agg, tag)

    out = {"params": {"lambdas": LAMBDAS, "J_phases": J_PHASES, "Ns": NS, "seeds": SEEDS,
                      "R_hat_substrate": R_HAT_SUBSTRATE, "h": H_DIAMOND, "n_burn": N_BURN,
                      "success_thr": SUCCESS_THR, "death_thr": DEATH_THR},
           "runs": runs, "aggregate": agg, "gates": gates,
           "verdict_tag": tag, "verdict": v, "runtime_s": time.time() - t0}
    (HERE / "E6d_coupling.json").write_text(json.dumps(out, indent=2))

    print("\n==== GATES ====")
    for k, val in gates.items():
        print(f"  {k}: {val}")
    print("\n==== aggregate (pooled over seeds, N=2000) ====")
    print(f"{'phase':>10} {'|M|':>5} {'λ':>4} {'P_tot':>7} {'nB':>5} {'frac_B':>8} "
          f"{'wlo':>8} {'whi':>8} {'b2/e2':>7}")
    for phase in J_PHASES:
        for lam in LAMBDAS:
            a = agg[f"2000_{phase}_{lam}"]
            if a.get("P_tot", 0) == 0:
                continue
            print(f"{phase:>10} {a['M']:>5.2f} {lam:>4.1f} {a['P_tot']:>7} {a['nB_tot']:>5} "
                  f"{a['frac_B']:>8.5f} {a['wilson_lo']:>8.5f} {a['wilson_hi']:>8.5f} "
                  f"{a['mean_b2_over_e2']:>7.3f}")
    print(f"\nVERDICT [{tag}]: {v}")
    print(f"runtime {out['runtime_s']:.0f}s -> E6d_coupling.json")
    return out


if __name__ == "__main__":
    main()
