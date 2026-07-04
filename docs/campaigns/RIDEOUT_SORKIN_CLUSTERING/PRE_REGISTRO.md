# PRÉ-REGISTRO — GATILHO 2 Rideout–Sorkin: clustering do grafo de cobertura do CSG

> Congelado **antes** de qualquer dado existir. Charter: prompt do usuário
> "Registro de memória — consolidação pós-auditoria + gatilho Rideout–Sorkin", item 4.
> Predecessor direto: `docs/campaigns/RIDEOUT_SORKIN_TRIGGER/` (Gatilho 1 = ARMADO:
> coordenação ⟨z⟩(N) do CSG satura, finita).
>
> **STATUS: EXECUTADO 2026-06-27 → GATILHO 2 NÃO ARMADO** (fronteira em 1/3 regimes após
> extensão a N=16000 — ver SYNTHESIS §3b). Protocolo abaixo intacto (congelado, critérios não
> reinterpretados). Resultado em `SYNTHESIS.md` (código `rs_clustering.py` + `extend_intermediate.py`,
> dados `rs_clustering.json` + `extend_intermediate.json`, figura `rs_clustering.png`). Achado-chave:
> transitividade ≡ 0 por teorema (Hasse livre de triângulos); square-clustering C4 sub-mean-field
> (abaixo do controle de Poisson) ⇒ grafo de cobertura tipo-árvore ⇒ 2ª barreira de pé. Morte em
> 2/3 (sparse, manifold); fronteira em 1/3 (intermediate, platô C4≈0.019 mas ainda sub-MF).

**Data de congelamento:** 2026-06-25

---

## POR QUE ESTE 2º GATILHO EXISTE (a pré-condição central)

O Gatilho 1 (RIDEOUT_SORKIN_TRIGGER) mostrou que a coordenação do CSG **satura** —
removendo a perna de *alta coordenação crescente* do argumento de Bethe que condenava o
sprinkling de Poisson na ESCALA_XI. **Mas coordenação finita é NECESSÁRIA, não
SUFICIENTE.** Uma **rede de Bethe** (árvore infinita) tem coordenação finita e **ainda é
mean-field exata**. O que distingue um substrato que pode sustentar um ξ divergente de um
que é mean-field-por-teorema é a **estrutura de laços de dimensão finita** (clustering
positivo), **não** a coordenação.

Logo: **nenhuma campanha completa (ferromagneto de orientação + ξ) sobre o CSG deve rodar
antes deste gatilho.** Ele é a 2ª pré-condição, e é mais barato que a campanha completa.

---

## PRÉ-CONDIÇÃO HERDADA DO GATILHO 1 (congelada)

O regime **`dense` (p=0.40) é trivial** — fração de ordenação 0.999 ≈ cadeia 1D, sem
transição a temperatura finita. **Excluído deste gatilho.** Os únicos regimes legítimos,
aqui e em qualquer trabalho subsequente, são **`sparse` (p=0.02), `intermediate` (p=0.10)
e `manifold` (p=4/N)**.

---

## PERGUNTA

O grafo de cobertura (Hasse, não-direcionado) do CSG, nos regimes legítimos, é
**localmente tipo-árvore** (clustering → 0 com N ⇒ mean-field garantido **independente**
da coordenação finita) ou tem **clustering que satura num valor positivo** (estrutura de
laços que **pode** sustentar um ξ divergente)?

---

## MÉTODO (a pré-registrar — NÃO executar nesta tarefa)

Substrato e estimadores reutilizam o que já existe, **sem modificar o engine**:

- **Gerador:** `RIDEOUT_SORKIN_TRIGGER/rs_trigger.py::grow_transitive_percolation`
  (VERBATIM). Mesmo guard anti-circularidade (só `p` adimensional + ordem de nascimento;
  nenhuma escala métrica).
- **Grafo de cobertura:** a mesma redução transitiva do Gatilho 1; construir o `Graph`
  não-direcionado (CSR `indptr`/`indices` de `orientation_core.Graph`) a partir dos
  links de cobertura. **A seta causal é ignorada para esta medida estrutural** (clustering
  é propriedade do grafo não-direcionado).

**Observável primário — coeficiente de clustering (transitividade global):**
- `C_transitivity = 3·(#triângulos fechados) / (#caminhos-de-2-arestas)` no grafo de
  cobertura não-direcionado. (Não existe métrica de clustering de grafo no engine —
  grep em `orientation_core.py` só acha o "clustering" físico de Mermin; portanto
  implementar a transitividade padrão sobre a adjacência CSR já disponível.)
- Reportar também o **clustering local médio** `⟨C_i⟩` (média sobre nós da fração de
  pares de vizinhos que são adjacentes) como verificação cruzada.

**Observável secundário — girth local / comprimento de laços curtos:**
- Distribuição do menor ciclo passando por cada nó (girth local), via BFS curto.
- Um grafo tipo-árvore tem girth local → ∞ com N (laços só aparecem por acidente raro,
  e ficam longos); um grafo com laços persistentes tem girth local **limitado**.

**Ladder e contraste:**
- Ladder de N **idêntico** ao do Gatilho 1: `[500, 1000, 2000, 3300, 3888]`, ≥5 sementes
  (cap no topo se preciso, como no Gatilho 1).
- 3 regimes legítimos: `sparse` (0.02), `intermediate` (0.10), `manifold` (4/N).
- **Poisson como referência de contraste** (mesmo `causal_link_graph` da XI): **esperado
  clustering → 0** com N, pois o Poisson tem coordenação divergente e é conhecido ser
  localmente tipo-árvore/Bethe-like (Achado 3 da XI). O Poisson é o controle negativo:
  se a métrica não der ~0 para o Poisson, a métrica está errada.

---

## CRITÉRIOS (congelados ANTES de qualquer dado — não inflar depois)

- **GATILHO 2 ARMADO:** em **≥1** regime legítimo, o clustering **satura num valor
  positivo** conforme N cresce (não decai a zero; `d C/d ln N → 0` com `C_∞ > 0`). Isto
  justificaria, **finalmente**, a campanha completa (ferromagneto de orientação O(3)
  sobre o CSG + medição de ξ_2nd/L com a suíte da ESCALA_XI VERBATIM).
- **GATILHO 2 NÃO ARMADO:** em **todos** os regimes legítimos, o clustering **decai a
  zero** com N (tipo-árvore). A porta da "Saída 2" (substrato diferente) **fecha pela
  segunda barreira**, apesar de ter passado a primeira (coordenação). Resultado
  **igualmente válido e publicável**: reforça que o mean-field em causal sets é robusto
  por uma **segunda via independente da coordenação** (topologia tipo-árvore, não só
  coordenação divergente).
- **Confound a vigiar:** distinguir "satura em C>0" de "decai devagar a 0". Reportar o
  expoente local `d C/d ln N` nos maiores N e o valor extrapolado `C_∞`. Um falso
  "satura" por range curto de N é o erro a evitar — o ladder vai a 3888 (mesmo do
  Gatilho 1) e o Poisson de contraste deve exibir o decaimento-a-zero claramente.

**SEM ANNEALING:** os dois vereditos estão pré-definidos acima; não reinterpretar depois
de ver a curva.

---

## PRIOR HONESTO (declarar, não pender)

**Genuinamente em aberto — não pender para nenhum lado.** Por um lado, grafos de
crescimento causal **podem** desenvolver clustering pela própria regra de crescimento:
cada novo evento se liga a múltiplos predecessores, e se dois desses predecessores forem
eles próprios relacionados (ou compartilharem um link de cobertura), formam-se
triângulos — o que diferenciaria o CSG do sprinkling de Poisson. Por outro lado, a
redução transitiva (cobertura) **remove** justamente as relações que têm intermediários,
o que tende a **destruir** triângulos (um triângulo i–k–j com i⋖k, k⋖j e i⋖j é proibido
pela definição de cobertura: se i⋖k e k⋖j então i NÃO cobre j). **Esta tensão é real e
não-trivial** — daí o gatilho. Tratar como genuinamente indecidido até medir.

> Nota técnica para a execução futura: por causa da observação acima (cobertura proíbe o
> triângulo "alinhado" i⋖k⋖j + i⋖j), os triângulos do grafo de cobertura **não-direcionado**
> virão de configurações onde os três pares são links mas **não** todos co-lineares na
> ordem (ex.: dois pais de um mesmo filho que também se cobrem). Reportar a contagem bruta
> de triângulos e checar que não é identicamente zero por construção **antes** de
> interpretar — se for estruturalmente zero, o veredito é NÃO ARMADO trivial e deve ser
> dito como tal (tipo-árvore por teorema da própria definição de cobertura).

---

## O QUE NÃO FAZER

- **Não executar esta campanha agora.** Só o protocolo é travado aqui.
- **Não rodar a campanha completa (ferromagneto+ξ)** sob nenhuma hipótese antes deste
  gatilho dar ARMADO.
- **Não citar o regime `dense`** como evidência de nada (Pré-condição herdada).
- **Não inserir escala métrica** no gerador (guard anti-circularidade do Gatilho 1).
