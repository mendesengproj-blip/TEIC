# DBI1 -- Propagador cos e validação obrigatória

A ação mínima `S = Σ Δτ[1−cos(φ+Δθ)]` tem EOM sine-Gordon de rede; a força é
`force_cos = d/dx[sin(Δθ)]`. Validação antes de qualquer colisão (parar se falhar):

## (A) Campo fraco reproduz BD

| amp | max rel diff (cos vs linear) |
|-----|-------------------------------|
| 0.005 | 1.19e-08 |
| 0.010 | 4.74e-08 |
| 0.020 | 1.90e-07 |
| 0.040 | 7.59e-07 |
| 0.080 | 3.04e-06 |

Escala como `rel ~ amp^2.00` (esperado ~2; correção principal sin(u)−u = −u³/6).

## (B) Estático reduz a D3

Solução estática de campo fraco: amplitude 1/r A = 0.979, expoente da cauda = -0.990 (esperado −1) → θ ~ 1/r.

## (C) Conservação de energia (propagação livre)

Energia cos: 0.0738 → 0.0738, deriva 8.5e-06.

## VERDICT DBI1: VALIDADO

The cos propagator is consistent: it reproduces the linear BD evolution in weak field (rel diff 1e-08 at amp=0.005, scaling ~ amp^2.0), its static weak-field limit is D3's 1/r potential (tail exponent -0.99), and the symplectic integrator conserves the cos energy (drift 8e-06). DBI3 may proceed.
