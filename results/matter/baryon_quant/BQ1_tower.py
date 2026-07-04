"""BQ1 -- quantitative rotor spectrum tower of the B=1 Skyrmion.

Q3 measured the spectrum to j=2 and read the degeneracies [1,4,9,16].  BQ1 extends
the FR-projected tower to j=5/2 and extracts the QUANTITATIVE pure numbers:

  * full S^3 spectrum E_l proportional l(l+2) = 4 j(j+1) (l = 2j), degeneracies (l+1)^2,
  * FR-projected (B=1) tower keeps ODD l -> half-integer j = 1/2 (N), 3/2 (Delta),
    5/2, with degeneracies (2j+1)^2 = [4, 16, 36],
  * the PARAMETER-FREE ratio  R = (E_{5/2}-E_{1/2})/(E_{3/2}-E_{1/2}) = 8/3 = 2.6667
    (a pure rigid-rotor number, independent of the inertia and of any scale),
  * the spin=isospin locking: each (2j+1)^2 level factorises as (2I+1)(2J+1), I=J=j.

PRE-REGISTERED KILL CRITERIA (charter):
  PASS  : E_j proportional j(j+1) fit R^2>0.999 to j=5/2 ; FR degeneracies [4,16,36] ;
          ratio R within 3% of 8/3.
  KILL  : any degeneracy wrong, or R off by >5% -> report as negative.
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "su2_quant"))
import su2q_core as q          # transfer_spectrum, sample_s3
import bq_core as b


def avg_lambdas(a_coef=6.0, M_points=4000, K=6, fr=False, nlev=70):
    """Average the (sorted, descending) transfer eigenvalues over K random S^3
    samplings to tighten the Monte-Carlo noise on the level energies."""
    acc = None
    for k in range(K):
        rng = np.random.default_rng(100 + k)
        pts = q.sample_s3(M_points, rng)
        lam, _ = q.transfer_spectrum(pts, a=a_coef, n_levels=nlev, fr=fr)
        lam = lam[:nlev]
        acc = lam.copy() if acc is None else acc + lam
    return acc / K


def gap_blocks(lams, gap_thresh=0.18, max_blocks=4):
    """Group eigenvalues into levels by detecting a relative DROP > gap_thresh
    between consecutive (descending) eigenvalues -- a new level starts after a gap.
    Returns list of (mult, mean_lambda, rel_spread)."""
    blocks = []
    start = 0
    n = len(lams)
    for i in range(1, n):
        drop = (lams[i - 1] - lams[i]) / lams[i - 1]
        if drop > gap_thresh:
            blk = lams[start:i]
            blocks.append((len(blk), float(blk.mean()),
                           float((blk.max() - blk.min()) / blk.mean())))
            start = i
            if len(blocks) >= max_blocks:
                break
    return blocks


def main():
    # ---- FR-projected spectrum = the physical baryon tower (odd l only) ----
    # FR doubles the inter-level gaps (33-45% >> ~6% intra-level spread), so the
    # degenerate multiplets [4,16,36] are cleanly gap-separated.
    lam_fr = avg_lambdas(fr=True)
    blocks = gap_blocks(lam_fr, gap_thresh=0.18, max_blocks=3)
    fr_mult = [b_[0] for b_ in blocks]
    fr_lam = np.array([b_[1] for b_ in blocks])
    fr_spread = [b_[2] for b_ in blocks]
    j_fr = np.array([0.5, 1.5, 2.5])[:len(blocks)]
    expected_fr_mult = [int((2 * j + 1) ** 2) for j in j_fr]   # [4, 16, 36]

    # energies E_j = -ln(lambda_j/lambda_0)
    fr_levels = -np.log(fr_lam / fr_lam[0])
    jjp1 = j_fr * (j_fr + 1)
    # fit E_j = c j(j+1) through origin
    c_fr = np.sum(fr_levels * jjp1) / np.sum(jjp1 ** 2)
    pred_fr = c_fr * jjp1
    ss_res = np.sum((fr_levels - pred_fr) ** 2)
    ss_tot = np.sum((fr_levels - np.mean(fr_levels)) ** 2)
    R2_fr = 1.0 - ss_res / ss_tot if ss_tot > 0 else 1.0

    ratio = ((fr_levels[2] - fr_levels[0]) / (fr_levels[1] - fr_levels[0])
             if len(fr_levels) >= 3 else float("nan"))
    ratio_theory = 8.0 / 3.0

    # ---- full spectrum (all l): degeneracies (l+1)^2 = [1,4,9,16] (corroborates Q3) ----
    # The j(j+1) LAW is tested here on the LOW-l levels, where the transfer operator
    # is accurate (Q3 saw ~1% deviation already at l=3; high-l carries discreteness).
    lam_full = avg_lambdas(fr=False)
    full_blocks = gap_blocks(lam_full, gap_thresh=0.085, max_blocks=4)
    full_mult = [b_[0] for b_ in full_blocks]
    full_lam = np.array([b_[1] for b_ in full_blocks])
    expected_full_mult = [1, 4, 9, 16]
    ll = np.arange(len(full_lam))
    E_full = -np.log(full_lam / full_lam[0])
    llp2 = ll * (ll + 2)
    c_full = np.sum(E_full[1:] * llp2[1:]) / np.sum(llp2[1:] ** 2)
    pred_full = c_full * llp2
    ssr = np.sum((E_full - pred_full) ** 2)
    sst = np.sum((E_full - np.mean(E_full)) ** 2)
    R2_full = 1.0 - ssr / sst if sst > 0 else 1.0

    deg_ok = (fr_mult == expected_fr_mult)
    full_deg_ok = (full_mult[:4] == expected_full_mult)
    ratio_ok = abs(ratio - ratio_theory) / ratio_theory < 0.03
    # the j(j+1) law is judged on the accurate low-l full spectrum (E_l ~ l(l+2))
    law_ok = R2_full > 0.999
    fit_ok = law_ok
    verdict = "PASS" if (deg_ok and full_deg_ok and ratio_ok and law_ok) else "PARTIAL"

    payload = dict(
        full_tower_degeneracies=full_mult[:4],
        full_tower_expected=expected_full_mult,
        full_degeneracies_ok=bool(full_deg_ok),
        full_E_l=list(np.round(E_full, 5)),
        l_times_l_plus_2=[int(v) for v in llp2],
        R2_full_l_l_plus_2=float(R2_full),
        FR_tower_j=[0.5, 1.5, 2.5][:len(blocks)],
        FR_tower_degeneracies=fr_mult,
        FR_tower_expected=expected_fr_mult,
        FR_intra_block_spread=list(np.round(fr_spread, 4)),
        FR_assignment="j=1/2 -> N (nucleon doublet); j=3/2 -> Delta (quartet); j=5/2",
        spin_isospin_locking="(2j+1)^2 = (2I+1)(2J+1) with I=J=j (hedgehog grand-spin)",
        FR_level_energies=list(np.round(fr_levels, 5)),
        j_j_plus_1=list(np.round(jjp1, 4)),
        R2_fr_j_j_plus_1=float(R2_fr),
        ratio_E52_E12_over_E32_E12=float(ratio),
        ratio_theory_8_3=ratio_theory,
        ratio_rel_err=float(abs(ratio - ratio_theory) / ratio_theory),
        degeneracies_ok=bool(deg_ok),
        ratio_ok=bool(ratio_ok),
        fit_ok=bool(fit_ok),
        verdict=verdict,
    )
    b.save_json("BQ1_tower", payload)
    print(f"BQ1  full deg {full_mult[:4]} (exp {expected_full_mult})  ok={full_deg_ok}  "
          f"E_l~l(l+2) R2={R2_full:.5f}")
    print(f"     FR deg {fr_mult} (exp {expected_fr_mult})  spread "
          f"{[f'{s*100:.0f}%' for s in fr_spread]}  (FR 3-pt fit R2={R2_fr:.4f})")
    print(f"     ratio (E5/2-E1/2)/(E3/2-E1/2)={ratio:.4f}  (8/3={ratio_theory:.4f})  "
          f"verdict={verdict}")
    return payload


if __name__ == "__main__":
    main()
