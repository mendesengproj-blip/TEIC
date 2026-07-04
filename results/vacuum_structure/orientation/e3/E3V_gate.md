# E3-V — Gate de validação do estimador de carga topológica

> Charter: `E3_DEFECTS.md` (gate E3-V, obrigatório antes de qualquer medição de
> estabilidade). Código: `E3V_gate.py`; motor: `e3_core.py`; dados:
> `E3V_gate.json`; figura: `E3V_gate.png`.
> **NÃO modifica nenhuma campanha anterior.**

## O que o gate testa

E3 precisa de um único motor crítico: o estimador do **número topológico B** —
o *grau* (degree) do mapa n⃗: superfície → S². Sem ele, "B(t)→0" não tem
significado. O gate valida B com texturas de resposta **conhecida**, usando
exatamente a maquinaria que rodará na medição física.

### O estimador: ângulo sólido (Berg–Lüscher)

A fronteira de cada cubo elementar da rede é uma pequena S². Triangula-se em 12
triângulos esféricos orientados para fora; o ângulo sólido assinalado de cada
triângulo (fórmula de Van Oosterom–Strackee,
Ω = 2·atan2(n₀·(n₁×n₂), 1+n₀·n₁+n₁·n₂+n₂·n₀)) somado e dividido por 4π é a
carga inteira contida no cubo. O total B = Σ_cubos q é o grau da superfície de
fronteira externa (faces internas cancelam — identidade geométrica).

### Resultados

```
G1  B(hedgehog)=+1 e B(vácuo)=0, exatos a 1e-6, em L=8,12,16,24,32,40   PASS
G2  B(anti-hedgehog)=-1 (sinal resolvido, não assumido)                  PASS
G3  invariância O(3): |dB|=2.2e-16 sob 5 rotações globais aleatórias;    PASS
    ruído suave (0.25) + cooling: B=+1.000 recuperado
G4  localidade/aditividade: Σ q_cubo = +1.0000000 = grau da fronteira;   PASS
    carga concentrada no caroço (bloco 4³ central = +1.0000);
    par hedgehog+anti (dipolo): B líquido = 0.0000
G5  inteiro sob refinamento L=8..40: drift < 1e-6                        PASS
```

| L | B(hedgehog) | B(anti) | B(vácuo) |
|---|---|---|---|
| 8 | +1.0000000 | −1.0000000 | 0 |
| 16 | +1.0000000 | −1.0000000 | 0 |
| 24 | +1.0000000 | −1.0000000 | 0 |
| 40 | +1.0000000 | −1.0000000 | 0 |

O painel direito da figura mostra a densidade de carga por cubo q (fatia central
de L=24): toda a carga +1 está localizada no caroço do hedgehog, fundo
exatamente zero — o estimador é local e topológico.

## Anti-circularidade

- Nenhum número topológico é inserido no gerador; B é uma contagem puramente
  geométrica de ângulo sólido dos spins.
- A invariância O(3) (G3) é uma exigência de consistência (S² é homogênea — o
  grau não pode depender de onde fica o "norte"), não um alvo ajustado.
- "matéria"/"partícula" não aparecem aqui — só na síntese (COMPARISON ONLY).

## Veredito do gate

```
G1 hedgehog=+1, vácuo=0 .................... PASS
G2 anti=-1 ................................. PASS
G3 invariante O(3) + ruído/cooling ......... PASS
G4 local/aditivo + par=0 ................... PASS
G5 inteiro sob refinamento ................. PASS
E3-V GATE: PASS — estimador validado, E3-1 pode prosseguir
```

O estimador mede B corretamente (+1 hedgehog, 0 vácuo, −1 anti) a precisão de
máquina, é invariante O(3), local e estável sob refinamento. Qualquer colapso de
B medido adiante é física, não artefato de discretização.
