"""he3_core.py -- HIGH_ENERGY_REGIME / HE3 engine: the causal ferromagnet in an INTENSE
orientation field (the Schwinger-effect analogue).

E1 established that the causal vacuum IS an ordered O(3) orientation ferromagnet
(n_i in S^2, energy E = -J sum n_i.n_j); E2 that its Goldstone waves are the magnons (the
photon analogue, omega = c k); E3 that hedgehog point defects (degree B = +/-1, pi_2(S^2)=Z)
are its topological textures.  HE3 asks the Schwinger question: does an INTENSE applied
orientation field h create hedgehog / anti-hedgehog PAIRS out of the ordered vacuum,
spontaneously, above a critical field?

This module ADDS to e3_core (which it imports unchanged) only the field h:

  * field_energy / total_energy_h : Zeeman coupling  E_h = -sum_i h_vec(x_i) . n_i, added to
    the e3_core gradient (exchange) energy.
  * llg_evolve : deterministic Landau-Lifshitz-Gilbert precession in the effective field
    H_eff = (neighbour sum) + h_vec,   dn/dt = -n x H_eff - lambda n x (n x H_eff),
    renormalised each step.  This is the closest lattice analogue of the field DRIVING the
    orientation dynamics at finite speed (the magnon sector of E2 is this linearised); a
    strong field that could wind the texture would show up here.
  * metropolis_h : finite-temperature Metropolis with the field (e3_core.relax_mc + Zeeman),
    so thermal NUCLEATION over a barrier (the analogue of Schwinger tunnelling) is allowed.
  * field protocols : anti-aligned (false-vacuum / the cleanest Schwinger setup), transverse,
    and a hedgehog-favouring radial probe field.
  * the decisive observables come straight from e3_core: charge_field -> (n_pos, n_neg) defect
    counts, topological_charge -> net B, gradient_energy.  PAIR CREATION = n_pos and n_neg
    both rise from 0 to >= 1 with net B ~ 0.

Anti-circularity: B is e3_core's solid-angle degree (pure geometry); J, h are the only
couplings; no critical field, no pair-creation rate is inserted.  "Schwinger", "pair
creation", "false vacuum" are COMPARISON-ONLY names.

DEATH CRITERION (pre-registered, HIGH_ENERGY_REGIME.md): no pair creation by the field at
any strength -> the vacuum-structure frontier stays where E3 put it.  Not tuned.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
E3 = HERE.parents[0] / "orientation" / "e3"
sys.path.insert(0, str(E3))

import e3_core as e3   # noqa: E402

OUT = HERE


# --------------------------------------------------------------------------- #
# field builders (uniform direction, or a per-site field)
# --------------------------------------------------------------------------- #
def uniform_field(L, h, direction=(0, 0, 1)):
    """Uniform Zeeman field h * direction_hat, shape (L,L,L,3)."""
    d = np.asarray(direction, float)
    d = d / (np.linalg.norm(d) + 1e-12)
    f = np.zeros((L, L, L, 3))
    f[...] = h * d
    return f


def radial_field(L, h, center=None):
    """A hedgehog-FAVOURING field h * r_hat (points outward).  This is the most generous
    Schwinger probe: a field whose own texture is that of a defect, so if ANY field can
    nucleate a hedgehog it is this one.  (A genuine creation must still come from the
    DYNAMICS, not from the field literally being painted on -- we start from the ordered
    state and let it evolve.)"""
    center = e3.default_center(L) if center is None else np.asarray(center, float)
    X = e3.lattice_coords(L)
    d = X - center
    r = np.linalg.norm(d, axis=-1, keepdims=True)
    rhat = np.where(r > 1e-9, d / (r + 1e-12), np.array([0.0, 0.0, 1.0]))
    return h * rhat


# --------------------------------------------------------------------------- #
# energy with field
# --------------------------------------------------------------------------- #
def field_energy(n, h_field):
    """Zeeman energy E_h = -sum_i h_vec_i . n_i."""
    return float(-np.sum(h_field * n))


def total_energy_h(n, h_field):
    """Exchange (e3_core.gradient_energy) + Zeeman."""
    return e3.gradient_energy(n) + field_energy(n, h_field)


# --------------------------------------------------------------------------- #
# Landau-Lifshitz-Gilbert precession in the effective field
# --------------------------------------------------------------------------- #
# =========================================================================== #
# SPECKLE-PROOF defect counting.
# A boosted / thermalised O(3) field is full of short-wavelength wrinkles, and EACH wrinkle
# carries a fractional solid angle, so a raw connected-component count of the per-cube charge
# explodes into the hundreds (lattice UV noise, NOT defects) -- the exact pathology FL3 hit
# with its baryon density.  We use the same fix FL3 used: a localized topological defect is a
# dual cube whose charge is a genuine INTEGER unit |q| ~ 1 (a lattice monopole); speckle has
# |q| << 1 per cube.  We count cubes with q > +0.5 and q < -0.5 (n_pos, n_neg), and ALSO
# report the radiation-proof smoothed matter content Q_def = sum |gaussian_smooth(q)| (the
# E3b/FL3 trick): ~0 for the ordered vacuum, ~1 per genuine hedgehog.
# =========================================================================== #
def count_defects(n, q_cut=0.5, smooth_sigma=1.0):
    """Return (n_pos, n_neg, Q_def, B_net): lattice-monopole counts (|q|>q_cut), the
    smoothed topological-matter content, and the net charge."""
    from scipy.ndimage import label, gaussian_filter
    q = e3.charge_field(n)
    n_pos = int(label(q > q_cut)[1])
    n_neg = int(label(q < -q_cut)[1])
    Q_def = float(np.sum(np.abs(gaussian_filter(q, smooth_sigma, mode="nearest"))))
    return n_pos, n_neg, Q_def, float(q.sum())


def llg_evolve(n0, h_field, n_steps, dt=0.05, lam=0.3, record_every=50,
               seed=None, noise=0.0):
    """Deterministic LLG: H_eff = neighbour_sum(n) + h_field;
        dn/dt = -n x H_eff - lam n x (n x H_eff),
    explicit step + renormalise.  `noise` adds a small random transverse kick each step
    (a thermal-fluctuation seed so an unstable ordered state can start to tip).  Returns
    (traj of measure-dicts incl. defect counts, final n)."""
    n = n0.copy()
    rng = np.random.default_rng(0 if seed is None else seed)
    traj = []

    def snap(t):
        npos, nneg, Qd, B = count_defects(n)
        return {"t": t, "B": B, "E_ex": e3.gradient_energy(n),
                "E_h": field_energy(n, h_field), "n_pos": npos, "n_neg": nneg,
                "Q_def": Qd, "r_eff": e3.r_eff(n)}

    traj.append(snap(0))
    for t in range(1, n_steps + 1):
        H = e3._neighbour_sum(n) + h_field
        nxH = np.cross(n, H)
        damp = np.cross(n, nxH)
        n = n - dt * nxH - dt * lam * damp
        if noise > 0:
            n = n + noise * rng.standard_normal(n.shape)
        n = e3._normalize(n)
        if t % record_every == 0 or t == n_steps:
            traj.append(snap(t))
    return traj, n


def metropolis_h(n0, h_field, J, n_steps, seed=0, step=0.5, record_every=50,
                 adapt=True, target=0.4):
    """Finite-temperature Metropolis with the Zeeman field (checkerboard, open BC).  Energy
    = -J sum n_i.n_j - sum h_i.n_i; J large = cold.  Thermal hops let the system NUCLEATE
    over a barrier (the tunnelling analogue).  Returns (traj, final n)."""
    n = n0.copy()
    L = n.shape[0]
    rng = np.random.default_rng(seed)
    g = np.arange(L)
    I, Ji, K = np.meshgrid(g, g, g, indexing="ij")
    parity = (I + Ji + K) % 2
    masks = [parity == 0, parity == 1]
    traj = []

    def snap(t):
        npos, nneg, Qd, B = count_defects(n)
        return {"t": t, "B": B, "E_ex": e3.gradient_energy(n),
                "E_h": field_energy(n, h_field), "n_pos": npos, "n_neg": nneg,
                "Q_def": Qd, "r_eff": e3.r_eff(n)}

    traj.append(snap(0))
    for t in range(1, n_steps + 1):
        for mask in masks:
            H = e3._neighbour_sum(n)
            old = n[mask]
            Hm = H[mask]
            hm = h_field[mask]
            v = old + step * rng.standard_normal(old.shape)
            prop = e3._normalize(v)
            dE = -J * np.einsum("...i,...i->...", prop - old, Hm) \
                 - np.einsum("...i,...i->...", prop - old, hm)
            p = np.exp(-np.clip(dE, 0.0, 50.0))
            acc = rng.random(old.shape[0]) < p
            n[mask] = np.where(acc[:, None], prop, old)
        if t % record_every == 0 or t == n_steps:
            traj.append(snap(t))
    return traj, n


def cooled_defects(n, steps=150, dt=0.15):
    """Defect counts AFTER zero-field gradient-flow cooling (removes UV wrinkles that carry
    spurious fractional solid angle), the standard 'cool before counting the integer'
    protocol.  Cooling is the HONEST test: a genuine defect survives gradient flow; speckle
    melts.  Returns (B_net, n_pos, n_neg, Q_def) using the speckle-proof |q|>0.5 monopole
    count and the smoothed matter content."""
    _, nc = e3.relax_gradient(n, n_steps=steps, dt=dt, record_every=steps)
    npos, nneg, Qd, B = count_defects(nc)
    return (B, npos, nneg, Qd)
