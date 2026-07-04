"""INV2_reproduce.py -- independent reproduction of the critical T14-T21BIS experiments.

AUDIT of TEIC-GE's teic_st T14-T21BIS ("matter = causal connectivity").  Reproduces
before judging (golden rule).  We re-implement the GE measurement functions VERBATIM
(same logic as ../TEIC-GE/results/teic_st/T14/*.py) so we can (a) add the missing
error bars over independent seeds and (b) probe robustness -- without polluting the
TEIC-GE tree.  GE's originals are single-seed (rng=42 or unseeded) with no error bars.

Anti-circularity of THIS harness: the Lorentz factor gamma is computed ONLY inside a
COMPARISON ONLY block, never fed into any measured quantity.  (This file lives under
results/, which the main guard does not scan, but the rule is obeyed regardless.)

Four reproductions, mapping to the central claim "matter = causal connectivity":
  R-REL  (T18/T19): does the link-overlap of a shifted blob reproduce gamma / 1/gamma?
  R-MASS (T15/T16): is "mass" = <k> robust, and is it independent of transport cost?
  R-GRAV (T17B):    where does the 1/r of "Schwarzschild from connectivity" come from?
  R-PART (T20/T21BIS): are "spin/exclusion" derived, or hand-built structures?
"""
from __future__ import annotations
import json, time
from pathlib import Path
import numpy as np

OUT = Path(__file__).resolve().parent
N_SEEDS = 20


# ===================================================================== #
#  Verbatim re-implementations of the GE measurement primitives         #
# ===================================================================== #
def ge_links_shifted_blob(n, v, seed, dt=0.2, sigma=0.1, dim=2):
    """T18A/T18BC/T19 measurement: causal links between a Gaussian blob at t=0 and
    the SAME blob translated by (dt, v*dt).  (GE used n=1000, dt=0.2, sigma=0.1.)"""
    rng = np.random.default_rng(seed)
    pts0 = rng.normal(0, sigma, size=(n, dim))
    pts0[:, 0] = 0.0
    pts1 = pts0.copy()
    pts1[:, 0] += dt
    pts1[:, 1] += v * dt
    diff_t = pts1[None, :, 0] - pts0[:, None, 0]
    diff_x2 = np.sum((pts1[None, :, 1:] - pts0[:, None, 1:]) ** 2, axis=-1)
    adj = (diff_t > 0) & (diff_t ** 2 > diff_x2)
    return np.sum(adj) / n


def ge_random_diamond(n, dim, rng):
    pts = []
    while len(pts) < n:
        p = rng.uniform(0, 1.0, size=dim)
        r = np.linalg.norm(p[1:] - 0.5)
        if abs(p[0] - 0.5) + r < 0.5:
            pts.append(p)
    return np.array(pts[:n])


def ge_longest_path(pts):
    n = len(pts)
    adj = _adj(pts)
    order = np.argsort(pts[:, 0])
    a = adj[order][:, order]
    L = np.zeros(n, dtype=int)
    for i in range(n):
        js = np.where(a[:i, i])[0]
        if js.size:
            L[i] = L[js].max() + 1
    return int(L.max()) if n else 0


def _adj(pts):
    dt = pts[None, :, 0] - pts[:, None, 0]
    dx2 = np.sum((pts[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    return (dt > 0) & (dt * dt > dx2)


def ge_transport_cost(pts, dt=0.1, window=0.2):
    n = len(pts)
    ps = pts.copy(); ps[:, 0] += dt
    d_t = ps[None, :, 0] - pts[:, None, 0]
    d_x2 = np.sum((ps[None, :, 1:] - pts[:, None, 1:]) ** 2, axis=-1)
    adj = (d_t > 0) & (d_t * d_t > d_x2) & (d_t <= window)
    return np.sum(adj) / n


def ge_avg_k(pts):
    return np.sum(_adj(pts)) / len(pts)


# ===================================================================== #
#  R-REL : T18/T19 -- "Special relativity emerges"                      #
# ===================================================================== #
def repro_relativity():
    vs = np.array([0, 0.2, 0.4, 0.6, 0.8, 0.9, 0.95, 0.98])
    # measured link-overlap vs v, mean +/- std over seeds (GE: single seed 42)
    M = np.array([[ge_links_shifted_blob(1000, v, s) for v in vs]
                  for s in range(N_SEEDS)])
    rate = M / M[:, :1]                     # normalised to v=0, per seed
    rate_mean, rate_std = rate.mean(0), rate.std(0)
    E = 1.0 / rate                          # GE's T19 definition E = rate0/rate
    E_mean, E_std = E.mean(0), E.std(0)

    # ---------------- COMPARISON ONLY -- textbook Lorentz factor ----------------
    gamma = 1.0 / np.sqrt(1.0 - vs ** 2)
    inv_gamma = np.sqrt(1.0 - vs ** 2)
    # how well does the measured rate match 1/gamma?  (GE claims rate ~ 1/gamma)
    res_rate = float(np.sqrt(np.mean((rate_mean - inv_gamma) ** 2)))
    res_E = float(np.sqrt(np.mean((E_mean - gamma) ** 2)))
    # control: fit the measured rate to a pure-Gaussian overlap exp(-a v^2) (no SR)
    a_fit = float(-np.polyfit(vs ** 2, np.log(rate_mean), 1)[0])
    gauss = np.exp(-a_fit * vs ** 2)
    res_gauss = float(np.sqrt(np.mean((rate_mean - gauss) ** 2)))
    # ---------------- END COMPARISON ONLY ----------------

    # robustness: does the curve change with the ARBITRARY blob width sigma?
    sigma_test = {}
    for sg in (0.05, 0.1, 0.2):
        r = np.array([ge_links_shifted_blob(1000, v, 0, sigma=sg) for v in vs])
        r = r / r[0]
        sigma_test[sg] = float(np.sqrt(np.mean((r - inv_gamma) ** 2)))

    return dict(
        vs=vs.tolist(), rate_mean=rate_mean.tolist(), rate_std=rate_std.tolist(),
        E_mean=E_mean.tolist(), E_std=E_std.tolist(),
        COMPARISON_inv_gamma=inv_gamma.tolist(), COMPARISON_gamma=gamma.tolist(),
        rmse_rate_vs_inv_gamma=res_rate, rmse_E_vs_gamma=res_E,
        gaussian_overlap_a=a_fit, rmse_rate_vs_gaussian=res_gauss,
        sigma_sensitivity_rmse_vs_inv_gamma=sigma_test,
        note="Measured 'rate' is the overlap of a hand-translated Gaussian blob; v is "
             "imposed by hand. A pure-Gaussian overlap exp(-a v^2) fits as well or "
             "better than 1/gamma, and the fit DEPENDS on the arbitrary blob width "
             "sigma -- so this is a one-parameter coincidence over a limited v-range, "
             "not a derivation of the Lorentz factor.")


# ===================================================================== #
#  R-MASS : T15/T16 -- "mass = <k> (connectivity)"                       #
# ===================================================================== #
def repro_mass():
    rows = []
    for d in (2, 3, 4):
        for n in (100, 300):
            costs, ks, nls = [], [], []
            for s in range(N_SEEDS):
                rng = np.random.default_rng(1000 + s)
                pts = ge_random_diamond(n, d, rng)
                L = ge_longest_path(pts)
                costs.append(ge_transport_cost(pts))
                ks.append(ge_avg_k(pts))
                nls.append(n / (L + 1))
            costs, ks, nls = map(np.array, (costs, ks, nls))
            ratio = costs / ks
            rows.append(dict(dim=d, n=n,
                             NL_mean=float(nls.mean()), NL_std=float(nls.std()),
                             avgk_mean=float(ks.mean()), avgk_std=float(ks.std()),
                             cost_mean=float(costs.mean()), cost_std=float(costs.std()),
                             cost_over_k_mean=float(ratio.mean()),
                             cost_over_k_std=float(ratio.std())))
    ratios = [r["cost_over_k_mean"] for r in rows]
    return dict(rows=rows, cost_over_k_range=[min(ratios), max(ratios)],
                note="Cost (links per event in a dt-window) and <k> (links per event) "
                     "BOTH count causal links per event, so Cost/<k> being O(1)-stable "
                     "is near-tautological, not a discovered law. GE used unseeded "
                     "single shots; here mean+/-std over 20 seeds.")


# ===================================================================== #
#  R-GRAV : T17B -- "Schwarzschild 1/r from connectivity"                #
# ===================================================================== #
def ge_solve_poisson_radial(r, k, alpha=1e-3):
    """Verbatim GE solver: it HARD-CODES the radial Poisson equation."""
    dr = np.gradient(r)
    m_enc = np.cumsum(k * (r ** 2) * dr)
    dtheta_dr = alpha * m_enc / (r ** 2 + 1e-9)
    theta = -np.cumsum((dtheta_dr[::-1] * dr[::-1]))[::-1]
    return theta


def repro_grav():
    r = np.linspace(0.05, 2.0, 50)
    out = {}
    # GE's source: an excess-connectivity-like central peak
    for label, src in [
        ("connectivity_like_peak", np.exp(-(r / 0.2) ** 2)),
        ("arbitrary_gaussian", np.exp(-(r / 0.3) ** 2)),
        ("arbitrary_topcap", (r < 0.3).astype(float)),
        ("arbitrary_triangle", np.clip(0.3 - r, 0, None))]:
        theta = ge_solve_poisson_radial(r, src - src[-1])
        far = r > 0.3
        corr = float(np.corrcoef(theta[far], (1.0 / r)[far])[0, 1])
        out[label] = corr
    return dict(corr_with_1_over_r=out,
                note="The GE solver hard-codes (1/r^2) d/dr(r^2 dtheta/dr) = alpha*k, "
                     "i.e. the radial Poisson operator. ANY centrally-peaked source -- "
                     "connectivity or not -- yields a ~1/r exterior (3D Green's "
                     "function). So 'corr 0.86 with 1/r' measures the coded Laplacian, "
                     "not connectivity. This rediscovers TEIC's own D1-D3 (nabla^2 "
                     "theta=J -> 1/r), which TEIC did far more rigorously (corr 0.9991, "
                     "unconstrained MC, no hard-coded Poisson).")


# ===================================================================== #
#  R-PART : T20/T21BIS -- "spin / Pauli exclusion"                       #
# ===================================================================== #
def ge_helix(n):
    t = np.linspace(0, 0.5, n)
    x = 0.1 * np.cos(2 * np.pi * t / 0.2)
    y = 0.1 * np.sin(2 * np.pi * t / 0.2)
    return np.column_stack([t, x, y, np.zeros_like(t)])


def repro_particles():
    # T21BIS exclusion: k_total of two helices vs separation (deterministic structure)
    f1 = ge_helix(30)
    dists = [1.0, 0.5, 0.2, 0.1, 0.05, 0.02]
    ktot = []
    for d in dists:
        f2 = ge_helix(30) + np.array([0, d, 0, 0])
        allp = np.concatenate([f1, f2])
        ktot.append(float(np.sum(_adj(allp)) / 60))
    # is the helix actually chiral/winding in any tested invariant? it is a fixed curve
    return dict(dists=dists, k_total=ktot,
                note="'fermion' is a hand-drawn deterministic helix (the winding "
                     "argument is unused); 'Pauli exclusion' is the link-count change "
                     "as two fixed curves overlap -- no spin, no spin-statistics, no "
                     "antisymmetry, single structure, no error bars. 'Spin-1/2' (T20) "
                     "is rotating a blob with an arctan2 z-offset and printing path "
                     "counts, with no 2pi-vs-4pi periodicity test. Interpretation, not "
                     "derivation.")


def main():
    t0 = time.time()
    result = dict(
        relativity=repro_relativity(),
        mass=repro_mass(),
        gravity=repro_grav(),
        particles=repro_particles(),
        n_seeds=N_SEEDS,
        runtime_s=round(time.time() - t0, 1),
        timestamp_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    (OUT / "INV2_reproduce_data.json").write_text(json.dumps(result, indent=2))

    rel = result["relativity"]; ms = result["mass"]; gr = result["gravity"]
    print("=" * 72)
    print("INV2 -- REPRODUCTION OF CRITICAL T14-T21BIS EXPERIMENTS")
    print("=" * 72)
    print("\n[R-REL] T18/T19 'relativity emerges' (20 seeds):")
    print(f"  rate(v)/rate(0) vs 1/gamma     : RMSE = {rel['rmse_rate_vs_inv_gamma']:.4f}")
    print(f"  E=1/rate vs gamma              : RMSE = {rel['rmse_E_vs_gamma']:.4f}")
    print(f"  rate vs pure Gaussian overlap  : RMSE = {rel['rmse_rate_vs_gaussian']:.4f}"
          f"  (a={rel['gaussian_overlap_a']:.2f}) -- fits as well, NO relativity")
    print(f"  RMSE vs 1/gamma at sigma=0.05/0.1/0.2: "
          + ", ".join(f"{v:.3f}" for v in rel['sigma_sensitivity_rmse_vs_inv_gamma'].values())
          + "  (curve depends on arbitrary blob width)")
    print("\n[R-MASS] T15/T16 'mass = <k>' (20 seeds):  Cost/<k> by (dim,n):")
    for r in ms["rows"]:
        print(f"  dim={r['dim']} n={r['n']:>3}: <k>={r['avgk_mean']:5.2f}+-{r['avgk_std']:.2f}"
              f"  cost={r['cost_mean']:5.2f}  cost/<k>={r['cost_over_k_mean']:.3f}"
              f"+-{r['cost_over_k_std']:.3f}")
    print(f"  Cost/<k> range across all: {ms['cost_over_k_range'][0]:.3f}"
          f"-{ms['cost_over_k_range'][1]:.3f}  (both count links/event -> near-tautology)")
    print("\n[R-GRAV] T17B 'Schwarzschild 1/r': corr with 1/r for sources:")
    for k, v in gr["corr_with_1_over_r"].items():
        print(f"  {k:<24}: {v:.3f}")
    print("  -> 1/r appears for ANY central source: it is the HARD-CODED Poisson solver.")
    print("\n[R-PART] T20/T21BIS 'spin/exclusion': k_total(two helices) =",
          [round(x, 1) for x in result["particles"]["k_total"]])
    print("  -> hand-drawn helices; no spin-statistics, no error bars.")
    print(f"\n[{result['runtime_s']}s]")
    return result


if __name__ == "__main__":
    main()
