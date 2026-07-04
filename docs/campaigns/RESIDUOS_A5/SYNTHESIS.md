# SÍNTESE — A5 / C5 · Resíduos de medição baratos

> Campanha RESIDUOS_A5 (Fase 2, Frente A, prioridade mais baixa). Pré-registro:
> `PRE_REGISTRO.md`. Driver: `a5_residuos.py` → `a5_residuos.json`. jun/2026.
> **Veredito: SUCCESS_A5. As duas últimas ressalvas do Paper MG fecham — (1) ε(2)=1
> é UNIFORME em campos winding-2 distintos (spin-estatística do bárion fechada);
> (2) θ=G_net·M/r sobrevive na malha 3D Cartesiana (não é artefato radial).**

---

## 1. Parte 1 — ε(2) uniforme (spin-estatística fechada)

O resíduo (PI4): "ε_swap=1 medido num único calibrador (PI0b); uniformidade na classe
swap ASSUMIDA, não provada". A5 mediu ε em **campos winding-2 distintos** de classe
conhecida 0 (Williams B mod 2):

| calibrador winding-2 (swap) | B | comps | estável | classe crua | ε |
|---|---|---|---|---|---|
| base z (PI0b, carregado) | 1.59 | 1 | sim | 1 | **1** |
| **width=1.5** (perfil distinto) | 1.36 | 1 | sim | [1,1] | **1** |
| **width=2.5** (perfil distinto) | 1.72 | 1 | sim | [1,1] | **1** |

**ε=1 em TODOS os 3 calibradores winding-2 swap distintos** (perfis radiais
estruturalmente diferentes, mesma estrutura azimutal/isospin-3). A anomalia de
framed-transfer é **uniforme** na classe swap → a correção ε(2)=1 do PI3 **não é mais
de campo único** → **a única ressalva de spin-estatística do bárion é fechada**.

**Controle de topologia (documentado):** uma rotação-alvo sobre um eixo de isospin
**diferente** (x) **não** preserva a topologia swap — dá **comps=2** (duas curvas
winding-1), classe 0, NÃO winding-2. Corretamente excluído do teste de ε; confirma
que a maquinaria distingue swap de não-swap (a estrutura de azimute-dobrado acopla ao
eixo isospin-3 especificamente). Achado lateral honesto.

Com PI5 (ε(3)=0, lei ε(n)=(n−1)mod2) + A5 (ε(2)=1 em 3 campos distintos), ε é agora
uma **paridade de winding medida em n=1,2,3 e robusta a campo** — a fronteira FR está
no degrau mínimo (só topologia algébrica geral + regra de quantização importadas).

## 2. Parte 2 — MG1-3D (não é artefato radial)

O resíduo: MG1 (θ=G_net·M/r, expoente −1, G_net∝M) foi medido no solver **radial**.
A5 re-mediu numa malha **3D Cartesiana completa** (`d3_audit_core.poisson3d_solve`,
−K∇²θ=fonte, sem 1/r inserido; L=40, n=48), fonte = densidade do Skyrmion:

| e_sk | M | expoente exterior | A | G_net=A/M |
|---|---|---|---|---|
| 0.3 | 175.1 | **−0.991** | 6.72 | 0.0384 |
| 0.5 | 182.2 | **−0.991** | 7.00 | 0.0384 |
| 1.0 | 200.1 | **−0.991** | 7.69 | 0.0384 |
| 1.5 | 218.0 | **−0.991** | 8.37 | 0.0384 |

**Expoente −0.991 ≈ −1** (bate com o radial −0.992) e **G_net=A/M constante (CV 0.0%)**
ao varrer e_sk (massas 175→218). ⇒ θ=G_net·M/r **não é artefato de simetria radial** —
o potencial Newtoniano (expoente −1) e a linearidade G_net∝M emergem igualmente numa
malha 3D sem simetria imposta. (O valor absoluto de G_net difere do radial por unidades
de discretização — irrelevante; a física é o expoente e a constância.)

## 3. Veredito (SUCCESS_A5)

As duas últimas ressalvas baratas do Paper MG fecham:
- **spin-estatística** (ε(2)=1 uniforme) — **removida**;
- **artefato radial** de θ=G_net·M/r — **excluído** (3D Cartesiano reproduz).

A5 é o item de **menor decisividade global** (não destrava nada a jusante), mas
fecha o débito de medição §2 do inventário com dois resultados limpos.

## 4. Limitação honesta

- ε(2): os 3 calibradores variam **perfil radial** (e o base, resolução/origem);
  todos compartilham a estrutura azimutal de azimute-dobrado (a única geradora barata
  de winding-2 swap de classe conhecida). Um campo winding-2 de estrutura **azimutal**
  radicalmente diferente não existe barato (B=3 axial dá winding-3, já usado em PI5).
  A uniformidade está testada **através de perfis**, não através de toda família
  concebível — registrado.
- MG1-3D: malha Cartesiana **regular** (não aspersão irregular). Uma aspersão 3D
  genuína bate na **mesma fronteira de não-localidade de A2/A4** (operador de grafo no
  causet) — **não tentada aqui**, registrada como fronteira (consistente com A2).
  O 3D-Cartesiano é o fechamento barato honesto: remove o artefato de simetria radial,
  não o de discretização-de-rede (que é a fronteira do causet).

## 5. Anti-circularidade

Gate A1 verde sobre `a5_residuos.py`. Classe verdadeira do calibrador = Williams
(topologia algébrica geral, sem input FR); ε de classe **medida**. Nenhum 1/r, G ou
GM/r no gerador de MG1 — fonte é peso adimensional, expoente **medido** do ajuste.
Campos reais (sem fase complexa injetada).
