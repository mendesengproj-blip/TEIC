"""bd_summed_action.py -- the SUMMED-action BD estimator (beats the rho^3/4 variance).

e10 documents that pointwise <B phi> is buried under O(rho^3/4) variance and that
Benincasa-Dowker validate the operator via the GLOBALLY SUMMED action, where the
zero-mean pointwise noise cancels as 1/sqrt(N).  This implements that for the two
Lorentz tests, summing over many bulk events with error bars across realisations.
Sharp (1,-2,1) vs smeared compared throughout.

Single pass: for each base event we compute its past P, interval counts m, smeared
weight w and edge vectors e ONCE, then evaluate every probe field and the second
moment from that cache (the earlier version recomputed the O(|P|^2) interval counts
~13x -- fixed).

(A) DISPERSION (the Lorentz-signature test): global Rayleigh quotient
        lambda = sum_x phi(x)(B phi)(x) / sum_x phi(x)^2
    for spatial cos(k x) and temporal cos(k t).  box = d_t^2 - d_x^2 gives
    lambda_space > 0, lambda_time < 0 -> OPPOSITE signs = Lorentzian.
(B) SUMMED SECOND MOMENT M2_BD = sum 2 eps w(m) e^mu e^nu / N -> g^{mu nu} if Lorentz.

Anti-circularity: w(m),(1,-2,1) are the BD definition; no dispersion/Lorentz formula
in the generator; cos fields are probes, not operator inputs.
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box  # noqa: E402
from bd_core import smeared_weight, causal_past_idx, interval_counts  # noqa: E402

OUT = Path(__file__).resolve().parent


def one_realisation(pts, base, eps, ks):
    """Single pass over base events; return per-field numerators/denominators and M2."""
    t, x = pts[:, 0], pts[:, 1]
    fields = {}
    for k in ks:
        fields[("space", k)] = np.cos(k * x)
        fields[("time", k)] = np.cos(k * t)
    num_sm = {key: 0.0 for key in fields}
    num_sh = {key: 0.0 for key in fields}
    den = {key: 0.0 for key in fields}
    M2 = np.zeros((2, 2)); used = 0
    for xi in base:
        P = causal_past_idx(pts, xi)
        if P.size < 4:
            continue
        m = interval_counts(pts, P)
        w = smeared_weight(m, eps)
        e = pts[xi] - pts[P]
        # layer masks for the sharp (1,-2,1) operator
        l0 = (m == 0); l1 = (m == 1); l2 = (m == 2)
        for key, fld in fields.items():
            fx = fld[xi]; fP = fld[P]
            B_sm = -fx + 2.0 * eps * np.dot(w, fP)
            inner = fP[l0].sum() - 2.0 * fP[l1].sum() + fP[l2].sum()
            B_sh = -2.0 * fx + 4.0 * inner
            num_sm[key] += fx * B_sm
            num_sh[key] += fx * B_sh
            den[key] += fx * fx
        M2 += np.tensordot(2 * eps * w, e[:, :, None] * e[:, None, :], axes=(0, 0))
        used += 1
    lam_sm = {key: (num_sm[key] / den[key] if den[key] else np.nan) for key in fields}
    lam_sh = {key: (num_sh[key] / den[key] if den[key] else np.nan) for key in fields}
    return lam_sm, lam_sh, (M2 / used if used else M2), used


def bulk_base(pts, T, X, rng, cap):
    t, x = pts[:, 0], pts[:, 1]
    b = np.nonzero((t > T * 0.4) & (t < T * 0.65) & (x > X * 0.3) & (x < X * 0.7))[0]
    if len(b) > cap:
        b = rng.choice(b, cap, replace=False)
    return b


def run(rho, T, X, eps, ks, n_real, cap=250, seed0=0):
    lam_s = {k: [] for k in ks}; lam_t = {k: [] for k in ks}
    lam_s_sh = {k: [] for k in ks}; lam_t_sh = {k: [] for k in ks}
    ats, axs = [], []; nb = 0
    for s in range(n_real):
        rng = np.random.default_rng(seed0 + s)
        pts = sprinkle_box(rho, [[0, T], [0, X]], rng)
        base = bulk_base(pts, T, X, rng, cap)
        if len(base) < 20:
            continue
        nb += len(base)
        lsm, lsh, M2, used = one_realisation(pts, base, eps, ks)
        for k in ks:
            lam_s[k].append(lsm[("space", k)]); lam_t[k].append(lsm[("time", k)])
            lam_s_sh[k].append(lsh[("space", k)]); lam_t_sh[k].append(lsh[("time", k)])
        ats.append(M2[0, 0]); axs.append(M2[1, 1])

    def ms(v):
        v = np.array([x for x in v if np.isfinite(x)])
        return float(v.mean()), float(v.std() / np.sqrt(len(v)))

    out = {"rho": rho, "T": T, "X": X, "eps": eps, "ks": list(ks), "n_real": n_real,
           "mean_base_per_real": nb / max(n_real, 1),
           "dispersion_smeared": {}, "dispersion_sharp": {}}
    sig = []
    for k in ks:
        sm, ss = ms(lam_s[k]); tm, ts_ = ms(lam_t[k])
        out["dispersion_smeared"][str(k)] = {
            "lambda_space": sm, "lambda_space_sem": ss,
            "lambda_time": tm, "lambda_time_sem": ts_,
            "opposite_signs": bool(sm * tm < 0),
            "space_pos_sig": bool(sm - 2 * ss > 0), "time_neg_sig": bool(tm + 2 * ts_ < 0)}
        sig.append(sm * tm < 0)
        sm2, _ = ms(lam_s_sh[k]); tm2, _ = ms(lam_t_sh[k])
        out["dispersion_sharp"][str(k)] = {"lambda_space": sm2, "lambda_time": tm2,
                                           "opposite_signs": bool(sm2 * tm2 < 0)}
    atm, ate = ms(ats); axm, axe = ms(axs)
    out["second_moment_smeared"] = {"a_t": atm, "a_t_sem": ate, "a_x": axm, "a_x_sem": axe,
                                    "opposite_signs": bool(atm * axm < 0)}
    out["lorentzian_dispersion_all_k"] = bool(all(sig))
    return out


def main():
    ks = (0.4, 0.6, 0.8)
    res = {"main": run(rho=30.0, T=8.0, X=14.0, eps=0.4, ks=ks, n_real=30, cap=250)}
    # epsilon scan (BD4): is there a magic eps0 that restores Lorentz, or is eps just
    # a bias-variance knob with SNR ~ 1 throughout?  Use k=0.6 as the representative.
    scan = []
    for eps in (0.2, 0.3, 0.5, 0.7):
        r = run(rho=30.0, T=8.0, X=14.0, eps=eps, ks=(0.6,), n_real=16, cap=200, seed0=500)
        d = r["dispersion_smeared"]["0.6"]; sm = r["second_moment_smeared"]
        scan.append({"eps": eps,
                     "lambda_space": d["lambda_space"], "lambda_space_sem": d["lambda_space_sem"],
                     "lambda_time": d["lambda_time"], "lambda_time_sem": d["lambda_time_sem"],
                     "lorentz_signature": d["space_pos_sig"] and d["time_neg_sig"],
                     "a_t": sm["a_t"], "a_t_sem": sm["a_t_sem"],
                     "a_x": sm["a_x"], "a_x_sem": sm["a_x_sem"]})
    res["eps_scan"] = scan
    res["timestamp_utc"] = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    (OUT / "bd_summed_action_data.json").write_text(json.dumps(res, indent=2))

    r = res["main"]
    print("=" * 72)
    print("BD SUMMED ACTION -- Lorentz signature (summed; error bars)")
    print("=" * 72)
    print(f"rho={r['rho']} box {r['T']}x{r['X']} eps={r['eps']} n_real={r['n_real']} "
          f"mean_base/real={r['mean_base_per_real']:.0f}")
    print("\nDISPERSION (Rayleigh lambda; Lorentz => space>0, time<0, OPPOSITE):")
    print("   k    SMEARED  lambda_space        lambda_time         opp?  SHARP opp?")
    for k in ks:
        sm = r["dispersion_smeared"][str(k)]; sh = r["dispersion_sharp"][str(k)]
        print(f"  {k:.1f}   {sm['lambda_space']:+7.3f}+/-{sm['lambda_space_sem']:.3f}  "
              f"{sm['lambda_time']:+7.3f}+/-{sm['lambda_time_sem']:.3f}   "
              f"{str(sm['opposite_signs']):>5}  {str(sh['opposite_signs']):>5}")
    sm2 = r["second_moment_smeared"]
    print(f"\nSUMMED 2nd MOMENT: a_t={sm2['a_t']:+.3f}+/-{sm2['a_t_sem']:.3f}  "
          f"a_x={sm2['a_x']:+.3f}+/-{sm2['a_x_sem']:.3f}  opposite(Lorentz)={sm2['opposite_signs']}")
    print(f"\nLorentzian dispersion at all k (smeared): {r['lorentzian_dispersion_all_k']}")
    print("\nEPS SCAN (k=0.6): is there a magic eps0? (Lorentz => space>0 & time<0)")
    print("  eps   lambda_space       lambda_time        a_t            a_x         Lorentz?")
    for sct in res["eps_scan"]:
        print(f"  {sct['eps']:.1f}  {sct['lambda_space']:+6.3f}+/-{sct['lambda_space_sem']:.3f}  "
              f"{sct['lambda_time']:+6.3f}+/-{sct['lambda_time_sem']:.3f}  "
              f"{sct['a_t']:+6.3f}+/-{sct['a_t_sem']:.3f}  "
              f"{sct['a_x']:+6.3f}+/-{sct['a_x_sem']:.3f}   {sct['lorentz_signature']}")
    return res


if __name__ == "__main__":
    main()
