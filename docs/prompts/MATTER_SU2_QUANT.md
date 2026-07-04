# PROMPT — SU2_QUANT: Quantização do Skyrmion — Spin-½ de Primeiros Princípios

> Quantiza as coordenadas coletivas (rotacionais) do Skyrmion SU(2).
> Objetivo: derivar spin-½ como número quântico do Skyrmion B=1.
> Continua MATTER_SU2 (Veredito B — Skyrmion estável, spin clássico indefinido).
> NÃO modifica nenhuma campanha anterior. Resultados em `results/matter/su2_quant/`.

## A estratégia

```
Q1: extrair zero modes rotacionais do Skyrmion (E[U_R]=E[U_0])
Q2: tensor de inércia I_ab = ∫Tr[ξ_a†ξ_b], esfericidade, espectro E_j=j(j+1)/(2I)
Q3: path integral sobre q(t)∈SU(2), ação (I/2)Σ|Δq|², propagador + espectro
Q4: fase FR (-1)^{B·W}, W = cruzamentos antipodais; seleciona j=½
Q5: rotação 2π → −ψ; 2 estados degenerados
Q6: θ(r) ~ M_tot/r, M_tot = M_Sk + 3/(8I)
Q7: síntese honesta
```

## Anti-circularidade

- SU(2) como quaternions unitários (su2_core, sem Pauli, sem complexo).
- Fase FR = contagem topológica de cruzamentos antipodais em S³; j lido do espectro.
- ψ→−ψ verificado pela amplitude do autovetor, não inserido.
- "Spin-½", "férmion", "bóson", "próton" — SÓ em COMPARISON ONLY.
- Q1 obrigatório antes de tudo; Q3 antes de Q4; Veredito A exige verificação tripla.

## Veredito

```
A — Spin-½ derivado: FR seleciona j=½, 2π→−ψ, 2 estados degenerados, M_tot=M_Sk+E_{1/2}
B — Spin-½ parcial    C — FR não seleciona j=½    D — path integral não converge
```

**Resultado: Veredito A** (ver `results/matter/su2_quant/Q7_synthesis.md`).
