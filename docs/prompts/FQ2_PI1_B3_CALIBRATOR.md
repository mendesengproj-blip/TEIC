# FQ2 — segundo calibrador de π₁: B=3 axial (classe verdadeira 1)

> Continuação direta de `MATTER_PI1_B2.md` (fechado em PI4). Executa o único
> residual declarado em `PI4_synthesis.md`: ε_swap foi medido num **único**
> calibrador (PI0b, classe verdadeira **0**). Esta campanha mede um **segundo
> calibrador independente, de classe verdadeira 1** (Williams, sem input FR),
> para testar se a anomalia de framing ε é uma propriedade topológica
> bem-definida da maquinaria de Pontryagin–Thom em pré-imagens multi-winding —
> ou um artefato do campo particular do PI0b.
> NÃO modifica resultados anteriores. Consome `pi1_core` por import (acréscimo
> aditivo de `axial_bn` + `preimage_windings`; funções existentes intactas).
> Resultados em `results/matter/pi1_b2/` (PI5_*). Numeração segue PI0–PI4.

---

## A escolha (declarada): por que B=3, não um segundo winding-2

O residual do PI4 pede "um segundo calibrador independente **de classe
conhecida 1** e topologia swap". Dois caminhos foram considerados:

- **Segundo campo grau-2 (classe 0, winding-2):** testaria a uniformidade de
  ε **dentro** da classe winding-2 — mas dá de novo classe verdadeira **0**,
  não satisfazendo "classe conhecida 1".
- **B=3 axial (classe 1, winding-3):** satisfaz "classe verdadeira 1". Não é
  winding-2 (é cobertura tripla), mas isso é uma **feature**: combinado com
  ε(1)=0 e ε(2)=1 já medidos, determina a **lei ε(n)** e prova que a leitura
  da maquinaria em topologia multi-winding é reprodutível, convergente e
  topologicamente sensata — exatamente o que a correção do PI3 pressupõe.

Escolha: **B=3 axial.** É impossível obter (winding-2, classe-1) por
rotação-alvo (lá classe = B mod 2 e winding = B estão travados; winding-2 força
classe 0). A única realização clássica de (winding-2, classe-1) é a própria
troca (PI3) — circular. B=3 é o calibrador classe-1 mais barato e independente.

### Limitação declarada (honestidade, não escondida)
B=3 é winding-3. Ele **valida a maquinaria em multi-winding** e **fixa a lei
ε(n)**, mas **não re-mede ε(2) num segundo campo**. O residual menor "ε(2)
uniforme entre campos winding-2 distintos" permanece aberto (precisaria da
Estratégia 2, deferida). A ressalva spin-estatística é portanto **reduzida**,
não eliminada: passa de "ε medido uma única vez, lei desconhecida" para "ε é
uma anomalia de winding com lei medida em n=1,2,3, e a maquinaria é confiável
em multi-winding".

---

## O calibrador

Campo axial de grau n (azimute multiplicado por n; mesmo ansatz do `axial_b2`
do PI0b, generalizado):

```
U = (cos F(r),  sin F(r) · n̂(θ, nφ)),   n̂ = (sinθ cos nφ, sinθ sin nφ, cosθ)
F(r) = π e^(−r/2)   (perfil do fr_core; mesmo do PI0b)
```

Para **n=3**: classe verdadeira = grau mod 2 = **3 mod 2 = 1** (Williams 1970,
álgebra de suspensão padrão — a mesma usada e confirmada no PI2-par = B mod 2 =
0; **sem nenhum input do teorema da troca FR**).

Loop medido: rotação-alvo (isospin) 2π global,
`U_s = q(s) U q(s)†`, `q(s) = (cos πs, 0, 0, sin πs)` — exatamente o loop do
PI0b, aplicado ao campo B=3.

**Topologia da pré-imagem (prevista):** 3 fitas em φ₀, φ₀+2π/3, φ₀+4π/3
girando 2π/3 cada ao longo de s ⇒ 3-ciclo ⇒ **curva única winding-3**
(comps=1, winding=3). É a cobertura tripla — análoga ao winding-2 swap do PI0b,
um passo acima.

---

## O modelo de ε e a PREVISÃO PRÉ-REGISTRADA

Definição operacional: para um loop com pré-imagem de winding n,
`classe_medida = classe_verdadeira ⊕ ε(n)`. Medido até aqui:

```
ε(1) = 0   (PI0 gate + PI1 + PI2 + troca² — muitos loops winding-1 lidos certos)
ε(2) = 1   (PI0b: classe verdadeira 0, medido 1)
ε(3) = ?   ← esta campanha
```

Como **classe_verdadeira(B=3) = 1 é conhecida**, a medição de classe_medida
**mede ε(3) diretamente**: ε(3) := classe_medida ⊕ 1.

Dois modelos naturais consistentes com (ε(1)=0, ε(2)=1):

```
H_lin   (transferência por folha extra):  ε(n) = (n−1) mod 2  → ε(3)=0
H_sat   (qualquer multi-winding):          ε(n) = [n ≥ 2]      → ε(3)=1
        (binomial C(n,2) mod 2 coincide com H_sat em n=3)
```

**PREVISÃO PRÉ-REGISTRADA (favorita): H_lin ⇒ ε(3)=0 ⇒ classe_medida(B=3) = 1.**
(O framing de referência acumula uma meia-torção por folha; duas folhas extra
cancelam mod 2.) A alternativa H_sat ⇒ classe_medida = 0 é declarada e aceita
como **determinação de lei alternativa**, não como morte.

Ponto crucial de honestidade: **ambos os desfechos preservam ε(2)=1** (todos os
modelos concordam em n=2), logo **a correção FR do PI3 permanece válida em
qualquer caso**. B=3 não pode *matar* a identificação FR — só a MORTE DE
MAQUINARIA (gate abaixo) poderia, ao mostrar que a leitura em multi-winding é
não-confiável.

---

## GATE OBRIGATÓRIO (anti-aliasing — roda ANTES de qualquer leitura de ε)

A B=2 axial subestimou o número bariônico no PI0b (1.59→1.75→1.83 sob
N=37→49→61). B=3 varia mais rápido no azimute ⇒ risco de aliasing maior. A
classe **NÃO pode ser reportada** antes de:

```
G1  Convergência bariônica: B(axial_b3) cresce monotonicamente com a resolução
    sobre N ∈ {37, 49, 61, 73}, com tendência clara ao limite 3 (extrapolação
    ∈ [2.6, 3.4]; e claramente separada de 2 e de 4).
G2  Topologia correta: a pré-imagem é UM componente (comps=1) com winding = 3,
    para os 3 valores regulares, na resolução de medição. (Confirma a cobertura
    tripla; descarta aliasing para winding-1/2/4.)
G3  Estabilidade: classe_medida idêntica nos 3 valores regulares.
G4  Convergência da classe: classe_medida idêntica em N=49 e N=61 (refinar a
    N=73 se divergirem). A leitura precisa estar convergida, não ser artefato.
Verificações de engenharia contínuas (do pi1_core): todas as cadeias FECHAM;
    nenhuma célula de pré-imagem na borda; rotações de frame consecutivas < 90°.
```

---

## CRITÉRIOS DE MORTE (pré-registrados)

```
MORTE DE MAQUINARIA (sem veredito de ε; e LANÇA DÚVIDA sobre o PI3): o gate
    falha — G2 não dá (comps=1, winding=3) na resolução convergida; OU G3
    instável entre valores regulares; OU G4 não converge (49≠61≠73); OU
    engenharia falha (cadeia aberta / borda / frame_dot < √0.5).
    ⇒ a maquinaria de PT é não-confiável em multi-winding ⇒ a leitura winding-2
      do PI3 fica suspeita. Reportar como tal.

SE O GATE PASSA (leitura definida ∈ {0,1}):
    classe_medida = 1  ⇒ ε(3)=0  ⇒ confirma H_lin; ε é anomalia de
        winding-paridade limpa; ε(2)=1 do PI3 é parte de lei coerente. POSITIVO
        MAIS FORTE — fecha o residual no grau máximo que B=3 permite.
    classe_medida = 0  ⇒ ε(3)=1  ⇒ seleciona H_sat; ε(2)=1 e a correção FR
        seguem válidas; lei ε(n) é do tipo "saturação". Reportado como lei
        alternativa medida — NÃO morte da FR.
```

`SUCESSO` = gate passa e ε(3) fica determinado (qualquer dos dois valores), com
a lei ε(n) selecionada e a maquinaria validada em multi-winding. A previsão
favorita (classe_medida=1) bate ou não bate — reportado honestamente.

---

## Parâmetros (fixados antes de rodar)

```
Campo: axial_b3, perfil F(r)=π e^(−r/2), caixa L=16 (a do PI0b).
Convergência bariônica G1: N ∈ {37, 49, 61, 73}.
Medição de classe: N ∈ {49, 61} (refinar a 73 se G4 falhar), NS = 48 passos de
    s (declarado: subir a 72 se houver aliasing-s; winding-3 já resolvido por 48
    no análogo winding-2). Loop: loop_target_rotation (do pi1_core).
Valores regulares: os 3 pré-registrados do pi1_core (REGULAR_VALUES), todos a
    >60° do vácuo e de −𝟙.
```

## Tarefas

```
pi1_core.py:  + axial_bn(X,Y,Z,n)         (generaliza axial_b2; b2 intacto)
              + preimage_windings(...)      (winding-s por componente; G2/G4)
PI5_b3_calibrator.py → PI5_b3_calibrator.{json}  (gate G1–G4 + medição)
PI5_synthesis.md     → ε(3), lei ε(n) selecionada, status do residual
```

## Prior art

Finkelstein–Rubinstein 1968 · Williams 1970 (rotação de grau n ≅ n mod 2 —
fonte da classe verdadeira do calibrador) · Pontryagin/Whitehead (π₄(S³)=ℤ₂).
