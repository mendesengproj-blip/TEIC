# BD5 — Synthesis: where the BD smeared route leaves the bridge

**Task.** With ε settled, re-state the full picture: operators, locked ratios, the
quartic, and the Lorentz status; give the closure scorecard and the final position.

## The closure scorecard

| Criterion | Status | Evidence |
|---|---|---|
| DEV operators present (X, √, A∂θ, quartic, F²) | **✓** | C1–C4 + W1–W4 (form-complete with plaquettes) |
| Ratios locked (C₂/C₁=1, C₃/C₁=2) | **✓** | C2; algebraic (Stückelberg square), unaffected by smearing (BD3b) |
| Strong-field quartic survives, sign<0 (DBI) | **✓** | W3; C_q≠0; smearing is 2nd-order so leaves it |
| Lorentz violation removed (E/B ≈ 1) | **✗ / not demonstrated** | BD3/BD4: λ's & a_t,a_x consistent with 0; no ε works |
| ε fixed by network geometry | **✗ (reframed)** | BD4: ε is a bias-variance regulator, not a constant |

Three of five close; the two that the BD route was meant to deliver — **Lorentz
restoration** and a **derived ε** — do **not**.

## What BD smearing did and did not do

**Did (BD1–BD2).** It correctly *diagnosed and addressed* the pathology: the sharp
action is a sum of positive terms → positive-definite second moment → can never be
$\propto g^{\mu\nu}$. The BD weight $w(m)$ alternates sign (the only network operator
that can be indefinite) and **collapses the $O(10^4)$, ratio-4 Euclidean anisotropy to
$O(0.1)$**, removing the temporal-elongation factor. The mechanism is structurally
right.

**Did not (BD3–BD4).** It did **not** positively restore Lorentz invariance at
accessible network sizes. With the summed-action estimator (the ~10× variance gain BD
prescribe), the dispersion $\lambda_{\rm space},\lambda_{\rm time}$ and the second
moment $a_t,a_x$ are all **consistent with zero**, and no ε produces the $\Box$
signature. The smeared signal is $\sim\Box/(2\epsilon\rho_{\rm eff})$ — buried under the
$\rho^{3/4}$ variance — exactly the wall e10 and Benincasa–Dowker–Glaser document, now
confirmed to also block the bridge closure.

## The honest position on the bridge

> The TEIC→DEV bridge is **form-complete but not Lorentz-closed**. Every DEV operator
> emerges from causal links + plaquettes with the Stückelberg ratios locked and genuine
> extra quartics (C/W tasks). The order-1 Lorentz violation (E/B≈3) is **identified as
> an artefact of the sharp, positive-definite operator**, and the structurally correct
> cure — the sign-alternating BD smeared operator — **removes the gross anisotropy**.
> But **positive numerical confirmation of Lorentz restoration (E/B→1) is beyond
> computationally accessible network sizes**: the smeared signal sits at SNR≈1 under the
> BD variance wall, at every ε. This is the *risk outcome* flagged in the prompt, and it
> is reported as such.

So the next layer is now **precisely located and it is computational, not conceptual**:
- the operator is identified (BD smeared, $w(m)$);
- the obstruction is identified (the $\rho^{3/4}$ variance / $\Box/(2\epsilon\rho)$ SNR);
- the route is identified (large-$\epsilon\rho$ networks, or the global summed action at
  network sizes well beyond what this machine reaches — the same regime BD/Glaser need
  for clean $\Box$ recovery).

A genuinely new, better-conditioned estimator of the smeared signal (variance-reduced
beyond $1/\sqrt N$) would be the alternative that could close it without brute-force
scale. That is the open problem this investigation hands forward.

## What did NOT change (still solid)

The non-Lorentz issue is confined to the *raw second-moment signature*. Everything that
does not depend on it stands: the operator content of the bridge, the locked 1:2 ratios,
the DBI saturation (W3), the emergence of $F^2$ from plaquettes (W1–W2), and D1's
result that the **summed** BD action yields $\Box\theta=J$ → Newtonian $GM/r$ (which
succeeds precisely because it uses the summed action on a quantity — const/linear
annihilation — that is *not* SNR-limited).

## Verdict (BD5)

> **Bridge: form-complete, Lorentz-open.** BD smearing is the right operator and removes
> the Euclidean anisotropy, but Lorentz restoration is not numerically demonstrable at
> accessible scales (SNR≈1, no magic ε). The investigation closes the *conceptual* gap
> (mechanism identified) and reduces the remaining gap to a *computational* one
> (variance wall), reported honestly rather than overclaimed.

## Output
This synthesis; data in `BD1_diagnosis_data.json`, `bd_summed_action_data.json`;
figure `BD_sharp_vs_smeared.png`.
