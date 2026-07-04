# E6-2 — photon dispersion gate H2: FAIL for the naive action (+ E6 overall status)

> Pre-registered in `E6_BD_GAUGE.md` (gate H2). Code: `E6_2_dispersion.py`; data:
> `E6_2_dispersion.json`. Flat-space validation of the photon dispersion of the
> non-compact Maxwell action S=(1/2) sum_P F_P^2 on causal diamonds. Run jun/2026.

## Result

Plane-wave 1-form symbol lambda(k,omega)=<theta,M theta>/<theta,theta> on transverse
spatial polarisations; the on-shell dispersion was taken as the omega that minimises
the symbol at each |k|:

```
k=1.37  omega*=0.29  (omega*/k=0.21)
k=1.91  omega*=0.15  (omega*/k=0.08)
k=2.46  omega*=0.05  (omega*/k=0.02)
k=3.01  omega*=0.10  (omega*/k=0.03)
k=3.55  omega*=0.39  (omega*/k=0.11)
k=4.10  omega*=0.58  (omega*/k=0.14)
fit: omega = 0.10 k (rel dev 47%)
```

The symbol minimum sits near **omega ~ 0**, not on the light cone omega=|k|. The
naive action does NOT yield a propagating photon.

## Why (the honest reason)

The hoped-for mechanism -- that an on-shell EM wave has F_{mu nu}F^{mu nu}=2(B^2-E^2)=0
so the action would vanish along omega=|k| -- requires the LORENTZIAN (indefinite)
action E^2-B^2. But S=(1/2) sum_P F_P^2 is a sum of squares: **positive-definite and
Euclidean**, minimised by STATIC (omega~0) configurations. The causal diamonds did
not reproduce the Lorentzian signature contraction (their bivector sampling does not
furnish the indefinite metric in the needed way). So H2 fails not by accident but
because the naive gauge action is Euclidean; a relativistic photon needs the
indefinite-signature Maxwell operator (electric vs magnetic with opposite sign), the
gauge analogue of the Lorentzian Benincasa-Dowker d'Alembertian that the scalar
sector (E2) required.

## Verdict H2

```
H2 FAIL (no propagation) for the naive non-compact Maxwell action: the symbol
minimum is at omega~0, not omega=ck. A relativistic photon dispersion requires a
LORENTZIAN (BD-type, indefinite-signature) gauge operator, which is NOT built here
and is the genuinely hard, open construction.
```

## E6 overall status (gauge sector of the photon search)

| Gate | Question | Result |
|---|---|---|
| H1 (E6-1) | gauge structure present? | **PASS** -- exact gauge invariance; gauge modes = N-1 (full redundancy); transverse physical sector exists. The structure E4 lacked. |
| H2 (E6-2) | relativistic dispersion omega=ck? | **FAIL** for the naive Euclidean action (minimum at omega~0). Needs the Lorentzian/BD gauge operator. |
| H3 | Coulomb 1/r? | not reached (gated behind H2). |

## Honest bottom line of the whole photon investigation (E4 -> E6)

- **E4**: orientation Goldstones are internal SCALARS, not a photon (measured).
- **E5**: U(1) Wilson on bare diamonds -- confinement question OBSTRUCTED by causal-set
  nonlocality (degree ~ L^2.9).
- **E6-1**: the link sector DOES carry the gauge structure a photon needs (H1 pass,
  gauge redundancy = N-1) -- a real positive distinguishing it from the scalar sector.
- **E6-2**: but the naive Euclidean gauge action does NOT propagate (H2 fail); a
  genuine photon needs a Lorentzian, indefinite-signature, BD-type gauge operator.

**No emergent photon has been established in any sector.** The investigation has,
instead, mapped precisely WHERE and WHY it is hard: the gauge structure is available
in the link sector, but the Lorentzian propagation requires taming the same causal-set
nonlocality the BD operator tamed for scalars -- now for a 1-form/gauge field. That
construction (the gauge Benincasa-Dowker / discrete-exterior-calculus operator with
the correct signature) is the well-defined, research-grade next step, and it has not
been faked here. The most defensible published statement remains E4's: spontaneous
orientational order + relativistic SCALAR Goldstone sector, with the photon located
(structurally) but not yet propagating in the gauge-link sector.
