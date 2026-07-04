# SU3 — Hedgehog/Skyrmion: existe e é estável na rede?

## Veredito: **SIM — hedgehog estável (estabilizado pelo termo de Skyrme)**

```
e_sk      E2        E4      E2/E4     massa    F(0)   F(∞)
1.00    72.796    73.198   0.995    145.99    π      0
2.00   103.330   103.230   1.001    206.56    π      0
4.00   142.884   149.878   0.953    292.76    π      0

virial E2=E4 (Derrick):           SIM (0.95–1.00)
perfil F: π→0:                    SIM
rede 3D com Skyrme: mínimo em     λ=0.90  → ESTÁVEL
rede 3D só sigma:                 colapso (mínimo em λ menor) → instável
```

## O resultado

O hedgehog `U(r)=exp(iF(r)r̂·σ)=(cos F, sin F·r̂)` com `F(0)=π`, `F(∞)=0` mapeia
S³→SU(2)≅S³ com enrolamento `B=1`. A questão de Derrick: a ação mínima da TEIC
estabiliza esse mapa, ou ele colapsa?

**O teorema do virial responde sem ambiguidade.** Sob dilatação `x→x/λ` em 3D,

```
E(λ) = λ E₂ + E₄/λ ,   dE/dλ=0 → λ* = √(E₄/E₂) ,
```

um mínimo estável existe **só com ambos os termos**, e no mínimo vale `E₂=E₄`. Ao
relaxar o perfil radial 1D do funcional completo (sigma + Skyrme) por L-BFGS-B com
gradiente analítico, encontra-se **E₂/E₄ = 0.995, 1.001, 0.953** para e_sk=1,2,4 —
a identidade do virial confirmada. O perfil vai limpo de `F(0)=π` a `F(∞)=0`.

**A rede 3D confirma.** Embebendo o perfil relaxado numa grade cúbica bem resolvida
(>5 pontos por núcleo) e varrendo a energia de dilatação `E(λ)`:
- **com Skyrme**: mínimo interior em `λ=0.90` (tamanho preferido finito) → estável;
- **só sigma (E₄=0)**: a energia cai monotonicamente até o menor `λ` → colapso, a
  imagem de rede da instabilidade de Derrick.

O termo de Skyrme `|c_i×c_j|²` (produto vetorial das correntes, que **anula-se** para
correntes colineares/Abelianas) é o estabilizador genuinamente não-Abeliano.

## Massa

`M_Sk = E₂ + E₄ = 146` (e_sk=1), nas unidades da rede. É a massa do sóliton pontual —
note que é um número finito e bem-definido, ao contrário do vórtice U(1) cujo núcleo
se difundia (CR_3D/PHI_EMERGE). O tamanho do núcleo escala como `√e_sk`.

## Anti-circularidade

Quaternions (4 reais), sem Pauli, sem complexo. "Bárion"/"próton" só como nomes; `B`
é o determinante discreto das correntes (`su2_core.baryon_number`).
`results/matter/su2/SU3_hedgehog.{json,png}` + `SU3_hedgehog.py`.
