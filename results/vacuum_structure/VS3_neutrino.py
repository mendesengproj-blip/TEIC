"""VS3 -- does the network support a QUASI-STABLE, GAUGE-NEUTRAL spin-1/2-marked
defect (a 'neutrino' candidate)?

Charter: VACUUM_STRUCTURE.md (VS3).  The charter asks for a localized object
that carries the spin-1/2 (double-cover) structure but NO U(1) gauge winding,
and to measure its lifetime.

Construction (the pi-TWIST BALL): on the SU(2) chiral lattice (su2_core,
quaternions, no Pauli/complex),

    U(x) = exp(i F(r) sigma_3)   with   F(0) = pi,  F(inf) = 0,

i.e. a FIXED-axis (abelian-embedded) twist whose centre sits at the ANTIPODE
-1.  Its topological book-keeping:

  * Z2 (spin-1/2) MARKER: a radial line carries the path 1 -> -1, which
    projects to the CLOSED non-contractible loop of SO(3) = the generator of
    pi_1(SO(3)) = Z2 -- exactly the double-cover structure Finkelstein-
    Rubinstein quantisation reads (MATTER_FR_EXCHANGE / PI1_B2).
  * NO gauge winding: F depends only on r, so the embedded-U(1) phase has
    zero winding around every loop (analytic; the azimuthal gradient is 0).
  * B = 0: the baryon current is a commutator determinant, identically zero
    for a fixed-axis (abelian) configuration -- measured below.
  * NOT protected: maps S^3 -> S^3 with B=0 are connected to the vacuum, so
    stability, if any, must be DYNAMICAL (a local minimum / long lifetime),
    not topological.  That is precisely the charter's question.

Controls:
  * trivial bump  F(0) = pi/2 (same shape, no antipode, no Z2 marker);
  * hedgehog B=1 (same profile, radial axis) -- topologically protected
    positive control (SU3: stable with Skyrme).

Measurements (both with the Skyrme term, e_sk = 4, the SU3 reference):
  (A) GRADIENT FLOW (chiral_cool): iterations until the antipode is lost
      (min a_0 rises above -0.5) -- the 'relaxation lifetime' tau_flow.  A
      metastable object shows a plateau; an unprotected transient unwinds
      monotonically on the same scale as the control.
  (B) REAL-TIME (chiral_evolve, geodesic leapfrog, w0=0): time until the
      antipode is lost, tau_dyn, plus energy bookkeeping.

Kill criterion (pre-registered): the Z2-marked neutral object unwinds on the
same scale as the trivial control (no plateau, no metastability) -- every
spin-1/2 carrier needs gauge/topological winding; no neutral quasi-defect.

Anti-circularity: quaternions only (4 real components); 'neutrino', 'spin'
appear only as names; no mass/lifetime target inserted.  Deterministic
initial data (no seeds needed); lattice and e_sk fixed in advance.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s    # noqa: E402

OUTDIR = Path(__file__).resolve().parent

N, L = 33, 11.0                      # dx ~ 1/3: the SU3 resolution class.
                                     # FIRST RUN at dx=0.5 was INVALID: the
                                     # protected hedgehog control ALSO unwound
                                     # (B 0.88 -> 0, tau_flow=28) -- the
                                     # coarse-lattice B leak VS4 documented.
                                     # A comparison needs the control to hold.
E_SK = 4.0
W_PROF = 0.18 * L                    # su2_core default profile width
COOL_ITERS = 500
COOL_RATE = 0.001                    # stability-tested at dx=0.344: 0.002
                                     # diverges after ~4 iters; 0.001 descends
COOL_SAMPLE = 5                      # record marker every 5 iters
DYN_CHUNK, DYN_NCHUNK = 12, 10       # 120 leapfrog steps, marker every chunk
ANTIPODE_LOST = -0.5                 # min(a0) above this => Z2 marker gone


def grid():
    xs = np.linspace(-L / 2, L / 2, N)
    return xs, float(xs[1] - xs[0])


def F_of_r(r, F0):
    return F0 * np.exp(-r / W_PROF)


def twist_ball(xs, F0):
    """Fixed-axis (sigma_3) twist: U = (cos F, 0, 0, sin F)."""
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    r = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    F = F_of_r(r, F0)
    U = np.zeros(X.shape + (4,))
    U[..., 0] = np.cos(F)
    U[..., 3] = np.sin(F)
    return s.q_normalize(U)


def hedgehog(xs):
    return s.hedgehog_field(xs, xs, xs,
                            profile=lambda r: F_of_r(r, np.pi))


def markers(U, dx):
    a0min = float(U[..., 0].min())
    B = s.baryon_number(U, dx)
    E2, E4, Et = s.chiral_energy(U, dx, E_SK)
    return {"a0_min": a0min, "B": float(B), "E": float(Et)}


def flow_lifetime(U, dx, label):
    """Cool and record the antipode marker each iteration (re-implemented loop
    around chiral_force so the marker is sampled; identical update rule to
    su2_core.chiral_cool)."""
    U = s.q_normalize(U.copy())
    track = []
    tau = None
    for it in range(COOL_ITERS):
        F = s.chiral_force(U, dx, E_SK)
        U = s.q_normalize(U + COOL_RATE * F)
        U = s._clamp_far(U)
        if (it + 1) % COOL_SAMPLE and it + 1 != COOL_ITERS:
            continue
        m = markers(U, dx)
        m["iter"] = it + 1
        track.append(m)
        if tau is None and m["a0_min"] > ANTIPODE_LOST:
            tau = it + 1
    print(f"  [flow] {label:14s} tau_flow={tau}  "
          f"a0_min(final)={track[-1]['a0_min']:+.3f}  "
          f"E(final)={track[-1]['E']:.2f}  B(final)={track[-1]['B']:+.3f}")
    return tau, track, U


def dyn_lifetime(U, dx, label):
    U = s.q_normalize(U.copy())
    w = np.zeros(U.shape[:-1] + (3,))
    dt = 0.04 * dx
    track = []
    tau = None
    t = 0.0
    for chunk in range(DYN_NCHUNK):
        U, w, hist = s.chiral_evolve(U, w, dx, dt, DYN_CHUNK, E_SK,
                                     record_B=False)
        t += DYN_CHUNK * dt
        m = markers(U, dx)
        m["t"] = t
        track.append(m)
        if tau is None and m["a0_min"] > ANTIPODE_LOST:
            tau = t
    print(f"  [dyn ] {label:14s} tau_dyn={tau}  "
          f"a0_min(final)={track[-1]['a0_min']:+.3f}  "
          f"E(final)={track[-1]['E']:.2f}")
    return tau, track


def main():
    xs, dx = grid()
    configs = {
        "pi_twist":  twist_ball(xs, np.pi),        # Z2-marked, neutral
        "half_bump": twist_ball(xs, 0.5 * np.pi),  # trivial control
        "hedgehog":  hedgehog(xs),                 # protected control (B=1)
    }

    print("initial book-keeping (N=%d, dx=%.3f, e_sk=%.1f):" % (N, dx, E_SK))
    init = {}
    for k, U in configs.items():
        m = markers(U, dx)
        init[k] = m
        print(f"  {k:14s} a0_min={m['a0_min']:+.3f}  B={m['B']:+.4f}  "
              f"E={m['E']:.2f}")

    print("\n(A) gradient flow (cooling, %d iters):" % COOL_ITERS)
    flow = {}
    for k, U in configs.items():
        tau, track, _ = flow_lifetime(U, dx, k)
        flow[k] = {"tau_flow": tau, "track": track}

    print("\n(B) real-time evolution (geodesic leapfrog):")
    dyn = {}
    for k, U in configs.items():
        tau, track = dyn_lifetime(U, dx, k)
        dyn[k] = {"tau_dyn": tau, "track": track}

    payload = {"params": {"N": N, "L": L, "dx": dx, "e_sk": E_SK,
                          "w_profile": W_PROF, "cool_iters": COOL_ITERS,
                          "cool_rate": COOL_RATE,
                          "dyn_steps": DYN_CHUNK * DYN_NCHUNK,
                          "antipode_lost_level": ANTIPODE_LOST},
               "initial": init, "flow": flow, "dyn": dyn}
    (OUTDIR / "VS3_neutrino.json").write_text(
        json.dumps(payload, indent=2, default=float))
    print("\nsaved VS3_neutrino.json")


if __name__ == "__main__":
    main()
