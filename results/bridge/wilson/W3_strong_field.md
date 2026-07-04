# W3 — Strong field: the regime map

**Task.** With both terms present
($S=\sum_{\rm links}\Delta\tau[1-\cos(\phi+\Delta\theta)]+\lambda_p\sum_{\rm plaq}[1-\cos W_p]$),
push the field to large amplitude and map which term dominates and how each behaves —
the quartic (link/DBI channel) vs $F^2$ (plaquette channel). Generator:
`W3_strong_field.py` (1+1D, n_links≈28 000, n_plaq≈16 000; no DEV).

## The decisive physical fact

$1-\cos$ is **bounded in $[0,2]$**. Nothing can explode. Each term **saturates**.
The two terms are sums of **different operators**, so they cannot cancel. The
relative size is set by the free weight $\lambda_p$ and the link/plaquette counts.

## Scalar channel ($A=0$, $\theta$-gradient ↑) — quartic → DBI

| amplitude Θ | 0.05 | 0.20 | 0.80 | 1.60 | 3.20 | 6.40 | 12.0 |
|---|---|---|---|---|---|---|---|
| $S_{\rm link}/S_{\rm quad}$ | 0.998 | 0.970 | 0.657 | 0.326 | 0.121 | 0.038 | 0.012 |
| saturation fraction | 0.001 | 0.020 | 0.217 | 0.430 | 0.639 | 0.800 | 0.920 |

The action falls progressively below its quadratic value — the **quartic
$-\tfrac1{24}(\phi+\Delta\theta)^4$ is the leading (negative) correction** — and then
saturates toward $S_{\rm link}^{\max}=n_{\rm links}\langle\Delta\tau\rangle$ (≈2963).
This is exactly the **DBI $\sqrt{1-X/X_0}$ saturation** of the NL work, now seen
directly: weak field = $X=(\partial\theta)^2$; growing field = quartic; strong field =
saturation. (`W3_strong_field.png`, left.)

## Gauge channel ($\theta=0$, $A$ ↑) — both channels saturate

| amplitude | 0.05 | 0.40 | 0.80 | 1.60 | 3.20 | 6.40 | 12.0 |
|---|---|---|---|---|---|---|---|
| $S_{\rm link}(\phi)$ | 18.8 | 583 | 1052 | 1663 | 2287 | 2793 | 2940 |
| $S_{\rm plaq}(W),\ \lambda_p{=}1$ | 7.3 | 348 | 831 | 1619 | 2740 | 4343 | 6168 |
| plaq/link | 0.39 | 0.60 | 0.79 | 0.97 | 1.20 | 1.56 | 2.10 |

Both grow from their quadratic ($A^2$ and $F^2$) forms and then **saturate** toward
their own ceilings ($n_{\rm links}\langle\Delta\tau\rangle\approx2963$ and
$\lambda_p\,n_{\rm plaq}\approx16013$). Neither explodes; they do not cancel. The
**hierarchy is set by $\lambda_p$**: at $\lambda_p=1$ the link channel leads at weak
field and the plaquette channel overtakes at strong field; at $\lambda_p=10$ the
plaquette ($F^2$) channel dominates throughout. (`W3_strong_field.png`, right.)

## Coherence test — the three possibilities

- **Cancel?** No — different operators ($(A\cdot\partial\theta)^2$ vs $(\partial A)^2$).
- **Explode?** No — $1-\cos\le2$ bounds every term; both saturate.
- **Hierarchy?** Yes — clean, controlled by $\lambda_p$ and the counts.

So the answer is the benign one: **a well-defined limit structure**. Weak field:
$X+F^2$ (both quadratic). Strong field: DBI saturation (links) coexisting with
plaquette saturation ($F^2$). The quartic is a genuine sub-leading nonlinearity, not a
pathology.

## Verdict (W3)

> Bounded cosine ⇒ **no explosion**; both channels **saturate**; distinct operators ⇒
> **no cancellation**. The full action has a clean weak-field ($X+F^2$) → strong-field
> (DBI + plaquette saturation) crossover, with the link/plaquette hierarchy set by the
> free $\lambda_p$. This matches the honest expectation: the quartic does **not**
> disappear, and $F^2$ dominates wherever $\lambda_p$ (the gauge sector weight) is
> large — i.e. it is a tunable hierarchy, not a prediction.

## Output
`W3_strong_field.py`, `W3_strong_field_data.json`, `W3_strong_field.png`.
