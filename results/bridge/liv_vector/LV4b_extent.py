"""LV4b_extent.py -- is the residual boost defect a box-reach artifact?

LIV_VECTOR task LV4b (follow-up to LV4's PARTIAL).  LV4 found the boost
defect |R(beta)-1| collapses by ~3 orders of magnitude when the field leaves
the quadratic regime, but the pre-registered 5% window was not met at
extent L = 4 in the sensitive block (E0 ~ u0).  If the residual defect is the
truncation of the boost orbit (reach eta_max ~ ln(L rho^{1/4})), it must
SHRINK as L grows at fixed rho, E0/u0 and beta.

PRE-REGISTERED: PASS if defect(beta=0.8; E0=u0) decreases monotonically
(within errors) with L over {3,4,5,6}; KILL if it is L-independent (floor =>
intrinsic LV remnant).
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from liv_core import (plaquette_ensemble, F_pure_E, boost_field,  # noqa: E402
                      F_invariant, action_sum)

OUT = Path(__file__).resolve().parent

RHO = 12.0
BETAS = [0.4, 0.8, 1.2]
YHAT = np.array([0.0, 1.0, 0.0])
SCANS = [(3.0, 16, 300), (4.0, 16, 200), (5.0, 12, 400), (6.0, 10, 500)]
E0FACS = [1.0, 2.0]


def main():
    res = {"rho": RHO, "betas": BETAS, "E0_factors": E0FACS, "scans": []}
    for extent, nseed, seed0 in SCANS:
        seeds = plaquette_ensemble(RHO, extent, nseed, seed0, n_bases=1500)
        Oms = [s["Om"] for s in seeds]
        om01 = np.concatenate([np.abs(O[:, 0, 1]) for O in Oms])
        u0 = 1.0 / float(np.median(om01))   # per-extent anchor (same granularity)
        eta = np.concatenate([s["eta"] for s in seeds])
        row = {"extent": extent, "n_seeds": len(seeds), "u0": u0,
               "n_plaquettes": int(sum(len(O) for O in Oms)),
               "eta_q95": float(np.quantile(eta, 0.95)), "blocks": []}
        for fac in E0FACS:
            F0 = F_pure_E(fac * u0, axis=1)
            inv0 = F_invariant(F0)
            blk = {"E0_factor": fac, "defects": []}
            for beta in BETAS:
                F = boost_field(F0, beta, YHAT)
                assert abs(F_invariant(F) - inv0) < 1e-9 * abs(inv0)
                r = np.array([action_sum(F, O)[0] / action_sum(F0, O)[0]
                              for O in Oms])
                blk["defects"].append({
                    "beta": beta, "R_mean": float(r.mean()),
                    "R_sem": float(r.std() / np.sqrt(len(r))),
                    "defect": float(abs(r.mean() - 1.0))})
            row["blocks"].append(blk)
        res["scans"].append(row)
        print(f"L={extent}: n_plaq={row['n_plaquettes']}, eta_q95={row['eta_q95']:.2f}, "
              + "; ".join(
                  f"E0={b['E0_factor']}u0: " + ", ".join(
                      f"d({d['beta']})={d['defect']:.4f}+/-{d['R_sem']:.4f}"
                      for d in b["defects"])
                  for b in row["blocks"]))

    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "LV4b_extent_data.json").write_text(json.dumps(res, indent=2))

    print("-" * 72)
    for fac in E0FACS:
        for beta in BETAS:
            ds = []
            for row in res["scans"]:
                blk = next(b for b in row["blocks"] if b["E0_factor"] == fac)
                d = next(x for x in blk["defects"] if x["beta"] == beta)
                ds.append((row["extent"], d["defect"], d["R_sem"]))
            mono = all(b[1] <= a[1] + np.hypot(a[2], b[2])
                       for a, b in zip(ds, ds[1:]))
            print(f"E0={fac}u0 beta={beta}: defect(L) = " +
                  ", ".join(f"L{int(L)}:{d:.4f}" for L, d, _ in ds) +
                  f"   monotone-decreasing(within err): {mono}")
    return res


if __name__ == "__main__":
    main()
