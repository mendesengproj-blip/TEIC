# HQ2 — CRITICAL FERROMAGNET: G_eff near J_c — S8 via critical fluctuations?

> Charter for `results/cosmology/hq2/`. Pre-registered BEFORE any measurement.
> Investigates whether **critical fluctuations** of the causal orientation
> ferromagnet (a mechanism distinct from the mean-field FM1–FM4) can give
> `G_eff < G_N` and so resolve the S8 tension.
> Motors: `orientation_core` (E1) + `e2_core` (E2). NO previous campaign modified.

---

## 1. Why HQ2 differs from FM1–FM4

FM1–FM4 treated the DEV as a **mean-field** theory:
`G_eff = G_N · μ(g/a₀)`, with μ ≥ 1 always (MOND enhances). S8 worsened in all
four sectors. HQ2 asks a different question: near the ferromagnet's critical
coupling `J_c`, orientation fluctuations diverge. Do those fluctuations
renormalise the stiffness downward, `J_eff < J`, and thereby **suppress** G?

```
FM1–FM4 : G_eff = G_N · μ(g/a₀)            [mean field, μ≥1]
HQ2     : G_eff = G_N · μ(g/a₀) · F(J/J_c)  [+ critical fluctuations]
```
The new factor `F(J/J_c) = Z(J/J_c)` is the question. `Z < 1` near `J_c` would be
the first suppression mechanism in the whole programme.

Measured anchors (from E1/E2, reused, not refitted):
- O(3) causal ferromagnet `J_c ≈ 0.08` (E1-2 χ-peak, 2nd-order). U(1) `J_c ≈ 0.05`.
- Deep-ordered moment `m_sat ≈ 0.997` at `J=10` (E1-1).
- Photon speed `c₀ ≈ 0.98` from the BD symbol dispersion (E2, Verdict A: ω=ck).
- E1-3: on the causal link graph S(k) is **flat / non-local** (mean-field) — the
  photon's linear ω=ck comes from the BD causal geometry, **not** from the spin
  gradient term. This fact is central below.

---

## 2. The DEV bridge relation adopted (stated, not re-derived)

From the prompt/DEV: `c² ∝ J` (vacuum rigidity) and the effective Newton constant
tracks the same softening, so we adopt the prompt's relation **as given**:

```
G_eff(J)/G_N = J_eff(J)/J = Z(J/J_c) = (c_eff(J)/c₀)²
```

Deriving the DEV `G–K` bridge is out of scope (done elsewhere). We test the
hypothesis on the prompt's own bridge: softening of the orientation stiffness ⇒
`Z < 1` ⇒ `G_eff < G_N`.

---

## 3. Two estimators for c_eff(J) — both anti-circular

The prompt says "measure c_eff(J) via BD perturbation (motor E2)". A literal
reading and a generous reading give two independent routes; we run **both** so the
death (if any) is triangulated and not an artefact of one estimator.

### Route A — literal (BD / E2 motor)
The BD smeared d'Alembertian is built **only** from the causal order matrix of a
Poisson sprinkle (`precompute_bd_operator`, `symbol_grid`). The spin coupling `J`
appears **nowhere** in it. Hence the dispersion ω=c·k it yields is `J`-independent
*by construction*: `c_BD(J) = c₀` for all J. This is the prompt's literal death
criterion realised structurally — the photon speed is geometric, not set by J.

### Route B — generous (E1 stiffness motor)
Give the hypothesis its **best** chance: measure the genuinely J-dependent
stiffness of the orientation ferromagnet. On the causal link graph (mean-field,
flat S(k)), the gradient/Goldstone stiffness of transverse fluctuations is set by
the squared ordered moment:
```
ρ_s(J) ∝ m(J)²        (mean-field spin stiffness; → 0 at J_c as m → 0)
Z_B(J/J_c) = c_eff²(J)/c₀² = ρ_s(J)/ρ_s(deep) = ( m(J) / m_sat )²
```
`m(J)` is measured fresh (O(3), 20 seeds, `orientation_core`). This route **does**
soften near `J_c` (m → 0), so Route B is the version that can make HQ2-2 positive.

**Anti-circularity:** `G_N` never enters as a constant; `Z = G_eff/G_N` is a
measured lattice ratio. No `c`, no critical coupling, no target exponent inserted
into any generator. `J_c` is the E1 χ-peak value, NOT tuned to escape death.
KiDS/ΛCDM σ8 are COMPARISON ONLY.

---

## 4. Pre-registered predictions (what I expect, on the record)

1. **HQ2-V gate:** ξ(J) rises sharply approaching `J_c` from below; χ(J) peaks at
   `J_c`; transition 2nd-order. (E1-2 already supports this.) **Expect PASS.**
2. **HQ2-1 Route A:** c_BD constant in J (BD is J-blind). **Expect c_eff const.**
3. **HQ2-1 Route B:** c_eff² ∝ m(J)² decreases as J→J_c (real softening).
   **Expect c_eff decreases.**
4. **HQ2-2:** Route B gives `Z = (m/m_sat)² < 1`, smallest near `J_c`
   ⇒ HQ2-2 "positive" on Route B ⇒ proceed to HQ2-3/4.
5. **HQ2-3:** the universe is **never** near `J_c`. A stable photon with constant
   c (observed |Δc/c| ≲ 1e-18) forces the vacuum **deep** into the ordered phase,
   `J₀/J_c ≫ 1` ⇒ `m ≈ m_sat` ⇒ `Z ≈ 1` today. Since `J ∝ a⁻³` grows into the
   past, `J(z=0.5)=3.375·J₀` is **even more** ordered ⇒ `Z(z=0.5)` even closer to 1.
   The near-critical regime that S8 needs is observationally forbidden.
   **Expect: universe NOT near J_c ⇒ no suppression.**
6. **HQ2-4:** `G_eff(z)/G_N = Z(z) ≈ 1` for all observable z ⇒ σ8(HQ2) ≈ σ8(ΛCDM),
   no movement toward KiDS. **Expect death.**

---

## 5. Death criteria (pre-registered, not negotiable)

```
DEATH (Verdict C): c_eff constant in J → J_c (Route A, structural), OR
  the near-critical regime (Z<1) is observationally inaccessible because the
  photon pins J₀/J_c ≫ 1 (Route B via HQ2-3). σ8 unmoved. Frontier final.

PARTIAL (Verdict B): Z<1 exists AND could plausibly act at z~0.5–1, but the
  σ8 shift is insufficient to reach KiDS. Record as promising direction.

SUCCESS (Verdict A): Z<1 sufficiently near J_c AND the z~0.5–1 universe could
  have been in that regime AND σ8(HQ2) < σ8(ΛCDM) toward 0.77.
  ⇒ TRIPLE verification (V1 finite-size, V2 protocol, V3 σ8 two-method) before
  any claim. Most important result since E1+E2.
```
Rule: do **not** adjust `J_c` to dodge death. HQ2-3/HQ2-4 run **only if** HQ2-2 is
positive (Route B), per protocol.

---

## 6. Task map → outputs (all under `results/cosmology/hq2/`)

| Task | Question | Output |
|------|----------|--------|
| HQ2-V | ξ diverges at J_c? 2nd order? | `HQ2V_gate.md/.json/.png` |
| HQ2-1 | c_eff(J): Route A const? Route B softens? (20 seeds) | `HQ2_1_jeff.md/.json/.png` |
| HQ2-2 | Z = G_eff/G_N < 1 for some J>J_c? | `HQ2_2_geff.md/.json/.png` |
| HQ2-3 | Could the z~0.5–1 universe be near J_c? | `HQ2_3_cosmology.md/.json` |
| HQ2-4 | σ8(HQ2) vs ΛCDM/KiDS (growth ODE) | `HQ2_4_sigma8.md/.json/.png` |
| HQ2-5 | Honest synthesis + verdict | `HQ2_5_synthesis.md` |

Protocol: gate first; reuse E1/E2 motors (do not rewrite); 20 seeds for HQ2-1;
HQ2-3/4 only if HQ2-2 positive; anti-circularity throughout.
