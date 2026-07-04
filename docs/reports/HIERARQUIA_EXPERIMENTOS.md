# HIERARQUIA DE EXPERIMENTOS TEIC — tiers + fichas (Fase 1)

> Base factual: `INVENTARIO_PIPELINE.md`. Critérios de priorização (nesta ordem):
> **(1)** custo/benefício (código existente > código novo); **(2)** decisividade
> (resolve pergunta aberta, positiva OU negativa > suporte incremental); **(3)**
> dependência (destrava outros vem antes); **(4)** risco de obsolescência (invalidar
> trabalho a jusante tem prioridade).
>
> **Regra de pré-registro:** as fichas abaixo já contêm critério de sucesso E de morte
> verbatim. Nenhum é movido depois. Experimentos novos só rodam após sua ficha estar
> congelada (esta tarefa é preparação; execução vem após revisão do usuário).
>
> Frente A = **CONSOLIDAR** (Tier 1). Frente B = **ESCALAS** (Tier 2). As duas rodam
> em paralelo onde recursos permitem; o caminho crítico está em `PLANO_EXECUCAO.md`.

---

## Convenção das fichas

```
ID · título
 Pergunta:      a pergunta exata que responde
 Sucesso:       critério pré-registrado (verbatim)
 Morte:         critério pré-registrado (verbatim)
 Código:        existe | adaptar | novo
 Custo:         CPU / wall-clock estimado
 Destrava:      o que fica possível a jusante
 Depende:       pré-requisitos a montante
 Anti-circ.:    como a guarda cobre (ou precisa cobrir) este código
```

---

# TIER 0 — JÁ EM EXECUÇÃO (intocável)

### T0 · L≳48 SU(3) multicanônico / Wang-Landau (ordem da transição)
- **Pergunta:** a transição de cor de SU(3) é 1ª ordem **forte** ou **fraca** (ou
  contínua-com-forte-finite-size)? — o que PT em L=32 não pôde decidir (0 round-trips).
- **Sucesso:** amostragem multicanônica achata a barreira o suficiente para **≥1
  round-trip por réplica** e P(E) bimodal **com vale estável** → calor latente ΔE
  extraível; forte se ΔE/E não → 0 com L, fraca se → 0.
- **Morte (da própria 1ª ordem):** P(E) torna-se **unimodal** ao crescer L com vale que
  desaparece como volume → transição **contínua**; OU ΔE→0 mais rápido que 1/L^d.
- **Código:** existe + cluster (multicanônico é extensão de `su3_core`).
- **Custo:** cluster (fora do desktop); **não estimar/iniciar** — Tier 0.
- **Destrava:** fecha a única seção aberta do Paper SU3.
- **Depende:** —. **Conduta:** não iniciar, não interromper, não inspecionar processo.
  Incorporar resultado ao RESEARCH_MAP + Paper SU3 quando concluir.

---

# TIER 1 — CONSOLIDAÇÃO (Frente A: reforçar o que temos)

Ordem interna por (custo/benefício × decisividade × destrava-confiança):
**C1 → C2 → C3 → C4 → C5**.

### C1 · Auditoria formal da guarda anti-circularidade (estender + auditar)
- **Pergunta:** algum dos ~166 arquivos geradores **fora** da varredura atual contém
  (a) fórmula de dilatação SR/GR, (b) número complexo não-rotulado, ou (c) **literal
  numérico que coincide com c, G, ℏ, a₀, M_Planck a <1%**?
- **Sucesso:** (i) `SCAN_DIRS` estendido para cobrir TODO gerador (incl.
  `results/gauge`, `results/vacuum_structure`, `results/cosmology`, `results/foundations`,
  `results/cmb`, `results/phi_emerge`, `results/falsification`, `results/convergence`,
  `docs/campaigns/**` com `sr_teic_core.py`), guarda **VERDE** após extensão; (ii) novo
  teste de **literais de escala** produz relatório: para cada literal float em gerador,
  flag se |literal/X − 1|<0.01 para X∈{c,G,ℏ,a₀,m_e,M_Pl, e suas potências/combinações
  usuais em unidades naturais}, com dependência (qual função o usa); (iii) zero literais
  de escala física não-justificados em código gerador.
- **Morte:** a varredura encontra ≥1 fórmula de dilatação OU ≥1 literal de escala física
  embutido num gerador que alimenta uma medição publicada → **resultado afetado é
  rebaixado e re-auditado** (resultado de 1ª classe: a circularidade que o programa diz
  ter evitado existia em algum canto). Reportar verbatim, não silenciar.
- **Código:** adaptar `tests/test_no_circularity.py` (estender `SCAN_DIRS`; novo módulo
  `test_no_scale_literal.py`).
- **Custo:** ~0.5 CPU-dia (escrever o detector de literais + rodar). Trivial em wall-clock.
- **Destrava:** **confiança em TODO o resto** — transforma "protocolo declarado" em
  "teste que roda em CI". Pré-requisito moral de qualquer submissão.
- **Depende:** —.
- **Anti-circ.:** É a própria guarda. Ponto de atenção: `e6*` (bivetor/assinatura) e
  `sr_teic_core.py` (gerador próprio fora da varredura).
- **Risco de obsolescência:** ALTO no sentido bom — se houver um problema, melhor achar
  antes de submeter. Por isso é o **primeiro** de Tier 1.

### C2 · Goldstone FSS com N maior (5–10k) + expoente S(k)~k^α
- **Pergunta:** (a) os achados do setor de orientação (LRO, U4=2/3, m(N)) sobrevivem a
  N=5–10k? (b) o **structure factor S(k)~k^α** seleciona campo médio (α=0) ou
  relativístico (α=−1)?
- **Sucesso:** (a) m(N) continua monotônico e U4→2/3 (não-decaimento) em N≥5k; (b) ajuste
  de S(k) num range de k ≥ 1.5 década dá α com barra que **exclui** um dos dois valores
  (|α−0|>3σ OU |α+1|>3σ).
- **Morte:** (a) m(N) **vira a decair** em N grande (LRO era artefato de tamanho) → o
  ferromagneto causal do paper Goldstone é rebaixado; (b) α fica **entre** 0 e −1 sem
  excluir nenhum, mesmo com range amplo → indecidível por este observável (reportar como
  fronteira de método, não mover trave).
- **Código:** adaptar (motor de orientação E1/E4 existe; medida de S(k) é nova mas é
  FFT de C(r) já computado).
- **Custo:** N de 1462→10k é ~7× nós; memória O(N), tempo O(N log N)–O(N²) conforme
  estimador. Estimar ~1–3 CPU-dias desktop por ponto grande; FSS = alguns pontos.
- **Destrava:** endurece o paper Goldstone (PRD, em prep de submissão); decide a natureza
  (relativística vs campo médio) do setor de orientação — input para a frente de escalas
  (ξ, §B2).
- **Depende:** —. (S(k) usa o mesmo ensemble da parte (a).)
- **Anti-circ.:** sob C1 estendida (vacuum_structure entra na varredura).

### C3 · Loops de Wilson no substrato causal (não só no controle cúbico)
- **Pergunta:** o confinamento SU(3) (V~σr, σ=Creutz>0) medido **vale no causet**, ou o
  resultado depende do lattice cúbico de controle? Qual o erro sistemático da
  não-localidade do causal set sobre σ?
- **Sucesso:** σ_causet > 0 com significância, e σ_causet concorda com σ_cúbico dentro de
  uma barra sistemática **quantificada** (ex.: |σ_causet/σ_cúbico − 1| reportado com sua
  origem na não-localidade grau∝L^2.9) → o claim "confina no causet" fica suportado.
- **Morte:** σ_causet **não distinguível de 0** no causet (mesmo com loops controlados),
  OU a não-localidade impede qualquer estimador de área-vs-perímetro limpo (como em E7) →
  o confinamento SU(3) fica **[FRONTEIRA] como E5/E7**, e o Paper SU3 deve rebaixar o
  claim de confinamento "no causet" para "no controle cúbico".
- **Código:** adaptar (su3_core + maquinaria de Wilson de `results/bridge/wilson`); o
  obstáculo é o mesmo de E5/E7 (retângulos R×T no causet não-local) — pode terminar em
  fronteira.
- **Custo:** ~2–5 CPU-dias (loops grandes no causet são caros pela não-localidade).
- **Destrava:** decide se o resultado mais forte do Paper SU3 (confinamento) é "no
  causet" ou "no controle"; **risco de obsolescência ALTO** (pode rebaixar um claim
  publicado) → prioridade dentro de Tier 1.
- **Depende:** idealmente após C1 (gauge/causet sob guarda).
- **Anti-circ.:** su3_core já varrido; loops novos sob C1.

### C4 · Propagação dinâmica estável dos Goldstones (BD smeared, não sharp)
- **Pergunta:** ω=ck do setor de orientação aparece por **propagação direta** de um
  pacote, usando o operador SBD *smeared* (não o símbolo do operador sharp)? — fecha a
  brecha [FRACO] de E2 ("é do símbolo; campo não propaga estável").
- **Sucesso:** um pacote inicial localizado propaga com **relação de dispersão linear
  ω=ck medida na evolução** (não no símbolo), c dentro de ~5% de 1, **estável** (sem
  blow-up) por ≥ vários tempos de travessia, em ≥2 tamanhos.
- **Morte:** a evolução é **instável** (cresce sem limite) OU difusiva (ω∝k²) mesmo com
  smearing → o "fóton/Goldstone propagante" permanece só simbólico; E2 fica [FRACO]
  permanente e o Paper Photon-Arc deve manter a ressalva.
- **Código:** adaptar (operador BD smeared existe em `results/audit/bridge_recheck/AB3_bd`
  e `experiments/e10_sorkin_dalembertian`; falta o **driver de evolução temporal**).
- **Custo:** ~1–2 CPU-dias.
- **Destrava:** promove E2 de [FRACO] a [SÓLIDO] se passar; conecta ao setor de escalas
  (a velocidade c emergente é uma das razões internas).
- **Depende:** estabilidade numérica do BD smeared (conhecida por ser delicada).
- **Anti-circ.:** **crítico** — propagação direta é onde "injetar e^{ikL}" seria a
  recaída clássica; precisa rodar sob C1 com o bloco COMPARISON ONLY se comparar a QM.

### C5 · Resíduos de medição baratos (fechar débito de §2 do inventário)
- **Pergunta:** os resíduos menores conhecidos fecham? — ε(2) entre dois campos
  winding-2 distintos (FR); MG1 versão 3D-sprinkling.
- **Sucesso:** ε(2)=1 confirmado por um 2º campo winding-2 (remove a única ressalva de
  spin-estatística); MG1-3D reproduz expo≈−1 e G_net∝M.
- **Morte:** ε(2)≠1 com 2º campo → a lei ε(n)=(n−1)mod2 e a afirmação π₁=ℤ₂ precisam
  revisão (resultado de 1ª classe).
- **Código:** existe (PI/FR + MG1).
- **Custo:** baixo (~1 CPU-dia total).
- **Destrava:** remove as últimas ressalvas do Paper MG; baixa decisividade global mas
  barato. **Prioridade mais baixa de Tier 1** (não destrava nada a jusante).
- **Depende:** —.

---

# TIER 2 — ESCALAS E RAZÕES (Frente B: a fronteira nova)

> Alvo: NÃO fixar G, ℏ, a₀ em SI (provado [EXTERNO-B] por 4+ falhas). Descobrir se o
> substrato fixa **razões adimensionais entre domínios** — o único tipo de escala que a
> teoria pode prever sem unidade. Ordem interna: **B1 → B2 → B3/B4 → B5**.

### B1 · [PRIORIDADE DA FRENTE] Razões internas independentes de K (hierarquia)
- **Pergunta:** existe combinação de M_Sk (massa do Skyrmion), σ (string tension) e
  G_net (resposta gravitacional) que seja **independente da normalização K da ação**?
  Se for um número puro, ataca o problema de hierarquia (M_próton/M_Planck~10⁻¹⁹), que é
  um problema de **razão entre escalas** — o tipo que a teoria pode prever.
- **Sucesso:** uma combinação adimensional (ex.: M_Sk²·G_net, M_Sk/√σ, σ·G_net, ou
  análoga) é **constante a <5%** ao varrer K em ≥1 década, enquanto M_Sk, σ, G_net
  **individualmente** escalam com K (controle). Reportar o número puro com barra e sua
  forma algébrica.
- **Morte:** **toda** combinação testada ou (a) ainda escala com K (não é invariante de
  K), ou (b) é trivialmente 1/constante-geométrica já conhecida (não carrega hierarquia)
  → o substrato **não fixa razão de massa entre domínios**; a hierarquia permanece
  [EXTERNO-B], reportado como porta fechada bem-entendida.
- **Código:** **existe** — M_Sk (MATTER_SU2/BQ), σ (FL1 Creutz), G_net (MG1/D3D) já são
  medidos; falta só o **varredor de K + análise de invariância** (script novo curto que
  orquestra medidas existentes).
- **Custo:** ~2–4 CPU-dias (re-rodar M_Sk, σ, G_net em ~5 valores de K).
- **Destrava:** se positivo, é o **primeiro número de escala (razão) derivado** do
  programa — muda a tese "só formas e números puros adimensionais locais" para "também
  razões entre domínios". Alimenta o Paper Síntese.
- **Depende:** —. (Mais decisivo e mais barato da frente → entra primeiro.)
- **Anti-circ.:** sob C1; **atenção máxima** — nenhum K-independente pode vir de um
  literal de escala; a invariância tem de emergir do varredor.

### B2 · Razões de comprimento de correlação entre domínios (ξ_grav/ξ_cor)
- **Pergunta:** ξ(J) na transição (setor gravidade vs setor cor) — a razão
  ξ_gravity/ξ_color é fixada pelo substrato? Há assinatura de **transmutação
  dimensional** (ξ~exp(c/J) ou ν grande)?
- **Sucesso:** ξ_grav/ξ_cor converge a um valor fixo (<10%) ao crescer L em ambos os
  setores; OU ξ exibe forma exp(c/J) com c medido (transmutação) → razão de escala entre
  domínios derivada.
- **Morte:** ξ_grav/ξ_cor **deriva sem convergir** com L (é só efeito de tamanho), OU os
  dois setores não têm transição comparável definível → sem razão fixa entre domínios.
- **Código:** adaptar (ξ do setor cor sai de FL1/OT; ξ gravitacional precisa de
  definição — usar correlação do campo de orientação E1). **Definir o observável ξ_grav
  é não-trivial** e deve ser pré-registrado antes de rodar.
- **Custo:** ~3–6 CPU-dias (FSS de ξ em dois setores).
- **Destrava:** 2ª razão entre domínios; complementa B1 (massa vs comprimento).
- **Depende:** **C2** (natureza relativística vs campo médio do setor Goldstone informa
  como ξ_grav se define) e idealmente B1.
- **Anti-circ.:** sob C1.

### B3 · 2-célula spacelike via bivetor de cones de luz futuros (Direção B genuína)
- **Pergunta:** classificando o **bivetor de área das intersecções de cones de luz
  futuros** de eventos distintos (em vez de diamantes causais height-2), aparece um setor
  magnético spacelike — o que altura (E6b), curvatura (E6c/e) e acoplamento (E6d) não
  deram?
- **Sucesso (pré-registrado verbatim):** **fB > 0.01 a baixa curvatura** (R̂≫1, regime do
  universo observável), N-estável, gauge-invariante — i.e. a 2-célula spacelike existe
  fora do regime Planckiano onde E6c a achou marginal.
- **Morte:** fB ≤ 0.01 a baixa curvatura em toda construção de cone-futuro testada → a
  intersecção de cones futuros **também** é eletricamente dominada; o fóton magnético no
  causet fica [FRONTEIRA] e a Direção B junta-se a altura/curvatura/acoplamento como
  alavanca esgotada.
- **Código:** **novo** (classificador de bivetor de intersecção de cones futuros — não
  tentado no Paper Photon; estende `results/gauge/e6*`).
- **Custo:** ~3–7 CPU-dias (geometria de cones em sprinkling 4D).
- **Destrava:** se positivo, é "o resultado mais publicável do programa" (RESEARCH_MAP)
  — o fóton emergente real; se negativo, fecha a Direção B limpamente.
- **Depende:** —. (Independente de B1/B2.)
- **Anti-circ.:** sob C1 (gauge entra na varredura); bivetor não pode injetar fase.

### B4 · Geometria anisotrópica (Direção A)
- **Pergunta:** sprinkle em de Sitter **flat slicing com anisotropia controlada** eleva
  fB? Há direção preferencial em fB?
- **Sucesso:** fB cresce mensuravelmente com a anisotropia e **cruza 0.01 a baixa
  curvatura** (R̂≫1), com dependência clara na direção preferencial.
- **Morte:** fB permanece <0.01 a baixa curvatura para toda anisotropia testada (só sobe
  no regime Planckiano, como a curvatura isotrópica de E6c) → Direção A esgotada.
- **Código:** adaptar (sprinkler de Sitter de E6c + parâmetro de anisotropia).
- **Custo:** ~3–6 CPU-dias.
- **Destrava:** fecha a outra metade da fronteira do fóton (junto com B3).
- **Depende:** —. **Pode rodar em paralelo a B3** (testam direções diferentes da mesma
  lacuna; melhor que uma dê positivo).
- **Anti-circ.:** sob C1.

### B5 · Por que η e ℏ "não pinam" (teorema vs artefato de tamanho)
- **Pergunta:** a morte de η no valor genérico de Erdős–Rényi (FD1: k_c≈1) e a não-fixação
  de ℏ são **fundamentais** (teorema a provar) ou **artefato de tamanho** (recalcular com
  N maior)?
- **Sucesso:** (a) recálculo de FD1 com N maior mostra k_c **estável e não-genérico**
  (afasta de 1 com significância) → η pina (reabre FD1, hoje morto); OU (b) prova-se que
  k_c→1 é forçado pela estrutura ER do grafo causal (teorema) → morte de η fica
  **fundamental**, porta definitivamente fechada e entendida.
- **Morte:** k_c permanece ≈1 com N maior **sem** que se consiga provar que é forçado →
  fica indecidível entre genérico-fundamental e tamanho (reportar como tal; não declarar
  teorema sem prova).
- **Código:** adaptar (`sr_teic_core` de FD1; parte teórica é analítica).
- **Custo:** ~1–2 CPU-dias (numérico) + esforço analítico.
- **Destrava:** resultado negativo **bem-entendido** fecha a porta η definitivamente
  (1ª classe); informa diretamente a tese de escalas (por que escalas absolutas não
  pinam). Menor decisividade para hierarquia de razões → entra por último na frente B.
- **Depende:** —.
- **Anti-circ.:** `sr_teic_core.py` é **gerador próprio fora da guarda** → tem de entrar
  sob C1 antes de qualquer nova corrida de FD1.

---

## Resumo de priorização (por que esta ordem)

| Exp | Custo/benef. | Decisividade | Destrava | Obsolescência | Posição |
|---|---|---|---|---|---|
| **C1** guarda | existente, barato | alta (positivo/negativo) | confiança global | **ALTO** (achar cedo) | **1º absoluto** |
| **B1** razões K-indep | existente, médio | **alta** (1ª razão derivada?) | tese de escalas | médio | **1º da frente B** |
| **C3** Wilson causet | adaptar, médio-caro | alta | claim de confinamento | **ALTO** (rebaixa paper) | alto em A |
| **C2** Goldstone N/S(k) | adaptar, médio | alta (relativ. vs MF) | endurece PRD + B2 | médio | alto em A |
| **C4** propagação BD | adaptar, médio | média-alta | E2 [FRACO]→[SÓLIDO] | médio | médio A |
| **B3/B4** fóton 2-cell/anisotr. | novo/adaptar, caro | alta (fóton real) | maior publicável | baixo | médio B (paralelo) |
| **B2** ξ entre domínios | adaptar, caro | média | 2ª razão | baixo | depende de C2 |
| **B5** η/ℏ não pinam | adaptar, barato | média (fecha porta) | tese de escalas | baixo | último B |
| **C5** resíduos | existente, barato | baixa | últimas ressalvas MG | baixo | último A |
