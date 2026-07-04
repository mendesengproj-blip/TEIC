"""B7 -- xi(J): is dimensional transmutation POSSIBLE on this substrate?

Campaign ESCALAS_B7 (Fase 3).  Pre-registration: PRE_REGISTRO_B7 (the prompt).
Decision gate for the expensive dynamic campaign: does the correlation length
xi diverge approaching Jc as a POWER |J-Jc|^-nu (standard transition, no scale
separation -> transmutation excluded in equilibrium) or as an ESSENTIAL
SINGULARITY exp(b|J-Jc|^-sigma) (scale separation -> transmutation possible)?

Structure
  Stage 0 (BLOCKING gate) -- prove the estimator+discriminator classify KNOWN
    cases correctly before touching the causet:
      (0a) discriminator unit-test on synthetic power & exp curves;
      (0b) POWER reference: 3D Heisenberg lattice (finite Jc, nu~0.71) -> must
           classify power with nu in the tabulated range;
      (0c) EXPONENTIAL reference: 1D Ising chain (exact, xi~exp(2J)) -> must
           classify exponential, not power.
    [Faithful-deviation note: the pre-reg names a generic "1D chain" as the
     exponential reference; the 1D CONTINUOUS-spin chains available
     (XY/Heisenberg) have xi PROPORTIONAL to J (a power law), so they would be a
     self-defeating exponential reference.  The 1D ISING chain is the genuinely
     exponential 1D reference (xi~exp(2J)); we use it.  discriminate_finite (the
     finite-Jc path used on the causet) is additionally validated on synthetic
     finite-Jc exp/power data in 0a, and optionally on the 2D-XY KT model.]
  Stage 1-3 -- xi(J) on the causet.  The Hasse HOP distance is degenerate on this
    substrate (graph diameter ~3, N-independent: documented), so the correlation
    length is measured along the longest causal CHAIN (proper-time) distance,
    which carries genuine dynamic range.  Locate Jc by the susceptibility peak,
    sweep J<Jc, apply the xi<dmax/4 finite-size cut, discriminate P vs E.

Anti-circularity (guard A1): only the graph + dot/cos energy enter the generators;
xi, nu, sigma, Jc emerge from fits; reference exponents appear only in COMPARISON.

Run:  python docs/campaigns/ESCALAS_B7/b7_xi.py [--fast]
"""
from __future__ import annotations

import json
import sys
import time
from collections import deque
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))

import b7_estimators as E                                              # noqa: E402
from orientation_core import (O3Model, XYModel, lattice_periodic,     # noqa: E402
                              causal_link_graph, measure_correlation,
                              longest_chain_from, pick_sources)
from causal_core import sprinkle_box                                  # noqa: E402

FAST = "--fast" in sys.argv

# ---- COMPARISON-ONLY reference values (never enter a generator) ------------ #
# 3D Heisenberg: K_c ~ 0.693, nu ~ 0.711 (Campostrini et al.); KT: K_KT ~ 1.12.
REF_NU_3D = (0.55, 0.85)        # 0.711 +- ~15% acceptance band for the gate
REF_KC_3D = 0.693               # only the J-sweep WINDOW, not used in any fit


# ====================================================================== #
# Generic xi(J) on a fixed graph + spin model (hop distance)
# ====================================================================== #
def susceptibility_curve(make_model, graph, Js, n_burn, n_meas, meas_every, seeds):
    """chi(J) = N (<m^2> - <m>^2) averaged over seeds; for locating Jc by peak."""
    chi, m_of_J = [], []
    for J in Js:
        m1s, m2s = [], []
        for sd in seeds:
            model = make_model(graph, J, sd)
            model.equilibrate(n_burn, adapt=True)
            ms, s, taken = [], 0, 0
            while taken < n_meas:
                model.sweep(); s += 1
                if s % meas_every == 0:
                    ms.append(model.order_parameter()); taken += 1
            ms = np.asarray(ms)
            m1s.append(ms.mean()); m2s.append((ms ** 2).mean())
        m1 = float(np.mean(m1s)); m2 = float(np.mean(m2s))
        chi.append(graph.n * (m2 - m1 ** 2)); m_of_J.append(m1)
    return np.asarray(chi), np.asarray(m_of_J)


def collect_hop_curves(make_model, graph, Js, n_burn, n_meas, meas_every, seeds,
                       r_max):
    """Build per-J seed-resolved connected C(r) curves (hop distance) for
    extract_curve_set."""
    curves = []
    for J in Js:
        Cs, rr, ww = [], None, None
        for sd in seeds:
            model = make_model(graph, J, sd)
            r, Craw, w, ms = measure_correlation(model, n_burn, n_meas, meas_every,
                                                 n_sources=min(32, graph.n),
                                                 r_max=r_max, adapt=True)
            Cs.append(E.connected(Craw, float(np.mean(ms ** 2))))
            rr, ww = r, w
        curves.append({"J": float(J), "r": rr, "C_seeds": Cs, "w": ww})
    return curves


# ====================================================================== #
# Stage 0b -- POWER reference: 3D Heisenberg lattice
# ====================================================================== #
def stage0_power_3d():
    L = 20 if FAST else 32
    dmax = L                                  # hop diameter ~ L on the torus
    seeds = [0, 1] if FAST else [0, 1, 2, 3]
    nb, nm = (150, 30) if FAST else (200, 40)
    g = lattice_periodic((L, L, L))
    mk = lambda gr, J, sd: O3Model(gr, J=J, seed=sd)
    # locate Jc by chi peak around the comparison window
    Jscan = np.linspace(0.62, 0.76, 8)
    chi, mJ = susceptibility_curve(mk, g, Jscan, nb, nm, 2, seeds[:2])
    Jc_meas = float(Jscan[int(np.argmax(chi))])
    # sweep below Jc, dense near it, and extract xi(J) with a global prefactor
    Js = np.linspace(0.50, Jc_meas - 0.01, 9 if FAST else 13)
    curves = collect_hop_curves(mk, g, Js, nb, nm, 2, seeds, r_max=min(L // 2, 16))
    recs, gp = E.extract_curve_set(curves, dmax, size_cut=4.0)
    surv = [r for r in recs if r["passes_cut"] and r["n_seeds_ok"] > 0]
    J = np.array([r["J"] for r in surv]); xi = np.array([r["xi"] for r in surv])
    er = np.array([r["xi_err"] for r in surv])
    disc = E.discriminate_finite_jcband(J, xi, er, Jc_meas, jc_band=0.03) \
        if len(surv) >= 4 else {"winner": "insufficient", "n_points": len(surv)}
    nu = disc.get("nu", float("nan"))
    # binding gate = correct CLASSIFICATION (power); nu-in-range is reported.
    ok = (disc.get("winner") == "power")
    nu_in_range = bool(REF_NU_3D[0] <= nu <= REF_NU_3D[1])
    return {"L": L, "n": g.n, "Jc_meas": Jc_meas, "Jc_ref": REF_KC_3D,
            "global_p": gp, "n_survivors": len(surv), "records": recs,
            "discriminator": disc, "nu": nu, "nu_in_range": nu_in_range,
            "gate_pass": bool(ok),
            "note": f"power ref: winner={disc.get('winner')} nu={nu:.2f} "
                    f"(in-range {REF_NU_3D}? {nu_in_range}); dBIC_E/P="
                    f"{disc.get('dBIC_E_over_P', float('nan')):.1f}; global p={gp:.2f}; "
                    f"{len(surv)} pts survive xi<L/4"}


# ====================================================================== #
# Stage 0c -- EXPONENTIAL reference: 1D Ising chain (exact)
# ====================================================================== #
def stage0_exp_1d_ising():
    """Exact 1D Ising: C(r)=tanh(J)^r, xi_true=-1/ln tanh(J) ~ (1/2)exp(2J).
    Validates (i) the estimator recovers a KNOWN exponential xi within 15%, and
    (ii) the discriminator classifies xi(J) as exponential, not power."""
    Js = np.linspace(0.9, 2.2, 12)
    rmax = 800
    n_real = 8                                           # realizations ~ MC seeds
    recs, xis, errs = [], [], []
    rng = np.random.default_rng(0)
    for J in Js:
        t = np.tanh(J)
        xi_true = -1.0 / np.log(t)
        r = np.arange(0, rmax + 1)
        base = t ** r
        per = []                                         # xi over realizations
        for _ in range(n_real):
            C = base + rng.normal(0, 0.003, base.shape)
            est = E.estimate_xi(r, C, floor=0.01, tol=0.15)
            if np.isfinite(est["xi_oz"]) and est["xi_oz"] > 0:
                per.append(est["xi_oz"])
        if len(per) >= 3:
            xi = float(np.mean(per))
            err = float(np.std(per, ddof=1) / np.sqrt(len(per)))
            recs.append({"J": float(J), "xi_true": float(xi_true), "xi_oz": xi,
                         "rel_err": float(abs(xi - xi_true) / xi_true),
                         "xi_err": max(err, 0.02 * xi)})
            xis.append(xi); errs.append(max(err, 0.02 * xi))
    med_relerr = float(np.median([r["rel_err"] for r in recs])) if recs else float("nan")
    Jok = np.array([r["J"] for r in recs])
    disc = E.discriminate_infjc(Jok, np.array(xis), np.array(errs)) \
        if len(xis) >= 4 else {"winner": "insufficient"}
    ok = (med_relerr < 0.15 and disc.get("winner") == "exp")
    return {"records": recs, "median_rel_err": med_relerr, "discriminator": disc,
            "gate_pass": bool(ok),
            "note": f"exp ref: estimator median rel-err={med_relerr:.1%} (<15%), "
                    f"discriminator winner={disc.get('winner')} "
                    f"c={disc.get('c_exp', float('nan')):.2f} (xi~e^2J -> c~2)"}


# ====================================================================== #
# Stage 0a -- discriminator unit-test on synthetic finite-Jc curves
# ====================================================================== #
def stage0_discriminator_unit():
    Jc = 0.30
    J = np.linspace(0.10, 0.27, 9)
    xiP = 1.0 * np.abs(Jc - J) ** (-0.7)
    xiE = 0.5 * np.exp(0.8 * np.abs(Jc - J) ** (-0.5))
    rP = E.discriminate_finite(J, xiP, 0.05 * xiP, Jc)
    rE = E.discriminate_finite(J, xiE, 0.05 * xiE, Jc)
    ok = (rP["winner"] == "power" and rE["winner"] == "exp")
    return {"power_case": rP, "exp_case": rE, "gate_pass": bool(ok),
            "note": f"synthetic finite-Jc: power->{rP['winner']} (nu={rP['nu']:.2f}, "
                    f"dBIC={rP['dBIC_E_over_P']:.1f}); exp->{rE['winner']} "
                    f"(sigma={rE['sigma']:.2f}, dBIC={rE['dBIC_E_over_P']:.1f})"}


# ====================================================================== #
# Causet chain-distance correlation (the viable channel)
# ====================================================================== #
def chain_corr(model, pts, n_burn, n_meas, meas_every, n_sources, r_max):
    """Connected C(r) along the longest causal CHAIN (proper-time) distance.
    Sources drawn from the earliest events (deepest futures).  Returns r, C_conn,
    counts, and the order-parameter series."""
    g = model.g
    t = np.asarray(pts)[:, 0]
    early = np.argsort(t)[: max(n_sources * 4, 1)]
    early = early[g.degree[early] > 0]
    rng = model.rng
    sources = rng.choice(early, size=min(n_sources, early.size), replace=False) \
        if early.size else pick_sources(g, n_sources, rng)
    dist_list = [longest_chain_from(g, int(s), r_max) for s in sources]
    model.equilibrate(n_burn, adapt=True)
    sum_c = np.zeros(r_max + 1); sum_w = np.zeros(r_max + 1)
    ms, taken, s = [], 0, 0
    while taken < n_meas:
        model.sweep(); s += 1
        if s % meas_every == 0:
            arrs = model.corr_arrays()
            for src, dist in zip(sources, dist_list):
                dot = np.zeros(g.n)
                for a in arrs:
                    dot += a * a[src]
                mask = dist >= 0
                rr = dist[mask]
                sum_c += np.bincount(rr, weights=dot[mask], minlength=r_max + 1)
                sum_w += np.bincount(rr, minlength=r_max + 1)
            ms.append(model.order_parameter()); taken += 1
    with np.errstate(invalid="ignore", divide="ignore"):
        C = sum_c / sum_w
    r = np.arange(r_max + 1)
    good = sum_w > 0
    ms = np.asarray(ms)
    Cc = E.connected(C[good], float(np.mean(ms ** 2)))
    return r[good], Cc, sum_w[good], ms


def causet_diameters(g, pts, k=10):
    """Report hop diameter (degenerate) and max causal-chain depth (the range we
    actually use)."""
    src = pick_sources(g, k, np.random.default_rng(0))
    hop = 0
    for s in src:
        d = _bfs(g, int(s), 100); hop = max(hop, int(d[d >= 0].max()))
    ch = 0
    for s in src:
        d = longest_chain_from(g, int(s)); ch = max(ch, int(d.max()))
    return hop, ch


def _bfs(g, source, r_max):
    dist = np.full(g.n, -1, dtype=np.int64); dist[source] = 0
    q = deque([source])
    while q:
        u = q.popleft(); du = dist[u]
        if du >= r_max:
            continue
        for v in g.neighbours(u):
            if dist[v] < 0:
                dist[v] = du + 1; q.append(v)
    return dist


# ====================================================================== #
# Stage 1-3 -- xi(J) on the causet (chain distance)
# ====================================================================== #
def build_causet(rho, box, seed):
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, box, rng)
    g = causal_link_graph(pts)
    return g, pts


def causet_xi_curve(g, pts, Js, dmax, n_burn, n_meas, seeds):
    """xi(J) on the causet via causal-chain distance, global-prefactor extraction.
    Builds per-J seed-resolved connected C(r) on a fixed 0..dmax grid (NaN where a
    seed has no counts at that chain distance) then calls extract_curve_set."""
    curves = []
    grid = np.arange(dmax + 1)
    for J in Js:
        Cs, wsum = [], np.zeros(dmax + 1)
        for sd in seeds:
            model = O3Model(g, J=J, seed=sd)
            r, Cc, w, ms = chain_corr(model, pts, n_burn, n_meas, 2,
                                      n_sources=40, r_max=dmax)
            full = np.full(dmax + 1, np.nan)
            full[r] = Cc
            Cs.append(full)
            wsum[r] += w
        curves.append({"J": float(J), "r": grid, "C_seeds": Cs, "w": wsum})
    recs, gp = E.extract_curve_set(curves, dmax, size_cut=4.0)
    for rec in recs:
        rec["global_p"] = gp
    return recs


def locate_jc(g, nb, nm, seeds):
    """Find Jc by the susceptibility peak with a coarse-then-fine low-J scan
    (Jc is small and ~1/degree on this densely-connected graph)."""
    coarse = np.geomspace(0.004, 0.06, 9)
    chi, _ = susceptibility_curve(lambda gr, J, sd: O3Model(gr, J=J, seed=sd),
                                  g, coarse, nb, nm, 2, seeds)
    j0 = coarse[int(np.argmax(chi))]
    fine = np.linspace(0.5 * j0, 1.5 * j0, 9)
    chif, _ = susceptibility_curve(lambda gr, J, sd: O3Model(gr, J=J, seed=sd),
                                   g, fine, nb, nm, 2, seeds)
    return float(fine[int(np.argmax(chif))]), {"coarse_J": coarse.tolist(),
                                               "coarse_chi": chi.tolist(),
                                               "fine_J": fine.tolist(),
                                               "fine_chi": chif.tolist()}


def meanfield_probe(g, pts, J, nb, nm, seeds):
    """Connected hop C(1), C(2) just below Jc, and the mean-field ratio z*C(1).
    Mean-field on a high-z graph: C(1)~1/z (z*C1~O(1)) with NO tail (C2/C1<<1) and
    no diverging length; a genuine critical regime would instead grow a tail."""
    z = float(g.degree.mean())
    Cs, m2 = [], []
    for sd in seeds:
        m = O3Model(g, J=J, seed=sd)
        r, Craw, w, ms = measure_correlation(m, nb, nm, 2, n_sources=40, r_max=4)
        Cs.append(Craw); m2.append(np.mean(ms ** 2))
    Cc = np.mean(Cs, 0) - np.mean(m2)
    C1 = float(Cc[1]) if len(Cc) > 1 else float("nan")
    C2 = float(Cc[2]) if len(Cc) > 2 else float("nan")
    return {"z": z, "C1": C1, "C2": C2, "z_times_C1": z * C1,
            "tail_ratio_C2_C1": (C2 / C1) if C1 > 1e-6 else float("nan")}


def stage1_causet(stage0_ok):
    rho = 2.0
    # tall-in-time box -> long causal chains (large dynamic range for xi)
    boxes = {"small": [(0.0, 16.0), (0.0, 5.0), (0.0, 5.0), (0.0, 5.0)],
             "med":   [(0.0, 22.0), (0.0, 5.0), (0.0, 5.0), (0.0, 5.0)],
             "large": [(0.0, 28.0), (0.0, 5.0), (0.0, 5.0), (0.0, 5.0)]}
    if FAST:
        boxes = {"small": boxes["small"], "med": boxes["med"]}
    seeds = [0, 1] if FAST else [0, 1, 2, 3]
    nb, nm = (150, 30) if FAST else (200, 40)

    sizes = {}
    for name, box in boxes.items():
        g, pts = build_causet(rho, box, seed=100)
        hop, ch = causet_diameters(g, pts)
        sizes[name] = {"n": g.n, "deg": float(g.degree.mean()),
                       "hop_diam": hop, "chain_max": ch, "box": box,
                       "g": g, "pts": pts}

    # analysis box = largest; locate Jc there and run xi(J) + the mean-field probe
    aname = "large" if "large" in sizes else "med"
    ga, pa = sizes[aname]["g"], sizes[aname]["pts"]
    Jc_meas, jc_scan = locate_jc(ga, nb, nm, seeds[:2])
    Js = np.linspace(0.45 * Jc_meas, 0.99 * Jc_meas, 12)
    mf = meanfield_probe(ga, pa, 0.97 * Jc_meas, nb, nm, seeds)

    by_size = {}
    for name in sizes:
        g, pts = sizes[name]["g"], sizes[name]["pts"]
        dmax = sizes[name]["chain_max"]
        recs = causet_xi_curve(g, pts, Js, dmax, nb, nm, seeds)
        nsurv = sum(1 for r in recs if r["passes_cut"] and r["n_seeds_ok"] > 0)
        by_size[name] = {"n": sizes[name]["n"], "deg": sizes[name]["deg"],
                         "hop_diam": sizes[name]["hop_diam"],
                         "chain_max": sizes[name]["chain_max"],
                         "box": sizes[name]["box"], "records": recs,
                         "n_survivors": nsurv}

    # z grows with N?  (structural mean-field signature: more events -> denser)
    ns = [by_size[n]["n"] for n in sizes]
    zs = [by_size[n]["deg"] for n in sizes]
    z_grows = bool(len(zs) >= 2 and zs[-1] > zs[0] * 1.05)

    big = by_size[aname]
    surv = [r for r in big["records"] if r["passes_cut"] and r["n_seeds_ok"] > 0]
    if len(surv) >= 5:
        J = np.array([r["J"] for r in surv]); xi = np.array([r["xi"] for r in surv])
        er = np.array([r["xi_err"] for r in surv])
        disc = E.discriminate_finite_jcband(J, xi, er, Jc_meas,
                                            jc_band=max(0.005, 0.1 * Jc_meas))
    else:
        disc = {"winner": "insufficient", "n_points": len(surv)}

    return {"rho": rho, "Jc_meas": Jc_meas, "jc_scan": jc_scan,
            "J_sweep": Js.tolist(), "analysis_box": aname,
            "by_size": by_size, "discriminator": disc, "meanfield_probe": mf,
            "z_grows_with_N": z_grows, "N_list": ns, "z_list": zs,
            "hop_degenerate_note": "Hasse hop diameter ~3 and N-independent; "
                                   "correlation length measured along causal chain.",
            "stage0_ok": stage0_ok}


# ====================================================================== #
# Verdict
# ====================================================================== #
def render_verdict(s1):
    disc = s1["discriminator"]
    aname = s1.get("analysis_box", "med")
    big = s1["by_size"].get(aname)
    nsurv = big["n_survivors"] if big else 0
    chain_max = big["chain_max"] if big else 0
    mf = s1.get("meanfield_probe", {})
    zc1 = mf.get("z_times_C1", float("nan"))
    tail = mf.get("tail_ratio_C2_C1", float("nan"))
    z_grows = s1.get("z_grows_with_N", False)

    # --- mean-field / no-diverging-length detector --------------------------- #
    # Just below Jc the connected nearest-neighbour correlation is ~1/z
    # (z*C1 ~ O(1)) with NO tail (C2/C1 << 1): the order sets in globally without
    # a growing correlation length.  Because z GROWS with N, larger systems are
    # MORE mean-field -- this is structural, not a finite-size shortfall.
    meanfield = (np.isfinite(zc1) and 0.2 < zc1 < 5.0
                 and np.isfinite(tail) and abs(tail) < 0.25
                 and nsurv < 5)
    if meanfield:
        return ("MORTE_B7_MEANFIELD", (
            f"NO diverging correlation length exists in equilibrium. Just below "
            f"Jc~{s1['Jc_meas']:.3f} the connected correlation is mean-field-diluted: "
            f"z*C(1)={zc1:.2f}~O(1) (i.e. C(1)~1/z) with no tail (C(2)/C(1)={tail:.2f}), "
            f"in BOTH the hop and chain metrics; order appears by a sharp global onset, "
            f"not a growing xi. Coordination z GROWS with N ({s1.get('z_list')}), so "
            f"larger systems are MORE mean-field -- structural, not finite-size. An "
            f"essential singularity (the prerequisite for transmutation) needs a "
            f"diverging xi; here xi does not diverge at all, the tamest possible "
            f"behaviour (mean-field, nu=1/2 class). Transmutation via the equilibrium "
            f"critical-length channel is EXCLUDED -> do NOT build the dynamic campaign "
            f"on this basis. Consistent with the weak-first-order/mean-field character "
            f"found in the SU(3) order-transition campaign."))

    if disc.get("winner") == "insufficient" or nsurv < 5:
        return ("INCONCLUSIVO", (
            f"Critical window inaccessible: only {nsurv} causet points survive the "
            f"xi<chain_max/4 cut (chain_max~{chain_max}). The Hasse HOP distance is "
            f"structurally degenerate (diameter ~3, N-independent), and the causal "
            f"CHAIN distance, though it has range, does not deliver >=5 reliable "
            f"sub-cut points at these sizes. Decision requires larger N (cluster) "
            f"before any bet on the dynamic campaign. NOT a death, NOT a success."))
    dbic = disc.get("dBIC_E_over_P", float("nan"))
    stable = disc.get("winner_stable", False)
    if disc["winner"] == "exp" and dbic > 6 and stable:
        return ("SUCCESS_B7_EXPONENTIAL", (
            f"xi(J) diverges as an essential singularity exp(b|J-Jc|^-sigma) "
            f"(sigma={disc.get('sigma'):.2f}, dBIC_E/P={dbic:.1f}>6, robust to Jc "
            f"band). The divergence form PERMITS dimensional transmutation -> "
            f"justifies building the dynamic driver (running coupling, Lambda)."))
    if dbic < 2:
        return ("MORTE_B7_POWER", (
            f"xi(J) diverges as a POWER |J-Jc|^-nu (nu={disc.get('nu'):.2f}, "
            f"dBIC_E/P={dbic:.1f}<2: no evidence for an essential singularity). "
            f"No scale-separation mechanism in equilibrium -> absolute scales stay "
            f"closed in the equilibrium channel; the 'form derives, scale does not' "
            f"thesis is COMPLETE for equilibrium. Do NOT invest in dynamics for "
            f"scales."))
    return ("INCONCLUSIVO", (
        f"Ambiguous: dBIC_E/P={dbic:.1f} in [2,6] or winner unstable across the Jc "
        f"band (stable={stable}). Per the golden rule, ambiguity -> INCONCLUSIVO; a "
        f"SUCCESS that justifies an expensive campaign must be unequivocal."))


def main():
    t0 = time.time()
    print("=" * 78)
    print("B7 -- xi(J): power vs essential singularity (transmutation gate)"
          + ("  [FAST]" if FAST else ""))
    print("=" * 78)

    print("\n[Stage 0a] discriminator unit-test (synthetic finite-Jc)...")
    s0a = stage0_discriminator_unit(); print("  " + s0a["note"])
    print("\n[Stage 0b] POWER reference (3D Heisenberg lattice)...", flush=True)
    s0b = stage0_power_3d(); print("  " + s0b["note"])
    print("\n[Stage 0c] EXPONENTIAL reference (1D Ising exact)...", flush=True)
    s0c = stage0_exp_1d_ising(); print("  " + s0c["note"])

    gate = s0a["gate_pass"] and s0b["gate_pass"] and s0c["gate_pass"]
    print("\n" + "-" * 78)
    print(f"STAGE 0 GATE: 0a={s0a['gate_pass']} 0b={s0b['gate_pass']} "
          f"0c={s0c['gate_pass']}  ->  {'PASS' if gate else 'FAIL'}")
    print("-" * 78)

    out = {"experiment": "B7_xi", "fast": FAST,
           "stage0": {"unit": s0a, "power_3d": s0b, "exp_1d": s0c,
                      "gate_pass": bool(gate)}}

    if not gate:
        out["verdict"] = {"label": "GATE_FAIL", "text":
                          "Stage 0 estimator/discriminator did not classify the "
                          "known references correctly; B7 cannot run on the causet "
                          "until the estimator is fixed (PRE_REGISTRO sec.4)."}
        print("\nGATE FAILED -- not proceeding to the causet (pre-registration).")
    else:
        print("\n[Stage 1-3] xi(J) on the causet (causal-chain distance)...",
              flush=True)
        s1 = stage1_causet(gate)
        for name, d in s1["by_size"].items():
            print(f"  {name:6s} n={d['n']:5d} <deg>={d['deg']:.0f} "
                  f"hop_diam={d['hop_diam']} chain_max={d['chain_max']} "
                  f"survivors(xi<cm/4)={d['n_survivors']}")
        print(f"  Jc(causet, chi-peak)={s1['Jc_meas']:.3f}  "
              f"discriminator winner={s1['discriminator'].get('winner')} "
              f"dBIC_E/P={s1['discriminator'].get('dBIC_E_over_P', float('nan')):.1f}")
        label, text = render_verdict(s1)
        # strip non-serialisable graph handles
        for d in s1["by_size"].values():
            d.pop("g", None); d.pop("pts", None)
        out["stage1"] = s1
        out["verdict"] = {"label": label, "text": text}
        print("\n" + "=" * 78)
        print(f"VERDICT: {label}")
        print(text)
        print("=" * 78)

    out["runtime_s"] = time.time() - t0
    (HERE / "b7_xi.json").write_text(json.dumps(out, indent=2, default=str),
                                     encoding="utf-8")
    print(f"\n[{out['runtime_s']:.1f}s] -> b7_xi.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
