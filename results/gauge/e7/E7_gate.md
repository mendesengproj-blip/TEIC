# E7 — validation gates G1 / G2 (synthesis)

> Pre-registered in `E7_COULOMB_PHASE.md` ("GATE DE VALIDAÇÃO — obrigatório antes de
> medir física"). Reuses the E5 engine and gate functions verbatim (`e5_core`,
> `e5_fast`, `E5V_gate.gate_G1`, `E5V_gate.scan_specific_heat`). Code: `E7_gate.py`,
> data: `E7_gate.json`. Run jun/2026 (89 s).

## Results

| Gate | Test | Result |
|---|---|---|
| **G1** | gauge invariance — random local transform leaves every plaquette holonomy fixed | **PASS** |
| **G2** | 4D U(1) deconfinement transition near β_c≈1.01 (specific-heat peak) | **PASS** |

### G1 — gauge invariance (exact, three substrates)

```
regular 4D (3^4) : max|Δcos| = 1.8e-15
regular 3D (4^3) : max|Δcos| = 1.8e-15
causal DIAMONDS  : max|Δcos| = 3.3e-15   (n=319 events, 5045 diamond plaquettes)
```

The same per-node transform θ_(a,b) → θ_(a,b) + λ_b − λ_a that left the regular-lattice
plaquettes invariant also leaves the **causal-diamond** plaquette holonomies invariant to
machine precision — the diamond loops are genuinely closed and the U(1) gauge structure on
the causal set is exact. This reproduces E5-V/G1 (1.8e-15) and E5-1 step 0 (1.8e-15).

### G2 — 4D transition reproduces β_c≈1.01

```
specific-heat proxy C(β) on a 4^4 lattice peaks at  β = 1.00
known compact-U(1) value  β_c ≈ 1.01   (Guth/Jersák/DeGrand-Toussaint)
E5-V/G2 found              β = 1.00
```

The engine reproduces the canonical 4D confinement→Coulomb transition coupling, identical
to E5-V. The motor that will measure Wilson loops is the validated one.

## Decision

Both gates **PASS** → the charter's gate ("if G1 or G2 fail, STOP") is cleared. The E7
Wilson-loop area-law / perimeter-law measurement may run on the same engine. No engine was
rebuilt; E5's motor is reused unchanged.
