# BRIDGE_DYNAMICS — deriving ρ(r) dynamically: the BD action with a matter source

> **Independent investigation.** This does **not** modify R1–R3 or e6–e11, and is
> not part of the TEIC paper. It continues [`BRIDGE_RHO.md`](BRIDGE_RHO.md) (paths
> P1–P3) and the internal record in
> [`docs/DEV_bridge_future.md`](docs/DEV_bridge_future.md). All artefacts live in
> [`results/bridge/dynamics/`](results/bridge/dynamics/).

**Central rule (anti-circularity).** Schwarzschild, `G`, `GM/r`, the potential `Φ`,
and the redshift `√(1−2M/r)` enter **only in the final comparison** — never in the
generator. The geometry (the volume element `1−2M/r`, the spatial dimension `d`, the
shell measure `r^{d-1}`) is the allowed background; the density profile and its `1/r`
shape must *emerge* from minimising the action. The main pipeline's guard
(`tests/test_no_circularity.py`) still **passes** (the new code lives under
`results/`, and uses no dilation formula in any generator).

---

## The question

P2/P3 closed the bridge **kinematically**: *given* Schwarzschild, the network
density that reproduces it is ρ_eff = ρ₀/√(1−2M/r), and the DEV scalar maps onto
δρ_eff/ρ₀ = GM/rc². The honest bottleneck that remained: **why** does the network
density take the g_tt profile around matter? That needs the **dynamics** — an action
that, minimised, produces the causal equilibrium configuration in the presence of
matter. This investigation attacks it via the Benincasa–Dowker action with a source.

Three tasks, run in strict order D1 → D2 → D3 (D1 is analytic and decides whether
the action is correct; D2/D3 are numerical and progressively cleaner).

---

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **D1** — action (analytic) | vary `S_BD + S_source`; check continuum limit is relativistic Poisson | **PASSA** — kernel moments `[0,0,2]` (kills const+linear, 2nd order) ⇒ `B → □`; field eq `Bθ=J → □θ=4πG T/c⁴`; point mass → `θ = GM/rc²` = P2 (cross-check 0.985). |
| **D2** — minimise over shapes | which `f(r)` minimises the action? proper time vs Schwarzschild | **PASSA (weak field)** — `f=1/r` minimises the d=3 action and is annihilated by the operator (`rms □(1/r)=3×10⁻⁹`); emergent `dτ/dt` matches `√(1−2M/r)` to **0.39%** (r ≥ 20). |
| **D3** — Monte-Carlo, no shape | let the network find ρ(r) by Metropolis | **PASSA** — `ρ_MC(r)=ρ₀(1+A/r)`, tail exponent **−1.02** (offset = exact event conservation); far field = P2's `ρ₀(1+GM/rc²)` to **0.62%** (corr 0.9991). |

All three close. Full detail per task:
[`D1_action.md`](results/bridge/dynamics/D1_action.md) ·
[`D2_minimization.md`](results/bridge/dynamics/D2_minimization.md) ·
[`D3_montecarlo.md`](results/bridge/dynamics/D3_montecarlo.md).

---

## The result

$$\boxed{\;S_{\rm total}[\theta]=\tfrac12\!\sum_x \theta\,(B\theta)\,V_x-\sum_x J\,\theta\,V_x \;\xrightarrow{\ \delta/\delta\theta\ }\ B\theta=J\ \xrightarrow{\ \text{continuum}\ }\ \Box\theta=\tfrac{4\pi G}{c^4}T\;}$$

Minimising this action with **only a point-mass source** (no Schwarzschild profile
imposed) yields the network density

$$\rho_{\rm eff}(r)=\rho_0\Bigl[\,1+\frac{GM}{rc^2}\,\Bigr],\qquad \theta=\frac{\delta\rho_{\rm eff}}{\rho_0}=\frac{GM}{rc^2},$$

the **weak-field limit of P2's** `ρ₀/√(1−2M/r)`, with unit coefficient. D2 obtains
the `1/r` shape by ranking candidate profiles; **D3 obtains it with no ansatz at
all** — the network relaxes to it under Metropolis. This upgrades the `1/r` profile
from *imposed* (P3) to *output of the action*.

### What changed vs BRIDGE_RHO

| | BRIDGE_RHO (P2/P3) | BRIDGE_DYNAMICS (D1–D3) |
|---|---|---|
| status | kinematic | **dynamic** |
| `ρ_eff = ρ₀/√(1−2M/r)` | *measured* given Schwarzschild | weak-field `ρ₀(1+GM/rc²)` **derived** from the action |
| `1/r` profile | **imposed** (P3: `f=1−2M/r`) | **emerges** from minimising `S` (D2) / free MC (D3) |
| field equation | asserted (`∇²θ = −4πGρ/c²`) | **derived** from `δS=0`, `B→□` (D1) |

---

## Consistency with R3 and P2 (required, and met)

- **D1** point-mass solution `θ = GM/rc²` equals P2's bridge scalar; cross-checked
  against P2's *counted* density (far-field coefficient `θ·r/M = 0.985 ≈ 1`).
- **D2** emergent static clock rate `dτ/dt = 1/(1+θ)` matches R3/P2's `√(1−2M/r)` to
  0.39% in the weak field (r ≥ 20).
- **D3** emergent `ρ_MC/ρ₀` matches P2's `1/√(1−2M/r)` to 0.62% (corr 0.9991) in the
  far field — the same density P2 derived by counting and R3 measured as the clock
  rate.

---

## Connection to the bridge TEIC↔DEV

With ρ_eff derived from the action, the soldering relation gives the TEIC-floor
scalar `θ = δρ_eff/ρ₀ = GM/rc²`, which satisfies the DEV's Poisson equation
`∇²θ = −4πGρ_matter/c²` — now as the **continuum limit of `δS_BD/δθ = J`** (D1), not
as an assertion. So:

> **The scalar bridge TEIC→DEV is now *dynamically derived*, not merely kinematically
> consistent.** The DEV scalar `θ` is the fractional proper-time causal-density
> contrast `δρ_eff/ρ₀` of the network, and that contrast is what the network settles
> into when a mass sources the Benincasa–Dowker action.

This moves the bridge's status from **"consistent + kinematic"** (BRIDGE_RHO) to
**"derived + dynamic (weak field)"**.

---

## What remains open (the honest bottleneck, precisely located)

D1–D3 close the **weak-field / Newtonian** dynamics. Two inputs and one frontier
remain explicit — *mapping* them is itself the result, in the spirit of the
e6→e11 two-floor closure and BRIDGE_RHO's P1 circular verdict:

1. **Spatial dimension `d=3` is geometric input** (the shell measure `r^{d-1}`),
   exactly as the Schwarzschild metric was input in P2/P3. The literal 1+1D causal
   structure used for tractability prefers a *screened* profile, not `1/r` (D2): the
   Newtonian `1/r` is a three-space feature. A first-principles derivation of `d=3`
   is out of scope (and is itself an open problem in CST — spectral/dimension
   estimators).
2. **Only the leading (Newtonian) term is derived:** `θ = GM/rc²`. The full
   `√(1−2M/r)` (strong field) needs the **nonlinear** gravitational action — the
   BD action beyond its quadratic/linear-response truncation. This is the precise
   next frontier.
3. **D3 samples the coarse-grained density field** `θ = δρ/ρ₀`, not individual
   events — a deliberate, documented choice (the event-level MC has a small-volume
   core sampling pathology; the field is the faithful continuum description).

What is **no longer** open: *why the network density rises toward matter*. It rises
because a mass sourcing the Benincasa–Dowker action drives the causal density to the
harmonic `1+GM/rc²` profile — derived here, three independent ways.

---

## Reproduce

```bash
python results/bridge/dynamics/D1_action.py     # action, B->box, point mass; ~20 s
python results/bridge/dynamics/D2_numeric.py    # minimise over shapes -> 1/r;  ~5 s
python results/bridge/dynamics/D3_MC.py         # Metropolis -> rho(r);         ~30 s
python tests/test_no_circularity.py             # guard still passes (exit 0)
```

Outputs (seeded, self-describing): `D1_action_data.json`, `D2_numeric_data.json`,
`D3_MC_data.json`, and figures `D2_numeric.png`, `D3_MC.png` in
`results/bridge/dynamics/`.
