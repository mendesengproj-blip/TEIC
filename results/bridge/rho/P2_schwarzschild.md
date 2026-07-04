# P2 — Effective causal density from the diamond / proper-time argument (CST)

> Path 2 of the ρ(r) bridge investigation. Independent of R1–R3 / e6–e11.
> **Verdict: PASSA (closes within CST/Schwarzschild). Coefficient on M/r is 1.
> Consistent with R3. Content ⊂ R3 — a reinterpretation, not new physics.**
>
> Code: [`P2_numeric.py`](P2_numeric.py) · Data: [`P2_numeric_data.json`](P2_numeric_data.json) · Figure: `P2_numeric.png`

---

## 1. Setup (non-circular by construction)

Sprinkle the 2D radial Schwarzschild slice in **tortoise coordinates**, where

$$ds^2 = \Bigl(1-\tfrac{2M}{r}\Bigr)\bigl(-dt^2 + dr_*^2\bigr)$$

is conformally flat, so the causal relation is the bare 45° light cone. The metric
enters the generator **only** as the proper-volume sprinkling weight
Ω² = (1 − 2M/r); it is **never square-rooted** there (`src/curved.py`,
`sprinkle_schwarzschild`). The sprinkle is at uniform **proper** density ρ₀ — the
covariant CST sprinkling. This is the exact generator R3 / e3 already use.

## 2. The analytic statement

The covariant sprinkling density is uniform (ρ₀ per unit proper volume) — that is
what "uniform sprinkle" *means*, and it does not vary. The quantity that varies,
and that the bridge needs, is the **event rate per unit of a static observer's
proper time**. A static observer at r runs slow by the redshift factor; in a fixed
amount of *his* proper time, more far-frame causal slices stream past, so the
events he encounters per unit proper time are denser:

$$
\rho_{\rm eff}(r) \;=\; \rho_0 \,\frac{dt}{d\tau}
\;=\; \frac{\rho_0}{\sqrt{1-2M/r}}
\;\approx\; \rho_0\Bigl[\,1 + \frac{GM}{rc^2} + \tfrac{3}{2}\Bigl(\tfrac{GM}{rc^2}\Bigr)^2 + \dots\Bigr].
$$

This is the prompt's P2 result, **with the leading weak-field coefficient = 1**
(the 1D time-ratio, not the 2D area factor — see the numerical check). Its
reciprocal is the static-observer clock rate dτ/dt = √(1 − 2M/r), which is exactly
**R3**. So P2 and R3 are the *same measurement, inverted*.

## 3. The numerical verification (counting only)

`P2_numeric.py` measures the static-observer clock rate dτ/dt **by counting**
(R3's estimator τ = √(2N/ρ₀)), then forms ρ_eff/ρ₀ = 1/(dτ/dt). The closed forms
√(1−2M/r) and 1/√(1−2M/r) appear **only** in the final comparison (`validation.py`,
quarantined). Seed 31415926, ρ₀ = 4000, 60 realisations per point.

| r | dτ/dt (counted) | ρ_eff/ρ₀ (counted) | CST 1/√(1−2M/r) |
|---:|---:|---:|---:|
| 3 | 0.5776 | 1.7314 | 1.7321 |
| 4 | 0.7068 | 1.4148 | 1.4142 |
| 6 | 0.8163 | 1.2251 | 1.2247 |
| 10 | 0.8953 | 1.1170 | 1.1180 |
| 20 | 0.9479 | 1.0549 | 1.0541 |
| 40 | 0.9744 | 1.0262 | 1.0260 |
| 80 | 0.9882 | 1.0119 | 1.0127 |
| 160 | 0.9939 | 1.0062 | 1.0063 |

- **Match to the CST form 1/√(1−2M/r):** correlation **1.00000**, max relative
  error **0.09%**.
- **Consistency with R3:** the counted clock rate vs √(1−2M/r) has correlation
  **0.99999**, max error **0.09%** — by construction the same number R3 reports
  (R3 itself: corr 1.0000, max err 0.21%). ✅
- **Weak-field leading coefficient → 1:** the apparent slope (ρ_eff−1)/(M/r)
  descends toward 1 as r grows (0.955 at r=80, 0.985 at r=160). The strong-field
  points (M/r up to 0.33) confirm the *full* 1/√ form, including the +1.5(M/r)²
  curvature; they cannot be used to read the leading slope and are not.

**Death criterion (prompt): does the count scale as 1 + GM/rc²?** Yes — it scales
as the full 1/√(1−2M/r), whose leading term is exactly 1·(GM/rc²). **P2 PASSES.**

## 4. The coefficient P1 left free is now fixed

P1 ended with ρ(r) = ρ₀[1 + (α/M_scale)·GM/rc²] and a **free** α/M_scale. P2
supplies the coefficient from network counting:

$$\frac{\delta\rho_{\rm eff}}{\rho_0} = \frac{GM}{rc^2} \quad\Longrightarrow\quad \frac{\alpha}{M_{\rm scale}} = 1.$$

It comes from the geometric expansion of the proper-time ratio, with **no**
gravitational input in the generator. This is exactly the non-circular ingredient
P1 lacked.

## 5. Honest scope — two densities, do not conflate them

The single most important caveat. "Causal density near a mass" is **ambiguous**,
and the two natural meanings move in **opposite directions**:

| Quantity | Definition | Near the mass | Formula |
|---|---|---|---|
| **Coordinate** density ρ_coord | events per unit *coordinate* volume | **decreases** | ρ₀(1 − 2M/r) |
| **Proper-time** density ρ_eff | events per unit static-observer *proper time* | **increases** | ρ₀/√(1 − 2M/r) |

They are reciprocally related through the clock:
ρ_eff/ρ₀ = (ρ_coord/ρ₀)^(−1/2). The covariant sprinkling density itself is **uniform**
(ρ₀ everywhere) — neither of the above; both are *frame-relative* readings of it.

The bridge / DEV identification δρ/ρ₀ ↔ −Φ/c² needs the **increase**, i.e. the
**proper-time** density ρ_eff. The bare coordinate count goes the *other way* and
would give the wrong sign. So P2 closes the bridge **only** with ρ ≡ ρ_eff (the
inverse-redshift / clock-deficit density), not the literal coordinate event count.
This is the precise, defensible content of "the causal density grows near a mass."

Because ρ_eff is R3 inverted, **P2 adds no physics beyond R3** — it is R3
re-expressed as a density, exactly as e8 is R2 re-expressed as a redshift. Honest
verdict: the bridge gains an **analytic + numerical foothold in CST**, not an
independent new result. The genuinely new step (deriving why ρ varies as g_tt from
network *dynamics with matter*) is P3's domain and, ultimately, the discrete
action — see `P3_*` and `../../../BRIDGE_RHO.md`.

## Outcome

**P2 PASSES** (within CST/Schwarzschild): ρ_eff(r) = ρ₀/√(1−2M/r) ≈ ρ₀[1 + GM/rc²],
coefficient 1, correlation 1.00000 with the CST form, fully consistent with R3.
The bridge has analytic + numerical support — with the ρ ≡ ρ_eff caveat made
explicit.
