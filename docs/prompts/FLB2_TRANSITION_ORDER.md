# FLB2_TRANSITION_ORDER — a ordem da transição SU(3) em L>12

> **Charter PRÉ-REGISTRADO.** Item 15 da Seção 6 do `RESEARCH_MAP.md`; o resíduo que
> FLB deixou explícito e que o FLR re-flagou. FLB (L≤12) achou sinais MISTOS para a
> ordem da transição do ferromagneto de cor SU(3) (J_c≈2.65 cúbico) e a própria síntese
> de FLB recomendou: "L≥16, grade fina em J em torno de 2.65, histogramas longos em J_c".
>
> Motor: `su3_core.py` (`SU3ChiralModel`, `lattice_periodic`). Script:
> `results/matter/fl1/FLB2_transition_order.py`. **NÃO modifica nada.**

## A pergunta

A transição de fase do modelo principal-chiral SU(3) (já estabelecida em FLB) é de
**primeira ordem** (como a literatura prevê para N≥3) ou **contínua**? FLB ficou
inconclusivo em L≤12, mas com sinais de 1ª ordem **começando a aparecer** em L=12
(dip de Binder 0.432; salto χ_max 2.07→5.20) — comportamento típico de 1ª ordem fraca,
cujas assinaturas só emergem quando L excede o (grande) comprimento de correlação.

## O que medir (as três assinaturas decisivas)

```
L ∈ {12 (âncora/overlap com FLB), 14, 16}  na rede cúbica, J fino em torno de 2.65.

D1  χ_max(N) scaling:   χ_max ∝ N^x.   x→1 = 1ª ordem (lei de volume); x<1 = contínua.
                        (FLB: x≈0.72 em L≤12 — testar se sobe com L maior.)
D2  Binder dip:         min do cumulante de Binder de m vs L. Aprofunda com L = 1ª ordem;
                        satura em valor universal = contínua. (FLB: 0.432 em L=12.)
D3  histograma de energia em J_c:  bimodalidade (calor latente / coexistência).
                        Pico duplo que afina com L = 1ª ordem; unimodal persistente =
                        contínua. (FLB: unimodal em L≤12 — o teste mais decisivo.)
```

## CRITÉRIOS DE MORTE / VEREDITO (pré-registrados)

```
GATE G0: L=12 reproduz FLB (J_c≈2.65, χ_max≈5, Binder_min≈0.43).

1ª ORDEM   se ≥2 de 3: x→1 (χ_max lei de volume); Binder dip aprofunda com L;
           histograma bimodal em J_c afinando com L.
CONTÍNUA   se x permanece <0.85 E Binder satura E histograma unimodal em todo L.
INCONCLUSIVO (mas mais apertado): sinais ainda mistos em L=16 — reportar o bound
           apertado e a leitura mais provável, SEM forçar (resultado válido; a ordem
           de transição fraca pode exigir L=24–32, declarado).
```

## HONESTIDADE / ESCOPO
A determinação de ordem de transição por escala finita é genuinamente difícil; "1ª
ordem fraca" pode precisar de L grande. Aceito **inconclusivo-mais-apertado** como
desfecho válido e pré-registrado. Sem número de QCD; J_c, expoentes e bimodalidade
saem só dos dados; a referência "1ª ordem para N≥3" é só enquadramento (COMPARISON
ONLY). Sementes fixas; JSON auto-descritivo; G0 reproduz FLB antes de qualquer alegação.
