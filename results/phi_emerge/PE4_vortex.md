# PE4 — The vortex core: does |Φ|=ρ dip and pin?

**Task.** Build a winding-1 gauge vortex (V=0) on the 3+1D lattice and measure the emergent
`Φ = ρ·e^{iφ̄}` around the core: (1) does the magnitude `|Φ|=ρ` dip toward 0 at the core (the
abelian-Higgs core that pins)? (2) does the phase carry the winding? Given PE2 (no
spontaneous condensate), the expected outcome is `|Φ| ≈ 1` everywhere — no core, no pinning.

## Results (20 seeds, grid 33×28×28, V=0)

**The decisive test — `|Φ|(r⊥)` radial profile about the core:**

| r⊥ (cells) | 0.5 | 1.5 | 2.5 | 3.5 | 4.5 | 6.5 | 8.5 |
|---|---|---|---|---|---|---|---|
| `|Φ|` | 1.003 | 1.001 | 1.000 | 0.999 | 0.999 | 1.000 | 1.000 |

- **Core dip depth `(|Φ|(∞)−|Φ|(0))/|Φ|(∞)` = −0.003 ± 0.014 — i.e. no dip at all.**
- **σ_core is undefined in 100% of seeds** (there is no sub-threshold region to measure).

**Secondary — the winding:**
- The gauge-sector holonomy `winding_planes = {xy:0, xz:0, yz:0}`: on the **compact**
  lattice the single vortex's 2π core flux **wraps to 0** — the CR_WILSON fact that a 2π
  quantum is invisible to the compact cosine.
- `arg(Φ) = φ̄` node winding around the core = 0.00 ± 0.00: φ̄ is a **node average** of link
  gradients, and a winding is a **loop holonomy** — a node average cannot carry it.

(See `PE4_vortex.png`: `|Φ|(r⊥)` is flat on the vacuum line 1.0 with no core.)

## Verdict (PE4)

> **No core, no pinning.** `|Φ| = ρ` is the bare causal density, **decoupled from the gauge
> vortex**, so it stays ≈ 1 at the core (dip ≈ 0; σ_core undefined). There is nothing to pin.
> This is the precise diagnosis of what the emergent composition lacks relative to
> CR_ABELIAN_HIGGS: there, the complex Higgs **magnitude** is a genuine dynamical degree of
> freedom whose covariant kinetic term `|Φ|²|D_μΦ|²` forces |Φ|→0 at the core and pins it.
> Here the magnitude is the static substrate density — it never develops a core.
>
> Secondary: `arg(Φ)=φ̄` does not even carry the vortex winding (it is a loop holonomy; the
> compact-lattice 2π flux is CR_WILSON-invisible). So the emergent Φ reproduces neither the
> abelian-Higgs magnitude core nor a node-phase vortex.
>
> **Since |Φ| does not dip, PE5 (collision) is N/A for a pinning/Veredito-A claim.**

## Output
`PE4_vortex.py`, `PE4_vortex.json`, `PE4_vortex.png`.
