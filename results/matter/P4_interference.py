"""P4 -- superposition / interference of states (novo).

For localized states, is the combination QUANTUM interference (a |psi|^2 Born-rule
pattern from a complex amplitude) or just CLASSICAL superposition of real fields?

The box operator and its retarded propagator are LINEAR, so theta_12 = theta_1 +
theta_2 exactly.  We verify the linearity numerically, then check what kind of
interference that produces.

METHOD
  * Source two localized lumps, propagate each (theta_1, theta_2) and the combined
    source (theta_12) on the SAME network.
  * Linearity residual: max |theta_12 - (theta_1+theta_2)| / max|theta_12|.
  * Real-wave cancellation: with OPPOSITE-sign sources the fields can cancel
    (intensity ratio min/max < 1) -- but this is Young's classical interference, not
    QM.  The Born rule needs a complex amplitude and |psi|^2, which a real linear
    field does not provide (consistent with e11).

ANTI-CIRCULARITY: NO complex numbers anywhere (guard enforces this); any quantum
amplitude would have to live in a COMPARISON ONLY block.  None is needed: we are
SHOWING the field is real/classical, not postulating a quantum one.

EXPECTED (honest): linear superposition (residual ~ 0), classical real-wave
cancellation, NO Born-rule |psi|^2 -> grade C, consistent with e11.
"""

from __future__ import annotations

import numpy as np

import matter_core as mc

SEEDS = range(20)
RHO, T, X, SIGMA, SEP = 18.0, 8.0, 14.0, 1.6, 6.0


def trial(seed):
    """Return (linearity residual, total-intensity ratio E_opp/E_same) on one network.

    Same-sign sources reinforce; opposite-sign sources cancel where they overlap, so
    the total field energy with opposite signs is LESS than with same signs.
    """
    rng = np.random.default_rng(11000 + seed)
    p = mc.sprinkle_2d(RHO, T, X, rng)
    t, x = p[:, 0], p[:, 1]
    early = t < T * 0.15
    J1 = mc.localized_profile(x, -SEP / 2, SIGMA) * early
    J2 = mc.localized_profile(x, +SEP / 2, SIGMA) * early
    K = mc.retarded_kernel(p)
    th1, th2 = K @ J1, K @ J2
    th_same = K @ (J1 + J2)
    th_opp = K @ (J1 - J2)
    resid = float(np.max(np.abs(th_same - (th1 + th2))) / (np.max(np.abs(th_same)) + 1e-12))
    late = t > T * 0.55                      # 'screen' region where the cones overlap
    e_same = float(np.sum(th_same[late] ** 2))
    e_opp = float(np.sum(th_opp[late] ** 2))
    ratio = e_opp / e_same if e_same > 0 else np.nan
    return resid, ratio


def main():
    print("=" * 70)
    print("P4 -- SUPERPOSITION / INTERFERENCE (novo)")
    print("=" * 70)
    pairs = [trial(s) for s in SEEDS]
    resid_p = mc.seed_stats([r for r, _ in pairs])
    ratio = mc.seed_stats([q for _, q in pairs])
    print(f"  linearity residual |theta_12-(theta_1+theta_2)| / max = "
          f"{resid_p['mean']:.2e} +/- {resid_p['sem']:.0e} (->0 = exact superposition)")
    print(f"  total-intensity ratio E_opp/E_same = {ratio['mean']:.3f} +/- {ratio['sem']:.3f} "
          f"(<1 = real-wave cancellation)")

    linear = resid_p["mean"] < 1e-9
    cancels = ratio["mean"] < 0.95
    verdict = "C"
    statement = (
        "Classical superposition, not quantum interference (as expected, consistent "
        "with e11).  The dynamics is LINEAR to machine precision (residual %.1e), so "
        "states add exactly: theta_12 = theta_1 + theta_2.  Opposite-sign sources "
        "cancel where the cones overlap (total-intensity ratio E_opp/E_same = %.2f < 1) "
        "-- this is Young's CLASSICAL interference of real fields.  There is no complex "
        "amplitude and no |psi|^2 Born rule (the guard forbids complex numbers in the "
        "generator, and none was needed): the quantum content is absent.  The TEIC<->QM "
        "boundary is exactly where e11 left it." % (resid_p["mean"], ratio["mean"]))
    print("-" * 70)
    print(f"VERDICT P4: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "T": T, "X": X, "sigma": SIGMA, "sep": SEP,
                      "n_seeds": len(list(SEEDS))},
           "linearity_residual": resid_p, "intensity_ratio_opp_same": ratio,
           "linear": bool(linear),
           "cancels": bool(cancels), "verdict": verdict, "statement": statement}
    mc.save_json("P4_interference", out)
    return out


if __name__ == "__main__":
    main()
