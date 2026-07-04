# SÍNTESE — B5 · Por que η e ℏ "não pinam"

> Campanha ESCALAS_B5 (Fase 2, Frente B), promovido ao topo pelo R-1 (B1 negativo).
> Pré-registro: `PRE_REGISTRO.md`. Varredor: `B5_fss.py` → `B5_fss.json`. jun/2026.
> **Veredito: REVISA FD1 (MORTE → Verdito B). η é FORÇADO (limiar de percolação
> calculável do grafo causal), SIZE-STABLE (teorema, não artefato de tamanho), mas
> DIMENSION-DEPENDENT → não há η universal a pinar. Este É o mecanismo da tese de
> escalas (fecha a porta de B1 com um porquê).**
>
> **⚠ REFINADO por B6 (jun/2026):** a alegação de **size-stability** abaixo era
> baseada em N≤1600. B6 estendeu a N=3600 e encontrou **drift residual** de k_c(4)
> (~0.69 no platô N≤1600 → ~0.61 na banda N≥1800, band-spread 0.10). A palavra
> "size-stable (teorema, não artefato)" deve ser lida como **"platô a N≤1600 com
> drift finite-size suave além disso"**. O **núcleo permanece intacto**: k_c(4) é
> dimension-dependent, **não-genérico a ~8σ** abaixo do valor ER=1, e liderado pelo
> termo de Molloy–Reed (z_c_MR=0.50, rock-stable). Só a precisão do valor (0.67) e a
> força da palavra "size-stable/teorema" são suavizadas. Ver `../ESCALAS_B6/SYNTHESIS_B6.md`.

---

## 1. Pergunta e contexto

FD1 declarou η MORTE: k_c≈1 (limiar ER genérico) a N=300, disparado pela
**não-robustez** (k_c move >20% sob ±10% densidade). B5 pergunta: é **artefato de
tamanho** (k_c muda com N) ou **fundamental** (forçado pela estrutura do grafo)?
Relação SR (pós-dição): k_c = 1+√η ⇒ η = (k_c−1)².

## 2. Resultado (FSS, N=200..1600, d∈{2,4}, bootstrap)

| d | k_c(∞) | σ de 1 (N=1600) | tail-spread N350..1600 | CV grau | Molloy–Reed z_c |
|---|---|---|---|---|---|
| 2 | **1.01** | 1.0σ (≈ER-genérico) | 0.052 | 0.33 | 0.90 |
| 4 | **0.67** | **29.8σ (não-genérico)** | 0.008 | 1.00 | 0.50 |

- **Size-stable:** k_c plano em N (d4: 0.678→0.694→0.685→0.688). A não-robustez de
  FD1 era efeito de N=300 — **é teorema, não artefato**.
- **Dimension-dependent:** d2≈1 (genérico), d4≈0.67 (30σ ≠1). **Sem η universal.**
- **Mecanismo calculável:** k_c segue o **Molloy–Reed** z_c=⟨k⟩²/(⟨k²⟩−⟨k⟩)
  (=1 só para Poisson/árvore) fixado pela **heterogeneidade geométrica de grau**
  (CV N-estável: 0.33 em d2, 1.0 em d4 — nº de ancestrais depende da posição no
  diamante), **elevado** pelo clustering/transitividade do DAG causal (d2:
  0.90→1.01; d4: 0.50→0.67). Ambas as parcelas são propriedades de grafo calculáveis.

## 3. Veredito (Verdito B)

η **não é o parâmetro livre da SR**: o substrato o **força** ao limiar de
percolação do grafo causal — uma quantidade Molloy–Reed (heterogeneidade de grau)
mais correção de clustering, **size-stable** (teorema). MAS esse valor **depende da
dimensão** (η≈0 em d2, η≈0.11 em d4), logo o net **não seleciona um η universal**:
ele herda o input de dimensão (como d=3 é [EXTERNO] no DS1–3). 

"Por que η e ℏ não pinam" = **não há valor independente-de-dimensão a pinar**; o
limiar é uma propriedade geométrica do grafo, calculável mas não-universal. Padrão
recorrente do programa: **forma/mecanismo emerge, o número herda um input externo.**

Isto **revisa** o FD1 MORTE: a morte ("k_c genérico, η não pina") era (i) parcial
(vale em d2, falha em d4: 30σ não-genérico) e (ii) contaminada por tamanho
(N=300). O enquadramento correto é **Verdito B** (forçado até o input de dimensão).

## 4. Consequência para a tese de escalas (elo com B1)

B1 mostrou que a **normalização global da ação** (S→K·S) não fixa razão de massa
(hierarquia ∝√K escala). B5 fornece o **mecanismo complementar**: as escalas/limiares
absolutos que o net produz (η, e por analogia ℏ) são **propriedades de grafo
calculáveis** mas **dependentes de input** (dimensão) — não constantes universais
pináveis. Juntas, B1+B5 fecham a tese **"forma deriva, escala não" com um porquê**:
o substrato fixa formas e limiares-de-grafo (Molloy–Reed, percolação), não números
absolutos universais; estes precisam de inputs externos (unidade de ação, dimensão).

## 5. Limitação honesta

N≤1600 (size-stability sólida no range; w de FSS mal-determinado, mas o platô já é
plano sem extrapolação). d∈{2,4} (d=3 não rodado aqui — interpolaria entre 1.0 e
0.67; previsível mas não medido). A correção de clustering é diagnosticada
(gap k_c − z_c) mas não derivada analiticamente — fica como [IDENTIFICADO].

## 6. Anti-circularidade

`sr_teic_core.py` sob a guarda A1 (cobre `docs/campaigns/**`); `B5_fss.py` passa as
duas guardas (dilatação + literais de escala). k_c, CV, z_c, η **emergem do scan**;
nenhum número-puro de literal. Os valores SR (0.1, 0.99) entram só como pós-dição.
