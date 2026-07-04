# PRÉ-REGISTRO — Percolação de longo alcance sobre a ordem causal (3ª família, gatilho cinemático)

**Data de congelamento:** 2026-06-29 (critérios fixados ANTES de qualquer execução)
**Diretório:** `docs/campaigns/PERCOLACAO_LONGO_ALCANCE/`
**Natureza:** gatilho cinemático barato (coordenação ⟨z⟩ + clustering C4), **sem** ferromagneto, **sem** medição de ξ. Mesma disciplina de funil dos Gatilhos 1–3 (RIDEOUT_SORKIN_TRIGGER / RIDEOUT_SORKIN_CLUSTERING / CDT_VIABILIDADE).

---

## 1. A família e o substrato

Sobre o **mesmo sprinkling de Poisson** já validado (ESCALA_XI: `causal_core.sprinkle_box`, Lorentz preservado por construção), substitui-se a regra de conexão "todo par causalmente relacionado conecta" por uma regra de **percolação de longo alcance** sobre a ordem causal:

dois eventos causalmente relacionados `i ≺ j` conectam (aresta não-direcionada) com probabilidade

```
p(Δτ_ij) = min(1, (Δτ_ij / Δτ₀)^(−σ))
```

- `Δτ_ij = sqrt(interval²)` = tempo-próprio entre os dois eventos = **invariante de Lorentz por definição**.
- `σ` = **único parâmetro novo, adimensional**, a varrer.
- `Δτ₀` = escala de normalização **`[External]`**, **declarada**, fixada à escala de discretude do sprinkling `ρ^(−1/d)` (o mesmo `ρ` que já era externo desde a ESCALA_XI). Não há física nova nela.

**Dimensão:** 2+1D (`d=3`, coords `t,x,y`) — alinhada à referência de Poisson `dim=3` da RIDEOUT_SORKIN_CLUSTERING e à menor dimensão (maior chance de laços de dimensão finita).

**Decaimento esperado da coordenação (motiva a localização do scan):** o número de vizinhos causais dentro de tempo-próprio τ cresce ~τ^d; a coordenação esperada é `z(σ) ~ ∫ ρ τ^(d−1) min(1,(τ/τ₀)^(−σ)) dτ` com `τ₀=ρ^(−1/d)`. Esse integral, com cutoff superior crescendo com o sistema, **diverge com N para σ < d e satura para σ > d** → transição esperada em **σ ≈ d = 3**. O scan cobre densamente 0.5 → 6.

---

## 2. ALERTA ANTI-CIRCULARIDADE (travas)

1. **NÃO se testa "emergência de escala".** `Δτ₀` é `[External]`, declarado e fixo a `ρ^(−1/d)`. O que se mede é **classe de universalidade cinemática** (⟨z⟩ + C4) em função de σ.
2. **Invariância de Lorentz é gate obrigatório e separado da física (Seção 3.5).** A regra depende só de `Δτ_ij` (invariante) e de um sorteio por par `u_ij` chaveado pela **identidade dos nós** (preservada sob boost), nunca por coordenada. Verificação: re-derivar o grafo a partir de coordenadas *boosted* (mesmo conjunto de eventos, referencial diferente) deve dar **o mesmo grafo** (⟨z⟩ e C4 idênticos).
3. **"Saturou" nunca é decisivo sem o diagnóstico de expoente local** `d⟨z⟩/d ln N` e `dC4/d ln N` nos pontos extremos do scan.

---

## 3. GATE DE VALIDAÇÃO (antes de qualquer leitura física)

1. **σ grande (decaimento rápido, σ=6 ≥ d):** só pares causais muito próximos conectam → ⟨z⟩ **baixo** e saturante (análogo a CSG/Hasse, regime esparso).
2. **σ → 0 (sem decaimento, σ=0.5):** quase todo par causalmente relacionado conecta → ⟨z⟩ **diverge fortemente com N**, mais densamente que o grafo de cobertura de Poisson (extremo mais denso possível, claramente mean-field).
3. **Cross-check de estimador:** ⟨z⟩ e C4 são calculados pela função `clustering_metrics` **importada VERBATIM** da RIDEOUT_SORKIN_CLUSTERING; ⟨z⟩ deve bater `2·#arestas/N` à precisão de máquina.
4. **Triviality do C4:** controle de grafo aleatório com a **mesma contagem de arestas** sorteadas uniformemente entre os pares causais (sem a estrutura de decaimento por Δτ). O C4 da família só conta como não-trivial se ficar **acima** desse controle.
5. **Invariância de Lorentz:** boost de rapidez η≠0 numa direção espacial; recomputar C e Δτ; o grafo (⟨z⟩, C4, lista de arestas) deve ser **idêntico** ao do referencial original (tolerância numérica em τ; arestas bit-idênticas).

**Gate VERMELHO em qualquer item ⇒ ABORTA**, sem leitura física.

---

## 4. MEDIÇÃO CENTRAL

- Scan de σ ∈ **{0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.0, 6.0}** (10 valores, cobre os dois extremos e a janela esperada em σ≈3).
- Ladder de N (via ρ, box fixo `[(0,1)]³`, `N≈ρ`): **{500, 1000, 2000, 3000}**; seeds reduzidos no topo se necessário (mesma prática do lineage).
- Para cada (σ, N): ⟨z⟩(N,σ) e C4(N,σ) com SEM; e o **expoente local** `d⟨z⟩/d lnN`, `dC4/d lnN` nos dois maiores N.
- Dois gráficos no maior N: ⟨z⟩(σ) e C4(σ), com barras de erro e referências de Poisson/CSG nos extremos.

---

## 5. CRITÉRIOS (pré-registrados, TRAVADOS antes de rodar)

Discriminadores operacionais (mesma disciplina dos Gatilhos 1–3):
- **⟨z⟩ satura** ⟺ expoente local relativo `(d⟨z⟩/dlnN)/z_top < 0.05` E não-crescente.
- **C4 satura > 0** ⟺ `C4_top > 0.02`, expoente local `dC4/dlnN` não decaindo a zero (`C4_top ≥ 0.5·C4_first`), **E** `C4_top` acima do controle aleatório de mesma densidade (Seção 3.4).

Veredito:

- **JANELA ENCONTRADA** (resultado novo, sem precedente nesta linha): existe um intervalo de σ onde **⟨z⟩ satura E C4 satura > 0 simultaneamente**. Seria o **primeiro substrato de toda a investigação** a passar as DUAS barreiras cinemáticas ao mesmo tempo de forma **conquistada** (não trivial por Euler como o tipo-CDT 2D).

- **SEM JANELA** (o trade-off de sempre, em versão contínua): a região de σ onde ⟨z⟩ satura é a mesma onde C4 **já decai a zero** (ou cai ao controle), e a região de C4 não-trivial é a mesma onde ⟨z⟩ **ainda diverge** — troca contínua e suave em σ, **sem ponto de sobreposição**. Reproduz o trade-off coordenação-vs-clustering (Poisson vs CSG vs CDT) como função contínua de σ.

- **TROCA COM LORENTZ** (mais informativo, se ocorrer): se uma janela aparente só existir mediante uma regularização que **falhe** o gate de invariância (Seção 3.5) — registrar como **trade-off quantificado entre invariância de Lorentz e escape do mean-field**, com o valor de σ onde a invariância começa a falhar. Possivelmente o resultado mais valioso da linha, ainda que morte.

---

## 6. O QUE NÃO FAZER (travas de funil)

- Não rodar ferromagneto nem medir ξ — gatilho puramente cinemático.
- Não pular o gate de Lorentz (Seção 3.5).
- Não tratar 3 pontos de σ como scan suficiente — scan completo de 10.
- Não concluir "satura"/"decai" sem expoente local nos extremos.
- Não avançar para qualquer ferromagneto/ξ sobre esta família sem reportar o veredito e receber autorização.
