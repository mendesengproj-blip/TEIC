"""e3 -- R3 + Task C: gravitational time dilation.

PART 1 (R3, CIRCULAR -- consistency only).  The original derivation accumulated
local proper time dtau = sqrt(g_tt) dt along a static worldline and then "found"
the redshift.  That is circular: the answer sqrt(1-2M/r) was put in by hand.  We
reproduce it ONLY as an arithmetic consistency check and label it as such.  Because
it must reference sqrt(g_tt), this part uses validation.py (comparison module) for
that factor -- it is NOT a derivation.

PART 2 (Task C, NON-CIRCULAR).  Sprinkle the 2D Schwarzschild radial slice in
tortoise coordinates, where ds^2 = (1-2M/r)(-dt^2 + dr*^2).  The causal relation is
the bare 45-degree light cone (conformal flatness); the metric enters ONLY as the
proper-volume element setting the local sprinkle density -- it is NEVER square-rooted
in the generator.  For a static observer at radius r we measure the proper time
between two events on its worldline (coordinate separation dt) purely by counting:
    tau_meas = sqrt(2 N / rho).
For small dt this equals the geodesic proper time ~ sqrt(1-2M/r) dt.  Fitting the
slope dtau_meas/d(dt) at each r and comparing to sqrt(1-2M/r) (validation, comparison
only) tests whether gravitational dilation EMERGES from counting.

Verdict: PROVADO / PARCIAL / NEGATIVO / INCONCLUSIVO.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from causal_core import alexandrov_interval  # noqa: E402
from curved import rstar_of_r, sprinkle_schwarzschild  # noqa: E402
from repro import FIGS, rng, save_run  # noqa: E402
from validation import schwarzschild_redshift  # noqa: E402 (COMPARISON ONLY)
from volume import tau_from_count  # noqa: E402

SEED = 27182818
M = 1.0
RHO = 4000.0
N_REAL = 40
RADII = np.array([3.0, 4.0, 6.0, 10.0, 20.0])
DELTAS = np.array([0.8, 1.2, 1.6, 2.0])   # coordinate-time separations (small)


def part1_circular():
    """Arithmetic consistency: sum local dtau = sqrt(g_tt) dt. CIRCULAR."""
    dt = 1.0
    rate = schwarzschild_redshift(RADII, M)   # sqrt(1-2M/r) -- inserted by hand
    return {float(r): float(rt * dt) for r, rt in zip(RADII, rate)}


def measure_tau(r_obs, dt, g):
    """Non-circular proper-time estimate between two static-worldline events."""
    x0 = rstar_of_r(r_obs, M)
    t1, t2 = -dt / 2, dt / 2
    A = np.array([t1, x0]); B = np.array([t2, x0])
    pad = 0.05 * dt
    t_bounds = (t1 - pad, t2 + pad)
    rstar_bounds = (x0 - dt / 2 - pad, x0 + dt / 2 + pad)
    ns = []
    for _ in range(N_REAL):
        pts = sprinkle_schwarzschild(RHO, M, t_bounds, rstar_bounds, g)
        ns.append(len(alexandrov_interval(pts, A, B)))
    return tau_from_count(np.mean(ns), RHO, 2)


def main():
    g = rng(SEED)
    circular = part1_circular()

    # Part 2: slope of tau_meas vs dt (through origin) at each radius.
    slopes, ref = [], []
    tau_table = {}
    for r in RADII:
        taus = np.array([measure_tau(r, dt, g) for dt in DELTAS])
        slope = float(np.sum(DELTAS * taus) / np.sum(DELTAS ** 2))  # least squares, origin
        slopes.append(slope)
        ref.append(float(schwarzschild_redshift(r, M)))
        tau_table[float(r)] = taus.tolist()
    slopes = np.array(slopes)
    ref = np.array(ref)

    rel_err = np.abs(slopes - ref) / ref
    corr = float(np.corrcoef(slopes, ref)[0, 1])
    max_err = float(rel_err.max())

    # ---- figure ----
    fig, ax = plt.subplots(1, 2, figsize=(11.5, 4.5))
    rr = np.linspace(2.6, 21, 200)
    ax[0].plot(rr, schwarzschild_redshift(rr, M), "k-", lw=1.5,
               label=r"$\sqrt{1-2M/r}$ (GR)")
    ax[0].plot(RADII, slopes, "o", ms=7, label="counting estimate")
    ax[0].set_title("(Task C) Gravitational dilation by counting")
    ax[0].set_xlabel("r"); ax[0].set_ylabel(r"$d\tau/dt$"); ax[0].legend()

    ax[1].plot(ref, slopes, "o", ms=7)
    lim = [ref.min() * 0.95, ref.max() * 1.02]
    ax[1].plot(lim, lim, "k--", lw=1, label="y=x")
    ax[1].set_title(f"counting vs GR (corr {corr:.4f}, max err {max_err:.1%})")
    ax[1].set_xlabel(r"$\sqrt{1-2M/r}$ (GR)"); ax[1].set_ylabel("counting estimate")
    ax[1].legend()
    fig.tight_layout()
    fig.savefig(FIGS / "e3_gravitational.png", dpi=130)

    verdict = "PROVADO" if (corr > 0.999 and max_err < 0.03) else (
        "PARCIAL" if corr > 0.99 else "INCONCLUSIVO")

    summary = {
        "part1_circular_note": "sum of local dtau=sqrt(g_tt)dt -- CIRCULAR, consistency only",
        "part1_values": circular,
        "taskC_slopes": slopes.tolist(),
        "taskC_reference_sqrt_gtt": ref.tolist(),
        "taskC_corr": corr, "taskC_max_rel_err": max_err,
        "verdict": verdict,
    }
    save_run("e3_gravitational", SEED,
             {"M": M, "rho": RHO, "n_real": N_REAL, "radii": RADII.tolist(),
              "deltas": DELTAS.tolist()},
             arrays={"radii": RADII, "slopes": slopes, "ref": ref},
             summary={**summary, "tau_table": tau_table})

    print("=" * 70)
    print("R3 + TASK C -- GRAVITATIONAL TIME DILATION")
    print("=" * 70)
    print("PART 1 (CIRCULAR, consistency only): dtau=sqrt(g_tt)dt reproduces redshift")
    print("        -- flagged circular; not a derivation.")
    print("PART 2 (NON-CIRCULAR, counting): static-observer dtau/dt vs sqrt(1-2M/r)")
    for r, s, rf in zip(RADII, slopes, ref):
        print(f"   r={r:5.1f}: counting {s:.4f}   GR {rf:.4f}   err {abs(s-rf)/rf:.2%}")
    print(f"   correlation {corr:.4f}, max rel err {max_err:.2%}")
    print("-" * 70)
    print(f"VERDICT (Task C): {verdict}")
    return summary


if __name__ == "__main__":
    main()
