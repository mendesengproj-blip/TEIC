# MATTER_COMPLEXITY — Massa como Complexidade Causal

> Campanha que testa a hipótese fundacional da TEIC sobre a origem da massa.
> **Não modifica** R1–R3, e6–e11, D1–D3, M1–S1.
> Código e resultados: `results/matter/complexity/`.

---

## A hipótese a testar

> "Todas as informações propagam na mesma velocidade causal c.
> Mas estruturas mais complexas exigem mais atualizações internas
> para produzir o mesmo deslocamento macroscópico.
>
> Fóton: cada tick causal = 1 deslocamento externo.
> Elétron: N ticks internos antes de 1 deslocamento externo.
>
> Massa ∝ custo causal de deslocamento = N_interno."

Conexão com física conhecida:

```
E² = (pc)² + (mc²)²
energia causal = propagação externa + atualização interna
mc² = energia presa em estrutura interna
```

Hipótese precisa: `custo(deslocamento) ∝ N_interno`, onde N_interno é a
complexidade topológica da estrutura causal.

---

## Por que M1 não testou isso

M1 mediu F/a num campo escalar livre (□θ = 0); o campo dispersa (P1: σ ~ t^0.76)
— não há objeto para acelerar. O teste correto não é campo livre: é **construir
objetos causais com complexidade topológica controlada** e medir o trabalho
causal necessário para movê-los. Estruturas **por construção**, não por emergência.

---

## Definições operacionais (sem circularidade)

**Estrutura causal de complexidade N.** Subgrafo causal (DAG embutido em Minkowski
1+1D) cujo grafo não-direcionado tem **primeiro número de Betti = N** (posto de
ciclos = E − V + componentes). O ciclo causalmente admissível é o *diamante*: um
ponto que se divide em dois ramos espacialmente separados que voltam a se fundir.
Não é curva temporal fechada (proibida); é um laço no grafo não-direcionado que
consome tempo causal sem deslocar o centróide. N diamantes ⇒ Betti = N.

```
N=0 (fóton):   A → B → C → D …            cadeia linear, Betti 0, v=1
N=1 (loop):    split → {ramo+, ramo−} → merge   1 diamante, Betti 1
N=k:           k diamantes empilhados,    Betti k
```

**Custo de deslocamento C(N).** Número de eventos/ticks causais para mover o
centróide da estrutura uma distância causal unitária: `C = Δt_causal / Δx`.

**Massa efetiva.** `m_eff(N) = C(N) / C(0)`, normalizada pelo fóton (N=0).

**Anti-circularidade absoluta.** Massa, energia, força, F=ma, E=mc², Klein–Gordon,
Dirac, γ = 1/√(1−β²) **nunca** entram no gerador. C(N) é contagem de eventos.
Boosts são mapas de coordenadas em rapidez (cosh/sinh), nunca fatores de dilatação.
Verificado por `tests/test_no_circularity.py` (varre `results/matter/`).

---

## Tarefas

| # | Pergunta | Output |
|---|----------|--------|
| CC1 | Construir 6 estruturas N=0,1,3,10,30,100; Betti = N? v_eff(0)=1? | `CC1_structures.{py,md,json,png}` |
| CC2 | C(N) ∝ N? Expoente? (kinemático + dinâmico, 20 sementes) | `CC2_cost.{py,md,json,png}` |
| CC3 | C(N) é Lorentz-invariante? C_boost = C(N)·cosh φ? | `CC3_lorentz.{py,md,json,png}` |
| CC4 | N_interno é conservado sob perturbação? | `CC4_conservation.{py,md,json}` |
| CC5 | θ(r) gerado ∝ N? (D3, fonte = complexidade) | `CC5_gravity.{py,md,json,png}` |
| CC6 | Síntese; E² = (pc)² + (mc²)² emerge? | `CC6_synthesis.md` |

Ordem: CC1 → CC2 → CC3 → CC4 → CC5 → CC6. CC1 é pré-requisito. Se CC2 morre
(C independente de N), documentar e seguir para extrair informação parcial.

---

## Protocolo

1. **Anti-circularidade absoluta** (acima).
2. **Barras de erro obrigatórias:** 20 sementes por N, ± desvio.
3. **Honestidade:** se C(N) for independente de N, a hipótese **falha** — reportar
   como resultado, não como problema. Critérios de morte são válidos.
4. **Estruturas por construção, não por emergência.**
5. **Distinguir definitional de emergente.** Onde um resultado é consequência
   direta da construção (tautológico) e onde é genuinamente medido/arriscado.

---

## RESULTADOS

> Preenchido por CC6 após a execução. Ver `results/matter/complexity/CC6_synthesis.md`
> para a síntese completa com graus (A = derivado, B = real-mas-herdado,
> C = definitional/inconclusivo, D = refutado).

<!-- VERDICT_BLOCK_START -->

| Tarefa | Resultado | Grade |
|--------|-----------|-------|
| CC1 — estruturas N controlado | CONSTRUÍDO (Betti=N, v_eff(0)=1) | build |
| CC2 — τ(N) ∝ N | CONFIRMADO (linear) (p=1.008) | A |
| CC3 — Lorentz | CONFIRMADO | B |
| CC4 — N conservado | CONSERVADO (perturbacao pequena) / QUEBRA (grande) | A |
| CC5 — θ(r) ∝ N | CONFIRMADO | B |
| CC6 — E²=(pc)²+(mc²)² | EMERGE | B |

**Síntese honesta:** τ(N) ∝ N (custo causal medido) é invariante de Lorentz e
fecha o ciclo até θ(r) ∝ N e E²=(pc)²+(mc²)². O núcleo proporcional `C(N)=1+N/n_ext`
é **definitional**; a invariância e a relação E² são **herdadas** de R1; θ∝N
segue da linearidade de D3 dada a identificação fonte=N. Avanço real sobre M1:
existe um objeto com custo de deslocamento bem-definido. Aberto: fazer as
estruturas **emergirem** de uma ação, e derivar uma escala de massa física.
Ver `results/matter/complexity/CC6_synthesis.md`.

<!-- VERDICT_BLOCK_END -->
