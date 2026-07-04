# FX1 — VEREDITO: **H_NULO — [CLASSE GRANDE] SELADO**

> Avaliação contra os critérios congelados em `FX1_PRE_REGISTRO.md` (2026-06-27). Números
> primeiro. Pré-registro NÃO editado após ver os dados. Código `fx1_ratio.py`, dados
> `fx1_ratio.json`.

## Resultado (números primeiro)

**Stage 0 (gate de engenharia) — PASSA:**
- G0-a invariância de escala (M→7M): |ΔR| = **6.66e-16** ✓ (a razão é genuinamente
  scale-free; a parede de escala não está sendo medida por acidente).
- G0-b termo cruzado: **2.6%** < 20% ✓ (modos bem separados, comparação com Var limpa).
- G0-c controle GOE-aleatório: R = **1.74** [IQR 1.70, 1.81] (referência "espectro genérico,
  modo genérico").

**Observável primário R_FX1 = Γ_dec / Var_bulk(λ), operador BD:**

| | σ_x=0.10 | σ_x=0.18 | σ_x=0.30 |
|---|---|---|---|
| dim2 N100 | 0.932 | 0.371 | 0.161 |
| dim2 N200 | 0.768 | 0.348 | 0.142 |
| dim2 N400 | 0.691 | 0.329 | 0.121 |
| dim4 N100 | 2.440 | 1.927 | 0.659 |
| dim4 N200 | 1.500 | 1.932 | 0.645 |
| dim4 N400 | 2.570 | 1.435 | 0.689 |

## Avaliação dos 4 critérios de morte (congelados)

| Critério | Valor | Dispara? |
|---|---|---|
| 1 — R cavalga em σ_x (>±20% a dim,N fixos) | max_sigma_spread = **2.07** (fator ~6) | **SIM** |
| 2 — deriva sistemática em dim/N | dim_spread = **1.25** (dim2~0.3 vs dim4~1.5) | **SIM** (dim); N_spread=0.15 não |
| 3 — coincide com controle GOE (±15%) | grand=0.69 vs GOE=1.74 | não |
| 4 — = identidade Lindblad ½ (±15%) | grand=0.69 | não |

**NOVIDADE MORRE** (critérios 1 e 2 disparam). **Desfecho: H_NULO.**

## Leitura (narrativa, depois do número)

A taxa de colapso (Γ_dec, FS1) e a escala do gás espectral de Dyson (Var_bulk, FS2) **NÃO
estão travadas** por uma constante. A razão adimensional entre elas **cavalga fortemente na
largura do modo σ_x** (fator ~6 ao varrer σ_x de 0.10 a 0.30) e na **dimensão** (~2×). O modo
gaussiano espacial amostra o espectro de um jeito **dependente de largura e de dimensão** — não
há um número fixo ligando colapso a estatística espectral.

Notável: R_FX1 também **não** é o valor trivial (nem ½ de Lindblad, nem o 1.74 do controle
GOE-aleatório) — então não é nem mesmo uma identidade definicional estável; é genuinamente
**uma razão que varia**. As duas quantidades vivem no mesmo operador, mas a geometria causal
**não** impõe proporção fixa entre elas.

Isto é **exatamente o prior pré-registrado** (H_nulo): FS1 já havia achado o PREFATOR do Δx²
não-universal (rel_var 0.05–3.26, `RESEARCH_MAP.md:274-276`); FX1 confirma que essa não-
universalidade do prefator se propaga à razão colapso/espectro. O dado **não** derrubou o prior.

## Consequência para o programa

O **único** candidato a previsão fora do núcleo compartilhado (§C do `MAPA_CONVERGENCIA.md`)
está **morto pelo critério pré-registrado**. Com ele, fecha-se a última fresta pela qual o
veredito poderia subir de [CLASSE GRANDE] para [FORÇA ESTRUTURA]:

- **[CLASSE GRANDE] está agora SELADO empiricamente**, não só argumentado. O núcleo invariante
  TEIC×DEV×SR é genérico-por-teorema (Milgrom/RMT/Laplaciano/Poisson) E **não** esconde nenhuma
  razão adimensional forçada que pudesse ancorar uma teoria invertida única.
- A teoria invertida construída só do núcleo seria **mais um membro da classe de equivalência**
  — confirmado agora por experimento, não por suposição.

**Recomendação (inalterada e agora reforçada):** não construir a teoria invertida como teoria
nova/única. O resultado publicável é o próprio mapa + este selo: *três programas independentes
convergem no resíduo genérico-por-teorema, divergem em toda microestrutura, e não compartilham
nenhuma razão adimensional forçada além desse resíduo.*

## Caveats honestos

- Testou-se **uma** construção de razão (Γ_dec de modo gaussiano espacial / Var_bulk do mesmo
  operador). É a tradução natural do candidato §C, mas não esgota toda forma concebível de
  "Γ compartilhado". Uma razão construída em base espectral pura (autoestados, não modos
  espaciais) é uma variante não testada — porém ela seria a identidade de Lindblad ½ por
  construção (definicional), então não abriria novidade. A escolha de modo ESPACIAL é o que
  torna o teste não-trivial, e é onde a razão cavalga.
- Operador secundário (adjacência A) não tabelado no veredito (gerado em `fx1_ratio.json`);
  o primário BD é o discriminador pré-registrado. Conclusão robusta no primário.
