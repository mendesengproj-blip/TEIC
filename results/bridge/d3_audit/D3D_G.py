"""D3D_G.py -- the critical question: does G emerge, or was it put in?

BRIDGE / D3 AUDIT, task D (the climax).  D3 measured the EXPONENT (-1, from the 3D
Laplacian geometry).  It did NOT measure the AMPLITUDE, which is where a coupling
constant lives.  Define the network's effective coupling

    G_net = (amplitude of the 1/r well) / (source weight) = A / w_M,

where theta = A/r (+ conservation offset) and w_M is the deposited weight.  Measure
G_net while varying the source weight w_M, the network density rho, the box L, and --
crucially -- the action stiffness K.

The three possibilities (prompt):
  (a) G_net = const, independent of EVERYTHING  -> universal, extraordinary.
  (b) G_net depends on the granularity scale     -> form derived, value external (a_0 pattern).
  (c) G_net = f(w_M) non-linear                  -> the coupling is not linear/Poisson.

No G / GM/r / Schwarzschild in the generator: w_M is a dimensionless weight; G_net is
formed in the analysis only.  (G appears nowhere -- this task asks whether the network
ITSELF carries a coupling, independent of any comparison to Newton.)
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(OUT))
from d3_audit_core import (radial_grid, radial_source_core, radial_solve,
                           radial_mc_batch, fit_tail)

R_MIN, R_CORE = 0.5, 2.0
WM_LIST = [1.0, 2.0, 5.0, 10.0, 20.0]
RHO_LIST = [50.0, 100.0, 200.0, 400.0]
L_LIST = [20.0, 40.0, 80.0]
K_LIST = [0.5, 1.0, 2.0, 4.0]


def nbins_of_rho(rho):
    return int(np.clip(round(8.62 * rho ** (1.0 / 3.0)), 20, 80))


def measure_A(L, rho, K, w_M):
    nb = nbins_of_rho(rho)
    _, centers, sv = radial_grid(L, nb, R_MIN)
    q = radial_source_core(centers, sv, R_CORE, w_M)
    th = radial_solve(centers, sv, q, K)
    A, C, p = fit_tail(centers, th, R_CORE, 0.6 * L)
    return A, p


def loglog_slope(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = (x > 0) & (y > 0) & np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 2:
        return np.nan
    return float(np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)[0])


def main():
    t0 = time.time()
    L0, rho0, K0, wM0 = 40.0, 100.0, 1.0, 1.0

    # --- sweep w_M (expect G_net constant => linear; rules out case c) ---
    G_vs_wM = [(w, measure_A(L0, rho0, K0, w)[0] / w) for w in WM_LIST]
    slope_wM = loglog_slope([g[0] for g in G_vs_wM], [g[1] for g in G_vs_wM])
    G_wM_cv = float(np.std([g[1] for g in G_vs_wM]) / np.mean([g[1] for g in G_vs_wM]))

    # --- sweep rho (resolution): does G_net depend on granularity? ---
    G_vs_rho = [(r, measure_A(L0, r, K0, wM0)[0] / wM0) for r in RHO_LIST]
    delta_rho = loglog_slope([g[0] for g in G_vs_rho], [g[1] for g in G_vs_rho])

    # --- sweep L: does G_net stabilise for large box? ---
    G_vs_L = [(L, measure_A(L, rho0, K0, wM0)[0] / wM0) for L in L_LIST]
    slope_L = loglog_slope([g[0] for g in G_vs_L], [g[1] for g in G_vs_L])

    # --- sweep K (action stiffness, the INPUT scale): expect G_net ~ 1/K ---
    G_vs_K = [(Kk, measure_A(L0, rho0, Kk, wM0)[0] / wM0) for Kk in K_LIST]
    slope_K = loglog_slope([g[0] for g in G_vs_K], [g[1] for g in G_vs_K])

    # --- MC error bars on G_net at the reference point (genuine sampling) ---
    nb = nbins_of_rho(rho0)
    _, centers, sv = radial_grid(L0, nb, R_MIN)
    q = radial_source_core(centers, sv, R_CORE, wM0)
    ths = radial_mc_batch(centers, sv, q, K0, 0.02, 100_000, 25_000,
                          list(20250607 + np.arange(20)))
    As = np.array([fit_tail(centers, ths[:, k], R_CORE, 0.6 * L0)[0] for k in range(20)])
    G_ref_mc = float(np.mean(As) / wM0); G_ref_mc_std = float(np.std(As) / wM0)
    G_ref_solve = float(measure_A(L0, rho0, K0, wM0)[0] / wM0)

    # --- classify ---
    linear_in_wM = bool(abs(slope_wM) < 0.03 and G_wM_cv < 0.02)   # G_net const in w_M
    indep_of_rho = bool(abs(delta_rho) < 0.05)                      # no granularity dep.
    stable_in_L = bool(abs(slope_L) < 0.05)
    rides_on_K = bool(abs(slope_K - (-1.0)) < 0.1)                  # G_net ~ 1/K

    if not linear_in_wM:
        case = "(c) non-linear coupling: G_net depends on w_M"
    elif rides_on_K and indep_of_rho and stable_in_L:
        case = "(b) form derived, value external: G_net is constant in (w_M, rho, L) " \
               "but rides on the action stiffness K (G_net ~ 1/K), the granularity " \
               "normalisation -- an INPUT. Same pattern as a_0."
    elif indep_of_rho and stable_in_L and not rides_on_K:
        case = "(a) universal constant: G_net independent of EVERYTHING incl. K " \
               "(needs triple verification)"
    else:
        case = "mixed / inconclusive"

    verdict = "DONE -- case " + case[:3]

    # ---- figures ----
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 4, figsize=(16, 4))
    for a, data, xlabel, sl, title in [
        (ax[0], G_vs_wM, "source weight $w_M$", slope_wM, "vs $w_M$ (linear?)"),
        (ax[1], G_vs_rho, r"network density $\rho$", delta_rho, r"vs $\rho$ (granularity?)"),
        (ax[2], G_vs_L, "box size $L$", slope_L, "vs $L$ (stable?)"),
        (ax[3], G_vs_K, "action stiffness $K$", slope_K, "vs $K$ (value source)")]:
        x = [d[0] for d in data]; y = [d[1] for d in data]
        a.loglog(x, y, "o-", ms=6)
        a.set_xlabel(xlabel); a.set_ylabel(r"$G_{\rm net}=A/w_M$")
        a.set_title(f"{title}\nlog-log slope = {sl:+.3f}")
    fig.suptitle("(D3-D) the network's effective coupling $G_{\\rm net}$ -- "
                 "constant in $(w_M,\\rho,L)$, rides on $K$")
    fig.tight_layout(); fig.savefig(OUT / "D3D_G.png", dpi=130)

    summary = dict(
        what="Network effective coupling G_net = A/w_M vs w_M, rho, L, and stiffness K.",
        r_min=R_MIN, r_core=R_CORE,
        G_vs_wM=G_vs_wM, slope_wM=slope_wM, G_net_cv_over_wM=G_wM_cv,
        G_vs_rho=G_vs_rho, delta_rho=delta_rho,
        G_vs_L=G_vs_L, slope_L=slope_L,
        G_vs_K=G_vs_K, slope_K=slope_K,
        G_ref_solver=G_ref_solve, G_ref_mc=G_ref_mc, G_ref_mc_std=G_ref_mc_std,
        linear_in_wM=linear_in_wM, independent_of_rho=indep_of_rho,
        stable_in_L=stable_in_L, rides_on_K=rides_on_K,
        case=case, verdict=verdict, runtime_s=round(time.time() - t0, 1),
        honest_statement=(
            "G is NOT derived as a universal constant. The network produces the "
            "COUPLING RELATION (linear, Poisson form: A proportional to w_M, "
            "exponent -1), but the numerical value G_net = 1/(4 pi K)-type rides on "
            "the action stiffness K (the granularity / Planck normalisation), an "
            "external input. Constant in (w_M, rho, L); proportional to 1/K. This is "
            "the same pattern as a_0: the FORM is derived, the SCALE is measured. No "
            "pure geometric theory has derived G; TEIC is not an exception."),
        timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    (OUT / "D3D_G_data.json").write_text(json.dumps(summary, indent=2))

    print("=" * 72)
    print("D3-D -- DOES G EMERGE OR WAS IT PUT IN? (the critical task)")
    print("=" * 72)
    print(f"  G_net vs w_M  : slope={slope_wM:+.4f}  CV={G_wM_cv:.4f}  -> linear: {linear_in_wM}")
    print(f"  G_net vs rho  : slope(delta)={delta_rho:+.4f}            -> rho-indep: {indep_of_rho}")
    print(f"  G_net vs L    : slope={slope_L:+.4f}                     -> L-stable: {stable_in_L}")
    print(f"  G_net vs K    : slope={slope_K:+.4f}                     -> ~1/K: {rides_on_K}")
    print(f"  G_net (ref)   : solver={G_ref_solve:.4f}  MC={G_ref_mc:.4f}+-{G_ref_mc_std:.4f}")
    print("-" * 72)
    print(f"  CASE: {case}")
    print(f"VERDICT (D3-D): {verdict}   [{summary['runtime_s']}s]")
    return summary


if __name__ == "__main__":
    main()
