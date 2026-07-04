"""kr_pta_core -- Khmelnitsky-Rubakov line vs published PTA direct searches.

Campaign #10 of RESEARCH_MAP Section 6: the DIRECT-SEARCH confrontation that HQ3
left open.  HQ3 established only THEORETICAL consistency (the KR line frequency
f = 2 m c^2/h falls in the PTA band; amplitude "grazes the threshold").  Here we
confront the m_A prediction with the *published upper limits from the PTAs' own
direct searches* -- i.e. ask whether the line the m_A would produce has already
been looked for and excluded.

Anti-circularity / honesty
--------------------------
- m_A window is taken from Paper II / FM4 (SPARC lower bound), NOT tuned to PTA.
- All formulas and limits are from the literature, quoted with reference:
    * KR signal model: Khmelnitsky & Rubakov, JCAP 02 (2014) 019 [arXiv:1309.5888],
      Eqs (12),(21),(22) (fetched verbatim).
    * Direct-search limit benchmark: Porayko et al. (PPTA), PRD 98 (2018) 102002
      [arXiv:1810.03227]: rho_ULDM < 6 GeV/cm^3 (95%) for m <= 1e-23 eV
      (gravitational/universal KR signal).
    * NANOGrav 15yr [arXiv:2306.16219] searched the same gravitational metric-
      fluctuation signal and found NO evidence (used qualitatively; we anchor the
      quantitative bound on the cleanly-quoted PPTA number).
- We do NOT re-run a PTA pipeline on raw residuals (out of scope / not needed:
  the falsification question is answered by the published exclusion curves).
- This is a TEST, not a fit; the kill criterion is pre-registered in KR2.
"""

import numpy as np

# --- physical constants ---
HBAR_EV_S = 6.582119569e-16          # reduced Planck constant [eV s]
RHO_LOCAL = 0.4                      # local DM density [GeV/cm^3] (standard ~0.3-0.45)

# --- m_A window (Paper II / FM4 / HQ3) ---
M_A_SPARC_LOWER = 3.7e-25           # eV, SPARC lower bound (Paper II)
# HQ3 KR-PTA overlap window (where f_KR lands in the PTA band):
M_A_PTA_LO = 4.1e-24                # eV
M_A_PTA_HI = 1.2e-22               # eV

# --- PTA observing band (NANOGrav 15yr-like): f in [1/T_span, ~N_h/T_span] ---
PTA_F_LO = 2.0e-9                   # Hz (~1/16yr)
PTA_F_HI = 6.0e-8                   # Hz

# --- PPTA 2018 published gravitational limit benchmark ---
PPTA_RHO_LIMIT_AT_1e23 = 6.0        # GeV/cm^3 at m = 1e-23 eV (95%)


def f_signal(m_eV):
    """KR signal frequency [Hz].  Energy density oscillates at 2x the Compton
    frequency: f = m c^2/(pi hbar).  KR Eq (22): ~5e-9 Hz (m/1e-23 eV)."""
    return m_eV / (np.pi * HBAR_EV_S)


def m_from_f(f_hz):
    """Inverse of f_signal: boson mass [eV] producing a KR line at frequency f."""
    return f_hz * np.pi * HBAR_EV_S


def h_c(m_eV, rho_GeVcm3):
    """KR characteristic strain, Eq (21):
        h_c = 2 sqrt(3) Psi_c = 2e-15 (rho/0.3 GeV cm^-3)(1e-23 eV/m)^2 ."""
    return 2.0e-15 * (rho_GeVcm3 / 0.3) * (1e-23 / m_eV) ** 2


def psi_c(m_eV, rho_GeVcm3):
    """Oscillating gravitational potential amplitude, KR Eq (12) = h_c/(2 sqrt3)."""
    return h_c(m_eV, rho_GeVcm3) / (2.0 * np.sqrt(3.0))


def timing_residual_s(m_eV, rho_GeVcm3):
    """Induced pulsar-timing residual amplitude [s]: dt = Psi_c/(2 pi f)."""
    return psi_c(m_eV, rho_GeVcm3) / (2.0 * np.pi * f_signal(m_eV))


def ppta_rho_limit(m_eV):
    """Approximate PPTA-2018 gravitational density limit [GeV/cm^3] vs mass.
    Anchored at rho<6 at m=1e-23 eV; white-noise (constant-strain) scaling gives
    rho_lim ~ m^2 because the KR strain ~ rho/m^2.  CAVEAT (declared): this
    extrapolation ignores PPTA's frequency-dependent sensitivity, which DEGRADES
    at f < 1/T_span (low m, <1 cycle in the data span); so the low-m limit is, if
    anything, WEAKER than this scaling -> the extrapolation is conservative for
    the 'is it excluded?' question only at the HIGH-m end of the window."""
    return PPTA_RHO_LIMIT_AT_1e23 * (m_eV / 1e-23) ** 2


def ppta_fraction_limit(m_eV):
    """Max allowed ULDM fraction f = rho_ULDM/rho_DM from the PPTA benchmark."""
    return ppta_rho_limit(m_eV) / RHO_LOCAL


if __name__ == "__main__":
    for m in (4.1e-24, 1e-23, 3e-23, 1.2e-22):
        print(
            f"m={m:.2e} eV  f={f_signal(m):.2e} Hz  "
            f"h_c(f=1)={h_c(m, RHO_LOCAL):.2e}  "
            f"dt(f=1)={timing_residual_s(m, RHO_LOCAL)*1e9:.2f} ns  "
            f"f_max(PPTA)={ppta_fraction_limit(m):.1f}"
        )
