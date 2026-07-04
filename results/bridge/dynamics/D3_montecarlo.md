# D3 — The network finds ρ(r) by Monte-Carlo (no profile imposed)

> **Bridge / dynamics investigation.** Independent of R1–R3 and e6–e11; modifies
> nothing. Continues [D1](D1_action.md) and [D2](D2_minimization.md). Reproduce:
> `python results/bridge/dynamics/D3_MC.py` (~30 s). Data:
> [`D3_MC_data.json`](D3_MC_data.json) · figure [`D3_MC.png`](D3_MC.png).

**Anti-circularity.** The generator uses only: the shell measure `r^{d-1}`
(geometry, as the metric was in P2/P3), the BD gradient action (D1), event-number
conservation, and a **free** coupling `κ` (never `G`). No `GM/r`, no `√(1−2M/r)`.
`G`, `M` and Schwarzschild appear only in the final *comparison-only* block.

---

## The cleanest test

D2 *ranked supplied shapes*. D3 imposes **no** functional form: the network's
density relaxes freely under the BD action with a point source, and we read off the
equilibrium ρ(r).

**What is sampled.** The network's coarse-grained order parameter is the density
contrast `θ_i = ρ(r_i)/ρ₀ − 1 = δρ/ρ₀` — *exactly* the bridge scalar (soldering
`θ = δρ/ρ₀`). Metropolis runs on this field directly, under the D1 action
(`B → −∇²` in the static limit):

$$E[\theta] = \frac{K}{2}\sum_i\Big(\frac{\theta_{i+1}-\theta_i}{dr_i}\Big)^2 V_i \;-\; \kappa M\sum_i s_i\,\theta_i,$$

with `V_i` the shell volume, `s_i` a finite source-core profile (`r < R_core`), and
event-number conservation as the exact constraint `Σ_i θ_i V_i = 0` (a denser core
is balanced by a thinner far field), enforced by paired moves.

> **Why the field, not individual events.** An event-level sprinkle MC was built
> first and **abandoned**: a `1/r` over-density piles events into a
> microscopic-volume core (`V ∝ r²`) that volume-uniform proposals almost never
> sample — the network stayed empty at the core regardless of coupling. That is a
> *sampling pathology*, not physics. The field `θ` **is** the coarse-grained
> density; sampling it is the faithful, robust form. For the quadratic BD action the
> Metropolis **mean equals the action minimum exactly**, so the network genuinely
> *finds* the profile with no shape imposed.

---

## Result

The network responds to the source and finds a decaying over-density (no shape was
imposed):

| r | ρ_MC/ρ₀ | θ_MC |
|---|---|---|
| 1.1 | 1.321 | +0.321 |
| 3.6 | 1.247 | +0.247 |
| 8.2 | 1.099 | +0.099 |
| 18.5 | 1.027 | +0.027 |
| 27.9 | 1.007 | +0.007 |
| 42.0 | 0.998 | −0.002 |

- **Network responded (anti-MORTE):** `⟨θ⟩_core = +0.29 > 0`, far from uniform. The
  source–network coupling *does* move the network. ✅
- **Emergent tail `θ = A/r + C`** with `A = 1.028`, `C = −0.0281`. The fit was a
  *generic* `1/r` shape (anti-circular: `A` free, no GR input).
- **The offset `C` is event conservation, confirmed.** Conservation forces the
  positive core over-density to be balanced by a small negative far-field offset;
  the pure-`1/r` full-box estimate gives `C_pred = −0.0257`, matching the fitted
  `C = −0.0281` in sign and scale. ✅
- **Tail exponent.** The raw log–log slope is `−1.99` (contaminated by the offset
  `C`); removing the known conservation offset gives **`−1.018 ≈ −1`** — the
  Newtonian `1/r`. ✅

### Consistency with P2 / R3 (comparison only)

Calibrating the free coupling so the Newtonian coefficient is `A = M` (`G=c=1`),
i.e. `θ = GM/rc²` (P2's bridge scalar), the emergent `ρ_eff/ρ₀ = 1 + M/r` versus
P2's `1/√(1−2M/r)` over the far field (`15 ≤ r ≤ 36`):

**corr 0.9991, max relative error 0.62%.** ✅ The Monte-Carlo network reproduces
P2's `ρ₀(1 + GM/rc²)` in the weak field — the same density P2 derived by counting
in Schwarzschild and R3 measured as the static-observer clock rate.

---

## Verdict — D3: **PASSA**

| check | result |
|---|---|
| network responds to source (not uniform) | ✅ `⟨θ⟩_core = +0.29` |
| tail exponent `−1` (Newtonian `1/r`), offset removed | ✅ `−1.018` |
| offset `C` is event conservation | ✅ `−0.028` vs `−0.026` pred |
| far field `= ρ₀(1+GM/rc²)` = P2 | ✅ 0.62%, corr 0.9991 |

**With no functional form imposed, the network's density relaxes under the BD
action with a point source to `ρ_MC(r) = ρ₀(1 + A/r)`: an over-density that decays
as the Newtonian `1/r` (exponent `−1.02`), balanced by the exact event-conservation
offset. Calibrating the coupling, it reproduces P2's `ρ₀(1 + GM/rc²)` to 0.62%.**
This is the strongest form of the result: the Schwarzschild-weak-field network
density is an **output** of minimising the discrete gravitational action, not an
imposed profile (contrast P3) and not a ranked ansatz (contrast D2).

**Honest caveats (same two as D2, precisely located).**
1. **Spatial dimension `d=3`** (shell measure `r^{d-1}`) is geometric input — the
   same status the Schwarzschild metric had in P2/P3. The `1/r` falloff is a 3-space
   feature, not fixed by the causal-set dimension alone.
2. **Only the leading (Newtonian) term** emerges: `θ = A/r`. The full
   `√(1−2M/r)` (strong field) needs the nonlinear action — the next frontier.
3. **Coarse-grained field, not individual events** (for the sampling reason above);
   the two are equivalent in the continuum (`θ = δρ/ρ₀`).
