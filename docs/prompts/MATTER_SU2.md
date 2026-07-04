# PROMPT — SU2: Grupo Não-Abeliano e Hedgehog/Skyrmion

> Estende o motor para grupo de gauge SU(2) não-Abeliano.
> Testa se o hedgehog/Skyrmion (topologia S², π₃) emerge da rede 3+1D.
> NÃO modifica nenhuma campanha anterior. Resultados em `results/matter/su2/`.

## Por que SU(2)

```
U(1):  π₁(U(1)) = ℤ   → vórtice S¹ (objeto 1D em 3D)
SU(2): π₃(SU(2)) = ℤ  → Skyrmion (objeto 0D = PARTÍCULA em 3D)
       π₂(S²) = ℤ      → hedgehog (monopolo magnético)
       π₄(SU(2)) = ℤ₂ → spin-½ (rotação 2π ≠ identidade)
```

SU(2) é o grupo mínimo que suporta sólitons pontuais estáveis em 3+1D.

## Anti-circularidade SU(2)

- `U_ij` armazenado como quaternion `(a₀,a₁,a₂,a₃)` — 4 reais, `|a|²=1`.
- Produto de grupo via quaternions (Hamilton), **sem matrizes de Pauli**, sem
  números complexos no gerador.
- `W_p = ½Tr(U₁U₂U₃⁻¹U₄⁻¹)` = componente `a₀` do produto (real, ∈ [-1,1]).
- "Próton", "quark", "nêutron", "isospin", "bárion" — SÓ em blocos `COMPARISON ONLY`.
- Número topológico `B` = integral discreta de `U` (sem rótulo físico no gerador).

## Tarefas

- **SU1** — Motor SU(2): portão de 4 verificações (limite U(1) exato, U·U⁻¹=1,
  invariância de gauge da ação, conservação de energia).
- **SU2** — Vácuo SU(2): densidade de monopolos e lei de área de Wilson (confinamento).
- **SU3** — Hedgehog relaxado sob a ação SU(2): mínimo local? F(r) estável? razão E₂/E₄.
- **SU4** — Número de Pontryagin B=1 conservado (hedgehog, anti-hedgehog, par, evolução).
- **SU5** — Termo de Skyrme: estabilidade de Derrick; **emerge do quártico C4?**
  Se sim, não é axioma novo.
- **SU6** — Colisão com campo SU(2), medir B na janela tardia, 20 sementes, N~300.
- **SU7** — Rotação 2π do Skyrmion: estado muda de sinal? (spin-½)
- **SU8** — Cinco consistências (massa, dispersão, θ~M/r, isotropia, spin).
  Veredito A exige verificação tripla.
- **SU9** — Síntese honesta.

## Veredito

```
A — Skyrmion estável + spin-½ + cinco consistências → matéria fermiônica
B — Skyrmion estável mas sem spin-½ verificado     → matéria bosônica B=1
C — Hedgehog estático mas sem criação por colisão
D — SU(2) não confina ou hedgehog instável         → física além do motor atual
```
