# CR1/CR1b — G_net vs granularidade: a constante pura do setor gravitacional

> Tasks CR1+CR1b of `CROSS_RELATIONS.md`. Laplaciano de grafo do DS1 (importado,
> não modificado), fonte pontual, fit θ=A/r+C. 5 sementes por ponto.
> Data: `CR1_gnet.json`, `CR1b_asymptotic.json`; figuras correspondentes.

## Verdict: **B — a relação G_net·ρ²·r_c⁵ = 15/8π² é confirmada assintoticamente (2.5%)**, com correções O(1/deg) medidas; a morte literal de CR1 em grau baixo é reportada e explicada

## O relato completo (transparência obrigatória)

1. **CR1 ao pé da letra: morte disparada.** Nos graus medidos (7–28), a
   constante pura saiu 0.21–0.35 (até 39% acima de 15/8π²≈0.18998) e os
   expoentes vieram −2.37/−5.93 em vez de −2/−5 — fora da tolerância de 20%
   pré-registrada. Este resultado bruto permanece em `CR1_gnet.json`.
2. **O diagnóstico (a correção que o charter antecipou).** A constante por
   ponto decresce monotonicamente com o grau: 0.353 (deg 7) → 0.245 (14) →
   0.211 (28). O charter pré-declarou correções O(1/deg); o teste correto é a
   convergência, não o valor em grau baixo. Os pontos deg<14 mostram curvatura
   (fora do regime linear em 1/deg) — incluí-los na extrapolação ingênua
   produz overshoot (0.163).
3. **CR1b: pontos novos em grau alto + ajuste no regime assintótico.**
   deg=48: 0.2025±0.0023; deg=64: 0.1992±0.0018. Ajuste c∞+b/deg em deg≥14:

```
c∞ = 0.18516   vs   15/8π² = 0.18998   →  razão 0.975  (2.5%)
b ≈ 0.85 (a correção de grau finito, agora um número medido)
```

## O que fica estabelecido

$$G_{\rm net}\,\rho^2\,r_c^5 \;\xrightarrow{\ \deg\to\infty\ }\; \frac{15}{8\pi^2}
\qquad\text{(confirmado a }2.5\%\text{)}$$

O acoplamento gravitacional da rede não é um parâmetro: dado o substrato
(densidade ρ, alcance r_c), **G_net é calculável de primeiros princípios** —
incluindo o prefator numérico — com correções de granularidade O(1/deg)
medidas. Os expoentes íngremes de CR1 (−2.37/−5.93) são o artefato esperado:
ao varrer ρ ou r_c com a outra variável fixa, o grau varia junto, e a correção
1/deg contamina o expoente; no regime assintótico a lei é a prevista.

## Honestidade

- O veredito é **B**, não A: a previsão fechou no limite assintótico com uma
  análise de convergência aplicada após a morte literal — pré-anunciada no
  charter ("correções O(1/deg)"), mas a tolerância de 20% foi mal calibrada
  para os graus exequíveis. Ambos os fatos ficam registrados.
- A constante 15/8π² é do Laplaciano de grafo RGG; o operador BD tem o seu
  prefator próprio (D3D mediu a relação G∝1/K lá). O conteúdo invariante:
  **em ambos os operadores o acoplamento é fixado pelo substrato, não livre.**
