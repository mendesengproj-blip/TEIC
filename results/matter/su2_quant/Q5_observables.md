# Q5 — Observáveis de spin-½: rotação 2π → −ψ e degenerescência

## Veredito: **SIM — 2π→−ψ (5e-16) e 2 estados de spin (multiplicidade 4)**

```
1 rotação 2π (q→−q): autovetor fundamental FR  ψ(−q)+ψ(q) = 5.1e-16  → ψ → −ψ   ✓
  verificação harmônica: grau 1 (j=½) ÍMPAR err=0.0   grau 2 (j=1) PAR err=0.0  ✓
2 multiplicidade do fundamental FR = 4 = (2j+1)² para j=½  (= 2 spin × 2 isospin)  ✓
  2 estados de spin (m = ±½)
  dois Skyrmions: ½ ⊗ ½ = 0 ⊕ 1 → 4 estados
```

## O resultado

Se FR (Q4) torna o fundamental `j=½`, dois observáveis devem seguir — e seguem:

1. **Rotação de 2π → −ψ.** As funções de onda `j=½` são os harmônicos de S³ de grau 1
   (ímpares). Tomando o **autovetor fundamental do núcleo FR** numa amostra de S³
   pareada por antípodas, verifica-se `ψ(−q) = −ψ(q)` a **precisão de máquina
   (`5e-16`)**: uma rotação de 2π (`q→−q`) envia o estado para **menos ele mesmo**. (Um
   estado `j=1`, grau 2 par, daria `+ψ` — confirmado: grau 1 ímpar, grau 2 par,
   exatamente.) Este é o sinal de spin semi-inteiro — agora **derivado do autovetor**,
   não inserido.

2. **Degenerescência.** O nível fundamental FR é **4-fold** `= (2j+1)² = 4` para `j=½`,
   decomposto como **2 spin × 2 isospin** (o hedgehog trava spin = isospin). São, em spin,
   `2j+1 = 2` estados (`m = ±½`). A adição de dois Skyrmions, `½ ⊗ ½ = 0 ⊕ 1`, dá os
   `2×2 = 4` estados esperados.

## Anti-circularidade

`ψ` é autovetor real do núcleo FR; a troca de sinal é **lida** do autovetor.
"spin-½"/"férmion" só em COMPARISON ONLY.
`results/matter/su2_quant/Q5_observables.{json,py}`.
