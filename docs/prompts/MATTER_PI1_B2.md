# MATTER_PI1_B2: medir π₁ — a troca e a rotação-2π têm a MESMA classe ℤ₂?

> Continuação direta de `MATTER_FR_EXCHANGE.md` (Ataque 7), executando o passo
> que FR4 declarou como "a continuação natural": converter o teorema importado
> **troca ≅ rotação-2π em π₁(config B=2)** (Finkelstein–Rubinstein 1968;
> Williams 1970) em **medição na rede**. Resultados em `results/matter/pi1_b2/`.
> NÃO modifica campanhas anteriores (consome `fr_core`/`su2_core` por import).

## ✅ VEREDITO: **a identificação FR está MEDIDA — [troca] = [rotação-2π] = 1 ∈ ℤ₂** (com calibração ε declarada)

```
PI0  gate VERDE (após 1 bug de matching pego pelo g4 e corrigido ANTES da física):
     g1=0, g1b=0, estável em 3 valores regulares, refinamento N33→41 estável.
PI1  (2π, 4π) = (1, 0) ✓ — a suspensão age nos campos da rede.
PI2  (um sóliton, par) = (1, 0) ✓ — composto B=2 bosônico (par = Williams B mod 2).
PI3  CRU: troca = 0 (morte aparente). Análise: pré-imagem da troca é curva única
     winding-2 (fitas trocam) — topologia nunca coberta pelo gate.
PI0b CALIBRADOR (declarado após a surpresa, ANTES de rodar, leitura pré-fixada):
     iso-rotação 2π do B=2 axial — classe CONHECIDA 0 (Williams), mesma topologia
     swap (comps=1 confirmado). Medido 1 estável ⇒ ε_swap = 1.
     ⇒ troca corrigida = 0⊕1 = 1; troca² (winding-1, fiel) = 0 ✓.
RESULTADO: [troca] = [rotação-2π de um sóliton] = 1; 2-torção e espectro do
     composto medidos. Condição declarada: ε uniforme na classe de topologia
     (um único calibrador disponível) — assumido, não provado.
```
Síntese: [`results/matter/pi1_b2/PI4_synthesis.md`](results/matter/pi1_b2/PI4_synthesis.md).

## Pré-registro original (intacto abaixo; previsões e critérios fixados ANTES de qualquer corrida)

---

## A ideia (e o que é importado, declarado antes)

O espaço de configurações do setor B é o espaço de mapas baseados
U: S³ → SU(2)≅S³ (vácuo fixado no infinito — exatamente os campos da rede).
Topologia padrão (importada, citada):

```
π₁(Maps_B) = π₁(Ω³S³) = π₄(S³) = ℤ₂          (Pontryagin; Whitehead)
```

e a classe ℤ₂ de um loop U_s(x) tem um **invariante completo e computável**:
o invariante de Pontryagin–Thom. O loop define um mapa do domínio 4D
(s, x) → S³; a pré-imagem de um valor regular y ∈ S³ é uma curva fechada
1D em 4D com framing (pullback de uma base de T_yS³ pela diferencial);
a classe = **paridade total de torção do framing** (em 4D círculos não
enlaçam nem se atam; o framing é o único conteúdo — π₁(SO(3)) = ℤ₂).

**O que esta campanha mede:** as classes ℤ₂ dos loops físicos (troca,
rotação-2π de um sóliton, rotação do par, quadrados). **O que permanece
importado** (e encolhe): apenas π₄(S³) = ℤ₂ + completude do invariante —
topologia algébrica de livro-texto. A identificação física
troca ≅ rotação-2π deixa de ser teorema citado e vira igualdade de
dois números medidos.

Complementaridade declarada: FR3/Q4 mediram W=1 no SUBESPAÇO rígido
(coordenada coletiva); aqui mede-se no espaço de campos COMPLETO.

## PREVISÕES PRÉ-REGISTRADAS

```
PI0 (gate de engenharia, roda ANTES de qualquer física):
  g1 loop constante U_s = U₀ (B=1): classe 0;
  g2 estabilidade: a classe de cada loop é idêntica para 3 valores
     regulares y distintos;
  g3 todas as cadeias de pré-imagem FECHAM (endpoints casados) e nenhuma
     célula de pré-imagem toca a borda da caixa;
  g4 refinamento: classe do loop de rotação B=1 inalterada sob um
     refinamento de grade (N→N+8).

PI1 (B=1 — a suspensão age):
  rotação espacial 2π do hedgehog:  classe 1   (gerador = suspensão de Hopf)
  rotação 4π (loop percorrido 2×):  classe 0   (2-torção)

PI2 (B=2 — spins do composto):
  rotação 2π de UM sóliton do par:  classe 1
  rotação 2π do PAR inteiro:        classe 0   (grau B mod 2 = 0 — o
                                                composto B=2 é bosônico)

PI3 (B=2 — o teorema FR vira medida):
  loop de troca (FR1 + segmento de fechamento slerp):  classe 1
  troca percorrida 2×:                                 classe 0
  ⇒ [troca] = [rotação-2π de um sóliton] = 1 ∈ ℤ₂  — FR MEDIDO.
```

## CRITÉRIOS DE MORTE (pré-registrados)

```
PI0 morre (MAQUINARIA, aborta campanha sem veredito físico) se: g1 ≠ 0; ou
    classe instável entre valores regulares; ou cadeias não fecham mesmo
    após um refinamento; ou pré-imagem toca a borda.
PI1 morre se (2π, 4π) ≠ (1, 0) — a estrutura de suspensão não age nos
    campos da rede; rota FR inteira errada para esta rede.
PI2 morre se (um sóliton, par) ≠ (1, 0) — espectro de spin do composto
    inconsistente.
PI3 morre se (troca, troca²) ≠ (1, 0) — a troca NÃO é homotópica à
    rotação-2π na rede; o teorema FR não se aplica a este substrato.
SUCESSO = todas as previsões batem. Qualquer outro padrão é morte
    correspondente, reportada como tal.
Verificações de engenharia contínuas (pré-registradas): fechamento slerp
    válido só se distância pontual máx U(1)↔U(0) < 0.5 (longe de antípoda);
    rotações de frame consecutivas < 90° (senão re-amostrar a cadeia).
```

## Tarefas

```
pi1_core.py: avaliação dos loops (analítica, via fr_core), extração de
    pré-imagem (marching 4-simplexes de Freudenthal sobre a grade (s,x)),
    encadeamento, framing por pullback da diferencial afim por simplexo,
    torção relativa ao framing de referência (projeção de frame constante),
    lift contínuo → paridade ℤ₂ por componente.
PI0_gate.py        → PI0_gate.{md,json}
PI1_b1_rotation.py → PI1_b1_rotation.{md,json}
PI2_b2_rotation.py → PI2_b2_rotation.{md,json}
PI3_b2_exchange.py → PI3_b2_exchange.{md,json}
PI4_synthesis.md   → o quadro final: o que está medido, o que segue importado
```

## Parâmetros (fixados antes de rodar)

```
B=1: caixa L=12, grade espacial N=33, 32 passos de s (64 para loops 2×).
B=2: caixa L=24, grade N=41, 48 passos de s (+8 de fechamento na troca),
     separação d=6 (a do FR1), perfil F(r)=π e^{-r/2} (o do fr_core).
Valores regulares: y₁=(0.05,0.70,−0.50,0.50)/|·|, y₂=(−0.20,0.40,0.65,−0.55)/|·|,
     y₃=(0.10,−0.60,0.45,0.60)/|·| — todos a >60° do vácuo (1,0,0,0) e de −𝟙.
Refinamento do gate: N=33→41 (B=1).
```

## Honestidade pré-declarada

- O importado NÃO desaparece: π₄(S³)=ℤ₂ e a completude do invariante de
  Pontryagin–Thom são teoremas citados (Pontryagin; Whitehead). O ganho: o
  conteúdo FÍSICO (troca ≅ rotação) sai do importado e vira medição; o
  importado residual é topologia de livro-texto sem conteúdo dinâmico.
- O loop de troca só fecha assintoticamente (e^{-d/2}, FR1); o segmento de
  fechamento slerp é parte declarada do loop e sua validade é critério de
  engenharia, não ajuste.
- A quantização coletiva (W=1 → fase −1, j=½) continua externa
  (MATTER_SU2_QUANT, inalterado): aqui mede-se a topologia do loop, não a
  regra de quantização.
- Prior art obrigatório: Finkelstein–Rubinstein 1968; Williams 1970;
  Friedman–Sorkin 1980; Giulini 1993/95.
