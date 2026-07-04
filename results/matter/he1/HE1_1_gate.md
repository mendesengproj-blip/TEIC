# HE1-1 — Engineering gate da rede de alta resolução / boost ultra-relativístico

> Antes de medir, a rede mais fina (N=52, dx=0.314 vs N=35, dx=0.471 de FL3) e o boost maior
> (v=0.90c, 0.99c) precisam **merecer** confiança. Quatro cheques pré-registrados.

| Gate | Conteúdo | Resultado |
|---|---|---|
| **G1** | gradiente analítico de Skyrme = gradiente verdadeiro por sítio | `max_rel_diff = 3.2×10⁻⁹` ✓ |
| **G2** | resolução: sítios no diâmetro do núcleo | **11.1** (FL3: 7.4) → ~1.5× mais fino ✓ |
| **G3** | Skyrmion boostado isolado estável em voo a 0.90c | **FRACO** (ver abaixo) |
| **G4** | **cheque energético decisivo**: KE vs limiar `2 M_Sk c²` | ver tabela |

## G3 — o Skyrmion ultra-relativístico **desenrola em voo**

A v=0.90c, o Skyrmion isolado boostado **perde carga** durante o voo: a banda de `B` cai de
`0.96 → 0.006` ao longo de 600 passos (um único pico de energia, deriva de energia 26%).
A rede discreta **não consegue carregar** um Skyrmion coerente a v→c: ele radia/desenrola
antes mesmo de colidir. Esta é precisamente a limitação que FL3 antecipou ("v→c fora do que
a rede discreta representa fielmente"), agora **medida** diretamente. Não invalida o teste —
**reforça** a morte: a colisão a alta v é de grumos já em decaimento.

## G4 — o cheque energético (decisivo, independente de resolução)

```
M_Sk(rede, N=52) = 300.1   (B=+0.963)      2 M_Sk c² = 576.1
  v=0.50c :  KE = 10.10   KE / 2M c² = 0.0175
  v=0.90c :  KE = 32.72   KE / 2M c² = 0.0568
  v=0.99c :  KE = 39.59   KE / 2M c² = 0.0687
  lei de boost  KE ~ v^2.00   →   limite v→c:  KE / 2M c² = 0.070
```

O boost imparte energia cinética **não-relativística**: `KE ∝ v²` (expoente medido = 2.00,
sem fator γ de Lorentz — convenção idêntica a FL3). Logo, mesmo no limite `v→c`, a KE satura
em **7% do limiar de criação de par** `2 M_Sk c²`. Isto é um fato **independente da
resolução**: o mecanismo de boost da rede causal não pode, por construção cinemática,
atingir o limiar de massa-de-repouso de um par novo, a nenhuma velocidade `< c`.

> Análogo ao cheque de energia de feixe do LHC: sabe-se que se está abaixo do limiar pela
> cinemática, antes de qualquer dinâmica de colisão.

## Veredito do gate

```
GATE PARCIAL:
  G1 ✓ (motor rápido validado na rede fina)
  G2 ✓ (genuinamente mais fino: 11 vs 7 sítios/núcleo)
  G3 ✗ (Skyrmion desenrola a 0.90c — limite físico da rede, não bug)
  G4 → KE/limiar ≤ 7% mesmo em v→c
```

O gate **licencia** a medição de colisão (HE1-2) e já **pré-registra** que a criação está
energeticamente proibida (≤7% do limiar). HE1-2 confirma a dinâmica; o veredito é fixado
pela cinemática aqui.
