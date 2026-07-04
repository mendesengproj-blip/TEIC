"""creation_core.py -- shared engine for the MATTER_CREATION campaign (CR1-CR6).

Tests whether the collision of dense causal chains spontaneously creates internal
cycles (loops = matter) under the linear Benincasa-Dowker dynamics, and whether the
total causal rate is conserved.  Complementary to CC1-CC6 (which BUILT loops); here
the DYNAMICS must decide the topology.  Modifies nothing in R1-R3 / e6-e11 / D1-D3 /
M1-S1; reuses the bare Poisson generator of src/causal_core.py and the loop/field
helpers of the complexity campaign.

ANTI-CIRCULARITY (scanned by tests/test_no_circularity.py over results/matter/):
  * Energy, mc^2, the QED pair threshold 2mc^2, electron, positron NEVER enter a
    generator.  "Causal energy" E_causal and loop counts are integer counts.
  * No special-/general-relativistic dilation formula; boosts are rapidity (cosh/
    sinh) coordinate maps.  No complex numbers.

How "creation" is probed -- two decisive, honest observables (both counted)
--------------------------------------------------------------------------
(1) FIELD level.  The retarded propagator K = (1/2) C (Johnston 2008) and the smeared
    d'Alembertian are LINEAR, so theta(J_A + J_B) = theta(J_A) + theta(J_B) exactly.
    The superposition residual is ~ machine epsilon for ANY density -- a decisive,
    energy-independent demonstration that the field creates no new structure.  We
    MEASURE it; we do not assert it.

(2) TOPOLOGY level.  A dense 2D causal set has MANY geometric "diamonds", so the
    absolute Betti number of the covering graph is an artifact of local density (the
    detector check below shows a CC structure embedded in Minkowski reads far above
    its built-in N).  The genuine collision signature is therefore NOT absolute Betti
    but the BICHROMATIC cross-links: covering (Hasse) edges that join an A-chain event
    to a B-chain event.  These exist only where the two chains share a causal region.
    A bound state (created matter) keeps A and B causally interwoven AFTER the
    crossing; a pass-through (free radiation) lets them separate, so the LATE-TIME
    cross-link density returns to ~ its disjoint baseline.  The persistent late-time
    cross-link excess is the matter-creation order parameter.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "complexity"))

from causal_core import causal_matrix  # noqa: E402
import complexity_core as cx  # noqa: E402

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

RHO0 = 1.0            # background density unit (chain densities measured in rho/rho0)
SEEDS = range(20)
T_SPAN = 9.0
VEL = 0.9
WIDTH = 0.4


# --------------------------------------------------------------------------- #
# Causal chains as tubes of events (pure geometry -- no physics)
# --------------------------------------------------------------------------- #
def sprinkle_tube(rho_chain, t0, t1, x0, vel, width, rng):
    """Poisson events in a thin tube around the worldline x = x0 + vel*(t-t0).

    rho_chain = events per unit coordinate area inside the half-width ``width`` tube;
    vel is the chain velocity.  Returns (n,2) (t,x).  "Causal energy" = count rate.
    """
    area = (t1 - t0) * 2.0 * width
    n = rng.poisson(rho_chain * area)
    t = rng.uniform(t0, t1, n)
    center = x0 + vel * (t - t0)
    x = center + rng.uniform(-width, width, n)
    return np.column_stack([t, x])


def collision(rho_chain, seed, mode="headon", t_span=T_SPAN, vel=VEL, width=WIDTH,
              x_meet=0.0, sep=8.0):
    """Two chains. 'headon': A(+vel) from left and B(-vel) from right cross at
    (t_span/2, x_meet).  'disjoint': the same two chains pulled sep apart so they
    never share a causal region (the no-collision baseline).  A's events come first.
    """
    rng = np.random.default_rng(seed)
    tmid = t_span / 2.0
    shift = 0.0 if mode == "headon" else sep
    A = sprinkle_tube(rho_chain, 0, t_span, x_meet - vel * tmid - shift, +vel, width, rng)
    B = sprinkle_tube(rho_chain, 0, t_span, x_meet + vel * tmid + shift, -vel, width, rng)
    ev = np.vstack([A, B])
    color = np.concatenate([np.zeros(len(A), int), np.ones(len(B), int)])
    return {"events": ev, "color": color, "nA": len(A), "nB": len(B),
            "t_collision": tmid, "x_meet": x_meet}


# --------------------------------------------------------------------------- #
# Covering (Hasse) graph and bichromatic cross-links
# --------------------------------------------------------------------------- #
def covering_edges(events):
    """Covering relation: pairs (i,j) with i<j and no k with i<k<j  =  C & ~(C@C)."""
    if len(events) < 2:
        return np.empty((0, 2), dtype=int)
    C = causal_matrix(events)
    Ci = C.astype(np.int32)
    cover = C & ~((Ci @ Ci) > 0)
    ii, jj = np.nonzero(cover)
    return np.column_stack([ii, jj])


def loop_count(events):
    """First Betti number of the undirected covering graph (geometric; see module
    docstring -- use only differentially)."""
    return cx.betti(len(events), covering_edges(events))


def _bichromatic_in_window(ev, color, edges, t_lo=None, t_hi=None):
    """Count covering edges joining different colours, optionally with both endpoints
    in [t_lo, t_hi].  Takes precomputed ``edges`` so the O(n^3) covering is done once."""
    if len(edges) == 0:
        return 0
    i, j = edges[:, 0], edges[:, 1]
    bich = color[i] != color[j]
    if t_lo is not None:
        t = ev[:, 0]
        win = (t[i] >= t_lo) & (t[i] <= t_hi) & (t[j] >= t_lo) & (t[j] <= t_hi)
        bich = bich & win
    return int(np.sum(bich))


def cross_links(config, t_lo=None, t_hi=None):
    """Number of covering edges that join an A event to a B event (bichromatic),
    optionally restricted to edges whose endpoints both lie in [t_lo, t_hi].

    This is the count of causal "bridges" between the two chains -- the order
    parameter for them being interwoven (bound) vs separated (pass-through).
    """
    ev, color = config["events"], config["color"]
    return _bichromatic_in_window(ev, color, covering_edges(ev), t_lo, t_hi)


# --------------------------------------------------------------------------- #
# Causal energy (counting) and the linear retarded field
# --------------------------------------------------------------------------- #
def e_causal(events, t0, t1):
    """Causal energy = events per unit proper time-length = n / (t1 - t0).  A count
    rate; no energy inserted."""
    return len(events) / (t1 - t0)


def retarded_field(events, source):
    """theta = K @ source, K = (1/2) C^T (Johnston retarded kernel).  LINEAR."""
    C = causal_matrix(events)
    K = 0.5 * C.T.astype(float)
    return K @ np.asarray(source, dtype=float)


def superposition_residual(config):
    """|| theta(A+B) - theta(A) - theta(B) || / || theta(A)+theta(B) ||.

    Each chain event is a unit source on its own chain.  ~ machine epsilon for any
    linear dynamics: density-independent proof of no field-level creation.
    """
    color = config["color"]
    src_A = (color == 0).astype(float)
    src_B = (color == 1).astype(float)
    ev = config["events"]
    tA = retarded_field(ev, src_A)
    tB = retarded_field(ev, src_B)
    tAB = retarded_field(ev, src_A + src_B)
    num = float(np.linalg.norm(tAB - (tA + tB)))
    den = float(np.linalg.norm(tA + tB))
    return num / den if den > 0 else float("nan")


def central_density_excess(config, t_lo, t_hi, half=1.0):
    """Late-time persistent over-density at the collision centre.

    Counts events in the box [t_lo,t_hi] x [x_meet +/- half] for the head-on case and
    subtracts the disjoint baseline (where the chains never meet there).  A bound state
    (created matter) leaves a persistent central clump (> 0); a pass-through leaves the
    centre empty at late time (~ 0).
    """
    ev = config["events"]
    x0 = config["x_meet"]
    t, x = ev[:, 0], ev[:, 1]
    return int(np.sum((t >= t_lo) & (t <= t_hi) & (np.abs(x - x0) <= half)))


def collision_observables(rho, seed):
    """All creation order parameters for one collision, head-on vs disjoint control.

    Returns:
      residual    -- field superposition residual (linearity proof, ~ 0)
      cross_mid   -- bichromatic covering links during the encounter (transient)
      cross_late  -- bichromatic covering links AFTER the encounter (bound -> > 0)
      central_late-- persistent central over-density vs disjoint baseline (bound -> >0)
    """
    head = collision(rho, seed, "headon")
    disj = collision(rho, seed, "disjoint")
    tc = head["t_collision"]
    lo, hi = tc + 2.0, T_SPAN
    # one O(n^3) covering for the head-on case; reuse it for mid and late windows.
    edges = covering_edges(head["events"])
    ev, color = head["events"], head["color"]
    cross_mid = _bichromatic_in_window(ev, color, edges, tc - 1.5, tc + 1.5)
    cross_late_head = _bichromatic_in_window(ev, color, edges, lo, hi)
    # disjoint chains share no causal region, so their bichromatic cross-links are
    # structurally zero; the central baseline is a cheap O(n) count.
    cen_head = central_density_excess(head, lo, hi)
    cen_disj = central_density_excess(disj, lo, hi)
    return {"residual": superposition_residual(head),
            "cross_mid": cross_mid,
            "cross_late": cross_late_head,           # minus disjoint (= 0)
            "central_late": cen_head - cen_disj}


# --------------------------------------------------------------------------- #
# Stats + IO
# --------------------------------------------------------------------------- #
def seed_stats(values):
    return cx.seed_stats(values)


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    # detector sanity: clean isolated diamond -> 1 cycle, a straight chain -> 0
    diamond = np.array([[0., 0.], [0.5, 0.3], [0.5, -0.3], [1., 0.]])
    chain = np.array([[0., 0.], [0.7, 0.], [1.4, 0.], [2.1, 0.]])
    print(f"clean diamond Betti = {loop_count(diamond)} (want 1)")
    print(f"straight chain Betti = {loop_count(chain)} (want 0)")
    print("NOTE: absolute Betti of a DENSE causal set is geometric, not the built N "
          "-- hence we use bichromatic cross-links differentially.")
    print("collision smoke (cross-links mid vs late):")
    for rho in (10.0, 50.0):
        cfg = collision(rho, 0, "headon")
        tc = cfg["t_collision"]
        mid = np.mean([cross_links(collision(rho, s, "headon"), tc - 1.5, tc + 1.5)
                       for s in range(5)])
        late = np.mean([cross_links(collision(rho, s, "headon"), tc + 3, T_SPAN)
                        for s in range(5)])
        print(f"  rho={rho:5.0f}: <cross_mid>={mid:.1f}  <cross_late>={late:.1f}")
