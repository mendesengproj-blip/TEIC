# FLB2 — a ordem da transição SU(3) em L>12: primeira ordem DESFAVORECIDA

> Charter: `docs/prompts/FLB2_TRANSITION_ORDER.md` (kill criteria pré-registrados).
> Item 15 (Seção 6) do `RESEARCH_MAP.md`; o resíduo que FLB deixou explícito e o FLR
> re-flagou. Dados/código: `FLB2_transition_order.py`, `.json`. Run jun/2026.

## Veredito (honesto, não o auto-veredito do script): **1ª ordem DESFAVORECIDA; contínua-ou-muito-fraca; statistics-limited em L≤16**

FLB (L≤12) deixou a ordem da transição do ferromagneto de cor SU(3) (J_c≈2.65) sem
resolução, com sinais mistos e *hints* de 1ª ordem em L=12 (dip de Binder 0.43; salto
χ_max 5.2). FLB2 estende a L=14, 16 com grade fina em J e histogramas longos. As três
assinaturas decisivas, medidas em L=12/14/16 (rede cúbica, J em torno do pico):

| Assinatura | L=12 | L=14 | L=16 | Lê como |
|---|---|---|---|---|
| **D3 histograma de E em J_c** (calor latente) | unimodal | unimodal | unimodal | **contra 1ª ordem** (sem coexistência; bimod_coeff 0.42–0.49 < 0.555; dip 0.00) |
| **D2 dip de Binder** | 0.509 | 0.533 | 0.574 | **contra 1ª ordem** (dip *encolhe* com L; 1ª ordem aprofundaria) |
| **D1 χ_max(N)** | 10.4 | 5.6 | 9.0 | **inconclusivo** (ruidoso; nem N^0.67 contínuo nem N^1 volume) |
| **D4 salto de m** | 0.092 | 0.140 | 0.124 | **inconclusivo** (ruidoso, não afia com L) |

## Leitura honesta

- **A assinatura mais decisiva de 1ª ordem — bimodalidade do histograma de energia em
  J_c (calor latente/coexistência) — está LIMPAMENTE AUSENTE** em L=12, 14 e 16, e
  **não emerge** com o tamanho. O histograma foi medido *no* J_c(L) localizado (o pico
  de χ, = ponto de coexistência), não num J fixo fora da transição (correção sobre a
  v1, ver abaixo). Esta é a evidência mais forte, e ela aponta **contra** 1ª ordem.
- **O dip de Binder ENCOLHE com L** (0.509→0.574), o oposto do aprofundamento de 1ª
  ordem — também aponta contínua.
- **χ_max é plano/ruidoso** (10.4, 5.6, 9.0): não cresce como N^0.67 (contínua O(N)-like)
  *nem* como N^1 (lei de volume, 1ª ordem). Isto é **limitação de estatística** em
  L≤16 (o pico de χ é um estimador de variância, ruidoso com 3 sementes), não um
  resultado físico limpo — declarado honestamente.

**Conclusão:** as duas assinaturas robustas (histograma + Binder) apontam **contra
primeira ordem**; as duas ruidosas (χ_max, salto de m) não confirmam nenhuma das duas.
A previsão pré-registrada de **1ª ordem (literatura, N≥3) NÃO é suportada** nestes
tamanhos. O quadro mais provável é **contínua, ou uma 1ª ordem fraca demais para ser
visível em L≤16**. Os *hints* de 1ª ordem que FLB viu em L=12 (dip 0.43, χ_max 5.2)
**não reproduziram** sob amostragem mais limpa (FLB2 mede dip 0.51, e χ_max ruidoso) —
eram em boa parte **estatística**, não sinal.

## Correção registrada (transparência, disciplina do projeto)

A **primeira versão do FLB2** deu um auto-veredito "CONTÍNUA" que **rejeitei por
falha metodológica** antes de reportar: (i) a grade de J era grossa e o pico de χ
**deriva com L** (J_c 2.65→2.70), então χ_max parecia "plano" por *errar o pico*, não
por ser plano; (ii) o histograma foi amostrado num J **fixo** (2.65) que para L=16 cai
no lado *desordenado* (m=0.10), tornando "unimodal" sem sentido. Corrigido: grade fina
2.60–2.75, histograma medido *no* J_c(L) localizado, e um 4º diagnóstico (D4, salto de
m). Mesmo após a correção, **não inflei o auto-veredito**: o script imprime "CONTINUOUS"
pela contagem de votos, mas a leitura honesta é "1ª ordem desfavorecida, statistics-
limited" — porque χ_max ruidoso não confirma positivamente o expoente contínuo. (Mesma
postura das correções de FLR/Creutz e C1/Ward: corrigir a operacionalização, declarar,
não deixar o resultado automático overclaimar em nenhuma direção.)

## O que isto fecha (RESEARCH_MAP)

- Seção 3.2 / Seção 6 item 15 (ordem de transição SU(3)): de **[NUNCA TENTADO]/resíduo
  aberto** para **medido em L≤16 — 1ª ordem desfavorecida**. Não muda o veredito de FL1
  (a transição *existe*, FLB Fase B), nem a robustez (FLR): só caracteriza a ordem, e o
  faz **contra** a expectativa de 1ª ordem.
- **Resíduo remanescente declarado:** uma 1ª ordem fraca não está *estritamente*
  excluída; uma decisão definitiva exigiria L=24–32 com muitas sementes e histogramas
  longuíssimos (caro). O ganho marginal é baixo — o sinal decisivo (calor latente) já
  está ausente em três tamanhos.

## Anti-circularidade
Nenhum número de QCD; J_c, expoentes e bimodalidade saem só dos dados; "1ª ordem para
N≥3" é só enquadramento (COMPARISON ONLY). G0 reproduz FLB (J_c≈2.66). Sementes fixas;
guard `test_no_circularity.py` passa; `FLB2_transition_order.json` guarda todos os
diagnósticos crus (incl. ambos os estimadores e o histograma por L).
