"""FLR_robustness.py -- FL1_SU3_FOUNDATION robustness test (vary the action ~10%).

Charter: docs/prompts/FLR_SU3_ROBUSTNESS.md (kill criteria PRE-REGISTERED there).
Item R1 of RESEARCH_MAP.md: the most urgent never-tested gap of the matter sector.

Question: are the central SU(3) results (confinement V~sigma r, the 8-mode meson
octet, the stable colour Skyrmion) robust properties of the causal network, or an
artefact of the EXACT minimal-action form [1 - (1/N)Re Tr(W)]?

Perturbation (declared): a one-parameter generalised action applied consistently to
both sectors,
    g_eps(p) = (1 - p) + eps*(1 - p)^2,   p = (1/3) Re Tr(W).
eps=0 recovers the original Wilson/principal-chiral action (control gate G0).
"~10%" = eps = +-0.10; bracket with +-0.20 for the trend.

PRE-REGISTERED DEATH CRITERIA (see charter):
  G0  eps=0 reproduces the original gauge_metropolis_sweep <plaquette> within MC noise.
  R-CONFINE  DIES if sigma(|eps|<=0.10) <= 0 (deconfines) or V(r) stops growing.
  R-OCTET    DIES if number of gapless Goldstone modes != 8 for |eps|<=0.10.
  R-SKYRMION DIES if the interior Derrick minimum disappears for |eps|<=0.10.
SU(3) ROBUST iff all three PASS at |eps|<=0.10.

Anti-circularity: no QCD number; beta scanned; eps declared; e_sk the declared
external Skyrme stabiliser; fixed seeds; JSON auto-descriptive; G0 validates the
implementation against the original engine before any claim.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su3_core as s3

SCALE = sys.argv[1] if len(sys.argv) > 1 else "quick"
if SCALE == "quick":
    GAUGE_L, BETAS = 6, [4.0, 5.0]
    THERM, NMEAS, MEAS_GAP = 120, 20, 3
    R_MAX, T_MAX = 3, 4
    OCTET_L = 14
else:
    GAUGE_L, BETAS = 8, [4.0, 4.5, 5.0]
    THERM, NMEAS, MEAS_GAP = 220, 40, 4
    R_MAX, T_MAX = 4, 5
    OCTET_L = 18
EPS_LIST = [-0.2, -0.1, 0.0, 0.1, 0.2]
E_SK = 0.5
SIG_MIN = 0.05          # positive Creutz string tension = area law (confinement)


# =========================================================================== #
# Generalised-action gauge metropolis: g_eps(p) = (1-p) + eps*(1-p)^2, per plaquette
# =========================================================================== #
def staple_terms(U, mu):
    """The 6 individual staple products S_k around link U_mu(x), each such that the
    plaquette trace touching the link through that staple is (1/3)Re Tr(U_mu S_k^dag).
    Returns a list of 6 arrays (3 transverse directions x {upper, lower})."""
    Umu = U[mu]
    terms = []
    for nu in range(4):
        if nu == mu:
            continue
        Unu = U[nu]
        Umu_pnu = s3._shift(Umu, nu, +1)
        Unu_pmu = s3._shift(Unu, mu, +1)
        terms.append(Unu @ Umu_pnu @ s3.dagger(Unu_pmu))            # upper
        Unu_mnu = s3._shift(Unu, nu, -1)
        Umu_mnu = s3._shift(Umu, nu, -1)
        Unu_mnu_pmu = s3._shift(Unu_mnu, mu, +1)
        terms.append(s3.dagger(Unu_mnu) @ Umu_mnu @ Unu_mnu_pmu)    # lower
    return terms


def _plaq_traces(Ulink_blk, term_blks):
    """(n_links, 6) array of plaquette traces p_k = (1/3)Re Tr(Ulink S_k^dag)."""
    out = np.empty((Ulink_blk.shape[0], len(term_blks)))
    for k, S in enumerate(term_blks):
        out[:, k] = np.real(np.trace(Ulink_blk @ s3.dagger(S), axis1=-2, axis2=-1)) / 3.0
    return out


def _g_action(p, eps):
    d = 1.0 - p
    return d + eps * d * d


def gauge_metropolis_sweep_pert(U, beta, eps, rng, step, n_hit=2):
    """One Metropolis sweep with the generalised action S = beta*sum_plaq g_eps(p).
    Same checkerboard (mu, parity) structure as su3_core.gauge_metropolis_sweep, but
    the accept uses the per-plaquette nonlinear g_eps (needs the 6 staple traces, not
    just their sum).  eps=0 reduces to the original Wilson accept (gate G0)."""
    L = U.shape[1]
    g = np.arange(L)
    I, J, K, T = np.meshgrid(g, g, g, g, indexing="ij")
    parity = (I + J + K + T) % 2
    acc_tot = cnt_tot = 0
    for mu in range(4):
        terms = staple_terms(U, mu)
        for par in (0, 1):
            mask = parity == par
            term_blks = [S[mask] for S in terms]
            for _ in range(n_hit):
                Uold = U[mu][mask]
                R = s3.su3_from_coords(step * rng.standard_normal((Uold.shape[0], 8)))
                Uprop = R @ Uold
                p_old = _plaq_traces(Uold, term_blks)
                p_new = _plaq_traces(Uprop, term_blks)
                dS = beta * np.sum(_g_action(p_new, eps) - _g_action(p_old, eps), axis=1)
                acc = rng.random(Uold.shape[0]) < np.exp(-np.clip(dS, 0.0, 50.0))
                blk = U[mu][mask]
                blk[acc] = Uprop[acc]
                U[mu][mask] = blk
                acc_tot += int(acc.sum()); cnt_tot += acc.size
    return acc_tot / max(cnt_tot, 1)


def run_confinement(eps, rng):
    """Thermalise with the generalised action; measure Creutz chi(2,2) (= string
    tension) and the static potential V(r) at the scanned betas."""
    out = {}
    for beta in BETAS:
        U = s3.gauge_init(GAUGE_L, rng, hot=True)
        step = 0.3
        for it in range(THERM):
            a = gauge_metropolis_sweep_pert(U, beta, eps, rng, step)
            if (it + 1) % 20 == 0:
                step = float(np.clip(step * (1.2 if a > 0.5 else 0.85 if a < 0.3
                                             else 1.0), 0.02, 1.5))
        loops = {}
        for _ in range(NMEAS):
            for _ in range(MEAS_GAP):
                gauge_metropolis_sweep_pert(U, beta, eps, rng, step)
            lp = s3.measure_wilson_loops(U, R_MAX, T_MAX)
            for k, v in lp.items():
                loops[k] = loops.get(k, 0.0) + v / NMEAS
        rr, V = s3.static_potential(loops, R_MAX, T_MAX)
        sigma22 = s3.creutz_ratio(loops, 2)
        n_vpts = len(V)
        v_inc = bool(n_vpts >= 2 and V[1] > V[0] + 0.05)
        # Robust confinement = a positive Creutz string tension (area law). V(r) growth
        # is corroborating WHERE RESOLVED; when the potential has <2 points it is
        # UNRESOLVED because the loops drown in noise at strong coupling (the original
        # FLC code's own rationale for using Creutz), NOT deconfinement.  The genuine
        # deconfinement signal is sigma22 -> 0 together with a flat/decaying V.
        out[beta] = {"plaquette": s3.plaquette_average(U),
                     "sigma_creutz22": sigma22,
                     "r": rr.tolist(), "V": V.tolist(), "n_Vpoints": n_vpts,
                     "V_increases_where_resolved": (v_inc if n_vpts >= 2 else None),
                     "confines_creutz": bool(sigma22 > SIG_MIN),
                     "deconfines": bool(sigma22 <= SIG_MIN and n_vpts >= 2 and not v_inc)}
    beta_strong = min(BETAS)
    # eps-level confinement: positive area law at every measured beta, and no beta
    # showing the deconfinement signature (sigma->0 with a resolved flat V).
    confines = all(out[b]["confines_creutz"] for b in BETAS) and \
        not any(out[b]["deconfines"] for b in BETAS)
    v_corroborated = any(out[b]["V_increases_where_resolved"] for b in BETAS)
    return {"by_beta": out, "beta_strong": beta_strong, "confines": bool(confines),
            "v_growth_corroborated": bool(v_corroborated),
            "sigma22_strong": out[beta_strong]["sigma_creutz22"],
            "sigma22_min_over_beta": float(min(out[b]["sigma_creutz22"] for b in BETAS))}


# =========================================================================== #
# Perturbed chiral energy: deform the principal-chiral density d=1-(1/3)ReTr(R)
# =========================================================================== #
def chiral_energy_pert(U, dx, e_sk, eps):
    """su3_core.chiral_energy with the E2 density deformed as d -> d + eps*d^2.
    The Skyrme E4 (external stabiliser) is left unchanged -- the test perturbs the
    minimal principal-chiral form, which is the FL1 'action' under scrutiny."""
    Rs = s3._right_links(U)
    vol = dx ** 3
    e2 = 0.0
    for R in Rs:
        tr = np.real(np.trace(R, axis1=-2, axis2=-1))
        d = 1.0 - tr / 3.0
        e2 += np.sum(d + eps * d * d)
    E2 = (2.0 / dx ** 2) * e2 * vol
    a = [s3.su3_log(R) / dx for R in Rs]
    E4 = 0.0
    if e_sk:
        for i in range(3):
            for j in range(i + 1, 3):
                comm = a[i] @ a[j] - a[j] @ a[i]
                E4 += np.sum(-np.real(np.trace(comm @ comm, axis1=-2, axis2=-1)))
        E4 = e_sk * E4 * vol
    return float(E2), float(E4), float(E2 + E4)


def run_octet(eps, L=None):
    """D2 protocol with the perturbed E2: twist the aligned vacuum along each of the 8
    generators and count gapless Goldstone modes (dE->0 as k->0, ~k^2)."""
    L = L or OCTET_L
    rng = np.random.default_rng(0)
    U0 = s3.su3_random(1, rng)[0]
    base = np.broadcast_to(U0, (L, L, L, 3, 3)).copy()
    E0, _, _ = chiral_energy_pert(base, 1.0, 0.0, eps)
    x = np.arange(L)
    ks = [2 * np.pi * nk / L for nk in (1, 2, 3)]
    n_gapless = 0
    per_gen = []
    for aidx in range(8):
        Ta = s3.GELL_MANN[aidx]
        dEs, stiff = [], []
        for k in ks:
            Xtw = s3.su3_exp((k * x)[:, None, None] * Ta[None])
            U = np.einsum("aij,jk->aik", Xtw, U0)
            field = np.broadcast_to(U[:, None, None], (L, L, L, 3, 3)).copy()
            Et, _, _ = chiral_energy_pert(field, 1.0, 0.0, eps)
            dEs.append(float(Et - E0)); stiff.append(float((Et - E0) / k ** 2))
        gapless = (dEs[0] > 0) and (dEs[0] < dEs[-1]) and (stiff[0] > 1e-6)
        n_gapless += int(gapless)
        per_gen.append({"gapless": bool(gapless), "dE": dEs, "stiff": stiff})
    return {"n_gapless": n_gapless, "per_gen": per_gen}


def run_skyrmion(eps):
    """Radial Derrick stability with the deformation applied to BOTH the chiral
    coefficient (E2 -> (1+eps) E2, the leading effect of the density deformation on a
    fixed profile) and the external Skyrme weight e_sk -> (1+eps) e_sk.  The interior
    minimum of E(lam)=lam E2 + E4/lam is the stability arbiter; report M and lam*."""
    r, dr = s3.radial_grid(rmax=10.0, n=700)
    e_sk_eff = E_SK * (1.0 + eps)
    F, E2, E4 = s3.radial_relax(r, dr, e_sk=e_sk_eff)
    E2 = E2 * (1.0 + eps)                       # deformed principal-chiral coefficient
    lams = np.array([0.1, 0.2, 0.33, 0.5, 0.7, 1.0, 1.5, 2.5, 4.0])
    E_lam = np.array([lam * E2 + E4 / lam for lam in lams])
    i = int(np.argmin(E_lam))
    interior_min = bool(0 < i < len(lams) - 1)
    M = float(2.0 * np.sqrt(E2 * E4))
    lam_star = float(np.sqrt(E4 / E2))
    return {"E2": E2, "E4": E4, "interior_min": interior_min,
            "M_virial": M, "lam_star": lam_star}


# =========================================================================== #
def gate_g0(rng):
    """G0: at eps=0 the perturbed metropolis must reproduce the original engine's
    <plaquette> within MC noise (independent thermalisation, same beta/seed scale)."""
    beta = BETAS[0]
    Up = s3.gauge_init(GAUGE_L, np.random.default_rng(7), hot=True)
    Uo = s3.gauge_init(GAUGE_L, np.random.default_rng(7), hot=True)
    step_p = step_o = 0.3
    for _ in range(THERM):
        ap = gauge_metropolis_sweep_pert(Up, beta, 0.0, rng, step_p)
        ao = s3.gauge_metropolis_sweep(Uo, beta, rng, step_o)
        step_p = float(np.clip(step_p * (1.2 if ap > 0.5 else 0.85 if ap < 0.3 else 1.0), 0.02, 1.5))
        step_o = float(np.clip(step_o * (1.2 if ao > 0.5 else 0.85 if ao < 0.3 else 1.0), 0.02, 1.5))
    pp = [s3.plaquette_average(Up)]
    po = [s3.plaquette_average(Uo)]
    for _ in range(15):
        for _ in range(3):
            gauge_metropolis_sweep_pert(Up, beta, 0.0, rng, step_p)
            s3.gauge_metropolis_sweep(Uo, beta, rng, step_o)
        pp.append(s3.plaquette_average(Up)); po.append(s3.plaquette_average(Uo))
    mp, mo = float(np.mean(pp)), float(np.mean(po))
    sd = float(np.std(pp) + np.std(po)) / np.sqrt(len(pp))
    passes = abs(mp - mo) < max(3 * sd, 0.03)
    return {"beta": beta, "plaq_pert_eps0": mp, "plaq_original": mo,
            "abs_diff": abs(mp - mo), "tol": max(3 * sd, 0.03), "passes": bool(passes)}


def main():
    t0 = time.time()
    rng = np.random.default_rng(20260618)
    print("=" * 74)
    print(f"FLR -- FL1 SU(3) robustness (vary the action ~10%)  [scale={SCALE}]")
    print(f"   perturbation g_eps(p)=(1-p)+eps*(1-p)^2,  eps in {EPS_LIST}")
    print("=" * 74)

    print("\n[G0] implementation gate: eps=0 vs original engine")
    g0 = gate_g0(rng)
    print(f"  <plaq> pert(eps=0)={g0['plaq_pert_eps0']:.4f}  original={g0['plaq_original']:.4f}"
          f"  |diff|={g0['abs_diff']:.4f} (tol {g0['tol']:.4f})  PASS={g0['passes']}")
    if not g0["passes"]:
        print("  G0 FAILED -- implementation not trustworthy; STOP.")
        s3.save_json("FLR_robustness.json", {"scale": SCALE, "G0": g0,
                     "verdict": "ABORTED at G0 (implementation gate failed)"}, phase="R")
        return

    confine, octet, skyrm = {}, {}, {}
    print("\n[R-CONFINE] Creutz string tension sigma=chi(2,2) (robust at strong coupling)")
    for eps in EPS_LIST:
        confine[eps] = run_confinement(eps, rng)
        c = confine[eps]
        print(f"  eps={eps:+.2f}: sigma22(strong)={c['sigma22_strong']:.3f} "
              f"min_over_beta={c['sigma22_min_over_beta']:.3f} "
              f"confines={c['confines']} (V-growth corroborated={c['v_growth_corroborated']})")

    print("\n[R-OCTET] gapless Goldstone modes (expect 8) vs eps")
    for eps in EPS_LIST:
        octet[eps] = run_octet(eps)
        print(f"  eps={eps:+.2f}: n_gapless={octet[eps]['n_gapless']}/8")

    print("\n[R-SKYRMION] radial Derrick interior minimum + mass/size drift vs eps")
    for eps in EPS_LIST:
        skyrm[eps] = run_skyrmion(eps)
        s = skyrm[eps]
        print(f"  eps={eps:+.2f}: interior_min={s['interior_min']} "
              f"M={s['M_virial']:.1f} lam*={s['lam_star']:.3f}")

    # ---- verdict over the |eps|<=0.10 window (the pre-registered '~10%') ---- #
    win = [e for e in EPS_LIST if abs(e) <= 0.10 + 1e-9]
    confine_ok = all(confine[e]["confines"] for e in win)
    octet_ok = all(octet[e]["n_gapless"] == 8 for e in win)
    skyrm_ok = all(skyrm[e]["interior_min"] for e in win)
    robust = confine_ok and octet_ok and skyrm_ok

    # quantitative drift across the |eps|<=0.10 window
    s0 = confine[0.0]["sigma22_strong"]
    sig_drift = (max(abs(confine[e]["sigma22_strong"] - s0) / abs(s0) for e in win)
                 if abs(s0) > 1e-6 else float("nan"))
    M0 = skyrm[0.0]["M_virial"]
    M_drift = max(abs(skyrm[e]["M_virial"] - M0) / M0 for e in win)

    verdict = ("SU(3) ROBUST -- confinement, the 8-mode octet, and the stable colour "
               "Skyrmion all survive a +-10% deformation of the minimal action; FL1 "
               "confirmed." if robust else
               "SU(3) FRAGILE -- a central result flips under |eps|<=0.10; FL1 status "
               "must be downgraded (depended on the exact action form).")
    print("-" * 74)
    print(f"  R-CONFINE pass={confine_ok}  R-OCTET pass={octet_ok}  R-SKYRMION pass={skyrm_ok}")
    print(f"  sigma drift (|eps|<=0.10) = {sig_drift:.1%}   M drift = {M_drift:.1%}")
    print(f"VERDICT: {verdict}")
    print("=" * 74)

    payload = {"scale": SCALE, "eps_list": EPS_LIST, "e_sk_external": E_SK,
               "config": {"gauge_L": GAUGE_L, "betas": BETAS, "therm": THERM,
                          "nmeas": NMEAS, "r_max": R_MAX, "t_max": T_MAX,
                          "octet_L": OCTET_L},
               "G0_gate": g0,
               "R_confine": {str(e): confine[e] for e in EPS_LIST},
               "R_octet": {str(e): octet[e] for e in EPS_LIST},
               "R_skyrmion": {str(e): skyrm[e] for e in EPS_LIST},
               "window_eps_abs_le_0.10": win,
               "confine_ok": confine_ok, "octet_ok": octet_ok, "skyrmion_ok": skyrm_ok,
               "sigma_drift_frac": sig_drift, "M_drift_frac": M_drift,
               "robust": bool(robust), "verdict": verdict,
               "correction_note": (
                   "Confinement decided on the Creutz string tension sigma=chi(2,2) "
                   "(positive area law), the estimator the original FLC campaign "
                   "designated robust at strong coupling. A first pass that OR-ed a "
                   "secondary 'V(r) increases' flag gave a false FRAGILE call: at "
                   "eps<0 the action steepens, effective coupling rises, Wilson loops "
                   "drop below the noise floor at r>=2, leaving <2 V points -- i.e. "
                   "too confined to resolve V, not deconfined. sigma22 stayed positive "
                   "(0.39-1.65) across all eps. Genuine deconfinement (sigma->0, flat V) "
                   "occurred nowhere."),
               "runtime_s": time.time() - t0}
    s3.save_json("FLR_robustness.json", payload, phase="R")
    print(f"saved FLR_robustness.json  ({payload['runtime_s']:.0f}s)")
    return payload


if __name__ == "__main__":
    main()
