# SYNTHESIS — CDT×TEIC: o ferromagneto de orientação sobre o substrato CDT 3D validado

> **Pré-registro:** `PRE_REGISTRO.md` (critérios A e B congelados ANTES de rodar). **Código:**
> `cdt_substrate.py` (adaptador 1-esqueleto→Graph, motor CDT 3D de F1b intacto), `ferro_cdt.py`
> (gate + A + B, reusa `orientation_core`/`xi_suite` verbatim). **Dados:** `ferro_cdt.json`,
> `ferro_cdt.png`. **Data:** 2026-06-28. **Runtime:** 4125 s.
>
> Esta é a campanha **"CDT-COMPLETA (tipo-CDT + ação + ξ)"** que o `RESEARCH_MAP §FILA DE
> SUBSTRATOS` registrava como PENDENTE — agora viável porque F1b entregou o motor CDT 3D **com
> ação de Regge + Wick** validado (E0-3D verde, d_H→~3). Roda o ferromagneto O(3) da TEIC
> (GOLDSTONE_A3) **verbatim** sobre o 1-esqueleto da geometria CDT 3D na fase estendida (k₀=1,3),
> **sem a semente** (morta em FS-3D/D2).

---

## VEREDITOS (separados, como exige o pré-registro §0)

### Gate de validação: **VERDE**
O `O3Model` reproduz os anchors clássicos com o pipeline desta campanha: rede cúbica 3D → LRO
(m=0.86–0.88, U₄=0.667) ✓; rede 2D → m decai com N (0.77→0.65, Mermin-Wagner, sem LRO de
simetria contínua) ✓. Grafo CDT: coloração própria (0 violações), conexo.

### Pergunta A (reprodução): **REPRODUZ — LRO genuíno por FSS, nos dois k₀**
O ferromagneto de orientação sobre o CDT 3D produz a **mesma física qualitativa** da TEIC sobre
Poisson:

| k₀ | N₀ (nós) | m | m/floor | U₄ | C(r) | m-trend dlnm/dlnN |
|---|---|---|---|---|---|---|
| **1** | 238→920 | 0.948→0.940 | 14.6→**28.5** | 0.667 | **plateau** (C_long≈0.84–0.90) | **−0.006** |
| **3** | 282→1144 | 0.931→0.869 | 15.6→**29.4** | 0.667→0.661 | **plateau** (C_long≈0.84) | −0.050 |

m **estabiliza** (não decai), m/floor **cresce** com N (LRO real, não artefato), U₄ no valor
ordenado O(3) (2/3), C(r) **satura em plateau positivo** (`fit_forms`→'const'). **Mesma
assinatura qualitativa do resultado original sobre Poisson** (GOLDSTONE_A3). Veredito **REPRODUZ**
inequívoco. (Modos transversos escalares/vetoriais — §4 opcional — **NÃO testados**, sem
orçamento; registrado como **ADIADO**, sem conclusão, conforme pré-registro.)

### Pergunta B (universalidade): **NÃO RESOLVIDO — mean-field NÃO excluído (sinal mais limpo lean MF)**
**Não há demonstração de escape do mean-field com este orçamento.** O discriminante (χ_max∝N^x)
ficou **dominado por ruído** e os dois k₀ **discordam por artefato**:

| k₀ | χ_max(N) | expoente | J_c por tamanho | U₄@J_c |
|---|---|---|---|---|
| **1** | 1.49, 1.46, 2.05 | N^**0.24** | 0.22→0.18→**0.16** (deriva ↓) | 0.626→0.539 (deriva ↓) |
| **3** | 1.16, 1.39, **3.93** | N^**0.88** | 0.22, 0.22, 0.20 | 0.555, 0.624, 0.588 |
| *Poisson (ref)* | 1.0–1.4 | N^0.07 (plano=MF) | deriva ↓ | — |

**Por que NÃO RESOLVIDO (disciplina §4, "não interpretar ambíguo como decisivo"):**
1. **As curvas χ(J) são serrilhadas, não picos limpos** — ex. k₀=3, N=1144: χ = [0.34, 0.57,
   **1.85**, 1.25, **3.93**, 1.30, 0.69, 0.60]. O χ_max=3.93 é um **spike de ruído**, não um pico
   de susceptibilidade. O estimador χ=N·Var(m) com **4 seeds** sobre desordem *quenched* (cada
   grafo CDT tem J_c efetivo distinto → grande variância seed-a-seed) é ruidoso demais para
   extrair o expoente. Os expoentes 0.24 e 0.88 **bracketam** as referências (MF 0.5, geom 0.66)
   **sem resolver** — são artefato.
2. **O sinal mais limpo (k₀=1) lean MEAN-FIELD:** χ_max comparável ao Poisson (1.5–2.0 vs 1.0–1.4)
   com crescimento fraco, **e J_c deriva para baixo** (0.22→0.16) — exatamente a assinatura do
   Poisson (`baseline_3p1`: Jc_drifts_down=True). U₄@J_c também deriva (não cruza fixo).
3. **U₄(J) afia com N** (curvas mais íngremes a N maior) → uma transição **existe**, mas isso
   **não** distingue MF (que também tem transição, com expoentes MF) de criticalidade genuína; o
   discriminante é o expoente, que é noise-limited aqui.

**Leitura honesta:** o CDT 3D, com z~13–15 (coordenação alta do 1-esqueleto), **não demonstra**
escapar do mean-field; o sinal limpo o coloca **junto do Poisson/CSG** (mean-field), apesar de
ter C4≠0 (laços) — a alta coordenação domina. Mas o orçamento (4 seeds) **não exclui** uma
criticalidade fraca. **Veredito: NÃO RESOLVIDO, com o peso da evidência limpa em mean-field.**

---

## O que esta campanha estabelece (e o que não)

**Estabelece:**
1. **Pergunta A = REPRODUZ.** O mecanismo central da TEIC (ferromagneto de orientação O(3) → LRO +
   Goldstones) **roda e reproduz** sobre o substrato CDT 3D dinâmico validado — primeira vez que a
   ordem da TEIC é reproduzida sobre uma **geometria dinâmica** (não Poisson estático). A física
   conhecida sobrevive à troca de substrato.
2. **O motor CDT 3D de F1b é reutilizável como substrato** para a física da TEIC sem modificação
   (anti-contaminação respeitada: TEIC importa o CDT como substrato, não o contrário).

**NÃO estabelece (honestidade, anti-circularidade §1):**
1. **Pergunta B fica em aberto.** Não se demonstrou nem se excluiu o escape do mean-field; o
   sinal limpo lean MF (junto de Poisson/CSG). **"Geometria dinâmica não BASTOU"** para
   demonstrar uma classe de universalidade nova com este orçamento — o resultado anticipado na
   §6 do prompt como "interessante por si", aqui com a ressalva de **noise-limited**.
2. **Nada "escala emergiu"** (a aresta do CDT é `[External]` por F1b; B é sobre classe, não escala).
3. **Modos transversos (escalar vs vetorial) não testados** — ADIADO.

## Follow-ups registrados (não decididos aqui)
- **B com muitos seeds (12–24):** média de desordem para bater o ruído de χ e resolver o expoente
  de χ_max (o único caminho para decidir B de verdade; custo: horas de equilibração CDT).
- **Acoplamento com peso espacial/temporal** (variante de 3.1.3, deixada pré-registrada): a tensão
  uniforme foi a escolha mínima; um peso por tipo de link é o follow-up.
- **Polarização dos modos transversos** (A §4 opcional): natureza escalar/vetorial dos Goldstones.

**Resumo de uma linha:** o ferromagneto O(3) da TEIC, rodado **verbatim** sobre o 1-esqueleto do
CDT 3D **validado** (fase estendida, sem semente), **REPRODUZ o LRO genuíno** da TEIC (Pergunta A,
limpo nos dois k₀) — mas a **classe de universalidade (Pergunta B) fica NÃO RESOLVIDA** com 4
seeds (χ_max noise-dominated; o sinal limpo de k₀=1 lean mean-field junto do Poisson/CSG, J_c
deriva ↓), de modo que **geometria dinâmica reproduz a ordem mas não demonstra escapar do
mean-field** — resolver B exige média de desordem com muitos seeds (follow-up registrado).
