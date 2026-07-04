# NL1 — Is the non-linear coefficient λ geometric or free? (analytic)

> **Bridge / non-linear investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing. Continues [`BRIDGE_DYNAMICS.md`](../../../BRIDGE_DYNAMICS.md) (D1–D3
> closed the bridge at first order, `θ = GM/rc²`). Reproduce:
> `python results/bridge/nonlinear/NL1_action.py` (~3 s). Data:
> [`NL1_action_data.json`](NL1_action_data.json).

**Anti-circularity.** All Schwarzschild content (the series `1/√(1−2u)`, the
coefficients) is *comparison-only* reasoning; the derivation content is the BD
action's structure and the radial Green's function. No `√(1−2M/r)` generates
anything.

---

## Two corrections to the premise (both verified symbolically)

**(A) The target coefficient is +3/2, not +1/2.** The bridge density is

$$\frac{\rho_{\rm eff}}{\rho_0} = \frac{1}{\sqrt{1-2u}} = 1 + u + \tfrac{3}{2}u^2 + \tfrac{5}{2}u^3 + \dots,\qquad u=\frac{GM}{rc^2}.$$

Its quadratic coefficient is **+3/2**. The "½" in the prompt is the coefficient of
the **redshift** `√(1−2u) = 1 − u − ½u²` — the *reciprocal* quantity (`dτ/dt`), not
the density. D3 measured the density, so the correct second-order target is
**A₂/A₁² = 3/2**. We use 3/2 throughout NL2/NL3.

**(B) `λθ²` gives a logarithm, not `1/r²`.** With the linear point-mass field
`θ₁ = M/r`, candidate non-linear sources of `∇²θ = (source) + (non-linear term)`
give:

| non-linear term | `θ₂` (from `∇²θ₂ = term`) | clean `1/r²`? |
|---|---|---|
| `λ θ²` (prompt) | `C₁ + C₂/r + λM²·ln r` | ❌ logarithm |
| `λ (∇θ)²` | `C₁ + C₂/r + λM²/(2r²)` | ✅ `1/r²` |

So the prompt's `λθ²` cannot produce the quadratic term; the **gradient
self-coupling** `λ(∇θ)²` does, with `1/r²` coefficient `λ/2`. Matching +3/2
requires **λ = 3**.

---

## The decisive question: does the BD action fix λ?

The smeared Benincasa–Dowker action is **quadratic** in the field,

$$S_{BD,\rm smeared} = \sum_{x} (B_\varepsilon\phi)(x)\,\phi(x)\,V_x,$$

because the smeared Sorkin operator `B_ε` is **linear** (D1). Its variation gives
the linear equation `B_ε φ = J → □θ = 4πG T/c⁴`. There is **no** `φ³` term (prompt's
`λΣφ³V`) and **no** `(∇θ)²` term in `S_BD`. Adding either imports a coupling the
action does not contain.

$$\boxed{\;\lambda \text{ is a } \textbf{free parameter}\text{ at the level of the BD action.}\;}$$

The value `λ = 3` that reproduces Schwarzschild's +3/2 is **imposed to match**, not
derived. The only place a *geometric* non-linearity hides in BD is the curved-space
limit `⟨Bφ⟩ → □φ − ½Rφ`: the `−½Rφ` curvature coupling, with `R` sourced by the
field's own energy, **is** a genuine geometric non-linearity — but extracting its
coefficient needs the full non-linear map `R[θ]` (the causal-set Einstein / Regge
sector), which is **not** contained in the quadratic action as used. That is the
open frontier (documented below; not attempted — and *not* the horizon).

---

## Verdict — NL1: **λ LIVRE (não geométrico)**

| check | result |
|---|---|
| correct density 2nd-order coefficient | **+3/2** (prompt's ½ is the redshift's) |
| `λθ²` produces clean `1/r²` | ❌ (gives `ln r`) |
| `λ(∇θ)²` produces `1/r²`, matches 3/2 at | `λ = 3` |
| BD action contains such a term | ❌ — it is quadratic |
| **λ fixed by the BD action?** | **NO — free** |

**NL1's death criterion is met: λ is free, so the non-linearity is not derived from
the Benincasa–Dowker action.** Reproducing Schwarzschild's second order dynamically
would require physics beyond BD — the curvature back-reaction `−½Rφ` (the Regge /
causal-set Einstein sector), the open frontier.

**This does not stop the investigation.** Per the prompt, NL2/NL3 proceed: their
evidence is numerical and independent of NL1. And — anticipating them — the second
order is reproduced **kinematically** (through the proper-time clock `√`, the same
mechanism as P2/P3) rather than dynamically. NL1 tells us *why* there is no
dynamical derivation; NL2/NL3 show the kinematic convergence is nonetheless real and
has the correct coefficient (3/2).
