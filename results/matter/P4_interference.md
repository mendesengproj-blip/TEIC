# P4 — superposition / interference of states (novo)

**Verdict: C** — classical superposition, not quantum interference. Consistent with
e11.

## Question
For localized states, is the combination **quantum** interference (a `|ψ|²` Born-rule
pattern from a complex amplitude) or just **classical** superposition of real fields?

## Method (ρ=18, T=8, X=14, σ=1.6, sep=6, 20 seeds)
Source two localized lumps, propagate each (θ₁, θ₂) and the combined source on the
same network via the retarded kernel. Measure: (i) the linearity residual
`max|θ_same−(θ₁+θ₂)| / max|θ_same|`; (ii) the total-intensity ratio
`E_opp/E_same = Σθ_opp² / Σθ_same²` (opposite- vs same-sign sources).

## Results
- Linearity residual = **1.1×10⁻¹⁵** (machine precision) → exact superposition.
- Total-intensity ratio **E_opp/E_same = 0.279 ± 0.005** → real fields cancel where
  the cones overlap.

## What it means
The dynamics is **linear**, so states add exactly: `θ₁₂ = θ₁ + θ₂`. Opposite-sign
sources cancel (down to 28 % energy) — but this is **Young's classical interference of
real fields**, not quantum mechanics. There is **no complex amplitude and no `|ψ|²`
Born rule** (the anti-circularity guard forbids complex numbers in the generator, and
none was needed: we are *showing* the field is classical, not postulating a quantum
one). The TEIC↔QM boundary is exactly where **e11** left it: the network supplies
real-wave interference and the alternating-sign ingredient (e10), but the complex
amplitude / Born rule remain absent.
