"""CR1 -- the network's gravitational coupling vs granularity: exponents and
the pure number G_net * rho^2 * r_c^5.

Pre-registered (CROSS_RELATIONS.md): G_net = 15/(8 pi^2 rho^2 r_c^5), i.e.
exponents -2 (rho) and -5 (r_c), pure constant 15/8pi^2 ~ 0.18998 (tolerance
20%: finite-degree / RGG-clustering corrections are O(1/deg)).

Reuses the DS1 generator (graph Laplacian, Dirichlet shell, CG) by import --
no modification to DS1. The amplitude A is fitted as theta = A/r + C on the
same window protocol as DS1 (the offset C absorbs the grounded-shell image
term). 5 seeds per point.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

HERE = Path(__file__).resolve().parent
DS1_PATH = HERE.parent / "dimension_scan" / "DS1_profiles.py"
spec = importlib.util.spec_from_file_location("ds1", DS1_PATH)
ds1 = importlib.util.module_from_spec(spec)
sys.modules["ds1"] = ds1
spec.loader.exec_module(ds1)

N_SEEDS = 5
RHO_SCAN_N = [20000, 40000, 80000]          # r_c fixed
RC_FIX = (14.0 / 40000.0) ** (1.0 / 3.0)    # the DS1 d=3 radius
RC_SCAN_DEG = [8, 14, 24]                   # N fixed at 40000
N_FIX = 40000
V_BALL = 4.0 * np.pi / 3.0
PRED_CONST = 15.0 / (8.0 * np.pi ** 2)


def amplitude(n, rc, seed):
    """Fit theta = A/r + C on the DS1 window; returns A."""
    rng = np.random.default_rng(7000 + seed)
    pts = ds1.sprinkle_ball(3, n, rng)
    theta, _, _ = ds1.relax(pts, rc)
    rr, th = ds1.binned_profile(pts, theta, 2.0 * rc, ds1.FIT_HI)
    X = np.c_[1.0 / rr, np.ones_like(rr)]
    co, *_ = np.linalg.lstsq(X, th, rcond=None)
    return float(co[0])


def stats(vals):
    v = np.asarray(vals)
    return {"mean": float(np.mean(v)),
            "sem": float(np.std(v, ddof=1) / np.sqrt(len(v)))}


def main():
    rho_rows, rc_rows = [], []
    for n in RHO_SCAN_N:
        A = [amplitude(n, RC_FIX, s) for s in range(N_SEEDS)]
        rho = n / V_BALL
        st = stats(A)
        rho_rows.append({"N": n, "rho": rho, "A": st,
                         "pure_const": st["mean"] * rho ** 2 * RC_FIX ** 5})
    for deg in RC_SCAN_DEG:
        rc = (deg / N_FIX) ** (1.0 / 3.0)
        A = [amplitude(N_FIX, rc, s) for s in range(N_SEEDS)]
        rho = N_FIX / V_BALL
        st = stats(A)
        rc_rows.append({"deg": deg, "r_c": rc, "A": st,
                        "pure_const": st["mean"] * rho ** 2 * rc ** 5})

    lr_rho = np.polyfit(np.log([r["rho"] for r in rho_rows]),
                        np.log([r["A"]["mean"] for r in rho_rows]), 1)
    lr_rc = np.polyfit(np.log([r["r_c"] for r in rc_rows]),
                       np.log([r["A"]["mean"] for r in rc_rows]), 1)
    consts = [r["pure_const"] for r in rho_rows + rc_rows]
    const_mean = float(np.mean(consts))

    payload = {
        "rho_scan": rho_rows, "rc_scan": rc_rows,
        "exponent_rho": {"measured": float(lr_rho[0]), "predicted": -2.0},
        "exponent_rc": {"measured": float(lr_rc[0]), "predicted": -5.0},
        "pure_constant": {"measured_mean": const_mean,
                          "all": consts,
                          "predicted": PRED_CONST,
                          "ratio": const_mean / PRED_CONST},
        "death": bool(abs(const_mean / PRED_CONST - 1.0) > 0.20),
        "_meta": {"timestamp": datetime.now(timezone.utc).isoformat(),
                  "numpy": np.__version__, "n_seeds": N_SEEDS},
    }
    (HERE / "CR1_gnet.json").write_text(json.dumps(payload, indent=2))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2))
    rhos = [r["rho"] for r in rho_rows]
    ax1.errorbar(rhos, [r["A"]["mean"] for r in rho_rows],
                 yerr=[r["A"]["sem"] for r in rho_rows], fmt="o", color="tab:blue",
                 label=f"measured (slope {lr_rho[0]:.2f})")
    rr = np.array(rhos)
    ax1.plot(rr, PRED_CONST / (rr ** 2 * RC_FIX ** 5), "k:",
             label=r"$15/(8\pi^2\rho^2 r_c^5)$")
    ax1.set_xscale("log"); ax1.set_yscale("log")
    ax1.set_xlabel(r"$\rho$"); ax1.set_ylabel(r"$G_{\rm net}$")
    ax1.set_title(f"density scan: slope {lr_rho[0]:.3f} (pred -2)")
    ax1.legend(fontsize=8)

    rcs = [r["r_c"] for r in rc_rows]
    ax2.errorbar(rcs, [r["A"]["mean"] for r in rc_rows],
                 yerr=[r["A"]["sem"] for r in rc_rows], fmt="s", color="tab:red",
                 label=f"measured (slope {lr_rc[0]:.2f})")
    cc = np.array(rcs)
    rho0 = N_FIX / V_BALL
    ax2.plot(cc, PRED_CONST / (rho0 ** 2 * cc ** 5), "k:",
             label=r"$15/(8\pi^2\rho^2 r_c^5)$")
    ax2.set_xscale("log"); ax2.set_yscale("log")
    ax2.set_xlabel(r"$r_c$"); ax2.set_ylabel(r"$G_{\rm net}$")
    ax2.set_title(f"range scan: slope {lr_rc[0]:.3f} (pred -5); "
                  f"pure const {const_mean:.4f} (pred {PRED_CONST:.4f})")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(HERE / "CR1_gnet.png", dpi=150)

    print(json.dumps({"exponent_rho": payload["exponent_rho"],
                      "exponent_rc": payload["exponent_rc"],
                      "pure_constant": {"measured": const_mean,
                                        "predicted": PRED_CONST,
                                        "ratio": const_mean / PRED_CONST},
                      "death": payload["death"]}, indent=2))


if __name__ == "__main__":
    main()
