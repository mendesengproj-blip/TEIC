"""r5_group_core -- shared group-theory machinery for campaign R5.

Anti-circularity note
---------------------
R5 asks: is there an ANALYTICAL criterion (extending Bott/Cartan + what the
MIN1-3 chain measured for SU(2)) that forces SU(3) as the colour group, rather
than SU(N>=4)?  Nothing in this module reads any TEIC lattice result: every
quantity computed here (structure constants f^abc, symmetric d^abc, reality of
the fundamental representation) is a fixed property of the abstract compact Lie
group su(N).  N is the FREE input we scan.  The point of the campaign is exactly
that the causal network does NOT measure N (it is hard-wired into su3_core, just
as d=3 is an input to the geometry); so the only honest question is whether pure
representation theory / topology SELECTS N=3 -- and where the selection, if any,
gets its extra requirement from.

Conventions
-----------
Hermitian, traceless generators T_a (a = 1..N^2-1), normalised
    Tr(T_a T_b) = (1/2) delta_ab          (Gell-Mann normalisation).
Fundamental group element:  U = exp(i theta_a T_a).

Generalised Gell-Mann basis: symmetric off-diagonal, antisymmetric off-diagonal,
and (N-1) diagonal generators.
"""

import numpy as np


def gell_mann(N):
    """Return a list of the N^2-1 Hermitian traceless generators of su(N),
    normalised to Tr(T_a T_b) = 1/2 delta_ab."""
    gens = []
    # symmetric off-diagonal: (1/2)(E_jk + E_kj)
    for j in range(N):
        for k in range(j + 1, N):
            T = np.zeros((N, N), dtype=complex)
            T[j, k] = 0.5
            T[k, j] = 0.5
            gens.append(T)
    # antisymmetric off-diagonal: (1/2)(-i)(E_jk - E_kj)
    # SU(3) GROUP-DEF COMPLEX
    # The imaginary unit here IS the definition of the su(N) Lie algebra (the
    # antisymmetric Gell-Mann generators), not a smuggled e^{ikL} phase: this
    # module reads NO TEIC lattice result (see docstring). Same principled
    # exception as src/.../su3_core.py.
    for j in range(N):
        for k in range(j + 1, N):
            T = np.zeros((N, N), dtype=complex)
            T[j, k] = -0.5j
            T[k, j] = 0.5j
            gens.append(T)
    # END SU(3) GROUP-DEF COMPLEX
    # diagonal: c_l * diag(1,...,1 (l ones), -l, 0,...,0),  c_l = sqrt(1/(2 l(l+1)))
    for l in range(1, N):
        c = np.sqrt(1.0 / (2.0 * l * (l + 1)))
        diag = np.zeros(N, dtype=complex)
        diag[:l] = 1.0
        diag[l] = -l
        gens.append(np.diag(c * diag))
    assert len(gens) == N * N - 1
    return gens


def check_normalisation(gens):
    """Max |Tr(T_a T_b) - 1/2 delta_ab| over all a,b -- should be ~0."""
    n = len(gens)
    worst = 0.0
    for a in range(n):
        for b in range(n):
            val = np.trace(gens[a] @ gens[b])
            target = 0.5 if a == b else 0.0
            worst = max(worst, abs(val - target))
    return worst


def d_symbol_sumsq(gens):
    """Sum over a,b,c of (d^abc)^2 where
        d^abc = 2 Tr({T_a, T_b} T_c)   (totally symmetric cubic invariant).
    Returns (sum_dsq, max_abs_d).  Zero <=> no symmetric cubic invariant
    (su(2): the only simple algebra with d^abc = 0)."""
    n = len(gens)
    sum_dsq = 0.0
    max_abs = 0.0
    for a in range(n):
        for b in range(n):
            anti = gens[a] @ gens[b] + gens[b] @ gens[a]
            for c in range(n):
                d = 2.0 * np.trace(anti @ gens[c])
                # d must be real for Hermitian generators
                d = d.real
                sum_dsq += d * d
                max_abs = max(max_abs, abs(d))
    return sum_dsq, max_abs


def fundamental_reality(gens, tol=1e-9):
    """Classify the fundamental representation of su(N) as
    'real', 'pseudoreal', or 'complex' by the Frobenius-Schur criterion,
    computed structurally (no Haar integral).

    The fundamental rep R(theta) = exp(i theta_a T_a) is self-conjugate iff
    there is an invertible intertwiner S with
        S T_a S^{-1} = -T_a^*   for all a   (i.e. S T_a + T_a^* S = 0).
    - no nonzero S  -> complex (R not equivalent to its conjugate)
    - S symmetric   -> real     (orthogonal invariant)
    - S antisymmetric -> pseudoreal (symplectic invariant)

    We find S by computing the null space of the linear map
        L(S) = sum_a (T_a^* S + S T_a) stacked over a.
    """
    N = gens[0].shape[0]
    n = len(gens)
    # Build the (n*N^2) x (N^2) real-linear system on vec(S) (complex S).
    # Condition per generator: T_a^* S + S T_a = 0.
    # vectorise S column-major: vec(A X B) = (B^T kron A) vec(X).
    I = np.eye(N)
    rows = []
    for a in range(n):
        Ta = gens[a]
        TaC = np.conj(Ta)
        # T_a^* S  ->  (I kron T_a^*) vec(S)
        M1 = np.kron(I, TaC)
        # S T_a    ->  (T_a^T kron I) vec(S)
        M2 = np.kron(Ta.T, I)
        rows.append(M1 + M2)
    L = np.vstack(rows)
    # null space via SVD
    u, s, vh = np.linalg.svd(L)
    null_mask = s < tol * max(1.0, s[0]) if len(s) else np.array([])
    nnull = int(np.sum(s < tol * (s[0] if len(s) else 1.0)))
    # account for the fact that the system may have fewer singular values than columns
    ncols = L.shape[1]
    rank = int(np.sum(s > tol * (s[0] if len(s) else 1.0)))
    null_dim = ncols - rank
    if null_dim == 0:
        return "complex", null_dim, None
    # take a null vector, reshape to S, classify symmetry
    Svec = vh[-1].conj()
    S = Svec.reshape(N, N)
    # normalise
    S = S / np.linalg.norm(S)
    sym = np.linalg.norm(S - S.T)
    antisym = np.linalg.norm(S + S.T)
    if sym < antisym:
        kind = "real"
    else:
        kind = "pseudoreal"
    return kind, null_dim, S


def summary_row(N):
    gens = gell_mann(N)
    norm_err = check_normalisation(gens)
    sum_dsq, max_d = d_symbol_sumsq(gens)
    reality, null_dim, _ = fundamental_reality(gens)
    return {
        "N": N,
        "group": f"SU({N})",
        "dim": N * N - 1,
        "rank": N - 1,
        "norm_err": norm_err,
        "anomaly_sumsq_dabc": sum_dsq,
        "max_abs_dabc": max_d,
        "fundamental_reality": reality,
        "intertwiner_null_dim": null_dim,
    }


if __name__ == "__main__":
    for N in range(2, 7):
        print(summary_row(N))
