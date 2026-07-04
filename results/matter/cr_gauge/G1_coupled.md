# G1 -- Dinâmica acoplada θ+φ e validação obrigatória

A ação completa `S = Σ Δτ[1−cos(φ+Δθ)]` com **ambos** os campos dinâmicos
(`gauge_core`). θ vive nos nós, φ (gauge, compacto) nos links; a combinação
invariante de Stückelberg é `u_i = φ_i + (θ_{i+1}−θ_i)`. Três verificações
obrigatórias antes de G2–G6 (parar se falhar):

## (A) Limite θ-puro (φ=0) reproduz DBI1/DBI3

- `force_theta(·, φ=0)` − `force_cos`: máx |diff| = 0.0e+00 (idêntico, propagação a velocidade unitária).
- Colisão escalar (gauge congelado): ψ_tardio = +0.002 → **pass-through = True** (o nulo escalar de DBI3).

## (B) Limite φ-puro (θ=0) reproduz DBI4

- `force_phi(θ=0, ·)` − `(1/dx²)·sine-Gordon`: máx |diff| interior = 0.0e+00 (idêntico a menos do fator global de tempo).
- Kink compacto explícito (winding 1): massa de repouso = 7.996 (teoria sine-Gordon 8); após T: contagem 1→1, **estável = True**.

## (C) Conservação de energia (propagação livre acoplada)

E_total = E_θ + E_φ + E_acoplamento: 7.345 → 7.341, deriva = **5.3e-04** (< 1%).

## VERDICT G1: VALIDADO

The coupled engine is consistent. theta-pure limit IS DBI's force_cos (force diff 0e+00) and a frozen-gauge collision passes through (psi_late 0.00 ~ 0, DBI3). phi-pure limit IS DBI's sine-Gordon (force diff 0e+00 interior); an explicit compact kink is STABLE with rest mass 7.996 (theory 8, DBI4). The symplectic integrator conserves the coupled energy E_theta+E_phi+E_coupling to 5.3e-04 (< 1%). G2-G6 may proceed.
