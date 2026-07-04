# SÍNTESE — GATILHO Rideout–Sorkin (coordenação do crescimento sequencial)

> Pré-registro: `PRE_REGISTRO.md` (congelado 2026-06-25, antes de qualquer medição).
> Gerador + estimador + gate: `rs_trigger.py`. Figura: `make_figure.py` → `rs_trigger.png`.
> Dados: `rs_trigger.json`, `validation_gate.json`.
> Estimador **idêntico** ao da ESCALA_XI (cross-check numérico: z=18.5000 vs 18.5000,
> 2775 links vs 2775, diff 0.00e+00 num mesmo causal set de Poisson).

## VEREDITO DE UMA LINHA

**GATILHO ARMADO.** A coordenação do grafo de Hasse do crescimento sequencial clássico
(CSG / percolação transitiva de Rideout–Sorkin) **satura num valor finito O(1)–O(10)**
em **todos** os quatro regimes testados, enquanto o sprinkling de Poisson **diverge**
(z=33→103). O CSG **não** é o grafo tipo-árvore de **alta coordenação** que o argumento
de Bethe condena ⇒ um ξ divergente tem onde morar ⇒ **a campanha completa (ferromagneto
de orientação sobre CSG + medição de ξ) se justifica.** **PARO aqui** — a campanha
completa é decisão separada, com pré-registro próprio.

> **Este resultado contraria o prior declarado** ("mais provável NÃO ARMADO"). O prior
> está registrado e foi **falsificado pela medição** — reporto o desfecho real, sem
> reinterpretar o critério (sem annealing).

---

## 1. GATE DE VALIDAÇÃO — VERDE

O gerador reproduz propriedades documentadas da percolação transitiva (`validation_gate.json`):

| Check | Resultado |
|---|---|
| `E[#minimais] = (1−(1−p)^N)/p` (forma fechada) | 19.86±0.21 vs 20.00; 9.88±0.14 vs 10.00 ✓ |
| `E[#arestas diretas] = p·N(N−1)/2` (forma fechada) | 996.0 vs 995.0; 7977 vs 7980 ✓ |
| Aciclicidade/DAG (ancestrais < j) | ✓ |
| Fecho transitivo idempotente | ✓ |
| Percolação: fração de ordenação cresce com N (p fixo) | 0.47→0.84→0.92 ✓ |

(Uma execução-piloto com 40 sementes deu falso-vermelho de 2.7σ no #minimais; com 200–600
sementes converge a −0.9σ do fechado — era ruído de amostragem, não viés. Gate refeito VERDE.)

---

## 2. A MEDIÇÃO — `⟨z⟩(N)` por regime (mesmo estimador, mesmo ladder da XI)

| Regime | p | N=500 | 1000 | 2000 | 3300 | 3888 | razão | `d⟨z⟩/d ln N` (topo) |
|---|---|---|---|---|---|---|---|---|
| **Poisson (XI)** | — | 33.4 | 52.1 | 75.7 | 103.0 | — | **×3.1** | **+25 → +38 → +51 (acelera)** |
| sparse_fixed | 0.02 | 6.50 | 8.00 | 8.42 | 8.67 | 8.63 | ×1.33 | −0.23 (vira) |
| intermediate_fixed | 0.10 | 5.74 | 5.80 | 5.91 | 5.96 | 6.00 | ×1.05 | +0.26 |
| **dense_fixed** | 0.40 | 3.56 | 3.57 | 3.54 | 3.57 | 3.57 | **×1.00** | **−0.00 (plano)** |
| manifold_scaled | 4/N | 3.84 | 3.92 | 3.98 | 3.99 | 4.01 | ×1.04 | +0.12 |

**A pergunta binária e visual (`rs_trigger.png`): o CSG satura enquanto o Poisson diverge?
SIM.** O expoente local do Poisson é **+25 a +51 e acelerando**; o de **todos** os regimes
CSG é **≤ +0.26 e plano/decrescente** — duas ordens de grandeza menor, no **mesmo** range
de N. O confound "satura vs cresce devagar" está descartado: a saturação não vem de range
curto (o Poisson, no mesmo range, dispara), e os expoentes CSG não estão "diminuindo
devagar" — já são ~0.

---

## 3. MECANISMO — por que o CSG escapa e o Poisson não

A XI diagnosticou a **não-localidade Lorentz-protegida** como o motor da coordenação
divergente do Poisson: pares boostados têm tempo-próprio pequeno mas separação coordenada
enorme, então o slab que define "link" tem volume que cresce com a caixa ⇒ z↑ com N. **O
CSG não tem métrica, não tem boosts, não tem embedding** — a relação de cobertura é
**local na ordem aleatória**, então a coordenação satura. O CSG escapa **exatamente** do
mecanismo que a XI isolou. Confirma, por contraste, que a divergência do Poisson é um
fato sobre o *sprinkling em fundo Lorentziano*, **não** sobre causal sets em geral.

---

## 4. CAVEATS HONESTOS = PRÉ-CONDIÇÕES PARA QUALQUER CAMPANHA FUTURA (não inflar o ARMADO)

> **Estes dois caveats têm peso de PRÉ-CONDIÇÃO, não de nota de rodapé.** Qualquer
> trabalho subsequente sobre o substrato CSG está vinculado a eles:
> - **Pré-condição A:** o regime `dense` (p=0.40) **não pode ser citado como evidência
>   de saturação genuína** em nenhum resumo, tabela ou paper — é trivial (cadeia 1D).
>   Os regimes legítimos são **sparse, intermediate, manifold**.
> - **Pré-condição B:** **nenhuma campanha de ferromagneto/ξ sobre o CSG deve ser
>   executada antes de medir o clustering** do grafo de cobertura nos regimes legítimos
>   (Gatilho 2, `docs/campaigns/RIDEOUT_SORKIN_CLUSTERING/`). Coordenação finita é
>   necessária, **não suficiente**.


1. **A saturação do regime `dense` é parcialmente trivial.** p=0.40 dá fração de
   ordenação 0.999 → quase-ordem-total → grafo de Hasse ≈ **cadeia 1D** → z≈3.6 por
   construção. Uma cadeia 1D **não** tem transição a T finito. Portanto "armado pelo
   `dense`" seria oco. **Os regimes legítimos** são `sparse`/`intermediate`/`manifold`,
   onde a ordem **não** é trivialmente 1D (fração 0.006–0.89) e ainda assim z satura em
   4–9. O `manifold_scaled` (fração→0.006, esparso, z≈4) é o esteio genuíno: causal set
   esparso de baixa coordenação que **não** colapsa em cadeia.

2. **Coordenação finita é NECESSÁRIA, não SUFICIENTE, para fugir do mean-field.** Uma
   **rede de Bethe** (árvore infinita) tem z finito e **ainda é mean-field exata**. Logo
   o gatilho ARMA porque remove a perna de *alta coordenação crescente* do argumento da
   XI (que era o que condenava o Poisson) — mas a campanha completa terá de verificar se
   o grafo de cobertura do CSG tem **estrutura de laços de dimensão finita (clustering ≠
   0, não-árvore)** ou se é ele próprio uma árvore (→ continuaria mean-field). O gatilho
   responde só à pergunta de coordenação (a barata); essa é a próxima pergunta, e é da
   campanha completa.

3. **ARMADO ≠ "ξ diverge".** ARMADO significa apenas: *a pré-condenação por Bethe-alta-
   coordenação não se aplica automaticamente; vale gastar a campanha completa.* Se ξ
   diverge ou não é a medição separada.

---

## 5. O QUE A CAMPANHA COMPLETA (separada) DEVE FAZER

- Pré-registro próprio. Rodar o ferromagneto de orientação O(3) (engine `orientation_core`,
  VERBATIM) sobre o grafo de cobertura do CSG nos regimes **legítimos**
  (`manifold_scaled` λ∈{2,4,8} e `intermediate`), localizar J_c pela varredura, medir
  U₄ / χ_max / ξ.
- **Primeiro discriminador (barato, antes de ξ):** medir o **clustering** e a contagem
  de laços curtos do grafo de cobertura do CSG. Se for tipo-árvore (clustering→0), o
  destino é mean-field por Bethe **apesar** da coordenação finita — e a campanha morre
  cedo. Se tiver laços de dimensão finita, ξ tem chance real.
- Critério de morte da campanha completa: ξ_2nd/L não-crescente + U₄ sem cruzamento
  invariante + χ_max em lei-de-volume ⇒ mean-field estrutural confirmado também no CSG.

---

## 6. CONSEQUÊNCIAS PARA O PROGRAMA

1. **Reabre a "Saída 2" da XI** (substrato genuinamente diferente) que a XI havia
   deixado dormente: a §4.4 da SÍNTESE da XI afirmava "§10 (crescimento sequencial RS)
   NÃO se justifica como sucessor". **Esse fechamento era prematuro** — baseava-se em
   "nenhuma alavanca A–C deu sinal não-circular", mas as alavancas A–C eram todas
   variações do **sprinkling**; o CSG é uma classe de geração diferente e, medido agora,
   **tem coordenação finita**. A frente RS sai de "dormente" para **gatilho ARMADO**.
2. **Refina a memória** [[escala-xi-correlation-divergence]] e [[b7-escalas-transmutacao]]:
   o mean-field dos causal sets que a XI/B7 chamaram de "estrutural" é estrutural ao
   **sprinkling Lorentziano** (via não-localidade), **não** à ideia de causal set por si.
   Mudar a *forma de gerar* o conjunto (crescimento vs sprinkling) muda a coordenação de
   divergente para finita.
3. **Resíduo registrado na §6 do RESEARCH_MAP (item 14, FM5):** "família CSG completa
   (t_n)" — este gatilho cobre a subfamília de percolação transitiva (t_n=t^n); a família
   RS geral (t_n livres / regra por n_componentes do `e7_growth_dynamics.py`) fica como
   varredura adicional opcional da campanha completa.

---

## ARQUIVOS
- `PRE_REGISTRO.md` — critérios congelados (incl. prior honesto, depois falsificado).
- `rs_trigger.py` — gerador CSG (percolação transitiva), estimador de Hasse (= XI),
  gate de validação, medição, veredito. `validation_gate.json`, `rs_trigger.json`.
- `make_figure.py` → `rs_trigger.png` — ⟨z⟩(N) CSG (4 regimes) sobreposto ao Poisson.
