"""dbi_core.py -- shared engine for the MATTER_CR_DBI campaign (DBI1-DBI6).

Tests whether the NON-LINEAR (cos) sector of the minimal action creates loops, after
CR3 refuted the linear BD action.  The minimal action is

    S_DBI = sum_links Dtau [1 - cos(phi + Dtheta)] ,

whose Euler-Lagrange equation is the lattice SINE-GORDON wave equation; its weak-field
limit sin(u) -> u is exactly the linear BD wave equation (box theta = J).  We evolve a
1+1D field with a symplectic (leapfrog/Verlet) integrator and look for persistent
localized structures (kink / breather cores) and topological winding -- the dynamical
analogue of created matter.  Modifies nothing in R1-R3 / e6-e11 / D1-D3 / M1-S1 / CC /
CR; reuses the radial Poisson solver of the complexity campaign for the static check.

ANTI-CIRCULARITY (scanned by tests/test_no_circularity.py over results/matter/):
  * pi appears ONLY as the critical point of the cosine (a mathematical property),
    never inserted as a "creation threshold"; rho_DBI is MEASURED.
  * No mc^2 / 2mc^2 / electron / positron; no SR/GR dilation formula; no complex
    numbers (winding is computed from the real field by summing link phase increments).

The compact-vs-noncompact question
-----------------------------------
Topological winding needs a COMPACT (S^1) field.  The density field theta = drho/rho
(D3) is real/non-compact (single vacuum) -> the cosine only saturates, no winding.
The gauge phase is compact.  We run BOTH a non-compact (physical density) collision and
a compact-field control, so we can tell "the detector cannot see winding" from "the
physics does not produce it".
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "results" / "matter" / "complexity"))
import complexity_core as cx  # noqa: E402  (radial Poisson solver for the static check)

OUTDIR = Path(__file__).resolve().parent
OUTDIR.mkdir(parents=True, exist_ok=True)

TWO_PI = 2.0 * np.pi


# --------------------------------------------------------------------------- #
# 1+1D grid and forces (the only "physics" is the cited cos action's EOM)
# --------------------------------------------------------------------------- #
def make_grid(L=80.0, N=801):
    x = np.linspace(-L / 2, L / 2, N)
    dx = float(x[1] - x[0])
    return x, dx


def force_linear(theta, dx):
    """BD / linear wave force = discrete Laplacian (Dirichlet ends).  This is the
    weak-field limit of the cos force below (sin(u) -> u)."""
    f = np.zeros_like(theta)
    f[1:-1] = (theta[2:] - 2 * theta[1:-1] + theta[:-2]) / dx ** 2
    return f


def force_cos(theta, dx):
    """DBI / sine-Gordon force = d/dx[ sin(d theta) ] on the lattice (Dirichlet ends).

        F_i = [ sin(theta_{i+1}-theta_i) - sin(theta_i-theta_{i-1}) ] / dx^2

    Weak field: sin(u) ~ u  =>  F -> Laplacian = force_linear (the BD limit, verified
    in DBI1).  Bounded sin => the force saturates; no explosion.
    """
    f = np.zeros_like(theta)
    s = np.sin(np.diff(theta))               # link phases sin(u_i), length N-1
    f[1:-1] = (s[1:] - s[:-1]) / dx ** 2
    return f


def force_sine_gordon_potential(theta, dx):
    """COMPACT-FIELD control: standard sine-Gordon with a cos POTENTIAL of the field
    VALUE, V(theta)=1-cos(theta), giving F = Laplacian - sin(theta).

    This is NOT the minimal TEIC action (whose cos is of the link GRADIENT, force_cos);
    it is the genuinely COMPACT (S^1-valued) field, with degenerate vacua at theta=2pi n
    and topological kinks.  Used only to show the creation mechanism EXISTS if the field
    is compact -- i.e. to separate 'the detector cannot see winding' from 'the scalar
    density sector does not produce it'.  Its weak-field limit is a massive Klein-Gordon
    field, not BD, so it is never used for the DBI1 BD-reproduction check.
    """
    return force_linear(theta, dx) - np.sin(theta)


def evolve(theta0, v0, force_fn, dx, dt, nsteps, record_every=0):
    """Symplectic leapfrog (velocity Verlet) evolution with Dirichlet ends.

    Returns (theta, v) at the final step, plus an optional (k, N) history of theta.
    """
    theta = theta0.copy()
    v = v0.copy()
    a = force_fn(theta, dx)
    hist = []
    for n in range(nsteps):
        v_half = v + 0.5 * dt * a
        theta = theta + dt * v_half
        theta[0] = theta0[0]; theta[-1] = theta0[-1]      # clamp ends
        a = force_fn(theta, dx)
        v = v_half + 0.5 * dt * a
        v[0] = 0.0; v[-1] = 0.0
        if record_every and (n % record_every == 0):
            hist.append(theta.copy())
    return theta, v, (np.array(hist) if hist else None)


# --------------------------------------------------------------------------- #
# Counter-propagating wave packets (the two "chains")
# --------------------------------------------------------------------------- #
def packet(x, amp, x0, w, direction):
    """A Gaussian field packet of amplitude ``amp`` at ``x0``, width ``w``, moving with
    unit speed in ``direction`` (+1 right, -1 left).  For the wave equation a packet
    f(x - direction t) has d_t theta = -direction * d_x theta."""
    th = amp * np.exp(-((x - x0) ** 2) / (2 * w ** 2))
    dth_dx = th * (-(x - x0) / w ** 2)
    v = -direction * dth_dx
    return th, v


def two_packets(x, amp, x0=18.0, w=2.5, noise=0.0, rng=None, vfrac=1.0):
    """Two counter-propagating packets (A from left +, B from right -), colliding at 0.

    ``amp`` is the field amplitude (the 'energy density' / rho proxy).  Optional small
    IC noise (seed sensitivity) and a velocity fraction vfrac (<1 emulates an oblique /
    slower approach, so the packets dwell longer in the overlap region).
    """
    thA, vA = packet(x, amp, -x0, w, +1)
    thB, vB = packet(x, amp, +x0, w, -1)
    th = thA + thB
    v = vfrac * (vA + vB)
    if noise and rng is not None:
        th = th + noise * amp * rng.standard_normal(len(x))
    return th, v


# --------------------------------------------------------------------------- #
# Order parameters (all real-valued; no complex phase)
# --------------------------------------------------------------------------- #
def phase_max(theta):
    """Max link phase |theta_{i+1} - theta_i| -- the (phi+Dtheta)_max of the config."""
    return float(np.max(np.abs(np.diff(theta))))


def energy_density(theta, v, dx, kind="cos"):
    """Local energy density e_i = 1/2 v^2 + potential, potential from the cos (or
    quadratic) action.  Used to localize persistent structures."""
    pot = np.zeros_like(theta)
    d = np.diff(theta)
    if kind == "cos":
        link = (1.0 - np.cos(d)) / dx ** 2
    else:
        link = 0.5 * d ** 2 / dx ** 2
    pot[1:-1] = 0.5 * (link[:-1] + link[1:])
    return 0.5 * v ** 2 + pot


def energy_density_sg(theta, v, dx):
    """Energy density of the COMPACT sine-Gordon field: 1/2 v^2 + 1/2 (d_x theta)^2 +
    (1 - cos theta).  The potential is of the FIELD VALUE (compact target), distinct
    from energy_density(kind='cos') whose potential is of the link GRADIENT (the DBI
    action).  Used for the compact-field kink mass / conservation in DBI4."""
    grad = np.zeros_like(theta)
    grad[1:-1] = (theta[2:] - theta[:-2]) / (2 * dx)
    return 0.5 * v ** 2 + 0.5 * grad ** 2 + (1.0 - np.cos(theta))


def central_energy(theta, v, x, dx, half=4.0, kind="cos"):
    """Total energy within |x| < half (the collision core)."""
    e = energy_density(theta, v, dx, kind)
    m = np.abs(x) < half
    return float(np.sum(e[m]) * dx)


def winding_net(theta):
    """Net winding (theta[-1]-theta[0])/2pi.  ~0 for clamped symmetric ends; a
    kink-antikink PAIR has cancelling local windings, so see kink_count too."""
    return float((theta[-1] - theta[0]) / TWO_PI)


def kink_count(theta, level=np.pi):
    """Number of localized 2pi-structures: count upward crossings of theta = pi (each
    kink-antikink/breather core climbs above pi and returns).  A robust, real-valued
    topological order parameter for the non-compact field."""
    above = theta > level
    # rising edges of the 'above pi' mask
    return int(np.sum((~above[:-1]) & above[1:]))


def peak_theta(theta):
    return float(np.max(np.abs(theta)))


# --------------------------------------------------------------------------- #
# Static reduction (DBI1 D3 check): weak-field cos static solve = radial Poisson
# --------------------------------------------------------------------------- #
def radial_static(centers, sv, q, K=1.0):
    """Reuse the complexity radial Poisson solver (the weak-field static limit of the
    cos action, sin->linear, is exactly D3's discrete Poisson) -> theta ~ 1/r."""
    return cx.radial_solve(centers, sv, q, K)


# --------------------------------------------------------------------------- #
# IO
# --------------------------------------------------------------------------- #
def seed_stats(values):
    return cx.seed_stats(values)


def save_json(name, payload):
    path = OUTDIR / f"{name}.json"
    path.write_text(json.dumps(payload, indent=2))
    return path


if __name__ == "__main__":
    x, dx = make_grid()
    dt = 0.2 * dx
    # weak field: cos and linear evolution must agree
    th0, v0 = two_packets(x, amp=0.02)
    thc, _, _ = evolve(th0, v0, force_cos, dx, dt, 1500)
    thl, _, _ = evolve(th0, v0, force_linear, dx, dt, 1500)
    rel = np.max(np.abs(thc - thl)) / np.max(np.abs(thl))
    print(f"weak-field cos vs linear max rel diff = {rel:.2e} (want small)")
    # strong field: does theta climb above pi anywhere?
    th0, v0 = two_packets(x, amp=3.0)
    thc, vc, _ = evolve(th0, v0, force_cos, dx, dt, 1800)
    print(f"strong field: peak|theta| late = {peak_theta(thc):.2f}, "
          f"kinks = {kink_count(thc)}, central E = {central_energy(thc, vc, x, dx):.3f}")
