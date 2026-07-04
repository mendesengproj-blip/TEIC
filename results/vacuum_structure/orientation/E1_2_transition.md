# E1-2 — Temperatura crítica e fase ordenada do vácuo causal

> Charter: `E1_ORIENTATION.md` (E1-2). Roda porque E1-1 encontrou fase
> ordenada. Código: `E1_2_transition.py` (re-análise dos dados de 20 sementes
> de E1-1, **sem novo Monte Carlo**); dados: `E1_2_transition.json`;
> figura: `E1_2_transition.png`. **NÃO modifica nenhuma campanha anterior.**

## O que se mede

E1-1 já varreu J finamente através da transição e registrou, por (modelo, J),
o parâmetro de ordem m, a susceptibilidade χ = N(⟨m²⟩−⟨m⟩²) e a correlação de
longo alcance C(∞) = C_long. E1-2 destila isso nos observáveis da transição:

- **m(J):** parâmetro de ordem — zero (≈ 1/√N) abaixo de J_c, levanta acima;
- **χ(J):** pico localiza J_c;
- **C_long(J) vs m(J)²:** teste de clustering de Mermin (ordem genuína);
- **J_c** pelo pico de χ e pelo crossover exp→const de C(r).

Linha de base desordenada: N ≈ 2178 ⇒ 1/√N ≈ 0.022.

## Resultado

```
U(1)/XY                               O(3)/Heisenberg
 J     m      χ       C(r)             J     m      χ       C(r)
0.01  0.022  0.281  desord.           0.01  0.022  0.174  desord.
0.02  0.026  0.422  desord.           0.02  0.024  0.210  desord.
0.03  0.034  0.688  desord.           0.03  0.027  0.276  desord.
0.05  0.452  1.497  crítico (χ máx)   0.05  0.042  0.633  desord.
0.08  0.772  0.208  ordenado          0.08  0.483  0.733  crítico (χ máx)
0.13  0.882  0.082  ordenado          0.13  0.751  0.137  ordenado
0.20  0.930  0.020  ordenado          0.20  0.855  0.038  ordenado
...   →1     →0     ordenado          ...   →1     →0     ordenado
```

```
modelo  J_c (pico χ)   J_c (crossover exp→const)   onset m>5/√N   χ_max
U(1)    0.05           ≈ 0.065                     0.05           1.50
O(3)    0.08           ≈ 0.105                     0.08           0.73
```

## Tipo de transição

```
[x] 2ª ORDEM (contínua): m levanta continuamente de 0 (≈1/√N) através de
    J_c; χ tem pico finito em J_c; C(∞) salta de 0 para m² > 0.
[ ] Kosterlitz–Thouless: não — há parâmetro de ordem m > 0 genuíno com
    C(∞) = m² (não power-law sem ordem).
[ ] Nenhuma: descartada — a transição é nítida e reprodutível (20 sementes).
```

- **Parâmetro de ordem m > 0?** SIM, para J > J_c. m sobe de ≈0.022 (=1/√N,
  paramagneto) para ≈0.99 (alinhamento quase completo), continuamente.
- **χ diverge/pica em J_c?** SIM, pico finito (tamanho finito): χ_max=1.50
  (U(1)) em J=0.05; χ_max=0.73 (O(3)) em J=0.08. Acima de J_c, χ→0
  (alinhamento congelado).
- **Ordem genuína (não quasi-ordem)?** SIM: na fase `const`, C(∞)=m² a
  <2.5% — o clustering de Mermin de uma fase de quebra espontânea de simetria.
- **Ordenação física:** J_c(O(3)) > J_c(U(1)) — Heisenberg precisa de
  acoplamento maior que XY para ordenar (mais componentes para desordenar),
  exatamente como no gate 3D (3D XY J_c≈0.45 < 3D O(3) J_c≈0.69). Consistência
  interna independente.

A rede causal é 3+1D mas a propagação é essencialmente 3D — e o que se observa
é a transição **contínua de 2ª ordem** típica de um ferromagneto 3D (XY/
Heisenberg), não a transição KT de 2D. A coordenação alta (⟨grau⟩≈46, a
não-localidade dos causal sets) empurra J_c para baixo e aproxima os expoentes
de campo médio, mas a **natureza** da transição (contínua, com m e χ) é
inequívoca.

## Limites declarados

- **Classe de universalidade não medida.** Localizar expoentes críticos
  (β, γ, ν) exigiria scaling de tamanho finito com vários N — fora do escopo
  de E1-2. O que está estabelecido: J_c existe, a transição é contínua, m e χ
  se comportam como num ferromagneto 3D.
- **J_c fino.** O ponto J≈0.05 (U(1)) / 0.08 (O(3)) está na região de
  *critical slowing*; com N_burn=1000 a localização de J_c tem incerteza de
  ~um ponto da grade. A existência e o tipo da transição são robustos; o valor
  fino de J_c, não.
- **Re-análise, não nova campanha.** Todos os números vêm dos mesmos 20
  seeds de E1-1 (declarado). Nenhum MC adicional foi rodado.

## Veredito

**O vácuo causal tem uma transição de fase contínua (2ª ordem) entre um
paramagneto de orientação desordenado (J < J_c) e um ferromagneto de
orientação ordenado (J > J_c), em ambos os candidatos U(1) e O(3).** Isso
fecha P1/P2 de NIVEL4 (alinhamento espontâneo existe; há quebra de simetria)
e habilita E1-3 (o modo de Goldstone da simetria quebrada — o fóton?).
