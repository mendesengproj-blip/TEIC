# A3 — Methodology and honesty

## 1. Anti-circularity checklist

| Phase | DEV/MOND/a₀ in the generator? | Verdict |
|---|---|---|
| `teic_fundamental` (T1–T8) | No — sprinkle + loops + probe field only | **PASS** |
| `teic_gauge` (T7/T8 sub) | No (md analyses of fundamental) | PASS |
| `teic_st` (ST/T11/T12/T14) | **Yes** — T11 reports a₀ "in units of network-c/T" (assumes scale); T12 reasons toward MOND | **FAIL (a₀ assumed)** |
| `teic_np/T13` | **Yes** — `T13_solver.py` hand-codes `g=sqrt(gn·a0)` MOND law; `T13_numerical_experiment.py` inputs `rho(r)=rho0(1+2M/r)` and labels "1/r (MOND)" | **FAIL (MOND inserted)** |

So Gemini's **fundamental** results are anti-circular (its T4 self-assessment is
justified); its **phenomenology** phases are **not** — they import the MOND
interpolation / the Schwarzschild density / the c/T scale they then "find". The grep is
in the audit log; the offending lines are `T13_solver.py:38,61`, `T13_numerical_*.py:17,81`,
`T11_scale_emergence.py:89`.

## 2. Test count and depth (vs TEIC's ~40)

- **Gemini:** 19 `.py` scripts, 66 `.md` reports. But the `.md` count is inflated —
  e.g. T7A–E, T8A–F, T9A–G, T10A–F, T13A–H, T14A–G are *many short sub-reports of a few
  computations*. Net **executed** computations ≈ a dozen (and 2 of those are stubs:
  `ST3_cosmology`, `T11 test_phase_a_dynamic`).
- **TEIC:** ~40 numbered tests (R1–R3, e6–e11, D1–D3, NL1–3, P1–3, C1–4, W1–4, BD1–5),
  each with a generator `.py` + a `_data.json` + multi-seed averaging + a `.md`.
- **Quality, not just count:** TEIC results carry error bars (averaging over
  realisations); most Gemini results are **single-seed point estimates with no
  uncertainty**. That is the main reason Gemini is "fast" — fewer realisations, no
  variance quantification, prose instead of data dumps. Not illegitimate, but **lighter**.

## 3. Honesty about open bottlenecks

Gemini is, to its credit, **honest in the fundamental phase**:
- T2: "a₀ **não foi derivada**… nenhuma escala IR emerge naturalmente."
- T6: BD layering "Minkowski check (diff signs): **NO**" — admits Lorentz not restored.
- EXECUTIVE_SUMMARY: "o gargalo fundamental restante é a **Recuperação da Covariância de
  Lorentz**."

These match TEIC's own three open bottlenecks (Lorentz, a₀ scale, derived $d$). **The
honest core of Gemini agrees with TEIC's honest core.** The over-statement lives only in
the scalar-tensor phase (a₀~c/T presented as a result, "DEV inferior" generalised from a
truncation) and, most of all, in the **user's verbal summary** ("a₀ foi derivado"),
which is not what Gemini's careful files say.

## 4. Reproducibility

| criterion | Gemini | TEIC |
|---|---|---|
| fixed seeds | ✅ (42 / 0–4) | ✅ |
| outputs saved | ⚠️ prose `.md`, **no `.json`** | ✅ `.json` per test |
| multi-realisation error bars | ⚠️ mostly single-seed | ✅ |
| stubs / dead code | ⚠️ 2 stubs (`pass`) | none |
| re-runnable | ✅ (we re-ran T1/T2/T3/T6) | ✅ |

**Verdict:** Gemini's fundamental phase is reproducible and was reproduced (A2);
it is anti-circular and honest. The phenomenology phases are lighter, partly circular
(a₀/MOND assumed), partly stubbed, and single-seed.
