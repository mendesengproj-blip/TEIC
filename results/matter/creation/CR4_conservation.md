# CR4 -- Conservação da taxa causal total na colisão

Energia causal total = taxa de eventos. Conservação medida por contagem:
`E_antes` (t < t_colisão) vs `E_depois` (t > t_colisão). Testa-se desbalanço
**sistemático** (média assinada ~0); o espalhamento por-semente é ruído de
contagem de Poisson (~1/√N), não perda física.

| ρ/ρ₀ | dE/E assinado (média) | rms (ruído Poisson) | N_loops tardios |
|------|------------------------|---------------------|------------------|
| 2 | -8.00% ± 3.33% | 16.6% | +0.00 ± 0.00 |
| 10 | -0.73% ± 1.82% | 8.0% | +0.00 ± 0.00 |
| 50 | +0.87% ± 0.98% | 4.3% | +0.00 ± 0.00 |
| 100 | -1.11% ± 0.62% | 2.9% | +0.00 ± 0.00 |

- maior desbalanço **sistemático**: **8.0%** (consistente com 0)
- N_loops escala com ρ? **False** (slope 0.000)
- criação em pares: **N/A (no loops created)**

## VERDICT CR4: SIM

The total causal rate is CONSERVED across the collision: the SIGNED before/after event-count imbalance is consistent with ZERO at every density (largest |mean| 8.0%, within 3 sigma of 0); the per-seed scatter is pure Poisson 1/sqrt(N) counting noise, not physical loss. This conservation is the flip side of LINEARITY -- the chains carry their events through unchanged. N_loops does NOT scale with density (late bound order parameter ~ 0 at every rho, slope 0.000), so 'more energy -> more loops' is refuted and pair creation is N/A (no loops created). The network neither creates nor dissipates events.

A conservação é o outro lado da **linearidade**: as cadeias atravessam-se
carregando seus eventos sem perda nem ganho. Como não há criação (CR3), não há
o que escalar com a energia nem pares a formar.
