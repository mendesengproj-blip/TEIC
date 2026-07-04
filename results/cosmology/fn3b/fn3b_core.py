"""fn3b_core.py -- second-scale-for-DM engine for FN3b_SECOND_FIELD.

DATA GENERATOR for FN3b (does the DEV have a natural f~1e17 GeV without breaking
galaxy phenomenology?).  Contains NO verdict: "promising"/"death" live only in the
.md reports.  FN3b-0 (analytic gate) found paths A(free-mass) and C converge to the
SAME relic -- a misalignment scalar with f=theta0*M_Pl ~ GUT scale and m in the
fuzzy band -- so this engine focuses there.  It knows:

  * the misalignment relic (reused from fn3_core: canonical closed form + f_A that
    gives Omega=0.12) re-expressed as the REQUIRED initial misalignment
    theta0_req(m) = f_req/M_Pl ;

  * the oscillation epoch z_osc(m) (3H=m): a field must oscillate (turn cold) BEFORE
    recombination (z~1100) or it behaves as dark energy, not dark matter ;

  * the frozen-field overclosure ratio rho_frozen/rho_crit for a light field that has
    not yet oscillated (the Path-A dark-energy death) ;

  * the NATURAL theta0 measured on the lattice: the rms orientation-fluctuation
    amplitude in E1's disordered / near-critical O(3) vacuum (orientation_core) --
    grounds theta0 in the substrate instead of assuming it (anti-circular).

Anti-circularity: m from Paper II / lattice; relic from field dynamics; Omega_DM=0.12,
Lyman-alpha (m>2e-21 eV for 100% DM) and z_rec are COMPARISON ONLY.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                                  # .../TEIC
sys.path.insert(0, str(ROOT / "results" / "cosmology" / "fn3"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))

import fn3_core as c                                    # noqa: E402  (relic engine)

# ---- constants ------------------------------------------------------------- #
M_PL_GEV = c.M_PL_GEV                                   # 1.22e19 GeV
H0_EV = c.H0_EV
OMEGA_M = c.OMEGA_M
Z_REC = 1100.0                                          # recombination
LYA_100PCT_FLOOR = 2.0e-21                              # eV (100%-DM Lyman-alpha bound)
M_SLIP_BOUND = 6.4e-30                                  # eV (DEV slip-mediator upper bound)
RHO_CRIT_EV4 = 0.45 * c.RHO_CRIT_OVER_H2_EV4            # ~3.6e-11 eV^4 (h^2~0.45 today)
E_EM = np.sqrt(4 * np.pi / 137.036)                     # ~0.303 (DEV effective EM coupling)


# ====================================================================== #
# relic re-expressed as the required initial misalignment theta0
# ====================================================================== #
def theta0_required(m_eV, omega_target=0.12):
    """theta0 needed so the misalignment relic reaches Omega h^2 = omega_target,
    with f = theta0 * M_Pl.  theta0_req = f_req(m)/M_Pl."""
    return c.f_A_for_target(m_eV, omega_target) / M_PL_GEV


def z_osc(m_eV):
    """Redshift at oscillation onset 3H=m (general FRW).  A field is cold (matter)
    only AFTER this; before it is frozen (w=-1, dark-energy-like)."""
    f = lambda a: 3.0 * c.H_of_a_eV(a) - m_eV
    # bracket a in (tiny, almost 1); very light fields oscillate at low z (a near 1)
    a_lo, a_hi = 1e-12, 0.999999
    if f(a_hi) > 0:        # 3H(today) still > m -> never oscillated (a_osc > 1)
        return -1.0        # sentinel: not yet oscillating
    a = brentq(f, a_lo, a_hi, xtol=1e-30, rtol=1e-12)
    return 1.0 / a - 1.0


def cold_by_recombination(m_eV):
    """True if the field oscillates (turns cold) before recombination."""
    z = z_osc(m_eV)
    return z > Z_REC


def overclosure_ratio(m_eV, theta0):
    """rho_frozen/rho_crit for a field frozen at amplitude phi0=theta0*M_Pl that has
    NOT yet oscillated (relevant when z_osc < 0 or the field is dark-energy-like).
    rho_frozen = 1/2 m^2 phi0^2."""
    phi0_eV = theta0 * M_PL_GEV * 1e9                   # GeV -> eV
    rho = 0.5 * m_eV ** 2 * phi0_eV ** 2                # eV^4
    return rho / RHO_CRIT_EV4


def lya_safe_100pct(m_eV):
    """True if mass is heavy enough to be 100% of DM without violating Lyman-alpha."""
    return m_eV >= LYA_100PCT_FLOOR


def stueckelberg_vev_GeV(m_A_eV):
    """Path B: the Stueckelberg vev v=m_A/e bounds the misalignment amplitude."""
    return (m_A_eV / E_EM) * 1e-9                        # eV -> GeV


def galactic_scale_eV():
    """(kpc)^-1 in eV -- the screening scale for Path C (chi heavy if m_chi >> this)."""
    return 197.327e-9 / 3.0856775815e19                 # hbar c / kpc


# ====================================================================== #
# NATURAL theta0 from the lattice (E1 disordered / near-critical O(3) vacuum)
# ====================================================================== #
def lattice_theta0(L=12, J_list=(0.0, 0.04, 0.08), n_burn=120, seed=0):
    """Measure the natural orientation-fluctuation amplitude theta0 in E1's O(3)
    vacuum on a periodic L^3 lattice.  theta0 here = rms of a spin component
    sqrt(<n_z^2>) (for fully disordered O(3) this is 1/sqrt(3)=0.577) and the mean
    polar misalignment angle <|acos(n_z)| - pi/2>.  Returns rows over J with the
    order parameter (magnetization) to show the disordered phase.  Grounds the
    'natural theta0 ~ O(1)' assumption used by paths A/C in the substrate."""
    from orientation_core import O3Model, lattice_periodic
    g = lattice_periodic((L, L, L))
    rows = []
    for J in J_list:
        model = O3Model(g, J, seed=seed)
        model.equilibrate(n_burn)
        comps = model.corr_arrays()                     # [n_x, n_y, n_z]
        nz = np.asarray(comps[2])
        rms_comp = float(np.sqrt(np.mean(nz ** 2)))     # ~0.577 disordered
        # rms full 3D displacement of a spin from a fixed axis (the misalignment)
        # angle from +z axis; rms angle / pi as a dimensionless theta0 proxy
        ang = np.arccos(np.clip(nz, -1, 1))
        theta0_ang = float(np.sqrt(np.mean(ang ** 2)) / np.pi)
        rows.append({"J": J, "order_param": model.order_parameter(),
                     "rms_component": rms_comp, "theta0_angle_over_pi": theta0_ang})
    return rows


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("fn3b_core self-test")
    print(f"  e_EM={E_EM:.3f}  rho_crit~{RHO_CRIT_EV4:.2e} eV^4  galactic scale={galactic_scale_eV():.2e} eV")
    for m in (6.4e-30, 1e-28, 1e-22, 2e-21, 1e-20):
        zo = z_osc(m)
        print(f"  m={m:.1e} eV: theta0_req={theta0_required(m):.2e}  z_osc={zo:.1e}  "
              f"cold_by_rec={cold_by_recombination(m)}  Lya_safe={lya_safe_100pct(m)}")
    print(f"  overclosure (m=6.4e-30, theta0=1) = {overclosure_ratio(6.4e-30,1.0):.2e}  "
          f"(theta0_max no-overclose = {1/np.sqrt(overclosure_ratio(6.4e-30,1.0)):.2e})")
    print(f"  Stueckelberg vev (m_A=1e-22 eV) = {stueckelberg_vev_GeV(1e-22):.2e} GeV (need ~1e17)")
    print("self-test OK")
