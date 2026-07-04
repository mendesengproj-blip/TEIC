# SÍNTESE — A1 / C1 · Auditoria formal da guarda anti-circularidade

> Campanha de organização TEIC (Fase 2), Frente A, item A1 (gate de entrada).
> Pré-registro: `PRE_REGISTRO.md`. Relatório verbatim: `SCALE_LITERAL_REPORT.md`.
> Data: jun/2026. **Veredito: R-0 NÃO disparado — guarda VERDE, gate liberado.**

---

## 1. O que foi feito

**(i) Extensão da varredura.** `tests/test_no_circularity.py` varria só
`{src, experiments, results/matter, results/bridge, results/tier3,
results/dev_from_teic}`. `SCAN_DIRS` foi reapontado para **todo o tree gerador**:
`src`, `experiments`, `results/**`, `docs/campaigns/**` (inclui `sr_teic_core.py`).
Cobertura: **396 arquivos `.py`** (verificado; cobre `e6_bd_core.py`,
`sr_teic_core.py`, `su3_core.py`, `r5_group_core.py`). Break-test confirmou que a
guarda ainda detecta uma dilatação injetada.

**(ii) Detector de literais de escala.** Novo módulo
`tests/test_no_scale_literal.py`: faz `ast`-parse de cada gerador, extrai cada
literal numérico real (ignora complexos — função da outra guarda), e sinaliza
`|literal/X − 1| < 1%` contra uma tabela de **48 alvos** (c, G, ℏ, h, k_B, e,
m_e, a₀_MOND, a₀_Bohr, M_Pl, α, ℓ_Pl, t_Pl, ℏc + potências/recíprocos usuais).
Reporta arquivo, linha, valor, constante casada, erro relativo e **função
envolvente** (a dependência exigida pelo critério ii).

**(iv) CI/pytest.** Ambas as guardas ganharam função `test_*` descobrível por
pytest (a antiga `test_no_circularity.py` não tinha nenhuma — o passo de CI
coletava zero testes) e o workflow roda as duas explicitamente.

## 2. Achados da auditoria

- **(a) Dilatação SR/GR:** **0** em 396 geradores. Os matches de grep em
  comentários/docstrings e em ferramentas de auditoria (`results/audit/*`, cujo
  uso do padrão é regex de busca em string) são removidos por `_code_only`.
- **(b) Complexo não-rotulado:** **0**. Único achado fora de bloco —
  `results/foundations/r5_group/r5_group_core.py:44-45` (geradores de Gell-Mann
  de su(N)) — recebeu o marcador `# SU(3) GROUP-DEF COMPLEX`, a mesma exceção
  principiada de `su3_core.py` (matemática do grupo, não fase contrabandeada; o
  módulo não lê resultado de rede TEIC). **Não é morte.**
- **(c) Literais de escala:** **21 candidatos**, **todos classificados** como
  constante externa numa camada de **comparação / conversão de unidades /
  falsificação** — nenhum alimenta um gerador da rede causal:
  - `falsification/F_EHT.py`, `F_CMB.py` — testes de falsificação contra dados
    EHT / bound de Parker (G, c, ℓ_Pl, M_Pl, a₀);
  - `cmb/fm1/FM1_2_class_impl.py`, `cmb/fm4/fm4_core.py` — cosmologia de
    comparação CAMB/CLASS (S8 = MORTO; a₀ "SPARC-calibrated, NOT a CMB fit");
  - `cosmology/{c6,fn3,fn4,hq3}/*core.py` — "constantes externas / charter,
    nothing fit" (c, G, ℏ, M_Pl, a₀, EV_PER_JOULE=1/e);
  - `dev_from_teic/A2_saturation_scale.py` — a₀ dentro de bloco
    `# COMPARISON ONLY (never used by the generator)`;
  - `matter/baryon_quant/bq_core.py` — `HBARC=197.327 MeV·fm`, conversão padrão
    de r² adimensional da rede para fm (comparação com raio do próton).

  Tabela completa com a classificação por linha em `SCALE_LITERAL_REPORT.md` e em
  `JUSTIFIED_NOTES` (test_no_scale_literal.py). Falsos-positivos previstos no
  pré-registro (α, e, Bohr) não apareceram como problema; o único match de
  recíproco (`1/e_charge`) é o fator eV-por-joule, conversão de unidade.

## 3. Veredito (R-0)

**R-0 NÃO disparado.** Zero fórmula de dilatação e zero literal de escala física
em qualquer **gerador da rede causal**. Os motores que produzem os dados
adimensionais (`src/`, núcleos su(2)/su(3), motor de orientação E1/E4, sampler MC
`fm2`) não geraram **nenhum** match. As escalas físicas aparecem **só** na
fronteira de comparação com observação — exatamente onde a tese do programa
("forma emerge, escala é externa", tags [EXTERNO]/[POSTULADO]) prevê que devam
estar, e todas declaradas como tal no próprio código.

A circularidade que o programa diz ter evitado **de fato não existe** no tree
completo — antes este era um protocolo declarado verificado num subconjunto;
agora é um teste que roda em CI sobre todos os 396 geradores.

## 4. Consequência para a campanha

Gate A1 **VERDE** ⇒ R-0 do `PLANO_EXECUCAO.md` libera todo o paralelismo:
**B1** (razões internas K-indep), **A2** (Wilson no causet), **A3** (Goldstone
N/S(k)), **A4** (propagação BD), **A5** (resíduos), **B3∥B4** (fóton). Nenhuma
medição a jusante foi construída sobre fundação não-verificada.

## 5. Entregáveis (estado)

- [x] `PRE_REGISTRO.md` (critério + tabela + critério de morte)
- [x] `tests/test_no_circularity.py` — SCAN_DIRS estendido + `test_*` + r5 marcado
- [x] `tests/test_no_scale_literal.py` — detector + `test_*` + relatório
- [x] `SCALE_LITERAL_REPORT.md` — relatório verbatim (21 candidatos classificados)
- [x] `.github/workflows/ci.yml` — roda as duas guardas
- [x] `RESEARCH_MAP.md` — nota A1 no Protocolo de pesquisa
- [x] suíte completa verde (`pytest tests/ -q` = 6 passed)
