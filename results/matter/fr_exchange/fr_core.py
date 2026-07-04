"""fr_core.py -- shared helpers for MATTER_FR_EXCHANGE (FR1-FR4).

Two-Skyrmion product configurations evaluated ANALYTICALLY at arbitrary
(possibly rotated/translated) coordinates -- no interpolation, so the exact
identities (FR2, FR3) can be tested at machine precision. Quaternion engine
from su2_core (real arithmetic; no Pauli, no complex).
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
import su2_core as s2  # noqa: E402

OUT = Path(__file__).resolve().parent
L_BOX = 24.0
N_GRID = 61
PROFILE_W = 2.0          # F(r) = pi exp(-r / PROFILE_W)


def grid():
    x = np.linspace(-L_BOX / 2, L_BOX / 2, N_GRID)
    dx = float(x[1] - x[0])
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    return X, Y, Z, dx


def hedgehog_at(X, Y, Z, center):
    """U0(x - c) = (cos F, sin F rhat) evaluated analytically at given coords."""
    cx, cy, cz = center
    Xr, Yr, Zr = X - cx, Y - cy, Z - cz
    r = np.sqrt(Xr ** 2 + Yr ** 2 + Zr ** 2)
    rs = np.where(r > 0, r, 1.0)
    F = np.pi * np.exp(-r / PROFILE_W)
    U = np.empty(X.shape + (4,))
    U[..., 0] = np.cos(F)
    sinF = np.sin(F)
    U[..., 1] = sinF * Xr / rs
    U[..., 2] = sinF * Yr / rs
    U[..., 3] = sinF * Zr / rs
    U[r == 0, 1:] = 0.0
    U[r == 0, 0] = np.cos(np.pi)        # F(0) = pi
    return s2.q_normalize(U)


def pair(X, Y, Z, c1, c2):
    """Product ansatz U0(x-c1) * U0(x-c2)."""
    return s2.q_mul(hedgehog_at(X, Y, Z, c1), hedgehog_at(X, Y, Z, c2))


def qdist(U, V):
    """Pointwise quaternion distance: max and mean of |U - V| over the grid."""
    d = np.sqrt(np.sum((U - V) ** 2, axis=-1))
    return float(np.max(d)), float(np.mean(d))


def conj_global(U, g):
    """Global isospin conjugation g U g^{-1} (g a single quaternion)."""
    G = np.broadcast_to(g, U.shape).copy()
    return s2.q_mul(s2.q_mul(G, U), s2.q_conj(G))


def save_json(name, payload):
    payload = dict(payload)
    payload["_meta"] = {"campaign": "MATTER_FR_EXCHANGE",
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "numpy": np.__version__,
                        "grid": N_GRID, "L_box": L_BOX, "profile_w": PROFILE_W}
    (OUT / name).write_text(json.dumps(payload, indent=2))
