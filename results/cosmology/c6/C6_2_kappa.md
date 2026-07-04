# C6-2 — Identificar κ e compará-lo com ℏ/m_A

> Resultado: **κ = ℏ/m_A — por construção (não por ajuste).** A constante de
> proporcionalidade de `v_TEIC = κ∇θ` é fixada pela própria redução de Madelung do
> campo massivo coerente; ela É ℏ/m_A. Portanto a circulação física é
> `∮v·dl = n·h/m_A`, e ela é **consistente** com o valor conhecido de ℏ — o que é o
> que C6 testa (consistência), não uma derivação de ℏ.

---

## Extração estrutural de κ (não ajustada à mão)

Da redução não-relativística de C6-1, a corrente de número e a velocidade são

```
j = (ℏ/m_A)·n·∇θ ,     v_TEIC = j/n = (ℏ/m_A) ∇θ
                       └────────────┘
                            κ ≡ ℏ/m_A
```

κ **não é um parâmetro livre**: ele aparece travado no operador cinético
`−(ℏ²/2m_A)∇²` da equação de Schrödinger/Gross-Pitaevskii do condensado. O mesmo κ²
(via ℏ²/m_A²) é o coeficiente da **pressão quântica** que FM4 já usou para a escala de
Jeans (`fuzzy_transfer`, `jeans_scale_z`). Logo:

```
κ_TEIC = ℏ/m_A        (IDÊNTICO a ℏ/m_A, por construção da matéria-onda)
```

Não há discrepância a documentar — diferente de CR4 (onde m_A "cavalgava" numa escala
externa não-vinculada). Aqui a igualdade é estrutural porque o campo de velocidade
**é** o gradiente de fase de Madelung.

## Circulação física quantizada

Como θ é a fase de Ψ (univalente, single-valued), o winding é inteiro
`∮∇θ·dl = 2πn` (a mesma topologia π₁(S¹)=ℤ já [DERIVADO]). Multiplicando por κ:

```
∮ v_TEIC·dl = κ ∮∇θ·dl = (ℏ/m_A)·2πn = n · h/m_A          (n inteiro)
```

**Esta é a circulação de Onsager-Feynman de um superfluido / fuzzy DM**, idêntica em
forma à de Khoury (`∮v·dl = nℏ/m`). A topologia 2πn da TEIC [DERIVADO] traduz-se, no
setor m_A, em circulação física quantizada com quantum `h/m_A`.

## Valor numérico do quantum de circulação (ℏ EXTERNO, m_A do Paper II)

`κ_circ = h/m_A` (m²/s), calculado em `c6_scales.py` / `C6_3_scales.json`:

| m_A [eV] | κ_circ = h/m_A [m²/s] |
|---|---|
| 3.7×10⁻²⁵ (piso Paper II) | 1.01×10²⁷ |
| 1×10⁻²⁴ | 3.72×10²⁶ |
| 1×10⁻²³ | 3.72×10²⁵ |
| 1×10⁻²² | 3.72×10²⁴ |
| 1.2×10⁻²² (topo Paper II) | 3.10×10²⁴ |

## Nota de honestidade (anti-circularidade)

- **ℏ é INPUT EXTERNO declarado** (ℏ = 1.0546×10⁻³⁴ J·s). C6 NÃO deriva ℏ. O valor
  absoluto de ℏ permanece externo (T3C: ℏ=k/N estrutural; VS5: α conteria ℏ,
  contradição "dois andares"). O que C6-2 mostra é que a **estrutura de vórtices do
  condensado m_A é consistente com o ℏ que a física conhece** — um teste de
  consistência, exatamente como o enunciado pede.
- **m_A vem do Paper II**, não recalibrado aqui (janela [3.7×10⁻²⁵, 1.2×10⁻²²] eV).
- A igualdade κ=ℏ/m_A é *forte* mas não-surpreendente: ela é a assinatura de que o
  setor massivo é genuinamente uma **matéria-onda quântica** (ao contrário do vácuo de
  orientação, clássico). É o que distingue o candidato 1 do candidato 2.

→ C6-2 = SUCESSO (κ=ℏ/m_A estrutural). Prosseguir para **C6-3** (escalas físicas).
