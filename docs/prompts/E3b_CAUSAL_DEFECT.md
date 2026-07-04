# PROMPT — E3b_CAUSAL_DEFECT: Hedgehog na Rede Causal 3+1D

> Charter da campanha. Testa o mecanismo 3 de E3: rigidez topológica do cone causal.
> Pergunta: o hedgehog de n⃗ é estável na rede causal 3+1D real?
> Resultados em `results/vacuum_structure/orientation/e3b/`.
> NÃO modifica nenhuma campanha anterior.
>
> **STATUS: EXECUTADO (jun/2026) — VEREDITO B (SUCESSO PARCIAL).**
> Ver `results/vacuum_structure/orientation/e3b/E3b_5_synthesis.md` e `README.md`.

---

## O QUE E3 ESTABELECEU E O QUE FICOU ABERTO

E3 rodou no substrato cúbico espacial e encontrou:
- Hedgehog metaestável (Cenário B): B=1 preservado no gradiente descendente,
  des-enrola termicamente em ~2700 sweeps
- Sem mínimo de Derrick (E3-2): sem escala intrínseca
- Curvatura θ~1/r não estabiliza (E3-2): enfraquece a parede

A limitação honesta documentada: o mecanismo 3 (rigidez topológica do cone causal)
não foi testado — é o teste honesto restante antes de declarar o ferromagneto nu
insuficiente. E3b testa exatamente isso.

## A HIPÓTESE DO MECANISMO 3

A rede causal 3+1D tem links causais orientados no tempo com a geometria do cone de
luz. A hipótese: a seta do tempo — a irreversibilidade causal — fornece uma
barreira topológica extra que impede o des-enrolamento do hedgehog.

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (Veredito C): B(t) → 0 na rede causal (Protocolo A). O cone não dá rigidez.
SUCESSO PARCIAL (B): hedgehog sobrevive mais que no cúbico mas ainda des-enrola.
SUCESSO (A): B=1 preservado + mínimo interior de Derrick + E=mc² (verificação tripla).
```

## TAREFAS

- **E3b-V** (gate, obrigatório): SR reproduzida no substrato (corr>0.99 com
  √(1−β²)); B medido em Poisson via tetraedros de Delaunay (hh=+1, vac=0);
  ⟨degree⟩ < E1 (~46). Morte do gate: se B não pode ser medido → parar.
- **E3b-1**: hedgehog em cada evento, evolução causal determinística (Protocolo A,
  ordem temporal, passado fixo); medir B(t), E(t), r_eff(t); 20 sementes.
- **E3b-2**: Protocolo A (causal) vs Protocolo B (MC com causalidade); tempo de
  vida de B=1; controles para isolar causalidade de pinçamento de contorno.
- **E3b-3**: Derrick causal separando E_spatial(λ) de E_temporal(λ); refinamento
  de escala.
- **E3b-4**: APENAS se Veredito A em E3b-1+E3b-3 — verificar E²=(mc²)²+(pc)² com
  c=0.98 de E2; verificação tripla (V1 estabilidade, V2 Derrick, V3 dispersão).
- **E3b-5**: síntese honesta + veredito.

## PROTOCOLO

1. Gate E3b-V obrigatório antes de qualquer medida de defeito.
2. Protocolo A (evolução causal) antes do Protocolo B.
3. E3b-4 apenas se Veredito A.
4. Anti-circularidade: "massa"/"energia"/"E=mc²" COMPARISON ONLY; c não entra como
   constante (é 0.98 medido em E2); E_defeito é funcional de energia.
5. 20 sementes para E3b-1 e E3b-2.
6. Critério de morte pré-registrado: B(t)→0 em Protocolo A = Veredito C. Não
   ajustar parâmetros para escapar da morte.

## RESULTADO EXECUTADO (resumo)

- **E3b-V: PASS.** Cadeia causal corr 0.9991 com √(1−β²); Delaunay B=+1/−1/0;
  ⟨grau⟩=23 < 46; 0 violações da seta do tempo.
- **E3b-1: B=1 preservado** (100%/20 sementes) sob Protocolo A — morte não acionada.
- **E3b-2:** causal (passado congelado) 100% vs MC acausal 0% (vida >1000 vs 200
  sweeps) — MAS o controle de fatia **futura** congelada também preserva (100%) ⇒
  a rigidez é **pinçamento de contorno propagado pelos links causais**, não a seta
  do tempo.
- **E3b-3: sem mínimo interior de Derrick causal** (λ*=0.40, 3 escalas; E_temporal
  <1% de E_total, não compensa).
- **E3b-4: não rodado** (Veredito não é A).
- **E3b-5: VEREDITO B — SUCESSO PARCIAL.** A rigidez do cone existe (defeito vive
  muito mais que na relaxação livre) mas é insuficiente: é proteção de contorno,
  não estabilização intrínseca, e não há mínimo de Derrick. **Matéria estável ainda
  exige SU(2)+Skyrme (Paper II permanece). E=mc² não derivado do ferromagneto.**
