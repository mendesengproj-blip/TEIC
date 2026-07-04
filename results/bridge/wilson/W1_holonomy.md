# W1 — Wilson loops generate F (holonomy → field tensor)

**Task.** Verify numerically that the plaquette holonomy — the sum of link phases
around a closed causal loop — reproduces the field tensor: $W/\text{area}\to F_{\mu\nu}$.
If yes, plaquettes are the correct mechanism for the Maxwell term that the link-only
action *missed* (BRIDGE_COEFFICIENTS C4). Generator: `W1_holonomy.py` +
`wilson_core.py`.

**Anti-circularity.** $F^2$ is never inserted. The only object built is the closed
line integral $W=\oint A_\mu dx^\mu$ (a sum of link phases $\phi=\int A\cdot dx$).
That $W\to\iint F\,dx\wedge dx$ by Stokes is the thing **verified**, not assumed; the
reference $F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu$ is computed only to score
against.

## Results

**(1) Constant $F$ (1+1D, $F_0=0.7$).** $W/\text{area}=F_0$ to machine precision at
*every* loop scale (rel.err $3\times10^{-12}$ for $h=0.4\dots0.05$) — exact, as it
must be for constant $F$.

**(2) Varying $F$ (1+1D, $F_{tx}=\cos t$, loop at $t_0=1$, $F=0.5403$).** $W/\text{area}\to F$
with clean **$O(\text{area})\sim O(h^2)$** convergence:

| $h$ | 0.40 | 0.20 | 0.10 | 0.05 | 0.025 |
|---|---|---|---|---|---|
| rel.err | 1.33e−2 | 3.33e−3 | 8.33e−4 | 2.08e−4 | 5.21e−5 |

(each halving of $h$ → ×¼ error: second-order, the expected Stokes discretisation).

**(3) Gauge invariance.** Under $A_\mu\to A_\mu+\partial_\mu\chi$:
- loop $W$: $-0.021540\to-0.021540$, $|\Delta|=0$ — **invariant**.
- single link phase $\phi$: $+0.0782\to+0.1422$, $|\Delta|=0.064$ — **not** invariant.

This is the decisive structural point: the *link* phase is gauge-dependent (it is the
$A^2$ / Stückelberg content), but the *loop closure* is gauge-invariant (it is the
$F^2$ content). Exactly why a single link cannot carry $F$ and a plaquette can.

**(4) Constant $F$ in 3+1D (electric + magnetic).** Per-plane $W/\text{area}=F_{\mu\nu}$
to $10^{-12}$ for the $tx$ (electric, 0.5), $xy$ (magnetic, 0.3) and $ty$ (null, 0.0)
planes.

**(5) Real sprinkled causal diamonds.** Minimal causal-diamond loops
$i\to j\to\ell\leftarrow k\leftarrow i$ built from genuine covering links of a Poisson
sprinkle (n=1545 loops, median area 0.02). With constant $F$ (so $W=\tfrac12F_{\mu\nu}\Omega^{\mu\nu}$
holds for any loop shape): **corr $=1.0000$, slope $=1.000$**. The holonomy machinery
works on real causal links.

> Note (honest): with a *varying* $F$, the same nearest-neighbour diamonds give only
> corr ≈ 0.97 — because they are long, near-null, non-compact loops (the causal-set
> **link non-locality** flagged in C1), so the linear-$F$ estimate degrades over their
> extent. That is an $F$-sampling limitation of raw causal loops, not a failure of the
> holonomy; the controlled convergence (2) already proves $W/\text{area}\to F$.

## Verdict (W1) — **PASSA**

Wilson loops generate $F_{\mu\nu}$ correctly: $W/\text{area}\to F$ (exact for constant
$F$, $O(\text{area})$ otherwise), gauge-invariant at the loop level while link phases
are not, in 1+1D and 3+1D and on real causal diamonds. The plaquette is the right
mechanism for the missing Maxwell term. → proceed to W2 (coarse-graining).

## Output
`W1_holonomy.py`, `wilson_core.py`, `W1_holonomy_data.json`, `W1_holonomy.png`.
