"""E1 -- energy as causal counting (refaz T18/T19).

T18/T19 fit a hand-translated Gaussian blob to e^{-0.52 v^2}, not 1/gamma, and the
fit depended on the arbitrary blob width.  The correct route uses the proper time
tau already DERIVED by R1 from causal counting -- nothing energy-related is inserted.

Relation (note: the prompt's 'E=m dtau/dt' is a typo; the relativistic energy is
E = m * dt/dtau = m * gamma, since dtau/dt = sqrt(1-beta^2) < 1 DEcreases with beta
while energy increases).  So:

    E_rede(beta) = m * (coordinate time / proper time) = m * gamma_measured ,

where gamma_measured = tau(0)/tau(beta) is obtained by COUNTING (longest chain and
volume estimators of R1), not from any formula.

METHOD
  * A clock moves at velocity beta for coordinate time T: A=(0,0), B=(T, beta T).
  * Measure its proper time tau(beta) from the Alexandrov interval by (i) the
    longest causal chain and (ii) the volume estimator (k_d N/rho)^(1/d).
  * gamma_measured = tau(0)/tau(beta).  E_rede = m * gamma_measured (m = 1 unit;
    the rest scale is the unverified M1 connectivity scale, so E1 is reported as a
    reinterpretation of R1, not an independent mass-energy).
  * COMPARE to gamma = 1/sqrt(1-beta^2) (validation.py, comparison only).

SUCCESS: E_rede grows with beta and matches m*gamma.
DEATH:   E_rede does not track gamma -> energy not recovered.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

import matter_core as mc

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import alexandrov_interval, sprinkle_box  # noqa: E402
from chain import longest_chain_2d  # noqa: E402
from volume import tau_from_count  # noqa: E402
from validation import lorentz_factor  # noqa: E402  (COMPARISON ONLY)

SEEDS = range(20)
RHO, T = 10.0, 9.0
BETAS = np.array([0.0, 0.2, 0.4, 0.6, 0.75, 0.85])
MASS_UNIT = 1.0   # arbitrary rest scale; E1 tests the gamma factor, not m itself


def _bounds(A, B, pad=1.0):
    t0, t1 = sorted([A[0], B[0]])
    cx = 0.5 * (A[1] + B[1])
    half = 0.5 * abs(B[0] - A[0]) + abs(B[1] - A[1]) + pad
    return [(t0 - pad, t1 + pad), (cx - half, cx + half)]


def proper_times(beta, seed):
    """(chain tau, volume tau) for a clock at velocity beta, one seed."""
    rng = np.random.default_rng(7000 + seed)
    A, B = np.array([0.0, 0.0]), np.array([T, beta * T])
    pts = sprinkle_box(RHO, _bounds(A, B), rng)
    idx = alexandrov_interval(pts, A, B)
    sub = np.vstack([A, pts[idx], B])
    return float(longest_chain_2d(sub)), float(tau_from_count(len(idx), RHO, 2))


def main():
    print("=" * 70)
    print("E1 -- ENERGY AS CAUSAL COUNTING (refaz T18/T19)")
    print("=" * 70)

    # proper times per beta (averaged over seeds)
    tau_chain, tau_vol = {}, {}
    for b in BETAS:
        cs, vs = zip(*[proper_times(b, s) for s in SEEDS])
        tau_chain[b] = mc.seed_stats(cs)
        tau_vol[b] = mc.seed_stats(vs)

    tc0, tv0 = tau_chain[0.0]["mean"], tau_vol[0.0]["mean"]
    gamma_chain = np.array([tc0 / tau_chain[b]["mean"] for b in BETAS])
    gamma_vol = np.array([tv0 / tau_vol[b]["mean"] for b in BETAS])
    gamma_ref = lorentz_factor(BETAS)            # COMPARISON ONLY

    E_chain = MASS_UNIT * gamma_chain
    E_vol = MASS_UNIT * gamma_vol
    E_ref = MASS_UNIT * gamma_ref

    dev_chain = float(np.mean(np.abs(E_chain - E_ref) / E_ref))
    dev_vol = float(np.mean(np.abs(E_vol - E_ref) / E_ref))
    grows = bool(E_chain[-1] > E_chain[0] and E_vol[-1] > E_vol[0])

    for i, b in enumerate(BETAS):
        print(f"  beta={b:.2f}: E_chain={E_chain[i]:.3f} E_vol={E_vol[i]:.3f} "
              f"m*gamma={E_ref[i]:.3f}")
    print(f"  mean rel.dev E_chain={dev_chain:.1%}  E_vol={dev_vol:.1%}  grows={grows}")

    matches = grows and dev_chain < 0.10 and dev_vol < 0.10
    if matches:
        verdict = "D"
        statement = ("E_rede = m*gamma is recovered (rel.dev %.1f%%/%.1f%%, grows "
                     "with beta), but this is a REINTERPRETATION of R1: gamma is "
                     "measured purely by R1's causal counting, and E=m*gamma just "
                     "multiplies it by a rest scale m that M1 could not pin down as a "
                     "real inertia.  Energy emerges as a consequence of R1+(an "
                     "assumed m), not as an independent derivation.  Additivity "
                     "E_tot=E1+E2 for non-interacting clocks holds by construction "
                     "(the count of a disjoint union is the sum)."
                     % (dev_chain*100, dev_vol*100))
    else:
        verdict = "C"
        statement = ("E_rede tracks gamma only roughly at this size; the relativistic "
                     "energy relation is not cleanly recovered.")
    print("-" * 70)
    print(f"VERDICT E1: {verdict}\n  {statement}")

    out = {"params": {"rho": RHO, "T": T, "betas": BETAS.tolist(),
                      "mass_unit": MASS_UNIT, "n_seeds": len(list(SEEDS))},
           "tau_chain": {str(b): tau_chain[b] for b in BETAS},
           "tau_vol": {str(b): tau_vol[b] for b in BETAS},
           "gamma_chain": gamma_chain.tolist(), "gamma_vol": gamma_vol.tolist(),
           "gamma_ref": gamma_ref.tolist(),
           "E_chain": E_chain.tolist(), "E_vol": E_vol.tolist(), "E_ref": E_ref.tolist(),
           "rel_dev_chain": dev_chain, "rel_dev_vol": dev_vol, "grows": grows,
           "verdict": verdict, "statement": statement}
    mc.save_json("E1_energy", out)
    return out


if __name__ == "__main__":
    main()
