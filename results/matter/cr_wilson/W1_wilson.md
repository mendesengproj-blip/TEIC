# W1 -- Ação completa (Stückelberg + Wilson) e validação obrigatória

Ação `S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` numa rede espacial **2D** (x = eixo de colisão, extremos fixos; y = transverso, periódico). Quatro verificações antes de W2–W6 (parar se falhar):

## (1) λ_p=0 reproduz CR_GAUGE exatamente
Config y-uniforme, λ_p=0: diferença por linha vs motor 1D = θ 0.0e+00, φx 0.0e+00; permanece y-uniforme (0.0e+00) → **ok = True**.

## (2) θ=0, λ_p>0 → pure gauge (Maxwell estático)
Config pure-gauge (φ=∇χ): W_p = 0.0e+00 e força de Wilson sobre ela = 8.3e-17 (nula → estática). Fluxo magnético relaxa 398.69→0.00 sob amortecimento (termo magnético de Maxwell) → **ok = True**.

## (3) Kink isolado com λ_p>0: massa ≈ 8
Kink y-uniforme tem W_p=0 → Wilson não altera a auto-energia: massa 7.996 → 7.996 (fluxo no kink 0.0e+00, contagem 1) → **ok = True**.

## (4) Conservação de energia (E_links + E_plaquetas)
Deriva = 7.8e-04 (< 1%) → **ok = True**.

## VERDICT W1: VALIDADO

The full action is consistent. (1) lambda_p=0 reproduces CR_GAUGE exactly (row diffs 0e+00). (2) A pure-gauge config has W_p=0 and feels zero Wilson force; magnetic flux relaxes (398.69->0.00) -- the lattice Maxwell term. (3) A y-uniform kink has W_p=0, so Wilson leaves its rest mass 8 untouched (7.996, stable). (4) E_links+E_plaquettes is conserved (drift 8e-04 < 1%). W2-W6 may proceed.
