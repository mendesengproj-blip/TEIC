# C1_KHOURY_EQUIVALENCE — TEIC ≡ Superfluid DM (Khoury): a equivalência formal

> **Charter PRÉ-REGISTRADO.** Critérios de morte ANTES de qualquer código.
> Item R3 do `RESEARCH_MAP.md` (FASE 3) e Caminho C1 de `CONVERGENCE_PATHS.md`
> (rank 2). Pré-requisitos prontos: E1 (⟨n⃗⟩≠0), E2 (magnon ω=ck), FM2-1
> (χ∥~h^{−0.4±0.1}), e o teorema de Milgrom da Fase 2 (deep-MOND L∝X^{3/2}
> compartilhado por DEV e Khoury).
>
> Motor: `results/cmb/fm2/fm2_core.py` (O(3) ferromagneto com campo h ↔ g). Script:
> `results/convergence/c1/C1_khoury_equivalence.py`. **NÃO modifica nada anterior.**

## A pergunta — SHARPENED

A Fase 2 já provou *analiticamente* que DEV e Khoury compartilham o limite deep-MOND
L∝X^{3/2} (teorema de Milgrom/AQUAL: μ→x força L∝|∇Φ|³). FM2-1 mediu χ∥~h^{−1/2} e
**identificou** com ν_MOND. O que C1 decide é mais fino:

> **A equivalência TEIC↔Khoury é uma identidade de ÁRVORE da ação do fônon
> (∝X^{3/2}, como Khoury postula), ou ela vive APENAS no setor de RESPOSTA
> longitudinal (χ∥), com o fônon transverso sendo quadrático (∝X, o magnon ω=ck)?**

Isto distingue a afirmação solta "o magnon da TEIC É o fônon de Khoury" da afirmação
rigorosa "as duas teorias compartilham o limite deep-MOND".

## K1 — analítico (na síntese)

Expandir o sigma model O(3) em torno de ⟨n⃗⟩: 2 Goldstones transversos (∝X,
quadráticos, ω=ck — E2) + 1 longitudinal. Khoury usa X^{3/2} (n=3/2), potência
**fracionária/não-analítica**, que um Goldstone livre **não tem**. A não-analiticidade
deep-MOND no O(3) aparece como a **anomalia de coexistência longitudinal**
χ∥~h^{−1/2} (Brezin–Wallace) — um efeito de **loop/IR dos Goldstones**, não um termo
cinético de árvore. Estabelecer onde a equivalência vive.

## K2 — numérico (o discriminador)

Medir, no MESMO ferromagneto O(3) ordenado, AS DUAS susceptibilidades vs h:
- **χ∥ = V·Var(m_par)** (longitudinal) → previsão deep-MOND/anomalia: ~h^{−1/2}.
- **χ⊥ = V·Var(M_transversa)** (transversa, o setor do magnon) → previsão Goldstone/
  Ward: ~h^{−1} (χ⊥ = ⟨m_par⟩/h), expoente DIFERENTE.
- **ρ_s(J)** (módulo de helicidade) — o candidato a "Λ" (constante de decaimento do
  Goldstone); testar se o coeficiente deep-MOND é fixado por ρ_s (rede) ou cavalga em
  escala externa (J, K).

## CRITÉRIOS DE MORTE (pré-registrados; herdados de CONVERGENCE_PATHS + sharpening)

```
GATE G0: reproduzir o expoente χ∥~h^{−p}, p≈0.5 de FM2-1 (sanidade do motor).

K2-SETOR (o discriminador):
  Se χ⊥ e χ∥ têm o MESMO expoente → a deep-MOND não distingue setores (improvável).
  Se χ⊥~h^{−1} (Ward) e χ∥~h^{−1/2} (anomalia), expoentes DISTINTOS →
    a equivalência com Khoury vive no setor LONGITUDINAL (resposta), NÃO no fônon
    transverso de árvore. → death criterion do charter ("ação transversa NÃO ∝X^{3/2}")
    DISPARA de forma informativa: o fônon transverso é ∝X (quadrático), não X^{3/2}.

K2-ESCALA (Λ):
  Se o coeficiente deep-MOND (via ρ_s) depende de J/K (escala externa) →
    "forma equivalente, escala externa" (não é derivação de ℏ/a₀ absoluto). [esperado]
```

## VEREDITO

```
EQUIVALÊNCIA DE ÁRVORE (forte)  se χ⊥ e χ∥ coincidem em ∝X^{3/2}: o fônon da TEIC É
                                 o de Khoury no nível cinético. [a priori improvável]
EQUIVALÊNCIA DE LIMITE (parcial) se χ⊥~h^{−1} (quadrático) e χ∥~h^{−1/2} (anomalia):
                                 TEIC e Khoury compartilham o limite deep-MOND no setor
                                 LONGITUDINAL (χ∥, anomalia IR emergente), enquanto
                                 Khoury o POSTULA na ação do fônon. Confirma e SHARPENA
                                 a Fase 2; mata a afirmação solta "magnon = fônon de
                                 Khoury". a₀ externo pela mesma estrutura.
```

## HONESTIDADE (declarada de saída)
ℏ e a₀ ABSOLUTOS continuam externos (VS5: α conteria ℏ; C3/CR3: a₀ externo). O alvo é
a RELAÇÃO ℏ/a₀ ↔ condensado e o SETOR onde a equivalência vive, não o valor. Nenhum
número de MOND/SI no gerador (a₀ é COMPARISON ONLY). Sementes fixas; JSON
auto-descritivo; G0 reproduz FM2-1 antes de qualquer alegação.
