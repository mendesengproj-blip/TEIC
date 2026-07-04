"""volume.py -- The "volume" (expansion) formulation of proper time.

Proper time estimated from the number N of events in an Alexandrov interval:

    tau = (k_d * N / rho)^(1/d)

with the flat-space causal-diamond volume coefficients
    d = 2 :  Vol2 = (1/2)  tau^2          -> k_2 = 2
    d = 4 :  Vol4 = (pi/24) tau^4         -> k_4 = 24/pi

These coefficients are pure geometry of the flat causal diamond; they contain no
dilation formula, so they belong in the generator.  (The derivation/units are
re-verified symbolically in experiments/e2 and analytically in e4.)
"""

from __future__ import annotations

import numpy as np

# Flat-space inversion constants k_d such that tau = (k_d * N / rho)**(1/d).
K_D = {2: 2.0, 4: 24.0 / np.pi}


def tau_from_count(N, rho, d):
    """Volume-formulation proper-time estimator from a causal-interval count."""
    if d not in K_D:
        raise ValueError(f"no volume constant for d={d}; have {sorted(K_D)}")
    return (K_D[d] * N / rho) ** (1.0 / d)


def diamond_volume(tau, d):
    """Flat causal-diamond volume for proper time tau in d spacetime dimensions."""
    if d == 2:
        return 0.5 * tau ** 2
    if d == 4:
        return (np.pi / 24.0) * tau ** 4
    raise ValueError(f"no volume formula for d={d}")
