# PE5 — Collision (N/A for Veredito A; confirmed, not assumed)

**Task.** The protocol runs the AH5-style collision **only if PE4 showed pinning**. PE4
found no magnitude core (`|Φ|=ρ` is the bare substrate, decoupled from the gauge sector),
so a Veredito-A "stable matter without the extra ingredient" claim is **N/A**. Rather than
assert N/A, we confirm it: drive a gauge-sector collision (two counter-propagating gauge
wavepackets that build transient flux) and check whether the emergent `|Φ|=ρ` ever develops
a persistent core anywhere along the way.

## Results (20 seeds, grid 49×16×16, V=0)

| Quantity | Value |
|---|---|
| max `\|Φ\|` core dip over the whole collision | **0.001 ± 0.002** |
| fraction of seeds where a core (dip>0.15) ever forms | **0.00** |

The gauge collision stirs the **phase** (φ̄), but `|Φ|=ρ` — the static causal-density
substrate — never develops a core. No stable structure is created by the composition
alone.

## Verdict (PE5)

> **No stable matter without the extra ingredient (N/A for Veredito A).** Because `|Φ|=ρ`
> is decoupled from the gauge dynamics, no collision can make it form a core: the maximum
> dip seen over the entire collision is 0.001 ± 0.002, and a core forms in 0% of seeds.
> The emergent composition is insufficient for matter creation — exactly as PE4 predicted.
> This is the negative half of Veredito C.

## Output
`PE5_collision.py`, `PE5_collision.json`.
