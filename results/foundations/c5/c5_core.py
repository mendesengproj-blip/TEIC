"""c5_core.py -- shared engine for the C5 SPECTRAL DIMENSION campaign.

Question (C5_SPECTRAL_DIMENSION.md): does the Poisson causal network have a
RUNNING spectral dimension D_s(sigma) -- D_s varying with the diffusion scale
sigma -- analogous to Causal Dynamical Triangulations (D_s: 4 -> 2 in the UV)?

Spectral dimension is the standard diffusion probe:
    K(sigma) = (1/N) sum_i exp(-sigma lambda_i)        (avg return probability)
    D_s(sigma) = -2 d log K / d log sigma .
A smooth d-dim space has D_s = d at all scales.  A running D_s is the
fingerprint of scale-dependent geometry.

ENGINE CHOICE (decided empirically by the C5-V gate, _proto_engines.py):
  The naive undirected graph Laplacian of the causal LINKS (covering relations)
  does NOT reproduce the Myrheim-Meyer dimension at large scale -- the link
  graph is non-local in space (links spread along the light cone), giving a
  small-world / fragmented graph whose D_s overshoots (d=2: ~6) or fragments
  (d=4).  Per the gate protocol ("se nao bater, corrigir o motor"), the engine
  is the CAUSAL d'Alembertian instead: the smeared Sorkin / Benincasa-Dowker
  operator already implemented and validated in e10 (annihilates constants,
  recovers box in the mean).  Its LOCALITY (the smeared weight w(m) decays in
  the order-interval cardinality m) is exactly what makes its continuum limit
  the LOCAL Laplacian, hence reproduces the manifold dimension.

  We build the SYMMETRIC, EUCLIDEANISED operator
      M[i,j] = w(m_ij)            for i,j causally related (either cone)
      M[i,i] = -sum_j M[i,j]      (annihilates constants -> zero mode = IR)
  with w the e10 smeared weight, m_ij the order-interval cardinality, and use
  |eigenvalues| as a POSITIVE diffusion generator (the Lorentzian box is not
  bounded below; the Euclidean continuation -> a heat kernel).  This is an
  explicit methodological choice, stated as such; D_s is invariant under an
  overall rescaling of the spectrum, so the operator normalisation is irrelevant.

ANTI-CIRCULARITY: no hbar, no Planck scale, no relativistic dilation, no complex
numbers anywhere in this engine.  The smeared weight w(m) and the layer
structure are the DEFINITION of the Sorkin/BD operator (cited in e10), not an
ad hoc fit.  hbar appears ONLY in C5-3, as a structural comparison, never in the
generator.  The MM dimension target enters only in the gate / verdict code.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "tier3"))

import tier3_core as t3   # noqa: E402  sprinkle_diamond, causal_matrix_anc, MM dim

EPS_DEFAULT = 0.25        # smearing retention (e10 used 0.2; 0.25 here -- both
                          # in the validated regime; locality scale ~ 1/eps ticks)


# --------------------------------------------------------------------------- #
# Sprinkling + causal structure (reuse tier3_core / causal_core substrate)
# --------------------------------------------------------------------------- #
def sprinkle(n, dim, rng):
    """n Poisson events in the unit causal diamond of M^dim (tier3_core)."""
    return t3.sprinkle_diamond(n, dim, rng)


def ancestor_matrix(pts):
    """A[i,j] = True iff j strictly precedes i (Minkowski light cones)."""
    return t3.causal_matrix_anc(pts)


def mm_dimension(A, n):
    """Myrheim-Meyer spacetime dimension from the global ordering fraction
    (the R1/R2 estimator, via tier3_core)."""
    return t3.mm_global(A, n)


# --------------------------------------------------------------------------- #
# The causal-d'Alembertian diffusion operator (smeared Sorkin/BD, e10)
# --------------------------------------------------------------------------- #
def smeared_weight(m, eps):
    """e10 smeared Sorkin weight for an order-interval of cardinality m:
        w(m) = (1-eps)^m - 2 m eps (1-eps)^(m-1) + C(m,2) eps^2 (1-eps)^(m-2).
    Alternates sign (>0 near m=0, <0 at intermediate m) and DECAYS in m -- the
    decay is the operator's locality.  Vectorised over an integer array m."""
    m = np.asarray(m, dtype=float)
    return ((1 - eps) ** m
            - 2 * m * eps * (1 - eps) ** (m - 1)
            + (m * (m - 1) / 2.0) * eps ** 2 * (1 - eps) ** (m - 2))


def bd_operator_eigs(A, eps=EPS_DEFAULT):
    """Eigenvalues |lambda_i| of the symmetric Euclideanised causal
    d'Alembertian built from the ancestor matrix A.

    m_ij (order-interval cardinality between related i,j) = #k with i,k,j a
    chain.  For a related pair exactly one of (i<j),(j<i) holds, so
    m_ij = (A@A)[i,j] + (A@A)[j,i] picks the right count symmetrically.
    """
    n = A.shape[0]
    Af = A.astype(np.float32)
    inter = (Af @ Af).astype(np.float64)        # inter[i,j] = #k with A[i,k]&A[k,j]
    m = inter + inter.T                          # symmetric interval cardinality
    R = A | A.T                                  # symmetric causal relation
    W = smeared_weight(m, eps)
    M = np.where(R, W, 0.0)
    np.fill_diagonal(M, 0.0)
    np.fill_diagonal(M, -M.sum(axis=1))          # annihilate constants (zero mode)
    eigs = np.linalg.eigvalsh(M)
    return np.abs(eigs)                          # Euclidean continuation: positive


# --------------------------------------------------------------------------- #
# Heat kernel return probability and spectral dimension
# --------------------------------------------------------------------------- #
def heat_return(eigs, sigmas):
    """K(sigma) = (1/N) sum_i exp(-sigma |lambda_i|).  Eigenvalue 0 (constant
    mode) gives the finite-size floor 1/N as sigma -> infinity."""
    eigs = np.clip(np.asarray(eigs, dtype=float), 0.0, None)
    return np.array([np.mean(np.exp(-s * eigs)) for s in sigmas])


def spectral_dimension(sigmas, K):
    """D_s(sigma) = -2 d log K / d log sigma (central log-log gradient)."""
    lx = np.log(np.asarray(sigmas, dtype=float))
    ly = np.log(np.asarray(K, dtype=float))
    return -2.0 * np.gradient(ly, lx)


def lambda_scale(eigs):
    """A spectrum reference (median nonzero |lambda|) used to put sigma on a
    density-comparable footing across N: the operator's overall normalisation
    grows with density, so a fixed physical sigma corresponds to fixed
    sigma*lambda_scale.  D_s is invariant under this rescaling."""
    e = np.sort(np.asarray(eigs, dtype=float))
    nz = e[e > 1e-9 * e.max()]
    return float(np.median(nz)) if nz.size else float("nan")


# --------------------------------------------------------------------------- #
# Ensemble measurement over seeds (averages K(sigma) at fixed dimensionless s)
# --------------------------------------------------------------------------- #
def measure_ensemble(n, dim, seeds, sigmas_dimensionless, eps=EPS_DEFAULT):
    """For each seed: sprinkle, build operator, compute K at sigma = s/lambda_scale
    (so the dimensionless grid s is comparable across N/density).  Returns the
    seed-averaged K(s), its sem, the spectral dimension of the mean, the mean MM
    dimension, and the mean lambda_scale."""
    Ks, mms, lams = [], [], []
    for sd in seeds:
        rng = np.random.default_rng(sd)
        pts = sprinkle(n, dim, rng)
        A = ancestor_matrix(pts)
        eigs = bd_operator_eigs(A, eps=eps)
        lam = lambda_scale(eigs)
        sig = np.asarray(sigmas_dimensionless) / lam
        Ks.append(heat_return(eigs, sig))
        mms.append(mm_dimension(A, A.shape[0]))
        lams.append(lam)
    Ks = np.array(Ks)
    Kmean = Ks.mean(axis=0)
    Ksem = Ks.std(axis=0, ddof=1) / np.sqrt(len(seeds)) if len(seeds) > 1 else np.zeros_like(Kmean)
    ds = spectral_dimension(sigmas_dimensionless, Kmean)
    return {
        "n": int(n), "dim": int(dim), "eps": float(eps),
        "n_seeds": len(list(seeds)),
        "s": np.asarray(sigmas_dimensionless, dtype=float),
        "K_mean": Kmean, "K_sem": Ksem, "D_s": ds,
        "mm_mean": float(np.mean(mms)), "mm_std": float(np.std(mms)),
        "lambda_scale_mean": float(np.mean(lams)),
        "floor": 1.0 / n,
    }
