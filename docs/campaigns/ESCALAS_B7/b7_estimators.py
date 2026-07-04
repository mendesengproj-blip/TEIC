"""b7_estimators.py -- correlation-length estimators + power-vs-exponential
discriminator for campaign ESCALAS_B7 (xi(J): is dimensional transmutation
possible on this substrate?).

This is the NEW code the pre-registration calls "the real work": two xi
estimators (Ornstein-Zernike log-fit and the fit-free second moment) and the
P-vs-E model discriminator.  It contains NO physics scale and NO critical value:
xi, nu, sigma, Jc all emerge from the supplied (r, C) curves / (J, xi) curves.
The reference exponents (3D Heisenberg nu, KT sigma) live only in the gate's
COMPARISON, never in a generator.

Forms discriminated (PRE_REGISTRO sec.2, sec.4):
    Model P (power):        xi = A * |Jc - J|^(-nu)
    Model E (exponential):  xi = B * exp(b * |Jc - J|^(-sigma))   [sigma free]
and, for a system whose ordering point is at infinity (the 1D chain, Jc->inf),
the J-direct forms:
    Model P_inf:  xi = A * J^p           (power in J)
    Model E_inf:  xi = B * exp(c * J)    (exponential in J)

All comparisons are by BIC computed from log-space chi^2 (Gaussian errors on
log xi), penalising Model E's extra parameter.
"""
from __future__ import annotations

import numpy as np


# ====================================================================== #
# Connected correlation and the two xi estimators (PRE_REGISTRO sec.3)
# ====================================================================== #
def connected(C_raw, m2):
    """C_conn(r) = <s(0).s(r)> - m^2 (subtract the disconnected/clustering part)."""
    return np.asarray(C_raw, float) - float(m2)


def _positive_window(r, C, r_lo, floor):
    """Contiguous run r>=r_lo with C>floor (stop at the first drop below floor):
    the reliable decaying part of the curve before it hits the noise plateau."""
    r = np.asarray(r, float)
    C = np.asarray(C, float)
    idx = []
    for i in range(len(r)):
        if r[i] < r_lo:
            continue
        if np.isfinite(C[i]) and C[i] > floor:
            idx.append(i)
        elif idx:                       # first drop after we started -> stop
            break
    return np.array(idx, dtype=int)


def xi_oz(r, C, w=None, r_lo=1, floor=0.01):
    """Ornstein-Zernike estimator: fit log C = a - r/xi - p*log(r) over the
    reliable window and read xi off the -r coefficient.  The p*log r term is the
    OZ power prefactor C ~ exp(-r/xi)/r^p; including it de-biases xi.

    Returns dict(xi, p, R2, n_points) -- xi = inf if no decay, nan if < 3 points.
    """
    r = np.asarray(r, float)
    C = np.asarray(C, float)
    sel = _positive_window(r, C, r_lo, floor)
    out = {"xi": float("nan"), "p": float("nan"), "R2": float("nan"),
           "n_points": int(sel.size), "coef": None, "sel": sel}
    if sel.size < 3:
        return out
    rr, cc = r[sel], C[sel]
    logc = np.log(cc)
    X = np.column_stack([np.ones_like(rr), rr, np.log(rr)])
    coef, *_ = np.linalg.lstsq(X, logc, rcond=None)
    pred = X @ coef
    ss_res = float(np.sum((logc - pred) ** 2))
    ss_tot = float(np.sum((logc - logc.mean()) ** 2))
    out["R2"] = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    out["xi"] = float(-1.0 / coef[1]) if coef[1] < 0 else float("inf")
    out["p"] = float(-coef[2])
    out["coef"] = coef
    return out


def xi_second_moment(r, C, w=None, r_lo=1, floor=0.01):
    """Fit-free second-moment estimator.  PRE_REGISTRO writes
    xi^2_2nd = sum r^2 C / sum C; we normalise by 1/2 so that for a pure 1D
    exponential C(r)=exp(-r/xi) the estimator returns xi exactly
    (int r^2 e^{-r/xi} / int e^{-r/xi} = 2 xi^2).  This convention-match is what
    makes the +-15% cross-check against xi_oz meaningful: a >15% gap then flags a
    genuinely non-exponential / saturated / noisy tail, not a units mismatch.

    Optional weights w (e.g. shell pair-counts) are folded in if supplied.
    """
    r = np.asarray(r, float)
    C = np.asarray(C, float)
    sel = _positive_window(r, C, r_lo, floor)
    if sel.size < 3:
        return float("nan")
    rr, cc = r[sel], C[sel]
    ww = np.ones_like(cc) if w is None else np.asarray(w, float)[sel]
    # data-driven geometric tail: the second moment over-weights the part of the
    # exponential tail truncated by the noise floor.  Estimate the per-unit-r decay
    # ratio q from the last few measured points and append the analytic tail
    # C(r)~C_last q^(r-r_last) so the moments integrate the full curve, not the
    # truncated one.  This uses only local data (no global fit) -> stays fit-free.
    if w is None and cc.size >= 3 and cc[-1] > 0 and cc[-2] > 0:
        q = (cc[-1] / cc[-3]) ** (1.0 / (rr[-1] - rr[-3]))
        if 0.0 < q < 1.0:
            j = np.arange(1, 400)
            r_tail = rr[-1] + j
            c_tail = cc[-1] * q ** j
            keep = c_tail > 1e-6 * cc[0]
            rr = np.concatenate([rr, r_tail[keep]])
            cc = np.concatenate([cc, c_tail[keep]])
            ww = np.concatenate([ww, np.ones(int(keep.sum()))])
    num = float(np.sum(ww * rr ** 2 * cc))
    den = float(np.sum(ww * cc))
    if den <= 0:
        return float("nan")
    return float(np.sqrt(0.5 * num / den))


def xi_fixed_p(r, C, p, w=None, r_lo=1, floor=0.01):
    """OZ fit with the prefactor p FIXED: log(C r^p) = a - r/xi (a pure line).
    Fixing p removes the xi-p degeneracy that makes the free-p fit oscillate on
    short windows.  Returns dict(xi, R2, n_points)."""
    r = np.asarray(r, float); C = np.asarray(C, float)
    sel = _positive_window(r, C, r_lo, floor)
    out = {"xi": float("nan"), "R2": float("nan"), "n_points": int(sel.size)}
    if sel.size < 3:
        return out
    rr = r[sel]
    y = np.log(C[sel]) + p * np.log(rr)
    A = np.column_stack([np.ones_like(rr), rr])
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    pred = A @ c
    ss_res = float(np.sum((y - pred) ** 2)); ss_tot = float(np.sum((y - y.mean()) ** 2))
    out["R2"] = 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
    out["xi"] = float(-1.0 / c[1]) if c[1] < 0 else float("inf")
    return out


def extract_curve_set(curves, dmax, size_cut=4.0, tol=0.15, r_lo=1, floor=0.01):
    """Two-pass xi(J) extraction over a whole J-sweep (lattice OR causet).

    Pass 1: free-p OZ fit on each J's seed-averaged connected C(r) -> a GLOBAL
            prefactor p (median over clean curves), breaking the xi-p degeneracy.
    Pass 2: fixed-(global p) fit per J for the value, per seed for the error bar;
            cross-checked against the second moment (mapped through the same p);
            finite-size cut xi < dmax/size_cut.

    `curves` is a list of dicts {J, r, C_seeds (list of connected-C arrays), w}.
    Returns (records, global_p).
    """
    free_p = []
    for cv in curves:
        Cm = np.nanmean(cv["C_seeds"], axis=0)
        oz = xi_oz(cv["r"], Cm, cv.get("w"), r_lo, floor)
        if oz["R2"] > 0.9 and np.isfinite(oz["xi"]) and oz["xi"] > 0:
            free_p.append(oz["p"])
    gp = float(np.clip(np.median(free_p), 0.0, 1.5)) if free_p else 0.0
    fac2 = (2.0 - gp) * (1.0 - gp) / 2.0

    recs = []
    for cv in curves:
        Cm = np.nanmean(cv["C_seeds"], axis=0)
        fxm = xi_fixed_p(cv["r"], Cm, gp, cv.get("w"), r_lo, floor)
        per = []
        for Cs in cv["C_seeds"]:
            fx = xi_fixed_p(cv["r"], Cs, gp, cv.get("w"), r_lo, floor)
            if np.isfinite(fx["xi"]) and fx["xi"] > 0 and fx["R2"] > 0.85:
                per.append(fx["xi"])
        xi = fxm["xi"]
        if np.isfinite(xi) and xi > 0 and fxm["R2"] > 0.92 and len(per) >= 1:
            err = float(np.std(per, ddof=1) / np.sqrt(len(per))) if len(per) > 1 \
                else 0.12 * xi
            x2 = xi_second_moment(cv["r"], Cm, cv.get("w"), r_lo, floor)
            x2_eq = x2 / np.sqrt(fac2) if fac2 > 0.02 and np.isfinite(x2) else x2
            gap = abs(xi - x2_eq) / (0.5 * (xi + x2_eq)) if np.isfinite(x2_eq) else float("nan")
            recs.append({"J": float(cv["J"]), "xi": float(xi),
                         "xi_err": max(err, 0.03 * xi), "R2": fxm["R2"],
                         "xi_2nd": float(x2), "gap": float(gap),
                         "n_points": fxm["n_points"], "n_seeds_ok": len(per),
                         "cross_check_ok": bool(np.isfinite(gap) and gap <= tol),
                         "passes_cut": bool(xi < dmax / size_cut)})
        else:
            recs.append({"J": float(cv["J"]), "xi": float("nan"),
                         "n_seeds_ok": len(per), "passes_cut": False,
                         "cross_check_ok": False})
    return recs, gp


def estimate_xi(r, C, w=None, r_lo=1, floor=0.01, tol=0.15):
    """Two estimators + the cross-check (PRE_REGISTRO sec.3).

      xi_oz   : Ornstein-Zernike log-fit (free prefactor p), the primary value
                fed to the discriminator.
      xi_2nd  : the fit-free second moment sqrt( (1/2) sum r^2 C / sum C ) of the
                pre-registration, reported verbatim.

    Cross-check.  The raw second moment carries a known prefactor bias
    (<r^2>=(2-p)(1-p)xi^2) and a discreteness/truncation shift, so it is NOT
    numerically equal to xi_oz.  The reliable comparison is in MOMENT SPACE on the
    SAME support: compute the second moment of the DATA and of the fitted OZ curve
    over identical r, and map xi_2nd_resid = xi_oz * sqrt(M2_data/M2_fit).  For a
    clean OZ curve this equals xi_oz (gap->0); a fat/saturated/noisy tail makes
    M2_data depart from M2_fit and the gap grows -- precisely the per-point
    reliability the gate needs, free of the normalisation ambiguity.  A point is
    accepted iff gap<=tol AND the OZ fit is good (R^2>0.92)."""
    oz = xi_oz(r, C, w, r_lo, floor)
    x1, p = oz["xi"], oz["p"]
    x2_raw = xi_second_moment(r, C, w, r_lo, floor)
    res = {"xi_oz": x1, "xi_2nd": x2_raw, "p": p, "R2_oz": oz["R2"],
           "n_points": oz["n_points"]}
    sel = oz["sel"]
    if not (np.isfinite(x1) and x1 > 0 and oz["coef"] is not None and sel.size >= 3):
        res.update(xi=float("nan"), gap=float("nan"), accept=False,
                   xi_2nd_resid=float("nan"))
        return res
    rr = np.asarray(r, float)[sel]
    cc = np.asarray(C, float)[sel]
    coef = oz["coef"]
    c_fit = np.exp(coef[0] + coef[1] * rr + coef[2] * np.log(rr))
    m2_data = float(np.sum(rr ** 2 * cc) / np.sum(cc))
    m2_fit = float(np.sum(rr ** 2 * c_fit) / np.sum(c_fit))
    x2_resid = x1 * np.sqrt(m2_data / m2_fit) if m2_fit > 0 else float("nan")
    gap = abs(x1 - x2_resid) / (0.5 * (x1 + x2_resid)) if np.isfinite(x2_resid) else float("nan")
    res.update(xi_2nd_resid=float(x2_resid), xi=float(x1), gap=float(gap),
               accept=bool(np.isfinite(gap) and gap <= tol and oz["R2"] > 0.92))
    return res


# ====================================================================== #
# BIC helper (log-space Gaussian chi^2 + parameter penalty)
# ====================================================================== #
def _bic(logxi, pred, sig, k):
    n = len(logxi)
    chi2 = float(np.sum(((logxi - pred) / sig) ** 2))
    return chi2 + k * np.log(n), chi2


# ====================================================================== #
# Discriminator -- finite ordering point Jc (causet, 3D lattice, 2D KT)
# ====================================================================== #
def discriminate_finite(J, xi, xi_err, Jc, sigma_grid=None):
    """Fit xi(J) to Model P and Model E with a FIXED finite Jc.

    log xi = logA - nu * log(Jc - J)                       (P, k=2)
    log xi = logB + b * (Jc - J)^(-sigma)  [sigma scanned] (E, k=3)

    Returns dict with winner ('power'|'exp'), dBIC_E_over_P (=BIC_P-BIC_E; >0
    favours E), nu, sigma, b, both chi^2, n_points.
    """
    J = np.asarray(J, float)
    xi = np.asarray(xi, float)
    xi_err = np.asarray(xi_err, float)
    d = Jc - J
    good = (d > 0) & np.isfinite(xi) & (xi > 0)
    J, xi, xi_err, d = J[good], xi[good], xi_err[good], d[good]
    n = len(xi)
    out = {"n_points": int(n)}
    if n < 4:
        out.update(winner="insufficient", dBIC_E_over_P=float("nan"))
        return out
    logxi = np.log(xi)
    sig = np.maximum(xi_err / xi, 1e-3)            # error on log xi

    # ---- Model P: linear in (logA, nu) over [1, -log d] ----
    Xp = np.column_stack([np.ones(n), -np.log(d)])
    cp, *_ = np.linalg.lstsq((Xp / sig[:, None]), logxi / sig, rcond=None)
    predp = Xp @ cp
    bic_p, chi2_p = _bic(logxi, predp, sig, k=2)
    nu = float(cp[1])

    # ---- Model E: scan sigma, linear in (logB, b) over [1, d^-sigma] ----
    if sigma_grid is None:
        sigma_grid = np.linspace(0.25, 2.0, 36)
    best = None
    for s in sigma_grid:
        Xe = np.column_stack([np.ones(n), d ** (-s)])
        ce, *_ = np.linalg.lstsq((Xe / sig[:, None]), logxi / sig, rcond=None)
        prede = Xe @ ce
        bic_e, chi2_e = _bic(logxi, prede, sig, k=3)
        if best is None or bic_e < best[0]:
            best = (bic_e, chi2_e, float(s), float(ce[1]), float(ce[0]))
    bic_e, chi2_e, sigma, b, logB = best

    dbic = bic_p - bic_e                            # >0 -> E preferred
    winner = "exp" if dbic > 2.0 else "power"
    out.update(winner=winner, dBIC_E_over_P=float(dbic), nu=nu, sigma=sigma,
               b=b, chi2_power=chi2_p, chi2_exp=chi2_e,
               R2_power=_r2(logxi, predp))
    # R2 of the winning E for reporting
    Xe = np.column_stack([np.ones(n), d ** (-sigma)])
    out["R2_exp"] = _r2(logxi, Xe @ np.array([logB, b]))
    return out


# ====================================================================== #
# Discriminator -- ordering point at infinity (1D chain, Jc -> inf)
# ====================================================================== #
def discriminate_infjc(J, xi, xi_err):
    """xi(J) for a system with no finite transition (1D chain).
    log xi = logA + p * log J     (power in J,     k=2)
    log xi = logB + c * J         (exponential in J, k=2)
    Equal parameter count -> pure chi^2 (BIC penalty cancels).
    """
    J = np.asarray(J, float); xi = np.asarray(xi, float); xi_err = np.asarray(xi_err, float)
    good = np.isfinite(xi) & (xi > 0) & (J > 0)
    J, xi, xi_err = J[good], xi[good], xi_err[good]
    n = len(xi)
    out = {"n_points": int(n)}
    if n < 4:
        out.update(winner="insufficient", dBIC_E_over_P=float("nan"))
        return out
    logxi = np.log(xi)
    sig = np.maximum(xi_err / xi, 1e-3)
    Xp = np.column_stack([np.ones(n), np.log(J)])
    cp, *_ = np.linalg.lstsq(Xp / sig[:, None], logxi / sig, rcond=None)
    bic_p, chi2_p = _bic(logxi, Xp @ cp, sig, k=2)
    Xe = np.column_stack([np.ones(n), J])
    ce, *_ = np.linalg.lstsq(Xe / sig[:, None], logxi / sig, rcond=None)
    bic_e, chi2_e = _bic(logxi, Xe @ ce, sig, k=2)
    dbic = bic_p - bic_e
    out.update(winner="exp" if dbic > 2.0 else "power",
               dBIC_E_over_P=float(dbic), p_power=float(cp[1]), c_exp=float(ce[1]),
               chi2_power=chi2_p, chi2_exp=chi2_e,
               R2_power=_r2(logxi, Xp @ cp), R2_exp=_r2(logxi, Xe @ ce))
    return out


def discriminate_finite_jcband(J, xi, xi_err, Jc, jc_band, n_jc=7):
    """Run discriminate_finite over a band of Jc values; return the central
    result plus the min/max dBIC and the set of winners (robustness, Stage 3)."""
    centre = discriminate_finite(J, xi, xi_err, Jc)
    jcs = np.linspace(Jc - jc_band, Jc + jc_band, n_jc)
    dbics, winners = [], []
    for jc in jcs:
        if jc <= np.max(J):
            continue
        r = discriminate_finite(J, xi, xi_err, jc)
        if np.isfinite(r.get("dBIC_E_over_P", np.nan)):
            dbics.append(r["dBIC_E_over_P"]); winners.append(r["winner"])
    centre["dBIC_band_min"] = float(np.min(dbics)) if dbics else float("nan")
    centre["dBIC_band_max"] = float(np.max(dbics)) if dbics else float("nan")
    centre["winner_stable"] = bool(len(set(winners)) == 1) if winners else False
    centre["winners_band"] = winners
    return centre


def _r2(y, yhat):
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    return 1.0 - ss_res / ss_tot if ss_tot > 0 else 0.0
