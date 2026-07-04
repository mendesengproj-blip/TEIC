# FM3-2 — O relíquia é frio e congelado?

> `FM3_2_freezing.py` → `.{json,png}`. Textura do quench (τ_Q=8, L=20, 20 sementes).
> (A) equação de estado w_eff via escala da energia de gradiente sob expansão.
> (B) congelamento (E3b) vs coarsening (relaxação plana).

## (A) Equação de estado: w_eff ≈ −1/3 — NÃO frio

```
ρ_grad ~ λ^(−1.85)   →   w_eff = −0.43 ± (pequeno)
```

| λ (≈ a) | ρ_grad/ρ₀ medido | λ^(−2) (textura, w=−1/3) | λ^(−3) (frio, CDM, w=0) |
|---|---|---|---|
| 1.0 | 1.00 | 1.00 | 1.00 |
| 3.0 | ~0.13 | 0.11 | 0.037 |

A densidade de energia do relíquia cai como **ρ ~ a^(−2)** sob expansão — porque uma
textura **congelada em coordenadas comóveis tem seus gradientes físicos diluídos** por
1/a. Isso é **w ≈ −1/3** (tipo textura / monopolo global de Barriola–Vilenkin), **não
w = 0** (matéria escura fria, que cairia como a^(−3)).

> **A distinção honesta e decisiva:** o relíquia é **frio de posição** (congelado, não
> se reconfigura — congelamento causal de E3b) mas **NÃO frio de pressão** (w=−1/3, não
> w=0). "Congelado por causalidade" ≠ "frio como CDM". Uma textura de orientação
> congelada tem equação de estado de textura, não de poeira.

## (B) Congelamento (super-horizonte) vs coarsening (sub-horizonte)

```
Relaxação plana (acausal) contínua após o quench:
  t=  0:  n_def = 1015      (ruído + defeitos)
  t= 20:  n_def =   56
  t= 50:  n_def =   17
  t=100:  n_def =    5.5
  t=200:  n_def =    1.9
  t=400:  n_def =    0.25
  lei de coarsening: n_def ~ t^(−1.75)  (defeitos aniquilam rápido)
```

- **Sob evolução plana (acausal), o relíquia COARSENA** — os defeitos aniquilam-se e a
  teia desaparece (n_def ~ t^(−1.75)).
- **Mas a rigidez causal de E3b (confirmada no gate) CONGELA a textura super-horizonte**:
  uma configuração maior que o horizonte causal não pode se reconfigurar (seria mais
  rápido que a luz). Então o relíquia fica **frozen enquanto super-horizonte** e só
  **coarsena depois de re-entrar** no horizonte.

Isto difere da textura **scaling** de Turok (que mantém ~fração constante da energia do
horizonte): o relíquia da TEIC é **frozen-then-decaying**, não scaling. Bom — escapa da
exclusão exata de Turok; mas o w=−1/3 permanece.

## Veredito FM3-2

O relíquia é **cosmológico** (FM3-1) e **congelado super-horizonte** (E3b) — as duas
metades da escala/posição que faltavam em FM2. **Mas sua equação de estado é w≈−1/3
(textura), não w=0 (frio).** Logo ele **não** é a componente fria-e-clusterizante tipo
CDM que S8 precisa. O destino do crescimento (suprime ou não) vai para FM3-3.
