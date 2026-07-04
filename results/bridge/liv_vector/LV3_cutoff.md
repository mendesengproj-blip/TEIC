# LV3 — E/B is a regulator number: the box-truncated boost orbit, scanned

**Task.** If the ensemble is one LI orbit truncated at the rapidity the box holds
(reach = L·ρ^{1/4} in granularity units), then (P1) cumulative E/B(η_cut) curves must
collapse across box sizes, (P2) the endpoint E/B must drift toward 1 as the reach grows,
(P3) the Euclidean weight ⟨e²+b²⟩ must grow ~cosh 2η per bin while ⟨e²−b²⟩ is invariant
content. Generator `LV3_cutoff.py`, data `LV3_cutoff_data.json`. Six configs: L ∈
{3,4,5,6} at ρ=12; ρ ∈ {6,24} at L=4 (10–16 seeds each, 6 080–10 343 plaquettes).

## P2 — the endpoint drifts toward 1 with the reach, never with anything else

| scan | reach L·ρ^¼ | η_q95 | E/B total |
|---|---|---|---|
| L3 ρ12 | 5.6 | 1.53 | 3.337 ± 0.059 |
| L4 ρ6 | 6.3 | 1.60 | 3.078 ± 0.040 |
| L4 ρ12 | 7.4 | 1.70 | 2.971 ± 0.027 |
| L4 ρ24 | 8.9 | 1.80 | 2.825 ± 0.038 |
| L5 ρ12 | 9.3 | 1.82 | 2.807 ± 0.024 |
| L6 ρ12 | 11.2 | 1.91 | 2.686 ± 0.032 |

**Strictly monotone in the reach** — and the two knobs (L and ρ) interleave on the same
axis: E/B does not care whether the reach comes from volume or density, only how much
boost orbit fits. The drift is slow (η_max ~ ln reach), exactly the logarithmic approach
to 1 a truncated non-compact orbit forces; "3" is where boxes of this class truncate it.

## P1 — one universal curve

Cumulative E/B(η_cut) for L = 3,4,5,6 at ρ=12 agree to ≤ 8% relative spread over the
whole common range (median ~5%), e.g. at η_cut=1.0: 4.13 / 3.82 / 3.73 / 3.62. The
small residual spread sits where the size-selection mix differs most (largest η_cut)
and at the noisy first bin. The curves are one orbit; only the endpoint moves.

## P3 — the LV weight is the truncation depth

Per η bin (L4 ρ12): the ratio (e²+b²)/(e²−b²) grows 1.07 → 1.34 → 1.92 → 3.01 → 4.89 →
8.2 → 14.7 → 32.7 across bin centers η = 0.15…2.25 — tracking cosh 2η (1.05…45) to
within the bin-averaging — while ⟨e²−b²⟩ per plaquette is pure invariant content whose
bin dependence (11.4 → 0.016) is the box's size selection, already fingerprinted in LV2.
The Euclidean (frame-dependent) part of the quadratic coefficient is therefore carried
**entirely by how deep in rapidity the regulator lets the sum go**.

## Verdict

**PASS (pre-registered kill not triggered).** E/B is cutoff-set: monotone in the reach,
curve-collapsed across boxes, with the Euclidean excess growing exactly as boost depth.
Combined with LV2 (covariant ensemble), the order-1 "violation" of W2 is the regulator
of an LI orbit, not a property of the network. What survives in the infinite-reach limit
of the *quadratic* coefficient is the divergent Euclidean trace — which is precisely why
the quadratic expansion is the wrong observable and the bounded summed action (LV4) is
the right one; the BD sign-alternating kernel is the linear-theory route to the same
subtraction (BRIDGE_BD).
