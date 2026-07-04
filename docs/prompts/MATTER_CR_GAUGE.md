# MATTER_CR_GAUGE — Criação de Matéria pelo Setor de Gauge

> Testa se o setor vetorial A_μ (campo de gauge φ) com acoplamento Stückelberg cria
> sólitons estáveis a partir da colisão de cadeias causais escalares.
> Continua após `MATTER_CR_DBI.md` (θ sem winding; A_μ com kink estável).
> **Não modifica** R1–R3, e6–e11, D1–D3, M1–S1, CC*, CR*, DBI*.
> Código e resultados: `results/matter/cr_gauge/`.

---

## Por que CR_GAUGE depois de CR_DBI

DBI revelou três fatos estruturais: (1) a EOM do cosseno **é** sine-Gordon; (2) o
campo escalar θ tem ∮Δθ = 0 → sem winding → sem sólitons; (3) o campo compacto
(gauge) **tem** kinks estáveis (massa = 8) e pares kink-antikink transientes. A
conclusão: criação estável exige o setor de gauge A_μ.

A ação mínima **completa** acopla os dois campos dentro do mesmo cosseno:

```
S = Σ_links Δτ_ij · [1 − cos(φ_ij + Δθ_ij)]
```

onde φ é a fase de gauge (A_μ, nos links, **compacta**) e Δθ é a variação escalar
(nos nós). O acoplamento Stückelberg `A_μ ∂^μ θ` emerge exatamente deste cosseno (C2).
Até agora os setores foram testados **separados**:
- CR3: θ sozinho (BD linear) → sem criação;
- DBI3: θ sozinho (cos completo) → sem winding;
- DBI4: φ sozinho (compacto, isolado) → kink estável.

O que **nunca** foi testado: os dois **juntos, acoplados** — esta campanha.

## A hipótese

Quando duas cadeias colidem com energia suficiente, a energia escalar (θ) pode
transferir para o setor de gauge (φ) via Stückelberg; no setor de gauge a topologia
permite winding → kinks podem ser criados (par kink-antikink).

---

## Estrutura do modelo (e os dois limites)

O cosseno único `cos(u_i)`, `u_i = φ_i + (θ_{i+1}−θ_i)`, faz papel duplo: com φ=0 é o
cos do **gradiente** escalar (= `force_cos` de DBI3, massless → pass-through); com θ=0
é o cos do **valor** de gauge `1−cos(φ)` (potencial compacto S¹ → kinks). O setor de
gauge carrega ainda o termo de **rigidez F²/Wilson** (BRIDGE_WILSON), de modo que φ
isolado é a sine-Gordon padrão (kink de massa 8). O escalar não tem rigidez própria —
todo o seu acoplamento espacial vive dentro do cosseno. Essa assimetria é a afirmação
física de que a criação vive no setor de gauge. Detalhe de normalização em `gauge_core.py`.

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| G1 | Limites (φ=0→DBI3, θ=0→DBI4) + conservação de energia? | `G1_coupled.{py,md,json}` |
| G2 | Transferência θ→φ via Stückelberg? taxa? | `G2_transfer.{py,md,json,png}` |
| G3 | Colisão acoplada: W_φ≠0? ρ_gauge? (20 sementes) | `G3_collision.{py,md,json,png}` |
| G4 | Se kink: estável? massa? par transiente? | `G4_stability.{py,md,json}` |
| G5 | Carga topológica conservada (criação em pares)? | `G5_charge.{py,md,json}` |
| G6 | Síntese + cenário (1–4) | `G6_synthesis.md` |

---

## Protocolo

1. **Anti-circularidade:** carga / winding medidos por contagem de fase **real** nos
   links (sem números complexos). QED, Dirac, pares e⁻e⁺ só em COMPARISON ONLY. Sem
   mc²/2mc², sem fórmula de dilatação SR/GR.
2. **G1 obrigatório:** as três verificações passam antes de G2–G6 (parar se falhar).
3. **Detector de kink:** funcional de energia **corrigido** de DBI4 (massa ≈ 8).
4. **20 sementes mínimo** para G3 (sensível a condições iniciais).
5. **Conservação crítica:** E_total e Q_total monitorados; violação > 5% → bug.

## Cenários

```
1 — Kinks estáveis criados → matéria da TEIC
2 — Pares transientes → pares virtuais QFT
3 — Sem criação estável (setores acoplados mas insuficiente) → fronteira mais profunda
4 — Sem transferência θ→φ → Stückelberg ineficaz
```

---

## RESULTADOS

<!-- VERDICT_BLOCK_START -->

| Tarefa | Resultado | Grade |
|--------|-----------|-------|
| G1 — dinâmica acoplada | VALIDADO (θ-puro=force_cos, φ-puro=sine-Gordon m≈8, E conservada) | A |
| G2 — transferência θ→φ | SIM (até 57% ao gauge; taxa cresce com ρ) | A |
| G3 — kink por colisão | MARGINAL (par só em ρ≥50, regime mal-posto; controlado: peak_φ<π) | C |
| G4 — estabilidade/massa | kink isolado ESTÁVEL (m=8.0≈8); par TRANSIENTE (aniquila) | — |
| G5 — carga topológica | CONSERVADA (Q=0 sempre; criação em pares ±) | A |

**Cenário: 2 + 3 (transferência real, par virtual, mas sem matéria estável).** A
ação acoplada `S=Σ Δτ[1−cos(φ+Δθ)]` tem **transferência Stückelberg efetiva**
(G2: até 57% da energia escalar flui ao gauge — Cenário 4 EXCLUÍDO) e
hospeda **matéria topológica** (G4: kink isolado estável m=8.0≈8, par
kink-antikink **transiente**=pares virtuais), com **carga conservada** (G5: Q=0,
criação em pares). Mas a colisão acoplada **não** cria matéria **estável** no
regime controlado: a energia transferida vira radiação de gauge e a fase só atinge
π (nucleação) em ρ≳50, onde o escalar já é mal-posto (DBI3). **Cenário 3 refinado:**
o gargalo não é a transferência (funciona) mas a **estabilização** da carga —
exige dinâmica de gauge própria (plaquetas/Wilson) ou campo externo. Ver
`results/matter/cr_gauge/G6_synthesis.md`.

<!-- VERDICT_BLOCK_END -->
