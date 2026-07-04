"""E4_R_robustness.py -- robustness sweep of the Goldstone-sector results.

Pre-registered robustness checks requested by external review of PAPER_GOLDSTONE_PRD.
Reuses orientation_core (O(3) Metropolis on the 3+1D causal link graph) WITHOUT
modifying it; the alternative coupling is a thin subclass defined HERE.

Three checks (all cheap, all reusing the existing engine):

  (i)   DENSITY SWEEP. Repeat the finite-size-scaling order test (m, U4) and the
        polarisation-locking test at sprinkling density rho x2 and rho x0.5.
        Pre-registered survival criterion:
          - ordering survives  : m well above the random floor N^{-1/2}, U4 ~ 2/3;
          - photon stays dead   : locking permutation p > 0.05 (no k-locking).

  (ii)  ALTERNATIVE COUPLING. The engine couples neighbours with a UNIFORM weight
        (-J n_i.n_j). The paper's action Eq.(1) carries a per-link proper-time
        weight Delta tau_ij. We run the locking test with that proper-time-weighted
        coupling -- a genuinely different coupling form -- and check the Goldstone
        modes stay internal scalars (locking p > 0.05). This verifies the photon
        retraction is not an artefact of the uniform coupling.

  (iii) N-CONVERGENCE TABLE. Tabulate m(N), U4(N), and the ratio to the random floor
        across N, making the convergence the reviewer asks for explicit.

Anti-circularity: only the graph + cos/dot energy + proper-time link weights drive
the dynamics; no relativistic or critical quantity is inserted. 'photon' appears
only in synthesis/comparison text, never in a generator.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORI = HERE.parent
sys.path.insert(0, str(ORI))
from orientation_core import (  # noqa: E402
    O3Model, causal_link_graph, transverse_components,
)
from E4_1_locking import (  # noqa: E402
    fibonacci_directions, polarisation_tensors, anisotropy_and_axis,
)

ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402


# ====================================================================== #
# Alternative coupling: proper-time-weighted O(3) (the paper's Eq.(1))
# ====================================================================== #
def link_proper_times(pts, g):
    """Per-CSR-entry proper time Delta tau_ij = sqrt(dt^2 - |dx|^2) for every stored
    (i, neighbour) entry of the undirected link graph, aligned with g.indices."""
    pts = np.asarray(pts, float)
    W = np.empty(g.indices.shape[0], dtype=float)
    for i in range(g.n):
        lo, hi = g.indptr[i], g.indptr[i + 1]
        nb = g.indices[lo:hi]
        if nb.size == 0:
            continue
        d = pts[nb] - pts[i]
        s2 = d[:, 0] ** 2 - np.sum(d[:, 1:] ** 2, axis=1)
        W[lo:hi] = np.sqrt(np.clip(s2, 0.0, None))
    return W


class WeightedO3Model(O3Model):
    """O(3) model with per-link proper-time weights (paper Eq.(1)):
        S = J sum_<ij> Delta tau_ij (1 - n_i . n_j).
    Differs from the base engine, which uses a uniform link weight."""

    def __init__(self, graph, pts, J, seed=0, step=None):
        self._Wcsr = link_proper_times(pts, graph)
        # per-colour neighbour weights aligned with graph._nbr[c]
        self._wnbr = []
        for nodes in graph.groups:
            if nodes.size:
                w = np.concatenate(
                    [self._Wcsr[graph.indptr[v]:graph.indptr[v + 1]] for v in nodes])
            else:
                w = np.zeros(0)
            self._wnbr.append(w)
        super().__init__(graph, J=J, seed=seed, step=step)

    def _color_field(self, c):
        nbr, seg, m = self.g._nbr[c], self.g._seg[c], self.g.groups[c].size
        w = self._wnbr[c]
        H = np.empty((m, 3))
        for k in range(3):
            H[:, k] = np.bincount(seg, weights=w * self.n[nbr, k], minlength=m)
        return H


# ====================================================================== #
# (i)+(iii)  FSS order test (m, U4) at a given density
# ====================================================================== #
def fss_at_density(rho, Ls, J=2.0, n_seeds=8, n_burn=300, n_meas=50,
                   meas_every=2, seed0=0):
    rows = []
    for L in Ls:
        per_seed_m = []
        m2_acc = m4_acc = n_samp = 0.0
        Ns, degs = [], []
        for s in range(n_seeds):
            rng = np.random.default_rng(20000 + seed0 + s)
            pts = sprinkle_box(rho, [(0.0, L)] * 4, rng)
            g = causal_link_graph(pts)
            Ns.append(g.n)
            degs.append(float(g.degree.mean()))
            model = O3Model(g, J=J, seed=21000 + seed0 + s)
            model.equilibrate(n_burn, adapt=True)
            ms, taken, sw = [], 0, 0
            while taken < n_meas:
                model.sweep(); sw += 1
                if sw % meas_every == 0:
                    ms.append(model.order_parameter()); taken += 1
            ms = np.asarray(ms)
            per_seed_m.append(ms.mean())
            m2_acc += np.sum(ms ** 2); m4_acc += np.sum(ms ** 4); n_samp += ms.size
        per_seed_m = np.asarray(per_seed_m)
        m2 = m2_acc / n_samp; m4 = m4_acc / n_samp
        U4 = 1.0 - m4 / (3.0 * m2 ** 2) if m2 > 0 else float("nan")
        Nmean = float(np.mean(Ns))
        floor = 1.0 / np.sqrt(Nmean)
        rows.append(dict(L=L, N=Nmean, deg=float(np.mean(degs)),
                         m=float(per_seed_m.mean()),
                         m_sem=float(per_seed_m.std(ddof=1) / np.sqrt(n_seeds)),
                         U4=float(U4), floor=floor, ratio=float(per_seed_m.mean() / floor)))
    Ns = np.array([r["N"] for r in rows]); ms = np.array([r["m"] for r in rows])
    trend = float(np.polyfit(np.log(Ns), np.log(ms), 1)[0])
    ratios = np.array([r["ratio"] for r in rows])
    U4s = np.array([r["U4"] for r in rows])
    survives = bool(np.all(ratios > 3.0) and trend > -0.15 and np.all(U4s > 0.55))
    return dict(rho=rho, rows=rows, m_trend=trend,
                ratio_min=float(ratios.min()), ratio_max=float(ratios.max()),
                U4_min=float(U4s.min()), U4_max=float(U4s.max()),
                ordering_survives=survives)


# ====================================================================== #
# (i)+(ii)  Locking test, parametrised by density and model class
# ====================================================================== #
def locking_test(rho, L, model_factory, n_seeds=12, J=2.0, n_dirs=32, n_kmag=5,
                 n_burn=300, n_samples=40, meas_every=2, seed0=0, n_perm=2000):
    dirs = fibonacci_directions(n_dirs)
    kmin = 2 * np.pi / L
    kmax = 0.5 * np.pi * rho ** (1 / 4)
    kmags = np.linspace(kmin, kmax, n_kmag)
    kvecs = (dirs[:, None, :] * kmags[None, :, None]).reshape(-1, 3)

    P_real = np.zeros((kvecs.shape[0], 2, 2))
    P_shuf = np.zeros((kvecs.shape[0], 2, 2))
    n_acc = 0
    for s in range(n_seeds):
        rng = np.random.default_rng(30000 + seed0 + s)
        pts = sprinkle_box(rho, [(0.0, L)] * 4, rng)
        xs = pts[:, 1:4]
        g = causal_link_graph(pts)
        model = model_factory(g, pts, J, 31000 + seed0 + s)
        model.equilibrate(n_burn, adapt=True)
        shuf_rng = np.random.default_rng(32000 + seed0 + s)
        taken, sw = 0, 0
        while taken < n_samples:
            model.sweep(); sw += 1
            if sw % meas_every != 0:
                continue
            comps = transverse_components(model)
            P_real += polarisation_tensors(xs, comps, kvecs)
            perm = shuf_rng.permutation(xs.shape[0])
            P_shuf += polarisation_tensors(xs[perm], comps, kvecs)
            taken += 1; n_acc += 1
    P_real /= n_acc; P_shuf /= n_acc
    r_real, ang_real = anisotropy_and_axis(P_real)
    r_shuf, _ = anisotropy_and_axis(P_shuf)
    dr = r_real.mean() - r_shuf.mean()
    sig = r_shuf.std(ddof=1) / np.sqrt(len(r_shuf))
    dr_sigma = dr / sig if sig > 0 else float("nan")

    khat = kvecs / np.linalg.norm(kvecs, axis=1, keepdims=True)
    az = np.arctan2(khat[:, 1], khat[:, 0])

    def circ_corr(a, b):
        a = a - np.arctan2(np.sin(a).mean(), np.cos(a).mean())
        b = b - np.arctan2(np.sin(b).mean(), np.cos(b).mean())
        num = np.sum(np.sin(a) * np.sin(b))
        den = np.sqrt(np.sum(np.sin(a) ** 2) * np.sum(np.sin(b) ** 2))
        return float(num / den) if den > 0 else 0.0

    lock_corr = circ_corr(ang_real, az)
    rng_perm = np.random.default_rng(12345)
    null = np.array([abs(circ_corr(ang_real, az[rng_perm.permutation(len(az))]))
                     for _ in range(n_perm)])
    p_value = float(np.mean(null >= abs(lock_corr)))
    lock_sigma = float((abs(lock_corr) - null.mean()) / (null.std() + 1e-12))
    photon_dead = bool(p_value > 0.05)
    return dict(rho=rho, L=L, n_samples_total=n_acc,
                anisotropy_excess_sigma=float(dr_sigma),
                eigvec_khat_circ_corr=float(lock_corr),
                lock_permutation_pvalue=p_value, lock_sigma_vs_null=lock_sigma,
                photon_stays_dead=photon_dead)


def _plain_factory(g, pts, J, seed):
    return O3Model(g, J=J, seed=seed)


def _weighted_factory(g, pts, J, seed):
    return WeightedO3Model(g, pts, J=J, seed=seed)


# ====================================================================== #
def main():
    t0 = time.time()
    rho0 = 0.5
    out = {"baseline_rho": rho0, "checks": {}}

    # ---------------- (i)+(iii) density sweep of the ordering ----------------
    print("=== (i)/(iii) FSS ordering vs density ===", flush=True)
    Ls = [4.4, 5.4, 6.4]
    fss = {}
    for tag, rho in [("rho_x0.5", 0.5 * rho0), ("rho_x1_baseline", rho0),
                     ("rho_x2", 2.0 * rho0)]:
        r = fss_at_density(rho, Ls)
        fss[tag] = r
        mstr = " ".join(f"{x['m']:.3f}" for x in r["rows"])
        ustr = " ".join(f"{x['U4']:.3f}" for x in r["rows"])
        print(f"  {tag:18s} rho={rho:.3f}: m=[{mstr}] U4=[{ustr}] "
              f"trend={r['m_trend']:+.3f} ratio={r['ratio_min']:.0f}-{r['ratio_max']:.0f}x "
              f"-> survives={r['ordering_survives']}", flush=True)
    out["checks"]["fss_density_sweep"] = fss

    # ---------------- (i) locking vs density ----------------
    print("\n=== (i) photon-locking test vs density ===", flush=True)
    lock_density = {}
    for tag, rho, L in [("rho_x0.5", 0.5 * rho0, 6.4),
                        ("rho_x1_baseline", rho0, 6.4),
                        ("rho_x2", 2.0 * rho0, 6.4)]:
        r = locking_test(rho, L, _plain_factory)
        lock_density[tag] = r
        print(f"  {tag:18s} rho={rho:.3f}: corr={r['eigvec_khat_circ_corr']:+.3f} "
              f"p={r['lock_permutation_pvalue']:.3f} -> photon_dead={r['photon_stays_dead']}",
              flush=True)
    out["checks"]["locking_density_sweep"] = lock_density

    # ---------------- (ii) alternative coupling ----------------
    print("\n=== (ii) alternative coupling: proper-time-weighted O(3) ===", flush=True)
    r_alt = locking_test(rho0, 6.4, _weighted_factory)
    print(f"  proper-time weighted: corr={r_alt['eigvec_khat_circ_corr']:+.3f} "
          f"p={r_alt['lock_permutation_pvalue']:.3f} -> photon_dead={r_alt['photon_stays_dead']}",
          flush=True)
    out["checks"]["locking_alt_coupling_weighted"] = r_alt

    # ---------------- overall verdict ----------------
    ordering_ok = all(v["ordering_survives"] for v in fss.values())
    photon_ok = (all(v["photon_stays_dead"] for v in lock_density.values())
                 and r_alt["photon_stays_dead"])
    out["summary"] = {
        "ordering_survives_all_densities": ordering_ok,
        "photon_dead_all_densities": all(v["photon_stays_dead"] for v in lock_density.values()),
        "photon_dead_alt_coupling": r_alt["photon_stays_dead"],
        "all_robust": bool(ordering_ok and photon_ok),
    }
    out["runtime_s"] = time.time() - t0
    (HERE / "E4_R_robustness.json").write_text(json.dumps(out, indent=2))
    print("\n=== SUMMARY ===")
    print(json.dumps(out["summary"], indent=2))
    print(f"runtime {out['runtime_s']:.1f}s -> E4_R_robustness.json")


if __name__ == "__main__":
    main()
