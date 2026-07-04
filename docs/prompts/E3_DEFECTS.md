# PROMPT — E3_DEFECTS: Defeitos Topológicos de n⃗ = Matéria?

> Terceira campanha do programa NIVEL4_ORIENTATION.
> Pergunta central: os defeitos topológicos do ferromagneto
> causal são estáveis sem SU(2) nem Skyrme externos?
> Resultados em `results/vacuum_structure/orientation/e3/`.
> NÃO modifica nenhuma campanha anterior.

---

## CONTEXTO: O QUE E1+E2 ESTABELECERAM

```
E1: Vácuo = ferromagneto de orientação (n⃗ se alinha espontaneamente)
E2: Fóton = modo de Goldstone BD-smeared (ω=ck, 2 polarizações)
```

A pergunta natural que se segue:

> Se o fóton é uma perturbação propagante de n⃗,
> o que é uma perturbação estática e topologicamente não-trivial?

Em ferromagnetos da matéria condensada, a resposta é conhecida:
defeitos topológicos de n⃗ são **Skyrmions magnéticos** —
estruturas estáveis com número topológico B=1 que existem
em materiais como MnSi e FeGe.

A pergunta de E3: **a rede causal suporta Skyrmions de n⃗
sem precisar adicionar SU(2) nem Skyrme externamente?**

Se sim: matéria emerge do ferromagneto causal pelo mesmo
mecanismo que o fóton — sem ingredientes externos.

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE: defeito topológico de n⃗ colapsa para o vácuo.
       A energia diminui monotonicamente quando o defeito
       é dilatado/contraído — teorema de Derrick ativo.
       Matéria não emerge do ferromagneto nu.

SUCESSO PARCIAL: defeito topológico existe mas é metaestável
       (barreira de energia finita, mas colapsa em tempo longo).

SUCESSO: defeito topológico com número B=1 é estável:
       energia tem mínimo interior em λ=1 (sem dilatação),
       barreira topológica medida sob refinamento de grade.
```

---

## A FÍSICA DO DEFEITO

### O que é um Skyrmion magnético

Em um ferromagneto 3D, o campo de orientação n⃗(x) ∈ S²
pode fazer um "enrolamento" do espaço físico R³ sobre S²:

$$B = \frac{1}{4\pi} \int d^3x\, \epsilon^{ijk}
  \vec{n} \cdot (\partial_i \vec{n} \times \partial_j \vec{n})
  \partial_k \vec{n}$$

B ∈ π₃(S²) = ℤ — o número topológico.

**O hedgehog:** n⃗(r) = r̂ (aponta radialmente para fora)
tem B=1 e é o candidato mais simples.

### O problema de Derrick para n⃗ ∈ S²

Em 3D, a ação do modelo sigma O(3):

$$E = \int d^3x \, |\nabla n⃗|^2$$

tem Derrick: E(λ) = λ E₀ sob dilatação r → λr.
Portanto E decresce com λ → 0: **hedgehog colapsa em S².**

Esta é a diferença entre O(3) e SU(2):
- n⃗ ∈ S² (O(3)): π₂(S²)=ℤ em 2D, π₃(S²)=ℤ em 3D
  mas Derrick mata o Skyrmion em 3D sem estabilização.
- U ∈ SU(2) (Skyrme): π₃(SU(2))=ℤ com Skyrme estabiliza.

### A hipótese de E3

A rede causal tem dois mecanismos que podem estabilizar
o defeito de n⃗ sem Skyrme externo:

**Mecanismo 1 — Discretização:**
A rede discreta introduz um comprimento mínimo a (espaçamento).
Isso regulariza a divergência UV e impede o colapso total.
O defeito pode ser estável em a ≤ r ≤ ∞.

**Mecanismo 2 — Curvatura induzida:**
O próprio defeito curva a rede causal ao redor de si
(D3 mostrou θ(r) ~ M/r). A curvatura pode atuar como
estabilizador (análogo ao acoplamento com gravidade).

**Mecanismo 3 — Topologia causal:**
A rede causal tem estrutura temporal que a rede espacial
não tem. O cone causal pode fornecer a rigidez topológica
extra que estabiliza o defeito.

---

## Tarefas

- **E3-V** (gate, obrigatório): verificar que B é medido corretamente
  (B=1 hedgehog, B=0 vácuo) antes de qualquer medição de estabilidade.
- **E3-1**: criar hedgehog n⃗(r)=r̂ no estado ferromagnético ordenado de E1,
  relaxar via gradiente descendente E Monte Carlo, medir B(t), E(t), r_eff(t)
  em 20 sementes. Cenários A (colapso) / B (metaestável) / C (estável).
- **E3-2**: medir E(λ) sob dilatação, comparar plana vs com curvatura θ~1/r,
  refinamento N=32³,48³,64³.
- **E3-3**: se defeito sobrevive, verificar θ ~ M/r ao redor.
- **E3-4**: catálogo (anti-hedgehog, dipolo, toroidal).
- **E3-5**: síntese honesta + veredito.

## Protocolo

1. Gate E3-V obrigatório antes de qualquer medida de estabilidade.
2. Dinâmica de relaxação (gradiente descendente) além de Monte Carlo (MC pode
   escalar barreiras topológicas artificialmente).
3. Refinamento de grade para E3-2 (N=32³,48³,64³).
4. Anti-circularidade: "partícula"/"matéria"/"massa" — COMPARISON ONLY.
   B é contagem topológica das plaquetas; E é funcional de energia da rede.
5. Critério de morte pré-registrado: colapso total de B = Veredito C.
   Não ajustar parâmetros para escapar da morte.
6. 20 sementes para E3-1, configuração única para E3-2.
