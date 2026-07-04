"""CR4 -- the pure constant of the vector mass m_A on the causal substrate:
does the PE3 heritage (m_A ~ sqrt(rho)) survive?

Pre-registered (CROSS_RELATIONS_II.md). On the SAME sprinklings as CR3
(crii_core seed formula): links = covering relations (C1 protocol),
plaquettes = minimal causal diamonds (W2 protocol), both bulk-filtered.

  C2^{mu nu} = (1/2 V_in) sum_links dtau e^mu e^nu     (C2_t = C2^00, C2_x = mean C2^ii)
  Pi_E = (1/V_in) sum_plaq sum_i (Om^{0i})^2 ;  Pi_B with spatial pairs
  m2_E = 4 C2_x/(lam_p Pi_E/3) ; m2_B = 4 C2_x/(lam_p Pi_B/3)
  m2_iso = 4 (C2_t + 3 C2_x)/(lam_p (Pi_E + Pi_B))          [lam_p = 1 declared]

O(1) convention factors declared; the recorded content is (a) the exponent,
(b) the constancy of the pure number across the sweep, (c) the E/B split
(cross-referenced to LIV_VECTOR: regulator artifact, reported not hidden).

REGISTERED HYPOTHESIS: natural causal units have one scale rho^{1/4}, so the
honest translation of PE3 (3D proxy, m_A ~ sqrt(rho_3D)) is s_m = +1/2 in
m2_iso * lam_p ~ rho^{s_m}. Pure-number candidate P = m2_iso * lam_p * rho^{-1/2}
(first measurement, no predicted value -- reported like CR1b's b).

KILL CRITERIA (pre-registered, from CROSS_RELATIONS_II.md):
  - heritage dies if |s_m - 0.5| > 3 sigma of the fit -> report as death of
    the inherited entry; record the measured exponent + its pure constant.
  - table entry closes ONLY if some m2 * lam_p * rho^{-s} (s measured) is
    constant across the sweep with CV < 20%; otherwise verdict "not constant".
  - regulator check: one density (rho=45) re-measured in the smaller box
    (E=2.56); |m2_small/m2_main - 1| > 0.2 -> report as IR-regulated (same
    status as CR3's H^2), not hidden.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import crii_core as core

HERE = Path(__file__).resolve().parent
LAMBDA_P = 1.0   # declared (free weight, = the DEV's free K -- W4)
S_REGISTERED = 0.5


def measure(pts, bounds):
    C2, n_links = core.link_second_moment(pts, bounds)
    pe, pb, n_plaq = core.plaquette_moments(pts, bounds)
    c2_t = float(C2[0, 0])
    c2_x = float(np.mean([C2[1, 1], C2[2, 2], C2[3, 3]]))
    m2_E = 4.0 * c2_x / (LAMBDA_P * pe / 3.0) if pe > 0 else np.nan
    m2_B = 4.0 * c2_x / (LAMBDA_P * pb / 3.0) if pb > 0 else np.nan
    m2_iso = 4.0 * (c2_t + 3.0 * c2_x) / (LAMBDA_P * (pe + pb)) if pe + pb > 0 else np.nan
    return {"C2_t": c2_t, "C2_x": c2_x, "Pi_E": pe, "Pi_B": pb,
            "n_links_bulk": n_links, "n_plaq_bulk": n_plaq,
            "m2_E": m2_E, "m2_B": m2_B, "m2_iso": m2_iso,
            "EB_split_PiE_over_PiB": pe / pb if pb > 0 else np.nan}


def stats(vals):
    v = np.asarray(vals, float)
    return {"mean": float(np.mean(v)),
            "sem": float(np.std(v, ddof=1) / np.sqrt(len(v)))}


def main():
    rows = []
    m2_iso_seed = np.zeros((core.N_SEEDS, len(core.RHOS)))
    m2_E_seed = np.zeros_like(m2_iso_seed)
    m2_B_seed = np.zeros_like(m2_iso_seed)
    for k, rho in enumerate(core.RHOS):
        per_seed = []
        for s in range(core.N_SEEDS):
            pts, bounds = core.sprinkling(k, s)
            r = measure(pts, bounds)
            per_seed.append(r)
            m2_iso_seed[s, k] = r["m2_iso"]
            m2_E_seed[s, k] = r["m2_E"]
            m2_B_seed[s, k] = r["m2_B"]
            print(f"rho={rho:5.0f} seed={s}  N={len(pts):5d}  "
                  f"links={r['n_links_bulk']:6d} plaq={r['n_plaq_bulk']:5d}  "
                  f"m2_iso={r['m2_iso']:.4g}  E/B={r['EB_split_PiE_over_PiB']:.3f}",
                  flush=True)
        rows.append({"rho": rho,
                     "m2_iso": stats([r["m2_iso"] for r in per_seed]),
                     "m2_E": stats([r["m2_E"] for r in per_seed]),
                     "m2_B": stats([r["m2_B"] for r in per_seed]),
                     "EB_split": stats([r["EB_split_PiE_over_PiB"] for r in per_seed]),
                     "C2_t": stats([r["C2_t"] for r in per_seed]),
                     "C2_x": stats([r["C2_x"] for r in per_seed]),
                     "Pi_E": stats([r["Pi_E"] for r in per_seed]),
                     "Pi_B": stats([r["Pi_B"] for r in per_seed])})

    # exponent: per-seed log-log fit of m2_iso vs rho
    lr = np.log(np.asarray(core.RHOS))
    s_fits = [np.polyfit(lr, np.log(m2_iso_seed[s]), 1)[0]
              for s in range(core.N_SEEDS)]
    s_mean = float(np.mean(s_fits))
    s_sem = float(np.std(s_fits, ddof=1) / np.sqrt(len(s_fits)))
    heritage_dead = abs(s_mean - S_REGISTERED) > 3.0 * s_sem

    # pure-number constancy across the sweep (CV), registered s and measured s
    def cv_pure(m2_seed, s_exp):
        p = m2_seed.mean(axis=0) * np.asarray(core.RHOS) ** (-s_exp)
        return {"values": [float(x) for x in p],
                "mean": float(np.mean(p)),
                "cv": float(np.std(p, ddof=1) / np.mean(p))}

    pure = {
        "iso_s_registered_0.5": cv_pure(m2_iso_seed, S_REGISTERED),
        "iso_s_measured": cv_pure(m2_iso_seed, s_mean),
        "E_s_measured": cv_pure(m2_E_seed, s_mean),
        "B_s_measured": cv_pure(m2_B_seed, s_mean),
    }
    table_closes = pure["iso_s_measured"]["cv"] < 0.20

    # regulator check: rho=45 in the smaller box, same seeds
    k45 = core.RHOS.index(45.0)
    chk = []
    for s in range(core.N_SEEDS):
        pts, bounds = core.sprinkling(k45, s, extent=core.EXTENT_CHK,
                                      seed_base=core.SEED_BASE_CHK)
        chk.append(measure(pts, bounds)["m2_iso"])
    chk_stats = stats(chk)
    ratio_box = chk_stats["mean"] / rows[k45]["m2_iso"]["mean"]
    ir_regulated = abs(ratio_box - 1.0) > 0.20

    payload = {
        "rows": rows,
        "exponent_s": {"measured": s_mean, "sem": s_sem,
                       "registered_PE3_heritage": S_REGISTERED,
                       "per_seed": [float(x) for x in s_fits],
                       "heritage_dead": bool(heritage_dead)},
        "pure_numbers": pure,
        "table_closes_cv_lt_20pct": bool(table_closes),
        "box_check": {"rho": 45.0, "extent_small": core.EXTENT_CHK,
                      "m2_iso_small": chk_stats,
                      "m2_iso_main": rows[k45]["m2_iso"],
                      "ratio_small_over_main": float(ratio_box),
                      "ir_regulated": bool(ir_regulated)},
        "lambda_p_declared": LAMBDA_P,
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__, "n_seeds": core.N_SEEDS,
                  "extent": core.EXTENT, "margin_frac": core.MARGIN_FRAC,
                  "seed_base": core.SEED_BASE},
    }
    (HERE / "CR4_ma_constant_data.json").write_text(json.dumps(payload, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    rr = np.asarray(core.RHOS)
    for arr, lab, c in [(m2_iso_seed, "iso", "tab:blue"),
                        (m2_E_seed, "E", "tab:red"),
                        (m2_B_seed, "B", "tab:green")]:
        m = arr.mean(axis=0)
        e = arr.std(axis=0, ddof=1) / np.sqrt(core.N_SEEDS)
        ax1.errorbar(rr, m, yerr=e, fmt="o-", color=c, ms=4, label=f"$m^2_{{{lab}}}$")
    ax1.plot(rr, m2_iso_seed.mean(axis=0)[0] * (rr / rr[0]) ** 0.5, "k:",
             label=r"$\rho^{+1/2}$ (PE3 heritage)")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel(r"$\rho$"); ax1.set_ylabel(r"$m^2\,\lambda_p$")
    ax1.set_title(f"CR4: slope {s_mean:.3f} ± {s_sem:.3f} (registered +0.5)")
    ax1.legend(fontsize=8)

    p = pure["iso_s_measured"]["values"]
    ax2.plot(rr, p, "o-", color="tab:blue",
             label=rf"$m^2_{{iso}}\rho^{{-{s_mean:.2f}}}$ (CV {pure['iso_s_measured']['cv']:.1%})")
    p05 = pure["iso_s_registered_0.5"]["values"]
    ax2.plot(rr, p05, "s--", color="tab:orange",
             label=rf"$m^2_{{iso}}\rho^{{-0.5}}$ (CV {pure['iso_s_registered_0.5']['cv']:.1%})")
    ax2.set_xscale("log")
    ax2.set_xlabel(r"$\rho$"); ax2.set_ylabel("pure number")
    ax2.set_title("constancy of the pure number"); ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "CR4_ma_constant.png", dpi=150)

    print(json.dumps({"exponent_s": s_mean, "sem": s_sem,
                      "heritage_dead": bool(heritage_dead),
                      "cv_measured_s": pure["iso_s_measured"]["cv"],
                      "box_ratio": float(ratio_box),
                      "ir_regulated": bool(ir_regulated)}, indent=2))


if __name__ == "__main__":
    main()
