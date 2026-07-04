# FM2-V — Gate: reproduzir E1 (ferromagneto) e E2 (mágnon)

> `FM2V_gate.py` → `.{json,png}`. Obrigatório antes de FM2-1/FM2-2.

## Veredito do gate: **PASS**

| Verificação | Critério | Medido | Status |
|---|---|---|---|
| **E1 — transição O(3)** | m sobe acima de J_c≈0.693, baixo abaixo | sobe (m: 0.05→0.83); knee em J_c | ✅ |
| **E1 — motor novo válido** | `fm2_core` concorda com `orientation_core` | \|Δm\|max = **0.015** | ✅ |
| **E2 — mágnon** | dispersão linear, c≈1 | c_fit = **1.014** | ✅ |

## Detalhe

- **E1:** ordem-parâmetro m(J) medido em dois motores independentes — o de E1
  (`orientation_core.O3Model`) e o novo (`fm2_core.O3Lattice`, periódico com campo
  externo). Concordam a |Δm|<0.015 em J∈{0.3..1.6}, com a transição O(3) 3D em
  J_c≈0.693 (valor de literatura/E1). Isso **valida o motor novo** que FM2-1/FM2-2
  usam.
- **E2:** dispersão de mágnon re-medida com uma corrida reduzida do símbolo BD de
  `e2_core` (estatística completa de E2 é cara; o gate só precisa da **velocidade**).
  c_fit=1.014 ≈ 1 (cone de luz), reproduzindo c=0.98 de E2. A classificação de forma
  (massless/massive) da corrida curta é ruidosa — não é critério do gate.

**Anti-circularidade:** J_c≈0.693 e c≈1 são âncoras COMPARISON ONLY; nenhuma escala
de segunda transição ou velocidade do som é inserida. Gate aprovado → FM2-1/FM2-2
prosseguem.
