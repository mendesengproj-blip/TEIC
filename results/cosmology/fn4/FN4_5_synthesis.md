# FN4-5 — Síntese honesta e veredito

> Campanha FN4_MOND_SCREENING. Charter: [`../../../FN4_MOND_SCREENING.md`](../../../FN4_MOND_SCREENING.md).
> a₀ = 1.2×10⁻¹⁰ m/s², λ_A = 17.3 pc — fixos, não ajustados.

## Quadro de resultados

```
FN4-1 (perfil):
  Transição clara em r = λ_A = 17.3 pc?            SIM (S=1−1/e em λ_A)
  Boost recuperado em r = 0.05 pc:                 ~0.3% (≈ Newton)
  Boost recuperado em r = 17.3 pc:                 ~65% (S = 0.63)
  r_MOND(1 M☉) = 0.034 pc ≪ λ_A = 17.3 pc:         há ~1.5 década de zona blindada

FN4-2 (velocidades):
  ṽ_DEV diverge de ṽ_MOND para s < 17 pc?          SIM (DEV→1, MOND→1.16)
  Divergência máxima:                              ~0.16 em ṽ, saturando para s ≲ 1 pc
                                                   (no regime sub-pc, não no joelho)

FN4-3 (Gaia/Chae 2309.08160):
  Separações de Chae (0.001–0.145 pc) no regime de blindagem?   SIM (≪ λ_A; máx 0.84% de λ_A)
  Blindagem no regime de Chae:                     DEV mantém < 1% do boost → γ_DEV ≈ 1.00
  Chae compatível com DEV?                         NÃO (γ=1.43 vs 1.00 → 7.1σ) — mas CONTESTADO
  Regime relevante para λ_A:                        s ~ 5–50 pc

FN4-4 (forecast):
  Dados existentes cobrem 5–50 pc com binárias ligadas?  NÃO (maré r_J = 1.7 pc)
  Survey que pode testar diretamente:              nenhum com binárias ligadas;
                                                   só pares co-móveis (Gaia DR4, não-orbital)
  N para 3σ:                                        ~2.8×10⁴ pares (transição) /
                                                   ~1.6×10⁴ binárias (sub-pc, já em mãos)
```

## VEREDITO: **C — TENSÃO** (condicional a D; com obstáculo estrutural B para a transição)

A DEV faz uma previsão exclusiva e nítida: **gravidade newtoniana em binárias largas
sub-pc** (reforço MOND blindado abaixo de λ_A = 17.3 pc). O confronto se divide em dois:

1. **Discriminador sub-pc (testável agora):** as binárias de Chae+2023 estão
   profundamente na zona blindada (≤ 0.84% de λ_A), onde a DEV prevê γ ≈ 1.00. Chae mede
   γ = 1.43 ± 0.06 → **tensão de 7.1σ**, que é literalmente a condição de MORTE
   pré-registrada. **Mas o sinal de binárias largas é contestado:** Banik et al. 2024 e
   Pittordis & Sutherland encontram GR/Newton (γ≈1) nas mesmas separações. A previsão da
   DEV coincide com esse campo do não-sinal. → o destino da DEV está **amarrado à
   resolução de uma disputa observacional aberta**, não a uma refutação isolada.

2. **Joelho da transição em 17 pc (o teste "limpo"):** inacessível a binárias ligadas —
   a maré galáctica as desfaz em r_J ≈ 1.7 pc, dez vezes dentro de λ_A. Só pares
   co-móveis (não-ligados, velocidade não-orbital) alcançam 5–50 pc, com confusão
   estatística. → este caminho é **B (indeciso por falta de tracer adequado)**.

## A leitura honesta

- **Não é morte limpa (D):** porque o único dado no regome — Chae — é contestado, e o
  lado newtoniano da controvérsia *confirma* a DEV.
- **Não é sucesso (A):** porque não há demonstração positiva da supressão com o perfil
  S(r); e se Chae estiver certo, a DEV morre.
- **É tensão (C):** a DEV está exposta. A previsão de blindagem é **falsificável já**, e o
  seu veredito final será decidido pela resolução do debate de binárias largas (Gaia DR4
  + modelagem de triplos), não por um survey futuro do joelho em 17 pc.

## O que esta campanha adiciona ao programa

- **Uma segunda previsão falsificável**, ao lado da BTFR do Paper I: *binárias largas
  sub-pc devem ser newtonianas* (MOND blindado abaixo de λ_A = 17.3 pc). Diferentemente
  da MOND de Milgrom, que prevê reforço em toda escala com g < a₀.
- **Um alvo observacional concreto e iminente:** o debate Chae vs Banik/Pittordis com
  Gaia DR4 testa a DEV diretamente — sem precisar esperar pelo regime de 17 pc.
- **Conexão com Paper II:** λ_A = 17.3 pc é ℏ/(m_A c); se a blindagem for refutada
  (γ=1.43 robusto), o m_A do Paper II precisa ser revisto — ver nota no charter.

## Encaminhamento

- Se o debate de binárias largas convergir para **γ ≈ 1 (Newton)** → DEV confirmada,
  promover a previsão ao Paper I como 2ª previsão falsificável.
- Se convergir para **γ ≈ 1.4 (MOND robusto, Chae)** → **morte** da blindagem em 17 pc;
  reabrir m_A (Paper II) ou o mecanismo de coerência.
- Próximo: monitorar análises Gaia DR4 de binárias largas (2026+); FN4 não precisa de
  novo cálculo até os dados moverem.
