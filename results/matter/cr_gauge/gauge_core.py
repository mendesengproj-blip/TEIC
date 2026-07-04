"""gauge_core.py -- shared engine for the MATTER_CR_GAUGE campaign (G1-G6).

First test of the FULL minimal action with BOTH fields dynamical and coupled:

    S = sum_links Dtau [ 1 - cos( phi_ij + Dtheta_ij ) ] ,

where theta is the scalar (density) field on the SITES and phi is the compact gauge
phase (A_mu) on the LINKS.  The gauge-invariant link phase is the Stueckelberg
combination

    u_i = phi_i + (theta_{i+1} - theta_i) = phi_i + Dtheta_i .

CR_DBI established three structural facts this campaign builds on:
  * the cos EOM IS lattice sine-Gordon (DBI1);
  * the scalar density theta is non-compact => oint Dtheta = 0 => no winding (DBI3);
  * the COMPACT field has stable kinks (mass 8) and transient pairs (DBI4).
What was never tested before: the two fields TOGETHER, coupled inside one cosine.

Field content and why phi (not theta) carries the kinks
-------------------------------------------------------
The single cosine cos(phi + Dtheta) does double duty:
  * with phi = 0 it is the cos of the scalar GRADIENT Dtheta -- exactly DBI's
    force_cos, a massless (gradient-only) scalar => pass-through, NO kinks (DBI3);
  * with theta = 0 it is the cos of the gauge VALUE phi -- a genuine compact (S^1)
    potential 1 - cos(phi) with a mass gap => topological kinks (DBI4).
The gauge field additionally carries its own field-strength (Wilson F^2, established
in BRIDGE_WILSON) gradient-stiffness term, so the phi sector in isolation IS the
standard sine-Gordon model (force_phi == force_sine_gordon_potential up to a global
time-unit factor; kink rest mass 8).  The scalar has NO separate stiffness -- all its
spatial coupling lives inside the cosine.  This asymmetry is the physical statement
that creation lives in the gauge sector.

Lattice normalisation (Option A): the cosine coefficient and the Wilson stiffness are
both fixed at 1/dx^2 so that (i) theta propagates at unit speed (force_theta == DBI's
force_cos when phi=0, so the two chains actually collide in a finite time) and
(ii) the compact kink width equals 1 and is resolved on the grid (force_phi reduces to
(1/dx^2) * DBI4's force when theta=0).  The common 1/dx^2 is a global time-unit
convention; it cancels in every energy-RATIO and conservation check, and the kink rest
MASS is reported with DBI4's own (unscaled) functional so the comparison value stays 8.

ANTI-CIRCULARITY (scanned by tests/test_no_circularity.py over results/matter/):
  * No mc^2 / 2mc^2, no electron/positron, no SR/GR dilation, no complex numbers.
  * Topological charge (winding) is computed from the REAL gauge phase by summing the
    principal-branch link increments -- never from a complex order parameter.
  * QED / e-e+ pair production appears ONLY inside labelled COMPARISON ONLY blocks,
    as an analogy for the measured kink-antikink behaviour, never feeding a generator.

Reuses dbi_core (packets, kink detector, winding, seed stats, IO) and, through it,
complexity_core.  Modifies nothing in R1-R3 / e6-e11 / D1-D3 / M1-S1 / CC / CR / DBI.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "cr_dbi"))
import dbi_core as dbi  # noqa: E402  (packets, kink_count, winding, seed_stats, IO)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi


# --------------------------------------------------------------------------- #
# Grid
# --------------------------------------------------------------------------- #
def make_grid(L=60.0, N=301):
    """1+1D grid.  Default (L=60,N=301 -> dx=0.2) is the cheap sweep grid; the kink
    mass check uses the finer dbi default (dx=0.1) for a clean 7.996 ~ 8."""
    x = np.linspace(-L / 2, L / 2, N)
    dx = float(x[1] - x[0])
    return x, dx


def dt_cfl(dx, safety=0.4):
    """Stable step for the STIFF gauge sector: the phi wave operator has
    omega_max = 2/dx^2, so dt < dx^2; we take a safety fraction of it."""
    return safety * dx ** 2


# --------------------------------------------------------------------------- #
# Coupled forces (the only 'physics' is the cited minimal action's EOM)
# --------------------------------------------------------------------------- #
def link_phase(theta, phi):
    """Stueckelberg-invariant link phase u_i = phi_i + (theta_{i+1}-theta_i),
    length N-1 (link i sits between sites i and i+1; phi_i is the left-site value)."""
    return phi[:-1] + np.diff(theta)


def force_theta(theta, phi, dx):
    """Scalar EOM, delta S / delta theta_i = 0 ->  theta'' = d/dx[ sin(u) ].

        F^theta_i = [ sin(u_i) - sin(u_{i-1}) ] / dx^2 .

    With phi = 0 this is EXACTLY dbi.force_cos (the DBI3 scalar sector): unit-speed,
    massless, pass-through.  Weak field sin(u)->u recovers the linear BD Laplacian.
    """
    u = link_phase(theta, phi)
    s = np.sin(u)
    f = np.zeros_like(theta)
    f[1:-1] = (s[1:] - s[:-1]) / dx ** 2
    return f


def force_phi(theta, phi, dx):
    """Gauge EOM = Wilson F^2 stiffness (Laplacian) + Stueckelberg cosine drag:

        F^phi_i = ( Laplacian(phi)_i - sin(u_i) ) / dx^2 .

    With theta = 0 (u_i = phi_i) this is (1/dx^2) * dbi.force_sine_gordon_potential --
    DBI4's compact sine-Gordon, time-rescaled.  The cosine drag -sin(u)/dx^2 is the
    channel through which a steep scalar gradient (collision) drives the gauge phase.
    """
    u = link_phase(theta, phi)
    lap = np.zeros_like(phi)
    lap[1:-1] = (phi[2:] - 2 * phi[1:-1] + phi[:-2]) / dx ** 2
    sinu_site = np.zeros_like(phi)
    sinu_site[:-1] = np.sin(u)               # site i receives its left link i
    f = np.zeros_like(phi)
    f[1:-1] = (lap[1:-1] - sinu_site[1:-1]) / dx ** 2
    return f


# --------------------------------------------------------------------------- #
# Symplectic coupled evolution (velocity Verlet, both fields together)
# --------------------------------------------------------------------------- #
def evolve_coupled(theta0, vth0, phi0, vph0, dx, dt, nsteps,
                   freeze_theta=False, freeze_phi=False, record_every=0):
    """Leapfrog evolution of the coupled (theta, phi) system, Dirichlet ends.

    freeze_theta / freeze_phi hold that field at its initial value (used for the G1
    pure-sector limit checks).  Returns final (theta, vth, phi, vph) and an optional
    history list of (theta, phi) snapshots.
    """
    theta, vth = theta0.copy(), vth0.copy()
    phi, vph = phi0.copy(), vph0.copy()
    ath = np.zeros_like(theta) if freeze_theta else force_theta(theta, phi, dx)
    aph = np.zeros_like(phi) if freeze_phi else force_phi(theta, phi, dx)
    hist = []
    for n in range(nsteps):
        if not freeze_theta:
            vth_h = vth + 0.5 * dt * ath
            theta = theta + dt * vth_h
            theta[0] = theta0[0]; theta[-1] = theta0[-1]
        if not freeze_phi:
            vph_h = vph + 0.5 * dt * aph
            phi = phi + dt * vph_h
            phi[0] = phi0[0]; phi[-1] = phi0[-1]
        ath = np.zeros_like(theta) if freeze_theta else force_theta(theta, phi, dx)
        aph = np.zeros_like(phi) if freeze_phi else force_phi(theta, phi, dx)
        if not freeze_theta:
            vth = vth_h + 0.5 * dt * ath
            vth[0] = 0.0; vth[-1] = 0.0
        if not freeze_phi:
            vph = vph_h + 0.5 * dt * aph
            vph[0] = 0.0; vph[-1] = 0.0
        if record_every and (n % record_every == 0):
            hist.append((theta.copy(), phi.copy()))
    return theta, vth, phi, vph, hist


# --------------------------------------------------------------------------- #
# Energy: components consistent with the leapfrog (conserved by construction)
# --------------------------------------------------------------------------- #
def energy_components(theta, vth, phi, vph, dx):
    """(E_kin_theta, E_kin_phi, E_wilson, E_cos) for the discrete action.  The kinetic
    metric is m=dx; the Wilson and cosine coefficients are the 1/dx^? that make
    force_theta/force_phi the gradients of this V (so leapfrog conserves the sum)."""
    u = link_phase(theta, phi)
    E_kin_th = 0.5 * dx * float(np.sum(vth ** 2))
    E_kin_ph = 0.5 * dx * float(np.sum(vph ** 2))
    E_wilson = (1.0 / (2.0 * dx ** 3)) * float(np.sum(np.diff(phi) ** 2))
    E_cos = (1.0 / dx) * float(np.sum(1.0 - np.cos(u)))
    return E_kin_th, E_kin_ph, E_wilson, E_cos


def energy_total(theta, vth, phi, vph, dx):
    return float(sum(energy_components(theta, vth, phi, vph, dx)))


def sector_energies(theta, vth, phi, vph, dx):
    """Honest 3-way split for the transfer/collision diagnostics:
        E_theta  = scalar kinetic              (the 'chain' energy)
        E_phi    = gauge kinetic + Wilson F^2   (zero iff phi==0 and vphi==0)
        E_coup   = the Stueckelberg cosine      (shared; = theta-gradient energy at phi=0)
    """
    Ekt, Ekp, Ew, Ec = energy_components(theta, vth, phi, vph, dx)
    return {"E_theta": Ekt, "E_phi": Ekp + Ew, "E_coup": Ec,
            "E_total": Ekt + Ekp + Ew + Ec}


# --------------------------------------------------------------------------- #
# Topological observables on the COMPACT gauge phase (all real-valued)
# --------------------------------------------------------------------------- #
def winding_phi(phi):
    """Net gauge winding W_phi = (1/2pi) oint dphi, computed from the REAL phase by
    summing the principal-branch link increments wrap(dphi) in (-pi, pi].  Integer for
    smooth compact configs; structurally 0 for clamped symmetric ends (=> a created
    kink must be matched by an antikink: charge conservation, G5)."""
    d = np.diff(phi)
    d = (d + np.pi) % TWO_PI - np.pi
    return float(np.sum(d) / TWO_PI)


def kink_count_phi(phi, level=np.pi):
    """Localized gauge cores: rising crossings of phi=pi (reuses the DBI detector,
    validated there on an explicit kink)."""
    return dbi.kink_count(phi, level)


def peak_phi(phi):
    return float(np.max(np.abs(phi)))


# --------------------------------------------------------------------------- #
# Initial data: two scalar chains, gauge phase cold (phi=0)
# --------------------------------------------------------------------------- #
def two_chains(x, amp, x0=8.0, w=2.0, phi0=0.0, noise=0.0, rng=None, vfrac=1.0):
    """Two counter-propagating SCALAR chains (theta packets) colliding at 0, with the
    gauge phase initialised cold and uniform (phi == phi0, vphi == 0).  All the initial
    energy is scalar; G2/G3 watch whether it flows into the gauge sector."""
    th, vth = dbi.two_packets(x, amp, x0=x0, w=w, noise=noise, rng=rng, vfrac=vfrac)
    phi = np.full_like(x, float(phi0))
    vph = np.zeros_like(x)
    return th, vth, phi, vph


def gauge_packets(x, dx, amp, x0=8.0, w=2.5):
    """Two counter-propagating GAUGE packets (phi) colliding at 0, travelling at the
    gauge wave speed c = 1/dx (so the leading dispersion phi_tt = (1/dx^2) phi_xx is a
    travelling solution).  Used in G4/G5 to nucleate a kink-antikink pair directly in
    the gauge sector (theta frozen), isolated from the scalar runaway."""
    c = 1.0 / dx
    phiA = amp * np.exp(-((x + x0) ** 2) / (2 * w ** 2))
    phiB = amp * np.exp(-((x - x0) ** 2) / (2 * w ** 2))
    phi = phiA + phiB
    vph = -(+1) * c * (phiA * (-(x + x0) / w ** 2)) - (-1) * c * (phiB * (-(x - x0) / w ** 2))
    return phi, vph


# --------------------------------------------------------------------------- #
# IO
# --------------------------------------------------------------------------- #
def seed_stats(values):
    return dbi.seed_stats(values)


def save_json(name, payload):
    import json
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    # smoke test: the two limits reduce to DBI, and the coupled energy is conserved
    x, dx = make_grid()
    rng = np.random.default_rng(0)
    th = rng.standard_normal(len(x)) * 0.3
    ph = rng.standard_normal(len(x)) * 0.3
    # theta-pure: force_theta(., phi=0) == dbi.force_cos
    d_th = np.max(np.abs(force_theta(th, np.zeros_like(x), dx) - dbi.force_cos(th, dx)))
    # phi-pure: force_phi(theta=0, .) == dbi.force_sine_gordon_potential / dx^2
    d_ph = np.max(np.abs(force_phi(np.zeros_like(x), ph, dx)
                         - dbi.force_sine_gordon_potential(ph, dx) / dx ** 2))
    print(f"theta-pure limit matches DBI force_cos:      max|diff| = {d_th:.2e}")
    print(f"phi-pure limit matches DBI sine-Gordon/dx^2: max|diff| = {d_ph:.2e}")
    th0, vth0, phi0, vph0 = two_chains(x, 2.0)
    dt = dt_cfl(dx)
    E0 = energy_total(th0, vth0, phi0, vph0, dx)
    thf, vthf, phif, vphf, _ = evolve_coupled(th0, vth0, phi0, vph0, dx, dt, 800)
    E1 = energy_total(thf, vthf, phif, vphf, dx)
    print(f"coupled energy drift over 800 steps: {abs(E1 - E0) / E0:.2e}")
