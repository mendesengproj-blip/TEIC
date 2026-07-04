# FN3-1 — Cálculo analítico da densidade relíquia Ω_{m_A} h²(m_A, f_A)

> `FN3_1_analytic.py` → `FN3_1_analytic.json` + `FN3_1_analytic.png`.
> Fórmula padrão de ULDM (charter FN3-1, passo 3) + checagem de 1º princípios.

## A pergunta

Existe algum ponto no espaço (m_A, f_A) **compatível com o Paper II** onde
Ω_{m_A} h² ≈ 0.12? **Resposta: SIM** — a linha de 0.12 passa por f_A ≈ (1–4)×10¹⁷ GeV
em toda a janela de massa do Paper II.

## Grade Ω_{m_A} h² (fórmula canônica, θ_i ~ O(1))

```
  m_A [eV] \ f_A [GeV]      1e15       1e16       1e17       1e18
   3.70e-25 (piso)        7.3e-07    7.3e-05    7.3e-03    7.3e-01
   1.00e-24               1.2e-06    1.2e-04    1.2e-02    1.2e+00
   1.00e-23               3.8e-06    3.8e-04    3.8e-02    3.8e+00
   1.00e-22 (~teto)       1.2e-05    1.2e-03    1.2e-01    1.2e+01
```

Ω = 0.12 · (m_A/10⁻²² eV)^{1/2} · (f_A/10¹⁷ GeV)².

## A linha de Ω h² = 0.12 (qual f_A é necessário)

```
   m_A = 3.70e-25 eV  →  f_A = 4.05e17 GeV
   m_A = 1.00e-24 eV  →  f_A = 3.16e17 GeV
   m_A = 1.00e-23 eV  →  f_A = 1.78e17 GeV
   m_A = 1.00e-22 eV  →  f_A = 1.00e17 GeV
```

A linha de 0.12 corre por **f_A ≈ 1.0–4.0 ×10¹⁷ GeV** — exatamente a banda de
**escala GUT**. Isto é a conhecida "coincidência do axiverso": um campo ultraleve
(m ~ 10⁻²² eV) com constante de decaimento na escala GUT dá Ω ~ 0.1 automaticamente.

- Em **f_A = 10¹⁷ GeV** a grade dá 0.007–0.12 na janela — ordem certa.
- Em **f_A = 10¹⁸ GeV** super-produz (0.73–12) — DM em excesso.
- Em **f_A ≤ 10¹⁶ GeV** sub-produz por ≥3 ordens — m_A seria DM desprezível.

> **Crítico (antecipa FN3-3):** 0.12 exige f_A na escala GUT. Se f_A vem da relação
> de Stückelberg f_A = m_A/e (~10⁻³¹ GeV), está **47–50 ordens abaixo** → relíquia
> desprezível. A banda que funciona é uma **escala alta livre**, não derivada das
> galáxias. Isto empurra para o **Veredito B**.

## Checagem de 1º princípios (entropia)

A estimativa entrópica independente (ρ_osc = ½m²f_A² diluída por a⁻³ do onset 3H=m
até hoje, com g_*=106.75) dá Ω(10⁻²², 10¹⁷) ≈ **0.015** — um fator ~8 abaixo da
canônica 0.12. A diferença é a **ambiguidade O(1) de onset/g_***: g_*=106.75 (input
do charter, valor de alta-T) super-dilui, pois o onset físico ocorre em T_osc ~ keV
onde g_* ~ 3.4. A integração numérica (FN3-2) remove essa ambiguidade e fixa o fator.
Reportado como cross-check, **não** como número de manchete.

## Critério de morte — NÃO acionado

O critério pré-registrado mata se Ω estiver >2 ordens de 0.12 para **todo** m_A na
janela. Como 0.12 é **alcançável** (f_A ~ 10¹⁷ GeV) para toda a janela, **a relíquia
não é estruturalmente inconsistente**. Sem morte. O que resta decidir (FN3-3/4): f_A
é derivado (A) ou livre (B), e os limites de Lyman-α/estrutura.
