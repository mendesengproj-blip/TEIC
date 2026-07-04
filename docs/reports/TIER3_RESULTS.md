# TIER3_RESULTS — As Três Apostas Exploratórias (executado jun/2026)

Campanha pré-registrada em `TIER3_EXPLORATIONS.md` (critérios de morte fixados
antes de qualquer célula rodar; nenhum critério foi alterado após ver dados).
Código e dados em `results/tier3/`.

## Veredito geral: 1/3 — resultado interessante, reportar como exploração

| Aposta | Pergunta | Veredito | Resultado |
|---|---|---|---|
| T3A | d_MM converge sob crescimento e7? | **MORTE** | Converge para d\* = 1.43 ± 0.27 ≠ 4; causet não-manifold |
| T3B | d=3+1 é atrator dinâmico? | **MORTE** | Seeds mantêm a dimensão de entrada; nenhum fluxo para 4 |
| T3C | k ∝ N (ℏ como granularidade)? | **SUCESSO** | α = 1.008, R² = 0.99997; franjas ∝ 1/N; com caveats fortes |

## Infraestrutura nova (validada antes da física)

O protocolo e7 (regra TEIC de crescimento, membro da família Rideout–Sorkin
geral parametrizado por n_components) foi escalado de N=7 para N=2000 com um
sampler MCMC lazy-Metropolis sobre o reticulado de ideais de ordem
(`results/tier3/tier3_core.py`). Gate de engenharia `T3V` (pré-registrado):

- **V0** bookkeeping incremental de componentes: 20 000 propostas auditadas,
  0 divergências.
- **V1** distribuição estacionária sobre ideais de causets fixos: TV ≤ 0.015
  (limite 0.05).
- **V2** distribuição end-to-end de causets em N=6 vs DP exato sobre formas
  canônicas: TV_mcmc = 0.098 ≈ piso de ruído do sampler exato de e7 (0.098).
  O gate pegou um bug real (cadeia periódica em reticulados pequenos),
  corrigido com laziness ½ ANTES de qualquer corrida física.
- **V3** estimador Myrheim–Meyer recupera o input em sprinkling estático
  (d=2 → 1.97, d=4 → 4.06).

## T3A — Poisson dinâmico (MORTE)

Crescimento e7 (w_meet = 1/3) até N=2000, 5 runs. O estimador primário
(mediana de d_MM sobre os maiores intervalos de Alexandrov) converge para
**d\* = 1.43 ± 0.27** — próximo de cadeia, não de 3+1D. Os estimadores
interval e global divergem em N grande (1.43 vs 2.43), o que num sprinkling
de variedade não acontece (controles T3A-2: 2→1.98, 3→2.98, 4→3.97, 5→5.16):
o causet crescido **não é manifold-like**. A dimensão é insensível ao
acoplamento (w_meet ∈ [0.2, 3]: d ∈ [1.25, 1.48]). Caveat de engenharia:
dobrar o mixing desloca d em +0.18 — não muda o veredito.

## T3B — Atrator dimensional (MORTE)

Seeds de 300 eventos sprinkladas em d=2, d=4 (controle) e d=5; crescimento
combinatório até N=1500 (3 runs cada). Nenhuma seed flui para 4:
d=2 → 2.03, d=4 → 4.88, d=5 → 5.69 (a deriva de d=5 é para CIMA). A região
crescida não produz intervalos grandes nas seeds d ≥ 4 (não-manifold, como
T3A); na seed d=2 ela lê d ≈ 2.5–3.4, instável entre runs — curiosidade, não
resultado. Crescimento puro (T3B-3) → 1.50, consistente com T3A.
**d=3+1 não é atrator dinâmico desta regra de crescimento.**

## T3C — ℏ como granularidade causal (SUCESSO, com caveats explícitos)

k(N) = θ₀·τ(N)/X medido com o protocolo CC2 (ρ=60, 20 sementes):
**k ∝ N^1.008, R² = 0.99997** — o critério pré-registrado de SUCESSO
(|α−1| ≤ 0.10, R² ≥ 0.99) é atingido. A leitura interferométrica (maquinaria
e11, bloco COMPARISON ONLY) confirma: espaçamento de franjas ∝ 1/N, picos
contados batem com o analítico (227 picos em N=100).

**Caveats de honestidade (verificação tripla, protocolo item 4):**

1. Para o tipo "diamond" isto é CC2 (τ ∝ N) relido pela fase de e10/e11 — não
   é descoberta independente. O coeficiente bate com CC2 com razão 1.000 POR
   CONSTRUÇÃO (mesmo protocolo): coerência interna, não confirmação.
2. Os tipos "diamond" e "chain" dão números idênticos até o último dígito: o
   estimador τ só vê os endpoints das regiões internas — **o driver de k é a
   duração tipo-tempo interna, não a topologia de ciclos (Betti)**. O teste
   genuinamente distinto é o tipo "poisson" (durações aleatórias): α = 0.941.
3. A escala ABSOLUTA de ℏ continua externa à geometria (veredito e11,
   inalterado): aqui mede-se apenas a ESTRUTURA k ∝ N, que sustenta a leitura
   "ℏ = ação por evento causal" como consistência, não como derivação.

## Linha honesta final

As duas apostas de dimensão emergente morreram como esperado ("probabilidade
baixa"/"muito baixa" no pré-registro): a regra de crescimento e7, covariante e
Bell-causal, produz causets não-manifold — dimensão 3+1 não emerge nem é
atraída. O resultado positivo (T3C) é o de probabilidade moderada prevista, e
é uma extensão coerente de CC2+e10+e11, não um resultado novo independente:
seu conteúdo novo real é (a) a leitura interferométrica franjas ∝ 1/N e
(b) a identificação do driver (tempo próprio interno, não ciclos).

## Artefatos

| O quê | Onde | Reproduzir |
|---|---|---|
| Motor + estimador | `results/tier3/tier3_core.py` | `python results/tier3/tier3_core.py` |
| Gate do sampler | `results/tier3/T3V_validation/` | `python results/tier3/T3V_validation.py` |
| T3A | `results/tier3/T3A_dynamic_poisson/` | `python results/tier3/T3A_dynamic_poisson/T3A_growth.py` |
| T3B | `results/tier3/T3B_dimension_attractor/` | `python results/tier3/T3B_dimension_attractor/T3B_attractor.py` |
| T3C | `results/tier3/T3C_hbar_granularity/` | `python results/tier3/T3C_hbar_granularity/T3C_phase.py` |
| Campanha completa | — | `python results/tier3/run_all.py` |

Anti-circularidade: `results/tier3` incluído em `tests/test_no_circularity.py`
(SCAN_DIRS); guard PASSED. Nenhum gerador contém d=4, ℏ, escala de Planck ou
fórmula de dilatação; números complexos só no bloco COMPARISON ONLY de e11.
