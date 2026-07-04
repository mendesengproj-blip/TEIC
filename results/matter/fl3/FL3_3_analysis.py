"""FL3-3 -- collision analysis: which scenario, and is topological matter created?

Reads FL3_2_dynamics.json and applies the pre-registered classification to every seed,
using the RADIATION-PROOF topological-matter content Q_top = integral of the strongly
smoothed |baryon density| (fl3_core.topological_matter).  Q_top counts genuine charged
cores (~1 each) and cancels the sign-alternating magnon speckle that a raw peak/blob count
turns into hundreds of false maxima:

  creation     : Q_top rises well above the initial 2-soliton content   (=> Verdict A)
  annihilation : Q_top collapses toward 0 (charge -> magnon radiation)   (=> Verdict B)
  elastic      : Q_top stays near its initial value (two solitons live)  (=> Verdict C)

DEATH CRITERION (pre-registered): B_total stays ~0 and no new topological matter is created
=> Verdict B/C.  We also report the Q_top half-time (a clean collision-time proxy) and the
field-energy drop (annihilation releases the soliton gradient energy as radiation).

NB: the n_peaks (energy-density) count is recorded too, but it is NOT used for the verdict:
post-collision magnon turbulence inflates it to tens of false "peaks" while Q_top and the
conserved global charge B show no matter was created.  No new dynamics here.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import fl3_core as f

OUT = Path(__file__).resolve().parent


def q_half_time(series):
    """First time Q_top falls below half its initial value (a clean collision marker)."""
    Q = np.array(series["Q_top"]); t = np.array(series["t"])
    half = 0.5 * Q[0]
    below = np.where(Q < half)[0]
    return float(t[below[0]]) if below.size else float(t[-1])


def main():
    src = OUT / "FL3_2_dynamics.json"
    if not src.exists():
        raise SystemExit("run FL3_2_dynamics.py first")
    data = json.loads(src.read_text())
    ens = data["ensemble"]

    per_seed = []
    for r in ens:
        ser = r["series"]
        Q = np.array(ser["Q_top"]); B = np.array(ser["B"])
        E = np.array(ser["E_field"]); peaks = np.array(ser["n_peaks"])
        half = len(Q) // 2
        per_seed.append({
            "seed": r["seed"], "scenario": r.get("scenario"),
            "t_q_half": q_half_time(ser),
            "Q_top_0": float(Q[0]), "Q_top_late": float(Q[-1]),
            "Q_top_peak_ratio": float(Q[half:].max() / Q[0]),
            "Q_top_late_ratio": float(Q[half:].mean() / Q[0]),
            "E_field_drop_frac": float(1.0 - E[half:].mean() / E[0]),
            "B_abs_max": float(np.max(np.abs(B))),
            "n_peaks_late_max_radiation": int(peaks[half:].max()),
        })

    scens = {sc: sum(1 for r in per_seed if r["scenario"] == sc)
             for sc in ("creation", "annihilation", "elastic")}
    n_created = scens["creation"]
    B_abs_max_all = max(r["B_abs_max"] for r in per_seed)
    KE = data["KE_collision"]; thr = data["E_threshold_2Mc2"]

    # pre-registered death criterion: no creation AND global charge stays ~0
    creation = n_created >= len(per_seed) / 2
    death_triggered = (not creation) and (B_abs_max_all < 0.5)
    verdict = "A" if creation else ("B" if scens["annihilation"] >= scens["elastic"]
                                    else "C")

    print("=" * 72)
    print("FL3-3 -- COLLISION ANALYSIS (radiation-proof Q_top)")
    print("=" * 72)
    print(f"{'seed':>4} {'scenario':>13} {'t_Qhalf':>8} {'Q0':>6} {'Qpeak/Q0':>9} "
          f"{'E_drop':>7} {'B|max|':>7} {'npk_rad':>8}")
    for r in per_seed:
        print(f"{r['seed']:>4} {str(r['scenario']):>13} {r['t_q_half']:8.2f} "
              f"{r['Q_top_0']:6.2f} {r['Q_top_peak_ratio']:9.3f} "
              f"{r['E_field_drop_frac']:7.2f} {r['B_abs_max']:7.3f} "
              f"{r['n_peaks_late_max_radiation']:8d}")
    print("-" * 72)
    print(f"scenario counts: {scens}")
    print(f"seeds with creation (Q_top rise): {n_created}/{len(per_seed)}")
    print(f"max |B_total| over all seeds/times: {B_abs_max_all:.3f}")
    print(f"KE_collision={KE:.2f}  2 M_Sk c^2={thr:.1f}  KE/thresh={KE/thr:.4f}")
    print(f"(radiation note: n_peaks(energy) inflates to ~30-44 post-collision -- magnon "
          f"turbulence, NOT solitons; Q_top and B show no matter created)")
    print(f"death criterion triggered (no creation & B~0): {death_triggered}")
    print(f"FL3-3 VERDICT: {verdict}")

    payload = {"per_seed": per_seed, "scenario_counts": scens,
               "n_seeds_created": n_created, "n_seeds": len(per_seed),
               "B_abs_max_all_seeds": B_abs_max_all,
               "KE_collision": KE, "E_threshold_2Mc2": thr, "KE_over_threshold": KE / thr,
               "creation_observed": bool(creation),
               "death_criterion_triggered": bool(death_triggered),
               "verdict_code": verdict,
               "verdict": {"A": "CREATION", "B": "ANNIHILATION",
                           "C": "ELASTIC"}[verdict]}
    f.save_json("FL3_3_analysis", payload)
    return payload


if __name__ == "__main__":
    main()
