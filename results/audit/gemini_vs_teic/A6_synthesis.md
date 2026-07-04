# A6 — Synthesis: what Gemini got right and wrong

## Checklist

```
Gemini's method:
  [~] Rigorous methodology         -- fundamental phase YES (numeric, anti-circular);
                                      ST/NP phases NO (single-seed, stubs, MOND assumed)
  [~] Anti-circularity maintained  -- fundamental PASS; teic_st/teic_np FAIL (a0/MOND inserted)
  [x] Honest open bottlenecks      -- fundamental YES (a0, Lorentz admitted open);
                                      but ST phase overstates a0~c/T and "DEV inferior"
  [~] Reproducible                 -- seeds fixed & re-ran OK; but prose-only, no json,
                                      single-seed, 2 stub scripts

Gemini's conclusions:
  [~] "TEIC is independent"        -- substance CORRECT (DEV = special case of a TEIC
                                      EFT family); WORD wrong ("independent" -> "origin of")
  [x] "a0 was derived"             -- FALSE; fundamental phase says not derived (=TEIC C3);
                                      ST phase POSTULATES a0~c/T (stub code, poor 1/T fit)
  [x] a0 derivation valid          -- it is an identification a0=cH, not a derivation

Speed:
  [x] Many tests == less care      -- partly: 66 md from ~12 real computations, single-seed,
                                      2 stubs. Fast because lighter, not because better.
  [ ] Outputs incomplete           -- 2 stub scripts (ST3, T11) + no data dumps; but the
                                      fundamental numerics are complete and reproduce.
```

## What Gemini got RIGHT (accept)

1. **Maxwell from Wilson loops, Lorentz-violating (E/B≈2.5–2.9).** Reproduced; matches
   TEIC W2 (2.97).
2. **a₀ is not a derived IR scale; only UV $\rho$ scales exist.** T2 = TEIC C3. Honest.
3. **Minimal action ⇒ Proca + Maxwell + DBI; DEV is the high-symmetry special case.**
   T3/T5 = TEIC C2/W4 (gauge-invariant Stückelberg/Proca "sister theory").
4. **BD smearing does not restore Lorentz** (T6 "diff signs: NO") = TEIC BD5. Independent
   (same-tooling) confirmation of the project's hardest negative result.
5. **Lorentz covariance is the central open problem.** = TEIC's standing verdict.

On the genuinely fundamental questions, **Gemini and TEIC agree** — a meaningful
cross-check (tempered by shared tooling, A1).

## What Gemini got WRONG / overstated (reject or scope-limit)

1. **"a₀ derived."** Not derived — postulated as $cH$ in the scalar-tensor phase, with
   stub code and a poor $1/T$ fit; the fundamental phase itself denies it (A5). *This is
   the user's-summary claim that the audit most firmly refutes.*
2. **"TEIC independent."** Misleading word; substance is "DEV = special case of a
   TEIC-generated family" (A4). Restate as "microscopic origin," not "independent."
3. **"DEV phenomenologically inferior / does not emerge."** Scope error: derived from a
   **scalar-tensor truncation that drops the vector sector**, then over-generalised. Not
   a verdict on full TEIC (A4).
4. **Methodological lightness:** single-seed, no error bars, no data dumps, 2 stub
   scripts, MOND/a₀ inserted in the phenomenology generators. Fast = lighter, not better.

## Final recommendation: **USE PARTIALLY**

- **Accept** the fundamental phase (T1–T6): it is correct, anti-circular, reproducible,
  and independently corroborates TEIC's Maxwell-LV, UV-a₀, Proca/DBI, and BD-fails-
  Lorentz results.
- **Reject** the headline "a₀ derived" (it is postulated) and the bare word "independent"
  (use "fundamental origin").
- **Scope-limit** the "DEV inferior" claim to the scalar-tensor truncation; it does not
  bear on the full vector-inclusive bridge.
- **Net:** Gemini found *nothing TEIC did not already find*, and where it appears to
  ("a₀ derived") it is an over-statement of a postulate. No new validated result; one
  useful independent corroboration (BD/Lorentz); several scope/lexical errors to correct.

The golden rule held: we reproduced before judging, and the data — not the speed —
decided. Gemini was fast because it was lighter, not because it was wrong on the core;
its *conclusions as summarised to the user* are where the errors are, not in its sound
fundamental numerics.
