"""bq_core.py -- shared engine for BARYON_QUANTITATIVE (BQ1-BQ5), RESEARCH_MAP gap #12.

Quantitative collective-coordinate quantization of the B=1 hedgehog Skyrmion.

Q1-Q7 (su2_quant) did the QUALITATIVE job (spin-1/2: ladder shape, FR sign,
degeneracies).  Their moment of inertia I=312.7 is the SIGMA-MODEL PART ONLY (the
zero-mode overlap 2 int xi.xi); the Skyrme 4-derivative term ALSO stiffens the
rotor and is omitted there.  For QUANTITATIVE baryon numbers the full inertia
matters.

This module works in the standard reduced Skyrme units x = e f_pi r, derived from
the Lagrangian
    L = (f_pi^2/16) Tr(L_mu L^mu) + (1/(32 e^2)) Tr([L_mu,L_nu][L^mu,L^nu]),
    L_mu = U^dag d_mu U,  U = cos F + i tau.rhat sin F  (hedgehog, F(0)=pi, F(inf)=0).

Reductions used (all standard, re-derived in BARYON_QUANTITATIVE.md):
  Soliton mass        M     = (pi f_pi/e) * Ehat,
      Ehat = int dx [ (1/2) x^2 F'^2 + sin^2 F + sin^2 F (4 F'^2 + 2 sin^2 F / x^2) ]
  Moment of inertia   Iner  = (2 pi/3)(1/(e^3 f_pi)) * Lhat,
      Lhat = int dx [ x^2 sin^2 F (1 + 4 (F'^2 + sin^2 F / x^2)) ]
                    = int dx [ x^2 sin^2 F + 4 x^2 sin^2 F F'^2 + 4 sin^4 F ]
  Isoscalar <r^2>_B   = (1/(e f_pi)^2) * X2hat,  X2hat = -(2/pi) int dx x^2 sin^2 F F'
  Magnetic moments (ANW): mu_p,mu_n = 2 M_N [ <r^2>_B/(12 Iner) +- Iner/6 ]
      => RATIO mu_p/mu_n = (<r^2>_B + 2 Iner^2)/(<r^2>_B - 2 Iner^2)   (M_N cancels)

The sigma part of Lhat (the "1" term) equals the lattice zero-mode inertia of
su2q_core when rescaled -- this is checked in BQ2.  ANTI-CIRCULARITY: the PROFILE
F(x) is obtained by relaxing the reduced energy here AND independently by
su2_core.radial_relax (the 3D-lattice engine); BQ2 verifies they coincide.  The
ANW current decomposition (isoscalar=baryon current, isovector=iso-Noether) is
imported standard physics (like the FR phase in Q4), declared in the charter.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2"))
sys.path.insert(0, str(ROOT / "results" / "matter" / "su2_quant"))

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

PI = np.pi
HBARC = 197.3269804  # MeV fm


# =========================================================================== #
# Reduced-unit radial profile  F(x),  x = e f_pi r
# =========================================================================== #
def reduced_grid(xmax=25.0, n=2000):
    x = np.linspace(0.0, xmax, n + 1)[1:]      # avoid x=0
    dx = float(x[1] - x[0])
    return x, dx


def reduced_energy_density(F, x, dx):
    """Integrands of Ehat (so Ehat = sum * dx).  Returns (e2hat_sum, e4hat_sum)."""
    Fp = np.gradient(F, dx)
    s2 = np.sin(F) ** 2
    e2 = 0.5 * x ** 2 * Fp ** 2 + s2                       # sigma-model reduced
    e4 = s2 * (4.0 * Fp ** 2 + 2.0 * s2 / x ** 2)          # Skyrme reduced
    return e2, e4


def reduced_mass_integral(F, x, dx):
    e2, e4 = reduced_energy_density(F, x, dx)
    return float(np.sum(e2 + e4) * dx)                     # Ehat


def relax_profile(xmax=25.0, n=2000, F0=None, maxiter=4000):
    """Minimise Ehat with F(0)=pi, F(inf)=0 fixed (L-BFGS-B over interior nodes).
    Mirrors su2_core.radial_relax: F lives on the n grid nodes x (none at r=0);
    node 0 pinned to pi, node -1 pinned to 0, interior = F[1:-1].
    Returns (F, x, dx, Ehat)."""
    from scipy.optimize import minimize

    x, dx = reduced_grid(xmax, n)                           # len(x) = n
    if F0 is None:
        Ffull = PI * np.exp(-x / 2.5)
    else:
        Ffull = F0.copy()
    Ffull[0] = PI
    Ffull[-1] = 0.0

    def assemble(interior):
        F = np.empty_like(x)
        F[0] = PI
        F[-1] = 0.0
        F[1:-1] = interior
        return F

    def obj(interior):
        return reduced_mass_integral(assemble(interior), x, dx)

    res = minimize(obj, Ffull[1:-1], method="L-BFGS-B",
                   options={"maxiter": maxiter, "ftol": 1e-15, "gtol": 1e-12})
    F = assemble(res.x)
    Ehat = reduced_mass_integral(F, x, dx)
    return F, x, dx, Ehat


# =========================================================================== #
# Reduced observables of the relaxed profile
# =========================================================================== #
def inertia_integral(F, x, dx):
    """Lhat = int dx x^2 sin^2 F (1 + 4(F'^2 + sin^2 F/x^2)).
    Returns (Lhat, Lhat_sigma, Lhat_skyrme)."""
    Fp = np.gradient(F, dx)
    s2 = np.sin(F) ** 2
    sig = x ** 2 * s2                                       # the "1" term (sigma)
    sky = 4.0 * (x ** 2 * s2 * Fp ** 2 + s2 ** 2)           # the 4(...) term (Skyrme)
    Lsig = float(np.sum(sig) * dx)
    Lsky = float(np.sum(sky) * dx)
    return Lsig + Lsky, Lsig, Lsky


def baryon_r2_integral(F, x, dx):
    """X2hat = -(2/pi) int dx x^2 sin^2 F F'  (isoscalar baryon mean-square radius,
    reduced).  Also returns the baryon-number check int 4pi r^2 rho_B dr = B."""
    Fp = np.gradient(F, dx)
    s2 = np.sin(F) ** 2
    X2 = -(2.0 / PI) * float(np.sum(x ** 2 * s2 * Fp) * dx)
    # baryon number: B = -(2/pi) int dx sin^2 F F'  = (1/pi)(F - sinF cosF) | pi..0 = 1
    Bnum = -(2.0 / PI) * float(np.sum(s2 * Fp) * dx)
    return X2, Bnum


def axial_integral(F, x, dx):
    """Reduced axial integral D_A used in g_A (best-effort, validated in BQ4).
    ANW: g_A = -(pi/3)(1/e^2) * int dx ( x^2 F' + x sin 2F ).  Returned as D_A."""
    Fp = np.gradient(F, dx)
    return float(np.sum(x ** 2 * Fp + x * np.sin(2.0 * F)) * dx)


# =========================================================================== #
# Physical observables given (f_pi [MeV], e)
# =========================================================================== #
def physical(F, x, dx, f_pi, e):
    """Return a dict of physical baryon observables for given (f_pi, e)."""
    Ehat = reduced_mass_integral(F, x, dx)
    Lhat, Lsig, Lsky = inertia_integral(F, x, dx)
    X2hat, Bnum = baryon_r2_integral(F, x, dx)
    D_A = axial_integral(F, x, dx)

    M_sol = PI * f_pi / e * Ehat                            # MeV
    Iner = (2.0 * PI / 3.0) * Lhat / (e ** 3 * f_pi)        # 1/MeV
    r2_B = X2hat / (e * f_pi) ** 2                          # 1/MeV^2
    r_iso_fm = np.sqrt(r2_B) * HBARC                        # fm

    # rigid rotor: M_N = M_sol + 3/(8 Iner), M_Delta = M_sol + 15/(8 Iner)
    M_N = M_sol + 3.0 / (8.0 * Iner)
    M_D = M_sol + 15.0 / (8.0 * Iner)

    mu_ratio = (r2_B + 2.0 * Iner ** 2) / (r2_B - 2.0 * Iner ** 2)
    # absolute moments in nuclear magnetons need the proton mass conversion;
    # ANW: mu = 2 M_N [ r2_B/(12 Iner) +- Iner/6 ] in units of e/(2 M_N) -> nuclear magn.
    Mp = 938.272
    mu_p = 2.0 * Mp * (r2_B / (12.0 * Iner) + Iner / 6.0)
    mu_n = 2.0 * Mp * (r2_B / (12.0 * Iner) - Iner / 6.0)
    g_A = -(PI / 3.0) * (1.0 / e ** 2) * D_A

    return dict(Ehat=Ehat, Lhat=Lhat, Lsig=Lsig, Lsky=Lsky, X2hat=X2hat, Bnum=Bnum,
                M_sol=M_sol, Iner=Iner, r2_B=r2_B, r_iso_fm=r_iso_fm,
                M_N=M_N, M_D=M_D, M_D_minus_N=M_D - M_N,
                mu_p=mu_p, mu_n=mu_n, mu_ratio=mu_ratio, g_A=g_A,
                skyrme_inertia_frac=Lsky / Lhat)


def calibrate(F, x, dx, M_N_target=939.0, M_D_target=1232.0):
    """Solve (f_pi, e) from the two inputs M_N, M_Delta (ANW procedure).
    M_D - M_N = 3/(2 Iner) = (9/(4 pi)) e^3 f_pi / Lhat  -> gives e^3 f_pi.
    M_N = (pi f_pi/e) Ehat + 3/(8 Iner)                  -> closes the system."""
    Ehat = reduced_mass_integral(F, x, dx)
    Lhat, _, _ = inertia_integral(F, x, dx)
    split = M_D_target - M_N_target
    # 3/(2 Iner) = split ; Iner = (2pi/3) Lhat/(e^3 f_pi)
    # => e^3 f_pi = (2pi/3) Lhat * (2/(3?))... solve directly:
    # split = 3/(2 Iner) = 3 e^3 f_pi / (2 (2pi/3) Lhat) = 9 e^3 f_pi/(4 pi Lhat)
    e3fpi = split * 4.0 * PI * Lhat / 9.0                   # = e^3 f_pi
    # M_N = pi f_pi Ehat / e + split/4   (since 3/(8 Iner) = split/4)
    # let a = f_pi/e ; M_N - split/4 = pi a Ehat -> a = (M_N - split/4)/(pi Ehat)
    a = (M_N_target - split / 4.0) / (PI * Ehat)            # = f_pi/e
    # f_pi = a e  (from a = f_pi/e) ; e3fpi = e^3 f_pi = e^3 (a e) = a e^4
    # => e^4 = e3fpi/a
    e = (e3fpi / a) ** 0.25
    f_pi = a * e
    return f_pi, e


# =========================================================================== #
# IO
# =========================================================================== #
def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    print("bq_core smoke -- reduced profile + ANW validation")
    F, x, dx, Ehat = relax_profile()
    Lhat, Lsig, Lsky = inertia_integral(F, x, dx)
    X2hat, Bnum = baryon_r2_integral(F, x, dx)
    print(f"Ehat={Ehat:.4f}  Lhat={Lhat:.4f} (sigma={Lsig:.3f} skyrme={Lsky:.3f})  "
          f"X2hat={X2hat:.4f}  B(check)={Bnum:.4f}")
    f_pi, e = calibrate(F, x, dx)
    obs = physical(F, x, dx, f_pi, e)
    print(f"calibrated  f_pi={f_pi:.2f} MeV  e={e:.3f}   (ANW: 64.5, 5.45)")
    print(f"M_sol={obs['M_sol']:.1f}  M_N={obs['M_N']:.1f}  M_D={obs['M_D']:.1f}  "
          f"split={obs['M_D_minus_N']:.1f}")
    print(f"mu_p={obs['mu_p']:.3f} (ANW 1.87)  mu_n={obs['mu_n']:.3f} (ANW -1.31)  "
          f"ratio={obs['mu_ratio']:.3f} (ANW -1.43)")
    print(f"r_iso={obs['r_iso_fm']:.3f} fm (ANW 0.59)  g_A={obs['g_A']:.3f} (ANW 0.61)  "
          f"Skyrme inertia frac={obs['skyrme_inertia_frac']:.3f}")
