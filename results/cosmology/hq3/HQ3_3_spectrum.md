# HQ3-3 — Forma espectral: linha do m_A vs lei de potência do NANOGrav

> Mesmo que frequência e amplitude coincidissem, a **forma** do espectro precisa
> bater. Aqui ela não bate — e isso é decisivo.

## O que o NANOGrav mediu

Um fundo **estocástico, de banda larga**, com correlação angular de Hellings–Downs e
densidade espectral de potência (PSD) de resíduos de tempo

```
P(f) ∝ f^(−γ),   γ = 13/3 ≈ 4.33   ⇒   h_c(f) ∝ f^((3−γ)/2) = f^(−2/3)
```

O índice 13/3 e a inclinação −2/3 do strain são a assinatura de **fusões de buracos
negros supermassivos** (SMBH) — a interpretação dominante.

## O que o m_A produz

Um condensado coerente oscila com uma **única** frequência. O sinal é uma **linha**
em f_GW = 2m_A c²/h, alargada apenas pela dispersão de velocidades da DM:

```
Δf/f ~ (v/c)² ~ 10⁻⁶   ⇒   linha ultraestreita
```

Para m_A = 10⁻²³ eV: f_GW = 4.84×10⁻⁹ Hz, Δf ≈ 4.8×10⁻¹⁵ Hz. O caráter **vetorial**
(3 polarizações) adiciona uma modulação O(1) de stress anisotrópico, mas **não**
transforma a linha num contínuo.

## Comparação

| | NANOGrav 2023 | m_A (DEV) |
|---|---|---|
| forma | lei de potência de banda larga | linha monocromática |
| índice | γ = 13/3 ≈ 4.33 | γ → ∞ (linha) |
| largura | ~uma década em f | Δf/f ~ 10⁻⁶ |
| correlação | Hellings–Downs (quadrupolar) | monopolar/dipolar (relógio comum) |

Uma linha alargada por velocidade (Δf/f ~ 10⁻⁶) **não pode imitar** uma lei de
potência γ = 13/3 que se estende por uma década em frequência. São observáveis de
naturezas opostas: contínuo vs raia.

## Resposta HQ3-3

| Pergunta | Resposta |
|---|---|
| Espectro do m_A compatível com o SGWB γ=13/3? | **NÃO** |
| Índice espectral do m_A | linha (γ→∞), não lei de potência |
| Índice do NANOGrav | γ = 13/3 = 4.33 |

A forma sela o ponto: o NANOGrav 2023 detectou um **contínuo**; o m_A é uma **linha**.
O m_A não é — e não pode ser — a origem do fundo estocástico reportado. O que ele
oferece é um observável **diferente** (uma raia de PTA), que se distingue do SGWB
justamente por essa forma.

Figura: [`HQ3_3_spectrum.png`](HQ3_3_spectrum.png) — a linha do m_A (vermelho, raia
estreita) sobre a lei de potência de banda larga do NANOGrav (azul) na banda do PTA.
