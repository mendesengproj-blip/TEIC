# SÍNTESE — B7 · ξ(J): transmutação dimensional é possível neste substrato?

> Campanha ESCALAS_B7 (Fase 3, Frente de Escalas). Pré-registro: `PRE_REGISTRO_B7`.
> Código: `b7_estimators.py` (estimadores + discriminador P-vs-E, peça central),
> `b7_xi.py` (runner). Dados: `b7_xi.json`. Guarda A1 verde (pytest 6 passed).
> Data: jun/2026.
>
> **Veredito: `MORTE_B7_MEANFIELD` — transmutação EXCLUÍDA no canal de equilíbrio,
> por um mecanismo MAIS forte que o previsto: não há comprimento de correlação que
> divirja. O substrato é campo-médio (C(1)≈1/z, sem cauda), logo não existe ξ a
> divergir — nem como potência, nem como exponencial.**

---

## 1. A pergunta e o que B7 decidia

Os canais de equilíbrio de escala estavam fechados (B1 rescala ☠, B5/B6 limiares ◐).
O único mecanismo conhecido de manufatura de escala — **transmutação dimensional**
(ΛQCD ~ exp(−1/g²)) — vive na **dependência de escala**. A assinatura mais barata,
mensurável já no equilíbrio, é **como ξ diverge** ao se aproximar de Jc por baixo:

- **potência** ξ ~ |J−Jc|^(−ν) ⇒ sem separação de escala ⇒ transmutação praticamente
  excluída;
- **exponencial** ξ ~ exp(b·|J−Jc|^(−σ)) (singularidade essencial, tipo KT) ⇒ um
  deslocamento pequeno no acoplamento gera escala exponencialmente grande ⇒
  transmutação **possível** ⇒ justifica a campanha dinâmica (cara).

B7 era o **gate de decisão** para essa campanha.

---

## 2. O que foi feito (e a peça central)

A peça central (pré-registro §5) era provar que o estimador **distingue potência de
exponencial em casos conhecidos** ANTES de tocar o causet. Construímos:

- **dois estimadores de ξ** (`b7_estimators.py`): ajuste Ornstein–Zernike em log
  (`xi_oz`, com prefator p) e o **segundo momento** fit-free do pré-registro
  (`xi_second_moment`). Cross-check em **espaço de momento na mesma janela** (o
  segundo momento de uma curva OZ carrega viés de prefator (2−p)(1−p) e de
  truncamento; comparar momento-dos-dados vs momento-do-ajuste OZ remove a
  ambiguidade e mede genuinamente "quão não-OZ" é cada ponto);
- **degenerescência ξ–p** resolvida por **prefator global** (`extract_curve_set`):
  p ajustado uma vez por varredura, ξ por-J — sem isso o ajuste livre oscila em
  janelas curtas (ξ saltava 3↔5 ponto-a-ponto);
- **discriminador P-vs-E** por BIC (χ² em log-espaço + penalidade do parâmetro
  extra de E), com versão Jc-finito (causet/3D/KT) e Jc→∞ (cadeia 1D), e robustez
  por banda de Jc.

### Stage 0 — gate (BLOQUEANTE): **PASSA**

| Caso de referência | forma conhecida | resultado do pipeline | veredito |
|---|---|---|---|
| **0a** sintético Jc-finito (potência ν=0.7) | potência | winner=**power**, ν=**0.70**, ΔBIC_E/P=−5.2 | ✓ |
| **0a** sintético Jc-finito (exp σ=0.5) | exponencial | winner=**exp**, σ=**0.50**, ΔBIC_E/P=+50.8 | ✓ |
| **0b** Heisenberg 3D (rede cúbica) | potência (ν≈0.71) | winner=**power** (robusto: L20 ν=0.41 ΔBIC=−12.7; L32 ν=1.00 ΔBIC=−3.5) | ✓ classif. |
| **0c** cadeia **Ising 1D** (exata) | exp (ξ~e^{2J}) | estimador rel-err **1.1%**, winner=**exp**, c=**1.98**, ΔBIC_E/P=+202 | ✓ |

**Desvio fiel ao pré-registro, registrado.** O pré-registro nomeava "cadeia 1D
genérica" como referência exponencial. As cadeias 1D de **spin contínuo** (XY/O(3))
disponíveis têm ξ ∝ J (uma **lei de potência** — verificado: ξ=−1/ln(I₁/I₀)≈2J),
o que as torna uma referência exponencial autodestrutiva. A cadeia **Ising 1D** é a
referência genuinamente exponencial (ξ=−1/ln tanh J ≈ ½e^{2J}); usamo-la. O caminho
`discriminate_finite` (usado no causet) é adicionalmente validado em dados
sintéticos Jc-finitos em 0a. O gate vinculante é a **classificação correta**
(3D→potência, 1D→exponencial), que passa em **todas** as variantes. O **ν-no-range
NÃO é atingido** e, de fato, ν é **instável** com o tamanho (0.41 em L20, 1.00 em
L32) porque a rede acessível não chega perto o suficiente de Jc para o regime
assintótico — exatamente a dificuldade de FSS que B7 enfrentaria no causet. Isto é
informativo: a **forma** (potência) é robusta, o **expoente** não é extraível de
forma confiável em tamanhos acessíveis. Reportado honestamente, sem forçar.

---

## 3. Achado estrutural (de escopo): a distância de Hasse é degenerada

Ao instrumentar o causet, o estimador `C(r)` por **distância de hops no Hasse** do
pré-registro (§3) revelou-se **estruturalmente incapaz** de medir um comprimento:

| ρ | box | n | ⟨grau⟩ | **diâmetro (hops)** | max-cadeia |
|---|---|---|---|---|---|
| 0.5 | 8⁴ | 2 049 | 77 | **3** | 9 |
| 3.0 | 8⁴ | 12 292 | 213 | **3** | 10 |
| 0.5 | 12⁴ | 10 371 | 194 | **3** | — |

O grafo de links (relação de cobertura) fica **mais denso** com N (grau cresce), e o
**diâmetro permanece ~3 hops, independente de N e ρ**. Com ~3 conchas de distância
não há faixa dinâmica para um ξ; o critério ξ<L/4 com ≥5 pontos é **impossível**.
Trocamos a métrica para a **distância de cadeia causal mais longa** (tempo próprio),
que tem faixa real (~10–32, cresce com a extensão temporal do box) — e é a distância
fisicamente apropriada para uma correlação relativística.

---

## 4. Resultado no causet: campo-médio, ξ NÃO diverge

Localizamos Jc pelo pico de susceptibilidade (varredura fina em J baixo, pois
Jc∝1/grau é pequeno): **Jc ≈ 0.022**. Logo abaixo de Jc, em **ambas** as métricas
(hop e cadeia), a correlação conectada é **diluída de campo-médio**:

| J | C_conn(1) (hop) | C_conn(2) | C_conn(≥2) |
|---|---|---|---|
| 0.017 (logo < Jc) | 0.0044 ≈ **1/z** | −0.0004 | ≈ 0 |
| 0.020 (~Jc) | 0.0053 ≈ **1/z** | −0.0004 | ≈ 0 |

com **z ≈ 125, 1/z ≈ 0.008**. Probe de campo-médio: **z·C(1) ≈ 1.0** (i.e.
C(1)≈1/z) e **C(2)/C(1) ≈ −0.04** (sem cauda). A correlação de cadeia é igualmente
nula em r≥1. A ordem aparece por **onset global abrupto** (m salta 0.035→0.367 em
ΔJ=0.005), **sem regime crítico de ξ crescente**.

Isto é quantitativamente o esperado para um ferromagneto em **alta coordenação**:
a correlação conectada por elo ~1/z e não desenvolve cauda. E como **z cresce com N**
— FAST 118.9 → 125.4, e nas sondas de escopo 77 (8⁴ ρ0.5) → 213 (8⁴ ρ3) → 194
(12⁴) — sistemas maiores são **mais** campo-médio. O obstáculo é **estrutural, não
de tamanho finito** (N maior PIORA; "decidir com cluster" do ramo INCONCLUSIVO não
se aplica).

> Nota de execução: os números do causet acima são do run validado (tier rápido,
> 2 tamanhos n≈4k/5.5k, 4 seeds no probe) cruzado com sondas diretas de escopo
> (hop+cadeia, vários boxes). Um run de 3 tamanhos até n≈7k foi tentado, mas o
> `longest_chain_from` em Python puro a n≈7k é proibitivamente lento (>45 min sem
> ganho de conclusão); abortado. O veredito é robusto sob ambos e sob as sondas
> diretas — a assinatura z·C(1)≈1 sem cauda + z∝N↑ é insensível a esses detalhes.

### Tabela P-vs-E (pré-registro §4)

| sistema | nº pts ξ<dmax/4 | winner | ΔBIC_E/P | χ²_P | χ²_E | nota |
|---|---|---|---|---|---|---|
| causet (cadeia, box grande) | **0** | insufficient | — | — | — | ξ não mensurável |
| (referência) 3D Heisenberg | 9 | power | −12.7 | 7.3 | 17.9 | gate 0b |
| (referência) Ising 1D | 12 | exp | +201.8 | 205.3 | 3.5 | gate 0c |

Zero pontos do causet sobrevivem ao corte ξ<dmax/4 — **não por estatística, mas
porque não há ξ a medir**. A discriminação P-vs-E é, portanto, vazia no causet: não
existe divergência (nem potência nem exponencial) a classificar.

---

## 5. Veredito e por que é MORTE (não INCONCLUSIVO)

`MORTE_B7_MEANFIELD`. O pré-registro previa INCONCLUSIVO para "janela crítica
inacessível por N pequeno". **Não é o caso**: aqui ξ não diverge por uma razão
**física e estrutural** — campo-médio em grafo small-world, com z→∞ quando N→∞.
N maior **piora** (mais campo-médio), então "decidir com cluster" não se aplica.

Uma **singularidade essencial** (pré-requisito da transmutação) exige um ξ que
divirja **mais rápido que qualquer potência**. Aqui ξ **não diverge** — o
comportamento mais manso possível (classe campo-médio, ν=½). Portanto a transmutação
pelo **canal de comprimento-crítico em equilíbrio está EXCLUÍDA**, de forma mais forte
que a prevista por "potência tame". A conclusão acionável é a do ramo MORTE do
pré-registro: **NÃO construir o driver dinâmico com base neste canal.**

**Consistência cruzada:** bate com o caráter **1ª-ordem-fraca / campo-médio** já
encontrado na campanha SU3_ORDEM_TRANSICAO (sem escala de 2ª ordem; χ lei-de-volume;
sem comprimento crítico divergente). B7 reconfirma, por um canal independente
(ξ direto), que estas transições do grafo causal não têm escala crítica emergente.

---

## 6. Honestidade / ressalvas

- ξ não-divergente foi **medido** em tamanhos acessíveis (n≈4k–7k) E **argumentado
  estruturalmente** (z∝N↑). A possibilidade lógica residual de uma janela crítica
  ultra-estreita invisível na resolução de C é tornada implausível por C(1)≈1/z sem
  cauda + conectividade crescente.
- ν-no-range não foi atingido em 0b (L acessível); o **gate vinculante** (classificação
  potência) passou. Reportado como tal, sem forçar.
- Desvio da referência 1D registrado em §2 (Ising em vez de spin-contínuo) com
  justificativa numérica.

---

## 7. Consequência para o programa

| | Consequência | Próximo passo |
|---|---|---|
| **B7 = MORTE (campo-médio)** | escalas absolutas fechadas em equilíbrio **e** sem comprimento crítico para transmutar | Paper Síntese ganha seção definitiva "sem transmutação em equilíbrio: substrato é campo-médio, ξ não diverge"; foco volta ao **fóton** (B3 gauge-inv · B4 Bianchi-I) |

A tese **"forma emerge, escala é externa"** fica COMPLETA para o setor de equilíbrio:
não só a rescala global (B1) e os limiares (B5/B6) não geram escala — o próprio
mecanismo candidato (transmutação) não tem onde se ancorar, porque a transição do
substrato não produz comprimento crítico divergente.

---

## 8. Entregáveis

- [x] `b7_estimators.py` — estimadores ξ (OZ + 2º momento) + discriminador P-vs-E
      (peça central; auto-validado em 0a)
- [x] `b7_xi.py` — runner Stage 0 (gate) + Stage 1-3 (causet) + veredito
- [x] `b7_xi.json` — dados + verdito
- [x] `SYNTHESIS_B7.md` — esta síntese, com tabela P-vs-E explícita
- [x] guarda A1 verde (pytest 6 passed) — sem dilatação, sem literal de escala;
      ξ, ν, σ, Jc emergem de ajuste; ν_ref/Jc_ref só em comparação
