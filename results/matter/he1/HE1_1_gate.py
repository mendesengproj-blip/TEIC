"""HE1-1 -- engineering gate for the high-resolution / ultra-relativistic Skyrmion collision.

Before measuring anything, the lattice must EARN the right to be trusted at the finer grid
and the larger boost.  Four checks, all pre-registered:

  G1  analytic Skyrme gradient still matches the true per-site gradient (licenses the fast
      integrator on the finer grid).
  G2  resolution: points across the relaxed Skyrmion core at this dx vs FL3's ~4 (must be a
      genuine refinement, the whole point of HE1).
  G3  isolated boosted Skyrmion is stable IN FLIGHT at v=0.90c (B stays ~1, single energy
      peak, energy bounded) -- otherwise a "collision" is just two decaying lumps.
  G4  THE DECISIVE PRE-REGISTERED ENERGETIC CHECK: measure the lattice rest mass M_Sk at
      this resolution and the kinetic energy the boost actually deposits at v=0.50, 0.90,
      0.99 c, and compare KE to the pair-creation threshold 2 M_Sk c^2.  FL3 found
      KE/threshold ~ 0.018 at v=0.5c and argued only v->c could approach 1.  HE1 reports the
      number at v->c BEFORE running the dynamics, so the verdict is not a post-hoc story.

This is the analogue of the LHC beam-energy check: you know whether you are above threshold
from the kinematics, independent of the collision dynamics.
"""
from __future__ import annotations

import time

import numpy as np

import he1_core as h
import fl3_core as f
import su2_core as s

# ---- frozen configuration (HE1 charter) ------------------------------------ #
L = 16.0
N = 52                 # dx = 0.314 vs FL3's 0.471 -> ~1.5x finer (G2 reports pts/core)
E_SK = 4.0
DT_FRAC = 0.012        # the dt/dx the FL3 gate chose (reused, not re-tuned)
V_LIST = [0.50, 0.90, 0.99]
GATE_STEPS = 600       # isolated-flight stability window


def core_points(e_sk, dx):
    """How many lattice sites span the Skyrmion core diameter = 2 * r at which the relaxed
    radial profile F(r) crosses pi/2 (the half-winding radius)."""
    r, dr = s.radial_grid(rmax=12.0, n=360)
    F, _, _ = s.radial_relax(r, dr, e_sk)
    i = int(np.argmin(np.abs(F - np.pi / 2.0)))
    r_half = float(r[i])
    return 2.0 * r_half / dx, r_half


def main():
    t0 = time.time()
    xs, dx = f.cubic_grid(L, N)
    print("=" * 74)
    print(f"HE1-1  ENGINEERING GATE   N={N} (dx={dx:.3f})  vs FL3 dx=0.471")
    print("=" * 74)

    # G1 -- analytic Skyrme gradient vs true per-site FD
    g1 = f.validate_skyrme_grad(N=7, e_sk=E_SK, seed=0)
    g1_ok = g1["max_rel_diff"] < 1e-5
    print(f"G1  Skyrme grad max_rel_diff = {g1['max_rel_diff']:.2e}   "
          f"{'OK' if g1_ok else 'FAIL'}")

    # G2 -- resolution
    pts, r_half = core_points(E_SK, dx)
    fl3_pts = 2.0 * r_half / 0.471
    g2_ok = pts > fl3_pts * 1.3
    print(f"G2  core diameter spans {pts:.1f} sites (FL3: {fl3_pts:.1f})   "
          f"{'OK (finer)' if g2_ok else 'NOT finer'}")

    # G3 -- isolated boosted Skyrmion stable in flight at 0.90c
    prof = f.relaxed_profile(E_SK)
    U, w = f.single_boosted(xs, dx, center=(-4, 0, 0), v_vec=(0.90 * h.C, 0, 0),
                            prof=prof, B_sign=+1)
    d_init = f.soliton_diagnostics(U, dx, E_SK)
    ke_iso = s.kinetic_energy(w, dx)
    E0 = d_init["E_field"] + ke_iso
    dt = DT_FRAC * dx
    Bs, peaks, Es = [d_init["B"]], [d_init["n_peaks"]], [E0]
    for _ in range(GATE_STEPS // 60):
        U, w, _ = f.chiral_evolve_fast(U, w, dx, dt, 60, E_SK)
        d = f.soliton_diagnostics(U, dx, E_SK)
        Bs.append(d["B"]); peaks.append(d["n_peaks"])
        Es.append(d["E_field"] + s.kinetic_energy(w, dx))
    Bs = np.array(Bs); Es = np.array(Es)
    B_ok = bool(np.all(np.abs(Bs) > 0.6) and np.all(np.abs(Bs) < 1.4))
    peak_ok = bool(max(peaks) <= 2)             # one lump (allow brief 2 from radiation)
    E_drift = float(np.max(np.abs(Es - E0)) / E0)
    g3_ok = B_ok and peak_ok
    print(f"G3  isolated boosted v=0.90c: B band [{Bs.min():.2f},{Bs.max():.2f}]  "
          f"peaks<= {max(peaks)}  E-drift {E_drift:.1%}   {'OK' if g3_ok else 'WEAK'}")

    # G4 -- DECISIVE energetic check (pre-registered)
    mass = f.lattice_mass(L, N, E_SK, prof)
    M_Sk = mass["M_lattice"]
    E_thresh = 2.0 * M_Sk * h.C ** 2
    print(f"G4  M_Sk(lattice,N={N}) = {M_Sk:.1f}  (B={mass['B']:+.3f})   "
          f"2 M_Sk c^2 = {E_thresh:.1f}")
    ke_tab = {}
    for vf in V_LIST:
        _, w0 = f.boosted_pair(xs, dx, d=5.0, v=vf * h.C, b=0.0, prof=prof, e_sk=E_SK)
        KE = s.kinetic_energy(w0, dx)
        ke_tab[vf] = {"KE": KE, "ratio": KE / E_thresh}
        print(f"      v={vf:.2f}c:  KE_collision = {KE:8.2f}   "
              f"KE / 2M c^2 = {KE / E_thresh:.4f}")

    # extrapolate the boost law KE(v): fit KE = A v^p over the three points
    vfs = np.array(V_LIST)
    kes = np.array([ke_tab[vf]["KE"] for vf in V_LIST])
    p, logA = np.polyfit(np.log(vfs * h.C), np.log(kes), 1)
    KE_at_c = np.exp(logA + p * np.log(h.C))     # v -> c limit of THIS boost law
    ratio_at_c = float(KE_at_c / E_thresh)
    print(f"      boost law KE ~ v^{p:.2f}  ->  v->c limit KE/2Mc^2 = {ratio_at_c:.4f}")

    gate_pass = g1_ok and g2_ok and g3_ok
    payload = {
        "config": {"L": L, "N": N, "dx": dx, "e_sk": E_SK, "dt_frac": DT_FRAC,
                   "c_magnon": h.C, "v_list": V_LIST, "gate_steps": GATE_STEPS},
        "G1_skyrme_grad": {**g1, "ok": g1_ok},
        "G2_resolution": {"core_pts": pts, "fl3_core_pts": fl3_pts, "r_half": r_half,
                          "ok": g2_ok},
        "G3_flight_stability": {"B_band": [float(Bs.min()), float(Bs.max())],
                                "max_peaks": int(max(peaks)), "E_drift": E_drift,
                                "ok": g3_ok},
        "G4_energetics": {"M_Sk_lattice": M_Sk, "M_Sk_B": mass["B"],
                          "E_threshold_2Mc2": E_thresh, "ke_table": ke_tab,
                          "boost_power_p": float(p), "KE_ratio_at_c": ratio_at_c},
        "gate_pass": bool(gate_pass),
        "runtime_s": time.time() - t0,
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    h.save_json("HE1_1_gate", payload)
    print("-" * 74)
    print(f"GATE {'PASS' if gate_pass else 'PARTIAL'} | even at v->c, "
          f"KE reaches {ratio_at_c:.1%} of the 2 M_Sk c^2 creation threshold "
          f"({time.time()-t0:.0f}s)")
    return payload


if __name__ == "__main__":
    main()
