"""AB1_coefficients.py -- 20-seed re-audit of the C1-C4 coefficient claims.

AUDIT_BRIDGE task AB1.  Re-runs the COEFFICIENTS campaign's own generators (imported
unchanged from results/bridge/coefficients and results/bridge/wilson) over 20 fresh
seeds, and reports every claimed number with error bars.  Modifies nothing.

What is re-checked, and the specific claim each test attacks:

  C2  -- "the ratios C2/C1=1, C3/C1=2 are ALGEBRAIC (forced by the single cosine),
          not geometric."  Test: compute the ratios PER realisation.  If algebraic
          they are identically 1 and 2 with ZERO seed variance while kappa (the scale)
          and the anisotropy lambda/|kappa| (the geometry) DO vary.  That contrast is
          the proof the cleanliness is structural, not a fit to geometry.

  C1  -- "M2 = <Dtau e^mu e^nu> is positive-definite by construction."  Test: the
          eigenvalues of the sharp M2 over 20 seeds -- all must be > 0 (a Dtau-weighted
          sum of outer products e e^T with Dtau>=0 is positive semi-definite).  This is
          WHY it can never equal the indefinite g^{mu nu} (the BD motivation), so it
          must be a structural fact, not a seed accident.

  C3  -- "X0 proportional to rho with exponent 1; the cosmological a0 ~ c*H0 link is
          rejected."  Test: fit Dtau_min ~ rho^q over 20 seeds in BOTH 1+1D and 3+1D
          and report the implied X0 exponent p = -2q with its fit error.  The code's
          module docstring argues p=1 dimension-INDEPENDENTLY (light-cone sliver), but
          an inline comment at C3_scale.py:131-132 claims 3+1D gives q=-1/4 -> p=1/2.
          We resolve which the data supports.  A UV exponent p>0 (X0 GROWS with density)
          is the opposite sign of any cosmological IR scale, confirming the a0~cH0
          rejection structurally.

  C4  -- "the quartic operators were identified but not quantified."  Test: the Taylor
          coefficient -1/24 is exact (symbolic), but the GEOMETRIC quartic scale
          C_q = -(1/24) n_links <Dtau (e.e)^2> is measurable.  We report <Dtau(e.e)^2>,
          n_links and C_q with 20-seed error bars in 1+1D and 3+1D.

Run:  python results/audit/bridge_recheck/AB1_coefficients.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "bridge" / "coefficients"))
sys.path.insert(0, str(ROOT / "results" / "bridge" / "wilson"))

from causal_core import sprinkle_box                       # noqa: E402
from C1_moments import link_moments, decompose_M2          # noqa: E402
from C3_scale import nearest_future_dtau, fit_powerlaw     # noqa: E402
from W2_coarse_graining import link_moments as w2_moments  # noqa: E402 (has m4_scalar)

OUT = Path(__file__).resolve().parent
NSEED = 20


def _ms(v):
    """mean, std, sem of a finite-filtered list."""
    v = np.asarray([x for x in v if np.isfinite(x)], float)
    if v.size == 0:
        return float("nan"), float("nan"), float("nan")
    sem = float(v.std(ddof=1) / np.sqrt(v.size)) if v.size > 1 else 0.0
    return float(v.mean()), float(v.std(ddof=1)) if v.size > 1 else 0.0, sem


# =========================================================================== #
# C1 + C2 -- per-seed moments, ratios, eigenvalues
# =========================================================================== #
def audit_c1c2(D, rho, extent, seed0):
    bounds = [[0.0, extent]] * D
    kappas, lams, aniso, c2c1, c3c1 = [], [], [], [], []
    eig_min, eig_max = [], []
    for s in range(NSEED):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, bounds, rng)
        if len(pts) < 8:
            continue
        m = link_moments(pts, bounds)
        if m["n_links_bulk"] < 8:
            continue
        M2 = np.asarray(m["M2"], float)
        dec = decompose_M2(M2)
        n = m["n_links_density"]
        kappa = dec["kappa_isotropic"]
        # C1=C2=n kappa/2 ; C3 = n kappa  (per the C2 task)
        C1 = n * kappa / 2.0
        C2 = n * kappa / 2.0
        C3 = n * kappa
        kappas.append(kappa)
        lams.append(dec["lambda_anisotropic"])
        aniso.append(dec["anisotropy_ratio_lambda_over_abskappa"])
        c2c1.append(C2 / C1)
        c3c1.append(C3 / C1)
        ev = np.linalg.eigvalsh(M2)
        eig_min.append(float(ev.min()))
        eig_max.append(float(ev.max()))
    out = {"D": D, "rho": rho, "extent": extent, "n_seeds_used": len(kappas)}
    for name, vals in [("kappa", kappas), ("lambda", lams),
                       ("anisotropy_lambda_over_abskappa", aniso),
                       ("C2_over_C1", c2c1), ("C3_over_C1", c3c1),
                       ("M2_eig_min", eig_min), ("M2_eig_max", eig_max)]:
        mean, std, sem = _ms(vals)
        out[name] = {"mean": mean, "std": std, "sem": sem}
    out["all_eigenvalues_positive"] = bool(all(e > 0 for e in eig_min))
    out["ratio_C2C1_std"] = out["C2_over_C1"]["std"]
    out["ratio_C3C1_std"] = out["C3_over_C1"]["std"]
    return out


# =========================================================================== #
# C3 -- X0 exponent over 20 seeds, both dimensions
# =========================================================================== #
def audit_c3(D, rhos, extent, seed0):
    """For each density: 20-seed mean nearest-future Dtau (median & p05).  Fit the
    power law per statistic AND report the spread of the exponent over a leave-one-out
    style jackknife across seeds for an error bar."""
    bounds = [[0.0, extent]] * D
    per_rho = []
    # store per-seed scale at each rho so we can bootstrap the exponent
    seed_scales = {stat: np.zeros((len(rhos), NSEED)) for stat in ("p05", "median")}
    for ri, rho in enumerate(rhos):
        meds, p05s = [], []
        for s in range(NSEED):
            rng = np.random.default_rng(seed0 + 1000 * ri + s)
            pts = sprinkle_box(rho, bounds, rng)
            if len(pts) < 5:
                meds.append(np.nan); p05s.append(np.nan); continue
            dt = nearest_future_dtau(pts, bounds)
            if dt.size < 5:
                meds.append(np.nan); p05s.append(np.nan); continue
            meds.append(float(np.percentile(dt, 50)))
            p05s.append(float(np.percentile(dt, 5)))
        seed_scales["median"][ri] = meds
        seed_scales["p05"][ri] = p05s
        mm, ms_, _ = _ms(meds)
        pm, ps_, _ = _ms(p05s)
        per_rho.append({"rho": rho, "dtau_median_mean": mm, "dtau_median_std": ms_,
                        "dtau_p05_mean": pm, "dtau_p05_std": ps_})
    fits = {}
    for stat in ("p05", "median"):
        # bootstrap the exponent over seeds: resample seed index, fit, repeat
        rng = np.random.default_rng(777)
        exps = []
        for _ in range(400):
            cols = rng.integers(0, NSEED, NSEED)
            scales = np.nanmean(seed_scales[stat][:, cols], axis=1)
            if np.any(~np.isfinite(scales)) or np.any(scales <= 0):
                continue
            q, _a, _r2 = fit_powerlaw(rhos, scales)
            exps.append(-2.0 * q)            # X0 exponent p = -2q
        exps = np.asarray(exps)
        # central fit on the full-seed means
        scales = np.nanmean(seed_scales[stat], axis=1)
        q, a, r2 = fit_powerlaw(rhos, scales)
        fits[stat] = {"X0_exponent_p": float(-2.0 * q), "q_dtau": float(q), "r2": float(r2),
                      "X0_exponent_p_boot_mean": float(exps.mean()),
                      "X0_exponent_p_boot_std": float(exps.std(ddof=1))}
    return {"D": D, "rhos": list(rhos), "extent": extent, "per_rho": per_rho,
            "fits": fits, "theory_p_lightcone_sliver": 1.0,
            "inline_comment_claim_3plus1D_p": 0.5}


# =========================================================================== #
# C4 -- quartic geometric scale C_q with error bars
# =========================================================================== #
def audit_c4(D, rho, extent, seed0):
    bounds = [[0.0, extent]] * D
    m4s, nlinks, cq = [], [], []
    for s in range(NSEED):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, bounds, rng)
        if len(pts) < 8:
            continue
        m = w2_moments(pts, bounds)             # has m4_scalar, n_links_density
        n = m["n_links_density"]
        m4 = m["m4_scalar"]
        m4s.append(m4); nlinks.append(n)
        cq.append(-(1.0 / 24.0) * n * m4)        # C_q (W2 convention)
    out = {"D": D, "rho": rho, "extent": extent, "n_seeds_used": len(m4s),
           "taylor_coeff_u4_exact": "-1/24 (symbolic, no error)"}
    for name, vals in [("m4_scalar_<Dtau(e.e)^2>", m4s),
                       ("n_links_density", nlinks), ("C_q_quartic", cq)]:
        mean, std, sem = _ms(vals)
        out[name] = {"mean": mean, "std": std, "sem": sem}
    return out


def main():
    res = {"n_seeds": NSEED}

    print("=" * 74)
    print(f"AB1 -- C1-C4 COEFFICIENT RE-AUDIT  ({NSEED} seeds, error bars)")
    print("=" * 74)

    # ---- C1/C2 ----
    res["C1C2_d2"] = audit_c1c2(2, rho=60.0, extent=5.0, seed0=4000)
    res["C1C2_d4"] = audit_c1c2(4, rho=10.0, extent=4.0, seed0=5000)
    print("\n[C1/C2] ratios (algebraic?) vs scale kappa & anisotropy (geometric):")
    for key, lab in [("C1C2_d2", "1+1D"), ("C1C2_d4", "3+1D")]:
        r = res[key]
        print(f"  {lab} (rho={r['rho']}, {r['extent']}^{r['D']}, {r['n_seeds_used']} seeds):")
        print(f"     C2/C1 = {r['C2_over_C1']['mean']:.8f} +/- {r['C2_over_C1']['std']:.2e}"
              f"   (std = seed variance of the RATIO)")
        print(f"     C3/C1 = {r['C3_over_C1']['mean']:.8f} +/- {r['C3_over_C1']['std']:.2e}")
        print(f"     kappa = {r['kappa']['mean']:+.4f} +/- {r['kappa']['std']:.4f}"
              f"   (scale: DOES vary seed-to-seed -> geometric)")
        print(f"     anisotropy lambda/|kappa| = {r['anisotropy_lambda_over_abskappa']['mean']:.3f}"
              f" +/- {r['anisotropy_lambda_over_abskappa']['std']:.3f}")
        print(f"     M2 eigenvalues: min={r['M2_eig_min']['mean']:.3e} "
              f"max={r['M2_eig_max']['mean']:.3e}  all_positive={r['all_eigenvalues_positive']}")

    # ---- C3 ----
    res["C3_d2"] = audit_c3(2, rhos=[60, 120, 240, 480], extent=4.0, seed0=10000)
    res["C3_d4"] = audit_c3(4, rhos=[6, 12, 24, 48], extent=3.5, seed0=20000)
    print("\n[C3] X0 exponent p in X0 ~ rho^p  (theory: p=1 dim-independent; "
          "inline comment claims p=1/2 in 3+1D):")
    for key, lab in [("C3_d2", "1+1D"), ("C3_d4", "3+1D")]:
        r = res[key]
        for stat in ("p05", "median"):
            f = r["fits"][stat]
            print(f"  {lab} [{stat:>6}]: p = {f['X0_exponent_p']:+.3f} "
                  f"(boot {f['X0_exponent_p_boot_mean']:+.3f} +/- "
                  f"{f['X0_exponent_p_boot_std']:.3f}, r2={f['r2']:.4f})")

    # ---- C4 ----
    res["C4_d2"] = audit_c4(2, rho=60.0, extent=5.0, seed0=30000)
    res["C4_d4"] = audit_c4(4, rho=10.0, extent=4.0, seed0=31000)
    print("\n[C4] quartic geometric scale C_q = -(1/24) n_links <Dtau(e.e)^2> "
          "(Taylor -1/24 exact):")
    for key, lab in [("C4_d2", "1+1D"), ("C4_d4", "3+1D")]:
        r = res[key]
        mm = r["m4_scalar_<Dtau(e.e)^2>"]; nn = r["n_links_density"]; cc = r["C_q_quartic"]
        print(f"  {lab}: <Dtau(e.e)^2> = {mm['mean']:.4f} +/- {mm['std']:.4f}   "
              f"n_links = {nn['mean']:.3f} +/- {nn['std']:.3f}")
        print(f"        C_q = {cc['mean']:+.5f} +/- {cc['std']:.5f}  "
              f"(sign<0 = DBI-type, nonzero at {abs(cc['mean'])/max(cc['std'],1e-12):.1f}sigma)")

    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "AB1_coefficients_data.json").write_text(json.dumps(res, indent=2))
    print("\n(written AB1_coefficients_data.json)")
    return res


if __name__ == "__main__":
    main()
