"""fn4_core.py -- physics engine for FN4_MOND_SCREENING.

Implements the DEV "screened MOND" prediction: the MOND modification, mediated by
the massive vector m_A, is the LONG-range condensate effect that switches ON above
the field's correlation (Compton) length lambda_A = 17.3 pc and is screened OFF
(Newtonian) below it.

    g_DEV(r) = g_N(r) * [ 1 + (nu_eff(r) - 1) * S(r) ]
    S(r)     = 1 - exp(-r / lambda_A)        (de-screening / MOND turn-on)
    nu_eff   = nu_RAR( sqrt(g_N^2 + g_ext^2) / a0 )   (MOND boost, EFE-capped)

Limits (the whole point):
    r >> lambda_A :  S -> 1  =>  g_DEV -> g_MOND   (full MOND; galaxies, kpc)
    r << lambda_A :  S -> 0  =>  g_DEV -> g_N       (Newton; wide binaries, sub-pc)

------------------------------------------------------------------------------
TWO PROMPT FORMULAS CORRECTED (documented, NOT to fudge any number):

1. SCREENING SIGN.  The charter prose writes the boost as ~ e^{-r/lambda_A} and
   then says "r << lambda -> e^{-inf} -> Newton", which is backwards: e^{-r/lambda}
   -> 1 as r->0.  More importantly, a bare e^{-r/lambda} would screen MOND at LARGE
   r and break galactic MOND (kpc >> 17 pc).  The physically consistent form
   (MOND survives in galaxies, screened in sub-pc binaries) is the condensate
   coherence factor S(r) = 1 - e^{-r/lambda_A}.  lambda_A = 17.3 pc is NOT changed.

2. INTERPOLATION FUNCTION.  The charter writes nu(x)=1/sqrt(1-e^{-sqrt(x)}); the
   extra square root gives deep-MOND g ∝ g_N^{3/4}, NOT g=sqrt(g_N a0).  The DEV /
   Paper I MOND is calibrated on the SPARC radial-acceleration relation, whose
   interpolation is McGaugh's nu_RAR(x)=1/(1-e^{-sqrt(x)}).  We use that.

Neither correction touches a0 or lambda_A, and the qualitative FN4 conclusions
(screening below 17 pc, Chae regime deeply screened, tidal limit at 1.7 pc) are
independent of these choices.
------------------------------------------------------------------------------
"""
from __future__ import annotations

import numpy as np

# --- constants (SI) ----------------------------------------------------------
G = 6.67430e-11           # m^3 kg^-1 s^-2
M_SUN = 1.98892e30        # kg
PC = 3.0856775814913673e16  # m
AU = 1.495978707e11       # m
KAU = 1e3 * AU            # kilo-au

# --- fixed parameters (CHARTER -- DO NOT FIT) --------------------------------
A0 = 1.2e-10              # m/s^2     (Milgrom acceleration)
LAMBDA_A_PC = 17.3        # pc        (m_A correlation/Compton length, FM2/SCALE_BOUNDARY)
LAMBDA_A = LAMBDA_A_PC * PC

# Milky Way external field at the solar circle (V_c=233 km/s, R0=8.2 kpc).
# g_ext = V_c^2 / R0.  Drives the MOND external-field effect (EFE) that caps the
# boost at gamma ~ 1.35 -- this is what Chae+2023 actually measures (gamma=1.43).
V_C = 233e3              # m/s
R0_KPC = 8.2
R0 = R0_KPC * 1e3 * PC
G_EXT = V_C**2 / R0      # ~2.1e-10 m/s^2 ~ 1.8 a0

# Chae+2023 (arXiv:2309.08160) sample: 200 - 30000 au, anomaly at s >~ 2 kau.
CHAE_S_MIN_AU = 200.0
CHAE_S_MAX_AU = 30000.0
CHAE_S_ANOMALY_AU = 2000.0
CHAE_GAMMA = 1.43        # reported acceleration boost in the low-accel bin
CHAE_GAMMA_ERR = 0.06

# Galactic tidal (Jacobi) radius for a solar-mass binary in the solar
# neighbourhood (Jiang & Tremaine 2010): bound binaries do not survive beyond it.
R_JACOBI_PC = 1.7


# --- gravity -----------------------------------------------------------------
def g_newton(r_m, M_msun=1.0):
    """Newtonian internal acceleration GM/r^2 [m/s^2]; r in metres."""
    return G * M_msun * M_SUN / r_m**2


def nu_rar(x):
    """McGaugh radial-acceleration-relation interpolation, g = g_N * nu(g_N/a0).
    nu(x) = 1/(1 - exp(-sqrt(x))).  x>>1 -> 1 (Newton); x<<1 -> 1/sqrt(x) (deep MOND
    g=sqrt(g_N a0))."""
    x = np.asarray(x, dtype=float)
    return 1.0 / (1.0 - np.exp(-np.sqrt(x)))


def nu_eff(r_m, M_msun=1.0, efe=True):
    """EFE-capped boost factor nu_eff = g_MOND/g_N.  With efe=True the interpolation
    is evaluated at the total field sqrt(g_N^2+g_ext^2)/a0, so the boost saturates at
    nu_RAR(g_ext/a0) ~ 1.35 instead of diverging (this matches Chae's gamma~1.4)."""
    gN = g_newton(r_m, M_msun)
    if efe:
        gtot = np.hypot(gN, G_EXT)
    else:
        gtot = gN
    return nu_rar(gtot / A0)


def screening(r_m):
    """De-screening / MOND turn-on factor S(r) = 1 - exp(-r/lambda_A).
    0 deep inside lambda_A (Newton), 1 far outside (full MOND)."""
    return 1.0 - np.exp(-r_m / LAMBDA_A)


def boost_newton(r_m, M_msun=1.0):
    return np.ones_like(np.asarray(r_m, dtype=float))


def boost_mond(r_m, M_msun=1.0, efe=True):
    """g_MOND/g_N (no screening)."""
    return nu_eff(r_m, M_msun, efe)


def boost_dev(r_m, M_msun=1.0, efe=True):
    """g_DEV/g_N = 1 + (nu_eff - 1) * S(r)."""
    return 1.0 + (nu_eff(r_m, M_msun, efe) - 1.0) * screening(r_m)


def g_dev(r_m, M_msun=1.0, efe=True):
    return g_newton(r_m, M_msun) * boost_dev(r_m, M_msun, efe)


def g_mond(r_m, M_msun=1.0, efe=True):
    return g_newton(r_m, M_msun) * boost_mond(r_m, M_msun, efe)


# --- velocity statistic ------------------------------------------------------
def vtilde(boost):
    """v_obs/v_Newton = sqrt(g_eff/g_N) = sqrt(boost) for a fixed-separation orbit
    (v^2 = g_eff * r)."""
    return np.sqrt(boost)


def vtilde_dev(r_m, M_msun=1.0, efe=True):
    return vtilde(boost_dev(r_m, M_msun, efe))


def vtilde_mond(r_m, M_msun=1.0, efe=True):
    return vtilde(boost_mond(r_m, M_msun, efe))


# --- scales ------------------------------------------------------------------
def mond_radius(M_msun=1.0):
    """r where g_N = a0 [m]: sqrt(GM/a0).  MOND active beyond it."""
    return np.sqrt(G * M_msun * M_SUN / A0)


# --- self-test ---------------------------------------------------------------
def _selftest():
    print("=" * 74)
    print("fn4_core self-test")
    print("=" * 74)
    print(f"  a0           = {A0:.3e} m/s^2   (fixed)")
    print(f"  lambda_A     = {LAMBDA_A_PC} pc = {LAMBDA_A:.3e} m   (fixed, not fit)")
    print(f"  g_ext (MW)   = {G_EXT:.3e} m/s^2 = {G_EXT/A0:.2f} a0")
    print(f"  nu_RAR(g_ext/a0) plateau boost gamma = {float(nu_rar(G_EXT/A0)):.3f} "
          f"(Chae measures {CHAE_GAMMA})")
    print(f"  r_MOND(1 Msun) = {mond_radius(1.0)/AU:.0f} au = "
          f"{mond_radius(1.0)/PC:.4f} pc")

    # screening checkpoints required by the charter
    for r_pc, tag in [(0.05, "Chae mid (~10 kau)"), (1.7, "Jacobi r_J"),
                      (17.3, "lambda_A"), (100.0, "galactic outskirt")]:
        r = r_pc * PC
        print(f"  S({r_pc:>6.2f} pc) = {float(screening(r)):.4f}  "
              f"v~_DEV={float(vtilde_dev(r)):.4f}  v~_MOND={float(vtilde_mond(r)):.4f}"
              f"   [{tag}]")

    # limit checks
    r_small = 1e-4 * LAMBDA_A
    r_big = 50.0 * LAMBDA_A
    assert abs(float(boost_dev(r_small)) - 1.0) < 1e-2, "DEV should be Newton for r<<lambda"
    assert abs(float(boost_dev(r_big)) - float(boost_mond(r_big))) < 1e-2, \
        "DEV should be MOND for r>>lambda"
    # screening at the charter checkpoint 17 pc ~ 1/e suppression of the *gap*
    assert abs(float(screening(LAMBDA_A)) - (1 - np.exp(-1))) < 1e-6
    print("  limit checks: r<<lambda -> Newton OK ; r>>lambda -> MOND OK ; "
          "S(lambda)=1-1/e OK")
    print("self-test PASSED")


if __name__ == "__main__":
    _selftest()
