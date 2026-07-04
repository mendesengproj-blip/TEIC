"""bd_core.py -- Benincasa-Dowker SMEARED second moment, general dimension.

BRIDGE/BD investigation.  Independent of R1-R3, e6-e11; modifies nothing.  Continues
BRIDGE_WILSON.md, whose W2 found the emergent F^2 is Lorentz-violating (E/B~3) -- the
same anisotropy as C1 (a_t/a_x~3.4).

THE MECHANISM (why this can work).  The sharp action S=sum_links Dtau[1-cos] is a sum
of POSITIVE terms, so its second moment M2 = <Dtau e^mu e^nu> is positive-definite and
can NEVER equal g^{mu nu} (indefinite).  The Benincasa-Dowker smeared weight w(m)
(Sorkin 2007; Aslanbeigi-Saravani-Sorkin 2014; identical to experiments/e10) ALTERNATES
SIGN with the interval count m -- and an alternating weight CAN give an indefinite form.
The smeared second moment is exactly the d'Alembertian's leading tensor:

   B_eps theta(x) = -theta(x) + 2 eps sum_{y<x} w(m_y) theta(y),
   theta(y) = theta(x) - e^mu d_mu theta + (1/2) e^mu e^nu d_mu d_nu theta + ...,
   =>  the d_mu d_nu coefficient is   M2_BD^{mu nu} = sum_{y<x} 2 eps w(m_y) e^mu e^nu,
       e = x - y  (future-pointing).

BD theory says B_eps -> box = d_t^2 - d_x^2 - ..., so M2_BD should -> g^{mu nu}
(Lorentzian: time-time and space-space OPPOSITE sign), versus the sharp M2 (both same
sign, Euclidean).  This module measures M2_BD in any dimension and the gauge analogue.

ANTI-CIRCULARITY.  w(m) and (1,-2,1) are the DEFINITION of the BD operator (cited), not
a fit; no Lorentz/dispersion formula in any generator.  The signature restoration must
EMERGE.  m is the bias-variance knob discussed in e10 (small eps damps variance; the
continuum/Lorentz limit is eps*rho -> infinity).
"""
from __future__ import annotations

import numpy as np


def smeared_weight(m, eps):
    """BD binomial-thinning weight (identical to experiments/e10.smeared_weight).
    Alternates sign: w>0 near m=0, w<0 at intermediate m. (eps<1.)"""
    m = np.asarray(m, float)
    return ((1 - eps) ** m
            - 2 * m * eps * (1 - eps) ** (m - 1)
            + (m * (m - 1) / 2) * eps ** 2 * (1 - eps) ** (m - 2))


def causal_past_idx(pts, xi):
    """Indices of events strictly in the causal past of pts[xi] (any dimension)."""
    d = pts[xi] - pts                       # x - y ; past => dt>0, timelike
    dt = d[:, 0]
    dx2 = np.sum(d[:, 1:] ** 2, axis=1)
    return np.nonzero((dt > 0) & (dt * dt > dx2))[0]


def interval_counts(pts, P):
    """m_i = #events of P strictly between P_i and x (= #P_j that P_i precedes).
    Vectorised prec matrix over the past set P (any dimension)."""
    q = pts[P]
    dT = q[None, :, 0] - q[:, None, 0]
    dX2 = np.sum((q[None, :, 1:] - q[:, None, 1:]) ** 2, axis=-1)
    prec = (dT > 0) & (dT * dT > dX2)       # prec[i,j] = P_i precedes P_j
    return prec.sum(axis=1).astype(float)


def bd_link_second_moment(pts, eps, base_idx):
    """M2_BD^{mu nu} = sum_{y<x} 2 eps w(m_y) e^mu e^nu, averaged over base events x.
    Also returns the SHARP positive-weight moment over the same pasts (Dtau weight),
    which is positive-definite by construction -- the Euclidean control."""
    D = pts.shape[1]
    M_bd = np.zeros((D, D))
    M_sharp = np.zeros((D, D))
    n_pairs = 0
    used = 0
    for xi in base_idx:
        P = causal_past_idx(pts, xi)
        if P.size < 4:
            continue
        m = interval_counts(pts, P)
        w = smeared_weight(m, eps)
        e = pts[xi] - pts[P]                # (|P|, D), future-pointing
        dtau = np.sqrt(np.maximum(e[:, 0] ** 2 - np.sum(e[:, 1:] ** 2, axis=1), 0.0))
        ee = e[:, :, None] * e[:, None, :]  # (|P|, D, D)
        M_bd += np.tensordot(2 * eps * w, ee, axes=(0, 0))
        M_sharp += np.tensordot(dtau, ee, axes=(0, 0))
        n_pairs += P.size
        used += 1
    if used:
        M_bd /= used
        M_sharp /= used
    return M_bd, M_sharp, used, n_pairs


def signature(M):
    """Diagonal time/space entries and the Lorentzian test (opposite signs)."""
    M = np.asarray(M, float)
    D = M.shape[0]
    a_t = float(M[0, 0])
    a_x = float(np.mean([M[k, k] for k in range(1, D)]))
    eig = np.linalg.eigvalsh(M)
    n_pos = int(np.sum(eig > 0)); n_neg = int(np.sum(eig < 0))
    return {
        "a_t": a_t, "a_x": a_x,
        "opposite_signs_lorentzian": bool(a_t * a_x < 0),
        "ratio_at_over_ax": float(a_t / a_x) if a_x != 0 else np.inf,
        "eigsigns_pos": n_pos, "eigsigns_neg": n_neg,
        "indefinite": bool(n_pos > 0 and n_neg > 0),
    }
