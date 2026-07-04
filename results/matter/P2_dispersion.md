# P2 — dispersion relation (refaz T21)

**Verdict: C** — dispersion not resolved (honest negative). The k²-signal is buried
under the Benincasa–Dowker variance; no mass can be read off.

## Question
Measure the eigenvalue of the causal `□` operator on plane waves and read the
dispersion. For `□ = ∂ₜ²−∂ₓ²`: `□cos(kx)=+k²cos(kx)` and `□cos(ωt)=−ω²cos(ωt)`. A
massive (Klein–Gordon) field adds a constant: `λ_space = k² + m²`. So a nonzero
intercept of `λ_space` vs `k²` would be an effective mass². We measure it; we do not
insert it.

## Method (ρ=20, T=10, X=18, ε=0.2, 20 seeds)
Apply the smeared Sorkin operator `B_ε` to `cos(kx)` and `cos(kt)` and estimate the
eigenvalue by regression `λ = ⟨Bφ·φ⟩/⟨φ·φ⟩` over interior events; fit `λ_space` vs k².

## Results (mean ± SEM)

| k | λ_space (want >0) | λ_time (want <0) |
|---|---|---|
| 0.30 | −0.042 ± 0.062 | +0.040 ± 0.131 |
| 0.45 | −0.099 ± 0.054 | −0.025 ± 0.053 |
| 0.60 | −0.072 ± 0.062 | +0.018 ± 0.060 |
| 0.80 | −0.039 ± 0.085 | +0.200 ± 0.071 |
| 1.00 | −0.071 ± 0.067 | +0.174 ± 0.041 |

- Fit `λ_space = 0.004·k² − 0.067` → **slope ≈ 0**, intercept = the const-annihilation
  discreteness bias.
- Effective **m² = −0.067 ± 0.060** — formally consistent with 0, but uninformative.

## What it means
The signs do **not** separate (`λ_space` even comes out slightly negative): the
k²-dependent signal does not emerge above the discreteness bias (the same
`const`-annihilation offset e10 documents) and the BD `ρ^{3/4}` variance. This
**reproduces e10's known difficulty** — Benincasa–Dowker validate via the *summed
action*, not pointwise `⟨Bφ⟩`. So `ω²=k²` is **neither confirmed nor refuted** here,
and no positive mass² appears but none could be resolved either. A clean dispersion
would need the summed-action route or much larger networks (future work).
