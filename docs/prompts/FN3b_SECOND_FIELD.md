# FN3b_SECOND_FIELD — DEV com segunda escala para a matéria escura

> Campanha de cosmologia (segue FN3). Investiga se a DEV pode produzir f ~ 10¹⁷ GeV
> (escala GUT) — a constante de decaimento que FN3 mostrou ser necessária para
> Ω_DM h²=0.12 — **sem conflitar com a fenomenologia galáctica** (MOND).
> Três caminhos, com critério de morte por caminho.
> Resultados em `TEIC/results/cosmology/fn3b/`.
> **NÃO modifica nenhuma campanha anterior** (consome m_A do Paper II, a relíquia de
> FN3, o bound do slip mediator e o motor `orientation_core` de E1).

---

## Contexto — o que FN3 deixou

FN3-3 mostrou o gap fatal para "m_A É a matéria escura":
- f_A = m_A/e (Stückelberg) ~ 10⁻³¹ GeV
- Necessário para Ω=0.12: f_A ~ 10¹⁷ GeV
- **Gap: 47–50 ordens de magnitude**

Causa: m_A foi calibrado para MOND galáctico (acoplamento forte e, amplitude pequena
v=m_A/e) — incompatível com misalignment eficiente (amplitude grande, escala GUT).
FN3b pergunta: existe extensão **natural** da DEV que produz f~10¹⁷ GeV sem mexer na
fenomenologia de galáxias?

---

## Os três caminhos (com critério de morte)

### Caminho A — o campo escalar θ como candidato ao misalignment
θ (a fase de orientação / contraste de densidade causal) teria amplitude inicial θ₀
no universo primordial; f_θ = θ₀·M_Pl. Relíquia Ω_θ = 0.12 (m_θ/10⁻²²)^½ (f_θ/10¹⁷)².
- **Morte A:** θ₀ necessário para Ω=0.12 é fine-tuned além de 10⁻³ (<0.1%) sem
  mecanismo natural.

### Caminho B — hierarquia: dois modos de A_μ (cosmológico vs galáctico)
O modo homogêneo cosmológico (misalignment, amplitude grande) seria independente do
modo galáctico sourced por θ (amplitude pequena v=m_A/e).
- **Morte B:** os dois modos são fortemente acoplados — fixar o galáctico (v=m_A/e)
  fixa o cosmológico, sem liberdade para f_A grande.

### Caminho C — extensão: campo escalar oculto extra χ
χ com m_χ, f_χ~M_GUT, acoplamento λχ²θ ao setor TEIC, **sem** acoplar a bárions
(screened em galáxias). Candidato à identificação natural: χ = |⟨n⃗⟩| (módulo do
condensado ferromagnético de E1).
- **Morte C:** não existe janela (m_χ, f_χ, λ) com Ω=0.12 + MOND-safe + Lyman-α-safe.

---

## CRITÉRIO DE MORTE GERAL (PRÉ-REGISTRADO)

```
PROMISSOR (≥1 caminho):  extensão natural da DEV pode dar Ω_DM=0.12 sem conflitar
        com galáxias → investigar em detalhe; possível Paper sobre DM na TEIC+DEV.
MORTE (todos):  a DEV não estende naturalmente para Ω_DM=0.12 sem nova física
        fundamental → m_A é DM subdominante; a DM principal é outra escala → fronteira.
```

**Honestidade obrigatória:**
1. Parâmetros da DEV/rede do Paper II — **não** ajustar ao CMB. Ω_DM=0.12 é
   COMPARISON ONLY; os cálculos partem da rede/DEV.
2. Critério de morte **por caminho** — não mover parâmetros para escapar da morte de
   um caminho específico.
3. **Fine-tuning reportado como fine-tuning:** se θ₀ precisa de 10⁻³, dizer
   "fine-tuned", não "previsão natural".

---

## PROTOCOLO

```
FN3b-0  ESTIMATIVA ANALÍTICA OBRIGATÓRIA PRIMEIRO (sem código). Ordem de grandeza
        para A/B/C; identificar o caminho mais promissor ANTES de codificar.
                                                       → FN3b_0_estimate.md
FN3b-código  Focar no caminho mais promissor; medir θ₀ natural na rede (orientation_core).
FN3b-A/B/C   Relatório por caminho.   → A_theta_candidate.md / B_two_modes.md / C_extra_scalar.md
FN3b-síntese Veredito por caminho + geral.            → FN3b_synthesis.md
```

Cosmologia padrão (fixa): H₀=67, Ω_m=0.3, T_CMB=2.725 K, g_*=106.75, M_Pl=1.22×10¹⁹ GeV.
Janela do Paper II: m_A ∈ 3.7×10⁻²⁵–1.2×10⁻²² eV; slip mediator m_φ ≲ 6.4×10⁻³⁰ eV.
