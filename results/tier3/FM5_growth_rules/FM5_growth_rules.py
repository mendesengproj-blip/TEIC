"""FM5_growth_rules.py -- does the e7 death generalise to other RULE FORMS?

Charter: docs/prompts/FM5_GROWTH_RULES.md (kill criteria PRE-REGISTERED).
Item 14 (Sec. 6) of RESEARCH_MAP.md / FM5 of FUTURE_EXPERIMENTS.md.

T3A-3 already swept the COUPLING w_meet of the binary e7 rule (all d~1.3, none -> 4).
FM5 varies the rule's FUNCTIONAL FORM, graded by the number of connected components
ncomp of the chosen past-ideal:

  R0 binary (e7):       w(nc) = w_meet if nc>=2 else 1            (anchor, reproduces T3A)
  R1 graded-penalise:   w(nc) = a^(nc-1),  a<1                    (favours chains -> low d)
  R2 graded-reward:     w(nc) = c^(nc-1),  c>1                    (favours wide antichains
                                                                  -> the high-d candidate)

The binary e7 form cannot tell 2 components from 10; the graded forms can.  R2 (reward
each extra component) is the decisive test for whether ANY rule form lifts d toward 4.

We subclass tier3_core.GrowthCauset and override ONLY the weight via a weight_fn; the
component bookkeeping and the MCMC machinery (validated rule-independently by the T3V
gate) are reused verbatim.  Detailed balance holds for any w(nc) (symmetric toggle
proposal + Metropolis acceptance w_new/w_old => target ~ prod w).

Anti-circularity: no d=4 target in the generator; fixed seeds; auto-descriptive JSON.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))          # results/tier3
import tier3_core as t3                         # noqa: E402

N_TARGET = 1200
N_SEEDS = 5
K_MIN, K_FACTOR = t3.K_MIN, t3.K_FACTOR


class GradedCauset(t3.GrowthCauset):
    """e7 growth engine with a configurable weight w(ncomp).  Only _run_chain's two
    weight evaluations change; everything else (ncomp bookkeeping, addability,
    laziness) is the validated base-class logic."""

    def __init__(self, n_max, weight_fn, rng=None):
        super().__init__(n_max, w_meet=1.0, rng=rng)
        self.weight_fn = weight_fn

    def _run_chain(self, K):
        n = self.n
        A = self.A
        cur = self.cur
        anc_count = self.anc_count
        past_conn = self.past_connected
        wfn = self.weight_fn
        xs = self.rng.integers(0, 2 * n, size=K)
        us = self.rng.random(K)
        ncomp = self.ncomp
        accepted = 0
        bfs = 0
        for t in range(K):
            x = xs[t]
            if x >= n:
                continue
            if cur[x]:
                if np.any(A[:n, x] & cur[:n]):
                    continue
                if anc_count[x] == 0:
                    nc2 = ncomp - 1
                elif past_conn[x]:
                    nc2 = ncomp
                else:
                    cur[x] = False
                    nc2 = self._ncomp_of_mask_static(A, n, cur[:n])
                    cur[x] = True
                    bfs += 1
                w_old = wfn(ncomp); w_new = wfn(nc2)
                if w_new >= w_old or us[t] < w_new / w_old:
                    cur[x] = False
                    ncomp = nc2
                    accepted += 1
            else:
                if np.any(A[x, :n] & ~cur[:n]):
                    continue
                if anc_count[x] == 0:
                    nc2 = ncomp + 1
                elif past_conn[x]:
                    nc2 = ncomp
                else:
                    cur[x] = True
                    nc2 = self._ncomp_of_mask_static(A, n, cur[:n])
                    cur[x] = False
                    bfs += 1
                w_old = wfn(ncomp); w_new = wfn(nc2)
                if w_new >= w_old or us[t] < w_new / w_old:
                    cur[x] = True
                    ncomp = nc2
                    accepted += 1
        self.ncomp = ncomp
        self.n_proposals += K
        self.n_accepted += accepted
        self.n_bfs_fallback += bfs


def binary_weight(w_meet):
    return lambda nc: (w_meet if nc >= 2 else 1.0)


def graded_weight(base):
    # w(nc) = base^(nc-1); base<1 penalises each extra component, base>1 rewards it
    return lambda nc: float(base) ** max(nc - 1, 0)


RULES = [
    ("R0_binary_e7",        binary_weight(1.0 / 3.0)),
    ("R1_graded_pen_0.33",  graded_weight(0.33)),
    ("R1_graded_pen_0.6",   graded_weight(0.6)),
    ("R2_graded_reward_2",  graded_weight(2.0)),
    ("R2_graded_reward_3",  graded_weight(3.0)),
    ("R2_graded_reward_5",  graded_weight(5.0)),
]


def run_rule(name, wfn, rng_seed):
    rng = np.random.default_rng(rng_seed)
    g = GradedCauset(N_TARGET + 20, wfn, rng=rng)
    g.grow(N_TARGET)
    m = t3.measure_causet(g.A, g.n, rng)
    return {"d_int": m["d_mm_interval"], "d_glob": m["d_mm_global"],
            "r": m["ordering_fraction"], "acc": g.n_accepted / max(g.n_proposals, 1)}


def main():
    t0 = time.time()
    t3.validation_gate()                         # the rule-independent sampler gate
    print("=" * 76)
    print(f"FM5 -- growth-rule FORMS: does the e7 death (d*~1.43) generalise?  "
          f"N={N_TARGET}, {N_SEEDS} seeds")
    print("=" * 76)

    results = {}
    for name, wfn in RULES:
        d_ints, d_globs, rs = [], [], []
        for sd in range(N_SEEDS):
            o = run_rule(name, wfn, 4200 + sd)
            d_ints.append(o["d_int"]); d_globs.append(o["d_glob"]); rs.append(o["r"])
        di = t3.seed_stats(d_ints); dg = t3.seed_stats(d_globs); rr = t3.seed_stats(rs)
        manifold = abs(di["mean"] - dg["mean"]) < 0.5
        near4 = abs(di["mean"] - 4.0) < 0.5
        results[name] = {"d_int": di, "d_glob": dg, "r": rr,
                         "manifold_like": bool(manifold), "near_d4": bool(near4)}
        print(f"  {name:22s}: d_int={di['mean']:.3f}+-{di['std']:.3f}  "
              f"d_glob={dg['mean']:.3f}  r={rr['mean']:.3f}  "
              f"manifold={manifold}  near4={near4}")

    g0 = abs(results["R0_binary_e7"]["d_int"]["mean"] - 1.43) < 0.4
    any_success = any(results[n]["near_d4"] and results[n]["manifold_like"] for n in results)
    verdict = ("SUCCESS (surprise) -- a rule form gives manifold-like d*~4." if any_success else
               "DEATH GENERALISES -- no graded rule form (penalise OR reward components) "
               "yields manifold-like d*~4; every form stays low-d and/or non-manifold. "
               "The e7 dimensional death (T3A/T3B) is robust to the rule FORM, not just the "
               "coupling (T3A-3 already swept the coupling).")
    print("-" * 76)
    print(f"  G0 (R0 reproduces T3A d*~1.43): {g0}")
    print(f"VERDICT: {verdict}")
    print("=" * 76)

    payload = {"N_target": N_TARGET, "n_seeds": N_SEEDS,
               "K_MIN": K_MIN, "K_FACTOR": K_FACTOR,
               "rules": list(results.keys()),
               "results": results, "G0_e7_anchor_ok": bool(g0),
               "any_success": bool(any_success), "verdict": verdict,
               "note": ("T3A-3 already swept the coupling w_meet of the binary e7 form; "
                        "FM5 varies the FUNCTIONAL FORM (graded by component count). "
                        "Scope: the component-graded subfamily, not the full RS/CSG "
                        "coupling-sequence family."),
               "runtime_s": time.time() - t0}
    t3.save_json(HERE, "FM5_growth_rules", payload)
    print(f"saved FM5_growth_rules.json  ({payload['runtime_s']:.0f}s)")
    return payload


if __name__ == "__main__":
    main()
