# FALSIFICATION_BTFR_V2 — DEV vs dados primários de Übler+2017 (KMOS³D)

> Refina o teste BTFR de `FALSIFICATION.md` (que usou banda de consenso) com os dados
> **primários** de Übler+2017 (arXiv:1703.04321), obtidos do próprio paper.
> Resultados em `results/falsification/btfr_v2/`.

## Veredito: **TENSÃO MODERADA com a DEV** — a tendência observada é *oposta* à prevista
## (mas o teste está no regime errado; não é falsificação limpa)

```
                          z~0.9        z~2.3        mudança interna (z~0.9→2.3)
DEV   Δlog(v):           +0.0551      +0.1325      +0.0774  (CRESCE com z)
obs   Δlog(v) (a local): +0.1173      +0.0720      −0.0453  (DIMINUI com z)  ← robusto
ΛCDM:                     0            0            0

tensão (erros estat., piso inferior):
  a local:   vs DEV  5.8σ / 4.5σ      vs ΛCDM  11.0σ / 5.4σ
  interno:   vs DEV  7.2σ             vs ΛCDM  2.7σ      (tendência OPOSTA à DEV)
```
![BTFR](results/falsification/btfr_v2/B3_comparison.png)

## O cálculo (honesto, com dados reais)

**B1 — previsão DEV** (astropy `FlatLambdaCDM(H0=67, Ωm=0.3)`):
`Δlog(v)=(1/4)log[H(z)/H₀]` → **+0.0551 (z~0.9)**, **+0.1325 (z~2.3)**. *Nota:* em ΛCDM
plano, `H(z)/H₀` é **independente de H₀**, então `H₀±1` propaga **zero** erro; a banda
vem de `Ωm` (±0.002 dex). (Os valores tabulados do prompt, 0.040/0.138, estavam levemente
errados em baixo-z.)

**B2 — dados primários Übler+2017** (Tabela 2; slope `a=3.75` Lelli+2016, `v_ref=242` km/s):
zero-point de massa bariônica `b(z~0.9)=10.68±0.04`, `b(z~2.3)=10.85±0.05`; offset a local
`−0.44`, `−0.27`; **evolução interna +0.17 dex**. Convertendo a `Δlog(v)` a massa fixa
(`Δlog v = −Δb/a`): **+0.117 (z~0.9)**, **+0.072 (z~2.3)**.

**B3 — comparação.** Duas leituras que **discordam** — sinal de sistemáticos dominantes:
- **A local** (variável da DEV): a observação mostra evolução **positiva forte** (galáxias
  giram mais rápido por massa fixa em alto-z). Isso **desfavorece ΛCDM** (zero) **mais** que
  a DEV (11σ vs 5.8σ em z~0.9). Ou seja, "existe evolução" — lado da DEV contra ΛCDM. Mas
  as barras são **só estatísticas** (piso inferior); os sistemáticos dominam.
- **Interno** (z~0.9→2.3, **robusto**, livre da comparação a local): a velocidade a massa
  fixa **diminui** (−0.045±0.017), enquanto a DEV prevê **aumento** (+0.077). **Tendência
  oposta → 7.2σ de tensão com a DEV**; ΛCDM fica a 2.7σ.

## A resposta honesta (mais negativa que a v1)

A v1 reportou "tensão tentativa de ~1.6σ" com banda de consenso. **Os dados primários NÃO
resgataram a previsão para consistência — eles revelaram uma tensão de tendência:**

1. **O sinal a local favorece a DEV sobre ΛCDM** (a bTFR evolui no sentido +, como a DEV
   prevê e ΛCDM não). Isso é genuíno e a favor da ideia de `a₀∝H(z)`.
2. **Mas a forma específica da DEV (Δlog v crescente monotônico) está em tensão** com a
   única quantidade robusta (a evolução interna z~0.9→2.3), que é **plana-a-decrescente** —
   direção **oposta**. Tomado ao pé da letra (erros estatísticos), seria >3σ → "falsificado".

3. **Por que NÃO declaro falsificação limpa** (honestidade nos dois sentidos):
   - **Sistemáticos dominam.** Übler **alertam** que incluir galáxias perturbadas /
     dominadas por dispersão torna a evolução a local "insignificante". A discordância
     entre as leituras "a local" e "interna" **prova** que sistemáticos (não estatística)
     mandam — as barras de 5–7σ são um piso, não a incerteza real.
   - **Viés de massa / regime errado (ressalva obrigatória B5).** KMOS³D é de galáxias
     **massivas, alto brilho** → regime de **alta aceleração (Newtoniano)**, onde o sinal
     de `a₀(z)` da DEV é **intrinsecamente fraco**. A DEV é calibrada em galáxias de
     **baixa massa, ricas em gás** (MOND profundo). **Este não é o regime onde a DEV faz a
     previsão forte** — então não pode falsificá-la de forma limpa.

## Conclusão

```
[ ] DEV CONSISTENTE (<1σ)
[x] DEV EM TENSÃO MODERADA — a tendência interna robusta é OPOSTA à previsão
     monotônica da DEV (~7σ estatístico), atenuada por sistemáticos dominantes
     e por viés de massa (amostra no regime de alta aceleração, errado para a DEV).
[ ] DEV FALSIFICADA (sistemáticos + regime errado impedem falsificação limpa)
[~] vs ΛCDM: os dados a local favorecem "evolução existe" sobre ΛCDM=0, mas
     a forma da DEV não é confirmada.
```

**A teoria não é confirmada nem limpa-mente falsificada por Übler+2017.** O sinal da
evolução bariônica é encorajador (lado da DEV vs ΛCDM), mas a **forma específica** (Δlog v
crescente com z) está em tensão com a medição robusta, e a amostra está no **regime
errado**. **O teste decisivo exige rotadores de baixa massa, ricos em gás, no regime de
baixa aceleração a alto-z** (JWST/ALMA de anãs/discos gasosos) — não galáxias massivas.
O paper deve apresentar esta tensão **honestamente**, não como confirmação.

`results/falsification/btfr_v2/B{1,2,3}.{py,json}`, `B4_literature.md`, `B3_comparison.png`.
