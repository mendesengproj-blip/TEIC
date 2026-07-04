# PRE-REGISTRO — A1 / C1 · Auditoria formal da guarda anti-circularidade

> Campanha de organização TEIC (Fase 2), Frente A, item A1 = C1.
> Fontes: `HIERARQUIA_EXPERIMENTOS.md` §C1, `PLANO_EXECUCAO.md` §5.
> **Gate de entrada bloqueante.** Nada da Frente B roda antes de A1 verde (R-0).
> Pré-registro escrito ANTES do detector de literais (disciplina do programa:
> critério e critério-de-morte antes de qualquer código).

---

## 1. Pergunta

Algum gerador **fora da varredura atual** (`SCAN_DIRS` cobria só
`src`, `experiments`, `results/{matter,bridge,tier3,dev_from_teic}`) contém:

- **(a)** fórmula de dilatação SR/GR (Lorentz `1/sqrt(1-β²)`, redshift
  `sqrt(1-2M/r)`, `gamma=1/sqrt…`);
- **(b)** número complexo não-rotulado (fora de bloco `COMPARISON ONLY` ou
  `SU(3) GROUP-DEF COMPLEX`);
- **(c)** **literal numérico que coincide com uma escala física** (c, G, ℏ,
  a₀, m_e, M_Pl e potências/combinações usuais) a **< 1 %**?

A tese do programa é "**forma emerge, escala é externa**". Um literal de escala
embutido num gerador e depois "observado" na saída é a versão-escala do pecado
de circularidade que a guarda de dilatação já proíbe.

## 2. Critério de sucesso (pré-registrado)

- **(i)** `SCAN_DIRS` estendido para cobrir **TODO gerador** (`results/**`,
  `docs/campaigns/**` incl. `sr_teic_core.py`, `experiments/**`, `src/**`);
  guarda de dilatação/complexos **VERDE** após extensão.
- **(ii)** Novo módulo `tests/test_no_scale_literal.py` produz um **relatório**:
  para cada literal `float` em código gerador, sinaliza se
  `|literal / X − 1| < 0.01` para X na tabela de constantes (§4), com a
  **dependência** (qual função o usa).
- **(iii)** **Zero literais de escala física não-justificados** em código
  gerador (todo candidato sobrevivente é coincidência benigna explicitamente
  classificada, ou está num arquivo `ALLOWED`/bloco rotulado).
- **(iv)** Ambas as guardas **descobríveis por pytest** e no CI (transforma
  "protocolo declarado" em "teste que roda").

## 3. Critério de morte (R-0)

A varredura encontra **≥ 1** fórmula de dilatação **OU** **≥ 1** literal de
escala física embutido num gerador que **alimenta uma medição publicada/em-prep**
→ **o resultado afetado é REBAIXADO e RE-AUDITADO** antes de qualquer Frente B,
e a correção é propagada ao paper. Reportar **verbatim**, não silenciar.
(Resultado de 1ª classe: a circularidade que o programa diz ter evitado existia.)

Distinção que NÃO dispara morte:
- Complexo de **definição do grupo** (Gell-Mann de su(N)) em arquivo que não lê
  resultado de rede TEIC → exceção `SU(3) GROUP-DEF COMPLEX` (matemática, não
  fase contrabandeada). Ex. esperado: `results/foundations/r5_group/r5_group_core.py`.
- Complexo numa comparação rotulada `COMPARISON ONLY` (compara contra QM
  postulada, não realimenta o gerador).
- Padrão de dilatação dentro de **docstring/comentário/string** (a guarda já
  ignora — testa só código executável) ou dentro de uma **ferramenta de auditoria**
  cujo único uso do padrão é como regex de busca.

## 4. Tabela de constantes (detector de literais)

Valores em SI (e formas usuais em unidades naturais), tolerância relativa **1 %**.
Para cada base X também se testam `X²`, `X³`, `1/X`, `1/X²`, `sqrt(X)` quando
fisicamente usuais, mais as combinações de Planck.

| Símbolo | Valor | Unidade |
|---|---|---|
| c | 2.99792458e8 | m/s |
| G | 6.67430e-11 | m³ kg⁻¹ s⁻² |
| ℏ (hbar) | 1.054571817e-34 | J·s |
| h | 6.62607015e-34 | J·s |
| k_B | 1.380649e-23 | J/K |
| e (carga) | 1.602176634e-19 | C |
| m_e | 9.1093837015e-31 | kg |
| m_e (energia) | 510998.95 / 0.51099895e6 | eV |
| a₀ (MOND) | 1.2e-10 | m/s² |
| a₀ (Bohr) | 5.29177210903e-11 | m |
| M_Pl | 2.176434e-8 (kg) / 1.220890e19 (GeV) | — |
| M_Pl reduzida | 2.435323e18 | GeV |
| α (estrutura fina) | 7.2973525693e-3 | — |
| ℓ_Planck | 1.616255e-35 | m |
| t_Planck | 5.391247e-44 | s |
| ℏc | 3.16153e-26 | J·m |

## 5. Escopo e limitação (honestidade)

O detector captura o **modo de falha realista**: a injeção *acidental ou de
conveniência* de uma constante SI / unidade-natural num gerador — exatamente como
a guarda de dilatação captura as formas específicas de Lorentz/Schwarzschild, não
toda contrabando concebível. Um adversário determinado poderia codificar uma
escala numa combinação não-tabulada ou já em unidades de rede; isso está **fora**
do alcance e é declarado aqui, não escondido. Falsos-positivos previsíveis (α e
e como acoplamentos adimensionais O(10⁻³–10⁻¹⁹), raio de Bohr vs G na mesma
década) são **reportados e classificados**, não suprimidos silenciosamente.

## 6. Entregáveis

1. `tests/test_no_circularity.py` — `SCAN_DIRS` estendido + função `test_*`
   descobrível por pytest. (r5_group_core.py recebe marcador `SU(3) GROUP-DEF
   COMPLEX`.)
2. `tests/test_no_scale_literal.py` — detector + `test_*` + relatório `__main__`.
3. `docs/campaigns/GUARDA_A1/SCALE_LITERAL_REPORT.md` — relatório verbatim.
4. `docs/campaigns/GUARDA_A1/SYNTHESIS.md` — veredito + status R-0.
5. `.github/workflows/ci.yml` — roda as duas guardas.
6. Linha no `RESEARCH_MAP.md` (plano §4, passo 1).
