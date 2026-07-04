# SU1 — O motor SU(2): portão de quatro verificações

## Veredito: **SIM — motor validado**

```
1 limite U(1)        angle+=4.4e-16  trace=0.0e+00  action=0.0e+00  mono=3.3e-16  PASS
2 identidade grupo   inv=4.4e-16     assoc=3.3e-16  close=3.3e-16                 PASS
3 invariância gauge  rel_err=0.0e+00                                              PASS
4 conservação energia drift=4.0e-4 em 150 passos (geodésico leapfrog)             PASS
```

## O que foi construído

SU(2) é representado como **quaternions unitários** `q=(a₀,a₁,a₂,a₃)`, `|q|²=1`
(SU(2)≅S³). O produto de grupo é o produto de Hamilton sobre esses quatro reais,

```
c₀ = a₀b₀ − a·b ,   c = a₀b + b₀a − a×b ,
```

derivado de `U = a₀ + i(a₁σ₁+a₂σ₂+a₃σ₃)` mas **calculado sem matrizes de Pauli e sem
números complexos**. `½Tr(U)=a₀`; o laço de Wilson é a componente `a₀` da holonomia.
Inverso = conjugado `(a₀,−a)`; exponencial de grupo `exp(i F n̂·σ)=(cos F, sin F·n̂)`.

Dois setores vivem no motor:
- **setor de gauge (links)** — um quaternion SU(2) por link espacial (x,y,z) na grade
  CR_3D → plaquetas de Wilson SU(2), monopolos (SU2), lei de área (SU2);
- **setor quiral (sítios)** — um quaternion `U(x)∈SU(2)` por sítio → energia do
  modelo sigma principal (E₂) + Skyrme (E₄), cujo sóliton é o hedgehog/Skyrmion com
  carga topológica `B∈π₃(SU(2))` (SU3–SU8).

## As quatro verificações

1. **Limite U(1) (exato).** Restringindo todo link/campo ao subgrupo σ₃,
   `exp(iφσ₃)=(cosφ,0,0,sinφ)`: (a) produto = soma de ângulos `4.4e-16`; (b)
   `½Tr=cosφ` `0.0`; (c) a ação de Wilson SU(2) **iguala bit-a-bit** a energia de
   Wilson U(1) de `cr3d_core` (`0.0`); (d) a carga de monopolo da projeção Abeliana
   iguala `cr3d_core.monopole_charge` (`3.3e-16`). **O motor contém CR_3D como caso
   exato.**

2. **Axiomas de grupo.** `U U⁻¹=1`, associatividade e fechamento `|UV|=1` a `~1e-16`.

3. **Invariância de gauge.** `S_Wilson[U]=S_Wilson[gUg⁻¹]` para `g(x)∈SU(2)` aleatório:
   erro relativo **exatamente 0.0** (a holonomia transforma por conjugação, `½Tr`
   invariante).

4. **Conservação de energia.** O integrador é um **leapfrog geodésico** em S³: a
   velocidade angular de corpo `w` é "chutada" pela força e o campo deriva ao longo de
   grandes círculos via `U·exp(dt·w)` (geodésica livre exata). A força do setor sigma
   é analítica (a *staple* `S_n=Σᵢ(U_{n+i}+U_{n−i})`), o que torna o esquema simplético;
   o termo de Skyrme entra por diferença finita estêncil. Deriva de energia
   `4.0e-4` em 150 passos — **limitada e oscilante**, assinatura de um integrador
   simplético correto.

## Nota de honestidade (caminho até o portão)

A primeira tentativa de integrador (Verlet projetado por renormalização) **aqueceu**
a energia monotonicamente — a renormalização ingênua não é simplética em S³. A
segunda (leapfrog geodésico com força por diferença finita da energia baseada em
correntes) ainda derivava de modo independente de `dt` e da amplitude: sinal de uma
componente não-conservativa. A solução foi a **forma O(4) padrão** do modelo sigma de
rede, `e₂=(2/dx²)Σᵢ[1−U_n·U_{n+i}]`, cujo gradiente analítico (*staple*) conserva
energia a `~1e-4`. O motor agora é rápido e simplético. Tudo a jusante usa este motor.

## Anti-circularidade

Quaternions (4 reais), sem Pauli, sem literal complexo, sem fórmula de dilatação SR/GR.
`results/matter/su2/SU1_motor.json` + `su2_core.py`.
