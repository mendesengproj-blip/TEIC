# AB2 — Re-audit of W1–W4 (Wilson loops)

**Task.** Re-run the WILSON generators (imported unchanged) and stress each claim with
the specific test the audit asks for. `AB2_wilson.py`, data in `AB2_wilson_data.json`.

## W1 — holonomy → F beyond constant fields

The original reported `rel_err ~ 1e-12` for constant fields. The audit pushes harder:

**(a) Strong constant F** — W/area must equal F0 at *any* strength (the holonomy of a
linear A is exact):

| F0 | W/area | rel_err |
|---|---|---|
| 0.1 | 0.100000 | 2.8×10⁻¹⁶ |
| 1.0 | 1.000000 | 4.4×10⁻¹⁶ |
| 10 | 10.000000 | 1.8×10⁻¹⁶ |
| 100 | 100.000000 | 5.7×10⁻¹⁶ |

Exact to machine precision at every strength — no breakdown at strong field.

**(b) Non-constant F** (`F_tx = k·cos kx`, curvature set by k) — the error must be the
O(area) Stokes-curvature error, i.e. fall as `h²`:

| k | log-log slope of rel_err vs loop size h | rel_err (smallest loop) |
|---|---|---|
| 0.5 | **2.00** | 1.3×10⁻⁵ |
| 1.0 | **2.00** | 5.2×10⁻⁵ |
| 2.0 | **1.99** | 2.1×10⁻⁴ |

**Confirmed:** the error is exactly second order in loop size (vanishes as area→0); a
larger field curvature k raises the coefficient but not the power. W1 is robust beyond
the constant-field regime.

## W2 — E/B ≈ 3 in 3+1D, with 20 seeds

| Quantity (3+1D, 20 seeds) | Value |
|---|---|
| **E/B anisotropy** | **3.25 ± 0.10** |
| off-Maxwell cross ⟨Ω₀₁Ω₂₃⟩ | +1.1×10⁻² ± 8.9×10⁻³ (consistent with 0 — parity) |

**Confirmed: E/B ≈ 3 in genuine 3+1D over 20 seeds** (the value the Gemini cross-check
also found), a real order-1 Lorentz violation in the raw vector sector. The cross term is
consistent with zero, so no parity (θ-term) violation. **Is E/B the same in 3+1D as in
2D? The question is ill-posed:** E/B is a *3+1D-only* quantity — 1+1D has a single (t,x)
plane and **no magnetic plane**, so there is no B to form the ratio. This is why W2's
anisotropy test lives in 4D and the 1+1D run only measures the link `a_t/a_x`.

## W3 — strong field: saturate or explode?

`1−cos ∈ [0,2]`, so the action has a **hard ceiling** of `2·n·⟨Δτ⟩`; nothing can diverge.
Pushed to amplitude 50 over 20 seeds:

| Channel | S/(n⟨Δτ⟩) at max amp | interpretation |
|---|---|---|
| scalar (link) | **1.000 ± 0.010** | random-phase plateau ⟨1−cos⟩→1 |
| plaquette | 0.92 ± 0.02 | saturating toward its own ceiling |

Maximum observed fraction over all seeds = 1.03, **well below the hard ceiling of 2**.
**Confirmed: the action saturates (random-phase plateau), it does not explode** — the
bounded cosine guarantees it. (The plateau sits at ⟨1−cos⟩=1, not at the absolute
ceiling 2, because at strong field the phases are effectively uniform.)

## W4 — do any *forbidden* operators emerge?

The claim is that all five DEV operators emerge. The audit's extra question: does any
*forbidden* higher-derivative operator (`∂⁴θ`, or an anisotropic Hořava-Lifshitz
`∂_t²∂_x²`, z=2) emerge too? Symbolic check of `1−cos u`, `u = (A_μ+∂_μθ)e^μ`:

| order | # monomials | first-derivative covectors only? | contains 2nd+ derivative? |
|---|---|---|---|
| u² | 3 | yes | **no** |
| u⁴ | 8 | yes | **no** |
| u⁶ | 15 | yes | **no** |

**Confirmed: no forbidden operator can appear.** The link action contains only *first
differences* (`Δθ` over a link, `F=∂A` around a plaquette); coarse-graining replaces
products of the link vector `e^μ` by **constant** Poisson moments, which cannot raise the
derivative order. Every emergent operator is a polynomial in the first-derivative fields
`(A, ∂θ, F)` — exactly the DEV set, never a `∂⁴θ` or Hořava-Lifshitz term.

## Verdict (AB2)

All four Wilson claims survive:
- **W1:** holonomy → F is exact for strong constant F and O(h²) for varying F.
- **W2:** E/B = 3.25 ± 0.10 in 3+1D (order-1 LV, a real prediction; 4D-only).
- **W3:** bounded cosine ⇒ saturation, no explosion.
- **W4:** only first-derivative operators emerge — no forbidden higher-derivative term.
