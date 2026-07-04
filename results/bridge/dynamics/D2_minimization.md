# D2 — Minimising the BD action over candidate profiles f(r)

> **Bridge / dynamics investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing. Continues [D1](D1_action.md). Reproduce:
> `python results/bridge/dynamics/D2_numeric.py` (~5 s). Data:
> [`D2_numeric_data.json`](D2_numeric_data.json) · figure
> [`D2_numeric.png`](D2_numeric.png).

**Anti-circularity.** The generator uses only: the candidate shapes `f(r)`, the
radial shell measure `r^{d-1}` (geometry — an allowed volume element, exactly the
kind P2/P3 used for the metric), and a **free** source coupling `κ` (never labelled
`G`). `G`, `GM/r` and `√(1−2M/r)` appear only in the final *comparison-only* block,
to calibrate `κ` and score against Schwarzschild / P2 / R3.

---

## What is minimised

From D1, the static field action (continuum limit `B → □ → −∇²`) for a point mass
sourcing `θ(r) = ε·f(r)` is the field-energy functional

$$S[\theta] = \tfrac12\!\int\!\Big(\frac{d\theta}{dr}\Big)^2 r^{d-1}\,dr \;-\; \kappa\!\int\!\rho_{\rm matter}\,\theta\, r^{d-1}\,dr,$$

with `d` the number of **spatial** dimensions. Minimising over the amplitude `ε`
for a fixed shape gives a closed form,

$$S_{\min}[f] = -\tfrac12(\kappa M)^2\,Q[f],\qquad Q[f]=\frac{f(r_{\min})^2}{\int (f')^2\, r^{d-1}\,dr},$$

so the **preferred shape maximises `Q[f]`** — and the maximiser is exactly the
Green's function of the static operator `−∇²` (the variational characterisation of
the Newtonian potential). This is scale-invariant in `f`, so candidate
normalisation is irrelevant.

The four candidates (prompt): `f₁=1/r`, `f₂=1/r²`, `f₃=e^{−r/r₀}`,
`f₄=1/√(r²+r₀²)`.

---

## Result

`S_min[f]` (more negative = preferred), at the literal causal-set dimension `d=1`
and the bridge-relevant `d=3`:

| candidate | `S_min` (d=3, 3D radial — bridge) | `S_min` (d=1, literal 1+1D) |
|---|---|---|
| **f₁ = 1/r** | **−0.50251** ← min | −1.50000 |
| f₂ = 1/r² | −0.37500 | −0.62500 |
| f₃ = e^{−r/r₀} | −0.35294 | −3.00000 |
| f₄ = 1/√(r²+r₀²) | −0.26160 | **−7.25301** ← min |

- **d=3 winner: `f₁ = 1/r`.** ✅ The 3D-radial action prefers the Newtonian
  potential. The discrete operator **annihilates** `1/r` in vacuum:
  `rms □(1/r) = 2.6×10⁻⁹ ≈ 0` (it is harmonic) — a direct demonstration that the
  network's second-order operator (D1) discretises the Newtonian field equation
  `Bθ = 0` away from the source.
- **d=1 winner: `f₄` (smoothed/decaying), *not* `1/r`.** In one spatial dimension
  the Green's function of `−∂_r²` is `|r|` (it *grows*, non-normalisable), so a
  localised field instead prefers a screened/decaying profile. This is the **honest
  dimensional caveat**: the Newtonian `1/r` is a feature of **three** spatial
  dimensions, which the literal 1+1D causal sets of P2/P3 do not carry.

### Consistency with Schwarzschild / R3 / P2 (comparison only)

Calibrating the free coupling so the emergent scalar is `θ = M/r = GM/rc²` (P2's
bridge scalar), the emergent static clock rate `dτ/dt = 1/(1+θ)` versus
`√(1−2M/r)`:

| r | emergent `dτ/dt` | GR `√(1−2M/r)` |
|---|---|---|
| 3 | 0.7500 | 0.5774 |
| 10 | 0.9091 | 0.8944 |
| 20 | 0.9524 | 0.9487 |
| 40 | 0.9756 | 0.9747 |
| 160 | 0.9938 | 0.9937 |

**Weak-field (r ≥ 20) max relative error: 0.39%.** The emergent `θ = M/r` is the
*linear/Newtonian* potential, so it agrees with the full GR redshift exactly where
linear theory is valid (large r) and deviates at small r — as it must: the
higher-order GR terms (`√` vs `1+`) require the **nonlinear** action, not the
quadratic one minimised here. The full-range correlation is 0.990 for this reason;
gating on a strong-field 0.999 would wrongly penalise linear theory for not being
full GR.

---

## Verdict — D2: **PASSA (campo fraco / weak field)**

| check | result |
|---|---|
| `f = 1/r` minimises the d=3 (bridge) action | ✅ |
| operator annihilates `1/r` in vacuum (harmonic) | ✅ `rms □ ≈ 3×10⁻⁹` |
| emergent proper time matches Schwarzschild (weak field) | ✅ 0.39% (r ≥ 20) |
| literal 1+1D prefers `1/r` | ❌ prefers screened `f₄` — needs d=3 |

**The network's discrete dynamics prefers the Newtonian potential `f(r)=1/r`: it
both minimises the action and is annihilated by the operator in vacuum. The
emergent proper time matches Schwarzschild in the weak field to 0.4%, consistent
with R3 and P2.** This is a genuine advance over P3: there the profile
`f=1−2M/r` was *imposed*; here the `1/r` shape is an **output** of minimising the
action with only a point source.

**Two honest caveats, precisely located.**
1. **Spatial dimension `d=3` is geometric input** (the shell measure `r^{d-1}`),
   exactly as the Schwarzschild metric was input in P2/P3. The 1+1D causal
   *structure* alone prefers a screened profile; the `1/r` falloff needs three
   spatial dimensions.
2. **Only the leading (Newtonian) term is derived.** The quadratic action gives
   `θ = M/r`; the full `√(1−2M/r)` (strong field) needs the nonlinear action.

What D2 leaves to D3: here the candidate shapes were *supplied* and ranked. D3 lets
the network find its own equilibrium profile by Monte-Carlo, with no shape imposed.
