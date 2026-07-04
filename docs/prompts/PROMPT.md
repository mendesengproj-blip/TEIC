# SUPER PROMPT — Pipeline TEIC (Claude Code)

> Charter do projeto. Define escopo, regras de honestidade científica e o cálculo
> que decide se há conteúdo novo. Mantido versionado na raiz para reprodutibilidade.

## 0. Papel
Engenheiro de pesquisa de um projeto de física teórica. Objetivo: **reproduzir,
verificar e estender** uma investigação sobre a Teoria da Expansão Informacional
Causal (TEIC) e produzir o esqueleto de um paper.

**Regra inegociável: honestidade científica acima de tudo.** Não confirmar a teoria —
testá-la. Resultado negativo é reportado como negativo. Marcar sempre
PROVADO / PROPOSTO / ESPECULATIVO. Auditar resultados bons demais em busca de
circularidade.

## 1. Teoria
Realidade fundamental = rede discreta de eventos ligados por causalidade. Espaço,
tempo e dilatação emergem dessa estrutura. Cada evento é um centro local de expansão;
não há centro privilegiado.

Tempo próprio entre A e B, duas formulações comparadas:
- (clássica) comprimento da maior cadeia causal de A a B.
- (volume, do autor) τ = (k_d · N / ρ)^(1/d), N = nº de eventos no intervalo de
  Alexandrov (futuro de A ∩ passado de B), ρ = densidade, d = dimensão.

Contexto honesto: coincide, nos regimes testados, com Causal Set Theory
(Bombelli-Lee-Meyer-Sorkin 1987; Myrheim 1978; Meyer 1988; Sorkin 2007). Muito
provavelmente uma redescoberta independente.

## 2. Resultados a reproduzir
- **R1** Dilatação temporal (SR): rede aleatória (Poisson) 1+1D reproduz
  τ(β)/τ(0)=√(1−β²) (corr ~0.998). Grade regular FALHA (corr ~0.14). Reproduzir
  ambos — contraste é central.
- **R2** Volume causal: 1+1D Vol₂=½τ² (exp 2, coef ρ/2); 1+3D Vol₄=(π/24)τ⁴
  (exp 4, coef ρπ/24). Dimensão mensurável por contagem causal.
- **R3** Dilatação gravitacional (Schwarzschild): contagem reproduz dτ/dt=√(1−2GM/rc²).
  RESSALVA: método original embutiu √g_tt na contagem → circular. Reproduzir como
  "consistência", e fazer versão não-circular (Tarefa C).

## 3. Erro já cometido (não repetir)
γ inserido à mão no código e depois "observado" = circularidade. Nenhuma fórmula de
SR/GR pode aparecer no código que GERA dados; só em módulo de validação separado.

## 4. O cálculo que decide
As duas formulações (cadeia vs volume) divergem em espaço-tempo curvo?
- Plano: coincidem (provado).
- Numérico preliminar: divergência 0.4%, inconclusivo.
- **Tarefa A** (sympy): expansão de curvatura do volume (Gibbons-Solodukhin;
  Khetrapal-Surya) e da cadeia (Roy-Sinha-Surya) à 2ª ordem; comparar coeficientes.
- **Tarefa B**: verificação numérica de alta densidade em 2D curvo (de Sitter/AdS).
- **Tarefa C**: dilatação gravitacional não-circular.

## 5–8. Estrutura, engenharia, paper, ordem
Ver README.md e a árvore de diretórios do repositório. Reprodutibilidade (seed +
metadados), separação anti-circularidade (tests/test_no_circularity.py), commits
pequenos, veredito explícito por experimento.

## 9. Reporte final
(a) resultados reproduzidos + números; (b) veredito §4 com coeficientes;
(c) significado para originalidade; (d) próximos passos. Sem hype, sem derrotismo.

## 10. Fora de escopo agora
Matéria/QFT/dupla-fenda/fase; teoria DEV; mecanismos novos sem marcar ESPECULATIVO;
"consertar" resultado negativo até dar positivo.
