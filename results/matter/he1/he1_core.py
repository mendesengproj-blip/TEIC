"""he1_core.py -- HIGH_ENERGY_REGIME / HE1 driver helpers.

HE1 asks the SAME question as FL3 (does a Skyrmion(B=+1) + anti-Skyrmion(B=-1) collision
CREATE an extra pair?) but in the regime FL3 could not reach:

  * HIGHER LATTICE RESOLUTION  -- dx smaller, so the soliton core is resolved by ~2x more
    sites than FL3's ~4 points/core (FL3 honest-limitations item #1).
  * ULTRA-RELATIVISTIC BOOST    -- v = 0.90 c and v = 0.99 c (FL3 ran v = 0.50 c; its
    synthesis said only "v -> c" could even APPROACH the 2 M_Sk c^2 threshold).

This module adds NOTHING to the physics: it imports fl3_core unchanged (which itself imports
su2_core unchanged) and only re-runs its validated machinery on a finer grid at higher v.

  * c = C_MAGNON is the E2-measured magnon speed (fl3_core loads it from E2_2_dispersion);
    "v = 0.99 c" is anchored to that measurement, not hand-set.
  * B is the geometric current-determinant baryon number (su2_core.baryon_number).
  * M_Sk is the 3D lattice energy of the relaxed Skyrmion at THIS resolution.
  * The boost imparts a translation velocity as the exact finite-difference body angular
    velocity the geodesic leapfrog integrates -- NO Lorentz gamma is baked into the profile,
    so the kinetic energy is whatever the lattice carries and the E >= 2 M c^2 test is not
    circular (identical convention to FL3, only v is larger).

DEATH CRITERION (pre-registered, HIGH_ENERGY_REGIME.md):
  no creation even as v -> c  =>  the matter-creation frontier stays where FL3 put it.
  Do NOT tune parameters to force creation.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
FL3 = HERE.parents[0] / "fl3"
SU2 = HERE.parents[0] / "su2"
sys.path.insert(0, str(FL3))
sys.path.insert(0, str(SU2))

import fl3_core as f   # noqa: E402  (imports su2_core internally)
import su2_core as s   # noqa: E402

C = f.C_MAGNON
OUT = HERE


# --------------------------------------------------------------------------- #
# collision run (high-resolution clone of FL3_2_dynamics.run_collision, with v free)
# --------------------------------------------------------------------------- #
def run_collision(L, N, e_sk, d0, v_frac, b, seed, dt_frac, t_end,
                  record_every=40, vac_noise=0.03, record_fields=False):
    xs, dx = f.cubic_grid(L, N)
    prof = f.relaxed_profile(e_sk)
    v = v_frac * C
    U, w = f.boosted_pair(xs, dx, d=d0, v=v, b=b, prof=prof, e_sk=e_sk,
                          seed=seed, vac_noise=(0.0 if seed == 0 else vac_noise))
    dt = dt_frac * dx
    KE0 = s.kinetic_energy(w, dx)
    n_blocks = int(np.ceil(t_end / (record_every * dt)))

    ser = {"t": [], "B": [], "E_field": [], "E_total": [], "Q_top": [],
           "n_peaks": [], "n_pos": [], "n_neg": [], "n_blobs": []}
    snaps = []
    t = 0.0
    kz = N // 2
    for blk in range(n_blocks):
        diag = f.soliton_diagnostics(U, dx, e_sk)
        ke = s.kinetic_energy(w, dx)
        ser["t"].append(t)
        ser["B"].append(diag["B"])
        ser["E_field"].append(diag["E_field"])
        ser["E_total"].append(diag["E_field"] + ke)
        ser["Q_top"].append(diag["Q_top"])
        ser["n_peaks"].append(diag["n_peaks"])
        ser["n_pos"].append(diag["n_pos"])
        ser["n_neg"].append(diag["n_neg"])
        ser["n_blobs"].append(diag["n_blobs"])
        if record_fields and blk % 2 == 0:
            e_tot = f.energy_density_total(U, dx, e_sk)
            bdens = s.baryon_density(U, dx)
            snaps.append({"t": t, "e": e_tot[:, :, kz].tolist(),
                          "b": bdens[:, :, kz].tolist()})
        U, w, _ = f.chiral_evolve_fast(U, w, dx, dt, record_every, e_sk)
        t += record_every * dt

    Q = np.array(ser["Q_top"])
    Bser = np.array(ser["B"])
    half = len(Q) // 2
    Q0 = float(Q[0]) if Q[0] > 0 else 1e-9
    out = {"seed": seed, "v_frac": v_frac, "v_lattice": v, "b": b, "KE0": KE0,
           "dx": dx, "n_blocks": len(Q), "series": ser,
           "B_abs_max": float(np.max(np.abs(Bser))),
           "Q_top_0": Q0, "Q_top_late": float(Q[-1]),
           "Q_top_late_ratio": float(Q[half:].mean() / Q0),
           "Q_top_peak_ratio": float(Q[half:].max() / Q0)}
    if record_fields:
        out["snaps"] = snaps
    return out, dx


def classify(r):
    """Identical to FL3: creation if late Q_top rises >1.5x the initial 2-soliton content;
    annihilation if it collapses <0.3x; elastic otherwise."""
    if r["Q_top_peak_ratio"] > 1.5:
        return "creation"
    if r["Q_top_late_ratio"] < 0.3:
        return "annihilation"
    return "elastic"


def save_json(name, payload):
    p = OUT / f"{name}.json"
    p.write_text(json.dumps(payload, indent=2, default=float))
    return p
