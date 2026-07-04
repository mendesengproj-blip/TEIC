# Q3 — Path integral sobre coordenadas coletivas em SU(2) (sem FR)

## Veredito: **SIM — espectro do rotor rígido E_j ∝ j(j+1) reproduzido**

```
matriz de transferência (a=6, M=5000 pontos Haar em S³):
  λ agrupados (ℓ=0..3):  [94.4, 82.8, 66.9, 49.3]
  degenerescências:       [1, 4, 9, 16]  = (2j+1)² = (ℓ+1)²    ✓
  E_ℓ/E_0:                [0, 0.131, 0.345, 0.649]   vs ℓ(ℓ+2)=[0,3,8,15]
  razão E_2/E_1 = 2.638 (alvo 2.67)   E_3/E_1 = 4.965 (alvo 5.0)   ✓
Monte Carlo (N_tempo=50, N_MC=1000):
  gap E_1−E_0 (MC) = 0.150   vs transferência 0.131   → concorda
```

## O resultado

A dinâmica de baixa energia é uma **partícula livre em SU(2)≅S³** com ação
`S=(I/2)∫Tr[q̇†q̇]dt`. Dois métodos independentes, ambos com o núcleo Euclidiano
`exp(−a|q−q'|²)`, `a=I/(2dt)`:

1. **Matriz de transferência** — diagonalizando o núcleo numa amostra de Haar de S³, os
   autovalores se agrupam com multiplicidades **`(ℓ+1)² = 1, 4, 9, 16 = (2j+1)²`** (`j=ℓ/2`),
   e `E_ℓ ∝ ℓ(ℓ+2) = 4j(j+1)` (razões 2.638≈8/3 e 4.965≈5). Logo `E_j ∝ j(j+1)`: o
   espectro do **rotor rígido**.

2. **Monte Carlo** — Metropolis sobre caminhos fechados; o correlator de grau 1 (j=½)
   `C(τ)=⟨q_t·q_{t+τ}⟩` decai como `e^{−(E_1−E_0)τ}`, dando o gap `0.150`, consistente com
   a matriz de transferência `0.131` (mesmo `a`). O propagador reproduz a estrutura.

A estrutura `j(j+1)` e as degenerescências `(2j+1)²` são **medidas**, não inseridas. O
coeficiente absoluto vem de `I` (Q2) via `E_j=j(j+1)/(2I)`; a matriz de transferência
confirma a forma.

## Anti-circularidade

`q` são quaternions unitários; o espectro é lido de autovalores/decaimentos. "spin" só em
notas COMPARISON ONLY. `results/matter/su2_quant/Q3_pathintegral.{json,py}`.
