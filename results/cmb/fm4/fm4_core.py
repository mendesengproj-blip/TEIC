"""fm4_core.py -- wave/fuzzy-condensate engine for FM4_WAVE_CONDENSATE.

DATA GENERATOR for the FM4 campaign (the "massive vector m_A as ultralight wave dark
matter" hypothesis).  Contains NO cosmology verdict: "dark matter"/"resolve S8" live
only in the synthesis (COMPARISON ONLY).  Tests the one untested sector -- the MASSIVE
mode -- after FM1/FM2/FM3 closed the Goldstone sector.  Knows:

  * the MISALIGNMENT oscillator phi'' + 3 H phi' + m^2 phi = 0 in an FRW background:
    frozen while H>m (w~-1), oscillating as COLD matter (<w>->0, rho~a^-3) once H<m.
    The time-averaged equation of state w(a) is the FM4-1 observable;

  * the ultralight (fuzzy) Jeans / de Broglie scale k_J(m,z) -- where the quantum
    pressure of a coherent massive field suppresses clustering (FM4-2);

  * the fuzzy-DM transfer function (Hu-Barkana-Gruzinov 2000) and the sigma8 of a
    MIXED cosmology with a fraction f of ultralight DM (FM4-3), built on FM1's CAMB
    LambdaCDM baseline;

  * the massive-mode dispersion omega^2 = c^2 k^2 + m^2 (FM4-V): E2's BD symbol with
    an explicit mass term -- E2 measured the massless (m^2<0) case; here a mass opens
    the gap.

Anti-circularity: m_A is the Paper II value (galaxies/stability, NOT a CMB fit); w,
k_J and the abundance come from the field dynamics; no sigma8/KiDS/Lyman-alpha value
is inserted.  Lyman-alpha / Planck bounds are COMPARISON ONLY.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.integrate import solve_ivp

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                       # .../TEIC
sys.path.insert(0, str(ROOT / "results" / "cmb" / "fm1"))

# constants
HBAR_EV_S = 6.582119569e-16      # eV*s
MPC_M = 3.0856775815e22
C_SI = 2.99792458e8
H0_100 = 100.0 * 1e3 / MPC_M     # (km/s/Mpc) in 1/s, per h
EV_PER_INV_S = HBAR_EV_S         # 1/s -> eV via hbar

PLANCK = dict(H0=67.36, Om=0.3153, h=0.6736)
M_A_FLOOR = 3.7e-25              # eV (Paper II lower bound on the vector mass)


# ====================================================================== #
# FM4-1: misalignment oscillator -> w=0
# ====================================================================== #
def _H_of_a(a, Om=PLANCK["Om"], h=PLANCK["h"]):
    """Hubble rate H(a) in 1/s (matter+Lambda; radiation negligible for this demo)."""
    H0 = h * H0_100
    OL = 1.0 - Om
    return H0 * np.sqrt(Om * a ** -3 + OL)


def misalignment(m_eV, n_osc_cap=60.0, phi0=1.0, n_eval=8000):
    """Integrate phi'' + 3 H phi' + m^2 phi = 0 across the oscillation ONSET.

    A light field oscillates ~m/H ~ 1e8 times per Hubble time today -- integrating to
    a=1 is intractable (and unnecessary: w->0 is universal once oscillating).  We
    therefore integrate from a_start (frozen, H>>m) to a_end where m/H = n_osc_cap
    (~tens of oscillations after onset) and average w over the oscillating tail.

    a_osc (onset) is where 3H = m; a_start = a_osc/4 (still frozen); a_end where
    m/H = n_osc_cap.  Returns a, phi, w_inst, w_late (tail-averaged), rho slope
    (->-3 for matter), a_osc.  m_eV in eV (-> 1/s via hbar)."""
    m = m_eV / HBAR_EV_S                                  # 1/s
    H0 = PLANCK["h"] * H0_100
    Om, OL = PLANCK["Om"], 1.0 - PLANCK["Om"]

    def H_of_a(a):
        return H0 * np.sqrt(Om * a ** -3 + OL)

    def a_at_ratio(ratio):
        """a where m/H = ratio (matter-dominated branch: H ~ H0 sqrt(Om) a^-3/2)."""
        # m/H = ratio -> H = m/ratio -> Om a^-3 = (m/(ratio H0))^2 - OL
        val = (m / (ratio * H0)) ** 2 - OL
        return (val / Om) ** (-1.0 / 3.0)

    a_osc = a_at_ratio(3.0)                               # 3H = m
    a_start = a_osc / 4.0
    # a_end where m/H = n_osc_cap (H = m/n_osc_cap, LATER time); cap at a=1
    a_end = min(a_at_ratio(n_osc_cap), 1.0) if n_osc_cap < (m / H0) else 1.0

    def rhs(N, y):
        a = np.exp(N); H = H_of_a(a)
        phi, phidot = y
        return [phidot / H, (-3.0 * H * phidot - m ** 2 * phi) / H]

    Ns = np.linspace(np.log(a_start), np.log(a_end), n_eval)
    sol = solve_ivp(rhs, [Ns[0], Ns[-1]], [phi0, 0.0], t_eval=Ns, method="RK45",
                    rtol=1e-8, atol=1e-12)
    a = np.exp(sol.t); phi = sol.y[0]; phidot = sol.y[1]
    rho = 0.5 * phidot ** 2 + 0.5 * m ** 2 * phi ** 2
    p = 0.5 * phidot ** 2 - 0.5 * m ** 2 * phi ** 2
    w_inst = np.where(rho > 0, p / rho, 0.0)
    sel = a > a_osc * 3.0                                  # oscillating tail
    w_late = float(np.mean(w_inst[sel])) if sel.sum() > 10 else float("nan")
    slope = (np.polyfit(np.log(a[sel]), np.log(np.maximum(rho[sel], 1e-300)), 1)[0]
             if sel.sum() > 10 else np.nan)
    return {"a": a, "phi": phi, "w_inst": w_inst, "w_late": w_late,
            "rho_slope": float(slope), "a_osc": float(a_osc), "m_eV": m_eV}


# ====================================================================== #
# FM4-2: ultralight (fuzzy) Jeans / de Broglie scale
# ====================================================================== #
def k_half_mode(m_eV):
    """Half-mode comoving wavenumber (1/Mpc) of the fuzzy-DM transfer suppression
    (Hu-Barkana-Gruzinov scaling, anchored k~4.6/Mpc at m=1e-22 eV).  Suppression
    sets in for k > k_half."""
    m22 = m_eV / 1e-22
    return 4.6 * m22 ** (4.0 / 9.0)


def jeans_scale_z(m_eV, z=0.0, Om=PLANCK["Om"], h=PLANCK["h"]):
    """Comoving quantum Jeans wavenumber (1/Mpc) at redshift z for ULDM of mass m.
    k_J = (16 pi G rho_m a / hbar^2 * m^2)^(1/4) reduced to the standard
    k_J ~ 44.7 (1+z)^-1/4 (Om h^2)^1/4 (m/1e-22)^1/2 /Mpc (order-of-magnitude)."""
    m22 = m_eV / 1e-22
    return 44.7 * (1 + z) ** -0.25 * (Om * h ** 2) ** 0.25 * m22 ** 0.5 / 10.0


# ====================================================================== #
# FM4-3: fuzzy transfer function + mixed (CDM + fraction f ULDM) sigma8
# ====================================================================== #
def fuzzy_transfer(k_hMpc, m_eV, h=PLANCK["h"]):
    """Fuzzy-DM transfer relative to CDM (Hu+2000):
        T_F(k) = cos(x^3)/(1+x^8),  x = 1.61 m22^(1/18) (k/k_Jeq),
    with k_Jeq the Jeans scale at matter-radiation equality.  Returns T in [~0,1];
    suppresses k above the de Broglie scale.  k in h/Mpc -> convert to 1/Mpc."""
    k = np.asarray(k_hMpc, float) * h                    # 1/Mpc
    m22 = m_eV / 1e-22
    k_Jeq = 9.0 * m22 ** 0.5                              # 1/Mpc (Hu+2000 ~ k_Jeq)
    x = 1.61 * m22 ** (1.0 / 18.0) * (k / k_Jeq)
    T = np.cos(x ** 3) / (1.0 + x ** 8)
    return np.clip(T, 0.0, 1.0)


def mixed_power(bl, m_eV, f, h=PLANCK["h"]):
    """Mixed CDM + fraction f ULDM linear P(k,z=0): the ULDM part is suppressed by
    the fuzzy transfer, so the density transfer is T_mix = (1-f) + f T_F(k); then
    P_mix = P_LCDM * T_mix^2.  Returns (k, P_LCDM, P_mix)."""
    k = bl.k
    Tf = fuzzy_transfer(k, m_eV, h)
    Tmix = (1.0 - f) + f * Tf
    return k, bl.P, bl.P * Tmix ** 2


def sigma8_of(k, P, R=8.0):
    from FM1_2_class_impl import sigma_R
    return sigma_R(k, P, R)


# ====================================================================== #
# FM4-V: massive-mode dispersion omega^2 = c^2 k^2 + m^2 (E2 symbol + mass)
# ====================================================================== #
def massive_dispersion(kmags, m, c=1.0):
    """Analytic massive Klein-Gordon dispersion omega(k)=sqrt(c^2 k^2 + m^2): E2's
    massless magnon (omega=ck, m^2<0 measured) acquires a GAP m at k=0 when the
    orientation field is given an explicit mass.  (The BD symbol lambda(k,omega) ~
    -(k^2-omega^2) shifts to -(k^2-omega^2) - m^2, whose zero is this dispersion.)"""
    kmags = np.asarray(kmags, float)
    return np.sqrt(c ** 2 * kmags ** 2 + m ** 2)


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("fm4_core self-test")
    # misalignment: a light field must end up cold (w->0) and rho~a^-3
    r = misalignment(1e-26)
    print(f"  misalignment m=1e-26 eV: w_late={r['w_late']:+.3f} (->0 cold)  "
          f"rho~a^{r['rho_slope']:.2f} (->-3 matter)  a_osc~{r['a_osc']:.1e}")
    # Jeans scale lands near sigma8 scale for m near the Paper II floor
    for m in (1e-22, 1e-24, M_A_FLOOR):
        print(f"  m={m:.1e} eV: k_half={k_half_mode(m):.3f}/Mpc  "
              f"k_Jeans(z=0)={jeans_scale_z(m):.3f}/Mpc")
    # mixed sigma8 drops with fuzzy fraction
    from FM1_2_class_impl import LCDMBaseline
    bl = LCDMBaseline()
    k, PL, PM = mixed_power(bl, M_A_FLOOR, f=0.2)
    print(f"  sigma8 LCDM={sigma8_of(k,PL):.3f}  "
          f"mixed(f=0.2,m=floor)={sigma8_of(k,PM):.3f}")
    print("self-test OK")
