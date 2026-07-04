# BRIDGE_RHO — deriving ρ(r): the causal density around a mass

> **Independent investigation.** This does **not** modify R1–R3 or e6–e11, and is
> not part of the TEIC paper. It extends the internal record in
> [`docs/DEV_bridge_future.md`](docs/DEV_bridge_future.md). All artefacts live in
> [`results/bridge/rho/`](results/bridge/rho/).

**Central rule (anti-circularity).** G, GM/r, the gravitational potential Φ, and
the redshift √(1−2M/r) appear **only in the final comparison** — never in the
generator of ρ. The dilation/density must *emerge* from counting. The main
pipeline's guard (`tests/test_no_circularity.py`) still **passes**; the bridge
generators use the volume element (1 − 2M/r) but never its square root.

---

## The question

How does the causal-network event density ρ(r) vary around a mass M? If ρ(r) is
*derived* (not assumed), the soldering relation θ = (M/α)·δρ/ρ₀ becomes physical:
the DEV scalar field is the perturbation of the causal density, and the
TEIC→DEV scalar bridge has a foundation.

Three paths, run in strict order P1 → P2 → P3 (stop only if P1 closes cleanly).

---

## Verdicts

| Path | What | Verdict |
|---|---|---|
| **P1** — dimensional + soldering | obtain ρ(r) from θ ≈ −Φ/c² and the soldering relation | **CIRCULAR** — uses Φ to get Φ; coefficient α/M_scale free. Does not close. |
| **P2** — CST diamond / proper time | ρ_eff(r) = ρ₀/√(1−2M/r) by counting in Schwarzschild | **PASSA** — corr **1.00000** with CST form, max err **0.09%**, leading coeff **1**, consistent with R3. Content ⊂ R3. |
| **P3** — variable-density sprinkle | flat causal set with ρ(r)=ρ₀·f(r) reproduces Schwarzschild | **PASSA numerically** (corr 1.00000, err 0.07%) — but f(r)=1−2M/r is **imposed, not derived**. |

P1 did **not** close (circular), so we proceeded. **P2 closes the bridge within
CST**; **P3 confirms the mechanism** but localises the remaining gap (the density
profile's origin). Full detail per path:
[`P1_dimensional.md`](results/bridge/rho/P1_dimensional.md) ·
[`P2_schwarzschild.md`](results/bridge/rho/P2_schwarzschild.md) ·
[`P3_perturbative.md`](results/bridge/rho/P3_perturbative.md).

---

## The result

$$\boxed{\;\rho_{\rm eff}(r) \;=\; \frac{\rho_0}{\sqrt{1-2M/r}} \;\approx\; \rho_0\Bigl[\,1 + \frac{GM}{rc^2}\,\Bigr]\;}$$

derived (P2) and cross-checked (P3) by counting, with the coefficient on GM/rc²
equal to **1** — fixing the α/M_scale that P1 left free: **α/M_scale = 1**.

### The one caveat that matters: *which* density

"Causal density near a mass" is ambiguous; the two natural readings move in
**opposite directions**, and only one closes the bridge:

| | per coordinate volume | per static-observer **proper time** |
|---|---|---|
| symbol | ρ_coord | **ρ_eff** |
| near mass | **decreases**: ρ₀(1 − 2M/r) | **increases**: ρ₀/√(1 − 2M/r) |
| role | makes the counting clock run slow (R3, P3) | the bridge / DEV density (P2) |

The covariant sprinkling density itself is **uniform** ρ₀; both rows are
frame-relative readings of it, reciprocally related through the clock
(ρ_eff = ρ₀·(dτ/dt)^(−1), ρ_coord = ρ₀·(dτ/dt)²). The DEV identification
δρ/ρ₀ ↔ −Φ/c² (an *increase*) requires ρ ≡ **ρ_eff**, the inverse-redshift
density — **not** the literal coordinate event count, which has the wrong sign.

### Consistency with R3 (required, and met)

P2's measured quantity is R3's static-observer clock rate, inverted: dτ/dt =
√(1−2M/r) (R3: corr 1.0000, max err 0.21%). The P2 run reproduces it at corr
0.99999, max err 0.09% — automatically consistent because it is the same counting
estimator. P3 reproduces the same √(1−2M/r) from a flat variable-ρ sprinkle to
0.07%.

---

## Connection to the DEV (Newtonian regime)

With ρ_eff above, δρ/ρ₀ = GM/rc². The soldering relation (coefficient now fixed,
α/M_scale = 1) gives the TEIC-floor scalar

$$\theta(r) = \frac{M_{\rm scale}}{\alpha}\,\frac{\delta\rho}{\rho_0} = \frac{GM}{rc^2}.$$

In the DEV, the Newtonian-limit scalar for a point mass satisfies the Poisson
equation and is θ ≈ GM/rc². The two agree:

- **Point-mass value:** θ_TEIC = GM/rc² = θ_DEV. ✅
- **Field equation:** θ = −Φ/c² with ∇²Φ = 4πGρ_matter ⇒ ∇²θ = −4πGρ_matter/c²;
  i.e. θ obeys the same Poisson equation as −Φ/c², sourced by matter. For a point
  mass this integrates to GM/rc², matching δρ_eff/ρ₀. ✅ (G=c=1 used numerically.)

So **the scalar bridge TEIC→DEV is closed in the Newtonian regime**: the DEV scalar
θ *is* the fractional proper-time causal-density contrast δρ_eff/ρ₀ of the network,
with unit coefficient.

---

## What remains open (the honest bottleneck)

P2/P3 close the bridge *kinematically* — given Schwarzschild as the background, the
network density that reproduces it is ρ_eff = ρ₀/√(1−2M/r), and the DEV scalar maps
onto it. What is **not** derived is the **dynamics**: why the network density
should take the g_tt profile around matter in the first place. P3 imposes that
profile; deriving it needs the discrete gravitational action with a matter source
(Benincasa–Dowker), the frontier already flagged in the TEIC README's "next steps"
and in `docs/DEV_bridge_future.md`. Mapping that gap precisely — rather than
hiding it — is itself the result, in the same spirit as the e6→e11 two-floor
closure.

---

## Reproduce

```bash
python results/bridge/rho/P2_numeric.py     # Schwarzschild count -> rho_eff(r); ~1 min
python results/bridge/rho/P3_numeric.py     # flat variable-rho   -> Schwarzschild; ~1 min
python tests/test_no_circularity.py         # guard still passes (exit 0)
```

Outputs (seeded, self-describing): `P2_numeric_data.json`, `P3_numeric_data.json`,
and the figures `P2_numeric.png`, `P3_numeric.png` in `results/bridge/rho/`.
