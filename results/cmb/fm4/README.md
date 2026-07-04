# results/cmb/fm4 — campanha FM4_WAVE_CONDENSATE (jun/2026)

> Charter: `FM4_WAVE_CONDENSATE.md` (raiz). A última porta — o setor MASSIVO (m_A
> como matéria escura de onda/fuzzy via misalignment) — depois que FM1/FM2/FM3
> fecharam o setor de Goldstone. **NÃO modifica campanhas anteriores.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **FM4-V** | dispersão massiva ω²=c²k²+m²? | **PASS** — gap em k=0, limite E2 ω=ck | `FM4V_gate.md` |
| **FM4-1** | misalignment → frio (w=0)? | **SIM** — w=−0.04, ρ~a⁻³·⁰¹ → **é matéria escura fria** | `FM4_1_misalignment.md` |
| **FM4-2** | Jeans na banda de σ8? | **SIM** — k_half=0.38/Mpc no piso do m_A | `FM4_2_jeans.md` |
| **FM4-3** | fração f suprime σ8 p/ KiDS? | **NÃO** — 0.811→0.807 (melhor), KiDS 0.766 | `FM4_3_sigma8_fraction.md` |
| **FM4-4** | sobrevive ao Lyman-α? | **NÃO** — f=0.1 no piso → 19% supp (4ª morte) | `FM4_4_lyman_abundance.md` |
| **FM4-5** | síntese | **C p/ S8, MAS o massivo É DM fria (w=0)** | `FM4_5_synthesis.md` |

Motor: `fm4_core.py` (misalignment φ''+3Hφ'+m²φ=0 → w(a); escala de Jeans/de Broglie
de ULDM; transfer fuzzy Hu+2000; σ8 misto CDM+fração f via baseline CAMB de FM1;
dispersão massiva). Runner: `FM4_run.py` → `FM4_run.{json,png}`. Self-test:
`python fm4_core.py`.

## Resultado de uma linha

**O setor massivo É matéria escura fria (w=0) — mas não resolve S8.** O vetor massivo
m_A, via misalignment, oscila como matéria fria (w=−0.04≈0, ρ∝a⁻³) — **a primeira
componente w=0 do programa**, a peça que FM1 (realça)/FM2 (quente)/FM3 (w=−1/3) não
davam. **A TEIC+DEV tem um candidato a matéria escura (o m_A).** MAS a rota fuzzy/Jeans
para S8 morre: a supressão de σ8 é fraca no intervalo de massa permitido (FM4-3), e a
massa leve + fração que ajudaria σ8 super-suprime o Lyman-α (FM4-4, 4ª morte). Não há
janela. **Veredito C para S8**, com o positivo de que o setor massivo responde "o que
é a matéria escura?".

## Mapa completo das quatro portas

```
FM1 (Goldstone/MOND)     → realça σ8
FM2 (Goldstone/2 fases)  → escala errada (17pc) + obstrução
FM3 (Goldstone/textura)  → escala certa, w=-1/3 (não frio)
FM4 (MASSIVO/fuzzy)      → w=0 FRIO ✓ (é DM) mas S8 morto pelo Lyman-α
```
Setor de Goldstone nunca dá w=0 (estrutural); o setor massivo dá (m_A frio) — mas
nenhum setor resolve S8.

## Honestidade / engenharia

- **m_A do Paper II** (galáxias/estabilidade), NÃO ajustado ao CMB; w/Jeans/σ8 da
  dinâmica + transfer; nenhum σ8/KiDS/Lyman-α inserido. Janelas fixadas antes.
- **Misalignment:** integrado ~60 oscilações pós-onset (m/H~10⁸ torna a=1 intratável;
  w→0 é universal). w_late=−0.04, ρ~a⁻³·⁰¹ robusto em 3 massas.
- **Caveats:** transfer fuzzy de Hu+2000 (analítica); números finais de Lyman-α/σ8
  com perturbações ULDM completas pediriam CLASS+axionCAMB (como FM1). Direção robusta.

## Regras (as de sempre)

Charter pré-registrado (predições + morte ANTES do código); gate FM4-V; negativos
(S8 morre, Lyman-α) E positivo (w=0 frio = DM) reportados; anti-circularidade (m_A do
Paper II, resto medido, nada de σ8/Lyman-α inserido); critério de morte C3 (Lyman-α)
acionado como escrito. Ver `FM4_5_synthesis.md`.
