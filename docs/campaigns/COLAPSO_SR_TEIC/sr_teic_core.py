"""sr_teic_core.py -- shared engine for CAMPANHA_COLAPSO_SR_TEIC.

Tests whether the SR collapse mechanism (saturation of chi_eff = lambda_max/N,
arrow of time, threshold eta) EMERGES from TEIC's already-validated causal
network, or must be INSERTED externally.

INVIOLABLE RULE (TEIC/DEV standard): it must ARISE, not be PLACED. No new tuned
parameter may be introduced to manufacture collapse. This module therefore
REUSES the validated substrate engines and only ADDS the SR-faithful spectral
order parameters on top -- it implements no new causal dynamics.

Reused (unmodified) validated engines:
  * tier3_core.sprinkle_diamond     -- Poisson sprinkling in the unit causal
                                       diamond of M^d (the CST substrate).
  * tier3_core.causal_matrix_anc    -- ancestor (causal order) matrix.
  * c5_core.bd_operator_eigs        -- smeared Sorkin/Benincasa-Dowker causal
                                       d'Alembertian spectrum (validated in e10/C5).

SR-faithful definitions (SR_v7_full-38.pdf, Zambuzi):
  * chi_eff = lambda_max(A)/N, A = SYMMETRIC adjacency  (Eq. 9, Listing 2)
              -- the COLLAPSE-sector operator. Measures relational concentration
                 / global spectral dominance, NOT density (Remark 3).
  * chi_L   = lambda_max(L)/N, L = combinatorial Laplacian of the Hasse links
              -- the GEOMETRY-sector operator (d_s).
  * R       = (lambda_max - lambda_2)/lambda_max  -- spectral rigidity; SR states
              "collapse is loss of spectral rigidity, not fragmentation" (Eq. 170).

NO eta, NO pruning rate, NO arrow direction is injected anywhere in this module.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# --- locate and import the validated TEIC engines (no reimplementation) ------ #
HERE = Path(__file__).resolve().parent
# repo root = .../003-TEORIAS ; TEIC tree underneath
ROOT = HERE
for _ in range(6):
    if (ROOT / "TEIC" / "src" / "causal_core.py").exists():
        break
    ROOT = ROOT.parent
TEIC = ROOT / "TEIC"
sys.path.insert(0, str(TEIC / "src"))
sys.path.insert(0, str(TEIC / "results" / "tier3"))
sys.path.insert(0, str(TEIC / "results" / "foundations" / "c5"))

import tier3_core as t3          # noqa: E402  sprinkle_diamond, causal_matrix_anc
import c5_core as c5             # noqa: E402  bd_operator_eigs (validated BD operator)


# =========================================================================== #
# Substrate (reused) : sprinkle a Poisson causal set, build causal structures
# =========================================================================== #
def sprinkle(n, dim, rng):
    """n Poisson events in the unit causal diamond of M^dim (tier3_core)."""
    return t3.sprinkle_diamond(n, dim, rng)


def ancestor_matrix(pts):
    """A[i,j] = True iff j strictly precedes i (Minkowski light cones)."""
    return t3.causal_matrix_anc(pts)


def hasse_links(A):
    """Covering relations (irreducible links) of the causal order given the
    ancestor matrix A (A[i,j] = j < i). i covers j iff j<i and there is no k with
    j<k<i. Returns a boolean link matrix Lk[i,j] = (i covers j)."""
    Af = A.astype(np.float32)
    two_step = (Af @ Af) > 0.5          # two_step[i,j] = exists k: j<k<i
    return A & ~two_step


# =========================================================================== #
# SR-faithful spectral order parameters (ADDED on top; nothing tuned)
# =========================================================================== #
def _sym_adjacency(A):
    """Symmetric 0/1 adjacency of the causal relation A v A^T (undirected)."""
    S = (A | A.T).astype(np.float64)
    np.fill_diagonal(S, 0.0)
    return S


def _laplacian(W):
    """Combinatorial Laplacian L = D - W of a symmetric weight matrix W."""
    d = W.sum(axis=1)
    return np.diag(d) - W


def chi_adjacency(A):
    """SR collapse order parameter chi_A = lambda_max(A_sym)/N (Eq. 9, Listing 2).
    Returns (chi_A, rigidity R, lambda_max, lambda_2)."""
    S = _sym_adjacency(A)
    n = S.shape[0]
    if n < 2:
        return 0.0, 0.0, 0.0, 0.0
    ev = np.linalg.eigvalsh(S)          # ascending
    lmax, l2 = float(ev[-1]), float(ev[-2])
    chi = lmax / n
    R = (lmax - l2) / lmax if lmax > 0 else 0.0
    return chi, R, lmax, l2


def chi_laplacian_links(A):
    """Geometry-sector order parameter chi_L = lambda_max(L_link)/N, L = Laplacian
    of the Hasse-link graph. Returns (chi_L, lambda_max)."""
    Lk = hasse_links(A)
    W = (Lk | Lk.T).astype(np.float64)
    np.fill_diagonal(W, 0.0)
    n = W.shape[0]
    if n < 2 or W.sum() == 0:
        return 0.0, 0.0
    L = _laplacian(W)
    ev = np.linalg.eigvalsh(L)
    lmax = float(ev[-1])
    return lmax / n, lmax


def chi_bd(A, eps=c5.EPS_DEFAULT):
    """Causal-d'Alembertian order parameter chi_BD = lambda_max(|M_BD|)/N using the
    VALIDATED smeared Sorkin/BD operator (c5_core). Returns (chi_BD, lambda_max)."""
    eigs = c5.bd_operator_eigs(A, eps=eps)   # |eigenvalues|, validated engine
    n = A.shape[0]
    lmax = float(np.max(eigs)) if eigs.size else 0.0
    return lmax / n, lmax


def spectral_entropy(A):
    """Structural entropy S = -sum p_i ln p_i of the normalised adjacency spectrum
    p_i = lambda_i / sum lambda_i (lambda_i >= 0 after shift). A proxy for the
    relational disorder of the causal order at a given size."""
    S = _sym_adjacency(A)
    ev = np.linalg.eigvalsh(S)
    ev = ev - ev.min()                  # shift to non-negative
    tot = ev.sum()
    if tot <= 0:
        return 0.0
    p = ev / tot
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))


# =========================================================================== #
# Growth in causal (Hasse) time order : the "evolution under causal dynamics"
# =========================================================================== #
def hasse_time_order(pts):
    """Indices sorting events by their time coordinate = a linear extension of the
    Hasse partial order (sequential causal growth, CST classical-sequential-growth
    style). Past-to-future."""
    return np.argsort(pts[:, 0], kind="stable")


def growth_trajectory(pts, fracs, eps=c5.EPS_DEFAULT, reverse=False):
    """Grow the causet by adding events in Hasse time order and measure the SR
    order parameters at each prefix.

    reverse=False : add earliest events first (past -> future, the physical arrow).
    reverse=True  : add latest events first (future -> past, time-reversed run).

    Returns dict of arrays keyed by 'n','chi_A','R','chi_L','chi_BD','S'.
    """
    order = hasse_time_order(pts)
    if reverse:
        order = order[::-1]
    A_full = ancestor_matrix(pts)
    N = len(pts)
    out = {k: [] for k in ("n", "chi_A", "R", "chi_L", "chi_BD", "S")}
    for f in fracs:
        n = max(4, int(round(f * N)))
        idx = order[:n]
        sub = np.ix_(idx, idx)
        A = A_full[sub]
        chiA, R, _, _ = chi_adjacency(A)
        chiL, _ = chi_laplacian_links(A)
        chiBD, _ = chi_bd(A, eps=eps)
        out["n"].append(n)
        out["chi_A"].append(chiA)
        out["R"].append(R)
        out["chi_L"].append(chiL)
        out["chi_BD"].append(chiBD)
        out["S"].append(spectral_entropy(A))
    return {k: np.array(v, dtype=float) for k, v in out.items()}


# =========================================================================== #
# Plateau test (pre-registered, EXP 1)
# =========================================================================== #
def plateau_test(n, chi, N, tail_frac=0.6, drift_tol=0.10, floor_mult=2.0):
    """Pre-registered saturation test for one order parameter trajectory chi(n).

    Returns dict with the tail drift, the plateau value, and booleans for the
    three pre-registered conditions (tail drift < drift_tol; chi_plateau > 2/N).
    N-stability across scales is checked separately by the caller.
    """
    n = np.asarray(n, float); chi = np.asarray(chi, float)
    tail = n >= tail_frac * N
    if tail.sum() < 2:
        tail = n >= 0.5 * N
    chi_tail = chi[tail]
    chi_lo = float(chi_tail[0]); chi_hi = float(chi_tail[-1])
    plateau = float(np.mean(chi_tail))
    drift = abs(chi_hi - chi_lo) / chi_lo if chi_lo > 1e-12 else np.inf
    floor = floor_mult / N
    return {
        "plateau": plateau,
        "tail_drift": drift,
        "drift_ok": bool(drift < drift_tol),
        "above_floor": bool(plateau > floor),
        "floor": floor,
    }
