"""a5_higgs_core.py -- 4D abelian-Higgs engine for the A5_ANDERSON_HIGGS campaign:
an O(3) orientation ferromagnet (the E1/FM2 vacuum) whose gauged U(1) subgroup
(rotations about e_z) is coupled to a U(1) link field, to test whether the gauge
field acquires a mass by eating a Goldstone (Anderson-Higgs) -> the DEV's A_mu.

This module is the DATA GENERATOR.  It contains NO DEV/relativistic number AND NO
complex literal: like the project's own U(1) engine (results/gauge/e5/e5_core.py), the
gauge connection is handled with REAL cos/sin arithmetic on the link angle theta, so the
anti-circularity guard (which forbids complex numbers in generators -- a smuggled e^{ikL}
quantum phase) stays meaningful.  The words "photon", "A_mu", "m_A" live only in the
synthesis; m_A_DEV is COMPARISON ONLY in the gate scripts.  Built on the validated pieces:
  * gauge sector: the non-compact Maxwell link action (matches E6's non-compact choice);
  * matter sector: the O(3) Heisenberg ferromagnet of fm2_core (same beta=1 Metropolis
    convention, J = coupling, large J = ordered).

Construction (exactly gauge invariant for ANY real charge lambda):
  charged field   (phi0,phi1) = (n^0, n^1)    (transverse, rotates under U(1)_z)
  neutral field   n^2 = n_z                    (longitudinal, U(1)_z-invariant)
  S = -J sum_<ij> [ n_z(i) n_z(j) + Re( conj(phi_i) e^{i lambda theta_ij} phi_j ) ]
      + D sum_i n_z(i)^2                        (easy-plane: pins order in-plane so phi
                                                 condenses and U(1)_z is broken)
      + (1/(2 g^2)) sum_P theta_P^2             (non-compact Maxwell, beta = 1/g^2)
  with, for phase ph = lambda*theta on the link i->j and A=phi0_i phi0_j+phi1_i phi1_j,
  B = phi0_i phi1_j - phi1_i phi0_j :
      Re(conj(phi_i) e^{i ph} phi_j) = A cos(ph) - B sin(ph)
      Im(conj(phi_i) e^{i ph} phi_j) = A sin(ph) + B cos(ph)   (the vector operator W)
Gauge transform:  theta_ij -> theta_ij + a_i - a_j ,  phi_i -> R(lambda a_i) phi_i ,
n_z invariant; S invariant to machine precision (gauge_invariance_check).
The prompt's linear coupling -lambda A.(n x n).e_z is exactly the O(lambda) term, since
(n_i x n_j).e_z = Im(conj(phi_i)phi_j) = B.
"""
from __future__ import annotations

import numpy as np


def _normalize(v, eps=1e-12):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + eps)


class AbelianHiggs4D:
    """O(3) matter + non-compact U(1) gauge on a periodic L^4 lattice (axis 0 = time)."""

    def __init__(self, L, J, lam, g, D=0.5, seed=0, step_n=0.4, step_a=0.4,
                 inplane_seed=True):
        self.L = int(L)
        self.J = float(J)
        self.lam = float(lam)
        self.g = float(g)
        self.beta_g = 1.0 / float(g) ** 2          # non-compact Maxwell coefficient
        self.D = float(D)
        self.rng = np.random.default_rng(seed)
        self.step_n = float(step_n)
        self.step_a = float(step_a)
        sh = (self.L,) * 4
        # matter: start ordered in the x-y plane (along +x) so phi condenses and the
        # gauged U(1)_z is spontaneously broken (Higgs branch).
        if inplane_seed:
            n0 = np.zeros(sh + (3,))
            n0[..., 0] = 1.0
            self.n = n0 + 0.05 * self.rng.standard_normal(sh + (3,))
        else:
            self.n = self.rng.standard_normal(sh + (3,))
        self.n = _normalize(self.n)
        # gauge: small random non-compact link angles
        self.theta = 0.1 * self.rng.standard_normal(sh + (4,))
        g_ = np.arange(self.L)
        I, Jx, K, T = np.meshgrid(g_, g_, g_, g_, indexing="ij")
        self.parity = (I + Jx + K + T) % 2

    # ------------------------------------------------------------------ #
    # gauge-covariant bond helpers (REAL arithmetic; no complex literal)
    # ------------------------------------------------------------------ #
    def _bond_AB(self, mu):
        """A,B per site for the link in direction +mu: A=phi_i.phi_{i+mu} (real dot of
        the in-plane parts), B=Im(conj(phi_i)phi_{i+mu}) = phi0_i phi1_j - phi1_i phi0_j."""
        p0, p1 = self.n[..., 0], self.n[..., 1]
        q0 = np.roll(p0, -1, axis=mu)
        q1 = np.roll(p1, -1, axis=mu)
        A = p0 * q0 + p1 * q1
        B = p0 * q1 - p1 * q0
        return A, B

    def plaquette_holonomies_sq_sum(self):
        """sum_P theta_P^2 over all (mu<nu) plaquettes."""
        th = self.theta
        tot = 0.0
        for mu in range(4):
            for nu in range(mu + 1, 4):
                tP = (th[..., mu] + np.roll(th[..., nu], -1, axis=mu)
                      - np.roll(th[..., mu], -1, axis=nu) - th[..., nu])
                tot += float(np.sum(tP ** 2))
        return tot

    def action(self):
        nz = self.n[..., 2]
        Sm = 0.0
        for mu in range(4):
            A, B = self._bond_AB(mu)
            ph = self.lam * self.theta[..., mu]
            reW = A * np.cos(ph) - B * np.sin(ph)
            Sm += -self.J * np.sum(nz * np.roll(nz, -1, axis=mu) + reW)
        Seasy = self.D * np.sum(nz ** 2)
        Sg = 0.5 * self.beta_g * self.plaquette_holonomies_sq_sum()
        return float(Sm + Seasy + Sg)

    # ------------------------------------------------------------------ #
    # gauge-invariance gate (verify BEFORE any physical measurement)
    # ------------------------------------------------------------------ #
    def gauge_invariance_check(self):
        """Apply a random local gauge transform a_x and return the absolute change in
        the total action (should be ~0 to machine precision)."""
        S0 = self.action()
        a = self.rng.uniform(-np.pi, np.pi, (self.L,) * 4)
        th = self.theta.copy()
        n = self.n.copy()
        for mu in range(4):
            th[..., mu] = self.theta[..., mu] + a - np.roll(a, -1, axis=mu)
        ca, sa = np.cos(self.lam * a), np.sin(self.lam * a)        # rotate phi by R(lam a)
        n[..., 0] = self.n[..., 0] * ca - self.n[..., 1] * sa
        n[..., 1] = self.n[..., 0] * sa + self.n[..., 1] * ca
        th_save, n_save = self.theta, self.n
        self.theta, self.n = th, n
        S1 = self.action()
        self.theta, self.n = th_save, n_save
        return abs(S1 - S0), S0

    # ------------------------------------------------------------------ #
    # Metropolis updates (vectorised checkerboard)
    # ------------------------------------------------------------------ #
    def _matter_effective_field(self):
        """H_eff(x) such that the matter energy is E = -sum_x n_x . H_eff(x) (+easy-plane).
        Transverse (0,1) from the covariant hopping; (2) from the n_z bonds.  Real trig."""
        p0, p1 = self.n[..., 0], self.n[..., 1]
        H = np.zeros_like(self.n)
        for mu in range(4):
            ph = self.lam * self.theta[..., mu]                   # phase on link x->x+mu
            c, s = np.cos(ph), np.sin(ph)
            # +mu neighbour j=x+mu: contributes to site x via e^{i ph} phi_j
            q0, q1 = np.roll(p0, -1, axis=mu), np.roll(p1, -1, axis=mu)
            H[..., 0] += q0 * c - q1 * s
            H[..., 1] += q1 * c + q0 * s
            # -mu neighbour j=x-mu with link x-mu -> x: phase ph_back=lam theta_mu(x-mu),
            # site x gets e^{-i ph_back} phi_j
            ph_b = self.lam * np.roll(self.theta[..., mu], 1, axis=mu)
            cb, sb = np.cos(ph_b), np.sin(ph_b)
            r0, r1 = np.roll(p0, 1, axis=mu), np.roll(p1, 1, axis=mu)
            H[..., 0] += r0 * cb + r1 * sb
            H[..., 1] += r1 * cb - r0 * sb
            H[..., 2] += np.roll(self.n[..., 2], -1, axis=mu) + np.roll(self.n[..., 2], 1, axis=mu)
        return self.J * H

    def matter_sweep(self):
        H = self._matter_effective_field()
        acc = 0
        tot = 0
        for p in (0, 1):
            mask = self.parity == p
            old = self.n[mask]
            Hm = H[mask]
            prop = _normalize(old + self.step_n * self.rng.standard_normal(old.shape))
            dE = (-np.einsum("ij,ij->i", prop - old, Hm)
                  + self.D * (prop[:, 2] ** 2 - old[:, 2] ** 2))
            a = self.rng.random(old.shape[0]) < np.exp(-np.clip(dE, 0, 60))
            new = np.where(a[:, None], prop, old)
            self.n[mask] = new
            acc += int(a.sum())
            tot += a.size
        return acc / max(tot, 1)

    def _gauge_G(self, mu):
        """G_mu(x) = sum over the 6 plaquettes containing link theta_mu(x) of
        sign * theta_P (current holonomies).  Used in dE = (1/g^2)(delta G + 3 delta^2)."""
        th = self.theta
        G = np.zeros((self.L,) * 4)
        for nu in range(4):
            if nu == mu:
                continue
            # plaquette (mu,nu) at x  (self link sign +1)
            Pa = (th[..., mu] + np.roll(th[..., nu], -1, axis=mu)
                  - np.roll(th[..., mu], -1, axis=nu) - th[..., nu])
            # plaquette (mu,nu) at x-nu  (self link sign -1)
            Pb = (np.roll(th[..., mu], 1, axis=nu)
                  + np.roll(np.roll(th[..., nu], 1, axis=nu), -1, axis=mu)
                  - th[..., mu] - np.roll(th[..., nu], 1, axis=nu))
            G += Pa - Pb
        return G

    def gauge_sweep(self):
        acc = 0
        tot = 0
        for mu in range(4):
            A, B = self._bond_AB(mu)                    # in-plane bond carriers (real)
            G = self._gauge_G(mu)
            for p in (0, 1):
                mask = self.parity == p
                old = self.theta[..., mu][mask]
                delta = self.step_a * self.rng.standard_normal(old.shape)
                new = old + delta
                # gauge part: (1/g^2)(delta G + 3 delta^2)
                dE_g = self.beta_g * (delta * G[mask] + 3.0 * delta ** 2)
                # matter part: -J [ reW(new) - reW(old) ], reW = A cos(lam th) - B sin(lam th)
                Am, Bm = A[mask], B[mask]
                reW_new = Am * np.cos(self.lam * new) - Bm * np.sin(self.lam * new)
                reW_old = Am * np.cos(self.lam * old) - Bm * np.sin(self.lam * old)
                dE_m = -self.J * (reW_new - reW_old)
                dE = dE_g + dE_m
                a = self.rng.random(old.shape[0]) < np.exp(-np.clip(dE, 0, 60))
                upd = np.where(a, new, old)
                tmp = self.theta[..., mu]
                tmp[mask] = upd
                self.theta[..., mu] = tmp
                acc += int(a.sum())
                tot += a.size
        return acc / max(tot, 1)

    def sweep(self, adapt=True):
        am = self.matter_sweep()
        ag = self.gauge_sweep()
        if adapt:
            if am > 0.55:
                self.step_n *= 1.05
            elif am < 0.35:
                self.step_n *= 0.95
            self.step_n = float(np.clip(self.step_n, 1e-2, 2.0))
            if ag > 0.55:
                self.step_a *= 1.05
            elif ag < 0.35:
                self.step_a *= 0.95
            self.step_a = float(np.clip(self.step_a, 1e-2, 3.0))
        return am, ag

    def equilibrate(self, n_burn):
        for _ in range(n_burn):
            self.sweep()

    # ------------------------------------------------------------------ #
    # observables
    # ------------------------------------------------------------------ #
    def gauge_invariant_bond(self):
        """<Re conj(phi_i) e^{i lam theta} phi_j> averaged over links (the Higgs
        condensate proxy; gauge invariant)."""
        tot = 0.0
        for mu in range(4):
            A, B = self._bond_AB(mu)
            ph = self.lam * self.theta[..., mu]
            tot += float(np.mean(A * np.cos(ph) - B * np.sin(ph)))
        return tot / 4.0

    def m_inplane(self):
        """<|phi|> = per-site transverse magnitude (gauge invariant)."""
        return float(np.mean(np.hypot(self.n[..., 0], self.n[..., 1])))

    def vector_slices(self):
        """Zero-spatial-momentum projection of the gauge-invariant vector operator
        W_k(x) = Im[ conj(phi_x) e^{i lam theta_k(x)} phi_{x+k} ] = A sin(ph)+B cos(ph)
        for spatial k=1,2,3.  Returns (3, L): M_k(t) = sum over spatial sites of W_k."""
        out = np.zeros((3, self.L))
        for idx, k in enumerate((1, 2, 3)):
            A, B = self._bond_AB(k)
            ph = self.lam * self.theta[..., k]
            Wk = A * np.sin(ph) + B * np.cos(ph)                  # (L,L,L,L)
            out[idx] = Wk.sum(axis=(1, 2, 3))                     # sum spatial -> (L,)
        return out


def temporal_correlator(slices_list):
    """Connected zero-momentum vector correlator C(t) from a list of vector_slices()
    samples (each (3,L)).  C(t) = < sum_k M_k(t0+t) M_k(t0) >_{t0,k,config} (connected)."""
    arr = np.array(slices_list)            # (n_meas, 3, L)
    L = arr.shape[2]
    arr = arr - arr.mean(axis=0, keepdims=True)        # connected (subtract <M_k(t)>)
    C = np.zeros(L)
    for t in range(L):
        prod = arr * np.roll(arr, -t, axis=2)          # M(t0+t) M(t0)
        C[t] = prod.mean()                             # over config, k, t0
    return C


def fit_mass(C, t_min=1, t_max=None):
    """Extract the mass from the exponential decay of the (folded) correlator
    C(t) ~ cosh(m (t - L/2)) -> for small t, ~ e^{-m t}.  Fit log C over a clean
    window.  Returns (m, used_window, C_folded)."""
    L = len(C)
    half = L // 2
    Cf = np.array([0.5 * (C[t] + C[(L - t) % L]) for t in range(half + 1)])
    if t_max is None:
        t_max = half
    ts = np.arange(t_min, t_max + 1)
    y = Cf[t_min:t_max + 1]
    good = y > 0
    if good.sum() < 2:
        return float("nan"), (t_min, t_max), Cf
    m = -np.polyfit(ts[good], np.log(y[good]), 1)[0]
    return float(m), (t_min, t_max), Cf


if __name__ == "__main__":
    # self-test: gauge invariance + that ordered+coupled raises the gauge-invariant bond
    print("a5_higgs_core self-test (L=6)")
    for lam in (0.0, 1.0):
        m = AbelianHiggs4D(6, J=1.0, lam=lam, g=1.0, D=0.5, seed=0)
        dS, S0 = m.gauge_invariance_check()
        print(f"  lam={lam}: gauge-inv |dS|={dS:.2e}  (S0={S0:.1f})  "
              f"{'OK' if dS < 1e-7 else 'FAIL'}")
    m = AbelianHiggs4D(6, J=1.5, lam=1.0, g=1.0, D=0.5, seed=0)
    m.equilibrate(60)
    print(f"  ordered+coupled: bond={m.gauge_invariant_bond():.3f}  "
          f"<|phi|>={m.m_inplane():.3f}")
