# FALSIFICATION — Teste da TEIC/DEV contra EHT, JWST, CMB e lensing

> Testa as previsões contra dados públicos **antes** de qualquer paper.
> NÃO modifica nenhuma campanha anterior. Resultados em `results/falsification/`.
> Princípio: a teoria é **testada**, não ajustada; dados externos citados; veredito honesto.

## Quadro de falsificação

```
TESTE EHT (sombra):
  δ_TEIC (M87*):  4.6e-12 μas (escala DEV)  …  1.3e-95 μas (Planck)
  Margem EHT:     ±3 μas       →  CONSISTENTE — mas NÃO-DISCRIMINANTE (TEIC→GR forte)

TESTE JWST (BTFR):
  Δlog(v)_DEV(z=2) = +0.120 dex      vs   BTFR observada ~ não-evolui (0 ± 0.075 dex)
  Tensão = 1.6σ    →  TENSÃO (tentativa, limitada por dados) — ÚNICO TESTE DISCRIMINANTE

TESTE CMB (monopolos):
  Tipo em T3D2: Polyakov (instantons de vácuo)
  Parker bound: não se aplica  →  CONSISTENTE — mas não prevê relíquias físicas

TESTE LENSING (slip):
  η_DEV − 1 ∈ [2.2%, 6.7%]   vs   precisão WL atual ~20%
  →  CONSISTENTE (mas NÃO testado; Euclid é o teste)
```

## Veredito geral

```
[x] TEORIA NÃO FALSIFICADA — consistente com todos os dados atuais
    PORÉM: três dos quatro testes são NÃO-DISCRIMINANTES; o único discriminante
    (JWST/BTFR) mostra TENSÃO tentativa de ~1.6σ que precisa dos dados primários.
[ ] TENSÃO severa    [ ] FALSIFICADA
```

## A resposta honesta

A TEIC **não é falsificada** por nenhum dos quatro testes — mas a leitura honesta é mais
sóbria do que "tudo consistente":

1. **EHT (não-discriminante).** A GR já casa com o EHT (sombra 39.7/50.4 μas vs
   42±3 / 51.8±2.3). A correção quártica da TEIC é `10⁻¹²` (escala DEV, `a₀/a`) a `10⁻⁹⁵`
   (Planck) do tamanho da sombra — **12 a 95 ordens** abaixo das barras. A TEIC **reduz-se
   à GR em campo forte** (os termos `F²`/quárticos são inertes onde `F=0`), então o EHT
   **não testa** o setor quártico. A figura de "5–10%" da introdução **não tem suporte**.

2. **JWST/BTFR (discriminante, tensão tentativa).** Esta é a previsão **realmente
   falsificável**: `Δlog(v)=(1/4)log[H/H₀]`, **+0.120 dex em z=2**, contra ΛCDM (zero). A
   BTFR observada é **aproximadamente não-evolutiva** (Übler+2017/2023), o que coloca a
   previsão a **~1.6σ** — tensão tentativa, dominada por sistemáticos e **limitada pelos
   dados** (não fabriquei os offsets primários). **É o teste que importa.**

3. **CMB/monopolos (não-discriminante).** O plasma de monopolos de T3D2 é de **Polyakov**
   (instantons de vácuo de U(1) compacto), não partículas relíquias — o Parker bound não
   se aplica → consistente. Mas isso significa que T3D2 **não prevê** monopolos físicos a
   serem testados. (Como relíquias, seria falsificado por `~10¹¹²`.)

4. **Lensing/slip (não-discriminante).** Um slip de 2–7% está dentro das barras atuais
   (~20%) → consistente, mas **não testado**. O Euclid (~1%) e a busca pela **anisotropia**
   do slip (assinatura específica da DEV-V) são os testes reais.

## O que isto significa para o paper

- **Pode proceder** — nada está falsificado.
- **Mas com honestidade**: das quatro, **só a evolução da BTFR é um teste genuíno** com os
  dados de hoje, e ela está em **tensão tentativa de ~1.6σ**. O paper deve (a) apresentar a
  previsão da BTFR como a frente falsificável, (b) confrontá-la com os offsets **primários**
  de Übler+2023 (não com uma banda de consenso), e (c) ser explícito de que EHT, CMB e
  lensing atuais **não discriminam** a teoria — são consistências, não confirmações.
- O confronto decisivo futuro: **JWST/ALMA BTFR (z>3)** e **Euclid (slip direcional)**.

`results/falsification/F_{EHT,JWST,CMB,LENSING,synthesis}.{md,py,json}`.
