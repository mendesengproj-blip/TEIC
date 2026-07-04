"""A3 / C2 -- Goldstone FSS (larger N) + transverse structure-factor exponent.

Campaign GOLDSTONE_A3 (Fase 2, Frente A).  Reuses orientation_core WITHOUT
modification (O(3) Metropolis on the 3+1D causal link graph).  Two prongs
(PRE_REGISTRO):
  (a) FSS of the long-range order m(N), U4(N) to larger N -- does the LRO of E1/E4
      survive, or is it a finite-size artefact?
  (b) transverse structure factor S(k) ~ A/k^alpha on the BARE causal links:
      alpha~0 (flat) = mean-field / non-local;  alpha~2 (S~1/k^2) = gradient
      rigidity (omega~k, photon-like).  E1-3 found alpha~0.28 (flat) at N~1462;
      A3 tests whether that flatness is robust in N.

Estimator gate: S(k) on a 3D ordered cubic lattice must give alpha~2 (validated as
in E1-3) before trusting the causal-set measurement.

Anti-circularity: only the graph + cos/dot energy; no relativistic/critical literal;
orientation_core is under the A1 guard.  alpha emerges from the fit.

Run:  python docs/campaigns/GOLDSTONE_A3/A3_fss_sk.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
ORI = ROOT / "results" / "vacuum_structure" / "orientation"
sys.path.insert(0, str(ORI))
sys.path.insert(0, str(ROOT / "src"))
from orientation_core import (O3Model, causal_link_graph, lattice_periodic,   # noqa: E402
                              transverse_components, structure_factor)
from causal_core import sprinkle_box                                          # noqa: E402

J = 2.0
RHO = 0.5
N_BURN, N_MEAS, MEAS_EVERY = 300, 40, 2


def kgrid(L, n=24, span_decades=1.6):
    """k magnitudes over >=1.5 decade, from the box fundamental upward."""
    k_min = 2.0 * np.pi / L
    return np.geomspace(k_min, k_min * 10 ** span_decades, n)


def fit_alpha(kmags, S):
    """S ~ A/k^alpha -> slope of log S vs log k is -alpha. Returns alpha over the
    finite, positive window."""
    m = np.isfinite(S) & (S > 0) & np.isfinite(kmags) & (kmags > 0)
    if m.sum() < 3:
        return float("nan")
    slope = np.polyfit(np.log(kmags[m]), np.log(S[m]), 1)[0]
    return float(-slope)


def measure_sk_one(model, xs, kmags, n_burn, n_meas, meas_every):
    """Equilibrate, collect transverse-component samples, return S(k) for one seed
    plus the order-parameter samples."""
    model.equilibrate(n_burn, adapt=True)
    comps, ms = [], []
    taken, s = 0, 0
    while taken < n_meas:
        model.sweep(); s += 1
        if s % meas_every == 0:
            comps.append(transverse_components(model))
            ms.append(model.order_parameter())
            taken += 1
    S = structure_factor(comps, xs, kmags, n_dirs=xs.shape[1])
    return S, np.asarray(ms)


def estimator_gate(L=12, seed=0):
    """S(k) on a 3D ordered cubic lattice -> expect alpha~2 (gradient rigidity)."""
    g = lattice_periodic((L, L, L))
    shape = (L, L, L)
    xs = np.stack(np.unravel_index(np.arange(g.n), shape), axis=1).astype(float)
    model = O3Model(g, J=J, seed=seed)
    km = np.geomspace(2 * np.pi / L, np.pi, 20)
    S, _ = measure_sk_one(model, xs, km, n_burn=200, n_meas=30, meas_every=2)
    alpha = fit_alpha(km, S)
    return {"L": L, "n": g.n, "alpha": alpha, "k": km.tolist(), "S": S.tolist()}


def run_size(L, n_seeds, want_sk, seed0=0):
    per_seed_m, m2_acc, m4_acc, n_samp = [], 0.0, 0.0, 0
    Ns, degs, S_seeds = [], [], []
    kmags = kgrid(L)
    for s in range(n_seeds):
        rng = np.random.default_rng(1000 + seed0 + s)
        pts = sprinkle_box(RHO, [(0.0, L)] * 4, rng)
        g = causal_link_graph(pts)
        Ns.append(g.n); degs.append(float(g.degree.mean()))
        model = O3Model(g, J=J, seed=2000 + seed0 + s)
        if want_sk:
            xs = np.asarray(pts)[:, 1:4]            # spatial coords (drop time)
            S, ms = measure_sk_one(model, xs, kmags, N_BURN, N_MEAS, MEAS_EVERY)
            S_seeds.append(S)
        else:
            model.equilibrate(N_BURN, adapt=True)
            ms, taken, sw = [], 0, 0
            while taken < N_MEAS:
                model.sweep(); sw += 1
                if sw % MEAS_EVERY == 0:
                    ms.append(model.order_parameter()); taken += 1
            ms = np.asarray(ms)
        per_seed_m.append(ms.mean())
        m2_acc += np.sum(ms ** 2); m4_acc += np.sum(ms ** 4); n_samp += ms.size
    per_seed_m = np.asarray(per_seed_m)
    m2, m4 = m2_acc / n_samp, m4_acc / n_samp
    U4 = 1.0 - m4 / (3.0 * m2 ** 2) if m2 > 0 else float("nan")
    N_mean = float(np.mean(Ns))
    row = {"L": L, "N_mean": N_mean, "N_max": int(np.max(Ns)),
           "degree_mean": float(np.mean(degs)),
           "m_mean": float(per_seed_m.mean()),
           "m_sem": float(per_seed_m.std(ddof=1) / np.sqrt(len(per_seed_m)))
                    if len(per_seed_m) > 1 else float("nan"),
           "U4": float(U4), "random_floor": float(1.0 / np.sqrt(N_mean)),
           "n_seeds": n_seeds}
    if want_sk:
        Sm = np.mean(S_seeds, axis=0)
        alpha = fit_alpha(kmags, Sm)
        # bootstrap alpha over seeds
        rng = np.random.default_rng(7)
        boots = []
        for _ in range(300):
            idx = rng.integers(0, len(S_seeds), len(S_seeds))
            boots.append(fit_alpha(kmags, np.mean([S_seeds[i] for i in idx], axis=0)))
        row["sk"] = {"k": kmags.tolist(), "S": Sm.tolist(), "alpha": alpha,
                     "alpha_err": float(np.nanstd(boots)),
                     "k_decades": float(np.log10(kmags[-1] / kmags[0]))}
    return row


def main():
    t0 = time.time()
    print("=" * 78)
    print("A3 / C2 -- Goldstone FSS (larger N) + transverse S(k)~1/k^alpha")
    print("=" * 78)

    gate = estimator_gate()
    print(f"[estimator gate] 3D ordered cubic lattice L={gate['L']} (n={gate['n']}): "
          f"alpha={gate['alpha']:.2f}  (expect ~2 = gradient rigidity)")

    # sizes: extend the E4-0 ladder (..7.4 ~ 1462) up to ~4-5k events
    plan = [(4.4, 12, False), (5.4, 12, False), (6.4, 10, True),
            (7.4, 8, True), (8.4, 6, True), (9.4, 4, True)]
    rows = []
    for L, ns, want_sk in plan:
        r = run_size(L, ns, want_sk)
        rows.append(r)
        sk = (f"  alpha={r['sk']['alpha']:.2f}+/-{r['sk']['alpha_err']:.2f} "
              f"({r['sk']['k_decades']:.1f} dec)") if "sk" in r else ""
        print(f"  L={L:.1f} N~{r['N_mean']:.0f} <deg>={r['degree_mean']:.0f}  "
              f"m={r['m_mean']:.4f}+/-{r['m_sem']:.4f}  U4={r['U4']:.3f}  "
              f"floor={r['random_floor']:.4f}{sk}", flush=True)

    # ---- verdict (a) LRO ---------------------------------------------------- #
    Ns = np.array([r["N_mean"] for r in rows])
    ms = np.array([r["m_mean"] for r in rows])
    floors = np.array([r["random_floor"] for r in rows])
    U4s = np.array([r["U4"] for r in rows])
    m_trend = float(np.polyfit(np.log(Ns), np.log(ms), 1)[0])
    above_floor = bool(np.all(ms / floors > 3.0))
    lro_ok = above_floor and (m_trend > -0.15) and bool(np.all(U4s > 0.55))
    lro = ("SUCCESS_LRO" if lro_ok else
           ("DEATH_ARTEFACT" if (not above_floor and m_trend < -0.35) else "PARTIAL"))

    # ---- verdict (b) S(k) alpha --------------------------------------------- #
    sk_rows = [r for r in rows if "sk" in r]
    alphas = np.array([r["sk"]["alpha"] for r in sk_rows])
    errs = np.array([r["sk"]["alpha_err"] for r in sk_rows])
    a_big, e_big = float(alphas[-1]), float(errs[-1])
    a_trend = float(np.polyfit(np.log([r["N_mean"] for r in sk_rows]), alphas, 1)[0]) \
        if len(sk_rows) >= 2 else float("nan")
    excl_meanfield = abs(a_big - 0.0) > 3 * e_big and a_big > 0.5
    excl_rigid = abs(a_big - 2.0) > 3 * e_big
    if (not excl_meanfield) and a_big < 1.0:
        sk_verdict = (f"MEAN-FIELD confirmed at large N: alpha={a_big:.2f}+/-{e_big:.2f} "
                      f"~0 (flat), N-trend d(alpha)/d(lnN)={a_trend:+.2f}. The bare causal "
                      f"links carry NON-LOCAL mean-field orientation, NOT k^2 gradient "
                      f"rigidity -> hardens E1-3 Verdict C; the relativistic magnon needs "
                      f"the BD/Sorkin operator (E2/e10), not the bare links.")
    elif (not excl_rigid) and a_big > 1.4:
        sk_verdict = (f"GRADIENT RIGIDITY at large N: alpha={a_big:.2f}+/-{e_big:.2f} ~2 -> "
                      f"bare links DO show k^2 rigidity (revises E1-3).")
    else:
        sk_verdict = (f"INDETERMINATE: alpha={a_big:.2f}+/-{e_big:.2f} between 0 and 2, "
                      f"neither excluded (method frontier); N-trend {a_trend:+.2f}.")

    out = {"config": {"J": J, "rho": RHO, "n_burn": N_BURN, "n_meas": N_MEAS},
           "estimator_gate": gate, "rows": rows,
           "lro": {"m_trend_dlnm_dlnN": m_trend, "above_floor": above_floor,
                   "verdict": lro},
           "sk": {"alpha_by_N": [(r["N_mean"], r["sk"]["alpha"], r["sk"]["alpha_err"])
                                 for r in sk_rows],
                  "alpha_trend_dalpha_dlnN": a_trend, "verdict": sk_verdict},
           "runtime_s": time.time() - t0}
    (HERE / "A3_fss_sk.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"(a) LRO: {lro}  (m-trend dlnm/dlnN={m_trend:+.3f}, N up to {Ns.max():.0f})")
    print(f"(b) S(k): {sk_verdict}")
    print(f"[{out['runtime_s']:.1f}s] -> A3_fss_sk.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
