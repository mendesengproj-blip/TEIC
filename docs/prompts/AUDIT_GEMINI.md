# AUDIT_GEMINI — Gemini CLI (TEIC-GE) findings vs TEIC results

> **Audit, not a new result.** Validates/refutes the conclusions of the Gemini CLI work
> in `../TEIC-GE` against the TEIC project's own results. Does **not** modify R1–R3 or
> e6–e11. Artefacts in [`results/audit/gemini_vs_teic/`](results/audit/gemini_vs_teic/).
> Golden rule obeyed: **reproduced before judging** — Gemini's scripts were re-run and
> compared to TEIC's stored JSON.

## The user's summary of Gemini, tested

| Claim (as summarised) | Audit verdict |
|---|---|
| "TEIC is an **independent** framework, not a derivation of DEV" | **Right in substance, wrong word.** Gemini's content = "DEV is the high-symmetry special case of a Proca–Maxwell–LV family TEIC generates" = TEIC's own C2/W4. Say "**microscopic origin**", not "independent" (which wrongly implies disconnected). |
| "**a₀ was derived**" | **False.** Gemini's *fundamental* phase (T2) says a₀ is **not** derived (only UV ∝ρ scales) — identical to TEIC C3. The "derivation" is in a *scalar-tensor* phase that **postulates** a₀∼c/T (with stub code and a poor 1/T fit). |
| "Many tests, very fast" | **Fast because lighter.** 19 `.py` / 66 `.md` but ~12 real computations, mostly **single-seed, no error bars, no data dumps, 2 stub scripts**. The fundamental numerics are complete and reproduce; the phenomenology is thin. |
| "Results may be wrong (simplification/error)" | **Fundamental phase: correct & reproduces.** The over-statements are in the phenomenology phase and, most of all, in the **verbal summary** ("a₀ derived"), not in Gemini's careful files. |

## What we found

**Gemini's tooling is a fork of TEIC's** (`causal_core.py`/`wilson_core.py` essentially
identical), so the cross-check is a *same-tooling reproduction*, not a fully independent
one (A1).

**Where Gemini did real fundamental numerics, it agrees with TEIC** (reproduced, A2):

| Quantity | Gemini | TEIC | |
|---|---|---|---|
| E/B Lorentz violation (4D) | 2.5–2.9 | **2.97** | ✅ agree |
| a₀ origin | UV ∝ρ, "no IR scale emerges" (T2) | UV ∝ρ, cH not derived (C3) | ✅ agree |
| Minimal action structure | Proca–Maxwell–DBI; DEV special case (T3/T5) | Stückelberg/Proca + Maxwell + DBI; DEV sister (C2/W4) | ✅ agree |
| BD restores Lorentz? | **NO** ("diff signs: NO", T6) | **NO** (BD5) | ✅ agree |
| M2 link anisotropy a_t/a_x (4D) | 7.6 (random pairs) | 3.4 (covering links) | ~ link-def difference |
| C₂/C₁=1, C₃/C₁=2 ratios | **not computed** | **exact** | Gemini gap |

**Anti-circularity** (A3): Gemini's **fundamental** phase is clean; its **teic_st /
teic_np** phases are **not** — `T13_solver.py` hand-codes the MOND law `g=√(g_N·a₀)`,
`T13_numerical_experiment.py` inputs `ρ(r)=ρ₀(1+2M/r)` ("1/r MOND"), and `T11` reports a₀
"in units of network-c/T" (assumes the scale).

**The a₀ "derivation" (A5)** is two mutually inconsistent statements: T2 (fundamental) =
"not derived, UV only"; ST3/T11/T14 = "a₀ **vinculada** to c/T" (postulated, stub code,
ST3 admits acceleration "não emerge naturalmente"). So **a₀ was not derived.**

**The "DEV inferior" claim (A4)** comes from a **scalar-tensor Brans–Dicke truncation**
(ST2: f(θ)R) that **drops the vector/Wilson sector** — the very sector TEIC's bridge
shows carries the gravitational modification. True for that truncation; over-generalised
to all of TEIC.

## Bottom line

> **Gemini found nothing TEIC had not already found, and got its honest fundamental
> phase right — it independently (same-tooling) corroborates TEIC's Maxwell-LV, UV-a₀,
> Proca/DBI, and "BD does not restore Lorentz" results.** The errors are in the
> *summary*: a₀ was **not** derived (it is postulated as cH in a lighter, partly stubbed,
> partly circular scalar-tensor phase), and "independent" should read "microscopic
> origin." Recommendation: **use partially** — accept the fundamental phase, reject "a₀
> derived," scope-limit "DEV inferior" to the scalar-only truncation.

Reassuringly, the one place Gemini and TEIC most strongly agree is the **hardest negative
result**: BD smearing does **not** restore Lorentz invariance at accessible scales —
found independently by both.

## Documents

| file | content |
|---|---|
| [`A1_inventory.md`](results/audit/gemini_vs_teic/A1_inventory.md) | full file list, phases, tooling, first impressions |
| [`A2_reproduction.md`](results/audit/gemini_vs_teic/A2_reproduction.md) | the 3 critical tests reproduced, side by side |
| [`A3_methodology.md`](results/audit/gemini_vs_teic/A3_methodology.md) | anti-circularity, test count, honesty, reproducibility |
| [`A4_conclusion_critique.md`](results/audit/gemini_vs_teic/A4_conclusion_critique.md) | the 3 readings of "independent"; which is right |
| [`A5_a0_reconstruction.md`](results/audit/gemini_vs_teic/A5_a0_reconstruction.md) | Gemini's a₀ algorithm reconstructed; postulate, not derivation |
| [`A6_synthesis.md`](results/audit/gemini_vs_teic/A6_synthesis.md) | scorecard; right/wrong; use-partially recommendation |

Reproduce the cross-check: `python results/audit/gemini_vs_teic/A2_reproduce.py`
(re-runs Gemini's T3; reads TEIC's C1/W2 JSON). Gemini's fundamental scripts re-run from
`../TEIC-GE/results/teic_fundamental/` (`T1`,`T2`,`T3`,`T6`).
