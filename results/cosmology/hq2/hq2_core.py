"""hq2_core.py -- shared engine for HQ2_CRITICAL_FERROMAGNET.

WIRES the two existing motors (does NOT rewrite them):
  * orientation_core (E1) -- causal-vacuum O(3) ferromagnet: order parameter m(J),
    susceptibility chi(J), orientation correlation C(r) -> correlation length xi(J).
  * e2_core         (E2) -- BD smeared causal-set d'Alembertian: photon speed c0
    from the symbol-dispersion zero ridge omega = c k.

HQ2 hypothesis (prompt): near the critical coupling J_c the orientation stiffness
softens, J_eff < J, so via the DEV bridge

    G_eff(J)/G_N = J_eff(J)/J = Z(J/J_c) = (c_eff(J)/c0)^2 .

Two anti-circular estimators of c_eff(J) (see HQ2_CRITICAL_FERROMAGNET.md sec.3):
  ROUTE A (literal, BD motor): c_BD is built from the causal ORDER MATRIX only; the
    spin coupling J appears NOWHERE in it -> c_BD(J) = c0 for all J (J-blind).
  ROUTE B (generous, E1 stiffness): mean-field spin stiffness rho_s(J) ~ m(J)^2
    (E1-3 found flat/non-local S(k), so the stiffness that softens at J_c is the
    squared ordered moment).  Z_B(J/J_c) = (m(J)/m_sat)^2.

ANTI-CIRCULARITY.  G_N never enters as a constant; Z is a measured lattice ratio.
No c, no critical coupling, no target exponent is inserted into any generator.
J_c is the E1 chi-peak value, never tuned to escape the death criterion.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# ---- locate the two motors (reuse, do not duplicate) -------------------- #
ROOT = Path(__file__).resolve().parents[3]                       # .../TEIC
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
E2 = ORI / "e2"
for p in (str(ORI), str(E2)):
    if p not in sys.path:
        sys.path.insert(0, p)

import orientation_core as oc       # noqa: E402  (E1 motor)
import e2_core as e2c               # noqa: E402  (E2 motor)

# ---- E1 measured anchors (NOT refitted here; see E1_1/E1_2 json) -------- #
JC = {"O(3)": 0.08, "U(1)": 0.05}          # chi-peak critical coupling (E1-2)
M_SAT = 0.997                               # deep-ordered moment, O(3) J=10 (E1-1)
C0_PHOTON = 0.98                            # BD photon speed (E2 synthesis)

# ---- causal-vacuum build (identical geometry to E1-1) ------------------- #
RHO = 2.0
BOX = [(0.0, 40.0), (0.0, 3.0), (0.0, 3.0), (0.0, 3.0)]   # elongated causal tube
N_SOURCES = 24
R_CAP = 50


def build_seed(seed):
    """Causal link graph + longest-chain distance arrays from early sources.
    Byte-for-byte the E1-1 construction so m(J), chi, C(r) are comparable."""
    rng = np.random.default_rng(7000 + seed)
    pts = oc.sprinkle_box(RHO, BOX, rng)
    g = oc.causal_link_graph(pts)
    early = g.topo_order[:max(N_SOURCES, int(0.3 * g.n))]
    sources = rng.choice(early, size=min(N_SOURCES, early.size), replace=False)
    dist_list = [oc.longest_chain_from(g, int(s), r_max=R_CAP) for s in sources]
    return g, sources, dist_list


def run_o3(g, sources, dist_list, J, seed, n_burn=1000, n_meas=120, meas_every=2):
    """One O(3) equilibrium measurement at coupling J on graph g.
    Returns (r, C, counts, m_mean, m_std, chi).  Pure E1 motor; no interpretation."""
    m = oc.O3Model(g, J=J, seed=10_000 * seed + 2)
    m.equilibrate(n_burn, adapt=True)
    acc = oc.CorrelationAccumulator(sources, dist_list, R_CAP)
    m_series = []
    taken, s = 0, 0
    while taken < n_meas:
        m.sweep()
        s += 1
        if s % meas_every == 0:
            acc.add(m)
            m_series.append(m.order_parameter())
            taken += 1
    r, C, w = acc.result()
    ms = np.array(m_series)
    chi = float(g.n * (np.mean(ms ** 2) - np.mean(ms) ** 2))
    return r, C, w, float(ms.mean()), float(ms.std()), chi


def aggregate_curves(per_seed_curves, r_ref, n_seeds):
    """Count-weighted seed average of C(r) on common grid r_ref (E1-1 recipe)."""
    Cs, Ws = [], []
    for r, C, w in per_seed_curves:
        Cg = np.full(r_ref.shape, np.nan)
        Wg = np.zeros(r_ref.shape)
        idx = {int(rr): k for k, rr in enumerate(r)}
        for k, rr in enumerate(r_ref):
            if rr in idx:
                Cg[k] = C[idx[rr]]
                Wg[k] = w[idx[rr]]
        Cs.append(Cg)
        Ws.append(Wg)
    Cs, Ws = np.array(Cs), np.array(Ws)
    with np.errstate(invalid="ignore"):
        Cmean = np.nansum(Cs * Ws, axis=0) / np.maximum(np.nansum(Ws, axis=0), 1e-9)
        Cstd = np.nanstd(Cs, axis=0)
    return Cmean, Cstd, np.nansum(Ws, axis=0)


def xi_from_curve(r_ref, Cmean, Cstd, Wtot, min_count=200, r_lo=2):
    """Correlation length xi from C(r) using the SAME validated classifier as E1.
    Returns dict {winner, xi, eta, C_long, n_points}.  In the disordered phase
    (J<J_c) the exponential fit's xi is the physical correlation length; it grows
    as J->J_c.  In the ordered phase the curve is a plateau ('const')."""
    ok = Wtot >= min_count
    r_use = r_ref[ok]
    C_use = Cmean[ok]
    fit = oc.fit_forms(r_use, C_use, sigma=Cstd[ok], r_lo=r_lo)
    xi = fit["exp"]["xi"] if np.isfinite(fit["exp"]["xi"]) else float("nan")
    return {"winner": fit["winner"], "xi": float(xi),
            "eta": float(fit["power"]["eta"]), "C_long": float(fit["C_long"]),
            "n_points": int(fit["n_points"]), "fit": fit,
            "r": r_use.tolist(), "C": C_use.tolist()}


# ---- the DEV bridge (prompt's relation, adopted as given) --------------- #
def Z_from_stiffness(m_J, m_sat=M_SAT):
    """Route B: Z = G_eff/G_N = (c_eff/c0)^2 = (m(J)/m_sat)^2  (mean-field rho_s)."""
    return (m_J / m_sat) ** 2


# ---- Route A: BD photon speed (the E2 motor), demonstrably J-blind ------ #
def bd_photon_speed(rho=6.0, T=18.0, X=9.0, eps=0.2, n_seeds=8, seed0=0):
    """Photon speed c0 from the BD symbol dispersion omega=ck on a Poisson causal
    set (E2 motor).  The operator is built from the causal ORDER MATRIX only -- no
    spin coupling J is an input -- so this c is J-independent BY CONSTRUCTION.
    Returns (c_fit, dev_pct, winner, n_k_found)."""
    kmags, omegas = e2c.default_grids(T, X, rho)
    res = e2c.measure_symbol_dispersion(rho, T, X, eps, kmags, omegas,
                                        n_seeds=n_seeds, max_n=120, seed0=seed0)
    found = res["found"]
    if found.sum() < 3:
        return float("nan"), float("nan"), "none", int(found.sum())
    fit = e2c.fit_dispersion(res["k"][found], res["omega_star"][found],
                             sigma=res["sem"][found])
    return (float(fit["massless"]["c"]), float(fit["linear_rel_deviation_pct"]),
            fit["winner"], int(found.sum()))


# ---- cosmology: how J/J_c evolves with redshift (prompt HQ2-3) ---------- #
def J_over_Jc_of_z(z, J0_over_Jc):
    """J ∝ rho_vacuum ∝ a^-3 (prompt): J(z)/J_c = (J0/J_c)*(1+z)^3.
    Higher z -> denser -> MORE ordered -> further from J_c."""
    return J0_over_Jc * (1.0 + np.asarray(z, float)) ** 3


def m_of_J_meanfield(J_over_Jc):
    """Mean-field magnetisation curve m(J/J_c): 0 below 1, rising above.
    Calibrated to the E1-1 O(3) causal-graph measurement (m(J_c)=0, m_sat~1).
    Used ONLY in HQ2-3/4 to map an assumed J0/J_c to Z(z); the SHAPE is the
    measured E1 m(J), interpolated -- see HQ2_3 for the data-anchored version."""
    x = np.asarray(J_over_Jc, float)
    m = np.zeros_like(x)
    above = x > 1.0
    # mean-field O(3): m ~ sqrt(1 - J_c/J) saturating to 1; matches E1 m(J) shape
    m[above] = np.sqrt(np.clip(1.0 - 1.0 / x[above], 0.0, 1.0))
    return m


if __name__ == "__main__":
    print("hq2_core self-test")
    g, src, dl = build_seed(0)
    print(f"  causal graph: n={g.n} links={g.n_links} avgdeg={2*g.n_links/g.n:.0f}")
    r, C, w, m, ms, chi = run_o3(g, src, dl, J=0.2, seed=0, n_burn=200, n_meas=40)
    print(f"  O(3) J=0.20: m={m:.3f} chi={chi:.2f}  (E1 ref m~0.855)")
    print(f"  Z_B(J=0.20) = {Z_from_stiffness(m):.3f}")
    print(f"  J/J_c(z=0.5, J0/J_c=10) = {J_over_Jc_of_z(0.5, 10.0):.2f} "
          "(grows with z -> further from J_c)")
    print("self-test done")
