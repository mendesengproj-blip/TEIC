"""c3_core.py -- shared helpers for the C3_REGGE_SKYRMIONS campaign.

Charter: C3_REGGE_SKYRMIONS.md (pre-registered).  Asks whether the rotating
Skyrmion of the TEIC SU(2) causal ferromagnet follows a Regge trajectory
m^2 = alpha' J + alpha_0 -- the law obeyed by hadrons (alpha' ~ 0.9 GeV^-2 in
QCD).  The death criterion (pre-registered) is: m^2(J) NOT linear in J -> C.

Engine (UNMODIFIED): su2q_core.py / su2_core.py of the MATTER_SU2 + SU2_QUANT
campaigns supply the classical Skyrmion, its mass E_class, and the rotational
inertia tensor I_ab (the collective-coordinate zero modes).  pi1_core.axial_bn
supplies the B>=2 ansatz.  Nothing in those modules is touched.

The physics being measured here.  Quantising the Skyrmion's orientation (a rigid
rotor on SU(2)=S^3) gives the collective spectrum

    E_J = E_class + J(J+1)/(2 I) ,    J = 0, 1/2, 1, 3/2, 2, ...

and the rest mass of the spinning state is m = E_J (lattice units, c=1), so
m^2(J) = E_J^2.  We FIT m^2 against J (the Regge variable) and against the
Casimir J(J+1) (the rigid-rotor variable) and compare the two fits.  The lattice
energy scale is NOT derived (it is external, like hbar and G), so alpha' is
reported in lattice units only -- the QCD comparison is a dimensionless ratio.

ANTI-CIRCULARITY: E_class and I are real overlap/energy integrals of quaternion
fields (su2_core); "spin J", "Regge", "alpha'", "hadron" are COMPARISON-ONLY
labels of an energy spectrum -- nothing physical is inserted by hand.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

MATTER = Path(__file__).resolve().parents[1]
for sub in ("su2", "su2_quant", "pi1_b2"):
    sys.path.insert(0, str(MATTER / sub))
import su2_core as s          # noqa: E402  (quaternions, energy, baryon, relax)
import su2q_core as q         # noqa: E402  (skyrmion, inertia_tensor, zero modes)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

PI = np.pi

# Pre-registered spin ladder (charter C3-1) and engine parameters (match Q2).
JS = [0.0, 0.5, 1.0, 1.5, 2.0]
E_SK = 4.0
N_GRID = 41
L_BOX = 16.0


# --------------------------------------------------------------------------- #
# Classical Skyrmion + inertia (B=1, reuse the SU2_QUANT engine verbatim)
# --------------------------------------------------------------------------- #
def build_b1(e_sk=E_SK, N=N_GRID, L=L_BOX):
    """Relaxed B=1 hedgehog Skyrmion.  Returns (U0, dx, M, I_tensor, I_mean)."""
    U0, dx, M, E2, E4, xs = q.skyrmion(e_sk=e_sk, N=N, L=L)
    I, _ = q.inertia_tensor(U0, dx)
    return U0, dx, float(M), I, float(np.mean(np.diag(I)))


def measure(U, dx, e_sk=E_SK):
    """(E_class, I_tensor, I_mean) of an arbitrary chiral field U."""
    E2, E4, M = s.chiral_energy(U, dx, e_sk)
    I, _ = q.inertia_tensor(U, dx)
    return float(M), I, float(np.mean(np.diag(I)))


def _smooth(field, passes):
    """Box-blur a (...,4) field by ``passes`` nearest-neighbour averaging sweeps
    over the three spatial axes (a low-pass filter): turns white noise into a
    long-wavelength fluctuation whose gradient (and hence Skyrme) energy is
    finite as dx->0, instead of the UV-divergent ~eps^2/dx^2 of white noise."""
    f = field
    for _ in range(passes):
        acc = f.copy()
        for ax in range(3):
            acc = acc + np.roll(f, 1, axis=ax) + np.roll(f, -1, axis=ax)
        f = acc / 7.0
    return f


def vacuum_perturb(U0, rng, eps, passes=6):
    """Add a small SMOOTH (long-wavelength) tangent vacuum fluctuation to U0.

    White noise on a fine lattice carries UV gradient energy ~eps^2/dx^2 that
    swamps the soliton; a genuine background vacuum fluctuation is long-wavelength,
    so we low-pass the noise (``passes`` box-blurs), renormalise its amplitude to
    ``eps``, project onto the tangent of S^3 at each site, and add.  Models the
    'background vacuum fluctuations' of charter C3-1 (10 seeds): each seed gives a
    slightly different (E_class, I) at a few-percent ΔE, testing whether the
    linearity verdict survives noise."""
    xi = _smooth(rng.standard_normal(U0.shape), passes)
    nrm = np.sqrt(np.mean(np.sum(xi * xi, axis=-1)))
    xi = eps * xi / max(nrm, 1e-300)
    xi = xi - np.sum(xi * U0, axis=-1, keepdims=True) * U0   # tangent projection
    return s.q_normalize(U0 + xi)


# --------------------------------------------------------------------------- #
# Rotational spectrum and the two competing fits
# --------------------------------------------------------------------------- #
def spectrum(E_class, I_mean, Js=JS):
    """Rigid-rotor masses m_J = E_class + J(J+1)/(2 I) (lattice units, c=1)."""
    Js = np.asarray(Js, float)
    E_J = E_class + Js * (Js + 1.0) / (2.0 * I_mean)
    return E_J


def linfit(x, y):
    """Least-squares y = a*x + b.  Returns dict(slope, intercept, r2, resid)."""
    x = np.asarray(x, float); y = np.asarray(y, float)
    A = np.vstack([x, np.ones_like(x)]).T
    (a, b), *_ = np.linalg.lstsq(A, y, rcond=None)
    yhat = a * x + b
    ss_res = float(np.sum((y - yhat) ** 2))
    ss_tot = float(np.sum((y - np.mean(y)) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0
    return {"slope": float(a), "intercept": float(b), "r2": float(r2),
            "resid": (y - yhat).tolist(), "ss_res": ss_res, "ss_tot": ss_tot}


def regge_analysis(E_class, I_mean, Js=JS):
    """Build the spectrum and fit m^2 against BOTH J and the Casimir J(J+1).

    Returns a dict with the masses, m^2, both fits, and the fitted Casimir slope
    alpha'_C = d(m^2)/d[J(J+1)] (the lattice-unit 'Regge-like' slope of the
    rigid rotor)."""
    Js = np.asarray(Js, float)
    cas = Js * (Js + 1.0)
    E_J = spectrum(E_class, I_mean, Js)
    m2 = E_J ** 2
    fit_J = linfit(Js, m2)            # the Regge hypothesis: m^2 linear in J
    fit_cas = linfit(cas, m2)         # the rigid-rotor law: m^2 linear in J(J+1)
    return {"Js": Js.tolist(), "casimir": cas.tolist(),
            "E_J": E_J.tolist(), "m2": m2.tolist(),
            "fit_vs_J": fit_J, "fit_vs_casimir": fit_cas,
            "alpha_casimir": fit_cas["slope"], "E_class": float(E_class),
            "I_mean": float(I_mean)}
