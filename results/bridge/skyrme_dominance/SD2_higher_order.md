# SD2 — O sêxtico resgata o Skyrmion em d = 3?

> Gerador: `SD2_higher_order.py` → `SD2_higher_order.json` + `.png`.
> Pré-registro: adendo item 7. Critério pré-registrado: o resgate só é real
> se u(λ*) < 1 **e** o cosseno completo tiver mínimo interior na mesma grade.

## c₆: positivo, exato, garantido

Sexta ordem do cosseno por link: $+\frac{a^6}{46080}|\ell_e|^6$. Média
isotrópica em d = 3 (verificada simbolicamente em G diagonal via momentos
racionais exatos da esfera, e por MC com 2·10⁶ direções em G não-diagonal,
razão 0.9997):

$$\langle|\ell|^6\rangle = \frac{(\mathrm{Tr}G)^3 + 6\,\mathrm{Tr}G\,\mathrm{Tr}G^2 + 8\,\mathrm{Tr}G^3}{105}$$

Todos os termos ≥ 0 para G PSD ⇒ **c₆ > 0 sempre** (sinal estabilizador),
como pré-registrado. A oitava ordem (também verificada, divisor 945) volta a
ser negativa — a série alterna.

## O mínimo existe formalmente — e é um artefato

Derrick truncado para o hedgehog F = π e^{−u}:
E(λ) = λE₂ − C₄I₄/λ + C₆I₆/λ³ diverge em λ→0 e λ→∞, logo **sempre** tem
mínimo interior em d = 3 (algébrico: λ*² da quadrática em λ²). Medido:

| diagnóstico | valor | limiar de validade |
|---|---|---|
| λ* | 0.196 | — |
| **fase de link no mínimo u(λ*) = aπ/2λ*** | **8.0** | **< 1** |
| termo óctico / termo sêxtico em λ* | 0.55 | ≪ 1 |
| erro de truncamento vs cosseno completo em λ* | 42% | pequeno |
| cosseno completo: monotônico? | **sim** | mínimo interior exigido |

O mínimo do truncamento sêxtico fica em fase de link u ≈ 8 — oito vezes fora
do raio útil da série alternante, com a oitava ordem valendo metade da sexta
e o truncamento errando a energia em 42%. A função verdadeira (o cosseno,
limitado, que ressoma todas as ordens) é **monotônica** na mesma grade — já
medido em SC4 e DS3, reconfirmado aqui com as ordens lado a lado na figura.

## Veredito SD2: **sem ajuda do sêxtico**

c₆ > 0 com magnitude exata conhecida, mas o critério pré-registrado falha nos
dois ramos: u(λ*) = 8.0 ≫ 1 e o cosseno completo não tem mínimo interior.
O "mínimo" de c₄|φ|⁴ + c₆|φ|⁶ em d = 3 é um artefato de truncar uma série
alternante de uma função limitada na ordem em que ela é positiva. Qualquer
truncamento par estabiliza; qualquer truncamento ímpar colapsa; a ressoma
decide — e é monotônica. Consistente com DS3 (que já matou o resgate sêxtico
em d = 5 pelo mesmo mecanismo).

Reprodução: `python SD2_higher_order.py` (~1 min).
