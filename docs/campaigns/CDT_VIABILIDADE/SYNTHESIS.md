# SYNTHESIS — GATILHO 3: viabilidade cinemática tipo-CDT (aresta fixa + colagem livre)

> Execução do protocolo congelado em `PRE_REGISTRO.md` (CDT_VIABILIDADE). Resultado-primeiro.
> Código `cdt_kinematics.py`, dados `cdt_kinematics.json`, figura `cdt_kinematics.png`.
> **Data de execução:** 2026-06-27. Cinemática pura, **sem ação/dinâmica** (conforme travado).

## VEREDITO DE UMA LINHA

**GATILHO 3 = ARMADO** (regime `flipped`/DT), **com duas ressalvas que limitam o peso**. O
1-esqueleto da triangulação 2D evoluída por movimentos de Pachner tem **estrutura de laços de
dimensão finita** — C4≈0.145 e transitividade≈0.30 **saturantes**, ~5× o piso mean-field do
Poisson e da ordem de uma rede 2D genuína. É o **primeiro** substrato da fila a passar a 2ª
barreira (laços), depois de Poisson (morto na 1ª) e CSG (morto na 2ª). **Mas:** (1) em 2D a
coordenação ⟨z⟩→6 é **identidade de Euler**, não um escape dinâmico do Bethe — a 1ª barreira é
passada **por construção, não conquistada**; (2) movimentos de Pachner **sem peso de ação** são
conhecidos por gerar patologia branched-polymer na geometria global — o ARMADO cinemático é
**necessário, não suficiente** para a teoria dinâmica completa.

---

## 1. Resultado (números primeiro)

**Gate de validação — VERDE:** seed = bordo do tetraedro = K4 (z=3, transitividade=1, C4=1,
exatos); invariante de manifold preservado após movimentos (cada aresta em 2 triângulos;
característica de Euler V−E+F=2 = esfera); **rede triangular regular transitividade = 0.400**
(valor conhecido) — gerador e estimador corretos.

**Medição no 1-esqueleto** (ladder N=500→3888, 5 seeds, cap 3 no topo). Dois regimes do espaço
de movimentos: `stacked` = só crescimento (1,3) (Apollonian); `flipped` = (1,3) + 4 flips (2,2)
por vértice (o ensemble de triangulações dinâmicas, DT):

| Regime | obs | N=500 | 1000 | 2000 | 3300 | 3888 |
|---|---|---|---|---|---|---|
| stacked | ⟨z⟩ | 5.976 | 5.988 | 5.994 | 5.996 | 5.997 |
| stacked | transitividade | 0.236 | 0.225 | 0.202 | 0.181 | 0.167 |
| stacked | C4 | 0.149 | 0.148 | 0.146 | 0.138 | 0.138 |
| **flipped** | ⟨z⟩ | 5.976 | 5.988 | 5.994 | 5.996 | 5.997 |
| **flipped** | **transitividade** | 0.310 | 0.303 | 0.307 | 0.300 | **0.302** |
| **flipped** | **C4** | 0.146 | 0.148 | 0.148 | 0.147 | **0.145** |

**Referências da fila:** Poisson (controle mean-field) C4≈0.029–0.054 **decaindo**; CSG
intermediate (Gatilho 2) C4≈0.019 (platô sub-MF); rede 2D dim-finita C4=0.125 / transitividade=0.4.

## 2. Leitura barreira-por-barreira

**Barreira 1 (coordenação ⟨z⟩ finita?) — PASSA, mas TRIVIALMENTE.** ⟨z⟩ satura em 6.0 nos dois
regimes. **Porém isto NÃO é um escape dinâmico:** para qualquer triangulação 2D fechada, Euler
(V−E+F=2 com 2E=3F) força E=3V−6 ⇒ ⟨z⟩=2E/V=6−12/V → **6 exatamente**. Os valores medidos
(5.976, 5.988, 5.994, 5.997) batem com 6−12/V à 4ª casa. ⇒ a "saturação de coordenação" do
tipo-CDT em 2D é uma **identidade topológica**, não uma propriedade dinâmica conquistada como no
CSG (onde ⟨z⟩ saturar foi um resultado não-trivial da regra de crescimento). **A barreira 1 é
passada por construção em 2D.**

**Barreira 2 (laços de dimensão finita?) — PASSA, genuinamente informativo.** Aqui está o
conteúdo real: C4≈0.145 e transitividade≈0.30 (regime flipped), **estáveis** com N, ~5× o piso
mean-field do Poisson e da **ordem da rede 2D dim-finita** (C4=0.125, transitividade=0.4). Ao
contrário do CSG (cuja cobertura é tipo-árvore, C4 sub-MF), o 1-esqueleto da triangulação **tem
laços de dimensão finita** — porque é, literalmente, uma superfície 2D triangulada. A
transitividade é **não-degenerada** aqui (≠ grafo de Hasse do CSG, onde era 0 por teorema), e o
1-esqueleto a exibe robustamente.

**Diferença stacked vs flipped (registrada):** o `stacked` (Apollonian, só crescimento) tem
transitividade **decaindo** (0.236→0.167) — um 3-tree planar perde densidade local de triângulos
com N; o `flipped` (DT genuíno, com reconexão de Pachner) **estabiliza** transitividade≈0.30 e
C4≈0.145. O regime fisicamente relevante (colagem livre) é o que arma claramente.

## 3. As duas ressalvas (limitam o peso do ARMADO — simétricas ao prior pré-registrado)

1. **A barreira 1 é trivial em 2D (Euler).** ⟨z⟩→6 não distingue um substrato "bom" de um "ruim"
   — toda triangulação 2D fechada tem ⟨z⟩→6. Então, das duas barreiras, **só a de laços é
   informativa aqui**, e ela é passada em parte **por construção** (uma superfície triangulada
   tem triângulos). O tipo-CDT 2D não "conquista" os laços do mesmo jeito que o CSG conquistou a
   coordenação finita — eles vêm com a definição de triangulação.

2. **Pachner sem ação ⇒ possível patologia (o prior pré-registrado, confirmado como pertinente).**
   A literatura de triangulações dinâmicas estabelece que movimentos de Pachner **aleatórios sem
   peso de ação** geram tipicamente geometrias **branched-polymer** (dimensão de Hausdorff
   degenerada, d_H→∞ efetiva) — é por isso que a CDT real pesa a soma com ação de Regge e faz
   rotação de Wick. O nosso teste mede clustering **local** (sadio), mas **não** mede a geometria
   **global** (dimensão de Hausdorff/espectral), onde a patologia se manifestaria. ⇒ um ARMADO
   cinemático **local** é **necessário mas não suficiente**: diz que a classe tem a pré-condição
   de laços, **não** que sustenta criticalidade não-trivial na teoria dinâmica completa.

**Anti-circularidade (não-negociável, respeitado):** a aresta é **fixa `[External]` por
construção**. Nada aqui é "uma escala emergiu" — o resultado é puramente sobre **estrutura de
laços + coordenação** da classe cinemática, uma pré-condição estrutural para a dinâmica completa
(ação + integral de caminho + Wick), jamais uma derivação de escala.

## 4. Posição na fila de substratos (atualizada)

| Via | Barreira 1 (⟨z⟩ finito) | Barreira 2 (laços dim-finita) | Status |
|---|---|---|---|
| Poisson | **FALHA** (diverge) | — | MORTA |
| CSG | PASSA (não-trivial) | **FALHA** (tipo-árvore, C4 sub-MF) | ENCERRADA (fronteira em 1/3) |
| **tipo-CDT (2D)** | passa **trivialmente** (Euler) | **PASSA** (C4≈0.145 ~ rede 2D) | **ARMADO (com ressalvas)** |

O tipo-CDT é o **único** que passa as duas — mas a leitura honesta é que em 2D ele as passa
**em grande parte por construção** (Euler + superfície triangulada), e a questão genuína
(geometria global sadia, criticalidade não-trivial) **fica para a dinâmica completa com ação**,
fora do escopo de gatilhos baratos.

## 5. Próximo passo (registrado como PENDENTE, NÃO executado)

Gatilho 3 ARMADO ⇒ entra na fila, **não iniciada nesta tarefa**, a campanha completa equivalente
à de ξ **sobre o substrato tipo-CDT com AÇÃO adicionada** (Regge/Einstein-Hilbert + peso +
rotação de Wick), que é o único teste capaz de decidir se a geometria global é sadia (resolve a
ressalva 2) e se há criticalidade não-trivial. **Bloqueio explícito:** sem o peso de ação, o
resultado cinemático não se estende à teoria dinâmica (ressalva 2). Também não testado: a
extensão a **dim 3** (onde ⟨z⟩ **não** é Euler-fixado e a barreira 1 voltaria a ser informativa).

---

## ATUALIZAÇÃO (2026-06-28) — fechamento no MOTOR FOLIADO VALIDADO de F1 (TEORIA_CDT)

> Re-execução do gatilho **no próprio ensemble que passou o gate G1 (d_H=2)** da TEORIA_CDT
> (`TEORIA_CDT/F1_acao/f1_cdt2d.py`), com os **mesmos estimadores** dos Gatilhos 1/2
> (`rs_clustering.clustering_metrics`, VERBATIM) e um **teste de trivialidade de C4** que a
> medição original (sobre o gerador `cdt_kinematics` não-foliado) não tinha. Código/dados:
> `task1_kinematics_foliated.py`, `task1_foliated_kinematics.json`. Motivo: a medição original
> rodou sobre um gerador de triangulação **genérico** (sphere/DT); esta amarra o veredito ao
> substrato **foliado** que de fato vai para F1b/F2.

**Gate da reconstrução do 1-esqueleto (engenharia):** o grafo de vértices reconstruído da
triângulo-adjacência do motor F1 dá V=Σℓ, E=3N/2, ⟨z⟩=6.0 **exatos** → reconstrução correta.

**Medição (mesmos estimadores, ladder de vértices V=500/1000/2000, 4 seeds):**

| Ensemble | ⟨z⟩ | C4 | C_trans |
|---|---|---|---|
| **CDT FOLIADO (motor F1)** | **6.000** (exato) | **0.103** (0.103/0.1025/0.1027, estável) | 0.353 |
| genérico NÃO-foliado (Pachner livre, controle) | 5.98→5.99 (→6) | 0.149 (0.155→0.149) | 0.31 |
| Poisson (mean-field, ref.) | — | 0.029–0.054 ↓ | — |
| CSG (tree-like, ref.) | — | 0.019 | — |

**Teste de trivialidade de C4 (pré-registrado nesta tarefa):** C4 foliado (0.1027) **vs** C4
genérico (0.1486) → Δ=0.046 contra 3σ=0.0025 (**~18σ**). ⇒ **C4 NÃO é trivial nesta classe**: a
folheação deixa uma **impressão digital mensurável** — *abaixa* C4 de ~0.149 (triangulação livre)
para ~0.103 (foliada). A preocupação "C4 é trivialmente positivo porque toda face é triângulo"
é **parcialmente** verdadeira mas **não fatal**: embora C4~0.1 seja em parte *de-construção*
(ressalva 1 já registrada — toda triangulação 2D tem laços), o valor foliado é **estatisticamente
distinto** do genérico **e** ~5× o Poisson e ~5× o CSG → **C4 discrimina CDT de mean-field/árvore**.

**Veredito do gatilho (qualificado, agora no substrato certo):** **ARMADO confirmado.**
⟨z⟩ satura (finito, =6 — *trivial por Euler*, barreira 1 de-construção) **E** C4 satura num valor
**não-trivial** (0.103), separado de mean-field (Poisson) e de árvore (CSG), **e** portador da
assinatura da folheação (≠ triangulação genérica). As duas ressalvas originais **permanecem** e
foram, em parte, **resolvidas por F1**: ressalva 1 (barreira 1 trivial) — confirmada exatamente
(⟨z⟩=6); ressalva 2 (geometria global sadia / branched-polymer) — **resolvida** pelo gate G1
(**d_H=2**, geometria estendida sadia) + cross-check β=0 (`TEORIA_CDT/F1_acao/F1_SYNTHESIS.md §2b`:
em 2D a folheação, não a ação, exclui o branched-polymer). **Pendente genuíno:** dim 3 (onde ⟨z⟩
volta a ser informativo, fora de Euler) — é o alvo de F1b.
