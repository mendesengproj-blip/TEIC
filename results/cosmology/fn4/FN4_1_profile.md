# FN4-1 — Perfil analítico do MOND blindado g_DEV(r)

> `FN4_1_profile.py` → `FN4_1_profile.json` + `FN4_1_profile.png`.
> M = 1 M_☉, a₀ = 1.2×10⁻¹⁰ m/s², λ_A = 17.3 pc (fixos).

## A pergunta

O perfil g_DEV(r) = g_N·[1 + (ν_eff−1)·(1−e^{−r/λ_A})] mostra uma transição limpa em
r = λ_A = 17.3 pc, de Newton (r < λ_A) para MOND (r > λ_A)? **Resposta: SIM.**

## Escalas do problema

```
λ_A           = 17.3 pc          (comprimento de correlação de m_A — input)
r_MOND(1 M☉)  = 0.0341 pc = 7031 au   (onde g_N = a₀; MOND só age além disto)
g_ext (MW)    = 1.79 a₀          (campo externo; cap do EFE)
γ_plateau     = ν_RAR(g_ext/a₀) = 1.356   (boost MOND assintótico, capado pelo EFE)
```

A hierarquia é r_MOND (0.034 pc) ≪ λ_A (17.3 pc): há toda uma década e meia onde MOND
**estaria** ativo (g_N < a₀) mas a DEV o **blinda**.

## Perfil (boost g/g_N) nos checkpoints

```
   r [pc]     S(r)   g_DEV/g_N  g_MOND/g_N   regime
    0.050   0.0029     1.0010     1.3457     binárias de Chae  → DEV ≈ Newton
    1.700   0.0936     1.0333     1.3561     raio de maré r_J  → DEV ≈ Newton
   17.300   0.6321     1.2251     1.3561     λ_A (transição)   → meio do caminho
  100.000   0.9969     1.3550     1.3561     galáctico         → DEV = MOND
 1000.000   1.0000     1.3561     1.3561     galáctico         → DEV = MOND
```

- **S(λ_A) = 0.6321 = 1 − 1/e** exatamente — a definição da transição.
- Para r ≪ λ_A o boost da DEV cai para ~1 (Newton puro); o reforço MOND é blindado.
- Para r ≫ λ_A o boost satura em γ ≈ 1.356 (MOND padrão capado pelo EFE da MW).

## Por que o EFE (campo externo) importa

Sem o campo externo da Via Láctea, ν divergiria (em deep-MOND ν ∝ r), e o boost
cresceria sem limite. Com g_ext ≈ 1.8 a₀, o boost satura em γ ≈ 1.36 — exatamente a
ordem do que binárias largas medem (Chae: γ = 1.43). O EFE é o que torna a previsão
**quantitativa e comparável aos dados**.

## Leitura física

A figura (`FN4_1_profile.png`, painel direito) mostra a curva-assinatura: o boost MOND
(tracejado, ~1.36 em toda escala onde g_N < a₀) é multiplicado pela coerência S(r),
produzindo a curva DEV (sólida) que **adere a Newton até ~alguns pc e só sobe para MOND
perto de 17.3 pc**. A faixa laranja (binárias de Chae, 0.001–0.145 pc) cai inteiramente
na zona blindada → próxima previsão (FN4-2/FN4-3) é Newton ali, não MOND.

## Resultado FN4-1

**Transição em r = λ_A = 17.3 pc: SIM, limpa.**
Fator de blindagem (boost recuperado) em r = 0.05 pc: ~0.3% do reforço MOND.
S(λ_A) = 0.37 de supressão restante (1 − 1/e de turn-on). Perfil pronto para FN4-2/3.
