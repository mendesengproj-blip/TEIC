"""validation.py -- Reference relativistic formulas (COMPARISON ONLY).

This is the ONLY module in src/ allowed to contain special- or general-relativistic
expressions.  Nothing here is ever used to generate causal-network data; it is used
exclusively to compare against what the bare causal counting produces.

Keeping these formulas quarantined here is what makes the anti-circularity test
(tests/test_no_circularity.py) meaningful: if any of these appears in a generator
module, that test fails.
"""

from __future__ import annotations

import numpy as np


# --- Special relativity ---------------------------------------------------- #
def lorentz_proper_time_ratio(beta):
    """tau(beta)/tau(0) = sqrt(1 - beta^2) for a fixed coordinate time separation."""
    return np.sqrt(1.0 - np.asarray(beta, dtype=float) ** 2)


def lorentz_factor(beta):
    """gamma = 1/sqrt(1 - beta^2)."""
    return 1.0 / np.sqrt(1.0 - np.asarray(beta, dtype=float) ** 2)


# --- General relativity (Schwarzschild, c = 1) ----------------------------- #
def schwarzschild_redshift(r, M, G=1.0):
    """Static-observer proper-time rate dtau/dt = sqrt(1 - 2 G M / r)."""
    return np.sqrt(1.0 - 2.0 * G * M / np.asarray(r, dtype=float))


# --- Curved 2D causal-diamond volume (de Sitter / constant R) -------------- #
def volume_curvature_correction(R, tau):
    """Leading curvature correction factor of the 2D causal-diamond volume.

        Vol(tau) = (1/2) tau^2 * [1 - R tau^2 / 24 + O(R^2 tau^4)]

    (Gibbons-Solodukhin 2007; Khetrapal-Surya 2013).  Re-derived symbolically in
    experiments/e4_curvature_analytic.py; this is the reference value.
    """
    return 1.0 - R * np.asarray(tau, dtype=float) ** 2 / 24.0
