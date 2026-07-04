# AB4 — Anti-circularity of the whole `results/bridge/` tree (priority gate)

**Task.** Before re-auditing any number, confirm no bridge result is circular. The
repository guard `tests/test_no_circularity.py` scans `src/`, `experiments/` and
`results/matter/` — it does **not** scan `results/bridge/`. AB4 closes that gap
*without modifying the guard or any campaign*: `AB4_circularity.py` imports the guard's
own primitives (`FORBIDDEN`, `COMPLEX_FORBIDDEN`, `_comparison_block_lines`,
`_code_only`) so the rules are byte-for-byte the ones enforced elsewhere, and re-runs
them over the 28 `.py` files under `results/bridge/`.

## Result

| Check | Finding |
|---|---|
| (1) Dilation literal (`sqrt(1-2M/r)`, `1/sqrt(1-β²)`, `gamma=1/sqrt…`) — forbidden **everywhere** | **0** in any bridge file |
| (2) Complex literal (`1j`, `complex()`, `cmath`) in a generator (outside COMPARISON) | **0** |
| (3) DEV parameter / dataset (`a_0`, `SPARC`, `BTFR`, `RAR`, `MOND`, `cH0`) in live code | **0** outside a COMPARISON block |
| (4) Schwarzschild references | 19 resolve to an **allowed source**; 0 circular; 2 symbolic comparison targets |

**Verdict: CLEAN.** No dilation formula, no complex literal, and no DEV parameter or
empirical dataset feeds any bridge generator.

## Why the Schwarzschild references are not circular

The bare word "schwarzschild" appears as an identifier 21 times. Each was classified:

- **19 are `schwarzschild_redshift`, imported from `src/validation.py`** — the single
  file the guard designates as ALLOWED to hold the dilation formula `sqrt(1-2M/r)`.
  Every importing file tags it `# (COMPARISON ONLY)` and uses it only to *score* the
  network output (e.g. `P2_numeric.py:95` `gr_rate = schwarzschild_redshift(...)`
  followed by the explicit note "*comparison only (never fed back into a generator)*").
  The generators in those files sprinkle in the **background metric** via
  `sprinkle_schwarzschild` / `rstar_of_r` (from `src/curved.py`), which the guard's own
  docstring explicitly permits: "*the metric / volume element itself … WITHOUT a square
  root … is ALLOWED in generator code (it is background geometry, not a dilation applied
  to an estimator)*." The proper-time ratio is **counted** from the sprinkling and only
  then compared to `validation.py`'s formula — the correct, non-circular direction.

- **2 are in `NL1_action.py`** (`schwarzschild_coeffs()`), which computes the Taylor
  series of `(1-2u)^{±1/2}` **symbolically in sympy**. `NL1_action.py` imports **no data
  generator at all** (it is a pure symbolic exercise asking which non-linear source term
  reproduces the +3/2 density coefficient). A reference that no generator consumes cannot
  be circular. It is recorded as an advisory only.

## Advisories (convention, **not** circularity) — **all addressed**

All three advisories this audit surfaced were fixed in the same commit (none affected any
result):

1. **`C2_ratios.py` and `C4_completeness.py`** opened a `# COMPARISON ONLY` block closed by
   a dashed rule instead of the canonical sentinel. **Fixed:** a `# END COMPARISON ONLY`
   line now closes each block after the DEV comparison material.

2. **`NL1_action.py`** computed the Schwarzschild Taylor series inline. **Fixed:** the
   `schwarzschild_coeffs()` function is now wrapped in a `# COMPARISON ONLY … # END
   COMPARISON ONLY` block (the only residual identifier is the call site in `main()`, which
   merely invokes the wrapped comparison function in a generator-free file).

3. **`results/bridge/` was not in the guard's `SCAN_DIRS`.** **Fixed:** with (1)–(2)
   resolved, `ROOT / "results" / "bridge"` is now added to `tests/test_no_circularity.py`'s
   `SCAN_DIRS`, and the canonical guard passes verbatim over the whole bridge tree. This
   audit is now redundant with the standing guard — kept as the documented one-time sweep.

## Output
`AB4_circularity.py`, `AB4_circularity_data.json`. Reproduce with
`python results/audit/bridge_recheck/AB4_circularity.py`.
