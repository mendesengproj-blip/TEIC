"""P3_numeric.py -- Variable-density sprinkling in a FLAT causal generator.

BRIDGE investigation (independent of R1-R3 / e6-e11; modifies nothing).

Question (P3, the cleanest test).  Forget the curved metric.  Take bare flat
2D Minkowski (45-degree light cones) and sprinkle at a *position-dependent*
density rho(r) = rho0 * f(r).  A static observer at r measures its proper time
between two worldline events at coordinate separation dt purely by counting,
normalising against the GLOBAL reference density rho0 (the cosmic-mean / far
value), not the local one:

    tau_meas(r) = sqrt( 2 N / rho0 ).

Because the diamond is locally flat with N ~ rho(r) * (1/2) dt^2, this gives

    (dtau/dt)(r) = sqrt( rho(r)/rho0 ) = sqrt( f(r) ).

So the static-observer dilation is set ENTIRELY by the density profile f(r).
Asking which f(r) reproduces the Schwarzschild static-observer rate is therefore
asking: for what f is sqrt(f(r)) = sqrt(1 - 2M/r)?  Answer: f(r) = 1 - 2M/r.

ANTI-CIRCULARITY.  The generator never square-roots anything: it sprinkles at a
density f(r) = (1 - 2M/r), an allowed metric/volume element (the guard forbids
sqrt(1-2M/r), not 1-2M/r).  The redshift sqrt(1-2M/r) and the potential GM/r enter
ONLY in the final comparison.  The dilation must EMERGE from counting.

Honest scope.  This shows the *mechanism* (density variation alone reproduces the
full Schwarzschild static-observer dilation in a flat causal set).  It does NOT
derive the profile f(r) = 1 - 2M/r from network dynamics -- that form is imposed
and then confirmed by counting.  Deriving f from first principles needs a discrete
action with matter (Benincasa-Dowker); out of scope here (see P3 markdown).
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

SEED = 27182818
M = 1.0
RHO0 = 6000.0
N_REAL = 60
RADII = np.array([3.0, 4.0, 6.0, 10.0, 20.0, 40.0])
DELTAS = np.array([0.8, 1.2, 1.6, 2.0])


def density_profile(r):
    """f(r) = rho(r)/rho0 = (1 - 2M/r).  An allowed volume element; NO square root.

    This is the network-density modulation hypothesised at radius r.  It is the
    only relativistic-looking quantity in the generator and it is NOT a dilation
    factor (the dilation sqrt(f) must come out of the counting, never go in)."""
    return 1.0 - 2.0 * M / r


def sprinkle_flat_variable(rho0, fval, t_bounds, x_bounds, g):
    """Flat 2D Poisson sprinkle at uniform density rho0*fval over a small box.

    The box around a static observer is small enough that f is ~constant across it,
    so a homogeneous sprinkle at the local density rho0*f(r) is exact to leading
    order -- exactly the regime in which tau_meas probes the LOCAL density."""
    t_bounds = np.asarray(t_bounds, float)
    x_bounds = np.asarray(x_bounds, float)
    area = (t_bounds[1] - t_bounds[0]) * (x_bounds[1] - x_bounds[0])
    n = g.poisson(rho0 * fval * area)
    return np.column_stack([
        g.uniform(t_bounds[0], t_bounds[1], n),
        g.uniform(x_bounds[0], x_bounds[1], n),
    ])


def measure_clock_rate(r_obs, g):
    """Static-observer dtau/dt by counting, normalised against GLOBAL rho0."""
    fval = density_profile(r_obs)        # local density modulation (no sqrt)
    x0 = 0.0                             # flat space: observer position is arbitrary
    taus = []
    for dt in DELTAS:
        t1, t2 = -dt / 2, dt / 2
        A = np.array([t1, x0]); B = np.array([t2, x0])
        pad = 0.05 * dt
        t_bounds = (t1 - pad, t2 + pad)
        x_bounds = (x0 - dt / 2 - pad, x0 + dt / 2 + pad)
        ns = [len(alexandrov_interval(
                  sprinkle_flat_variable(RHO0, fval, t_bounds, x_bounds, g), A, B))
              for _ in range(N_REAL)]
        # NOTE: normalise by the GLOBAL rho0, not the local rho0*fval -> dilation.
        taus.append(tau_from_count(np.mean(ns), RHO0, 2))
    taus = np.array(taus)
    return float(np.sum(DELTAS * taus) / np.sum(DELTAS ** 2))


def main():
    g = rng(SEED)

    clock_rate = np.array([measure_clock_rate(r, g) for r in RADII])  # dtau/dt
    f_used = density_profile(RADII)                                  # rho/rho0 input

    # ---- comparison only ----
    gr_rate = schwarzschild_redshift(RADII, M)        # sqrt(1-2M/r)
    corr = float(np.corrcoef(clock_rate, gr_rate)[0, 1])
    max_err = float(np.max(np.abs(clock_rate - gr_rate) / gr_rate))

    # Inverse check: does the counted dilation^2 recover the input density f(r)?
    f_recovered = clock_rate ** 2
    f_err = float(np.max(np.abs(f_recovered - f_used) / f_used))

    passes = (corr > 0.999 and max_err < 0.03)
    verdict = "PASSA" if passes else "FALHA"

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    rr = np.linspace(2.7, 41, 300)
    ax[0].plot(rr, schwarzschild_redshift(rr, M), "k-", lw=1.5,
               label=r"$\sqrt{1-2M/r}$ (GR)")
    ax[0].plot(RADII, clock_rate, "o", ms=7,
               label=r"counted $d\tau/dt$ (flat, variable $\rho$)")
    ax[0].set_title("(P3) Schwarzschild dilation from a flat variable-density sprinkle")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$d\tau/dt$"); ax[0].legend()

    ax[1].plot(f_used, f_recovered, "o", ms=7)
    lim = [f_used.min() * 0.98, f_used.max() * 1.02]
    ax[1].plot(lim, lim, "k--", lw=1, label="y=x")
    ax[1].set_title(r"input density $f(r)$ vs counted $(d\tau/dt)^2$")
    ax[1].set_xlabel(r"$f(r)=\rho/\rho_0$ (input)")
    ax[1].set_ylabel(r"$(d\tau/dt)^2$ (counted)"); ax[1].legend()
    fig.tight_layout()
    fig.savefig(OUT / "P3_numeric.png", dpi=130)

    summary = {
        "what": "flat 2D variable-density sprinkle; dtau/dt counted vs global rho0",
        "M": M, "rho0": RHO0, "n_real": N_REAL,
        "radii": RADII.tolist(),
        "density_input_f=rho/rho0 (=1-2M/r)": f_used.tolist(),
        "clock_rate_counted": clock_rate.tolist(),
        "clock_rate_GR_sqrt(1-2M/r)": gr_rate.tolist(),
        "dilation_corr": corr,
        "dilation_max_rel_err": max_err,
        "density_recovered_(dtau/dt)^2": f_recovered.tolist(),
        "density_recovery_max_rel_err": f_err,
        "verdict": verdict,
        "note": "profile f(r)=1-2M/r is imposed, not derived; deriving it needs a "
                "discrete action with matter (Benincasa-Dowker) -- out of scope.",
        "seed": SEED,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "P3_numeric_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("P3 -- SCHWARZSCHILD DILATION FROM A FLAT VARIABLE-DENSITY SPRINKLE")
    print("=" * 72)
    print("generator: flat light cones, rho(r)=rho0*(1-2M/r) [no sqrt]; count vs rho0")
    for r, cr, gr in zip(RADII, clock_rate, gr_rate):
        print(f"  r={r:5.1f}:  dtau/dt(count)={cr:.4f}   GR sqrt(1-2M/r)={gr:.4f}   "
              f"err {abs(cr-gr)/gr:.2%}")
    print("-" * 72)
    print(f"dilation vs GR : corr {corr:.5f}, max rel err {max_err:.2%}")
    print(f"density recover: (dtau/dt)^2 vs input f(r), max rel err {f_err:.2%}")
    print(f"VERDICT (P3)   : {verdict}")
    print("note: f(r)=1-2M/r is IMPOSED then confirmed by counting; not derived from")
    print("      network dynamics (that needs a discrete action -- out of scope).")
    return summary


if __name__ == "__main__":
    main()
