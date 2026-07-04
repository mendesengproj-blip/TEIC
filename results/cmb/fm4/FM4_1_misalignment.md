# FM4-1 — Misalignment → matéria fria (w=0)  ✅ POSITIVO

> `FM4_run.py` → `FM4_run.json`. Oscilador φ''+3Hφ'+m²φ=0 em fundo FRW.

## Resultado: o setor massivo É frio (w=0) — o que FM3 não tinha

```
m_A (eV)     w_late       ρ ~ a^slope     a_osc (onset)
1.0e-26     -0.042        a^-3.01         3.9e-5
1.0e-25     -0.042        a^-3.01         8.4e-6
3.7e-25     -0.042        a^-3.01         3.5e-6
```

- Enquanto **H > m_A** o campo é **frozen** por fricção de Hubble (w≈−1).
- Quando **H cai abaixo de m_A** ele **oscila** coerentemente, e a média temporal dá
  **⟨w⟩ → 0** (a energia cinética e potencial se alternam). A densidade escala como
  **ρ ~ a⁻³** — **matéria fria**, exatamente como CDM.

> **Esta é a peça que faltou em FM1/FM2/FM3.** O setor de orientação (Goldstone) só
> dava w realçado (MOND), quente (c_s~c) ou w=−1/3 (textura). O setor **massivo**
> (m_A oscilando via misalignment) dá **w=0 frio de verdade** — a primeira componente
> de matéria escura genuína (w=0) do programa.

## Significado

A TEIC+DEV **tem** um candidato a matéria escura: o **vetor massivo m_A**, que via
misalignment se comporta como matéria escura fria (w=0, ρ∝a⁻³). Isso responde "o que
é a matéria escura?" na teoria — é o setor massivo do vácuo. Se essa componente
**resolve a tensão S8** (precisa de um freio de Jeans na escala certa) é o que FM4-2/3/4
decidem.

> Nota numérica: integrar até a=1 é intratável (campo leve oscila ~10⁸ vezes por tempo
> de Hubble). Integramos do onset (3H=m) por ~60 oscilações e fazemos a média — w→0 é
> universal e não precisa da hierarquia completa.
