# HQ3-4 — Consistência com limites existentes

> Um m_A com f_GW na banda do PTA viola algum limite já estabelecido?

## Limites checados

### 1. Nucleossíntese (BBN) — ΔN_eff

O SGWB que o m_A irradia tem teto ~Ψ_c² (HQ3-2b); integrado, dá uma contribuição de
radiação muito abaixo do limite ΔN_eff < 0.3:

```
teto Ω_GW             = 1.4×10⁻²⁹
Ω_GW h² (integrado)   = 6.4×10⁻³⁰
ΔN_eff                = 1.1×10⁻²⁴   <<  0.3   ✓ OK
```

A linha KR, por sua vez, **não carrega energia que se propaga** — não contribui para
ΔN_eff de modo algum.

### 2. CMB primordial

```
Ω_GW h² (integrado) = 6.4×10⁻³⁰  <<  10⁻⁵   ✓ OK  (sem distorção espectral)
```

### 3. Lyman-α (herdado de FM4/FN3)

O piso para m_A ser **100% da DM** é ~2×10⁻²¹ eV, **acima** do teto do Paper II
(1.2×10⁻²² eV). Logo, em **toda** a janela testável por PTA (4.1×10⁻²⁴ – 1.2×10⁻²² eV),
o m_A só pode ser DM **subdominante**.

```
Pode ser 100% da DM na banda?   NÃO em nenhuma massa da janela
Implicação:                     a amplitude KR escala com a fração subdominante
                                → reduz Ψ_c proporcionalmente (HQ3-2)
```

Isto **não é violação de um limite duro** — é a mesma 4ª morte de FM4 reaparecendo: a
janela de massa leve útil para 100%-DM é fechada pelo Lyman-α. Aqui ela rebaixa a
amplitude do sinal de PTA, não a proíbe.

### 4. Janela excluída por sólitons (1.3×10⁻²¹ – 1.4×10⁻²⁰ eV)

```
Massas da banda (≤ 1.2×10⁻²² eV) dentro da janela excluída?   NÃO
```

Todo o overlap testável fica **abaixo** da janela de exclusão por sólitons — **não
afetado**. Limpo.

## Resposta HQ3-4

| Limite | Status |
|---|---|
| BBN (ΔN_eff < 0.3) | ✓ OK (trivial) |
| CMB (Ω_GW h² < 10⁻⁵) | ✓ OK (trivial) |
| Lyman-α | m_A **subdominante** na banda (rebaixa amplitude, não proíbe) |
| Sólitons (1.3e-21–1.4e-20 eV) | ✓ não afetado (banda abaixo) |

Nenhum limite **duro** é violado. O único custo é o Lyman-α empurrar o m_A para
DM subdominante na faixa testável, o que enfraquece a amplitude da linha KR — uma
tensão, não uma falsificação.

Figura: [`HQ3_4_constraints.png`](HQ3_4_constraints.png) — janela do Paper II, faixa
que produz sinal na banda, overlap testável (verde), piso de Lyman-α (roxo) e janela
excluída por sólitons (vermelho).
