"""matter_core.py -- shared substrate for the matter experiments M1-P4.

Reimplemented from scratch for the matter campaign (does NOT copy ../TEIC-GE and
does NOT modify R1-R3 / e6-e11 / D1-D3).  It reuses ONLY the bare causal-network
generator in ``src/causal_core.py`` (Poisson sprinkling + light-cone relation).

ANTI-CIRCULARITY (this file is scanned by tests/test_no_circularity.py):
  * No special-/general-relativistic dilation formula anywhere (no sqrt(1-beta^2),
    no Lorentz gamma, no Schwarzschild redshift).  Reference relativity lives in
    src/validation.py and is imported only by COMPARISON blocks of the experiments.
  * No complex numbers (no quantum phase) outside an explicit COMPARISON ONLY block.
  * Mass, energy, momentum, spin, F=ma, E=mc^2, Klein-Gordon, Dirac, Pauli are NEVER
    inserted here; the experiments must MEASURE them from what is defined below.

What IS defined here (all are pure causal-set / geometry objects):
  * Poisson sprinkling in 1+1D / 2+1D (delegated to causal_core).
  * The causal past, and interval-counts, of an event.
  * The SMEARED causal d'Alembertian of Sorkin (2007) / Benincasa-Dowker (2010) --
    the "box" operator on a causal set.  This is a CITED definition, not an ad-hoc
    wave equation.  box theta must EMERGE as its continuum limit; it is not put in.
  * The causal-set retarded propagator K = (1/2) C of Johnston (2008) for the 2D
    massless scalar (continuum retarded Green's function = 1/2 inside the cone).
  * Geometry helpers: a localized real profile, centroid/width, Lorentz boost and
    spatial rotation of coordinates (pure coordinate maps, no dilation factor).
  * Seed statistics (mean +/- std +/- sem) and JSON output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from causal_core import causal_matrix, sprinkle_box  # noqa: E402

OUTDIR = ROOT / "results" / "matter"
OUTDIR.mkdir(parents=True, exist_ok=True)


# --------------------------------------------------------------------------- #
# Sprinkling (thin wrappers over the bare generator)
# --------------------------------------------------------------------------- #
def sprinkle_2d(rho, T, X, rng):
    """Poisson sprinkle in 1+1D box [0,T] x [-X,X].  Returns (n,2) cols (t, x)."""
    return sprinkle_box(rho, [(0.0, T), (-X, X)], rng)


def sprinkle_3d(rho, T, X, rng):
    """Poisson sprinkle in 2+1D box [0,T] x [-X,X]^2.  Returns (n,3) (t, x, y)."""
    return sprinkle_box(rho, [(0.0, T), (-X, X), (-X, X)], rng)


# --------------------------------------------------------------------------- #
# Causal past and interval counts (inputs to the Sorkin operator)
# --------------------------------------------------------------------------- #
def causal_past(pts, i):
    """Indices of events strictly in the causal past of event i (any dim)."""
    p = pts[i]
    dt = p[0] - pts[:, 0]
    dx2 = np.sum((p[1:] - pts[:, 1:]) ** 2, axis=1)
    mask = (dt > 0) & (dt * dt > dx2)
    return np.nonzero(mask)[0]


def interval_counts(pts, P):
    """For each ancestor P_i, the number of P-events strictly between P_i and x.

    Since every event in ``P`` precedes x, this is just how many other ancestors
    P_i precedes.  Vectorised m x m precedence matrix.
    """
    q = pts[P]
    dT = q[None, :, 0] - q[:, None, 0]
    dX2 = np.sum((q[None, :, 1:] - q[:, None, 1:]) ** 2, axis=-1)
    prec = (dT > 0) & (dT * dT > dX2)        # prec[i,j] = P_i precedes P_j
    return prec.sum(axis=1).astype(float)


def smeared_weight(m, eps):
    """Sorkin smeared d'Alembertian layer weight (binomial thinning, retention eps).

        w(m) = (1-eps)^m - 2 m eps (1-eps)^(m-1) + C(m,2) eps^2 (1-eps)^(m-2)

    This is the published weight (Sorkin 2007; Benincasa-Dowker 2010; Aslanbeigi-
    Saravani-Sorkin 2014), NOT an ad-hoc fit.  It alternates sign (positive near
    m=0, negative at intermediate m), which is what makes sum_y w -> 1/(2eps) so the
    operator annihilates constants.
    """
    m = np.asarray(m, dtype=float)
    return ((1 - eps) ** m
            - 2 * m * eps * (1 - eps) ** (m - 1)
            + (m * (m - 1) / 2) * eps ** 2 * (1 - eps) ** (m - 2))


def box_smeared(pts, phi, i, eps):
    """Smeared causal d'Alembertian (box) of field phi at event i (Sorkin/BD).

        B_eps phi(x) = -phi(x) + 2 eps * sum_{y < x} w(m_y) phi(y)

    Continuum limit (rho -> inf) is the flat d'Alembertian box phi = (d_t^2 -
    d_x^2) phi.  It is DERIVED from the causal order; no wave equation is inserted.
    """
    P = causal_past(pts, i)
    if P.size == 0:
        return -phi[i]
    m = interval_counts(pts, P)
    return -phi[i] + 2.0 * eps * float(np.dot(smeared_weight(m, eps), phi[P]))


# --------------------------------------------------------------------------- #
# Causal-set retarded propagator (Johnston 2008), 2D massless scalar
# --------------------------------------------------------------------------- #
def retarded_kernel(pts):
    """K[x,y] = 1/2 if y precedes x, else 0  (Johnston 2008, 2D massless).

    In the continuum the 2D massless retarded Green's function is exactly 1/2
    inside the forward light cone, so K = (1/2) * (causal matrix)^T reproduces it.
    This is a property of the causal order; nothing relativistic is inserted.
    """
    C = causal_matrix(pts)            # C[i,j] = i precedes j
    return 0.5 * C.T.astype(float)    # K[x,y] = 1/2 [y precedes x]


def propagate(pts, source):
    """Retarded response phi = K @ source of a real source on the network."""
    return retarded_kernel(pts) @ np.asarray(source, dtype=float)


# --------------------------------------------------------------------------- #
# Localized real profile and its moments (NO physics inserted -- pure geometry)
# --------------------------------------------------------------------------- #
def localized_profile(x, center, width):
    """A real localized bump exp(-(x-center)^2 / (2 width^2)).  Just a function of
    coordinates: it carries no mass, energy, charge or spin -- those must be
    measured from how the network operator/propagator acts on it."""
    x = np.asarray(x, dtype=float)
    return np.exp(-((x - center) ** 2) / (2.0 * width ** 2))


def centroid(weights, coord):
    """Weight-averaged coordinate (the 'position' of a field lump)."""
    w = np.asarray(weights, dtype=float)
    s = w.sum()
    return float(np.dot(w, coord) / s) if s != 0 else float("nan")


def spread(weights, coord):
    """Weight std of a field lump (its spatial 'width')."""
    w = np.abs(np.asarray(weights, dtype=float))
    s = w.sum()
    if s == 0:
        return float("nan")
    c = np.dot(w, coord) / s
    return float(np.sqrt(np.dot(w, (coord - c) ** 2) / s))


# --------------------------------------------------------------------------- #
# Coordinate maps (pure geometry -- NOT dilation formulas)
# --------------------------------------------------------------------------- #
def boost_2d(pts, rapidity):
    """Active Lorentz boost of 1+1D events by rapidity phi (hyperbolic rotation).

        t' = t cosh phi + x sinh phi ,   x' = x cosh phi + t sinh phi

    This is a coordinate transformation (cosh^2 - sinh^2 = 1), the same pure-
    geometry construction used in e1/R1 Panel B.  It contains NO 1/sqrt(1-beta^2)
    dilation factor; it merely relabels event coordinates.
    """
    pts = np.asarray(pts, dtype=float)
    ch, sh = np.cosh(rapidity), np.sinh(rapidity)
    t, x = pts[:, 0], pts[:, 1]
    out = pts.copy()
    out[:, 0] = ch * t + sh * x
    out[:, 1] = sh * t + ch * x
    return out


def rotate_xy(pts, angle):
    """Rotate the (x, y) spatial plane of 2+1D events by ``angle`` (radians)."""
    pts = np.asarray(pts, dtype=float)
    c, s = np.cos(angle), np.sin(angle)
    out = pts.copy()
    x, y = pts[:, 1], pts[:, 2]
    out[:, 1] = c * x - s * y
    out[:, 2] = s * x + c * y
    return out


# --------------------------------------------------------------------------- #
# Statistics over seeds + IO
# --------------------------------------------------------------------------- #
def seed_stats(values):
    """mean / std / sem of a list of per-seed scalars (NaNs dropped)."""
    a = np.asarray([v for v in values if np.isfinite(v)], dtype=float)
    if a.size == 0:
        return {"mean": float("nan"), "std": float("nan"),
                "sem": float("nan"), "n": 0}
    return {"mean": float(a.mean()), "std": float(a.std(ddof=1) if a.size > 1 else 0.0),
            "sem": float(a.std(ddof=1) / np.sqrt(a.size)) if a.size > 1 else 0.0,
            "n": int(a.size)}


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path
