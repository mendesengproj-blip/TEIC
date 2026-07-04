# E7_COULOMB_PHASE — Honest synthesis

> Campaign charter: `docs/prompts/E7_COULOMB_PHASE.md` (or the in-repo copy of the
> prompt). Pre-requisite probe for E6_BD_GAUGE_LORENTZIANO. Engine REUSED from E5; no
> motor rebuilt. Deliverables in `results/gauge/e7/` (the gauge-sector sibling of
> `results/gauge/e5/` — the "pasta equivalente" the charter permits, chosen so the E5
> engine imports cleanly). Run jun/2026.

## The question

In which phase is the U(1) link sector of the Poisson causal set built in E5 — **area
law (confining → no emergent photon, independent of action signature)** or **perimeter
law (Coulomb → a photon is possible in principle, and E6's signature problem is the real
obstacle)**?

## Synthesis table (charter format)

```
Literature scan (CST gauge):
  Sverdlov 0807.2066 / Sverdlov-Bombelli 0905.1506: gauge fields on causets via
  holonomies on causal diamonds EXIST as an action construction; the Monte-Carlo
  confinement/Coulomb PHASE of that action on a sprinkled causet was NOT measured in
  the literature -> the E7 measurement is itself a small original step.   [E7_literature.md]

Gate de validação:
  G1 (gauge invariance, reproduces E5):     PASS  (lattice 1.8e-15, diamonds 3.3e-15)
  G2 (4D transition β_c≈1.01):              PASS  (peak at β=1.00, = E5-V)         [E7_gate.md]

Medição principal:
  Discriminator that works (lattice):       Creutz ratio χ(2,2): 1.22 (confine) vs 0.15 (Coulomb)
  Discriminator portable to causet:         Creutz UNAVAILABLE (no controlled rectangles
                                            on a non-local causet); patch surrogate is
                                            biased (mislabels known-confining β=0.7).
  Comportamento de ⟨W(C)⟩ com tamanho:      confinement→Coulomb CROSSOVER near β≈0.85–1.0,
                                            mirroring the 4D lattice; but Coulomb anchor
                                            not cleanly reached, σ_area never → 0.
  β_c (se encontrado):                      crossover ≈ 0.85–1.0 (consistent with E5/G2),
                                            but NOT a certified deconfinement point.
  Fase a β típico:                          area-dominated at β≲0.8; perimeter-LEANING but
                                            not certified at β≳0.9.                 [E7_wilson.md]

Veredito:
[X] INCONCLUSIVE — registered honestly. Area-vs-perimeter is NOT decidable on the bare
    causal diamonds at the sizes reached, because the only clean discriminator (Creutz
    ratio on R×T rectangles) cannot be constructed on the non-local substrate and the
    patch surrogate fails its own Stage-A control. IMPORTANT NUANCE: the data DISFAVOURS
    "confining at all β" (a clear lattice-like crossover is seen) and mildly FAVOURS a
    weak-coupling Coulomb regime, but does not certify it.
[ ] MORTE (confining): NOT supported — confinement-at-all-β is positively disfavoured.
[ ] SUCCESS (Coulomb certified): NOT reached — Coulomb anchor not cleanly attained, σ≠0.
```

## What this means for the programme

- **Photon status stays [FRONTEIRA]** — it is **not** downgraded to [FRONTEIRA-ESTRUTURAL]
  (that needs a demonstrated permanent area law; E7 disfavours it) and **not** promoted to
  [SÓLIDO-PARCIAL] (Coulomb not certified). E7 adds a sharpened, honest boundary: the
  area/perimeter phase *observable* is itself obstructed by causal-set non-locality, the
  **same wall E5-1b hit** (deg∝L^2.9) and the same wall the BD operator was invented to
  tame in the scalar sector.

- **E6 (BD-gauge Lorentziano) is NOT killed and retains its motivation.** The honest read
  is mildly favourable to E6: the link sector behaves like the 4D lattice (which *does*
  have a Coulomb phase) and is disfavoured from being permanently confined. So the
  signature problem E6 targets (½ΣF² Euclidean) plausibly *is* the real obstacle rather
  than a hidden permanent confinement. But E7 cannot *certify* this — it can only say "not
  contradicted." E6 does not get a free pass; it gets a not-disconfirmed prior.

- **The decisive next step is E6 itself, not a bigger E7.** Resolving area-vs-perimeter
  needs controlled rectangular loops, which require either an explicit Lorentz-breaking
  localisation (a regulator, a new external ingredient) or the BD-smeared 2-cochain gauge
  operator of E6. Growing the bare-diamond N cannot fix a *structural* (no-rectangles)
  obstruction. So E7 hands the baton straight to E6 with the phase question still open but
  the "permanent confinement" escape route closed off.

## Anti-circularity & honesty notes

- Engine reused verbatim from E5 (gates G1/G2 re-passed); no relativistic/quantum literal
  in the dynamics (real Metropolis on S=β∑[1−cos]); "photon" appears only in synthesis.
- The patch surrogate's failure was **caught by its own pre-built control** (Stage A on the
  known-phase lattice) and reported, not hidden — the verdict is conservative *because* the
  control failed, exactly as the charter's INCONCLUSIVE branch requires.
- Three independent substrates give error bars; the inconclusiveness is **structural** (no
  clean discriminator on a non-local set), not merely statistical — more seeds/larger N
  would not convert it to a clean verdict.
- No previous campaign was modified. RESEARCH_MAP updated (photon line: [FRONTEIRA] +
  E7 note; Seção 5; roteiro R4).
