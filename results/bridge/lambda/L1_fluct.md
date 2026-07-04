# L1 — Flutuações de Poisson em volumes aninhados: a lei 1/√(ρV)

> Task L1 of `LAMBDA_EVERPRESENT.md`. N total ~ Poisson (processo de Poisson
> genuíno), 200 sementes, 4 raios aninhados. Data: `L1_fluct.json`.

## Verdict: **coeficiente 0.97 ± 0.05 — a lei δρ/ρ = 1/√(ρV) confirmada com coeficiente 1**

```
raio   rms(δN/N)·√(ρv)
0.2    0.980
0.3    1.027          média: 0.971   (pré-registrado 1.00 ± 0.05 ✓)
0.4    0.926
0.5    0.953
```

## Transparência de procedimento

A primeira rodada (20 sementes, como nos demais experimentos) deu média 0.88 —
dentro de 1σ do erro amostral de um rms com n=20 (≈16%), mas inconclusivo para
a banda de 5%. A correção foi **estatística, não de modelo**: 200 sementes
(erro ≈5%), sem tocar em mais nada. Resultado: 0.971. Os quatro raios são
correlacionados (volumes aninhados, mesmas sementes), então a média não é 4×
mais apertada que cada ponto.

## O que estabelece

O elo (L1) da cadeia: a rede de Poisson tem, em qualquer região de volume V,
um contraste de densidade regional irredutível δρ/ρ = 1/√(ρV), coeficiente 1.
É a entrada estatística do argumento de Λ flutuante (a "everpresent Λ" da
CST); a resposta dinâmica a esse contraste é L2.
