# LAMBDA_EVERPRESENT: Λ flutuante com coeficiente medido na rede

## ✅ VEREDITO: **cadeia fechada — coeficientes medidos; herança CST citada, nunca confundida** (morte NÃO ativada)

```
L1  δρ/ρ·√(ρV) = 0.971±0.05 (pred. 1; 200 sementes — a 1ª rodada de 20 deu
    0.88, dentro de 1σ amostral; correção foi estatística, não de modelo)
L2  fonte uniforme → quadrático puro R²=0.9999; β medido 5.218±0.015 vs 5.203
    calibrado por CR1b (razão 1.003 — SEM fit novo; 3º uso independente da
    mesma constante de transporte)
L3  transplante V_Hubble ⇒ Λ_rms ~ 10⁻¹²², sinal flutuante — herança CST
    (Sorkin; ADGS 2004), citada como tal
```
Síntese: [`results/bridge/lambda/L3_synthesis.md`](results/bridge/lambda/L3_synthesis.md).

> Ataque 8 do `ROADMAP_REVOLUCAO.md`. A previsão famosa da CST (Sorkin, anos 90,
> pré-1998): Λ flutua com ±1/√V no volume de Hubble — ordem de grandeza correta
> do Λ observado. **Herança declarada** (Sorkin; Ahmed–Dodelson–Greene–Sorkin
> 2004). O que a TEIC adiciona: a maquinaria de resposta gravitacional D1–D3/CR1
> permite MEDIR o coeficiente que liga a flutuação de densidade ao termo de Λ
> efetivo — onde a literatura tem estimativa dimensional, a rede dá um número.
> Resultados em `results/bridge/lambda/`. NÃO modifica campanhas anteriores.

## A cadeia (cada elo medido ou citado, nunca confundidos)

```
(L1) Poisson: flutuação de densidade regional  δρ/ρ = 1/√(ρV)
     [exato para N~Poisson; coeficiente 1 — baseline a confirmar]
(L2) resposta da rede a uma fonte UNIFORME j: potencial QUADRÁTICO
     θ(r) = β(R²−r²)-tipo (a forma de de Sitter estático), com β fixado pelo
     MESMO coeficiente de transporte medido em CR1/CR1b — loop de consistência
(L3) transplante dimensional (herança CST, citada): V_Hubble ~ 10^244 ℓ_Pl⁴
     → Λ_rms ~ 1/√V ~ 10^−122 m_Pl² — a ordem do Λ observado; sinal flutuante
```

## PREVISÕES PRÉ-REGISTRADAS

```
L1: rms(δN/N)·√(ρv) = 1.00 ± 0.05 nos raios testados (N total ~ Poisson)
L2: perfil quadrático com R² > 0.99; coeficiente medido
    β/j = (15/12π)·κ/(ρ r_c⁵), com κ = 1.066 a deg=48 (a correção de grau
    finito MEDIDA em CR1b — não um fit novo): acordo dentro de 10%
```

## CRITÉRIO DE MORTE (pré-registrado)

```
L2 morre se o perfil não for quadrático (R²<0.99) ou se β desviar >10% da
previsão calibrada por CR1b — i.e., se a resposta a fonte uniforme NÃO for
governada pelo mesmo transporte da resposta pontual (quebra de linearidade
que o D3-audit diz não existir).
```

## Tarefas

```
L1: flutuações Poisson em volumes aninhados, 20 sementes → L1_fluct.{py,md,json}
L2: Lθ = j·𝟙 (fonte uniforme), perfil quadrático, β vs CR1b → L2_response.{py,md,json,png}
L3: síntese + transplante dimensional honesto → L3_synthesis.md
```

## Honestidade pré-declarada

- A ordem 10^−122 é da CST, não nossa; o sinal flutuante também. O que é da
  TEIC: o **coeficiente de resposta medido** (β via CR1b) e o loop de
  consistência fonte-pontual ↔ fonte-uniforme no mesmo substrato.
- Isto NÃO é um modelo de energia escura dinâmica (sem evolução temporal aqui);
  é a estática da resposta + a estatística de Poisson + o transplante citado.
