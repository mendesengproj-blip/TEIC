# E3b-5 — Síntese honesta: rigidez do cone causal

> Campanha E3b_CAUSAL_DEFECT. Testou o mecanismo 3 de E3 (rigidez topológica do
> cone causal 3+1D) — o único teste honesto restante antes de declarar o
> ferromagneto nu insuficiente para matéria.

## Quadro de resultados (charter E3b-5)

```
E3b-V (gate):
  SR reproduzida no substrato?             [SIM]  corr cadeia 0.9991 com √(1−β²)
  B medido corretamente em Poisson?        [SIM]  Delaunay: hh=+1, anti=−1, vac=0
  ⟨degree⟩ menor que E1 (less mean-field)? [SIM]  ⟨grau⟩=23.0 vs ~46 em E1

E3b-1 (hedgehog causal, Protocolo A):
  B(t)=1 preservado na evolução causal?    [SIM]  100% das 20 sementes, todas as folhas
  r_eff converge para r > 0?               [SIM]  r_eff ≈ 2.7 estável (não colapsa)

E3b-2 (causal vs MC):
  Causal preserva B melhor que MC?         [SIM]  100% vs 0% de sobrevivência
  Diferença quantitativa (tempo de vida):  [>1000 sweeps (sobrevive) vs 200 sweeps]
  → CONTROLE: fatia FUTURA congelada também preserva (100%) ⇒ é pinçamento de
    contorno propagado pelos links, NÃO a seta do tempo.

E3b-3 (Derrick causal):
  E_temporal compensa E_spatial?           [NÃO]  E_temporal < 1% de E_total, ~const(λ)
  Mínimo interior em E_total(λ)?           [NÃO]  λ*=0.40 (encolhe), 3 escalas, robusto

E3b-4 (E=mc², só se Sucesso):
  E_total² = (mc²)² + (pc)² verificado?    [NÃO RODADO — Veredito não é A]
  Desvio de E=mc²:                         [n/a]
```

## VEREDITO: **B — SUCESSO PARCIAL: rigidez causal existe mas é insuficiente**

```
[ ] A — SUCESSO: hedgehog causal estável            (B preservado + Derrick mínimo + E=mc²)
[X] B — SUCESSO PARCIAL: rigidez causal insuficiente
[ ] C — MORTE: hedgehog des-enrola igualmente
```

**Por que B e não A.** Veredito A exigia três coisas; só uma se confirma:
1. ✅ B=1 preservado na evolução causal (E3b-1, E3b-2).
2. ❌ **Sem mínimo interior de Derrick causal** (E3b-3): E_total(λ) ainda
   decresce com o encolhimento; o link temporal carrega <1% da energia e não
   compensa. Não há escala intrínseca, nem soliton auto-sustentado.
3. ❌ E=mc² não derivado (não rodado — protocolo: só sob Veredito A).

**Por que B e não C.** O critério de morte pré-registrado (B(t)→0 sob Protocolo A)
**não** foi acionado: a rede causal com uma fatia de contorno fixa preserva B=1
indefinidamente, enquanto o Monte Carlo livre (acausal) des-enrola em ~200 sweeps.
Existe rigidez extra real — o hedgehog sobrevive muito mais na rede causal
contornada que na relaxação livre.

**A nuance que mantém a honestidade.** O controle de fatia **futura** preserva B
exatamente como o de fatia passada. Logo a rigidez é **pinçamento de Dirichlet de
uma fatia coerente, transmitido pelos links causais** — não a irreversibilidade
da seta do tempo. O acoplamento causal *propaga* o contorno fixo; ele não
*cria* um mínimo de energia. Sem o contorno congelado (MC acausal), o defeito
des-enrola.

## Consequência para a TEIC

```
Fronteira mapeada definitivamente:
  c        ← R1 (Lorentz de Poisson)            [derivado]
  fóton    ← E1+E2 (magnon BD do ferromagneto)  [derivado]
  matéria  ← AINDA exige SU(2)+Skyrme           [Paper II permanece]
  E=mc²    ← Lorentz+SR, NÃO do ferromagneto    [não derivado de defeitos n⃗]
```

- O **Paper II permanece correto**: matéria estável exige SU(2)+Skyrme externos;
  o ferromagneto de orientação nu (O(3), π₂/π₃) não tem mínimo de Derrick em 3+1D,
  nem na rede cúbica (E3) nem na rede causal (E3b).
- **Refinamento sobre E3**: E3 mostrou metaestabilidade (des-enrola no MC térmico);
  E3b mostra que um contorno causal fixo prolonga muito a vida do defeito — mas é
  proteção de contorno, não estabilização intrínseca. O mecanismo 3 está **testado
  e descartado** como fonte de matéria estável.
- **FM1 (CMB/S8) avança** com fundamento sólido e o kill-criterion ativo. A teoria
  permanece em 8/10: fóton derivado, matéria ainda não.

## Anti-circularidade preservada

"massa"/"matéria"/"E=mc²" apareceram apenas como COMPARISON; B é contagem de
ângulo sólido das plaquetas (Delaunay), E é o funcional de bond, c nunca entrou no
gerador (seria o 0.98 medido de E2, usado só sob Veredito A — que não ocorreu).
O critério de morte foi avaliado exatamente como escrito; nenhum parâmetro foi
ajustado para escapar dele.
