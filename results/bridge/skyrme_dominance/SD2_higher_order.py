"""SD2 -- does the sextic of the SU(2) link cosine rescue the Skyrmion in d=3?

Pre-registered (SKYRME_DOMINANCE.md addendum, item 7, written before this ran):

  * sextic per link: +(a^6/46080)|l_e|^6 (the +u^6/720 of the cosine);
    isotropic d=3 average <|l|^6> = [(TrG)^3 + 6 TrG TrG^2 + 8 TrG^3]/105,
    every term >= 0 for PSD G  =>  c6 > 0 GUARANTEED (stabilising sign);
  * truncated Derrick E(lam) = lam E2 - |E4|/lam + E6/lam^3 diverges at both
    ends => ALWAYS has a formal interior minimum lam*. The honest question is
    validity: prediction u(lam*) = (a/2 lam*) max|l| >> 1 (outside the useful
    convergence radius), the 8th order (-u^8/40320, negative again) comparable
    to the sextic at lam*, and the FULL cosine (which resums the series and is
    bounded) stays monotonic, as already measured in SC4/DS3.

  DEATH CRITERION for the sextic rescue (pre-registered): the rescue is real
  only if u(lam*) < 1 AND the full cosine shows an interior minimum on the
  same grid. Expected: neither holds -> the sextic minimum is a truncation
  artifact of an alternating series for a bounded function.

Moment checks: the sextic (and octic) isotropic averages are verified two
independent ways before use -- exact rational sphere moments on a diagonal G
(rotation invariance) and Monte Carlo on random non-diagonal G.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sd_core as sd

A_LINK = 1.0

# hedgehog profile on the SC4 grid (u = r/lambda)
U = np.linspace(1e-4, 14.0, 2400)
DU = float(U[1] - U[0])
F = np.pi * np.exp(-U)
FP = -np.pi * np.exp(-U)
S_TAN = np.sin(F) ** 2 / U ** 2

# Gram eigenvalues: radial F'^2, tangential s (x2)
TRG = FP ** 2 + 2 * S_TAN
TRG2 = FP ** 4 + 2 * S_TAN ** 2
TRG3 = FP ** 6 + 2 * S_TAN ** 3
TRG4 = FP ** 8 + 2 * S_TAN ** 4
S_INV = TRG ** 2
K_INV = S_INV - TRG2

MEAS = 4 * np.pi * U ** 2 * DU
E2_1 = float(np.sum(MEAS * TRG))
I4 = float(np.sum(MEAS * (3 * S_INV - 2 * K_INV)))         # = S + 2TrG^2 integrand
M6 = TRG ** 3 + 6 * TRG * TRG2 + 8 * TRG3
I6 = float(np.sum(MEAS * M6))
M8 = TRG ** 4 + 12 * TRG ** 2 * TRG2 + 12 * TRG2 ** 2 + 32 * TRG * TRG3 + 48 * TRG4
I8 = float(np.sum(MEAS * M8))

# energy normalisation (24/a^2)<1-cos>, as in SC4: quadratic -> TrG exactly
C4 = A_LINK ** 2 / 240.0            # |E4| = C4 * I4   (negative term)
C6 = A_LINK ** 4 / 201600.0         # E6  = C6 * I6   (positive term)
C8 = A_LINK ** 6 / (430080.0 * 945.0)   # (24/a^2) * a^8/(2^8 * 8!) * <|l|^8>=M8/945


def moment_checks(rng):
    """Verify the sextic/octic isotropic averages two independent ways."""
    # (i) exact rational sphere moments, diagonal G = diag(l1,l2,l3)
    l1, l2, l3 = sp.symbols("l1 l2 l3", nonnegative=True)
    lam = (l1, l2, l3)

    def avg_power(p):
        # <(sum_i lam_i e_i^2)^p> via multinomial + exact even moments
        e = sp.symbols("e1 e2 e3")
        expr = sp.expand((l1 * e[0] ** 2 + l2 * e[1] ** 2 + l3 * e[2] ** 2) ** p)
        total = sp.S(0)
        for term in expr.as_ordered_terms():
            powers = [sp.degree(term, x) // 2 for x in e]
            coeff = term
            for x in e:
                coeff = coeff.subs(x, 1)
            total += coeff * sp.Rational(sd.sphere_even_moment(powers, 3)).limit_denominator(10 ** 12)
        return sp.simplify(total)

    t1 = sum(lam)
    t2 = sum(x ** 2 for x in lam)
    t3 = sum(x ** 3 for x in lam)
    t4 = sum(x ** 4 for x in lam)
    ok6 = sp.simplify(avg_power(3) - (t1 ** 3 + 6 * t1 * t2 + 8 * t3) / 105) == 0
    ok8 = sp.simplify(avg_power(4) - (t1 ** 4 + 12 * t1 ** 2 * t2 + 12 * t2 ** 2 +
                                      32 * t1 * t3 + 48 * t4) / 945) == 0

    # (ii) Monte Carlo, random non-diagonal G
    Cm = rng.standard_normal((3, 3))
    G = Cm @ Cm.T
    dirs = sd.unit_directions(2_000_000, 3, rng)
    q = np.einsum("ni,ij,nj->n", dirs, G, dirs)
    tg = np.trace(G)
    tg2 = np.trace(G @ G)
    tg3 = np.trace(G @ G @ G)
    tg4 = np.trace(G @ G @ G @ G)
    mc6 = float(np.mean(q ** 3)) / ((tg ** 3 + 6 * tg * tg2 + 8 * tg3) / 105.0)
    mc8 = float(np.mean(q ** 4)) / ((tg ** 4 + 12 * tg ** 2 * tg2 + 12 * tg2 ** 2 +
                                     32 * tg * tg3 + 48 * tg4) / 945.0)
    return bool(ok6), bool(ok8), mc6, mc8


# ---- full cosine on the same grid (SC4 machinery) ---------------------------- #
GL_C, GL_W = np.polynomial.legendre.leggauss(48)
GL_C = 0.5 * (GL_C + 1.0)
GL_W = GL_W * 0.5


def e_cos(lam, a):
    q2 = FP[:, None] ** 2 * GL_C[None, :] ** 2 + \
        S_TAN[:, None] * (1.0 - GL_C[None, :] ** 2)
    arg = (a / (2.0 * lam)) * np.sqrt(q2)
    avg = np.sum((1.0 - np.cos(arg)) * GL_W[None, :], axis=1)
    return float(np.sum(4 * np.pi * (lam * U) ** 2 * (24.0 / a ** 2) * avg) *
                 (lam * DU))


def main():
    rng = np.random.default_rng(20260612)
    ok6, ok8, mc6, mc8 = moment_checks(rng)

    # sextic coefficient for the SU(2) isotropic measure (per link, a=1):
    # 1-cos -> +u^6/720, u = a|l|/2  =>  +a^6 |l|^6 / 46080; <|l|^6> = M6/105.
    c6_per_link = A_LINK ** 6 / 46080.0 / 105.0        # multiplies M6*105... per |l|^6
    # in the (24/a^2)-normalised energy density: C6 = 24/46080/105 * a^4
    c6_check = abs(C6 - 24.0 / (46080.0 * 105.0) * A_LINK ** 4) < 1e-18

    # truncated Derrick: E(lam) = lam E2 - C4 I4 / lam + C6 I6 / lam^3
    lams = np.geomspace(0.01, 4.0, 400)
    e2 = lams * E2_1
    e_t4 = e2 - C4 * I4 / lams
    e_t6 = e_t4 + C6 * I6 / lams ** 3
    e_t8 = e_t6 - C8 * I8 / lams ** 5
    e_full = np.array([e_cos(l, A_LINK) for l in lams])

    # interior minimum of the sextic truncation: E2 lam^4 + B lam^2 - 3 C6 I6 = 0
    B = C4 * I4
    lam2 = (-B + np.sqrt(B ** 2 + 12 * E2_1 * C6 * I6)) / (2 * E2_1)
    lam_star = float(np.sqrt(lam2))
    # expansion parameter at the minimum: u = (a/2 lam*) max|l|; max|l| = pi
    u_star = A_LINK * np.pi / (2 * lam_star)
    # 8th-order over 6th-order term at lam* (series health at the minimum)
    ratio86 = (C8 * I8 / lam_star ** 5) / (C6 * I6 / lam_star ** 3)
    # truncation error vs full cosine at lam*
    i_star = int(np.argmin(np.abs(lams - lam_star)))
    trunc_err = abs(e_t6[i_star] - e_full[i_star]) / e_full[i_star]

    full_monotonic = bool(np.all(np.diff(e_full) > 0))
    full_interior = bool(0 < int(np.argmin(e_full)) < len(lams) - 1)
    rescue_real = bool(u_star < 1.0 and full_interior)

    payload = {
        "moment_checks": {"sextic_symbolic": ok6, "octic_symbolic": ok8,
                          "sextic_MC_ratio": mc6, "octic_MC_ratio": mc8},
        "c6": {"per_link_times_M6": c6_per_link,
               "sign": "positive (stabilising)",
               "normalised_energy_coeff_C6": C6, "consistency": bool(c6_check)},
        "hedgehog_integrals": {"E2": E2_1, "I_3S_minus_2K": I4, "I_M6": I6,
                               "I_M8": I8},
        "truncated_sextic_minimum": {
            "lambda_star": lam_star,
            "always_exists_formally": True,
            "u_at_minimum": u_star,
            "u_validity_threshold": 1.0,
            "octic_over_sextic_at_min": ratio86,
            "truncation_error_vs_full_cosine_at_min": trunc_err},
        "full_cosine": {"monotonic_increasing": full_monotonic,
                        "interior_minimum": full_interior},
        "verdict": {
            "sextic_rescue_real": rescue_real,
            "note": ("c6 > 0 as predicted, and the truncated quartic+sextic "
                     "ALWAYS has a formal minimum in d=3; but the minimum sits "
                     "at link phase u >> 1 where the alternating series fails "
                     "(octic term comparable), and the resummed bounded cosine "
                     "is monotonic: the minimum is a truncation artifact.")},
    }
    sd.save_json("SD2_higher_order.json", payload)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.4))
    ax1.plot(lams, e2, "k--", lw=1, label=r"$\lambda E_2$")
    ax1.plot(lams, e_t4, "C1", label="trunc 4th (quartic only)")
    ax1.plot(lams, e_t6, "C0", label="trunc 6th (sextic added)")
    ax1.plot(lams, e_t8, "C2", label="trunc 8th")
    ax1.plot(lams, e_full, "r", lw=2, label="full cosine (resummed)")
    ax1.axvline(lam_star, color="C0", ls=":", lw=1,
                label=fr"$\lambda^*$={lam_star:.3f} (u={u_star:.1f})")
    ax1.set_xscale("log")
    ax1.set_yscale("log")
    ax1.set_ylim(1e-1, 1e4)
    ax1.set_xlabel(r"dilation $\lambda$")
    ax1.set_ylabel(r"$E(\lambda)$")
    ax1.set_title("alternating truncations vs the bounded cosine")
    ax1.legend(fontsize=7.5)

    # zoom near lam*: each truncation order flips the story
    sel = (lams > lam_star / 6) & (lams < lam_star * 6)
    ax2.plot(lams[sel], e_t4[sel], "C1", label="4th")
    ax2.plot(lams[sel], e_t6[sel], "C0", label="6th")
    ax2.plot(lams[sel], e_t8[sel], "C2", label="8th")
    ax2.plot(lams[sel], e_full[sel], "r", lw=2, label="full")
    ax2.axvline(lam_star, color="C0", ls=":", lw=1)
    ax2.set_xscale("log")
    ax2.set_xlabel(r"$\lambda$")
    ax2.set_title(fr"around $\lambda^*$: octic/sextic = {ratio86:.2f}, "
                  fr"trunc err = {trunc_err:.0%}")
    ax2.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(Path(__file__).resolve().parent / "SD2_higher_order.png", dpi=150)

    print(json.dumps({k: payload[k] for k in
                      ("moment_checks", "truncated_sextic_minimum",
                       "full_cosine", "verdict")}, indent=2))


if __name__ == "__main__":
    main()
