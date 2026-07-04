# NÍVEL 4 — A Variável de Orientação (registro de fronteira)

> **O que este documento é.** Um registro formal de hipótese e
> pré-registro de experimentos, **não** uma campanha executada. Nenhum
> experimento é rodado aqui; nenhuma campanha anterior é modificada. Este é
> o documento que orienta a primeira nova investigação **após** os papers.
> Charter-irmão: as entradas FN1–FN4 em `FUTURE_EXPERIMENTS.md`.
>
> Disciplina do projeto, mantida: critério de morte pré-registrado antes de
> qualquer código. A hipótese pode morrer em E1, e o resultado será
> registrado como negativo válido.

---

## 1. O que motivou este registro

VS1 (campanha VACUUM_STRUCTURE) fechou a hipótese:

> "a densidade ρ é o parâmetro de ordem do vácuo."

Resultado medido: ρ **não condensa espontaneamente** — a estrutura de ρ é
resposta linear escravizada ao drive, e desaparece com ele (ganho constante
0.43, corr −0.51, três vias independentes com PE2/V4). **A densidade
obedece — não lidera.**

Isso abriu uma hipótese nova, mais coerente com o que a teoria já encontrou:

> **O parâmetro de ordem do vácuo não é ρ — é a orientação interna dos nós
> n⃗(x).**

A hipótese não é especulativa. Tem suporte indireto em três resultados já
commitados:

1. **O Skyrmion SU(2) já é um defeito de orientação** — n⃗ fazendo uma volta
   de 2π do centro ao infinito (a configuração hedgehog). A matéria que a
   TEIC derivou é defeito de orientação, não de densidade. [DERIVADO — SU3]

2. **A ação mínima S = Σ Δτ[1−cos(φ+Δθ)] é uma ação de modelo sigma
   O(3)/XY** — cujas excitações naturais são magnons (ondas de orientação),
   não ondas de densidade. [ESTRUTURAL — C1–C4]

3. **LIV_VECTOR mostrou que E/B > 1 em plaquetas causais é causalidade, não
   frame preferido.** O campo vetorial A_μ que carrega as plaquetas é uma
   variável de orientação de link, não de densidade. [DERIVADO — LV1]

---

## 2. A hipótese formal: o vácuo da TEIC é um ferromagneto causal

Em linguagem precisa:

```
Estado fundamental:
  n⃗(x) = orientação de cada nó ∈ S² (ou SO(3))
  ⟨n⃗⟩ ≠ 0 — alinhamento espontâneo

Excitações de baixa energia (fótons):
  δn⃗(x,t) — ondas de spin (magnons)
  □(δn⃗) = 0 — propagação causal

Defeitos topológicos estáveis (matéria):
  π₂(S²) = ℤ — hedgehog (monopolo)
  π₃(S³) = ℤ — Skyrmion (bárion)

Energia do defeito (massa):
  m ∝ E_deformação = custo de manter n⃗ enrolado
```

### A correspondência com a física conhecida

```
Ferromagneto       →   TEIC                →   Física
──────────────────────────────────────────────────────────
spin s             →   orientação n⃗(x)    →   campo interno do vácuo
magnon             →   onda δn⃗            →   fóton
domínio magnético  →   região de n⃗ unif.  →   vácuo local
skyrmion magnético →   Skyrmion SU(2)      →   bárion
anti-vórtice       →   anti-Skyrmion       →   anti-bárion
temperatura T      →   rigidez K           →   K > K_c ≈ 8.5
```

A linha `T ↔ K` não é analogia solta: VS1 mediu que o vácuo uniforme só é
estável para rigidez K > K_c ≈ 8.5 — exatamente a estrutura de uma fase
ordenada abaixo de uma temperatura crítica.

### O análogo de bancada (Hu, Manitoba, 2024–2026)

O sistema YIG acoplado a micro-ondas é um ferromagneto onde magnons (ondas
de n⃗) se acoplam a fótons de cavidade. Se o vácuo da TEIC é um ferromagneto
causal, esse experimento realiza em laboratório a mesma estrutura de
acoplamento campo↔orientação. [IDENTIFICADO como análogo — não é um teste
da TEIC; é uma referência de que a estrutura proposta existe e é estudada.]

---

## 3. As quatro perguntas a responder

### P1 — Existe alinhamento espontâneo de orientação?

**Pergunta:** ⟨n⃗(x)⟩ ≠ 0 espontaneamente no vácuo causal?

**O que medir:** a correlação de orientação em função da distância,
C(r) = ⟨e^{iφ(0)}·e^{−iφ(r)}⟩.

- C(r) → C₀ ≠ 0 (r→∞): alinhamento de longo alcance — fase ferromagnética,
  ⟨n⃗⟩ ≠ 0.
- C(r) → 0 exponencial: desordem de curto alcance — fase paramagnética,
  sem ordem.
- C(r) ∝ r^(−η): lei de potência — transição de Kosterlitz–Thouless, vácuo
  no ponto crítico.

**Critério de morte:** C(r) decai mais rápido que qualquer lei de
potência — sem ordem de orientação em nenhuma escala.

### P2 — Os nós têm estados degenerados de orientação?

**Pergunta:** cada nó pode apontar em qualquer direção de S² com igual
energia, ou há direções preferenciais?

**O que medir:** o histograma de orientações {n⃗_i} em equilíbrio. Uniforme
em S² = degenerescência completa (O(3) simétrico); concentrado = direção
preferida (quebra de simetria).

**Implicação:** degenerescência completa = bóson de Goldstone em cada
direção quebrada = fóton como magnon (excitação de Goldstone).

### P3 — O fóton é uma oscilação de n⃗?

**Pergunta:** uma perturbação localizada de n⃗(x,t) propaga-se como onda com
as propriedades do fóton?

**O que medir:** (1) criar δn⃗ em x=0,t=0; (2) acompanhar δn⃗(x,t); (3)
propaga em c? (4) dispersão E = pc sem massa? (5) polarização transversal
(dois modos)?

**Critério de morte:** δn⃗ não se propaga de forma ondular — dissipa ou tem
dispersão errada.

### P4 — A matéria é um defeito de n⃗?

**Pergunta:** um defeito topológico de n⃗(x) — onde n⃗ enrola π₂(S²)=ℤ — é
estável sem nenhum ingrediente externo?

**O que medir:** (1) construir hedgehog n⃗(r)=r̂; (2) é estável (barreira >
0)? (3) campo θ ao redor ~ M/r? (4) gravita?

**Critério de morte:** o defeito de n⃗ colapsa ao vácuo — a topologia de n⃗
sozinha não estabiliza.

> Nota de continuidade com a fronteira já medida: SKYRME_DOMINANCE provou
> que a ação mínima de cossenos **não** estabiliza o quártico sozinha (o
> custo de núcleo é importado). P4 reabre a pergunta numa variável
> diferente (n⃗ contínuo em S², não a fase compacta) — se a estabilização
> falhar aqui também, isso *fortalece* o teorema de impossibilidade; se
> tiver sucesso, identifica a variável que faltava. Os dois desfechos são
> informativos.

---

## 4. Os quatro experimentos (após os papers)

### E1 — Correlações de fase/orientação

- Rede 3+1D com campo de orientação n⃗(x) ∈ S².
- Ação: S = −J Σ_links n⃗(x)·n⃗(y) (modelo sigma O(3)).
- Medir C(r) = ⟨n⃗(0)·n⃗(r)⟩; varrer a rigidez J/T; identificar fase
  ordenada vs desordenada.
- **Infraestrutura:** motor de modelo sigma O(3) em rede causal (novo —
  análogo de `su2_core` para campo vetorial real em S²).
- **Ponto de partida no código:** a fase de plaqueta W_p em Wilson U(1) é
  θ ∈ [0,2π]; a orientação n⃗ ∈ S² é a versão não-compacta. `su2_core`
  (quaternions = S³) é o esqueleto mais próximo.

### E2 — Espectro de excitações de n⃗ (magnons)

- A partir de E1 na fase ordenada, criar δn⃗ localizada e medir a relação de
  dispersão ω(k).
- **O discriminador:** ω = ck (modo acústico, Goldstone relativístico) =
  **fóton** ✓; ω = Dk² (modo difusivo, magnon não-relativístico) ✗.
- **Critério de morte:** dispersão não-linear (ω ∝ k², ou com gap).

### E3 — Catálogo de defeitos topológicos de n⃗

- Buscar todos os defeitos estáveis em n⃗; classificar por π₁, π₂, π₃ do
  espaço-alvo; medir energia, estabilidade, carga; verificar se há
  hierarquia (partículas leves/pesadas).
- **O que pode encontrar:** π₁(S¹)=ℤ vórtices (n⃗∈S¹); π₂(S²)=ℤ monopolos
  (n⃗∈S²); π₃(S³)=ℤ Skyrmions (n⃗∈S³).

### E4 — Colisão de defeitos de n⃗

- Criar dois defeitos opostos, colidir em alta energia, medir se há criação
  de novos defeitos e se a carga total se conserva.
- **Conexão:** criação de defeitos estáveis na colisão = criação de matéria
  do vácuo — o análogo de e⁺e⁻ → hádrons. Liga-se a SU6 (criação suave de
  B=1 falhou) e a FL3.

---

## 5. Conexão com resultados existentes

Este programa não começa do zero. Tem suporte (indireto) em:

```
LIV_VECTOR (LV1): toda plaqueta causal é um bivetor simples num plano
  tipo-tempo → A_μ é variável de orientação de link.   [DERIVADO]

MATTER_SU2 (SU3): o Skyrmion é um hedgehog de orientação n⃗(r)=r̂ da
  configuração de gauge.                                [DERIVADO]

BRIDGE_SU2_COEFF (SC1): o operador de Skyrme emerge da isotropia de
  Poisson — isotropia de orientação que gera o estabilizador. [DERIVADO]

VS1 (VACUUM_STRUCTURE): a densidade obedece à configuração de orientação,
  não o contrário — evidência de que n⃗ lidera.         [DERIVADO]
```

Todas são evidências **indiretas**. A hipótese do ferromagneto causal
**não foi testada diretamente** — é o que E1–E4 fazem.

---

## 6. O estado atual da sequência

```
FILA IMEDIATA:
  FQ2 — segundo calibrador π₁    ✅ EXECUTADO (jun/2026, PI5_synthesis.md)
                                  ε(n)=(n−1)mod2; ressalva spin-estat. reduzida

DEPOIS DE FQ2:
  TEIC_MASTER — organização + 4 papers    ← PRÓXIMO

APÓS PAPERS SUBMETIDOS:
  FN1 (E1) — correlações de orientação  ← PRIMEIRA NOVA CAMPANHA
  FN2 (E2) — espectro de magnons
  FN3 (E3) — catálogo de defeitos
  FN4 (E4) — colisão de defeitos
```

---

## 7. Nota honesta

A hipótese do ferromagneto causal é suportada por evidências indiretas
(VS1, LV1, SU3, SC1) mas **não foi testada diretamente**.

E1 pode mostrar que C(r) decai exponencialmente — o vácuo não tem ordem de
orientação de longo alcance. Nesse caso a hipótese morre e a investigação
registra o resultado, como fez com as cinco mortes de VACUUM_STRUCTURE.

A disciplina do projeto se mantém: critério de morte pré-registrado antes de
qualquer código; negativo reportado como negativo; nenhum parâmetro ajustado
para escapar de uma morte.
