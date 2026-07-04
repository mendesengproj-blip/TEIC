# SÍNTESE — A2 / C3 · Loops de Wilson SU(3) no substrato causal

> Campanha CONFINAMENTO_A2 (Fase 2, Frente A). Pré-registro: `PRE_REGISTRO.md`.
> Driver: `a2_su3_causet.py` → `a2_su3_causet.json`. jun/2026.
> **Veredito: FRONTEIRA (death-trigger 2). O confinamento SU(3) é robusto no
> controle cúbico mas NÃO mensurável no causet (obstrução de não-localidade E5/E7,
> agora confirmada para o não-abeliano). O escopo cúbico-só do Paper SU3 está
> CORRETO e permanece — sem rebaixamento.**

---

## 1. Contexto e risco (resolvido benignamente)

A2 era o item de **maior risco de obsolescência** da frente A (poderia rebaixar o
claim de confinamento do Paper SU3). Verificação do paper **mitigou o risco a
priori**: o confinamento já é escopado ao **lattice cúbico 8⁴** explicitamente
("Wilson loops on an $8^4$ lattice"); só o ferromagnetismo é reivindicado nos dois
(cúbico E causet). Logo A2 não rebaixa claim publicado — ele **confirma** o escopo
honesto ou **promove** se o causet confinar.

## 2. Stage A — validação (lattice 4D regular, resposta conhecida)

MC de gauge SU(3) (`su3_core`), Creutz χ(2,2) padrão-ouro em retângulos R×T:

| β | χ(2,2) medido | FLC (paper) | ⟨plaq⟩ |
|---|---|---|---|
| 4.0 | **1.393** | 1.35 | 0.239 |
| 5.0 | **0.960** | 0.96 | 0.346 |
| 6.0 | **0.376** | 0.33 | 0.552 |

**Reproduz FLC quase exatamente:** σ>0 em todo β, **decresce** com acoplamento mais
fraco (direção da liberdade assintótica). O MC SU(3) + estimador estão **validados**
— a obstrução adiante é da geometria do causet, não do código.

## 3. Stage B — causet (a obstrução, quantificada)

MC de gauge SU(3) nas plaquetas de diamante causal (links = matrizes SU(3),
holonomia = produto ORDENADO; ação β·Σ(1−⅓ReTr W)):

- **Gauge vivo:** o setor termaliza; o **plaqueta fundamental** ⟨W₁⟩ **sobe**
  0.311→0.462 de β=4 a 6 (1016 plaquetas, 188 eventos, 1613 links). −ln⟨W₁⟩ é a
  **energia livre de plaqueta**, NÃO a string tension.
- **Obstrução estrutural (death-trigger 2):**
  1. **Todas as 1016 plaquetas são diamantes de altura-2, área=1** (4 links) — não
     há loop SU(3) controlado de área k≥2.
  2. **Zero retângulos R×T controlados** (R,T≥2): o causet não tem direções de grade
     μ/ν consistentes → o discriminador padrão-ouro (Creutz) é **estruturalmente
     indisponível**.
  3. A holonomia SU(3) de um *patch* crescido é um **produto ordenado de matrizes**
     sem palavra-de-bordo limpa em diamantes não-planares. O surrogate abeliano de
     E7 (soma `coeff·θ`) **não se estende** ao não-abeliano — pior ainda que U(1).

⇒ a **string tension** (declive da área-lei k≥2), que É o confinamento, **não tem
estimador controlado no causet não-local**.

## 4. Veredito (FRONTEIRA)

Confinamento SU(3) no causet permanece **[FRONTEIRA]**, exatamente como U(1) em
E5/E7 (obstrução de não-localidade E5-1b), e por uma razão **mais forte** no
não-abeliano: além da ausência de retângulos controlados, a própria holonomia de
patch não fecha um loop limpo. O confinamento é **[SÓLIDO] no controle cúbico**
(Stage A reproduz FLC) e **[FRONTEIRA] no causet**.

**Consequência para o Paper SU3:** o escopo "Wilson loops on an $8^4$ lattice" é
**correto e permanece** — **sem rebaixamento**. A fronteira do causet fica
documentada (não era um claim do paper). O risco de obsolescência ALTO da ficha C3
**não se materializou** porque a redação já era honesta.

## 5. Limitação honesta

Stage B em caixa pequena (188 eventos, plaquetas capadas a ~1016) — suficiente para
mostrar (i) gauge vivo e (ii) o fato estrutural (área=1, zero retângulos), que são
invariantes de tamanho (a obstrução é geométrica, não estatística). Não se tentou um
estimador novo de área-lei não-abeliano no causet porque nenhum é bem-definido — isso
é a fronteira, reportada como tal (não como falha de esforço). Um eventual avanço
exigiria coarse-graining que preserve ordenação não-abeliana (não existe hoje;
mesmo obstáculo de E5/E7).

## 6. Anti-circularidade

`su3_core` e o causet sob a guarda A1; `a2_su3_causet.py` passa as duas guardas
(dilatação + literais de escala). β varrido, nunca input; nenhum σ/α_s/massa
inserido; matrizes SU(3) via `su3_core` (sem literal imaginário cru no driver).
