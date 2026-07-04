# P3 — Variable-density sprinkling reproduces Schwarzschild

> Path 3 of the ρ(r) bridge investigation. Independent of R1–R3 / e6–e11.
> **Verdict: PASSA numerically (mechanism confirmed) — but the profile f(r) is
> IMPOSED, not derived. The form is external, exactly as e11's phase scale was.**
>
> Code: [`P3_numeric.py`](P3_numeric.py) · Data: [`P3_numeric_data.json`](P3_numeric_data.json) · Figure: `P3_numeric.png`

---

## 1. What P3 does (the most rigorous, fully flat test)

No curved metric at all. Bare flat 2D Minkowski, 45° light cones. Sprinkle at a
**position-dependent density** ρ(r) = ρ₀·f(r). A static observer at r measures its
proper time between two worldline events (coordinate separation dt) **by counting**,
normalising against the **global** reference density ρ₀ (the far / cosmic-mean
value), not the local one:

$$\tau_{\rm meas}(r) = \sqrt{\tfrac{2N}{\rho_0}}, \qquad N \approx \rho(r)\cdot\tfrac12 dt^2 \;\Rightarrow\; \frac{d\tau}{dt}(r) = \sqrt{\frac{\rho(r)}{\rho_0}} = \sqrt{f(r)}.$$

So in a flat causal set the static-observer dilation is set **entirely by the
density profile**. Asking which f reproduces Schwarzschild is asking: for what f is
√(f(r)) = √(1 − 2M/r)? Trivially, **f(r) = 1 − 2M/r**.

**Anti-circularity.** The generator sprinkles at f(r) = (1 − 2M/r) — an allowed
volume element — and **never square-roots it** (the guard forbids √(1−2M/r), not
1−2M/r). The redshift √(1−2M/r) and GM/r enter only in the final comparison. The
dilation emerges from counting.

## 2. Numerical result

`P3_numeric.py`, seed 27182818, ρ₀ = 6000, 60 realisations per point.

| r | dτ/dt (counted, flat variable-ρ) | GR √(1−2M/r) | err |
|---:|---:|---:|---:|
| 3 | 0.5774 | 0.5774 | 0.01% |
| 4 | 0.7066 | 0.7071 | 0.07% |
| 6 | 0.8164 | 0.8165 | 0.01% |
| 10 | 0.8943 | 0.8944 | 0.01% |
| 20 | 0.9482 | 0.9487 | 0.05% |
| 40 | 0.9745 | 0.9747 | 0.02% |

- **Dilation vs GR:** correlation **1.00000**, max relative error **0.07%**.
- **Inverse check** (does the counted (dτ/dt)² recover the input f(r)?): max
  error **0.13%**. ✅

The full Schwarzschild static-observer dilation is reproduced, to sub-percent, by
a **purely flat causal set whose only structure is a varying sprinkle density**.

## 3. Honest judgement — mechanism yes, derivation no

P3 confirms the **mechanism**: density variation alone, with bare flat light cones
and counting, produces gravitational time dilation. That is a clean, non-circular
demonstration of the density↔geometry link.

But it does **not** derive f(r). We *imposed* f(r) = 1 − 2M/r and then confirmed by
counting that it reproduces Schwarzschild. Scanning candidate profiles would only
recover the same f = g_tt — i.e. it re-measures the metric. The form's **origin**
(why the network density should track g_tt around matter) is not supplied here. To
derive it from first principles one needs the discrete gravitational action with a
matter source (Benincasa–Dowker causal-set action); that is **out of scope**
(weeks→months, and the open frontier the prompt flags).

This is structurally identical to **e11**: *form derived, scale/profile external*.
P3 derives the *mechanism* (dilation = √(ρ/ρ₀)); the *profile* f(r) = 1 − 2M/r
remains an input.

## 4. The sign, again (consistency with P2)

P3's reproducing profile is the **coordinate** density f(r) = 1 − 2M/r, which
**decreases** near the mass — because the counting clock needs *fewer* events per
coordinate diamond to run slow. This is the **opposite** sign to P2's
ρ_eff = ρ₀/√(1−2M/r), which **increases**. Both are correct and consistent: they
are reciprocally related through the clock (ρ_eff = ρ₀·(dτ/dt)^(−1), with
(dτ/dt)² = ρ_coord/ρ₀). The bridge needs the increase (ρ_eff, proper-time density);
the dilation-by-counting needs the decrease (ρ_coord, coordinate density). See
`P2_schwarzschild.md` §5 — this two-density distinction is the central subtlety of
the whole investigation.

## Outcome

**P3 PASSES numerically** (flat variable-density sprinkle reproduces √(1−2M/r) to
0.07%), confirming the dilation-from-density mechanism non-circularly. **But the
profile f(r) = 1 − 2M/r is imposed, not derived** — its origin needs the discrete
action with matter, which is the documented bottleneck.
