# PRÉ-REGISTRO — CAMPANHA SU3_ORDEM_L32

> Congelado **antes** de qualquer simulação. Charter: FASE 2 / PRIORIDADE 1 do prompt
> MASTER_UPDATE. Predecessor direto: SU3_ORDEM_TRANSICAO (L≤24), cujo veredito foi
> **"1ª ordem fraca é a leitura mais provável; H0 (2ª ordem) desfavorecida; calor
> latente não-resolvido até L=24"**. Esta campanha ataca o **resíduo declarado** por
> aquela síntese: distinguir **1ª ordem forte vs fraca**, e **1ª ordem fraca vs
> contínua com forte correção pré-assintótica**, medindo a **barreira de energia
> livre (∝ tensão interfacial σ) diretamente em L≳32**.

**Data de congelamento:** 2026-06-22
**Branch:** `su3-ordem-transicao`
**Status:** CHARTER PRÉ-REGISTRADO — nenhum código de produção rodado ainda.

---

## 0. O QUE O PREDECESSOR DEIXOU EM ABERTO (ponto de partida, não re-litigado)

Da `SU3_ORDEM_TRANSICAO/SYNTHESIS.md` (resultado, não reaberto aqui):

- **H0 (2ª ordem limpa, como SU(2)) está DESFAVORECIDA** — χ_max cresce mais rápido que
  qualquer γ/ν de 2ª ordem (x_eff≈3.2–3.9), o dip de Binder aprofunda sem saturar.
- **A leitura provável é 1ª ordem FRACA**, mas o teste termodinâmico decisivo — a
  **bimodalidade do histograma de energia em J_c** (calor latente / coexistência) —
  está **ausente e plano até L=24** (dip=0.00). Isso **limita** a 1ª ordem a fraca e
  **não exclui** contínua-com-forte-finite-size.
- O **caminho limpo registrado** por aquela campanha: amostragem que cruza a barreira
  em **L≳32** para medir a barreira de energia livre ΔF (∝ σ): **σ>0 finito ⇒ 1ª ordem;
  σ→0 ⇒ contínua**; a magnitude do calor latente separa forte de fraca.

Dois confounds que esta campanha deve eliminar (não repetir):
1. **Sub-equilíbrio:** 500 sweeps de burn (OT) é curto perto de uma transição lenta;
   inflou o expoente local de χ. → ESTA campanha usa termalização muito mais longa +
   parallel tempering para garantir cruzamento da barreira.
2. **Histerese por sweep rápido** (OT3): lag de não-equilíbrio cresce com L e imita 1ª
   ordem num contínuo. → ESTA campanha **NÃO usa histerese** como indicador; usa a
   barreira P(E) equilibrada via reweighting.

---

## 1. HIPÓTESES

- **H_forte:** transição de **1ª ordem FORTE** — P(E) em J_c desenvolve **dois picos
  separados**, com barreira ΔF crescendo com L (escala interfacial ∝ L^{d-1}=L²) e
  **calor latente resolvível** (gap ΔE/|E| acima do limiar congelado).
- **H_fraca:** **1ª ordem FRACA** — dois picos emergem em L=32/40 mas o gap ΔE é
  pequeno (acima do ruído, abaixo do limiar de "forte"); σ>0 mas pequena.
- **H_contínua:** **contínua / 2ª ordem com forte finite-size** — P(E) permanece
  **unimodal** em L=32 (e 40), o expoente de χ_max **cai** em direção a γ/ν<2, e o dip
  de Binder **satura** num valor universal. σ→0.

---

## 2. MÉTODO — PARALLEL TEMPERING (alternativa registrada ao multicanônico)

O prompt autoriza **parallel tempering (PT)** como alternativa mais simples ao
multicanônico. Justificativa registrada:

- PT roda **R réplicas** do mesmo sistema, cada uma a um J diferente numa escada que
  **bracketa J_c**, com trocas de configuração entre réplicas vizinhas. Cada
  configuração faz um **random walk em J**, atravessa a região de transição, e assim
  **equilibra através da barreira** que o Metropolis canônico (OT) não cruzava. Isto
  ataca diretamente o confound de sub-equilíbrio.
- O peso do modelo é `w ∝ exp(J·U)` com `U ≡ Σ_<ij> (1/3)Re Tr(U_iU_j†)` (a soma de
  overlap, adimensional; `energy_per_link = -J·U/N_links`). A **aceitação de troca**
  entre réplicas a,b (em J_a,J_b, com overlaps U_a,U_b) é:
  > `p_swap = min(1, exp[ (J_a − J_b)·(U_b − U_a) ])`
  (derivada de β↔J, E↔−U na fórmula padrão de replica-exchange). **Congelada agora.**

**Limitação honesta registrada (define o critério de morte):** PT melhora a
*ergodicidade* através da barreira, mas **não achata a barreira** como o multicanônico/
Wang-Landau. Se a barreira em L=32 for alta demais para o PT cruzar com taxa de troca
útil (réplicas "congelam" em ramos separados), o método **falha em equilibrar** e o
resultado é morte técnica (→ §6), não um veredito de ordem. O diagnóstico de saúde do
PT (round-trips em J) é monitorado e congelado abaixo.

**Extração da barreira:** combinando os histogramas de E de todas as réplicas via
**reweighting multi-histograma (WHAM / Ferrenberg–Swendsen)**, reconstrói-se P(E) no
J_c reponderado. Barreira `ΔF = ln(P_max/P_min)` entre os dois picos; calor latente
`ΔE = (E_alto − E_baixo)/|E|` (gap entre picos). **Estas são as observáveis decisivas.**

---

## 3. PARÂMETROS CONGELADOS (não ajustar após ver resultados)

| Parâmetro | Valor frozen |
|---|---|
| Engine | `su3_core.SU3ChiralModel` em `lattice_periodic((L,L,L))`, importado **SEM modificação** |
| Driver | **novo** `OT_L32_parallel_tempering.py` (puramente real; complexo SU(3) só dentro de `su3_core`) |
| L primário | **32** |
| L condicional | **40** — só roda se L=32 der veredito na zona inconclusiva (§6), ou se L=32 resolver 1ª-ordem e L=40 for necessário para confirmar crescimento de ΔF(L) |
| Escada J (PT) | **R=24 réplicas, lineares em [2.66, 2.82]** (ΔJ≈0.007), bracketando J_c(L=24)=2.74 com folga de ±0.08 (a deriva do pseudo-crítico sobe com L). A escada final pode ser **re-espaçada UMA vez** num smoke-test NÃO-registrado para atingir taxa de troca alvo, e então **congelada antes do run registrado** (re-espaçamento muda só a densidade de réplicas, não bracketa diferente). |
| Taxa de troca alvo | **20–40%** entre réplicas vizinhas (saúde do PT) |
| Tentativa de troca | a cada **10 sweeps** |
| Termalização | **20 000 sweeps** por réplica (≫ os 500 de OT; passo adaptativo target acc 0.4 desligado após burn, step congelado no valor pós-burn) |
| Medição | **100 000 sweeps**, `meas_every=10` → 10 000 amostras de (m, U) por réplica |
| Sementes | **4 runs PT independentes**: seed ∈ {7, 1007, 2007, 3007} |
| Histograma E p/ P(E) | reweighting WHAM de TODAS as réplicas; bins de E escolhidos por regra de Freedman–Diaconis, congelados após o burn |

> Custo: L=32 (N=32 768 sítios) × 24 réplicas × 120k sweeps × 4 sementes é pesado.
> Se inviável em desktop, **reduzir nesta ordem fixa** (registrado para não ser ad-hoc):
> (1) sementes 4→2; (2) medição 100k→60k; (3) réplicas 24→16. **NÃO** reduzir burn
> (o burn é o que elimina o confound de sub-equilíbrio). Se nem (1)+(2)+(3) couberem
> ⇒ morte técnica por CPU (§6), declarar L≳32 inacessível neste hardware.

---

## 4. OBSERVÁVEIS (definições congeladas)

- `m = model.order_parameter()` (= |⟨v_i⟩|, ≥0); `U4 = 1 − ⟨m⁴⟩/(3⟨m²⟩²)`.
- `χ = N·(⟨m²⟩ − ⟨m⟩²)`; `χ_max(L)` = máximo sobre a escada J (reponderado).
- `e = energy_per_link()`; histograma reponderado **P(E)** em J_c.
- **ΔF(L) = ln(P_max/P_min)** (barreira); **ΔE(L)** = gap normalizado entre picos.
- **Saúde do PT:** nº de round-trips de cada réplica entre as pontas da escada (J_lo↔J_hi)
  durante a medição.

---

## 5. KILL-CRITERIA NUMÉRICOS (pré-registrados)

### L32-1 — Barreira / bimodalidade de P(E) em J_c  *(indicador decisivo)*
- **1ª ORDEM (forte ou fraca):** P(E) em L=32 é **duplo-pico** com vale resolvível
  (`ΔF ≥ 3×` o ruído MC de ln P, estimado por bootstrap das 4 sementes), **e** ΔF(L=40)
  > ΔF(L=32) se L=40 rodar (barreira crescendo). → **σ>0 finito.**
- **CONTÍNUA / 2ª ordem:** P(E) **unimodal** em L=32 (e L=40 se rodar), `ΔF` compatível
  com 0 dentro do ruído. → **σ→0.**

### L32-2 — Calor latente (separa FORTE de FRACA)  *(só se L32-1 = 1ª ordem)*
- **FORTE:** `ΔE/|E| > 0.10` (gap grande entre picos).
- **FRACA:** `0 < ΔE/|E| ≤ 0.10` (picos resolvíveis mas próximos).
- (limiar 0.10 congelado agora, antes de qualquer dado de L=32.)

### L32-3 — Expoente de χ_max  *(corrobora, não decide sozinho)*
Ajuste `χ_max ∝ L^x` incluindo os pontos de OT (L=8,12,16,20,24) + L=32 (+40).
- **1ª ordem:** `x → 3` (lei de volume; o expoente local deve **cair** de 3.6 em
  direção a 3 com o novo ponto — em OT já caíra 3.91→3.22 em L20→24).
- **2ª ordem:** `x → γ/ν < 2`.
- **Inconclusivo isolado:** `x ∈ (2, 3.5)` — não decide; L32-1 prevalece.

### L32-4 — Dip de Binder
- **1ª ordem:** dip de U4 **continua aprofundando** (sem saturar) com L=32.
- **2ª ordem:** dip **satura** num valor universal estável.

> **Hierarquia de decisão congelada:** L32-1 (barreira) é o árbitro. L32-2 só roda se
> L32-1 = 1ª ordem. L32-3/L32-4 corroboram. Em conflito, **L32-1 prevalece** (é o teste
> termodinâmico direto; expoente e dip são pré-assintóticos por construção).

---

## 6. CRITÉRIO DE MORTE / FRONTEIRA TÉCNICA (congelado)

**MORTE TÉCNICA — declarar fronteira, indicar L≳48 + multicanônico em cluster — se
QUALQUER uma:**
1. **PT não equilibra:** taxa de troca < 10% em alguma vizinhança da escada **OU**
   < 1 round-trip médio por réplica na medição (réplicas congelam em ramos separados;
   a barreira é alta demais para PT cruzar). → o método não consegue amostrar a
   barreira; multicanônico/Wang-Landau é necessário.
2. **L=32 não resolve:** P(E) tem barreira **abaixo de 3× o ruído** (não-decidível
   duplo-vs-único pico) **E** o expoente de χ_max permanece em `(2, 3.5)` **E** o dip de
   U4 ainda deriva. Mesmo após rodar L=40, se ambos ficam não-decidíveis. → declarar
   que **L≳48 com amostragem multicanônica/Wang-Landau (medição direta de ΔF) em
   cluster** é o requisito; registrar como fronteira técnica, não como veredito.
3. **CPU esgotada** antes de L=32 completar mesmo com as reduções da §3 → fronteira de
   hardware.

> "Morte" aqui é resultado válido: significa que a distinção forte-vs-fraca-vs-contínua
> está **abaixo da resolução acessível**, e o paper SU3 mantém a linguagem atual
> ("1ª ordem fraca provável, 2ª ordem limpa excluída, resolução definitiva exige L≳48
> multicanônico") — apenas com o limite empurrado de L=24 para L=32/40.

---

## 7. CRITÉRIO DE SUCESSO (congelado)

**SUCESSO = resolução limpa** entre os três cenários, operacionalizada por L32-1
(+L32-2): P(E) decide duplo-vs-único pico acima do ruído em L=32 (confirmado por
crescimento de ΔF em L=40 se 1ª ordem), e — se 1ª ordem — L32-2 separa forte de fraca.
Especificamente o sucesso do prompt ("resolução clara entre 1ª ordem forte vs fraca")
ocorre quando L32-1 = 1ª ordem **e** L32-2 cai limpo de um lado do limiar 0.10.

---

## 8. VERIFICAÇÕES DE CONSISTÊNCIA

- **V1 (vs OT):** o J_c reponderado de L=32 deve continuar a tendência de deriva de OT
  (2.65→2.74 em L=8→24), i.e. cair em **[2.74, 2.80]**. Fora disso: PARAR e investigar
  a escada antes de interpretar a ordem.
- **V2 (gate em substrato conhecido — OBRIGATÓRIO antes de medir):** rodar o driver PT
  em **L=16** e reproduzir os números de OT (χ_max≈29, U4_pico≈0.565, J_c≈2.71) dentro
  de ±10%. Só medir em L=32 **depois** que o gate L=16 passar. (Padrão do programa:
  validar o motor novo em tamanho já caracterizado antes do tamanho novo.)
- **V3 (saúde do PT):** histograma de round-trips por réplica reportado; se alguma
  réplica nunca cruza a escada, a escada é inadequada (→ §6.1).

---

## 9. PROTOCOLO ANTI-CIRCULARIDADE

- Nenhum número de QCD entra. J_c, ΔF, ΔE, expoentes saem **só** dos dados; "1ª ordem
  para N≥3" é só enquadramento de literatura (COMPARISON ONLY).
- O pico/cruzamento é localizado **sem** usar 2.65/2.74; comparação só em V1.
- Sementes e escada congeladas acima antes de rodar; escada só re-espaçada num smoke
  NÃO-registrado e então congelada.
- Guard `tests/test_no_circularity.py` deve passar: o driver PT é puramente real; todo
  o complexo SU(3) fica dentro de `su3_core` (blocos SU(3) GROUP-DEF). **Guard verde
  antes de qualquer afirmação sobre o resultado.**

---

## 10. DESFECHOS (registrar resultado primeiro, narrativa depois)

- **A — 1ª ORDEM FORTE confirmada** (L32-1 duplo-pico + L32-2 ΔE>0.10): adendo ao
  PAPER_SU3 — "1ª ordem forte, calor latente resolvido em L=32"; reverte a ressalva.
- **B — 1ª ORDEM FRACA confirmada** (L32-1 duplo-pico + L32-2 ΔE≤0.10): PAPER_SU3
  atualiza de "fraca provável (L≤24)" para "1ª ordem fraca **confirmada** em L=32,
  σ>0 finito pequeno".
- **C — CONTÍNUA / 2ª ordem com finite-size** (L32-1 unimodal, x→γ/ν, dip satura):
  **reverte** o veredito de OT — a 1ª ordem fraca era artefato pré-assintótico;
  PAPER_SU3 corrigido para "contínua com forte correção de tamanho finito" (correção
  honesta, declarada como tal).
- **D — MORTE TÉCNICA / FRONTEIRA** (§6): PAPER_SU3 mantém a linguagem atual com o
  limite empurrado para L=32/40; requisito L≳48 multicanônico em cluster registrado.

Em todos: kill-criterion não reaberto após ver resultado; resultado vai para
`RESEARCH_MAP.md` **antes** de qualquer edição de paper; dados em
`docs/campaigns/SU3_ORDEM_L32/`; commit na branch `su3-ordem-transicao`. **Reportar ao
autor ao final, antes de avançar para a PRIORIDADE 2.**
