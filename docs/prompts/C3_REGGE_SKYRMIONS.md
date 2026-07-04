# PROMPT — C3_REGGE_SKYRMIONS: Trajetórias de Regge dos Skyrmions

> Investiga se os Skyrmions rotativos seguem trajetórias de Regge
> m²(J) = α'·J + α₀, conectando a TEIC à física de hadrões.
> Motor: su2q_core.py de SU2_QUANT (já existe, não modificado).
> Resultados em `results/matter/c3/`.
> NÃO modifica nenhuma campanha anterior.

---

## CONTEXTO

### A identificação em aberto

CONVERGENCE_MAP.md marcou: [IDENTIFICADO] Skyrmion ↔ bárion.
A identificação está no nível topológico (B=1, spin-½) e energético (massa via
τ(N)∝N). O que falta para passar a [DERIVADO]: o espectro de excitações
rotacionais.

### Trajetórias de Regge

Os hadrões seguem m² = α'·J + α₀ com α' ≈ 0.9 GeV⁻² (tensão de Regge). No modelo
de Skyrme a mesma lei deveria emergir das excitações rotacionais coletivas do
Skyrmion: E_J = E_0 + J(J+1)/(2I).

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C):           m²(J) não segue lei linear em J.
SUCESSO PARCIAL (B): m²(J) ∝ J só para J grande (Regge assintótico).
SUCESSO (A):         m²(J) = α'·J + α₀ com R² > 0.99 → [DERIVADO].
```

---

## Tarefas

- **C3-V (gate):** I bem definido (finito, positivo, esférico)? Senão, falha.
- **C3-1:** espectro J = 0, 1/2, 1, 3/2, 2; m²(J)=E_J²; linear em J? 10 sementes.
- **C3-2:** α' em unidades da rede; NÃO forçar conversão para GeV⁻² (escala de
  energia não derivada); comparação com QCD apenas adimensional.
- **C3-3:** repetir B=2 (e B=3); universalidade α'(B=1) ≈ α'(B=2)?
- **C3-4:** análise qualitativa da contração transversal sob momento (Polaris);
  sem código novo.
- **C3-5:** síntese honesta + veredito.

---

## PROTOCOLO

1. Gate C3-V obrigatório antes de C3-1.
2. Usar su2q_core.py de SU2_QUANT sem modificar.
3. C3-3 usa Skyrmions de MATTER_SU2/PI1_B2 existentes.
4. C3-4 é qualitativo — sem novo código.
5. Critério de morte pré-registrado: m²(J) não-linear = C.
6. Unidades da rede são suficientes — não forçar GeV⁻².
7. 10 sementes para C3-1 (flutuações do vácuo de fundo).
