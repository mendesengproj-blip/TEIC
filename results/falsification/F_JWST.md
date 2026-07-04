# F_JWST — Evolução da BTFR com redshift: previsão DEV vs dados de alto-z

## Veredito: **TENSÃO (tentativa, ~1.6σ, limitada por dados)** — o único teste genuinamente discriminante

```
LCDM (Ωm=0.315, ΩΛ=0.685):  Δlog₁₀(v) = (1/4) log₁₀[H(z)/H₀]
  z=0.5:  H/H₀=1.322   Δlog(v) = +0.0303 dex
  z=1.0:  H/H₀=1.790   Δlog(v) = +0.0632 dex
  z=2.0:  H/H₀=3.032   Δlog(v) = +0.1204 dex   ← âncora canônica
  z=3.0:  H/H₀=4.566   Δlog(v) = +0.1649 dex

Observado (consenso da literatura, NÃO medido aqui): BTFR ~ não-evolui, offset ≈ 0 ± 0.075 dex
Tensão em z=2: 1.6σ
```

## A previsão

Se a escala de aceleração MONDiana rastreia o ritmo de Hubble, `a₀(z) ~ c·H(z)` (a relação
`a₀~cH` é uma **coincidência medida**, não derivada — `paper/main.tex`, AB1/C3), a relação
bariônica de Tully-Fisher (`v⁴ = G·a₀·M_b`) desloca-se com o redshift por
`Δlog(v) = (1/4)log[H(z)/H₀]`. **ΛCDM prevê evolução nula** (a₀=const); a DEV prevê os
deslocamentos acima. As duas são distinguíveis — **falsificável**. Em z=2: **+0.120 dex**.

## Os dados (honestidade)

**Não fabriquei** os offsets tabulados de Übler+2023. O resultado **robusto e citável** é
que a BTFR é **aproximadamente não-evolutiva** até z~1–2.5 dentro das incertezas:

- Übler et al. 2017, ApJ 842 121 (KMOS³D): o zeropoint da TFR estelar evolui, mas a TFR
  **bariônica** é consistente com **não-evolução**;
- Übler et al. 2023 (arXiv:2302.06647); Nestor Shachar et al. 2023 (arXiv:2304.05339).

Representando o observado como `offset ≈ 0 ± 0.075 dex` (banda dominada por sistemáticos:
suporte de pressão, beam smearing, seleção de amostra), a previsão DEV de **+0.120 dex**
em z=2 fica a **~1.6σ** — **tensão tentativa**.

## Conclusão honesta

Este é o **único dos quatro testes genuinamente discriminante** (EHT e lensing estão no
regime GR/não-testado; CMB depende de interpretação). A previsão é firme; o dado é
limitado. **TENSÃO tentativa de ~1.6σ** — não falsificação, mas o ponto que **exige os
offsets tabulados primários** de Übler+2023 (e idealmente ALMA/JWST a z>3) para um veredito
definitivo. É aqui que a teoria pode ser efetivamente testada.

`results/falsification/F_JWST.{json,py}`.
