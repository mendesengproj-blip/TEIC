"""LV3_cutoff.py -- is E/B ~ 3 a regulator number (box-truncated boost orbit)?

LIV_VECTOR task LV3.  If the plaquette ensemble is an LI boost orbit truncated
at the rapidity the box can hold (eta_max ~ ln(L rho^{1/4})), then:

  (P1) the cumulative E/B(eta_cut) curves for different box extents L must
       COLLAPSE onto one universal curve, with only the endpoint moving;
  (P2) the endpoint E/B(L) must drift DOWN (toward 1) as L (or rho) grows;
  (P3) per plaquette, <e2-b2> (invariant proper area^2) must be stable across
       eta, while <e2+b2> (the Euclidean, frame-dependent weight) grows ~
       cosh(2 eta): the LV part of the quadratic coefficient is carried
       entirely by the truncation depth.

PRE-REGISTERED KILL: E/B independent of the cutoff (no drift with L at fixed
rho and with rho at fixed L), or no collapse of the cumulative curves =>
the violation is intrinsic, not a regulator artifact => restoration fails.
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from liv_core import plaquette_ensemble  # noqa: E402

OUT = Path(__file__).resolve().parent

ETA_GRID = np.arange(0.1, 2.05, 0.1)
SCANS = [
    # (label, rho, extent, n_seeds, seed0, n_bases)
    ("L3.0_rho12", 12.0, 3.0, 16, 300, 1500),
    ("L4.0_rho12", 12.0, 4.0, 16, 200, 1500),
    ("L5.0_rho12", 12.0, 5.0, 12, 400, 1500),
    ("L6.0_rho12", 12.0, 6.0, 10, 500, 1500),
    ("L4.0_rho06", 6.0, 4.0, 16, 600, 1500),
    ("L4.0_rho24", 24.0, 4.0, 12, 700, 1500),
]


def analyze(label, rho, extent, nseed, seed0, nbases):
    seeds = plaquette_ensemble(rho, extent, nseed, seed0, n_bases=nbases)
    e2 = np.concatenate([s["e2"] for s in seeds])
    b2 = np.concatenate([s["b2"] for s in seeds])
    eta = np.concatenate([s["eta"] for s in seeds])
    eb_seed = np.array([s["e2"].mean() / s["b2"].mean() for s in seeds])
    # cumulative E/B(eta_cut)
    curve = []
    for ec in ETA_GRID:
        sel = eta <= ec
        curve.append(e2[sel].mean() / b2[sel].mean() if sel.sum() > 50 else np.nan)
    # per-eta-bin invariant vs Euclidean weights
    binw = 0.3
    bins = np.arange(0.0, eta.max() + binw, binw)
    inv_bin, euc_bin, n_bin = [], [], []
    for lo in bins[:-1]:
        sel = (eta >= lo) & (eta < lo + binw)
        if sel.sum() < 30:
            inv_bin.append(np.nan); euc_bin.append(np.nan); n_bin.append(int(sel.sum()))
            continue
        inv_bin.append(float((e2[sel] - b2[sel]).mean()))
        euc_bin.append(float((e2[sel] + b2[sel]).mean()))
        n_bin.append(int(sel.sum()))
    return {
        "label": label, "rho": rho, "extent": extent, "n_seeds": len(seeds),
        "n_plaquettes": int(len(e2)),
        "reach": float(extent * rho ** 0.25),       # box size in granularity units
        "EB_total": float(eb_seed.mean()),
        "EB_total_sem": float(eb_seed.std() / np.sqrt(len(eb_seed))),
        "eta_q95": float(np.quantile(eta, 0.95)),
        "eta_max": float(eta.max()),
        "curve_eta": ETA_GRID.tolist(),
        "curve_EB": curve,
        "bin_lo": bins[:-1].tolist(),
        "bin_inv_e2_minus_b2": inv_bin,
        "bin_euc_e2_plus_b2": euc_bin,
        "bin_n": n_bin,
    }


def main():
    res = {"scans": [analyze(*cfg) for cfg in SCANS]}
    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    # P1 collapse: rms spread of curves across L (rho=12) where all defined
    Ls = [s for s in res["scans"] if s["rho"] == 12.0]
    common = []
    for i, ec in enumerate(ETA_GRID):
        vals = [s["curve_EB"][i] for s in Ls]
        if all(v is not None and np.isfinite(v) for v in vals):
            common.append((float(ec), [float(v) for v in vals],
                           float(np.std(vals) / np.mean(vals))))
    res["collapse_rel_spread_max"] = max(c[2] for c in common) if common else None

    (OUT / "LV3_cutoff_data.json").write_text(json.dumps(res, indent=2))

    print("=" * 72)
    print("LV3 -- cutoff scan: is E/B set by how much boost orbit the box holds?")
    print("=" * 72)
    print(f"{'scan':>12} {'reach':>6} {'n_plaq':>7} {'eta_q95':>8} {'E/B total':>12}")
    for s in res["scans"]:
        print(f"{s['label']:>12} {s['reach']:>6.2f} {s['n_plaquettes']:>7}"
              f" {s['eta_q95']:>8.2f} {s['EB_total']:>8.3f}+/-{s['EB_total_sem']:.3f}")
    print("\nP1 cumulative-curve collapse across L (rho=12):")
    print(f"{'eta_cut':>8} " + " ".join(f"{s['label']:>11}" for s in Ls) + "  rel.spread")
    for ec, vals, sp in common:
        print(f"{ec:>8.1f} " + " ".join(f"{v:>11.3f}" for v in vals) + f"  {sp:>9.3f}")
    print("\nP3 per-bin weights (L4.0_rho12): eta_bin | <e2-b2> (invariant) | "
          "<e2+b2> (Euclidean) | n")
    s4 = next(s for s in res["scans"] if s["label"] == "L4.0_rho12")
    for lo, iv, eu, nb in zip(s4["bin_lo"], s4["bin_inv_e2_minus_b2"],
                              s4["bin_euc_e2_plus_b2"], s4["bin_n"]):
        if np.isfinite(iv):
            print(f"  [{lo:.1f},{lo+0.3:.1f}) {iv:>12.3e} {eu:>12.3e} {nb:>7}")
    print("-" * 72)
    ebs = [(s["reach"], s["EB_total"]) for s in res["scans"]]
    drift = all(b[1] < a[1] + 1e-9 for a, b in
                zip(sorted(ebs), sorted(ebs)[1:]))
    print(f"E/B vs reach (sorted): " +
          ", ".join(f"{r:.1f}->{v:.2f}" for r, v in sorted(ebs)))
    print(f"monotone decrease with reach: {drift}; "
          f"max curve rel. spread: {res['collapse_rel_spread_max']:.3f}")
    return res


if __name__ == "__main__":
    main()
