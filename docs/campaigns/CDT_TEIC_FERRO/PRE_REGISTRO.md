# PRÉ-REGISTRO — CDT×TEIC: o ferromagneto de orientação roda sobre o substrato CDT 3D?

> **Congelado ANTES de qualquer leitura física.** Data: 2026-06-28. Esta campanha porta o
> mecanismo central da TEIC (ferromagneto de orientação O(3), GOLDSTONE_A3) para o substrato
> **CDT 3D já validado e gateado em F1b** (`TEORIA_CDT/F1b_acao/`), **sem a semente** (que
> morreu em FS-3D/D2). Reusa `orientation_core` (O3Model, Graph, structure_factor,
> measure_correlation) e o `xi_suite` da ESCALA_XI **sem reimplementar**, e o motor CDT 3D
> `f1b_cdt3d.py` **sem modificar a geometria** (só como gerador de substrato).
>
> Esta é, em substância, a campanha **"CDT-COMPLETA (tipo-CDT + ação + ξ)"** que o
> `RESEARCH_MAP §FILA DE SUBSTRATOS` registrava como PENDENTE — agora viável porque F1b
> entregou o motor 3D **com ação de Regge + Wick** validado (resolve a ressalva-2 do Gatilho 3:
> geometria global sadia, d_H→~3, não branched-polymer).

---

## 0. DUAS perguntas independentes — vereditos SEPARADOS (nunca um só)

- **A (reprodução):** o ferromagneto O(3) sobre o CDT 3D produz a **mesma física qualitativa**
  que sobre o Poisson (LRO genuíno por FSS, U₄→ordenado, Goldstones escalares)?
- **B (universalidade):** este substrato — geometria dinâmica, C4≠0 já em 2D — **escapa do
  mean-field tipo-Bethe** que matou Poisson e CSG? Isto é, há **criticalidade genuína**
  (U₄(J) cruza em J_c único; χ_max∝N^x com x→geométrico, não MF) em vez de mean-field?

A é reprodução de física conhecida; B é universalidade nova. Reportados **separados**.

## 1. ANTI-CIRCULARIDADE (igual ESCALA_XI / Gatilhos 1-3)

A aresta do CDT é `[External]` por F1b (decisão antiga, não desta tarefa). **Nada aqui é "uma
escala emergiu".** B testa **classe de universalidade** (criticalidade vs mean-field), não
emergência de escala absoluta. Toda quantidade é aritmética real sobre spins/grafo; nenhum T_c
inserido; J_c é **localizado pela varredura** (pico de χ), nunca um valor externo.

## 2. IMPLEMENTAÇÃO — escolhas CONGELADAS

### 2.1 Onde o campo vive + acoplamento (decisão 3.1.3 travada AQUI, antes de rodar)
- n⃗ ∈ S² em cada **vértice** do 1-esqueleto da triangulação CDT 3D (`cdt_substrate.py`,
  `cdt_skeleton_graph`). Acoplamento por aresta: **S = J Σ_⟨ij⟩ (1 − n⃗ᵢ·n⃗ⱼ)** (= −J Σ n⃗ᵢ·n⃗ⱼ
  a menos de constante; idêntico ao `O3Model` de `orientation_core`, usado VERBATIM).
- **Pesagem de links — DECISÃO: UNIFORME** (links espaciais e temporais com o MESMO J).
  **Razão (registrada antes de ver dados):** (i) é a "tensão mínima idêntica à TEIC original" —
  o `O3Model` acopla todos os links igualmente, sem peso por tipo; (ii) um peso espacial/temporal
  introduziria um parâmetro `[External]` novo que NÃO existe na forma mínima original; (iii) o
  1-esqueleto é o objeto type-agnóstico já usado para ⟨z⟩/C4 nos Gatilhos. **A variante com peso
  (análogo a Δτ_ij) fica como follow-up pré-registrado, NÃO decidida ad hoc depois.** (Diagnóstico:
  reportamos `frac_links_spatial` para transparência, mas ela não entra no acoplamento.)

### 2.2 Fase e volumes (reaproveita calibração de F1b)
- **Apenas a fase ESTENDIDA**, em **k₀=1 e k₀=3** (os dois pontos de FS-3D, p/ comparabilidade
  direta). **Nunca** a fase degenerada/branched-polymer (k₀≳6) — patológica por geometria.
- Volumes do **ladder do d_H de F1b** (T=10): Vt = 1500, 3000, 6000 → N₃ ≈ 1586, 3073, 6094
  (N₀ nós ≈ 250, 480, 940). Geometria CDT PURA equilibrada e congelada; média sobre seeds
  (snapshots independentes) para FSS, como ESCALA_XI mediava sobre sprinkles.

### 2.3 Gate de validação (ANTES de qualquer leitura)
Com o MESMO pipeline de medição: **(i)** controle POSITIVO = O(3) em rede cúbica 3D periódica
(`build_lattice_3d`) → deve dar LRO + U₄(J) cruzando + χ_max∝N^~0.66; **(ii)** controle NEGATIVO
= O(3) em rede 2D (Mermin-Wagner: SEM LRO de simetria contínua) → m→0 por FSS; **(iii)** o grafo
CDT tem coloração própria (0 violações) e é conexo. Sem este gate verde, não confiar na medição.

## 3. PERGUNTA A — critérios de REPRODUÇÃO (congelados)
Observáveis de GOLDSTONE_A3: m(N₃), U₄, C(r) por distância de grafo (`measure_correlation`).
- **REPRODUZ:** m(N₃) acima do piso aleatório (m/floor>3, floor=1/√N₀), m-trend dlnm/dlnN > −0.15
  (não decai como artefato), U₄ > 0.55 (ordenado), C(r) satura em plateau positivo (`fit_forms`
  → 'const'). LRO genuíno por FSS — mesma assinatura qualitativa do Poisson original.
- **NÃO REPRODUZ:** m decai ~N^(−1/2), U₄→0, C(r) sem plateau.
- **Modos transversos escalares (opcional):** só se sobrar orçamento, via teste de polarização de
  GOLDSTONE_A3/FOTON. Se não rodar, fica **ADIADO explicitamente**, sem conclusão.

## 4. PERGUNTA B — critérios de UNIVERSALIDADE (mesmo padrão ESCALA_XI)
Varredura em J (reusando os MESMOS grafos por tamanho, como `xi_suite`). Observáveis:
- **U₄(J):** cruzamento das curvas de tamanhos diferentes num **J_c único** = criticalidade.
- **χ_max(N) = pico de χ=N·Var(m):** expoente x em χ_max∝N^x. Referências (mesma suite):
  controle 3D-lattice ≈ **N^0.66** (geométrico); **mean-field ≲ N^0.5** (Poisson/CSG).
- **ξ por distância de grafo** (substituto honesto, ver §5): ξ_g de C(r); razão ξ_g/L_g cresce/
  cruza (criticalidade) ou platô (mean-field).
- **ESCAPA DO MEAN-FIELD:** U₄ cruza em J_c único **E** χ_max-expoente aproxima do geométrico
  (do controle 3D), super-mean-field.
- **MEAN-FIELD (replica Poisson/CSG):** sem cruzamento limpo / χ_max-expoente ≲0.5 / ξ_g/L em platô.
- **Disciplina:** sinal intermediário = **NÃO RESOLVIDO com o orçamento de N**, sem forçar veredito.
- Sobrepor χ_max(N) e ξ_g/L do CDT no MESMO gráfico das curvas de Poisson (ESCALA_XI) e CSG.

## 5. DESVIO REGISTRADO — ξ_2nd de Fourier NÃO é portável (e por quê)
O `xi_second_moment` da ESCALA_XI usa **fator de estrutura de Fourier**, que exige **coordenadas
espaciais de embedding**. O CDT é **background-independent**: os vértices têm só rótulo de fatia
(tempo), não coordenadas espaciais. Logo o ξ_2nd/L_s de Fourier **não se aplica** sem inventar um
embedding (escolha artificial). **Substituição (declarada, não maquiada):** ξ por **distância de
grafo** (segundo momento de C(r), coordenada-livre) + os discriminadores **coordenada-livres** da
própria suite — **U₄(J)-crossing e χ_max∝N^x** — que carregam a Pergunta B (o veredito da própria
ESCALA_XI repousou no expoente de χ_max + U₄, não só no ξ de Fourier). Esta é uma adaptação
**necessária e fiel**, não um relaxamento de critério.

## 6. ENTREGÁVEIS
`cdt_substrate.py` (adaptador, feito), `ferro_cdt.py` (gate + A + B), `*.json` (dados),
`figura` (overlay χ_max/ξ_g vs Poisson/CSG), `SYNTHESIS.md` (vereditos A e B separados).
Atualizar `RESEARCH_MAP §FILA DE SUBSTRATOS` com CDT 3D como entrada própria (A e B).

**Resumo de uma linha:** rodar o ferromagneto O(3) **verbatim** sobre o 1-esqueleto do CDT 3D
**validado** (fase estendida, k₀=1,3; sem semente), responder SEPARADAMENTE se ele **reproduz** a
ordem da TEIC (A) e se **escapa do mean-field** (B), com ξ de Fourier honestamente substituído por
ξ de grafo + U₄-crossing + χ_max-expoente, tudo com a aresta já `[External]` e nada "escala emergiu".
