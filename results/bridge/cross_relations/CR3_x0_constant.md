# CR3 — a constante pura de X₀: estatística de extremos do sliver causal

> Tarefa CR3 de `CROSS_RELATIONS_II.md`. Kill criteria pré-registrados na
> docstring de `CR3_x0_constant.py` ANTES de rodar; nenhum critério alterado
> após ver dados. Dados: `CR3_x0_constant_data.json`; figura
> `CR3_x0_constant.png`.

## Veredito: **SUCESSO — colapso Exp(1) confirmado; a constante pura de X₀ é π/ln2, com fechamento assintótico a 0.3%**

| Critério (pré-registrado) | Limite | Medido | Passa? |
|---|---|---|---|
| KS(u, Exp(1)) nos dois ρ mais altos | ≤ 0.05 | 0.0247 (ρ=45), 0.0115 (ρ=75) | ✅ |
| median(u)/ln2 nos dois ρ mais altos | ∈ [0.85, 1.15] | 0.979, 0.980 | ✅ |
| expoente q de Δτ_med ∝ ρ^q | \|q+½\| ≤ 3σ | −0.534 ± 0.017 (2.0σ) | ✅ |

## Os números

| ρ | n eventos bulk | KS vs Exp(1) | med(u)/ln2 | check exato ρV(τ_med)/ln2 | π̂ ≡ ln2/(τ²_med ρH²) | fração truncada (esperada) |
|---|---|---|---|---|---|---|
| 16 | 819 | 0.029 | 1.043 | 1.043 | 2.795 | 0.37% (0.50%) |
| 27 | 1413 | 0.017 | 1.026 | 1.026 | 2.926 | 0.07% (0.01%) |
| 45 | 2454 | 0.025 | 0.979 | 0.979 | 3.120 | 0% (0%) |
| 75 | 3876 | 0.011 | 0.980 | 0.980 | **3.151** | 0% (0%) |

- **A relação exata** u = ρ·V(Δτ_min, H) ~ Exp(1) (probabilidade de vazio de
  Poisson sobre o volume exato do sliver capado) vale em TODOS os ρ — o check
  de mediana fecha entre 0.98 e 1.04 sem forma líder nenhuma.
- **A constante pura de forma líder** converge para π por baixo
  (2.795 → 3.151 = π·1.0029 no ρ mais alto) — mesmo padrão de fechamento
  assintótico O(1/escala) do CR1b. Em unidades do charter:

```
X₀ · Δθ_max⁻² = 1/Δτ²_med = π ρ H² / ln 2          (constante pura π/ln2 ≈ 4.532)
medido em ρ=75:  3.151/ln2 · ρH²  ⇒  razão para π/ln2 = 1.0029  (0.29%)
```

- O expoente −0.534 ± 0.017 é 2σ abaixo de −½ — consistente com a correção
  sublíder t⁴ln(H/t) do volume exato (o mesmo desvio que faz π̂ se aproximar
  por baixo); o critério 3σ pré-registrado não dispara.

## Leitura honesta

1. **O conteúdo novo:** a constante pura de X₀ não é geometria UV pura — é
   **estatística de extremos** do sliver que abraça o cone. O expoente é UV
   (X₀ ∝ ρ, C3 inalterado), mas a constante carrega o **regulador IR H²**
   declarado: o sliver é não-compacto e o cap H (frame-dependente) é quem o
   trunca — mesmo status do regulador de caixa em LV3.
2. **Zero parâmetros**: π/ln2 não foi ajustado; π vem do volume do cone em
   3+1D e ln2 da mediana da exponencial. Qualquer rede futura que meça
   Δτ_min capado e não encontre Exp(1) derruba o resultado.
3. **Honestidade dimensional**: Δθ_max segue propriedade do campo (não da
   geometria) e fica explícito; X₀ em unidades físicas continua não derivado.

## Reproduzir

```
python results/bridge/cross_relations/CR3_x0_constant.py
```
