# PI5 (FQ2) — Síntese: segundo calibrador classe-1 confirma a lei ε(n)=(n−1) mod 2

> Fecha `FQ2_PI1_B3_CALIBRATOR.md`. Executa o único residual declarado em
> `PI4_synthesis.md`: ε_swap medido num único calibrador (PI0b, classe
> verdadeira 0). Aqui um **segundo calibrador independente, de classe verdadeira
> 1** (B=3 axial, Williams, sem input FR), com a previsão favorita batida.

## O resultado

**Calibrador:** campo axial de grau 3 (azimute triplo) sob a rotação-alvo
(isospin) 2π global. Classe verdadeira = B mod 2 = **3 mod 2 = 1** (Williams
1970; álgebra de suspensão, **nenhum input do teorema da troca FR**).
Pré-imagem: **curva única winding-3** (cobertura tripla — as 3 fitas azimutais
se permutam ciclicamente). Como a classe verdadeira é conhecida, a medição
**mede a anomalia diretamente:** ε(3) := classe_medida ⊕ 1.

| Resolução | y₁ | y₂ | y₃ | comps | \|winding\| | classe | min frame-dot |
|---|---|---|---|---|---|---|---|
| N=49 | 1 | 1 | 1 | 1 | 3 | **1** | 0.78 |
| N=61 | 1 | 1 | 1 | 1 | 3 | **1** | 0.87 |

**Gate (obrigatório, anti-aliasing) — TODOS verdes:**
- **G1** número bariônico: 2.041 → 2.382 → 2.573 → 2.690 (N=37,49,61,73),
  monótono; extrapolação 1/N→0 = **3.37** (claramente o limite 3, não 2 nem 4).
- **G2** topologia: comps=1, \|winding\|=3 em **todos** os valores regulares e
  ambas as resoluções — a cobertura tripla, descartando aliasing.
- **G3** estável: classe 1 nos 3 valores regulares.
- **G4** convergida: classe 1 idêntica em N=49 e N=61.
- Engenharia: todas as cadeias fecham; nenhuma na borda; frame-dot ≥ √0.5.

**⇒ classe_medida(B=3) = 1 = previsão pré-registrada (H_lin). ε(3) = 1⊕1 = 0.**

## A lei ε(n) — agora medida em três pontos

```
ε(1) = 0   (PI0 gate + PI1 + PI2 + troca² — muitos loops winding-1)
ε(2) = 1   (PI0b: classe verdadeira 0, medido 1)
ε(3) = 0   (PI5: classe verdadeira 1, medido 1)   ← ESTA CAMPANHA
```

Isto **seleciona H_lin: ε(n) = (n−1) mod 2** (o framing de referência por
vetores constantes acumula meia-torção por folha extra da cobertura; duas
folhas extra cancelam mod 2) e **descarta** H_sat (ε(n)=[n≥2], que previa ε(3)=1
⇒ classe_medida 0). A anomalia de framing é, portanto, uma **paridade de
winding bem-definida e preditiva**, não um artefato do campo particular do PI0b.

## O que isto fecha (e o que não fecha — declarado)

- **Fecha:** a maquinaria de Pontryagin–Thom dá leitura **reprodutível,
  convergente e topologicamente sensata** em pré-imagens multi-winding, validada
  agora num calibrador de **classe verdadeira 1** independente. O ε(2)=1 usado
  no PI3 deixa de ser ponto isolado: é o termo n=2 de uma lei medida em
  n=1,2,3. A correção FR do PI3 ([troca]=1) está apoiada em lei, não em
  coincidência.
- **Não fecha (residual menor, honesto):** B=3 é winding-3, não um segundo campo
  **winding-2**. A uniformidade de ε **entre campos winding-2 distintos** não foi
  re-medida (precisaria da Estratégia 2 — segundo campo grau-2, deferida). A
  ressalva spin-estatística é **reduzida** (de "ε medido uma vez, lei
  desconhecida" para "ε é anomalia de winding com lei medida"), não eliminada.

## Nota de engenharia (honestidade)

Primeira corrida marcou G2 como falha → "morte de maquinaria" espúria: o check
testava `winding == 3` literal, mas dois valores regulares percorrem a curva com
orientação oposta (winding **−3**). O sinal do winding é orientação de travessia
— topologicamente irrelevante; o invariante é \|winding\|=3. Check corrigido para
magnitude; medição (determinística, seed 421) reproduzida idêntica, gate verde.
Documentado como correção de engenharia, no espírito do bug de buckets de
matching pego pelo g4 no PI0.

## Prior art

Williams 1970 (rotação de grau n ≅ n mod 2 — classe verdadeira do calibrador) ·
Finkelstein–Rubinstein 1968 · Pontryagin/Whitehead (π₄(S³)=ℤ₂).
