# C3-V -- Gate de validacao: momento de inercia do Skyrmion B=1

**Veredito do gate: PASS**

O momento de inercia rotacional I_ab do Skyrmion B=1 e reconstruido a partir
dos modos-zero de SU2_QUANT (`su2q_core.inertia_tensor`, nao modificado).

| quantidade | valor (unidades da rede) |
|---|---|
| massa classica E_class = M_Sk | 297.1681 |
| I_diag | [312.737, 312.737, 312.737] |
| I (media diagonal) | 312.7366 |
| anisotropia diag (spread) | 0.00e+00 |
| off-diagonal / I | 3.09e-18 |

**Criterios do gate (pre-registrados):**

- I finito: **True**
- I positivo (> 0): **True**
- I esferico (I_ab = I d_ab, esperado pela simetria SO(3) do hedgehog): **True**

=> I e **BEM DEFINIDO** (nao divergente, nao zero).

**Espectro de rotor a construir** (E_J = E_class + J(J+1)/(2I)):
o salto fundamental E_(j=1/2) - E_class = 1.199092e-03 (unidades da rede).

**Cross-check com SU2_QUANT (selecao de spin semi-inteiro):**
uma rotacao 2pi envia psi -> -psi com residuo
|psi(-q)+psi(q)|_max = 5.100087019371813e-16 (Q5_observables.json),
confirmando o estado fundamental j = 1/2 (constraint de Finkelstein-Rubinstein,
B=1) sobre o qual a banda rotacional e construida.

**Conclusao:** gate PASSA -> prosseguir para C3-1.
