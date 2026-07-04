# DEV bridge — future extension (internal record, NOT part of the TEIC paper)

> **Status: internal note.** This file documents a *proposed* extension and the
> soldering relation that would make the TEIC link/vector structure connect to a
> scalar–vector–tensor theory of modified gravity ("DEV"). It is **not** a claim,
> **not** part of the TEIC paper, and **not** to be added to the DEV paper while
> that paper is under review. It is a record for a possible *Paper V* of the DEV
> programme, to be considered **only after the current DEV paper is accepted**.
>
> The TEIC paper records only the **negative** result of the bridge investigation
> (see `paper/main.tex`, "A negative bridge to modified-gravity dynamics"): the
> vector bridge does **not** exist in the DEV as it currently stands. Everything
> below is the *future* direction, kept out of the public record on purpose.

---

## 0. Why this file exists

The TEIC investigation mapped the structure of fields on the causal network:

- **Nodes** carry scalar degrees of freedom → Sorkin causal d'Alembertian →
  geometry, special relativity, curvature (the established TEIC results).
- **Links** carry $U(1)$ phases → Wilson lattice-gauge structure → electromagnetism
  (structural conjecture; numerical confirmation open — Sverdlov–Bombelli 2009).

The natural question was whether the link/vector sector of TEIC could be soldered
to the vector sector $A_\mu$ of the DEV. The honest answer **in the DEV as it
stands today is: no** (three structural reasons, §1). The bridge would close only
if the DEV were extended with an explicit dilaton–gauge term $f(\theta)\,F^2$.
This file records that extension, the soldering relation it implies, and its one
potentially observable consequence.

---

## 1. Why the bridge fails in the current DEV (the negative result)

The current DEV Lagrangian for the scalar/vector sector is

$$
\mathcal{L}_{\mathrm{DEV}}
= F(X,\theta)
\;-\; \frac{K}{4}\,F_{\mu\nu}F^{\mu\nu}
\;-\; \frac{m_A^2}{2}\,A_\mu A^\mu
\;+\; \gamma\,A_\mu \nabla^\mu \theta .
$$

The proposed identification "$A_\mu^{\mathrm{DEV}} \leftrightarrow$ Wilson link
field of TEIC, coupled dilatonically" fails for three independent, structural
reasons:

1. **No dilatonic modulation.** The coefficient of $F^2$ is the *constant* $K$,
   not a function $f(\theta)$. A Wilson term whose coupling tracks the local
   network density would map to a $\theta$-dependent $f(\theta)F^2$, which is
   simply absent.
2. **Wrong coupling operator.** The existing scalar–vector coupling is of
   **Stückelberg** type, $\gamma A_\mu\nabla^\mu\theta$ — structurally distinct
   from a **dilatonic** $\theta F^2$ coupling. The two operators do not match at
   any order in a derivative/field expansion; one cannot be reabsorbed into the
   other.
3. **Inert where it matters.** In the galactic regime the field strength
   $F_{\mu\nu}=0$. A Wilson/$F^2$ term contributes nothing exactly in the regime
   where the gravitational modification is needed, so even a correct dilatonic
   term would be observationally silent there.

A separate order-of-magnitude note: the acceleration scale relation
$a_0 \sim cH$ holds to $\sim 10\%$, but it is **not derived** within the DEV as it
stands — it is a coincidence of magnitudes, recorded as such.

**Conclusion:** the vector/dilaton bridge does not exist in the current theory.
The rest of this file is the *future* extension that would create it.

---

## 2. The proposed extension: DEV-V with $f(\theta)\,F^2$

Add an explicit dilaton–gauge term, promoting the constant $K$ to a function of
the scalar:

$$
\mathcal{L}_{\mathrm{DEV\text{-}V}}
= F(X,\theta)
\;-\; \frac{f(\theta)}{4}\,F_{\mu\nu}F^{\mu\nu}
\;-\; \frac{m_A^2}{2}\,A_\mu A^\mu
\;+\; \gamma\,A_\mu \nabla^\mu \theta ,
\qquad
f(\theta) \xrightarrow[\theta\to 0]{} K ,
$$

so the current DEV is recovered as the $f(\theta)\to K$ (constant) limit and **all
existing DEV predictions are preserved** wherever $F^2$ is negligible (i.e. on the
scales already tested). On the TEIC side, $f(\theta) \propto 1/\mu_0(x) \propto
n_P(x)$, the local diamond-plaquette density, which is what a Wilson coupling
running with network density produces in the continuum limit.

---

## 3. The soldering relation

The extension makes the identification consistent provided the scalar $\theta$ is
soldered to the relative network density contrast:

$$
\boxed{\;\theta(x) \;=\; \frac{M}{\alpha}\;\frac{\rho(x)-\rho_0}{\rho_0}\;}
$$

where $\rho(x)$ is the local causal-network (sprinkling) density, $\rho_0$ a
reference (cosmic-mean) density, $M$ a mass scale, and $\alpha$ the dilaton–gauge
coupling normalisation in $f(\theta)$. The relation says: the DEV scalar field is,
on the TEIC floor, the **fractional density contrast of the causal network**. In
the low-contrast limit $\theta \propto \delta\rho/\rho_0$ is linear, recovering the
weak-field DEV behaviour.

---

## 4. Modified equations of motion

With $f(\theta)$ promoted, the vector and scalar equations of motion acquire the
dilatonic cross-terms (schematically, on a curved background $\nabla$):

**Vector ($A_\mu$):**
$$
\nabla_\mu\!\big(f(\theta)\,F^{\mu\nu}\big) \;-\; m_A^2\,A^\nu
\;+\; \gamma\,\nabla^\nu\theta \;=\; 0
\quad\Longrightarrow\quad
f(\theta)\,\nabla_\mu F^{\mu\nu}
+ f'(\theta)\,(\nabla_\mu\theta)\,F^{\mu\nu}
- m_A^2 A^\nu + \gamma\nabla^\nu\theta = 0 .
$$
The new piece is $f'(\theta)(\nabla_\mu\theta)F^{\mu\nu}$: a **directional**
coupling between the scalar gradient and the field strength.

**Scalar ($\theta$):**
$$
\frac{\partial F}{\partial\theta}
\;-\; \nabla_\mu\!\Big(\frac{\partial F}{\partial(\nabla_\mu\theta)}\Big)
\;-\; \frac{f'(\theta)}{4}\,F_{\mu\nu}F^{\mu\nu}
\;-\; \gamma\,\nabla_\mu A^\mu \;=\; 0 .
$$
The new source term $-\tfrac{1}{4}f'(\theta)F^2$ feeds field-strength energy back
into the scalar — the dilatonic channel absent from the current DEV.

---

## 5. Observable consequence: directional gravitational slip

The new term $f'(\theta)(\nabla_\mu\theta)F^{\mu\nu}$ makes the effective response
**anisotropic** in regions of strong scalar gradient $\partial_\nu\theta$ — i.e.
where $\delta\rho/\rho_0$ varies sharply: **galaxy edges and cosmic filaments**.
The gravitational slip $\eta = \Phi/\Psi$ would then carry a **directional
dependence** aligned with $\nabla\theta$, rather than being a pure function of
scale and redshift.

**Magnitude estimate.** The anisotropy amplitude scales as
$f'(\theta)\,|\nabla\theta|/(m_A^2)$ relative to the isotropic slip; with
$\theta \sim (M/\alpha)\,\delta\rho/\rho_0$ the effect is largest where
$|\delta\rho/\rho_0|$ and its gradient are both large (filament boundaries,
cluster outskirts). This is, in principle, an **anisotropy of the slip
measurable by a wide-area weak-lensing survey (e.g. Euclid)**: a slip whose value
depends on orientation relative to the local density gradient. The existing DEV
predictions are unaffected because $F^2$ is negligible on the scales already
confronted with data.

---

## 6. Timing

- This extension is for **after acceptance of the current DEV paper**.
- It is intended as **DEV Paper V**, not as an addition to the paper in review.
- Nothing here is to be cited or claimed publicly until then.
- The TEIC paper records only the *negative* bridge result (§1), described
  generically ("a scalar–vector–tensor theory of modified gravity"), without
  naming the DEV.
