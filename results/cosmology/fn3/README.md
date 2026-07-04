# FN3 — Densidade relíquia do vetor massivo m_A

Campanha de cosmologia que segue FM4. FM4 mostrou que o setor massivo (m_A via
misalignment) **é** matéria escura fria (w=0). FN3 pergunta **quanto**: Ω_{m_A} h² ≈
0.12 com os parâmetros do Paper II (galáxias), sem ajuste ao CMB?

Charter: [`FN3_RELIC_DENSITY.md`](../../../FN3_RELIC_DENSITY.md) (raiz do TEIC).

## Veredito: **B** — Ω~0.12 alcançável, mas com f_A livre (escala GUT)

A massa m_A vem das galáxias; a abundância 0.12 cai na banda f_A~(1–4)×10¹⁷ GeV
(escala GUT, natural mas **não derivada** — o f_A de Stückelberg m_A/e está 47–50
ordens curto). Como 100% da DM, sobrevive ao Lyman-α só no topo da janela (~10⁻²² eV);
senão é DM **subdominante**. Critério de morte pré-registrado **não acionado**.

## Arquivos

| Tarefa | Relatório | Código | Saída |
|---|---|---|---|
| FN3-1 analítico | [`FN3_1_analytic.md`](FN3_1_analytic.md) | `FN3_1_analytic.py` | `.json` + `.png` |
| FN3-2 numérico | [`FN3_2_numerical.md`](FN3_2_numerical.md) | `FN3_2_numerical.py` | `.json` + `.png` |
| FN3-3 f_A da DEV | [`FN3_3_fA.md`](FN3_3_fA.md) | — | — |
| FN3-4 limites | [`FN3_4_constraints.md`](FN3_4_constraints.md) | `FN3_4_constraints.py` | `.json` + `.png` |
| FN3-5 síntese | [`FN3_5_synthesis.md`](FN3_5_synthesis.md) | — | — |
| motor de física | — | `fn3_core.py` | — |

## Reproduzir

```bash
cd TEIC/results/cosmology/fn3
python fn3_core.py            # self-test do motor
python FN3_1_analytic.py      # grade Ω(m_A,f_A) + figura
python FN3_2_numerical.py     # integração FRW do oscilador + figura
python FN3_4_constraints.py   # Lyman-α / Jeans / z_eq + figura
```

Cosmologia (fixa, charter): H₀=67, Ω_m=0.3, T_CMB=2.725 K, g_*=106.75, Ω_DM h²=0.12
(este último COMPARISON ONLY). Janela de massa do Paper II: 3.7×10⁻²⁵–1.2×10⁻²² eV.

## Números-chave

```
Ω~0.12 exige:        f_A = (1–4)×10¹⁷ GeV  (escala GUT)
Ω_num (FRW):         0.067 no f_A da linha de 0.12 (fator 0.55 da canônica; onset O(1))
f_A Stückelberg:     m_A/e ~ 10⁻³¹ GeV  → 47–50 ordens curto → relíquia ~0
Lyman-α (100% DM):   piso ~2×10⁻²¹ eV > teto do Paper II (1.2×10⁻²²); só o topo é marginal
CMB primordial:      a_osc ≪ a_eq em toda a janela → frio antes de z_eq ✓
```
