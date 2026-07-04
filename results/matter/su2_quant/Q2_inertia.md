# Q2 — Tensor de inércia rotacional e espectro de spin

## Veredito: **SIM — I esférico, espectro E_j = j(j+1)/(2I) calculado**

```
tensor de inércia I_ab (∫Tr[ξ_a†ξ_b]):
   [312.74    0       0   ]
   [  0     312.74    0   ]
   [  0       0     312.74]
I (média diag) = 312.74    diag spread = 0.0    offdiag/I = 3e-18    → ESFÉRICO

espectro do rotor E_j = j(j+1)/(2I):
   j=0:    0.00000
   j=½:    0.00120   = 3/(8I)
   j=1:    0.00320
   j=3/2:  0.00600
   j=2:    0.00959
```

## O resultado

O tensor de inércia rotacional, `I_ab = ∫d³x Tr[ξ_a†ξ_b] = 2Σ(ξ_a·ξ_b)dx³`, é
**perfeitamente esférico** (`I_ab = I δ_ab`, spread `0`, offdiag `3e-18`) — como exige a
simetria SO(3) do hedgehog. O valor `I = 312.74` (unidades de rede, e_sk=4).

Quantizando o rotor rígido em SU(2)≅S³, os níveis são `E_j = j(j+1)/(2I)`,
`j = 0, ½, 1, 3/2, …`. Ainda **sem** a restrição FR — todos os `j` aparecem aqui; Q4
seleciona os meio-inteiros. O estado meio-inteiro de menor energia, `E_½ = 3/(8I) =
0.00120`, é a energia rotacional do Skyrmion no estado fundamental físico.

## Anti-circularidade

`I_ab` é uma integral real de sobreposição de tangentes-quaternion; "spin j" é rótulo do
espectro. `results/matter/su2_quant/Q2_inertia.{json,py}`.
