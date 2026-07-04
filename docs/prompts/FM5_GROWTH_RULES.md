# FM5_GROWTH_RULES — a morte do e7 generaliza para outras FORMAS de regra de crescimento?

> **Charter PRÉ-REGISTRADO.** Item 14 da Seção 6 do `RESEARCH_MAP.md` e FM5 de
> `FUTURE_EXPERIMENTS.md`. Pré-requisitos prontos: motor Tier-3 (`tier3_core.py`,
> gate T3V passado), T3A/T3B (morte do e7: d*≈1.43, não-manifold).
>
> Script: `results/tier3/FM5_growth_rules/FM5_growth_rules.py`. **NÃO modifica nada.**

## Correção de premissa (declarada)

O **varrimento do acoplamento** w_meet já foi feito em **T3A-3** (N=500,
w_meet∈{0.2,0.333,0.5,1,2,3} → d_MM ∈ 1.25–1.48, nenhum perto de 4). Portanto FM5
**não** re-varre w_meet. O que é genuinamente novo é variar a **FORMA FUNCIONAL** da
regra: T3A usou a forma binária do e7 — w(I) = w_meet se ncomp≥2, senão 1 — que **não
distingue 2 de 10 componentes**. A família Rideout–Sorkin/CSG tem formas mais ricas.

## A pergunta

Existe alguma FORMA de regra de crescimento (na subfamília graduada por número de
componentes) que produza um causet **manifold-like com d* → 4**, ou a morte do e7
(d*≈1.43, não-manifold) **generaliza** para a família?

## As regras testadas (formas, não só acoplamentos)

```
R0  binária (e7):       w(nc) = w_meet  se nc>=2, senão 1     [anchor, reproduz T3A]
R1  graduada-penaliza:  w(nc) = a^(nc-1),  a<1  (0.33)        [penaliza CADA componente
                                                              -> favorece cadeia -> d baixo]
R2  graduada-premia:    w(nc) = c^(nc-1),  c>1  (2, 3, 5)     [premia CADA componente ->
                                                              favorece anticadeia larga ->
                                                              o CANDIDATO a d ALTO]
```

A regra R2 (premiar componentes) é o teste decisivo: se **nenhuma** intensidade de
prêmio levar d→4 com manifold-likeness, a morte é robusta à forma da regra, não só ao
acoplamento.

## Manifold-likeness (o teste de T3A)

Num sprinkling de variedade, d_MM(intervalo) ≈ d_MM(global) (controles T3A-2: batem).
Num causet não-manifold eles DIVERGEM (T3A: 1.43 vs 2.43). Reporto ambos; manifold-like
exige concordância **e** d* estável.

## CRITÉRIOS DE MORTE (pré-registrados)

```
GATE G0: R0 (e7) reproduz d*≈1.4 de T3A (sanidade do motor/forma).

MORTE (a morte do e7 GENERALIZA): toda regra R1/R2 testada dá
  d_MM(intervalo) longe de 4 (|d*-4|>1) E/OU não-manifold (|d_int-d_glob|>0.5).
  -> confirma T3A/T3B na subfamília graduada; a dimensão não emerge de NENHUMA
     destas formas.

SUCESSO (surpresa): alguma regra dá d* → 4 (|d*-4|<0.5) com d_int≈d_glob
  (manifold-like, |d_int-d_glob|<0.5), estável em N.
  -> a dimensão 4 emergiria de uma forma de regra específica; resultado maior.
```

## HONESTIDADE / ESCOPO (declarado)
Testa a subfamília **graduada por número de componentes** (uma extensão genuína da
forma binária do e7), **não** a família CSG completa de Rideout–Sorkin (sequência de
acoplamentos t_n) — essa fica como passo maior. O sampler MCMC e a contagem de
componentes são validados pelo gate T3V (independente da regra; só a razão de
aceitação Metropolis muda, com balanço detalhado preservado para qualquer w(nc)).
Sementes fixas; sem alvo d=4 no gerador (anti-circularidade); JSON auto-descritivo.
