"""SD1 -- is K <= (2/3)S an exact identity or a statistical (isotropic) result?

Pre-registered (SKYRME_DOMINANCE.md addendum, items 1-3 and 6, written before
this ran):

  (a) K = S - Tr(G^2), G PSD  =>  K <= S exactly, equality only at G = 0;
  (b) Cauchy-Schwarz on the d eigenvalues of G:
      d*Tr(G^2) - (TrG)^2 = sum_{i<j} (lam_i - lam_j)^2 >= 0
      =>  K <= (1 - 1/d) S  POINTWISE (link by link, not on average),
      saturated exactly at G ~ I (the hedgehog). In d=3: K <= (2/3) S.
  (c) the isotropic ratio -3:+2 is d-independent:
      <|l_e|^4> = (3S - 2K)/(d(d+2)) for every d
      =>  3S - 2K = S + 2Tr(G^2) >= (1 + 2/d) S > 0 in EVERY d, EVERY config;
  (d) the four numbers are different numbers: 5/9 (SC2 residual ratio B/A),
      2/3 (pointwise K/S of the hedgehog), 2/5 (mean cross-channel fraction
      of a link in d=3), 1/2 (same fraction with 4 components).

  DEATH CRITERION (charter): SUCESSO PARCIAL/COMPLETO require K/S > 2/3 in
  some regime. (b) predicts that is impossible in d=3. The adversarial
  search below (10^6 random configs + hill climb per d) must approach
  1 - 1/d and NEVER exceed it; one counterexample kills the identity and
  the numeric result wins.
"""

from __future__ import annotations

import json
import sys
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sd_core as sd


# ---- (a)+(b) symbolic: pointwise bound and saturation ------------------------ #
def symbolic_pointwise_bound(dims=(2, 3, 4, 5, 6)):
    out = {}
    for d in dims:
        lam = sp.symbols(f"lam0:{d}", nonnegative=True)
        sum1 = sum(lam)
        sum2 = sum(x ** 2 for x in lam)
        # d*Tr(G^2) - (TrG)^2 == sum_{i<j}(lam_i - lam_j)^2  (exact identity)
        lhs = sp.expand(d * sum2 - sum1 ** 2)
        rhs = sp.expand(sum((a - b) ** 2 for a, b in combinations(lam, 2)))
        ok_identity = sp.simplify(lhs - rhs) == 0
        # saturation: lam_i = c for all i  ->  K/S = 1 - 1/d
        c = sp.symbols("c", positive=True)
        S_sat = (d * c) ** 2
        K_sat = S_sat - d * c ** 2
        ok_sat = sp.simplify(K_sat / S_sat - (1 - sp.Rational(1, d))) == 0
        out[d] = {"cauchy_schwarz_identity": bool(ok_identity),
                  "hedgehog_saturates_1_minus_1_over_d": bool(ok_sat),
                  "bound_K_over_S": float(1 - 1.0 / d)}
    return out


# ---- (c) symbolic in d: the -3:+2 lock and the net-quartic gap ---------------- #
def symbolic_ratio_lock():
    """Contract <e_i e_j e_k e_l> = (d_ij d_kl + d_ik d_jl + d_il d_jk)/(d(d+2))
    against G_ij G_kl for a symbolic symmetric G and SYMBOLIC d."""
    d = sp.symbols("d", positive=True)
    n = 4                      # explicit matrix size; d stays symbolic in the
    G = sp.Matrix(n, n, lambda i, j: sp.Symbol(f"g{min(i,j)}{max(i,j)}"))
    trG = sp.trace(G)
    trG2 = sp.trace(G * G)
    # explicit contraction of the three delta pairings against G_ij G_kl:
    # sum_{ijkl} G_ij G_kl (d_ij d_kl + d_ik d_jl + d_il d_jk)
    delta = sp.eye(n)
    contraction = sp.expand(sum(
        G[i, j] * G[k, l] * (delta[i, j] * delta[k, l] +
                             delta[i, k] * delta[j, l] +
                             delta[i, l] * delta[j, k])
        for i in range(n) for j in range(n)
        for k in range(n) for l in range(n)))
    avg = contraction / (d * (d + 2))
    S = trG ** 2
    K = trG ** 2 - trG2
    lock = sp.simplify(avg - (3 * S - 2 * K) / (d * (d + 2))) == 0
    # net-quartic gap: 3S - 2K = S + 2Tr(G^2); with Tr(G^2) >= S/n (CS, size n):
    gap = sp.simplify((3 * S - 2 * K) - (S + 2 * trG2)) == 0
    return bool(lock), bool(gap)


def numeric_pairing_check(d_val, rng, n_dirs=400_000):
    """MC check that <(e^T G e)^2> = [(TrG)^2 + 2Tr(G^2)]/(d(d+2)) at d=d_val."""
    Cm = rng.standard_normal((d_val, d_val))
    G = Cm @ Cm.T
    dirs = sd.unit_directions(n_dirs, d_val, rng)
    q = np.einsum("ni,ij,nj->n", dirs, G, dirs)
    lhs = float(np.mean(q ** 2))
    trG, S, K = sd.invariants_d(Cm)
    rhs = (3 * S - 2 * K) / (d_val * (d_val + 2))
    return lhs / rhs


# ---- adversarial search: sup K/S over configurations ------------------------- #
def adversarial_max_KS(d, rng, n_random=1_000_000, n_climb=200):
    """Random configs (heavy-tailed scales) + hill climb. K/S must stay
    <= 1 - 1/d. Returns (max over random, max after climb)."""
    best = -1.0
    chunk = 100_000
    done = 0
    best_C = None
    while done < n_random:
        m = min(chunk, n_random - done)
        Cs = rng.standard_normal((m, d, d)) * \
            np.exp(rng.standard_normal((m, 1, 1)) * 2.0)
        Gs = Cs @ np.transpose(Cs, (0, 2, 1))
        tr = np.trace(Gs, axis1=1, axis2=2)
        tr2 = np.einsum("nij,nji->n", Gs, Gs)
        ks = 1.0 - tr2 / tr ** 2                       # K/S
        i = int(np.argmax(ks))
        if ks[i] > best:
            best, best_C = float(ks[i]), Cs[i].copy()
        done += m
    # hill climb from the best random start
    C = best_C
    step = 0.3
    cur = best
    for _ in range(n_climb):
        cand = C + step * rng.standard_normal((d, d))
        G = cand @ cand.T
        tr = float(np.trace(G))
        tr2 = float(np.trace(G @ G))
        v = 1.0 - tr2 / tr ** 2
        if v > cur:
            cur, C = v, cand
        else:
            step *= 0.95
    return best, cur


# ---- (d) the four numbers ----------------------------------------------------- #
def four_numbers():
    # SC2 residual ratio B/A
    _, SA, KA = sd.sc.invariants(sd.sc.config_A(1.0))
    _, SB, KB = sd.sc.invariants(sd.sc.config_B(1.0))
    r_sc2 = (3 * SB - 2 * KB) / (3 * SA - 2 * KA)
    ks_hedgehog = KB / SB
    frac3 = 1.0 - 3.0 / (3 + 2)                        # mean kappa, d=3
    frac4 = 1.0 - 3.0 / (4 + 2)                        # mean kappa, 4 components
    return {"SC2_residual_ratio_B_over_A": {"value": r_sc2, "exact": "5/9"},
            "hedgehog_pointwise_K_over_S": {"value": ks_hedgehog, "exact": "2/3",
                                            "note": "saturates the bound"},
            "link_cross_channel_fraction_d3": {"value": frac3, "exact": "2/5"},
            "link_cross_channel_fraction_d4": {"value": frac4, "exact": "1/2"}}


def main():
    rng = np.random.default_rng(20260612)

    sym = symbolic_pointwise_bound()
    lock, gap = symbolic_ratio_lock()
    pairing = {d: numeric_pairing_check(d, rng) for d in (2, 3, 4, 5)}

    adv = {}
    for d in (2, 3, 4, 5, 6):
        rnd, climbed = adversarial_max_KS(d, rng)
        bound = 1.0 - 1.0 / d
        adv[d] = {"max_random": rnd, "max_hill_climb": climbed,
                  "bound_1_minus_1_over_d": bound,
                  "violated": bool(climbed > bound + 1e-12)}

    # cross-channel mean fraction, symbolic d and numeric d=1..8
    d_sym = sp.symbols("d", positive=True)
    e4 = 3 / (d_sym * (d_sym + 2))                     # <e_mu^4>
    frac_sym = sp.simplify(1 - d_sym * e4)             # 1 - 3/(d+2)
    frac_ok = sp.simplify(frac_sym - (1 - 3 / (d_sym + 2))) == 0

    payload = {
        "a_K_le_S": "K = S - Tr(G^2), Tr(G^2)>=0 (G PSD): exact, equality iff G=0",
        "b_pointwise_bound_symbolic": sym,
        "c_ratio_lock_d_independent_symbolic": bool(lock),
        "c_net_quartic_gap_S_plus_2TrG2_symbolic": bool(gap),
        "c_pairing_MC_lhs_over_rhs": pairing,
        "adversarial_max_K_over_S": adv,
        "cross_channel_fraction_formula_ok": bool(frac_ok),
        "d_four_numbers": four_numbers(),
        "conclusion": (
            "K <= (1-1/d)S is an exact POINTWISE identity (Cauchy-Schwarz on "
            "the PSD Gram eigenvalues), saturated by the hedgehog; in d=3 the "
            "bound is 2/3 and there is no configuration above it. The -3:+2 "
            "coefficient ratio is d-independent, so 3S-2K >= (1+2/d)S > 0 in "
            "every dimension: dominance via the quartic channel is impossible, "
            "not merely unobserved."),
    }
    sd.save_json("SD1_identity.json", payload)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
