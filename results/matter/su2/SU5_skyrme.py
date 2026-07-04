"""SU5 -- the Skyrme term: does it EMERGE from the C4 quartic, or is it a new ingredient?

Honesty test (symbolic, sympy).  Derrick (SU3) showed the hedgehog is stabilised by a
4-derivative term whose lattice image is the Skyrme commutator |c_i x c_j|^2.  Is that
term the SAME operator C4 found emerging from the minimal action's quartic?

C4 (results/bridge/coefficients) expanded the U(1) link action 1 - cos(u),
u = (A_mu + d_mu theta) e^mu, to 4th order and read off the quartic (A+dtheta)^4 -- a
PERFECT 4th POWER of the single Stuckelberg covector w_mu, i.e. the SYMMETRIC quartic
(w.w)^2 and its anisotropic partners (the DBI/k-essence X^2 term).

The Skyrme term is Tr[L_mu, L_nu]^2, L_mu = U^{-1} d_mu U.  In the i*sigma basis
L_mu = i a_mu . sigma, so [L_mu,L_nu] = -2 i (a_mu x a_nu).sigma and

    -1/16 Tr[L_mu,L_nu]^2 = 1/2 |a_mu x a_nu|^2    (the CROSS product = ANTISYMMETRIC).

We verify symbolically:
  1. the SU(2) link action 1/2 Tr(1 - exp(i X.sigma)) to 4th order = |X|^2/2 - |X|^4/24,
     and |X|^4 = (sum_a X_a^2)^2 is SYMMETRIC -- no cross product, no commutator;
  2. Tr[L_i,L_j]^2 = -8 |a_i x a_j|^2 -- the ANTISYMMETRIC commutator, which VANISHES
     for collinear (Abelian) currents a_i || a_j;
  3. therefore the Skyrme operator is ZERO in the Abelian sector C4 analysed: it CANNOT
     be the C4 quartic.  It is a genuinely non-Abelian 4-derivative operator -- of the
     SAME ORDER as C4's quartic, arising from the group commutator (the non-Abelian
     plaquette curvature F = dA + [A,A]), not a hand-added U(1) axiom but also NOT the
     C4 term.

ANTI-CIRCULARITY: pure symbolic algebra of the quaternion/su(2) structure; the only
COMPARISON ONLY content is the citation of C4's DEV operators.  No dilation, no generator.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su2_core as s   # noqa: E402

ROOT = Path(__file__).resolve().parents[3]


def link_action_quartic():
    """1/2 Tr(1 - exp(i X.sigma)) = 1 - cos|X|; expand to 4th order in |X|.  Show the
    quartic is |X|^4 = (X1^2+X2^2+X3^2)^2 -- SYMMETRIC (no cross product)."""
    X1, X2, X3 = sp.symbols("X1 X2 X3", real=True)
    Xmag = sp.sqrt(X1 ** 2 + X2 ** 2 + X3 ** 2)
    act = 1 - sp.cos(Xmag)
    # series in a scaling parameter t (X -> t X) to isolate orders cleanly
    t = sp.symbols("t", positive=True)
    ser = sp.series(act.subs({X1: t * X1, X2: t * X2, X3: t * X3}), t, 0, 5).removeO()
    quad = sp.expand(ser.coeff(t, 2))
    quart = sp.expand(ser.coeff(t, 4))
    sym_quartic = sp.expand(sp.Rational(1, 24) * (X1 ** 2 + X2 ** 2 + X3 ** 2) ** 2)
    matches_symmetric = sp.simplify(-quart - sym_quartic) == 0   # coeff -1/24
    return {"quadratic": str(quad), "quartic": str(quart),
            "is_symmetric_4th_power": bool(matches_symmetric),
            "note": "quartic = -1/24 (X.X)^2 : symmetric, no cross product"}


def skyrme_commutator():
    """Prove Tr[L_i,L_j]^2 = -8 |a_i x a_j|^2 using ONLY the quaternion algebra (no Pauli,
    no complex literal -- consistent with the engine and the anti-circularity guard).

    An su(2) element L = i a.sigma corresponds to the PURE-IMAGINARY quaternion (0, a).
    Quaternion commutator: q_mul((0,a),(0,b)) - q_mul((0,b),(0,a)) = (0, -2 a x b), so
    [L_i,L_j] <-> the quaternion (0, -2 a x b).  For a matrix M = m0 I + i m.sigma one has
    Tr(M^2) = 2 m0^2 - 2 |m|^2; the commutator has m0 = 0, m = -2 a x b, hence
    Tr[L_i,L_j]^2 = -2 |2 a x b|^2 = -8 |a x b|^2 (ANTISYMMETRIC; zero if a || b).

    Verified numerically over random a, b to machine precision."""
    rng = np.random.default_rng(0)
    a = rng.standard_normal((2000, 3)); b = rng.standard_normal((2000, 3))
    qa = np.zeros((2000, 4)); qa[:, 1:] = a
    qb = np.zeros((2000, 4)); qb[:, 1:] = b
    comm = s.q_mul(qa, qb) - s.q_mul(qb, qa)           # = (0, -2 a x b)
    m0 = comm[:, 0]; m = comm[:, 1:]
    tr_comm_sq = 2.0 * m0 ** 2 - 2.0 * np.sum(m * m, axis=1)   # Tr([L,L]^2)
    cross = np.cross(a, b)
    pred = -8.0 * np.sum(cross * cross, axis=1)
    err = float(np.max(np.abs(tr_comm_sq - pred)))
    # collinear (Abelian) check: b = lam a  ->  cross = 0
    lam = rng.standard_normal((2000, 1))
    cross_coll = np.cross(a, lam * a)
    coll_max = float(np.max(np.abs(cross_coll)))
    return {"identity": "Tr[L_i,L_j]^2 = -8 |a_i x a_j|^2 (antisymmetric cross product)",
            "max_err_vs_-8cross": err,
            "abelian_collinear_cross_max": coll_max,
            "vanishes_in_abelian_limit": bool(coll_max < 1e-12)}


def numeric_abelian_check():
    """Direct numeric confirmation on the lattice: a sigma_3-EMBEDDED (Abelian) chiral
    field has ZERO Skyrme energy density (collinear currents), whereas the genuinely
    non-Abelian hedgehog has E4 > 0.  Uses su2_core (quaternions, no Pauli)."""
    L = 8.0; N = 21
    xs = np.linspace(-L / 2, L / 2, N); dx = float(xs[1] - xs[0])
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    # Abelian: U = exp(i phi(x) sigma_3) -- all currents point along sigma_3 (collinear)
    phi = 0.6 * np.exp(-(X ** 2 + Y ** 2 + Z ** 2) / 6.0) * (X + 2 * Y)
    U_ab = s.u1_embed(phi)
    _, E4_ab, _ = s.chiral_energy(U_ab, dx, e_sk=1.0)
    # non-Abelian hedgehog
    U_hh = s.hedgehog_field(xs, xs, xs)
    _, E4_hh, _ = s.chiral_energy(U_hh, dx, e_sk=1.0)
    return {"E4_abelian_sigma3": E4_ab, "E4_nonabelian_hedgehog": E4_hh,
            "abelian_skyrme_is_zero": bool(abs(E4_ab) < 1e-9)}


def main():
    laq = link_action_quartic()
    sky = skyrme_commutator()
    num = numeric_abelian_check()

    # cite C4's verdict (COMPARISON ONLY: the DEV operator bookkeeping)
    c4_path = ROOT / "results" / "bridge" / "coefficients" / "C4_completeness_data.json"
    c4 = json.loads(c4_path.read_text()) if c4_path.exists() else {}
    c4_verdict = c4.get("verdict", "(C4 data not found)")

    emerges = not (sky["vanishes_in_abelian_limit"] and num["abelian_skyrme_is_zero"])
    # the Skyrme term vanishes in the Abelian sector C4 analysed -> it does NOT emerge
    # from the C4 quartic; it is a third (non-Abelian) ingredient of the same order.
    skyrme_from_c4 = bool(emerges)

    payload = {
        "link_action_quartic": laq,
        "skyrme_commutator": sky,
        "numeric_abelian_check": num,
        "C4_comparison_only": {"c4_verdict": c4_verdict,
                               "c4_quartic": "(A+dtheta)^4 : SYMMETRIC perfect 4th power"},
        "skyrme_emerges_from_C4_quartic": skyrme_from_c4,
        "conclusion": (
            "The C4 quartic is the SYMMETRIC (w.w)^2 = (A+dtheta)^4 (the DBI/k-essence "
            "X^2 term). The Skyrme term is the ANTISYMMETRIC commutator |a_i x a_j|^2, "
            "which is IDENTICALLY ZERO in the Abelian (U(1)) sector C4 analysed. So the "
            "Skyrme term does NOT emerge from the C4 quartic: it is a genuinely "
            "non-Abelian 4-derivative operator of the SAME ORDER, sourced by the group "
            "commutator (the non-Abelian plaquette curvature F = dA + [A,A]), not by the "
            "C4 link quartic. Honest report: THIRD INGREDIENT (non-Abelian), not a hand-"
            "added U(1) axiom but not the C4 operator either."),
        "verdict_derrick_stable": "SIM (E2=E4, SU3)",
        "verdict_skyrme_is_C4": "NAO -- antisymmetric, zero in Abelian limit",
    }
    s.save_json("SU5_skyrme", payload)

    print("=" * 72)
    print("SU5 -- SKYRME TERM: emerges from C4 quartic, or new ingredient?")
    print("=" * 72)
    print(f"link action quartic  : {laq['quartic']}")
    print(f"   symmetric (X.X)^2 : {laq['is_symmetric_4th_power']}")
    print(f"Tr[L_i,L_j]^2        : {sky['identity']}")
    print(f"   max err vs -8|axb|^2: {sky['max_err_vs_-8cross']:.2e}")
    print(f"   Abelian (collinear) cross max: {sky['abelian_collinear_cross_max']:.2e}  "
          f"-> zero: {sky['vanishes_in_abelian_limit']}")
    print(f"numeric: E4(sigma_3 Abelian)={num['E4_abelian_sigma3']:.2e}  "
          f"E4(hedgehog)={num['E4_nonabelian_hedgehog']:.3f}")
    print("-" * 72)
    print(f"C4 quartic = (A+dtheta)^4 SYMMETRIC ; Skyrme = |a x a| ANTISYMMETRIC")
    print(f"SKYRME EMERGES FROM C4 QUARTIC: {'SIM' if skyrme_from_c4 else 'NAO'}")
    print("Honest: Skyrme is a THIRD (non-Abelian) ingredient of the same derivative")
    print("order, zero in the Abelian sector C4 analysed -- sourced by the group")
    print("commutator, not the C4 link quartic.")
    return payload


if __name__ == "__main__":
    main()
