"""e2_core.py -- BD-smeared causal-set wave propagation + S(k,omega) estimator.

DATA GENERATOR for the E2_MAGNON_BD campaign (NIVEL4_ORIENTATION, entry FN2).
Contains NO relativistic dispersion formula: the words 'photon'/'magnon' and the
relation omega=ck live ONLY in the synthesis (COMPARISON ONLY).  This module
knows:

  * how to sprinkle a 1+1D Poisson causal set (cols [t, x]) and build its strict
    causal order matrix C (reusing src/causal_core.py);
  * the SMEARED Sorkin / Benincasa-Dowker d'Alembertian B_eps (the *exact* e10
    definition -- imported, not re-derived: w(m) = binomial-thinning weight);
  * the BD DISPERSION SYMBOL.  How the dispersion is actually measured: we do NOT
    invert B_eps to propagate (that retarded recursion phi(x)=2eps sum w(m)phi(y)
    is numerically UNSTABLE -- it compounds the documented BD pointwise variance;
    the constant zero-mode is not preserved and the field blows up.  bd_propagate
    below is kept only to DEMONSTRATE that instability).  Instead we read the
    dispersion off the operator's symbol, exactly the sign-robust content e10
    validated: feed a real probe wave  phi = cos(k x - omega t)  and measure the
    BD eigenvalue  lambda(k,omega) = <phi, B_eps phi> / <phi,phi>  by regression
    over bulk events.  In the continuum B_eps -> box = d_t^2 - d_x^2, whose symbol
    on cos(kx-wt) is (k^2 - omega^2): lambda > 0 below the light cone (omega<k),
    lambda < 0 above it (omega>k), and the ON-SHELL dispersion omega*(k) is the
    ZERO CROSSING.  e10's T2 already verified the two anchors (lambda_space=+k^2>0
    at omega=0, lambda_time=-omega^2<0 at k=0); E2 scans the full (k,omega) plane
    and locates the zero ridge.  THE CAUSAL ORDER IS TIME and the light cone is
    geometry -- but no dispersion law is inserted; omega is scanned freely and the
    operator decides where it vanishes.
  * the structure factor  S(k,omega) = |sum_i phi_i e^{-i k x_i + i omega t_i}|^2/N
    by DIRECT non-uniform DFT (real cos/sin sums -- same estimator style as
    orientation_core.structure_factor), peak finding omega*(k), and a three-model
    dispersion fit (massless ck / massive KG / diffusive Dk^2) by chi^2/AIC.

ANTI-CIRCULARITY.  c does NOT enter the generator.  The Minkowski light cone
(slope 1) is the *geometry* of any causal set (the relation dt^2 > dx^2 is how a
sprinkle is defined), but no dispersion law omega=ck is inserted anywhere.  The
DISCRIMINATOR is the SHAPE of omega*(k) (linear vs quadratic vs gapped), which is
not circular; c_fit is a free parameter, compared to 1 only in the synthesis.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from causal_core import sprinkle_box, causal_matrix          # noqa: E402
from e10_sorkin_dalembertian import smeared_weight           # noqa: E402  (Sorkin/BD def.)


# ====================================================================== #
# Causal set (1+1D) and its strict order
# ====================================================================== #
def sprinkle_1plus1(rho, T, X, seed):
    """Poisson sprinkle in [0,T] x [-X,X].  Returns pts (n,2), cols [t, x]."""
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, T), (-X, X)], rng)
    # order by time for deterministic sweeps / reproducibility
    pts = pts[np.argsort(pts[:, 0], kind="stable")]
    return pts


def order_matrix(pts):
    """Strict causal order C[i,j] = (i precedes j) for a (n,2) [t,x] set."""
    return causal_matrix(pts)


# ====================================================================== #
# RETARDED BD-smeared propagation:  B_eps[phi] = 0  ->  phi(x)=2eps sum w(m) phi(y)
# ====================================================================== #
def bd_propagate(pts, C, phi_init, init_mask, eps):
    """Propagate a scalar field on the causal set by the retarded BD recursion.

    Parameters
    ----------
    pts       : (n,2) event coords [t,x] (any order; C must match the same order)
    C         : (n,n) bool strict order, C[i,j]=(i precedes j)
    phi_init  : (n,) initial field; values on init_mask are held fixed (the
                characteristic/initial data), the rest are overwritten.
    init_mask : (n,) bool; True = held initial event.
    eps       : smearing retention (e10/Sorkin).

    Returns phi (n,) with the held data on init_mask and the retarded solution
    elsewhere.  Sweep order = increasing t so every ancestor is already set.
    """
    n = pts.shape[0]
    phi = np.array(phi_init, dtype=float, copy=True)
    order = np.argsort(pts[:, 0], kind="stable")
    Cb = C  # bool
    for x in order:
        if init_mask[x]:
            continue
        P = np.nonzero(Cb[:, x])[0]          # ancestors y < x
        if P.size == 0:
            phi[x] = 0.0
            continue
        # m_y = #events strictly between y and x = #{z in P : y < z}
        sub = Cb[np.ix_(P, P)]               # sub[a,b] = P[a] precedes P[b]
        m = sub.sum(axis=1).astype(float)
        w = smeared_weight(m, eps)
        phi[x] = 2.0 * eps * float(w @ phi[P])
    return phi


# ====================================================================== #
# BD operator as a precomputed sparse linear map (stable; the symbol route)
# ====================================================================== #
def bulk_events(pts, t_frac=(0.25, 0.75), x_frac=0.6, max_n=160, seed=0):
    """Pick interior events whose causal past is well inside the box (so B_eps is
    not truncated by the boundary).  Returns an index array."""
    t, x = pts[:, 0], pts[:, 1]
    T, X = t.max(), np.abs(x).max()
    sel = (t > t_frac[0] * T) & (t < t_frac[1] * T) & (np.abs(x) < x_frac * X)
    idx = np.nonzero(sel)[0]
    if idx.size > max_n:
        rng = np.random.default_rng(seed)
        idx = np.sort(rng.choice(idx, max_n, replace=False))
    return idx


def precompute_bd_operator(pts, C, mids, eps):
    """For each bulk event xi, precompute (P, W) so that
        B_eps[phi](xi) = -phi[xi] + sum_k W_k phi[P_k],   W_k = 2 eps w(m_k).
    The past P and the smeared weights W depend only on the causal set, NOT on the
    probe field, so the (k,omega) scan reuses them.  Returns list of (P, W)."""
    ops = []
    for xi in mids:
        P = np.nonzero(C[:, xi])[0]
        if P.size == 0:
            ops.append((P, np.zeros(0)))
            continue
        m = C[np.ix_(P, P)].sum(axis=1).astype(float)
        W = 2.0 * eps * smeared_weight(m, eps)
        ops.append((P, W))
    return ops


def bd_apply(phi, ops, mids):
    """Apply the precomputed B_eps to field phi at the bulk events.  Returns B (len
    mids): B_a = -phi[mids[a]] + sum_k W_k phi[P_k]."""
    B = np.empty(len(mids))
    for a, xi in enumerate(mids):
        P, W = ops[a]
        B[a] = -phi[xi] + (float(W @ phi[P]) if P.size else 0.0)
    return B


def symbol_lambda(pts, ops, mids, k, omega):
    """BD eigenvalue lambda(k,omega) = <f, B_eps f>/<f,f> for the real probe wave
    f = cos(k x - omega t), regressed over bulk events.  Anti-circular: f is real
    (no complex literal), omega is a free scan coordinate."""
    f = np.cos(k * pts[:, 1] - omega * pts[:, 0])
    B = bd_apply(f, ops, mids)
    fm = f[mids]
    d = float(fm @ fm)
    return float(fm @ B / d) if d > 0 else float("nan")


def symbol_grid(pts, ops, mids, kmags, omegas):
    """lambda(k,omega) over the full grid, vectorised over omega for speed.

    For fixed k, build phi(event, omega) = cos(k x - omega t) once, then
    lambda(k,omega) = <phi_mids, B_eps phi>_omega / <phi_mids, phi_mids>_omega.
    Returns L (len k, len omega)."""
    t = pts[:, 0]
    x = pts[:, 1]
    omegas = np.asarray(omegas, float)
    mids = np.asarray(mids)
    L = np.empty((len(kmags), len(omegas)))
    for ik, k in enumerate(kmags):
        # phi[event, w] = cos(k x_event - w t_event)
        phi = np.cos(k * x[:, None] - omegas[None, :] * t[:, None])   # (n, W)
        fm = phi[mids]                                                # (M, W)
        # B_eps phi at each bulk event, vectorised over omega
        B = -fm.copy()                                                # -phi(xi)
        for a, xi in enumerate(mids):
            P, W = ops[a]
            if P.size:
                B[a] += W @ phi[P]                                    # (W,)
        num = np.sum(fm * B, axis=0)                                  # (W,)
        den = np.sum(fm * fm, axis=0)
        L[ik] = np.where(den > 0, num / den, np.nan)
    return L


def dispersion_from_symbol(kmags, omegas, L):
    """omega*(k) = on-shell zero crossing of the symbol lambda(k,omega) in omega.

    The continuum symbol is proportional to (k^2 - omega^2) up to an overall
    NORMALIZATION CONSTANT whose sign the smeared operator does not fix (e10 only
    pinned down sign-ORDERING, not absolute sign; measured here the operator
    behaves as ~ -(k^2-omega^2), i.e. spacelike region omega<k has one sign and
    timelike omega>k the other).  Either way the ON-SHELL dispersion is the FIRST
    zero crossing in omega -- from the spacelike sign (small omega) to its
    opposite.  We detect the spacelike sign from the smallest-omega samples and
    find the first crossing to the opposite sign.  Normalization-independent and
    therefore not circular.  Returns omega_star and a boolean 'found' per k."""
    ostar = np.full(len(kmags), np.nan)
    found = np.zeros(len(kmags), dtype=bool)
    for ik in range(len(kmags)):
        lam = L[ik]
        # spacelike sign = sign of the mean over the lowest-omega third (omega<k)
        n_lo = max(2, len(omegas) // 4)
        s0 = np.sign(np.mean(lam[:n_lo]))
        if s0 == 0:
            s0 = np.sign(lam[0]) if lam[0] != 0 else 1.0
        for j in range(len(omegas) - 1):
            # crossing from spacelike sign s0 to opposite sign
            if np.sign(lam[j]) == s0 and np.sign(lam[j + 1]) == -s0:
                w0, w1 = omegas[j], omegas[j + 1]
                l0, l1 = lam[j], lam[j + 1]
                ostar[ik] = w0 + (w1 - w0) * abs(l0) / (abs(l0) + abs(l1))
                found[ik] = True
                break
    return ostar, found


def gaussian_seed(pts, t_seed, sigma_x, amp=1.0, x0=0.0):
    """Initial data: a static x-Gaussian on the early time slab t<=t_seed.

    Returns (phi_init, init_mask).  A time-static Gaussian slab has box phi =
    -d_x^2(gauss) != 0, so it sources outgoing waves -- no dispersion law assumed.
    """
    t, x = pts[:, 0], pts[:, 1]
    init_mask = t <= t_seed
    phi_init = np.zeros(pts.shape[0])
    phi_init[init_mask] = amp * np.exp(-0.5 * ((x[init_mask] - x0) / sigma_x) ** 2)
    return phi_init, init_mask


def detrend_envelope(pts, phi, n_tbins=20):
    """Divide out a global exponential growth/decay envelope in time.

    Fits log(RMS phi) linear in t over time bins and divides phi by exp(fit).
    Removes the overall amplitude trend so the oscillatory dispersion is visible;
    it multiplies each event by a t-only positive factor and so does NOT move the
    spectral peak omega*(k).  Returns (phi_detrended, growth_rate per unit t).
    """
    t = pts[:, 0]
    edges = np.linspace(t.min(), t.max(), n_tbins + 1)
    ctr, rms = [], []
    for a, b in zip(edges[:-1], edges[1:]):
        sel = (t >= a) & (t < b)
        if sel.sum() > 5:
            r = np.sqrt(np.mean(phi[sel] ** 2))
            if r > 0:
                ctr.append(0.5 * (a + b))
                rms.append(r)
    if len(ctr) < 3:
        return phi.copy(), 0.0
    ctr, rms = np.array(ctr), np.array(rms)
    sl, ic = np.polyfit(ctr, np.log(rms), 1)
    env = np.exp(ic + sl * t)
    env = np.where(env > 0, env, 1.0)
    return phi / env, float(sl)


# ====================================================================== #
# S(k, omega) by direct non-uniform DFT  (real cos/sin sums)
# ====================================================================== #
def structure_factor_kw(pts, phi, kmags, omegas):
    """S(k,omega) = |sum_i phi_i e^{-i k x_i + i omega t_i}|^2 / N.

    Returns S (len(kmags), len(omegas)).  Real arithmetic, no complex literals
    in the generator (anti-circularity).
    """
    t, x = pts[:, 0], pts[:, 1]
    N = pts.shape[0]
    S = np.empty((len(kmags), len(omegas)))
    for ik, k in enumerate(kmags):
        kx = k * x                                   # (N,)
        # phase = omega*t - k*x  -> outer over omega
        wt = np.outer(omegas, t)                     # (W,N)
        ph = wt - kx[None, :]
        re = np.cos(ph) @ phi                         # (W,)
        im = np.sin(ph) @ phi
        S[ik] = (re ** 2 + im ** 2) / N
    return S


def peak_dispersion(kmags, omegas, S, omega_floor=1e-9):
    """For each k, omega*(k) = argmax_{omega>0} S(k,omega).  Returns omega_star,
    peak_height, and a coarse half-width (for weighting)."""
    pos = omegas > omega_floor
    om = omegas[pos]
    ostar = np.empty(len(kmags))
    height = np.empty(len(kmags))
    width = np.empty(len(kmags))
    for ik in range(len(kmags)):
        s = S[ik, pos]
        j = int(np.argmax(s))
        ostar[ik] = om[j]
        height[ik] = s[j]
        half = 0.5 * s[j]
        above = s >= half
        if above.sum() > 1:
            idx = np.nonzero(above)[0]
            width[ik] = om[idx[-1]] - om[idx[0]]
        else:
            width[ik] = om[1] - om[0] if om.size > 1 else 0.0
    return ostar, height, width


# ====================================================================== #
# Three-model dispersion fit (massless ck / massive KG / diffusive Dk^2)
# ====================================================================== #
def _chi2(y, yhat, sigma):
    return float(np.sum(((y - yhat) / sigma) ** 2))


def fit_dispersion(k, omega_star, sigma=None):
    """Fit omega*(k) to three models and pick by AIC = chi^2 + 2 n_params.

    massless : omega = c k                 (1 param, c free)        -> photon
    massive  : omega = sqrt(c^2 k^2 + m^2) (2 params)               -> Klein-Gordon
    diffusive: omega = D k^2               (1 param)                -> magnon

    Anti-circularity: c is a FREE parameter (not fixed to 1); the value is only
    compared to the light-cone speed in the synthesis.  Returns dict with each
    model's params, chi^2, AIC, plus the winner and the linear relative deviation.
    """
    k = np.asarray(k, float)
    y = np.asarray(omega_star, float)
    if sigma is None:
        sigma = np.full_like(y, max(np.std(y) * 0.1, 1e-3))
    sigma = np.asarray(sigma, float)
    sigma = np.where(sigma > 0, sigma, np.median(sigma[sigma > 0]) if np.any(sigma > 0) else 1.0)

    out = {}

    # ---- massless: omega = c k  (least squares through origin) ----
    c_ls = float(np.sum(k * y / sigma ** 2) / np.sum(k ** 2 / sigma ** 2))
    yhat = c_ls * k
    chi2_m = _chi2(y, yhat, sigma)
    out["massless"] = {"c": c_ls, "chi2": chi2_m, "n_params": 1,
                       "aic": chi2_m + 2 * 1}

    # ---- diffusive: omega = D k^2 ----
    D_ls = float(np.sum(k ** 2 * y / sigma ** 2) / np.sum(k ** 4 / sigma ** 2))
    yhat = D_ls * k ** 2
    chi2_d = _chi2(y, yhat, sigma)
    out["diffusive"] = {"D": D_ls, "chi2": chi2_d, "n_params": 1,
                        "aic": chi2_d + 2 * 1}

    # ---- massive KG: omega^2 = c^2 k^2 + m^2  (linear in k^2, weighted) ----
    # fit Y=omega^2 vs Xk=k^2 ; weights from error propagation sigma_Y=2 omega sigma
    Y = y ** 2
    Xk = k ** 2
    sY = 2.0 * np.abs(y) * sigma + 1e-12
    wv = 1.0 / sY ** 2
    A = np.vstack([Xk, np.ones_like(Xk)]).T
    W = np.diag(wv)
    try:
        coef = np.linalg.solve(A.T @ W @ A, A.T @ W @ Y)
        c2, m2 = float(coef[0]), float(coef[1])
    except np.linalg.LinAlgError:
        c2, m2 = c_ls ** 2, 0.0
    c2 = max(c2, 1e-9)
    yhat = np.sqrt(np.maximum(c2 * k ** 2 + m2, 0.0))
    chi2_kg = _chi2(y, yhat, sigma)
    out["massive"] = {"c": float(np.sqrt(c2)), "m2": m2, "m": float(np.sqrt(m2)) if m2 > 0 else 0.0,
                      "chi2": chi2_kg, "n_params": 2, "aic": chi2_kg + 2 * 2}

    # ---- winner by a scale-free, sigma-independent discriminator ----
    # The phase velocity v(k)=omega/k has a model-distinguishing TREND in k:
    #   massless : v = c           (flat)
    #   diffusive: v = D k         (rises with k)
    #   massive  : v = sqrt(c^2+m^2/k^2)  (falls with k, diverges as k->0)
    # The sign+size of the relative slope of v(k) classifies the law without any
    # assumed noise level (the AIC race above is kept only as diagnostic info).
    v = y / k
    # weighted linear fit v = a + b k
    bcoef = np.polyfit(k, v, 1)
    b, a = float(bcoef[0]), float(bcoef[1])
    k_mid = float(np.median(k))
    v_mid = a + b * k_mid
    rel_slope = b * k_mid / v_mid if abs(v_mid) > 1e-9 else 0.0
    out["v_rel_slope"] = float(rel_slope)
    THRESH = 0.15
    if rel_slope > THRESH:
        winner = "diffusive"
    elif rel_slope < -THRESH:
        winner = "massive"
    else:
        winner = "massless"
    out["winner"] = winner
    out["winner_aic"] = min(["massless", "diffusive", "massive"],
                            key=lambda nm: out[nm]["aic"])

    # linear relative deviation: RMS residual of the massless fit / RMS(omega)
    res = y - c_ls * k
    rel = float(np.sqrt(np.mean(res ** 2)) / (np.sqrt(np.mean(y ** 2)) + 1e-12))
    out["linear_rel_deviation"] = rel
    out["linear_rel_deviation_pct"] = 100.0 * rel
    return out


# ====================================================================== #
# Seed-averaged symbol dispersion (shared by the gate, E2-1 and E2-2)
# ====================================================================== #
def measure_symbol_dispersion(rho, T, X, eps, kmags, omegas, n_seeds, max_n=120,
                              seed0=0, verbose=False):
    """Seed-averaged BD symbol lambda(k,omega) and its zero-crossing dispersion.

    Returns dict with the averaged grid L, the dispersion omega*(k) from the
    averaged grid, the per-seed omega*(k) stack (for error bars / E2-2), the SEM,
    and the number of seeds actually used.  This is the SOLE physics estimator of
    E2: it measures the causal-set wave operator's symbol on real Poisson sets and
    locates the on-shell zero ridge.  c is never inserted; omega is scanned."""
    Lacc = np.zeros((len(kmags), len(omegas)))
    per_seed = []
    used = 0
    for s in range(n_seeds):
        pts = sprinkle_1plus1(rho, T, X, seed0 + s)
        C = order_matrix(pts)
        mids = bulk_events(pts, max_n=max_n, seed=seed0 + s)
        if mids.size < 8:
            continue
        ops = precompute_bd_operator(pts, C, mids, eps)
        L = symbol_grid(pts, ops, mids, kmags, omegas)
        Lacc += L
        ostar_s, _ = dispersion_from_symbol(kmags, omegas, L)
        per_seed.append(ostar_s)
        used += 1
        if verbose:
            print(f"     seed {seed0+s}: n={pts.shape[0]} mids={mids.size}", flush=True)
    L = Lacc / max(used, 1)
    ostar, found = dispersion_from_symbol(kmags, omegas, L)
    per_seed = np.array(per_seed)                       # (used, n_k)
    with np.errstate(invalid="ignore"):
        sem = np.nanstd(per_seed, axis=0) / np.sqrt(max(used, 1))
    return {"k": np.asarray(kmags), "omega": np.asarray(omegas), "L": L,
            "omega_star": ostar, "found": found, "per_seed": per_seed,
            "sem": sem, "n_seeds_used": used}


# ====================================================================== #
# Synthetic plane-wave field (estimator validation, COMPARISON ONLY input)
# ====================================================================== #
def synthetic_field(pts, kmags, disp_fn, amp=1.0):
    """phi_i = sum_k amp * cos(k x_i - disp_fn(k) t_i).  Used ONLY to validate the
    S(k,omega) estimator+fit against a KNOWN dispersion (the dispersion is the
    input, not produced by the network).  Labelled COMPARISON ONLY at call site."""
    t, x = pts[:, 0], pts[:, 1]
    phi = np.zeros(pts.shape[0])
    for k in kmags:
        w = disp_fn(k)
        phi += amp * np.cos(k * x - w * t)
    return phi


# ====================================================================== #
# default k / omega grids from the box
# ====================================================================== #
def default_grids(T, X, rho, n_k=14, n_omega=140):
    kmin = 2 * np.pi / (2 * X)
    kmax = np.pi * np.sqrt(rho)               # ~ spatial Nyquist of the sprinkle
    kmags = np.linspace(kmin, 0.6 * kmax, n_k)
    omega_max = np.pi * np.sqrt(rho)
    omegas = np.linspace(0.0, omega_max, n_omega)
    return kmags, omegas


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("e2_core self-test")
    pts = sprinkle_1plus1(rho=6.0, T=16.0, X=8.0, seed=0)
    print(f"  n={pts.shape[0]} events")
    C = order_matrix(pts)
    # constant field must be (approximately) preserved by the recursion: a
    # constant is a zero mode of box, so phi(x)=2eps sum w(m) -> 1 on average.
    eps = 0.2
    init_mask = pts[:, 0] <= 3.0
    phi_const = np.ones(pts.shape[0])
    phi = bd_propagate(pts, C, phi_const, init_mask, eps)
    bulk = ~init_mask & (pts[:, 0] > pts[:, 0].max() * 0.3) & (pts[:, 0] < pts[:, 0].max() * 0.7)
    print(f"  recursion constant-mode: <phi_bulk>={phi[bulk].mean():+.3f} "
          "(UNSTABLE by design -- the retarded recursion is the e10 BD-variance "
          "pathology; E2 uses the symbol route instead, see E2-V B1)")
    # estimator sanity on a known linear dispersion (S(k,omega) route)
    kk, ww = default_grids(16.0, 8.0, 6.0)
    f = synthetic_field(pts, kk, lambda k: 1.0 * k)          # COMPARISON ONLY input
    S = structure_factor_kw(pts, f, kk, ww)
    ostar, h, wd = peak_dispersion(kk, ww, S)
    fit = fit_dispersion(kk, ostar)
    print(f"  S(k,w) estimator on omega=1.0*k: winner={fit['winner']} "
          f"c_fit={fit['massless']['c']:.3f} dev={fit['linear_rel_deviation_pct']:.1f}%")
    # BD symbol route: lambda(k,omega) zero crossing on the real causal set
    mids = bulk_events(pts)
    ops = precompute_bd_operator(pts, C, mids, eps)
    # measured B_eps ~ -(k^2-omega^2): spacelike (omega<k) and timelike (omega>k)
    # have OPPOSITE signs; the zero crossing (the dispersion) is sign-independent.
    print(f"  symbol anchors: lambda(k=0.8,w=0)={symbol_lambda(pts,ops,mids,0.8,0.0):+.3f} (spacelike)"
          f"  lambda(k=0,w=0.8)={symbol_lambda(pts,ops,mids,0.0,0.8):+.3f} (timelike; opposite sign)")
    Ls = symbol_grid(pts, ops, mids, kk, ww)
    od, fnd = dispersion_from_symbol(kk, ww, Ls)
    if fnd.sum() >= 3:
        sfit = fit_dispersion(kk[fnd], od[fnd])
        print(f"  symbol dispersion: winner={sfit['winner']} c_fit={sfit['massless']['c']:.3f} "
              f"dev={sfit['linear_rel_deviation_pct']:.1f}% ({fnd.sum()}/{len(kk)} k found)")
    print("self-test done")
