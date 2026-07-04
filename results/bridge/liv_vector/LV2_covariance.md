# LV2 — the plaquette ensemble is boost-covariant (no intrinsic preferred frame)

**Task.** Internal covariance test: bin plaquettes by axis rapidity η of the causal
diagonal d₁; **predict** each bin's E/B by analytically boosting the measured rest-bin
population (η < 0.15) to the bin's rapidity along random directions; compare. No
continuum model, no fit. Generator `LV2_covariance.py`, data
`LV2_covariance_data.json`. Same ensemble as LV1 (12 941 plaquettes, 20 seeds).

## Result

E/B(η) falls from ≈19 near rest to 1.58 at the box's rapidity reach — the global
E/B ≈ 3 is the rapidity-weighted average of this single orbit. Bin by bin
(size-controlled = fixed invariant proper-area band, middle quartiles of rest bin):

| η bin | n | measured E/B | predicted (boosted rest) | z (band) |
|---|---|---|---|---|
| [0.15,0.35) | 325 | 19.27 ± 0.83 | 21.5 ± 4.4 | 1.53 |
| [0.35,0.55) | 1071 | 7.38 ± 0.12 | 8.6 ± 1.4 | 0.52 |
| [0.55,0.75) | 1954 | 3.89 ± 0.04 | 4.70 ± 0.51 | 0.16 |
| [0.75,0.95) | 2552 | 2.62 ± 0.02 | 2.75 ± 0.28 | 0.21 |
| [0.95,1.15) | 2497 | 1.98 ± 0.01 | 2.15 ± 0.16 | 0.03 |
| [1.15,1.45) | 2769 | 1.58 ± 0.01 | 1.45 ± 0.04 | **3.19** |

Median z (size-controlled) = **0.36**; 5/6 bins agree within ≲1.5σ.

## The one deviating bin is the regulator's edge

⟨pa²⟩ (the *invariant* proper area²) drifts across bins: 12.7 (rest) → 11.1 → 9.3 →
6.3 → 3.6 → 1.9 → **0.80**. A boost cannot change pa²; this 16× drift is pure
**box selection** — large diamonds boosted to high η no longer fit in the window
(coordinate extent ~ τ·e^η). The only >2σ bin is precisely the last one, sitting at
the truncation edge where the surviving population is most distorted. This is the
quantitative fingerprint of the cutoff mechanism that LV3 then scans directly.

## Verdict

**PASS (pre-registered: median size-controlled z ≤ 2).** Within errors, the population
at rapidity η *is* the boost of the rest population: the ensemble carries **no intrinsic
preferred frame**. What breaks Lorentz invariance in the W2 numbers is the **truncation**
of this covariant orbit by the finite box — a regulator, not a property of the network.
The 3σ edge bin is flagged honestly and is consistent with that same truncation.
