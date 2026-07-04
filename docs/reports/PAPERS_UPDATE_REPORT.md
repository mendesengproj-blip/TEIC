# PAPERS_UPDATE_REPORT — verificação da FASE 1 do MASTER_UPDATE

> Data: 2026-06-22. Tarefa: verificar se os papers de submissão precisavam das
> atualizações descritas na FASE 1 do prompt MASTER_UPDATE, aplicar o que faltava,
> e registrar honestamente o que já estava correto e o que ainda exige campanha nova.
>
> **Conclusão de uma linha:** a FASE 1 já estava essencialmente completa antes desta
> verificação — os papers foram atualizados por commits *posteriores* à escrita do
> prompt. Restava **um** gap real (cross-citação Goldstone→Photon-Arc), agora resolvido.

---

## Como verifiquei

Li `PAPER_DIAGNOSTICO.md`, o `git log`, e fiz grep direto em cada `.tex` de
`paper/submission/{goldstone_prd, matter_gravity_prd, photon_arc_cqg, su3_prd,
btfr_mnras, ferromagneto_prl}`. Os commits que implementaram a FASE 1 (todos
anteriores a esta verificação):

- `7890550` papers: matter-gravity (MG1+BQ) + photon-arc
- `0dfbe55` papers: strengthen 3 papers with robustness
- `3f7b04b` PHOTON_ARC: adicionar A5 (Anderson-Higgs)
- `8b6b6ed` PAPER_SU3: draft completo (Paper V)
- `33c4a1c` PAPER_FERROMAGNETO: draft (afirmação v2)

---

## Estado por paper (FASE 1)

| Paper | Atualização pedida pelo prompt | Estado verificado | Veredito |
|---|---|---|---|
| **Matter-Gravity** | MG1 (expoente −0.992; sóliton sourceia o próprio campo θ=G_net M/r); BQ (μ_p/μ_n; split N-Δ a 1% de ANW); seção "Beyond Poisson" respondendo ao revisor | `−0.992` + `θ=G_net M/r` na §VII; `μ_p/μ_n=−1.51`, `e=5.39 (1.0% de ANW)`, degenerescências `[4,16,36]` paramfree; **§"What the network adds beyond Poisson"** (l.243) | ✅ JÁ FEITO |
| **Goldstone** | varredura de robustez (densidade ×2/×0.5 + acoplamento alternativo); tabela de convergência com N explícita; arco da retratação do fóton | §"Robustness checks" (Tab. tab:robust): `ρ×0.5`, baseline `ρ×0.5`→`ρ×2`, e linha `Δτ-weighted coupling`; Tab. FSS com `N=175…1462`, `U4=2/3` em todos os tamanhos | ✅ JÁ FEITO + gap resolvido (ver abaixo) |
| **Photon-Arc** | A5 (Anderson-Higgs morto por não-localidade); E6c (setor magnético ∝H², 1.17% em R̂=2); E6e (extrapolação O(10%) requer curvatura sub-Planckiana) | A5 Anderson-Higgs (l.206); E6c (l.21); E6e `Δfrac_B~(1/R̂)^1.73~H²` (R²=0.997), sub-Planckiano (l.27) | ✅ JÁ FEITO |
| **BTFR** | apenas verificar fonte Times (`\usepackage{mathptmx}`) — NÃO modificar conteúdo | `\usepackage{mathptmx}` na linha 24 | ✅ JÁ FEITO |
| **SU3** | FLB2 + SU3_ORDEM com linguagem correta ("2ª ordem limpa excluída, 1ª fraca favorecida, L≳32 multicanônica necessária"); J_c≈0.3 (causal) vs ≈2.65 (lattice) declarado/explicado | "clean second order EXCLUDED; weak first order favoured; latent heat unresolved → strong-vs-weak open (needs L≥32)"; `J_c≈2.65` (cúbico) vs `J_c≈0.3` (causal), explicado pela coordenação (grau médio ≈45) | ✅ JÁ FEITO |
| **Ferromagneto** | (se existir) afirmação v2 corrigida: escala interna em unidades de rede, conversão rede→SI externa, analogia QCD com a diferença honesta que transmutação não foi identificada | Existe; cabeçalho e abstract v2 explícitos; "QCD analogy includes the honest difference: ... in TEIC no such transmutation mechanism is identified" | ✅ JÁ FEITO |

**Build:** todos os 6 PDFs estavam atualizados em relação aos `.tex` antes desta sessão;
`pdflatex` (MiKTeX) disponível. Após a edição do Goldstone, o paper foi recompilado
(pdflatex×3 + bibtex): 6 páginas, **zero** "Citation undefined", `PhotonArcCQG`
resolvida no `.bbl`. (O `bibtex` retorna exit≠0 por um warning pré-existente de
tipo de campo na entrada `Meyer1988`, sem relação com esta mudança.)

---

## O único gap real — RESOLVIDO

A retratação do fóton no Goldstone (§Conclusions/Outlook) retratava corretamente a
conjectura E4 e relocava a questão do fóton para o setor de conexão (link-variable),
**mas não citava o paper companion Photon-Arc** que completa o arco E4→E6c/e→A5. Não
era uma contradição — era uma cross-citação ausente.

**Correção aplicada:**
- Nova entrada `@misc{PhotonArcCQG}` adicionada a `paper/submission/goldstone_prd/
  TEIC_CONSOLIDATED.bib` e ao master `paper/TEIC_CONSOLIDATED.bib`.
- §Outlook: a frase sobre o setor link-connection como "well-posed, separate
  programme" agora aponta `\cite{PhotonArcCQG}` e resume seus achados (diamantes 100%
  elétricos; Anderson-Higgs frustrado por não-localidade; setor magnético só sob
  curvatura sub-Planckiana).
- §Conclusions: a frase de retratação agora termina com "where the companion
  paper~\cite{PhotonArcCQG} pursues it."

---

## O que NÃO precisa de mudança (estava correto)

Nenhum paper afirma algo que campanhas posteriores contradisseram sem declarar a
atualização. Em particular, a reversão parcial do FLB2 (2ª ordem → 1ª fraca, campanha
SU3_ORDEM_TRANSICAO) está corretamente incorporada no SU3 com a linguagem cautelosa
correta ("weak first order favoured, NOT first order confirmed").

---

## GAPs que exigiriam CAMPANHA NOVA (registrados, não inventados)

Fora do escopo da FASE 1 (atualização de texto), `PAPER_DIAGNOSTICO.md` lista o que os
papers genuinamente não cobrem e que só uma campanha — não uma edição — poderia mudar:

1. **Elo MOND-microscópico (FM2-1/C1)** é `[FRACO]` (ν=−0.4±0.1 vs −0.5, tamanho
   finito empurra para zero). Enquanto fraco, não sustenta afirmação de unificação
   física vácuo↔galáxias em nenhum paper — só compatibilidade.
2. **Ordem da transição SU(3) forte vs fraca** — não resolvida em L≤24; o próprio SU3
   declara "needs L≥32 with multicanonical". → é exatamente a FASE 2 / PRIORIDADE 1.
3. **Propagação dinâmica dos Goldstones (smeared)** — Goldstone reporta `c` via símbolo;
   propagação de pacote direta é fronteira técnica. → FASE 2 / PRIORIDADE 2.
4. **Setor B da 2-célula spacelike (Photon-Arc)** — obstrução do fóton testada via
   diamantes causais; intersecção de cones futuros é definição alternativa não testada.
   → FASE 2 / PRIORIDADE 3.
5. **Transmutação dimensional** — por que as escalas são externas continua em aberto;
   o Ferromagneto declara honestamente que nenhum mecanismo de transmutação foi
   identificado. → FASE 2 / PRIORIDADE 4.

Esses são GAPs verdadeiros, não correções de texto. Não foram "consertados" aqui —
estão na fila da FASE 2.

---

## Veredito FASE 1

- [x] Todos os papers compilam limpos (Goldstone recompilado e verificado; demais com PDF up-to-date).
- [x] Nenhum paper afirma algo contradito por campanha posterior sem declarar.
- [x] BTFR com fonte Times New Roman (`mathptmx`).
- [x] O único gap (cross-citação Goldstone→Photon-Arc) resolvido.
- [x] GAPs que exigiriam campanha nova registrados acima, não fabricados.

**FASE 1 fechada.** Próximo: FASE 2 / PRIORIDADE 1 (`SU3_ORDEM_L32`), charter
pré-registrado antes de qualquer código.
