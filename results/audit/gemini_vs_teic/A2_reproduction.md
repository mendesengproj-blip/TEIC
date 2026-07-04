# A2 — Reproduction of the three critical tests

Golden rule obeyed: **reproduce before judging.** Gemini's fundamental-phase scripts
were re-run (`A2_reproduce.py` re-runs its T3 verbatim; T1/T2/T6 run from
`TEIC-GE/results/teic_fundamental/`). Numbers placed beside TEIC's stored results.

## Test 1 — Does the minimal action produce the DEV structure / the (1,2) ratios?

**Gemini (T3).** Computes the Δτ-weighted moments $M2,M4$ (over **random causal
pairs**) and $L2=\langle\Omega\Omega\rangle$ (Maxwell). Reproduced (seed 42):

| | Gemini T3 | TEIC (C1/C2/W2) |
|---|---|---|
| M2 anisotropy $a_t/a_x$ (2D) | 5.08 | 1.03 |
| M2 anisotropy $a_t/a_x$ (4D) | 7.57 | 3.38 |
| E/B (4D, from $L2$) | 2.48–2.85 | **2.97** |
| coefficient ratios $C_2/C_1,\,C_3/C_1$ | **not computed** | **1, 2 (exact)** |

- **E/B agrees** (2.5–2.9 vs 2.97) — same loop tooling, same Lorentz-violating result.
- **M2 anisotropy differs in magnitude** (7.6 vs 3.4 in 4D) because Gemini uses *random
  causal pairs* while TEIC uses *covering-relation links*; random pairs are more time-
  elongated, so a larger $a_t/a_x$. **Qualitatively identical** (both $>1$, positive-
  definite, Euclidean/LV); the difference is a documented link-definition choice, not a
  contradiction.
- **Gap:** Gemini **never extracts the $C_2/C_1=1$, $C_3/C_1=2$ ratios** — the decisive
  structural prediction. It infers "Proca" from the *form* (the $(A+\partial\theta)$
  combination) but does not verify the locked ratios numerically. TEIC's C2 does (they
  are an algebraic consequence of the single-cosine perfect square). **Methodological
  gap, not an error.**

**Verdict T1:** consistent where measured (E/B); Gemini did not test the (1,2) ratios.

## Test 2 — Is TEIC independent or derived?

Both agree on the *content*: the minimal action yields **Proca + Maxwell + DBI**, and
**DEV is the high-symmetry (Lorentz-invariant, massless) special case** (Gemini T3/T5;
TEIC C2/W4 "gauge-invariant Stückelberg/Proca special case = sister theory"). This is
**not** "disconnected" — it is "TEIC is more fundamental; DEV is a special point." See
A4 for the three readings of Gemini's word "independente". **No contradiction with
TEIC.**

## Test 3 — Was a₀ derived?

**Gemini's own fundamental phase says NO.** T2 reproduced: the boundary bias does **not**
scale as $1/T$ ($B_{\rm end}\cdot T$ = 3.6, 7.4, 55, 46 — not constant), and T2
concludes *"C) Nenhuma escala IR emerge naturalmente… apenas o comprimento de
discreteness $\rho^{-1/d}$"*, with $X_0\propto\rho$ (UV). **This is exactly TEIC's C3**
($X_0\propto\rho$, UV, $a_0\sim cH$ not supported).

The "a₀ derived" the user heard comes from the **scalar-tensor phase** (ST3/T11/T14),
where $a_0\sim c/T$ is **identified/postulated** ("a escala $a_0$ é *vinculada* ao
horizonte IR"), not derived — and the supporting code is partly **stubbed** (T11
`test_phase_a_dynamic`=`pass`; ST3 `analyze_boundary_curvature`=`pass`) with a poor
$1/T$ fit. So **a₀ was NOT derived** by Gemini; one phase explicitly says so, the other
postulates it. Detail in A5.

**Verdict T3:** a₀ not derived (Gemini-fundamental = TEIC-C3); the c/T claim is a
postulate from a truncated phase.

## Bottom line (A2)

Where Gemini did real fundamental numerics, **it reproduces and agrees with TEIC**
(E/B≈3 LV, a₀ UV not IR, Proca/Maxwell/DBI, BD fails to restore Lorentz — see A3/T6).
The divergences are (i) a link-definition magnitude difference, (ii) an untested (1,2)
ratio, and (iii) a postulated (not derived) c/T scale in the lighter scalar-tensor
phase.

Reproduce: `python results/audit/gemini_vs_teic/A2_reproduce.py`
(`A2_reproduce_data.json`).
