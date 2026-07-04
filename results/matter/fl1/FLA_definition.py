"""FLA_definition.py -- FL1_SU3_FOUNDATION, Phase A.

Establishes whether an SU(3) field can be DEFINED on the same 3+1D Poisson causal
lattice that produced SU(2), with a positive-semidefinite minimal action and
without violating causal locality.  Five gates, each MEASURED then checked against
the pre-registered prediction.

PRE-REGISTERED PREDICTIONS (written before running):
  A1  Group axioms hold to machine precision (SU(3) is a Lie group -- definitional).
  A2  Wilson plaquette action s_p = 1 - (1/3)Re Tr(W) >= 0 for every W in SU(3),
      = 0 iff W = I.  Eigenvalues of W lie on the unit circle => Re Tr W <= 3.
  A3  Quadratic (sigma) density Tr((e.C)^2) >= 0 for every current C and direction e
      (Gram form of a Hermitian matrix).
  A4  THE SKYRME_DOMINANCE REPEAT.  The cosine's leading quartic for SU(3) is
      -Tr((e.C)^4) <= 0 (SD4 sign theorem, group-independent: Tr X^4 = sum lambda^4).
      Isotropic identity <Tr X^4>_e = (1/15)(3 TrM2 - K/2) => Cauchy-Schwarz bound
      K <= 6 TrM2 (the SU(3) analogue of SU(2)'s K <= 2/3 S).  Net leading quartic
      stays NEGATIVE: Skyrme dominance is structurally absent for SU(3) too.
      NOTE: this is NOT a Phase-A death -- the action is still PSD.  It is the note
      carried to Phase C (a stabiliser/core-cost is needed, exactly as for SU(2)).
  A5  Causal locality preserved: 100% of action links are future-directed timelike
      covering relations; the loop holonomy is gauge-covariant (W -> gWg^dag), so the
      action couples ONLY causally connected events.

DEATH CRITERION (Phase A): action not PSD under any reasonable operator choice, OR
causal structure violated.  Neither can occur for the Wilson action of a unitary
group on a causal set -- so Phase A is expected to PASS, and the result is the
honest delimitation that the SUBSTRATE hosts SU(3) just as it hosts SU(2).
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su3_core as s3

TOL = 1e-9          # machine-precision gate for the group axioms
SIGN_TOL = 1e-9     # tolerance for "<= 0" / ">= 0" sign theorems


def gate_A1_group_axioms(rng, n=200_000):
    """SU(3) field is well defined: generators, structure constants, group laws."""
    G = np.einsum("aij,bji->ab", s3.GELL_MANN, s3.GELL_MANN).real
    norm_err = float(np.max(np.abs(G - 2 * np.eye(8))))
    f, d = s3.structure_constants()
    f_antisym = float(np.max(np.abs(f + np.swapaxes(f, 0, 1))))
    d_sym = float(np.max(np.abs(d - np.swapaxes(d, 0, 1))))
    f123 = float(f[0, 1, 2]); f458 = float(f[3, 4, 7]); d118 = float(d[0, 0, 7])

    U = s3.su3_random(n, rng)
    unit_err, det_err = s3.is_su3(U)
    UV = U[:-1] @ U[1:]                                   # closure
    clos_unit, clos_det = s3.is_su3(UV)
    # associativity of the matrix product (definitional, but verify on a sample)
    A, B, Cc = U[:1000], U[1000:2000], U[2000:3000]
    assoc = float(np.max(np.abs((A @ B) @ Cc - A @ (B @ Cc))))
    # the exponential map lands in SU(3) from arbitrary algebra coordinates
    Uexp = s3.su3_from_coords(3.0 * rng.standard_normal((5000, 8)))
    exp_unit, exp_det = s3.is_su3(Uexp)

    passed = max(norm_err, f_antisym, d_sym, unit_err, det_err, clos_unit,
                 clos_det, assoc, exp_unit, exp_det) < TOL
    return passed, {
        "gellmann_norm_err": norm_err, "f_antisym_err": f_antisym,
        "d_sym_err": d_sym, "f_123": f123, "f_458": f458, "d_118": d118,
        "random_unit_err": unit_err, "random_det_err": det_err,
        "closure_unit_err": clos_unit, "closure_det_err": clos_det,
        "associativity_err": assoc, "exp_unit_err": exp_unit,
        "exp_det_err": exp_det, "n_samples": n,
    }


def gate_A2_wilson_psd(rng, n=1_000_000):
    """Wilson plaquette action s_p = 1 - (1/3)Re Tr(W) >= 0, = 0 iff W = I."""
    mins, maxs = [], []
    # (a) Haar-random plaquettes (far from identity)
    A, B, C, D = (s3.su3_random(n, rng) for _ in range(4))
    s_haar = s3.wilson_density(s3.plaquette(A, B, C, D))
    mins.append(float(s_haar.min())); maxs.append(float(s_haar.max()))
    # (b) near-identity plaquettes at a ladder of algebra scales (probe the floor
    #     where the cosine quartic lives -- the regime the SD theorem is about)
    floor_mins = {}
    for scale in (1e-3, 1e-2, 1e-1, 0.5, 1.0, 2.0):
        m = n // 6
        A, B, C, D = (s3.su3_defects(m, rng, scale=scale) for _ in range(4))
        s = s3.wilson_density(s3.plaquette(A, B, C, D))
        floor_mins[f"scale_{scale}"] = float(s.min())
        mins.append(float(s.min())); maxs.append(float(s.max()))
    # (c) the exact identity case W = I -> density exactly 0
    s_id = float(s3.wilson_density(np.eye(3, dtype=complex)))
    global_min = min(mins)
    passed = (global_min >= -SIGN_TOL) and (abs(s_id) < 1e-14)
    return passed, {
        "min_density_overall": global_min, "max_density_overall": max(maxs),
        "haar_min": mins[0], "identity_density": s_id,
        "near_identity_floor_mins": floor_mins,
        "analytic": "eig(W) on unit circle => Re Tr W = sum cos(theta_k) <= 3",
        "n_samples": n,
    }


def gate_A3_sigma_psd(rng, n=1_000_000):
    """Quadratic (sigma) density Tr((e.C)^2) >= 0 for all currents and directions."""
    worst = np.inf
    samples = 0
    batch = 200_000
    while samples < n:
        m = min(batch, n - samples)
        C = s3.algebra_from_coords(rng.standard_normal((m, 3, 8)))     # (m,3,3,3)
        e = rng.standard_normal((m, 3)); e /= np.linalg.norm(e, axis=1, keepdims=True)
        X = np.einsum("ne,neij->nij", e, C)
        tr2 = np.real(np.einsum("nij,nji->n", X, X))
        worst = min(worst, float(tr2.min()))
        samples += m
    passed = worst >= -SIGN_TOL
    return passed, {"min_sigma_density": worst, "n_samples": n,
                    "analytic": "Tr(X^2) = sum lambda_k^2 >= 0 for Hermitian X"}


def gate_A4_cauchy_schwarz(rng, n=1_000_000):
    """The SKYRME_DOMINANCE Cauchy-Schwarz repeat for SU(3).

    (i)  sign theorem: net quartic density -Tr((e.C)^4) <= 0 (adversarial max).
    (ii) isotropic identity <Tr X^4>_e = (1/15)(3 TrM2 - K/2) (formula vs direct MC).
    (iii) Cauchy-Schwarz bound: max K/TrM2 over random configs -> bound 6, never above.
    """
    # (i) sign theorem on net quartic density
    worst_quartic = -np.inf
    samples = 0
    batch = 200_000
    while samples < n:
        m = min(batch, n - samples)
        C = s3.algebra_from_coords(rng.standard_normal((m, 3, 8)))
        e = rng.standard_normal((m, 3)); e /= np.linalg.norm(e, axis=1, keepdims=True)
        X = np.einsum("ne,neij->nij", e, C)
        X2 = X @ X
        net_quartic = -np.real(np.einsum("nij,nji->n", X2, X2))   # -Tr(X^4)
        worst_quartic = max(worst_quartic, float(net_quartic.max()))
        samples += m
    sign_ok = worst_quartic <= SIGN_TOL

    # (ii) isotropic identity, checked EXACTLY (no sampling) on independent configs:
    #      the rank-4 moment formula vs the K/TrM2 formula, both closed form.
    id_rel_errs = []
    for _ in range(200):
        C = s3.random_currents(rng, scale=float(rng.uniform(0.3, 1.5)))
        exact = s3.quartic_isotropic_mean_exact(C)
        formula = s3.quartic_isotropic_mean_formula(C)
        id_rel_errs.append(abs(exact - formula) / abs(formula))
    id_rel_err = float(np.max(id_rel_errs))

    # (iii) Cauchy-Schwarz bound K <= 6 TrM2; adversarial max over random configs
    max_ratio = 0.0
    for _ in range(n // 1000):
        C = s3.random_currents(rng, scale=float(rng.uniform(0.2, 3.0)))
        K, TrM2 = s3.skyrme_invariant(C)
        if TrM2 > 1e-12:
            max_ratio = max(max_ratio, K / TrM2)

    # reference configs (named, no fit): Abelian (K=0) and su(2)-subalgebra hedgehog
    C_abelian = s3.algebra_from_coords(np.tile([1, 0, 0, 0, 0, 0, 0, 0], (3, 1)))
    K_ab, TrM2_ab = s3.skyrme_invariant(C_abelian)
    # su(2)-in-su(3) hedgehog: c_x=l1, c_y=l2, c_z=l3 (max commutators, the analogue
    # of sc_core.config_B that saturated the SU(2) bound)
    phi_h = np.eye(8)[[0, 1, 2]]
    C_hedge = s3.algebra_from_coords(phi_h)
    K_h, TrM2_h = s3.skyrme_invariant(C_hedge)

    passed = sign_ok and (id_rel_err < 1e-3) and (max_ratio <= 6.0 + 1e-6)
    return passed, {
        "max_net_quartic_density": worst_quartic,
        "sign_theorem_holds": bool(sign_ok),
        "identity_max_rel_err": id_rel_err,
        "cauchy_schwarz_bound": 6.0,
        "max_ratio_K_over_TrM2": max_ratio,
        "abelian_ref": {"K": K_ab, "TrM2": TrM2_ab, "ratio": K_ab / TrM2_ab},
        "su2_hedgehog_ref": {"K": K_h, "TrM2": TrM2_h, "ratio": K_h / TrM2_h},
        "note": ("Net leading quartic <= 0 for SU(3), same as SU(2). Bound constant "
                 "changes (K<=6 TrM2 here vs K<=2/3 S there) but conclusion is "
                 "identical: Skyrme dominance structurally absent. NOT a Phase-A "
                 "death (action still PSD); carried to Phase C."),
        "n_samples": n,
    }


def gate_A5_causal_locality(rng, rho=80.0, n_seeds=12):
    """SU(3) links on the Poisson causal lattice: 100% causal + gauge-covariant loop
    holonomy => the action couples only causally connected events."""
    causal_fracs, n_links_list, n_loops_list, gauge_errs = [], [], [], []
    for seed in range(n_seeds):
        r = np.random.default_rng(1000 + seed)
        # 3+1D box (1 time + 3 space), the SU(2) substrate geometry
        pts = s3.sprinkle_box(rho, [(0, 1.0), (0, 1.0), (0, 1.0), (0, 1.0)], r)
        if len(pts) < 8:
            continue
        links = s3.causal_links(pts)
        if len(links) == 0:
            continue
        frac, _ = s3.links_are_causal(pts, links)
        causal_fracs.append(frac)
        n_links_list.append(int(len(links)))

        # assign an SU(3) variable to each directed covering link
        U = {}
        Us = s3.su3_random(len(links), r)
        for (a, b), Uab in zip(links, Us):
            U[(int(a), int(b))] = Uab

        # smallest closed loops of the causal set: 4-element diamonds (the Hasse
        # plaquette).  Holonomy of i->j->l->k->i = U_ij U_jl U_kl^dag U_ik^dag.
        loops = s3.find_diamond_loops(links, max_loops=500)
        n_loops_list.append(int(len(loops)))
        if len(loops) == 0:
            continue
        # gauge covariance: random site transforms g_i; the closed loop holonomy
        # transforms as W -> g_i W g_i^dag, so 1 - (1/3)Re Tr W is invariant.
        g = s3.su3_random(len(pts), r)
        worst = 0.0
        for (i, j, k, l) in loops:
            Uij, Ujl, Ukl, Uik = U[(i, j)], U[(j, l)], U[(k, l)], U[(i, k)]
            H = Uij @ Ujl @ s3.dagger(Ukl) @ s3.dagger(Uik)   # closed loop holonomy
            s_before = s3.wilson_density(H)
            Uij_g = g[i] @ Uij @ s3.dagger(g[j])
            Ujl_g = g[j] @ Ujl @ s3.dagger(g[l])
            Ukl_g = g[k] @ Ukl @ s3.dagger(g[l])
            Uik_g = g[i] @ Uik @ s3.dagger(g[k])
            Hg = Uij_g @ Ujl_g @ s3.dagger(Ukl_g) @ s3.dagger(Uik_g)
            s_after = s3.wilson_density(Hg)
            worst = max(worst, abs(float(s_before) - float(s_after)))
        gauge_errs.append(worst)

    min_causal = float(np.min(causal_fracs)) if causal_fracs else 0.0
    max_gauge = float(np.max(gauge_errs)) if gauge_errs else 1.0
    passed = (min_causal >= 1.0 - 1e-12) and (max_gauge < 1e-9)
    return passed, {
        "min_causal_fraction": min_causal,
        "mean_causal_fraction": float(np.mean(causal_fracs)) if causal_fracs else 0.0,
        "links_per_seed": s3.seed_stats(n_links_list) if n_links_list else {},
        "diamond_loops_per_seed": s3.seed_stats(n_loops_list) if n_loops_list else {},
        "max_gauge_invariance_err": max_gauge,
        "rho": rho, "n_seeds": len(causal_fracs),
        "analytic": ("links = transitive reduction of the timelike relation "
                     "(identical to SU(2) substrate); loop holonomy W->gWg^dag"),
    }


def main():
    rng = np.random.default_rng(20260616)
    print("=" * 72)
    print("FL1_SU3_FOUNDATION -- Phase A (definition / positivity / causality)")
    print("=" * 72)

    results = {}
    pa1, d1 = gate_A1_group_axioms(rng); results["A1_group_axioms"] = d1
    print(f"A1 group axioms          : {'PASS' if pa1 else 'FAIL'}  "
          f"(max err {max(d1['gellmann_norm_err'], d1['random_unit_err'], d1['associativity_err']):.1e})")
    pa2, d2 = gate_A2_wilson_psd(rng); results["A2_wilson_psd"] = d2
    print(f"A2 Wilson action PSD     : {'PASS' if pa2 else 'FAIL'}  "
          f"(min density {d2['min_density_overall']:+.2e}, identity {d2['identity_density']:.1e})")
    pa3, d3 = gate_A3_sigma_psd(rng); results["A3_sigma_psd"] = d3
    print(f"A3 sigma term PSD        : {'PASS' if pa3 else 'FAIL'}  "
          f"(min sigma density {d3['min_sigma_density']:+.2e})")
    pa4, d4 = gate_A4_cauchy_schwarz(rng); results["A4_cauchy_schwarz"] = d4
    print(f"A4 Cauchy-Schwarz/sign   : {'PASS' if pa4 else 'FAIL'}  "
          f"(max net quartic {d4['max_net_quartic_density']:+.1e}, "
          f"max K/TrM2 {d4['max_ratio_K_over_TrM2']:.3f}/6, id err {d4['identity_max_rel_err']:.1e})")
    pa5, d5 = gate_A5_causal_locality(rng); results["A5_causal_locality"] = d5
    print(f"A5 causal locality       : {'PASS' if pa5 else 'FAIL'}  "
          f"(causal frac {d5['min_causal_fraction']:.4f}, gauge err {d5['max_gauge_invariance_err']:.1e})")

    all_pass = pa1 and pa2 and pa3 and pa4 and pa5
    verdict = "PHASE A PASSES" if all_pass else "PHASE A DEATH"
    print("-" * 72)
    print(f"VERDICT: {verdict}")
    print("=" * 72)

    results["verdict"] = {
        "phase_A_passes": bool(all_pass),
        "A1": bool(pa1), "A2": bool(pa2), "A3": bool(pa3),
        "A4": bool(pa4), "A5": bool(pa5),
        "action_positive_semidefinite": bool(pa2 and pa3),
        "causal_locality_preserved": bool(pa5),
    }
    s3.save_json("FLA_definition.json", results)
    return results


if __name__ == "__main__":
    main()
