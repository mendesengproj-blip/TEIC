# PE1 — Is the emergent field Φ = ρ·e^{iφ̄} well-defined? (the gate)

**Task.** Define, on the cr3d 3+1D lattice, the composite
`Φ_i = ρ_i · e^{i φ̄_i}` from two fields the network already carries —

- `|Φ_i| = ρ_i` = local **causal density**: a 4D Poisson sprinkle is assigned to the
  nearest spatial lattice node (Voronoi cell, y,z periodic), `ρ_i = N_i/⟨N⟩` (a pure
  count, no formula);
- `arg(Φ_i) = φ̄_i` = **circular mean of the incident gauge link phases** at node i
  (`atan2(Σ sin φ, Σ cos φ)` — real arithmetic, no complex literal).

Φ is stored as two real arrays `(Re, Im) = (ρ cosφ̄, ρ sinφ̄)`. **PE1 is the gate**: if Φ
is not well-defined the campaign stops.

## Results (20 seeds, hot/disordered gauge vacuum, grid 29×20×20)

| ρ_sprinkle | ⟨N⟩/cell | empty-cell frac | ⟨ρ⟩ | std(ρ) | [expected 1/√⟨N⟩] | arg χ²/dof |
|---|---|---|---|---|---|---|
| 2.0 | 16.0 | 0.0000 | 1.0000 | 0.250 | 0.250 | 1.14 |
| 4.0 | 32.0 | 0.0000 | 1.0000 | 0.177 | 0.177 | 1.13 |
| 8.0 | 64.0 | 0.0000 | 1.0000 | 0.125 | 0.125 | 1.32 |
| 16.0 | 127.9 | 0.0000 | 1.0000 | 0.089 | 0.088 | 1.21 |

- **(1) ρ_i ≥ 0, never empty here.** A Poisson Voronoi cell *can* be empty in principle,
  but at these densities the empty-cell fraction is 0 to 4 decimals; it is a **resolution
  knob** (→0 as ρ_sprinkle grows), not a pathology.
- **(2) φ̄_i defined everywhere.** Node degree ∈ {5,6} on this lattice (≥1 always), so the
  circular mean is always defined.
- **(3) |Φ| = ρ fluctuates about 1 with spread exactly 1/√⟨N⟩.** ⟨ρ⟩ = 1.0000 by
  normalisation, and the measured std (0.250, 0.177, 0.125, 0.089) matches the Poisson
  prediction 1/√⟨N⟩ to three decimals — a clean confirmation that |Φ| is a genuine
  Poisson causal-density field.
- **(4) arg(Φ) = φ̄ is uniform on [−π,π]** in the bulk (reduced χ² ≈ 1.1–1.3). *Honest
  caveat:* the two Dirichlet x-end slices have a link pinned to 0 (`phix[0]=phix[-1]=0`),
  which biases their φ̄ toward 0; the test is therefore run on the interior x-slices,
  where Φ's phase is uniform as required.
- `max | |Φ| − ρ | = 4.4×10⁻¹⁶` over all runs (Φ correctly reconstructed from two real
  arrays; no complex number anywhere).

## Verdict (PE1)

> **WELL-DEFINED.** `Φ = ρ·e^{iφ̄}` is a valid composition of two pre-existing causal-network
> fields: a positive Poisson causal density for the magnitude and the gauge Stückelberg
> phase (circular-averaged) for the argument. No new parameter was introduced. **The gate
> is open — PE2–PE6 may proceed.**

## Output
`phi_emerge_core.py`, `PE1_definition.py`, `PE1_definition.json`.
