"""sc_core.py -- shared helpers for the BRIDGE_SU2_COEFF campaign (SC1-SC5).

Tests whether the Skyrme quartic emerges from coarse-graining the SU(2) link
cosine on a Poisson (isotropic) link measure, against the cubic-lattice control.

Anti-circularity: pure real arithmetic (quaternions from su2_core; cos/sin).
No complex numbers, no Pauli matrices, no dilation formula. The Skyrme operator
is NEVER inserted as a fit target: SC2 measures the quartic residual first and
compares against the pre-registered prediction afterwards.

Conventions (see BRIDGE_SU2_COEFF.md, technical addendum):
  * currents matrix C: rows = spatial directions mu (3), cols = isospin a (3);
    c_mu = C[mu] is the su(2) current 3-vector in direction mu.
  * link of length ``a_link`` in unit spatial direction e: holonomy
    Omega = exp(a L_e), L_e = i (e.C).sigma/2, i.e. the engine quaternion
    q_from_axis_angle(axis = e.C, angle = a_link*|e.C|/2);
    link energy = 1 - half_trace(Omega) = 1 - cos(a_link |e.C| / 2).
  * invariants of G = C C^T:  S = (Tr G)^2  (symmetric quartic),
    K = (Tr G)^2 - Tr(G^2) = sum_{mu,nu} |c_mu x c_nu|^2   (Skyrme operator).
"""

from __future__ import annotations

import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s2  # noqa: E402

OUTDIR = Path(__file__).resolve().parent


# ---- direction measures ----------------------------------------------------- #
def isotropic_directions(n, rng):
    """n unit 3-vectors, exactly isotropic (the spatial direction statistics of
    links in a Poisson sprinkling: positions uniform in a ball -> directions
    uniform on S^2)."""
    v = rng.standard_normal((n, 3))
    return v / np.linalg.norm(v, axis=1, keepdims=True)


CUBIC_AXES = np.eye(3)   # the 3 forward lattice axes (the grid's link measure)


# ---- constant-current configurations (SC2) ---------------------------------- #
def config_A(g=1.0):
    """Abelian-like: all currents parallel in isospace (K = 0), S matched to B.
    c_x = c_y = c_z = g*(1,0,0)."""
    C = np.zeros((3, 3))
    C[:, 0] = g
    return C


def config_B(g=1.0):
    """Hedgehog-like: orthogonal currents (maximal K at matched S).
    c_x = g*x_hat, c_y = g*y_hat, c_z = g*z_hat."""
    return g * np.eye(3)


def invariants(C):
    """S = (TrG)^2, K = (TrG)^2 - Tr(G^2), with G = C C^T."""
    G = C @ C.T
    trG = float(np.trace(G))
    trG2 = float(np.trace(G @ G))
    return trG, trG * trG, trG * trG - trG2     # TrG, S, K


# ---- exact link energy through the SU(2) engine ----------------------------- #
def link_energy(C, dirs, a_link):
    """1 - (1/2)Tr(Omega) per link, computed through su2_core quaternions.

    dirs: (N,3) unit directions; returns (N,) energies."""
    l_e = dirs @ C                                  # (N,3) su(2) vectors
    mag = np.linalg.norm(l_e, axis=1)
    omega = s2.q_from_axis_angle(l_e, 0.5 * a_link * mag)
    return 1.0 - s2.half_trace(omega)


def quartic_residual(C, dirs, a_link):
    """Per-link quartic residual: [E_link - exact quadratic term] averaged.

    quadratic term per link = a^2 |l_e|^2 / 8 (same sampled directions, so the
    subtraction is exact sample-by-sample; only the quartic average fluctuates)."""
    l_e = dirs @ C
    mag2 = np.sum(l_e * l_e, axis=1)
    e_full = link_energy(C, dirs, a_link)
    return float(np.mean(e_full - (a_link ** 2 / 8.0) * mag2))


# ---- bookkeeping ------------------------------------------------------------- #
def seed_stats(values):
    v = np.asarray(values, dtype=float)
    return {"mean": float(np.mean(v)), "sem": float(np.std(v, ddof=1) / np.sqrt(len(v))),
            "n_seeds": int(len(v))}


def save_json(name, payload):
    payload = dict(payload)
    payload["_meta"] = {
        "campaign": "BRIDGE_SU2_COEFF",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0],
        "numpy": np.__version__,
        "platform": platform.platform(),
    }
    path = OUTDIR / name
    path.write_text(json.dumps(payload, indent=2))
    return path
