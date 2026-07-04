# SU5 — O termo de Skyrme emerge do quártico C4?

## Veredito: **NÃO — Skyrme é um terceiro ingrediente (não-Abeliano), não o quártico C4**
## (mas: estabilidade de Derrick com Skyrme = **SIM**, E₂=E₄, ver SU3)

```
quártico da ação de link:  −(1/24)(X₁²+X₂²+X₃²)²   → SIMÉTRICO (4ª potência perfeita)
Tr[L_i,L_j]²             = −8 |a_i × a_j|²          → ANTISSIMÉTRICO (produto vetorial)
                           (verificado a erro 0.0e+00 via álgebra de quaternions)
limite Abeliano (colinear): |a × a| = 0  → Skyrme ≡ 0
numérico: E₄(σ₃ Abeliano)=0.0   E₄(hedgehog não-Abeliano)=47.9
```

## A análise honesta

Derrick (SU3) mostrou que o hedgehog é estabilizado por um termo de 4 derivadas cuja
imagem de rede é o comutador de Skyrme `|c_i×c_j|²`. **É o mesmo operador que C4
identificou emergindo da ação mínima?**

**C4** (results/bridge/coefficients) expandiu a ação de link U(1) `1−cos(u)`,
`u=(A+dθ)·e`, até 4ª ordem e leu o quártico `(A+dθ)⁴` — uma **4ª potência perfeita**
do covetor de Stueckelberg, i.e. o quártico **simétrico** `(w·w)²` (o termo
DBI/k-essência `X²`, que casa com `F₂` da DEV).

**O termo de Skyrme** é `Tr[L_μ,L_ν]²`, `L_μ=U⁻¹∂_μU`. Na base `i·σ`,
`L_μ=i a_μ·σ`, e a álgebra de quaternions dá (a erro de máquina)

```
Tr[L_μ,L_ν]² = −8 |a_μ × a_ν|²   — o produto VETORIAL (ANTISSIMÉTRICO).
```

Esse comutador **anula-se identicamente** para correntes colineares (Abelianas)
`a_μ ∥ a_ν`. Confirmação numérica direta na rede: um campo quiral embebido em σ₃
(Abeliano) tem `E₄ = 0` exatamente, enquanto o hedgehog não-Abeliano tem `E₄ = 47.9`.

**Conclusão.** O quártico C4 é simétrico `(A+dθ)⁴`; o Skyrme é o comutador
antissimétrico `|a×a|²`, **identicamente zero no setor Abeliano que C4 analisou**.
Logo o termo de Skyrme **não emerge do quártico C4** — é um operador de 4 derivadas da
**mesma ordem**, porém **genuinamente não-Abeliano**, fornecido pelo **comutador de
grupo** (a curvatura de plaqueta não-Abeliana `F = dA + [A,A]`), não pelo quártico de
link de C4.

Reportado honestamente: **terceiro ingrediente** (estrutura não-Abeliana). Não é um
axioma adicionado à mão no sentido U(1) — surge inevitavelmente do produto de grupo
SU(2) — mas também **não** é o operador que C4 derivou. A estabilização de Derrick que
ele fornece (E₂=E₄) é real (SU3).

## Anti-circularidade

Prova por álgebra de quaternions (real, sem Pauli, sem complexo). C4 citado só em bloco
COMPARISON ONLY. `results/matter/su2/SU5_skyrme.json` + `SU5_skyrme.py`.
