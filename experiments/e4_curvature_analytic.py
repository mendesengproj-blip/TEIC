"""e4 -- Task A: analytic curvature expansion (the deciding calculation).

Question: in CURVED 2D spacetime, do the two proper-time formulations
  * chain  : longest causal chain  ~  geodesic proper time tau_geo
  * volume : tau_vol = sqrt(2 N / rho)  (flat inversion of the interval count)
agree, or diverge?

Method (exact, symbolic).  Use a 2D constant-curvature background written in
conformally-flat coordinates ds^2 = Omega^2(-dt^2+dx^2),
    Omega = 1 / (1 + (R/8)(x^2 - t^2))   ->   Ricci scalar = R   (verified below).
Because the metric is conformally flat the light cones are EXACTLY 45 degrees, so
the causal diamond between tips A=(-T/2,0), B=(T/2,0) is the ordinary coordinate
diamond and the proper volume is the exact integral of Omega^2 over it.  The
timelike geodesic between the tips stays on x=0 by symmetry, so tau_geo is an
elementary integral.  Both are expanded to second order in R and re-expressed as
functions of tau_geo.

Result (derived here, not assumed):
    V(tau)        = (1/2) tau^2 [ 1 - R tau^2/48 + R^2 tau^4/1440 + ... ]
    tau_vol/tau_geo = 1 - R tau^2/96 + 3 R^2 tau^4/10240 + ...

Convention note: with R = Ricci SCALAR the leading volume coefficient is 1/48.
The value 1/24 sometimes quoted corresponds to using the GAUSSIAN curvature
K = R/2 (then -R tau^2/48 = -K tau^2/24).

Interpretation: the volume formulation, inverted with the flat-space law, does NOT
return the geodesic proper time in curved space -- it differs at O(R tau^2).  If the
chain formulation returns tau_geo (no curvature correction to its normalisation),
the two diverge with relative coefficient -1/96.  Whether the chain really has zero
correction is an empirical question answered numerically in e5 (Task B).

This module is symbolic only; it contains relativistic geometry but generates no
causal-network data, so it is outside the anti-circularity perimeter by design
(it lives in the comparison/derivation layer, like validation.py).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from repro import DATA  # noqa: E402


def verify_ricci():
    """Confirm Omega = 1/(1+(R/8)(x^2-t^2)) has constant Ricci scalar R."""
    t, x, R = sp.symbols("t x R", real=True)
    Omega = 1 / (1 + (R / 8) * (x ** 2 - t ** 2))
    g = sp.diag(-Omega ** 2, Omega ** 2)
    gi = g.inv()
    co = [t, x]
    n = 2
    G = [[[sp.simplify(sum(gi[a, d] * (sp.diff(g[d, b], co[c]) + sp.diff(g[d, c], co[b])
            - sp.diff(g[b, c], co[d])) for d in range(n)) / 2)
           for c in range(n)] for b in range(n)] for a in range(n)]
    Ric = sp.zeros(n, n)
    for b in range(n):
        for c in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(G[a][b][c], co[a]) - sp.diff(G[a][b][a], co[c])
                for d in range(n):
                    s += G[a][a][d] * G[d][b][c] - G[a][c][d] * G[d][b][a]
            Ric[b, c] = sp.simplify(s)
    return sp.simplify(sum(gi[i, j] * Ric[i, j] for i in range(n) for j in range(n)))


def expansions():
    t, x, R, T, tau = sp.symbols("t x R T tau", real=True, positive=True)
    # proper-volume element to O(R^2)
    u = (R / sp.Integer(8)) * (x ** 2 - t ** 2)
    Om2 = sp.series(1 / (1 + u) ** 2, R, 0, 3).removeO()
    w = T / 2 - t
    V_T = sp.expand(2 * sp.integrate(sp.integrate(Om2, (x, -w, w)), (t, 0, T / 2)))
    # geodesic proper time along x=0
    integ = sp.series(1 / (1 - (R / 8) * t ** 2), R, 0, 3).removeO()
    tau_T = sp.expand(2 * sp.integrate(integ, (t, 0, T / 2)))

    # invert tau(T) -> T(tau): T = tau + R*A + R^2*B
    A, B = sp.symbols("A B", cls=sp.Function)
    Ts = tau + R * A(tau) + R ** 2 * B(tau)
    expr = sp.expand(sp.series(tau_T.subs(T, Ts), R, 0, 3).removeO() - tau)
    solA = sp.solve(expr.coeff(R, 1), A(tau))[0]
    solB = sp.solve(expr.coeff(R, 2).subs(A(tau), solA), B(tau))[0]
    Tt = tau + R * solA + R ** 2 * solB

    V_tau = sp.expand(sp.series(V_T.subs(T, Tt), R, 0, 3).removeO())
    tau_vol_ratio = sp.expand(sp.series(sp.sqrt(2 * V_tau) / tau, R, 0, 3).removeO())

    # leading coefficients, extracted with the SAME R, tau symbols
    vol_brace_coeff = sp.simplify(sp.expand(2 * V_tau / tau ** 2).coeff(R, 1) / tau ** 2)
    lead_coeff = sp.simplify(sp.expand(tau_vol_ratio - 1).coeff(R, 1) / tau ** 2)
    return V_T, tau_T, V_tau, tau_vol_ratio, vol_brace_coeff, lead_coeff


def main():
    R = verify_ricci()
    V_T, tau_T, V_tau, ratio, vol_brace_coeff, lead_coeff = expansions()

    summary = {
        "ricci_scalar_of_background": str(R),
        "V_of_tau": str(V_tau),
        "tau_vol_over_tau_geo": str(ratio),
        "volume_leading_coeff_in_brace_(Ricci units)": str(vol_brace_coeff),
        "divergence_leading_relative_coeff_(Ricci units)": str(lead_coeff),
        "convention_note": "Ricci-scalar coeff 1/48 == Gaussian-curvature coeff 1/24",
        "chain_proviso": "chain estimator assumed = tau_geo; its actual curvature "
                         "response is measured in e5 (Task B)",
        "verdict": "PROVADO (analytic): volume formulation diverges from geodesic/chain "
                   "proper time at O(R tau^2), relative coeff -1/96 (Ricci units), "
                   "IF chain has zero curvature correction -- tested in e5.",
    }
    (DATA / "e4_curvature_analytic.meta.json").write_text(json.dumps(summary, indent=2))

    print("=" * 70)
    print("TASK A -- ANALYTIC CURVATURE EXPANSION (2D constant curvature)")
    print("=" * 70)
    print(f"Ricci scalar of background  : {R}   (target: R)")
    print(f"V(tau)                      : {V_tau}")
    print(f"  = (1/2)tau^2 [1 + ({vol_brace_coeff}) R tau^2 + ...]")
    print(f"tau_vol/tau_geo             : {ratio}")
    print(f"leading divergence coeff    : ({lead_coeff}) * R   (relative, per tau^2)")
    print("-" * 70)
    print("Convention: 1/48 (Ricci scalar) == 1/24 (Gaussian curvature K=R/2).")
    print("The prompt's -R tau^2/24 is the Gaussian-curvature convention.")
    print("VERDICT: volume formulation != geodesic proper time at O(R tau^2).")
    print("         Chain-vs-volume divergence coeff -1/96 IF chain = tau_geo")
    print("         (chain's actual curvature response measured in e5).")
    return summary


if __name__ == "__main__":
    main()
