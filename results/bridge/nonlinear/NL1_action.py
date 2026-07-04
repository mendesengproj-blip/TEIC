"""NL1_action.py -- Is the non-linear coefficient lambda geometric or free? (analytic)

BRIDGE / NON-LINEAR investigation.  Independent of R1-R3 and e6-e11; modifies
nothing.  Continues BRIDGE_DYNAMICS.md (D1-D3 closed the bridge at FIRST order:
theta = GM/rc^2).  NL1 asks whether the *second* order of Schwarzschild -- the
quadratic term of rho_eff/rho0 = 1/sqrt(1-2GM/rc^2) -- is fixed by the
Benincasa-Dowker action, or requires a free parameter.

Two facts established here (symbolically):

  (A) The CORRECT second-order coefficient.  The bridge density is
          rho_eff/rho0 = 1/sqrt(1-2u) = 1 + u + (3/2) u^2 + (5/2) u^3 + ...,  u=GM/rc^2,
      so its quadratic coefficient is +3/2 (and theta = rho_eff/rho0 - 1 has
      A2/A1^2 = 3/2).  The value 1/2 in the prompt is the coefficient of the
      REDSHIFT sqrt(1-2u) = 1 - u - (1/2) u^2 (the reciprocal quantity, dtau/dt),
      NOT of the density.  We target 3/2 for the density throughout.

  (B) Which non-linearity can even produce a 1/r^2 term.  A point-mass linear
      solution is theta1 = M/r.  Feeding it through candidate non-linear sources of
      the static equation nabla^2 theta = (source) + (non-linear term):
        * lambda theta^2     -> theta2 ~ lambda M^2 ln r   (a LOG, not 1/r^2)
        * lambda (grad theta)^2 -> theta2 = lambda M^2 /(2 r^2)  (clean 1/r^2)
      So the prompt's lambda theta^2 does NOT give a clean quadratic term; the
      gradient self-coupling lambda (grad theta)^2 does, and matching +3/2 needs
      lambda = 3.

The decisive question (NL1): is that lambda fixed by the BD action?

  The smeared BD action is QUADRATIC in the field,
      S_BD,smeared = sum_x (B_eps phi)(x) phi(x) V_x,
  because the smeared Sorkin operator B_eps is LINEAR (D1).  Its variation gives the
  linear equation B_eps phi = J -> box theta = 4 pi G T/c^4.  There is NO cubic
  (phi^3) or gradient-self-coupling term in S_BD: adding lambda sum phi^3 V (prompt)
  or lambda (grad theta)^2 imports a term the action does not contain.  Hence:

      => lambda is a FREE parameter at the level of the BD action.

  The only place a geometric non-linearity hides in BD is the curved-space limit
  <B phi> -> box phi - (1/2) R phi: the -(1/2) R phi curvature coupling, with R
  itself sourced by the field's energy, IS a genuine geometric non-linearity -- but
  extracting its coefficient needs the full non-linear map R[theta] (the causal-set
  Einstein/Regge sector), which is NOT contained in the quadratic action as used.
  That is the open frontier (documented; not attempted here).

VERDICT (NL1 death criterion, prompt): if lambda is free -> the non-linearity is
NOT derived -> needs physics beyond the BD action.  That is what we find: lambda is
free.  Per the prompt, NL2/NL3 proceed regardless (their evidence is numerical and
independent of NL1).

ANTI-CIRCULARITY.  Everything Schwarzschild (1/sqrt(1-2u), the coefficients 3/2,
1/2) lives in clearly-marked COMPARISON ONLY reasoning; the generator/derivation
content is only the BD action's structure (quadratic) and the radial Green's
function.  No sqrt(1-2M/r) is used to generate anything.
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent


# COMPARISON ONLY: the GR/Schwarzschild Taylor series is the comparison TARGET that the
# network-derived non-linear coefficient is matched against; it is a pure symbolic
# expansion (no data generator in this file) and is never fed into any sprinkling.
def schwarzschild_coeffs():
    """Exact Taylor coefficients of the density 1/sqrt(1-2u) and redshift sqrt(1-2u)."""
    u = sp.symbols("u", positive=True)
    dens = sp.series((1 - 2 * u) ** sp.Rational(-1, 2), u, 0, 4).removeO()
    red = sp.series((1 - 2 * u) ** sp.Rational(1, 2), u, 0, 4).removeO()
    return {
        "density_series": str(dens),
        "redshift_series": str(red),
        "density_u2_coeff": sp.nsimplify(dens.coeff(u, 2)),     # 3/2
        "redshift_u2_coeff": sp.nsimplify(red.coeff(u, 2)),     # -1/2
    }
# END COMPARISON ONLY


def nonlinear_second_order():
    """Which non-linear source gives a clean 1/r^2 second-order term, and the lambda
    that matches the density's +3/2."""
    r, M, lam = sp.symbols("r M lambda", positive=True)
    th1 = M / r                                                 # linear point-mass field
    y = sp.Function("y")

    def lap3(f):                                               # 3D radial Laplacian
        return sp.diff(r ** 2 * sp.diff(f, r), r) / r ** 2

    # lambda theta^2 source
    th2_sq = sp.dsolve(sp.Eq(lap3(y(r)), lam * th1 ** 2), y(r)).rhs
    # lambda (grad theta)^2 source
    th2_grad = sp.dsolve(sp.Eq(lap3(y(r)), lam * sp.diff(th1, r) ** 2), y(r)).rhs
    # coefficient of 1/r^2 in the gradient case (drop homogeneous C1 + C2/r)
    C1, C2 = sp.symbols("C1 C2")
    grad_clean = th2_grad.subs({sp.Symbol("C1"): 0, sp.Symbol("C2"): 0})
    coeff_1_over_r2 = sp.simplify(grad_clean * r ** 2 / M ** 2)  # = lambda/2
    lam_star = sp.solve(sp.Eq(coeff_1_over_r2, sp.Rational(3, 2)), lam)[0]  # 3
    return {
        "theta2_from_theta_squared": str(sp.simplify(th2_sq)),
        "theta2_from_gradient_squared": str(sp.simplify(th2_grad)),
        "gradient_1_over_r2_coeff_in_lambda": str(coeff_1_over_r2),  # lambda/2
        "lambda_matching_3_2": str(sp.nsimplify(lam_star)),          # 3
    }


def main():
    sch = schwarzschild_coeffs()
    nl = nonlinear_second_order()

    # BD action is quadratic -> the operator is linear -> no intrinsic cubic/gradient
    # self-coupling.  This is a structural fact, encoded as the verdict.
    bd_action_is_quadratic = True
    lambda_is_geometric = False        # NOT fixed by the BD action
    lambda_is_free = not lambda_is_geometric

    target_density_coeff = sp.Rational(3, 2)
    prompt_value = sp.Rational(1, 2)
    prompt_value_is_redshift_not_density = (sch["redshift_u2_coeff"] == -prompt_value)

    verdict = "lambda LIVRE (nao geometrico)" if lambda_is_free else "lambda GEOMETRICO"

    summary = {
        "what": "Is the non-linear coefficient lambda fixed by the BD action? -> NO (free).",
        "schwarzschild": {k: str(v) for k, v in sch.items()},
        "correct_density_2nd_order_coeff": str(target_density_coeff),
        "prompt_value_one_half_is_redshift_coeff_not_density":
            bool(prompt_value_is_redshift_not_density),
        "nonlinear_structure": nl,
        "lambda_theta2_gives_log_not_r2": True,
        "gradient_coupling_gives_clean_r2": True,
        "lambda_matching_density_3_2": str(nl["lambda_matching_3_2"]),
        "bd_action_is_quadratic": bd_action_is_quadratic,
        "lambda_is_geometric": lambda_is_geometric,
        "lambda_is_free": lambda_is_free,
        "geometric_nonlinearity_lives_in": "-(1/2) R phi curvature coupling + causal-"
            "structure back-reaction (Regge / causal-set Einstein sector) -- OPEN "
            "FRONTIER, not contained in the quadratic BD action.",
        "verdict": verdict,
        "note": "NL1 death criterion met: lambda free -> non-linearity not derived. "
                "Per the prompt, NL2/NL3 proceed (numerical, independent of NL1). "
                "Target for NL2/NL3 is the DENSITY coefficient 3/2, not the prompt's "
                "1/2 (which is the redshift's).",
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "NL1_action_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("NL1 -- IS THE NON-LINEAR COEFFICIENT lambda GEOMETRIC OR FREE? (analytic)")
    print("=" * 72)
    print(f"density  1/sqrt(1-2u) = {sch['density_series']}")
    print(f"redshift sqrt(1-2u)   = {sch['redshift_series']}")
    print(f"  -> CORRECT density 2nd-order coeff = {sch['density_u2_coeff']}  "
          f"(target for NL2/NL3)")
    print(f"  -> prompt's 1/2 is the REDSHIFT coeff ({sch['redshift_u2_coeff']}), "
          f"a different (reciprocal) quantity")
    print("-" * 72)
    print("Which non-linearity yields a clean 1/r^2 second order? (theta1 = M/r)")
    print(f"  lambda*theta^2       -> theta2 = {nl['theta2_from_theta_squared']}  "
          f"(LOG -> not 1/r^2)")
    print(f"  lambda*(grad theta)^2-> theta2 = {nl['theta2_from_gradient_squared']}")
    print(f"     1/r^2 coeff = {nl['gradient_1_over_r2_coeff_in_lambda']} -> "
          f"matches 3/2 at lambda = {nl['lambda_matching_3_2']}")
    print("-" * 72)
    print(f"BD smeared action is QUADRATIC (operator B_eps linear): "
          f"{bd_action_is_quadratic}")
    print(f"  -> no intrinsic phi^3 / (grad theta)^2 term; lambda is NOT fixed by BD")
    print(f"  -> geometric non-linearity would live in -(1/2)R phi back-reaction "
          f"(open frontier)")
    print("-" * 72)
    print(f"VERDICT (NL1): {verdict}")
    print("  lambda free -> non-linearity not DERIVED from BD. NL2/NL3 proceed anyway")
    print("  (numerical evidence is independent of NL1).")
    return summary


if __name__ == "__main__":
    main()
