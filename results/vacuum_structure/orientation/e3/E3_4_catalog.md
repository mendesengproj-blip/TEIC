# E3-4 — Catálogo de texturas de n⃗

> Charter: `E3_DEFECTS.md` (E3-4). Código: `E3_4_catalog.py`; motor:
> `e3_core.py`; dados: `E3_4_catalog.json`; figura: `E3_4_catalog.png`.

## O que se busca

Além do hedgehog B=+1, medir carga, energia e destino (sob gradiente
descendente, L=24, 3000 passos) de: anti-hedgehog, dipolo (hedgehog+anti) e uma
textura toroidal (anel de vórtice).

## Resultados

```
textura          B inicial → final    E inicial → final    destino
-----------------------------------------------------------------------------
hedgehog         +1.00 → +1.00        176 → 172            metaestável (caroço persiste)
anti-hedgehog    −1.00 → −1.00        176 → 172            metaestável (sinal espelhado)
dipolo (+1,−1)    0.00 →  0.00        1192 → 0             ANIQUILA para o vácuo
toroidal          0.00 →  0.00        598 → 0              decai (carga de ponto nula)
```

## Leitura

- **Anti-hedgehog B=−1 existe e sobrevive** — exatamente o espelho do hedgehog
  (a textura "anti", COMPARISON ONLY). Carga oposta, mesma energia e mesmo
  destino metaestável.
- **Dipolo: carga líquida 0, aniquila.** O par (+1,−1) relaxa com a energia
  caindo de 1192 → 0: as duas cargas opostas se atraem, se fundem e o campo
  retorna ao vácuo uniforme — o análogo de aniquilação partícula–antipartícula
  (COMPARISON ONLY).
- **Toroidal: B=0.** A textura de anel **não** carrega carga de ponto π₂; sob
  relaxação ela simplesmente desfaz (E→0). Não é um defeito topológico do tipo
  hedgehog.

## Veredito E3-4

```
Anti-hedgehog B=−1 existe?            SIM (sobrevive, espelho exato do +1)
Par B=+1,−1 cria/aniquila?           SIM (dipolo aniquila para o vácuo, E→0)
Toroidal é defeito topológico?        NÃO (B=0, decai)
```

O catálogo confirma o quadro: as cargas de ponto ±1 (hedgehog/anti) são os
defeitos metaestáveis genuínos; pares opostos aniquilam; texturas sem carga de
ponto (toroidal) decaem. Tudo medido por ângulo sólido (B) e funcional de
ligações (E), sem inserir interpretação.
