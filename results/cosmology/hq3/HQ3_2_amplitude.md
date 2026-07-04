# HQ3-2 — Amplitude do sinal do m_A vs NANOGrav

> A frequência cai na banda (HQ3-1). A amplitude acompanha? Aqui separamos **dois**
> observáveis fisicamente distintos que o prompt mistura — e essa separação **é** o
> resultado.

## Dois sinais diferentes (não confundir)

### (a) Oscilação métrica monocromática de Khmelnitsky–Rubakov (LINHA)

Um condensado **homogêneo** de DM tem uma pressão oscilante p = −ρ cos(2ωt). Essa
pressão move o potencial newtoniano com amplitude adimensional (KR 2014):

```
Ψ_c = π G ρ_DM / ω²,    ω = m_A c²/ℏ
```

É uma **linha** monocromática em f_GW — o observável real de PTA para DM ultraleve.
**Não** é um fundo estocástico que se propaga; é uma oscilação local da métrica.

### (b) Fundo estocástico de GW que se propaga (SGWB)

Um condensado **homogêneo não irradia gráviton on-shell** (fonte com k=0; dois quanta
de massa m em repouso → gráviton com energia 2m e momento 0 é cinematicamente
proibido). O SGWB das flutuações de densidade do m_A é, no máximo, da ordem de Ψ_c²
da densidade de DM — astronômicamente pequeno. Reportamos um **teto generoso** ~Ψ_c²
só para mostrar a ordem de grandeza.

## Resultados

### (a) Linha KR vs força do NANOGrav

```
  m_A [eV]   f_GW [Hz]   Ψ_c(1ºpr)  Ψ_c(KR-lit)   h_c,NG    Ψ_c/h_c
  4.14e-24   2.00e-09     3.8e-15    1.6e-14     1.5e-14    0.25
  5.00e-24   2.42e-09     2.6e-15    1.1e-14     1.3e-14    0.19
  1.00e-23   4.84e-09     6.5e-16    2.7e-15     8.4e-15    0.077
  3.00e-23   1.45e-08     7.2e-17    3.0e-16     4.0e-15    0.018
  1.00e-22   4.84e-08     6.5e-18    2.7e-17     1.8e-15    0.0036
  1.20e-22   5.80e-08     4.5e-18    1.9e-17     1.6e-15    0.0028
```

- `Ψ_c(1ºpr)` = π G ρ/ω² (transparente, conservador); `Ψ_c(KR-lit)` = forma citada
  ~2×10⁻¹⁵ (ρ/0.3)(10⁻²³/m)² — fator ~4 acima, a ambiguidade O(1) de definição
  (potencial vs strain vs resíduo; o fator 2 do 2ω). Mesma escala, mesma conclusão.
- `h_c,NG` = strain de banda larga do NANOGrav na **mesma** frequência.
- Ambos assumem m_A = **100% da DM local** (ρ ≈ 0.4 GeV/cm³).

**Leitura:** no **fundo** da janela de sobreposição (m_A ≈ 4–5×10⁻²⁴ eV), a linha KR
chega a Ψ_c ≈ 1.6×10⁻¹⁴ (KR-lit), **comparável** ao strain do NANOGrav (~1.5×10⁻¹⁴) —
razão ~1 nessa leitura, ~0.25 na conservadora. Subindo em massa, Ψ_c ∝ m⁻² **cai
rápido**: em 10⁻²² eV está 2–3 ordens abaixo. Ou seja, a amplitude só **roça** a
sensibilidade do PTA na ponta de massa baixa da janela.

**O porém de Lyman-α (HQ3-4, herdado de FM4/FN3):** justamente nessas massas baixas o
m_A **não pode ser 100% da DM** (o piso de 100%-DM é ~2×10⁻²¹ eV, acima de toda a
janela). Como subdominante (frac < 1), Ψ_c escala com a fração: a 10% da DM local, a
linha cai 10× e fica claramente **abaixo** do limiar atual.

### (b) SGWB que se propaga

```
  teto Ω_GW(m_A) na banda  =  1.4×10⁻²⁹   (gravemente superestimado)
  Ω_GW(1/yr) do NANOGrav   =  8.1×10⁻⁹
  razão (m_A / NANOGrav)   =  1.8×10⁻²¹   (<< 1)
```

O m_A **não** é a fonte do fundo estocástico detectado pelo NANOGrav: mesmo o teto
generoso fica ~21 ordens de grandeza abaixo. O critério de morte "Ω_GW << observado"
**É acionado** para a interpretação SGWB.

## Resposta HQ3-2

| Observável | Veredito |
|---|---|
| Linha KR (frequência) | na banda ✓ (HQ3-1) |
| Linha KR (amplitude, 100% DM local) | **roça o limiar** só em m_A ≈ 4–10×10⁻²⁴ eV |
| Linha KR (amplitude, subdominante via Lyman-α) | **abaixo do limiar** |
| SGWB que se propaga | **~21 ordens abaixo** — não é o fundo do NANOGrav |

A amplitude **não** confirma o m_A como fonte do sinal NANOGrav 2023. O positivo
honesto é que o **mesmo** m_A produz uma **linha** de PTA na frequência certa, perto
do limiar de sensibilidade atual no melhor caso — um alvo distinto e testável, não o
fundo estocástico que o NANOGrav já reportou.

Figura: [`HQ3_2_amplitude.png`](HQ3_2_amplitude.png) — esquerda: linha KR (1ºpr, KR-lit
e caso subdominante 10%) vs strain NANOGrav; direita: SGWB que se propaga ~21 ordens
abaixo do NANOGrav.
