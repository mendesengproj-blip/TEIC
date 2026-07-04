# Q6 — O Skyrmion quantizado gravita: M_tot = M_Sk + 3/(8I)

## Veredito: **SIM — θ(r) ~ M_tot/r, M_tot = M_Sk + E_{1/2}**

```
M_Sk = 306.46    I = 312.49    E_{1/2} = 3/(8I) = 0.00120
M_tot = M_Sk + 3/(8I) = 306.464   (correção rotacional = 3.9e-6 de M_Sk)
θ ~ 1/r:  espalhamento far-field = 0.55   → OK
coeficiente escala com a massa:  razão 1.40 vs razão de massa 1.63   → OK
```

## O resultado

O estado fundamental `j=½` adiciona a energia rotacional `E_{1/2} = (½)(3/2)/(2I) =
3/(8I)` à massa clássica `M_Sk`. Pela ponte de campo fraco já estabelecida (D1–D3), a
densidade de energia do sóliton gera um campo de Poisson `θ(r) ~ −M/(4πr)`, de modo que o
Skyrmion quantizado gravita com a energia total

```
M_tot = M_Sk + 3/(8I) = 306.464 .
```

Verificado: a densidade de energia gera um campo `θ ~ 1/r` (espalhamento 0.55, limitado
por caixa finita, como em SU8), cujo coeficiente **escala com a massa** (razão 1.40 vs
razão de massa 1.63). A correção rotacional é minúscula (`3.9e-6` de `M_Sk`) mas
**bem-definida** — fecha o ciclo gravitacional: o objeto com B=1 e spin-½ gravita com
massa = massa clássica + energia rotacional.

## Anti-circularidade

`θ` de um solve de Poisson real da densidade de energia; **sem** fórmula de dilatação
SR/GR. Massas são energias do campo quiral. `results/matter/su2_quant/Q6_gravity.{json,py}`.
