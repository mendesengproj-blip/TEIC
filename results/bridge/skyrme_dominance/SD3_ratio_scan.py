"""SD3 -- does K/S grow with any network parameter (d, rho, link type)?

Pre-registered (SKYRME_DOMINANCE.md addendum, items 2, 3, 5, 9):

  (a) mean cross-channel fraction of an isotropic link direction:
      <kappa>(d) = 1 - 3/(d+2): d=1 -> 0 (no commutator channel), d=2 -> 1/4,
      d=3 -> 2/5, d=4 -> 1/2, d=5 -> 4/7, d->inf -> 1. GROWS with d, but
  (b) the field bound K <= (1-1/d) S and the net-quartic gap
      3S-2K >= (1+2/d) S > 0 close in step: no d reaches dominance;
  (c) density: Poisson isotropy is exact at every rho (spatial directions of
      causal links in a diamond are uniform on S^2 by symmetry). Prediction:
      kappa(rho) = const = 2/5 within noise ~ N_links^{-1/2}; the SC2-style
      residual ratio r4(B)/r4(A) on MEASURED link directions = 5/9 at every
      rho. The 4-component fraction of causal links deviates from the
      isotropic 1/2 (timelike component dominates near the diagonal);
  (d) link type: spacelike (unrelated) pairs have a different time/space
      split but their SPATIAL direction statistics are also isotropic ->
      same 2/5, same 5/9.

  DEATH CRITERION (charter, SUCESSO PARCIAL): some regime with field
  K/S > 2/3. SD1 proved that pointwise-impossible in d=3; here the scan
  verifies no measured regime even approaches the per-link proxy bound.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sd_core as sd

RHOS = [10, 50, 200, 1000]
N_SEEDS = 20
DIMS = list(range(1, 9))


def dimension_scan(rng, n=400_000):
    out = {}
    for d in DIMS:
        dirs = sd.unit_directions(n, d, rng)
        kap = sd.cross_channel_fraction(dirs)
        out[d] = {"kappa_mean": float(np.mean(kap)),
                  "kappa_sem": float(np.std(kap) / np.sqrt(n)),
                  "predicted": 1.0 - 3.0 / (d + 2),
                  "field_bound_K_over_S": 1.0 - 1.0 / max(d, 1),
                  "net_quartic_gap_factor": 1.0 + 2.0 / d}
    return out


def density_scan():
    rows = {}
    for rho in RHOS:
        kap3, kap4, ratio59, kap3_sp = [], [], [], []
        n_links_all = []
        for seed in range(N_SEEDS):
            rng = np.random.default_rng(7000 + 100 * rho + seed)
            t, x = sd.sprinkle_diamond(rho, rng)
            links = sd.causal_links(t, x)
            if len(links) == 0:
                continue
            i, j = links[:, 0], links[:, 1]
            dx = x[j] - x[i]
            dt = (t[j] - t[i])[:, None]
            # spatial unit directions of causal links (skip dx ~ 0)
            r = np.linalg.norm(dx, axis=1)
            ok = r > 1e-12
            e3 = dx[ok] / r[ok, None]
            kap3.append(float(np.mean(sd.cross_channel_fraction(e3))))
            # 4-component (Euclidean-normalised) direction fractions
            v4 = np.concatenate([dt, dx], axis=1)
            e4 = v4 / np.linalg.norm(v4, axis=1, keepdims=True)
            kap4.append(float(np.mean(sd.cross_channel_fraction(e4))))
            # SC2-style residual ratio on the MEASURED spatial directions
            g = 0.05
            rA = sd.sc.quartic_residual(sd.sc.config_A(g), e3, 1.0)
            rB = sd.sc.quartic_residual(sd.sc.config_B(g), e3, 1.0)
            ratio59.append(rB / rA)
            n_links_all.append(int(len(links)))
            # spacelike (unrelated) pairs: sample up to the same count
            n_el = len(t)
            ii = rng.integers(0, n_el, size=4 * len(links))
            jj = rng.integers(0, n_el, size=4 * len(links))
            dxs = x[jj] - x[ii]
            dts = t[jj] - t[ii]
            r2 = np.sum(dxs ** 2, axis=1)
            sp_mask = (dts ** 2 < r2) & (r2 > 1e-24)
            if np.any(sp_mask):
                es = dxs[sp_mask] / np.sqrt(r2[sp_mask])[:, None]
                kap3_sp.append(float(np.mean(sd.cross_channel_fraction(es))))
        rows[rho] = {
            "n_links_mean": float(np.mean(n_links_all)),
            "kappa3_causal": sd.seed_stats(kap3),
            "kappa3_spacelike": sd.seed_stats(kap3_sp),
            "kappa4_causal": sd.seed_stats(kap4),
            "ratio_B_over_A": sd.seed_stats(ratio59),
            "predicted": {"kappa3": 0.4, "kappa4_isotropic_ref": 0.5,
                          "ratio": 5.0 / 9.0},
        }
    return rows


def main():
    rng = np.random.default_rng(20260612)
    dscan = dimension_scan(rng)
    rscan = density_scan()

    # verdicts against pre-registration
    kappa_ok = all(abs(dscan[d]["kappa_mean"] - dscan[d]["predicted"]) <
                   5 * dscan[d]["kappa_sem"] + 1e-3 for d in DIMS)
    rho_const = all(abs(rscan[r]["kappa3_causal"]["mean"] - 0.4) <
                    5 * rscan[r]["kappa3_causal"]["sem"] + 5e-3 for r in RHOS)
    ratio_ok = all(abs(rscan[r]["ratio_B_over_A"]["mean"] - 5.0 / 9.0) <
                   5 * rscan[r]["ratio_B_over_A"]["sem"] + 5e-3 for r in RHOS)
    any_dominance = any(rscan[r]["kappa3_causal"]["mean"] > 2.0 / 3.0
                        for r in RHOS)

    payload = {
        "dimension_scan": {str(d): dscan[d] for d in DIMS},
        "density_scan": {str(r): rscan[r] for r in RHOS},
        "verdict": {
            "kappa_d_formula_confirmed": bool(kappa_ok),
            "kappa_rho_constant_2_5": bool(rho_const),
            "residual_ratio_5_9_all_rho": bool(ratio_ok),
            "any_regime_above_2_3": bool(any_dominance),
            "note": ("kappa grows with d but the field bound (1-1/d) and the "
                     "net gap (1+2/d)S grow/shrink in step: no dimension and "
                     "no density reaches dominance; rho does not move the "
                     "ratio at all (isotropy is exact at every rho)."),
        },
    }
    sd.save_json("SD3_ratio_scan.json", payload)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
    ds = np.array(DIMS, dtype=float)
    ax1.plot(ds, [dscan[d]["kappa_mean"] for d in DIMS], "o", color="tab:blue",
             label=r"measured $\langle\kappa\rangle$")
    dd = np.linspace(1, 8, 200)
    ax1.plot(dd, 1 - 3 / (dd + 2), "-", color="tab:blue", lw=1,
             label=r"$1-3/(d+2)$ (link fraction)")
    ax1.plot(dd, 1 - 1 / dd, "--", color="tab:red",
             label=r"$1-1/d$ (field bound, saturable)")
    ax1.axhline(1.0, color="k", lw=0.8, ls=":")
    ax1.text(6.5, 1.01, "dominance", fontsize=8)
    ax1.set_xlabel("spatial dimension d")
    ax1.set_ylabel("ratio")
    ax1.set_ylim(0, 1.1)
    ax1.set_title("both ratios grow with d; neither reaches 1")
    ax1.legend(fontsize=8)

    rs = np.array(RHOS, dtype=float)
    m3 = [rscan[r]["kappa3_causal"]["mean"] for r in RHOS]
    s3 = [rscan[r]["kappa3_causal"]["sem"] for r in RHOS]
    msp = [rscan[r]["kappa3_spacelike"]["mean"] for r in RHOS]
    m59 = [rscan[r]["ratio_B_over_A"]["mean"] for r in RHOS]
    s59 = [rscan[r]["ratio_B_over_A"]["sem"] for r in RHOS]
    ax2.errorbar(rs, m3, yerr=s3, fmt="o-", color="tab:blue",
                 label=r"$\kappa_3$ causal links")
    ax2.plot(rs, msp, "s--", color="tab:cyan", label=r"$\kappa_3$ spacelike pairs")
    ax2.errorbar(rs, m59, yerr=s59, fmt="^-", color="tab:green",
                 label=r"$r_4(B)/r_4(A)$ measured dirs")
    ax2.axhline(0.4, color="tab:blue", ls=":", lw=1)
    ax2.axhline(5 / 9, color="tab:green", ls=":", lw=1)
    ax2.axhline(2 / 3, color="tab:red", ls="--", lw=1, label="2/3 dominance bound")
    ax2.set_xscale("log")
    ax2.set_xlabel(r"density $\rho$")
    ax2.set_title("density moves nothing (Poisson isotropy exact)")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SD3_ratio_scan.png", dpi=150)

    print(json.dumps(payload["verdict"], indent=2))
    print(json.dumps({str(r): {"kappa3": rscan[r]["kappa3_causal"]["mean"],
                               "kappa4": rscan[r]["kappa4_causal"]["mean"],
                               "ratio": rscan[r]["ratio_B_over_A"]["mean"],
                               "n_links": rscan[r]["n_links_mean"]}
                      for r in RHOS}, indent=2))


if __name__ == "__main__":
    main()
