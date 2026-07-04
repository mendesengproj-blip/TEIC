# FN4-4 — Forecast: testar a transição em λ_A = 17.3 pc

> `FN4_4_forecast.py` → `FN4_4_forecast.json` + `FN4_4_forecast.png`.
> Calibração de sensibilidade ancorada em Chae: σ_γ = K/√N, com K = 0.06·√26615 ≈ 9.79.

## O obstáculo estrutural (a descoberta central de FN4-4)

```
Raio de maré (Jacobi) de binária ~1 M☉ na vizinhança solar:  r_J ≈ 1.7 pc
                                                              = 3.5×10⁵ au
Comprimento de correlação a testar:                          λ_A = 17.3 pc
Regime da transição:                                          s ~ 5–50 pc  (3–30 × r_J)
```

Binárias **ligadas** são desfeitas pela maré galáctica além de r_J ≈ 1.7 pc
(Jiang & Tremaine 2010). O regime onde a transição da DEV acontece (5–50 pc) é
**3 a 30 vezes mais largo que r_J** → **não existem binárias ligadas ali**. A densidade
de pares tem um mínimo em poucos × r_J e um pico exterior em 100–300 pc feito de pares
**outrora ligados que se afastam** (não-ligados). Logo:

> **O teste limpo do joelho em 17 pc não pode ser feito com binárias ligadas.** Precisa
> de pares co-móveis / aglomerados em dissolução, cujo movimento relativo **não é
> orbital** (3D em vez de circular) — confundindo a estatística ṽ.

## N de tracers para 3σ

```
Teste da transição (5↔50 pc):  γ vai de 1.09 (blindado) a 1.34 (MOND), Δγ ≈ 0.25
   N ≈ 28.000 pares co-móveis cobrindo 5–50 pc para 3σ
   PORÉM: pares não-ligados → velocidade não-orbital → teste confundido.

Discriminador sub-pc (Chae):   DEV≈Newton (1.00) vs MOND (1.36), Δγ ≈ 0.33
   N ≈ 15.600 binárias ligadas para 3σ — JÁ EM MÃOS (Chae tem 26.615).
```

A ironia quantitativa: o teste que **podemos** fazer (sub-pc) já tem dados de sobra; o
teste que **queremos** (joelho em 17 pc) precisa de um tracer que não é binária ligada.

## Surveys

| Survey | Cobre s ~ 10–100 pc ligado? | Utilidade real |
|---|---|---|
| **Gaia DR4** (2026) | Não — binárias ligadas ainda ≲ 1–2 pc (maré) | aprofunda o teste **sub-pc** (Chae estendido) |
| **Pares co-móveis** DR3/DR4 | Sim em 10–100 pc, mas mistura ligados + dissolvendo | velocidade 3D não-orbital → só estatístico |
| **4MOST / WEAVE** (2025+) | — | RV de alta resolução afia ṽ sub-pc |
| **Roman** (2027+) | — | binárias mais fracas/distantes, estatística sub-pc |

## Resultado FN4-4

Dados existentes cobrem o regime de transição (5–50 pc) com binárias ligadas: **NÃO**
(maré em 1.7 pc). Survey que pode testar λ_A diretamente: **nenhum com binárias
ligadas**; só estatística de pares co-móveis (Gaia DR4 6D), com a ressalva de movimento
não-orbital. N para 3σ: ~2.8×10⁴ pares co-móveis (transição) ou ~1.6×10⁴ binárias
ligadas (discriminador sub-pc, já disponível). **O teste decisivo de curto prazo é o
sub-pc (FN4-3), não a transição.**
