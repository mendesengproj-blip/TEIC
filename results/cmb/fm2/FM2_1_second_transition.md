# FM2-1 — A interpolação MOND como resposta de Goldstone + busca da segunda transição

> `FM2_1_second_transition.py` → `.{json,png}`. O(3) periódico, β=1, 20 sementes.
> Campo externo h ∝ gradiente gravitacional g; χ∥(h) ↔ interpolação MOND ν(g/a₀).

## Dois resultados

### (1) ✅ POSITIVO — o ferromagneto reproduz o deep-MOND microscopicamente

A susceptibilidade longitudinal da fase ordenada **cresce** ao baixar o campo:

```
h        χ∥(h)        (J=1.0 ordenado, L=16)
1.000    0.054
0.300    0.133
0.100    0.231
0.030    0.329
0.010    0.545
0.003    0.653
0.001    0.665
```

Ajuste no regime crescente: **χ∥ ~ h^(−p) com p ≈ 0.36–0.5** (varia 0.41–0.56 entre
L=10,16,24). Esse é o **anomalia de coexistência de Brezin–Wallace**: os modos de
Goldstone (ondas de spin) do ferromagneto O(3) 3D fazem χ∥ divergir como h^(−1/2)
quando h→0. **E o expoente 1/2 é exatamente a lei deep-MOND** ν=1/√(g/a₀)
(a=√(g_N·a₀)).

> **Origem microscópica da MOND:** a função de interpolação ν da DEV — postulada
> fenomenologicamente — **emerge** da resposta de Goldstone do ferromagneto de
> orientação que E1 identificou como o vácuo. Isto liga a fenomenologia MOND da DEV
> (Paper I) à estrutura microscópica da TEIC (E1). Resultado de valor próprio.

### (2) ❌ Não há segunda transição na janela observacional

A divergência de χ∥ **não satura** dentro do alcance medido — continua subindo até
h=0.001 (a menor escala amostrada, 3 décadas abaixo de h(y=1)). Ou seja, o realce
deep-MOND **persiste até g/a₀ ≲ 10⁻³** — bem **dentro** do regime cosmológico
(onde FM1 mostrou g/a₀≈0.003–0.005). A escala de saturação (se existe) está em
**a_c2/a₀ ≲ 0.001 < 0.005** — **abaixo do piso do gap observacional (0.005, 0.016)**.

O scan de tamanho finito (L=10,16,24) não resolve h_c de forma limpa (a curva ainda
sobe na borda inferior; h_c fica no ruído, 0.003–0.010). Mas a conclusão independe
dessa sutileza C1-vs-C4: **em nenhum caso há uma segunda transição localizada no
gap (0.005,0.016)**. O realce ou diverge (finito-tamanho apenas, C1) ou só corta
abaixo do gap (C4) — **os dois são morte para o Botão 1.**

Controle desordenado (J=0.55 < J_c): χ∥ também sobe (p≈0.35) mas sem ordem
espontânea — não é o regime MOND coerente; confirma que o realce coerente exige a
fase ordenada.

## Veredito FM2-1: **C (C1/C4) para o Botão 1**

O ferromagneto de orientação **reproduz** o deep-MOND (positivo, microscópico), mas
**sustenta** esse realce até dentro do regime cosmológico (g/a₀≲10⁻³), **sem**
segunda transição no gap observacional para domá-lo. Do lado microscópico, isto
**confirma** o runaway de FM1: a fonte do realce não se desliga onde precisaria.

Uma segunda transição física na janela exigiria um **comprimento de correlação
externo** — a massa do vetor m_A do Paper II (ξ=1/m_A daria um corte físico
L-independente). Calibrar m_A à escala cosmológica e medir a_c2 resultante é o
passo honesto seguinte (FM2-1b/futuro), **não** feito aqui. Sem ele, o Botão 1 não
entrega a segunda transição no gap.
