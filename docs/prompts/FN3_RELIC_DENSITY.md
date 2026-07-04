# FN3_RELIC_DENSITY — Densidade relíquia do vetor massivo m_A

> Campanha de cosmologia. Calcula a densidade relíquia do campo vetorial massivo
> m_A da DEV via mecanismo de *misalignment* e pergunta: **Ω_{m_A} h² ≈ 0.12?**
> (o valor observado de Ω_DM h²).
> Resultados em `TEIC/results/cosmology/fn3/`.
> **NÃO modifica nenhuma campanha anterior** (consome m_A do Paper II, a relação
> `m²_iso·λ_p ≈ 520` de CROSS_RELATIONS_II e o resultado de Lyman-α de FM4).

---

## Contexto — o que já se sabe

FM4 (`TEIC/results/cmb/fm4/`) estabeleceu, com disciplina anti-circular, que o
**setor massivo** da TEIC+DEV (o vetor m_A oscilando via *misalignment*) **é
matéria escura fria**:

- FM4-1: `w_late ≈ 0`, `ρ ∝ a^{-3.01}` — frio de verdade (a peça que FM1/FM2/FM3
  não davam: realça / quente / w=−1/3).
- FM4-4: a janela fuzzy/Jeans que *moveria* σ8 é **excluída pelo Lyman-α** (4ª
  morte do programa para S8).

**A questão que FM4 deixou aberta e que FN3 ataca:** *quanto* m_A existe hoje?
Se Ω_{m_A} h² ≈ 0.12 usando os parâmetros do **Paper II** (calibrados em 167
galáxias SPARC, **não** no CMB), então a TEIC+DEV **derivou a abundância de
matéria escura sem ajustar ao CMB**.

### Parâmetros herdados (fixados ANTES de rodar)

| Quantidade | Valor | Fonte |
|---|---|---|
| Janela de massa do vetor | **3.76×10⁻²⁵ < m_A < 1.2×10⁻²² eV** | Paper II + GW170817 (CLAUDE.md DEV) |
| Piso do Paper II | m_A > 3.7×10⁻²⁵ eV (K=1) | Paper II, Item 2 |
| Número puro da rede | m²_iso·λ_p ≈ 520 (escala-invariante) | CROSS_RELATIONS_II, CR4 |
| Cosmologia | H₀=67, Ω_m=0.3, T_CMB=2.725 K, g_*=106.75 | padrão (input) |
| Alvo | Ω_DM h² = 0.12 | Planck (COMPARISON ONLY) |

Varredura: **m_A ∈ {3.7×10⁻²⁵, 10⁻²⁴, 10⁻²³, 10⁻²²} eV** (toda dentro da janela
do Paper II) × **f_A ∈ {10¹⁵, 10¹⁶, 10¹⁷, 10¹⁸} GeV**.

---

## A física do *misalignment* (padrão para campos ultraleves)

1. **Frozen (H ≫ m_A):** o campo é congelado em φ₀ por fricção de Hubble.
   φ'' + 3Hφ' + m²φ = 0 → φ ≈ φ₀.
2. **Onset (3H ≈ m_A):** começa a oscilar coerentemente em T_osc ~ (m_A M_Pl/√g_*)^{1/2}.
3. **Oscilação (H ≪ m_A):** ρ_φ = ½m²φ² com ⟨w⟩→0, ⟨ρ_φ⟩ ∝ a⁻³ (matéria fria).
4. **Relíquia:**
   Ω_{m_A} h² ≈ 0.12 · (m_A/10⁻²² eV)^{1/2} · (f_A/10¹⁷ GeV)²
   onde f_A é a amplitude inicial do campo (a "constante de decaimento").

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO — não alterar após rodar)

```
MORTE:  Ω_{m_A} h² >> 0.12 ou << 0.12 por mais de 2 ordens de magnitude para
        TODO m_A na janela do Paper II — a densidade relíquia é estruturalmente
        inconsistente com a DM observada, qualquer que seja f_A no range testado.

SUCESSO PARCIAL (B):  Ω_{m_A} h² ≈ 0.12 para ALGUM (m_A, f_A) no range, mas f_A
        precisa ser escolhido independentemente (não vem das galáxias).

SUCESSO (A):  Ω_{m_A} h² ≈ 0.12 para o m_A central do Paper II SEM AJUSTE — f_A
        determinado pelos parâmetros da rede/DEV. → 2ª confirmação observacional.
```

**Honestidade obrigatória:**
1. m_A e f_A vêm do Paper II / da rede, **não** do CMB. FN3 é um TESTE, não um ajuste.
2. Se Ω_{m_A} ≫ 0.12: reportar sobreprodução, **não** baixar m_A para escapar.
3. Lyman-α não foi esquecido: FM4 mostrou que m_A leve como 100% da DM é excluído.
   FN3-4 reverifica isso para a densidade relíquia.
4. m_A pode ser DM **subdominante** (Ω < 0.12) coexistindo com outra DM — resultado
   parcial, não excludente.

---

## Tarefas

```
FN3-1  Cálculo analítico Ω_{m_A} h²(m_A, f_A), fórmula padrão + 1º princípios
       (entropia). Figura Ω vs (m_A, f_A) com linha 0.12.   → FN3_1_analytic.{py,md}
FN3-2  Integração numérica de φ''+3Hφ'+m²φ=0 em FRW; ρ_φ(a), Ω numérico;
       cruzar com FN3-1.                                     → FN3_2_numerical.{py,md}
FN3-3  f_A dos parâmetros da DEV: f_A=m_A/e (Stückelberg) vs escala da rede;
       CROSS_RELATIONS_II 520. f_A é livre ou derivado?      → FN3_3_fA.md
FN3-4  Limites: Ω≤0.12, Lyman-α (k~3/Mpc), subdominância em z>z_eq, Jeans z~0.
       Região permitida em (m_A, f_A).                       → FN3_4_constraints.md
FN3-5  Síntese honesta + veredito A/B/C.                     → FN3_5_synthesis.md
```

Protocolo: FN3-1 (analítico) guia FN3-2 (numérico); FN3-3 em paralelo; FN3-4 após
ter Ω calculado. Cosmologia padrão fixa. Critério de morte pré-registrado — não
ajustar parâmetros para escapar de inconsistência.
