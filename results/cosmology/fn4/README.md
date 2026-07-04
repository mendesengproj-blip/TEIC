# FN4 — Blindagem MOND abaixo de λ_A = 17.3 pc (teste com Gaia)

Campanha de falsificação. A DEV prevê que o reforço MOND, mediado pelo vetor massivo
m_A, é **blindado abaixo do comprimento de correlação λ_A = 17.3 pc** → binárias largas
sub-pc devem ser **newtonianas**. Previsão exclusiva (nenhuma MOND padrão a faz).

Charter: [`FN4_MOND_SCREENING.md`](../../../FN4_MOND_SCREENING.md) (raiz do TEIC).

## Veredito: **C — TENSÃO** (condicional a D; transição inacessível a binárias ligadas)

As binárias de Chae+2023 (0.001–0.145 pc, ≤ 0.84% de λ_A) estão na zona blindada, onde a
DEV prevê γ ≈ 1.00; Chae mede γ = 1.43 ± 0.06 → **7.1σ** (= condição de morte
pré-registrada), **mas o sinal é contestado** (Banik/Pittordis acham γ≈1, que confirma a
DEV). O joelho da transição em 17 pc é inacessível a binárias ligadas (maré r_J ≈ 1.7 pc).
A previsão é falsificável **já**, via o debate de binárias largas no Gaia DR4.

## Arquivos

| Tarefa | Relatório | Código | Saída |
|---|---|---|---|
| FN4-1 perfil | [`FN4_1_profile.md`](FN4_1_profile.md) | `FN4_1_profile.py` | `.json` + `.png` |
| FN4-2 velocidades | [`FN4_2_velocity.md`](FN4_2_velocity.md) | `FN4_2_velocity.py` | `.json` + `.png` |
| FN4-3 Gaia/Chae | [`FN4_3_gaia.md`](FN4_3_gaia.md) | `FN4_3_gaia.py` | `.json` + `.png` |
| FN4-4 forecast | [`FN4_4_forecast.md`](FN4_4_forecast.md) | `FN4_4_forecast.py` | `.json` + `.png` |
| FN4-5 síntese | [`FN4_5_synthesis.md`](FN4_5_synthesis.md) | — | — |
| motor de física | — | `fn4_core.py` | — |

## Reproduzir

```bash
cd TEIC/results/cosmology/fn4
python fn4_core.py            # self-test do motor
python FN4_1_profile.py       # perfil g_DEV(r) + figura
python FN4_2_velocity.py      # estatística ṽ(s) + figura
python FN4_3_gaia.py          # blindagem no regime de Chae + figura
python FN4_4_forecast.py      # N para 3σ + obstáculo de maré + figura
```

Parâmetros fixos (charter): a₀ = 1.2×10⁻¹⁰ m/s², λ_A = 17.3 pc, g_ext = 1.79 a₀
(V_c=233 km/s, R₀=8.2 kpc). **Não ajustar λ_A.**

## Números-chave

```
λ_A = 17.3 pc;  r_MOND(1 M☉) = 0.034 pc;  γ_plateau (EFE) = 1.356
Modelo:  g_DEV = g_N·[1 + (ν_eff−1)·(1−e^{−r/λ_A})],  ν_eff = ν_RAR(√(g_N²+g_ext²)/a₀)
Chae+2023: 26.615 binárias, 200–30.000 au = 0.001–0.145 pc, γ = 1.43 ± 0.06
Blindagem no regime de Chae: DEV mantém <1% do boost → γ_DEV ≈ 1.00 → tensão 7.1σ
Maré: r_J ≈ 1.7 pc ≪ λ_A → joelho de 17 pc inacessível a binárias ligadas
N(3σ): ~1.6×10⁴ binárias sub-pc (já em mãos) / ~2.8×10⁴ pares co-móveis (transição)
```

## Duas correções de fórmula (documentadas em `fn4_core.py`)

1. Blindagem `S(r) = 1 − e^{−r/λ_A}` (não `e^{−r/λ_A}`): MOND on em grande r (galáxias),
   off em pequeno r (binárias). λ_A inalterado.
2. Interpolação `ν_RAR = 1/(1−e^{−√x})` (McGaugh/SPARC), não `1/√(1−e^{−√x})`. a₀ inalterado.

As conclusões independem dessas escolhas.
