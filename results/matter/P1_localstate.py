"""P1 -- localized stable state? (refaz T20).

T20's 'particles' were hand-drawn helices.  The correct question: does the causal
network support a state that is (a) localized, (b) stable under evolution, (c) moves
coherently?  We do not draw one; we source a localized real lump and let the network
propagate it under its OWN dynamics (the retarded propagator of the box operator),
then measure whether it stays localized.

METHOD
  * Sprinkle a 1+1D Poisson network.
  * Source a localized lump theta(x)=exp(-x^2/2 sigma0^2) in an early thin slab.
  * Propagate with the causal-set retarded kernel K=(1/2)C (Johnston 2008): this is
    the network's massless box dynamics, not inserted by hand.
  * Measure the spatial width sigma(t) of |theta| at successive later slabs and fit
    sigma(t) ~ t^p:  p~0 stable; p~1/2 diffusive dispersion; p~1 ballistic light-cone
    spreading.  Also measure flatness (does the profile keep a peak or go flat?).

ANTI-CIRCULARITY: no wave equation, no dispersion relation, no mass inserted; the
dynamics is the retarded Green's function of the causal order.

SUCCESS: sigma(t) ~ const -> a genuine localized stable state.
DEATH:   sigma(t) grows -> no localized stable rest-state (report the growth law).
"""

from __future__ import annotations

import numpy as np

import matter_core as mc

SEEDS = range(20)
RHO, T, X, SIGMA0 = 22.0, 10.0, 16.0, 1.6


def width_profile(seed):
    rng = np.random.default_rng(6000 + seed)
    p = mc.sprinkle_2d(RHO, T, X, rng)
    t, x = p[:, 0], p[:, 1]
    J = mc.localized_profile(x, 0.0, SIGMA0) * (t < T * 0.12)
    phi = mc.propagate(p, J)
    edges = np.linspace(T * 0.2, T * 0.95, 8)
    ts, sg, flat = [], [], []
    for a, b in zip(edges[:-1], edges[1:]):
        m = (t >= a) & (t < b)
        if m.sum() < 40:
            continue
        w = np.abs(phi[m])
        if w.sum() <= 0:
            continue
        ts.append(0.5 * (a + b))
        sg.append(mc.spread(w, x[m]))
        # flatness: ratio of central density to mean density (1 = flat plateau)
        xc = x[m]
        central = w[np.abs(xc) < 2.0].mean() if np.any(np.abs(xc) < 2.0) else np.nan
        flat.append(central / w.mean() if w.mean() > 0 else np.nan)
    return np.array(ts), np.array(sg), np.array(flat)


def main():
    print("=" * 70)
    print("P1 -- LOCALIZED STABLE STATE? (refaz T20)")
    print("=" * 70)

    # accumulate sigma(t) across seeds on a common time grid
    all_ts, all_sg, exps, flats0, flats1 = None, [], [], [], []
    sg_by_seed = []
    for s in SEEDS:
        ts, sg, fl = width_profile(s)
        if len(ts) < 4:
            continue
        all_ts = ts
        sg_by_seed.append(sg)
        # fit log sigma = p log t
        good = (ts > 0) & (sg > 0)
        p_exp = float(np.polyfit(np.log(ts[good]), np.log(sg[good]), 1)[0])
        exps.append(p_exp)
        flats0.append(fl[0]); flats1.append(fl[-1])
    sg_arr = np.array(sg_by_seed)
    sg_mean, sg_sem = sg_arr.mean(0), sg_arr.std(0) / np.sqrt(len(sg_arr))
    p_stat = mc.seed_stats(exps)
    f0, f1 = mc.seed_stats(flats0), mc.seed_stats(flats1)

    for i, tt in enumerate(all_ts):
        print(f"  t={tt:4.1f}: sigma={sg_mean[i]:5.2f} +/- {sg_sem[i]:.2f}")
    print(f"  growth exponent p (sigma~t^p) = {p_stat['mean']:.2f} +/- {p_stat['sem']:.2f}")
    print(f"  central/mean flatness: early={f0['mean']:.2f} late={f1['mean']:.2f} "
          f"(->1 means a flat plateau, no peak)")

    stable = p_stat["mean"] < 0.2
    ballistic = abs(p_stat["mean"] - 1.0) < 0.35
    if stable:
        verdict = "B"
        statement = "sigma(t) is constant -> the network supports a localized stable state."
    else:
        verdict = "C"
        kind = "ballistic light-cone spreading (p~1)" if ballistic else \
               "intermediate/diffusive spreading"
        statement = (
            "No localized stable rest-state (death criterion met).  A sourced lump "
            "delocalizes with growth exponent p=%.2f -- %s -- and its profile flattens "
            "toward a light-cone plateau (central/mean %.2f -> %.2f).  This is the 2D "
            "massless retarded Green's function (1/2 inside the cone): the free network "
            "scalar has no localized particle-like rest-state, consistent with a "
            "massless field (no rest frame) and with M1's null inertia.  A genuine non-"
            "dispersing wavepacket would need Cauchy (initial-data) evolution with "
            "theta-dot, which the retarded kernel alone does not provide (limitation "
            "noted)." % (p_stat["mean"], kind, f0["mean"], f1["mean"]))
    print("-" * 70)
    print(f"VERDICT P1: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "T": T, "X": X, "sigma0": SIGMA0,
                      "n_seeds": len(sg_by_seed)},
           "times": all_ts.tolist(), "sigma_mean": sg_mean.tolist(),
           "sigma_sem": sg_sem.tolist(), "growth_exponent": p_stat,
           "flatness_early": f0, "flatness_late": f1,
           "stable": bool(stable), "verdict": verdict, "statement": statement}
    mc.save_json("P1_localstate", out)
    return out


if __name__ == "__main__":
    main()
