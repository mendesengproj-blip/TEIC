# B1 SCAN REPORT (verbatim) — `B1_kscan.py`

K = global action rescaling S→K·S.  K ∈ [0.3, 10] (33×), 7 points.  Exponents
FITTED from the scan (not imposed).  Full data: `B1_kscan.json`.

```
M_Sk(K=1) = 173.280  (E2=164.34, E4=17.88; Bogomolny 2sqrt(E2E4)=108.42)
fitted exponents:  M_Sk ~ K^+1.000   G_net ~ K^-1.000   sigma: runs (not a clean power)
individuals scale with K (control): True
----------------------------------------------------------------------------
combination                                            K-exp       CV  flat<5%?
M_Sk * G_net  (= Poisson amplitude A; definitional)    -0.00    0.000  YES
M_Sk * sqrt(G_net)  (= M_Sk / M_Pl, THE hierarchy)     +0.50    0.563  no
M_Sk^2 * G_net                                         +1.00    1.028  no
----------------------------------------------------------------------------
sigma-combos on the MEASURED beta-window [4,6] (K in [0.8,1.2]); sigma runs ~ K^-3.22:
  sigma * G_net              CV=0.514  max/min=6.22  flat<5%? no
  M_Sk / sqrt(sigma)         CV=0.415  max/min=3.06  flat<5%? no
----------------------------------------------------------------------------
VERDICT: DEATH (well-understood). Only <5%-flat combo is the definitional
M_Sk*G_net (= amplitude A, G_net:=A/M). The hierarchy M_Sk*sqrt(G_net) (= M_Sk/M_Pl)
SCALES as K^+0.50. sigma RUNS. The overall action normalisation does NOT fix a mass
ratio between domains -> hierarchy stays [EXTERNO-B]; feeds B5.
```

Sources of the measured anchors: M_Sk radial relax (`su3_core.radial_relax`,
e_sk=0.5); G_net Poisson scan (`d3_audit_core`, reproduces D3D `G_net~1/K`);
sigma(beta) Creutz curve (`results/matter/fl1/FLC_confinement.json`).
