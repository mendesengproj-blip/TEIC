# CC2 -- Custo de deslocamento C(N) e tempo próprio τ(N)

Duas medições complementares:

1. **Custo kinemático** `C_kin(N) = Δt/Δx = 1 + N/n_ext` — exato, definitional.
2. **Tempo próprio** `τ(N)` = maior cadeia causal através da estrutura embutida
   num meio de Poisson (ρ=60.0), medido sobre 20 sementes
   independentes (barras de erro). τ é **genuinamente medido** e é um
   invariante combinatório do conjunto causal — candidato a `m c²`.

| N | C_kin | v_eff | τ medido (mean ± sem) |
|---|-------|-------|------------------------|
| 0 | 1.0000 | 1.0000 | 0.00 ± 0.00 |
| 1 | 1.0833 | 0.9231 | 9.95 ± 0.32 |
| 3 | 1.2500 | 0.8000 | 30.85 ± 0.60 |
| 10 | 1.8333 | 0.5455 | 103.15 ± 1.17 |
| 30 | 3.5000 | 0.2857 | 312.45 ± 1.57 |
| 100 | 9.3333 | 0.1071 | 1036.20 ± 2.64 |

## Fits do tempo próprio medido τ(N)

- Tempo próprio por loop `a = τ/N` = **10.366** links
- Fit afim `τ = 10.366 N -0.018`
- Expoente de potência `τ ~ N^p`, p = **1.008** (esperado 1.0)
- Curvatura quadrática = -0.0008 (esperado ~0)
- R² do fit proporcional `τ = a N` = **1.00000**

## VERDICT CC2: CONFIRMADO (linear)  (grade A)

The MEASURED proper time tau(N) -- the longest causal chain through the structure in the Poisson medium -- is proportional to N (exponent p=1.008, intercept consistent with 0, R^2=1.00000). Each internal cycle contributes a fixed quantum of proper time a=10.37 links; the photon (N=0) has tau=0. This is the causal rest cost m c^2 = (internal updates), grown from event counting alone.

### Honestidade

O custo kinemático C = 1 + N/n_ext é **definitional** (a definição operacional
realizada). O conteúdo genuinamente medido é τ(N): a maior cadeia causal cresce
**linearmente** com N porque cada diamante interno é uma região temporal de
tempo próprio fixo, e o passo externo é quase-nulo (τ ≈ 0). Que a maior cadeia
seja proporcional a N (e não, p.ex., a √N ou ao nº de eventos) é uma propriedade
do conjunto causal — esse é o resultado que sustenta `m c² = atualizações internas`.

![custo](CC2_cost.png)
