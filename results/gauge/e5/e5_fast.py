"""e5_fast.py -- VECTORISED (checkerboard) U(1) Wilson gauge Metropolis.

The pure-Python per-link loop of e5_core.U1Gauge is too slow to reach the volumes
that resolve the finite-size scaling of the 4D U(1) deconfinement transition (the
E5-V G3 gate came out INCONCLUSIVE for that reason). This module updates all links
of one colour class at once, where the colouring guarantees no two links in a class
share a plaquette (so their staples are mutually independent and the simultaneous
Metropolis update is exact). It is validated against the slow engine before use.

Same physics, same Wilson action S=beta*sum_P[1-cos theta_P], same anti-circularity
(real cos only; no relativistic/quantum literal; 'photon' only in synthesis).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from e5_core import regular_lattice, build_link_plaqs, U1Gauge  # noqa: E402


def link_conflict_colouring(L, plaq_links):
    """Colour links so that no two links sharing a plaquette get the same colour
    (greedy, highest-degree-first). Returns colors (L,) int."""
    # adjacency: links sharing a plaquette
    adj = [set() for _ in range(L)]
    for p in range(plaq_links.shape[0]):
        ls = plaq_links[p]
        for a in range(4):
            for b in range(a + 1, 4):
                adj[ls[a]].add(int(ls[b]))
                adj[ls[b]].add(int(ls[a]))
    deg = np.array([len(a) for a in adj])
    order = np.argsort(-deg, kind="stable")
    colors = np.full(L, -1, dtype=np.int64)
    for v in order:
        used = {colors[u] for u in adj[v] if colors[u] >= 0}
        c = 0
        while c in used:
            c += 1
        colors[v] = c
    return colors


class FastU1Gauge:
    def __init__(self, L, plaq_links, plaq_signs, beta, seed=0, step=1.0):
        self.L = L
        self.plaq_links = plaq_links
        self.plaq_signs = plaq_signs
        self.beta = float(beta)
        self.rng = np.random.default_rng(seed)
        self.step = float(step)
        self.theta = self.rng.uniform(-np.pi, np.pi, L)
        ss, ol, os = build_link_plaqs(L, plaq_links, plaq_signs)
        Kmax = max((a.shape[0] for a in ol), default=0)
        self.Kmax = Kmax
        # padded global arrays
        self.SS = np.zeros((L, Kmax))
        self.OL = np.zeros((L, Kmax, 3), dtype=np.int64)
        self.OS = np.zeros((L, Kmax, 3))
        self.MASK = np.zeros((L, Kmax))
        for l in range(L):
            k = ol[l].shape[0]
            if k:
                self.SS[l, :k] = ss[l]
                self.OL[l, :k] = ol[l]
                self.OS[l, :k] = os[l]
                self.MASK[l, :k] = 1.0
        colors = link_conflict_colouring(L, plaq_links)
        self.color_groups = [np.nonzero(colors == c)[0] for c in range(colors.max() + 1)]

    def plaquette_holonomies(self):
        return (self.plaq_signs * self.theta[self.plaq_links]).sum(axis=1)

    def mean_cos_plaq(self):
        return float(np.cos(self.plaquette_holonomies()).mean())

    def sweep(self):
        acc = 0
        for idx in self.color_groups:
            if idx.size == 0:
                continue
            SS = self.SS[idx]                       # (m,K)
            OL = self.OL[idx]                       # (m,K,3)
            OS = self.OS[idx]
            MK = self.MASK[idx]
            staple = (OS * self.theta[OL]).sum(axis=2)   # (m,K)
            old = self.theta[idx]                        # (m,)
            new = old + self.step * self.rng.standard_normal(old.size)
            dE = -self.beta * np.sum(
                MK * (np.cos(SS * new[:, None] + staple) - np.cos(SS * old[:, None] + staple)),
                axis=1)
            p = np.exp(-np.clip(dE, 0.0, 50.0))
            a = self.rng.random(old.size) < p
            self.theta[idx] = np.where(a, new, old)
            acc += int(a.sum())
        return acc / max(self.L, 1)

    def equilibrate(self, n_burn, adapt=True, target=0.4):
        for s in range(n_burn):
            a = self.sweep()
            if adapt and (s + 1) % 20 == 0:
                if a > target + 0.1:
                    self.step *= 1.15
                elif a < target - 0.1:
                    self.step *= 0.87
                self.step = float(np.clip(self.step, 1e-2, 6.28))

    def measure_plaq(self, n_meas, meas_every=2):
        vals = []
        s = 0
        while len(vals) < n_meas:
            self.sweep(); s += 1
            if s % meas_every == 0:
                vals.append(self.mean_cos_plaq())
        return np.array(vals)


def _validate_against_slow():
    """The optimisation gate: the fast engine must reproduce the slow engine's
    mean plaquette on a small lattice at several couplings."""
    L, pl, ps = regular_lattice((3, 3, 3, 3))
    print("validation: fast vs slow U(1), 3^4 lattice")
    ok = True
    for beta in [0.5, 1.0, 1.4]:
        gs = U1Gauge(L, pl, ps, beta=beta, seed=1)
        gs.equilibrate(250); vs = gs.measure_plaq(120)
        gf = FastU1Gauge(L, pl, ps, beta=beta, seed=1)
        gf.equilibrate(250); vf = gf.measure_plaq(120)
        ms, mf = vs.mean(), vf.mean()
        sem = (vs.std() / np.sqrt(len(vs)) + vf.std() / np.sqrt(len(vf)))
        agree = abs(ms - mf) < 4 * sem + 0.01
        ok = ok and agree
        print(f"  beta={beta}: slow<cos>={ms:+.4f} fast<cos>={mf:+.4f} "
              f"|diff|={abs(ms-mf):.4f} -> {'OK' if agree else 'MISMATCH'}")
    print("VALIDATION", "PASSED" if ok else "FAILED")
    return ok


if __name__ == "__main__":
    t0 = time.time()
    _validate_against_slow()
    print(f"({time.time()-t0:.0f}s)")
