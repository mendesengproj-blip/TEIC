# BRIDGE_BD — the minimal action with BD smearing: attempted closure

> **Independent investigation.** Does **not** modify R1–R3 or e6–e11, and is not part
> of the TEIC paper. Continues [`BRIDGE_WILSON.md`](BRIDGE_WILSON.md) (W1–W4), whose W2
> left an order-1 Lorentz violation (E/B≈3). Artefacts in
> [`results/bridge/bd/`](results/bridge/bd/).

**Anti-circularity (obeyed).** The BD smeared weight $w(m)$ and the layer coefficients
$(1,-2,1)$ are the *definition* of the network operator (Sorkin 2007; Benincasa–Dowker
2010; identical to `experiments/e10`), not a fit. No Lorentz / dispersion formula enters
any generator; the signature must **emerge**. $\cos(kx)$, $\cos(kt)$ are probe fields,
not operator inputs. Main-pipeline guard untouched.

---

## The bottleneck

W2 found that $F^2$ emerges from plaquettes but with **E/B ≈ 3** (Lorentz-violating),
the same anisotropy as C1's $a_t/a_x\approx3.4$. The conjecture: the BD **smeared**
operator (which D1 used to derive $\Box\theta=J$) is the correct microscopic operator and
will remove the violation, restoring E/B → 1, with ε a network parameter.

## Verdicts

| Task | What | Verdict |
|---|---|---|
| **BD1** — diagnosis | source of the anisotropy | **Identified exactly.** Sharp action = sum of *positive* terms ⇒ second moment is **positive-definite** (eigenvalues $\{+5046,+20114\}$, a_t/a_x=3.99) ⇒ can **never** be $\propto g^{\mu\nu}$ (indefinite). Root: temporal elongation of causal links + all-positive weights. |
| **BD2** — implement $B_\epsilon$ | smeared action | **Mechanism in place.** $w(m)$ alternates sign (the only operator that *can* be indefinite); collapses the $O(10^4)$, ratio-4 Euclidean anisotropy to $O(0.1)$. |
| **BD3** — coarse-grain | moments, ratios, E/B | **Anisotropy removed, but Lorentz NOT restored.** Summed-action λ_space, λ_time and a_t, a_x all **consistent with zero** (and mis-ordered where nonzero). Ratios 1:2 hold (algebra). E/B = 1 **not** demonstrated. |
| **BD4** — determine ε | scan ε for E/B→1 | **No magic ε₀.** Lorentz signature absent at every ε; error **grows** with ε. ε is a **bias-variance regulator** (limit $\epsilon\rho\to\infty$), not a derived constant. |
| **BD5** — synthesis | closure scorecard | **Form-complete, Lorentz-open.** 3/5 criteria pass; Lorentz restoration and a derived ε do not — blocked by the BD $\rho^{3/4}$ variance wall. |

---

## The honest bottom line

**BD smearing is the structurally correct operator and it removes the pathology — but
it does not numerically close Lorentz invariance at accessible network sizes.**

- **The diagnosis is exact and valuable (BD1).** The order-1 violation is not deep
  physics: it is the unavoidable consequence of the minimal action being a sum of
  *positive* terms, whose second moment is positive-definite and therefore can never
  equal the indefinite metric. This pinpoints *why* the sharp operator fails.

- **The cure is the right one and it acts (BD2).** The sign-alternating BD weight $w(m)$
  is the only network operator that can produce an indefinite form, and it collapses the
  sharp $O(10^4)$, factor-4 anisotropy to $O(0.1)$ — the Euclidean temporal dominance is
  gone.

- **But the closure does not land (BD3–BD4).** With the summed-action estimator (the
  ~10× variance reduction BD prescribe), the Lorentzian dispersion ($\lambda_{\rm space}>0$,
  $\lambda_{\rm time}<0$) and the indefinite second moment do **not** emerge: every
  quantity is consistent with zero, at every ε. The smeared signal is
  $\sim\Box/(2\epsilon\rho_{\rm eff})$ — buried under the $\rho^{3/4}$ variance, exactly
  the wall e10 and Benincasa–Dowker–Glaser document. SNR ≈ 1 throughout.

This is the **risk outcome the prompt anticipated** ("se não resolver: identifica a
próxima camada"), reported straight rather than dressed as success.

## Where this leaves the bridge

```
TEIC causal network
  → S = Σ Δτ[1−cos(φ+Δθ)]  + λ_p Σ[1−cos W_p]      all DEV operators present   ✓
  → ratios locked (1, 2); strong-field quartic; F² from plaquettes              ✓
  → order-1 Lorentz violation (E/B≈3)  = artefact of the SHARP positive operator (BD1)
  → cure = BD smeared (sign-alternating w(m))     removes the anisotropy        ✓ (mechanism)
  → positive E/B → 1                               NOT demonstrable: SNR≈1 wall  ✗ (scale)
```

The remaining gap is now **precisely located and computational, not conceptual**:
- the operator is identified (BD smeared $w(m)$),
- the obstruction is identified (the $\Box/(2\epsilon\rho)$ SNR under $\rho^{3/4}$ noise),
- the route is identified (large-$\epsilon\rho$ networks beyond this machine, the same
  regime BD/Glaser need for clean $\Box$ recovery — or a new variance-reduced estimator).

What stands unaffected: the bridge's **operator content**, the **locked 1:2 ratios**,
the **DBI saturation** (W3), the **emergence of $F^2$** (W1–W2), and **D1's success**
($\Box\theta=J\to GM/r$) — which works precisely because it uses the summed action on a
quantity (const/linear annihilation) that is *not* SNR-limited.

> **Net:** the conceptual bridge is closed (every operator derived; the Lorentz
> violation explained as a sharp-operator artefact with the correct cure identified);
> the *quantitative* Lorentz closure is an open computational problem, not a flaw in the
> structure. Honest either way.

---

## Artefacts

| file | content |
|---|---|
| [`results/bridge/bd/BD1_diagnosis.md`](results/bridge/bd/BD1_diagnosis.md) | positive-definite sharp moment; exact diagnosis |
| [`results/bridge/bd/BD2_action.md`](results/bridge/bd/BD2_action.md) | BD smeared operator; sign alternation; anisotropy collapse |
| [`results/bridge/bd/BD3_moments.md`](results/bridge/bd/BD3_moments.md) | summed-action dispersion + second moment; Lorentz not resolved |
| [`results/bridge/bd/BD4_epsilon.md`](results/bridge/bd/BD4_epsilon.md) | ε scan; no magic ε₀; bias-variance regulator |
| [`results/bridge/bd/BD5_synthesis.md`](results/bridge/bd/BD5_synthesis.md) | scorecard; form-complete, Lorentz-open |

Shared: `bd_core.py` (operator), `bd_summed_action.py` (estimator), `BD1_diagnosis.py`;
figure `BD_sharp_vs_smeared.png`. Reproduce:

```
python results/bridge/bd/BD1_diagnosis.py
python results/bridge/bd/bd_summed_action.py
python results/bridge/bd/make_figures.py
```
