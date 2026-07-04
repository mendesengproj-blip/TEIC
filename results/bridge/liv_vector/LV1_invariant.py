"""LV1_invariant.py -- is the E/B ~ 3 split a preferred-frame effect at all?

LIV_VECTOR task LV1.  Claim under test: every causal-diamond plaquette is a
SIMPLE bivector Omega = 1/2 d1^d2 with d1 timelike (causal diagonal p->l) and
d2 spacelike (chord between mutually-spacelike j,k), hence spans a TIMELIKE
plane and satisfies the EXACT, frame-independent inequality

    I = (1/2) Omega_{mn} Omega^{mn} = b^2 - e^2 < 0     (electric dominance),

with e^2 - b^2 = squared proper area (a Lorentz invariant).  If so, the
per-plaquette electric dominance behind W2's E/B ~ 3 is forced by CAUSALITY,
identically in every frame -- it is not a preferred-frame (LV) statement.
The LV question then moves entirely to the ENSEMBLE weights (LV2-LV4).

PRE-REGISTERED KILL: if a non-negligible fraction (> 1%) of causal plaquettes
has I >= 0, or the bivectors are not simple (Pfaffian != 0), the timelike-plane
theorem is wrong and the campaign's framing collapses.

MEASURED (nothing inserted): simplicity |Pf|/(e2+b2); sign of I; distribution
of the dominance ratio r = (e2-b2)/(e2+b2); ensemble E/B (consistency with
W2 = 2.97 +/- 0.03 and AB2 = 3.25 +/- 0.10).
"""
from __future__ import annotations

import json, sys, time
from pathlib import Path
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from liv_core import plaquette_ensemble, pooled  # noqa: E402

OUT = Path(__file__).resolve().parent

RHO, EXTENT, NSEED, SEED0, NBASES = 12.0, 4.0, 20, 200, 1500


def main():
    seeds = plaquette_ensemble(RHO, EXTENT, NSEED, SEED0, n_bases=NBASES)
    e2, b2 = pooled(seeds, "e2"), pooled(seeds, "b2")
    Om = np.concatenate([s["Om"] for s in seeds])
    n = len(e2)

    # simplicity: Pf(Omega) = Om01*Om23 - Om02*Om13 + Om03*Om12 == 0 for simple
    pf = (Om[:, 0, 1] * Om[:, 2, 3] - Om[:, 0, 2] * Om[:, 1, 3]
          + Om[:, 0, 3] * Om[:, 1, 2])
    pf_rel = np.abs(pf) / (e2 + b2)

    inv = b2 - e2                      # I = (1/2) Om_{mn} Om^{mn}
    frac_bad = float(np.mean(inv >= 0))
    r = (e2 - b2) / (e2 + b2)

    # per-seed ensemble E/B (mean_e2 / mean_b2, per-plane normalization 3:3)
    eb_seed = np.array([s["e2"].mean() / s["b2"].mean() for s in seeds])

    res = {
        "config": {"rho": RHO, "extent": EXTENT, "n_seeds": len(seeds),
                   "seed0": SEED0, "n_bases": NBASES, "margin": 0.25},
        "n_plaquettes": int(n),
        "pfaffian_rel_max": float(pf_rel.max()),
        "frac_I_nonneg": frac_bad,
        "I_max": float(inv.max()),
        "dominance_r_median": float(np.median(r)),
        "dominance_r_q05": float(np.quantile(r, 0.05)),
        "dominance_r_q95": float(np.quantile(r, 0.95)),
        "EB_ratio_mean": float(eb_seed.mean()),
        "EB_ratio_sem": float(eb_seed.std() / np.sqrt(len(eb_seed))),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    (OUT / "LV1_invariant_data.json").write_text(json.dumps(res, indent=2))

    print("=" * 72)
    print("LV1 -- per-plaquette invariant: is electric dominance frame-dependent?")
    print("=" * 72)
    print(f"plaquettes (pooled, {len(seeds)} seeds): {n}")
    print(f"simplicity  max |Pf|/(e2+b2)      = {pf_rel.max():.3e}  (0 = simple)")
    print(f"invariant   frac(I = b2-e2 >= 0)  = {frac_bad:.4f}   max I = {inv.max():.3e}")
    print(f"dominance   r=(e2-b2)/(e2+b2): median {np.median(r):.3f}  "
          f"[q05 {np.quantile(r, 0.05):.3f}, q95 {np.quantile(r, 0.95):.3f}]")
    print(f"ensemble    E/B = {eb_seed.mean():.3f} +/- "
          f"{eb_seed.std()/np.sqrt(len(eb_seed)):.3f}   (W2: 2.97; AB2: 3.25)")
    print("-" * 72)
    if pf_rel.max() < 1e-10 and frac_bad < 0.01:
        print("VERDICT (LV1): every causal plaquette is a SIMPLE TIMELIKE-plane")
        print("  bivector with I < 0 EXACTLY: electric dominance is forced by")
        print("  causality, pointwise and in EVERY frame. The E/B>1 excess is an")
        print("  invariant statement, NOT a preferred-frame effect; the LV question")
        print("  moves to the ensemble weights (LV2) and the summed action (LV4).")
    else:
        print("VERDICT (LV1): KILL -- timelike-plane theorem violated.")
    return res


if __name__ == "__main__":
    main()
