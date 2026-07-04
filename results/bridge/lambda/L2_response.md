# L2 — Resposta a fonte uniforme: o potencial quadrático com coeficiente de CR1b

> Task L2 of `LAMBDA_EVERPRESENT.md`. `Lθ = j·𝟙` no Laplaciano de grafo
> (N=80000, deg=48 — o mesmo regime calibrado de CR1b), casca de Dirichlet,
> 5 sementes. Data: `L2_response.json`; figura: `L2_response.png`.

## Verdict: **quadrático a R² = 0.9999, coeficiente a 0.3% do valor calibrado por CR1b — loop de consistência fechado; morte NÃO ativada**

```
perfil:    θ(r) = α − β r²        R² médio 0.99994 (mínimo 0.99991)
β medido:  5.218 ± 0.015
β previsto (calibração CR1b, κ=1.066 a deg=48, SEM fit novo):  5.203
razão:     1.003   (banda pré-registrada: ±10%)
```

## O que estabelece

1. **A forma:** uma fonte uniforme (o análogo estático de uma densidade de
   energia homogênea — um termo de Λ) produz na rede exatamente o potencial
   quadrático de de Sitter estático, θ ∝ (R²−r²), com pureza R²=0.9999.
2. **O coeficiente não é novo:** β é previsto pelo **mesmo** coeficiente de
   transporte medido em CR1b para a fonte pontual (incluindo a correção de
   grau finito κ=1.066), e bate a 0.3%. Fonte pontual (1/r) e fonte uniforme
   (r²) são respostas do mesmo operador com a mesma constante — a linearidade
   que o D3-audit estabeleceu, agora fechada entre dois regimes de fonte.
3. **A cadeia de Λ fica quantitativa:** combinando L1 e L2, uma flutuação
   regional de densidade j = δρ/ρ = 1/√(ρV) induz um termo quadrático com
   β = (15κ/12π)·j/(ρ r_c⁵) — **cada fator medido** (coeficiente 1 de L1;
   transporte de CR1b; pureza quadrática de L2). Onde a literatura tem
   estimativa dimensional, a rede dá a constante.
