# PUBLICATION_REVIEW.md — Papers III, IV, V

**Escopo:** revisão de estratégia editorial e estrutura de manuscrito. **Não** avalia
a física (assumida inalterada). Perspectiva: editor/referee cético de PRD, JCAP,
CQG, EPJC ou Foundations of Physics, fazendo o screening inicial.
Data: 2026-06-17.

---

## Veredito (1 linha)

A "Section 0" de ~4 páginas (tese central + hierarquia Núcleo/Aplicações + Tabela
Canônica de Status do programa inteiro + conquistas + fracassos) na abertura de
III/IV/V **prejudica** a probabilidade de publicação: dispara o heurístico
"theory of everything" antes do resultado específico. **Recomendação: remover a
Section 0 dos papers de submissão** (feito), mantendo só um parágrafo de contexto
+ citações. A Tabela completa fica no Master/Zenodo.

---

## 1–2. Section 0 ajuda, atrapalha ou é contraproducente?

- **Ajuda** apenas o leitor que *já* aceitou a TEIC (contexto cômodo).
- **Atrapalha** o editor do primeiro screening: 4 páginas de resumo de programa
  antes do resultado, afirmando derivar espaço-tempo, relatividade, gravitação,
  luz, matéria, confinamento, matéria escura, MOND — mais um catálogo de "mortes".
- **Contraproducente** no agregado: o público que decide a sobrevivência do paper
  (editor + 1–2 referees) é justamente o mais sensível a sinal de overreach. O
  benefício recai sobre quem não decide; o custo, sobre quem decide.

## 3. "Contribuição focada" vs "resolver toda a física"?

Com a Section 0: pende **forte para "resolver toda a física"**. Um autor
independente (sem afiliação institucional) + tabela de programa grandiosa antes de
qualquer resultado = amplificador de desk-reject. Sem a Section 0, cada paper é
**genuinamente focado**: III = rigidez estrutural do substrato; IV = uma predição
observacional (BTFR(z)) e seu teste; V = setor de cor SU(3).

## 4. Destino da Section 0

Avaliado: remover / parágrafo curto / meia página / apêndice / paper separado.
**Decisão adotada: substituir por um parágrafo curto de contexto + citações**,
igual para preprint e submissão. A Tabela Canônica completa permanece no
`TEIC_MASTER` (depósito Zenodo guarda-chuva) e em `theory_overview.tex` (ativo
opcional). Apêndice foi descartado (ainda sinaliza "manifesto" e infla o PDF);
paper separado de overview já existe (o Master).

## 5. Consistência com I e II

Ponto decisivo: **I e II (carros-chefe, já submetidos) não têm Section 0.** Mantê-la
em III/IV/V tornava os papers downstream mais finos *mais grandiosos* que os
flagship — estrategicamente invertido. **Remover a Section 0 alinha III/IV/V a I e
II.** (As cópias staged de Section 0 que existiam localmente em I/II foram
revertidas, restaurando-os à forma submetida.)

## 6. Abertura mais publicável por paper

- **Paper IV** — abertura mínima: a predição BTFR(z) no primeiro parágrafo. É o
  paper mais vendável (uma predição limpa, falsificável, com teste). A Introdução
  existente já fazia isso bem; só sobrava a Section 0 na frente. **Resolvido com a
  remoção.**
- **Paper III** — abrir pela cadeia de seleção como *resultado*, não como tese de
  programa; **retirar "cannot avoid" do título**.
- **Paper V** — abrir pelo resultado SU(3) (ferromagneto de cor → confinamento →
  octeto); remover "verdict is positive on all four phases" e "as everywhere in
  the programme".

## 7. Reescritas aplicadas (antes → depois)

**Paper III — título**
- Antes: *"The structure a causal network **cannot avoid**: measured selection…"*
- Depois: *"Structural selection in a discrete causal network: operators,
  dimension, gauge group, and stabiliser"*

**Paper III — afirmação organizadora (citação-bloco)**
- Antes: *"Each structural choice… is, on measurement, **not a choice**—and the
  forced structure is the observationally selected one."* + *"The claim of this
  **Letter**…"*
- Depois: *"For the structural choices tested, a Lorentz-invariant discrete causal
  substrate **admits essentially one option**, and that option coincides with the
  observationally selected structure."* (registro condicional; "Letter"→"paper" no
  texto; abertura agora com um parágrafo "Context." curto).

**Paper V — "Preview of the answer"**
- Antes: *"The substrate hosts SU(3) as readily as SU(2). We report a four-phase
  campaign **whose verdict is positive on all four phases**… the absolute lattice
  scale is underived, **as everywhere in the programme**."*
- Depois: *"We find that the substrate supports SU(3) as it does SU(2). We report a
  four-phase study; **in the cases tested** the substrate yields each feature… the
  absolute lattice scale is underived."*

**Paper IV** — nenhuma reescrita necessária além de remover a Section 0; a
Introdução existente já é concisa e neutra.

## 8. Frases fortes → alternativas conservadoras

| Forte (evitar) | Conservador (usar) |
|---|---|
| "cannot avoid" (título III) | "structural selection" / "structural rigidity" |
| "The central thesis…" | "We consider…" / "We examine whether…" |
| "The Core" / "The whole framework" | "the geometric and matter sectors" / "this construction" |
| "The programme establishes…" | "In the cases tested, we find…" |
| "verdict is positive on all four phases" | "in the cases tested, the substrate yields…" |
| "not a choice" (absoluto) | "admits essentially one option (in the cases tested)" |
| "as everywhere in the programme" | "as in the SU(2) construction" |

Princípio: trocar quantificadores universais ("every", "cannot", "the central")
por escopo declarado ("in the cases tested", "for the choices examined").

## 9. Resultado imediato vs resumo de programa primeiro

Os três ficam **mais fortes** com o resultado novo imediato. O referee chega ao
conteúdo avaliável na 1ª página em vez da 5ª. IV é o caso extremo: 4 páginas de
preâmbulo antes de uma predição que é, por si, o argumento de venda do paper.

## 10. Recomendação final

**Remover a Section 0** das versões de III/IV/V (e reverter I/II ao estado
submetido). Substituir por um parágrafo de contexto curto + citações. Manter a
Tabela Canônica completa apenas no `TEIC_MASTER` (Zenodo). Restaurar Paper III a
Letter PRL (a reclasse para PRD só existia por causa do tamanho da Section 0).

---

## Estado após esta revisão (implementado)

| Paper | Section 0 | Outras mudanças | Páginas | Build |
|---|---|---|---|---|
| I | revertida (forma submetida) | — | 13 | ✅ 0 erros/undef |
| II | revertida (forma submetida) | — | 6 | ✅ |
| III | removida | título sem "cannot avoid"; abertura suavizada; PRL restaurado | 3 | ✅ |
| IV | removida | — (Introdução já ótima) | 7 | ✅ |
| V | removida | "Preview" suavizado | 5 | ✅ |

`theory_overview.tex` permanece como ativo opcional (não é mais `\input` por
nenhum paper). `TEIC_MASTER` segue como guarda-chuva Zenodo com a Tabela completa.

## Ressalva honesta

Isto reverte parte da Opção C (STRUCTURE_ANALYSIS.md). Não é contradição: a Opção C
resolvia o "fatia isolada" para o **público de preprint**; esta revisão otimiza
para o **público de submissão** (editor/referee), cuja psicologia é oposta. O
insight do autor continua válido para as versões Zenodo — se desejado, um build
"full-anchor" do preprint pode reintroduzir a Section 0 via `theory_overview.tex`
sem afetar os arquivos de submissão.
