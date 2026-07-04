"""FLB_ordering.py -- FL1_SU3_FOUNDATION, Phase B (spontaneous ordering).

Runs ONLY because Phase A passed (SU(3) definable, action PSD, causal).  Repeats
the E1 protocol (Monte Carlo, C(r), J_c) for the SU(3) principal-chiral field
instead of O(3): does the SU(3) vacuum order spontaneously, and if so where and how?

MODEL (the matrix analogue of E1's O(3) Heisenberg model):
    site field U_i in SU(3),   E = -J sum_{<ij>} (1/3) Re Tr(U_i U_j^dag).
Order parameter m = |mean_i v_i|, v = (1/sqrt3)[ReU, ImU] the unit 18-vector with
v_i.v_j = (1/3)Re Tr(U_i U_j^dag).  Ordering breaks SU(3)xSU(3) -> diagonal SU(3).
Disordered baseline m ~ 1/sqrt(N); C(r) plateau = m^2 (Mermin clustering).

PRE-REGISTERED PREDICTION (written before the production run):
  * A continuous-symmetry spin model on a high-coordination 3D / 4D-causal graph
    DOES order at finite J -> Phase B expected to FIND a J_c (so PASS).
  * DISTINGUISHER vs SU(2): SU(N>=3) principal-chiral / matrix transitions are
    known (COMPARISON ONLY, literature) to be FIRST ORDER, unlike SU(2)~O(4)
    (second order, E1).  Signatures to MEASURE (not assume): a discontinuous jump
    in m and in E/link, susceptibility peak chi_max ~ V (volume law, vs sub-volume
    for 2nd order), specific-heat peak C_max ~ V, a Binder-cumulant dip near J_c,
    and a BIMODAL energy histogram at J_c (coexistence / latent heat).  The pilot
    scan already showed m jumping 0.08->0.56 across one J unit -- consistent, to be
    confirmed by finite-size scaling.

DEATH CRITERION (Phase B, pre-registered): no ordering transition in any reasonable
region of (J) -- m stays ~1/sqrt(N) and C(r) exponential at all J.  If that holds,
the SU(3) vacuum never picks a direction: honest death at Phase B.

Anti-circularity: no QCD number anywhere; no critical coupling inserted; the order
parameter, classifier and metric are fixed before the data; fixed seeds.  The only
external reference is the literature "first-order for N>=3" statement, used ONLY to
frame the prediction and confined to COMPARISON ONLY notes -- never an input.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su3_core as s3

# ---- scale presets ---------------------------------------------------------- #
SCALE = sys.argv[1] if len(sys.argv) > 1 else "full"
if SCALE == "quick":
    CUBIC_LS = [6, 8]
    N_SEEDS_CUBIC = 2
    BURN_C, MEAS_C = 600, 600
    CAUSAL_RHO, CAUSAL_BOX = 2.0, [(0.0, 24.0), (0.0, 3.0), (0.0, 3.0), (0.0, 3.0)]
    N_SEEDS_CAUSAL = 4
    BURN_G, MEAS_G = 500, 120
else:
    CUBIC_LS = [6, 8, 10, 12]
    N_SEEDS_CUBIC = 4
    BURN_C, MEAS_C = 1200, 1500
    CAUSAL_RHO, CAUSAL_BOX = 2.0, [(0.0, 40.0), (0.0, 3.0), (0.0, 3.0), (0.0, 3.0)]
    N_SEEDS_CAUSAL = 8
    BURN_G, MEAS_G = 1200, 150

# J grids: coarse outside, fine across the pilot-located window [2.3, 3.1]
J_COARSE = [1.0, 1.5, 2.0, 3.5, 4.0, 5.0]
J_FINE = [2.3, 2.4, 2.5, 2.6, 2.65, 2.7, 2.75, 2.8, 2.85, 2.9, 3.0, 3.1]
JS_CUBIC = sorted(set(J_COARSE + J_FINE))
# the causal link graph has very high coordination (avgdeg ~44, the known
# non-locality of 4D causal-set links), so its J_c sits FAR BELOW the cubic value;
# extend the scan downward to expose the disordered phase and locate J_c (honest
# scoping, declared -- the same extension E1 made for O(3) on this substrate).
JS_CAUSAL = sorted(set([0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.5, 1.0,
                        1.5, 2.0, 2.5, 3.0, 4.0, 6.0]))
MEAS_EVERY = 2
R_CAP = 40
MIN_COUNT = 200
N_SOURCES = 24


# =========================================================================== #
# cubic-lattice anchor: finite-size scaling -> J_c and transition ORDER
# =========================================================================== #
def measure_run(model, n_burn, n_meas, meas_every=2):
    """Equilibrate, then collect time series of m and E/link."""
    model.equilibrate(n_burn, adapt=True)
    ms, es = [], []
    taken, s = 0, 0
    while taken < n_meas:
        model.sweep(); s += 1
        if s % meas_every == 0:
            ms.append(model.order_parameter())
            es.append(model.energy_per_link() / model.J)   # intensive overlap
            taken += 1
    return np.array(ms), np.array(es)


def run_cubic(L, Js, n_seeds, burn, meas):
    g = s3.lattice_periodic((L, L, L))
    N = g.n
    out = {}
    for J in Js:
        m_all, e_all = [], []
        for seed in range(n_seeds):
            mdl = s3.SU3ChiralModel(g, J=J, seed=100 * seed + 7)
            ms, es = measure_run(mdl, burn, meas, MEAS_EVERY)
            m_all.append(ms); e_all.append(es)
        ms = np.concatenate(m_all); es = np.concatenate(e_all)
        m_mean = float(ms.mean())
        chi = float(N * (np.mean(ms ** 2) - m_mean ** 2))
        binder = float(1.0 - np.mean(ms ** 4) / (3.0 * np.mean(ms ** 2) ** 2))
        e_mean = float(es.mean())
        cv = float(N * (np.mean(es ** 2) - e_mean ** 2))   # specific-heat proxy
        out[J] = {"m": m_mean, "m_series_std": float(ms.std()), "chi": chi,
                  "binder": binder, "E_per_link": e_mean, "Cv": cv,
                  "e_series": es.tolist()}
    return N, g, out


def transition_order_diagnostics(per_L):
    """From per-L cubic sweeps, locate J_c(L) (chi peak), extract chi_max(L),
    Cv_max(L), Binder dip, and the energy histogram at J_c(L) for the largest L.
    Returns scaling exponents and a first/second-order call."""
    Ls = sorted(per_L.keys())
    jc_chi, chi_max, cv_max, Ns, binder_min = [], [], [], [], []
    for L in Ls:
        N, _, res = per_L[L]
        Js = sorted(res.keys())
        chis = np.array([res[J]["chi"] for J in Js])
        cvs = np.array([res[J]["Cv"] for J in Js])
        binders = np.array([res[J]["binder"] for J in Js])
        jc = Js[int(np.argmax(chis))]
        jc_chi.append(jc); chi_max.append(float(chis.max()))
        cv_max.append(float(cvs.max())); Ns.append(N)
        binder_min.append(float(binders.min()))
    Ns = np.array(Ns, float)
    # power-law exponent of peak heights vs volume N: first order -> ~1
    def slope(y):
        y = np.array(y, float)
        if len(y) >= 2 and np.all(y > 0):
            return float(np.polyfit(np.log(Ns), np.log(y), 1)[0])
        return float("nan")
    chi_exp = slope(chi_max)
    cv_exp = slope(cv_max)

    # energy histogram at J_c for the largest L (bimodality / latent heat)
    Lbig = Ls[-1]
    _, _, resbig = per_L[Lbig]
    Jsbig = sorted(resbig.keys())
    jcbig = Jsbig[int(np.argmax([resbig[J]["chi"] for J in Jsbig]))]
    e_series = np.array(resbig[jcbig]["e_series"])
    hist, edges = np.histogram(e_series, bins=40, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    # bimodality: gap between the two largest separated peaks of a smoothed hist
    bimodal, latent = _bimodality(centers, hist)

    # first-order call: volume-law peaks (exp ~ 1) OR clear bimodality
    first_order = (chi_exp > 0.8) or (cv_exp > 0.8) or bimodal
    return {
        "Ls": Ls, "Ns": Ns.tolist(), "Jc_chi_peak_per_L": jc_chi,
        "chi_max_per_L": chi_max, "cv_max_per_L": cv_max,
        "binder_min_per_L": binder_min,
        "chi_max_volume_exponent": chi_exp, "cv_max_volume_exponent": cv_exp,
        "Jc_largest_L": jcbig, "largest_L": Lbig,
        "energy_hist_at_Jc": {"centers": centers.tolist(), "density": hist.tolist()},
        "energy_bimodal": bool(bimodal), "latent_heat_estimate": latent,
        "order_call": "first-order" if first_order else "second-order/continuous",
    }


def _bimodality(centers, hist):
    """Crude two-peak detector: smooth, find local maxima, require two with a clear
    valley (valley < 0.6 * min(peak heights)).  Returns (is_bimodal, peak gap)."""
    if len(hist) < 5:
        return False, 0.0
    k = np.array([0.25, 0.5, 0.25])
    h = np.convolve(hist, k, mode="same")
    peaks = [i for i in range(1, len(h) - 1) if h[i] > h[i - 1] and h[i] >= h[i + 1]]
    peaks = sorted(peaks, key=lambda i: -h[i])
    if len(peaks) < 2:
        return False, 0.0
    p1, p2 = sorted(peaks[:2])
    valley = h[p1:p2 + 1].min()
    ok = valley < 0.6 * min(h[p1], h[p2]) and (p2 - p1) >= 2
    return bool(ok), float(abs(centers[p2] - centers[p1]))


# =========================================================================== #
# causal-substrate run: C(r) by longest chain, J_c on the TEIC vacuum
# =========================================================================== #
def build_causal_seed(seed):
    rng = np.random.default_rng(7000 + seed)
    pts = s3.sprinkle_box(CAUSAL_RHO, CAUSAL_BOX, rng)
    g = s3.causal_link_graph(pts)
    early = g.topo_order[:max(N_SOURCES, int(0.3 * g.n))]
    sources = rng.choice(early, size=min(N_SOURCES, early.size), replace=False)
    dist_list = [s3.longest_chain_from(g, int(s), r_max=R_CAP) for s in sources]
    return g, sources, dist_list


def run_causal_model(g, sources, dist_list, J, seed):
    mdl = s3.SU3ChiralModel(g, J=J, seed=9001 * seed + 3)
    mdl.equilibrate(BURN_G, adapt=True)
    acc = s3.CorrelationAccumulator(sources, dist_list, R_CAP)
    ms = []
    taken, s = 0, 0
    while taken < MEAS_G:
        mdl.sweep(); s += 1
        if s % MEAS_EVERY == 0:
            acc.add(mdl); ms.append(mdl.order_parameter()); taken += 1
    r, C, w = acc.result()
    ms = np.array(ms)
    chi = float(g.n * (np.mean(ms ** 2) - np.mean(ms) ** 2))
    return r, C, w, float(ms.mean()), chi


def aggregate_curves(curves, r_ref):
    Cs, Ws = [], []
    for r, C, w in curves:
        Cg = np.full(r_ref.shape, np.nan); Wg = np.zeros(r_ref.shape)
        idx = {int(rr): k for k, rr in enumerate(r)}
        for k, rr in enumerate(r_ref):
            if rr in idx:
                Cg[k] = C[idx[rr]]; Wg[k] = w[idx[rr]]
        Cs.append(Cg); Ws.append(Wg)
    Cs, Ws = np.array(Cs), np.array(Ws)
    import warnings
    with np.errstate(invalid="ignore"), warnings.catch_warnings():
        warnings.simplefilter("ignore", RuntimeWarning)
        Cmean = np.nansum(Cs * Ws, axis=0) / np.maximum(np.nansum(Ws, axis=0), 1e-9)
        Cstd = np.nanstd(Cs, axis=0)
    return Cmean, Cstd, np.nansum(Ws, axis=0)


def run_causal(Js, n_seeds):
    raw = {J: [] for J in Js}
    mvals = {J: [] for J in Js}
    chivals = {J: [] for J in Js}
    gstats = []
    for seed in range(n_seeds):
        g, sources, dist_list = build_causal_seed(seed)
        gstats.append({"n": g.n, "links": g.n_links, "avgdeg": 2 * g.n_links / g.n})
        for J in Js:
            r, C, w, mm, chi = run_causal_model(g, sources, dist_list, J, seed)
            raw[J].append((r, C, w)); mvals[J].append(mm); chivals[J].append(chi)
    r_ref = np.arange(1, R_CAP + 1)
    res = {}
    for J in Js:
        Cmean, Cstd, Wtot = aggregate_curves(raw[J], r_ref)
        ok = Wtot >= MIN_COUNT
        fit = s3.fit_forms(r_ref[ok], Cmean[ok], sigma=Cstd[ok], r_lo=2)
        m_mean = float(np.mean(mvals[J]))
        res[J] = {"r": r_ref[ok].tolist(), "C": Cmean[ok].tolist(),
                  "C_err": (Cstd[ok] / np.sqrt(n_seeds)).tolist(),
                  "counts": Wtot[ok].tolist(), "fit": fit,
                  "m": m_mean, "m2": m_mean ** 2, "chi": float(np.mean(chivals[J])),
                  "C_long": fit["C_long"], "winner": fit["winner"]}
    chi_arr = np.array([res[J]["chi"] for J in Js])
    jc_chi = Js[int(np.argmax(chi_arr))]
    exp_Js = [J for J in Js if res[J]["winner"] == "exp"]
    const_Js = [J for J in Js if res[J]["winner"] == "const"]
    jc_cross = (0.5 * (max(exp_Js) + min(J for J in const_Js if J > max(exp_Js)))
                if exp_Js and const_Js and any(J > max(exp_Js) for J in const_Js)
                else None)
    gmean = {k: float(np.mean([s[k] for s in gstats])) for k in ("n", "links", "avgdeg")}
    return res, {"chi_peak_J": jc_chi, "crossover_J": jc_cross,
                 "chi_max": float(chi_arr.max())}, gmean


# =========================================================================== #
def main():
    t0 = time.time()
    print("=" * 74)
    print(f"FL1_SU3_FOUNDATION -- Phase B (spontaneous ordering)  [scale={SCALE}]")
    print("=" * 74)

    # ---- cubic anchor + finite-size scaling ---- #
    print("\n[1] cubic-lattice anchor (literature control) + finite-size scaling")
    per_L = {}
    for L in CUBIC_LS:
        N, g, res = run_cubic(L, JS_CUBIC, N_SEEDS_CUBIC, BURN_C, MEAS_C)
        per_L[L] = (N, g, res)
        chis = [res[J]["chi"] for J in JS_CUBIC]
        jc = JS_CUBIC[int(np.argmax(chis))]
        m_lo = res[JS_CUBIC[0]]["m"]; m_hi = res[JS_CUBIC[-1]]["m"]
        print(f"  L={L:2d} (N={N:4d}): J_c(chi)~{jc:.2f}  chi_max={max(chis):.2f}  "
              f"m[{JS_CUBIC[0]:.1f}]={m_lo:.3f} -> m[{JS_CUBIC[-1]:.1f}]={m_hi:.3f}  "
              f"({time.time()-t0:.0f}s)")
    order = transition_order_diagnostics(per_L)
    print(f"  -> J_c (largest L={order['largest_L']}): {order['Jc_largest_L']:.2f}")
    print(f"  -> chi_max ~ N^{order['chi_max_volume_exponent']:.2f}, "
          f"Cv_max ~ N^{order['cv_max_volume_exponent']:.2f} "
          f"(exponent ~1 => first order / volume law)")
    print(f"  -> energy histogram at J_c bimodal: {order['energy_bimodal']} "
          f"(latent~{order['latent_heat_estimate']:.3f})")
    print(f"  -> TRANSITION ORDER CALL: {order['order_call']}")

    # ---- causal substrate (the TEIC vacuum) ---- #
    print("\n[2] causal substrate (3+1D Poisson Hasse diagram, longest-chain C(r))")
    causal_res, causal_jc, gmean = run_causal(JS_CAUSAL, N_SEEDS_CAUSAL)
    print(f"  graph: n~{gmean['n']:.0f} links~{gmean['links']:.0f} "
          f"avgdeg~{gmean['avgdeg']:.0f}")
    for J in JS_CAUSAL:
        d = causal_res[J]
        print(f"  J={J:4.1f}  m={d['m']:.3f}  chi={d['chi']:8.2f}  "
              f"C(r):{d['winner']:6s}  C_long={d['C_long']:.3f}  m^2={d['m2']:.3f}")
    print(f"  -> J_c(chi-peak)={causal_jc['chi_peak_J']}  "
          f"J_c(exp->const crossover)~{causal_jc['crossover_J']}")

    # ---- verdict ---- #
    ordered_cubic = order["chi_max_per_L"][-1] > 1.0 and \
        per_L[CUBIC_LS[-1]][2][JS_CUBIC[-1]]["m"] > 0.3
    ordered_causal = any(causal_res[J]["winner"] == "const" for J in JS_CAUSAL)
    phase_B_passes = ordered_cubic or ordered_causal
    if not phase_B_passes:
        verdict = "PHASE B DEATH -- no ordering transition (vacuum never orders)"
    else:
        verdict = (f"PHASE B PASSES -- SU(3) vacuum orders ({order['order_call']}); "
                   f"J_c(cubic)~{order['Jc_largest_L']:.2f}, "
                   f"J_c(causal)~{causal_jc['chi_peak_J']}")
    print("-" * 74)
    print(f"VERDICT: {verdict}")
    print("=" * 74)

    # ---- figure ---- #
    _figure(per_L, order, causal_res, causal_jc)

    payload = {
        "scale": SCALE,
        "config": {"cubic_Ls": CUBIC_LS, "Js_cubic": JS_CUBIC,
                   "n_seeds_cubic": N_SEEDS_CUBIC, "burn_c": BURN_C, "meas_c": MEAS_C,
                   "causal_rho": CAUSAL_RHO, "causal_box": CAUSAL_BOX,
                   "Js_causal": JS_CAUSAL, "n_seeds_causal": N_SEEDS_CAUSAL,
                   "burn_g": BURN_G, "meas_g": MEAS_G, "r_cap": R_CAP},
        "cubic": {str(L): {"N": per_L[L][0],
                           "by_J": {str(J): {k: v for k, v in per_L[L][2][J].items()
                                             if k != "e_series"}
                                    for J in JS_CUBIC}}
                  for L in CUBIC_LS},
        "transition_order": order,
        "causal_graph": gmean,
        "causal": {str(J): causal_res[J] for J in JS_CAUSAL},
        "causal_Jc": causal_jc,
        "ordered_cubic": bool(ordered_cubic), "ordered_causal": bool(ordered_causal),
        "phase_B_passes": bool(phase_B_passes), "verdict": verdict,
        "runtime_s": time.time() - t0,
    }
    s3.save_json("FLB_ordering.json", payload, phase="B")
    print(f"saved FLB_ordering.json  ({payload['runtime_s']:.0f}s)")
    return payload


def _figure(per_L, order, causal_res, causal_jc):
    fig, axes = plt.subplots(2, 2, figsize=(13, 10))
    # (a) m(J) per L
    ax = axes[0, 0]
    for L in sorted(per_L):
        res = per_L[L][2]
        Js = sorted(res.keys())
        ax.plot(Js, [res[J]["m"] for J in Js], "o-", ms=3, label=f"L={L}")
    ax.set_xlabel("J (=1/T)"); ax.set_ylabel("order parameter m")
    ax.set_title("cubic: m(J) rises at the ordering transition"); ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    # (b) chi(J) per L
    ax = axes[0, 1]
    for L in sorted(per_L):
        res = per_L[L][2]; Js = sorted(res.keys())
        ax.plot(Js, [res[J]["chi"] for J in Js], "s-", ms=3, label=f"L={L}")
    ax.set_xlabel("J"); ax.set_ylabel("susceptibility chi")
    ax.set_title("chi(J) peaks at J_c"); ax.legend(fontsize=8); ax.grid(alpha=0.2)
    # (c) peak-height finite-size scaling (volume law => first order)
    ax = axes[1, 0]
    Ns = np.array(order["Ns"], float)
    ax.loglog(Ns, order["chi_max_per_L"], "o-", label=f"chi_max ~ N^{order['chi_max_volume_exponent']:.2f}")
    ax.loglog(Ns, order["cv_max_per_L"], "s-", label=f"Cv_max ~ N^{order['cv_max_volume_exponent']:.2f}")
    ax.set_xlabel("N (volume)"); ax.set_ylabel("peak height")
    ax.set_title("finite-size scaling of peaks\n(exponent ~1 = volume law = 1st order)")
    ax.legend(fontsize=8); ax.grid(alpha=0.2, which="both")
    # (d) causal C(r)
    ax = axes[1, 1]
    for J in sorted(causal_res):
        d = causal_res[J]
        r = np.array(d["r"]); C = np.array(d["C"]); sel = C > 0
        if sel.any():
            ax.plot(r[sel], C[sel], "o-", ms=3, label=f"J={J:g} ({d['winner']})")
    ax.set_yscale("log"); ax.set_xlabel("r (causal proper time, longest chain)")
    ax.set_ylabel("C(r)"); ax.set_title("causal vacuum: C(r) (flat = LRO)")
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.2)
    fig.suptitle("FL1 Phase B: SU(3) principal-chiral vacuum ordering "
                 "(cubic anchor + causal substrate)", fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(Path(__file__).resolve().parent / "FLB_ordering.png", dpi=130)
    print(f"saved FLB_ordering.png")


if __name__ == "__main__":
    main()
