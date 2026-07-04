# PAPER_AUDIT — PROGRAM_AUDIT_v2 (jun/2026)

> Diagnóstico de cada paper de submissão no estado **pós-delta** (após
> SU3_ORDEM_TRANSICAO, COLAPSO_SR_TEIC, FRONTEIRA_SETA_COSMOLÓGICA). Verificado
> contra os `.tex` reais em `paper/submission/`. Honestidade obrigatória: onde o
> baseline (`PROGRAM_AUDIT.md`) declarou um paper pronto e a varredura do `.tex`
> confirma ou desmente, registra-se o que o arquivo de fato contém.

**Conjunto de submissão real (4 papers):**
`btfr_mnras`, `goldstone_prd`, `matter_gravity_prd`, `photon_arc_cqg`.
(O esquema "Papers I–V" de `docs/reports/PAPERS_STRUCTURE.md` é a organização do
umbrella/Master, não o conjunto de submissão. Esta auditoria audita o conjunto de 4.)

---

## PAPER_GOLDSTONE_PRD — "Spontaneous orientational order and its relativistic scalar Goldstone modes"
**Alvo:** PRD · **Status atual: PRONTO PARA SUBMETER**

Cobertura de resultados:
- [x] E1 (ordem espontânea, FSS genuíno U₄=2/3, m=0.961→0.991) — coberto (§ferromagnet).
- [x] E2 (ω=ck via símbolo BD) — coberto, com a brecha "símbolo vs dinâmica" **declarada**.
- [x] E4 (Goldstones escalares internos, p=0.23, fóton retratado) — é o resultado-âncora.
- [x] Ponteiro SU(3) (octeto pseudoscalar) — presente (linhas 315–316, 456).

Críticas conhecidas a endereçar:
- [x] "ω=ck é do operador ou do campo?" — **endereçada** (§VIII, declarado símbolo).
- [x] "ordem é artefato de tamanho?" — **endereçada** (FSS).
- [~] S(k)~k^−0.58 expoente intermediário — **declarada** como diagnóstico limitado por N.

Impacto dos resultados novos:
- **SU3_ORDEM_TRANSICAO muda algo?** **NÃO.** O paper descreve o ferromagneto de
  *orientação* O(3) como transição "continuous second-order" em J_c≈0.08 (verificado,
  linhas 157–163) — esse é o setor O(3), **não** o setor de cor SU(3). As menções a
  SU(3) (linhas 59–60, 315–316, 456) são sobre a *natureza* dos Goldstones (mésons
  pseudoscalares), nunca sobre a *ordem da transição* de cor. **Nenhuma frase do paper
  afirma a ordem da transição SU(3)** → OT não toca nenhuma afirmação. Confirmado por grep.
- **SR↔TEIC muda algo?** NÃO (camada de colapso é ortogonal ao setor de Goldstone).

Ajustes necessários antes de submeter: **nenhum material.** (Opcional: um revisor pode
pedir o expoente de rigidez pinado em N maior — declarado como limitação, não bloqueante.)

**Veredito: PRONTO.** Paper mais limpo do conjunto; resultado-âncora é um negativo medido
honesto. Inalterado pelo delta.

---

## PAPER_MATTER_GRAVITY_PRD — "A soliton that sources its own gravitational field"
**Alvo:** PRD · **Status atual: PRONTO PARA SUBMETER**

Cobertura de resultados (verificado no `.tex`):
- [x] Gravidade Newtoniana (θ∝1/r, Poisson, Schwarzschild 0.2%) — coberto.
- [x] **MG1** (perfil próprio ε(r) sourceia θ=G_net·M/r) — **presente** (linhas 20, 55,
  129; "soliton sources its own gravitational field"). Não é mais "natural next step".
- [x] **Seção "Beyond Poisson"** — **presente** (§\ref{sec:beyondpoisson}, linha 243).
  Enfrenta a objeção "ação quadrática 3D dá 1/r trivialmente".
- [x] **BQ** (fenomenologia bariônica, [4,16,36], μ_p/μ_n, e=5.39) — **presente**
  (§baryon, linhas 24, 86, 274, 313).
- [x] Skyrmion SU(2) B=1 spin-½ fermiônico — coberto (linhas 9–10, 313).

Críticas conhecidas a endereçar:
- [x] "descobriu gravidade ou só Poisson?" — **respondida** (§Beyond Poisson).
- [~] A defesa "beyond Poisson" depende da razão de operador 5/9 medida em outra campanha
  (SC) — **dependência externa ao paper**, não desonestidade. Tornável mais autocontida.

Impacto dos resultados novos:
- **SU3_ORDEM_TRANSICAO?** Indireto e favorável: o paper se apoia no setor SU(3) como
  companion. OT **fortalece** a base SU(3) (caracteriza a transição) mas o paper não
  afirma nada sobre a ordem da transição → **nenhum ajuste requerido**.
- **SR↔TEIC?** NÃO.

Ajustes necessários antes de submeter:
1. (Opcional, baixa prioridade) Tornar a defesa "beyond Poisson" mais autocontida —
   resumir o argumento 5/9 em 1–2 frases em vez de terceirizar para SC.

**Veredito: PRONTO.** O mais autoconsciente dos quatro; todas as lacunas do baseline
(MG1, Beyond Poisson, BQ) estão fechadas no `.tex`. Inalterado pelo delta.

---

## PAPER_PHOTON_ARC_CQG — "Where, and why, a photon is hard to emerge in causal set theory"
**Alvo:** CQG · **Status atual: PRECISA DE 1 AJUSTE (A5) — quase pronto**

Cobertura de resultados (verificado no `.tex`, cabeçalho de campanhas):
- [x] Arco E4→E6e — **completo e atualizado** (E5/E7 não-localidade; E6/E6-3 operador
  BD-Lorentziano; E6b altura; E6c curvatura cruza 0.01; E6d morto; E6e frac_B∝H²).
- [x] Razão unificada da não-localidade — **declarada** (linha 70: "bare connection
  inherits the causal set's non-locality").
- [x] Obstrução restante (2-célula spacelike em baixa curvatura) — localizada (linha 34).
- [ ] **A5 (Anderson–Higgs) — AUSENTE.** Grep por `A5|anderson|higgs|frustrat` no `.tex`
  retorna **zero** ocorrências. **A lacuna #1 do baseline continua aberta.**

Críticas conhecidas a endereçar:
- [x] Limite contínuo do operador indefinido — **declarado** problema matemático aberto.
- [ ] **A terceira face da não-localidade (A5: condensado de Higgs frustrado) não está
  no paper.** O baseline (§3.3) já apontou isto como "a lacuna mais concreta do conjunto":
  o paper documenta a não-localidade em §4 (E5/E7) e §5 (E6), testa o acoplamento
  ferromagneto↔gauge em §6.3 (E6d), mas **não inclui A5**, que testa o *mesmo*
  acoplamento para a geração de massa de gauge (Higgs) e morre pela *mesma* não-localidade
  (~25 fases de gauge incoerentes/evento, ordem foge p/ eixo neutro, m_A=0). A5 é o
  **terceiro observável independente** que fortaleceria a tese central do paper.

Impacto dos resultados novos:
- **SU3_ORDEM_TRANSICAO?** NÃO.
- **SR↔TEIC?** NÃO. **A5 não é do delta desta rodada** — é anterior (commit `454c6fb`),
  mas continua não-integrado. Esta auditoria o reconfirma como o único ajuste de conteúdo
  pendente do conjunto inteiro.

Ajustes necessários antes de submeter (ordenados):
1. **[ALTA] Integrar A5** como a 3ª face da não-localidade (junto a E5/E7 e E6). É a
   adição que mais fortalece a tese sem custo de honestidade (A5 é morte medida com
   mecanismo quantificado). Recente o suficiente para entrar.
2. (Opcional) Frase explícita conectando A5/E5-E7/E6 sob "grau de Hasse ∝ N" como causa
   comum medida (a conexão 4.4 do baseline, hoje *parcialmente* declarada).

**Veredito: PRECISA DE A5 ANTES DE SUBMETER.** Sem A5, o paper é honesto mas
*incompleto em cobertura* num ponto que é exatamente o tema do paper. Com A5, é o
negativo informativo mais forte do conjunto. Bloqueio é de redação, não de resultado
(A5 já existe e está medido).

---

## PAPER_BTFR_MNRAS — "Does the radial-acceleration scale evolve? a₀∝H(z)"
**Alvo:** MNRAS · **Status atual: PRONTO NO CONTEÚDO — pré-condição de fonte NÃO VERIFICÁVEL no repo**

Cobertura de resultados:
- [x] Teste pré-registrado a₀(z)=a₀(0)H(z)/H₀ via BTFR; MUSE-DARK III (79 rotadores);
  a₀ sobe ≥15σ; casa SPARC a 0.5–0.9σ; RAR sem evolução desfavorecida ~19σ.
- [x] TEIC citada uma vez como proveniência, nunca usada (framework-independente).
- [x] Tensões abertas **declaradas** (slope 2–3σ mais rápido que H; z≥2 não medido;
  eixo de massa same-epoch sem evolução; σ_sys=0.04 dex é o teto).

Críticas conhecidas a endereçar:
- [x] Robustez do σ_sys=0.04 dex — tratada no corpo (é onde o resultado vive ou morre).
- [x] "evidence consistent with, not confirmation of" — enquadramento correto.

Impacto dos resultados novos:
- **SU3_ORDEM_TRANSICAO / SR↔TEIC?** NÃO (setores disjuntos).
- **MUSE-DARK III muda o conteúdo?** O paper **já usa** MUSE-DARK III (79 rotadores,
  0.33<z<1.44) como dataset central. Não é um resultado novo pendente; já integrado.

Pré-condição de fonte (charter): "rejeitado por fonte (Times New Roman via mathptmx)".
- **Verificação no repo:** o `.tex` usa `\documentclass{mnras}` + `\usepackage{mathptmx}`
  (linhas 21, 24), com comentário "Times New Roman (text + math) for MNRAS house style".
  **`mathptmx` É a house style da MNRAS** (Times é a fonte oficial da revista). **Não há,
  no repositório, nenhum registro de carta de rejeição** (grep no COVER e nos logs não
  acha "reject/desk/resubmit/font").
- **Diagnóstico honesto:** a premissa do charter ("rejeitado por fonte") **não está
  corroborada por nenhum documento do repo**. Ou (a) a rejeição ocorreu fora do repo
  (e-mail do editor) e não foi registrada, ou (b) é uma confusão — `mathptmx`/Times é
  precisamente o que a MNRAS exige, então uma rejeição "por usar Times" seria anômala.
  **Status: NÃO VERIFICADO.** Recomendo o autor confirmar: se houve rejeição real, qual
  foi o motivo textual do editor — porque a configuração de fonte atual está *correta*
  para MNRAS, não errada.

Ajustes necessários antes de reenvio:
1. **[BLOQUEANTE-INFORMAÇÃO] Esclarecer o motivo real da rejeição** (não está no repo).
   Se foi fonte, precisar qual (a config atual é a padrão MNRAS e não deveria ser causa).
2. Nenhum ajuste de conteúdo identificado.

**Veredito: PRONTO NO CONTEÚDO; reenvio bloqueado por uma pré-condição de informação
(motivo da rejeição) que não consta do repositório.** A física e a estrutura estão
honestas e completas.

---

## TABELA RESUMO

| Paper | Journal | Status | Ajuste necessário | Pré-condição |
|---|---|---|---|---|
| Goldstone | PRD | **Pronto** | nenhum material | — |
| Matter-Gravity | PRD | **Pronto** | (opcional) "Beyond Poisson" mais autocontido | — |
| Photon-Arc | CQG | **Precisa de A5** | integrar A5 (3ª face da não-localidade) | A5 já medido — só redação |
| BTFR | MNRAS | **Pronto no conteúdo** | nenhum de conteúdo | esclarecer motivo real da rejeição (ausente do repo) |

---

## LACUNA ESTRUTURAL (não de um paper) — confirmada e agora DESBLOQUEADA

**Não existe paper de submissão para o setor SU(3).** Confirmado por grep: nenhum `.tex`
em `paper/submission/` cobre SU(3)/cor/octeto (só aparições em `.bib`). É o resultado de
matéria mais forte depois do Skyrmion SU(2) — confinamento V~σr, octeto de 8 Goldstones
degenerado (OS), robustez ±10% (FLR) — todos **[SÓLIDO]** e **sem veículo próprio**,
vivendo apenas no umbrella (DOC1/DOC2).

**O que mudou no delta:** o portão que o baseline (§3.5) deixava com ressalva — "onde o
SU(3) for publicado, a ordem da transição precisa estar declarada" — **está agora
respondido por OT**. A "seção de ordem" pode ser escrita com a formulação honesta exata:
*"1ª ordem fraca é a leitura mais provável em L≤24; 2ª ordem limpa excluída; calor latente
abaixo da resolução; resolução definitiva (forte-vs-fraca-vs-contínua) exige L≳32
multicanônico/cluster."* Confinamento e octeto são **independentes da ordem** e podem ser
declarados como tal. → **PAPER_SU3 está desbloqueado** (ver NEXT_PAPER_CANDIDATES, C0).
