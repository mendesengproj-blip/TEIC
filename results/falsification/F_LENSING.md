# F_LENSING — Gravitational slip da DEV vs precisão de lensing fraco atual

## Veredito: **CONSISTENTE (mas NÃO testado)** — Euclid é o teste discriminante

```
previsão DEV:  η − 1 ∈ [2.2%, 6.7%]   (e, na DEV-V, slip DIRECIONAL/anisotrópico)
precisão WL atual sobre slip: ~20%  (KiDS-1000, DES Y3; E_G ~ 0.39±0.06 ~ GR)
previsão Euclid:  ~1%
distinguível agora: NÃO    distinguível com Euclid: SIM
```
Refs: Heymans+2021 (KiDS-1000); DES Collaboration 2021 (DES Y3); Reyes+2010 (E_G).

## A análise

A DEV (extensão futura **DEV-V**, `docs/DEV_bridge_future.md`) prevê um slip gravitacional
`η=Φ/Ψ` com `η−1 ∈ [2.2%, 6.7%]` — e, na teoria estendida, um slip **direcional**
(anisotrópico, alinhado ao gradiente de densidade, máximo em bordas de filamentos/aglomerados).

O lensing fraco atual restringe parâmetros de gravidade modificada **isotrópicos** ao
nível de **~10–30%** (KiDS-1000, DES Y3; o estatístico `E_G` de Reyes+2010 ≈ 0.39±0.06 é
consistente com GR). Um slip de **2–7%** está **bem dentro** das barras de erro atuais →
**CONSISTENTE, mas não testado**. O Euclid (~1%) é o instrumento discriminante.

Além disso, o slip da DEV-V é **direcional** — uma assinatura que análises isotrópicas
existentes **nem sequer miram**. Logo, com dados atuais, o teste é **não-discriminante**.

## Conclusão honesta

**CONSISTENTE** com dados atuais simplesmente porque a precisão atual (~20%) não consegue
sondar um slip de poucos %. Não é confirmação — é ausência de teste. O confronto real é o
**Euclid** (slip isotrópico a ~1%) e, idealmente, uma busca pela **anisotropia** do slip
alinhada a `∇θ` (a assinatura específica da DEV-V).

`results/falsification/F_LENSING.{json,py}`.
