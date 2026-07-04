"""a5_causal_core.py -- the A5 abelian-Higgs model on a CAUSAL SET (Phase B).

Same construction as a5_higgs_core (O(3) orientation ferromagnet + non-compact U(1) with
the exactly-gauge-invariant covariant hopping, real charge lambda, REAL cos/sin
arithmetic -- no complex literal, matching e5_core's discipline so the anti-circularity
guard stays meaningful), but on the irregular Hasse graph of a 3+1D Poisson sprinkling
instead of a regular cubic lattice.  Reuses the validated causal-set gauge machinery of
e5_core (diamond plaquettes, per-link plaquette structure) and the sprinkling of
causal_core.

Edges e=(lo,hi) are the Hasse covering relations (lo<hi by node index).  The connection
theta[e] lives along lo->hi.  Charged field (phi0,phi1)=(n0,n1); neutral n_z=n2.
With phase ph=lam*theta on edge lo->hi, A=phi0_lo phi0_hi+phi1_lo phi1_hi,
B=phi0_lo phi1_hi-phi1_lo phi0_hi:
  S = -J sum_e [ n_z(lo) n_z(hi) + (A cos ph - B sin ph) ]
      + D sum_i n_z(i)^2 + (1/(2 g^2)) sum_P theta_P^2 .
Gauge transform theta_e -> theta_e + a_lo - a_hi, phi_i -> R(lam a_i) phi_i ; S invariant
to machine precision (gauge_invariance_check).

The point of Phase B is whether the SAME Anderson-Higgs mechanism that G1 proved on the
cubic lattice survives the NON-LOCALITY of the causal set (the E5/E7 obstruction: degree
grows with N, no Lorentz-invariant local spatial slice).  No DEV/relativistic number;
m_A_DEV is COMPARISON ONLY in the synthesis.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))
sys.path.insert(0, str(ROOT / "results" / "gauge" / "e5"))
from causal_core import sprinkle_box  # noqa: E402
from orientation_core import causal_link_graph, longest_chain_from  # noqa: E402
import e5_core  # noqa: E402


def _normalize(v, eps=1e-12):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + eps)


def build_causal_substrate(rho, side, seed):
    """Sprinkle a 3+1D box, build the Hasse graph and the diamond U(1) plaquettes.
    Returns (g, pts, edges, plaq_links, plaq_signs, link_struct)."""
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0, side)] * 4, rng)
    g = causal_link_graph(pts)
    L, plaq_links, plaq_signs = e5_core.causal_diamond_plaquettes(g, max_per_pair=2,
                                                                  max_plaqs=40000, seed=seed)
    link_struct = e5_core.build_link_plaqs(L, plaq_links, plaq_signs)
    return g, pts, g.edges, plaq_links, plaq_signs, link_struct


class CausalHiggs:
    """O(3) matter + non-compact U(1) gauge on a causal-set Hasse graph (real arithmetic)."""

    def __init__(self, g, edges, plaq_links, plaq_signs, link_struct,
                 J, lam, g_gauge, D=0.5, seed=0, step_n=0.4, step_a=0.4):
        self.g = g
        self.edges = np.asarray(edges, np.int64)            # (E,2) lo<hi
        self.E = self.edges.shape[0]
        self.plaq_links = plaq_links
        self.plaq_signs = plaq_signs
        self.self_sign, self.other_links, self.other_signs = link_struct
        self.J, self.lam, self.g_gauge = float(J), float(lam), float(g_gauge)
        self.beta_g = 1.0 / float(g_gauge) ** 2
        self.D = float(D)
        self.rng = np.random.default_rng(seed)
        self.step_n, self.step_a = float(step_n), float(step_a)
        n = g.n
        n0 = np.zeros((n, 3)); n0[:, 0] = 1.0
        self.n = _normalize(n0 + 0.05 * self.rng.standard_normal((n, 3)))
        self.theta = 0.1 * self.rng.standard_normal(self.E)
        self.colors = g.colors
        self.groups = g.groups

    # ------------------------------------------------------------------ #
    def _bond_AB(self):
        """Per-edge A,B carriers (real): A=phi_lo.phi_hi, B=Im(conj(phi_lo)phi_hi)."""
        lo, hi = self.edges[:, 0], self.edges[:, 1]
        p0, p1 = self.n[:, 0], self.n[:, 1]
        A = p0[lo] * p0[hi] + p1[lo] * p1[hi]
        B = p0[lo] * p1[hi] - p1[lo] * p0[hi]
        return A, B

    def plaq_holonomies(self):
        return (self.plaq_signs * self.theta[self.plaq_links]).sum(axis=1)

    def action(self):
        lo, hi = self.edges[:, 0], self.edges[:, 1]
        A, B = self._bond_AB()
        ph = self.lam * self.theta
        reW = A * np.cos(ph) - B * np.sin(ph)
        Sm = -self.J * np.sum(self.n[lo, 2] * self.n[hi, 2] + reW)
        Seasy = self.D * np.sum(self.n[:, 2] ** 2)
        Sg = 0.5 * self.beta_g * np.sum(self.plaq_holonomies() ** 2)
        return float(Sm + Seasy + Sg)

    def gauge_invariance_check(self):
        S0 = self.action()
        a = self.rng.uniform(-np.pi, np.pi, self.g.n)
        lo, hi = self.edges[:, 0], self.edges[:, 1]
        th_save, n_save = self.theta.copy(), self.n.copy()
        self.theta = self.theta + a[lo] - a[hi]
        ca, sa = np.cos(self.lam * a), np.sin(self.lam * a)
        new = self.n.copy()
        new[:, 0] = self.n[:, 0] * ca - self.n[:, 1] * sa
        new[:, 1] = self.n[:, 0] * sa + self.n[:, 1] * ca
        self.n = new
        S1 = self.action()
        self.theta, self.n = th_save, n_save
        return abs(S1 - S0), S0

    # ------------------------------------------------------------------ #
    def _matter_field(self):
        """Effective field H (n,3): E = -J n.H + D n_z^2.  Real trig."""
        lo, hi = self.edges[:, 0], self.edges[:, 1]
        p0, p1 = self.n[:, 0], self.n[:, 1]
        ph = self.lam * self.theta
        c, s = np.cos(ph), np.sin(ph)
        H = np.zeros((self.g.n, 3))
        # node lo gets e^{i ph} phi_hi : (q0 c - q1 s, q1 c + q0 s)
        q0, q1 = p0[hi], p1[hi]
        np.add.at(H[:, 0], lo, q0 * c - q1 * s)
        np.add.at(H[:, 1], lo, q1 * c + q0 * s)
        # node hi gets e^{-i ph} phi_lo : (r0 c + r1 s, r1 c - r0 s)
        r0, r1 = p0[lo], p1[lo]
        np.add.at(H[:, 0], hi, r0 * c + r1 * s)
        np.add.at(H[:, 1], hi, r1 * c - r0 * s)
        # neutral n_z bonds
        np.add.at(H[:, 2], lo, self.n[hi, 2])
        np.add.at(H[:, 2], hi, self.n[lo, 2])
        return self.J * H

    def matter_sweep(self):
        acc = tot = 0
        for nodes in self.groups:
            if nodes.size == 0:
                continue
            H = self._matter_field()             # recompute (colour just changed)
            old = self.n[nodes]
            Hm = H[nodes]
            prop = _normalize(old + self.step_n * self.rng.standard_normal(old.shape))
            dE = (-np.einsum("ij,ij->i", prop - old, Hm)
                  + self.D * (prop[:, 2] ** 2 - old[:, 2] ** 2))
            a = self.rng.random(nodes.size) < np.exp(-np.clip(dE, 0, 60))
            self.n[nodes] = np.where(a[:, None], prop, old)
            acc += int(a.sum()); tot += nodes.size
        return acc / max(tot, 1)

    def gauge_sweep(self):
        """Per-edge Metropolis on theta (non-compact Maxwell + matter bond).  Real trig."""
        lo, hi = self.edges[:, 0], self.edges[:, 1]
        A, B = self._bond_AB()                       # per-edge in-plane carriers
        acc = 0
        order = self.rng.permutation(self.E)
        for l in order:
            ol = self.other_links[l]
            if ol.shape[0] == 0:
                nP = 0
                G = 0.0
            else:
                ss = self.self_sign[l]               # (nP,)
                staple = (self.other_signs[l] * self.theta[ol]).sum(axis=1)  # (nP,)
                nP = ss.shape[0]
                G = float(np.sum(ss * staple))
            old = self.theta[l]
            delta = self.step_a * self.rng.standard_normal()
            new = old + delta
            dE_g = 0.5 * self.beta_g * (nP * (new ** 2 - old ** 2) + 2.0 * delta * G)
            reW_new = A[l] * np.cos(self.lam * new) - B[l] * np.sin(self.lam * new)
            reW_old = A[l] * np.cos(self.lam * old) - B[l] * np.sin(self.lam * old)
            dE_m = -self.J * (reW_new - reW_old)
            dE = dE_g + dE_m
            if dE <= 0 or self.rng.random() < np.exp(-min(dE, 60)):
                self.theta[l] = new
                acc += 1
        return acc / max(self.E, 1)

    def sweep(self, adapt=True):
        am = self.matter_sweep()
        ag = self.gauge_sweep()
        if adapt:
            self.step_n = float(np.clip(self.step_n * (1.05 if am > 0.55 else 0.95 if am < 0.35 else 1.0), 1e-2, 2.0))
            self.step_a = float(np.clip(self.step_a * (1.05 if ag > 0.55 else 0.95 if ag < 0.35 else 1.0), 1e-2, 3.0))
        return am, ag

    def equilibrate(self, n_burn):
        for _ in range(n_burn):
            self.sweep()

    # ------------------------------------------------------------------ #
    def gauge_invariant_bond(self):
        A, B = self._bond_AB()
        ph = self.lam * self.theta
        return float(np.mean(A * np.cos(ph) - B * np.sin(ph)))

    def link_vector_W(self):
        """Gauge-invariant vector operator per edge: W_e = A sin(ph)+B cos(ph)
        = Im(conj(phi_lo)e^{i lam th}phi_hi)."""
        A, B = self._bond_AB()
        ph = self.lam * self.theta
        return A * np.sin(ph) + B * np.cos(ph)
