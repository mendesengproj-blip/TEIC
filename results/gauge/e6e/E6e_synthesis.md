# E6e — Synthesis: what curvature would give an O(1) photon? — Planck-scale (physical frontier)

> Analytic extrapolation of E6c (no new Monte Carlo). Code: `E6e_extrapolation.py`. Analysis:
> `E6e_extrapolation.md`. Data: `E6e_extrapolation.json`. Figure: `E6e_extrapolation.png`.
> Run jun/2026. Result goes to RESEARCH_MAP, not to a paper. Modifies no earlier campaign.

## Question

E6c showed de Sitter curvature furnishes a magnetic (B-type) 2-cell fraction that rises
monotonically with curvature, crossing 0.01 at R̂=2 (R_dS≈1.7ℓ). E6d ruled out amplifying it
by the orientation ferromagnet. E6e asks the purely analytic question: **what curvature R̂
would push frac_B to O(10%), and is that R̂ physically reasonable (sub-Planckian) or
trans-Planckian (a physical, not just technical, frontier)?**

## Method & conditioning

Fitted three pre-registered models (power `a(1/R̂)^α`, exponential `a·e^(−bR̂)`, quadratic
`a/R̂²`) to E6c's five finite-curvature points, both directly and to the curvature **excess**
Δ = frac_B − Minkowski floor. **The fit is well-conditioned** (max parameter uncertainty 17%
≪ the 50% ill-conditioning threshold) — contrary to the charter's worry, E6c has five clean
positive points, not one, so this is NOT the "need more points before extrapolating" branch.

**Best fit: Δ ∝ (1/R̂)^1.73, R²=0.997** — the curvature-added magnetic fraction scales as
≈ the curvature squared (`1/R̂² = H²`; the fixed quadratic gives R²=0.984, as good within
errors). Clean, physically sensible leading-order curvature law.

## Result

```
Extrapolated R̂ for frac_B = O(10%)  (well-fitting models, direct + excess):
   median R̂ ≈ 0.57,  range 0.13 – 0.75   -> ALL < 1
Targets (excess fits):
   frac_B = 0.05  ->  R̂ ≈ 0.8 – 0.9
   frac_B = 0.10  ->  R̂ ≈ 0.5 – 0.6
   frac_B = 0.50  ->  R̂ ≈ 0.2 – 0.3
Pessimistic outlier: the exponential model (R²≈0.99) SATURATES at ~3% -> O(10%) unreachable
   at ANY curvature.
b²/e² (mean) reaches 1 (avg cell on the light cone) at R̂ ≈ 1.9–2.2 (≈ the measured R̂=2),
   yet frac_B is only ~1.2% there -> a large FRACTION needs far more curvature than the MEAN.
```

**Physical scale [EXTERNO/ASSUMIDO]:** identifying the discreteness scale with the Planck
scale (ℓ ≡ ℓ_Planck), R̂ < 1 means a de Sitter radius **below the Planck length** — sub-Planckian
curvature, where the continuum/sprinkling picture is at/below its validity floor.

## Verdict (against the pre-registered criterion)

```
PRE-REGISTERED:
  SUCCESS  frac_B~O(10%) at R̂~0.5–5 (sub-Planckian, not absurd) -> run full E6e MC at R̂<2
  DEATH    frac_B~O(10%) needs R̂<0.1 (trans-Planckian) -> physical frontier, E6 closes
  INCONCL. <2 points / parameters uncertain >100% -> name the extra R̂ needed, don't fabricate

MEASURED  ->  PHYSICAL FRONTIER (not the hard death; not a clean success).
  - Well-conditioned (NOT the inconclusive/ill-posed branch): 5 clean points, σ_rel ≤ 17%.
  - O(10%) requires R̂ ≈ 0.5–0.6 (range 0.13–0.75) — BELOW the discreteness/Planck scale
    (R̂<1). O(50%) needs R̂ ≈ 0.2–0.3 (trans-Planckian). Even O(5%) needs R̂ ≈ 0.8–0.9.
  - This straddles the pre-registered boundary: R̂≈0.57 is just above the 0.1 hard-death floor
    and at the low edge of the 0.5–5 "worth-running" band, but BELOW R̂=1 (continuum validity).
  - The honest reading is therefore [FRONTEIRA FÍSICA], exactly the charter's "R̂~0.1–1 ->
    sub-/near-Planckian -> physical frontier, not just technical" branch: a usable photon
    magnetic sector via this mechanism needs Planck-scale curvature. The exponential reading
    is stronger still (O(10%) unreachable at any R̂).
```

## Physical reading — answer to "why does the observable universe have photons?"

The curvature mechanism (E6c) is **real and well-characterised** (frac_B ∝ H², R²=0.997), but
it delivers an O(1) magnetic sector only at **Planck-scale curvature** (R̂≲0.6). The observable
universe has R̂ astronomically large (de Sitter radius ≫ Planck length), where this mechanism
gives frac_B ≈ the flat tail ≈ 0. **So the BD-gauge curvature route does NOT explain the
photons of the observable, low-curvature universe** — it is a *physical* frontier: the
ingredient (extreme curvature) is well-defined and the scaling is clean, but the required
value lies at/below the Planck scale where the framework's own continuum description fails.

## Recommendation

- **A full E6e Monte-Carlo campaign at R̂<2 is of marginal value and NOT recommended as a
  photon search.** The extrapolation is already well-conditioned; pushing to R̂<1 would only
  probe the trans-continuum regime where the construction loses physical meaning.
- A **small confirmatory run at R̂=1.5, 1.0** (still within/near the valid continuum) would
  verify the ∝1/R̂² law and discriminate it from the saturating exponential — worthwhile as a
  *law-confirmation*, not a photon search. R̂<0.5 should not be run (sub-Planckian).
- **The live problem returns to: is there a DIFFERENT spacelike-2-cell construction that gives
  an O(1) magnetic fraction at LOW curvature?** Both "taller diamonds" (E6b) and "ordered
  ferromagnet" (E6d) are dead; curvature (E6c) works only at the Planck scale (E6e). The
  remaining unexplored direction is anisotropic/inhomogeneous geometry or a genuinely
  different 2-cell definition — not more of the de Sitter isotropic-curvature dial.

## What this changes for E6 / RESEARCH_MAP

- E6 is **refined**: the curvature route is now quantified — frac_B ∝ H², and an O(10%)
  magnetic sector needs **R̂≈0.5–0.6 (sub-Planckian)** → **[FRONTEIRA FÍSICA]** for the
  observable universe (the mechanism is real but Planck-scale). E6 keeps [FRONTEIRA TÉCNICA]
  as its overall tag (the operator/2-cell question is unresolved), now annotated with the
  Planck-scale curvature requirement.
- E6e (the full MC) is **not pursued**: the analytic extrapolation already answers its
  question (Planck-scale), so spending MC on R̂<1 is not warranted.

## Anti-circularity

Pure re-analysis of E6c's published JSON; no relativistic literal, no new sprinkling. The
Minkowski floor is handled explicitly (excess fit). Conditioning is reported honestly
(well-conditioned, σ_rel≤17%) rather than assumed; the model spread (power vs quad vs the
saturating exponential) is shown, not hidden, and the extrapolated R̂ is quoted as a **range**
(0.13–0.75), not a false-precision single value. The Planck identification is flagged
[EXTERNO/ASSUMIDO]. Earlier campaigns untouched.
