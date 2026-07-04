# FN3-2 — Integração numérica da equação de φ → densidade relíquia

> `FN3_2_numerical.py` → `FN3_2_numerical.json` + `FN3_2_numerical.png`.
> Integra φ''+3Hφ'+m²φ=0 em fundo FRW realista (radiação+matéria+Λ, Ω_r fixado por
> T_CMB) através do onset, lê a relíquia comóvel conservada ρ_φ a³.

## Resultado: confirma FN3-1 dentro de fator ~2

```
  m_A [eV]   f_A(linha 0.12)   Ω_num   Ω_canon   R(onset)   w_cauda
  3.70e-25      4.05e17 GeV     0.067    0.120      0.40     -0.047
  1.00e-24      3.16e17 GeV     0.067    0.120      0.40     -0.049
  1.00e-23      1.78e17 GeV     0.067    0.120      0.41     -0.044
  1.00e-22      1.00e17 GeV     0.066    0.120      0.41     -0.041
```

- **Ω numérico ≈ 0.067** no f_A da linha de 0.12 — razão Ω_num/Ω_canon = **0.55**,
  estável em todas as massas. Concorda com a fórmula canônica dentro do **fator ~2**.
- O resíduo é o **fator de onset R ≈ 0.40**: a relíquia verdadeira é 0.40× o valor
  ingênuo ½m²φ₀²a_osc³, porque em 3H=m o campo ainda não oscila plenamente. O
  coeficiente canônico 0.12 já embute esse casamento de onset (por isso a canônica
  fica ~2× acima do nosso ½m²φ₀² explícito). **Mesma física, convenção de onset
  diferente** — a direção e a ordem de grandeza são robustas.
- **w_cauda ≈ −0.045** (≈ 0): confirma independentemente o FM4-1 — o campo é **frio**
  depois do onset, e ρ_φ a³ **platôa** (matéria fria, ρ ∝ a⁻³).

## O que o numérico adiciona ao analítico

1. **Remove a ambiguidade de g_***: o fundo FRW usa Ω_r fixado por T_CMB=2.725 K, sem
   escolher g_* no onset. O numérico (0.067) fica **entre** a entrópica (0.015, g_*
   super-dilui) e a canônica (0.12) — consistente com ambas dentro do O(1).
2. **Confirma a escala de f_A**: para obter Ω ~ 0.06–0.12 ainda é preciso f_A ~ 10¹⁷
   GeV. A conclusão de FN3-1 (escala GUT) é robusta ao método.
3. **Onset antes da igualdade**: a_osc = 6.4×10⁻⁷ (m=10⁻²²) a 1.1×10⁻⁵ (piso), todos
   ≪ a_eq = 2.9×10⁻⁴ → m_A já é frio (CDM) bem antes de z_eq (relevante para FN3-4).

## Concordância

```
FN3-1 (analítico, canônico):  Ω(linha 0.12) = 0.120  (por construção)
FN3-2 (numérico, FRW):        Ω(linha 0.12) = 0.067  (fator 0.55, onset O(1))
1º princípios (entropia):     Ω             = 0.015  (g_*=106.75 super-dilui)
```

Os três concordam em **ordem de grandeza ~0.1**. A manchete (Ω~0.12 alcançável com
f_A~10¹⁷ GeV) não depende do método. A dispersão de fator ~8 entre os três é a
ambiguidade O(1) de onset/g_* bem conhecida na literatura de ULDM — declarada, não
escondida.
