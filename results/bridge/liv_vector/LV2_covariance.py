"""LV2_covariance.py -- is the plaquette ensemble boost-covariant?

LIV_VECTOR task LV2.  A genuine preferred frame would make the SHAPE of the
plaquette population at axis rapidity eta differ from the boost of the
rest population.  Internal covariance test (no continuum model, no fit):

  (i)  bin plaquettes by axis rapidity eta of the causal diagonal d1;
  (ii) PREDICT the E/B of bin eta by analytically boosting the measured
       rest-bin population (eta < 0.15) by eta along random directions;
  (iii) compare measured vs predicted bin by bin.

Also measured: <pa2> = <e2-b2> per bin.  pa2 is a Lorentz invariant, so any
eta-dependence is pure SELECTION (the box truncates large boosted diamonds),
quantifying the regulator at work; the covariance comparison is also run in
a fixed proper-area band (middle two quartiles of the rest bin) to control
that selection.

PRE-REGISTERED KILL: systematic measured-vs-predicted mismatch beyond ~2 sigma
across rapidity bins (in the size-controlled comparison) => the ensemble has
intrinsic Lorentz violation beyond sampling kinematics => restoration fails.
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from liv_core import plaquette_ensemble, boost_bivectors, eb_of  # noqa: E402

OUT = Path(__file__).resolve().parent

RHO, EXTENT, NSEED, SEED0, NBASES = 12.0, 4.0, 20, 200, 1500
ETA_REST = 0.15
BINS = [(0.15, 0.35), (0.35, 0.55), (0.55, 0.75), (0.75, 0.95),
        (0.95, 1.15), (1.15, 1.45)]
NBOOT = 400


def ratio_boot(e2, b2, rng, nboot=NBOOT):
    """E/B = mean e2 / mean b2 with bootstrap sem over plaquettes."""
    n = len(e2)
    r = e2.mean() / b2.mean()
    idx = rng.integers(0, n, size=(nboot, n))
    rs = e2[idx].mean(axis=1) / b2[idx].mean(axis=1)
    return float(r), float(rs.std())


def main():
    seeds = plaquette_ensemble(RHO, EXTENT, NSEED, SEED0, n_bases=NBASES)
    e2 = np.concatenate([s["e2"] for s in seeds])
    b2 = np.concatenate([s["b2"] for s in seeds])
    pa2 = e2 - b2
    eta = np.concatenate([s["eta"] for s in seeds])
    Om = np.concatenate([s["Om"] for s in seeds])
    rng = np.random.default_rng(7)

    rest = eta < ETA_REST
    q1, q3 = np.quantile(pa2[rest], [0.25, 0.75])
    band = (pa2 >= q1) & (pa2 <= q3)

    rows = []
    for lo, hi in BINS:
        sel = (eta >= lo) & (eta < hi)
        if sel.sum() < 30:
            continue
        ec = 0.5 * (lo + hi)
        # measured
        m_r, m_s = ratio_boot(e2[sel], b2[sel], rng)
        # predicted: boost the rest population to eta = bin center
        Ob = boost_bivectors(Om[rest], ec, rng)
        pe, pb = eb_of(Ob)
        p_r, p_s = ratio_boot(pe, pb, rng)
        # size-controlled comparison (fixed invariant proper-area band)
        selb, restb = sel & band, rest & band
        m_rb, m_sb = ratio_boot(e2[selb], b2[selb], rng) if selb.sum() > 30 else (np.nan, np.nan)
        Obb = boost_bivectors(Om[restb], ec, rng)
        peb, pbb = eb_of(Obb)
        p_rb, p_sb = ratio_boot(peb, pbb, rng)
        z = abs(m_r - p_r) / np.hypot(m_s, p_s)
        zb = (abs(m_rb - p_rb) / np.hypot(m_sb, p_sb)) if np.isfinite(m_rb) else np.nan
        rows.append({"eta_lo": lo, "eta_hi": hi, "n": int(sel.sum()),
                     "EB_measured": m_r, "EB_measured_sem": m_s,
                     "EB_predicted": p_r, "EB_predicted_sem": p_s, "z": float(z),
                     "EB_measured_band": m_rb, "EB_predicted_band": p_rb,
                     "z_band": float(zb) if np.isfinite(zb) else None,
                     "pa2_mean": float(pa2[sel].mean()),
                     "pa2_rest_mean": float(pa2[rest].mean())})

    z_all = [r["z_band"] for r in rows if r["z_band"] is not None]
    res = {
        "config": {"rho": RHO, "extent": EXTENT, "n_seeds": len(seeds),
                   "eta_rest": ETA_REST, "n_plaquettes": int(len(e2))},
        "rest_bin": {"n": int(rest.sum()),
                     "EB": float(e2[rest].mean() / b2[rest].mean())},
        "bins": rows,
        "z_band_median": float(np.median(z_all)),
        "z_band_max": float(np.max(z_all)),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "LV2_covariance_data.json").write_text(json.dumps(res, indent=2))

    print("=" * 72)
    print("LV2 -- boost covariance: measured E/B(eta) vs boosted rest population")
    print("=" * 72)
    print(f"plaquettes {len(e2)}, rest bin (eta<{ETA_REST}): n={rest.sum()}, "
          f"E/B={res['rest_bin']['EB']:.2f}")
    print(f"{'eta bin':>12} {'n':>6} {'measured':>10} {'predicted':>10} {'z':>6}"
          f" {'meas(band)':>11} {'pred(band)':>11} {'z_band':>7}")
    for r in rows:
        print(f"[{r['eta_lo']:.2f},{r['eta_hi']:.2f}) {r['n']:>6}"
              f" {r['EB_measured']:>7.2f}+/-{r['EB_measured_sem']:.2f}"
              f" {r['EB_predicted']:>7.2f}+/-{r['EB_predicted_sem']:.2f}"
              f" {r['z']:>6.2f}"
              f" {r['EB_measured_band']:>11.2f} {r['EB_predicted_band']:>11.2f}"
              f" {r['z_band'] if r['z_band'] is not None else float('nan'):>7.2f}")
    print(f"<pa2>(eta) selection drift: rest {res['rest_bin']['n']} plaq, "
          f"mean pa2 {rows[0]['pa2_rest_mean']:.3e}; per-bin means "
          + ", ".join(f"{r['pa2_mean']:.2e}" for r in rows))
    print("-" * 72)
    print(f"z (size-controlled): median {res['z_band_median']:.2f}, "
          f"max {res['z_band_max']:.2f}")
    if res["z_band_median"] <= 2.0:
        print("VERDICT (LV2): bin-by-bin, the boosted rest population reproduces the")
        print("  measured E/B(eta): the ensemble is boost-covariant within errors --")
        print("  no intrinsic preferred frame; the global E/B~3 is the rapidity-")
        print("  weighted average of an LI orbit truncated by the box.")
    else:
        print("VERDICT (LV2): KILL -- covariance mismatch beyond 2 sigma: intrinsic LV.")
    return res


if __name__ == "__main__":
    main()
