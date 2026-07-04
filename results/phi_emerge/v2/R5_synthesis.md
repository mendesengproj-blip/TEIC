# R5 — PE4_V2 synthesis (scorecard + verdict)

```
R1 — Rarefação ρ_eff(0) < ρ_eff(∞):     SIM (dinâmica, dip~1.0; cinemática PLANA)
R2 — Corrente J_μ circulante:            SIM (circulação 0.57)
R2 — L/(ρξ²) > 1:                        NÃO (=0.38, sub-limiar)
R3 — Dip ∝ W:                            SIM, |Δρ(0)| ∝ W^1.05 (≈linear)
R4 — |Φ_efetivo|(0) → 0:                 SIM (|Φ|(0)=0.00)
R4 — σ_núcleo = constante:               SIM (3.73 ± 0.01, definido 100%)
```

## VEREDITO: **B** — rarefação existe e fecha o núcleo, mas é back-reaction condicional

> **A rarefação existe e ATINGE `|Φ|(0)→0` com núcleo de largura constante na rigidez natural
> — mas só para a densidade causal DINÂMICA (o setor de geometria D1–D3), não o substrato
> fixo de Poisson de PE4, e com a profundidade fixada pela rigidez K (cheia para K≲5). É um
> quarto ingrediente REDUZIDO (promover ρ ao campo dinâmico que a ponte já tem + a rarefação
> faz o resto), não "sem ingrediente" (A).**

### Why B and not A

The prompt's Veredito A ("ação mínima é suficiente, sem quarto axioma") requires the
depletion to be **unconditional**. Here it is a **back-reaction** with two conditions:

1. **It requires ρ to be the dynamical geometry field** (the D1–D3/BD density that relaxes
   under the minimal action), not PE4's fixed Poisson substrate. The *kinematic link count is
   flat* (R1) — a vortex does not change the number of causal links. The depletion appears
   only when the density is allowed to relax (the same relaxation that gives D1–D3's Newtonian
   `GM/r`). Promoting ρ to dynamical is legitimate bridge physics, but it is the step that
   distinguishes this from PE4.
2. **The depth depends on the geometry stiffness K** — full (`|Φ|(0)→0`) for K≲5, partial above.
   K is a free parameter (like the DEV's K), so "the core fully empties" is a statement about
   the soft-stiffness regime, not an unconditional fact.

### Why B and not C

Veredito C ("current circulates but no detectable rarefaction") is the *kinematic* reading
alone. It undersells the result: the dynamical density **does** deplete, fully, reaching
`|Φ|(0)→0` with a pinned constant-width core (R4) — the mechanism is real and sufficient in
its regime, not absent.

### What this means for Φ = ρ·e^{iφ̄}

PHI_EMERGE (Veredito C) found the phase emerges (gauge mass `m_A∝√ρ`) but the *magnitude* does
not (no core in the fixed-substrate ρ). **PE4_V2 closes the magnitude sector — conditionally:**
if ρ is the dynamical geometry density, the vortex's circulating current/action depletes it at
the core (`|Φ_eff|(0)→0`, σ_core constant, dip ∝ W), pinning the vortex. So the chain

```
sprinkle → gauge φ → vortex W=1 → circulating current J (R2)
        → action peaks at core → dynamical ρ depletes there (R1, R3)
        → |Φ_eff| = ρ_eff → 0 at core, pinned (R4)
```

closes **provided** the causal density is dynamical and the stiffness is soft. The honest
position: the fourth ingredient is not eliminated but **reduced** — from "add a complex scalar
with its own `|Φ|²|DΦ|²` kinetic term" (CR_ABELIAN_HIGGS) to "let the causal density
back-react, as D1–D3 already do." Whether that reduction counts as "the minimal action
suffices" depends on whether the dynamical density is part of the theory or an extra
assumption — a genuinely open, and now precisely located, question.

## Triple verification for A — not asserted

Veredito A is the most important possible result and was held to require an *unconditional*
closure. The closure here is conditional (dynamical ρ + soft K), and the kinematic count is
flat, so **A is not claimed**; B is reported.

## Output
`R5_synthesis.py`, `R5_synthesis.json`. Full campaign: `results/phi_emerge/v2/`.
