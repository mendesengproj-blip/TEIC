# SC1 — Analytic expansion of the SU(2) link cosine to fourth order

> Task SC1 of `BRIDGE_SU2_COEFF.md`. All five identities verified (sympy symbolic
> + su2_core quaternion numerics). Data: `SC1_expansion.json`. Derivation in
> `SC1_expansion.tex` (ready for Paper II if the campaign closes positive).

## Verdict: **the fourth order of the link cosine, Poisson-averaged, CONTAINS the Skyrme operator** — with a locked ratio and a positive (stabilising-sign) coefficient; the cubic lattice is exactly blind to it

## The derivation (verified step by step)

**1. Single link = single cosine** (verified to 3e-15 by composing 64 engine steps):
for a link of length $a$ in unit spatial direction $e$, with chiral currents
$c_\mu = U^{-1}\partial_\mu U$ (su(2) 3-vectors), the holonomy is
$\Omega = \exp(aL_e)$, $L_e = i\,(\ell_e\cdot\sigma)/2$, $\ell_e = c_\mu e^\mu$, and

$$1 - \tfrac12\mathrm{Tr}\,\Omega \;=\; 1 - \cos\!\big(\tfrac{a|\ell_e|}{2}\big)
\;=\; \frac{a^2|\ell_e|^2}{8} \;-\; \frac{a^4|\ell_e|^4}{384} \;+\; O(a^6).$$

**2. Isotropic fourth moment** (symbolic, exact): with $G_{\mu\nu}=c_\mu\!\cdot c_\nu$,

$$\big\langle |\ell_e|^4 \big\rangle_{e\,\in\,S^2}
= \big\langle (e^\top G\, e)^2 \big\rangle
= \frac{(\mathrm{Tr}\,G)^2 + 2\,\mathrm{Tr}(G^2)}{15}
= \frac{3S - 2K}{15},$$

with $S=(\mathrm{Tr}G)^2$ (symmetric quartic) and

$$K = (\mathrm{Tr}G)^2 - \mathrm{Tr}(G^2)
= \sum_{\mu\nu}|c_\mu \times c_\nu|^2
\quad\text{(the Skyrme operator; symbolic identity verified).}$$

The engine commutator of pure quaternions **is** the cross product
($q_\mu q_\nu - q_\nu q_\mu = (0,\,-2\,c_\mu\!\times c_\nu)$, error 0.0), so $K$ is
the cross-product (commutator) invariant — zero in any Abelian (collinear) sector.

**3. The emergent quartic** (per link, Poisson measure):

$$\boxed{\;E^{(4)} = -\frac{a^4}{384\cdot15}\,(3S - 2K)
= \underbrace{-\frac{3a^4}{5760}\,S}_{\text{saturation (DBI)}}
\;+\; \underbrace{+\frac{a^4}{2880}\,K}_{\text{Skyrme, stabilising sign}}\;}$$

**4. The cubic lattice is blind.** A 3-axis link sum sees only
$\sum_i G_{ii}^2$ — no cross-direction terms, hence no $K$. This is why the
MATTER_SU2 cubic-grid campaign had to add the Skyrme term by hand: **the operator
is not absent from the theory; it is absent from the lattice measure.** Poisson
isotropy — the same ingredient that gives Lorentz invariance in R1 — is what
generates it.

**5. The gauge-plaquette channel is not the source.** For constant non-commuting
links the holonomy deficit is $1-\cos(a^2|f|/2)$ with $f$ the commutator vector
(ratio to $(a^4/8)|c_\mu\times c_\nu|^2$ measured $0.99995\pm2\times10^{-5}$): the
commutator enters **inside** $|F|^2$ at second order, and the fourth-order term in
$F$ is the symmetric $(|F|^2)^2$. In the soliton sector Stückelberg screening sends
$F\to0$, so the plaquette does not supply the Skyrmion's quartic. The chiral link
channel (above) does.

## Consistency with earlier campaigns

- **U(1) limit:** collinear currents ⇒ $K=0$ ⇒ pure negative symmetric quartic —
  exactly W2's "quartic survives, sign < 0 = DBI". The U(1) result is the $K=0$
  slice of the boxed formula.
- **Locked ratio:** $K\!:\!S = +2:-3$ is forced by isotropy alone (any isotropic
  link measure, any radial weight), the same way the Stückelberg ratios (1,2) were
  algebraically forced in C2. What isotropy cannot do is flip the **net** sign:
  $\mathrm{Tr}(G^2)\ge(\mathrm{Tr}G)^2/3 \Rightarrow K\le\tfrac23 S \Rightarrow
  3S-2K\ge\tfrac53 S>0$ — the net quartic is always negative (saturating). This
  bound is the pre-registered risk that SC4 tests.

| identity | method | result |
|---|---|---|
| (i) composition → single cosine | engine, 64 steps × 20 draws | max err 3.0e-15 |
| (ii) $\langle(e\!\cdot\!u)^2(e\!\cdot\!v)^2\rangle = [u^2v^2{+}2(u\!\cdot\!v)^2]/15$ | sympy | exact |
| (iii) $\langle|\ell_e|^4\rangle = (3S-2K)/15$ | sympy | exact |
| (iv) $K=\sum|c_\mu\times c_\nu|^2$; engine commutator = cross | sympy + engine | exact / 0.0 |
| (v) plaquette quartic symmetric in $F$ | engine, $a\to0$ | ratio 0.99995±2e-5 |
