# FL1_SU3_FOUNDATION — Fase C: Defeitos Topológicos e Confinamento

> Roda porque a **Fase B passou** (o vácuo SU(3) ordena). Duas perguntas
> pré-registradas: existe um defeito topológico estável (Skyrmion de cor)? E há
> análogo de confinamento (E(r)~σr)? Protocolo de defeito = E3/E3b (gradiente
> descendente + verificação térmica). Confinamento = potencial estático de
> Wilson loop. Motor: `su3_core.py` (Partes 7–8). Driver: `FLC_confinement.py`.
> Saídas: `FLC_confinement.{json,png}`. ~8 min, determinístico.

## ✅ VEREDITO: **FASE C PASSA** — Skyrmion de cor estável **E** confinamento

```
Existe um defeito topológico estável (o Skyrmion de cor, classe pi_3(SU(3))=Z),
estabilizado pelo termo de Skyrme externo declarado, e robusto a perturbação
térmica (proteção topológica). E o potencial estático carga-anticarga CRESCE
LINEARMENTE com a separação (lei de área, tensão de corda sigma>0) — confinamento.
Critério de morte (sem defeito estável OU E(r) sem crescimento): NÃO disparado.
Com A+B+C todas passando, a fundação para "quarks da TEIC" está estabelecida.
```

---

## [C1] Homotopia + carga topológica inteira

Espaço de vácuo da fase ordenada (Fase B) = SU(3)×SU(3)/SU(3)_diag ≅ **SU(3)**.
Grupos de homotopia:

| | π₁(SU(3)) | π₂(SU(3)) | π₃(SU(3)) |
|---|---|---|---|
| valor | 0 | 0 | **ℤ** |

`π₃ ≠ 0` → defeito **pontual** em 3D = **Skyrmion de cor** (carga `B ∈ ℤ`). (Nota:
não há vórtice de π₁ nem monopolo de π₂ — a estrutura de SU(3) força o defeito a ser
um ponto-partícula, como em SU(2).) O candidato B=1 é o hedgehog SU(2) embutido num
subgrupo SU(2) de SU(3) (resultado padrão: o Skyrmion mínimo de SU(3) vive num
subgrupo SU(2); a inclusão é isomorfismo em π₃).

Carga topológica **inteira**, convergindo com a resolução da rede:

| L | 15 | 21 | 31 | 41 |
|---|---|---|---|---|
| B | +0.806 | +0.892 | +0.948 | **+0.969** |

`B → +1` (e anti-Skyrmion `B → −1`). É a carga inteira de π₃(SU(3))=ℤ, calculada
nativamente pela fórmula de winding de SU(3) `B = (1/24π²)∫ε^{ijk}Tr(a_ia_ja_k)`.

---

## [C2] Estabilidade do defeito (protocolo E3/E3b) — com estabilizador externo

> **Ingrediente externo declarado.** A Fase A provou (Cauchy–Schwarz `K ≤ 6·TrM²` +
> teorema do sinal) que a dominância de Skyrme **não emerge** do cosseno em SU(3),
> exatamente como em SU(2). Logo o termo de Skyrme de 4 derivadas (E4) é **adicionado
> explicitamente** como estabilizador externo (`e_sk = 0.5`), **não escondido**. Sem
> ele, o termo sigma (E2) sozinho colapsa por Derrick.

### (a) Teorema de Derrick (radial, rigoroso)
Perfil B=1 relaxado; energia `E(λ) = λ·E2 + E4/λ` (escala exata de Derrick em 3D):

| | E2 | E4 | λ* = √(E4/E2) | mín. interior? | colapsa? |
|---|---|---|---|---|---|
| **com Skyrme** (e_sk=0.5) | 164.3 | 17.9 | 0.33 | **SIM** (M=2√(E2E4)=108) | — |
| **sem Skyrme** (E4=0) | 164.3 | 0 | — | não | **SIM** (λ→0) |

Com o termo de Skyrme, `E(λ)` tem **mínimo interior finito** (tamanho estável); a
barreira `E4/λ` impede o colapso. Sem ele, `E(λ)=λE2` decresce monotonicamente até
`λ→0` (colapso de Derrick). **O defeito é estável BECAUSE OF o estabilizador externo.**

### (b) Robustez térmica na rede 3D (proteção topológica)
Perturbação térmica SU(3) (amplitude 0.15) + curto resfriamento por gradiente (8
passos, removendo rugas UV sem colapsar o núcleo — o "cooled charge" de E3/E3b):

```
B0 = +0.948  ──ruído térmico──►  B = +0.688  ──resfriamento(8)──►  B = +0.942
energia:    (E2,E4)=(4138, 69037)  ────────────────────►  (82, 417)
```

O ruído injeta muita energia de gradiente e derruba a carga aparente; o resfriamento
cura as rugas, a energia despenca, e **B retorna a +0.94** — a carga inteira é
robusta. Proteção topológica confirmada. **→ DEFEITO ESTÁVEL.**

---

## [C3] Confinamento — potencial estático SU(3) de Wilson loop

Setor de gauge: campo de link SU(3), ação de Wilson (a ação mínima da Fase A).
Par carga–anticarga estático = loop de Wilson `r×t`; `V(r)` do decaimento temporal
`W(r,t)~e^{−V(r)t}`; tensão de corda `σ` da razão de Creutz `χ(2,2)` (robusta nos
loops pequenos bem medidos). `β` = acoplamento nu (varrido, **nunca input de QCD**);
`σ` é **medido**. Rede 8⁴, 30 medidas.

| β | ⟨plaq⟩ | V(r) | σ = χ(2,2) |
|---|---|---|---|
| 4.0 | 0.245 | [1.39, 2.73] | **1.35** |
| 4.5 | 0.291 | [1.23, 2.31] | 1.10 |
| 5.0 | 0.341 | [1.04, 1.98, 2.76] | 0.96 |
| 5.5 | 0.441 | [0.78, 1.46, 2.08, 2.65] | 0.67 |
| 6.0 | 0.566 | [0.47, 0.77, 0.96, 1.28] | 0.33 |

Dois sinais independentes de confinamento, ambos positivos:
- **V(r) cresce ~linearmente** com a separação — em β=5.5, `V = 0.78, 1.46, 2.08,
  2.65` (incrementos ≈0.68, 0.62, 0.56, quase constantes = potencial linear
  confinante `V(r)≈σr`). Em TODO β medido, V(r) sobe (SU(3) 4D confina em todo
  acoplamento, como esperado).
- **σ > 0** (lei de área) em todo β, e **σ DECRESCE monotonicamente** com β
  (1.35 → 1.10 → 0.96 → 0.67 → 0.33) — a tensão de corda enfraquece no acoplamento
  fraco, a direção correta da liberdade assintótica. Tudo medido, nada inserido.

(Nota honesta: em acoplamento forte σ é grande → loops grandes decaem rápido e
afundam no ruído; por isso `V(r)` em r grande e `χ(3,3)` são ruidosos lá. O sinal
robusto é `χ(2,2)` dos loops pequenos + `V(2)>V(1)`, usados no veredito.)

---

## Síntese honesta da Fase C

```
FASE C (defeitos / confinamento):
  Defeito topológico estável existe?         SIM (Skyrmion de cor, pi_3=Z, B=+1
                                             inteiro; Derrick-estável com Skyrme
                                             externo; B robusto a ruído térmico)
  Sinal de confinamento (E(r)~sigma r)?      SIM (V(r) linear; sigma=chi(2,2)>0 em
                                             todo beta; sigma(beta) decresce =
                                             liberdade assintótica)

[X] FASE C PASSA — Skyrmion de cor estável E confinamento. A fundação para física
    de "quarks" da TEIC está estabelecida.
```

### O que isto significa
1. **Trinca completa A+B+C.** O substrato causal de Poisson (i) **hospeda** SU(3)
   com ação PSD e causalidade (A), (ii) faz SU(3) **ordenar** num ferromagneto de cor
   (B), e (iii) suporta um **defeito de cor estável** e **confinamento** (C). É o
   análogo SU(3) completo do que E1–E3 fizeram para SU(2): vácuo ordenado → defeito
   topológico → (novo em SU(3)) confinamento.
2. **Ingrediente externo idêntico ao de SU(2).** O estabilizador de Skyrme é externo
   nos DOIS casos (Fase A já o previu via `K≤6·TrM²`). SU(3) não paga penalidade
   extra: a mesma peça que falta em SU(2) é a única que falta aqui.
3. **Confinamento é genuinamente novo.** É um fenômeno de acoplamento forte ausente
   de tudo que SU(2) produziu — e ele **emerge** da ação de Wilson mínima (lei de
   área medida, σ>0), sem nenhum número de QCD. Liga ao experimento do Polaris
   (estrutura do píon) e abre a Fase D.
4. **Anti-circularidade mantida.** Nenhuma massa de quark, valor de σ, ou α_s entrou.
   `e_sk` é escala de estabilizador declarada; `β` foi varrido; `σ` foi medido.

## Próximo passo (Fase D — aguardando aval)
Com A+B+C passando, o prompt prevê a **Fase D (síntese)**: comparar a massa do
Skyrmion SU(3) com o Skyrmion SU(2) (próton/nêutron?); construir o análogo do píon
(estado ligado quark+antiquark, spin 0); conexão Regge (defeito tipo-corda vs
corpo-rígido, ligando a [[c3]]); comparação qualitativa com o lattice QCD do Polaris.
**Só na Fase D** entram números de QCD reais, e apenas para comparação qualitativa.
Conforme o protocolo por fases, **não iniciar a Fase D antes do aval**.

---

*Reprodução:* `python FLC_confinement.py full` (≈8 min) ou `quick` (~30 s) →
`FLC_confinement.{json,png}`. Determinístico. numpy 2.4.4, scipy 1.17.1.
