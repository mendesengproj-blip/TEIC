# FL1_SU3_FOUNDATION — Fase B: Ordenamento Espontâneo

> Roda porque a **Fase A passou** (SU(3) definível, ação PSD, causalidade preservada).
> Repete o protocolo de E1 (Monte Carlo, C(r), busca de J_c) para o campo SU(3) em
> vez de O(3): o vácuo SU(3) ordena espontaneamente? Onde, e como?
> Motor: `su3_core.py` (Partes 5–6, próprias). Driver: `FLB_ordering.py`.
> Saídas: `FLB_ordering.{json,png}`. ~1.9 h, determinístico (sementes fixas).

## ✅ VEREDITO: **FASE B PASSA** — o vácuo SU(3) ordena espontaneamente

```
O campo SU(3) NÃO permanece desordenado: existe uma transição de fase para um
vácuo ordenado, tanto na rede cúbica de controle quanto — decisivamente — no
PRÓPRIO substrato causal de Poisson da TEIC. Lá, o mesmo substrato que deu o
ferromagneto de orientação SU(2) (E1, Veredito A) também produz um "ferromagneto
de cor" SU(3): quebra espontânea SU(3)×SU(3) → SU(3) diagonal, com ordem de longo
alcance genuína (C_long = m², teste de clustering de Mermin) em J_c(causal) ≈ 0.3.
Critério de morte da Fase B (sem transição em nenhum J razoável): NÃO disparado.
```

## O modelo (análogo matricial de E1)
Campo de sítio `U_i ∈ SU(3)`, energia
`E = −J Σ⟨ij⟩ (1/3) Re Tr(U_i U_j†)`.
Generaliza o Heisenberg O(3) de E1 (`E = −J Σ n_i·n_j`): o produto escalar `n_i·n_j`
vira o invariante `(1/3)Re Tr(U_iU_j†) ∈ [−⅓,1]`, = 1 sse `U_i=U_j`. **Identidade
chave:** achatando cada `U` no vetor real de 18 componentes `v = (1/√3)[Re U, Im U]`,
`v` é unitário e `v_i·v_j = (1/3)Re Tr(U_iU_j†)` — o modelo é literalmente um O(18)
de Heisenberg restrito à subvariedade SU(3) (8-dim) de S¹⁷. Logo o parâmetro de
ordem `m = |⟨v⟩|` tem a mesma linha de base desordenada `1/√N` de O(3), e o platô
de `C(r)` = `m²` (clustering de Mermin). Ordenar quebra SU(3)×SU(3) → SU(3) diagonal.

---

## [1] Âncora cúbica (controle de literatura) + escala finita

Transição clara em **J_c ≈ 2.65**, estável em L = 6, 8, 10, 12:

| L | N | J_c(χ) | χ_max | Binder_min | m(J=1) | m(J=5) |
|---|---|---|---|---|---|---|
| 6 | 216 | 2.60 | 0.98 | 0.580 | 0.083 | 0.798 |
| 8 | 512 | 2.60 | 1.94 | 0.580 | 0.054 | 0.788 |
| 10 | 1000 | 2.65 | 2.07 | 0.594 | 0.038 | 0.783 |
| 12 | 1728 | 2.65 | **5.20** | **0.432** | 0.029 | 0.779 |

`m` sobe da linha de base (`m≈0.03≈1/√N`, desordenado) para `≈0.8` (ordenado); `χ`
pica em J_c; `E/link` cai de −0.06 para −0.71. **A transição existe sem ambiguidade.**

### Ordem da transição — sinais MISTOS, não resolvida em L ≤ 12 (honesto)
Pré-registrei a previsão de que SU(3) (N≥3) daria transição de **primeira ordem**
(diferindo de SU(2)≅O(4), 2ª ordem em E1). Os dados de escala finita dão um quadro
**ambíguo**, que reporto sem forçar:

- **A favor de 1ª ordem:** em L=12, exatamente em J_c=2.65, o cumulante de Binder
  **mergulha para 0.432**, bem abaixo dos valores das duas fases (desordenada ≈0.63,
  ordenada ≈0.667) — o *dip de Binder* é uma assinatura clássica de primeira ordem;
  e χ_max salta 2.07→5.20 de L=10 para L=12 (pico afinando).
- **A favor de contínua:** χ_max escala **sub-volume**, `χ_max ∝ N^0.72` (1ª ordem
  exigiria expoente ≈1; mesmo excluindo o ponto L=10 subamostrado dá 0.80); o
  calor específico mal cresce (`Cv_max ∝ N^0.21`); e o **histograma de energia em
  J_c é unimodal** (sem calor latente / coexistência clara, latente estimado ≈0.04).

**Conclusão honesta:** a transição é real e bem localizada (J_c≈2.65), mas seu
caráter (primeira ordem fraca vs contínua) **não é definitivamente resolvido** nestes
tamanhos. Minha previsão pré-registrada de 1ª ordem **não foi confirmada** — há
suporte parcial (dip de Binder) mas as assinaturas decisivas de 1ª ordem (lei de
volume em χ, bimodalidade de energia) **não apareceram**. Um estudo de escala finita
dedicado (grade de J mais fina em torno de 2.65, L≥16, histogramas longos em J_c)
poderia fechar isso — mas não é necessário para o veredito da Fase B.

---

## [2] Substrato causal — o vácuo real da TEIC (o resultado central)

Sprinkling de Poisson 3+1D, grafo de Hasse (mesmo substrato de SU(2)/E1),
`C(r)` por distância de cadeia-mais-longa (tempo próprio causal). `n≈2152`,
`avgdeg≈45` (a alta coordenação conhecida dos links causais 4D).

| J | m | χ | C(r) | C_long | m² |
|---|---|---|---|---|---|
| 0.0–0.2 | 0.02–0.03 | ~0.04 | insuf. (sem platô) | ~0 | ~0 |
| **0.3** | 0.180 | **0.71** (pico) | — | 0.038 | 0.032 |
| 0.5 | 0.740 | 0.03 | **const** | 0.535 | 0.548 |
| 1.0 | 0.874 | 0.04 | **const** | 0.752 | 0.763 |
| 2.0 | 0.932 | 0.03 | **const** | 0.854 | 0.868 |
| 6.0 | 0.957 | 0.07 | **const** | 0.891 | 0.916 |

- **Fase desordenada exposta** (J≤0.2): `m` na linha de base `1/√N≈0.02`, `C(r)` sem
  platô — o vácuo SU(3) está genuinamente desordenado a baixo J. (A varredura foi
  estendida a J baixo justamente para expor isto e tornar o critério de morte um
  teste real, como E1 fez para O(3) — extensão declarada, não escondida.)
- **J_c(causal) ≈ 0.3** (pico de χ). Fica **muito abaixo** do J_c cúbico (≈2.65)
  pela alta coordenação do grafo causal (avgdeg 45 vs 6 do cúbico) — exatamente o
  mesmo deslocamento que E1 observou para O(3).
- **Ordem de longo alcance GENUÍNA** (J≥0.5): `C(r)` classificado **`const`** e
  `C_long = m²` dentro de ~1–3% (clustering de Mermin: 0.5→2.3%, 1.0→1.4%,
  2.0→1.7%, 6.0→2.8%). Não é pseudo-ordem nem artefato — é LRO de verdade.

Este é o **ferromagneto de cor SU(3)**: o análogo direto do Veredito A de E1
(ferromagneto causal de orientação) para SU(2). O mesmo vácuo de Poisson que escolhe
uma orientação `n⃗` (E1) também escolhe uma "direção de cor" SU(3) coletiva.

### Fases múltiplas?
O prompt pediu para documentar qualquer fase. O modelo principal-chiral com overlap
na representação fundamental exibe **uma única transição de ordenamento** (o
ferromagneto diagonal-SU(3)). Testei um parâmetro de ordem natural (`m=|⟨U⟩|`).
Estrutura de fases mais rica (análogos nemáticos) exigiria acoplamentos/representações
diferentes (ex.: overlap na adjunta), fora do modelo mínimo — escopo honesto: aqui
há uma fase ordenada, bem definida.

---

## Síntese honesta da Fase B

```
FASE B (ordenamento):
  Transição de fase encontrada?              SIM (cúbico e causal)
  J_c(SU(3)) cúbico =                        ≈ 2.65
  J_c(SU(3)) causal =                        ≈ 0.3   (alta coordenação, como E1)
  Ordem de longo alcance no substrato?       SIM (C_long = m², clustering de Mermin)
  Ordem da transição:                        NÃO resolvida em L≤12 (sinais mistos:
                                             dip de Binder ⟶ 1ª ordem; χ∝N^0.72 +
                                             energia unimodal ⟶ contínua).
                                             Previsão pré-registrada de 1ª ordem
                                             NÃO confirmada — correção honesta.

[X] FASE B PASSA — o vácuo SU(3) ordena espontaneamente. Existe um "ferromagneto
    de cor" no mesmo substrato causal que deu o ferromagneto SU(2) (E1). Prosseguir
    para a FASE C (defeitos topológicos / confinamento) é justificado.
```

### O que isto significa para o programa
1. **Paralelo E1 estendido a SU(3).** O substrato de Poisson não só *hospeda* SU(3)
   (Fase A) — ele faz SU(3) **ordenar coletivamente**, como fez com a orientação
   `n⃗` em E1. O vácuo TEIC tem agora uma fase de cor ordenada além da fase de
   orientação. Liga-se a [[teic-project-state]] (setor de matéria) e a E1.
2. **Vácuo ordenado em mãos para a Fase C.** O espaço de vácuo (coset
   SU(3)×SU(3)/SU(3)_diag ≅ grupo SU(3)) é o ponto de partida para classificar
   defeitos topológicos (π_n) e testar confinamento na Fase C.
3. **Correção honesta pré-registrada.** A expectativa de 1ª ordem para SU(3) não se
   confirmou de forma limpa; os dados de escala finita são ambíguos. Registrado como
   tal — o veredito da Fase B (existe ordenamento) não depende disso.
4. **Anti-circularidade mantida.** Nenhum número de QCD entrou; J_c, expoentes e
   classificação saíram só dos dados; a única referência externa ("1ª ordem para
   N≥3") foi usada apenas para enquadrar a previsão, nunca como input.

## Próximo passo (aguardando aval)
**FASE C — defeitos topológicos / confinamento:** classificar π₁, π₂, π₃ do espaço
de vácuo SU(3)×SU(3)/SU(3)_diag ≅ SU(3) [`π₁(SU(3))=0`, `π₂(SU(3))=0`, `π₃(SU(3))=ℤ`
→ candidato a Skyrmion de cor]; testar estabilidade sob relaxamento (protocolo
E3/E3b); buscar confinamento via energia carga–anticarga `E(r)~σr` (análogo ao
Wilson loop). Critério de morte C: nenhum defeito estável, OU defeito sem
confinamento. **Não iniciar a Fase C antes do aval**, conforme o protocolo por fases.

---

*Reprodução:* `python FLB_ordering.py full` (≈1.9 h) ou `quick` (≈8 min) →
`FLB_ordering.{json,png}`. Determinístico. numpy 2.4.4.
