# MATTER_CREATION — Criação de Matéria como Reorganização Causal

> Testa se a colisão de cadeias causais gera loops espontaneamente sob a dinâmica BD.
> Continua após `MATTER_COMPLEXITY.md` (CC1–CC6).
> **Não modifica** R1–R3, e6–e11, D1–D3, M1–S1.
> Código e resultados: `results/matter/creation/`.

---

## A hipótese a testar

> "O que colide é informacional. Mas os eventos que criaram os fótons tinham
> energia. Como essa energia saiu e criou matéria em outro lugar?"
>
> Resposta TEIC: energia não viaja separada da rede. Energia = taxa de criação de
> eventos causais. Matéria = reorganização topológica dessas cadeias de linear para
> cíclica (loops).

```
Antes:  cadeia A (linear, alta taxa) + cadeia B (linear, alta taxa)
Depois: estrutura C com loops internos (mc²) + propagação externa (pc)
Conservação:  E_total(antes) = E_total(depois) ?
```

**Hipótese precisa:** quando duas cadeias causais lineares de alta densidade se
encontram, a rede pode espontaneamente formar loops internos, conservando a taxa
total de eventos causais.

---

## Por que isto difere de CC1–CC6

CC1–CC6 **constrói** estruturas com N loops e mede o custo de deslocamento (massa ∝
complexidade?). CR1–CR6 deixa a **dinâmica da colisão** decidir a topologia: loops
emergem espontaneamente? A taxa causal total é conservada? São complementares: CC
testa estruturas pré-construídas; CR testa criação dinâmica.

---

## Definição operacional (sem circularidade)

**Energia causal.** `E_causal(cadeia) = nº de eventos causais por unidade de
comprimento próprio`. Alta energia = alta densidade de eventos. Para estrutura com
loops: `E_total = E_interna (N·loops) + E_externa (propagação)`.

**Loop criado.** Excesso do primeiro número de Betti do *grafo de cobertura*
(relação de cobertura = Hasse) dos eventos da estrutura, **acima** de um controle de
mesma densidade — para descontar os diamantes geométricos triviais de um conjunto
causal 2D. O detector é validado recuperando Betti = N numa estrutura CC.

**Anti-circularidade absoluta.** Energia, mc², 2mc² (limiar QED), elétron, pósitron
**nunca** entram no gerador. E_causal e N_loops são contagens. Boosts em rapidez.
Verificado por `tests/test_no_circularity.py`.

---

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| CR1 | E_causal bem-definida por contagem? conservada em propagação livre? | `CR1_energy.{py,md,json}` |
| CR2 | Baixa energia: colisão cria loops? (baseline) | `CR2_collision.{py,md,json}` |
| CR3 | Alta energia: loops criados? Existe limiar ρ*? | `CR3_high_energy.{py,md,json,png}` |
| CR4 | Taxa causal total conservada? criação em pares? | `CR4_conservation.{py,md,json}` |
| CR5 | θ(r) conservado na criação? | `CR5_gravity.{py,md,json,png}` |
| CR6 | Síntese: a dinâmica BD cria matéria? | `CR6_synthesis.md` |

Ordem: CR1 → CR2 → CR3 → CR4 → CR5 → CR6. CR2 (baixa E) antes de CR3 para
estabelecer o baseline sem criação.

---

## Protocolo

1. **Anti-circularidade absoluta** (acima).
2. **CR2 antes de CR3.**
3. **Barras de erro:** 20 sementes por (ρ, configuração).
4. **Critérios de morte válidos:** se CR3 não achar limiar, é resultado — a ação BD
   não cria matéria espontaneamente. Reportar honestamente.
5. **Distinguir dinâmico de geométrico:** todo excesso topológico é comparado a
   controles (mesma densidade; head-on vs co-movente) para isolar criação genuína.

---

## Expectativa honesta

A ação BD é **linear** (□θ = J): o propagador retardado K = ½C é um operador linear,
logo a superposição é exata e a colisão não pode criar estrutura nova no campo. O
resultado mais provável é que CR3 **não** encontre limiar ρ* — localizando
precisamente onde a não-linearidade (o setor interagente da QFT) seria necessária,
consistente com e11 e M1-S1. O resultado extraordinário (limiar ρ* genuíno) exigiria
verificação extrema. Reportamos o que a dinâmica de fato fizer.

---

## RESULTADOS

<!-- VERDICT_BLOCK_START -->

| Tarefa | Resultado | Grade |
|--------|-----------|-------|
| CR1 — E_causal definida/conservada | SIM (CV livre ~2%, Lorentz-invariante) | A |
| CR2 — baixa E: sem criação | CONFIRMADO (atravessam-se) | A |
| CR3 — alta E: limiar ρ* | NÃO EXISTE (sem criação até 100ρ₀) | D |
| CR4 — taxa causal conservada | SIM (desbalanço sistemático ~0; resto é ruído Poisson) | A |
| CR5 — θ conservado | SIM (aditivo, linear) | B |

**Síntese honesta:** a dinâmica BD (K = ½C, □ suavizado) é **linear** — o resíduo
de superposição é ~0e+00 em toda densidade. As cadeias
**atravessam-se**: interagem transientemente mas não criam nenhuma estrutura
ligada persistente; **não há limiar ρ\*** de criação. A taxa causal total e o
campo θ são conservados — conservação e ausência-de-criação são o mesmo fato
(linearidade). **Resultado de localização:** a criação de matéria exige
não-linearidade além de □θ = J (o setor interagente da QFT que a TEIC ainda não
tem), consistente com e11 / M1-S1. Critério de morte válido e informativo.
Ver `results/matter/creation/CR6_synthesis.md`.

<!-- VERDICT_BLOCK_END -->
