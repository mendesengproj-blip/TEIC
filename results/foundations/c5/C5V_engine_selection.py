"""C5V_engine_selection.py -- the C5-V engine-selection record.

Tests three candidate heat-kernel engines against the C5-V gate: does D_s at
large (pre-saturation) scale reproduce the Myrheim-Meyer dimension of the SAME
sprinkling?

  A  link-graph Laplacian  (undirected covering relations, L = D - Adj)
  B  relation-graph Laplacian (all causal relations as edges)
  C  symmetric smeared-BD diffusion (causal d'Alembertian structure,
     Euclideanised: |spectrum|)

Result (see C5V_gate.md): A overshoots (d=2: ~6) and fragments (d=4); B
saturates immediately; only C (the e10 Sorkin/BD operator) reproduces the MM
dimension.  Per the gate protocol the engine is therefore C (c5_core.py).
This file is the standalone, reproducible record of that decision; it is NOT
imported by the campaign.
"""
from __future__ import annotations
import sys, time
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "tier3"))
import tier3_core as t3   # sprinkle_diamond, causal_matrix_anc, mm_dimension, ordering_fraction


def link_matrix(A):
    """Covering relations: i->j is a link iff A[i,j] and no k with A[i,k]&A[k,j]."""
    Af = A.astype(np.float32)
    two = (Af @ Af) > 0.5          # at least one intermediary
    return A & ~two


def heat_return(eigs, sigmas):
    """Average return probability P(sigma) = (1/N) sum_i exp(-sigma * lambda_i)."""
    eigs = np.clip(eigs, 0, None)
    P = np.array([np.mean(np.exp(-s * eigs)) for s in sigmas])
    return P


def spectral_dim(sigmas, P):
    """D_s(sigma) = -2 d log P / d log sigma  (central differences in log-log)."""
    lx, ly = np.log(sigmas), np.log(P)
    ds = -2.0 * np.gradient(ly, lx)
    return ds


def laplacian_eigs(Adj):
    deg = np.asarray(Adj.sum(axis=1)).ravel().astype(float)
    L = np.diag(deg) - Adj.astype(float)
    return np.linalg.eigvalsh(L)


def smeared_weight(m, eps):
    return ((1 - eps) ** m - 2 * m * eps * (1 - eps) ** (m - 1)
            + (m * (m - 1) / 2) * eps ** 2 * (1 - eps) ** (m - 2))


def bd_sym_eigs(A, eps=0.25):
    """Symmetric Euclideanised causal-d'Alembertian operator.
    M[i,j] = w(m_ij) for j related to i (either cone); m_ij = # elements in the
    order-interval between i,j. Symmetrised; diagonal = -row offdiag so const
    annihilates. Use |spectrum| as a positive diffusion generator."""
    n = A.shape[0]
    R = A | A.T                       # symmetric relation
    # interval cardinality between related pairs:
    Af = A.astype(np.float32)
    # number of k strictly between i,j (for i>j causally): (A @ A)
    inter = (Af @ Af)                 # inter[i,j] = #k with A[i,k]&A[k,j]
    M = np.zeros((n, n))
    rel = np.argwhere(R)
    for i, j in rel:
        m = inter[i, j] + inter[j, i]   # interval count (one direction is 0)
        M[i, j] = smeared_weight(m, eps)
    M = 0.5 * (M + M.T)
    np.fill_diagonal(M, -M.sum(axis=1))   # annihilate constants
    eigs = np.linalg.eigvalsh(M)
    return np.abs(eigs)               # Euclideanise: positive generator


def mm_dim_of(A, n):
    r = t3.ordering_fraction(A, n)
    return t3.mm_dimension(r)


def run_engine(name, eigs, n, mm, dim):
    sig = np.geomspace(0.05, 50.0, 60)
    P = heat_return(eigs, sig)
    ds = spectral_dim(sig, P)
    # plateau: look in the region where P has dropped but not saturated (P>2/n)
    mask = P > (3.0 / n)
    print(f"  [{name}] dim={dim} N={n}  MM={mm:.2f}")
    for k in range(0, len(sig), 6):
        flag = "" if mask[k] else "  (saturating)"
        print(f"      sigma={sig[k]:8.3f}  P={P[k]:.4e}  D_s={ds[k]:6.2f}{flag}")
    # report max D_s and the value at the upper-sigma plateau within mask
    if mask.any():
        idx = np.where(mask)[0]
        ds_ir = np.median(ds[idx[-8:]]) if idx.size >= 8 else ds[idx[-1]]
        print(f"      -> IR-plateau D_s ~ {ds_ir:.2f} (target MM={mm:.2f}); "
              f"min D_s={np.nanmin(ds[idx]):.2f} max D_s={np.nanmax(ds[idx]):.2f}")
    print()


def main():
    for dim, N in [(2, 2500), (4, 2500)]:
        rng = np.random.default_rng(7 + dim)
        pts = t3.sprinkle_diamond(N, dim, rng)
        A = t3.causal_matrix_anc(pts)
        n = A.shape[0]
        mm = mm_dim_of(A, n)
        t0 = time.perf_counter()
        # Engine A: link graph
        Lk = link_matrix(A)
        Adj = (Lk | Lk.T)
        eigsA = laplacian_eigs(Adj)
        run_engine("A link-Laplacian", eigsA, n, mm, dim)
        # Engine B: full relation graph
        R = (A | A.T)
        eigsB = laplacian_eigs(R)
        run_engine("B relation-Laplacian", eigsB, n, mm, dim)
        # Engine C: symmetric Euclideanised BD
        eigsC = bd_sym_eigs(A, eps=0.25)
        run_engine("C bd-sym-euclid", eigsC, n, mm, dim)
        print(f"  [dim={dim} total {time.perf_counter()-t0:.1f}s]\n" + "="*60)


if __name__ == "__main__":
    main()
