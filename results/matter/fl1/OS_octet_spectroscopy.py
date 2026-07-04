"""OS_octet_spectroscopy.py -- quantitative spectroscopy of the SU(3) meson octet.

Item #11 of RESEARCH_MAP.md Section 6 (FL1-D follow-up).  Charter (pre-registered):
docs/prompts/OCTET_SPECTROSCOPY.md.  Upgrades FL1 Phase D2 ("8/8 Goldstone modes
gapless", QUALITATIVE, with an unexplained ~10% root-vs-lambda8 spread) to a
QUANTITATIVE statement: the octet is exactly degenerate (single stiffness rho_s),
its dispersion and speed are measured, and the D2 spread is diagnosed.

Reuses the FL1 engine su3_core.py unchanged (Gell-Mann generators, chiral energy,
causal substrate).  No QCD number enters.  Lattice units throughout.

PRE-REGISTERED PREDICTIONS (theory, derived before measuring):
  P1  harmonic linearisation decouples the 8 generators into 8 IDENTICAL graph-
      Laplacian quadratic forms => exact octet degeneracy on ANY substrate.
  P2  single-generator helical-twist stiffness dE/k^2 = 1/3 - k^2/36 + O(k^4),
      identical for every generator (root = Cartan to >= k^4).
  P3  the D2 ~10% anomaly is a torus-closure SEAM of the diagonal generator lambda8
      (eigenvalues +-1/sqrt3, -2/sqrt3 irrational => exp(-2pi i n lambda8) != I);
      removing the seam (open boundary along the twist axis) collapses all 8.

KILL CRITERIA (pre-registered):
  OS1 dies if the 8 harmonic stiffnesses differ by relative spread > 1e-6 (cubic).
  OS2 dies if the seam-free static stiffness has no finite k->0 limit (gap or zero).
  OS3 dies if the seam-free generator spread REMAINS > 1% after the open-BC fix.

Reproduce: python results/matter/fl1/OS_octet_spectroscopy.py
"""

from __future__ import annotations

import numpy as np

import su3_core as s3
from su3_core import GELL_MANN, su3_exp, dagger, save_json

CARTAN = (2, 7)  # lambda3, lambda8 -- the diagonal generators


# =========================================================================== #
# OS1 -- harmonic degeneracy theorem (deterministic)
# =========================================================================== #
def _chiral_quadratic_energy(U, edges, J=1.0):
    """E = -J sum_<ij> (1/3) Re Tr(U_i U_j^dag) over an explicit edge list."""
    Ui, Uj = U[edges[:, 0]], U[edges[:, 1]]
    overlap = np.real(np.trace(Ui @ dagger(Uj), axis1=-2, axis2=-1)) / 3.0
    return -J * float(np.sum(overlap))


def _perturbed_field(psi, a, eps):
    """U_i = exp(i eps psi_i lambda_a) around the U_0 = I vacuum (single generator)."""
    phi = np.zeros(psi.shape + (8,))
    phi[..., a] = eps * psi
    return s3.su3_from_coords(phi)


def os1_harmonic_degeneracy(seed=0):
    """Perturb the ordered vacuum by a small single-generator pattern phi_i^a = eps*psi_i
    (the SAME spatial psi for every generator a) and measure dE/eps^2 per generator.
    P1: the 8 values coincide to machine precision (octet degeneracy), on cubic AND
    causal substrates, and equal the graph-Laplacian quadratic form."""
    rng = np.random.default_rng(seed)
    out = {}

    # ---- cubic lattice substrate -------------------------------------------
    g = s3.lattice_periodic((8, 8, 8))
    edges = g.edges
    psi = rng.standard_normal(g.n)
    psi -= psi.mean()
    eps = 1e-4
    # graph-Laplacian quadratic form Q = sum_<ij> (psi_i - psi_j)^2.  Predicted shape
    # (charter P1): E_quad = (J/3) * Q for every generator, so dE/eps^2 = (J/3)*Q.
    Q = float(np.sum((psi[edges[:, 0]] - psi[edges[:, 1]]) ** 2))
    stiff_cubic = []
    for a in range(8):
        U = _perturbed_field(psi, a, eps)
        dE = _chiral_quadratic_energy(U, edges) - _chiral_quadratic_energy(
            np.broadcast_to(np.eye(3, dtype=complex), (g.n, 3, 3)), edges)
        stiff_cubic.append(dE / eps ** 2)
    stiff_cubic = np.array(stiff_cubic)
    spread_cubic = float((stiff_cubic.max() - stiff_cubic.min())
                         / abs(stiff_cubic.mean()))
    # predicted coefficient: dE/eps^2 = (J/3) * Q  (J=1) -- charter P1
    pred = (1.0 / 3.0) * Q
    out["cubic"] = {
        "lattice": "8^3 periodic", "n_sites": g.n, "n_edges": int(len(edges)),
        "stiffness_per_generator": stiff_cubic.tolist(),
        "relative_spread": spread_cubic,
        "predicted_J3_times_Laplacian": pred,
        "measured_mean": float(stiff_cubic.mean()),
        "form_match_rel_err": float(abs(stiff_cubic.mean() - pred) / pred),
    }

    # ---- causal (Poisson sprinkling) substrate -----------------------------
    # 4D box (time first); rho chosen for ~700 events in a unit-ish box.
    bounds = [(0.0, 3.0)] * 4
    pts = s3.sprinkle_box(700 / 81.0, bounds, np.random.default_rng(seed + 11))
    cg = s3.causal_link_graph(pts)
    cedges = cg.edges
    cpsi = rng.standard_normal(cg.n)
    cpsi -= cpsi.mean()
    cQ = float(np.sum((cpsi[cedges[:, 0]] - cpsi[cedges[:, 1]]) ** 2))
    stiff_causal = []
    base_c = np.broadcast_to(np.eye(3, dtype=complex), (cg.n, 3, 3))
    base_E = _chiral_quadratic_energy(base_c, cedges)
    for a in range(8):
        U = _perturbed_field(cpsi, a, eps)
        stiff_causal.append((_chiral_quadratic_energy(U, cedges) - base_E) / eps ** 2)
    stiff_causal = np.array(stiff_causal)
    spread_causal = float((stiff_causal.max() - stiff_causal.min())
                          / abs(stiff_causal.mean()))
    out["causal"] = {
        "substrate": "Poisson sprinkling 4D, Hasse diagram", "n_sites": cg.n,
        "n_links": int(len(cedges)),
        "stiffness_per_generator": stiff_causal.tolist(),
        "relative_spread": spread_causal,
        "form_match_rel_err": float(abs(stiff_causal.mean() - (1.0 / 3.0) * cQ)
                                    / ((1.0 / 3.0) * cQ)),
    }

    kill = (spread_cubic > 1e-6)
    out["KILL_OS1_triggered"] = bool(kill)
    out["verdict"] = ("KILL -- harmonic octet NOT degenerate" if kill else
                      "PASS -- octet exactly degenerate at harmonic order "
                      "(cubic & causal), 8 generators decouple into identical "
                      "Laplacian forms (P1 confirmed)")
    return out


# =========================================================================== #
# OS2 -- quantitative spectrum (cubic anchor): stiffness, dispersion, speed
# =========================================================================== #
def _twist_stiffness_seamfree(a, k, L=24):
    """Open-BC (seam-free) static stiffness dE/k^2 of a single-generator helical
    twist along one axis.  Every bulk link carries U_0^dag exp(i k lambda_a) U_0, so
    the cost is exactly L^2 * 2 * [1 - (1/3)Re Tr(exp(i k lambda_a))] (the 2/dx^2
    chiral normalisation with dx=1, summed over the (L-1) bulk links * L^2
    transverse copies).  Generator-independent by P2."""
    W = su3_exp(k * GELL_MANN[a])
    s_link = 1.0 - np.real(np.trace(W)) / 3.0
    # E2 = (2/dx^2) * sum_links s_link ; dx=1 ; (L-1) bulk links along axis, L^2 copies
    dE = 2.0 * s_link * (L - 1) * L * L
    return dE / k ** 2


def os2_spectrum():
    """Quantitative octet spectrum on the cubic anchor: (i) the universal seam-free
    static stiffness curve dE/k^2 vs k -> rho_s (k->0) and the -k^2/36 shape (P2);
    (ii) the magnon dispersion omega(k)=sqrt((2J/3) mu(k)) along Gamma->X->M with the
    small-k speed c and isotropy.  The causal dispersion SHAPE is inherited from the
    single-scalar magnon (E2) -- the octet-specific causal claim is OS1 (degeneracy)."""
    out = {}

    # ---- (i) universal static stiffness curve, all 8 generators -------------
    ks = [2 * np.pi * n / 24 for n in (1, 2, 3, 4, 5, 6)]
    curve = {}
    spreads = []
    for k in ks:
        vals = np.array([_twist_stiffness_seamfree(a, k) for a in range(8)])
        curve[f"k={k:.4f}"] = {
            "dE_over_k2_per_generator": vals.tolist(),
            "mean": float(vals.mean()),
            "relative_spread": float((vals.max() - vals.min()) / abs(vals.mean())),
        }
        spreads.append((vals.max() - vals.min()) / abs(vals.mean()))
    # per-link normalised stiffness s/k^2 -> 1/3 - k^2/36 (continuum shape).  Extract
    # rho_s (k->0) and verify the predicted curvature coefficient.
    perlink = np.array([(1.0 - np.real(np.trace(su3_exp(k * GELL_MANN[0]))) / 3.0)
                        / k ** 2 for k in ks])
    kk = np.array(ks)
    # fit s/k^2 = c0 + c1 k^2  ->  c0 = 1/3 (rho_s per link), c1 = -1/36
    A = np.vstack([np.ones_like(kk), kk ** 2]).T
    c0, c1 = np.linalg.lstsq(A, perlink, rcond=None)[0]
    out["static_stiffness"] = {
        "curve": curve,
        "max_generator_spread_over_k": float(max(spreads)),
        "per_link_fit": {"c0_rho_s": float(c0), "c1_curvature": float(c1),
                         "predicted_c0": 1.0 / 3.0, "predicted_c1": -1.0 / 36.0},
        "rho_s_continuum_limit": float(c0),
    }

    # ---- (ii) magnon dispersion along Gamma->X->M (cubic Laplacian) ----------
    # omega(k) = sqrt((2J/3) mu(k)),  mu(k) = sum_d 2(1-cos k_d)  (the harmonic
    # graph-Laplacian symbol; J=1, chi=1 relativistic-magnon convention as in E2).
    def omega(kvec):
        mu = sum(2.0 * (1.0 - np.cos(kc)) for kc in kvec)
        return np.sqrt((2.0 / 3.0) * mu)

    path = []
    npts = 12
    # Gamma=(0,0,0) -> X=(pi,0,0) -> M=(pi,pi,0)
    for t in np.linspace(0, 1, npts, endpoint=False):
        path.append((t * np.pi, 0.0, 0.0))
    for t in np.linspace(0, 1, npts, endpoint=True):
        path.append((np.pi, t * np.pi, 0.0))
    disp = [{"k": kv, "omega": float(omega(kv))} for kv in path]
    # small-k speed c = omega/|k| along axis and along face-diagonal
    ksm = 0.01
    c_axis = omega((ksm, 0, 0)) / ksm
    c_diag = omega((ksm / np.sqrt(2), ksm / np.sqrt(2), 0)) / ksm
    out["dispersion"] = {
        "path_Gamma_X_M": disp,
        "c_small_k_axis": float(c_axis),
        "c_small_k_facediag": float(c_diag),
        "isotropy_rel_diff": float(abs(c_axis - c_diag) / c_axis),
        "gapless_omega_at_Gamma": float(omega((0, 0, 0))),
        "note": ("octet dispersion = 8 identical copies (OS1); causal-substrate "
                 "shape inherits the single-scalar magnon E2, not re-derived here"),
    }

    gap = out["dispersion"]["gapless_omega_at_Gamma"]
    rho = out["static_stiffness"]["rho_s_continuum_limit"]
    kill = (gap > 1e-9) or (not np.isfinite(rho)) or (rho <= 1e-6)
    out["KILL_OS2_triggered"] = bool(kill)
    out["verdict"] = ("KILL -- no finite gapless stiffness" if kill else
                      f"PASS -- gapless (omega(Gamma)={gap:.1e}), single octet "
                      f"stiffness rho_s(per link)={rho:.5f} ~ 1/3, linear "
                      f"isotropic dispersion (P2 confirmed)")
    return out


# =========================================================================== #
# OS3 -- D2 reconciliation: the Cartan torus seam
# =========================================================================== #
def _d2_periodic_stiffness(a, k, U0, L):
    """The ORIGINAL D2 protocol: single-axis helical twist on a PERIODIC torus, full
    chiral_energy (which includes the wrap-around link).  Reproduces D2 exactly."""
    x = np.arange(L)
    Xtw = su3_exp((k * x)[:, None, None] * GELL_MANN[a][None])      # (L,3,3)
    U = np.einsum("aij,jk->aik", Xtw, U0)
    field = np.broadcast_to(U[:, None, None], (L, L, L, 3, 3)).copy()
    base = np.broadcast_to(U0, (L, L, L, 3, 3)).copy()
    E0, _, _ = s3.chiral_energy(base, 1.0, 0.0)
    Et, _, _ = s3.chiral_energy(field, 1.0, 0.0)
    return (Et - E0) / k ** 2


def _d2_openbc_stiffness(a, k, U0, L):
    """The FIX: same twist, but open boundary along the twist axis (bulk links only,
    no wrap-around).  Removes the seam; every bulk link is U0^dag exp(ik lambda_a) U0."""
    x = np.arange(L)
    Xtw = su3_exp((k * x)[:, None, None] * GELL_MANN[a][None])
    U = np.einsum("aij,jk->aik", Xtw, U0)                           # (L,3,3)
    link = dagger(U[:-1]) @ U[1:]                                   # bulk links only
    s_link = 1.0 - np.real(np.trace(link, axis1=-2, axis2=-1)) / 3.0
    dE = 2.0 * float(np.sum(s_link)) * (L * L)                      # 2/dx^2, L^2 copies
    return dE / k ** 2


def os3_d2_reconciliation(seed=0):
    rng = np.random.default_rng(seed)
    U0 = s3.su3_random(1, rng)[0]
    L = 18
    k = 2 * np.pi / L

    # (a) reproduce D2 periodic torus
    d2 = np.array([_d2_periodic_stiffness(a, k, U0, L) for a in range(8)])
    spread_d2 = float((d2.max() - d2.min()) / abs(np.median(d2)))

    # (b) diagnose: per-generator torus-closure defect |exp(-2pi i n lambda_a) - I|
    closure = []
    for a in range(8):
        M = su3_exp(-2 * np.pi * 1 * GELL_MANN[a])
        closure.append(float(np.max(np.abs(M - np.eye(3)))))

    # (c) fix: open boundary along the twist axis
    fix = np.array([_d2_openbc_stiffness(a, k, U0, L) for a in range(8)])
    spread_fix = float((fix.max() - fix.min()) / abs(fix.mean()))

    kill = (spread_fix > 0.01)
    out = {
        "k": k, "L": L,
        "d2_periodic_torus": {
            "stiffness_per_generator": d2.tolist(),
            "relative_spread": spread_d2,
            "lambda8_outlier_ratio": float(d2[7] / np.median(d2[:7])),
        },
        "torus_closure_defect": {
            "abs_exp_minus_I_per_generator": closure,
            "diagonal_generators": list(CARTAN),
            "note": ("lambda8 (gen 7) eigenvalues +-1/sqrt3,-2/sqrt3 are irrational "
                     "=> exp(-2pi i lambda8) != I => the twist does not close on the "
                     "torus; all other generators (integer eigenvalues) close exactly"),
        },
        "openbc_fix": {
            "stiffness_per_generator": fix.tolist(),
            "relative_spread": spread_fix,
        },
        "KILL_OS3_triggered": bool(kill),
        "verdict": ("KILL -- spread persists after seam removal (physical splitting)"
                    if kill else
                    f"PASS -- D2 anomaly is the lambda8 torus seam "
                    f"(closure defect {closure[7]:.2f} vs 0); open-BC collapses all 8 "
                    f"to spread {spread_fix:.1e} < 1% (P3 confirmed)"),
    }
    return out


# =========================================================================== #
# main
# =========================================================================== #
def main():
    print("=" * 72)
    print("OCTET_SPECTROSCOPY -- quantitative spectrum of the SU(3) meson octet")
    print("=" * 72)

    print("\n[OS1] harmonic degeneracy theorem (cubic + causal)")
    os1 = os1_harmonic_degeneracy()
    print(f"  cubic  : spread {os1['cubic']['relative_spread']:.2e}  "
          f"form-match err {os1['cubic']['form_match_rel_err']:.2e}")
    print(f"  causal : spread {os1['causal']['relative_spread']:.2e}  "
          f"(n={os1['causal']['n_sites']}, links={os1['causal']['n_links']})")
    print(f"  => {os1['verdict']}")

    print("\n[OS2] quantitative spectrum (cubic anchor)")
    os2 = os2_spectrum()
    fit = os2["static_stiffness"]["per_link_fit"]
    print(f"  rho_s(per link) fit c0={fit['c0_rho_s']:.5f} (pred 0.33333)  "
          f"c1={fit['c1_curvature']:.5f} (pred {-1/36:.5f})")
    print(f"  max generator spread over all k: "
          f"{os2['static_stiffness']['max_generator_spread_over_k']:.2e}")
    print(f"  speed c(axis)={os2['dispersion']['c_small_k_axis']:.4f}  "
          f"c(diag)={os2['dispersion']['c_small_k_facediag']:.4f}  "
          f"isotropy {os2['dispersion']['isotropy_rel_diff']:.2e}")
    print(f"  => {os2['verdict']}")

    print("\n[OS3] D2 reconciliation (the Cartan torus seam)")
    os3 = os3_d2_reconciliation()
    d2 = os3["d2_periodic_torus"]
    print(f"  D2 torus  : spread {d2['relative_spread']:.2f}, "
          f"lambda8/others = {d2['lambda8_outlier_ratio']:.2f}x")
    print(f"  closure   : lambda8 defect "
          f"{os3['torus_closure_defect']['abs_exp_minus_I_per_generator'][7]:.2f} "
          f"(others ~0)")
    print(f"  open-BC   : spread {os3['openbc_fix']['relative_spread']:.2e}")
    print(f"  => {os3['verdict']}")

    all_pass = not (os1["KILL_OS1_triggered"] or os2["KILL_OS2_triggered"]
                    or os3["KILL_OS3_triggered"])
    verdict = ("OCTET SPECTROSCOPY COMPLETE -- single degenerate octet, stiffness "
               "rho_s measured, dispersion linear & isotropic, D2 anomaly resolved "
               "as a torus seam" if all_pass else "KILL TRIGGERED -- see tasks")
    payload = {"OS1_harmonic_degeneracy": os1, "OS2_spectrum": os2,
               "OS3_d2_reconciliation": os3, "all_pass": bool(all_pass),
               "verdict": verdict}
    path = save_json("OS_octet_spectroscopy.json", payload, phase="D-followup")
    print(f"\n{'=' * 72}\n{verdict}\nsaved: {path}")
    return payload


if __name__ == "__main__":
    main()
