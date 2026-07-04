# MATTER_EXPERIMENTS — refazendo T14–T21BIS com metodologia rigorosa

> Reimplementação **do zero** (não copia `../TEIC-GE`) dos experimentos de matéria.
> Não modifica R1–R3, e6–e11, D1–D3. Código e resultados em `results/matter/`.
> Auditoria que motivou: [`AUDIT_T14_T21.md`](AUDIT_T14_T21.md).

## Por que refazer

A auditoria INV1–INV6 mostrou que T14–T21BIS eram, em graus variados,
**tautológicos, circulares ou interpretativos** (massa = cost/⟨k⟩ tautológico;
gravidade com Poisson hard-coded; energia com blob de velocidade imposta; spin sem
o teste decisivo). Refazer = mesma pergunta, **metodologia correta**: *o que a rede
causal realmente deriva sobre matéria?*

## Protocolo (obrigatório em todos)

- **Anti-circularidade absoluta.** Nunca inserir no gerador: massa, energia,
  momento, carga, spin, F=ma, E=mc², Klein–Gordon, Dirac, Pauli. Esses conceitos só
  aparecem em blocos `COMPARISON ONLY`. O guard `tests/test_no_circularity.py` deve
  passar (estendido para varrer `results/matter/`).
- **Barras de erro.** ≥ 20 sementes por configuração; reportar média ± desvio.
- **Honestidade do veredito.** A = calculado e verificado; B = calculado, real, não
  verificado por completo; C = argumento físico sem cálculo quantitativo robusto;
  D = reinterpretação de resultado anterior. **O critério de morte é tão válido
  quanto o de sucesso.**

## Os experimentos

| # | refaz | pergunta | output |
|---|---|---|---|
| **M1** | T15/T16 | inércia = resistência à aceleração; m=F/a derivado, não inserido | `M1_inertia.{py,md}` |
| **M2** | T15/T16 | m_rede é Lorentz-invariante sob boost? (conecta R1) | `M2_lorentz_mass.{py,md}` |
| **E1** | T18/T19 | E_rede = m·(Δt/Δτ) usando o Δτ de R1; bate com m·γ? | `E1_energy.{py,md}` |
| **E2** | — | energia conservada? (rede cresce → simetria temporal imperfeita) | `E2_conservation.{py,md}` |
| **P1** | T20 | existe estado localizado estável sob □θ=0 (operador de Sorkin)? | `P1_localstate.{py,md}` |
| **P2** | T21 | relação de dispersão ω²=k²+m²? m bate com M1? | `P2_dispersion.{py,md}` |
| **P3** | T21BIS | spin: rotação 2π→±estado, 4π→+estado? | `P3_spin.{py,md}` |
| **P4** | novo | dois estados interferem (quântico) ou somam (clássico)? | `P4_interference.{py,md}` |
| **S1** | — | síntese: tabela A/B/C/D + afirmação honesta | `S1_synthesis.md` |

Ordem: **M1 → M2 → E1 → E2 → P1 → P2 → P3 → P4 → S1.** M1 é pré-requisito de
M2/E1; P1 de P2/P4. Se M1 falhar, M2/E1 ficam prejudicados mas P1–P4 continuam.

## O que não fazer

Não desenhar estruturas à mão. Não ajustar parâmetros para o resultado desejado.
Não usar "emerge" para reinterpretações: tempo e gravidade emergiram (provado);
para massa/energia/partículas "emerge" só vale se M1–P3 produzirem o verificável.

## Expectativa honesta (a confirmar pelos dados)

Mais do que geometria emerge, menos do que o Modelo Padrão. Massa/energia
provavelmente B (correlato fraco / consequência de R1+M1); estados localizados e
dispersão incertos (B se houver modo estável, C se dispersarem); spin e
interferência quântica provavelmente C (θ escalar não tem estrutura interna nem
amplitude complexa — consistente com e11).

Os vereditos reais estão em [`results/matter/S1_synthesis.md`](results/matter/S1_synthesis.md).
