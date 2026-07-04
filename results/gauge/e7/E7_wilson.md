# E7 — Wilson-loop area-law vs perimeter-law measurement (analysis)

> Pre-registered in `E7_COULOMB_PHASE.md`. Engine REUSED from E5 (`e5_core`,
> `e5_fast.FastU1Gauge`), validated by `E7_gate` (G1 gauge-inv exact, G2 β_c=1.00).
> Code: `E7_wilson.py`. Data: `E7_wilson.json`. Figure: `E7_wilson.png`. Run jun/2026
> (214 s, 3 substrate seeds).

## What was measured

For a U(1) Wilson gauge field, ⟨W(C)⟩ = ⟨cos(holonomy around C)⟩ classifies the phase:
**area law** ⟨W⟩~exp(−σ·Area) ⇒ confining ⇒ **no emergent photon**; **perimeter law**
⟨W⟩~exp(−μ·Perimeter) ⇒ Coulomb ⇒ photon possible in principle. The campaign is in two
anti-circular stages.

### STAGE A — validate the classifier on the regular 4D lattice (known answer)

The gold-standard discriminator is the **Creutz ratio**
χ(R,T)=−ln[W(R,T)W(R−1,T−1)/(W(R−1,T)W(R,T−1))], which cancels the perimeter term:
χ→σ>0 (area/confining), χ→0 (perimeter/Coulomb). On a 6⁴ lattice with controlled R×T
rectangles:

```
                 Creutz χ(2,2)   χ(3,3)     (known phase)
 β=0.7  (β<β_c)     +1.219       −0.552     CONFINING  -> large χ, area law  ✔
 β=1.3  (β>β_c)     +0.147       +0.042     COULOMB    -> χ→0, perimeter law ✔
```

The Creutz ratio **cleanly separates the two phases (8× in χ(2,2))** — the engine and the
discriminator both work where the answer is known.

**But the surrogate that can be ported to the causal set (the "patch" method) does NOT
cleanly work**, and Stage A is what exposes this:

```
                 patch late-slope   patch sa/sf   winner-label
 β=0.7 CONFINING     −0.214            0.13          "perimeter"   (WRONG: is area law)
 β=1.3 COULOMB       −0.038            0.11          "perimeter"
```

- The `winner` label calls the **known-confining** β=0.7 point "perimeter" — a
  misclassification. Compact patches in 4D fold and nearly close, shrinking the boundary
  and masking the area law.
- The `sa/sf` ratio (measured tension ÷ independent-plaquette tension) gives 0.13 vs 0.11
  — **it does not separate the phases at all**.
- Only the **large-loop log-slope** `late_slope` separates them (−0.214 vs −0.038, ~5.6×)
  — it is the one portable discriminator with any power, so the causal-set verdict is read
  primarily against it.

### STAGE B — causal set, β-scan (3 independent Poisson substrates)

Substrate: ρ=0.5, L_box=5.6 → n≈492 events, 8031 links, 14462 diamond plaquettes. Patch
perimeter grows slowly with area k=[1,2,3,4,6,8] → P_k≈[4.0,4.1,4.7,4.9,5.5,6.2], so a
perimeter law would predict a near-flat ⟨W⟩; substantial decay in k indicates area-law.

```
 β      late_slope (mean±std)   σ_area   anchor side       (anchors: conf −0.214, Coul −0.038, mid −0.126)
 0.50     −0.274 ± 0.026        0.304    CONFINING-side
 0.70     −0.172 ± 0.048        0.183    CONFINING-side
 0.90     −0.099 ± 0.011        0.108    Coulomb-side
 1.00     −0.087 ± 0.011        0.095    Coulomb-side
 1.10     −0.081 ± 0.018        0.084    Coulomb-side
 1.30     −0.080 ± 0.007        0.083    Coulomb-side
 1.50     −0.071 ± 0.016        0.072    Coulomb-side
 1.80     −0.053 ± 0.012        0.056    Coulomb-side
 2.00     −0.056 ± 0.009        0.059    Coulomb-side
```

## Reading the result

1. **A confinement→deconfinement crossover IS present and mirrors the lattice.** The
   causal-set late-slope crosses from the confining side to the Coulomb side at **β≈0.85**,
   right where E5/G2 located the specific-heat peak (β_c≈1.0). At matched β it tracks the
   lattice (β=0.7: causal −0.172 vs lattice −0.214; β=1.3: causal −0.080 vs lattice
   −0.038). So **"confining at all β" is DISFAVOURED** — the link sector weakens markedly
   toward weak coupling, exactly like 4D compact U(1), not like permanently-confining 3D.

2. **But a Coulomb (perimeter-law) phase is NOT cleanly certified.** At the largest β the
   late-slope (−0.056) only **approaches** the lattice Coulomb anchor (−0.038) without
   reaching it within error, and σ_area never vanishes (min 0.056). The causal set is
   consistently **somewhat more confining than the lattice at matched β** — consistent with
   the mean-field/non-local bias of the substrate (E5-1b: deg∝L^2.9).

3. **The clean discriminator cannot be built here.** The Creutz ratio that decides the
   lattice needs controlled R×T rectangles; the non-local causal set has no rectangular
   loop structure, and the patch surrogate is demonstrably biased (Stage A control fails on
   `winner` and `sa/sf`). So area-vs-perimeter cannot be certified on the bare diamonds.

## Verdict (automated, conservative)

**INCONCLUSIVE.** No Coulomb phase is positively certified; confinement-at-all-β is
positively *disfavoured*. The honest residual: the causal U(1) shows a lattice-like
confinement→Coulomb **crossover near β≈1**, but the decisive observable (Creutz ratio) is
structurally unavailable on the non-local substrate and the portable surrogate cannot
close the gap. This is the **E5-1b non-locality obstruction reappearing in the Wilson-loop
observable** — the same wall that the BD-smeared construction (E6) was conceived to climb.

**Minimum to resolve:** controlled rectangular Wilson loops require either (i) an explicit
Lorentz-breaking localisation (accept a regulator), or (ii) the BD-smeared gauge operator
of E6 — i.e. the path forward is E6 itself, not a bigger bare-diamond run. Bare-diamond N
cannot fix a *structural* (no-rectangles) obstruction by growing.
