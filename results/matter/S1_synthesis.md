# S1 — synthesis: what the causal network derives about matter

> Re-run of T14–T21BIS with the methodology the audit ([`AUDIT_T14_T21.md`](../../AUDIT_T14_T21.md))
> demanded: reimplemented from scratch, ≥20 seeds, error bars, anti-circularity guard
> extended to cover this campaign (`tests/test_no_circularity.py` **passes**). Every
> verdict below is the *measured* one, including the death-criterion outcomes — which
> the protocol treats as equally valid results.

## The honest table

| Claim | Grade | Evidence |
|---|:---:|---|
| Time is causal connectivity | **A** | R1–R3 (verified; not re-done here) |
| Gravity is causal connectivity | **A** | D1–D3 (verified; not re-done here) |
| **Inertial mass emerges** | **C** | **M1**: `m=F/a` not recoverable — acceleration is force-independent (baseline artifact); only a marginal ~2–3σ trend. No particle to accelerate. |
| **Mass proxy is Lorentz-invariant** | **B** | **M2**: causal-diamond content invariant for Poisson (CV 1.5 %) vs lattice (14.1 %) — but inherited from R1, not an independent mass. |
| **Energy emerges** | **D** | **E1**: `E=m·γ` recovered to 0.4 % — but γ *is* R1's counting; a reinterpretation, not a new derivation. |
| **Energy is conserved** | **C** | **E2**: time-translation symmetry holds for static ρ (CV 1.6 %), broken by CSG growth (+21 %/slab); only approximately additive. |
| **Localized stable states exist** | **C** | **P1**: a sourced lump delocalizes (σ~t^0.76, profile flattens) — no stable rest-state. |
| **Dispersion relation ω²=k²+m²** | **C** | **P2**: not resolved — k²-signal buried under BD variance; m² intercept consistent with 0 but uninformative. |
| **Spin-½ emerges** | **C** | **P3**: 2π rotation → +state (O(2π)=+1 for all integer m). Scalar has no spinor double cover. |
| **Quantum interference** | **C** | **P4**: linear superposition (residual 1e-15); real-wave cancellation (E_opp/E_same=0.28); no `|ψ|²`. Consistent with e11. |

**No matter claim reaches A.** One reaches B (M2, and that one leans on R1). The rest
are C (argument / measured-but-negative) or D (reinterpretation of R1).

## The claim the data support — stated with precision

Not the maximum ("matter *is* connectivity"), not the minimum ("nothing new"), but
what the calculations actually show:

> **Time and gravity are derived from causal connectivity, with verification (R1–R3,
> D1–D3).** Beyond geometry, the causal network carries a **Lorentz-invariant
> connectivity scalar** (M2) — a genuine but modest fact, inherited from R1's Poisson
> invariance — and lets one **re-express relativistic energy as `E=m·γ`** once a rest
> scale is *assumed* (E1, a reinterpretation). But the network does **not** derive an
> inertial rest mass (M1), a stable localized particle (P1), a clean dispersion
> relation or a Klein–Gordon mass (P2), spin-½ (P3), or quantum interference (P4). The
> free scalar sector behaves as a **massless classical real field**: it delocalizes
> ballistically over the light cone, superposes linearly, and carries only
> integer angular structure. Energy is conserved only **approximately**, in the static
> regime, and is broken by the growth (CSG) that the dynamical theory requires.

**More than geometry emerges; far less than the Standard Model.** Spin, a particle
spectrum, Lorentz-invariant inertia, and quantum amplitudes all require structure —
spinor/vector fields, a complex amplitude with a Born rule, an interacting and stable
mode — that is **absent from the scalar θ on a causal set**. This is exactly where
honest fundamental physics should place the boundary, and it matches the audit's
prediction: the T14–T21 *direction* was right; the *tense* ("is / confirmed /
unified") was wrong.

## What would move the matter claims toward A

A stable localized mode with a conserved charge and a derived Klein–Gordon/Dirac
equation; an inertial mass independent of "links/event" shown Lorentz-invariant with
`E²=m²+p²`; a Noether energy that survives growth; a dispersion read from the *summed*
BD action (not pointwise `⟨Bφ⟩`); and a derived spin-statistics / `2π`-vs-`4π` flip
from a spinor sector. Until then, the statement above stands.

## Reproduce

```
python tests/test_no_circularity.py        # guard (now covers results/matter/)
python results/matter/run_all.py            # M1 → M2 → E1 → E2 → P1 → P2 → P3 → P4
```

Each experiment writes `results/matter/<name>.json` (+ a companion `.md`). Per-step
methodology, parameters and full numbers are in the individual reports.
