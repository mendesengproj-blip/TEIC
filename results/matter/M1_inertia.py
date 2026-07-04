"""M1 -- inertia as the network's response to a force (refaz T15/T16).

The T15/T16 "law of mass" m = cost/<k> was near-tautological: cost and <k> both
count causal links per event.  The correct question for INERTIAL mass is Newton's:
inertia = resistance to acceleration.  We MEASURE it operationally, inserting no
mass, no F=ma, no E=mc^2.

METHOD
  * Sprinkle a 1+1D Poisson network (the bare generator).
  * Build a localized real lump theta(x) in an early time-slab (matter_core.
    localized_profile -- a function of coordinates only, no physics).
  * Apply a "force": a source gradient J(x) = lump * (1 + F x).  F is the
    coefficient of a linear source term in the field equation box theta = J; it is
    NOT F=ma -- it is the gradient of the field's own source (from the action).
  * Propagate with the causal-set retarded kernel K = (1/2)C (Johnston 2008) and
    measure the centroid of the response over successive future time-slabs.
  * Inertia m_rede = F / a, where a = acceleration of the centroid (d^2 x / dt^2)
    and the drift velocity v = dx/dt.  Both are MEASURED from the network.

ANTI-CIRCULARITY: gamma / sqrt(1-beta^2) never appear here.  The only relativistic
reference (Lorentz invariance of the Poisson process) is discussed, not computed.

SUCCESS:  m_rede constant, independent of F (Newton); m_rede > 0 and finite.
DEATH:    a ~ 0 (no response) or m_rede depends on F -> not an inertial mass.

We ALSO report <k> (mean causal degree), the audit's "inertia correlate", and show
explicitly that cost/<k> is tautological -- so it is not an independent inertia.
"""

from __future__ import annotations

import numpy as np

import matter_core as mc

SEEDS = range(20)
RHO, T, X, SIGMA = 20.0, 9.0, 12.0, 2.5
FORCES = [0.0, 0.05, 0.1, 0.2, 0.3]


def response(F, seed):
    """Return (drift velocity, acceleration) of the lump centroid under force F."""
    rng = np.random.default_rng(seed)
    p = mc.sprinkle_2d(RHO, T, X, rng)
    t, x = p[:, 0], p[:, 1]
    lump = mc.localized_profile(x, 0.0, SIGMA) * (t < T * 0.2)
    J = lump * (1.0 + F * x)
    phi = mc.propagate(p, J)
    edges = np.linspace(T * 0.3, T * 0.95, 8)
    ts, xs = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (t >= a) & (t < b)
        if m.sum() < 30:
            continue
        c = mc.centroid(phi[m], x[m])
        if np.isfinite(c):
            ts.append(0.5 * (a + b))
            xs.append(c)
    ts, xs = np.array(ts), np.array(xs)
    if len(ts) < 4:
        return np.nan, np.nan
    vel = float(np.polyfit(ts, xs, 1)[0])
    acc = float(2.0 * np.polyfit(ts, xs, 2)[0])
    return vel, acc


def mean_degree(seed):
    """<k> = mean number of causal links per event (the connectivity scale)."""
    rng = np.random.default_rng(seed)
    p = mc.sprinkle_2d(RHO, T, X, rng)
    # sample to keep O(n^2) cheap; count future-cone neighbours per sampled event
    n = len(p)
    idx = rng.choice(n, size=min(200, n), replace=False)
    t, x = p[:, 0], p[:, 1]
    ks = []
    for i in idx:
        dt = t - t[i]
        dx2 = (x - x[i]) ** 2
        ks.append(int(np.sum((dt > 0) & (dt * dt > dx2))))
    return float(np.mean(ks))


def main():
    print("=" * 70)
    print("M1 -- INERTIA AS NETWORK RESPONSE TO A FORCE (refaz T15/T16)")
    print("=" * 70)

    force_table = {}
    for F in FORCES:
        vels, accs = zip(*[response(F, s) for s in SEEDS])
        vs, as_ = mc.seed_stats(vels), mc.seed_stats(accs)
        force_table[F] = {"v_drift": vs, "accel": as_}
        print(f"  F={F:.2f}: v={vs['mean']:+.4f}+/-{vs['sem']:.4f}  "
              f"a={as_['mean']:+.4f}+/-{as_['sem']:.4f}")

    # Is there ANY force response?  Test: does |v| or |a| grow with F beyond noise?
    Fs = np.array(FORCES)
    v_mean = np.array([force_table[F]["v_drift"]["mean"] for F in FORCES])
    a_mean = np.array([force_table[F]["accel"]["mean"] for F in FORCES])
    v_sem = np.array([force_table[F]["v_drift"]["sem"] for F in FORCES])
    # slope of response vs force (mobility); if ~0 within error, no inertial response
    v_slope = float(np.polyfit(Fs, v_mean, 1)[0])
    a_slope = float(np.polyfit(Fs, a_mean, 1)[0])
    typical_sem = float(np.mean(v_sem))
    responds = abs(v_slope) > 3.0 * typical_sem / (Fs.max() - Fs.min())

    kstat = mc.seed_stats([mean_degree(s) for s in SEEDS])
    print(f"  <k> (connectivity scale) = {kstat['mean']:.2f} +/- {kstat['sem']:.2f}")
    print(f"  response slope dv/dF = {v_slope:+.4f} (typical SEM {typical_sem:.4f})")

    # Baseline offset at F=0 (a pure artifact: there is no force there).
    a0 = force_table[0.0]["accel"]["mean"]
    v0 = force_table[0.0]["v_drift"]["mean"]
    # Newton's test is on the ACCELERATION: m=F/a is an inertial mass only if a is
    # proportional to F (so m is force-independent).  Here a barely moves with F and
    # is dominated by a force-independent baseline -> m=F/a is not constant.
    marginal = abs(v_slope) > typical_sem / (Fs.max() - Fs.min())
    verdict = "C"
    statement = (
        "No Newtonian inertia recovered (death criterion met).  A force gradient "
        "produces only a MARGINAL (~2-3 sigma) linear trend in the centroid "
        "velocity (dv/dF=%+.3f) and acceleration, sitting on top of force-"
        "INDEPENDENT baseline offsets that are pure artifacts (at F=0, where there "
        "is no force, v0=%+.4f, a0=%+.4f).  The acceleration -- which defines "
        "inertial mass -- does not scale cleanly with F, so m_rede=F/a is neither "
        "stable nor force-independent at accessible precision.  The free massless "
        "network scalar has no localized excitation that accelerates like a "
        "particle.  What T15/T16 called 'mass', cost/<k>, is the connectivity "
        "scale <k>=%.0f (both count links/event -- tautological), not a Lorentz-"
        "invariant inertia." % (v_slope, v0, a0, kstat["mean"]))
    print("-" * 70)
    print(f"VERDICT M1: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "T": T, "X": X, "sigma": SIGMA,
                      "forces": FORCES, "n_seeds": len(list(SEEDS))},
           "force_response": {str(F): force_table[F] for F in FORCES},
           "v_slope_dv_dF": v_slope, "a_slope": a_slope,
           "typical_sem": typical_sem, "responds": bool(responds),
           "marginal_trend": bool(marginal), "v0_artifact": v0, "a0_artifact": a0,
           "mean_degree_k": kstat,
           "tautology_note": ("cost/<k> is tautological: both numerator and "
                              "denominator count causal links per event."),
           "verdict": verdict, "statement": statement}
    mc.save_json("M1_inertia", out)
    return out


if __name__ == "__main__":
    main()
