"""phi_emerge_core.py -- the EMERGENT complex field  Phi_i = rho_i * e^{i phibar_i}.

PHI_EMERGE campaign.  CR_ABELIAN_HIGGS added a complex Higgs Phi by hand (a fourth
ingredient).  This campaign asks the sharper question: can Phi be a COMPOSITION of two
fields the causal network ALREADY has --

    |Phi_i|   = rho_i      = local causal density of events (Voronoi count, normalised),
    arg(Phi_i)= phibar_i   = mean gauge (Stueckelberg link) phase at node i,

so that  Phi_i = rho_i * e^{i phibar_i}  is not new physics but a derived observable?
If this composition condenses, gives the gauge a mass, and pins a vortex, then Phi
EMERGED.  If not, the complex field of CR_ABELIAN_HIGGS was a genuine extra ingredient.

ANTI-CIRCULARITY (same discipline as results/matter/, even though the guard does not
scan results/phi_emerge/):
  * NO Python complex numbers.  Phi is stored as TWO REAL arrays (Re, Im); every
    correlator is built from real cos/sin sums.  arg(Phi)=phibar uses a CIRCULAR mean
    (atan2 of summed sin/cos of the incident link phases) so it is well-defined on the
    phase circle -- still real arithmetic, no 1j.
  * rho_i is COUNTED from a Poisson sprinkling (no formula); phibar_i is read from the
    existing gauge links; nothing relativistic, no mc^2, no v inserted.
  * "Higgs", "condensate", "Meissner" appear as NAMES only; any DEV / abelian-Higgs
    number is a COMPARISON, never an input.

Geometry: reuses cr3d_core's 3+1D lattice (x Dirichlet ends, y,z periodic), its gauge
links phix/phiy/phiz, evolution, vortex/monopole constructors, and causal_core's 4D
Poisson sprinkler.  Modifies neither.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
for sub in ("src", "results/matter/cr_3d", "results/matter/cr_dbi"):
    sys.path.insert(0, str(ROOT / sub))
import causal_core as cc      # noqa: E402  (4D Poisson sprinkle)
import cr3d_core as c3        # noqa: E402  (3+1D gauge lattice, evolution, vortices)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)
TWO_PI = 2.0 * np.pi


# =========================================================================== #
# grid (unit spacing; x Dirichlet, y,z periodic) -- matches crahiggs geometry
# =========================================================================== #
def make_grid(Nx=33, Ny=24, Nz=24):
    x = np.arange(Nx, dtype=float)
    y = np.arange(Ny, dtype=float)
    z = np.arange(Nz, dtype=float)
    return x, y, z, 1.0


# =========================================================================== #
# (A) |Phi| = rho  -- the local causal density, COUNTED from a 4D sprinkle
# =========================================================================== #
def causal_density(Nx, Ny, Nz, rho_sprinkle, T, rng, return_counts=False):
    """Poisson-sprinkle a 4D box [0,T] x [0,Nx-1] x [0,Ny-1] x [0,Nz-1] at intensity
    ``rho_sprinkle`` (events per unit 4-volume), assign each event to its nearest
    SPATIAL lattice node (Voronoi cell; y,z periodic), count N_i, and return the
    normalised density rho_i = N_i / <N>.  The time axis is integrated (events are
    counted regardless of t), so rho_i is the per-node causal-event density.

    No formula: rho_i is a pure count.  <N> = mean over ALL nodes (the Poisson mean), so
    rho_i fluctuates about 1 in the vacuum and -> 1 with vanishing relative spread as
    rho_sprinkle grows."""
    bounds = [(0.0, T), (-0.5, Nx - 0.5), (-0.5, Ny - 0.5), (-0.5, Nz - 0.5)]
    pts = cc.sprinkle_box(rho_sprinkle, bounds, rng)
    counts = np.zeros((Nx, Ny, Nz))
    if len(pts):
        ix = np.clip(np.rint(pts[:, 1]).astype(int), 0, Nx - 1)
        iy = np.mod(np.rint(pts[:, 2]).astype(int), Ny)      # periodic y
        iz = np.mod(np.rint(pts[:, 3]).astype(int), Nz)      # periodic z
        np.add.at(counts, (ix, iy, iz), 1.0)
    mean_N = counts.mean() if counts.mean() > 0 else 1.0
    rho = counts / mean_N
    if return_counts:
        return rho, counts, mean_N
    return rho


# =========================================================================== #
# (B) arg(Phi) = phibar  -- circular mean of incident gauge link phases
# =========================================================================== #
def _incident_link_phases(phix, phiy, phiz):
    """Return a list of (phase_array, valid_mask) for every link incident on each node.

    x links: outgoing phix[i] (i<Nx-1), incoming phix[i-1] (i>0).
    y,z links (periodic): outgoing phi*, incoming roll(phi*, +1).
    """
    Nx = phix.shape[0]
    out = []
    # outgoing x (node i uses phix[i]; invalid at i=Nx-1)
    ox = phix.copy(); vox = np.ones_like(phix, bool); vox[-1] = False
    out.append((ox, vox))
    # incoming x (node i uses phix[i-1]; invalid at i=0)
    ix = np.zeros_like(phix); ix[1:] = phix[:-1]
    vix = np.ones_like(phix, bool); vix[0] = False
    out.append((ix, vix))
    # y periodic
    out.append((phiy, np.ones_like(phiy, bool)))
    out.append((np.roll(phiy, +1, axis=1), np.ones_like(phiy, bool)))
    # z periodic
    out.append((phiz, np.ones_like(phiz, bool)))
    out.append((np.roll(phiz, +1, axis=2), np.ones_like(phiz, bool)))
    return out


def phibar(phix, phiy, phiz):
    """Circular mean of the incident link phases at each node (real arithmetic):
    phibar_i = atan2( sum sin phi_inc , sum cos phi_inc ).  Also returns deg_i."""
    inc = _incident_link_phases(phix, phiy, phiz)
    S = np.zeros_like(phix); Cc = np.zeros_like(phix); deg = np.zeros_like(phix)
    for ph, valid in inc:
        S += np.where(valid, np.sin(ph), 0.0)
        Cc += np.where(valid, np.cos(ph), 0.0)
        deg += valid.astype(float)
    pb = np.arctan2(S, Cc)
    return pb, deg


# =========================================================================== #
# (C) Phi = rho e^{i phibar}  as two REAL arrays
# =========================================================================== #
def phi_field(rho, pb):
    """Return (Re, Im) = (rho cos phibar, rho sin phibar).  No complex literal."""
    return rho * np.cos(pb), rho * np.sin(pb)


def phi_abs(Re, Im):
    return np.sqrt(Re ** 2 + Im ** 2)


def phi_arg(Re, Im):
    return np.arctan2(Im, Re)


# =========================================================================== #
# (D) correlators  (radial; real arithmetic)
# =========================================================================== #
def _radial_pairs(shape, r_edges, periodic=(False, True, True), max_pairs=200000,
                  rng=None):
    """Precompute index pairs binned by separation r for a lattice of given shape.
    Returns list of (idxA, idxB) arrays per radial bin.  Subsamples to max_pairs/bin."""
    Nx, Ny, Nz = shape
    rng = rng or np.random.default_rng(0)
    coords = np.array(np.meshgrid(np.arange(Nx), np.arange(Ny), np.arange(Nz),
                                  indexing="ij")).reshape(3, -1).T
    n = coords.shape[0]
    # sample random ordered pairs, compute separation with periodic y,z
    nsamp = min(max_pairs * (len(r_edges) - 1), 6_000_000)
    a = rng.integers(0, n, nsamp); b = rng.integers(0, n, nsamp)
    d = coords[b] - coords[a]
    if periodic[1]:
        d[:, 1] = (d[:, 1] + Ny // 2) % Ny - Ny // 2
    if periodic[2]:
        d[:, 2] = (d[:, 2] + Nz // 2) % Nz - Nz // 2
    r = np.sqrt(np.sum(d.astype(float) ** 2, axis=1))
    bins = []
    for k in range(len(r_edges) - 1):
        sel = (r >= r_edges[k]) & (r < r_edges[k + 1])
        ia, ib = a[sel], b[sel]
        if ia.size > max_pairs:
            pick = rng.choice(ia.size, max_pairs, replace=False)
            ia, ib = ia[pick], ib[pick]
        bins.append((ia, ib))
    centers = 0.5 * (r_edges[:-1] + r_edges[1:])
    return coords, bins, centers


def precompute_pairs(shape, r_edges, max_pairs=40000, rng=None):
    """Precompute (bins, centers) ONCE for a (shape, r_edges); reuse across seeds to
    avoid the O(samples) pair sampling on every call."""
    _, bins, centers = _radial_pairs(shape, r_edges, max_pairs=max_pairs, rng=rng)
    return bins, centers


def correlation_full(Re, Im, r_edges, connected=True, rng=None, pairs=None):
    """C(r) = <Phi*(0) Phi(r)> radially.  Real part = <Re Re + Im Im>, plus the magnitude
    of the complex correlator |<Phi* Phi(r)>| (built from real sums).  If connected,
    subtract the field mean first.  Returns dict with centers, C_real, C_abs."""
    shape = Re.shape
    reF = Re - Re.mean() if connected else Re
    imF = Im - Im.mean() if connected else Im
    if pairs is not None:
        bins, centers = pairs
    else:
        _, bins, centers = _radial_pairs(shape, r_edges, rng=rng)
    rf = reF.ravel(); imf = imF.ravel()
    C_real, C_abs = [], []
    for ia, ib in bins:
        if ia.size == 0:
            C_real.append(np.nan); C_abs.append(np.nan); continue
        # Phi*(a) Phi(b) = (re_a - i im_a)(re_b + i im_b)
        cr = rf[ia] * rf[ib] + imf[ia] * imf[ib]       # real part
        ci = rf[ia] * imf[ib] - imf[ia] * rf[ib]       # imag part
        mr, mi = cr.mean(), ci.mean()
        C_real.append(float(mr))
        C_abs.append(float(np.hypot(mr, mi)))
    return {"centers": centers.tolist(), "C_real": C_real, "C_abs": C_abs}


def correlation_magnitude(rho, r_edges, rng=None, pairs=None):
    """Connected magnitude correlator C_|Phi|(r) = <drho(0) drho(r)> / <drho^2>,
    normalised so C(0)->1.  Tests whether the MAGNITUDE develops long-range order."""
    shape = rho.shape
    d = rho - rho.mean()
    var = float((d ** 2).mean())
    if pairs is not None:
        bins, centers = pairs
    else:
        _, bins, centers = _radial_pairs(shape, r_edges, rng=rng)
    df = d.ravel()
    C = []
    for ia, ib in bins:
        if ia.size == 0:
            C.append(np.nan); continue
        C.append(float((df[ia] * df[ib]).mean() / var) if var > 0 else np.nan)
    return {"centers": centers.tolist(), "C_norm": C, "var": var}


def gauge_correlator(pb, r_edges, rng=None, pairs=None):
    """Phase two-point function G(r) = <cos(phibar(0) - phibar(r))> radially.  For a
    massive gauge field G(r) ~ e^{-m_A r}; fit gives m_A.  Real arithmetic."""
    shape = pb.shape
    c = np.cos(pb).ravel(); s = np.sin(pb).ravel()
    if pairs is not None:
        bins, centers = pairs
    else:
        _, bins, centers = _radial_pairs(shape, r_edges, rng=rng)
    G = []
    for ia, ib in bins:
        if ia.size == 0:
            G.append(np.nan); continue
        # cos(a-b) = cos a cos b + sin a sin b
        G.append(float((c[ia] * c[ib] + s[ia] * s[ib]).mean()))
    return {"centers": centers.tolist(), "G": G}


def fit_mass(centers, G, r_lo=1.0, r_hi=None):
    """Fit log|G| = const - m_A r on r in [r_lo, r_hi]; return m_A and r2."""
    centers = np.asarray(centers, float); G = np.asarray(G, float)
    if r_hi is None:
        r_hi = centers.max()
    use = (centers >= r_lo) & (centers <= r_hi) & (G > 0) & np.isfinite(G)
    if use.sum() < 3:
        return float("nan"), float("nan")
    p = np.polyfit(centers[use], np.log(G[use]), 1)
    pred = np.polyval(p, centers[use])
    ss_res = np.sum((np.log(G[use]) - pred) ** 2)
    ss_tot = np.sum((np.log(G[use]) - np.log(G[use]).mean()) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan
    return float(-p[0]), float(r2)


# =========================================================================== #
# (E) gauge configurations (reuse cr3d) + a relaxer
# =========================================================================== #
def hot_gauge(x, y, z, rng, scale=np.pi):
    """Disordered compact-U(1) vacuum (cr3d.random_gauge)."""
    return c3.random_gauge(x, y, z, rng, scale=scale)


def relax_gauge(phix, phiy, phiz, dx, lam, n_relax=800, friction=0.05, density=1.0):
    """Cool the gauge field toward the (massive) vacuum with theta frozen at 0.

    ``density`` multiplies the Stueckelberg link stiffness (the minimal action's Dtau
    weight is proportional to the local causal density): a denser network has a stiffer
    cosine coupling, so the gauge mass scales with density.  Implemented by scaling dt
    so the effective coupling per step tracks the weight, leaving cr3d's force intact."""
    sh = phix.shape
    z0 = [np.zeros(sh) for _ in range(8)]
    theta, vth = z0[0], z0[1]
    dt = c3.dt_cfl(dx) / np.sqrt(max(density, 1e-6))
    out = c3.evolve(theta, vth, phix.copy(), np.zeros(sh), phiy.copy(), np.zeros(sh),
                    phiz.copy(), np.zeros(sh), dx, dt, n_relax, lam=lam,
                    freeze_theta=True, friction=friction)
    return out[2], out[4], out[6]      # phix, phiy, phiz


def vortex_gauge(x, y, z, n_wind=1):
    """A single winding-n gauge vortex line along z (phase winds in the xy plane), built
    as the wrapped lattice gradient of the multivalued angle -- reuses the construction
    style of cr3d.monopole_pair / crahiggs.vortex_state.  Returns (phix,phiy,phiz,(xc,yc))."""
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    xc = float(x[len(x) // 2]) + 0.5
    yc = float(y[len(y) // 2]) + 0.5
    ang = np.arctan2(Y - yc, X - xc) * n_wind
    phix = np.zeros_like(ang); phiy = np.zeros_like(ang); phiz = np.zeros_like(ang)
    phix[:-1] = c3._wrap(np.diff(ang, axis=0))
    phiy[:] = c3._wrap(c3._up_y(ang) - ang)
    phix[0] = phix[-1] = 0.0
    return phix, phiy, phiz, (xc, yc)


def core_width(rho, x, y, xc, yc, level):
    """Transverse RMS width of the region where rho dips below ``level`` (averaged over
    z), weighting by the deficit (level - rho)+.  NaN if no dip."""
    rho2d = rho.mean(axis=2)
    X, Y = np.meshgrid(x, y, indexing="ij")
    w = np.clip(level - rho2d, 0.0, None)
    W = float(w.sum())
    if W < 1e-9:
        return float("nan")
    r2 = (X - xc) ** 2 + (Y - yc) ** 2
    return float(np.sqrt((w * r2).sum() / W))


def save_json(name, payload):
    (OUTDIR / f"{name}.json").write_text(json.dumps(payload, indent=2))
    return OUTDIR / f"{name}.json"


if __name__ == "__main__":
    rng = np.random.default_rng(0)
    x, y, z, dx = make_grid(Nx=25, Ny=16, Nz=16)
    Nx, Ny, Nz = len(x), len(y), len(z)

    # smoke 1: causal density is positive, mean ~1, fluctuates
    rho, counts, meanN = causal_density(Nx, Ny, Nz, rho_sprinkle=4.0, T=8.0,
                                        rng=rng, return_counts=True)
    print(f"causal density: <N>={meanN:.2f}  <rho>={rho.mean():.3f}  "
          f"std(rho)={rho.std():.3f}  frac(rho=0)={np.mean(rho == 0):.3f}")

    # smoke 2: phibar well-defined; hot vacuum -> uniform arg
    phix, phiy, phiz = hot_gauge(x, y, z, rng)
    pb, deg = phibar(phix, phiy, phiz)
    print(f"phibar: range[{pb.min():+.2f},{pb.max():+.2f}]  deg in "
          f"[{deg.min():.0f},{deg.max():.0f}]  mean|sin|var check std(pb)={pb.std():.3f}")

    # smoke 3: Phi as two real arrays, |Phi| ~ rho
    Re, Im = phi_field(rho, pb)
    print(f"|Phi| matches rho: max|abs-rho|={np.max(np.abs(phi_abs(Re, Im) - rho)):.2e}")

    # smoke 4: correlators run
    r_edges = np.arange(0.5, Ny // 2, 1.0)
    cm = correlation_magnitude(rho, r_edges, rng=rng)
    gg = gauge_correlator(pb, r_edges, rng=rng)
    mA, r2 = fit_mass(gg["centers"], gg["G"], r_lo=1.0, r_hi=5.0)
    print(f"C_|Phi|(r) first 3: {[round(v,3) for v in cm['C_norm'][:3]]}  "
          f"(decays => no magnitude order)")
    print(f"gauge G(r) first 3: {[round(v,3) for v in gg['G'][:3]]}  m_A(fit)={mA:.3f} "
          f"r2={r2:.3f}")
