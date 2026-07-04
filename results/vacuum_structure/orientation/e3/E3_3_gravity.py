"""E3_3_gravity.py -- does the n-defect carry a 1/r gravitational field?

Charter E3-3.  If the defect survives (E3-1 found it metastable, so it does on
the relaxation timescale), test whether it sources a far-field theta(r) ~ M/r
around itself -- the signature D3 found for a localised mass.

Method (no gravity law inserted):
  1. relax the hedgehog by gradient flow to a stationary texture;
  2. measure the energy-density profile  rho(r) = <gradient density>_shell  and
     fit a power law rho ~ r^p  (a localised lump would fall off fast; the bare
     hedgehog falls as 1/r^2);
  3. form the enclosed "mass"  M(r) = integral_0^r rho 4pi r'^2 dr'.  A genuine
     particle has M(r) -> M_inf finite (localised); a marginal texture has M(r)
     growing without bound;
  4. solve the radial Poisson equation  (1/r^2) d/dr(r^2 dtheta/dr) = rho  for the
     induced potential theta(r) and test whether the FAR field behaves as M/r.

A clean theta ~ M/r with FINITE M => the defect gravitates like matter.
M(r) unbounded and no 1/r tail => the bare defect does not (consistent with a
scale-marginal, non-localised texture).  Reported honestly either way.
"""
from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

import e3_core as e3  # noqa: E402

OUT = Path(__file__).resolve().parent
L = 48


def main():
    t0 = time.time()
    print("=" * 72)
    print("E3-3 -- gravitational field of the defect (theta ~ M/r ?)")
    print("=" * 72)
    c = e3.default_center(L)
    nh = e3.hedgehog(L, +1)
    print(f"  relaxing hedgehog L={L} by gradient flow ...")
    _, nr = e3.relax_gradient(nh, n_steps=2000, dt=0.1, record_every=2000, center=c)
    print(f"  relaxed: B={e3.topological_charge(nr):+.3f}  "
          f"E={e3.gradient_energy(nr):.1f}  r_eff={e3.r_eff(nr):.2f}")

    # energy-density radial profile
    g = e3.gradient_density(nr)
    r, rho, cnt = e3.radial_profile(g, center=c, n_bins=L // 2)
    # fit power law on the bulk window (avoid the 1-cell core and the boundary)
    win = (r > 2.0) & (r < 0.45 * L) & (rho > 0)
    p, logA = np.polyfit(np.log(r[win]), np.log(rho[win]), 1)
    rho_fit_amp = np.exp(logA)
    print(f"  rho(r) ~ r^p :  p = {p:+.3f}  (hedgehog continuum: -2)")

    # enclosed mass M(r) = cumulative integral of rho * 4 pi r^2 dr (shells)
    dr = np.gradient(r)
    Mr = np.cumsum(rho * 4 * np.pi * r ** 2 * dr)
    # is M(r) saturating (localised) or growing (marginal)?  fit M ~ r^q on bulk
    q, _ = np.polyfit(np.log(r[win]), np.log(Mr[win]), 1)
    print(f"  M(r) ~ r^q :    q = {q:+.3f}  (localised particle: q->0 saturating; "
          f"marginal: q~1)")

    # induced potential theta(r): integrate Poisson outward,
    #   theta(r) = -INT_r^Rmax [ M(r')/(4 pi r'^2) ] dr'  (Newtonian shell form)
    field = Mr / (4 * np.pi * np.maximum(r, 1e-6) ** 2)     # -dtheta/dr = g(r)=M/(4pi r^2)
    theta = np.zeros_like(r)
    for i in range(len(r) - 2, -1, -1):
        theta[i] = theta[i + 1] - field[i] * dr[i]
    # far-field test: does theta ~ A/r ?  fit theta vs 1/r on the outer half
    far = (r > 0.25 * L) & (r < 0.45 * L)
    if far.sum() >= 3:
        # theta = A*(1/r) + B ; check linearity in 1/r
        inv = 1.0 / r[far]
        A, Bc = np.polyfit(inv, theta[far], 1)
        yhat = A * inv + Bc
        r2 = 1 - np.sum((theta[far] - yhat) ** 2) / np.sum((theta[far] - theta[far].mean()) ** 2)
    else:
        A, r2 = float("nan"), float("nan")
    print(f"  far-field theta vs 1/r:  amp A={A:.2f}  R^2={r2:.3f}")

    # verdict
    localised = abs(q) < 0.25                       # M(r) saturates
    clean_1r = (r2 > 0.9) and localised
    if clean_1r:
        verdict = "YES -- localised mass, theta ~ M/r far field"
    elif r2 > 0.9 and not localised:
        verdict = ("PARTIAL -- the profile fits 1/r in the window but M(r) keeps "
                   "growing (q~1): the 'mass' is not localised, so there is no "
                   "true asymptotic M/r; the apparent 1/r reflects rho~1/r^2 of a "
                   "scale-marginal texture, not a particle")
    else:
        verdict = "NO -- no clean 1/r field; defect does not gravitate as matter"
    print("-" * 72)
    print(f"  rho exponent p={p:+.2f}, M exponent q={q:+.2f}, theta~1/r R^2={r2:.2f}")
    print(f"  VERDICT theta~M/r: {verdict}")
    print("=" * 72)

    payload = {"L": L, "p_rho": float(p), "q_mass": float(q),
               "theta_1r_amp": float(A), "theta_1r_r2": float(r2),
               "localised": bool(localised), "clean_1r": bool(clean_1r),
               "verdict": verdict,
               "profile": {"r": r.tolist(), "rho": rho.tolist(),
                           "M": Mr.tolist(), "theta": theta.tolist()},
               "runtime_s": time.time() - t0,
               "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
    (OUT / "E3_3_gravity.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'E3_3_gravity.json'}  ({payload['runtime_s']:.0f}s)")

    fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))
    ax = axes[0]
    ax.loglog(r, rho, "o", ms=4)
    ax.loglog(r[win], rho_fit_amp * r[win] ** p, "r-",
              label=f"r^{p:.2f} (cont: -2)")
    ax.set_xlabel("r"); ax.set_ylabel("rho(r) energy density")
    ax.set_title("E3-3: defect energy density"); ax.legend(fontsize=8); ax.grid(alpha=0.25, which="both")
    ax = axes[1]
    ax.plot(r, Mr, "o-", ms=3)
    ax.set_xlabel("r"); ax.set_ylabel("enclosed M(r)")
    ax.set_title(f"enclosed mass M(r) ~ r^{q:.2f}\n(grows => not localised)")
    ax.grid(alpha=0.25)
    ax = axes[2]
    ax.plot(1.0 / r[r > 1], theta[r > 1], "o", ms=3)
    if np.isfinite(A):
        xx = 1.0 / r[far]
        ax.plot(xx, A * xx + Bc, "r-", label=f"A/r, R2={r2:.2f}")
    ax.set_xlabel("1/r"); ax.set_ylabel("theta(r) induced potential")
    ax.set_title("far field vs 1/r"); ax.legend(fontsize=8); ax.grid(alpha=0.25)
    fig.suptitle("E3-3: does the n-defect source a 1/r field?", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "E3_3_gravity.png", dpi=130)
    print(f"saved {OUT/'E3_3_gravity.png'}")


if __name__ == "__main__":
    main()
