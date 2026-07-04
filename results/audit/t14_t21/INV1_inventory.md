# INV1 — inventory of T14–T21BIS

> Audit of `../TEIC-GE/results/teic_st/T14/` ("matter = causal connectivity").
> Independent of TEIC R1–R3 / e6–e11. Reproduce nothing destructive: all reads only.

## Location and tooling
All T14–T21BIS files live in **one directory**: `../TEIC-GE/results/teic_st/T14/`
(the *scalar-tensor* `teic_st` phase — the same phase `AUDIT_GEMINI.md` already flagged
as the lighter, partly-circular one, distinct from GE's clean `teic_fundamental`).
Shared tooling: `../TEIC-GE/src/causal_core.py` + `wilson_core.py` — a **fork of TEIC's
core** (per `AUDIT_GEMINI.md` A1); `causal_core.py` is clean ("no SR/GR formulas"). Most
T-scripts, however, re-define their own inline `get_causal_adj` rather than import the
core.

## File census
28 Python generators (32–118 lines each; **median ≈ 60 lines**), 19 Markdown docs
(8 `*_RESUMO_FINAL.md` conclusions + 11 sub-notes), 6 PNG plots. Total Python ≈ 1500
lines. No JSON data dumps, **no test/guard file, no error bars in any original script**,
seeds either fixed at `42` or **absent** (`np.random.default_rng()` unseeded →
non-reproducible). This matches the "fast because lighter" signature of `AUDIT_GEMINI`.

## Calculation → conclusion map

| T | What was CALCULATED (the computation) | What was CONCLUDED (the claim) | directness |
|---|---|---|---|
| **T14A/B/F** | catalog of 4 hand-built structures (chain/tree/diamond/dense); "transport cost" = #links to a Δt-shifted copy; correlations cost vs N, L, N/L, entropy | "inércia = custo de manutenção de identidade"; $m\propto N/L$ | **indirect** — correlations of hand-built shapes; "mass" never tied to F=ma |
| **T14C/D/E/G** | analytic EFT phenomenology (BH hair, GW, $a_0(z)$, falsification matrix) | TEIC-ST "tensionada" by EHT/pulsars | **analytic argument**, no network calc; honest about tension |
| **T15** | $N/L$, $\langle k\rangle$, cost on random diamonds, dim 2/3/4 (unseeded, single shot) | $N/L$ falsified; $m\propto\langle k\rangle$ "universal" (cost/$\langle k\rangle\approx$0.24–0.29) | **indirect** — cost & $\langle k\rangle$ both count links/event |
| **T16** | inertial cost vs "gravitational flux" to a fixed light-cone point vs scale | equivalence principle $m_{in}=m_{gr}$ "confirmed" | **indirect** — two link-counts both $\propto$ cluster density |
| **T17A/B** | $\langle k\rangle(r)$ profile; solve **hard-coded** radial Poisson on excess $\langle k\rangle$ | "Schwarzschild emerges", corr 0.86 with $1/r$ | **circular** — Poisson is coded; $1/r$ is the Green's function |
| **T18A/B/C** | #links between a Gaussian blob and its hand-shifted copy vs $v$ | time dilation $1/\gamma$, length contraction, $m(v)$ | **coincidental** — fits a Gaussian overlap better than $1/\gamma$ |
| **T19** | same blob-overlap; define $E=1/\text{rate}$, $P=Ev$ | $E\propto\gamma$, $E^2-P^2=m^2$, "$E=mc^2$" | **definitional** — relabel + loose $\gamma$ fit |
| **T20A–D** | catalog/spectra of hand-built helices; rotate blob w/ arctan2 offset, count paths | spin-1/2, helicity = charge, "matter is topology" | **interpretive** — imposed topology; no periodicity/spin test |
| **T21/T21E/G** | spectral entropy + clustering of hand-built classes; coarse-graining stability | "quantized particle families ≈ Standard Model" | **descriptive** — clustering of structures chosen by hand |
| **T21BIS** | winding/chirality of helices; $k_{tot}$ of two helices vs separation | quantum numbers, Pauli exclusion emerge | **interpretive** — link saturation of two fixed curves |

## First read
The **direction** is consistent (connectivity correlates with inertia-like and
gravity-like quantities), but the path from calculation to conclusion is **long** in
every case: the computations are small, single-shot, error-bar-free measurements of
**hand-built** structures or **hand-imposed** velocities, and the strongest claims
(spin, Pauli, Standard Model, "$E=mc^2$") are interpretive labels on those measurements.
Two results (T17 gravity, T18 time) re-tread TEIC's own R1–R3 / D1–D3 with less rigor.
INV2 reproduces the load-bearing ones; INV3–INV6 grade them.
