# FM4-3 — σ8 com uma fração f de matéria escura de onda

> `FM4_run.py` → `FM4_run.{json,png}`. Cosmologia mista CDM + fração f de ULDM
> (transfer fuzzy), σ8 via CAMB baseline de FM1.

## Resultado: σ8 mal se move — não alcança KiDS

σ8(f, m_A)  (ΛCDM = 0.811; alvo KiDS ≈ 0.766):

```
m_A \ f      0.05    0.1     0.2     0.3     0.5
3.7e-25      0.811   0.810   0.809   0.809   0.807
1.0e-24      0.811   0.811   0.811   0.811   0.810
1.0e-23      0.811   0.811   0.811   0.811   0.811
```

- **Mesmo no melhor caso** (m no piso, f=0.5) σ8 cai só de 0.811 para **0.807** — 0.5%,
  longe dos ~6–8% necessários para KiDS (0.766). **Não alcança.**
- **Por quê:** a transfer fuzzy só corta acima de k_Jeq ≈ 0.55/Mpc (no piso). A σ8 é
  dominada por k ~ 0.13 h/Mpc, **abaixo** desse corte → fica intocada. Só a cauda de
  alto-k da integral de σ8 é suprimida, e só a fração f dela. Resultado: minúsculo.
- Para mover σ8 de verdade seria preciso k_Jeq ainda **menor** (massa ainda mais
  leve, m ≲ 10⁻²⁶) — **excluída pelo Paper II** (m_A > 3.7×10⁻²⁵) — **e/ou** uma
  fração grande. Ambos colidem com o Lyman-α (FM4-4).

## Veredito FM4-3

A fração de matéria escura de onda no intervalo de massa permitido **não suprime σ8**
o suficiente para resolver S8. A escala de Jeans estava na vizinhança certa (FM4-2),
mas a supressão na escala que domina σ8 é fraca demais sem ir a massas excluídas.
