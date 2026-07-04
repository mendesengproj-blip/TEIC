# FM1-6 — Síntese honesta: a DEV e a tensão S8

> Campanha FM1_CMB_S8. Testa se a DEV explica a tensão S8 (KiDS σ8≈0.75 vs Planck
> 0.83) com a₀ FIXO de SPARC (1.2×10⁻¹⁰ m/s²) — uma **previsão**, não um ajuste.

## Quadro de resultados (charter FM1-6)

```
FM1-1 (perturbações):
  μ(k,z) derivado analiticamente?          [SIM]  μ=ν(k/k_*(z)) da Poisson MOND
  Sinal de B_ε correto incorporado?        [SIM]  invariante no quase-estático (ω=0)

FM1-2 (módulo "CLASS"):
  Módulo DEV implementado sem erros?        [SIM]  CAMB+ODE de crescimento (CLASS indisp.)
  Reproduz ΛCDM para a₀→∞?               [SIM]  max|μ−1|=0, crescimento idêntico

FM1-3 (σ8) — DECISIVO:
  σ8_DEV < σ8_ΛCDM?                        [NÃO]  σ8_DEV=101 ≫ σ8_ΛCDM=0.81
  S8_DEV consistente com KiDS?             [NÃO]  S8_DEV=103.5 vs 0.766±0.020
  f(z)_DEV < f(z)_ΛCDM?                   [NÃO]  f_DEV > f_ΛCDM em todo z

FM1-4 (lensing CMB):
  C_ℓ^φφ_DEV consistente com Planck?      [NÃO]  realce ~10⁴ (slip OK; crescimento não)

FM1-5 (ISW):
  ISW_DEV consistente com obs?             [NÃO]  crescimento não estagna em z<1
```

## VEREDITO: **C — MORTE: a DEV NÃO reduz σ8 (e piora a tensão S8)**

```
[ ] A — DEV EXPLICA TENSÃO S8
[ ] B — DEV REDUZ σ8 MAS NÃO FECHA
[X] C — MORTE: DEV NÃO REDUZ σ8   (σ8_DEV ≥ σ8_ΛCDM em todo z)
```

**O critério de morte pré-registrado foi acionado**: σ8_DEV ≥ σ8_ΛCDM em todo z
testado (z=0, 0.5, 1, 2). Não houve ajuste para escapar — a₀ é o de SPARC.

## A física (honesta, registrada antes dos números)

A DEV é uma teoria **tipo-MOND**: no regime de baixa aceleração ela **realça** a
gravidade (μ≥1), não a suprime — é assim que explica curvas de rotação sem matéria
escura. A premissa do charter ("gravidade mais fraca nas bordas → cresce mais
devagar → σ8 menor") tem o **sinal errado** para MOND. A derivação honesta de
FM1-1 já avisava: μ≥1 ⇒ crescimento igual ou realçado, nunca suprimido.

O ponto quantitativo decisivo: a aceleração peculiar de um modo de densidade linear
hoje é **g ~ 3×10⁻¹³ m/s² ≪ a₀ = 1.2×10⁻¹⁰** em TODAS as escalas que definem σ8
(g/a₀ ≈ 0.003–0.005). Ou seja, **todo modo cosmológico linear está em MOND
profundo** — consequência direta da coincidência a₀ ≈ cH₀/2π (verificada:
cH₀/2π = 1.04×10⁻¹⁰). Logo μ ≫ 1 e o crescimento dispara (σ8 runaway ~10²). Esta é
a razão clássica pela qual MOND **superproduz** estrutura sem um setor
matéria-escura no completamento relativístico.

## Robustez

A equação `δ'' + (2+dlnH/dlna)δ' − (3/2)Ωm(a)μδ = 0` é monótona em μ:
**qualquer μ≥1 ⇒ σ8_DEV ≥ σ8_ΛCDM.** Independe da interpolação ν(y), do valor
exato de a₀, e do expoente s da lei a₀(z)∝H(z)ˢ (s=½ do charter ou s=1 do Paper V —
ambos realçam). Fechar a tensão S8 exigiria μ<1 em algum lugar, que MOND nunca
fornece. **A morte é estrutural.** O σ8≈101 é runaway (a teoria linear quebra) e
não é uma previsão de valor; o **sinal/direção** é inequívoco e é só isso que o
critério de morte requer.

## Honestidade sobre previsão vs ajuste

a₀ veio de 167 galáxias SPARC (Paper I), não do CMB. Portanto este é um **teste
genuíno** do setor CMB/LSS da DEV — e a DEV **falha** nele: não só não fecha a
tensão S8 como a inverte (S8 muito maior, não menor). É uma **falsificação parcial
da DEV no setor cosmológico de perturbações**, reportada como tal.

## Limitações declaradas (engenharia)

- **CLASS indisponível no host** (precisa de toolchain C no Windows). Usou-se CAMB
  1.6.6 para o baseline ΛCDM (σ8=0.811, S8=0.831, reproduz Planck) + ODE de
  crescimento DEV. Para σ8/S8/f(z) isso equivale a um run `mg_parametrization` do
  CLASS; as funções (μ, Σ) são exatamente as que se passariam ao CLASS.
- **FM1-4/FM1-5** (C_ℓ^φφ, ISW) são argumentos de **ordem de grandeza** ancorados
  no realce de crescimento medido em FM1-3, não espectros Boltzmann completos
  (exigiriam CLASS). A direção (incompatível com Planck) é robusta; números exatos
  ficariam para um run CLASS.

## O que a DEV ainda prevê honestamente no CMB

O **slip** Σ=(1+η)/2 com η−1≈αβ/√x é de poucos % (Paper I/V) — compatível com a
restrição A_lens do Planck. É o **crescimento** de perturbações via μ MOND que
falha. Os dois são consistentes entre si: o setor benigno (slip, BTFR, lensing de
galáxias) sobrevive; a extensão ao crescimento cosmológico não.

## Consequência

```
Tensão S8: NÃO explicada pela DEV (piorada).
  → NÃO há Paper V sobre CMB/S8 com esta física.
  → A previsão observacional válida da DEV permanece BTFR (kill-criterion ativo,
    galáxias), não o CMB.
  → Fronteira mapeada: a DEV funciona onde foi calibrada (baixa aceleração,
    sistemas ligados), mas o regime MOND-profundo universal dos modos lineares a
    torna incompatível com σ8/lensing/ISW.
```

A teoria não foi modificada para escapar da morte. Veredito C registrado.
