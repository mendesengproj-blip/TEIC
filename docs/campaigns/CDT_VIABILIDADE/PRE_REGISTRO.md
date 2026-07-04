# PRÉ-REGISTRO — GATILHO 3: viabilidade cinemática tipo-CDT (aresta fixa + colagem livre)

> Congelado **antes** de qualquer dado existir. Charter: prompt do usuário "Fila de
> substratos — executar Gatilho 2, projetar e travar Gatilho 3", Parte 2.
> Predecessores: `ESCALA_XI/` (Poisson, MORTO/Bethe), `RIDEOUT_SORKIN_TRIGGER/` (CSG,
> coordenação ARMADA), `RIDEOUT_SORKIN_CLUSTERING/` (CSG, clustering **NÃO ARMADO**).
>
> **STATUS: EXECUTADO 2026-06-27 → GATILHO 3 ARMADO (com ressalvas).** Protocolo abaixo intacto
> (congelado, critérios não reinterpretados). Resultado em `SYNTHESIS.md` (código
> `cdt_kinematics.py`, dados `cdt_kinematics.json`, figura `cdt_kinematics.png`). Achado: o
> 1-esqueleto da triangulação 2D (regime flipped/DT) tem C4≈0.145 saturante (~5× o piso
> mean-field, ordem da rede 2D) ⇒ passa a barreira de laços. Ressalvas: ⟨z⟩→6 é identidade de
> Euler em 2D (barreira de coordenação trivial, não conquistada); Pachner sem ação pode gerar
> patologia branched-polymer na geometria global (cinemática local ≠ dinâmica). Campanha
> completa com AÇÃO fica PENDENTE, não iniciada.
> **Prioridade: IMEDIATA** — fixada pelo branching §2.4 com o veredito real da Parte 1
> (Gatilho 2 = NÃO ARMADO: o CSG é tipo-árvore, então a busca por substrato com laços de
> dimensão finita continua, e a colagem livre tipo-Pachner é a próxima candidata natural).
>
> **Data de congelamento:** 2026-06-27.

---

## 1. A QUARTA VIA E POR QUE EXISTE (a fila de substratos)

Quatro famílias de substrato, distintas, testadas por **filtros cinemáticos baratos** (duas
barreiras) ANTES de qualquer ação/dinâmica/integral de caminho:

| Via | Substrato | Tamanho de link | Fundo | Status |
|---|---|---|---|---|
| 1 | **Poisson** (sprinkling Minkowski) | nenhum | Minkowski | **MORTA** (Bethe: ⟨z⟩ diverge) |
| 2 | **CSG** (crescimento sequencial) | nenhum | nenhum | **ENCERRADA** (⟨z⟩ finito mas grafo tipo-árvore, C4 sub-MF) |
| 3 | **Não-localidade intermediária** (B_k) | meio-inserido (ℓ_k) | Minkowski | nunca testada como família própria |
| 4 | **Tipo-CDT** (aresta fixa + colagem livre) | **fixo `[External]`** | nenhum | **esta ficha** |

A Via 4 é distinta: o tamanho de link é **fixo por construção**, mas a **combinatória de
colagem é livre** — soma/passeio sobre as maneiras de colar blocos simpliciais (movimentos
tipo-Pachner), não um reticulado rígido único. (Em CDT real, a invariância de Lorentz emerge
**estatisticamente** da soma sobre geometrias, não de uma colagem particular.)

---

## 2. ALERTA ANTI-CIRCULARIDADE (crítico — diferente das barreiras anteriores)

O tamanho de link fixo aqui **é inserido por construção** — é **`[External]`, declarado, NÃO
uma descoberta**. **Nada nesta campanha pode ser formulado como "uma escala emergiu"** — seria
circular, a escala já estava lá. O Gatilho 3 testa uma questão **puramente cinemática/
estrutural**: a classe (aresta fixa + colagem livre) escapa das **duas** barreiras que
mataram/ameaçaram as vias anteriores —

1. divergência de coordenação (Bethe, matou Poisson), **e**
2. topologia tipo-árvore / clustering-zero (matou CSG)?

Isto **não** é "achamos a escala" — é "esta classe passa os dois filtros cinemáticos baratos
antes de qualquer construção de ação completa". O guard anti-circularidade do Gatilho 1
permanece: nenhuma expressão métrica/relativística entra nos estimadores; só contagens
combinatórias adimensionais.

---

## 3. ESTRUTURA MÍNIMA A MEDIR (cinemática pura, SEM ação)

### 3.1 Ensemble (combinatório, sem peso de ação)
Gerar um ensemble de complexos simpliciais com arestas de comprimento fixo (unidade
arbitrária, `[External]` declarada), conectados por um conjunto mínimo de **movimentos tipo-
Pachner** (flips/bistellar em dim 2; (2,3)/(1,4) em dim 3). **Sem peso de ação** — colagens
válidas igualmente prováveis (ou passeio aleatório uniforme sobre colagens válidas a partir de
uma triangulação-semente, com checagem de validade do complexo a cada passo). Reaproveitar, se
possível, estruturas de grafo já existentes (`orientation_core.Graph` CSR, ou listas de
adjacência como em `RIDEOUT_SORKIN_CLUSTERING/rs_clustering.py`).

### 3.2 Grafo a medir e estimadores (mesmos das campanhas anteriores)
Medir no **1-esqueleto** do complexo (vértices = 0-simplices; arestas = 1-simplices), no mesmo
ladder de N: `[500, 1000, 2000, 3300, 3888]`, ≥5 sementes.
- **(a) Coordenação ⟨z⟩(N)** — mesmo estimador da ESCALA_XI/RIDEOUT_SORKIN_TRIGGER
  (`z = 2·#arestas/N`).
- **(b) Clustering** — a suíte de `RIDEOUT_SORKIN_CLUSTERING/rs_clustering.py` VERBATIM:
  transitividade (3-ciclos) **E** square-clustering C4 (4-ciclos), com o mesmo gate de
  validação (caminho→0, K_n→1, toro 2D→0.125).

> **LIÇÃO DA PARTE 1 incorporada (importante).** No grafo de **cobertura/Hasse** do CSG a
> transitividade é **0 por teorema** (Hasse livre de triângulos), então lá só o C4 discrimina.
> **Aqui NÃO** — o 1-esqueleto de uma **triangulação** é feito de triângulos (2-simplices) por
> construção, então a transitividade é **não-degenerada e volta a ser o observável primário
> significativo**. Reportar AMBOS (transitividade primária + C4 secundário) e declarar
> explicitamente que o teorema de degeneração da Parte 1 **não se aplica** ao 1-esqueleto.

### 3.3 Sobreposição obrigatória
Plotar as três curvas no mesmo eixo (clustering vs N): **Poisson** (controle mean-field,
C4 sub-mean-field decaindo), **CSG** (resultado da Parte 1: tipo-árvore), **tipo-CDT** (a medir).
Incluir a linha de referência **rede de dimensão finita** (toro 2D, transitividade/C4 fixos) —
o alvo que um substrato "loopy genuíno" deve aproximar.

---

## 4. CRITÉRIOS (congelados — branching pela Parte 1 = NÃO ARMADO)

Como a Parte 1 deu **GATILHO 2 NÃO ARMADO**, a linha tipo-CDT é a **prioridade imediata
seguinte**, e este pré-registro testa especificamente a lição da Parte 1.

**Hipótese motivadora (declarada como hipótese, NÃO resultado garantido):** o que matou o CSG
foi a ausência de laços de dimensão finita apesar da coordenação finita (clustering sub-mean-
field). A **colagem livre tipo-Pachner** é exatamente o ingrediente que falta ao CSG: movimentos
de Pachner em dimensão ≥2 tipicamente criam vizinhanças **com laços** (um flip 2D substitui a
diagonal de um quadrilátero, gerando novos triângulos/quadrados locais), ao contrário de uma
árvore de crescimento sequencial que nunca revisita/reconecta. Logo **pode** desenvolver
clustering de dimensão finita. **Não é garantido** (ver prior §5).

**Critérios (sem inflar depois):**
- **GATILHO 3 ARMADO:** em algum regime do espaço de movimentos testado, **⟨z⟩(N) satura**
  (finito, como o CSG — passa a 1ª barreira) **E** o clustering **satura num valor positivo
  robustamente acima do controle mean-field de Poisson** e na direção da referência de rede
  dimensional-finita (transitividade > 0 saturando, e/ou C4 saturando claramente > C4_Poisson).
  ⇒ a classe passa as DUAS barreiras; só então se justificaria desenhar a campanha completa
  (ação + integral de caminho), fora do escopo de gatilhos baratos.
- **GATILHO 3 NÃO ARMADO:** tipo-CDT **replica a divergência de coordenação do Poisson**
  (⟨z⟩→∞) **OU** **replica o clustering-zero/sub-MF do CSG** (tipo-árvore). ⇒ a busca por
  substrato alternativo via **cinemática pura** está **esgotada** nas três famílias testáveis
  baratas (Poisson, CSG, tipo-CDT); restariam só a Via 3 (não-localidade intermediária, nunca
  testada como família própria) e a **dinâmica completa** (ação real + integral de caminho +
  rotação de Wick), ambas fora do escopo de gatilhos baratos.

**SEM ANNEALING:** os dois vereditos estão pré-definidos; o critério "acima do controle MF" é a
lição metodológica direta da Parte 1 (onde um platô fraco isolado era enganoso e só o controle
de Poisson resolveu) — fixado aqui ANTES dos dados, não inventado depois.

---

## 5. PRIOR HONESTO (declarar, NÃO pender — com limitação SIMÉTRICA)

**Genuinamente em aberto.** Razão estrutural para suspeitar laços: a soma sobre colagens é
exatamente o ingrediente que falta ao CSG (regra sequencial única, sem revisita/reconexão);
movimentos de Pachner criam vizinhanças locais com ciclos. **MAS — limitação simétrica, igual
peso:** na literatura real de triangulações dinâmicas, movimentos tipo-Pachner aleatórios
**sem nenhum peso de ação** são conhecidos por gerar **geometrias patológicas** — dimensão de
Hausdorff colapsando, configurações degeneradas tipo "**branched polymer**" (árvore de galhos)
ou aglomerados singulares de coordenação divergente. É **por isso** que CDT real (a) pesa a
soma com uma ação de Regge/Einstein-Hilbert e (b) faz rotação de Wick antes de extrair física.
Consequências para o peso a dar ao resultado:
- Um resultado cinemático puro **positivo** (Gatilho 3 ARMADO) é **necessário mas pode não
  significar nada** sobre a teoria dinâmica completa — a colagem uniforme não é a medida física.
- Um resultado **negativo** (NÃO ARMADO) **pode ser artefato da ausência de peso de ação**, não
  uma propriedade intrínseca da classe tipo-CDT pesada.

⇒ **O Gatilho 3, como os anteriores, é um filtro barato NECESSÁRIO, não uma decisão sobre a
teoria dinâmica.** Registrar esta ressalva limita explicitamente quanto peso colocar no
resultado, em **qualquer** direção. (Mesma disciplina de honestidade de escopo das campanhas
anteriores: cinemática ≠ dinâmica.)

---

## 6. O QUE NÃO FAZER

- **Não executar esta campanha agora.** Só o protocolo é travado aqui.
- **Não tratar o tamanho de link fixo como "escala emergente"** em lugar nenhum — é `[External]`
  por construção (§2).
- **Não prometer que movimentos de Pachner aleatórios são dinamicamente significativos** — a
  ressalva da literatura (§5) é parte do veredito futuro, não nota de rodapé.
- **Não rodar a campanha completa (ação + integral de caminho)** mesmo que o Gatilho 3 arme — é
  decisão separada, fora do escopo de gatilhos baratos.
- **Não reusar a degeneração de triângulos da Parte 1** — ela é específica do grafo de Hasse;
  no 1-esqueleto da triangulação a transitividade é significativa (§3.2).
