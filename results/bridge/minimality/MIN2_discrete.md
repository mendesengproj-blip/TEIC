# MIN2 — Grupos discretos não carregam matéria pontual: o teste de projeção

> Task MIN2 of `MINIMALITY_SU2.md`. Hedgehog B=1 projetado no elemento mais
> próximo de Q8 (8 elementos) e do grupo binário tetraédrico 2T (24 elementos).
> Data: `MIN2_discrete.json`; figura: `MIN2_discrete.png`.

## Verdict: **a projeção discreta destrói a carga e converte o sóliton em paredes de domínio com energia divergente** — todas as previsões pré-registradas batem

```
                        B (61³)        E₂ ratio 61³/41³     pré-registrado
hedgehog suave          0.958          1.02                 ~0.95 / 1.0±0.1   ✓
projeção Q8 (8 el.)     0.051          1.62                 |B|<0.2 / 1.49±0.15 ✓
projeção 2T (24 el.)    0.076          1.50                 |B|<0.2 / 1.49±0.15 ✓
```

## O que o teste mostra

Um mapa contínuo S³ → (conjunto discreto) é constante: π₃ de qualquer grupo
discreto é trivial. A versão medida: projetar o hedgehog suave no subgrupo
discreto mais próximo

1. **colapsa a carga** (B: 0.958 → 0.05–0.08 — o índice de volume vive nos
   gradientes suaves; um campo constante-por-pedaços só tem contribuições de
   parede, não-inteiras e ~0);
2. **converte a energia em paredes de domínio**: E₂ cresce ∝1/dx sob refino
   (razões 1.62/1.50 ≈ 61/41 = 1.49) enquanto o hedgehog suave converge
   (1.02). No contínuo, o "sóliton discreto" custa energia infinita — não é
   um objeto, é um defeito de parede.

Aumentar a resolução do grupo (8 → 24 elementos) **não ajuda**: 2T se comporta
como Q8. A obstrução é topológica (discretude), não de tamanho do grupo.

## Honestidade

- O argumento contínuo é elementar; o valor do teste é tê-lo na rede, com o
  mesmo motor (su2_core) e o mesmo B dos resultados positivos — a eliminação
  (2) da cadeia MIN3 fica medida, não citada.
- A projeção "mais próximo" é a discretização canônica; outra regra de
  projeção mudaria as paredes, não a conclusão (B inteiro exige gradientes
  contínuos que nenhum campo a valores discretos tem).
