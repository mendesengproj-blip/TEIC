# M1 — inertia as the network's response to a force (refaz T15/T16)

**Verdict: C** — no Newtonian inertia recovered (death criterion met).

## Question
T15/T16's "law of mass" `m = cost/⟨k⟩` was near-tautological (cost and ⟨k⟩ both
count causal links per event). The correct question for *inertial* mass is Newton's:
inertia = resistance to acceleration. We measure `m = F/a` operationally, inserting
no mass, no `F=ma`, no `E=mc²`.

## Method
Poisson 1+1D network (ρ=20, T=9, X=12, 20 seeds). A localized real lump
`θ(x)=exp(−x²/2σ²)` is sourced in an early slab; a "force" is a source gradient
`J(x)=θ(x)·(1+F·x)` (F is the coefficient of a linear source term in `□θ=J`, **not**
`F=ma`). The field is propagated by the causal-set retarded kernel `K=½C`
(Johnston 2008) and the centroid of the response is tracked over future time-slabs.
`m_rede = F/a` with `a` the measured centroid acceleration.

## Results (mean ± SEM over 20 seeds)

| F | v_drift | acceleration a |
|---|---|---|
| 0.00 | +0.0016 ± 0.012 | −0.0197 ± 0.014 |
| 0.05 | −0.0020 ± 0.012 | −0.0222 ± 0.014 |
| 0.10 | −0.0058 ± 0.012 | −0.0244 ± 0.014 |
| 0.20 | −0.0140 ± 0.012 | −0.0277 ± 0.014 |
| 0.30 | −0.0230 ± 0.012 | −0.0296 ± 0.014 |

- Response slope `dv/dF = −0.082` (typical SEM 0.012) — a **marginal (~2–3σ)** trend.
- **Baseline artifacts:** at F=0, where there is no force, `v₀=+0.0016`, `a₀=−0.020`.
- Connectivity scale `⟨k⟩ = 487 ± 5`.

## What it means
The acceleration — which *defines* inertial mass — barely moves with F and is
dominated by a force-independent baseline offset (a pure discreteness/boundary
artifact). So `m=F/a` is **neither stable nor force-independent**: the death
criterion (m depends on force) is met. The free massless network scalar has **no
localized excitation that accelerates like a particle** (confirmed independently by
P1 and P2). What T15/T16 called "mass", `cost/⟨k⟩`, is the connectivity scale ⟨k⟩
(tautological — both count links/event), **not** a Lorentz-invariant inertia.

Because M1 finds no rest inertia, M2 and E1 are necessarily *weakened* (as the
protocol anticipated): they can only test the Lorentz behaviour of the connectivity
**proxy** (M2) and re-express R1's dilation as energy (E1).
