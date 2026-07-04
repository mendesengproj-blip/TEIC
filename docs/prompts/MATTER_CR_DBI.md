# MATTER_CR_DBI — Criação de Matéria pelo Setor Não-Linear (DBI)

> Testa se o setor não-linear (cos) da ação mínima cria loops espontaneamente.
> Continua após `MATTER_CREATION.md` (CR3 refutou a ação BD **linear**).
> **Não modifica** R1–R3, e6–e11, D1–D3, M1–S1, CC*, CR*.
> Código e resultados: `results/matter/cr_dbi/`.

---

## Por que DBI depois de CR3

CR3 mostrou que a ação BD **linear** (□θ = J) não cria loops: dinâmica linear,
superposição exata, sem topologia nova. A ação mínima **completa** é diferente:

```
S_DBI = Σ_links Δτ_ij · [1 − cos(φ_ij + Δθ_ij)]
```

O cosseno tem o que o quadrático não tem: (1) saturação |1−cos| ≤ 2; (2) ponto
crítico em φ+Δθ = π (onde sin reverte); (3) periodicidade (a fase pode enrolar).
Em matéria condensada, fases que cruzam π podem nuclear defeitos topológicos
(vórtices/kinks). Na rede causal, o análogo seria um loop persistente.

A equação de movimento do cosseno é a **sine-Gordon de rede**:
`∂_μ[Δτ·sin(φ+Δθ)] = J`. No limite fraco `sin(u) ≈ u` → recupera BD (□θ = J).

## A hipótese

Existe um limiar de fase crítico `(φ+Δθ)_colisão ≥ π` acima do qual o cosseno
inverte e a dinâmica pode criar topologia nova — definindo uma densidade crítica
ρ_DBI onde as fases da colisão atingem π.

---

## O ponto físico decisivo (compacto vs não-compacto)

Defeitos topológicos (winding ≠ 0) exigem um campo de **alvo compacto** (S¹): a fase
de gauge φ é compacta; o campo de densidade θ = δρ/ρ de D3 é **real/não-compacto**
(vácuo único). A ação `Σ[1−cos]` é a estrutura compacta de rede; se o campo físico
for não-compacto, o cosseno apenas **satura** sem criar winding. Testamos os dois e
distinguimos "o detector não vê" de "a física não produz".

Além disso, C3/W4 já estabeleceram que a escala de saturação **X₀ ∝ ρ é UV
(granularidade), não cosmológica (a₀ ~ cH₀)** — o que condiciona fortemente DBI5.

---

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| DBI1 | Propagador cos implementado; reproduz BD (fraco) e D3 (1/r)? | `DBI1_propagator.{py,md,json}` |
| DBI2 | (φ+Δθ)_max vs ρ; ρ_π onde fase atinge π? | `DBI2_phase_map.{py,md,json,png}` |
| DBI3 | Colisão DBI: ψ_tardio > 0? winding ≠ 0? (20 sementes) | `DBI3_collision.{py,md,json,png}` |
| DBI4 | Se loops: estáveis? τ(N) bate com CC2? | `DBI4_stability.{py,md,json}` |
| DBI5 | ρ_DBI ≈ ρ(a₀)? | `DBI5_a0.{py,md,json,png}` |
| DBI6 | Síntese + cenário (1–4) | `DBI6_synthesis.md` |

---

## Protocolo

1. **Anti-circularidade:** π é o ponto crítico do cosseno (propriedade matemática),
   **não** inserido como "limiar de criação". ρ_DBI é medido. Sem mc²/2mc².
2. **Validação obrigatória de DBI1:** se não reproduzir BD em campo fraco E D3
   estático, **parar e reportar**.
3. **Detector de loops:** o detector diferencial validado de CR (ψ tardio + winding/
   kink), nunca Betti absoluto.
4. **Barras de erro:** 20 sementes (ruído nas condições iniciais; a dinâmica cos pode
   ser sensível).
5. **Honestidade sobre o Cenário 4 (caos):** se o regime ultra-forte for caótico,
   reportar como física, não fracasso.

## Cenários

```
1 — ρ* existe, loops estáveis      → DBI cria matéria
2 — ρ* existe, loops instáveis     → DBI cria pares virtuais
3 — ρ* não existe (setor escalar)  → criação exige A_μ (próxima camada)
4 — caos ultra-forte               → fronteira de validade da ação
```

---

## RESULTADOS

<!-- VERDICT_BLOCK_START -->

| Tarefa | Resultado | Grade |
|--------|-----------|-------|
| DBI1 — propagador cos | VALIDADO (BD fraco ~amp², D3 1/r, energia conservada) | A |
| DBI2 — fase π | ρ_π = 18ρ₀ (medido) | A |
| DBI3 — criação (escalar) | NÃO (pass-through; ill-posto acima de ρ_π) | D |
| DBI4 — campo compacto | kink isolado ESTÁVEL (m≈8); par TRANSIENTE (aniquila) | — |
| DBI5 — ρ_DBI vs a₀ | NÃO (ρ_DBI é UV, a₀ é IR) | — |

**Cenário: 3 + 4 (escalar) / 2 (compacto).** O setor escalar (densidade) da ação
cos **não cria matéria**: pass-through abaixo de ρ_π≈18ρ₀, e perda de
hiperbolicidade (`cos''<0`, fuga não-convergente) acima — Cenário 4. O winding é
estruturalmente 0 (campo não-compacto). No campo **compacto** (S¹) a mesma
dinâmica dá um kink isolado **estável** (massa ≈ sóliton sine-Gordon 8) e um par
kink-antikink **transiente que aniquila** (pares virtuais, Cenário 2); o kink
carregado não nasce do vácuo (winding conservado). **Criação estável exige o setor
de gauge A_μ (Cenário 3)**, e a escala ρ_DBI é UV (X₀∝ρ), não o a₀ cosmológico
(DBI5) — reproduzindo C3/W4. Ver `results/matter/cr_dbi/DBI6_synthesis.md`.

<!-- VERDICT_BLOCK_END -->
