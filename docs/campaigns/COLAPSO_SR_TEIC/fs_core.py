"""fs_core.py -- shared analysis helpers for FS1 (Lindblad) + FS2 (Dyson/RMT).

Pure analysis layer for the COLAPSO_SR_TEIC follow-up campaign. Imports the
already-validated causal-network engines (sr_teic_core, c5_core) and adds ONLY
spectral-analysis observables on top. It implements NO new causal dynamics and
introduces NO tuned parameter (same inviolable rule as sr_teic_core).

FS2 (Dyson/RMT): consecutive level-spacing ratio <r> (Atas et al, PRL 110,
084101, 2013) -- unfolding-free discriminator between Poisson (<r>=0.38629,
integrable, no repulsion) and GOE (<r>=0.5307, chaotic real-symmetric repulsion).

FS1 (Lindblad): the signed BD operator matrix (for CP-channel sign census) and
the coherence-decay rate Gamma_dec(Dx) between two localized spatial modes under
the single-Hermitian-Lindblad dissipator D[rho]=L rho L - 1/2 {L^2,rho}.
"""
from __future__ import annotations

import numpy as np

import sr_teic_core as core          # validated substrate + SR order params
import c5_core as c5                 # validated smeared Sorkin/BD operator

# RMT reference values (fixed a priori in FS_PRE_REGISTRO.md)
R_POISSON = 2.0 * np.log(2.0) - 1.0          # 0.386294...
R_GOE = 0.5307                                # GOE consecutive-ratio mean


# =========================================================================== #
# Operator matrices (real symmetric); BD reconstructed WITH SIGN
# =========================================================================== #
def sym_adjacency(A):
    """Symmetric 0/1 causal adjacency A v A^T (the SR collapse operator)."""
    S = (A | A.T).astype(np.float64)
    np.fill_diagonal(S, 0.0)
    return S


def link_laplacian(A):
    """Combinatorial Laplacian L = D - W of the Hasse-link graph (geometry sector)."""
    Lk = core.hasse_links(A)
    W = (Lk | Lk.T).astype(np.float64)
    np.fill_diagonal(W, 0.0)
    d = W.sum(axis=1)
    return np.diag(d) - W


def bd_matrix(A, eps=c5.EPS_DEFAULT):
    """Signed smeared Sorkin/BD causal d'Alembertian matrix (same construction as
    c5.bd_operator_eigs, but RETURNS THE MATRIX so we can take the signed
    spectrum and Rayleigh quotients). Real symmetric."""
    Af = A.astype(np.float32)
    inter = (Af @ Af).astype(np.float64)        # inter[i,j] = #k with i<k<j
    m = inter + inter.T                          # symmetric interval cardinality
    R = A | A.T
    W = c5.smeared_weight(m, eps)
    M = np.where(R, W, 0.0)
    np.fill_diagonal(M, 0.0)
    np.fill_diagonal(M, -M.sum(axis=1))          # annihilate constants (zero mode)
    return M


# =========================================================================== #
# FS2 -- level-spacing statistics
# =========================================================================== #
def gap_ratios(eigs, edge_frac=0.10, deg_tol=1e-9):
    """Consecutive level-spacing ratios r_n = min(s_n,s_{n-1})/max(...) on the
    BULK spectrum (drop edge_frac fraction from each end).

    Returns (r_values, n_degenerate) where n_degenerate counts bulk spacings
    below deg_tol*spectral_range (exact/near-exact degeneracies; reported
    separately because they bias <r> toward 0 = spurious Poisson).
    """
    ev = np.sort(np.asarray(eigs, dtype=float))
    n = ev.size
    if n < 10:
        return np.array([]), 0
    lo = int(np.floor(edge_frac * n))
    hi = n - lo
    ev = ev[lo:hi]
    s = np.diff(ev)
    rng = ev[-1] - ev[0]
    n_deg = int(np.sum(s < deg_tol * rng)) if rng > 0 else 0
    # ratios use consecutive spacing pairs
    s_safe = s.copy()
    smin = np.minimum(s_safe[1:], s_safe[:-1])
    smax = np.maximum(s_safe[1:], s_safe[:-1])
    ok = smax > 0
    r = smin[ok] / smax[ok]
    return r, n_deg


def classify_r(r_mean):
    """Pre-registered FS2 classification of <r> for the PRIMARY operator."""
    if not np.isfinite(r_mean):
        return "indeterminado"
    if r_mean <= 0.42:
        return "Poisson/integravel (MORTE: sem repulsao)"
    if r_mean >= 0.50:
        return "GOE/RMT (SOBREVIVE: repulsao de Dyson)"
    return "intermediario (semi-Poisson)"


# =========================================================================== #
# FS1 -- Lindblad dissipator observables
# =========================================================================== #
def spatial_mode(pts, sigma, center=None):
    """Normalized Gaussian mode in the SPATIAL coords (not time), width sigma.
    center defaults to the spatial centroid (matches FD2's spatial_mode)."""
    x = pts[:, 1:]
    c = x.mean(axis=0) if center is None else np.asarray(center, float)
    r2 = np.sum((x - c) ** 2, axis=1)
    f = np.exp(-r2 / (2.0 * sigma ** 2))
    nrm = np.sqrt(np.sum(f * f))
    return f / nrm if nrm > 0 else f


def decoherence_rate(M, psi1, psi2):
    """Exact single-Hermitian-Lindblad decoherence rate of the off-diagonal
    coherence rho_12 = |psi1><psi2| under D[rho]=M rho M - 1/2 {M^2, rho} (gamma=1):

        Gamma_dec = 1/2 <psi1|M^2|psi1> + 1/2 <psi2|M^2|psi2> - <psi1|M|psi1><psi2|M|psi2>

    psi1, psi2 assumed (approximately) normalized."""
    Mp1 = M @ psi1
    Mp2 = M @ psi2
    q1 = float(Mp1 @ Mp1)              # <psi1|M^2|psi1> = ||M psi1||^2 (M symmetric)
    q2 = float(Mp2 @ Mp2)
    mu1 = float(psi1 @ Mp1)
    mu2 = float(psi2 @ Mp2)
    return 0.5 * q1 + 0.5 * q2 - mu1 * mu2


def kossakowski_sign_census(eigs, tol_frac=0.01):
    """CP channel-sign census for a Lindblad generator whose channel rates are the
    operator eigenvalues `eigs`. CP <=> all rates >= 0. Returns dict with the most
    negative rate (relative to max |rate|) and a boolean is_CP at tol_frac."""
    ev = np.asarray(eigs, float)
    amax = np.max(np.abs(ev)) if ev.size else 0.0
    if amax == 0:
        return {"min_rate_rel": 0.0, "n_neg": 0, "is_CP": True}
    rel = ev / amax
    n_neg = int(np.sum(rel < -tol_frac))
    return {"min_rate_rel": float(rel.min()), "n_neg": n_neg,
            "is_CP": bool(n_neg == 0)}


def fit_power(x, y):
    """Fit y ~ x^q (log-log), return (q, R2). Uses only y>0 points."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    ok = (y > 0) & (x > 0)
    if ok.sum() < 3:
        return float("nan"), float("nan")
    lx, ly = np.log(x[ok]), np.log(y[ok])
    b = np.polyfit(lx, ly, 1)
    pred = b[0] * lx + b[1]
    ss_res = np.sum((ly - pred) ** 2)
    ss_tot = np.sum((ly - ly.mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0
    return float(b[0]), float(r2)
