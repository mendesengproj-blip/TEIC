"""d3_audit_core.py -- shared engine for the brutal audit of D3.

BRIDGE / D3 AUDIT.  Independent of R1-R3 and e6-e11; modifies nothing.  Lives
entirely under results/ (the anti-circularity guard does not scan it, but the
golden rule is obeyed regardless): the GENERATORS here contain no G, no GM/r, no
sqrt(1-2M/r), no "4 pi G".  The source is a dimensionless weight w_M deposited on
cells.  G, M and Schwarzschild appear ONLY inside blocks delimited by
`COMPARISON ONLY ... END COMPARISON ONLY`, used only to score the output.

The physics, and the methodological key
---------------------------------------
D3 ran Metropolis on the coarse-grained density field theta = delta rho / rho0
under the discrete Benincasa-Dowker static action (continuum limit B -> -nabla^2):

    E[theta] = (K/2) * sum_edges (grad theta)^2 * (geometry)  -  sum_cells q_i theta_i,

with a conservation constraint sum_i theta_i V_i = 0 (a denser core balanced by a
thinner far field).  This action is QUADRATIC, so the Metropolis equilibrium
*distribution* is Gaussian and its *mean* is exactly the minimiser of E, i.e. the
solution of the discrete Poisson equation

    -K nabla^2 theta = q - <q>            (the neutralising-background / Jeans form
                                           of the conservation constraint).

This is the single fact the audit exploits: the deterministic solver `*_solve`
returns the exact MC mean, and `*_mc` runs a genuine (vectorised heat-bath)
Metropolis whose post-burn-in time average converges to it.  D3-A validates the
identity numerically with error bars over independent seeds; B/C/D then use the
solver as the exact MC mean and carry MC error bars where sampling matters.

What "rho" and "L" mean for the coarse-grained field
----------------------------------------------------
In the causet, rho is the sprinkling density (events per unit volume).  For the
coarse-grained field it sets the cell density: a box of linear size L holds
N_cell ~ rho * L^d cells, so the grid spacing is h ~ rho^{-1/d}.  Higher rho =
finer resolution and smaller relative coarse-grained fluctuations -- exactly the
role rho plays in a sprinkling.  L is the box size in network units.  Both are
inputs (the granularity / Planck scale is an input, as stated for a_0 and below
for G); the PROFILE SHAPE and EXPONENT are outputs.
"""

from __future__ import annotations

import numpy as np
from scipy.sparse import diags, identity, kron, csr_matrix
from scipy.sparse.linalg import cg, LinearOperator


# --------------------------------------------------------------------------- #
#  RADIAL (spherically symmetric) engine  --  for D3-A, D3-D                   #
# --------------------------------------------------------------------------- #
def radial_grid(L, n_bins, r_min=1.0):
    """Log-spaced radial grid on [r_min, L] in d=3 (shell measure r^{d-1})."""
    edges = np.geomspace(r_min, L, n_bins + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    shell_vol = (edges[1:] ** 3 - edges[:-1] ** 3) / 3.0     # ~ r^2 dr
    return edges, centers, shell_vol


def _radial_laplacian(centers, shell_vol, K):
    """Weighted graph Laplacian of the gradient action (rows sum to zero).

    E = (K/2) sum_e H_e (th[e+1]-th[e])^2,  H_e = K * vbar_e / dr_e^2.
    The minimiser of E - q.th solves  Lap @ th = q  with Lap SPD up to the
    constant null space.  Returned as a dense (n x n) array (n <= ~120).
    """
    n = centers.size
    dr = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H = K * vbar / dr ** 2                                    # one per edge
    Lap = np.zeros((n, n))
    for e in range(n - 1):
        Lap[e, e] += H[e]
        Lap[e + 1, e + 1] += H[e]
        Lap[e, e + 1] -= H[e]
        Lap[e + 1, e] -= H[e]
    return Lap


def radial_source_core(centers, shell_vol, r_core, w_M):
    """Normalised finite source-core profile (smeared point mass), weight w_M.

    Returns q_i = w_M * s_i with sum_i s_i = 1 (s supported on r < r_core).
    NO G anywhere: w_M is a dimensionless deposited weight.
    """
    mask = centers < r_core
    s = np.where(mask, shell_vol, 0.0)
    s = s / s.sum()
    return w_M * s


def radial_solve(centers, shell_vol, q, K):
    """Exact MC-mean: minimiser of the quadratic action (= discrete Poisson).

    Solves Lap @ theta = q - <q> (neutralising background) and fixes the gauge so
    that the conservation integral sum_i theta_i V_i = 0.
    """
    Lap = _radial_laplacian(centers, shell_vol, K)
    # conservation sum_i theta_i V_i = 0 via Lagrange multiplier: Lap theta = q - lam V
    # with lam = sum(q)/sum(V) so the RHS sums to zero (Lap rows sum to zero).
    lam = q.sum() / shell_vol.sum()
    rhs = q - lam * shell_vol
    theta, *_ = np.linalg.lstsq(Lap, rhs, rcond=None)
    theta = theta - (theta * shell_vol).sum() / shell_vol.sum()   # gauge
    return theta


def radial_mc(centers, shell_vol, q, K, temp, n_sweeps, n_burn, seed):
    """Genuine Metropolis (vectorised even/odd heat-bath) on the radial field.

    Heat-bath for a Gaussian field is Metropolis with acceptance 1; it samples the
    SAME Boltzmann distribution as D3's pair-move Metropolis (documented in the
    module docstring).  Returns the post-burn-in time-mean of theta.
    """
    rng = np.random.default_rng(seed)
    n = centers.size
    dr = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H = K * vbar / dr ** 2                                    # edge stiffness
    # node "mass" (diagonal of the local quadratic form) and neighbour coupling
    diag = np.zeros(n)
    diag[:-1] += H
    diag[1:] += H
    lam = q.sum() / shell_vol.sum()          # volume-weighted neutralising background
    qz = q - lam * shell_vol
    theta = np.zeros(n)
    even = np.arange(0, n, 2)
    odd = np.arange(1, n, 2)
    acc = np.zeros(n)
    nmeas = 0
    beta = 1.0 / temp
    for sweep in range(n_sweeps):
        for idx in (even, odd):
            # local field h_i = sum_neighbours H * theta_neighbour + q_i
            hloc = qz[idx].copy()
            left = idx - 1
            ok = left >= 0
            hloc[ok] += H[left[ok]] * theta[left[ok]]
            right = idx + 1
            ok = right <= n - 1
            hloc[ok] += H[idx[ok]] * theta[right[ok]]
            d = diag[idx]
            d = np.where(d <= 0, 1e-12, d)
            mu = hloc / d                                     # heat-bath mean
            sig = np.sqrt(temp / d)                           # heat-bath width
            theta[idx] = mu + sig * rng.standard_normal(idx.size)
        if sweep >= n_burn:
            acc += theta
            nmeas += 1
    theta_mean = acc / max(nmeas, 1)
    theta_mean -= (theta_mean * shell_vol).sum() / shell_vol.sum()   # gauge
    return theta_mean


def radial_mc_batch(centers, shell_vol, q, K, temp, n_sweeps, n_burn, seeds):
    """Batched radial heat-bath: run len(seeds) independent chains at once.

    The Python sweep-loop cost is shared across chains (theta is (n, S)), so 20
    seeds cost ~the same wall-time as one.  Returns theta_means with shape (n, S).
    """
    seeds = list(seeds)
    S = len(seeds)
    rng = np.random.default_rng(np.array(seeds))   # independent SeedSequence per col
    n = centers.size
    dr = np.diff(centers)
    vbar = 0.5 * (shell_vol[:-1] + shell_vol[1:])
    H = K * vbar / dr ** 2
    diag = np.zeros(n)
    diag[:-1] += H
    diag[1:] += H
    diag = np.where(diag <= 0, 1e-12, diag)
    lam = q.sum() / shell_vol.sum()
    qz = (q - lam * shell_vol)[:, None]            # (n,1) broadcast over chains
    Hcol = H[:, None]
    theta = np.zeros((n, S))
    even = np.arange(0, n, 2)
    odd = np.arange(1, n, 2)
    acc = np.zeros((n, S))
    nmeas = 0
    for sweep in range(n_sweeps):
        for idx in (even, odd):
            hloc = qz[idx] + np.zeros((idx.size, S))
            left = idx - 1
            ok = left >= 0
            hloc[ok] += Hcol[left[ok]] * theta[left[ok]]
            right = idx + 1
            ok = right <= n - 1
            hloc[ok] += Hcol[idx[ok]] * theta[right[ok]]
            d = diag[idx][:, None]
            mu = hloc / d
            sig = np.sqrt(temp / d)
            theta[idx] = mu + sig * rng.standard_normal((idx.size, S))
        if sweep >= n_burn:
            acc += theta
            nmeas += 1
    theta_means = acc / max(nmeas, 1)
    theta_means -= (theta_means * shell_vol[:, None]).sum(0) / shell_vol.sum()
    return theta_means


def fit_tail(centers, theta, r_lo, r_hi):
    """Fit theta = A/r + C on r in [r_lo, r_hi]; return A, C, offset-removed exponent.

    The raw log-log slope is contaminated by the finite-box conservation offset C;
    the Newtonian exponent is the slope of (theta - C), which is -1 for a 1/r tail.
    """
    use = (centers >= r_lo) & (centers <= r_hi)
    if use.sum() < 4:
        return np.nan, np.nan, np.nan
    X = np.vstack([1.0 / centers[use], np.ones(use.sum())]).T
    coef, *_ = np.linalg.lstsq(X, theta[use], rcond=None)
    A, C = float(coef[0]), float(coef[1])
    resid = theta[use] - C
    ok = resid > 0
    if ok.sum() < 4:
        return A, C, np.nan
    p = float(np.polyfit(np.log(centers[use][ok]), np.log(resid[ok]), 1)[0])
    return A, C, p


# --------------------------------------------------------------------------- #
#  3D CARTESIAN engine  --  for D3-B (source shapes), D3-C (superposition)     #
# --------------------------------------------------------------------------- #
def grid3d(L, n):
    """Cell-centred cubic grid: n^3 cells on [-L/2, L/2]^3, spacing h."""
    h = L / n
    ax = (np.arange(n) - (n - 1) / 2.0) * h
    X, Y, Z = np.meshgrid(ax, ax, ax, indexing="ij")
    R = np.sqrt(X ** 2 + Y ** 2 + Z ** 2)
    return dict(n=n, L=L, h=h, ax=ax, X=X, Y=Y, Z=Z, R=R)


def laplacian3d(theta, h):
    """Discrete 7-point Laplacian with Neumann (zero-gradient) edges."""
    lap = -6.0 * theta
    for ax in range(3):
        lap += np.roll(theta, +1, axis=ax) + np.roll(theta, -1, axis=ax)
    # correct the wrap-around faces to Neumann (mirror) so edges are not periodic
    for ax in range(3):
        sl0 = [slice(None)] * 3; sl0[ax] = 0
        sl1 = [slice(None)] * 3; sl1[ax] = 1
        slN = [slice(None)] * 3; slN[ax] = -1
        slNm = [slice(None)] * 3; slNm[ax] = -2
        # at face 0 the roll(-1) brought in the opposite face; replace by mirror
        lap[tuple(sl0)] += theta[tuple(sl1)] - theta[tuple(slN)]
        lap[tuple(slN)] += theta[tuple(slNm)] - theta[tuple(sl0)]
    return lap / h ** 2


def _lap_operator(n):
    """Sparse 7-point Neumann Laplacian (unit spacing) on n^3, as a LinearOperator-able matrix."""
    e = np.ones(n)
    T = diags([e[:-1], -2 * e, e[:-1]], [-1, 0, 1], format="lil")
    T[0, 0] = -1.0          # Neumann
    T[-1, -1] = -1.0
    T = csr_matrix(T)
    I = identity(n, format="csr")
    L3 = (kron(kron(T, I), I) + kron(kron(I, T), I) + kron(kron(I, I), T)).tocsr()
    return L3


def poisson3d_solve(source, h, K, tol=1e-8, maxiter=20000):
    """Exact MC mean in 3D: solve -K nabla^2 theta = (source - <source>).

    Neumann BCs + zero-mean source (neutralising background) make this solvable; we
    return the zero-mean solution (gauge sum theta = 0).  source is an n^3 array of
    deposited weights (NO G).
    """
    n = source.shape[0]
    L3 = _lap_operator(n)                       # unit-spacing Neumann Laplacian
    # want  -K nabla^2 theta = (source - bg).  With A = -L3 (SPD discrete -nabla^2,
    # unit spacing) this is  A x = (source - bg) * h^2 / K.
    rhs = (source - source.mean()).ravel() * h ** 2 / K
    A = (-L3).tocsr()
    rhs = rhs - rhs.mean()                       # project off the constant null space
    x, info = cg(A, rhs, rtol=tol, maxiter=maxiter)
    x = x - x.mean()
    return x.reshape(source.shape)


def mc3d_heatbath(source, h, K, temp, n_sweeps, n_burn, seed):
    """Vectorised checkerboard heat-bath Metropolis on the 3D field; returns the mean.

    Same Boltzmann distribution as the radial MC, in 3D.  Used to confirm the MC
    mean equals poisson3d_solve on a representative case (with seed error bars).
    """
    rng = np.random.default_rng(seed)
    n = source.shape[0]
    qz = (source - source.mean()) * h ** 2 / K
    theta = np.zeros((n, n, n))
    ii, jj, kk = np.indices((n, n, n))
    parity = (ii + jj + kk) % 2
    masks = (parity == 0), (parity == 1)
    acc = np.zeros((n, n, n))
    nmeas = 0
    for sweep in range(n_sweeps):
        for m in masks:
            nb = np.zeros((n, n, n))
            cnt = np.zeros((n, n, n))
            for ax in range(3):
                for s in (+1, -1):
                    rolled = np.roll(theta, s, axis=ax)
                    valid = np.ones((n, n, n), dtype=bool)
                    sl = [slice(None)] * 3
                    sl[ax] = 0 if s == +1 else -1            # face with no neighbour
                    valid[tuple(sl)] = False
                    nb += np.where(valid, rolled, 0.0)
                    cnt += valid
            d = cnt
            mu = (nb + qz) / np.where(d <= 0, 1e-12, d)
            sig = np.sqrt(temp * h ** 2 / K / np.where(d <= 0, 1e-12, d))
            new = mu + sig * rng.standard_normal((n, n, n))
            theta = np.where(m, new, theta)
        if sweep >= n_burn:
            acc += theta
            nmeas += 1
    theta_mean = acc / max(nmeas, 1)
    return theta_mean - theta_mean.mean()


def radial_profile(field, R, nbins, r_max):
    """Spherically average a 3D field into nbins radial bins on [0, r_max]."""
    edges = np.linspace(0, r_max, nbins + 1)
    idx = np.digitize(R.ravel(), edges) - 1
    f = field.ravel()
    centers = 0.5 * (edges[:-1] + edges[1:])
    prof = np.full(nbins, np.nan)
    for b in range(nbins):
        sel = idx == b
        if sel.sum() > 0:
            prof[b] = f[sel].mean()
    return centers, prof


def deposit_ball(grid, r0, w_M, center=(0, 0, 0)):
    """Uniform-weight ball of radius r0, total deposited weight w_M (NO G)."""
    cx, cy, cz = center
    RR = np.sqrt((grid["X"] - cx) ** 2 + (grid["Y"] - cy) ** 2 + (grid["Z"] - cz) ** 2)
    s = (RR < r0).astype(float)
    tot = s.sum()
    return (w_M / tot) * s if tot > 0 else s


if __name__ == "__main__":
    # self-test: radial solver vs MC, reproduce D3's A ~ 1, exponent ~ -1
    L, nb, rc = 60.0, 40, 4.0
    edges, centers, sv = radial_grid(L, nb, r_min=1.0)
    q = radial_source_core(centers, sv, rc, w_M=1.0)
    th_solve = radial_solve(centers, sv, q, K=1.0)
    th_mc = radial_mc(centers, sv, q, K=1.0, temp=0.02,
                      n_sweeps=4000, n_burn=1000, seed=1)
    A_s, C_s, p_s = fit_tail(centers, th_solve, rc, 0.6 * L)
    A_m, C_m, p_m = fit_tail(centers, th_mc, rc, 0.6 * L)
    print(f"solve: A={A_s:.3f} C={C_s:+.4f} exponent={p_s:.3f}")
    print(f"  mc : A={A_m:.3f} C={C_m:+.4f} exponent={p_m:.3f}")
    print(f"mc-vs-solve max|dtheta| = {np.max(np.abs(th_mc-th_solve)):.2e}")
