# PE2 — Does Φ = ρ·e^{iφ̄} condense spontaneously? (no potential, V=0)

**Task.** With **no added potential**, measure over 20 seeds whether the emergent Φ
develops a spontaneous condensate: ⟨|Φ|⟩ and σ_|Φ| vs density, and the correlation
function C(r). The decisive distinction kept honest throughout:

- `⟨|Φ|⟩ = ⟨ρ⟩ = 1` is **trivial** (the Voronoi normalisation), not condensation.
- A genuine spontaneous condensate shows the **connected** correlator → const (long-range
  order) with no potential added.

## Results (20 seeds, V=0, grid 25×20×20)

| ρ_sprinkle | ⟨\|Φ\|⟩ | σ_\|Φ\| | magnitude C(r) | relaxed full C(r) |
|---|---|---|---|---|
| 2.0 | 1.000 | 0.250 | decays (ξ≈5.5) | decays |
| 4.0 | 1.000 | 0.177 | decays (ξ≈3.7) | decays |
| 8.0 | 1.000 | 0.125 | decays | decays |
| 16.0 | 1.000 | 0.088 | decays (ξ≈3.2) | decays |

- **⟨|Φ|⟩ = 1.000 at every density** — but this is the normalisation, not a VEV.
- **σ_|Φ| = 1/√⟨N⟩** exactly (Poisson), shrinking with density — the magnitude is a
  Poisson density field, not an order parameter.
- **The connected magnitude correlator C_|Φ|(r) decays** with a short correlation length
  (ξ ≈ 3–5 cells, comparable to the Voronoi cell scale) at every density. The magnitude
  does **not** develop long-range order.
- The full Φ correlator after gauge relaxation also decays (the cooled gauge orders its
  phase locally, the Stückelberg vacuum, but this is not a |Φ| condensate).

(See `PE2_condensate.png`: both |C_|Φ|(r)| and the relaxed full correlator fall below the
0.05 line within a few cells, with no plateau.)

## Verdict (PE2)

> **No spontaneous condensate.** Without a potential, `Φ = ρ·e^{iφ̄}` does **not** condense:
> ⟨|Φ|⟩ = 1 is the Voronoi normalisation (trivial), and the connected magnitude correlator
> decays at the cell scale (ξ ≈ 3–5) — the magnitude is a Poisson causal-density field, not
> an order parameter. Any plateau seen after relaxation is the gauge (Stückelberg) phase
> vacuum, not a |Φ| condensate.
>
> This matches CR_HIGGS exactly: condensation requires an added potential V (the mexican
> hat). The composition `ρ·e^{iφ̄}` carries a phase that behaves like the gauge field, but
> its magnitude is the bare substrate density and does not spontaneously order. **C(r)
> always decays — there is no Kosterlitz-Thouless or long-range-ordered point at V=0.**

## Output
`PE2_condensate.py`, `PE2_condensate.json`, `PE2_condensate.png`.
