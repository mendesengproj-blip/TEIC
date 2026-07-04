"""E1_1_correlations.py -- orientation correlation C(r) of the CAUSAL vacuum.

Charter: E1_ORIENTATION.md (E1-1).  Runs ONLY after the E1-V gate passed.
Question (pre-registered): does the causal-network vacuum have long-range
orientational order?  Measure

    C(r) = <e^{i phi(0)} e^{-i phi(r)}>   (U(1))   or   <n(0).n(r)>   (O(3))

on the causal LINK graph (Hasse diagram of a 3+1D Poisson sprinkle), with r the
CAUSAL GEODESIC distance = longest-chain (proper-time) separation between two
timelike-related events.  Scan the rigidity J in {0.5,1,2,5,10}, 20 seeds, both
candidates.  Classify C(r) as exponential / power-law / constant (same validated
classifier as the gate).

Pre-registered verdict map:
  C(r) exp at ALL J            -> C  : disordered plasma, ferromagnet REJECTED.
  C(r) ~ r^{-eta} (power)      -> B  : quasi-order / critical (KT-like).
  C(r) -> C0 > 0 (const, =m^2) -> A  : causal ferromagnet CONFIRMED.

Anti-circularity: 'photon'/'magnon' do not appear in the generator; no critical
coupling inserted; the longest-chain metric and the classifier are fixed before
touching the data; real arithmetic only; fixed seeds.
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

import orientation_core as oc  # noqa: E402

OUT = Path(__file__).resolve().parent

# ---- pre-registered configuration ---------------------------------------- #
RHO = 2.0
BOX = [(0.0, 40.0), (0.0, 3.0), (0.0, 3.0), (0.0, 3.0)]   # elongated causal tube
# Charter J range {0.5..10}; the causal link graph has high coordination
# (avgdeg~46, the known non-locality of 4D causal-set links), so J_c sits far
# BELOW 0.5 and the whole charter range is ordered.  To make the pre-registered
# death criterion a genuine test we EXTEND the scan downward to expose the
# disordered phase and locate the transition.  Charter values are kept and
# reported.  (Honest scoping: the extension is declared, not hidden.)
CHARTER_JS = [0.5, 1.0, 2.0, 5.0, 10.0]
LOW_JS = [0.01, 0.02, 0.03, 0.05, 0.08, 0.13, 0.2, 0.35]
JS = sorted(set(LOW_JS + CHARTER_JS))
N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 20
N_SOURCES = 24
R_CAP = 50            # cap longest-chain bins; outer shells thin out
MIN_COUNT = 200       # minimum pair-count for a C(r) shell to be trusted
N_BURN = 1000
N_MEAS = 120
MEAS_EVERY = 2
MODELS = ("U(1)", "O(3)")


def build_seed(seed):
    """Causal link graph + precomputed longest-chain distance arrays from sources
    drawn in the earliest 30% of the time order (so they have deep futures)."""
    rng = np.random.default_rng(7000 + seed)
    pts = oc.sprinkle_box(RHO, BOX, rng)
    g = oc.causal_link_graph(pts)
    early = g.topo_order[:max(N_SOURCES, int(0.3 * g.n))]
    sources = rng.choice(early, size=min(N_SOURCES, early.size), replace=False)
    dist_list = [oc.longest_chain_from(g, int(s), r_max=R_CAP) for s in sources]
    return g, sources, dist_list


def run_model(g, sources, dist_list, model_name, J, seed):
    Model = oc.MODELS[model_name]
    m = Model(g, J=J, seed=10_000 * seed + (1 if model_name == "U(1)" else 2))
    m.equilibrate(N_BURN, adapt=True)
    acc = oc.CorrelationAccumulator(sources, dist_list, R_CAP)
    m_series = []
    taken, s = 0, 0
    while taken < N_MEAS:
        m.sweep()
        s += 1
        if s % MEAS_EVERY == 0:
            acc.add(m)
            m_series.append(m.order_parameter())
            taken += 1
    r, C, w = acc.result()
    ms = np.array(m_series)
    # susceptibility chi = N (<m^2> - <m>^2), N = number of nodes
    chi = float(g.n * (np.mean(ms ** 2) - np.mean(ms) ** 2))
    return r, C, w, float(ms.mean()), float(ms.std()), chi


def aggregate(per_seed_curves, r_ref):
    """Average C(r) over seeds on the common r grid r_ref (count-weighted)."""
    Cs, Ws = [], []
    for r, C, w in per_seed_curves:
        Cg = np.full(r_ref.shape, np.nan)
        Wg = np.zeros(r_ref.shape)
        idx = {int(rr): k for k, rr in enumerate(r)}
        for k, rr in enumerate(r_ref):
            if rr in idx:
                Cg[k] = C[idx[rr]]
                Wg[k] = w[idx[rr]]
        Cs.append(Cg)
        Ws.append(Wg)
    Cs, Ws = np.array(Cs), np.array(Ws)
    with np.errstate(invalid="ignore"):
        Cmean = np.nansum(Cs * Ws, axis=0) / np.maximum(np.nansum(Ws, axis=0), 1e-9)
        Cstd = np.nanstd(Cs, axis=0)
    Wtot = np.nansum(Ws, axis=0)
    return Cmean, Cstd, Wtot


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"E1-1 -- causal-vacuum orientation correlation  (seeds={N_SEEDS})")
    print(f"rho={RHO} box={BOX}  J={JS}  metric=longest-chain (causal proper time)")
    print("=" * 72)

    # graph stats (per seed) + storage
    raw = {model: {J: [] for J in JS} for model in MODELS}
    mvals = {model: {J: [] for J in JS} for model in MODELS}
    chivals = {model: {J: [] for J in JS} for model in MODELS}
    gstats = []
    for seed in range(N_SEEDS):
        g, sources, dist_list = build_seed(seed)
        gstats.append({"n": g.n, "links": g.n_links,
                       "avgdeg": 2 * g.n_links / g.n})
        for model in MODELS:
            for J in JS:
                r, C, w, mm, ms, chi = run_model(g, sources, dist_list,
                                                 model, J, seed)
                raw[model][J].append((r, C, w))
                mvals[model][J].append(mm)
                chivals[model][J].append(chi)
        print(f"  seed {seed:2d}: n={g.n} links={g.n_links} "
              f"avgdeg={2*g.n_links/g.n:.0f}   ({time.time()-t0:.0f}s)")

    r_ref = np.arange(1, R_CAP + 1)
    results = {model: {} for model in MODELS}
    for model in MODELS:
        for J in JS:
            Cmean, Cstd, Wtot = aggregate(raw[model][J], r_ref)
            ok = Wtot >= MIN_COUNT
            r_use = r_ref[ok]
            C_use = Cmean[ok]
            e_use = Cstd[ok] / np.sqrt(N_SEEDS)
            fit = oc.fit_forms(r_use, C_use, sigma=Cstd[ok], r_lo=2)
            m_mean = float(np.mean(mvals[model][J]))
            m_err = float(np.std(mvals[model][J]))
            chi_mean = float(np.mean(chivals[model][J]))
            results[model][J] = {
                "r": r_use.tolist(), "C": C_use.tolist(),
                "C_err": e_use.tolist(), "counts": Wtot[ok].tolist(),
                "fit": fit, "m": m_mean, "m_err": m_err, "chi": chi_mean,
                "C_long": fit["C_long"], "m2": m_mean ** 2}
            win = fit["winner"]
            tag = (f"xi={fit['exp']['xi']:.1f}" if win == "exp" else
                   f"eta={fit['power']['eta']:.2f}" if win == "power" else
                   f"C0={fit['const']['C0']:.3f}")
            print(f"  {model} J={J:5.2f}  m={m_mean:.3f}  chi={chi_mean:8.2f}  "
                  f"C(r): {win:12s} {tag:12s} C_long={fit['C_long']:.3f} "
                  f"m^2={m_mean**2:.3f}")

    # ---- pre-registered verdict --------------------------------------- #
    winners = {model: {J: results[model][J]["fit"]["winner"] for J in JS}
               for model in MODELS}

    def classify_model(model):
        ws = [winners[model][J] for J in JS]
        # genuine LRO requires a const plateau whose C_long matches m^2
        lro_Js = [J for J in JS
                  if results[model][J]["fit"]["winner"] == "const"
                  and results[model][J]["m"] ** 2 > 0
                  and abs(results[model][J]["C_long"] - results[model][J]["m"] ** 2)
                  / results[model][J]["m"] ** 2 < 0.25]
        power_Js = [J for J in JS if results[model][J]["fit"]["winner"] == "power"]
        all_exp = all(w in ("exp", "insufficient") for w in ws)
        if lro_Js:
            return "A", lro_Js
        if power_Js and not lro_Js:
            return "B", power_Js
        if all_exp:
            return "C", []
        return "D", []

    # ---- locate the transition J_c (susceptibility peak + exp->const crossover) #
    jc = {}
    for model in MODELS:
        chi_arr = np.array([results[model][J]["chi"] for J in JS])
        jc_chi = JS[int(np.argmax(chi_arr))]
        # crossover: highest J still classified exp (disordered) -> first const
        exp_Js = [J for J in JS if results[model][J]["fit"]["winner"] == "exp"]
        const_Js = [J for J in JS if results[model][J]["fit"]["winner"] == "const"]
        jc_cross = None
        if exp_Js and const_Js:
            jc_cross = 0.5 * (max(exp_Js) + min([J for J in const_Js
                                                 if J > max(exp_Js)] or [max(exp_Js)]))
        jc[model] = {"chi_peak_J": jc_chi, "crossover_J": jc_cross,
                     "chi_max": float(chi_arr.max())}

    verdicts = {model: classify_model(model) for model in MODELS}
    # overall: A if either candidate confirms LRO; C only if BOTH stay disordered
    codes = {v[0] for v in verdicts.values()}
    if "A" in codes:
        overall = "A"
    elif "B" in codes and "A" not in codes:
        overall = "B"
    elif codes == {"C"}:
        overall = "C"
    else:
        overall = "D"

    print("-" * 72)
    for model in MODELS:
        print(f"  {model}: J_c(chi-peak)={jc[model]['chi_peak_J']}  "
              f"J_c(exp->const crossover)~{jc[model]['crossover_J']}  "
              f"chi_max={jc[model]['chi_max']:.1f}")
    for model in MODELS:
        code, Js = verdicts[model]
        print(f"  {model}: verdict {code}  (J: {Js})")
    labels = {"A": "FERROMAGNETO CAUSAL (LRO, C0=m^2)",
              "B": "QUASI-ORDEM / CRITICO (power-law)",
              "C": "DESORDENADO (exp em todo J) -- ferromagneto REJEITADO",
              "D": "INCONCLUSIVO"}
    print(f"  OVERALL E1-1 VERDICT: {overall} -- {labels[overall]}")
    print("=" * 72)

    # ---- figure ------------------------------------------------------- #
    fig, axes = plt.subplots(1, 3, figsize=(17, 5.2))
    for ax, model in zip(axes[:2], MODELS):
        for J in JS:
            d = results[model][J]
            r = np.array(d["r"]); C = np.array(d["C"]); e = np.array(d["C_err"])
            sel = C > 0
            ax.errorbar(r[sel], C[sel], yerr=e[sel], fmt="o-", ms=3, lw=1,
                        capsize=1.5, label=f"J={J:g} m={d['m']:.2f}")
        ax.set_yscale("log")
        ax.set_xlabel("r  (causal proper-time, longest chain)")
        ax.set_ylabel("C(r)")
        ax.set_title(f"causal vacuum -- {model}")
        ax.legend(fontsize=7, ncol=2)
        ax.grid(alpha=0.2)
    # transition panel: m(J) and chi(J)
    axt = axes[2]
    axc = axt.twinx()
    for model, col in zip(MODELS, ("tab:blue", "tab:red")):
        Jarr = np.array(JS)
        marr = np.array([results[model][J]["m"] for J in JS])
        carr = np.array([results[model][J]["chi"] for J in JS])
        axt.plot(Jarr, marr, "o-", color=col, label=f"m {model}")
        axc.plot(Jarr, carr, "s--", color=col, alpha=0.5, label=f"chi {model}")
        axt.axvline(jc[model]["chi_peak_J"], color=col, ls=":", lw=1)
    axt.set_xscale("log")
    axt.set_xlabel("J  (= 1/T, rigidity)")
    axt.set_ylabel("order parameter m")
    axc.set_ylabel("susceptibility chi")
    axt.set_title("transition: m(J) rises, chi(J) peaks at J_c")
    axt.legend(fontsize=8, loc="center left")
    axt.grid(alpha=0.2)
    fig.suptitle("E1-1: orientation correlation of the causal vacuum vs causal "
                 "geodesic distance, and the ordering transition\n(C(r) flattening "
                 "= long-range order; straight log-line = exponential/disordered)",
                 fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E1_1_correlations.png", dpi=130)
    print(f"saved {OUT/'E1_1_correlations.png'}")

    payload = {
        "config": {"rho": RHO, "box": BOX, "Js": JS, "n_seeds": N_SEEDS,
                   "n_sources": N_SOURCES, "r_cap": R_CAP, "min_count": MIN_COUNT,
                   "n_burn": N_BURN, "n_meas": N_MEAS, "meas_every": MEAS_EVERY,
                   "metric": "longest_chain_causal_proper_time"},
        "graph_stats": {"mean_n": float(np.mean([s["n"] for s in gstats])),
                        "mean_links": float(np.mean([s["links"] for s in gstats])),
                        "mean_avgdeg": float(np.mean([s["avgdeg"] for s in gstats]))},
        "results": {model: {str(J): results[model][J] for J in JS}
                    for model in MODELS},
        "transition_Jc": jc,
        "charter_Js": CHARTER_JS, "low_Js": LOW_JS,
        "verdicts": {model: {"code": verdicts[model][0],
                             "lro_or_power_Js": verdicts[model][1]}
                     for model in MODELS},
        "overall_verdict": overall,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "E1_1_correlations.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E1_1_correlations.json'}  ({payload['runtime_s']:.0f}s)")
    return overall


if __name__ == "__main__":
    main()
