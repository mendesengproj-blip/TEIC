# AUDIT_BRIDGE — Parallel audit of every bridge result (C1–C4, W1–W4, BD1–BD5)

A fresh-eyes audit of `results/bridge/`, run as if the results were someone else's, looking
for where the story is stronger than the numbers. Everything here **re-runs the bridge
generators unchanged** (imported, not modified) over **20 seeds** with error bars, plus a
guard sweep. No campaign was altered. Scripts and data: `results/audit/bridge_recheck/`.

## Headline

> **The bridge survives the audit.** No circularity anywhere; every C/W claim reproduces
> with 20 seeds; the BD results reproduce *including their honest negative*. The one
> genuinely vulnerable result (BD5: Lorentz restoration at SNR≈1) is exactly the one the
> original synthesis already flagged as the risk outcome. Two minor code advisories and one
> wrong inline comment were found and are noted for the authors.

## AB4 — Anti-circularity (priority gate) → **CLEAN**

Re-using the repository guard's own primitives over all 28 bridge files:
- **0** dilation literals (`sqrt(1-2M/r)`, `1/sqrt(1-β²)`, `γ=…`) anywhere.
- **0** complex literals in any generator.
- **0** DEV parameters / datasets (`a_0`, SPARC, BTFR, MOND, cH₀) in live code.
- All 19 `schwarzschild_redshift` references import the dilation formula from
  `src/validation.py` (the designated scoring file) and are used for comparison only; the
  background-metric sprinkler comes from `src/curved.py` (allowed generator geometry).

**Advisories (convention, not circularity):** `C2_ratios.py` & `C4_completeness.py` open a
`# COMPARISON ONLY` block but close it with a dashed rule instead of `# END COMPARISON
ONLY` (over-exempts — safe side); `NL1_action.py` computes the Schwarzschild Taylor series
inline (sympy, no generator — cannot be circular) rather than wrapping it. Fixing these
would let `results/bridge/` be added to the guard's `SCAN_DIRS`.

## AB1 — Coefficients C1–C4 (20 seeds) → **all confirmed**

| Claim | 20-seed result | Status |
|---|---|---|
| C2: ratios algebraic | C₂/C₁ = 1, C₃/C₁ = 2 with **exactly zero** seed variance, while κ (scale) and λ/|κ| (anisotropy) vary | ✓ algebraic, not geometric |
| C1: M2 positive-definite | eigenvalues all > 0 in **every** seed (2D & 4D) | ✓ structural (and is why BD smearing is needed) |
| C3: X0 ∝ ρ^p | **p = 1.00 ± 0.02** (3+1D, median); ≈1 in both dimensions; a₀~cH₀ rejected (p>0 ⇒ UV) | ✓ — **and the inline comment `C3_scale.py:132` claiming p=1/2 in 3+1D is wrong** |
| C4: quartic quantified | C_q < 0 at **9σ (1+1D), 17σ (3+1D)** | ✓ (was "identified but not quantified") |

## AB2 — Wilson W1–W4 (20 seeds) → **all confirmed**

- **W1:** holonomy → F exact for strong constant F (rel_err ~10⁻¹⁶ at F0 up to 100) and
  O(h²) for varying F (log-log slope **2.00**).
- **W2:** E/B = **3.25 ± 0.10** in genuine 3+1D; off-Maxwell cross consistent with 0. (E/B
  is a 3+1D-only quantity — undefined in 2D.)
- **W3:** bounded cosine ⇒ saturation (plateau 1.00 ± 0.01, max 1.03 ≪ ceiling 2), no
  explosion.
- **W4:** only first-derivative operators emerge — **no forbidden** `∂⁴θ` / Hořava-Lifshitz
  term at orders u², u⁴, u⁶.

## AB3 — Benincasa–Dowker BD1–BD5 (20 seeds) → **confirmed incl. the negative**

- **BD3:** sharp anisotropy a_t/a_x = **4.03 ± 0.01** (positive-definite, 100% of seeds)
  collapses under smearing to |a_t|+|a_x| ≈ 0.68, **consistent with zero** — the gross
  Euclidean anisotropy is removed.
- **BD5:** the smeared dispersion sits at **SNR < 2 at every ε** with the *wrong sign*;
  smaller ε does not help. A **physical** □/(2ερ) variance wall, not a numerical bug.
  Lorentz restoration is **not** positively demonstrated.

## AB5 — The weakest result

Ranked by the numbers, the most vulnerable result is **BD5 (Lorentz restoration, SNR≈1)**:
a non-detection underpinning the central "Lorentz" story. The audit's recommendation
matches the original framing — present it as the *risk outcome* (anisotropy removal shown,
positive restoration not). The other three candidates (E/B≈3, operator completeness, the
locked ratios) all survive with their honest framings intact. See `AB5_weakest.md` for the
full RESULTADO | CRÍTICA | RESPOSTA table.

## Net position of the bridge after audit

> **Form-complete, Lorentz-open — confirmed.** Every DEV operator emerges from causal links
> + plaquettes with the Stückelberg ratios *algebraically* locked (1, 2), a quantified DBI
> quartic (C_q < 0 at 9–17σ), F² from plaquettes, and **no forbidden higher-derivative
> operators**. The single open frontier is the order-1 Lorentz violation (E/B≈3): its cure
> (BD smearing) is the right operator and removes the gross anisotropy, but positive Lorentz
> restoration is beyond accessible network sizes (SNR≈1). The audit changes no verdict; it
> hardens the numbers, locates the one soft spot precisely, and flags three small code
> fixes. **No surprises are waiting in peer review that this audit did not surface.**

### Action items for the authors (cosmetic / correctness, no result affected)
1. Fix the wrong inline comment at `results/bridge/coefficients/C3_scale.py:131-132`
   (3+1D exponent is p≈1, not 1/2; the recorded JSON value 1.0 is already correct).
2. Close the `# COMPARISON ONLY` blocks in `C2_ratios.py` / `C4_completeness.py` with the
   canonical `# END COMPARISON ONLY` sentinel; wrap or import the Schwarzschild series in
   `NL1_action.py`.
3. Then add `results/bridge/` to `tests/test_no_circularity.py`'s `SCAN_DIRS`.

## Files
`results/audit/bridge_recheck/AB{1,2,3,4,5}_*.{py,md,json}`. Reproduce each with
`python results/audit/bridge_recheck/AB<n>_*.py`.
