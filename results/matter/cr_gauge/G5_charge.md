# G5 -- Conservação de carga topológica (criação em pares obrigatória)

A carga topológica é o winding líquido `Q = (1/2π)∮dφ`, calculado da fase **real**
somando os incrementos de link no ramo principal (sem ordem complexa). Com extremos
fixos, Q=0 inicialmente → a rede **impõe** que todo kink (Q=+1) venha com um
antikink (Q=−1). Matéria carregada não nasce sozinha do vácuo Q=0.

- **Colisão acoplada completa (ρ=100):** Q: +0.000 → -0.000 (|Q|máx = 0.000), kink_máx = 0 → **Q conservado = True**.
- **Colisão de gauge direta:** Q: -0.000 → +0.000 (|Q|máx = 0.000), kink_máx = 2 → **Q conservado = True**.

## VERDICT G5: SIM (carga topológica conservada)

Topological charge Q = oint dphi / 2pi is conserved to machine precision in BOTH the full coupled collision (Q: 0.000 -> -0.000, |Q|max 0.000) and the direct gauge collision (|Q|max 0.000), even though the local kink count rises to 2 (a kink-antikink PAIR). Creation is therefore in balanced pairs: a lone charged kink can NEVER be nucleated from the Q=0 vacuum -- the lattice selection rule. (COMPARISON: like QED e-/e+ pair creation under charge conservation, the TEIC analogue under winding conservation.)
