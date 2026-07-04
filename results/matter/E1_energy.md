# E1 — energy as causal counting (refaz T18/T19)

**Verdict: D** — `E = m·γ` is recovered to <0.5 %, but it is a *reinterpretation* of
R1, not an independent derivation of energy.

## Question
T18/T19 fit a hand-translated Gaussian blob to `e^{−0.52v²}` (not `1/γ`) with the fit
depending on the arbitrary blob width. The correct route uses the proper time τ
**already derived by R1** from causal counting. (The prompt's `E = m·dτ/dt` is a
typo: `dτ/dt = √(1−β²) < 1` *decreases* with β, while energy increases; the
relativistic energy is `E = m·dt/dτ = m·γ`.)

## Method
A clock moves at velocity β for coordinate time T=9 (ρ=10, 20 seeds, 6 β values). Its
proper time τ(β) is measured from the Alexandrov interval by (i) longest causal chain
and (ii) volume estimator `(2N/ρ)^{1/2}`. Then `γ_measured = τ(0)/τ(β)` and
`E_rede = m·γ_measured` (m = 1 unit). Compared to `γ = 1/√(1−β²)` (validation.py,
COMPARISON ONLY).

## Results

| β | E_chain | E_vol | m·γ (SR) |
|---|---|---|---|
| 0.00 | 1.000 | 1.000 | 1.000 |
| 0.20 | 1.039 | 1.022 | 1.021 |
| 0.40 | 1.096 | 1.097 | 1.091 |
| 0.60 | 1.250 | 1.247 | 1.250 |
| 0.75 | 1.501 | 1.507 | 1.512 |
| 0.85 | 1.892 | 1.877 | 1.898 |

Mean relative deviation: **chain 0.5 %, volume 0.4 %**; `E_rede` grows with β. ✓

## What it means
`E_rede = m·γ` is recovered cleanly — but **γ is purely R1's causal counting**, and
`E = m·γ` only multiplies it by a rest scale `m` that M1 could **not** pin down as a
real inertia. So energy emerges as a *consequence of R1 + an assumed m*, not as an
independent result. Additivity `E_tot = E₁ + E₂` for non-interacting clocks holds by
construction (the count of a disjoint union is the sum). Hence **grade D**
(reinterpretation), honestly — the same status the audit assigned to "time =
R1–R3" when it was re-dressed.
