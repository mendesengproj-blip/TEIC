# P1 — Dimensional argument + soldering relation

> Path 1 of the ρ(r) bridge investigation. Independent of R1–R3 / e6–e11.
> **Verdict: CIRCULAR — does not close. Proceed to P2.**

---

## What P1 attempts

Use the already-derived soldering relation together with the DEV identification
θ ≈ −Φ/c² to obtain ρ(r) *indirectly*, without a network calculation.

## Derivation, step by step

1. **DEV, Newtonian limit.** The DEV scalar in weak field satisfies θ ≈ −Φ/c².
   For a point mass Φ = −GM/r, so

   $$\theta(r) \;\approx\; -\frac{\Phi}{c^2} \;=\; \frac{GM}{r c^2}.$$

2. **Soldering relation** (from `docs/DEV_bridge_future.md` §3, established by
   comparison of equations of motion; coefficient open):

   $$\theta(x) \;=\; \frac{M_{\rm scale}}{\alpha}\,\frac{\delta\rho}{\rho_0}.$$

3. **Combine** (1) and (2):

   $$\frac{\delta\rho}{\rho_0} \;=\; \frac{\alpha}{M_{\rm scale}}\,\frac{GM}{r c^2}.$$

4. **Result:**

   $$\boxed{\;\rho(r) \;=\; \rho_0\!\left[\,1 + \frac{\alpha}{M_{\rm scale}}\,\frac{GM}{r c^2}\,\right]\;}$$

## Boundary conditions (all satisfied — but see the verdict)

| Check | Result |
|---|---|
| Positivity for all r | ✅ yes, provided α > 0 |
| r → ∞ (flat network far away) | ✅ ρ → ρ₀ |
| r → 0 (near the source) | ρ diverges as 1/r — compatible with a singularity |
| Emergent force | ✅ ∂ρ/∂r ∝ −GM/r² reproduces the Newtonian inverse-square law |

So the **form** of ρ(r) is fine. The form is not the problem.

## Honest judgement — CIRCULAR

P1 fails its own pre-registered death criterion.

- **The 1/r came from Φ.** Step 1 *inserts* the gravitational potential
  Φ = −GM/r as the input. Step 4 then *recovers* δρ/ρ₀ ∝ GM/r. We used Φ to
  produce Φ. This is precisely the "γ-by-hand" error the anti-circularity guard
  exists to forbid: GM/r enters the **generator** of ρ, not just the final
  comparison. The prompt's hard rule —

  > *G, GM/r, e o potencial gravitacional só aparecem na comparação final, nunca
  > no gerador de ρ.*

  is violated by construction in step 3.

- **The coefficient α/M_scale is free.** It is the soldering normalisation
  (α = dilaton–gauge coupling, M_scale = a mass scale), and nothing in P1 ties it
  to a geometric quantity of the network (link density, mean chain length, …).
  The death criterion states: *if α/M_scale is free → tautology → CIRCULAR.* It is
  free. So P1 is circular.

P1 is a **consistency check**, not a derivation: it confirms that *if* the
soldering relation holds and *if* θ ↔ −Φ/c², *then* ρ(r) has the right shape and
the right Newtonian limit. It cannot establish that ρ(r) actually varies this way,
because it never asks the network anything.

## What would have made P1 non-circular

α/M_scale emerging from a measured geometric property of the causal network
(e.g. the diamond-plaquette density n_P(x), or a counted mean link length) with
**no** gravitational input. P1 supplies no such measurement, so the coefficient
stays free. **P2 is exactly the missing measurement**: it computes the coefficient
from counting on the network and finds α/M_scale = 1 (leading order), turning the
P1 tautology into a derived statement — see `P2_schwarzschild.md`.

## Outcome

**P1 CIRCULAR → does not close → continue to P2.** (Per the strict ordering, we
would have stopped here only if P1 had closed *without* circularity.)
