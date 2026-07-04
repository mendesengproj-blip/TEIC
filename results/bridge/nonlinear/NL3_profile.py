"""NL3_profile.py -- rho(r) at small r: Newtonian vs Schwarzschild vs truncated.

BRIDGE / NON-LINEAR investigation.  Independent of R1-R3 and e6-e11; modifies
nothing.  Continues NL2.  D3/NL2 are reliable in the far field; NL3 pushes to SMALL
r (strong field, sub-horizon), where the deviation from the linear/Newtonian regime
is largest, and asks which curve the counted density follows.

Method (kinematic counting -- the proper-time clock, P2/P3/R3 mechanism).  The
network's linear potential is theta = M/r (the D3-derived harmonic field; the BD
dynamics is linear, NL1).  A static observer's proper-time density rho_eff is got by
COUNTING in a flat sprinkle of local proper density rho0*(1 - 2 theta) -- an allowed
volume element, NO square root in the generator.  The counted clock rate comes out
sqrt(1 - 2 theta), so rho_eff/rho0 = 1/sqrt(1 - 2 theta).  We compare the counted
rho_eff at small r against three curves (COMPARISON ONLY):

    Newtonian        : 1 + u
    Schwarzschild    : 1/sqrt(1 - 2u)      (= 1 + u + (3/2)u^2 + ...)
    truncated (2nd)  : 1 + u + (3/2)u^2          u = M/r

Success (NL3): the counted density follows Schwarzschild better than Newtonian at
small r, and the deviation has the right SIGN (rho grows FASTER than 1 + u).

HORIZON -- OPEN FRONTIER (not attempted).  The exact result holds to r -> 2M (the
horizon, u -> 1/2), but counting there needs rho0 -> infinity (the diamond shrinks
and N -> 0 per shell): N >> tractable.  We stop at r >= 2.5 M (u <= 0.4) and document
r -> 2M as the open boundary.  No claim is made about the horizon.

ANTI-CIRCULARITY.  The generator sprinkles at (1 - 2 theta) (allowed volume
element); the square root EMERGES from causal counting (diamond volume), never
imposed.  Schwarzschild's 1/sqrt(1-2u) and the coefficient 3/2 appear ONLY in the
COMPARISON ONLY block.  Guard (tests/test_no_circularity.py) still passes.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval  # noqa: E402
from repro import rng  # noqa: E402
from volume import tau_from_count  # noqa: E402
from validation import schwarzschild_redshift  # noqa: E402 (COMPARISON ONLY)

OUT = Path(__file__).resolve().parent

SEED = 1414213562
M = 1.0                                   # calibrated source amplitude (theta = M/r)
RHO0 = 12000.0                            # high density: small-r diamonds need counts
N_REAL = 120
DELTAS = np.array([0.6, 0.9, 1.2, 1.5])
# sub-horizon radii: r >= 2.5 M (u <= 0.4).  r -> 2M is the open frontier (not probed).
RADII = np.array([2.5, 3.0, 4.0, 6.0, 9.0, 14.0, 22.0])


def sprinkle_flat_variable(rho0, fval, t_bounds, x_bounds, g):
    t_bounds = np.asarray(t_bounds, float); x_bounds = np.asarray(x_bounds, float)
    area = (t_bounds[1] - t_bounds[0]) * (x_bounds[1] - x_bounds[0])
    n = g.poisson(rho0 * fval * area)
    return np.column_stack([g.uniform(t_bounds[0], t_bounds[1], n),
                            g.uniform(x_bounds[0], x_bounds[1], n)])


def count_clock_rate(r_obs, g):
    """Static-observer dtau/dt at radius r_obs by counting (theta = M/r; f = 1 - 2 theta)."""
    fval = 1.0 - 2.0 * M / r_obs            # local proper density modulation (no sqrt)
    taus = []
    for dt in DELTAS:
        t1, t2 = -dt / 2, dt / 2
        A = np.array([t1, 0.0]); B = np.array([t2, 0.0])
        pad = 0.05 * dt
        tb = (t1 - pad, t2 + pad); xb = (-dt / 2 - pad, dt / 2 + pad)
        ns = [len(alexandrov_interval(sprinkle_flat_variable(RHO0, fval, tb, xb, g), A, B))
              for _ in range(N_REAL)]
        taus.append(tau_from_count(np.mean(ns), RHO0, 2))
    taus = np.array(taus)
    return float(np.sum(DELTAS * taus) / np.sum(DELTAS ** 2))


def main():
    g = rng(SEED)
    dtau = np.array([count_clock_rate(r, g) for r in RADII])
    rho_eff = 1.0 / dtau                                   # counted rho_eff/rho0

    # ============================ COMPARISON ONLY ============================
    u = M / RADII
    newt = 1.0 + u
    trunc = 1.0 + u + 1.5 * u ** 2
    sch = 1.0 / schwarzschild_redshift(RADII, M)           # 1/sqrt(1-2u)

    err_newt = np.abs(rho_eff - newt) / sch
    err_trunc = np.abs(rho_eff - trunc) / sch
    err_sch = np.abs(rho_eff - sch) / sch
    rms = lambda e: float(np.sqrt(np.mean(e ** 2)))
    rms_newt, rms_trunc, rms_sch = rms(err_newt), rms(err_trunc), rms(err_sch)

    small = RADII <= 6.0                                   # small-r (strong field) window
    sch_beats_newt_small = bool(rms(err_sch[small]) < rms(err_newt[small]))
    # right sign: counted density exceeds the Newtonian 1 + u (grows faster)
    excess = rho_eff - newt
    right_sign = bool(np.all(excess[small] > 0))
    # how much of the (Schw - Newt) second-order gap is captured by the count:
    gap = sch - newt
    captured = float(np.median((excess[small]) / gap[small]))   # ~1 if matches Schw
    # ========================== END COMPARISON ONLY =========================

    passes = bool(sch_beats_newt_small and right_sign and rms_sch < rms_newt)
    verdict = "PASSA" if passes else ("PARCIAL" if right_sign else "FALHA")

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    rr = np.linspace(RADII.min(), RADII.max(), 300)
    uu = M / rr
    ax[0].plot(rr, 1.0 / schwarzschild_redshift(rr, M), "k-", lw=1.5,
               label=r"Schwarzschild $1/\sqrt{1-2u}$")
    ax[0].plot(rr, 1.0 + uu + 1.5 * uu ** 2, "C2:", lw=1.4,
               label=r"truncated $1+u+\frac{3}{2}u^2$")
    ax[0].plot(rr, 1.0 + uu, "0.6", ls="--", lw=1.2, label=r"Newtonian $1+u$")
    ax[0].plot(RADII, rho_eff, "o", ms=7, color="C3", label="counted")
    ax[0].axvline(2.0, color="r", ls=":", lw=1, label="horizon $r=2M$ (open)")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$\rho_{\rm eff}/\rho_0$")
    ax[0].set_title("(NL3) density profile at small r")
    ax[0].legend(fontsize=8)

    ax[1].plot(RADII, err_newt, "o-", color="0.6", label=f"vs Newtonian (rms {rms_newt:.1%})")
    ax[1].plot(RADII, err_trunc, "s-", color="C2", label=f"vs truncated (rms {rms_trunc:.1%})")
    ax[1].plot(RADII, err_sch, "^-", color="k", label=f"vs Schwarzschild (rms {rms_sch:.1%})")
    ax[1].set_xlabel("r"); ax[1].set_ylabel("relative error of counted density")
    ax[1].set_title("counted density: which curve fits best?")
    ax[1].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(OUT / "NL3_profile.png", dpi=130)

    summary = {
        "what": "small-r density profile by counting (theta=M/r); which curve fits best.",
        "M": M, "rho0": RHO0, "n_real": N_REAL, "radii": RADII.tolist(),
        "counted_rho_eff": rho_eff.tolist(),
        "newtonian_1+u": newt.tolist(),
        "truncated_1+u+1.5u2": trunc.tolist(),
        "schwarzschild_1/sqrt(1-2u)": sch.tolist(),
        "rms_err_vs_newtonian": rms_newt,
        "rms_err_vs_truncated": rms_trunc,
        "rms_err_vs_schwarzschild": rms_sch,
        "schwarzschild_beats_newtonian_small_r": sch_beats_newt_small,
        "deviation_right_sign_small_r": right_sign,
        "fraction_of_2nd_order_gap_captured": captured,
        "horizon_note": "r -> 2M (u -> 1/2) is the OPEN FRONTIER: counting needs "
                        "rho0 -> inf (N -> 0 per shell). Stopped at r >= 2.5M; no "
                        "horizon claim.",
        "verdict": verdict,
        "seed": SEED,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "NL3_profile_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("NL3 -- DENSITY PROFILE AT SMALL r (Newtonian vs Schwarzschild vs truncated)")
    print("=" * 72)
    print("counted rho_eff/rho0 via proper-time counting (theta=M/r, f=1-2theta, no sqrt)")
    print(f"{'r':>6} {'u=M/r':>7} {'counted':>9} {'Newton':>8} {'trunc':>8} {'Schw':>8}")
    for r_, u_, c_, n_, t_, s_ in zip(RADII, u, rho_eff, newt, trunc, sch):
        print(f"{r_:6.1f} {u_:7.3f} {c_:9.4f} {n_:8.4f} {t_:8.4f} {s_:8.4f}")
    print("-" * 72)
    print(f"rms rel err  vs Newtonian={rms_newt:.2%}  vs truncated={rms_trunc:.2%}  "
          f"vs Schwarzschild={rms_sch:.2%}")
    print(f"small-r (r<=6): Schwarzschild beats Newtonian : {sch_beats_newt_small}")
    print(f"deviation from Newtonian has right sign (>0)   : {right_sign}")
    print(f"fraction of 2nd-order (Schw-Newt) gap captured : {captured:.2f}  (~1 = full)")
    print(f"horizon r->2M                                  : OPEN FRONTIER (not probed)")
    print("-" * 72)
    print(f"VERDICT (NL3): {verdict}")
    return summary


if __name__ == "__main__":
    main()
