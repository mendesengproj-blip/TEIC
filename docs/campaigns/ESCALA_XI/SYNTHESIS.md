# SÍNTESE — CAMPANHA XI: Um comprimento de correlação pode divergir?

> Pré-registro: `PRE_REGISTRO.md` (congelado 2026-06-24, antes de qualquer run).
> Engine reutilizado SEM MODIFICAÇÃO: `orientation_core.py` (O3Model, causal_link_graph,
> structure_factor). Código novo só na camada de ANÁLISE: `xi_suite.py`,
> `run_campaign.py`, `analyse.py`, `validate_positive.py`, `focused_knn.py`.
> Guard `tests/test_no_circularity.py` VERDE em toda a campanha.

## VEREDITO DE UMA LINHA

**HIPÓTESE FALSIFICADA (com uma fronteira honesta).** Reduzir a coordenação
não-local do substrato **não** faz emergir um comprimento de correlação divergente.
Pior: as duas alavancas "geométricas" (dimensão menor, janela de tempo-próprio) **nem
sequer reduzem a coordenação** — z diverge com N e J_c→0 em ambas. A única alavanca que
de fato fixa a coordenação (cap de contagem k-NN) produz uma transição contínua, mas o
comprimento de correlação **métrico** ξ_2nd/L permanece um platô pequeno (~0.1) de
ordem-de-longo-alcance, **não** um pico crítico — é a armadilha LRO, circular. O
caráter mean-field é **estrutural** para esta classe de substratos.

---

## 1. O CONTROLE POSITIVO (gate de confiança do estimador)

Antes de confiar em qualquer "não", rodei a suíte idêntica no **O(3) na rede cúbica 3D
periódica** — substrato com transição de 2ª ordem de manual (J_c≈0.69). Resultado:
- **U₄ cruza limpo em J≈0.69** (= J_c). ✓
- **χ_max ∝ N^0.667** = exatamente γ/ν/d do Heisenberg-3D (γ/ν≈1.97). ✓
- z FIXO (=6), J_c FIXO. ✓

**Porém** o estimador ξ_2nd de segundo-momento (transverso) é RUIDOSO mesmo aqui: na
fase ordenada os modos transversos são Goldstone (S(k)∝1/k², inversão OZ singular). Por
isso o veredito da campanha **não repousa em ξ/L sozinho** (que falha até no controle),
mas no tripé **z(N) fixo-vs-diverge + drift de J_c + escala de χ_max**, com ξ/L como
suporte. O controle prova que a suíte ENXERGA criticidade genuína via U₄+χ_max.

---

## 2. TABELA DE VEREDITO (todas as alavancas)

| Alavanca | escala inserida | z(N) | J_c(N) | ξ/L em J_c | χ_max | veredito |
|---|---|---|---|---|---|---|
| **Controle 3D** (lattice) | — | **6→6 fixo** | 0.69 fixo | cruza* | **N^0.67** | CRITICIDADE (ref.) |
| **Baseline** Hasse (3+1)D | — | 33**→103 diverge** | 0.10**→0.03→0** | decresce | off-grid | MEAN-FIELD (sem ponto fixo) |
| **C** — (2+1)D *(sem escala)* | nenhuma `[Derived]` | 14**→33 diverge** | 0.19**→0.10→0** | — | off-grid | MEAN-FIELD (sem ponto fixo) |
| **B** — janela ℓ_k=0.8 | ℓ_k `[External]` | 15**→43 diverge** | 0.19**→0.07→0** | — | off-grid | MEAN-FIELD (sem ponto fixo) |
| **A** — cap k-NN k=3 | k `[External]` | **4.5→5.2 fixo** (→2k=6) | **0.72→0.58 fixo** | platô ~0.1 | N^≲0.5 ruidoso | FRONTEIRA → mean-field (Bethe) |
| **A** — cap k-NN k=6 | k `[External]` | **8.6→9.9 fixo** (→2k=12) | **0.36→0.26 fixo** | platô | — | FRONTEIRA → mean-field (Bethe) |

\* o ξ/L do controle "cruza" apenas no sentido fraco (ruído Goldstone); a criticidade
do controle está certificada por U₄+χ_max, não por ξ/L.

---

## 3. OS TRÊS ACHADOS ESTRUTURAIS

### Achado 1 — A não-localidade é Lorentz-protegida: só contagem a reduz
As alavancas B (janela métrica de tempo-próprio) e C (dimensão menor) **falham em
reduzir a coordenação**: z DIVERGE com N em ambas (×2.3 a ×2.8 no ladder), exatamente
como o baseline cru (×3.1). Mecanismo: um corte por **tempo-próprio** ℓ_k não localiza
porque o slab hiperbólico {0<τ²<ℓ_k²} tem volume que cresce com a caixa (pares
boostados têm τ pequeno e separação coordenada enorme). Reduzir a **dimensão** também
não cura — o grafo de Hasse (2+1)D ainda tem z→∞. **A invariância de Lorentz proíbe um
corte local de coordenação por qualquer escala métrica.** O único redutor de coordenação
admissível é um **cap de contagem** (k-NN, Lorentz-invariante: usa o tempo-próprio
invariante só para ordenar, não para cortar). Um corte por distância ESPACIAL seria
circular (injeta um referencial) — e proibido pelo guard em espírito.

### Achado 2 — Sem cap, NÃO HÁ ponto crítico fixo: J_c→0
No baseline, em C e em B, conforme z→∞ o acoplamento crítico **J_c→0** (0.10→0.03 no
baseline; padrão idêntico em C e B). Isto é a assinatura mais nua possível de
mean-field/não-geométrico: como num grafo completo (J_c∼1/z), a transição "escorre"
para acoplamento nulo no limite termodinâmico. **Um ξ divergente não tem onde morar:
não existe um J_c fixo onde ele divergiria.** Isto sozinho mata a hipótese para 3 dos 4
substratos — sem precisar medir ξ.

### Achado 3 — Com cap (k-NN), há transição contínua, mas ξ métrico NÃO diverge
O cap k-NN é o único substrato com coordenação assintoticamente fixa (z→2k satura) e
J_c fixo. Lá existe uma transição contínua genuína: **U₄ cruza em J≈0.6** e χ_max cresce
sub-volume. MAS o teste decisivo da campanha — ξ_2nd/L **métrico** (de S(k) com as
coordenadas espaciais reais) — falha em divergir de forma não-circular:

- ξ/L em J_c≈0.64 cresce com L (0.063→0.099) — o que *isoladamente* satisfaria o
  critério ingênuo. **Porém** ξ/L cresce **identicamente** fundo na fase ordenada
  (J=0.88: 0.076→0.102; J=1.00: idem) e tem o **mesmo valor** (~0.1) em J_c e em J=2×J_c.
- Num ponto crítico **genuíno**, ξ/L tem um **PICO em J_c** (a curvatura de S(k) perto
  de k=0 é máxima na criticidade). Aqui ξ/L é um **platô** ~0.1 chato por toda a fase
  ordenada → é a **armadilha LRO**: qualquer ferromagneto ordenado tem correlação que
  abrange o sistema (ξ∼L trivialmente), logo ξ/L∼const e ξ/ℓ→∞ por LRO, **não** por
  criticidade. O teste ξ/ℓ→∞ do charter é **necessário mas não suficiente**; o
  suficiente (pico de ξ/L em J_c) **falha**.
- χ_max ∝ N^≲0.5 (ruidoso, não-monotônico): consistente com FSS **mean-field** (d>d_c=4,
  expoente d/2→N^{1/2}), **não** com a criticidade geométrica do controle (N^0.67).

**Interpretação:** o grafo k-NN causal é uma rede esparsa **small-world / tipo
árvore-de-Bethe** (links causais saltam no espaço). Modelo de Heisenberg numa rede
localmente-árvore = **mean-field exato**. A correlação de GRAFO diverge (mean-field),
mas a correlação **MÉTRICA** (em x_i real) é plana — não há geometria de dimensão finita
para ancorar um ξ que rastreie L como pico crítico.

---

## 4. CRITÉRIO DE MORTE (pré-registrado) — VERIFICAÇÃO

> "Se em todas as alavancas A,B,C que levam a coordenação ao regime O(1)–O(10)
> mantendo LRO, ξ_2nd(L) em J_c não diverge (ξ/L não-crescente, U₄ sem cruzamento
> invariante, χ_max em lei de volume/mean-field) → FALSIFICADA; mean-field ESTRUTURAL."

- **B e C nem entram na premissa**: não levam a coordenação a O(1)–O(10) — z diverge.
  (Achado 1: só o cap de contagem reduz coordenação.) Falsificação trivial para elas.
- **A entra na premissa** (z~5–10 fixo, LRO mantida) e: ξ/L é um platô LRO (não um pico
  crítico — não-circular FALHA), χ_max ∝ N^≲0.5 (mean-field FSS, não geométrico). U₄
  cruza, MAS criticidade mean-field também cruza U₄ — o cruzamento não distingue, e os
  expoentes + o platô de ξ/L dizem mean-field.

**⇒ CRITÉRIO DE MORTE SATISFEITO. Hipótese FALSIFICADA. Mean-field = ESTRUTURAL.**

A fronteira honesta: A tem uma transição contínua real com cruzamento de U₄; eu **não**
a chamo de sucesso porque (i) ξ/L é platô-LRO e não pico crítico, (ii) χ_max é
mean-field-FSS e não geométrico, (iii) o grafo é Bethe-like (mean-field por teorema).

---

## 5. CIRCULARIDADE — contabilidade `[External]`

| Escala inserida | onde | papel | usada na conclusão? |
|---|---|---|---|
| k (cap k-NN) | Alavanca A | fixa z≈2k | **NÃO** — conclusão só usa adimensionais (ξ/L, χ_max∝N^x, cruzamento U₄) |
| ℓ_k (janela) | Alavanca B | banda de τ | **NÃO** — B morre antes (z diverge) |
| nenhuma | Alavanca C | — | C é o teste limpo (sem escala) e mesmo assim morre |

Nenhuma conclusão de emergência usa um ξ absoluto. O sinal ingênuo ξ/ℓ→∞ aparece em A
mas é a armadilha LRO (necessário-não-suficiente), explicitamente marcado como circular.

---

## 6. CONSEQUÊNCIAS PARA O PROGRAMA

1. **Reforça a nota de rodapé 1 do paper do fóton** ("sem ξ divergente") com um
   mecanismo: não é só o Hasse cru — é **estrutural a substratos causais**, porque
   (a) Lorentz proíbe corte métrico de coordenação e (b) o grafo causal esparso é
   Bethe-like (mean-field). Confirma e aprofunda a memória `b7-escalas-transmutacao`
   (MORTE_B7_MEANFIELD) e `b9-piano-no-vacuo`.
2. **A transmutação dimensional continua sem âncora** — não há ξ métrico divergente em
   nenhuma das classes testadas. Fecha esta frente.
3. **Resultado publicável (negativo forte):** "Por que conjuntos causais resistem a
   fabricar escalas" — a invariância de Lorentz + a topologia small-world são uma
   barreira dupla. O charter previu corretamente que o "não" é o resultado de valor.
4. **§10 do charter (crescimento sequencial Rideout–Sorkin) NÃO se justifica** como
   sucessor: o gatilho era "ao menos uma alavanca A–C dar sinal não-circular". Nenhuma
   deu. Frente dormente, não próxima.

---

## 7. RESIDUOS / FRONTEIRA (honestos, sem inflar)

- **ξ_2nd transverso é Goldstone-singular na fase ordenada** (falha até no controle);
  usei full-S(k) shell-averaged + tripé z/J_c/χ_max para decidir. Um ξ verdadeiramente
  limpo exigiria BC periódica no substrato causal (não-trivial) ou um estimador de ξ
  por colapso de dados com mais tamanhos.
- **A (k-NN) é FRONTEIRA, não MORTE-limpa:** tem U₄-crossing real. A morte vem do platô
  de ξ/L + χ_max mean-field + argumento Bethe. Um L≳10 com J_c travado (FSS multicanônico
  ao redor de J_c fixo) e BC periódica sharpening χ_max(0.5 vs 0.66) selaria. Registrado,
  não executado (custo alto, retorno baixo: o veredito já é robusto pelo Achado 1+2).
- **χ_max ruidoso** (8 sementes ainda pouco para Var(m) em rede esparsa). Não muda o
  veredito (sub-volume ≲0.5 em todo caso).

---

## 8. ATUALIZAÇÃO POSTERIOR (jun/2026) — refinação de precisão, NÃO reversão

> O veredito original acima (§4, §6) **permanece intacto e correto** para o que ele
> testou. Esta seção é adicionada **depois**, sem reescrever nada, na mesma disciplina
> de honestidade das campanhas anteriores.

A campanha **RIDEOUT_SORKIN_TRIGGER** (`docs/campaigns/RIDEOUT_SORKIN_TRIGGER/`) mediu a
coordenação ⟨z⟩(N) do grafo de Hasse de causal sets gerados por **crescimento sequencial
clássico (CSG / percolação transitiva)** — uma classe de geração **diferente** do
sprinkling — com o **mesmo estimador** desta campanha (cross-check numérico: diff 0).
Resultado: ⟨z⟩(N) **satura** (finita, O(1)–O(10)) em todos os 4 regimes, enquanto o
Poisson **diverge** (33→103).

**Consequência para a tese desta campanha:**

- O item 4 da §6 ("§10 Rideout–Sorkin NÃO se justifica") era baseado no gatilho "≥1
  alavanca A–C dar sinal não-circular". Mas as alavancas A–C eram todas variações do
  **sprinkling**. O CSG é uma classe de geração diferente, e a pergunta de **coordenação**
  (a barata, decidida pelo Achado 1 lido ao contrário) tem resposta diferente lá. **Esse
  fechamento de §10 era, portanto, prematuro quanto à pergunta de coordenação.**
- O **Achado 1** desta campanha (a não-localidade que faz z divergir é **Lorentz-protegida**:
  vem dos boosts do background) é exatamente o mecanismo: o CSG **não tem boosts**, então
  não tem essa não-localidade, então sua coordenação satura.
- **A frase correta, revisada:** em vez de "mean-field é estrutural a substratos causais"
  (§6.1, sem qualificação), o preciso é **"o mean-field é estrutural ao sprinkling
  Lorentziano de Poisson, não aos causal sets como classe."** Os Achados 2 e 3 e a
  falsificação **para o sprinkling** permanecem corretos e inalterados.
- A frente RS sai de **"dormente"** (§6.4) para **GATILHO ARMADO**. A campanha completa
  (ferromagneto+ξ sobre CSG) ainda **não** está autorizada: depende de um **2º gatilho**
  (clustering do grafo de cobertura), pré-registrado em
  `docs/campaigns/RIDEOUT_SORKIN_CLUSTERING/` e **não executado**.

---

## ARQUIVOS
- `campaign_full.json` / `campaign_full.png` — varredura completa (6 substratos × 4 L × 12 J).
- `validate_positive.json` — controle positivo (rede 3D, criticidade certificada).
- `focused_knn.json` — FSS decisivo do único ponto fixo (k-NN k=3, 5 L até N~5300, 8 sementes).
- `verdict_full.json` — diagnósticos por alavanca.
