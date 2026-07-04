# E2 — energy conservation as a Noether test (novo)

**Verdict: C** — energy is *conditionally* conserved (static regime only), broken by
network growth; only approximately additive. An honest, anticipated result.

## Question
Noether: a conserved energy exists iff the dynamics has time-translation symmetry.
Does the causal network have that symmetry?

## Method (ρ₀=12, T=10, X=12, 8 slabs, 20 seeds)
1. **Substrate symmetry** — events per equal-duration time-slab for (i) uniform ρ and
   (ii) growing `ρ(t)=ρ₀(1+t)` (a Classical-Sequential-Growth proxy, by thinning).
2. **Energy additivity** — quadratic field-energy proxy `E[θ]=Σθ²` for two lumps,
   separated vs co-located, via the retarded kernel; cross-term `E[θ₁+θ₂]−E₁−E₂`.

## Results
- Uniform ρ: slab-count **CV = 1.6 %** (flat → time-translation symmetry present).
- Growing ρ(t): slab count **rises +21 %/slab** (symmetry broken).
- Energy cross-term: **+0.34 ± 0.01** for nominally *separated* sources,
  **+1.00 ± 0.00** for *co-located* sources.

## What it means
A static uniform sprinkling **is** statistically time-translation invariant, so a
conserved count-based quantity can exist — but a **growing** network (CSG) breaks
that symmetry, so there is **no exactly conserved energy** once the network grows.
The field energy is only **approximately additive**: even nominally separated sources
develop a cross-term because their **forward light cones overlap downstream** (0.34),
rising to maximal (1.00) for co-located sources; strict `E_tot=E₁+E₂` holds only
before the cones meet. Energy thus emerges as **approximately conserved in the static
regime** — not an exact Noether charge. Exactly as the protocol anticipated.
