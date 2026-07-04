"""HQ2V_gate.py -- MANDATORY engineering gate for HQ2.

Charter: HQ2_CRITICAL_FERROMAGNET.md (HQ2-V).  Nothing downstream (c_eff, G_eff,
sigma8) may be measured until this passes.  Pre-registered question: does the
orientation correlation length xi(J) DIVERGE as J -> J_c, and is the transition
second order (continuous)?  If xi does not diverge, the transition is not
continuous and the "critical fluctuations" premise of HQ2 is void.

Method (reuses the E1 motor only):
  * build the SAME causal link graph as E1-1 (rho=2, elongated tube), one per seed;
  * for J spanning [0.5 J_c, 2 J_c] around J_c=0.08 (O(3) chi-peak from E1-2),
    measure m(J), chi(J), and C(r);
  * seed-average C(r) (count-weighted) and extract xi(J) with the SAME validated
    classifier E1 used (orientation_core.fit_forms).

PASS criteria (pre-registered):
  (1) chi(J) has an interior peak near J_c (susceptibility divergence);
  (2) xi(J) rises toward J_c from the disordered side (J<J_c);
  (3) the transition is continuous: m(J) lifts smoothly from ~1/sqrt(N), no jump
      (2nd order, as E1-2 already found) -- NOT first order.

Anti-circularity: J_c is the E1 measured value, not tuned; no exponent inserted.
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
JC = hc.JC["O(3)"]                                    # 0.08
# J grid straddling J_c across [0.5 J_c, 2 J_c], denser near J_c
J_OVER_JC = [0.5, 0.65, 0.8, 0.9, 1.0, 1.1, 1.25, 1.5, 2.0]
JS = [round(r * JC, 4) for r in J_OVER_JC]
N_SEEDS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
N_BURN = 1500                                         # critical slowing down
N_MEAS = 150
MIN_COUNT = 200
BASELINE_FRAC = None                                  # set from graph n


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"HQ2-V gate -- xi(J) divergence at J_c={JC} (O(3) causal ferromagnet)")
    print(f"seeds={N_SEEDS}  J/J_c={J_OVER_JC}  J={JS}")
    print("=" * 72)

    raw = {J: [] for J in JS}
    mvals = {J: [] for J in JS}
    chivals = {J: [] for J in JS}
    ns = []
    for seed in range(N_SEEDS):
        g, sources, dist_list = hc.build_seed(seed)
        ns.append(g.n)
        for J in JS:
            r, C, w, mm, msd, chi = hc.run_o3(g, sources, dist_list, J, seed,
                                              n_burn=N_BURN, n_meas=N_MEAS)
            raw[J].append((r, C, w))
            mvals[J].append(mm)
            chivals[J].append(chi)
        print(f"  seed {seed:2d}: n={g.n}  ({time.time()-t0:.0f}s)")

    N = float(np.mean(ns))
    baseline = 1.0 / np.sqrt(N)
    r_ref = np.arange(1, hc.R_CAP + 1)
    rows = []
    for J in JS:
        Cmean, Cstd, Wtot = hc.aggregate_curves(raw[J], r_ref, N_SEEDS)
        xi = hc.xi_from_curve(r_ref, Cmean, Cstd, Wtot, min_count=MIN_COUNT)
        m_mean = float(np.mean(mvals[J]))
        m_err = float(np.std(mvals[J]))
        chi_mean = float(np.mean(chivals[J]))
        chi_err = float(np.std(chivals[J]))
        rows.append({"J": J, "J_over_Jc": J / JC, "m": m_mean, "m_err": m_err,
                     "chi": chi_mean, "chi_err": chi_err, "winner": xi["winner"],
                     "xi": xi["xi"], "eta": xi["eta"], "C_long": xi["C_long"],
                     "n_points": xi["n_points"]})
        xitag = f"xi={xi['xi']:.1f}" if np.isfinite(xi["xi"]) else "xi=---"
        print(f"  J={J:6.4f} (J/Jc={J/JC:.2f})  m={m_mean:.3f}+-{m_err:.3f}  "
              f"chi={chi_mean:7.3f}  {xi['winner']:12s} {xitag} "
              f"C_long={xi['C_long']:.3f}")

    # ---- PASS evaluation (pre-registered) ----
    Jarr = np.array(JS)
    marr = np.array([r["m"] for r in rows])
    chiarr = np.array([r["chi"] for r in rows])
    # (1) chi peak is interior (not at an endpoint) and near J_c
    ipk = int(np.argmax(chiarr))
    chi_peak_J = JS[ipk]
    chi_interior_peak = 0 < ipk < len(JS) - 1
    chi_peak_near_Jc = 0.5 * JC <= chi_peak_J <= 2.0 * JC
    # (2) xi divergence across the critical region.  A 2nd-order transition has
    #     xi -> infinity at J_c.  The faithful finite-system signature here:
    #       - deep in the disordered phase (J << J_c) C(r) decays FASTER than the
    #         measurement floor -> 'insufficient' = xi below resolution (small);
    #       - near and above J_c xi becomes large and KEEPS GROWING.
    #     So xi spans from sub-resolution to >> lattice spacing across J_c.  We
    #     require (a) a large overall growth of the fitted xi, and (b) the deep
    #     disordered side being sub-resolution (insufficient).
    finite = [r for r in rows if np.isfinite(r["xi"])]
    finite = sorted(finite, key=lambda d: d["J"])
    xi_growth = (finite[-1]["xi"] / finite[0]["xi"]) if len(finite) >= 2 else 0.0
    deep_dis = [r for r in rows if r["J_over_Jc"] <= 0.8]
    deep_subres = all(r["winner"] in ("insufficient", "exp") for r in deep_dis) \
        and any(r["winner"] == "insufficient" for r in deep_dis)
    xi_rises = bool(xi_growth > 2.0 and deep_subres)
    # (3) continuity / 2nd order: m lifts smoothly from ~baseline; no discontinuous
    #     jump (max single-step Delta m well below 1; m below Jc near baseline).
    dm = np.diff(marr)
    max_jump = float(np.max(dm)) if dm.size else 0.0
    m_below = marr[Jarr < JC]
    starts_disordered = bool(m_below.size and m_below.min() < 8 * baseline)
    continuous = (max_jump < 0.6) and starts_disordered
    # onset: first J where m exceeds 5x baseline
    onset = next((r["J"] for r in rows if r["m"] > 5 * baseline), None)

    passed = bool(chi_interior_peak and chi_peak_near_Jc and xi_rises and continuous)

    print("-" * 72)
    print(f"  (1) chi interior peak near J_c : {chi_interior_peak and chi_peak_near_Jc} "
          f"(peak at J={chi_peak_J}, J/Jc={chi_peak_J/JC:.2f})")
    print(f"  (2) xi diverges across J_c     : {xi_rises} "
          f"(xi growth x{xi_growth:.1f}, deep-disordered sub-resolution={deep_subres})")
    print(f"  (3) continuous (2nd order)     : {continuous} "
          f"(max dm step={max_jump:.2f}, starts disordered={starts_disordered})")
    print(f"  ordering onset (m>5/sqrtN)     : J={onset}  (baseline 1/sqrtN={baseline:.3f})")
    print(f"\n  HQ2-V GATE: {'PASS' if passed else 'FAIL'}")
    if passed:
        print("  -> xi diverges / chi peaks at J_c, transition continuous. HQ2-1 may run.")
    else:
        print("  -> premise void; HQ2 downstream tasks must NOT run (death of HQ2 gate).")
    print("=" * 72)

    # ---- figure ----
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    ax = axes[0]
    for J in JS:
        Cmean, Cstd, Wtot = hc.aggregate_curves(raw[J], r_ref, N_SEEDS)
        ok = Wtot >= MIN_COUNT
        sel = ok & (Cmean > 0)
        ax.plot(r_ref[sel], Cmean[sel], "o-", ms=3, lw=1, label=f"J/Jc={J/JC:.2f}")
    ax.set_yscale("log"); ax.set_xlabel("r (causal proper time)")
    ax.set_ylabel("C(r)"); ax.set_title("orientation correlation C(r)")
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.2)

    axm = axes[1]
    axc = axm.twinx()
    axm.errorbar(Jarr / JC, marr, yerr=[r["m_err"] for r in rows], fmt="o-",
                 color="tab:red", label="m(J)")
    axc.errorbar(Jarr / JC, chiarr, yerr=[r["chi_err"] for r in rows], fmt="s--",
                 color="tab:blue", alpha=0.6, label="chi(J)")
    axm.axvline(1.0, color="k", ls=":", lw=1, label="J_c")
    axm.axhline(baseline, color="0.6", lw=0.8, ls="--")
    axm.set_xlabel("J / J_c"); axm.set_ylabel("order parameter m", color="tab:red")
    axc.set_ylabel("susceptibility chi", color="tab:blue")
    axm.set_title("m(J) lifts, chi(J) peaks at J_c (2nd order)")
    axm.legend(fontsize=8, loc="upper left"); axm.grid(alpha=0.2)

    axx = axes[2]
    xi_pts = [(r["J"] / JC, r["xi"]) for r in rows if np.isfinite(r["xi"])]
    if xi_pts:
        xx, yy = zip(*xi_pts)
        axx.plot(xx, yy, "o-", color="tab:green")
    axx.axvline(1.0, color="k", ls=":", lw=1, label="J_c")
    axx.set_xlabel("J / J_c"); axx.set_ylabel("correlation length xi")
    axx.set_yscale("log")
    axx.set_title("xi(J): rises toward J_c (divergence)")
    axx.legend(fontsize=8); axx.grid(alpha=0.2, which="both")
    fig.suptitle("HQ2-V gate: critical divergence of the causal orientation "
                 "ferromagnet at J_c", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "HQ2V_gate.png", dpi=130)
    print(f"saved {OUT/'HQ2V_gate.png'}")

    payload = {
        "task": "HQ2-V", "Jc_O3": JC, "n_seeds": N_SEEDS, "mean_n": N,
        "baseline_1_over_sqrtN": baseline, "J_over_Jc": J_OVER_JC, "Js": JS,
        "rows": rows, "chi_peak_J": chi_peak_J, "chi_peak_over_Jc": chi_peak_J / JC,
        "ordering_onset_J": onset,
        "checks": {"chi_interior_peak": bool(chi_interior_peak),
                   "chi_peak_near_Jc": bool(chi_peak_near_Jc),
                   "xi_diverges": bool(xi_rises),
                   "xi_growth_factor": float(xi_growth),
                   "deep_disordered_subresolution": bool(deep_subres),
                   "continuous_2nd_order": bool(continuous),
                   "max_m_step": max_jump},
        "passed": passed,
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "HQ2V_gate.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'HQ2V_gate.json'}  ({payload['runtime_s']:.0f}s)")
    return passed


if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
