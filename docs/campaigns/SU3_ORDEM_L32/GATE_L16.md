# GATE L=16 — validação do motor PT contra SU3_ORDEM_TRANSICAO (OT)

> Charter V2 (PRE_REGISTRO §8): validar o driver de parallel tempering num tamanho já
> caracterizado por OT **antes** de medir em L=32. Dados: `gate_l16.json`.
> Run: jun/2026, motor `su3_core` importado SEM modificação.

## Resultado (R=18, ladder [2.655, 2.745], warmup 300 + burn 1200 + meas 5000, swap_every 2, seed 7)

| Observável | OT (L=16, Metropolis canônico) | PT (este gate) | Razão | Veredito |
|---|---|---|---|---|
| **U4 no pico** | 0.565 | **0.563** | 0.4% | ✅ PASSA (±10%) |
| **J_c (pico de χ)** | ~2.69–2.71 | **2.681** | ~1% | ✅ PASSA |
| **χ_max** | 29.2 | **21–23** | ~0.75 | ⚠️ ~25% BAIXO |
| **Saúde do PT** | (n/a) | min_swap=0.50; up_cross marginal | — | ✅ ladder conectada |
| **dip @ J_c** | 0.00 (unimodal) | 0.11–0.34 (seed-dependente, marginal) | — | ⚠️ no limiar |

## Veredito: PASSA PARCIAL

- **As observáveis robustas reproduzem limpo:** o vácuo ordena, o **Binder U4 no pico
  bate OT em 0.4%** (0.563 vs 0.565), e o J_c cai a ~1% do valor de OT. O motor PT está
  amostrando a mesma física no tamanho conhecido.
- **χ_max vem ~25% ABAIXO de OT (21–23 vs 29), e isto é consistente — não uma falha.**
  A própria síntese de OT registrou que seu χ estava **inflado por sub-equilíbrio**
  ("500 sweeps de burn é curto perto de uma transição lenta; a variância de m infla mais
  a L maior; x_eff≈3.6 > d=3 é impossível assintoticamente ⇒ inflação por
  sub-equilíbrio"). O PT deste gate usa burn muito mais longo + troca de réplicas
  (equilíbrio através da barreira), então um χ_max **menor e melhor-equilibrado é a
  leitura mais provável da verdade**, não um defeito. **Ajustar parâmetros até χ bater
  29 seria circularidade** (perseguir um número que OT mesmo declarou suspeito) — vetado
  pelo guard. Registramos a discrepância como refinamento, não como reprovação.
- **O dip (bimodalidade) em L=16 é marginal e seed-dependente (0.11–0.34).** Está no
  limiar de resolução já em L=16 com a estatística acessível — um aviso direto de que em
  L=32 (8× mais caro, transição mais aguda, pior sobreposição de réplicas) a resolução
  da barreira fica no limite do viável em desktop. OT achou unimodal (0.00) porque uma
  cadeia canônica única **fica presa numa fase** e não tuneliza; PT tuneliza, então pode
  expor coexistência que a cadeia presa de OT perdia — mas a baixa estatística desktop
  torna o sinal instável.

## Implicação para L=32 (registrada antes de rodar L=32)

O gate confirma o motor mas **antecipa Desfecho D (fronteira técnica)**: se a barreira
já é marginal em L=16 com ~1000 amostras/slot, L=32 com a estatística que cabe em
~3h de desktop (R≈20, meas≈3000, ~600 amostras/slot) provavelmente **não resolverá**
forte-vs-fraca-vs-contínua de forma limpa. Rodaremos L=32 mesmo assim (charter manda) e
reportaremos as assinaturas concretas (swap rate, round-trips, expoente de χ, dip) — se
não resolver, declara-se a fronteira com requisito **L≳48 + multicanônico em cluster**,
empurrando o limite de L=24 (OT) para L=32.
