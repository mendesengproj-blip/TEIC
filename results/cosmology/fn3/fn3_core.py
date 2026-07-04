"""fn3_core.py -- relic-density engine for FN3_RELIC_DENSITY.

DATA GENERATOR for the FN3 campaign ("how much m_A is there today?").  Contains NO
cosmology verdict: "is dark matter"/"derives the abundance" live only in the .md
syntheses (COMPARISON ONLY).  Picks up where FM4 stopped: FM4-1 showed the massive
sector is COLD (w->0, rho~a^-3); FN3 computes the misalignment RELIC DENSITY and
asks whether Omega_{m_A} h^2 ~ 0.12 for (m_A, f_A) in the Paper II window.

It knows:

  * the misalignment relic via the standard ULDM closed form (prompt FN3-1 step 3)
    Omega h^2 = 0.12 (m/1e-22 eV)^1/2 (f_A/1e17 GeV)^2 ;

  * a FIRST-PRINCIPLES entropy-conserving relic (rho_osc = 1/2 m^2 f_A^2 diluted by
    a^-3 from oscillation onset 3H=m to today, with relativistic d.o.f. g_*) as an
    independent analytic cross-check of the closed form;

  * the NUMERICAL misalignment oscillator phi''+3H phi'+m^2 phi=0 integrated across
    onset in a realistic FRW background (radiation+matter+Lambda, Omega_r FIXED by
    T_CMB), from which rho_phi a^3 plateaus to the conserved comoving relic and gives
    Omega_{m_A} h^2 directly (FN3-2) -- removes the onset-definition O(1) ambiguity;

  * the ULDM Jeans / half-mode scale and the FM4 Lyman-alpha suppression numbers,
    reused for the FN3-4 constraint map.

Anti-circularity: m_A and f_A are the Paper II / lattice inputs (galaxies/stability,
NOT a CMB fit); the relic comes from the field dynamics; Omega_DM h^2=0.12 and the
Lyman-alpha bound are COMPARISON ONLY.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

# ---------------------------------------------------------------------------- #
# constants (standard cosmology fixed by the charter; nothing fit to CMB)
# ---------------------------------------------------------------------------- #
HBAR_EV_S = 6.582119569e-16          # eV*s
MPC_M = 3.0856775815e22              # m
C_SI = 2.99792458e8                  # m/s
M_PL_GEV = 1.220910e19               # non-reduced Planck mass (GeV)
GEV_PER_EV = 1e-9                     # 1 eV in GeV
EV4_PER_GEV4 = 1e36                   # (1 GeV)^4 in eV^4
GEVCM3_PER_GEV4 = 1.301e41           # 1 GeV^4 = 1.301e41 GeV/cm^3  (= 1/(hbar c)^3)

# charter cosmology
H0_KMSMPC = 67.0
H_LITTLE = H0_KMSMPC / 100.0         # h = 0.67
OMEGA_M = 0.30
T_CMB_K = 2.725                      # K
T_CMB_EV = 2.348e-4                  # 2.725 K in eV (k_B T)
G_STAR = 106.75                      # relativistic d.o.f. (charter input)
G_STAR_S0 = 3.909                    # entropy d.o.f. today (photons + neutrinos)
OMEGA_DM_H2 = 0.12                   # observed DM density (COMPARISON ONLY)
Z_EQ = 3400.0                        # matter-radiation equality

# Paper II vector mass window (SPARC + GW170817; CLAUDE.md DEV)
M_A_FLOOR = 3.7e-25                  # eV (Paper II lower bound, K=1)
M_A_CEIL = 1.2e-22                   # eV (GW170817 upper bound)

# derived: H0 in eV, critical density today in eV^4
H0_INV_S = H0_KMSMPC * 1e3 / MPC_M               # 1/s
H0_EV = H0_INV_S * HBAR_EV_S                      # eV  (~1.43e-33)
# rho_crit,0 / h^2 = 1.0537e-5 GeV/cm^3 -> eV^4
RHO_CRIT_OVER_H2_EV4 = (1.0537e-5 / GEVCM3_PER_GEV4) * EV4_PER_GEV4   # ~8.1e-11 eV^4

# radiation density today: Omega_r h^2 ~ 4.15e-5 (photons + 3 nu)
OMEGA_R_H2 = 4.15e-5
OMEGA_R = OMEGA_R_H2 / H_LITTLE ** 2
OMEGA_L = 1.0 - OMEGA_M - OMEGA_R


# ====================================================================== #
# FN3-1: analytic relic density
# ====================================================================== #
def omega_canonical(m_eV, f_A_GeV):
    """Standard ULDM misalignment closed form (prompt FN3-1 step 3 / Hui+2017):
        Omega h^2 = 0.12 (m/1e-22 eV)^1/2 (f_A/1e17 GeV)^2,  theta_i ~ O(1).
    This is the PRIMARY analytic estimate used for the (m_A, f_A) grid."""
    m_eV = np.asarray(m_eV, float)
    f = np.asarray(f_A_GeV, float)
    return 0.12 * (m_eV / 1e-22) ** 0.5 * (f / 1e17) ** 2


def T_osc_GeV(m_eV, g_star=G_STAR):
    """Oscillation-onset temperature from H(T)=m in radiation domination:
        H = 1.66 sqrt(g_*) T^2 / M_Pl = m  ->  T_osc = sqrt(m M_Pl / (1.66 sqrt g_*)).
    m in eV; returns GeV.  (For the Paper II window T_osc ~ 0.1-100 keV.)"""
    m_GeV = m_eV * GEV_PER_EV
    return np.sqrt(m_GeV * M_PL_GEV / (1.66 * np.sqrt(g_star)))


def omega_firstprinciples(m_eV, f_A_GeV, theta_i=1.0, g_star=G_STAR):
    """First-principles entropy-conserving relic, INDEPENDENT of the closed form.

    rho_osc = 1/2 m^2 (theta_i f_A)^2 at onset (3H=m, radiation era); the comoving
    number density n = rho/m is then conserved, so
        rho_0 = rho_osc * (g_{*s,0}/g_{*s,osc}) (T_0/T_osc)^3 .
    Returns Omega_{m_A} h^2.  Carries the well-known O(1) onset/g_* ambiguity (the
    numerical FN3-2 pins the residual factor); reported as a cross-check, not the
    headline.  All masses in the Paper II window oscillate in radiation domination
    (T_osc >> T_eq ~ 0.8 eV), so the radiation-era formula applies."""
    m_GeV = m_eV * GEV_PER_EV
    phi0_GeV = theta_i * f_A_GeV
    rho_osc_GeV4 = 0.5 * m_GeV ** 2 * phi0_GeV ** 2
    Tosc = T_osc_GeV(m_eV, g_star)
    T0_GeV = T_CMB_EV * GEV_PER_EV
    dilution = (G_STAR_S0 / g_star) * (T0_GeV / Tosc) ** 3
    rho0_GeV4 = rho_osc_GeV4 * dilution
    rho0_eV4 = rho0_GeV4 * EV4_PER_GEV4
    return rho0_eV4 / RHO_CRIT_OVER_H2_EV4


def f_A_for_target(m_eV, omega_target=OMEGA_DM_H2):
    """Invert the canonical form: which f_A (GeV) gives Omega h^2 = target at mass m?
        f_A = 1e17 GeV * sqrt(target / (0.12 (m/1e-22)^1/2))."""
    return 1e17 * np.sqrt(omega_target / (0.12 * (m_eV / 1e-22) ** 0.5))


# ====================================================================== #
# FRW background (radiation + matter + Lambda; Omega_r fixed by T_CMB)
# ====================================================================== #
def H_of_a_eV(a):
    """Hubble rate H(a) in eV for the charter cosmology."""
    a = np.asarray(a, float)
    return H0_EV * np.sqrt(OMEGA_R * a ** -4 + OMEGA_M * a ** -3 + OMEGA_L)


def a_osc_of(m_eV, ratio=3.0):
    """Scale factor at oscillation onset, 3H = m (general FRW, solved numerically)."""
    m = m_eV
    f = lambda a: ratio * H_of_a_eV(a) - m
    # onset is deep in radiation/early matter era: bracket in log a
    return brentq(f, 1e-12, 0.5, xtol=1e-30, rtol=1e-12)


# ====================================================================== #
# FN3-2: numerical misalignment oscillator -> relic density
# ====================================================================== #
def misalignment_relic(m_eV, f_A_GeV, n_after=20.0, n_eval=12000):
    """Integrate phi'' + 3H phi' + m^2 phi = 0 in N=ln a across the oscillation onset
    and read off the conserved comoving relic rho_phi a^3.

    Units: phi in eV (phi0 = f_A converted GeV->eV), H in eV, a normalized to a_0=1.
    Integrate from a_start = a_osc/5 (frozen) to a_end where m/H = n_after*3 (tens of
    oscillations past onset), where rho_phi a^3 has plateaued.  Since a_0=1 and
    rho a^3 = const, Omega_{m_A} h^2 = (rho a^3)_plateau / (rho_crit/h^2).

    Returns dict with a, rho/rho_osc * (a/a_osc)^3 (the plateau diagnostic),
    w_inst, Omega_h2 (numerical), Omega_canonical, and the onset reduction factor
    R = (rho a^3)_plateau / (1/2 m^2 phi0^2 a_osc^3)."""
    m = m_eV                                            # eV
    phi0 = f_A_GeV / GEV_PER_EV                         # eV  (GeV -> eV)
    a_osc = a_osc_of(m_eV)
    a_start = a_osc / 5.0
    # a_end: where m/H = 3*n_after (well into oscillation); cap below a=1
    f_end = lambda a: m - 3.0 * n_after * H_of_a_eV(a)
    a_end = min(brentq(f_end, a_osc, 0.9, xtol=1e-30, rtol=1e-12), 0.9)

    def rhs(N, y):
        a = np.exp(N)
        H = H_of_a_eV(a)
        phi, phidot = y                                # phidot = dphi/dt (eV^2)
        return [phidot / H, (-3.0 * H * phidot - m ** 2 * phi) / H]

    Ns = np.linspace(np.log(a_start), np.log(a_end), n_eval)
    sol = solve_ivp(rhs, [Ns[0], Ns[-1]], [phi0, 0.0], t_eval=Ns,
                    method="RK45", rtol=1e-9, atol=1e-12 * phi0)
    a = np.exp(sol.t)
    phi, phidot = sol.y[0], sol.y[1]
    rho = 0.5 * phidot ** 2 + 0.5 * m ** 2 * phi ** 2          # eV^4
    p = 0.5 * phidot ** 2 - 0.5 * m ** 2 * phi ** 2
    w_inst = np.where(rho > 0, p / rho, 0.0)

    # conserved comoving relic: average rho*a^3 over the oscillating tail
    rho_a3 = rho * a ** 3
    sel = a > a_osc * 3.0
    relic_eV4 = float(np.mean(rho_a3[sel])) if sel.sum() > 10 else float(rho_a3[-1])
    omega_num = relic_eV4 / RHO_CRIT_OVER_H2_EV4               # = rho_0/rho_c (a_0=1)

    rho_osc_naive = 0.5 * m ** 2 * phi0 ** 2
    R = relic_eV4 / (rho_osc_naive * a_osc ** 3)
    # plateau diagnostic normalized to the naive onset value
    diag = rho_a3 / (rho_osc_naive * a_osc ** 3)

    return {"a": a, "diag_rho_a3": diag, "w_inst": w_inst, "a_osc": a_osc,
            "Omega_h2": float(omega_num), "Omega_canonical": float(omega_canonical(m_eV, f_A_GeV)),
            "onset_factor_R": float(R), "m_eV": m_eV, "f_A_GeV": f_A_GeV}


# ====================================================================== #
# FN3-4: ULDM structure constraints (Jeans / Lyman-alpha), reused from FM4 logic
# ====================================================================== #
def k_half_mode(m_eV):
    """Half-mode comoving wavenumber (1/Mpc) of the fuzzy-DM transfer suppression
    (Hu-Barkana-Gruzinov scaling, anchored k~4.6/Mpc at m=1e-22 eV) -- FM4-2."""
    return 4.6 * (m_eV / 1e-22) ** (4.0 / 9.0)


def lyman_suppression(m_eV, frac):
    """Fractional P(k) at the Lyman-alpha pivot k=3/Mpc for a mixed cosmology with a
    fraction `frac` of ULDM of mass m (the FM4-4 transfer).  Lyman-alpha needs this
    >~ 0.95; <0.95 is excluded.  T_mix = (1-frac) + frac*T_F(k=3)."""
    from math import cos
    k = 3.0                                            # 1/Mpc (Lyman-alpha pivot)
    m22 = m_eV / 1e-22
    k_Jeq = 9.0 * m22 ** 0.5
    x = 1.61 * m22 ** (1.0 / 18.0) * (k / k_Jeq)
    Tf = max(0.0, cos(x ** 3) / (1.0 + x ** 8))
    Tmix = (1.0 - frac) + frac * Tf
    return Tmix ** 2


def lyman_safe_100pct_floor():
    """Mass above which ULDM as 100% of DM survives Lyman-alpha (~2e-21 eV, the
    standard literature bound reproduced by FM4)."""
    return 2.0e-21


def jeans_mass_Msun(m_eV, z=0.0):
    """Order-of-magnitude ULDM Jeans mass (Msun): below it halos are suppressed.
    M_J ~ 1.5e7 (1+z)^3/4 (m/1e-22)^-3/2 Msun (Hui+2017 scaling)."""
    return 1.5e7 * (1 + z) ** 0.75 * (m_eV / 1e-22) ** -1.5


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("fn3_core self-test")
    print(f"  rho_crit/h^2 = {RHO_CRIT_OVER_H2_EV4:.3e} eV^4  (expect ~8.1e-11)")
    print(f"  H0 = {H0_EV:.3e} eV   Omega_r = {OMEGA_R:.3e}")
    # canonical: (1e-22, 1e17) must give exactly 0.12
    print(f"  Omega_canon(1e-22 eV, 1e17 GeV) = {omega_canonical(1e-22, 1e17):.3f} (expect 0.120)")
    print(f"  Omega_fp   (1e-22 eV, 1e17 GeV) = {omega_firstprinciples(1e-22, 1e17):.3f} "
          f"(first-principles, O(1) of canonical)")
    print(f"  f_A for Omega=0.12 at floor {M_A_FLOOR:.1e} eV: {f_A_for_target(M_A_FLOOR):.2e} GeV")
    print(f"  f_A for Omega=0.12 at ceil  {M_A_CEIL:.1e} eV: {f_A_for_target(M_A_CEIL):.2e} GeV")
    # numerical relic at (1e-22, 1e17): must land near 0.12
    r = misalignment_relic(1e-22, 1e17)
    print(f"  numerical relic (1e-22, 1e17): Omega_h2={r['Omega_h2']:.3f}  "
          f"(canon {r['Omega_canonical']:.3f})  a_osc={r['a_osc']:.2e}  R={r['onset_factor_R']:.2f}")
    print("self-test OK")
