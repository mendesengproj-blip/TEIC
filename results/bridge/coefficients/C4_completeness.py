"""C4_completeness.py -- 4th-order expansion of the minimal action vs the DEV.

BRIDGE / COEFFICIENTS, task C4: the anti-reverse-engineering test.  Symbolic
(sympy).  We expand the one-line action density

    L_link = Dtau * [ 1 - cos(u) ] ,    u = phi + Dtheta = (A_mu + d_mu theta) e^mu ,

to FOURTH order in u and read off every operator it predicts after coarse-graining
(replacing products of e^mu by their Dtau-weighted Poisson moments measured in C1).
We then compare term by term with the current DEV scalar/vector Lagrangian, which
appears ONLY in the clearly-marked COMPARISON block.

The expansion coefficients of 1 - cos(u) = u^2/2 - u^4/24 + u^6/720 - ... are pure
numbers (Taylor), not fits.  The question C4 answers: does the minimal action
predict EXACTLY the DEV operators, EXTRA operators, or MISS some?
"""

from __future__ import annotations

import json
import time
from pathlib import Path

import sympy as sp

OUT = Path(__file__).resolve().parent


def cos_expansion(order=4):
    """Taylor coefficients of 1 - cos(u) up to u^order (pure numbers)."""
    u = sp.symbols("u")
    series = sp.series(1 - sp.cos(u), u, 0, order + 1).removeO()
    poly = sp.Poly(series, u)
    return {int(m[0]): sp.nsimplify(c) for m, c in poly.terms()}


def gauge_invariant_combo():
    """Show u = (A_mu + d_mu theta) e^mu so every power of u is a power of the
    SINGLE gauge-invariant Stuckelberg covector w_mu = A_mu + d_mu theta.

    Returns the symbolic quadratic and quartic operator content (before moment
    contraction) as strings, plus the structural facts.
    """
    # 2D illustration is enough for the operator BOOKKEEPING (the structure is
    # dimension-independent): w = (w0, w1), e = (et, ex).
    w0, w1, et, ex = sp.symbols("w0 w1 et ex", real=True)
    u = w0 * et + w1 * ex
    quad = sp.expand(u ** 2)           # -> quadratic operators * e-bilinears
    quartic = sp.expand(u ** 4)        # -> quartic operators * e-quadrilinears
    return u, quad, quartic, (w0, w1, et, ex)


def main():
    coeffs = cos_expansion(4)
    c2 = coeffs.get(2, 0)              # 1/2
    c4 = coeffs.get(4, 0)             # -1/24
    u, quad, quartic, syms = gauge_invariant_combo()
    w0, w1, et, ex = syms

    # --- structural read-off (dimension-independent) ------------------------
    # Quadratic sector (order u^2, coeff 1/2), contracted with M2=<Dtau e e>:
    #   (1/2) w_mu w_nu <Dtau e^mu e^nu>
    #   = (1/2)[ kappa (w.w) + lambda (w.u)^2 ]      (C1 decomposition)
    #   kappa-part  ->  kappa/2 * (A+dtheta)^2  = perfect square
    #                = kappa/2 [ A^2 + 2 A.dtheta + (dtheta)^2 ]
    #   => among the Lorentz-invariant operators the coefficient RATIOS are fixed:
    #        (dtheta)^2 : A.dtheta : A^2  =  1 : 2 : 1   (the 1-2-1 of a square)
    #   lambda-part ->  lambda/2 * (A_0+d_0 theta)^2  = Lorentz-violating extras.
    quad_ops = {
        "(dtheta)^2 [X]": sp.Rational(1, 2),       # from (1/2) w.w, kappa-part
        "A.dtheta":       sp.Integer(1),           # cross term has 2x
        "A^2":            sp.Rational(1, 2),
    }
    # Quartic sector (order u^4, coeff -1/24), contracted with the 4th moment
    # M4=<Dtau e e e e>.  u^4 = (w.e)^4 -> every quartic in w_mu:
    #   w0^4, w0^3 w1, w0^2 w1^2, w0 w1^3, w1^4  (and their D-dim analogues),
    # i.e. the full gauge-invariant quartic self-interaction  (A+dtheta)^4  and
    # its anisotropic partners.  Operators present:
    #   (dtheta)^4, A.dtheta (dtheta)^2, A^2 (dtheta)^2, (A.dtheta)^2,
    #   A^3.dtheta, A^4   -- all from one perfect 4th power.
    # explicit list of quartic w-monomials from (w0 et + w1 ex)^4
    qp = sp.Poly(quartic, w0, w1)
    quartic_w_monomials = []
    for monom, c in qp.terms():
        pows = dict(zip((w0, w1), monom))
        quartic_w_monomials.append(
            {"w0_power": int(pows.get(w0, 0)), "w1_power": int(pows.get(w1, 0)),
             "e_factor": str(c)})

    # --------------------------------------------------------------------- #
    # COMPARISON ONLY: the current DEV scalar/vector Lagrangian
    #   L_DEV = F(X,theta) - (K/4) Fmn F^mn - (mA^2/2) A.A + gamma A.dtheta
    # (docs/DEV_bridge_future.md, eq.1).  F(X) is a general k-essence function:
    #   F(X) = F0 + F1 X + F2 X^2 + ...   with X = (dtheta)^2 (up to convention).
    # --------------------------------------------------------------------- #
    dev = {
        "quadratic": {
            "(dtheta)^2 [X]": "F1   (free, k-essence kinetic)",
            "A^2":            "-mA^2/2   (free mass)",
            "A.dtheta":       "gamma   (free Stuckelberg coupling)",
            "Fmn F^mn":       "-K/4   (free Maxwell coeff, from PLAQUETTES not links)",
        },
        "quartic": {
            "(dtheta)^4 [X^2]": "F2   (present: k-essence / DBI X^2 term)",
            "A^4, A^3 dtheta, A^2 (dtheta)^2, (A.dtheta)^2":
                "ABSENT (DEV vector sector is at most quadratic in A)",
        },
    }
    # END COMPARISON ONLY

    # Verdicts, term by term --------------------------------------------------
    findings = {
        "match_kinetic_quartic": (
            "(dtheta)^4 predicted by minimal action (-1/24 (dtheta)^4 piece) AND "
            "present in DEV as F2 X^2 / DBI expansion. STRUCTURAL MATCH (coeff free in DEV)."),
        "extra_stuckelberg_quartics": (
            "A^4, A^3.dtheta, A^2(dtheta)^2, (A.dtheta)^2: predicted by the minimal "
            "action's perfect 4th power (A+dtheta)^4, ABSENT in the DEV. EXTRA PREDICTIONS."),
        "missing_maxwell": (
            "F_mn F^mn: present in DEV (-K/4), but the LINK action sum_links cos(.) "
            "produces NO plaquette/curl, so F^2 is NOT generated by links. The minimal "
            "action MISSES the vector kinetic term -> A is auxiliary (varies to pure gauge "
            "A=-dtheta) unless a separate plaquette term sum_loops cos(F-flux) is added "
            "(Sverdlov-Bombelli). The 5-term S_eff is links(4 terms)+plaquettes(F^2)."),
        "lorentz_violating_extras": (
            "lambda-part of every even moment adds (A_0+d_0 theta)^{2n} Lorentz-violating "
            "operators absent from the (covariant) DEV; their size is set by C1's anisotropy."),
    }

    summary = {
        "cos_taylor_coeffs_1_minus_cos": {str(k): str(v) for k, v in coeffs.items()},
        "u_definition": "u = (A_mu + d_mu theta) e^mu  (single gauge-invariant covector w_mu)",
        "quadratic_u2_expanded": str(quad),
        "quartic_u4_expanded": str(quartic),
        "quadratic_operator_coeffs_1_2_1": {k: str(v) for k, v in quad_ops.items()},
        "quartic_w_monomials_from_(w.e)^4": quartic_w_monomials,
        "COMPARISON_DEV": dev,
        "findings": findings,
        "verdict": ("ALL THREE cases occur for different operators: MATCH (dtheta)^4, "
                    "EXTRA Stuckelberg quartics + LV terms, MISSING Maxwell F^2."),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "C4_completeness_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("C4 -- 4th-ORDER EXPANSION OF THE MINIMAL ACTION vs THE DEV")
    print("=" * 72)
    print(f"1 - cos(u) Taylor coeffs : {[ (k,str(v)) for k,v in coeffs.items() ]}")
    print(f"u = (A_mu + d_mu theta) e^mu   (one gauge-invariant covector)")
    print("-" * 72)
    print(f"order u^2 (coeff {c2}):  u^2 = {quad}")
    print("  -> after <Dtau e e>:  kappa/2 (A+dtheta)^2 + lambda/2 (A_0+d_0theta)^2")
    print("  -> LI operator ratios (dtheta)^2 : A.dtheta : A^2 = 1 : 2 : 1  (square)")
    print(f"order u^4 (coeff {c4}):  u^4 = {quartic}")
    print("  -> after <Dtau eeee>: full (A+dtheta)^4 self-interaction:")
    for m in quartic_w_monomials:
        print(f"       w0^{m['w0_power']} w1^{m['w1_power']}  x  {m['e_factor']}")
    print("-" * 72)
    print("COMPARISON with DEV  L=F(X,theta) - K/4 F^2 - mA^2/2 A^2 + gamma A.dtheta:")
    print("  MATCH   : (dtheta)^4  <-> F2 X^2 / DBI   (both have it; DEV coeff free)")
    print("  EXTRA   : A^4, A^3 dtheta, A^2(dtheta)^2, (A.dtheta)^2  (NOT in DEV)")
    print("  MISSING : F_mn F^mn   (in DEV; links give no plaquette -> needs loops)")
    print("  EXTRA   : Lorentz-violating (A_0+d_0theta)^{2n} from anisotropy lambda")
    print("-" * 72)
    print("VERDICT (C4):", summary["verdict"])
    return summary


if __name__ == "__main__":
    main()
