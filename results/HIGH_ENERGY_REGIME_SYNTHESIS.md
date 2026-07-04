# HIGH_ENERGY_REGIME — Síntese honesta dos três sub-experimentos

> Execução de `HIGH_ENERGY_REGIME.md`. Único regime ainda não testado da rede causal:
> alta energia (`v→c`, `g≫a₀`, campo intenso). Hipótese: poderia resolver simultaneamente
> a criação de Skyrmions (FL3) e a tensão S8. Três sub-experimentos, critério de morte
> geral pré-registrado: **se μ≥1 em HE2, sem criação em HE1 e HE3 — a fronteira permanece
> onde está.**

## Veredito por sub-experimento

| Sub-exp | Regime | Pergunta | Veredito | Número decisivo |
|---|---|---|---|---|
| **HE1** | `v→c`, rede fina (SU(2)) | colisão Skyrmion+anti cria par? | **MORTE (B: aniquilação)** | KE/2M_Sk c² ≤ **6.9%** em v=0.99c |
| **HE2** | `g≫a₀` (DEV/MOND) | boost gravitacional cai abaixo de 1? | **MORTE** | min(boost) = **1.000000** (sempre realça) |
| **HE3** | campo intenso (ferromagneto O(3)) | campo cria pares de defeitos (Schwinger)? | **MORTE** | 0 pares até h=30J; ΔE_par = **+524** |

**Todos os três disparam o critério de morte.** Conforme pré-registrado: a fronteira de alta
energia da rede causal **não tem física nova** que resolva FL3 ou S8. Nenhum parâmetro foi
ajustado para escapar; um falso-positivo em HE3 (300 "pares" de speckle) foi **rejeitado**
pela disciplina de gate, não explorado.

## A estrutura comum das três mortes

As três mortes têm a **mesma forma**: um **sinal fixo** que nenhuma intensidade inverte.

- **HE1:** o boost da rede é cinematicamente **não-relativístico** (`KE ∝ v²`, expoente
  medido 2.00, sem γ). A energia satura em ~7% do limiar `2 M_Sk c²` no limite `v→c`. O
  custo de massa-de-repouso de um par é **sempre** positivo e **sempre** inacessível.
- **HE2:** a modificação MOND é `+（αβ/2)/√(x(1+x))`, **positiva-definida** para `β>0`
  (β calibrado em galáxias). O boost é `≥1` em todo `x`, `→1⁺` quando `g≫a₀`. Suprimir
  exigiria `β<0` (destrói o ajuste de 167 galáxias).
- **HE3:** o acoplamento de Zeeman ao campo uniforme paga apenas **custo** (gradiente +
  desalinhamento) para um par de defeitos — `ΔE>0` em qualquer campo. Não há limiar de
  Schwinger porque o campo não acopla à estrutura que um par fornece.

Em todos: **criar / suprimir exigiria virar um sinal que a teoria fixa por construção.**
A rede causal é, nos três canais, uma teoria de sinal definido.

## Um achado positivo de mapeamento (HE2)

O regime `g≫a₀` que a hipótese esperava útil para S8 é fisicamente realizado **apenas em
sistemas compactos/densos** (interior de galáxias `x~1`, Via Láctea `x~1.8`, Sistema Solar
`x~5×10⁷`) — onde MOND já → Newton. As escalas que **fixam S8** (esfera σ₈ de 8 Mpc/h:
`x≈2.3×10⁻³`; modos lineares: `x~10⁻³–10⁻¹`) vivem no extremo **oposto**, MOND profundo,
onde o reforço é **máximo**. Mesmo que existisse supressão em `g≫a₀`, estaria na escala
errada. Isto **localiza** definitivamente por que o regime de alta energia não pode tocar S8.

## O que NÃO se perdeu (conforme pré-registrado)

Os resultados atuais são independentes do regime de alta energia. As três mortes **não
invalidam nada**: foram exploração pura com critério de morte honesto. O que cada uma
**adicionou**:

- **HE1:** estendeu FL3 ao canto ultra-relativístico/alta-resolução declarado fora de alcance,
  e quantificou o mecanismo (boost não-relativístico → limiar inacessível por construção).
  O motor `chiral_evolve_fast` foi revalidado em rede 1.5× mais fina.
- **HE2:** confirmou FM1/FM2 por caminho analítico independente — a supressão que S8 exige é
  **estruturalmente proibida**, não só numericamente desfavorecida — e mapeou onde está `g≫a₀`.
- **HE3:** fechou o canal "criação de matéria por campo" no setor de vácuo, complementar a
  HE1/FL3 (canal "criação por colisão" no setor de matéria). **Nenhum** canal da rede causal
  cria carga topológica de baixa para alta energia.

## Conclusão

```
A fronteira de alta energia permanece onde estava.
  Paper V (regime de alta energia) NÃO é justificado por novo fenômeno —
  é justificado, se algum, como o teorema de que os três canais têm sinal definido.
A criação/supressão exigiria um setor de interação NOVO (não-linear, além da
  dinâmica geodésica/quiral e além da função de interpolação positiva-definida).
```

Arquivos: `matter/he1/` (HE1-1 gate, HE1-2 colisão), `cosmology/he2/` (HE2 screening),
`vacuum_structure/he3/` (HE3 Schwinger). Cada sub-experimento tem `.py`, `.json`, `.md`, `.png`.
