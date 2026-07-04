# PRÉ-REGISTRO — GATILHO Rideout–Sorkin (coordenação do crescimento sequencial)

> Congelado **antes** de qualquer medição registrada. Charter: prompt do usuário
> "Gatilho de coordenação do crescimento sequencial (Rideout–Sorkin)", Parte B.
> Predecessor direto: Campanha XI (`docs/campaigns/ESCALA_XI/`), que fechou a porta
> da geometria do **sprinkling de Poisson** com o argumento de Bethe (grafos de alta
> coordenação localmente tipo-árvore ⇒ criticalidade mean-field, sem ξ divergente).

**Data de congelamento:** 2026-06-25

---

## O QUE ESTE GATILHO DECIDE (e o que NÃO é)

A pergunta em aberto: um substrato **genuinamente diferente** — o **crescimento
sequencial clássico (CSG) de Rideout–Sorkin**, onde o causal set *cresce* por uma
regra estocástica em vez de ser sorteado de um Minkowski de fundo — escaparia do
destino mean-field da XI?

Mas o CSG **só vale a campanha completa se escapar do argumento de Bethe**, e isso é
decidido por uma única propriedade barata: **a coordenação média do grafo de Hasse
⟨z⟩ cresce com N (como no Poisson) ou satura num valor finito?**

Este gatilho mede **exclusivamente isso**. **Não** roda ferromagneto, **não** mede ξ,
**não** constrói a campanha completa. Só decide se ela se justifica.

---

## ESTIMADOR (congelado — idêntico ao da ESCALA_XI)

`z = ⟨degree⟩` do **grafo de Hasse** (relações de cobertura), exatamente como
`orientation_core.causal_link_graph` + `Graph.degree.mean()`:

- Relação de cobertura (link) `i⋖j` ⟺ `i≺j` (na ordem causal/fecho transitivo) **e**
  não existe `k` com `i≺k≺j` (redução transitiva `L = C & ~(C@C)`).
- Grafo **não-dirigido**; `degree[i]` = nº de links incidentes a `i` (passado+futuro).
- `z_mean = degree.mean() = 2·(#links)/N`.

Baseline de Poisson (3+1)D para sobreposição, lido de
`ESCALA_XI/campaign_full.json` (mesmo estimador, mesma ρ=2.0):

| N_mean | z_mean (Poisson Hasse) |
|---|---|
| 501.8 | 33.44 |
| 1047.2 | 52.13 |
| 1947.2 | 75.70 |
| 3329.8 | 103.02 |

→ Poisson **DIVERGE** (×3.1 no ladder; expoente local ≈ d⟨z⟩/d ln N ≈ +37).

---

## GERADOR (congelado) — CSG / percolação transitiva

Dinâmica de crescimento sequencial **clássica**, na subfamília canônica de
percolação transitiva (Rideout–Sorkin 2000; Barak–Erdős):

- Elementos nascem em ordem `1..N`. Para cada par em ordem de nascimento `i<j`,
  uma **relação direta** `i→j` é sorteada independentemente com probabilidade `p`.
- A ordem causal `C` é o **fecho transitivo** dessas relações diretas.
- `p` é a única constante de acoplamento — **adimensional**. Equivale à subfamília
  RS com `t_n = t^n` (geométrica).

**GUARD ANTI-CIRCULARIDADE (congelado):** nenhuma escala métrica, nenhuma coordenada
de espaço-tempo, nenhuma expressão relativística entra no gerador. A dinâmica é
definida só por `p` (adimensional) e pela ordem de nascimento (rótulo). O `z`
medido é puramente combinatório (contagem de links no grafo de cobertura).

---

## GATE DE VALIDAÇÃO (congelado — roda ANTES de qualquer leitura de ⟨z⟩)

O gerador deve reproduzir propriedades **documentadas** da percolação transitiva:

1. **Contagem de elementos minimais (forma fechada).** `j` é minimal ⟺ nenhum
   `i<j` tem aresta direta para `j` ⟹ `P(j minimal)=(1−p)^{j−1}` ⟹
   `E[#minimais] = (1−(1−p)^N)/p`. Tolerância: medido dentro de ±3σ do fechado.
2. **Contagem de arestas diretas (forma fechada).** `E[#diretas] = p·N(N−1)/2`.
3. **Idempotência do fecho transitivo** (`C` = sua própria transitividade) e
   **antissimetria/aciclicidade** (DAG por construção em ordem de nascimento).
4. **Percolação da ordem:** a fração de ordenação (pares relacionados) **cresce com
   N a `p` fixo** (a ordem percola para uma quase-ordem-total) — comportamento
   qualitativo documentado.

Sem este gate VERDE, a medição de ⟨z⟩ não é confiável e o veredito é nulo.

---

## MEDIÇÃO CENTRAL E VARREDURA (congeladas)

- **Ladder de N:** `[500, 1000, 2000, 3300, 3888]` (faixa validada na XI,
  estendida ao topo do range do charter, ~175→3888).
- **Sementes:** ≥5 por (regime, N); determinísticas.
- **Regimes (≥3, da família CSG):**
  | rótulo | p | caráter |
  |---|---|---|
  | `sparse_fixed` | 0.02 | esparso (p fixo pequeno) |
  | `intermediate_fixed` | 0.10 | intermediário (p fixo) |
  | `dense_fixed` | 0.40 | denso (p fixo grande) |
  | `manifold_scaled` | 4/N | RS esparso genuíno (grau direto médio fixo λ=4) — o **steelman** da saturação (regime tipo-variedade) |

  (4 regimes; o `manifold_scaled` é incluído deliberadamente porque é o regime onde a
  saturação é *mais* plausível — não excluí-lo de antemão.)

---

## CRITÉRIOS (congelados ANTES de rodar)

- **GATILHO ARMADO:** em **algum** regime, `⟨z⟩(N)` **satura** num valor finito
  (`d⟨z⟩/d ln N → 0` nos maiores N). Coordenação finita ⇒ o grafo **não** é o
  tipo-árvore de alta coordenação que Bethe condena ⇒ ξ divergente tem onde morar ⇒
  **vale** rodar a TEIC (ferromagneto de orientação) sobre este substrato. (PARAR
  aqui mesmo assim; a campanha completa é decisão separada.)
- **GATILHO NÃO ARMADO:** em **todos** os regimes, `⟨z⟩(N)` **diverge** com N (mesmo
  comportamento qualitativo do Poisson). Coordenação divergente ⇒ CSG cai no **mesmo**
  argumento de Bethe ⇒ substrato pré-condenado ao mean-field ⇒ campanha completa
  **não** se justifica e **não** é executada.
- **Confound a vigiar:** distinguir "satura" de "cresce devagar mas ainda crescendo".
  Reportar o expoente local `d⟨z⟩/d ln N` nos maiores N e ver se vai a zero ou só
  diminui. Um falso "satura" por range curto de N é o erro a evitar.

**SEM ANNEALING:** os dois vereditos estão pré-definidos acima; não reinterpretar
após ver a curva.

---

## PRIOR HONESTO (declarado, não inflado)

Causal sets em geral tendem a small-world / alta coordenação ⇒ o desfecho **mais
provável** é **NÃO ARMADO** (CSG diverge como Poisson, cai no mesmo Bethe). Se for
esse o caso, é um resultado limpo e barato que fecha a "Saída 2" (substrato diferente)
sem gastar a campanha completa, e reforça que o mean-field dos causal sets é robusto à
*forma de gerar* o conjunto, não só ao sprinkling. O "não armado" é um resultado útil.
