# Q1 — Zero modes rotacionais do Skyrmion (portão obrigatório)

## Veredito: **SIM — 3 zero modes verificados**

```
massa do Skyrmion M_Sk = 297.17  (e_sk=4)
1 invariância de energia E[A U₀ A†]=E[U₀]: máx diff relativa = 1.0e-13   (alvo <0.1%)
2 tangência ξ_a·U₀ = 0:                     máx = 0.0e+00
  ξ_a casa com diferença finita:            máx erro = 5.0e-06
3 sobreposição (inércia) diag = [312.7, 312.7, 312.7]   offdiag_máx = 9.7e-16
  ortogonal + norma comum:                  SIM
```

## O resultado

A orientação do Skyrmion é uma **coordenada coletiva**: girá-la custa energia zero. Para
o hedgehog `U₀`, uma rotação global `U → A U₀ A†` (`A∈SU(2)`) tem energia **idêntica** —
uma simetria **exata** da ação quiral de rede, pois `½Tr` e os produtos vetoriais das
correntes são invariantes por conjugação. Confirmado: a diferença relativa de energia é
`1e-13` (precisão de máquina), muito abaixo do alvo de 0.1%.

Os três geradores dão três zero modes
`ξ_a(x) = d/d(ângulo)[A U₀ A†] = [T_a, U₀]`, `T_a=(0, e_a/2)`, **tangentes a S³** em cada
sítio (`ξ_a·U₀=0` exatamente) e que casam com a derivada por diferença finita (`5e-6`).
A matriz de sobreposição `⟨ξ_a|ξ_b⟩` é **diagonal** (offdiag `1e-15`) com **norma comum**
(diag `[312.7,312.7,312.7]`) — o espaço de configurações coletivas é `ℝ³×SU(2)`, com a
parte rotacional esfericamente simétrica (a inércia de Q2).

## Anti-circularidade

`A` são quaternions unitários (su2_core, sem Pauli/complexo); o ângulo é geométrico real.
`results/matter/su2_quant/Q1_zeromodes.{json,py}`.
