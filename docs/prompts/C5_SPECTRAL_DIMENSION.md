# C5 — SPECTRAL DIMENSION: Corrida Dimensional e a Fronteira de ℏ

**STATUS: COMPLETO — VEREDITO C (MORTE: sem corrida dimensional genuína).**

Investiga se a rede causal de Poisson tem corrida dimensional (dimensão
espectral D_s variando com a escala), análoga ao que Causal Dynamical
Triangulations (CDT) mostra (D_s: 4 → 2 no UV) — e se essa corrida ofereceria
um mecanismo geométrico para o *papel* de ℏ.

Resultados, código e figuras em `results/foundations/c5/`.
Não modifica nenhuma campanha anterior.

---

## Resultado em uma frase

A dimensão espectral do heat kernel da rede causal de Poisson tem um **único
plateau físico em D_s = d = dimensão de Myrheim-Meyer** (gate passa em 2D:
D_s = 1.95 vs MM = 1.99). A variação sub-d observada em escala pequena é o
**corte de discretude** (a borda genérica de qualquer espectro discreto finito):
é **invariante por refinamento** (curvas D_s(s) idênticas num fator 4 de
densidade, espalhamento 0.071) e **invariante em eps**, sem nenhum plateau
sub-d estável tipo CDT. A rede é **lisa em todas as escalas físicas
resolvidas** — não exibe o fenômeno de CDT. Logo **não há escala de transição
σ*** para identificar com k = ℏN de T3C: **ℏ permanece inteiramente externo,
sem origem geométrica candidata por esta via.**

---

## Mapa dos artefatos

| arquivo | conteúdo |
|---|---|
| `results/foundations/c5/c5_core.py` | motor: sprinkling, operador de Sorkin/BD simetrizado+Euclideanizado, heat kernel, D_s, MM |
| `results/foundations/c5/C5V_engine_selection.py` | registro da escolha de motor (A/B falham o gate, C passa) |
| `results/foundations/c5/C5V_gate.md` | **C5-V** gate: D_s(IR) reproduz Myrheim-Meyer (PASSA em 2D) |
| `results/foundations/c5/C5_1_heatkernel.py` / `.md` | **C5-1** heat kernel, D_s(σ) multi-N (2D {1000,2000,4000}, 4D {1500,3000,5000}) |
| `results/foundations/c5/C5_2_running.md` | **C5-2** corrida? três diagnósticos (refinamento, plateau sub-d, eps) → NÃO genuína |
| `results/foundations/c5/C5_3_hbar_connection.py` / `.md` | **C5-3** condicional a C5-2 → não executado (sem σ*); discussão honesta de ℏ |
| `results/foundations/c5/C5_4_synthesis.md` | **C5-4** síntese e veredito |
| `results/foundations/c5/C5_heatkernel.png` | figura: (a) colapso D_s(s) 2D, (b) decaimento K~s^(-MM/2), (c) tendência 4D |
| `results/foundations/c5/C5_data.json` | todos os números |

Reproduzir: `python results/foundations/c5/C5_1_heatkernel.py && python results/foundations/c5/C5_3_hbar_connection.py`

---

## Critério de morte (pré-registrado) e como foi resolvido

```
MORTE   : D_s constante (~MM) em todas as escalas testáveis, sem corrida.
PARCIAL : corrida existe mas não estabiliza / dominada por efeitos de
          tamanho finito sem significado físico claro.
SUCESSO : D_s corre de ~d (IR) para valor menor estável (idealmente ~2)
          no UV, com σ* robusto a N.
```

**Resolvido: MORTE (C).** Acima do corte de discretude D_s = MM em toda a
janela resolvível, invariante por refinamento. A queda sub-d em σ pequeno é o
limite genérico de espectro discreto (D_s → 0 quando σ → 0), não um segundo
regime dimensional estável. Recusamos ler a subida 0 → d como "corrida" porque
ela falha os três testes de fisicalidade (sem plateau sub-d; colapsa entre
densidades; independente de eps).

---

## Ressalva honesta de alcance

O resultado é com o operador **numericamente viável** (Sorkin suavizado). A
literatura de conjuntos causais (Eichhorn-Mizera 2014) associa o operador
**afiado** de Benincasa-Dowker a um comportamento UV genuíno (na verdade um
*aumento* dimensional, oposto a CDT). Esse operador afiado tem flutuações
~ρ^(3/4) e é numericamente inacessível em qualquer N viável (parede documentada
em e10). Não se reivindica que a rede de Poisson não possa ter fenômeno UV
nenhum — reivindica-se que, com o operador mensurável, o que se mede é uma
variedade lisa de dimensão fixa mais o corte de discretude.
