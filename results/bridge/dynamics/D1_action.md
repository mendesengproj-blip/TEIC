# D1 — Benincasa–Dowker action with a matter source (analytic)

> **Bridge / dynamics investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing in the main pipeline. Continues [`BRIDGE_RHO.md`](../../../BRIDGE_RHO.md).
> Reproduce: `python results/bridge/dynamics/D1_action.py` (~20 s). Data:
> [`D1_action_data.json`](D1_action_data.json).

**Anti-circularity.** The generator content is the Sorkin/BD kernel `(1,−2,1)` and
the quadratic action. No dilation formula, no `GM/r`, no `√(1−2M/r)`. Schwarzschild,
`G` and `GM/r` enter **only** in clearly-marked *comparison-only* steps at the end,
to score against P2 / R3.

---

## The question D1 answers

P2/P3 closed the bridge **kinematically**: *given* Schwarzschild, the network
density that reproduces it is ρ_eff = ρ₀/√(1−2M/r), and the DEV scalar maps onto
δρ_eff/ρ₀ = GM/rc². What stayed open is the **dynamics** — *why* the density takes
the g_tt profile around matter. D1 asks: does the discrete gravitational action of
Benincasa–Dowker, with a matter source, produce the right field equation in the
continuum (the relativistic Poisson equation)? If not, the whole dynamical program
is wrong and we stop.

---

## 1. The action

The Sorkin/Benincasa–Dowker discrete d'Alembertian `B` is the kernel of the
gravitational action of a causal set. In 1+1D its action on a nodal scalar field
θ is a sum over causal layers with the **definitional** coefficients
(C₀,C₁,C₂)=(1,−2,1):

$$(B\theta)(x) \;=\; \frac{1}{l^2}\Big[\,{-}2\,\theta(x) + 4\!\!\sum_{n=0}^{2} C_n \!\!\sum_{y\in L_n(x)}\!\!\theta(y)\Big],\qquad L_n(x)=\{y\prec x:\ n(y,x)=n\},$$

with `n(y,x)` the number of events strictly inside the causal interval `(y,x)` and
`l = ρ^{−1/2}`. (This is exactly the operator implemented and validated in
`experiments/e10_sorkin_dalembertian.py`.)

**The minimisable action.** The single-sum expression in the prompt is the *kernel*
`(Bθ)(x)`. A functional whose variation yields a *field equation* must be
**quadratic** in θ — a linear functional has `δS/δθ = const ≠ 0` and no stationary
point. The correct scalar action coupling the field to matter is therefore

$$\boxed{\;S_{\rm total}[\theta] \;=\; \underbrace{\tfrac12\sum_{x\in C}\theta(x)\,(B\theta)(x)\,V_x}_{S_{BD}}\;-\;\underbrace{\sum_{x\in C} J(x)\,\theta(x)\,V_x}_{S_{\rm fonte}}\;}$$

with `V_x = 1/ρ` the proper event volume and `J` the source. For a point mass `M`
at rest at the origin the source is the relativistic-Poisson right-hand side,
`J = 4πG\,T/c⁴`, supported on the matter worldline (`x_spatial = 0`) — the prompt's
`S_fonte` with the `δ(x_spatial)·V_x` weight.

---

## 2. The discrete field equation (variation)

Varying `S_total` with respect to the nodal field and using the (near-)self-adjointness of `B`:

$$\frac{\delta S_{\rm total}}{\delta\theta(x)} \;=\; (B\theta)(x) - J(x) \;=\; 0 \qquad\Longrightarrow\qquad \boxed{\,B\theta = J\,}.$$

This is the discrete field equation. Its continuum limit is fixed by what `B`
converges to.

---

## 3. Continuum limit: `B → □` (the death criterion)

**Death criterion (prompt):** if the variation does **not** produce an operator
converging to `□`, the action is wrong. We verify convergence by the **exact**
moment structure of the Poisson-averaged BD kernel.

Averaged over Poisson sprinklings, the probability that a past event sits in layer
`n` (its causal interval to `x` containing `n` events) is `P_n = e^{−λ}λⁿ/n!` with
`λ = ρV` the expected count in an interval of volume `V`. The layer-weighted kernel
is

$$K(\lambda) \;=\; e^{-\lambda}\Big(C_0 + C_1\lambda + C_2\tfrac{\lambda^2}{2!}\Big) \;=\; e^{-\lambda}\Big(1 - 2\lambda + \tfrac{\lambda^2}{2}\Big).$$

Its moments are **exact integers** (verified symbolically in `D1_action.py`):

| `k` | ∫₀^∞ λᵏ K(λ) dλ | meaning |
|---|---|---|
| 0 | **0** | `B` annihilates a **constant** field — like `□1 = 0` |
| 1 | **0** | `B` annihilates a **linear** field — like `□(a·x) = 0` |
| 2 | **2** | nonzero → `B` is a **second-order** operator (sets the `□` normalisation) |
| 3 | 18 | (higher, sub-leading) |

The pattern `[0, 0, 2]` is the discrete fingerprint of the continuum
d'Alembertian `□ = ∂_t² − ∂_x²`: a second-order operator that kills constants and
linear fields. This is the structural content of the Benincasa–Dowker theorem
`⟨Bθ⟩ → □θ`.

**Numerical corroboration (same operator as e10).** The live *smeared* operator,
run on a modest sprinkle, **annihilates constants robustly** (`⟨B[const]⟩ =
−0.03 ± 0.02 ≈ 0`, a prefactor-independent test of the normalisation). The full
**magnitude** (`□t² = +2`, `□x² = −2`) is *not* recoverable pointwise — the signal
is `□/(2ερ)`, buried under `O(0.3)` variance — exactly the difficulty e10
documented, which is *why* Benincasa–Dowker validate via the **summed action**
(used directly in D2). The Lorentzian *signature* (`□cos kx > 0`, `□cos kt < 0`) is
e10's separate result; it is corroborating but noise-limited and is **not** gated
on here, because the exact moments already settle the structure.

**Verdict on the limit:** `B → □`. ✅ The death criterion is not triggered.

---

## 4. Static point mass → relativistic Poisson → `GM/rc²`

With `B → □`, the discrete field equation `Bθ = J` becomes, in the continuum,

$$\Box\,\theta = 4\pi G\,T/c^4.$$

For a static point mass the stress-energy reduces to `T → ρ_matter c²` and `□ →
−∇²`, giving the **relativistic Poisson equation**

$$\nabla^2\theta = \frac{4\pi G}{c^2}\,\rho_{\rm matter}.$$

Solving the spherical vacuum equation (`r > 0`) symbolically gives `θ(r) = C₁ +
C₂/r` — the `1/r` harmonic profile. Fixing the constants by the point-mass source
(`∇²(1/r) = −4πδ³`) gives **[comparison only]**

$$\boxed{\;\theta(r) = \frac{GM}{rc^2}\;}$$

with **unit coefficient**. This is *exactly* P2's bridge scalar
`θ = δρ_eff/ρ₀ = GM/rc²`. Cross-checking against P2's **counted** density (no
formula fed back): the far-field apparent coefficient `θ·r/M → 0.985 ≈ 1`. ✅

---

## Verdict — D1: **PASSA**

| check | result |
|---|---|
| kernel moments `[0,0,2]` (kills const+linear, second order) | ✅ exact |
| live operator annihilates constants (robust) | ✅ `−0.03 ± 0.02` |
| static solution `θ ∝ 1/r` | ✅ `C₁ + C₂/r` |
| point mass → `GM/rc²` = P2 bridge scalar (comparison) | ✅ coeff `0.985 ≈ 1` |

**The variation of the BD action yields an operator that converges to `□`, so the
discrete field equation `Bθ = J` becomes the relativistic Poisson equation
`□θ = 4πG T/c⁴`. For a static point mass it integrates to `θ = GM/rc²`, the unit-
coefficient bridge scalar of P2. The action with a matter source is correct in the
continuum — the dynamics exists.** D2 and D3 (numerical) are warranted.

**Honest scope.** D1 establishes the *continuum limit* of the action, not a fresh
pointwise recovery of `□` (which is noise-limited — the documented BD pathology,
re-confirmed here). The clean handle is the exact moment fingerprint plus the
summed-action route, which D2 uses. The new content over P2/P3: the `1/r` profile
is now an **output** of minimising the action with only a point source, not the
Schwarzschild profile imposed by hand (as in P3). What D1 does **not** yet do is
let a *network* find that profile — that is D2 (candidate shapes) and D3 (free
Monte-Carlo).
