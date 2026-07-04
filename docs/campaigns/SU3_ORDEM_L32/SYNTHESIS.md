# SÍNTESE — CAMPANHA SU3_ORDEM_L32: a ordem da transição em L=32 via parallel tempering

> Pré-registro: `PRE_REGISTRO.md` (congelado antes de rodar). Driver:
> `OT_L32_parallel_tempering.py` (motor `su3_core` importado SEM modificação; camada de
> análise puramente real; guard anti-circularidade verde). Análise/figura:
> `OT_L32_analyse.py` → `L32_verdict.json`, `L32_histogram.png`. Predecessor: OT (L≤24).
> Run: jun/2026, desktop (1 GPU-less CPU), Python/NumPy.

## Veredito (honesto): **PRIMEIRA ORDEM REFORÇADA qualitativamente em L=32; magnitude (forte vs fraca) NÃO resolvida — FRONTEIRA TÉCNICA (Desfecho B + D)**

O parallel tempering em L=32 exibe **múltiplas assinaturas coerentes de 1ª ordem**, mais
fortes que as de OT em L≤24 — mas **não equilibra através da barreira** (zero
round-trips), então a altura da barreira ΔF / calor latente fica **não-quantificada**, e
a distinção forte-vs-fraca permanece em aberto. A continuação limpa exige
**L≳48 com amostragem multicanônica/Wang-Landau em cluster**.

---

## 1. Gate L=16 (validação do motor PT) — PASSA PARCIAL

Detalhe em `GATE_L16.md`. Resumo: o motor PT reproduz as observáveis robustas de OT —
**U4 no pico = 0.563 vs OT 0.565 (0.4%)**, J_c≈2.68 (~1%), ordenamento confirmado, e
**saúde de PT boa** (swap mínimo 0.50, round-trips > 0). χ_max vem ~25% abaixo de OT
(21 vs 29), **consistente com o caveat de sub-equilíbrio que a própria OT registrou**
(burn de 500 sweeps inflava χ); perseguir 29 por ajuste seria circularidade. Gate aceito.

## 2. L=32 — duas corridas

**Corrida 1 (ladder [2.72,2.80], mis-centrada — `prod_l32_miscentered.json`):** o pico de
χ caiu na borda inferior (J=2.720); 19 de 20 slots ficaram na fase ordenada e a região de
transição não foi bracketada. Descartada para o veredito (registrada por transparência).

**Corrida 2 (ladder [2.67,2.75], J_c interior — `prod_l32.json`):** decisiva. χ_max=271
em J=2.721 (slot interior). Estrutura nítida (tabela por slot em `L32_histogram.png`):

| Região (J) | χ | std(b) | U4 | leitura |
|---|---|---|---|---|
| 2.670–2.700 (8 slots) | 2–8 | ~0.002 | ~0.61 | **presos / metaestáveis** (fase única, fluct. mínima) |
| salto em 2.7037 | 8→185 | 0.004→0.015 | →0.376 | **degrau abrupto** de χ |
| 2.704–2.721 (banda, 5 slots) | 170–271 | ~0.016 | 0.38–0.52 | **banda de coexistência, P(b) bimodal** (dip até 0.60) |
| 2.725–2.750 | 159–240 | 0.016→0.012 | 0.57–0.62 | fase ordenada |

## 3. Assinaturas de 1ª ORDEM (todas coerentes, mais fortes que OT)

1. **P(b) bimodal numa banda contígua de slots centrais** (J=2.704–2.721), com ramo
   inferior b≈0.30 e ramo superior b≈0.34 — coexistência de fases, **não** um artefato de
   slot único (aparece em ≥3 slots consecutivos; ver figura).
2. **Degrau abrupto de χ** em J≈2.703 (8→185, ×23 num passo de ΔJ=0.004) — descontinuidade
   tipo calor-latente.
3. **Gargalo de troca de PT localizado EXATAMENTE no par de slots que cruza a transição**
   (swap=0.118 entre J=2.6995↔2.7037), com swap 0.40–0.51 nos dois bulks. Um mínimo
   localizado de aceitação de troca em J_c **é em si um diagnóstico de 1ª ordem**: o gap
   de energia (calor latente) entre as fases faz os histogramas de réplicas adjacentes
   mal se sobreporem. Numa transição contínua a aceitação varia suave, sem mínimo agudo.
4. **Aprisionamento metaestável** dos 8 slots abaixo de J_c (fluctuação mínima, presos na
   fase ordenada) — histerese/barreira, fenômeno de 1ª ordem.
5. **Expoente de χ_max (interno ao protocolo PT, 2 pontos L=16→32):**
   `x = ln(271/21.2)/ln 2 = 3.67`, batendo o `x≈3.63` de OT (5 pontos) e **muito acima**
   do limite contínuo (γ/ν<2) → **lei de volume** (1ª ordem). (Caveat: χ(32) pode estar
   inflado pela amostragem metaestável/mal-misturada, logo x=3.67 é estimativa-superior;
   ainda assim é claramente >2.)

→ Estas assinaturas **reforçam a leitura de 1ª ordem de OT** e tornam tanto a 2ª-ordem
limpa (H0, já morta) **quanto a contínua-com-finite-size MENOS prováveis** que após OT —
uma transição contínua não produziria o gargalo de troca localizado nem o degrau de χ.

## 4. O que NÃO foi resolvido (a fronteira)

- **up_crossings = 0** (nenhuma configuração atravessou a escada de ponta a ponta) e
  **swap mínimo = 0.118** no gargalo de J_c. Pela regra §6.1 do charter (round-trips < 1),
  o **critério de fronteira técnica está disparado**. O PT **não tuneliza através da
  barreira**, então os **pesos relativos das duas fases não são confiáveis em equilíbrio**:
  não dá para extrair ΔF nem o calor latente, nem separar **1ª ordem forte de fraca**.
- Isto **não** é erro de ladder (a corrida 2 centrou J_c no interior e o problema
  persistiu): é **intrínseco** — a barreira de 1ª ordem cresce com L, e PT canônico cruza
  a barreira em tempo que cresce exponencialmente. **É exatamente por isso que o
  multicanônico/Wang-Landau existe** (achata a barreira). Em desktop, mais réplicas ou
  runs mais longos de PT não resolvem.
- **L=40 não foi rodado:** avaliado como **não-viável E não-informativo** — ~8 h/run e o
  problema de cruzamento de barreira **piora** com L (a fronteira se aprofunda, não se
  abre). Só o multicanônico ajuda.

## 5. Reconciliação com OT e com o PAPER_SU3 (transparência)

- **OT (L≤24):** "1ª ordem fraca provável; 2ª ordem desfavorecida; calor latente
  não-resolvido". Esta campanha **avança**: chega a L=32, **reforça as assinaturas de 1ª
  ordem** (bimodalidade explícita numa banda, degrau de χ, gargalo de troca, metaestabi-
  lidade) — sinais que OT, com cadeia canônica presa numa fase, **não** via — e **não
  reverte** nada. A contínua fica mais improvável; a 1ª ordem fica melhor evidenciada.
- **Mas a pergunta quantitativa (forte vs fraca) continua aberta** pela mesma razão de
  fundo de OT (barreira não cruzada), agora com o limite empurrado de L=24 para **L=32**,
  e o requisito atualizado para **L≳48 multicanônico em cluster** (era "L≳32" em OT —
  L=32 agora foi feito e mostrou que PT não basta).

## 6. Verificações de consistência

- **V1 (vs OT):** J_c(PT, L=32)≈2.72; PT roda ~0.02–0.03 abaixo de OT (gate: PT 2.68 vs OT
  2.71 em L=16), então 2.72 é consistente com a deriva de OT (2.74 em L=24) corrigida pelo
  offset PT. ✓
- **V2 (gate):** passou parcial (§1). ✓
- **V3 (saúde de PT):** swap por par e round-trips reportados; o gargalo em J_c é o achado,
  não um defeito a esconder. ✓ (registrado em `L32_verdict.json`)

## 7. Anti-circularidade

Nenhum número de QCD. J_c, χ, expoente, bimodalidade saem só dos dados; "1ª ordem para
N≥3" é só enquadramento (COMPARISON ONLY). Guard `tests/test_no_circularity.py` **verde**
(análise puramente real; complexo SU(3) só dentro de `su3_core`). Sementes/ladders
congelados; a corrida mis-centrada foi preservada, não apagada.

## 8. O que isto muda (para RESEARCH_MAP e PAPER_SU3)

- **Ordem da transição:** de "1ª ordem fraca provável (L≤24, OT)" para **"1ª ordem
  reforçada em L=32 (bimodalidade + degrau de χ + gargalo de troca + metaestabilidade);
  2ª ordem e contínua-com-finite-size ambas desfavorecidas; forte-vs-fraca não resolvida
  porque PT não cruza a barreira (0 round-trips) → requer L≳48 multicanônico em cluster"**.
- **Não muda** o resto de FL1 (a transição existe; confinamento + octeto permanecem
  sólidos, independentes da ordem). Muda só a *força da evidência* sobre a ordem.
