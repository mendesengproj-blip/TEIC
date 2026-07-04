# MATTER_CR_HIGGS — Condensado escalar e (não-)pinamento do vórtice

> Testa se o escalar θ da TEIC pode condensar espontaneamente (⟨θ⟩=v) e **pinar** o
> núcleo do vórtice, estabilizando a matéria criada em 3+1D.
> Continua após `MATTER_CR_3D.md` (Veredito B — vórtice criado mas o núcleo difunde).
> **Não modifica** nenhuma campanha anterior.
> Código e resultados: `results/matter/cr_higgs/`.

---

## O que CR_3D deixou aberto

CR_3D criou um vórtice S¹ relativístico em rede genuinamente 3+1D com **4/5**
consistências; a quinta falhou: o **núcleo do vórtice não é pinado e difunde**. A causa
diagnosticada: não há campo que “segure” o centro do vórtice. A cura conhecida em física
é um **condensado escalar** (bloco COMPARISON ONLY: o vórtice de Abrikosov é estável
porque um condensado pina o núcleo). A TEIC já tem o campo θ — a pergunta é se θ pode
condensar e pinar.

## A ação com o potencial de nó (axioma novo)

$$S_{HIGGS} = \sum_{\text{links}} \Delta\tau\,[1-\cos(\phi+\Delta\theta)]
+ \lambda_p \sum_{\square} [1-\cos(W_p)]
+ \sum_{\text{nós}} V(\theta_i)\,V_i,
\qquad
V(\theta) = -\tfrac{\mu^2}{2}\theta^2 + \tfrac{\lambda_h}{4}\theta^4 .$$

`V_i` é o volume de Voronoi do nó (peso causal); na rede regular de CR_3D é uniforme
(`= dx` no balanço de energia do motor, comensurável com `E_kin`/`E_stuck`). O mínimo do
poço duplo está em `v = √(μ²/λ_h)`, **medido** por relaxação, nunca inserido.

> **Honestidade desde o início.** Na ação mínima θ é a **fase de Stückelberg**: entra
> em `cos(φ+Δθ)` só pelo *gradiente* Δθ, com simetria de shift θ→θ+const. V(θ) **quebra**
> essa simetria e fixa θ em ±v. Isso é um mecanismo genuíno, **mas não é idêntico** ao
> condensado de **magnitude** do modelo abeliano-Higgs (onde a magnitude de Φ=ρe^{iα}
> multiplica (∂α−eA)²). Se m_A=e·v, se há comprimento de coerência ξ, e se o núcleo
> pina, são perguntas **medidas** (H2/H3/H4), não presumidas.

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| H1 | θ condensa em ⟨θ⟩=√(μ²/λ_h)? (portão obrigatório) | `H1_condensate.{py,md,json,png}` |
| H2 | massa de gauge m_A da correlação C_φ; m_A=e·v? | `H2_gauge_mass.{py,md,json,png}` |
| H3 | perfil do vórtice: θ(r⊥), B(r⊥), ξ, λ_L, κ | `H3_vortex_profile.{py,md,json,png}` |
| H4 | σ_núcleo(t) vs μ²; μ_c onde pina? | `H4_pinning.{py,md,json,png}` |
| H5 | colisão com condensado (20 sementes); 5 consistências | `H5_collision.{py,md,json,png}` |
| H6 | síntese honesta + veredito A–D | `H6_synthesis.{py,md,json}` |

## Protocolo / anti-circularidade

1. **V(θ) é soma de potências do campo escalar**; `v=√(μ²/λ_h)` é medido por relaxação.
   m_A, ξ, λ_L são **ajustados** de correlatores/perfis reais. Potencial de Higgs,
   condensado de Cooper, Meissner, Abrikosov, Ginzburg-Landau — só em blocos
   `COMPARISON ONLY`. Sem mc², sem dilatação SR/GR, sem números complexos no gerador
   (validado por `tests/test_no_circularity.py`).
2. **H1 antes de tudo** (se ⟨θ⟩ não converge, parar) — imposto em `run_all.py`.
3. **H4 antes de H5** (pinamento estático antes do dinâmico).
4. **20 sementes para H5.** Custo: rede 3+1D + potencial + relaxação.

## Resultados (medidos)

| Hipótese | Resultado |
|----------|-----------|
| **H1 — condensado ⟨θ⟩=v** | **SIM (PASS)** — 100% dos casos convergem a v=√(μ²/λ_h) com erro ≤0.9%; μ²=0 sem condensado; vácuo quebrado preferido (V(v)=−μ⁴/4λ_h<0). |
| **H2 — m_A=e·v** | **NÃO** — a massa do bóson de gauge é ≈ **0.99 em todo v** (inclui v≈1.4), fixada pelo acoplamento do cosseno e≈1, **independente de v** e não-nula em v=0. |
| **H3 — ξ, κ** | **ξ indefinível** — θ não forma núcleo normal (permanece ≈v); λ_L≈0.72 medido (≈1/m_A); κ não classifica. |
| **H4 — pinamento** | **NÃO** — σ_núcleo cresce ~350% para todo μ² testado; μ_c não existe no regime computável; μ²=0 reproduz a difusão de CR_3D. |
| **H5 — colisão** | colisão na escala do condensado; núcleo criado **difunde** (5ª consistência não fecha). |

## Veredito: **C** — o condensado existe, o pinamento não ocorre

A causa raiz é física e honesta: **θ é a fase de Stückelberg, não a magnitude**. V(θ)
condensa θ (H1 ✓) e abaixa a energia do vácuo, mas o condensado de uma *fase* não
reproduz o mecanismo abeliano-Higgs — que precisa que a **magnitude** de um campo
complexo multiplique (∂α−eA)² para gerar m_A=e·v, o núcleo normal (ρ→0) e o pinamento.
A ação mínima **não tem** o termo |Φ|²|D_μ|².

**CR_HIGGS localiza o ingrediente ausente com mais precisão que CR_3D:** não é “um
condensado escalar” genérico, e sim um **escalar complexo cuja magnitude acopla ao
fluxo de gauge**. Adicionar V(θ) a um θ que é fase não basta — seria preciso promover θ
a magnitude (ou somar um campo de magnitude), um **quarto** ingrediente da ação. Detalhe
completo em `results/matter/cr_higgs/H6_synthesis.md`.

```
2D U(1) (CR_WILSON):     objeto suportado, SEM monopólos/corda                  → D
3D U(1) (CR_3D):         monopólos+plasma+corda; VÓRTICE relativístico;
                         núcleo difunde                                          → B
3D U(1)+V(θ) (CR_HIGGS): θ condensa (H1 ✓); m_A≠e·v (H2); sem núcleo normal (H3);
                         núcleo difunde (H4/H5)                                  → C
                         falta: escalar de MAGNITUDE acoplado ao fluxo de gauge
```
