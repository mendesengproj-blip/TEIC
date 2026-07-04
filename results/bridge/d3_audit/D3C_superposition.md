# D3-C — superposition (linearity)

> Brutal audit of D3, task C. Independent of R1–R3 / e6–e11. Reproduce:
> `python results/bridge/d3_audit/D3C_superposition.py` (~145 s).

## Question
Poisson is **linear**: $\nabla^2(\theta_1+\theta_2)=J_1+J_2$. Place two core sources a
distance $d$ apart; does $\theta_{\rm total}=\theta_1+\theta_2$ emerge?

## Two parts — and the honest split
**Part 1 (the implemented BD action).** The static Benincasa–Dowker action is
**quadratic** (NL1: no $\phi^3$/$(\nabla\theta)^2$ term), so its Euler–Lagrange equation
is the **linear** Poisson equation and superposition must be exact at every field
strength.

**Part 2 (illustrative, conditional — NOT the BD action).** The cone/clock sector
produces a DBI saturation $\sqrt{1-X/X_0}$ (NL, W3). Where that non-linearity is present,
superposition must break — only in strong field, in the **saturating** direction. We add
the DBI coefficient by hand (clearly labelled) to show what a non-linear completion does.

No $G$/$GM/r$/Schwarzschild in any generator.

## Result

**Part 1 — linear BD action** (two cores, $d=14$, grid $36^3$):
- **solver (zero MC noise): corr $=1.000000$, rms/std $=1.8\times10^{-9}$** →
  superposition is **exact**.
- genuine MC: corr $=0.859$, rms/std $=0.59$ — the difference is the independent
  sampling noise ($\sim\!\sqrt3\,\sigma$ from three separate MC means), **not** a
  superposition violation; consistent with Part-1 exact within the MC floor.

**Part 2 — illustrative DBI saturation** (strong, close sources; $X_0=7.69$): the
superposition residual $|\theta_{\rm tot}-(\theta_1+\theta_2)|$ binned by local field
strength $X/X_0$ rises **$\sim\!12\times$** from the weak bins ($0.0021$) to the strongest
bin ($0.0258$), in the **saturating direction** ($|\theta_{\rm tot}|<|\theta_1+\theta_2|$
where the field is strong).

## Verdict — **PASSA**
Superposition holds **exactly** for the implemented (linear) BD action — the network
obeys a **linear** equation (Poisson), not a non-linear one in disguise. This is the
decisive content of D3-C.

**Honest framing of the "huge result".** The prompt's hoped-for outcome — superposition
in weak field, breaking toward DBI in strong field — is realised **in two pieces, not
one action**: the BD action of D1–D3 is linear (exact superposition, Part 1), and the
DBI breakdown is a property of the **separate** cone/clock non-linearity (Part 2,
illustrative), consistent with NL1 (the BD action carries no non-linear term; the
non-linearity is the clock, not the field). We do **not** claim the implemented action
breaks superposition in strong field — it does not. Part 2 only characterises what the
non-linear completion would do, with the DBI coefficient added by hand and labelled.
