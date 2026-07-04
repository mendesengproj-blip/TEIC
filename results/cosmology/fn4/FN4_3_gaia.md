# FN4-3 — Confronto com Gaia DR3 / Chae+2023

> `FN4_3_gaia.py` → `FN4_3_gaia.json` + `FN4_3_gaia.png`.
> Chae 2023 (arXiv:2309.08160): 26.615 binárias largas do Gaia DR3, dentro de 200 pc.

## As separações de Chae — VERIFICADAS (charter FN4-3, passo crítico)

```
Amostra:           26.615 binárias, distância < 200 pc do Sol
Faixa de separação: 200 – 30.000 au = 0.00097 – 0.145 pc
Início da anomalia: s ≳ 2 kau (g ≲ 10⁻⁹ m/s²)
Resultado:          γ = 1.43 ± 0.06  (boost de aceleração, deep-MOND com EFE)
```

**Confirmado: as separações de Chae são TODAS sub-parsec** (a mais larga, 30.000 au =
0.145 pc, é apenas **0.84% de λ_A = 17.3 pc**). Elas estão profundamente DENTRO da zona
blindada da DEV.

> Nota sobre a conversão do texto-fonte: o charter escreveu "2–30 kpc → 0.01–0.15 pc",
> misturando kau e kpc. A faixa correta é **0.2–30 kau = 0.001–0.145 pc** (verificada na
> literatura). A conclusão (sub-pc, ≪ λ_A) é a mesma.

## Blindagem da DEV no regime de Chae

```
   s [au]   s/λ_A     S(r)    boost_DEV  boost_MOND   % do boost MOND mantido pela DEV
    200    0.00006  0.00006    1.0000     1.0000      0.00%  (< r_MOND: newtoniano de qq forma)
   2000    0.00056  0.00056    1.0000     1.0135      0.06%
   7031    0.00197  0.00197    1.0005     1.2772      0.20%  (= r_MOND, onset MOND)
  10000    0.00280  0.00280    1.0009     1.3311      0.28%
  30000    0.00841  0.00837    1.0030     1.3558      0.84%
```

Em **toda** a faixa de Chae a DEV mantém **< 1%** do reforço MOND → prevê
**γ_DEV ≈ 1.001 (Newton)**.

## A tensão

```
DEV prevê (zona blindada):   γ ≈ 1.00  (gravidade newtoniana)
Chae mede:                   γ  = 1.43 ± 0.06
Tensão:                      (1.43 − 1.00)/0.06 ≈ 7.1 σ
```

Se o sinal de Chae for real, ele é **exatamente a condição de MORTE pré-registrada**:
"sinal MOND abaixo de 17 pc com a mesma amplitude que acima, sem blindagem detectável".

## É o teste correto?

**SIM como discriminador, mas testa o platô blindado, não a transição.** As binárias de
Chae caem onde DEV (→Newton) e MOND (→1.36) **mais divergem** (FN4-2). Portanto é um
teste limpo e poderoso da blindagem — só que da *parte de baixo* do degrau, não do
joelho em 17 pc.

## Por que ainda é TENSÃO (C) e não MORTE (D) declarada

O resultado de binárias largas é **observacionalmente contestado**:

- Chae 2023 e Hernandez et al.: detectam quebra MOND (γ > 1).
- Banik et al. 2024, Pittordis & Sutherland: análises com modelagem de triplos/
  companheiras ocultas favorecem **GR/Newton** (γ ≈ 1) nas mesmas separações.

A previsão da DEV (binárias largas **newtonianas**) coincide com o campo do *não-sinal*
(Banik/Pittordis). Ou seja: a DEV não está isolada contra os dados — ela toma um lado de
uma disputa observacional ainda aberta. Por isso o veredito é **C (tensão)**, que vira
**D (morte)** se o sinal de Chae se confirmar robusto, ou **sobrevivência silenciosa** se
o campo newtoniano vencer.

## Regime relevante para testar λ_A = 17 pc

O joelho da transição está em s ~ 5–50 pc. Gaia cataloga binárias **ligadas** só até
~1 pc (resolução + confusão de campo + maré). Logo, o regime do teste limpo **não** é
coberto por binárias ligadas — ver FN4-4.

## Resultado FN4-3

Separações de Chae no regime de blindagem: **SIM** (≪ λ_A). Chae compatível com DEV:
**NÃO** (γ=1.43 vs γ_DEV≈1.00, 7.1σ), porém contestado. Regime relevante para λ_A:
**s ~ 5–50 pc**, inacessível a binárias ligadas.
