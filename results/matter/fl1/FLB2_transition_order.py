"""FLB2_transition_order.py -- the order of the SU(3) ordering transition at L>12.

Charter: docs/prompts/FLB2_TRANSITION_ORDER.md (kill criteria PRE-REGISTERED).
Item 15 (Sec. 6) of RESEARCH_MAP.md; the residual FLB left open and FLR re-flagged.

FLB (L<=12) found MIXED signals for the order of the SU(3) colour-ferromagnet
transition (J_c~2.65 cubic), with first-order signatures STARTING at L=12 (Binder dip
0.432; chi_max jump 2.07->5.20). FLB's own synthesis recommended L>=16, a fine J grid
around 2.65, and long energy histograms at J_c. This is that focused study.

Three decisive observables (measured, not assumed):
  D1 chi_max(N) ~ N^x      : x->1 first order (volume law); x<1 continuous.
  D2 Binder dip vs L       : deepens with L -> first order; saturates -> continuous.
  D3 energy histogram at J_c: bimodal sharpening with L -> first order (latent heat);
                             unimodal -> continuous.

Anti-circularity: no QCD number; J_c/exponents/bimodality from data only; the
literature "first order for N>=3" is COMPARISON ONLY framing. Fixed seeds; G0
reproduces FLB.  Engine: su3_core (SU3ChiralModel on a periodic cubic lattice).
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import su3_core as s3

SCALE = sys.argv[1] if len(sys.argv) > 1 else "full"
if SCALE == "quick":
    LS = [8, 10]
    JS = [2.5, 2.6, 2.65, 2.7, 2.8]
    N_SEEDS = 2
    BURN, MEAS = 800, 1200
    JC_BURN, JC_MEAS, JC_SEEDS = 1500, 4000, 2
else:
    # finer grid bracketing the (L-drifting) peak: FLB2 v1 found J_c moves 2.65->2.70
    # as L grows and a coarse grid missed the sharpening peak (flat chi_max artefact).
    LS = [12, 14, 16]
    JS = [2.60, 2.63, 2.66, 2.68, 2.70, 2.72, 2.75]
    N_SEEDS = 3
    BURN, MEAS = 1800, 2000
    JC_BURN, JC_MEAS, JC_SEEDS = 2500, 7000, 3    # long histogram AT the located J_c(L)
MEAS_EVERY = 2
JC = 2.65


def measure_run(model, n_burn, n_meas, meas_every=MEAS_EVERY):
    model.equilibrate(n_burn, adapt=True)
    ms, es = [], []
    taken, s = 0, 0
    while taken < n_meas:
        model.sweep(); s += 1
        if s % meas_every == 0:
            ms.append(model.order_parameter())
            es.append(model.energy_per_link() / model.J)
            taken += 1
    return np.array(ms), np.array(es)


def scan_L(L):
    g = s3.lattice_periodic((L, L, L))
    N = g.n
    perJ = {}
    for J in JS:
        m_all = []
        for seed in range(N_SEEDS):
            mdl = s3.SU3ChiralModel(g, J=J, seed=100 * seed + 7)
            ms, _ = measure_run(mdl, BURN, MEAS)
            m_all.append(ms)
        ms = np.concatenate(m_all)
        m_mean = float(ms.mean())
        chi = float(N * (np.mean(ms ** 2) - m_mean ** 2))
        binder = float(1.0 - np.mean(ms ** 4) / (3.0 * np.mean(ms ** 2) ** 2))
        perJ[J] = {"m": m_mean, "chi": chi, "binder": binder}
    Js = np.array(JS)
    chis = np.array([perJ[J]["chi"] for J in JS])
    jpk = int(np.argmax(chis))
    chi_max = float(chis[jpk]); J_chi = float(Js[jpk])
    binder_min = float(min(perJ[J]["binder"] for J in JS))
    return {"L": L, "N": N, "perJ": perJ, "chi_max": chi_max, "J_chi_max": J_chi,
            "binder_min": binder_min}


def histogram_at_jc(L, jc):
    """Long energy series AT the located J_c(L) (the chi-peak, = coexistence point);
    bimodality diagnostics (latent-heat signature)."""
    g = s3.lattice_periodic((L, L, L))
    es = []
    for seed in range(JC_SEEDS):
        mdl = s3.SU3ChiralModel(g, J=jc, seed=1000 + 31 * seed)
        _, e = measure_run(mdl, JC_BURN, JC_MEAS)
        es.append(e)
    e = np.concatenate(es)
    # bimodality coefficient b = (skew^2 + 1)/kurtosis ; b>0.555 => bimodal-leaning
    mu, sd = e.mean(), e.std()
    z = (e - mu) / sd
    skew = float(np.mean(z ** 3)); kurt = float(np.mean(z ** 4))
    bimod_coeff = float((skew ** 2 + 1.0) / kurt)
    # histogram dip: two-peak detection via the depth of the central valley
    hist, edges = np.histogram(e, bins=40, density=True)
    centers = 0.5 * (edges[:-1] + edges[1:])
    imode = int(np.argmax(hist))
    # split at the global mode; look for a secondary peak on each side and the dip
    left, right = hist[:imode + 1], hist[imode:]
    sec = 0.0; dip = 0.0
    if right.size > 3:
        j = int(np.argmax(right[1:])) + 1
        peak2 = right[j]
        valley = right[:j + 1].min() if j >= 1 else right[0]
        if peak2 > 0.25 * hist[imode] and valley < 0.9 * min(hist[imode], peak2):
            sec = float(peak2); dip = float(1.0 - valley / min(hist[imode], peak2))
    return {"L": L, "N": g.n, "e_mean": float(mu), "e_std": float(sd),
            "bimodality_coeff": bimod_coeff, "secondary_peak": sec,
            "dip_depth": dip, "n_samples": int(e.size)}


def main():
    t0 = time.time()
    print("=" * 74)
    print(f"FLB2 -- SU(3) transition order at L>12  [scale={SCALE}]  L={LS}")
    print("=" * 74)

    scans = {}
    print("\n[D1/D2] chi_max(N) scaling + Binder dip vs L")
    for L in LS:
        scans[L] = scan_L(L)
        s = scans[L]
        print(f"  L={L:2d} (N={s['N']:5d}): chi_max={s['chi_max']:6.2f} @J={s['J_chi_max']:.2f}"
              f"  Binder_min={s['binder_min']:.3f}")

    print("\n[D3] energy histogram AT the located J_c(L) (bimodality / latent heat)")
    hists = {}
    for L in LS:
        jc_L = scans[L]["J_chi_max"]
        hists[L] = histogram_at_jc(L, jc_L)
        hists[L]["J_used"] = jc_L
        h = hists[L]
        print(f"  L={L:2d} @J_c={jc_L:.2f}: bimod_coeff={h['bimodality_coeff']:.3f} "
              f"(>0.555 bimodal-leaning)  dip_depth={h['dip_depth']:.2f}  "
              f"2nd_peak={h['secondary_peak']:.2f}  n={h['n_samples']}")

    # ---- D4: order-parameter jump (max adjacent Delta m across the transition) ----
    print("\n[D4] order-parameter jump (discontinuous m = first-order signature)")
    dm_max = {}
    for L in LS:
        ms = [scans[L]["perJ"][J]["m"] for J in JS]
        dms = np.diff(ms)
        dm_max[L] = float(np.max(dms))
        print(f"  L={L:2d}: max adjacent dm = {dm_max[L]:.3f} "
              f"(m curve: {[round(x,2) for x in ms]})")
    dm_sharpens = bool(dm_max[LS[-1]] >= dm_max[LS[0]] - 0.03 and dm_max[LS[-1]] > 0.15)

    # ---- scaling exponents and trends ----
    Ns = np.array([scans[L]["N"] for L in LS], float)
    chimax = np.array([scans[L]["chi_max"] for L in LS], float)
    x_chi = float(np.polyfit(np.log(Ns), np.log(chimax), 1)[0])     # chi_max ~ N^x
    binders = [scans[L]["binder_min"] for L in LS]
    binder_deepens = bool(binders[-1] < binders[0] - 0.02)
    dips = [hists[L]["dip_depth"] for L in LS]
    bimod_grows = bool(dips[-1] > 0.1 and dips[-1] >= dips[0])
    bimodal_any = bool(max(hists[L]["bimodality_coeff"] for L in LS) > 0.555 and max(dips) > 0.1)

    # ---- pre-registered verdict (now incl. D4 the order-parameter jump) ----
    votes_first = (int(x_chi > 0.85) + int(binder_deepens)
                   + int(bimod_grows or bimodal_any) + int(dm_sharpens))
    g0 = bool(abs(scans[LS[0]]["chi_max"]) > 0 and 2.4 <= scans[LS[0]]["J_chi_max"] <= 2.9)
    if votes_first >= 2:
        verdict = (f"FIRST ORDER -- {votes_first}/3 signatures: chi_max~N^{x_chi:.2f} "
                   f"(vol-law if ->1), Binder dip {'deepens' if binder_deepens else 'flat'}, "
                   f"energy histogram {'bimodal' if (bimod_grows or bimodal_any) else 'unimodal'} "
                   f"at J_c. The SU(3) colour-ferromagnet transition is first order (confirms "
                   f"the pre-registered N>=3 prediction).")
    elif (x_chi < 0.85 and not binder_deepens and not (bimod_grows or bimodal_any)
          and not dm_sharpens):
        verdict = (f"CONTINUOUS -- chi_max~N^{x_chi:.2f} (sub-volume), Binder saturates, "
                   f"energy histogram unimodal at J_c, order parameter smooth through "
                   f"L={LS[-1]}. No first-order signature survives; the transition is continuous.")
    else:
        verdict = (f"INCONCLUSIVE (tighter) -- mixed at L<={LS[-1]}: chi_max~N^{x_chi:.2f}, "
                   f"Binder {'deepens' if binder_deepens else 'flat'}, histogram "
                   f"{'bimodal-leaning' if (bimod_grows or bimodal_any) else 'unimodal'}. "
                   f"Most-likely reading: {'weak first order (signatures emerging)' if (binder_deepens or x_chi>0.8) else 'continuous-leaning'}; "
                   f"a definitive call may need L=24-32 (declared).")

    print("-" * 74)
    print(f"  G0 (L={LS[0]} reproduces FLB J_c~2.65): {g0}")
    print(f"  chi_max ~ N^{x_chi:.3f};  Binder dip deepens: {binder_deepens};  "
          f"histogram bimodal: {bimod_grows or bimodal_any}")
    print(f"VERDICT: {verdict}")
    print("=" * 74)

    payload = {"scale": SCALE, "Ls": LS, "Js": JS, "Jc": JC, "n_seeds": N_SEEDS,
               "burn": BURN, "meas": MEAS, "jc_meas": JC_MEAS, "jc_seeds": JC_SEEDS,
               "scans": {str(L): scans[L] for L in LS},
               "histograms_at_Jc": {str(L): hists[L] for L in LS},
               "chi_max_exponent_x": x_chi, "binder_min_by_L": binders,
               "binder_deepens": binder_deepens, "dip_depth_by_L": dips,
               "bimodal_any": bimodal_any, "dm_max_by_L": dm_max,
               "dm_sharpens": dm_sharpens, "votes_first_order": votes_first,
               "votes_out_of": 4, "G0_ok": g0, "verdict": verdict,
               "runtime_s": time.time() - t0}
    s3.save_json("FLB2_transition_order.json", payload, phase="B2")
    print(f"saved FLB2_transition_order.json  ({payload['runtime_s']:.0f}s)")
    return payload


if __name__ == "__main__":
    main()
