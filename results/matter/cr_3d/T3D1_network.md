# T3D1 — A rede causal genuinamente 3+1D

## Objetivo

Construir e certificar a rede causal em 3+1 dimensões **reais** — o que CR_WILSON
(2D) não tinha — antes de medir monopólos (T3D2), corda (T3D3) e colisão (T3D4). A
rede tem dois lados, ambos verificados aqui:

- **Lado conjunto-causal** (sprinkling de Poisson 4D): certifica que a geometria é
  genuinamente d=4 pelo estimador de Myrheim–Meyer, por **contagem** de relações
  causais (sem nenhuma fórmula relativística).
- **Lado teoria-de-campo** (rede espacial 3D + tempo de evolução): o campo escalar
  θ nos sítios e o campo de gauge φ_x, φ_y, φ_z nos elos, com a ação completa
  `S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` agora em **três planos de plaqueta**
  (xy, xz, yz) em vez de um.

## Resultados (5 portões)

```
N (eventos interior)   f (fração de pares causais)   d_MM
        496                    0.0991                 4.011
        999                    0.1006                 3.993
       2001                    0.0988                 4.014
       3998                    0.1001                 3.999
   controle 2D                 0.5000                 2.001
```

| Verificação | Resultado | Critério |
|---|---|---|
| 1. Dimensão Myrheim–Meyer (4D) | **d = 4.00** (convergido) | \|d−4\|<0.1 ✔ |
| 1b. Controle 2D | d = 2.001 | \|d−2\|<0.1 ✔ |
| 2. Lei de volume ⟨N⟩∝τ^p | **p = 4.014** | \|p−4\|<0.15 ✔ |
| 3. Causalidade (1552 elos) | 0 acausais, 0 spacelike | =0 ✔ |
| 4. Limite θ-puro → Laplaciano 3D | erro 2.4×10⁻⁶ | <10⁻³ ✔ |
| 5. Gauge trivial/puro → W_p=0 | fluxo 0.0 | =0 ✔ |

## Como a dimensão é medida (anti-circularidade)

O estimador de Myrheim–Meyer é puramente combinatório. Para um sprinkling de Poisson
de um diamante causal (intervalo de Alexandrov) plano em d dimensões, a fração de
pares **causalmente relacionados** entre todos os pares é

$$f(d) = \frac{\Gamma(d+1)\,\Gamma(d/2)}{2\,\Gamma(3d/2)},\qquad f(2)=0.500,\; f(4)=0.100.$$

Mede-se `f` contando relações da **luz-de-cone nua de Minkowski** (`dt>0` e
`dt² > |dx|²`, `causal_core`) e inverte-se a relação. Nenhum fator de Lorentz, nenhuma
dilatação, nenhum número complexo entra no gerador. A rede 4D produz `f=0.100` →
`d=4.00`; a rede 2D de controle produz `f=0.500` → `d=2.00`. A convergência é estável
de N≈500 a N≈4000 eventos (custo O(N²) na contagem de relações; N~1000 já basta).

## O portão de redução (consistência com CR_WILSON)

A teoria de campo 3D reduz-se exatamente à de CR_WILSON (2D) quando a configuração é
**uniforme em z** com φ_z=0: então W_xz=W_yz=0, as derivadas em z anulam-se e cada
fatia-z evolui idêntica ao motor 2D. Verificado a **zero de máquina** (força de θ e de
φ_x batem com `wilson_core` por fatia, diff 0.0). O novo conteúdo físico — as plaquetas
xz, yz e o monopólo magnético que elas permitem — entra **por cima**, sem tocar a massa
própria do kink herdada (a rigidez 1/dx² de CR_GAUGE).

## Veredito

**T3D1 — Rede 3+1D consistente: SIM.** A geometria é genuinamente d=4 (Myrheim–Meyer
e lei de volume concordam), a causalidade é estrita, o limite escalar fraco reproduz a
equação de Poisson de D3 (`∇²θ = J`), e o gauge trivial tem W_p=0. Os cinco portões
abrem; T3D2–T3D6 prosseguem.
