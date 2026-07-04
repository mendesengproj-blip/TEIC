# results/cmb/fm2 — campanha FM2_TWO_PHASE (jun/2026)

> Charter: `FM2_TWO_PHASE.md` (raiz). Continua FM1 (que matou o MOND-μ de fase
> única). Pergunta: a TEIC+DEV completa (ferromagneto E1 + mágnon E2) dá a
> **inversão** que MOND puro não dá — matéria escura e MOND como duas fases do
> campo n⃗ — suprimindo σ8 em vez de realçá-la? **NÃO modifica campanhas anteriores.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **FM2-V** | E1 (ferromagneto) + E2 (mágnon) reproduzidos? | **PASS** — J_c≈0.693 (2 motores, \|Δm\|<0.015); c_fit=1.014 | `FM2V_gate.{py,json,png}` |
| **FM2-1** | segunda transição no gap (Botão 1)? | deep-MOND reproduzido (χ∥~h^(−0.4), Goldstone) MAS sem 2ª transição no gap → **C (C1/C4)** | `FM2_1_second_transition.{py,md,json,png}` |
| **FM2-2** | som do condensado na janela de Jeans (Botão 2)? | c_s/c ∈ [0.14, 6.4], O(1) → free-streama → **C3** | `FM2_2_condensate_cs.{py,md,json,png}` |
| **FM2-4** | uma fase dá MOND+Jeans+fundo ΛCDM? | **NÃO** — obstrução estrutural | `FM2_4_background.md` |
| **FM2-5** | síntese | **C — MORTE: duas fases não invertem S8** | `FM2_5_synthesis.md` |

Motor: `fm2_core.py` (ferromagneto O(3) periódico L³ com campo externo h∝g,
Metropolis checkerboard vetorizado β=1; susceptibilidade longitudinal χ∥(h); módulo
de helicidade ρ_s ensemble-averaged; c_s=√(ρ_s/χ)). Importa `orientation_core` (E1)
e `e2_core` (E2) só no gate. Self-test: `python fm2_core.py`.

## Resultado de uma linha

**A estrutura de duas fases da TEIC+DEV NÃO inverte S8 — e por uma obstrução
estrutural.** Os dois botões pedem fases **opostas** do ferromagneto: o realce MOND
quer a fase **ordenada** (divergência de Goldstone em χ∥, χ∥~h^(−1/2)), a supressão
de Jeans quer o **ponto crítico** (c_s→0 só em J_c). Nenhum J único dá os dois. O
condensado ordenado tem c_s~O(c) (relativístico, travado por R1+E2) → **free-streama**
(C3); a divergência deep-MOND é **sustentada** até g/a₀≲10⁻³ sem 2ª transição no gap
(C1/C4) — confirmando microscopicamente o runaway de FM1. **Veredito C.** Mas há um
**resultado positivo**: a interpolação MOND ν=1/√(g/a₀) da DEV **emerge** da resposta
de Goldstone do ferromagneto de orientação (origem microscópica, liga Paper I a E1).

## Honestidade / engenharia

- **FM2-V valida o motor novo:** `fm2_core.O3Lattice` concorda com o motor de E1
  (`orientation_core.O3Model`) a |Δm|<0.015 na transição O(3) 3D (J_c≈0.693).
- **a₀ de SPARC; a_c2 e c_s MEDIDOS na rede; nenhum σ8/KiDS inserido** (anti-
  circularidade dura). As duas janelas (gap a_c2 ∈ (0.005,0.016); Jeans c_s/c~10⁻³)
  fixadas no charter ANTES de medir; nenhuma atingida; nenhum parâmetro ajustado.
- **Mortes pré-registradas pontuadas como escritas** (C1 divergência sustentada / C3
  c_s~c / C4 a_c2 fora do gap). Desfecho mais provável pré-registrado (B/C) confirmado.
- **Caveats:** χ∥ ainda sobe na borda inferior de h (h_c não resolvido limpo; mas
  a_c2/a₀≲0.001 < gap em qualquer leitura). FM2-2 mede c_s na rede O(3) (não-
  relativística) normalizado pelo mágnon; o c_s relativístico do condensado a
  densidade finita exigiria a ação completa. FM2-4 é consistência qualitativa
  (CLASS indisponível, ver FM1).
- **Reabertura (cálculo honesto):** a massa do vetor m_A (Paper II) daria ξ_A=ℏ/(m_A c)
  ≈ **17 pc** (= "L<17 pc" do Paper II) — **sub-galáctico, ~6 ordens abaixo da escala
  de σ8 (12 Mpc)**, e no extremo de ALTA aceleração (lado newtoniano), não no gap.
  **NÃO muda o Veredito C.** Um corte cosmológico exigiria m~5×10⁻³¹ eV (~7×10⁵× mais
  leve), massa **excluída** pelo próprio Paper II → seria escala NOVA, não o m_A.
  (O m_A prevê blindagem sub-galáctica da MOND ~17 pc: aglomerados/binárias largas.)
  O Botão 2 exigiria a eq. de estado do condensado + ação relativística + CLASS.

## Regras (as de sempre)

Charter pré-registrado com predições + critério de morte ANTES de qualquer código;
gate de engenharia (FM2-V) reproduz E1/E2 e valida o motor novo antes da medição;
negativos reportados (ambos os botões morrem; obstrução estrutural); positivo também
reportado (origem microscópica do ν MOND); anti-circularidade (a₀ de SPARC; a_c2, c_s
da rede; σ8 só COMPARISON); 20 sementes em FM2-1. Veredito C registrado sem inflar a
teoria. Ver `FM2_5_synthesis.md`.
