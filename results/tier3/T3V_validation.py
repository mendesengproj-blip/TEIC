"""T3V_validation.py -- ENGINEERING GATE for the TIER3 MCMC growth sampler.

This is NOT a physics campaign: it validates that the scalable sampler in
tier3_core.py reproduces the EXACT e7 dynamics (enumeration of order ideals,
validated in e7_growth_dynamics.py up to N=7) before any T3A/T3B run.  If any
check fails, the campaigns refuse to run (tier3_core.validation_gate()).

Pre-registered pass criteria (engineering, fixed before running):

  V0 (bookkeeping): along MCMC chains on grown causets, the incremental
      component count must EQUAL a full BFS recount at every audited step.
      PASS: zero mismatches over >= 20_000 audited proposals.

  V1 (single-step distribution): on fixed small causets (chain, antichain,
      diamond stack, an e7-grown causet), the empirical distribution of the
      chain over order ideals must match the exact w(I)/Z distribution.
      PASS: total-variation distance TV <= 0.05 for every test causet
      (150_000 steps, burn-in 2_000, thinning 3).

  V2 (end-to-end growth distribution): grow M=4000 causets to N=6 with the
      MCMC sampler (production settings K = max(64, 6n), warm start) and
      compare the distribution over UNLABELLED causets with the EXACT
      distribution computed by dynamic programming over canonical forms
      (the labelled growth chain projects to a Markov chain on isomorphism
      classes because the e7 weights are label-invariant).  Calibration:
      M=4000 draws from e7's exact sampler give the sampling-noise floor.
      PASS: TV_mcmc <= max(0.04, 1.5 * TV_e7exact).

  V3 (estimator): Myrheim-Meyer inversion recovers the input dimension of
      static sprinklings.  PASS: |d_est_global - d| <= 0.15 for d=2 and d=4
      at N=1500 (3 seeds averaged).

Output: results/tier3/T3V_validation/{T3V_data.json, T3V_report.md}.
"""

from __future__ import annotations

import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "experiments"))

import tier3_core as t3                                     # noqa: E402
from e7_growth_dynamics import (downward_closed_subsets,    # noqa: E402
                                grow_one, n_components, sample_causet,
                                teic_weight)

OUT = HERE / "T3V_validation"
W_MEET = Fraction(1, 3)
W_MEET_F = float(W_MEET)

# ---------------------------------------------------------------------------
# canonical form of a small causet, vectorised (matches e7's equivalence)
# ---------------------------------------------------------------------------
_PERMS = {}


def canonical_bits(A, n):
    """Minimum over relabelings of the n*n relation matrix packed to an int."""
    import itertools
    if n not in _PERMS:
        _PERMS[n] = np.array(list(itertools.permutations(range(n))))
    perms = _PERMS[n]
    M = A[:n, :n]
    # all relabelings at once: (P, n, n)
    R = M[perms[:, :, None], perms[:, None, :]]
    w = (1 << np.arange(n * n, dtype=np.uint64))
    packed = (R.reshape(len(perms), -1).astype(np.uint64) * w).sum(axis=1)
    return int(packed.min())


def rel_to_anc(rel, n):
    """e7 list-of-lists relation -> numpy ancestor matrix A[i,j]=j precedes i."""
    A = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(n):
            if rel[j][i]:
                A[i, j] = True
    return A


# ---------------------------------------------------------------------------
# V0: incremental ncomp bookkeeping == full BFS recount
# ---------------------------------------------------------------------------
def v0_bookkeeping(n_audited=20000, seed=101):
    rng = np.random.default_rng(seed)
    mismatches = 0
    audited = 0
    for trial in range(8):
        g = t3.GrowthCauset(64, w_meet=W_MEET_F, rng=rng)
        g.grow(40 + 3 * trial)
        # audit single proposals: run 1-proposal chains and recount fully
        for _ in range(n_audited // 8):
            g._run_chain(1)
            audited += 1
            if g.ncomp != g._ncomp_full():
                mismatches += 1
    return {"audited": audited, "mismatches": mismatches,
            "passed": mismatches == 0}


# ---------------------------------------------------------------------------
# V1: chain stationary distribution over ideals of a FIXED causet
# ---------------------------------------------------------------------------
def _fixed_causets(rng):
    """Test causets as (name, ancestor-matrix, n)."""
    out = []
    # 5-chain
    n = 5
    A = np.zeros((n, n), dtype=bool)
    for i in range(n):
        A[i, :i] = True
    out.append(("chain5", A, n))
    # 5-antichain
    out.append(("antichain5", np.zeros((5, 5), dtype=bool), 5))
    # stack of two diamonds (0 < {1,2} < 3 < {4,5} < 6)
    n = 7
    A = np.zeros((n, n), dtype=bool)
    order = {1: [0], 2: [0], 3: [0, 1, 2], 4: [0, 1, 2, 3], 5: [0, 1, 2, 3],
             6: [0, 1, 2, 3, 4, 5]}
    for i, anc in order.items():
        A[i, anc] = True
    out.append(("diamond_stack7", A, n))
    # an e7-grown causet (exact sampler), size 6
    rel, n6 = sample_causet(6, W_MEET, rng)
    out.append(("e7_grown6", rel_to_anc(rel, n6), n6))
    return out


def v1_ideal_distribution(steps=150000, burn=2000, thin=3, seed=202):
    rng = np.random.default_rng(seed)
    results = []
    for name, A, n in _fixed_causets(rng):
        # exact distribution over ideals: w(I)/Z, via e7 enumeration
        rel = [[bool(A[j, i]) for j in range(n)] for i in range(n)]
        # rel[i][j] = i precedes j = A[j, i]
        exact = {}
        for past in downward_closed_subsets(rel, n):
            w = float(teic_weight(rel, n, past, W_MEET))
            key = frozenset(past)
            exact[key] = w
        Z = sum(exact.values())
        exact = {k: v / Z for k, v in exact.items()}

        # empirical distribution from the tier3 chain
        g = t3.GrowthCauset(n, w_meet=W_MEET_F, rng=rng, seed_matrix=A)
        g._run_chain(burn)
        counts = {}
        kept = 0
        for _ in range(steps // thin):
            g._run_chain(thin)
            key = frozenset(np.flatnonzero(g.cur[:n]).tolist())
            counts[key] = counts.get(key, 0) + 1
            kept += 1
        tv = 0.5 * sum(abs(exact.get(k, 0.0) - counts.get(k, 0) / kept)
                       for k in set(exact) | set(counts))
        results.append({"causet": name, "n": n, "n_ideals": len(exact),
                        "tv": float(tv), "passed": tv <= 0.05})
        print(f"    V1 {name:>14}: {len(exact):3d} ideals  TV={tv:.4f}  "
              f"{'PASS' if tv <= 0.05 else 'FAIL'}")
    return {"results": results, "passed": all(r["passed"] for r in results)}


# ---------------------------------------------------------------------------
# V2: end-to-end growth distribution at N=6 vs exact DP
# ---------------------------------------------------------------------------
def exact_distribution_n(n_target):
    """Exact unlabelled-causet distribution of the e7 dynamics at n_target,
    by DP over canonical forms (transition probs are label-invariant)."""
    A1 = np.zeros((1, 1), dtype=bool)
    dist = {canonical_bits(A1, 1): (1.0, A1)}
    for n in range(1, n_target):
        nxt = {}
        for _, (p, A) in dist.items():
            rel = [[bool(A[j, i]) for j in range(n)] for i in range(n)]
            table = []
            for past in downward_closed_subsets(rel, n):
                table.append((past, float(teic_weight(rel, n, past, W_MEET))))
            Z = sum(w for _, w in table)
            for past, w in table:
                A2 = np.zeros((n + 1, n + 1), dtype=bool)
                A2[:n, :n] = A
                m = np.zeros(n, dtype=bool)
                m[list(past)] = True
                A2[n, :n] = m
                key = canonical_bits(A2, n + 1)
                q = p * w / Z
                if key in nxt:
                    nxt[key] = (nxt[key][0] + q, nxt[key][1])
                else:
                    nxt[key] = (q, A2)
        dist = nxt
    return {k: v[0] for k, v in dist.items()}


def v2_growth_distribution(n_target=6, M=4000, seed=303):
    rng = np.random.default_rng(seed)
    print(f"    V2 exact DP to N={n_target} ...")
    exact = exact_distribution_n(n_target)
    print(f"       {len(exact)} unlabelled causets, sum p = "
          f"{sum(exact.values()):.6f}")

    # MCMC growth sampler (production settings)
    mcmc = {}
    for _ in range(M):
        g = t3.GrowthCauset(n_target, w_meet=W_MEET_F, rng=rng)
        g.grow(n_target)
        k = canonical_bits(g.A, n_target)
        mcmc[k] = mcmc.get(k, 0) + 1
    tv_mcmc = 0.5 * sum(abs(exact.get(k, 0.0) - mcmc.get(k, 0) / M)
                        for k in set(exact) | set(mcmc))

    # calibration: e7's exact sampler, same M -> sampling-noise floor
    e7s = {}
    for _ in range(M):
        rel, n = sample_causet(n_target, W_MEET, rng)
        k = canonical_bits(rel_to_anc(rel, n), n)
        e7s[k] = e7s.get(k, 0) + 1
    tv_e7 = 0.5 * sum(abs(exact.get(k, 0.0) - e7s.get(k, 0) / M)
                      for k in set(exact) | set(e7s))

    threshold = max(0.04, 1.5 * tv_e7)
    passed = tv_mcmc <= threshold
    print(f"    V2 TV(mcmc, exact) = {tv_mcmc:.4f}   "
          f"TV(e7sampler, exact) = {tv_e7:.4f}   "
          f"threshold = {threshold:.4f}   {'PASS' if passed else 'FAIL'}")
    return {"n_target": n_target, "M": M, "n_classes_exact": len(exact),
            "tv_mcmc": float(tv_mcmc), "tv_e7_exact_sampler": float(tv_e7),
            "threshold": float(threshold), "passed": bool(passed)}


# ---------------------------------------------------------------------------
# V3: MM estimator recovers input dimension of static sprinklings
# ---------------------------------------------------------------------------
def v3_estimator(N=1500, dims=(2, 4), n_seeds=3, seed=404):
    rng = np.random.default_rng(seed)
    results = []
    for d in dims:
        ests = []
        for _ in range(n_seeds):
            pts = t3.sprinkle_diamond(N, d, rng)
            A = t3.causal_matrix_anc(pts)
            ests.append(t3.mm_global(A, N))
        m = float(np.mean(ests))
        ok = abs(m - d) <= 0.15
        results.append({"d_input": d, "d_est_mean": m,
                        "d_est_all": [float(e) for e in ests], "passed": ok})
        print(f"    V3 d={d}: d_MM_global = {m:.3f}  "
              f"{'PASS' if ok else 'FAIL'}")
    return {"results": results, "passed": all(r["passed"] for r in results)}


# ---------------------------------------------------------------------------
def main():
    print("=" * 70)
    print("T3V -- SAMPLER VALIDATION GATE (engineering, pre-registered)")
    print("=" * 70)
    t0 = time.perf_counter()

    print("  V0: incremental component bookkeeping vs full recount")
    v0 = v0_bookkeeping()
    print(f"    audited={v0['audited']}  mismatches={v0['mismatches']}  "
          f"{'PASS' if v0['passed'] else 'FAIL'}")

    print("  V1: stationary ideal distribution on fixed causets")
    v1 = v1_ideal_distribution()

    print("  V2: end-to-end growth distribution at N=6")
    v2 = v2_growth_distribution()

    print("  V3: MM estimator on static sprinklings")
    v3 = v3_estimator()

    passed = v0["passed"] and v1["passed"] and v2["passed"] and v3["passed"]
    out = {"passed": bool(passed),
           "w_meet": str(W_MEET),
           "sampler": {"K_FACTOR": t3.K_FACTOR, "K_MIN": t3.K_MIN},
           "V0": v0, "V1": v1, "V2": v2, "V3": v3,
           "runtime_s": time.perf_counter() - t0}
    t3.save_json(OUT, "T3V_data", out)
    _report(out)
    print("-" * 70)
    print(f"GATE: {'PASSED -- campaigns may run' if passed else 'FAILED'}  "
          f"({out['runtime_s']:.1f}s)")
    return 0 if passed else 1


def _report(out):
    L = ["# T3V -- Validation gate do sampler MCMC (engenharia)", "",
         "Valida que o sampler escalavel de `tier3_core.py` reproduz a dinamica",
         "EXATA de e7 (enumeracao de ideais) antes de qualquer campanha fisica.",
         "Criterios pre-registrados no docstring do gerador.", "",
         f"- **V0** bookkeeping de componentes: {out['V0']['audited']} propostas "
         f"auditadas, {out['V0']['mismatches']} divergencias -> "
         f"{'PASS' if out['V0']['passed'] else 'FAIL'}",
         "- **V1** distribuicao estacionaria sobre ideais (TV <= 0.05):"]
    for r in out["V1"]["results"]:
        L.append(f"  - `{r['causet']}` ({r['n_ideals']} ideais): TV = "
                 f"{r['tv']:.4f} -> {'PASS' if r['passed'] else 'FAIL'}")
    v2 = out["V2"]
    L += [f"- **V2** distribuicao de crescimento N={v2['n_target']} "
          f"({v2['n_classes_exact']} classes): TV_mcmc = {v2['tv_mcmc']:.4f} vs "
          f"piso de ruido TV_e7 = {v2['tv_e7_exact_sampler']:.4f} "
          f"(limite {v2['threshold']:.4f}) -> "
          f"{'PASS' if v2['passed'] else 'FAIL'}",
          "- **V3** estimador MM em sprinkling estatico:"]
    for r in out["V3"]["results"]:
        L.append(f"  - d={r['d_input']}: d_MM = {r['d_est_mean']:.3f} -> "
                 f"{'PASS' if r['passed'] else 'FAIL'}")
    L += ["", f"## GATE: {'PASSED' if out['passed'] else 'FAILED'}", "",
          f"Sampler: K = max({out['sampler']['K_MIN']}, "
          f"{out['sampler']['K_FACTOR']} n) propostas Metropolis por passo de "
          f"crescimento, warm start; w_meet = {out['w_meet']}.",
          "", "Reproduzir: `python results/tier3/T3V_validation.py`", ""]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "T3V_report.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
