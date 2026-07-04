"""fm2_core.py -- two-phase orientation-ferromagnet engine for FM2_TWO_PHASE.

DATA GENERATOR for the FM2 campaign (the "two phases = dark matter + MOND"
hypothesis).  Contains NO cosmology interpretation: the words "dark matter" /
"resolve S8" / "sigma8" live ONLY in the synthesis (COMPARISON ONLY).  This module
knows the microscopic O(3) orientation ferromagnet that E1 identified as the vacuum,
extended with the two probes FM2 needs:

  * a PERIODIC L^3 O(3) Heisenberg lattice  E = -J sum_<ij> n_i.n_j - h sum_i n_i.z
    (the external field h represents the gravitational gradient g of the DEV; a0 is
    mapped to the field scale where the response leaves the linear regime), with a
    vectorised checkerboard Metropolis at beta=1 (same convention as
    orientation_core: J = coupling, large J = ordered/cold);

  * the LONGITUDINAL susceptibility chi_par(h) = d<m_par>/dh -- the microscopic
    response function that FM2-1 maps to the MOND interpolation nu(g/a0).  In the
    ordered phase of a 3D O(3) magnet the Goldstone (spin-wave) fluctuations make
    chi_par DIVERGE as h^{-1/2} as h->0 (Brezin-Wallace coexistence anomaly) --
    exactly the deep-MOND nu = 1/sqrt(g/a0).  FM2-1 measures whether this divergence
    is SUSTAINED (C1, runaway) or SATURATES at a second scale h_c (the second
    transition a_c2);

  * the spin stiffness rho_s (helicity modulus) and order-parameter susceptibility
    chi, whose ratio gives the Goldstone sound speed c_s = sqrt(rho_s/chi) that FM2-2
    compares to the magnon speed of E2 (c=0.98) to test the Jeans-suppression knob.

Anti-circularity: a0 comes from SPARC (mapped to the field scale here, NOT fitted to
the CMB); the second-transition scale a_c2 and the sound speed c_s are MEASURED on
the lattice; no sigma8/KiDS value is ever inserted.  The O(3) Heisenberg energy and
the beta=1 convention follow results/.../orientation/orientation_core.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]                       # .../TEIC
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))


# ====================================================================== #
# Periodic O(3) Heisenberg lattice with external field
# ====================================================================== #
def _normalize(v, eps=1e-12):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + eps)


class O3Lattice:
    """Periodic L^3 O(3) ferromagnet, energy  E = -J sum_<ij> n_i.n_j - h sum n_i.zhat.

    Vectorised checkerboard Metropolis at beta=1 (J = coupling).  The field h points
    along +z and represents the external gravitational gradient g of the DEV.
    """

    def __init__(self, L, J, h=0.0, seed=0, step=0.5, hate=(0.0, 0.0, 1.0)):
        self.L = int(L)
        self.J = float(J)
        self.h = float(h)
        self.hhat = _normalize(np.asarray(hate, float))
        self.rng = np.random.default_rng(seed)
        self.step = float(step)
        # start ALIGNED with the field (ordered seed) so we probe the ordered branch
        self.n = np.tile(self.hhat, (self.L, self.L, self.L, 1)).astype(float)
        g = np.arange(self.L)
        I, Jx, K = np.meshgrid(g, g, g, indexing="ij")
        self.parity = (I + Jx + K) % 2
        self.masks = [self.parity == 0, self.parity == 1]

    # ---- neighbour sum (periodic) ----
    def _neighbour_sum(self):
        n = self.n
        H = np.zeros_like(n)
        for ax in range(3):
            H += np.roll(n, +1, axis=ax)
            H += np.roll(n, -1, axis=ax)
        return H

    # ---- one Metropolis sweep (checkerboard, vectorised) ----
    def sweep(self, adapt=True, target=0.4):
        acc = 0; tot = 0
        Hfield = self.h * self.hhat
        for mask in self.masks:
            H = self._neighbour_sum()
            old = self.n[mask]
            Hm = self.J * H[mask] + Hfield                # effective local field
            v = old + self.step * self.rng.standard_normal(old.shape)
            prop = _normalize(v)
            dE = -np.einsum("ij,ij->i", prop - old, Hm)   # E = -(prop).(JH + h zhat)
            p = np.exp(-np.clip(dE, 0.0, 50.0))
            a = self.rng.random(old.shape[0]) < p
            self.n[mask] = np.where(a[:, None], prop, old)
            acc += int(a.sum()); tot += a.size
        if adapt:
            ar = acc / max(tot, 1)
            if ar > target + 0.1:
                self.step *= 1.1
            elif ar < target - 0.1:
                self.step *= 0.9
            self.step = float(np.clip(self.step, 1e-3, 3.0))
        return acc / max(tot, 1)

    def equilibrate(self, n_burn):
        for _ in range(n_burn):
            self.sweep()

    # ---- observables ----
    def magnetization_vec(self):
        return self.n.reshape(-1, 3).mean(axis=0)

    def m_parallel(self):
        """Magnetization projected on the field axis (the longitudinal order)."""
        return float(self.magnetization_vec() @ self.hhat)

    def m_abs(self):
        return float(np.linalg.norm(self.magnetization_vec()))

    def energy(self):
        H = self._neighbour_sum()
        bond = -0.5 * self.J * np.sum(self.n * H)
        field = -self.h * np.sum(self.n @ self.hhat)
        return float(bond + field)


# ====================================================================== #
# Sampling helpers
# ====================================================================== #
def sample_observables(L, J, h, seed, n_burn, n_meas, meas_every=2):
    """Equilibrate then collect time series of m_par, m_abs, and the transverse
    magnetization vector (for chi_perp).  Returns dict of arrays."""
    lat = O3Lattice(L, J, h, seed=seed)
    lat.equilibrate(n_burn)
    mpar, mabs, Mvecs, Es = [], [], [], []
    taken = 0; s = 0
    while taken < n_meas:
        lat.sweep()
        s += 1
        if s % meas_every == 0:
            Mvec = lat.magnetization_vec()
            mpar.append(float(Mvec @ lat.hhat))
            mabs.append(float(np.linalg.norm(Mvec)))
            Mvecs.append(Mvec)
            Es.append(lat.energy())
            taken += 1
    return {"m_par": np.array(mpar), "m_abs": np.array(mabs),
            "Mvec": np.array(Mvecs), "E": np.array(Es), "lat": lat}


def chi_parallel(L, J, h, seed, n_burn, n_meas, dh=None):
    """Longitudinal susceptibility chi_par = d<m_par>/dh by symmetric finite
    difference (robust to the Goldstone-divergent fluctuation estimator).  dh scaled
    to h so the derivative is local on a log grid."""
    if dh is None:
        dh = max(0.15 * h, 1e-4)
    out = {}
    for tag, hh in (("plus", h + dh), ("minus", max(h - dh, 1e-6))):
        s = sample_observables(L, J, hh, seed, n_burn, n_meas)
        out[tag] = float(s["m_par"].mean()), hh
    (mp, hp), (mm, hm) = out["plus"], out["minus"]
    return (mp - mm) / (hp - hm)


# ====================================================================== #
# Spin stiffness (helicity modulus) and sound speed
# ====================================================================== #
def _helicity_pieces(n, J, a, mu):
    """Per-config (curvature, current) for generator a-hat, lattice direction mu.
        curvature = J sum_{<ij>||mu} (n_i.n_j - (a.n_i)(a.n_j))
        current   = J sum_{<ij>||mu} a.(n_i x n_j)
    The helicity modulus is (<curvature> - <current^2>)/V (beta=1; <current>=0)."""
    nj = np.roll(n, -1, axis=mu)
    dot = np.sum(n * nj, axis=-1)
    ai = n @ a; aj = nj @ a
    curv = J * np.sum(dot - ai * aj)
    cross = np.cross(n, nj)
    cur = J * np.sum(cross @ a)
    return float(curv), float(cur)


def helicity_modulus_series(L, J, seed, n_burn, n_meas, meas_every=2, axes=None):
    """O(3) helicity modulus (spin stiffness) rho_s = (<curv> - <I^2>)/V at zero
    field, beta=1, ENSEMBLE-averaged over equilibrium configs (the correct estimator:
    the current-variance term needs a thermal average, not a single snapshot).
    Averaged over the 3 lattice directions mu and over the supplied generator axes
    (default the 3 cartesian axes).  Returns (rho_s, m_abs)."""
    if axes is None:
        axes = [np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0])]
    lat = O3Lattice(L, J, 0.0, seed=seed)
    lat.equilibrate(n_burn)
    V = L ** 3
    curv_acc = np.zeros((len(axes), 3))
    cur2_acc = np.zeros((len(axes), 3))
    mabs = []
    taken = 0; s = 0
    while taken < n_meas:
        lat.sweep(); s += 1
        if s % meas_every == 0:
            for ia, a in enumerate(axes):
                for mu in range(3):
                    cv, cu = _helicity_pieces(lat.n, J, a, mu)
                    curv_acc[ia, mu] += cv
                    cur2_acc[ia, mu] += cu ** 2
            mabs.append(lat.m_abs())
            taken += 1
    curv_mean = curv_acc / taken
    cur2_mean = cur2_acc / taken
    rho = float(np.mean((curv_mean - cur2_mean) / V))
    return rho, float(np.mean(mabs))


def order_susceptibility(series):
    """Order-parameter susceptibility chi = beta * V * Var(|M|) (beta=1, V absorbed
    via M being the per-site mean: chi = V*Var(m_abs))."""
    m = series["m_abs"]
    V = series["lat"].L ** 3
    return float(V * np.var(m))


def sound_speed(L, J, seed, n_burn, n_meas):
    """Goldstone sound speed proxy c_s = sqrt(rho_s / chi) in lattice units, measured
    in the ordered phase at zero field.  rho_s = helicity modulus (ensemble-averaged),
    chi = order-param susceptibility.  Returns (c_s, rho_s, chi, m_abs)."""
    s = sample_observables(L, J, 0.0, seed, n_burn, n_meas)
    chi = order_susceptibility(s)
    rho, mabs = helicity_modulus_series(L, J, seed, n_burn, n_meas)
    cs = float(np.sqrt(max(rho, 0.0) / chi)) if chi > 1e-12 else float("inf")
    return cs, rho, chi, mabs


# ====================================================================== #
# self-test
# ====================================================================== #
if __name__ == "__main__":
    print("fm2_core self-test")
    # ordered vs disordered: m_abs should lift above J_c~0.69 (3D O(3))
    for J in (0.4, 0.7, 1.2):
        s = sample_observables(12, J, 0.0, seed=0, n_burn=300, n_meas=120)
        print(f"  J={J:.2f}  <m_abs>={s['m_abs'].mean():.3f}  "
              f"(ordered if >~0.3 for L=12)")
    # external field aligns the magnet
    s0 = sample_observables(12, 1.0, 0.0, 0, 300, 120)
    sh = sample_observables(12, 1.0, 0.3, 0, 300, 120)
    print(f"  J=1.0: m_par(h=0)={s0['m_par'].mean():+.3f}  "
          f"m_par(h=0.3)={sh['m_par'].mean():+.3f} (field aligns)")
    # stiffness positive in ordered phase, sound speed finite; rho_s drops near J_c
    for J in (0.8, 1.2, 2.0):
        cs, rho, chi, m = sound_speed(12, J, 0, 400, 150)
        print(f"  J={J:.1f}: rho_s={rho:.3f} chi={chi:.4f} c_s={cs:.3f} m={m:.3f}")
    cs, rho, chi, m = sound_speed(12, 1.2, 0, 400, 150)
    assert rho > 0
    print("self-test OK")
