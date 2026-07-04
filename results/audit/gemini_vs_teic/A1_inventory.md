# A1 — Inventory of the Gemini (TEIC-GE) work

**Location.** `C:\Users\Mique\Documents\001-PROJETOS\003-TEORIAS\TEIC-GE`
(found; the prompt's path was correct). Structure: `src/` (2 generators) + `results/`
(5 phases). **19 `.py` scripts, 66 `.md` reports, 2 `.png` plots.**

## Phases (what Gemini actually did)

| Phase | Dir | Tests | Topic |
|---|---|---|---|
| **Fundamental** | `teic_fundamental/` | T1–T8 | Maxwell from Wilson loops, a₀ scale, minimal action, EFT tree, Lorentz/gauge restoration |
| **Gauge audit** | `teic_gauge/` | T7A–E, T8A–F | loop/kernel/tensor/scaling sub-analyses (md only) |
| **Scalar-tensor** | `teic_st/` | ST1–ST6, ST11, T11–T12, T14 | Brans-Dicke f(θ)R coupling, cosmology, a₀(z), galaxies, Tully-Fisher, DEV comparison |
| **Non-pert.** | `teic_np/T13/` | T13A–H | force law, MOND search |
| **Vector audit** | `teic_vector_audit/` | T9, T10 | emergent gauge vector, collective modes |

## Tooling (key for the audit)

`TEIC-GE/src/causal_core.py` and `wilson_core.py` are **essentially identical** to the
TEIC project's `src/causal_core.py` and `results/bridge/wilson/wilson_core.py`
(same `sprinkle_box`, `area_bivector`, `causal_diamond_loops`, `link_phase`,
`loop_holonomy`, `F_from_A`, `F_sq`, same 8-pt Gauss–Legendre). **So Gemini did not
build independent tooling — it shares (a fork of) the TEIC generators.** This makes the
cross-check a *same-tooling reproduction*, not a fully independent one — a point that
must temper any "two independent agents agree" claim.

## First impressions (methodology, apparent rigor)

- **Anti-circularity, fundamental phase: clean.** T1/T3/T6 generators use only
  sprinkle + loops + a chosen probe field $A_\mu$ (scored against `F_from_A` in a
  comparison step). No DEV/MOND/a₀ in those generators.
- **Anti-circularity, ST/NP phases: NOT clean.** `teic_np/T13_solver.py` hand-codes the
  MOND interpolation `g=sqrt(gn·a0)`; `T13_numerical_experiment.py` inputs
  `rho(r)=rho0(1+2M/r)` (a Schwarzschild-like profile) and plots "1/r (MOND)";
  `teic_st/T11` reports the acceleration scale "in units of network-c/T" (assumes the
  scale). These phases reason *toward* MOND/a₀ rather than deriving them.
- **Reproducibility: partial.** Seeds are fixed (`default_rng(42)`, or seeds 0–4), which
  is good. But most results are **single-realisation** point estimates with **no error
  bars**, outputs are **prose `.md` only** (no `_data.json` dumps like TEIC's), and
  **some scripts are stubs**: `ST3_cosmology.py::analyze_boundary_curvature` is `pass`;
  `T11_scale_emergence.py::test_phase_a_dynamic` ends in `pass`. So part of the "many
  tests" are hand-written analyses, not executed computations.
- **Rigor gradient.** The fundamental phase is genuine numerics and matches TEIC (A2).
  The ST/NP phenomenology phases are lighter (truncations + assumptions + stubs).

## Index of Gemini's headline claims (to be tested A2–A6)

1. Maxwell $F^2$ emerges from Wilson loops, **Lorentz-violating** (E>B) — T1, T3.
2. **a₀ not derived**; only UV scales ∝ρ — T2 (fundamental).
3. Minimal action $\Rightarrow$ **Proca-Maxwell-DBI**, LV; **DEV = high-symmetry special
   case** — T3, T5.
4. **a₀ ~ c/T** (cosmological horizon) — ST3, T11, T14 (scalar-tensor phase).
5. **DEV does not emerge / TEIC-ST is phenomenologically inferior** (Keplerian curves,
   Tully-Fisher slope 0.5) — T12, T12H.
6. **BD smearing does not restore Lorentz** ("diff signs: NO") — T6.

→ A2 reproduces 1, 2, 3, 6; A4 critiques 3/5; A5 dissects 2 vs 4.
