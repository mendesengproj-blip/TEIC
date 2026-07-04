"""OT_transition_order.py -- order of the SU(3) colour-ferromagnet transition at L>12.

CAMPANHA_SU3_ORDEM_TRANSICAO. Pre-registration frozen in PRE_REGISTRO.md (this dir)
and committed BEFORE this script was run. Direct successor of FLB2 (L<=16); this
pushes to L=20 (and conditionally L=24) with a clean Binder-CROSSING method.

Three pre-registered observables (kill-criteria in PRE_REGISTRO.md):
  OT1  Binder U4(J,L) crossings -> J_c(L); converge (2nd order) vs diverge (1st).
  OT2  chi_max(L) ~ L^x; x<2 continuous, x->3 (volume, 3D) first order.
  OT3  hysteresis (J up/down) at L=16,20 -- feeds the frozen L=24 decision.
Plus the decisive latent-heat signature (FLB2): energy histogram bimodality at the
located J_c(L) for L>=16.

Phases (mergeable -- always loads/updates OT_transition_order.json):
  primary : LS=[8,12,16,20] scan + histograms[16,20]   (the registered run)
  hyst    : hysteresis L=16,20                          (feeds L=24 decision)
  L24     : LS=[24] scan + histogram[24]                (only if frozen rule fires)
  quick   : smoke test (NON-registered tiny stats)

Engine: su3_core (cubic periodic lattice), imported UNMODIFIED. Analysis here is
pure real arithmetic (no complex literals) -> anti-circularity guard stays clean.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

_trapz = np.trapezoid if hasattr(np, "trapezoid") else np.trapz   # np.trapz gone in NumPy 2.0

HERE = Path(__file__).resolve().parent
FL1 = HERE.parents[2] / "results" / "matter" / "fl1"   # docs/campaigns/SU3.. -> TEIC
sys.path.insert(0, str(FL1))
import su3_core as s3  # noqa: E402

PHASE = sys.argv[1] if len(sys.argv) > 1 else "primary"
OUT = HERE / "OT_transition_order.json"

# ---- FROZEN parameters (PRE_REGISTRO.md, amended-pre-result) ----
if PHASE == "quick":
    JGRID = np.round(np.arange(2.60, 2.761, 0.04), 4).tolist()
    N_SEEDS, BURN, MEAS = 2, 150, 400
    H_BURN, H_MEAS, H_SEEDS = 300, 800, 2
else:
    JGRID = np.round(np.arange(2.60, 2.761, 0.01), 4).tolist()   # 2.60..2.76, dJ=0.01
    N_SEEDS, BURN, MEAS = 5, 500, 2000
    H_BURN, H_MEAS, H_SEEDS = 1500, 4000, 3

SEEDS = [1000 * s + 7 for s in range(N_SEEDS)]
H_SEED_LIST = [2000 + 31 * s for s in range(H_SEEDS)]


def load():
    if OUT.exists():
        return json.loads(OUT.read_text(encoding="utf-8"))
    return {"Jgrid": JGRID, "seeds": SEEDS, "burn": BURN, "meas": MEAS,
            "scans": {}, "histograms": {}, "hysteresis": {}}


def save(payload):
    payload["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def measure_m_e(model, n_burn, n_meas):
    model.equilibrate(n_burn, adapt=True)
    ms = np.empty(n_meas)
    es = np.empty(n_meas)
    for k in range(n_meas):
        model.sweep()
        ms[k] = model.order_parameter()
        es[k] = model.energy_per_link() / model.J
    return ms, es


def scan_L(L):
    g = s3.lattice_periodic((L, L, L))
    N = g.n
    perJ = {}
    for J in JGRID:
        m_all = []
        for sd in SEEDS:
            mdl = s3.SU3ChiralModel(g, J=J, seed=sd)
            ms, _ = measure_m_e(mdl, BURN, MEAS)
            m_all.append(ms)
        m = np.concatenate(m_all)
        m1, m2, m4 = float(m.mean()), float(np.mean(m ** 2)), float(np.mean(m ** 4))
        perJ[f"{J:.4f}"] = {"m": m1, "chi": float(N * (m2 - m1 ** 2)),
                            "U4": float(1.0 - m4 / (3.0 * m2 ** 2)), "m2": m2, "m4": m4}
    chis = np.array([perJ[f"{J:.4f}"]["chi"] for J in JGRID])
    ipk = int(np.argmax(chis))
    return {"L": L, "N": N, "perJ": perJ,
            "chi_max": float(chis[ipk]), "J_chi_max": float(JGRID[ipk])}


def histogram_at_jc(L, jc):
    g = s3.lattice_periodic((L, L, L))
    es = []
    for sd in H_SEED_LIST:
        mdl = s3.SU3ChiralModel(g, J=jc, seed=sd)
        _, e = measure_m_e(mdl, H_BURN, H_MEAS)
        es.append(e)
    e = np.concatenate(es)
    mu, sd_ = float(e.mean()), float(e.std())
    z = (e - mu) / sd_
    skew, kurt = float(np.mean(z ** 3)), float(np.mean(z ** 4))
    bimod = float((skew ** 2 + 1.0) / kurt)
    hist, _ = np.histogram(e, bins=40, density=True)
    imode = int(np.argmax(hist))
    right = hist[imode:]
    dip = 0.0
    if right.size > 3:
        j = int(np.argmax(right[1:])) + 1
        peak2, valley = right[j], right[:j + 1].min()
        if peak2 > 0.25 * hist[imode] and valley < 0.9 * min(hist[imode], peak2):
            dip = float(1.0 - valley / min(hist[imode], peak2))
    return {"L": L, "J_used": float(jc), "e_mean": mu, "e_std": sd_,
            "bimodality_coeff": bimod, "dip_depth": dip, "n_samples": int(e.size)}


def hysteresis(L):
    """One slow J cycle up then down on a single trajectory; normalised loop area."""
    g = s3.lattice_periodic((L, L, L))
    up = np.array(JGRID)
    mdl = s3.SU3ChiralModel(g, J=float(up[0]), seed=20260622)
    m_up = []
    for J in up:
        mdl.J = float(J)
        ms, _ = measure_m_e(mdl, 200, 400)
        m_up.append(float(ms.mean()))
    m_dn = []
    for J in up[::-1]:
        mdl.J = float(J)
        ms, _ = measure_m_e(mdl, 200, 400)
        m_dn.append(float(ms.mean()))
    m_up = np.array(m_up)
    m_dn = np.array(m_dn)[::-1]
    area = float(_trapz(np.abs(m_up - m_dn), up))
    amp = float(max(m_up.max(), m_dn.max()) - min(m_up.min(), m_dn.min()))
    norm = float(area / (amp * (up[-1] - up[0]))) if amp > 0 else 0.0
    return {"L": L, "loop_area": area, "amplitude": amp, "norm_hysteresis": norm,
            "m_up": m_up.tolist(), "m_down": m_dn.tolist()}


def binder_crossings(scans, Ls):
    Js = np.array(JGRID)
    out = []
    for La, Lb in zip(Ls[:-1], Ls[1:]):
        ua = np.array([scans[str(La)]["perJ"][f"{J:.4f}"]["U4"] for J in JGRID])
        ub = np.array([scans[str(Lb)]["perJ"][f"{J:.4f}"]["U4"] for J in JGRID])
        d = ua - ub
        sign = np.sign(d)
        cross = None
        for i in range(len(d) - 1):
            if sign[i] == 0:
                cross = float(Js[i]); break
            if sign[i] * sign[i + 1] < 0:
                t = d[i] / (d[i] - d[i + 1])
                cross = float(Js[i] + t * (Js[i + 1] - Js[i])); break
        out.append({"L_pair": [La, Lb], "J_cross": cross})
    return out


def compute_readout(payload):
    scans = payload["scans"]
    Ls = sorted(int(k) for k in scans)
    if len(Ls) < 2:
        return
    cr = binder_crossings(scans, Ls)
    valid = [c["J_cross"] for c in cr if c["J_cross"] is not None]
    spread = (max(valid) - min(valid)) if len(valid) >= 2 else None
    Lsd = np.array(Ls, float)
    cm = np.array([scans[str(x)]["chi_max"] for x in Ls], float)
    x = float(np.polyfit(np.log(Lsd), np.log(cm), 1)[0])
    jc_by_L = {str(x_): scans[str(x_)]["J_chi_max"] for x_ in Ls}

    hists = payload.get("histograms", {})
    bimod_any = any(hists[k]["bimodality_coeff"] > 0.555 and hists[k]["dip_depth"] > 0.1
                    for k in hists)

    # OT1 / OT2 verdicts
    if spread is not None and spread < 0.01:
        ot1 = "2nd"
    elif spread is not None and spread > 0.02:
        ot1 = "1st"
    else:
        ot1 = "inconclusive"
    ot2 = "2nd" if x < 2.0 else ("1st" if x > 2.5 else "inconclusive")

    # frozen L=24 decision rule (uses only L<=20 indicators)
    jc16 = jc_by_L.get("16")
    jc20 = jc_by_L.get("20")
    binder_drift = (abs(jc20 - jc16) if (jc16 is not None and jc20 is not None) else None)
    hyst20 = payload.get("hysteresis", {}).get("20", {}).get("norm_hysteresis")
    reasons = []
    if binder_drift is not None and binder_drift > 0.01:
        reasons.append(f"|J_c(20)-J_c(16)|={binder_drift:.3f}>0.01 (U4 not converged)")
    if 2.0 < x < 3.5:
        reasons.append(f"chi exponent x={x:.2f} in (2.0,3.5) inconclusive")
    if hyst20 is not None and 0.05 < hyst20 < 0.15:
        reasons.append(f"hysteresis@L20={hyst20:.2f} in (0.05,0.15)")
    concordant = (ot1 == ot2 and ot1 in ("1st", "2nd")
                  and not (2.0 < x < 3.5)
                  and (binder_drift is None or binder_drift <= 0.01))
    run_L24 = (not concordant) or bool(reasons)

    payload["readout"] = {
        "Ls": Ls, "binder_crossings": valid, "binder_cross_spread": spread,
        "binder_drift_16_20": binder_drift, "chi_max_exponent_x": x,
        "chi_max_by_L": {str(x_): scans[str(x_)]["chi_max"] for x_ in Ls},
        "J_chi_max_by_L": jc_by_L, "latent_heat_bimodal": bool(bimod_any),
        "hysteresis_norm_by_L": {k: v.get("norm_hysteresis")
                                 for k, v in payload.get("hysteresis", {}).items()},
        "OT1_binder": ot1, "OT2_chi": ot2,
        "concordant_at_L20": bool(concordant), "run_L24": bool(run_L24),
        "L24_trigger_reasons": reasons,
    }


def main():
    t0 = time.time()
    payload = load()
    payload.update({"Jgrid": JGRID, "seeds": SEEDS, "burn": BURN, "meas": MEAS})
    print("=" * 74)
    print(f"OT -- SU(3) transition order  [phase={PHASE}]  J={JGRID[0]}..{JGRID[-1]} "
          f"({len(JGRID)} pts)  seeds={SEEDS}")
    print("=" * 74)

    if PHASE in ("primary", "quick"):
        LS = [8, 12] if PHASE == "quick" else [8, 12, 16, 20]
        H_LS = [12] if PHASE == "quick" else [16, 20]
        for L in LS:
            tl = time.time()
            payload["scans"][str(L)] = scan_L(L)
            s = payload["scans"][str(L)]
            print(f"[OT1/2] L={L:2d} N={s['N']:5d}: chi_max={s['chi_max']:6.2f} "
                  f"@J={s['J_chi_max']:.3f}  ({time.time()-tl:.0f}s)")
            compute_readout(payload)
            save(payload)
        for L in H_LS:
            th = time.time()
            payload["histograms"][str(L)] = histogram_at_jc(L, payload["scans"][str(L)]["J_chi_max"])
            h = payload["histograms"][str(L)]
            print(f"[Hist] L={L:2d} @J_c={h['J_used']:.3f}: bimod={h['bimodality_coeff']:.3f} "
                  f"dip={h['dip_depth']:.2f}  ({time.time()-th:.0f}s)")
            compute_readout(payload)
            save(payload)

    elif PHASE == "hyst":
        for L in [16, 20]:
            th = time.time()
            payload["hysteresis"][str(L)] = hysteresis(L)
            hh = payload["hysteresis"][str(L)]
            print(f"[OT3] L={L:2d}: norm_hysteresis={hh['norm_hysteresis']:.3f} "
                  f"(>0.15 1st / <0.05 2nd)  ({time.time()-th:.0f}s)")
            compute_readout(payload)
            save(payload)

    elif PHASE == "L24":
        tl = time.time()
        payload["scans"]["24"] = scan_L(24)
        s = payload["scans"]["24"]
        print(f"[OT1/2] L=24 N={s['N']:5d}: chi_max={s['chi_max']:6.2f} @J={s['J_chi_max']:.3f}"
              f"  ({time.time()-tl:.0f}s)")
        compute_readout(payload)
        save(payload)
        th = time.time()
        payload["histograms"]["24"] = histogram_at_jc(24, s["J_chi_max"])
        print(f"[Hist] L=24: bimod={payload['histograms']['24']['bimodality_coeff']:.3f} "
              f"dip={payload['histograms']['24']['dip_depth']:.2f}  ({time.time()-th:.0f}s)")
        compute_readout(payload)
        save(payload)

    compute_readout(payload)
    payload["runtime_s_last_phase"] = time.time() - t0
    save(payload)

    r = payload.get("readout", {})
    print("-" * 74)
    print(f"  OT1 Binder: {r.get('OT1_binder')}  (crossings {r.get('binder_crossings')}, "
          f"spread {r.get('binder_cross_spread')})")
    print(f"  OT2 chi_max ~ L^{r.get('chi_max_exponent_x')}  -> {r.get('OT2_chi')}")
    print(f"  latent-heat bimodal: {r.get('latent_heat_bimodal')}")
    print(f"  concordant@L20: {r.get('concordant_at_L20')}   RUN_L24: {r.get('run_L24')}")
    if r.get("L24_trigger_reasons"):
        print(f"  L24 triggers: {r['L24_trigger_reasons']}")
    print(f"saved {OUT.name}  ({payload['runtime_s_last_phase']:.0f}s this phase)")
    print("=" * 74)
    return payload


if __name__ == "__main__":
    main()
