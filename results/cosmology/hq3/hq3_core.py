"""hq3_core.py -- gravitational-wave / PTA engine for HQ3_NANOGRAV.

DATA GENERATOR for the HQ3 campaign ("does the m_A of the DEV produce a signal in
the NANOGrav PTA band?").  Contains NO verdict: "consistent with NANOGrav"/"third
confirmation" live only in the .md syntheses (COMPARISON ONLY).  Picks up where FM4
(m_A is COLD dark matter, w->0) and FN3 (Omega_{m_A} h^2 ~ 0.12 reachable with
f_A~1e17 GeV) stopped, and asks the OBSERVATIONAL question: an oscillating m_A
condensate imprints a time-dependent metric; is that imprint in the PTA band, and at
what amplitude, compared with the NANOGrav 2023 stochastic background?

It knows three physically DISTINCT things, kept separate on purpose:

  * the OSCILLATION FREQUENCIES of the condensate (HQ3-1): the field oscillates at
    f_DM = m_A c^2 / h ; its stress-energy (quadratic in the field) oscillates at
    f_GW = 2 m_A c^2 / h = m_A c^2 / (pi hbar).  This second line is what a PTA sees.

  * the KHMELNITSKY-RUBAKOV (KR, 2014) monochromatic metric oscillation (HQ3-2): a
    homogeneous DM condensate has an oscillating PRESSURE p = -rho cos(2 omega t),
    which drives an oscillating Newtonian potential of dimensionless amplitude
    Psi_c = pi G rho_DM / omega^2 (omega = m_A c^2/hbar).  This is a LINE signal at
    f_GW, NOT a propagating stochastic background.  This is the real, citable PTA
    observable for ultralight DM (Khmelnitsky-Rubakov; vector case arXiv:2412.12975).

  * the PROPAGATING stochastic GW background (HQ3-3): a HOMOGENEOUS condensate radiates
    NO on-shell graviton (k=0 source, 2m -> graviton at zero momentum is kinematically
    forbidden); the SGWB from its density fluctuations is order Psi_c^2 of the DM and
    utterly negligible at PTA frequencies.  Reported as an upper-bound estimate to show
    the m_A is NOT the source of the broadband NANOGrav SGWB.

Anti-circularity: m_A is the Paper II / lattice input (galaxies + GW170817, NOT a PTA
fit); local rho_DM, the NANOGrav amplitude A_yr=2.4e-15, the index gamma=13/3 and the
band [2e-9, 1e-7] Hz are COMPARISON ONLY -- none is inserted to move m_A.  The death
criterion is pre-registered in the charter; m_A is NOT adjusted to NANOGrav.
"""
from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------- #
# constants (SI + eV; standard cosmology fixed by the charter, nothing fit)
# ---------------------------------------------------------------------------- #
HBAR_EV_S = 6.582119569e-16          # eV*s  (reduced Planck constant)
H_EV_S = 4.135667696e-15             # eV*s  (Planck constant h = 2*pi*hbar)
C_SI = 2.99792458e8                  # m/s
G_SI = 6.67430e-11                   # m^3 kg^-1 s^-2
EV_PER_JOULE = 6.241509074e18        # eV per J
KM = 1.0e3
MPC_M = 3.0856775815e22              # m
YEAR_S = 3.15576e7                   # s (Julian year)
F_YR = 1.0 / YEAR_S                  # 1/yr in Hz  (~3.17e-8 Hz, PTA reference)

# charter cosmology (same as FN3; COMPARISON ONLY where it touches observation)
H0_KMSMPC = 67.0
H_LITTLE = H0_KMSMPC / 100.0
OMEGA_M = 0.30
G_STAR = 106.75
H0_INV_S = H0_KMSMPC * KM / MPC_M    # 1/s  (~2.17e-18)

# Paper II vector mass window (SPARC lower bound + GW170817 upper bound; DEV CLAUDE.md)
M_A_FLOOR = 3.7e-25                   # eV
M_A_CEIL = 1.2e-22                   # eV

# local dark-matter density (Solar neighbourhood; COMPARISON ONLY, sets KR amplitude)
RHO_LOCAL_GEVCM3 = 0.4               # GeV/cm^3  (standard halo value)
RHO_KR_REF_GEVCM3 = 0.3             # GeV/cm^3  (Khmelnitsky-Rubakov reference density)

# NANOGrav 15yr (2023, arXiv:2306.16213) stochastic-background fit -- COMPARISON ONLY
NG_A_YR = 2.4e-15                    # characteristic-strain amplitude at f = 1/yr
NG_GAMMA = 13.0 / 3.0               # timing-residual PSD index (SMBH-binary value)
NG_BAND_HZ = (2.0e-9, 1.0e-7)       # PTA sensitivity band

# soliton-excluded ULDM mass window (independent constraint quoted in the charter)
SOLITON_EXCL_EV = (1.3e-21, 1.4e-20)


# ====================================================================== #
# unit helper
# ====================================================================== #
def rho_GeVcm3_to_kgm3(rho_GeVcm3):
    """GeV/cm^3 -> kg/m^3.  1 GeV = 1.602176634e-10 J; 1 cm^3 = 1e-6 m^3."""
    rho_J_m3 = rho_GeVcm3 * 1.602176634e-10 / 1.0e-6        # J/m^3 (energy density)
    return rho_J_m3 / C_SI ** 2                              # kg/m^3 (mass density)


# ====================================================================== #
# HQ3-1: oscillation frequencies of the condensate
# ====================================================================== #
def f_field(m_eV):
    """Field oscillation frequency f_DM = m_A c^2 / h  (Hz).  m_eV in eV."""
    return np.asarray(m_eV, float) / H_EV_S


def f_gw(m_eV):
    """Frequency a PTA sees: the stress-energy oscillates at twice the field frequency,
        f_GW = 2 m_A c^2 / h = m_A c^2 / (pi hbar).
    (Matches f = mu/pi of arXiv:2412.12975 for vector ULDM.)"""
    return 2.0 * f_field(m_eV)


def m_for_fgw(f_Hz):
    """Inverse of f_gw: the mass whose PTA frequency is f (eV).  m = f h / 2."""
    return np.asarray(f_Hz, float) * H_EV_S / 2.0


def band_mass_window():
    """Mass range whose f_GW lands inside the NANOGrav band [2e-9, 1e-7] Hz (eV)."""
    return (m_for_fgw(NG_BAND_HZ[0]), m_for_fgw(NG_BAND_HZ[1]))


def overlap_with_paper_II():
    """Intersection of the band-producing mass range with the Paper II window (eV)."""
    lo_b, hi_b = band_mass_window()
    lo = max(lo_b, M_A_FLOOR)
    hi = min(hi_b, M_A_CEIL)
    return (lo, hi) if lo < hi else None


# ====================================================================== #
# HQ3-2: Khmelnitsky-Rubakov monochromatic metric oscillation (LINE signal)
# ====================================================================== #
def omega_field_rad_s(m_eV):
    """Angular oscillation frequency of the field, omega = m_A c^2 / hbar (rad/s)."""
    return np.asarray(m_eV, float) / HBAR_EV_S


def kr_psi_amplitude(m_eV, rho_GeVcm3=RHO_LOCAL_GEVCM3, frac=1.0, vector=True):
    """Dimensionless amplitude of the oscillating Newtonian potential (KR 2014):
        Psi_c = pi G rho_DM / omega^2 ,  omega = m_A c^2 / hbar .
    This is the characteristic strain of the MONOCHROMATIC PTA signal at f_GW.
    `frac` is the fraction of the LOCAL DM made of m_A (<1 if subdominant, FM4/FN3).
    `vector` flags an O(1) polarization factor (the vector condensate carries an
    oscillating anisotropic stress as well as pressure); kept ~1 and folded into the
    declared O(1) coefficient ambiguity -- the headline scaling Psi_c ~ rho/m^2 is
    polarization-independent.  Returns Psi_c (first-principles)."""
    rho = rho_GeVcm3_to_kgm3(rho_GeVcm3) * frac
    omega = omega_field_rad_s(m_eV)
    psi = np.pi * G_SI * rho / omega ** 2
    return psi


def kr_psi_literature(m_eV, rho_GeVcm3=RHO_LOCAL_GEVCM3, frac=1.0):
    """KR closed form as quoted in the literature (calibration cross-check):
        Psi_c ~ 2e-15 (rho/0.3 GeV cm^-3)(1e-23 eV/m)^2 .
    Sits a factor ~4 above the transparent first-principles pi G rho/omega^2; the
    gap is the well-known O(1) definition ambiguity (Psi vs strain vs residual, the
    factor 2 from 2 omega).  Same scaling, same conclusion."""
    m = np.asarray(m_eV, float)
    return 2.0e-15 * (rho_GeVcm3 / 0.3) * (1e-23 / m) ** 2 * frac


def nanograv_hc(f_Hz):
    """NANOGrav characteristic-strain spectrum h_c(f) = A (f/f_yr)^alpha,
    alpha = (3 - gamma)/2 = -2/3 for the SMBH-binary index gamma=13/3.  COMPARISON
    ONLY -- the broadband strain to compare the DM line against."""
    f = np.asarray(f_Hz, float)
    alpha = (3.0 - NG_GAMMA) / 2.0
    return NG_A_YR * (f / F_YR) ** alpha


def kr_signal_vs_nanograv(m_eV, rho_GeVcm3=RHO_LOCAL_GEVCM3, frac=1.0):
    """Ratio Psi_c(m) / h_c(f_GW(m)): the DM line amplitude over the NANOGrav broadband
    strain at the same frequency.  >~1 => above current PTA strain; <1 => below.
    Uses the first-principles Psi_c (conservative)."""
    psi = kr_psi_amplitude(m_eV, rho_GeVcm3, frac)
    hc = nanograv_hc(f_gw(m_eV))
    return psi / hc


# ====================================================================== #
# HQ3-2/3: propagating stochastic GW background  (the SGWB comparison)
# ====================================================================== #
def nanograv_omega_gw(f_Hz=F_YR):
    """Energy-density of the NANOGrav SGWB at frequency f (default 1/yr):
        Omega_GW(f) = (2 pi^2 / 3) (f^2 / H0^2) h_c(f)^2 .
    Returns Omega_GW (not h^2-scaled); ~1e-8 at f=1/yr.  COMPARISON ONLY."""
    f = np.asarray(f_Hz, float)
    hc = nanograv_hc(f)
    return (2.0 * np.pi ** 2 / 3.0) * (f ** 2 / H0_INV_S ** 2) * hc ** 2


def omega_gw_propagating_bound(m_eV, rho_GeVcm3=RHO_LOCAL_GEVCM3):
    """ORDER-OF-MAGNITUDE UPPER BOUND on the PROPAGATING SGWB radiated by the m_A
    condensate.  A homogeneous condensate radiates no on-shell graviton; density
    fluctuations of order unity at the de Broglie scale source a background whose
    energy fraction per Hubble time is at most ~(pi G rho/omega^2)^2 = Psi_c^2.  We
    return Psi_c^2 as a deliberately generous ceiling -- the true value is far smaller.
    This is NOT the KR line signal; it is the radiated stochastic piece, and it is
    astronomically below the NANOGrav Omega_GW ~ 1e-8."""
    psi = kr_psi_amplitude(m_eV, rho_GeVcm3, frac=1.0)
    return psi ** 2


# ====================================================================== #
# HQ3-4: cross-constraints
# ====================================================================== #
def in_soliton_excluded(m_eV):
    """True if m lies in the soliton-excluded ULDM window (1.3e-21 - 1.4e-20 eV)."""
    lo, hi = SOLITON_EXCL_EV
    return bool(lo <= m_eV <= hi)


def delta_neff_from_omega_gw(omega_gw_h2_integrated):
    """Map an integrated Omega_GW h^2 to Delta N_eff (radiation at BBN):
        Delta N_eff = (Omega_GW h^2 integrated) / (5.6e-6).
    The BBN/CMB bound is Delta N_eff < ~0.3, i.e. integral < ~1.7e-6 ... 5.6e-6."""
    return omega_gw_h2_integrated / 5.6e-6


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("hq3_core self-test")
    print(f"  F_YR = {F_YR:.3e} Hz   NANOGrav band = {NG_BAND_HZ} Hz")
    for m in (M_A_FLOOR, 1e-24, 5e-24, 1e-23, 1e-22, M_A_CEIL):
        print(f"  m={m:.2e} eV : f_DM={f_field(m):.3e} Hz  f_GW={f_gw(m):.3e} Hz  "
              f"Psi_c={kr_psi_amplitude(m):.2e} (lit {kr_psi_literature(m):.2e})")
    lo_b, hi_b = band_mass_window()
    print(f"  band-producing masses: {lo_b:.3e} - {hi_b:.3e} eV")
    ov = overlap_with_paper_II()
    print(f"  overlap with Paper II: {ov}")
    print(f"  NANOGrav Omega_GW(1/yr) = {nanograv_omega_gw():.3e}  (expect ~1e-8)")
    print(f"  Omega_GW propagating bound @1e-23 eV = {omega_gw_propagating_bound(1e-23):.3e}")
    print(f"  KR/NANOGrav strain ratio @1e-23 eV = {kr_signal_vs_nanograv(1e-23):.3e}")
    print(f"  soliton-excluded @1e-22 eV? {in_soliton_excluded(1e-22)} (expect False)")
    print("self-test OK")
