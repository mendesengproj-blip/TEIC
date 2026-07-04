# E3b-3 — Derrick causal (energia espacial vs temporal)

> `E3b_3_derrick_causal.py` → `.{json,png}`. ρ=1.5, T=3.0, core=1.5,
> λ ∈ [0.4, 3.0] (18 pontos), 5 sementes, três escalas L ∈ {3.5, 4.0, 4.5}.

## A pergunta

Em E3-2 (rede cúbica) E(λ) ~ λ era monótona: sem mínimo, o hedgehog prefere
encolher (sem escala intrínseca). A rede causal tem links orientados no tempo —
eles fornecem um contra-termo que cria um mínimo interior?

Dilata-se o hedgehog espacialmente (x → (x−c)/λ + c) e separa-se a energia de link:
- **E_spatial(λ)**: links com separação espacial apreciável (dx > 0.5·dt)
- **E_temporal(λ)**: links quase puramente temporais (eventos quase co-localizados
  no espaço, separados no tempo)

## Resultado — sem mínimo interior, em nenhuma escala

| L | frac. links espaciais | E_temporal/E_total | λ\* (argmin) | mínimo interior? |
|---|---|---|---|---|
| 3.5 | 0.94 | 0.84% | 0.40 | **não** |
| 4.0 | 0.94 | 0.74% | 0.40 | **não** |
| 4.5 | 0.94 | 0.74% | 0.40 | **não** |

- **E_total(λ) decresce em direção a λ pequeno** (λ\*=0.40, a borda inferior
  amostrada): o defeito ainda **prefere encolher** — Derrick ativo, sem escala.
- **E_temporal é < 1% de E_total** e é quase independente de λ: eventos no mesmo
  ponto espacial têm n⃗ de hedgehog quase idêntico, então a dilatação espacial mal
  os afeta. **Não há contra-termo temporal.**
- Robusto às três escalas — não é artefato de tamanho finito.

## Veredito de E3b-3

**Não há mínimo interior de Derrick causal.** O cone causal **não** fornece o
contra-termo que estabilizaria o hedgehog. Mesmo desfecho que a rede cúbica
(E3-2). Combinado com E3b-2 (a preservação de B vem do contorno congelado, não de
um mínimo de energia), isto fecha o **Veredito A**: o defeito **não** é matéria
intrinsecamente estável. Portanto **E3b-4 (E=mc²) não roda**.
