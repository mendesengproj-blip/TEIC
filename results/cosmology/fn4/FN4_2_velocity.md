# FN4-2 — Estatística de velocidade prevista ṽ(s)

> `FN4_2_velocity.py` → `FN4_2_velocity.json` + `FN4_2_velocity.png`.
> ṽ = v_obs/v_Newton = √(g_eff/g_N). M = 1.5 M_☉ (típica), s ∈ [1, 100] pc.

## A pergunta

A curva ṽ(s) da DEV diverge da curva MOND padrão abaixo de λ_A = 17.3 pc? **SIM** — a
DEV cai para ṽ → 1 (Newton) enquanto a MOND permanece reforçada (ṽ → √γ ≈ 1.16).

## Tabela ṽ(s)

```
   s [pc]  v~_Newton   v~_DEV   v~_MOND   MOND−DEV   % do boost recuperado pela DEV
      1.0     1.0000   1.0100    1.1645     0.1546     6.0%
      1.7     1.0000   1.0165    1.1645     0.1480    10.0%   (raio de maré r_J)
      5.0     1.0000   1.0437    1.1645     0.1208    26.6%
     10.0     1.0000   1.0753    1.1645     0.0892    45.8%
     17.3     1.0000   1.1068    1.1645     0.0577    64.9%   (λ_A)
     30.0     1.0000   1.1372    1.1645     0.0273    83.4%
     50.0     1.0000   1.1560    1.1645     0.0085    94.8%
    100.0     1.0000   1.1640    1.1645     0.0005    99.7%
```

- **Plateau MOND:** ṽ_MOND ≈ 1.165 (= √1.356), constante porque o EFE da MW capa o
  boost — independe de s no regime deep-MOND.
- **DEV:** sobe de ~1.0 (Newton, s ≪ λ_A) para o mesmo plateau (s ≫ λ_A), cruzando o
  meio do caminho em λ_A.

## Onde a divergência DEV-vs-MOND é máxima

A divergência ṽ_MOND − ṽ_DEV **cresce monotonicamente para s pequeno** dentro de
[1,100] pc: máxima (≈ 0.155) na borda inferior s = 1 pc, e ainda maior abaixo disso
(satura em √γ − 1 ≈ 0.165 assim que s > r_MOND = 0.034 pc e S ≈ 0). 

**Isto é central:** a maior diferença entre DEV e MOND padrão está no regime **sub-pc**
— justamente onde binárias largas ligadas existem (Chae). Ali a DEV prevê Newton
(recupera só 6% do boost a 1 pc, < 1% a 0.05 pc) e a MOND prevê reforço total. O regime
de transição em si (5–50 pc, onde a DEV recupera 27–95% do boost) é onde as curvas
*convergem* de volta — e, como anota FN4-4, é o regime onde binárias **não** ficam
ligadas (maré em r_J = 1.7 pc).

## Resultado FN4-2

**ṽ_DEV diverge de ṽ_MOND abaixo de λ_A: SIM.**
Diferença máxima no regime observável: ≈ 0.16 em ṽ (≈ 0.36 em boost γ), saturando para
s < ~poucos pc. A assinatura exclusiva (DEV → Newton, MOND → reforçado) é **maximal nas
binárias sub-pc**, não na transição — o que redireciona o teste para FN4-3 (Chae).
