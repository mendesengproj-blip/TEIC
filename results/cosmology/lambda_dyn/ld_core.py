"""ld_core -- everpresent-Lambda DYNAMICS (RESEARCH_MAP Section 6 #7).

The static campaign LAMBDA_EVERPRESENT (L1-L3) measured the network fluctuation
coefficient delta_rho/rho = (0.971) / sqrt(rho V) and the static de Sitter
response, then DECLARED the temporal evolution OUT OF SCOPE (L3_synthesis.md:
"se a TEIC quiser diferenciar-se aqui, precisa do elo dinamico").  This campaign
supplies that link at the cheap level: feed the MEASURED L1 coefficient into the
Sorkin/ADGS everpresent-Lambda ansatz Lambda_rms ~ 1/sqrt(V_4past) and evolve it
over FRW cosmic history, asking the two pre-registered questions.

Honesty (mirrors L3 and the FM4 misalignment caveat):
- The temporal MODEL (Lambda fluctuates with the past 4-volume; V<->Hubble,
  rho<->Planck transplant) is IMPORTED CST cosmology (Sorkin ~1990s; Ahmed-
  Dodelson-Greene-Sorkin 2004 [astro-ph/0209274]; Zwane-Afshordi-Sorkin 2018).
  The causal network's OWN time-evolution is NOT simulated (T3 showed the e7
  growth rule does not even yield d=3+1 dynamically).
- The TEIC value-add is only (i) the MEASURED fluctuation coefficient (L1=0.971,
  not a dimensional guess) and (ii) showing the everpresent SCALING follows from
  the network's Poisson statistics delta_rho/rho=1/sqrt(rho V).
- This is a CONSISTENCY test, not a derivation. Kill criterion pre-registered in
  LD1/LD2.

Units: c = H0 = 1 (times/distances in Hubble units; 4-volumes in (c/H0)^4).
"""

import numpy as np
from scipy import integrate

# --- measured + imported inputs ---
L1_COEFF = 0.971                  # MEASURED network fluctuation coefficient (L1)
OMEGA_M = 0.31                    # flat LCDM background (imported)
OMEGA_L = 1.0 - OMEGA_M


def E(z):
    """Dimensionless Hubble rate H(z)/H0 for flat LCDM."""
    return np.sqrt(OMEGA_M * (1.0 + z) ** 3 + OMEGA_L)


def comoving_distance(z, zref=0.0):
    """Comoving distance chi from zref to z (c/H0 units), z >= zref."""
    if np.isclose(z, zref):
        return 0.0
    zs = np.linspace(zref, z, 400)
    return np.trapezoid(1.0 / E(zs), zs)


def past_4volume(z_obs, z_max=30.0, n=400):
    """Proper 4-volume of the causal past of an observer at redshift z_obs,
    in (c/H0)^4 units:
        V4 = INT_{z_obs}^{z_max} dt'  (4pi/3) chi_lc(z';z_obs)^3 a(z')^3
    with dt' = dz'/((1+z')E(z')), a=1/(1+z'), chi_lc = comoving radius of the
    past lightcone from the observer back to the source at z'.
    Dominated by low/moderate z' (a^3 suppresses early times); converges."""
    zs = np.linspace(z_obs, z_max, n)
    # comoving lightcone radius to each z' (cumulative integral of 1/E from z_obs)
    invE = 1.0 / E(zs)
    chi_lc = integrate.cumulative_trapezoid(invE, zs, initial=0.0)
    a = 1.0 / (1.0 + zs)
    integrand = (4.0 * np.pi / 3.0) * chi_lc ** 3 * a ** 3 * invE / (1.0 + zs)
    return np.trapezoid(integrand, zs)


def lambda_rms_unnorm(z_obs, **kw):
    """Everpresent ansatz (unnormalised): Lambda_rms ~ L1_COEFF / sqrt(V4past)."""
    return L1_COEFF / np.sqrt(past_4volume(z_obs, **kw))


def rho_crit(z):
    """Critical density up to constants: rho_crit ~ 3 H^2 / (8 pi G) ~ E(z)^2."""
    return E(z) ** 2


def everpresent_ratio(z_obs, **kw):
    """R(z) = Lambda_rms / rho_crit -- the 'everpresent' observable.
    Constant in z  <=>  Omega_Lambda ~ O(1) at all epochs (Sorkin's claim)."""
    return lambda_rms_unnorm(z_obs, **kw) / rho_crit(z_obs)


if __name__ == "__main__":
    for z in (0.0, 0.5, 1.0, 2.0, 5.0):
        v4 = past_4volume(z)
        print(f"z={z:4.1f}  V4past={v4:.4e}  Lrms~{lambda_rms_unnorm(z):.4e}  "
              f"rho_crit~{rho_crit(z):.4e}  R={everpresent_ratio(z):.4e}")
