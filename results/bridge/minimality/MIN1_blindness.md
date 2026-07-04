# MIN1 — A cegueira universal de U(1): teorema + medição

> Task MIN1 of `MINIMALITY_SU2.md`. Fecha o loophole dos harmônicos de ordem
> superior deixado por PHI_EMERGE V4. Data: `MIN1_blindness.json`.

## Verdict: **o custo de núcleo é ZERO EXATO para toda a classe de ações U(1)** — o winding existe geometricamente (fluxo 2π medido) e é energeticamente invisível

```
fluxo geométrico no núcleo (soma não-enrolada):  2π exato  (winding number 1.0)
elemento de grupo W no núcleo:                   0.0 exato
custo de núcleo:  1−cos(W):  0.0       1−cos(2W): 0.0
                  1−cos(3W): 0.0       série aleatória de 6 harmônicos: 0.0
```

## O teorema (agora fechado, não só o caso n=1)

Qualquer ação de gauge invariante em U(1) **compacto** é função do elemento de
grupo da holonomia — necessariamente 2π-periódica no ângulo. O vórtice carrega
fluxo geométrico 2π pela plaqueta do núcleo, mas o elemento de grupo lá é
exp(i2π) = identidade: **f(W_core) = f(0) = 0 para toda f da classe.** V4 mediu
isso para f = 1−cos W; MIN1 verifica que cos 2W, cos 3W e qualquer série de
harmônicos são igualmente cegos — não há ação de classe em U(1) que pinte o
núcleo. O resíduo de V4 é **irredutível dentro de U(1)**, não um acidente da
forma mínima da ação.

## Por que SU(2) escapa estruturalmente

A carga do Skyrmion **não é uma holonomia de loop**: é o índice de volume
B = −(1/2π²)∫det(c_x,c_y,c_z) (`su2_core.baryon_density`) — um funcional dos
gradientes, não do elemento de grupo de um circuito. O teorema da cegueira
simplesmente não se aplica a ela. A rota não-abeliana não é uma preferência:
é a única saída da classe cega.

## Honestidade

- O teorema vale para U(1) compacto (ângulos). U(1) não-compacto (W real, ação
  W²) veria o fluxo — mas não é um grupo de gauge compacto de links e
  reintroduziria exatamente o custo de núcleo "não-cosseno" que a fronteira
  V4/SC4 já nomeia como o ingrediente externo.
- Grade ideal (vórtice analítico), sem sprinkling: o resultado é exato por
  construção e é isso que um teorema pede; a versão Poisson está em V4.
