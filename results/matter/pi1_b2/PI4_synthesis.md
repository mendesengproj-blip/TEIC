# PI4 — Síntese: a identificação FR (troca ≅ rotação-2π) está MEDIDA na rede

> Fecha `MATTER_PI1_B2.md`. Ordem real dos eventos documentada abaixo — incluindo
> a surpresa do PI3 cru e o calibrador PI0b declarado depois dela e antes de rodar.

## O resultado

| Loop | Topologia da pré-imagem | Leitura crua | ε (calibrado) | **Classe ℤ₂** | Previsto |
|---|---|---|---|---|---|
| constante (g1) | 1 curva, winding 1 | 0 | 0 | **0** | 0 ✓ |
| translação contrátil (g1b) | 1 curva, winding 1 | 0 | 0 | **0** | 0 ✓ |
| rotação 2π, B=1 (PI1) | 1 curva, winding 1 | 1 | 0 | **1** | 1 ✓ |
| rotação 4π, B=1 (PI1) | 1 curva, winding 1 | 0 | 0 | **0** | 0 ✓ |
| rotação 2π de UM sóliton, B=2 (PI2) | 2 curvas, winding 1 | 1 | 0 | **1** | 1 ✓ |
| rotação 2π do PAR, B=2 (PI2) | 2 curvas, winding 1 | 0 | 0 | **0** | 0 (Williams: B mod 2) ✓ |
| iso-rotação 2π, B=2 axial (PI0b, **classe conhecida 0**) | **1 curva, winding 2 (swap)** | 1 | — | calibrador: **ε_swap = 1** | 0 (Williams) |
| **troca, B=2 (PI3)** | **1 curva, winding 2 (swap)** | 0 | 1 | **1** | 1 ✓ |
| troca², B=2 (PI3) | 2 curvas, winding 1 | 0 | 0 | **0** | 0 ✓ |

**⇒ [troca] = [rotação-2π de um sóliton] = 1 ∈ π₁ = ℤ₂ — a identificação de
Finkelstein–Rubinstein/Williams é uma igualdade de dois números MEDIDOS na rede.**
Com a 2-torção (4π=0, troca²=0) e o espectro do composto (par=0) também medidos.

## A ordem real dos eventos (honestidade)

1. PI0 (pré-registrado) validou a maquinaria em topologia winding-1: g1, g1b,
   g4-refinamento — tudo verde.
2. PI1 e PI2 bateram TODAS as previsões pré-registradas (1,0,1,0).
3. **PI3 cru deu troca = 0** (estável nos 3 valores regulares, engenharia verde)
   — disparando o critério de morte pré-registrado.
4. A análise identificou o buraco no gate: a pré-imagem da troca é uma curva
   única enrolando o círculo-s DUAS vezes (as fitas trocam de lugar) — o
   primeiro caso multi-winding; o framing de referência (vetores constantes
   Gram-Schmidt contra a tangente) nunca fora validado nessa topologia.
5. **PI0b** (declarado APÓS a surpresa, ANTES de rodar, com leitura
   pré-fixada): calibrador de classe CONHECIDA com a mesma topologia — campo
   B=2 axial (azimute dobrado), loop de iso-rotação 2π; classe verdadeira
   = B mod 2 = 0 (Williams 1970, sem nenhum input FR). Pré-imagem: 2 fitas a
   φ₀, φ₀+π girando −πs cada ⇒ swap, winding 2 — confirmado (comps=1).
   **Medido: 1, estável ⇒ ε_swap = 1.** A regra pré-fixada: ε=1 ⇒ troca
   corrigida para 0⊕1 = 1 ⇒ FR confirmado.
6. Consistência interna sem custo extra: troca² tem topologia winding-1
   (2 curvas) e lê 0 cru = 0 verdadeiro ✓; PI2-par é ele próprio um segundo
   calibrador winding-1 de classe conhecida (Williams B mod 2 = 0) e lê 0 ✓.

## Condição declarada da correção — REDUZIDA por FQ2 (PI5)

ε_swap foi medido num único calibrador da mesma classe de topologia (hélice de
2 fitas com meia-volta, winding 2). A correção assume ε uniforme dentro dessa
classe — plausível (em 4D curvas fechadas não se atam; o desvio do framing de
referência depende da classe de isotopia enquadrada do winding-2), mas
ASSUMIDO, não provado. Um segundo calibrador independente de classe conhecida 1
e topologia swap fecharia o residual; não existe candidato barato (B=3 axial dá
winding 3, não 2). Reportado como condição, não escondido.

> **ATUALIZAÇÃO FQ2 (jun/2026, `PI5_synthesis.md`):** executado o calibrador
> B=3 axial (classe verdadeira **1** por Williams, sem input FR; winding-3).
> Gate anti-aliasing G1–G4 verde; classe medida = **1** = previsão. ⇒ **ε(3)=0**,
> selecionando a lei **ε(n)=(n−1) mod 2** (descartando ε≡1 ∀n≥2). Agora ε é uma
> **paridade de winding medida em n=1,2,3**, não ponto isolado: o ε(2)=1 do PI3
> é termo de lei coerente, e a maquinaria de PT está validada em multi-winding
> num calibrador classe-1 independente. Residual remanescente (menor): ε(2)
> entre campos winding-2 **distintos** não foi re-medido (precisaria de 2º campo
> grau-2). A ressalva spin-estatística está **reduzida**, não eliminada.

## O que mudou de status

| Peça | Antes (FR4) | Agora |
|---|---|---|
| loop de troca fecha | medido | medido |
| troca = meia-volta rígida ∘ isospin | medido | medido |
| 2π arrasta ao antípoda (W=1) | medido | medido |
| **troca ≅ rotação-2π em π₁(config B=2)** | **TEOREMA IMPORTADO** | **MEDIDO (ε-calibrado, condição declarada)** |
| π₄(S³)=ℤ₂ + completude Pontryagin–Thom | — | importado residual (topologia de livro-texto, sem conteúdo dinâmico) |
| quantização coletiva (W=1 → fase −1, j=½) | externa | externa (inalterado) |

A fronteira FR está agora no degrau mínimo possível para uma teoria clássica de
campos na rede: importa-se apenas a topologia algébrica geral e a regra de
quantização — todo o conteúdo FÍSICO da estatística fermiônica do sóliton é
medição.

## Notas de engenharia

- Calibrador PI0b: B discreto 1.59 (N=37) → 1.75 (N=49) → 1.83 (N=61) — vai a 2
  sob refinamento; subestimação do estimador no eixo (azimute dobrado), o campo
  é analiticamente de grau 2. Mesmo status do B=1.813 do FR1.
- Fechamento slerp da troca: dist máx 0.486 < 0.5 (critério pré-registrado) —
  válido, mas perto do limite; d=6 é a separação do FR1. Sob d maior o critério
  folga (e^{−d/2}).
- Matching de cadeias: vizinho-mútuo via cKDTree no mergulho periódico-s
  (R⁵); o bug de buckets de arredondamento do matching ingênuo foi pego pelo
  gate g4 ANTES de qualquer física (exatamente o papel do gate).

## Prior art

Finkelstein & Rubinstein 1968 · Williams 1970 (rotação de grau n ≅ n mod 2;
usado como classe conhecida do calibrador) · Friedman & Sorkin 1980 ·
Giulini 1993/95 · Pontryagin/Whitehead (π₄(S³)=ℤ₂, invariante completo).
