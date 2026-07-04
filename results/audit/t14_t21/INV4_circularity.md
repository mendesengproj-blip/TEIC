# INV4 — anti-circularity checklist

> For each load-bearing experiment: what was in the *generator*? was any
> mass/energy/relativity formula injected and then "observed"? was there a guard?

## Per-experiment checklist

| experiment | forbidden formula in generator? | circular? | notes |
|---|---|---|---|
| T14/T15/T16 (mass/equiv.) | none ($\langle k\rangle$, cost are pure link counts) | **no** | clean inputs; the issue is tautology + no error bars, not circularity |
| T17B (Schwarzschild) | **yes** — the **Poisson operator is hard-coded** in `solve_poisson_radial` | **YES (structural)** | $1/r$ is the coded 3D Green's function; any central source gives it (INV2 R-GRAV). The metric/Poisson is exactly the kind of "background geometry" that must not then be sold as "1/r emerges". |
| T18A/B/C (relativity) | $\gamma=1/\sqrt{1-v^2}$ present | **no (comparison only)** | $\gamma$ is the dashed "theoretical" overlay; the measured blob-overlap is independent. **But** $v$ is imposed by hand and the curve fits a Gaussian, not $\gamma$ (INV2 R-REL). Not circular, not a derivation. |
| T19 (energy/momentum) | $\gamma$ present (comparison) | **no** | same as T18; $E\equiv1/\text{rate}$ is a definition, $E^2-P^2$ "invariance" is asserted within large discrete error |
| T20 / T21 / T21BIS (spin/particles) | none | **no** | structures (helices/braids) are **hand-drawn**; conclusions are interpretation, not injected formulas |

## The cardinal-sin test (TEIC's own guard)
TEIC's `tests/test_no_circularity.py` forbids `sqrt(1-beta^2)`, `gamma=1/sqrt(...)`,
`sqrt(1-2M/r)` in **generators**. Applying the same standard to T14–T21:
- **T18/T19 would pass** (γ lives only in comparison/plot overlays).
- **T17B is the gray case**: it does not inject $\sqrt{1-2M/r}$, but it **codes the
  Poisson equation itself** and then reports "$1/r$ emerges" — the discreteness-geometry
  analogue of the sin. By TEIC's own standard (metric/Laplacian is allowed as background
  but must not be sold as an emergent result), T17's *conclusion* over-reaches even
  though the *code* would not trip the regex.

## No guard, and the speed signal
- **There is no `test_no_circularity.py` (or any test) in the `teic_st` phase.** The
  experiments were never run under an automated anti-circularity guard.
- **Scale / speed.** Every generator is 32–118 lines, one numpy pass, $n=30$–$1000$
  events, **single seed (42) or unseeded, zero error bars**. This is exactly the
  "fast because lighter" pattern `AUDIT_GEMINI.md` documented for GE's non-fundamental
  phases — and `AUDIT_GEMINI` already found the `teic_st`/`teic_np` phases to contain
  hand-coded physics (the MOND law, $\rho(r)=\rho_0(1+2M/r)$, $a_0$ in units of $c/T$).
  T14–T21 belongs to that same phase.

## Bottom line
Only **one** experiment is structurally circular (T17B, via the hard-coded Poisson).
The relativity set is **not** circular but is a non-derivation. The rest use clean
inputs. The systemic weakness is **not** injected formulas — it is the **absence of a
guard, of seeds, and of error bars**, combined with conclusions that outrun the code.
