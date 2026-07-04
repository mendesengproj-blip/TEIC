# E3b-V — Gate de validação do substrato causal 3+1D

> Gate obrigatório. Nenhuma medida de defeito procede antes de o substrato
> reproduzir SR, ter estrutura causal local e medir B corretamente em Poisson.
> Gerado por `E3bV_gate.py` → `E3bV_gate.{json,png}`.

## Veredito do gate: **PASS** — E3b-1 pode prosseguir

| Verificação | Critério | Medido | Status |
|---|---|---|---|
| **SR reproduzida (R1)** | corr(τ, √(1−β²)) > 0.99 | cadeia mais longa **0.9991** | ✅ |
| **Invariância de Lorentz** | Poisson invariante, rede quebra | CV_Poisson **3.1%** vs CV_rede **78%** | ✅ |
| **Seta do tempo** | 0 links com t_j ≤ t_i | **0 violações** (5 sementes) | ✅ |
| **Localidade** | ⟨grau⟩ < E1 (≈46) | ⟨grau⟩ = **23.0** | ✅ |
| **B em Poisson (hedgehog)** | B = +1 | **+1.000** (5 sementes) | ✅ |
| **B em Poisson (anti)** | B = −1 | **−1.000** | ✅ |
| **B em Poisson (vácuo)** | B = 0 | **0.0000** | ✅ |

## Substrato

- Sprinkling de Poisson 3+1D em `[0,T]×[−L,L]³`, ρ=1.5, T=3.0, L=4.0 → n≈2300 eventos.
- Acoplamento ao longo de **links causais** (relação de cobertura / diagrama de
  Hasse, `L = C & ~(C @ C)`): cada evento liga-se apenas aos vizinhos causais
  irredutíveis. ⟨grau⟩ ≈ 23 — **metade** do grafo de E1 (⟨grau⟩≈46), portanto
  genuinamente mais **local** (menos mean-field), como o charter exige.
- Mesma geometria de R1/D3 — Lorentz-invariante em distribuição.

## 1. Relatividade especial emerge no substrato

Relógio em movimento A=(0,0,0,0) → B=(T cosh φ, T sinh φ, 0, 0), β=tanh φ.
Tempo próprio medido **só por contagem causal** (sem fórmula de Lorentz no
gerador):

- **Cadeia causal mais longa** (proxy canônico do tempo próprio): corr = **0.9991**
  com √(1−β²), |desvio| médio 1.4%.
- **Volume do intervalo de Alexandrov** τ∝N^{1/4}: corr = 0.970 (estimador
  secundário; carrega viés conhecido de truncamento do diamante perto do cone de
  luz em 4D — reportado como diagnóstico, não critério).

A τ₀ invariante fixo (rapidez φ variável, cosh²−sinh²=1 — geometria pura), a
contagem no intervalo é **constante** para Poisson (CV 3%) e **oscila** para a
rede regular (CV 78%): a rede quebra Lorentz, o sprinkle não. SR reproduzida.

## 2/3. Estrutura causal e estimador de B

- **Seta do tempo respeitada por construção:** todos os links dirigidos têm
  t_dst > t_src — 0 violações em 5 sementes. Um defeito no passado não pode ser
  modificado pelo futuro: é exatamente a assimetria que E3b testa.
- **Estimador de B adaptado a Poisson:** degrau de Berg–Lüscher (ângulo sólido,
  Van Oosterom–Strackee) sobre **tetraedros de Delaunay**. Cada tetraedro é uma
  S² pequena (4 triângulos orientados para fora); faces internas cancelam entre
  tetraedros adjacentes, restando o grau na fronteira externa. Retorna
  +1 (hedgehog), −1 (anti), 0 (vácuo) **exatamente** em todas as sementes.

**Anti-circularidade:** nenhum acoplamento crítico, nenhuma lei de dispersão,
nenhum c entra no gerador; o cone dt²>dx² é a geometria de qualquer sprinkle.
√(1−β²) e ⟨grau⟩≈46 (E1) entram só na comparação.

**Conclusão:** o substrato está correto. O mecanismo 3 (rigidez do cone causal)
pode ser testado em E3b-1.
