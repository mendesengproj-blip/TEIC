"""CR3 -- the pure constant of the DBI scale X0: extreme-value statistics of
the minimum capped link.

Pre-registered (CROSS_RELATIONS_II.md). X0 = (Dtheta_max/Dtau_min)^2 (C3).
Exact prediction, zero parameters: u = rho * V_cap(Dtau_min, H) is Exp(1)
for every bulk event (Poisson void probability), hence median(u) = ln 2 and,
at leading order, X0 * Dtheta_max^{-2} = 1/Dtau_med^2 = pi rho H^2 / ln 2
(pure constant pi/ln2 ~ 4.532). The exponent is UV (X0 ~ rho, C3 unchanged);
the CONSTANT carries the declared IR regulator H^2 (the sliver hugging the
cone is non-compact; H is frame-dependent and declared -- same status as the
box regulator in LV3).

KILL CRITERIA (pre-registered, from CROSS_RELATIONS_II.md):
  - KS distance between empirical u and Exp(1) > 0.05 at BOTH highest rho; OR
  - median(u)/ln2 outside [0.85, 1.15] at both highest rho; OR
  - exponent q of Dtau_med ~ rho^q with |q + 1/2| > 3 sigma.
Declared caveats: u_i of nearby events weakly correlated (overlapping cones)
-> KS DISTANCE is the criterion, not its p-value; truncation fraction
exp(-rho (pi/3) H^4) must stay < ~1% (rho*(pi/3)H^4 >= 5, satisfied by design).
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
LN2 = float(np.log(2.0))
PURE_CONST_PRED = float(np.pi / np.log(2.0))   # pi/ln2 ~ 4.5324


def ks_distance_exp1(u):
    """KS distance between sorted sample u and Exp(1) CDF (distance, not p)."""
    u = np.sort(np.asarray(u))
    n = len(u)
    cdf = 1.0 - np.exp(-u)
    ecdf_hi = np.arange(1, n + 1) / n
    ecdf_lo = np.arange(0, n) / n
    return float(max(np.max(ecdf_hi - cdf), np.max(cdf - ecdf_lo)))


def main():
    rows = []
    per_seed_medians = np.zeros((core.N_SEEDS, len(core.RHOS)))
    pooled_u = {}
    for k, rho in enumerate(core.RHOS):
        u_all, taus_all, n_trunc, n_tot = [], [], 0, 0
        for s in range(core.N_SEEDS):
            pts, bounds = core.sprinkling(k, s)
            taus, trunc = core.min_dtau_capped(pts, bounds)
            n_trunc += trunc
            n_tot += len(taus) + trunc
            u_all.append(rho * core.V_cap(taus, core.H_CAP))
            taus_all.append(taus)
            per_seed_medians[s, k] = float(np.median(taus))
        u = np.concatenate(u_all)
        taus = np.concatenate(taus_all)
        tau_med = float(np.median(taus))
        rows.append({
            "rho": rho,
            "n_bulk_events": int(n_tot),
            "trunc_fraction": n_trunc / max(n_tot, 1),
            "trunc_expected": float(np.exp(-rho * (np.pi / 3) * core.H_CAP ** 4)),
            "ks_distance_exp1": ks_distance_exp1(u),
            "median_u_over_ln2": float(np.median(u)) / LN2,
            "tau_med_pooled": tau_med,
            "pure_const_leading": 1.0 / (tau_med ** 2 * rho * core.H_CAP ** 2 * (1.0 / LN2)),
            "exact_median_check_rhoV_over_ln2":
                float(rho * core.V_cap(tau_med, core.H_CAP) / LN2),
        })
        pooled_u[rho] = u
        print(f"rho={rho:5.0f}  KS={rows[-1]['ks_distance_exp1']:.4f}  "
              f"med(u)/ln2={rows[-1]['median_u_over_ln2']:.4f}  "
              f"trunc={rows[-1]['trunc_fraction']:.4%} "
              f"(exp {rows[-1]['trunc_expected']:.4%})", flush=True)

    # exponent: per-seed log-log fit of median Dtau vs rho -> mean +/- sem
    lr = np.log(np.asarray(core.RHOS))
    qs = [np.polyfit(lr, np.log(per_seed_medians[s]), 1)[0]
          for s in range(core.N_SEEDS)]
    q_mean = float(np.mean(qs))
    q_sem = float(np.std(qs, ddof=1) / np.sqrt(len(qs)))

    two_highest = rows[-2:]
    death_ks = all(r["ks_distance_exp1"] > 0.05 for r in two_highest)
    death_med = all(not (0.85 <= r["median_u_over_ln2"] <= 1.15) for r in two_highest)
    death_exp = abs(q_mean + 0.5) > 3.0 * q_sem
    death = death_ks or death_med or death_exp

    payload = {
        "rows": rows,
        "exponent_q": {"measured": q_mean, "sem": q_sem, "predicted": -0.5,
                       "per_seed": [float(q) for q in qs]},
        "pure_constant": {"predicted_pi_over_ln2": PURE_CONST_PRED,
                          "note": "X0*Dtheta_max^-2 = pi rho H^2/ln2 (leading); "
                                  "exact check is rho*V(tau_med,H)/ln2 = 1"},
        "death": {"any": bool(death), "ks": bool(death_ks),
                  "median": bool(death_med), "exponent": bool(death_exp)},
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__, "n_seeds": core.N_SEEDS,
                  "H": core.H_CAP, "extent": core.EXTENT,
                  "margin_frac": core.MARGIN_FRAC, "seed_base": core.SEED_BASE},
    }
    (HERE / "CR3_x0_constant_data.json").write_text(json.dumps(payload, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    grid = np.linspace(0, 6, 300)
    for rho, u in pooled_u.items():
        uu = np.sort(u)
        ax1.plot(uu, np.arange(1, len(uu) + 1) / len(uu), lw=1.2,
                 label=rf"$\rho={rho:.0f}$ (KS {ks_distance_exp1(u):.3f})")
    ax1.plot(grid, 1 - np.exp(-grid), "k--", lw=1.5, label="Exp(1)")
    ax1.set_xlim(0, 6); ax1.set_xlabel(r"$u=\rho V(\Delta\tau_{\min},H)$")
    ax1.set_ylabel("CDF"); ax1.legend(fontsize=8)
    ax1.set_title("CR3: distributional collapse to Exp(1)")

    med = per_seed_medians.mean(axis=0)
    sem = per_seed_medians.std(axis=0, ddof=1) / np.sqrt(core.N_SEEDS)
    ax2.errorbar(core.RHOS, med, yerr=sem, fmt="o", color="tab:blue",
                 label=rf"measured (slope ${q_mean:.3f}\pm{q_sem:.3f}$)")
    rr = np.array(core.RHOS, float)
    ax2.plot(rr, np.sqrt(LN2 / (np.pi * core.H_CAP ** 2)) * rr ** -0.5, "k:",
             label=r"$\sqrt{\ln 2/\pi H^2}\,\rho^{-1/2}$ (zero params)")
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel(r"$\rho$"); ax2.set_ylabel(r"median $\Delta\tau_{\min}$")
    ax2.set_title(f"slope {q_mean:.3f} (pred −1/2)"); ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "CR3_x0_constant.png", dpi=150)

    print(json.dumps({"exponent_q": payload["exponent_q"]["measured"],
                      "sem": q_sem, "death": payload["death"]}, indent=2))


if __name__ == "__main__":
    main()
