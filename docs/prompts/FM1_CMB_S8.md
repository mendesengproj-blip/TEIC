# PROMPT — FM1_CMB_S8: Tensão S8 via DEV

> Charter da campanha. Testa a previsão da DEV para a tensão S8 do CMB, com o
> fundamento microscópico de E1+E2 (campo fundamental = n⃗; sinal de B_ε ≈ −K(k²−ω²)).
> Resultados em `results/cmb/fm1/`. a₀ FIXO de SPARC (1.2×10⁻¹⁰ m/s²) — previsão,
> não ajuste. NÃO modifica nenhuma campanha anterior.
>
> **STATUS: EXECUTADO (jun/2026) — VEREDITO C (MORTE).**
> Ver `results/cmb/fm1/FM1_6_synthesis.md` e `README.md`.

---

## CONTEXTO

A tensão S8: Planck prevê σ8≈0.83; lensing fraco (KiDS-1000, DES Y3) dá σ8≈0.75
(~3σ). A hipótese DEV: a₀∝H(z) tornaria a gravidade efetiva diferente em z~0.5–1,
modificando o crescimento de estruturas e σ8(z=0).

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C):   σ8_DEV ≥ σ8_ΛCDM em todo z. A DEV não reduz σ8.
PARCIAL (B): σ8_DEV < σ8_ΛCDM mas > σ8_obs(KiDS).
SUCESSO (A): σ8_DEV consistente com KiDS (0.766±0.020).
```

## TAREFAS

- **FM1-1**: derivar μ(k,z) analiticamente (G_eff=G_N·μ), a₀∝H(z)ˢ, sinal de B_ε.
- **FM1-2**: implementar módulo DEV (interface CLASS `mg_parametrization`: mu_MG,
  Sigma_MG); verificar limite ΛCDM quando a₀→∞.
- **FM1-3**: P(k,0), σ8, S8, f(z) DEV vs ΛCDM; comparar com KiDS S8=0.766±0.020.
- **FM1-4**: C_ℓ^φφ vs Planck 2018 lensing.
- **FM1-5**: ISW vs correlação CMB-LSS observada.
- **FM1-6**: síntese honesta + veredito.

## PROTOCOLO

1. FM1-1 antes de FM1-2 (analítico guia numérico).
2. Limite ΛCDM exato quando a₀→∞.
3. Sinal correto de B_ε de E2.
4. a₀ NÃO ajustado ao CMB (fixo de galáxias). FM1 é teste, não ajuste.
5. Critério de morte pré-registrado: σ8_DEV ≥ σ8_ΛCDM = C. Não modificar params.
6. 20 realizações para erro numérico.

## RESULTADO EXECUTADO (resumo)

- **FM1-1: μ(k,z)=ν(k/k_*(z))** derivado da Poisson MOND. **Descoberta honesta
  registrada antes dos números:** a DEV é tipo-MOND ⇒ μ≥1 (**realça** a gravidade),
  então a premissa do charter ("gravidade mais fraca → σ8 menor") tem **sinal
  errado**. O sinal de B_ε de E2 é invariante no crescimento quase-estático.
- **FM1-2: limite ΛCDM verificado** (a₀→∞ ⇒ max|μ−1|=0, crescimento idêntico).
  Engenharia: CLASS indisponível no host → CAMB 1.6.6 (baseline σ8=0.811, S8=0.831)
  + ODE de crescimento DEV (equivale a `mg_parametrization`).
- **FM1-3 (decisivo): σ8_DEV=101 ≫ σ8_ΛCDM=0.81; S8_DEV=103.5 vs KiDS 0.766.**
  σ8_DEV ≥ σ8_ΛCDM em todo z (0,0.5,1,2); f_DEV>f_ΛCDM. **Critério de morte
  ACIONADO.** Causa: modos lineares têm g~3×10⁻¹³ m/s² ≪ a₀ (MOND profundo
  universal, a₀≈cH₀/2π) ⇒ μ≫1 ⇒ crescimento runaway. Robusto: qualquer μ≥1 dá
  σ8_DEV≥σ8_ΛCDM (independe de ν, a₀, s).
- **FM1-4: C_ℓ^φφ inconsistente** com Planck (realce ~10⁴; slip OK, crescimento não).
- **FM1-5: ISW inconsistente** com obs (crescimento não estagna em z<1). [FM1-4/5
  são ordem-de-grandeza ancorados em FM1-3; CLASS exigido para números exatos.]
- **FM1-6: VEREDITO C — MORTE.** A DEV NÃO explica a tensão S8 — ela a **piora**
  (σ8 muito maior, não menor). Falsificação parcial da DEV no setor cosmológico de
  perturbações. A previsão observacional válida da DEV permanece **BTFR** (galáxias,
  kill-criterion ativo), não o CMB. Teoria não modificada para escapar da morte.
