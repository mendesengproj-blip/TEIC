"""E6c_1_curvature_scan.py -- B-type (spacelike/magnetic) fraction vs spatial CURVATURE.

Pre-registered question (E6c_CURVED_GEOMETRY): E6/E6b found that the causal-diamond
2-complex of a FLAT (Minkowski) Poisson causal set has no usable magnetic sector --
height-2 diamonds are 100% electric (frac_B = 0.0000) and taller 2h-gons only give a
non-growing ~0.25% tail (E6b, INCONCLUSIVE/leans-structural). Does background CURVATURE
furnish the missing spacelike (B-type) 2-cells? We sweep de Sitter curvature radius
R_dS from infinity (Minkowski) down to 2 ell (Planckian curvature) and remeasure frac_B
with the SAME E/B classifier (e6_bd_core) and the SAME 2h-gon diamonds (e6b core).

MANDATORY GATE (verbatim from the prompt):
  R_dS = inf (Minkowski) must reproduce E6b:  h=2 frac_B ~ 0 (Wilson-hi < 0.001),
  h=3 frac_B ~ 0.0024. If the gate fails the run is INVALID and no verdict is issued.

Pre-registered kill criterion (verbatim from the prompt):
  DEATH : frac_B < 0.001 across the WHOLE sweep (every R_dS, the best-sampled cell)
          -> spatial curvature does NOT furnish the magnetic sector
          -> E6 flips [FRONTEIRA-TECNICA] -> [FRONTEIRA-ESTRUTURAL], then E6d runs.
  SUCCESS : frac_B > 0.01 at some R_dS with statistical significance (Wilson-lo > 0.01)
          -> curvature opens the magnetic sector; report the minimal R_dS ("curvature
             radius" of the BD photon).
  INCONCLUSIVE : small non-zero, does not clear 0.001 robustly nor reach 0.01 -> report.

Result goes to RESEARCH_MAP.md, NOT to any paper.

Reuses e6c_curved_core (geometry) which reuses e6b_diamond_height_core / e6_bd_core (E/B
physics + 2h-gon topology) VERBATIM. No relativistic literal: the causal order is the
sprinkling's own conformal light-cone order, the E/B split uses only the embedding time
column -- identical anti-circularity posture to E6/E6b.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e6c_curved_core import desitter_sprinkle, measure_fraction, RHO   # noqa: E402

# curvature radii in units of the mean spacing ell = rho^(-1/4); inf = Minkowski (gate).
R_HATS = [np.inf, 16.0, 8.0, 4.0, 3.0, 2.0]
HEIGHTS = [2, 3, 4]                 # h=2 (E6 exact zero) + the E6b best-sampled heights
NS = [500, 1000, 2000]
SEEDS = [1, 2, 3]
MAX_PLAQS = 10000
PATHS_PER_SOURCE = 100
MAX_PAIRS = 4
MIN_P = 2000                        # a cell must carry this many plaquettes to be decisive


def _wilson(k, n, z=1.96):
    """(lo, hi) 95% Wilson bounds on a binomial fraction (meaningful when k is small/0)."""
    if n == 0:
        return float("nan"), float("nan")
    p = k / n
    den = 1 + z * z / n
    centre = p + z * z / (2 * n)
    half = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return float(max(0.0, (centre - half) / den)), float((centre + half) / den)


def _rkey(R_hat):
    return "inf" if not np.isfinite(R_hat) else f"{R_hat:g}"


def measure_one(N, R_hat, h, seed):
    pc, pe, info = desitter_sprinkle(N, R_hat, seed, rho=RHO)
    P, n_B, frac, me2, mb2, n = measure_fraction(
        pc, pe, h, seed, max_plaqs=MAX_PLAQS,
        paths_per_source=PATHS_PER_SOURCE, max_pairs=MAX_PAIRS)
    lo, hi = _wilson(n_B, P) if P else (float("nan"), float("nan"))
    return {"N_target": N, "N": n, "R_hat": (None if not np.isfinite(R_hat) else R_hat),
            "R_dS": (None if not np.isfinite(info["R_dS"]) else info["R_dS"]),
            "H": info["H"], "h": h, "seed": seed, "P": P, "n_B": n_B,
            "frac_B": frac, "mean_e2": me2, "mean_b2": mb2,
            "wilson_lo": lo, "wilson_hi": hi}


def make_figure(agg, verdict_tag):
    """frac_B vs curvature (1/R_hat), one curve per height at the best-sampled N, with the
    Minkowski gate point at 1/R_hat=0, plus the 0.001 death floor and 0.01 success line."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.6))
    colors = plt.cm.plasma(np.linspace(0.1, 0.8, len(HEIGHTS)))
    for h, col in zip(HEIGHTS, colors):
        xs, fr, er, rat = [], [], [], []
        for R_hat in R_HATS:
            a = agg[f"{2000}_{_rkey(R_hat)}_{h}"]
            if a.get("P_tot", 0) == 0 or a["frac_B"] != a["frac_B"]:
                continue
            invR = 0.0 if not np.isfinite(R_hat) else 1.0 / R_hat
            xs.append(invR); fr.append(a["frac_B"]); er.append(a["binom_err"])
            rat.append(a["mean_b2_over_e2"])
        order = np.argsort(xs)
        xs = np.array(xs)[order]; fr = np.array(fr)[order]
        er = np.array(er)[order]; rat = np.array(rat)[order]
        ax1.errorbar(xs, fr, yerr=er, marker="o", color=col, capsize=3,
                     label=f"h={h}", lw=1.6)
        ax2.plot(xs, rat, marker="s", color=col, lw=1.6, label=f"h={h}")
    ax1.axhline(0.01, ls="--", c="green", lw=1, label="success (0.01)")
    ax1.axhline(0.001, ls="--", c="red", lw=1, label="death floor (0.001)")
    ax1.axvline(0.0, ls=":", c="grey", lw=1)
    ax1.set_xlabel(r"curvature  $1/\hat{R}_{dS}$   (0 = Minkowski gate)")
    ax1.set_ylabel("B-type fraction  n_B / (n_B+n_E)")
    ax1.set_title(f"Magnetic 2-cell fraction vs de Sitter curvature  (N≈2000)\n[{verdict_tag}]")
    ax1.set_yscale("log"); ax1.set_ylim(5e-4, 3e-2)
    ax1.legend(fontsize=8, ncol=2); ax1.grid(alpha=0.3)
    ax2.set_xlabel(r"curvature  $1/\hat{R}_{dS}$")
    ax2.set_ylabel("mean  b² / e²   (per-cell magnetic content)")
    ax2.set_title("Per-cell magnetic content vs curvature")
    ax2.axhline(1.0, ls=":", c="grey", lw=1); ax2.legend(fontsize=8); ax2.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(HERE / "E6c_1_curvature_scan.png", dpi=130)
    plt.close(fig)


def main():
    t0 = time.time()
    runs = []
    for N in NS:
        for R_hat in R_HATS:
            for h in HEIGHTS:
                for seed in SEEDS:
                    r = measure_one(N, R_hat, h, seed)
                    runs.append(r)
                    print(f"N~{N:5d}(n={r['N']:5d}) Rhat={_rkey(R_hat):>4} h={h} s={seed} "
                          f"P={r['P']:6d} nB={r['n_B']:4d} fracB={r['frac_B']:.5f} "
                          f"b2/e2={(r['mean_b2']/r['mean_e2']) if r['mean_e2'] and r['mean_e2']==r['mean_e2'] else float('nan'):.3f}")

    # ---- aggregate over seeds per (N, R_hat, h): pooled fraction + binomial error ----
    agg = {}
    for N in NS:
        for R_hat in R_HATS:
            for h in HEIGHTS:
                key = f"{N}_{_rkey(R_hat)}_{h}"
                sub = [r for r in runs if r["N_target"] == N and
                       _rkey(np.inf if r["R_hat"] is None else r["R_hat"]) == _rkey(R_hat)
                       and r["h"] == h and r["P"] > 0]
                if not sub:
                    agg[key] = {"N_target": N, "R_hat_key": _rkey(R_hat), "h": h,
                                "P_tot": 0, "frac_B": float("nan")}
                    continue
                P_tot = sum(r["P"] for r in sub)
                nB_tot = sum(r["n_B"] for r in sub)
                frac = nB_tot / P_tot
                lo, hi = _wilson(nB_tot, P_tot)
                me2 = np.mean([r["mean_e2"] for r in sub])
                mb2 = np.mean([r["mean_b2"] for r in sub])
                agg[key] = {
                    "N_target": N, "R_hat_key": _rkey(R_hat), "h": h, "n_seeds": len(sub),
                    "R_dS": next((r["R_dS"] for r in sub if r["R_dS"] is not None), None),
                    "P_tot": P_tot, "nB_tot": nB_tot, "frac_B": frac,
                    "binom_err": float(np.sqrt(frac * (1 - frac) / P_tot)) if P_tot else float("nan"),
                    "wilson_lo": lo, "wilson_hi": hi,
                    "mean_b2_over_e2": float(mb2 / me2) if me2 else float("nan")}

    # ====================== MANDATORY GATE: R_dS = inf == E6b ======================
    # E6b best-sampled (N≈2000): h2 frac_B≈0 (Wilson-hi<0.001), h3≈0.0024, h4≈0.0025.
    g2 = agg[f"2000_inf_2"]; g3 = agg[f"2000_inf_3"]
    gate_h2_ok = (g2.get("P_tot", 0) >= MIN_P) and (g2["wilson_hi"] < 0.001)
    gate_h3_ok = (g3.get("P_tot", 0) >= MIN_P) and (0.0010 <= g3["frac_B"] <= 0.0045)
    gate_ok = bool(gate_h2_ok and gate_h3_ok)
    gate = {"h2_fracB": g2.get("frac_B"), "h2_wilson_hi": g2.get("wilson_hi"),
            "h2_ok_(<0.001 hi)": gate_h2_ok,
            "h3_fracB": g3.get("frac_B"), "h3_in_[0.001,0.0045]": gate_h3_ok,
            "PASS": gate_ok,
            "note": "Minkowski limit (R_dS=inf) must reproduce E6b before any curved verdict."}

    # ====================== pre-registered verdict logic ======================
    # decisive cells: best-sampled (P_tot >= MIN_P), across ALL curvatures + heights.
    decisive = [a for a in agg.values() if a.get("P_tot", 0) >= MIN_P]
    sig_success = [a for a in decisive if a["wilson_lo"] > 0.01]
    max_wilson_hi = max((a["wilson_hi"] for a in decisive), default=float("nan"))
    max_frac_dec = max((a["frac_B"] for a in decisive), default=float("nan"))

    # per-curvature best-sampled frac_B (max over heights at N=2000) -- the sweep summary.
    per_R_bestsampled = {}
    for R_hat in R_HATS:
        cells = [agg[f"2000_{_rkey(R_hat)}_{h}"] for h in HEIGHTS
                 if agg[f"2000_{_rkey(R_hat)}_{h}"].get("P_tot", 0) > 0]
        if cells:
            best = max(cells, key=lambda a: a["frac_B"])
            per_R_bestsampled[_rkey(R_hat)] = {
                "best_h": best["h"], "frac_B": best["frac_B"],
                "wilson_lo": best["wilson_lo"], "wilson_hi": best["wilson_hi"],
                "P_tot": best["P_tot"]}
        else:
            per_R_bestsampled[_rkey(R_hat)] = {"frac_B": float("nan")}

    if not gate_ok:
        verdict_tag = "INVALID-GATE"
        verdict = (f"GATE FAILED: the Minkowski limit (R_dS=inf) did NOT reproduce E6b "
                   f"(h2 frac_B={g2.get('frac_B')}, Wilson-hi={g2.get('wilson_hi')}; "
                   f"h3 frac_B={g3.get('frac_B')}). No curved-geometry verdict is issued -- "
                   f"the construction or sampling is broken and must be fixed first.")
    elif sig_success:
        winners = sorted(sig_success, key=lambda a: (-(a["R_dS"] or 0)))
        w = winners[0]
        verdict_tag = "SUCCESS"
        verdict = (f"SUCCESS: spatial curvature OPENS the magnetic sector -- the B-type "
                   f"(spacelike) fraction exceeds 0.01 with significance (Wilson-lo "
                   f"{w['wilson_lo']:.4f} > 0.01) at R_dS≈{w['R_dS']:.2f} (Rhat={w['R_hat_key']}), "
                   f"h={w['h']}. Largest curvature radius that still works = the BD-photon "
                   f"'curvature radius'. E6 advances past [FRONTEIRA-TECNICA].")
    elif max_wilson_hi == max_wilson_hi and max_wilson_hi < 0.001:
        verdict_tag = "DEATH"
        verdict = (f"DEATH (structural): across the ENTIRE curvature sweep R_dS=inf..2ℓ, every "
                   f"well-sampled cell (P>={MIN_P}) keeps frac_B below 0.001 even at its 95% "
                   f"Wilson upper bound (max Wilson-hi {max_wilson_hi:.5f}). Spatial curvature "
                   f"does NOT furnish the spacelike 2-cell -- the BD-gauge E²-B² photon is "
                   f"structurally blocked on the causal set independent of background curvature. "
                   f"E6 flips [FRONTEIRA-TECNICA] -> [FRONTEIRA-ESTRUTURAL]; E6d (orientation-"
                   f"gauge coupling) is the next move.")
    else:
        bs = ", ".join(f"Rhat{k}:{v['frac_B']:.4f}" for k, v in per_R_bestsampled.items()
                       if v.get("frac_B") == v.get("frac_B"))
        # does curvature push frac_B UP relative to the Minkowski gate?
        flat_f = per_R_bestsampled["inf"]["frac_B"]
        curved_max = max((v["frac_B"] for k, v in per_R_bestsampled.items()
                          if k != "inf" and v.get("frac_B") == v.get("frac_B")),
                         default=float("nan"))
        trend = ("curvature mildly raises frac_B but it stays sub-0.01"
                 if curved_max > flat_f + 0.0005 else
                 "curvature does NOT raise frac_B above the flat value")
        verdict_tag = "INCONCLUSIVE"
        verdict = (f"INCONCLUSIVE (leans structural): with the Minkowski gate PASSED, the "
                   f"curved sweep gives best-sampled (N≈2000) fractions {{{bs}}} -- all BELOW "
                   f"the 0.01 success threshold; the strongest decisive cell reaches only "
                   f"frac_B={max_frac_dec:.5f} (Wilson-hi {max_wilson_hi:.5f}). {trend.capitalize()}. "
                   f"The death floor 0.001 is not cleanly cleared across all curvatures, so the "
                   f"criterion does not strictly fire; report honestly. Curvature does not deliver "
                   f"the O(1) magnetic 2-cell.")

    out = {"params": {"R_hats": ["inf" if not np.isfinite(r) else r for r in R_HATS],
                      "heights": HEIGHTS, "Ns": NS, "seeds": SEEDS, "rho": RHO,
                      "max_plaqs": MAX_PLAQS, "paths_per_source": PATHS_PER_SOURCE,
                      "max_pairs": MAX_PAIRS, "MIN_P_decisive": MIN_P},
           "gate": gate, "runs": runs, "aggregate": agg,
           "per_R_bestsampled": per_R_bestsampled,
           "max_frac_decisive": max_frac_dec, "max_wilson_hi_decisive": max_wilson_hi,
           "verdict_tag": verdict_tag, "verdict": verdict,
           "runtime_s": time.time() - t0}
    (HERE / "E6c_1_curvature_scan.json").write_text(json.dumps(out, indent=2))
    make_figure(agg, verdict_tag)

    print("\n==== GATE (R_dS=inf must == E6b) ====")
    for k, v in gate.items():
        print(f"  {k}: {v}")
    print("\n==== aggregate (pooled over seeds, N=2000) ====")
    print(f"{'R_hat':>6} {'h':>2} {'P_tot':>7} {'nB':>5} {'frac_B':>8} {'wlo':>8} "
          f"{'whi':>8} {'b2/e2':>7}")
    for R_hat in R_HATS:
        for h in HEIGHTS:
            a = agg[f"2000_{_rkey(R_hat)}_{h}"]
            if a.get("P_tot", 0) == 0:
                print(f"{_rkey(R_hat):>6} {h:>2} {'0':>7}"); continue
            print(f"{_rkey(R_hat):>6} {h:>2} {a['P_tot']:>7} {a['nB_tot']:>5} "
                  f"{a['frac_B']:>8.5f} {a['wilson_lo']:>8.5f} {a['wilson_hi']:>8.5f} "
                  f"{a['mean_b2_over_e2']:>7.3f}")
    print(f"\nVERDICT [{verdict_tag}]: {verdict}")
    print(f"runtime {out['runtime_s']:.0f}s -> E6c_1_curvature_scan.json")
    return out


if __name__ == "__main__":
    main()
