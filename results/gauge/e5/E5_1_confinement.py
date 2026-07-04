"""E5_1_confinement.py -- first U(1) gauge measurement on the causal set.

Pre-registered in E5_PHOTON_LINK_SECTOR.md (E5-1). Uses the VALIDATED fast engine
(e5_fast, checked vs the slow engine and against the known 4D U(1) transition via
the E5-V / E5V_fss2 gates: G1 gauge-invariance, G2 beta_c~1.01, G3 4D-grows /
3D-flat). Builds the U(1) gauge field on the causal Hasse graph with height-2
causal-diamond plaquettes and asks, by the same average-plaquette / specific-heat
machinery the gate validated:

  Does the causal-set U(1) show a DECONFINEMENT-like transition (specific-heat peak
  that grows with system size, as in 4D -> a deconfined/Coulomb phase could host a
  photon), or only a smooth CROSSOVER (flat with size, as in 3D -> confines at all
  beta -> no massless photon in the link sector either)?

This is the natural first cut; the definitive Wilson-loop area-law and the photon
dispersion (E5-2) are separate and not claimed here. Step 0 re-validates gauge
invariance on the DIAMOND plaquettes specifically (the causal construction).
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ORI))
from e5_core import causal_diamond_plaquettes   # noqa: E402
from e5_fast import FastU1Gauge                  # noqa: E402
from orientation_core import causal_link_graph   # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box             # noqa: E402


def gauge_invariance_diamonds(g, plaq_links, plaq_signs, seed=0):
    """Apply a per-node gauge transform theta_(a,b) += lam[b]-lam[a] (edge a<b) and
    check the diamond plaquette holonomies are invariant -> the loops are closed."""
    edges = g.edges
    L = edges.shape[0]
    rng = np.random.default_rng(seed)
    theta = rng.uniform(-np.pi, np.pi, L)
    hol0 = (plaq_signs * theta[plaq_links]).sum(axis=1)
    lam = rng.uniform(-np.pi, np.pi, g.n)
    theta2 = theta + (lam[edges[:, 1]] - lam[edges[:, 0]])
    hol1 = (plaq_signs * theta2[plaq_links]).sum(axis=1)
    return float(np.max(np.abs(np.cos(hol1) - np.cos(hol0))))


def scan(g, plaq_links, plaq_signs, betas, n_seeds=3, n_burn=200, n_meas=120):
    L = g.edges.shape[0]
    Nplaq = plaq_links.shape[0]
    meanP = np.zeros(len(betas)); Cpp = np.zeros(len(betas))
    for ib, beta in enumerate(betas):
        mc = []
        for s in range(n_seeds):
            gg = FastU1Gauge(L, plaq_links, plaq_signs, beta=beta, seed=1000 * ib + s)
            gg.equilibrate(n_burn)
            mc.append(gg.measure_plaq(n_meas))
        mc = np.concatenate(mc)
        meanP[ib] = mc.mean()
        Cpp[ib] = beta ** 2 * Nplaq * mc.var()
    return meanP, Cpp, Nplaq


def build(L_box, rho=0.5, seed=0):
    rng = np.random.default_rng(seed)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    Lk, pl, ps = causal_diamond_plaquettes(g, max_per_pair=2, seed=seed)
    return g, pl, ps


def main():
    t0 = time.time()
    betas = np.array([0.3, 0.6, 0.9, 1.1, 1.3, 1.6, 2.0, 2.6])

    out = {"betas": betas.tolist(), "sizes": []}
    # step 0: gauge invariance on diamonds (engineering gate for the causal plaquettes)
    g0, pl0, ps0 = build(4.6, seed=0)
    gi = gauge_invariance_diamonds(g0, pl0, ps0)
    out["gauge_invariance_max_dcos"] = gi
    print(f"step 0 -- diamond gauge invariance: max|dcos|={gi:.1e} "
          f"-> {'OK' if gi < 1e-10 else 'FAIL'}  (n={g0.n}, plaq={pl0.shape[0]})",
          flush=True)

    # step 1: average plaquette + specific heat vs beta, two causal-set sizes
    Cpp_peaks = []
    for Lb in [4.6, 5.6]:
        g, pl, ps = build(Lb, seed=1)
        meanP, Cpp, Nplaq = scan(g, pl, ps, betas)
        jpk = int(np.argmax(Cpp))
        Cpp_peaks.append((Nplaq, float(Cpp[jpk]), float(betas[jpk])))
        out["sizes"].append({"L_box": Lb, "n_events": g.n, "n_plaq": int(Nplaq),
                             "mean_plaq": meanP.tolist(), "C_per_plaq": Cpp.tolist(),
                             "peak_beta": float(betas[jpk]),
                             "C_per_plaq_peak": float(Cpp[jpk])})
        print(f"L={Lb}: n={g.n} plaq={Nplaq}  <cos> {meanP.min():.2f}->{meanP.max():.2f}  "
              f"C/N_plaq peak={Cpp[jpk]:.3e} at beta={betas[jpk]:.1f}", flush=True)

    # verdict: does the specific-heat peak GROW with size (transition/deconfinement)
    # or stay flat (crossover/confinement)?
    (Np_s, C_s, _), (Np_l, C_l, _) = Cpp_peaks
    growth = C_l / C_s
    nplaq_ratio = Np_l / Np_s
    # C/N_plaq = beta^2 N_plaq Var(mc): a first-order transition grows ~ N_plaq
    # (exponent ~1 in ln C/N_plaq vs ln N_plaq); a crossover is ~flat (exponent ~0).
    # CONFOUND: the diamond plaquette count is not controlled across sizes (here it
    # grew x{nplaq_ratio:.1f} while events grew much less), so this 2-point exponent
    # is only a weak indicator and must be confirmed with controlled geometry.
    expo = np.log(growth) / np.log(nplaq_ratio) if nplaq_ratio > 1 else float("nan")
    if expo > 0.8:
        verdict = (f"DECONFINEMENT-LEANING (exploratory): C/N_plaq scales ~N_plaq^"
                   f"{expo:.2f} (first-order-like ~1). Needs controlled geometry + "
                   f"more sizes + Wilson-loop area law before any photon claim.")
        tag = "DECONFINEMENT_LEANING"
    elif expo < 0.25:
        verdict = (f"CONFINING-LEANING (exploratory): C/N_plaq ~flat (exponent "
                   f"{expo:.2f}, crossover-like ~0) -> link sector confines, no photon.")
        tag = "CONFINING_LEANING"
    else:
        verdict = (f"INCONCLUSIVE (exploratory): C/N_plaq scales ~N_plaq^{expo:.2f}, "
                   f"between crossover (0) and first-order (1); with only 2 sizes AND "
                   f"an uncontrolled plaquette count (x{nplaq_ratio:.1f}), this neither "
                   f"establishes nor excludes a deconfined phase. The diamond geometry "
                   f"must be controlled and more sizes run before any verdict.")
        tag = "INCONCLUSIVE"
    out["peak_growth_ratio"] = growth
    out["nplaq_ratio"] = float(nplaq_ratio)
    out["C_per_plaq_scaling_exponent"] = float(expo)
    out["verdict"] = verdict; out["verdict_tag"] = tag
    out["runtime_s"] = time.time() - t0
    (HERE / "E5_1_confinement.json").write_text(json.dumps(out, indent=2))
    print("\nVERDICT:", verdict)
    print(f"runtime {out['runtime_s']:.0f}s -> E5_1_confinement.json")


if __name__ == "__main__":
    main()
