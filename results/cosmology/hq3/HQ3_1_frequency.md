# HQ3-1 — Frequência central do sinal do m_A vs banda NANOGrav

> Campanha HQ3_NANOGRAV. Um condensado de m_A oscilante imprime uma métrica
> dependente do tempo. Em que frequência? Cai na banda do PTA?

## Física

O campo oscila com frequência **f_DM = m_A c²/h**. Seu tensor energia-momento é
quadrático no campo (ρ ∝ φ², p ∝ φ²), logo oscila no **dobro** da frequência — e é
isso que um Pulsar Timing Array enxerga:

```
f_GW = 2 m_A c²/h = m_A c² / (π ℏ)
```

Esta é exatamente a linha f = μ/π da literatura de DM vetorial ultraleve
(arXiv:2412.12975), confirmando a convenção.

## Resultados

```
      m_A [eV]     f_DM [Hz]     f_GW [Hz]   na banda?
      3.70e-25     8.95e-11      1.79e-10    não  (abaixo)
      1.00e-24     2.42e-10      4.84e-10    não  (abaixo)
      5.00e-24     1.21e-09      2.42e-09    SIM
      1.00e-23     2.42e-09      4.84e-09    SIM
      1.00e-22     2.42e-08      4.84e-08    SIM
      1.20e-22     2.90e-08      5.80e-08    SIM
```

Banda NANOGrav: **f ∈ [2×10⁻⁹, 10⁻⁷] Hz**.

**Massas que produzem f_GW na banda:** invertendo f_GW = 2m_A c²/h,

```
m_A ∈ [4.14×10⁻²⁴, 2.07×10⁻²²] eV
```

**Sobreposição com a janela do Paper II** (3.7×10⁻²⁵ – 1.2×10⁻²² eV):

```
OVERLAP testável por PTA:  m_A ∈ [4.14×10⁻²⁴, 1.20×10⁻²²] eV
```

Quase **dois terços** (em escala log) da janela de massa do Paper II produzem um
sinal na banda do NANOGrav. O piso do Paper II (3.7×10⁻²⁵ eV) fica abaixo da banda;
todo o resto, do meio ao teto (GW170817), está dentro.

## Resposta HQ3-1

| Pergunta | Resposta |
|---|---|
| Existe m_A do Paper II com f_GW na banda PTA? | **SIM** |
| Range compatível | **4.1×10⁻²⁴ – 1.2×10⁻²² eV** |

A frequência é o ingrediente **robusto e livre de modelo** desta campanha: depende só
de m_A (Paper II) e de h. Não há ajuste — a banda do PTA é COMPARISON ONLY. A questão
seguinte (HQ3-2) é se a **amplitude** acompanha.

Figura: [`HQ3_1_frequency.png`](HQ3_1_frequency.png) — f_GW(m_A) e f_DM(m_A) com a
banda NANOGrav (faixa verde horizontal) e a sobreposição testável (faixa laranja).
