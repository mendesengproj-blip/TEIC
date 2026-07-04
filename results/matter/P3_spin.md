# P3 — spin test: 2π vs 4π (refaz T21BIS)

**Verdict: C** — no spin-½ (as expected). A real scalar carries only integer angular
structure; a 2π rotation returns it to +itself.

## Question
The decisive spin test, which T21BIS never ran: under a full **2π** rotation a spin-½
state → **−itself** and only a **4π** rotation → +itself; an integer-spin/scalar state
→ +itself already at 2π.

## Method (2+1D Poisson network, ρ=6, T=6, X=8, σ=3, 20 seeds)
Rotation needs ≥2 spatial dimensions. On the 2+1D network we build a real field with
the only directional structure a scalar admits, `θ = exp(−r²/2σ²)·cos(m·φ)` (angular
number m=1, 2), rotate the spatial plane by α∈[0,4π], and measure the normalized
overlap `O(α)=⟨θ, R_α θ⟩/⟨θ,θ⟩`.

## Results

| m | O(2π) | O(4π) |
|---|---|---|
| 1 | **+1.000 ± 0.000** | +1.000 ± 0.000 |
| 2 | **+1.000 ± 0.000** | +1.000 ± 0.000 |

## What it means
A 2π rotation returns the field to **+itself** for every integer m (`O(α)=cos(mα)`);
there is no 4π double cover. A half-integer m — which would give `O(2π)=−1` — is **not
a single-valued function on the plane** and would require a spinor field (the double
cover of SO(2)), which the scalar θ does not have. **Spin-½ cannot emerge from a
scalar θ**; it needs internal spinor/vector structure absent from this sector. Exactly
as anticipated.
