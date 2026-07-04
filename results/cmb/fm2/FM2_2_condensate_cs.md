# FM2-2 — Velocidade do som do condensado (botão de Jeans)

> `FM2_2_condensate_cs.py` → `.{json,png}`. O(3) ordenado, L=16, 8 sementes.
> c_s = √(ρ_s/χ): ρ_s = módulo de helicidade (rigidez), χ = susceptibilidade.
> Referência c = velocidade do mágnon de E2 (=1 em unidades naturais).

## Resultado — condensado relativístico (free-streama): C3

```
J       c_s/c    ρ_s     χ        m       (J_c≈0.693)
0.72    0.14     0.070   3.83     0.371   ← perto de J_c (crítico)
0.80    0.45     0.166   0.874    0.533
0.90    0.83     0.258   0.415    0.630
1.10    1.34     0.411   0.244    0.727
1.40    2.46     0.626   0.106    0.800
1.80    3.96     0.902   0.060    0.852
2.40    6.38     1.312   0.034    0.892   ← ordem profunda
```

- **c_s/c é O(1) em toda a fase ordenada** (0.14 a 6.4). A janela de Jeans necessária
  para suprimir σ8 na escala relevante — **c_s/c ~ 1.7–3.3×10⁻³** — **não é atingida
  em lugar nenhum**. O mínimo (0.14, perto de J_c) está ~2 ordens de grandeza acima
  da janela.
- **Por quê:** o condensado de orientação é um meio **rígido** (ρ_s = O(J)) e seus
  Goldstones (perturbações) viajam a velocidade relativística — exatamente o mágnon
  c≈1 que E2 mediu, agora a densidade finita. Um meio com c_s~c **free-streama** em
  vez de clusterizar → **morte C3** (sem estrutura na escala de σ8).
- **c_s→0 só no ponto crítico:** ρ_s→0 quando J→J_c⁺ (a rigidez some na transição),
  então c_s cai. A janela de Jeans (10⁻³) só seria atingida ajustando J
  **exponencialmente perto** de J_c — fine-tuning, não genérico. E ali a ordem é
  fraca (m→0), incompatível com um condensado tipo-DM bem definido.

## A tensão estrutural (resultado honesto)

FM2-1 e FM2-2 puxam para fases **opostas**:
- **Botão 1 (realce MOND)** quer a **fase ordenada** (divergência de Goldstone em
  χ∥, mais forte com J grande).
- **Botão 2 (supressão de Jeans)** quer estar **no ponto crítico** (c_s→0 só em J_c).

Não dá para ter os dois ao mesmo tempo no mesmo J de forma genérica. O condensado
que produz MOND (ordenado, rígido) **free-streama** (c_s~c); o que poderia suprimir
σ8 (crítico, mole) não sustenta o realce MOND nem a densidade de DM. Esta é uma
**obstrução estrutural**, não um acidente numérico.

## Veredito FM2-2: **C3 para o Botão 2**

A velocidade do som do condensado de orientação é O(c) (relativística, travada pela
invariância de Lorentz R1 + mágnon E2) em toda a fase ordenada; a janela de Jeans
(c_s/c~10⁻³) só existiria sob fine-tuning crítico. **O condensado free-streama — não
fornece a supressão tipo-DM-fria que S8 precisa.**
