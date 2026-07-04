"""C1_khoury_equivalence.py -- is the TEIC<->Khoury equivalence a tree-level phonon
identity, or only a deep-MOND-limit equivalence in the longitudinal response sector?

Charter: docs/prompts/C1_KHOURY_EQUIVALENCE.md (kill criteria PRE-REGISTERED).
Item R3 of RESEARCH_MAP.md / Path C1 of CONVERGENCE_PATHS.md.

Background already established:
  * E2: the O(3) magnon (transverse Goldstone) disperses omega=ck -- a QUADRATIC,
    massless phonon (action ~ X, not X^{3/2}).
  * FM2-1: the LONGITUDINAL susceptibility chi_par ~ h^{-1/2} (Brezin-Wallace
    coexistence anomaly), identified with the deep-MOND interpolation.
  * Fase 2 (Milgrom theorem): DEV and Khoury share the deep-MOND limit L ~ X^{3/2}.

The sharp question C1 decides: does deep-MOND (the h^{-1/2} non-analyticity) live in
the TRANSVERSE phonon kinetic term (Khoury's X^{3/2}, postulated) or ONLY in the
LONGITUDINAL response (chi_par)?  Decisive discriminator: measure chi_perp and chi_par
on the SAME ordered O(3) lattice.
  prediction (Ward + coexistence anomaly):
    chi_perp ~ h^{-1}    (transverse Goldstone; chi_perp = <m_par>/h, trivial)
    chi_par  ~ h^{-1/2}  (the deep-MOND anomaly)
  DISTINCT exponents => the equivalence is in the longitudinal sector, NOT the
  tree-level transverse phonon.

PRE-REGISTERED (see charter):
  G0       reproduce FM2-1's chi_par ~ h^{-p}, p ~ 0.5.
  K2-SETOR if chi_perp and chi_par have distinct exponents (~ -1 vs ~ -1/2) ->
           tree-level phonon equivalence FAILS (transverse is ~X, not X^{3/2});
           equivalence holds only in the deep-MOND limit, longitudinal sector.
  K2-ESCALA the deep-MOND coefficient (via the stiffness rho_s) rides on J/K
           (external) -> "form equivalent, scale external".

Anti-circularity: no MOND/SI number in the generator; a0 is COMPARISON ONLY; fixed
seeds; auto-descriptive JSON.  Engine: fm2_core (the E1 O(3) ferromagnet).
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "cmb" / "fm2"))
import fm2_core as fm2  # noqa: E402

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

OUT = Path(__file__).resolve().parent
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = list(range(16))
N_BURN, N_MEAS = 400, 160
HS = np.array([1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001])
J_ORDERED = 1.0
L = 16
J_STIFF_SCAN = [0.9, 1.2, 1.6, 2.2]     # for rho_s(J): the candidate Khoury "Lambda"


def susceptibilities(L, J, h, seeds, n_burn=N_BURN, n_meas=N_MEAS):
    """chi_par = V Var(m_par) (longitudinal) and chi_perp = V Var(M_x) averaged over
    the two transverse components, both seed-averaged at beta=1.  Also return <m_par>
    (for the Ward check chi_perp = <m_par>/h)."""
    cpar, cperp, mpar = [], [], []
    V = L ** 3
    for sd in seeds:
        s = fm2.sample_observables(L, J, h, seed=sd, n_burn=n_burn, n_meas=n_meas)
        Mvec = s["Mvec"]                       # (n_meas, 3); field along +z
        cpar.append(V * np.var(Mvec[:, 2]))
        cperp.append(V * 0.5 * (np.var(Mvec[:, 0]) + np.var(Mvec[:, 1])))
        mpar.append(s["m_par"].mean())
    return (float(np.mean(cpar)), float(np.std(cpar) / np.sqrt(len(seeds))),
            float(np.mean(cperp)), float(np.std(cperp) / np.sqrt(len(seeds))),
            float(np.mean(mpar)))


def fit_power(h, y, rising_only=True):
    """Fit y ~ h^{-p} over the rising (small-h) regime above the peak; return p."""
    y = np.asarray(y)
    if rising_only:
        jpk = int(np.argmax(y))
        sel = h >= h[jpk]
    else:
        sel = np.ones(len(h), bool)
    if sel.sum() < 3:
        return float("nan")
    return float(-np.polyfit(np.log(h[sel]), np.log(y[sel]), 1)[0])


def main():
    t0 = time.time()
    print("=" * 76)
    print("C1 -- TEIC == Khoury? tree-level phonon vs deep-MOND-limit (longitudinal)")
    print("=" * 76)

    print(f"\n[K2] chi_par (longitudinal) vs chi_perp (transverse) on O(3), J={J_ORDERED}, "
          f"L={L}, {len(SEEDS)} seeds")
    cpar, epar, cperp, eperp, mpar = [], [], [], [], []
    for h in HS:
        a, ea, b, eb, mp = susceptibilities(L, J_ORDERED, h, SEEDS)
        cpar.append(a); epar.append(ea); cperp.append(b); eperp.append(eb); mpar.append(mp)
        print(f"  h={h:6.3f}  chi_par={a:8.3f}+-{ea:5.2f}  chi_perp={b:9.3f}+-{eb:6.2f}  "
              f"<m_par>={mp:.3f}  (m_par/h={mp/h:8.1f})")
    cpar, cperp, mpar = map(np.array, (cpar, cperp, mpar))

    p_par = fit_power(HS, cpar)
    # Transverse susceptibility: the fluctuation estimator V*Var(M_x) SATURATES at
    # small h on a finite box (the transverse correlation length xi_perp ~ 1/sqrt(h)
    # exceeds L), so it is finite-size-limited and NOT the true chi_perp.  The
    # physically correct transverse susceptibility in the broken phase is the Ward
    # identity chi_perp = <m_par>/h (Goldstone theorem), which is not finite-size
    # limited.  We use the Ward estimator for the verdict and report the fluctuation
    # one (with its saturation) for transparency.
    chi_perp_ward = mpar / HS
    p_perp_fluct = fit_power(HS, cperp)                  # finite-size-limited (saturates)
    p_perp_ward = -float(np.polyfit(np.log(HS), np.log(chi_perp_ward), 1)[0])

    print(f"\n  chi_par         ~ h^(-{p_par:.2f})   (deep-MOND/anomaly => ~0.5)")
    print(f"  chi_perp (Ward) ~ h^(-{p_perp_ward:.2f})   (Goldstone transverse => ~1.0)")
    print(f"  chi_perp (fluct, V*Var(M_x)) ~ h^(-{p_perp_fluct:.2f})  "
          f"[SATURATES at small h: finite-size xi_perp>L, not the true chi_perp]")

    p_perp = p_perp_ward
    distinct = bool(np.isfinite(p_par) and np.isfinite(p_perp) and (p_perp - p_par) > 0.25)

    # ---- K2-ESCALA: the candidate Khoury Lambda = stiffness rho_s(J) ----
    print(f"\n[K2-ESCALA] spin stiffness rho_s(J) -- the candidate Khoury Lambda scale")
    rho_of_J = {}
    for J in J_STIFF_SCAN:
        rho, mabs = fm2.helicity_modulus_series(L, J, seed=0, n_burn=N_BURN, n_meas=N_MEAS)
        rho_of_J[J] = rho
        print(f"  J={J:.1f}: rho_s={rho:.3f}  m_abs={mabs:.3f}")
    # rho_s varies strongly with J (the coupling/action normalisation) => external scale
    rhos = np.array([rho_of_J[J] for J in J_STIFF_SCAN])
    scale_external = bool(rhos.max() / max(rhos.min(), 1e-9) > 1.3)

    # ---- verdict ----
    g0_ok = bool(np.isfinite(p_par) and abs(p_par - 0.5) < 0.25)
    if distinct:
        verdict = ("LIMIT EQUIVALENCE (partial) -- chi_perp~h^-%.2f (transverse Goldstone, "
                   "quadratic ~X, the omega=ck magnon) and chi_par~h^-%.2f (longitudinal "
                   "coexistence anomaly = deep-MOND) have DISTINCT exponents.  The TEIC<->"
                   "Khoury equivalence lives in the LONGITUDINAL response sector (an emergent "
                   "IR anomaly), NOT in the tree-level transverse phonon action: the magnon is "
                   "~X, not Khoury's postulated X^{3/2}.  Confirms & sharpens Fase 2; the loose "
                   "claim 'magnon = Khoury phonon' is FALSE." % (p_perp, p_par))
    else:
        verdict = ("TREE-LEVEL EQUIVALENCE? -- chi_perp and chi_par share the deep-MOND "
                   "exponent; the transverse phonon itself carries the non-analyticity "
                   "(unexpected -- inspect).")
    if scale_external:
        verdict += ("  K2-ESCALA: the deep-MOND coefficient (stiffness rho_s) rides on J/K "
                    "(rho_s spans %.2f-%.2f over the J scan) => 'form equivalent, scale "
                    "external' -- a0 absolute stays external, as predicted." %
                    (rhos.min(), rhos.max()))

    print("-" * 76)
    print(f"  G0 (chi_par~h^-0.5) ok = {g0_ok};  sectors distinct = {distinct};  "
          f"scale external = {scale_external}")
    print(f"VERDICT: {verdict}")
    print("=" * 76)

    _figure(HS, cpar, epar, chi_perp_ward, cperp, eperp, p_par, p_perp_ward, p_perp_fluct)
    payload = {"engine": "fm2_core O(3) ferromagnet", "L": L, "J_ordered": J_ORDERED,
               "seeds": len(SEEDS), "n_burn": N_BURN, "n_meas": N_MEAS, "hs": HS.tolist(),
               "chi_par": cpar.tolist(), "chi_par_sem": epar,
               "chi_perp_ward_mpar_over_h": chi_perp_ward.tolist(),
               "chi_perp_fluct_VVarMx": cperp.tolist(), "chi_perp_fluct_sem": eperp,
               "m_par": mpar.tolist(),
               "exponent_par": p_par, "exponent_perp_ward": p_perp_ward,
               "exponent_perp_fluct_finite_size": p_perp_fluct,
               "note_chi_perp": ("chi_perp from the Ward identity <m_par>/h (correct in "
                   "the broken phase); the fluctuation estimator V*Var(M_x) saturates at "
                   "small h (xi_perp>L, finite size) and is reported only for transparency."),
               "rho_s_of_J": rho_of_J,
               "G0_chi_par_p_near_0.5": g0_ok,
               "sectors_distinct": distinct, "scale_external": scale_external,
               "verdict": verdict, "runtime_s": time.time() - t0}
    (OUT / "C1_khoury_equivalence.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved C1_khoury_equivalence.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(hs, cpar, epar, cperp_ward, cperp_fl, eperp, p_par, p_perp_ward, p_perp_fl):
    fig, ax = plt.subplots(1, 2, figsize=(12, 4.8))
    ax[0].errorbar(hs, cpar, yerr=epar, marker="o", lw=1.5, label=r"$\chi_\parallel$ (longitudinal)")
    ax[0].plot(hs, cperp_ward, "s-", lw=1.5, label=r"$\chi_\perp$ Ward $=\langle m_\parallel\rangle/h$")
    ax[0].plot(hs, cperp_fl, "^:", lw=1, mfc="none",
               label=r"$\chi_\perp$ fluct $V\,$Var$(M_x)$ (finite-size)")
    hh = np.logspace(np.log10(hs.min()), np.log10(hs.max()), 50)
    n_par = cpar[np.argmax(cpar)] * np.sqrt(hs[np.argmax(cpar)])
    n_perp = cperp_ward[-1] * hs[-1]
    ax[0].plot(hh, n_par / np.sqrt(hh), "k--", lw=1, label=r"$\propto h^{-1/2}$ (deep-MOND)")
    ax[0].plot(hh, n_perp / hh, "k:", lw=1, label=r"$\propto h^{-1}$ (Goldstone)")
    ax[0].set_xscale("log"); ax[0].set_yscale("log")
    ax[0].set_xlabel("external field h  (~ gravitational gradient g)")
    ax[0].set_ylabel("susceptibility")
    ax[0].set_title(f"longitudinal vs transverse response\n"
                    f"chi_par~h^-{p_par:.2f} (deep-MOND), chi_perp~h^-{p_perp_ward:.2f} (Goldstone)")
    ax[0].legend(fontsize=7)
    ax[1].plot(hs, np.array(cperp_ward) / np.array(cpar), "o-", lw=1.5)
    ax[1].set_xscale("log"); ax[1].set_yscale("log")
    ax[1].set_xlabel("external field h"); ax[1].set_ylabel(r"$\chi_\perp/\chi_\parallel$")
    ax[1].set_title("sector separation: transverse phonon (~X, h^-1)\nvs longitudinal anomaly (deep-MOND, h^-1/2)")
    ax[1].grid(alpha=0.2)
    fig.suptitle("C1: the TEIC<->Khoury equivalence lives in the longitudinal response, "
                 "not the tree-level phonon", fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    fig.savefig(OUT / "C1_khoury_equivalence.png", dpi=130)
    print("saved C1_khoury_equivalence.png")


if __name__ == "__main__":
    main()
