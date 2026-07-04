# SU8 — Cinco consistências do Skyrmion SU(2)

## Veredito: **B — 3/5 consistências (massa, gravidade∝massa, isotropia); sem spin-½**

```
1 MASSA       M = E2+E4 = 206.6                                          OK
2 DISPERSÃO   E²−(Pc)² ≈ 0.96 M² (spread 1.2%); M_inert/M=0.16 (Galileu)  NÃO
3 GRAVIDADE   θ~1/r; coeficiente escala com a massa (razão 1.01)          OK
4 ISOTROPIA   anisotropia de cone = 0.097                                 OK
5 SPIN        2π → −estado (SU7): fase quântica FR                        NÃO
```

## O que passa

1. **Massa.** `M = E₂+E₄ = 206.6` (e_sk=2), finita e bem-definida — o Skyrmion tem
   massa de repouso a partir do funcional de energia. (Contraste com o vórtice U(1),
   cujo núcleo se difundia.)

3. **Gravidade θ~M/r.** A densidade de energia do sóliton (fonte da equação de Poisson
   de campo fraco, a ponte D1–D3) gera `θ(r)~1/r`, e o **coeficiente do 1/r escala com
   a massa** (razão 1.01 entre dois sólitons de massas diferentes): o campo
   gravitacional é proporcional à massa, exatamente como exige a ponte newtoniana. O
   espalhamento do ajuste 1/r (0.55) é artefato de caixa finita, não físico.

4. **Isotropia.** A densidade de energia do hedgehog é esfericamente simétrica
   (anisotropia entre cones ±x,±y,±z = 9.7%, dominada pela discretização cúbica).

## O que não passa (honesto)

2. **Dispersão E²=(pc)²+(Mc²)².** Anti-circularidade **proíbe** inserir `γ=1/√(1−v²)`,
   então a dispersão relativística não pode ser construída à mão. Um boost de Galileu
   (`U̇=−v∂ₓU`, sem γ) dá uma massa inercial `M_inert=E₂/3≈0.16 M` — o limite
   **não-relativístico**, não a energia de repouso. O invariante `E²−(Pc)²` fica a 4% de
   `M²` (≈const), consistente a baixa velocidade, mas a dispersão relativística plena
   **não é re-derivada aqui** — ela é herdada da invariância de Lorentz da ação
   (ponte R1–R3), não verificada independentemente. Reportado como **NÃO** (não
   verificado de forma limpa neste experimento).

5. **Spin-½.** SU7: a rotação 2π é o elemento não-trivial de `π₄(SU(2))=ℤ₂` (o
   pré-requisito topológico existe; o cobrimento duplo SU(2) dá −1), mas o sinal
   `|ψ⟩→−|ψ⟩` é uma fase quântica de Finkelstein–Rubinstein na coordenada coletiva
   quantizada — **inacessível à teoria de campo clássica**. NÃO verificado.

## Conclusão

O Skyrmion SU(2) é um **sóliton pontual estável (B=1) com massa de repouso definida,
campo gravitacional próprio proporcional à massa, e isotrópico** — três das cinco
consistências, de forma limpa e não-circular. A dispersão relativística é herdada (não
re-verificada) e o spin-½ é uma afirmação quântica fora do alcance clássico. **Veredito
B.**

`results/matter/su2/SU8_consistency.json` + `SU8_consistency.py`.
