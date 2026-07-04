# PHI_EMERGE — Can the complex Higgs field Φ emerge from the causal network?

CR_ABELIAN_HIGGS added a complex scalar Φ **by hand** (an honest fourth ingredient) and
reached Veredito A: stable matter with the complex field. The sharpest question left open is
whether Φ was *new* physics or merely a **composition** of two fields the network already
carries:

> **Φ_i = ρ_i · e^{i φ̄_i}**, with `|Φ| = ρ` the local **causal density** and `arg(Φ) = φ̄`
> the mean **gauge (Stückelberg) phase** — both pre-existing.

If this composition condenses, gives the gauge a mass `m_A = e·v`, and pins a vortex, then Φ
*emerged*. If not, the complex field was a genuine extra ingredient. Everything below uses
**two real arrays** (no complex literal), **counts** for ρ, the existing gauge links for φ̄,
and **20 seeds**. Code/data: `results/phi_emerge/`.

## Scorecard

```
PE1 — Φ = ρ·e^{iφ̄} well-defined:        SIM
PE2 — Condensado espontâneo (V=0):       NÃO        (C(r) sempre decai)
PE3 — m_A vs ρ:                          SIM, m_A ∝ √ρ  (p_medido 0.34, polo analítico 0.5)
PE4 — |Φ|(0) < |Φ|(∞) no vórtice:        NÃO        (sem núcleo)
PE4 — σ_núcleo = constante:              NÃO        (núcleo indefinido)
PE5 — Matéria estável sem axioma extra:  NÃO / N/A
```

## VEREDITO: **C** — Φ emergente gera m_A mas não pina

> **The composition captures the *phase* sector of an abelian-Higgs field but not the
> *magnitude* sector. Partial mechanism: the complex field of CR_ABELIAN_HIGGS is still
> required for the vortex core and pinning.**

### Why C, step by step

- **PE1 (gate, passed):** `Φ = ρ·e^{iφ̄}` is well-defined — `ρ_i = N_i/⟨N⟩ ≥ 0` (a Poisson
  count, ⟨ρ⟩=1, σ = 1/√⟨N⟩ exactly), `φ̄` defined at every node (deg ∈ {5,6}), `arg(Φ)`
  uniform in the hot vacuum. No new parameter.
- **PE2 (no condensate):** with no potential, the connected magnitude correlator decays at
  the cell scale (ξ ≈ 3–5); ⟨|Φ|⟩=1 is the Voronoi normalisation, not a VEV. **C(r) always
  decays** — no spontaneous condensate, no KT point.
- **PE3 (positive — mass emerges):** `arg(Φ)=φ̄` behaves like the gauge field and gives it a
  **density-dependent mass m_A ∝ √ρ** (measured exponent 0.34, biased below the analytic
  pole 0.5 by the small-mass box floor). This **reproduces AH2** (`m_A = e⟨|Φ|⟩`, `⟨|Φ|⟩∝√ρ`)
  and beats CR_HIGGS, whose real phase gave a *constant* gauge mass.
- **PE4 (negative — no core):** `|Φ|=ρ` is the **static causal-density substrate, decoupled
  from the gauge vortex**, so it never dips at the core (dip −0.003 ± 0.014; σ_core undefined
  in 100% of seeds). Secondary: `φ̄` (a node average) cannot carry the winding (a loop
  holonomy; the compact-lattice 2π flux is CR_WILSON-invisible).
- **PE5 (negative — no matter):** a gauge collision stirs the phase but never makes `|Φ|`
  form a core (max dip 0.001). No stable structure from the composition alone.

### Triple verification for Veredito A — **not triggered**

Veredito A would be the single most important result of the whole investigation and so
requires PE4 (core) **and** PE5 (matter) to *both* pass. **Both are negative**, so **no A
claim is made.** This discipline is the point: the temptation to read PE3's genuine positive
(an emergent gauge mass) as "Φ emerged" is resisted because the magnitude sector fails.

### The physics the audit clarifies

The abelian-Higgs core needs `|Φ|` to be a **dynamical** field with the covariant kinetic
term `|Φ|²|D_μΦ|²` that drives `|Φ|→0` at the core and pins it. The bare causal density ρ has
no such term — it is the substrate, not a degree of freedom that can deplete. So
`Φ = ρ·e^{iφ̄}` captures the phase (gauge mass) but not the dynamical magnitude (core).

> **This confirms CR_ABELIAN_HIGGS was honest and correct: the complex field's *magnitude*
> was a genuine fourth ingredient, not something the minimal action already contained. The
> emergent composition reaches the gauge-mass frontier (a real, density-dependent m_A) and
> stops exactly where a dynamical |Φ| would be needed. The boundary CR_AH drew is
> confirmed — and now we know *which half* of Φ emerges (the phase) and which does not (the
> magnitude).**

## Per-task detail
`results/phi_emerge/PE1_definition.md` … `PE6_synthesis.md`, with `phi_emerge_core.py`,
JSON, and figures (`PE2_condensate.png`, `PE4_vortex.png`). Reproduce each with
`python results/phi_emerge/PE<n>_*.py`.
