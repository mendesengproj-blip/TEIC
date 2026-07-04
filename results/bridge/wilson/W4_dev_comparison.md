# W4 — Comparison with the DEV

**Task.** Compare the full action (links + plaquettes) with the DEV, operator by
operator and ratio by ratio; list genuine new predictions; state the final status.
Generator: `W4_dev_comparison.py` (reads W2; the DEV enters only here).

DEV (`docs/DEV_bridge_future.md`, eq. 1):
$$\mathcal L_{\rm DEV}=K(X,\theta)-\tfrac14F_{\mu\nu}F^{\mu\nu}-\tfrac{m_A^2}{2}A^2+\gamma A\!\cdot\!\partial\theta.$$
Full action coarse-grained (C1/C2 + W1/W2):
$$S_{\rm eff}=C_1X+C_2A^2+C_3A\!\cdot\!\partial\theta+C_q(A\!\cdot\!\partial\theta)^2+\rho\sqrt{1-X/X_0}+C_FF_{\mu\nu}F^{\mu\nu}.$$

## Operator-by-operator

| operator | full action | DEV | verdict |
|---|---|---|---|
| $X=(\partial\theta)^2$ | $C_1=\kappa n/2$ | $K(X)$ kinetic (free) | **match** (form) |
| $A^2$ | $C_2=C_1$ (locked) | $-m_A^2/2$ (free) | **match**; ratio $C_2/C_1{=}1$ locked, DEV free |
| $A\!\cdot\!\partial\theta$ | $C_3=2C_1$ (locked) | $\gamma$ (free) | **match**; ratio $C_3/C_1{=}2$ locked, DEV free |
| $F_{\mu\nu}F^{\mu\nu}$ | $C_F=\lambda_p\Pi/4$ (**emerges**) | $-\tfrac14$ (free $K$) | **match — closes C4's missing-F² gap**; weight free both sides |
| $\sqrt{1-X/X_0}$ (DBI) | link saturation (W3) | inside general $K(X)$ | **match** if $K$ is DBI-type |
| $(A\!\cdot\!\partial\theta)^2$ | $C_q\ne0$, sign $<0$ | absent | **EXTRA** → new prediction |
| $F\wedge F$ (θ-term, $E\!\cdot\!B$) | $\langle\Omega^{01}\Omega^{23}\rangle=0\pm$ (parity) | absent | absent both → consistent |
| $E/B$ Lorentz split | $2.97\pm0.03$ (raw) | $1$ | **mismatch** → order-1 LV (= C1 issue) |

## Ratios

- $C_2/C_1=1$, $C_3/C_1=2$ — **locked** by the Stückelberg perfect square (C2 task).
  DEV: free ($-m_A^2/2K'$, $\gamma/K'$).
- $C_F/C_3=\lambda_p\Pi/(4\kappa n)$ — **free** via $\lambda_p$. DEV analogue
  $(-\tfrac14)/\gamma$ — **also free** ($K$ independent of $\gamma$). So the gauge
  kinetic weight is undetermined on **both** sides: consistent, but not a prediction.

## New predictions (beyond the DEV)

1. **Gauge-invariant quartic self-interaction** $(A+\partial\theta)^4$ — including
   $(A\!\cdot\!\partial\theta)^2$, $A^2(\partial\theta)^2$, $A^4$ — absent in the DEV;
   appears in strong field / steep density gradients; its coefficient $C_q$ is fixed
   **relative** to the quadratic (not free).
2. **DBI saturation of both channels** (W3): the link DBI $\sqrt{1-X/X_0}$ **and** a
   plaquette saturation $1-\cos W$ — a "magnetic" saturation of $F^2$ at large field
   strength, absent from the polynomial DEV.
3. **Order-1 Lorentz violation** at the raw level ($E/B\approx3$, $a_t/a_x\approx3$):
   a falsifiable statement that the bare causal-set action is **not** Lorentz
   invariant; invariance is recovered only through the non-local Benincasa–Dowker
   kernel.

## Final status — **FORM-COMPLETE, CALIBRATION- AND LORENTZ-OPEN**

> With plaquettes, the action now produces **every** DEV operator ($X$, $F^2$, $A^2$,
> $A\!\cdot\!\partial\theta$) — the C4 "missing $F^2$" gap is **closed** — plus the
> locked Stückelberg ratios $(1,2)$ and extra quartics. What is **not** derived:
> (i) the gauge-sector weight $\lambda_p$ (free, exactly as the DEV's $K$ is free);
> (ii) Lorentz invariance at the raw level ($E/B\approx3$ → needs BD non-locality);
> (iii) the scale $a_0$ (C3: $X_0\propto\rho$ is UV, not $cH$).
>
> Net: the one-line action **+ plaquettes** is the gauge-invariant
> **Proca/Stückelberg + Maxwell structure** of a DEV-sister theory, with the gauge
> kinetic weight and the restoration of Lorentz invariance as the identified **next
> layer**.

This is the prompt's *"W4 reproduz DEV + predições extras"* on **form**, qualified:
the bridge does not *diverge* from the DEV (no operator the DEV needs is absent now),
but it does not *uniquely fix* the DEV either — the gauge weight and the Lorentz
restoration remain open, and the bare theory carries extra quartics and an order-1 LV.

## Output
`W4_dev_comparison.py`, `W4_dev_comparison_data.json`.
