# PE6 — PHI_EMERGE synthesis (honest scorecard + verdict)

```
PE1 — Φ = ρ·e^{iφ̄} well-defined:        SIM
PE2 — Condensado espontâneo:             NÃO
PE2 — C(r) = constante:                  decai (sempre)
PE3 — m_A ∝ ρ ou √ρ:                    SIM, ~√ρ (p_medido=0.34, analítico 0.5)
PE4 — |Φ|(0) < |Φ|(∞) no vórtice:       NÃO
PE4 — σ_núcleo = constante:              NÃO (sem núcleo)
PE5 — Matéria estável sem axioma extra:  NÃO / N/A
```

## VEREDITO: **C** — Φ emergente gera m_A mas não pina

> **The composition `Φ = ρ·e^{iφ̄}` captures the *phase* sector but not the *magnitude*
> sector of an abelian-Higgs field. Mechanism partial; the complex field of
> CR_ABELIAN_HIGGS is still required for the core/pinning.**

### What emerged (the positive)

- **PE1:** `Φ = ρ·e^{iφ̄}` is a well-defined composition of two pre-existing causal-network
  fields (a positive Poisson causal density and the circular-averaged gauge phase), with
  no new parameter.
- **PE3:** `arg(Φ)=φ̄` behaves like the gauge field and gives it a **density-dependent mass**
  `m_A ∝ √ρ` (measured exponent 0.34, biased below the analytic 0.5 by the small-mass box
  floor; the propagator pole is exactly √ρ). This **reproduces AH2** (`m_A = e⟨|Φ|⟩` with
  `⟨|Φ|⟩ ∝ √ρ`) and is a genuine improvement on CR_HIGGS, whose real phase gave a *constant*
  gauge mass independent of the condensate.

### What did not (the negative)

- **PE2:** with no potential, `Φ` does **not** condense — ⟨|Φ|⟩=1 is the Voronoi
  normalisation (trivial), and the connected magnitude correlator decays at the cell scale.
  `C(r)` always decays; there is no long-range-ordered point.
- **PE4:** `|Φ|=ρ` is the **static causal-density substrate, decoupled from the gauge
  vortex**, so it never forms a core (dip −0.003 ± 0.014, σ_core undefined in 100% of
  seeds). Secondary: `arg(Φ)=φ̄` (a node average) does not even carry the winding (a loop
  holonomy; the compact-lattice 2π flux is CR_WILSON-invisible).
- **PE5:** the gauge collision stirs the phase but never makes `|Φ|` form a core (max dip
  0.001) — no stable matter from the composition alone.

### Triple verification for Veredito A

> **Not triggered.** Veredito A — the most important possible result of the whole
> investigation — requires PE4 (core dip) *and* PE5 (matter) to *both* pass. Both are
> negative, so **no A claim is made.** The honest result is C.

### The physical reason (what the abelian-Higgs needs that ρ is not)

The abelian-Higgs core requires `|Φ|` to be a **dynamical** field with the covariant kinetic
term `|Φ|²|D_μΦ|²`, which drives `|Φ|→0` at the vortex core and pins it. The bare causal
density ρ has no such term — it is the substrate, not a degree of freedom that can deplete.
So the composition captures the *phase* (gauge mass, PE3) but not the *dynamical magnitude*
(core, PE4/PE5). **This confirms CR_ABELIAN_HIGGS's honesty: the complex field's magnitude
was a genuine fourth ingredient, not something the minimal action already contained.**

## Output
`PE6_synthesis.py`, `PE6_synthesis.json`.
