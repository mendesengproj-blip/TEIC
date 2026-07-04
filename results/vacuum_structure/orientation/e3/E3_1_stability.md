# E3-1 — Estabilidade do hedgehog (gradiente descendente + Monte Carlo)

> Charter: `E3_DEFECTS.md` (E3-1). Código: `E3_1_stability.py`; motor:
> `e3_core.py`; dados: `E3_1_stability.json`; figura: `E3_1_stability.png`.

## O que foi feito

A partir do estado ordenado, semeia-se o hedgehog n⃗(r)=r̂ no centro de uma rede
cúbica L³ **aberta** (uma rede periódica não pode carregar uma carga de ponto
líquida) e mede-se B(t), E(t), r_eff(t) por duas relaxações independentes
(protocolo 2 do charter):

1. **Gradiente descendente a T=0** (descida íngreme em S²,
   dn/dt = H − (H·n)n, H = soma dos vizinhos). É o teste de Derrick honesto:
   nenhuma dinâmica pode escalar barreira; uma textura que sobrevive é um mínimo
   local genuíno. L=24, 4000 passos.
2. **Monte Carlo a J frio**, 20 sementes, J=3.0 e J=2.0, L=20, 4000 sweeps.
   B é lido **após um cooling curto** (30 passos de gradiente) de cada snapshot —
   protocolo padrão de teoria de campo na rede: o cooling remove rugas térmicas
   UV (que carregam ângulo sólido fracionário espúrio) sem mover o enrolamento
   inteiro.

## Resultados

### Gradiente descendente (T=0)

```
B     +1.000 -> +1.000   (preservado indefinidamente)
E      176.4 -> 171.8    (cai ~3% e estaciona; NÃO monotônico até zero)
r_eff   7.66 ->  7.44    (converge para r>0; ~0.32·L, fixado pela caixa)
```

O hedgehog **não colapsa** sob gradiente descendente. A discretização regulariza
a divergência UV (mecanismo 1): o caroço não pode encolher abaixo de ~1
espaçamento, e a carga B permanece +1. Mas r_eff converge para um valor fixado
pela **caixa** (∝ L), não por uma escala intrínseca — sinal de marginalidade de
escala (confirmado em E3-2).

### Monte Carlo (T finito) — 20 sementes

```
J=3.0 (frio):  sobrevivência 30%   tempo mediano de des-enrolamento ~2800 sweeps
J=2.0 (morno): sobrevivência 20%   tempo mediano ~2700 sweeps
```

B=+1 é **metaestável**: flutuações térmicas atravessam uma barreira **finita** e
des-enrolam o defeito (B→0) em tempo finito. Esfriar menos (J menor) encurta o
tempo de vida — assinatura de barreira finita, não de estabilidade verdadeira.
O des-enrolamento é um evento súbito (B salta 1→0 quando o caroço passa pelo
corte da rede), exatamente o esperado de um número topológico protegido até o
cutoff.

## Cenário (pré-registrado)

```
A colapso    : B:1→0, E monotônico, r_eff→0      — NÃO (B não colapsa no gradiente)
B metaestável: B=1 mantido, barreira finita,
               des-enrolamento térmico em t longo — SIM  ◀
C estável    : B=1 indefinido, sem des-enrolamento — NÃO (térmico des-enrola)
```

**CENÁRIO B — METAESTÁVEL.** B=+1 sobrevive ao gradiente descendente (a rede
regulariza o colapso de Derrick), mas uma barreira finita é cruzada
termicamente: a maioria das sementes MC des-enrola para B=0 em ~2700–2800
sweeps. O defeito existe e é robusto na escala de relaxação, porém não é um
sóliton estável.

## Anti-circularidade

B é a carga geométrica (ângulo sólido), E é o funcional de ligações, r_eff é um
momento da densidade de gradiente medida. Nenhuma estabilidade é assumida. O
critério de morte "B(t)→0" é pontuado exatamente como escrito — e ocorre apenas
no canal térmico (MC), não no gradiente puro, o que define a metaestabilidade.
