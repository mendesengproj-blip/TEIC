"""e3_core.py -- topological-defect engine for the E3_DEFECTS campaign.

DATA GENERATOR for NIVEL4_ORIENTATION entry FN3.  Contains NO physics
interpretation: the words "matter"/"particle"/"mass" are forbidden here -- they
live only in the synthesis (COMPARISON ONLY).  This module knows how to:

  * build an O(3) orientation field  n(x) in S^2  on a finite L^3 cubic lattice
    with OPEN (free) boundaries -- the substrate where a hedgehog n(r)=r_hat is
    well defined (a periodic torus cannot carry a single net point charge);
  * seed topological textures: hedgehog (+r_hat), anti-hedgehog (-r_hat), a
    hedgehog/anti dipole, and a toroidal (vortex-ring) winding;
  * MEASURE the topological charge B as the DEGREE of the map n: surface -> S^2,
    by the gauge-invariant solid-angle (Berg-Luscher) construction: every
    elementary cube's boundary is a small S^2, triangulated into 12 outward
    spherical triangles, and the signed spherical area summed / 4pi is the
    integer charge enclosed in that cube.  Total B = sum over cubes = degree of
    the OUTER boundary surface (interior faces cancel).  The local charge field
    q(cube) localises WHERE the winding sits and detects unwinding through the
    lattice cutoff;
  * relax the field by (a) zero-temperature GRADIENT FLOW on S^2 (overdamped
    Landau-Lifshitz: dn/dt = +(H - (H.n)n), H = sum of neighbour spins) and
    (b) finite-J METROPOLIS Monte-Carlo (checkerboard, free BC), and record the
    time series B(t), E(t), r_eff(t);
  * the Derrick gradient energy  E = sum_<ij> (1 - n_i . n_j)  (= a lattice
    discretisation of integral |grad n|^2; zero on a uniform field) and its
    behaviour under an artificial dilation n_lambda(x) = n((x-c)/lambda + c).

Anti-circularity.  No topological number, critical coupling, or 1/r law is
inserted into the generator.  B is a pure geometric solid-angle count of the
spins; E is the cos/dot bond functional; r_eff is a moment of the measured
gradient density.  The words for "stable particle" appear only in the synthesis.

Conventions follow results/.../orientation/orientation_core.py (O(3) Heisenberg,
E = -J sum n_i.n_j); here the lattice is OPEN, not periodic, and carries an
explicit coordinate grid so a radial texture can be written down.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------- #
# Cube-boundary triangulation for the solid-angle (Berg-Luscher) charge.
# Corner label(x,y,z) = 4x + 2y + z, with x,y,z in {0,1}.  The 12 triangles
# tile the 6 faces, each consistently OUTWARD oriented (verified: the hedgehog
# n=r_hat returns B=+1, the uniform field B=0 -- see E3V_gate).
# ---------------------------------------------------------------------- #
_CORNER = np.array([(x, y, z) for x in (0, 1) for y in (0, 1) for z in (0, 1)],
                   dtype=np.int64)            # row i is corner with label i
_TRIANGLES = np.array([
    # +x face  quad [4,6,7,5]
    (4, 6, 7), (4, 7, 5),
    # -x face  quad [0,1,3,2]
    (0, 1, 3), (0, 3, 2),
    # +y face  quad [2,3,7,6]
    (2, 3, 7), (2, 7, 6),
    # -y face  quad [0,4,5,1]
    (0, 4, 5), (0, 5, 1),
    # +z face  quad [1,5,7,3]
    (1, 5, 7), (1, 7, 3),
    # -z face  quad [0,2,6,4]
    (0, 2, 6), (0, 6, 4),
], dtype=np.int64)


# ====================================================================== #
# Field builders (open L^3 lattice, field shape (L,L,L,3) unit vectors)
# ====================================================================== #
def lattice_coords(L):
    """Integer coordinate grid X with X[i,j,k] = (i,j,k).  Shape (L,L,L,3)."""
    g = np.arange(L)
    I, J, K = np.meshgrid(g, g, g, indexing="ij")
    return np.stack([I, J, K], axis=-1).astype(float)


def default_center(L):
    """Geometric centre.  For even L this is a half-integer (a cube centre), so
    no lattice site sits exactly on the radial singularity r=0."""
    return np.array([(L - 1) / 2.0] * 3)


def _normalize(v, eps=1e-12):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + eps)


def hedgehog(L, charge=+1, center=None):
    """Radial texture n(r) = sign * r_hat (r measured from `center`).

    charge=+1 -> hedgehog (degree +1);  charge=-1 -> anti-hedgehog (degree -1).
    A site exactly at r=0 (only for odd L with integer centre) is set to +z.
    """
    center = default_center(L) if center is None else np.asarray(center, float)
    X = lattice_coords(L)
    d = X - center
    r = np.linalg.norm(d, axis=-1, keepdims=True)
    n = np.where(r > 1e-9, np.sign(charge) * d / (r + 1e-12),
                 np.array([0.0, 0.0, 1.0]))
    return _normalize(n)


def uniform(L, axis=(0.0, 0.0, 1.0)):
    """Ordered ferromagnetic vacuum: n = const everywhere (degree 0)."""
    n = np.zeros((L, L, L, 3))
    n[...] = _normalize(np.asarray(axis, float))
    return n


def dipole(L, sep=None):
    """Hedgehog (+1) and anti-hedgehog (-1) displaced along z by `sep`.

    Net degree 0.  Built by multiplying the two radial fields' stereographic
    angles is overkill; here we simply blend by nearest centre: a site takes the
    hedgehog direction if closer to the + centre, anti otherwise -- a crude but
    well-defined two-defect configuration (net B should measure 0).
    """
    sep = (L // 3) if sep is None else sep
    c = default_center(L)
    cp = c + np.array([0, 0, sep / 2.0])
    cm = c - np.array([0, 0, sep / 2.0])
    X = lattice_coords(L)
    dp = X - cp
    dm = X - cm
    rp = np.linalg.norm(dp, axis=-1, keepdims=True)
    rm = np.linalg.norm(dm, axis=-1, keepdims=True)
    np_ = dp / (rp + 1e-12)            # +r_hat about cp
    nm = -dm / (rm + 1e-12)            # -r_hat about cm
    closer_plus = (rp <= rm)
    n = np.where(closer_plus, np_, nm)
    return _normalize(n)


def toroidal(L, center=None):
    """A toroidal / vortex winding: in-plane component winds around the z axis
    (U(1) vortex) while n tilts out of plane toward the core, giving a ring-like
    texture.  Used as a catalogue entry; its degree is measured, not assumed."""
    center = default_center(L) if center is None else np.asarray(center, float)
    X = lattice_coords(L)
    d = X - center
    x, y, z = d[..., 0], d[..., 1], d[..., 2]
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    R0 = L / 4.0                                   # ring radius
    s = np.sqrt((rho - R0) ** 2 + z ** 2)          # distance to the ring core
    chi = np.pi * np.clip(s / (L / 3.0), 0, 1)     # polar tilt 0..pi
    nx = np.sin(chi) * (-np.sin(phi))
    ny = np.sin(chi) * (np.cos(phi))
    nz = np.cos(chi)
    n = np.stack([nx, ny, nz], axis=-1)
    return _normalize(n)


# ====================================================================== #
# Topological charge B  (solid-angle degree, per elementary cube)
# ====================================================================== #
def _tri_solid_angle(a, b, c):
    """Signed solid angle of the spherical triangle (a,b,c) of unit vectors,
    Van Oosterom-Strackee:  Omega = 2 atan2(a.(b x c), 1+a.b+b.c+c.a).
    a,b,c are (...,3) arrays; returns (...) in (-2pi, 2pi)."""
    num = np.einsum("...i,...i->...", a, np.cross(b, c))
    den = (1.0 + np.einsum("...i,...i->...", a, b)
           + np.einsum("...i,...i->...", b, c)
           + np.einsum("...i,...i->...", c, a))
    return 2.0 * np.arctan2(num, den)


def charge_field(n):
    """Local topological charge per elementary cube.

    Returns q with shape (L-1,L-1,L-1): q[i,j,k] = (1/4pi) * sum of the 12
    outward spherical-triangle solid angles on the boundary of the cube whose
    minimal corner is the site (i,j,k).  Each q is ~integer (the degree of n on
    that little S^2); the total B = q.sum() is the degree of the outer boundary
    surface (interior faces cancel exactly).
    """
    L = n.shape[0]
    # corners[c] : field at the cube corner with offset _CORNER[c], shape
    # (L-1,L-1,L-1,3).  Built by slicing the eight shifted sub-blocks.
    corners = []
    for (dx, dy, dz) in _CORNER:
        corners.append(n[dx:dx + L - 1, dy:dy + L - 1, dz:dz + L - 1, :])
    corners = np.stack(corners, axis=0)            # (8, L-1,L-1,L-1, 3)
    omega = np.zeros(corners.shape[1:4])
    for (ia, ib, ic) in _TRIANGLES:
        omega += _tri_solid_angle(corners[ia], corners[ib], corners[ic])
    return omega / (4.0 * np.pi)


def topological_charge(n):
    """Total degree B = sum of the per-cube solid-angle charge.  Returns float
    (close to an integer for a clean texture)."""
    return float(charge_field(n).sum())


def core_charge(n, center=None, radius=2):
    """Charge contained in the central (2*radius)^3 block of cubes -- localises
    the defect so its survival can be tracked even if lattice noise scatters tiny
    fractional charge near the boundary."""
    q = charge_field(n)
    L = q.shape[0]
    c = (L // 2) if center is None else int(round(center[0]))
    lo = max(0, c - radius)
    hi = min(L, c + radius + 1)
    return float(q[lo:hi, lo:hi, lo:hi].sum())


# ====================================================================== #
# Energy, gradient density, effective radius
# ====================================================================== #
def _neighbour_sum(n):
    """H[i] = sum over the (up to 6) existing nearest neighbours of n[i], open
    boundaries (missing neighbours contribute 0).  Shape (L,L,L,3)."""
    H = np.zeros_like(n)
    H[:-1] += n[1:]
    H[1:] += n[:-1]
    H[:, :-1] += n[:, 1:]
    H[:, 1:] += n[:, :-1]
    H[:, :, :-1] += n[:, :, 1:]
    H[:, :, 1:] += n[:, :, :-1]
    return H


def gradient_energy(n):
    """Derrick functional  E = sum over existing bonds (1 - n_i . n_j) >= 0,
    a lattice discretisation of (1/2) integral |grad n|^2.  Zero on a uniform
    field; large where n turns fast."""
    e = 0.0
    e += np.sum(1.0 - np.einsum("...i,...i->...", n[:-1], n[1:]))
    e += np.sum(1.0 - np.einsum("...i,...i->...", n[:, :-1], n[:, 1:]))
    e += np.sum(1.0 - np.einsum("...i,...i->...", n[:, :, :-1], n[:, :, 1:]))
    return float(e)


def gradient_density(n):
    """Per-site gradient energy g_i = sum_{j~i} (1 - n_i.n_j).  Shape (L,L,L)."""
    H = _neighbour_sum(n)
    deg = np.zeros(n.shape[:3])
    deg[:-1] += 1; deg[1:] += 1
    deg[:, :-1] += 1; deg[:, 1:] += 1
    deg[:, :, :-1] += 1; deg[:, :, 1:] += 1
    return deg - np.einsum("...i,...i->...", n, H)


def r_eff(n, center=None):
    """Effective defect radius  r_eff = sum_i r_i g_i / sum_i g_i  with g_i the
    gradient density and r_i the distance from `center`.  Shrinks to 0 if the
    texture collapses to a point, grows if it spreads."""
    center = default_center(n.shape[0]) if center is None else np.asarray(center, float)
    g = gradient_density(n)
    X = lattice_coords(n.shape[0])
    r = np.linalg.norm(X - center, axis=-1)
    tot = g.sum()
    return float(np.sum(r * g) / tot) if tot > 1e-12 else 0.0


def cooled_charge(n, steps=30, dt=0.1):
    """Topological charge measured AFTER a short gradient-flow cooling that
    removes thermal UV wrinkles (each of which carries spurious fractional solid
    angle) without moving the integer topological content -- the standard
    'cooling before measuring the charge' protocol of lattice field theory.
    Returns (B_cooled, B_core_cooled, r_eff_cooled)."""
    _, nc = relax_gradient(n, n_steps=steps, dt=dt, record_every=steps)
    return (topological_charge(nc), core_charge(nc), r_eff(nc))


def measure(n, center=None):
    """Snapshot of the three pre-registered observables (B, E, r_eff) plus the
    localised core charge."""
    return {"B": topological_charge(n),
            "B_core": core_charge(n, center),
            "E": gradient_energy(n),
            "r_eff": r_eff(n, center)}


# ====================================================================== #
# Relaxers
# ====================================================================== #
def relax_gradient(n, n_steps, dt=0.1, record_every=10, center=None,
                   pin_boundary=False):
    """Overdamped zero-T gradient flow on S^2:
        n <- normalize(n + dt * (H - (H.n) n)),   H = neighbour sum.
    This is steepest descent of E = -sum n_i.n_j on the unit-sphere manifold;
    it can only LOWER the energy, so it is the honest Derrick test (a texture
    that survives gradient flow is a genuine local minimum).  Open boundaries by
    default (the winding may escape); set pin_boundary to hold the outer shell
    fixed (Dirichlet) -- then the boundary degree is frozen and only the interior
    profile relaxes.  Returns (traj list of measure-dicts with 't', final n)."""
    n = n.copy()
    center = default_center(n.shape[0]) if center is None else center
    if pin_boundary:
        bmask = np.zeros(n.shape[:3], dtype=bool)
        bmask[[0, -1], :, :] = True
        bmask[:, [0, -1], :] = True
        bmask[:, :, [0, -1]] = True
        fixed = n.copy()
    traj = []
    snap = measure(n, center); snap["t"] = 0; traj.append(snap)
    for t in range(1, n_steps + 1):
        H = _neighbour_sum(n)
        Hpar = np.einsum("...i,...i->...", H, n)[..., None] * n
        n = _normalize(n + dt * (H - Hpar))
        if pin_boundary:
            n[bmask] = fixed[bmask]
        if t % record_every == 0 or t == n_steps:
            snap = measure(n, center); snap["t"] = t; traj.append(snap)
    return traj, n


def relax_mc(n, J, n_steps, seed=0, step=0.5, record_every=10, center=None,
             adapt=True, target=0.4):
    """Finite-coupling Metropolis on the open cube (checkerboard, vectorised).
    Energy -J sum n_i.n_j; J large = cold.  Monte-Carlo can hop small barriers
    that gradient flow cannot, so running BOTH brackets the stability question
    (charter protocol 2).  Returns (traj, final n)."""
    n = n.copy()
    L = n.shape[0]
    center = default_center(L) if center is None else center
    rng = np.random.default_rng(seed)
    g = np.arange(L)
    I, Ji, K = np.meshgrid(g, g, g, indexing="ij")
    parity = (I + Ji + K) % 2
    masks = [parity == 0, parity == 1]
    traj = []
    snap = measure(n, center); snap["t"] = 0; traj.append(snap)
    for t in range(1, n_steps + 1):
        acc_n = 0; tot_n = 0
        for mask in masks:
            H = _neighbour_sum(n)                         # uses current n
            old = n[mask]
            Hm = H[mask]
            v = old + step * rng.standard_normal(old.shape)
            prop = _normalize(v)
            dE = -J * np.einsum("...i,...i->...", prop - old, Hm)
            p = np.exp(-np.clip(dE, 0.0, 50.0))
            acc = rng.random(old.shape[0]) < p
            new = np.where(acc[:, None], prop, old)
            n[mask] = new
            acc_n += int(acc.sum()); tot_n += acc.size
        if adapt and t % 25 == 0:
            a = acc_n / max(tot_n, 1)
            if a > target + 0.1:
                step *= 1.15
            elif a < target - 0.1:
                step *= 0.87
            step = float(np.clip(step, 1e-3, 3.0))
        if t % record_every == 0 or t == n_steps:
            snap = measure(n, center); snap["t"] = t; traj.append(snap)
    return traj, n


# ====================================================================== #
# Derrick dilation
# ====================================================================== #
def dilate(n, lam, center=None):
    """Artificial scale transform  n_lambda(x) = n((x-c)/lambda + c) by TRILINEAR
    resampling (coordinates clamped into the box).  lambda>1 spreads the texture,
    lambda<1 compresses it.  Trilinear (not nearest) interpolation avoids the
    staircase undersampling artefact that otherwise injects spurious gradient
    energy when lambda>1.  Renormalised on return."""
    L = n.shape[0]
    center = default_center(L) if center is None else np.asarray(center, float)
    X = lattice_coords(L)
    src = np.clip((X - center) / lam + center, 0, L - 1)
    i0 = np.floor(src).astype(int)
    i1 = np.minimum(i0 + 1, L - 1)
    f = src - i0                                   # (L,L,L,3) fractional offsets
    out = np.zeros_like(n)
    for ax, (a, b, c) in enumerate([(0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1),
                                    (1, 1, 0), (1, 0, 1), (0, 1, 1), (1, 1, 1)]):
        ii = np.where(a, i1[..., 0], i0[..., 0])
        jj = np.where(b, i1[..., 1], i0[..., 1])
        kk = np.where(c, i1[..., 2], i0[..., 2])
        wx = f[..., 0] if a else 1 - f[..., 0]
        wy = f[..., 1] if b else 1 - f[..., 1]
        wz = f[..., 2] if c else 1 - f[..., 2]
        out += (wx * wy * wz)[..., None] * n[ii, jj, kk, :]
    return _normalize(out)


def derrick_curve(n, lambdas, center=None, weight=None):
    """E(lambda) of the dilated texture.  `weight`, if given, is a per-site
    factor w(x) multiplying each site's bond energy (a COMPARISON-ONLY proxy for
    a curved metric, e.g. w = 1 + alpha/r); flat metric is weight=None."""
    center = default_center(n.shape[0]) if center is None else center
    Es, Bs = [], []
    for lam in lambdas:
        nl = dilate(n, lam, center)
        if weight is None:
            Es.append(gradient_energy(nl))
        else:
            Es.append(float(np.sum(weight * gradient_density(nl)) / 2.0))
        Bs.append(topological_charge(nl))
    return np.asarray(Es), np.asarray(Bs)


def radial_weight(L, alpha, center=None, r_floor=1.0):
    """w(x) = 1 + alpha / max(r, r_floor) -- a static curvature proxy peaked at
    the defect core (COMPARISON ONLY: stands in for theta(r) ~ M/r)."""
    center = default_center(L) if center is None else center
    X = lattice_coords(L)
    r = np.linalg.norm(X - center, axis=-1)
    return 1.0 + alpha / np.maximum(r, r_floor)


# ====================================================================== #
# Radial profiles (for the gravity / field-of-the-defect probe)
# ====================================================================== #
def radial_profile(field_scalar, center=None, n_bins=None):
    """Spherically bin a scalar field by distance from centre.  Returns
    (r_centres, mean_value, counts)."""
    L = field_scalar.shape[0]
    center = default_center(L) if center is None else center
    X = lattice_coords(L)
    r = np.linalg.norm(X - center, axis=-1).ravel()
    v = field_scalar.ravel()
    n_bins = (L // 2) if n_bins is None else n_bins
    edges = np.linspace(0, r.max(), n_bins + 1)
    which = np.clip(np.digitize(r, edges) - 1, 0, n_bins - 1)
    sumv = np.bincount(which, weights=v, minlength=n_bins)
    cnt = np.bincount(which, minlength=n_bins)
    ctr = 0.5 * (edges[:-1] + edges[1:])
    good = cnt > 0
    with np.errstate(invalid="ignore"):
        mean = sumv / cnt
    return ctr[good], mean[good], cnt[good]


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("e3_core self-test")
    for L in (8, 12, 16):
        nh = hedgehog(L, +1)
        na = hedgehog(L, -1)
        nu = uniform(L)
        Bh, Ba, Bu = topological_charge(nh), topological_charge(na), topological_charge(nu)
        print(f"  L={L:2d}  B(hedgehog)={Bh:+.4f}  B(anti)={Ba:+.4f}  "
              f"B(uniform)={Bu:+.4f}  E_hh={gradient_energy(nh):.1f} "
              f"r_eff={r_eff(nh):.2f}")
        assert abs(Bh - 1.0) < 1e-6, Bh
        assert abs(Ba + 1.0) < 1e-6, Ba
        assert abs(Bu) < 1e-6, Bu
    nd = dipole(16)
    print(f"  dipole  B={topological_charge(nd):+.4f} (expect ~0)")
    nt = toroidal(16)
    print(f"  toroidal B={topological_charge(nt):+.4f}  E={gradient_energy(nt):.1f}")
    # quick gradient-flow sanity: hedgehog energy must not increase
    traj, nf = relax_gradient(hedgehog(12, +1), n_steps=80, dt=0.1, record_every=40)
    print(f"  grad-flow L=12: E {traj[0]['E']:.1f} -> {traj[-1]['E']:.1f}, "
          f"B {traj[0]['B']:+.3f} -> {traj[-1]['B']:+.3f}, "
          f"r_eff {traj[0]['r_eff']:.2f} -> {traj[-1]['r_eff']:.2f}")
    assert traj[-1]["E"] <= traj[0]["E"] + 1e-6
    print("self-test OK")
