# Q4 — Restrição de Finkelstein-Rubinstein: j=½ selecionado para B=1

## Veredito: **SIM — FR seleciona j=½ como estado fundamental**

```
fase FR pela topologia do caminho:
  rotação 2π: termina no ANTÍPODA (q·q₀=−1.00), W=1, fase=(−1)^W = −1   ✓
  rotação 4π: termina no INÍCIO  (q·q₀=+1.00), W=2, fase=        +1   ✓
  → o path integral de B=1 pesa um laço de 2π por −1

espectro:
  fundamental sem FR:   j=0   (j inteiro permitido)
  fundamental com FR:   j=½   (multiplicidade 4 = (2j+1)²)
  E(j=3/2)/E(j=½) = 4.603   (alvo 5.0)   ✓
```

## O resultado

Para um Skyrmion B=1, um caminho fechado que executa uma **rotação de 2π** é um laço
**não-contraível** no espaço de configurações (`π₁(SO(3))=ℤ₂`): ele termina no **antípoda**
de SU(2), `q(T)=−q(0)`. Verificado diretamente: o caminho de 2π termina em `q·q₀=−1` (uma
travessia do equador, `W=1`), enquanto o de 4π retorna a `q·q₀=+1` (`W=2`). A fase de
Finkelstein-Rubinstein `(−1)^{B·W}` para B=1 dá **−1** ao laço de 2π.

Somada sobre caminhos, essa fase é a **projeção sobre funções de onda ÍMPARES** sob
`q→−q`:

```
K_FR(q_f,q_i) = K(q_f,q_i) − K(−q_f,q_i)
```

que age como `2K` nos harmônicos de S³ de grau **ímpar** (`ℓ` ímpar ⟺ `j=ℓ/2`
meio-inteiro) e **aniquila** os pares (`j` inteiro). Resultado: `j` inteiro é **removido**,
o fundamental passa a ser **`j=½`**, com multiplicidade `(2j+1)²=4`, e a razão
`E(3/2)/E(½)=4.6≈5` confirma a lei `j(j+1)` para meio-inteiros.

## Honestidade

A fase FR `(−1)^{B·W}` é o **teorema topológico** estabelecido para B=1 — não
re-derivado ab initio da ação de rede, mas **implementado** (W contado do caminho, B=1 de
SU4), não ajustado. O espectro FR usa a **projeção exata** no setor ímpar; um Monte Carlo
direto com peso `(−1)^W` sofre problema de sinal.

## Anti-circularidade

`W` é contagem topológica de cruzamentos antipodais; a fase vem dos quaternions; B=1 de
SU4. "férmion"/"bóson" só em COMPARISON ONLY. `results/matter/su2_quant/Q4_FR.{json,py}`.
