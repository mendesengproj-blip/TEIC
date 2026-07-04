# SYNTHESIS — GATILHO 2 Rideout–Sorkin: clustering do grafo de cobertura do CSG

> Execução do protocolo congelado em `PRE_REGISTRO.md` (2026-06-25). Resultado-primeiro.
> Código `rs_clustering.py`, dados `rs_clustering.json`, figura `rs_clustering.png`.
> **Data de execução:** 2026-06-27.

## VEREDITO DE UMA LINHA

**GATILHO 2 = NÃO ARMADO** (com qualificação de fronteira em 1/3 regimes — ver §3b). O grafo de
cobertura (Hasse) do CSG é **tipo-árvore ao nível de laços**: a transitividade (3-ciclos) é
**identicamente zero por teorema** e a square-clustering normalizada C4 (4-ciclos) é **minúscula
e sub-mean-field** — abaixo do próprio controle de Poisson (que a ESCALA_XI já provou ser
mean-field) e ~6–30× abaixo de uma rede de dimensão finita genuína. Coordenação finita
(Gatilho 1) **não é suficiente**; a 2ª barreira (topologia tipo-árvore ⇒ mean-field) **fica de
pé**. A "Saída 2" (substrato CSG) fecha pela segunda via.

> **ACHADO ESTRUTURAL DIGNO DE NOTA PRÓPRIA (generaliza, independe da extensão §3b):** *o
> crescimento sequencial clássico produz um grafo de cobertura **mais livre de laços que o
> próprio sprinkling de Poisson mean-field**.* O CSG escapou da barreira de coordenação (⟨z⟩
> finito, Gatilho 1) mas é **ainda mais tipo-árvore** que o Poisson na barreira de laços — o
> oposto do que se esperaria de "coordenação menor ⇒ mais estrutura local".

---

## 1. O achado estrutural primário: transitividade = 0 por TEOREMA

O observável primário pré-registrado (transitividade global C = 3·triângulos/2-caminhos) é
**identicamente zero** em todos os regimes, todos os N, **e também no Poisson** (tri = 0.0,
medido). Isto não é um nulo numérico — é um **teorema**: o diagrama de Hasse (grafo de
cobertura) de qualquer poset é **livre de triângulos**. Três nós mutuamente ligados por
cobertura seriam pairwise-comparáveis ⇒ formam uma cadeia a≺b≺c ⇒ a≺c tem o intermediário b
⇒ a **não cobre** c ⇒ (a,c) não é aresta de cobertura. Contradição. A nota técnica do
pré-registro **antecipou exatamente isto** ("se for estruturalmente zero, o veredito é NÃO
ARMADO trivial... tipo-árvore por teorema da própria definição de cobertura").

⇒ A transitividade **não discrimina nada** (zero para todo causal set). O veredito recai sobre
o **observável secundário** (laços curtos), como o pré-registro previu.

## 2. O discriminador real: square-clustering C4 (4-ciclos)

Como triângulos são proibidos, o menor ciclo possível é um **4-ciclo** (diamante: dois pais de
um filho com um ancestral comum). A métrica correta é o **coeficiente de square-clustering de
Lind** C4 ∈ [0,1] (coordenação-normalizado), validado no gate (caminho→0, K_n→1, **toro 2D→0.125**).

> **Correção de métrica registrada (transparência).** Uma 1ª versão usou `frac_on_square`
> (fração de nós em ≥1 quatro-ciclo) e a média de squares-por-par **não-normalizada**. Ambas
> são **confundidas por coordenação** — o Poisson (z divergente) dá `frac_on_square`≈0.99 e
> contagem alta, apesar de ser mean-field. Substituídas pelo C4 de Lind normalizado, que é o
> análogo padrão do coeficiente de clustering para grafos livres de triângulos. Os números
> abaixo são do C4 correto.

**C4 vs N (median sobre seeds):**

| Regime | N=500 | 1000 | 2000 | 3300 | 3888 | leitura |
|---|---|---|---|---|---|---|
| sparse (p=0.02) | 0.0056 | 0.0046 | 0.0045 | 0.0043 | 0.0043 | decai p/ ~0.004 |
| intermediate (p=0.10) | 0.0200 | 0.0195 | 0.0197 | 0.0192 | 0.0190 | platô fraco ~0.019 |
| manifold (p=4/N) | 0.0029 | 0.0013 | 0.0007 | 0.0004 | 0.0003 | decai→0 (claro) |
| **Poisson (controle MF)** | 0.0545 | 0.0401 | 0.0291 | — | — | decai→0 (Bethe) |
| 2D torus (ref. dim-finita) | — | — | — | — | **0.125** | rede genuína |

## 3. Por que NÃO ARMADO (o argumento decisivo é o controle)

O critério congelado diz "ARMADO se o clustering satura num valor positivo em ≥1 regime". Lido
**isoladamente**, o `intermediate` tem um platô fraco ~0.019 que *parece* saturar positivo. Mas
o **controle de Poisson resolve a ambiguidade**, e é o que o pré-registro exige olhar:

1. **O Poisson — provado mean-field na ESCALA_XI — tem C4 MAIOR (0.029–0.054) que TODOS os
   regimes do CSG** (≤0.019). Um substrato com *menos* estrutura de laços que o mean-field não
   pode escapar do mean-field. O `intermediate` (0.019) está **abaixo** do Poisson mean-field.
2. **O Poisson decai** (0.054→0.029, ~half por oitava de N) rumo a 0 — assinatura Bethe/tipo-
   árvore no limite. Os regimes do CSG ou decaem (sparse, manifold) ou platôm num valor **abaixo**
   do Poisson contemporâneo.
3. **Uma rede de dimensão finita genuína (toro 2D) tem C4 = 0.125** — ~6× o `intermediate` e
   ~30× o `sparse`. Nenhum regime do CSG chega perto de estrutura de laços dimensional-finita.

⇒ O grafo de cobertura do CSG é **mais tipo-árvore que o próprio Poisson mean-field**. **NÃO
ARMADO**, robusto.

## 3b. Fronteira do regime `intermediate` — extensão a N=16000 (Parte 1, 2026-06-27)

O platô fraco do `intermediate` (C4≈0.019 no ladder original até N=3888) foi medido num range
de N curto demais para distinguir "platô genuíno em C4>0" de "decaimento lento ainda não
convergido". **Estendi o ladder APENAS no intermediate** (mesmo gerador/estimador) a
N=6000/8000/12000/16000 (3 seeds), e calculei o expoente local d(C4)/d(ln N) — o critério
diagnóstico foi **pré-registrado antes de ver o resultado** (`extend_intermediate.py`):

| N | 3888 | 6000 | 8000 | 12000 | 16000 |
|---|---|---|---|---|---|
| C4 | 0.0190 | 0.0188 | 0.0193 | 0.0191 | 0.0191 |

Expoente local d(C4)/d(ln N) no segmento alto: [−0.0005, +0.0018, −0.0006, +0.0003], **média
+0.0002**, |rel| = 1.3%; os dois pontos mais altos consistentes dentro de 2·SEM. ⇒ **PLATÔ
GENUÍNO** (C4 estabiliza em ~0.019 > 0, expoente local → 0), **não** decaimento lento.

**Consequência (qualificação pré-registrada, sem annealing):** o veredito do Gatilho 2 muda de
"morte limpa em 3/3 regimes" para **"morte em 2/3 (sparse, manifold — C4 decai/→0); FRONTEIRA
(não morte limpa) em 1/3 (intermediate — C4 platô positivo ~0.019)"** — tratamento análogo ao
da Alavanca k-NN na ESCALA_XI.

**Mas o veredito GERAL "CSG ENCERRADA" PERMANECE**, por uma razão quantitativa que não depende
da extensão: o platô do intermediate (0.019) é **ainda abaixo do piso mean-field do Poisson**
(C4≈0.029–0.054, ele próprio decaindo) e ~6× abaixo da rede dim-finita (toro 0.125). O
intermediate tem uma densidade de laços pequena e **sub-mean-field** — uma fronteira, não uma
estrutura de laços dimensional-finita capaz de sustentar ξ divergente. A hierarquia geral de
clustering (CSG < Poisson-MF < rede-dim-finita) se sustenta. ⇒ a campanha completa de ξ **continua
não justificada**; "CSG ENCERRADA" deve ser citado **com a ressalva do intermediate-fronteira**.

## 4. Significado (a 2ª barreira de pé)

O Gatilho 1 removeu a perna de *coordenação divergente* do argumento de Bethe (CSG tem ⟨z⟩
finito). Mas **coordenação finita é necessária, não suficiente** (Caveat 2): uma rede de Bethe
tem coordenação finita e é mean-field exata. O Gatilho 2 testou a 2ª perna — **estrutura de
laços de dimensão finita** — e ela **falha**: o grafo de cobertura é tipo-árvore (C4 sub-mean-
field). Logo o CSG é mean-field **por uma segunda via independente da coordenação** (topologia
tipo-árvore), exatamente o desfecho NÃO ARMADO pré-registrado como "igualmente válido e
publicável: reforça que o mean-field em causal sets é robusto".

**Consequência operacional (congelada):** a campanha completa (ferromagneto de orientação O(3)
sobre o CSG + ξ_2nd/L) **NÃO deve rodar** — o CSG não passa a 2ª pré-condição. A linha CSG como
substrato para um ξ divergente está **encerrada**.

## 5. Caveats herdados (respeitados)

- **Regime `dense` EXCLUÍDO** (Caveat 1: p=0.40 ≈ cadeia 1D trivial). Não medido, não citado.
- **Confound satura-vs-decai-devagar:** endereçado pelo ladder até 3888 e pelo controle de
  Poisson (que exibe o decaimento claramente) + a referência de toro 2D (valor dim-finito real).
- **Sem annealing:** os dois vereditos eram pré-definidos; o intermediate-platô foi avaliado
  contra o controle MF como o pré-registro manda, não reinterpretado a favor.

## 6. Próximo passo (branching §2.4 da fila de substratos) — EXECUTADO

Parte 1 = **NÃO ARMADO** ⇒ a linha **tipo-CDT** (aresta fixa + colagem livre tipo-Pachner) virou
**prioridade imediata** e foi **EXECUTADA (Gatilho 3, 2026-06-27, `docs/campaigns/CDT_VIABILIDADE/`)
= ARMADO** (com ressalvas): o 1-esqueleto da triangulação 2D tem C4≈0.145 saturante (~5× o piso
mean-field, ordem da rede dim-finita) — a estrutura de laços que falta ao CSG. Ressalva central:
em 2D ⟨z⟩→6 é **identidade de Euler** (não escape dinâmico), e a colagem de Pachner sem peso de
ação pode gerar patologia branched-polymer na geometria global → ARMADO cinemático é necessário,
não suficiente. Ver o SYNTHESIS do Gatilho 3.
