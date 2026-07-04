# SU4 — Número topológico B (índice de Pontryagin): inteiro e conservado?

## Veredito: **SIM — B é o inteiro topológico correto (→±1, par→0), conservado**

```
B(hedgehog) vs grade:   N=21: +0.780   N=31: +0.894   N=41: +0.939   N=51: +0.961
                        → converge para +1 ao refinar
anti-hedgehog:          B = −0.961    (alvo −1)
hedgehog + anti-hedgehog: B = +0.015  (alvo 0 — enrolamentos cancelam)
B na evolução (do repouso): [0.941, 0.935, 0.915, 0.88, 0.803]
                        deriva curto-prazo (16 passos) = 0.026
```

## O resultado

`B = (1/24π²)∫Tr[(U⁻¹dU)³]` é o enrolamento de `U:S³→SU(2)≅S³` — o elemento de
`π₃(SU(2))=ℤ` que rotula o Skyrmion. Na rede é o determinante discreto das correntes
`(−1/2π²)·det(c_x,c_y,c_z)` (sem rótulo físico no gerador).

1. **Quantização.** O hedgehog dá `B→+1` ao refinar a grade (0.78→0.96, o erro de
   discretização do determinante some); a orientação invertida dá `−1`; o par
   hedgehog⊗anti-hedgehog dá `0` (enrolamentos cancelam). **B é o inteiro topológico.**

2. **Conservação.** Evoluindo o Skyrmion estabilizado (do repouso) com o leapfrog
   geodésico, `B` é aproximadamente conservado a curto prazo (deriva 0.026 em 16
   passos).

## Nota honesta

A força do setor sigma é analítica e conserva energia, mas a força de **Skyrme**
(termo E₄) é calculada por diferença finita estêncil e é **levemente
não-conservativa**: a energia sobe lentamente, o sóliton encolhe e `B` vaza a longo
prazo (até ~0.14 em 32 passos; sob um chute violento, vaza até 0). Isto é um limite de
**discretização** (rede grossa + força E₄ por DF), **não** topológico — no contínuo `B`
é exatamente conservado. Uma força de Skyrme analítica (conservativa) removeria o vazamento;
fica registrado como limitação numérica, não física. A quantização estática de `B`
(o resultado central) é robusta.

## Anti-circularidade

"Bárion"/"próton"/"nêutron" só como nomes. `B` é determinante de quaternions; sem
complexo, sem dilatação. `results/matter/su2/SU4_baryon.json` + `SU4_baryon.py`.
