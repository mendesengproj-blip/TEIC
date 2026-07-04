# PROMPT — FM3_PRIMORDIAL_TEXTURE: a textura primordial de n⃗ como a peça fria de grande escala

> Charter PRÉ-REGISTRADO. Salvar na raiz do projeto TEIC.
> Continua FM1 (MOND-μ ingênuo realça σ8) e FM2 (duas fases nuas têm obstrução
> estrutural). Nasce da imagem mental de `TEIC_DEV_VISION.md` §5–6.
> Pergunta central: a **transição ferromagnética do vácuo no universo jovem** deixa
> uma **textura de orientação primordial** que — congelada por causalidade (E3b) em
> escala cosmológica — fornece a componente **fria, grande e que FREIA** o crescimento
> que FM1/FM2 não tinham, na escala certa e fria pelo motivo certo?
> Resultados em `results/cmb/fm3/`. Reutiliza `orientation_core` (E1), `fm2_core`
> (FM2), `e3b_core` (E3b). **NÃO modifica nenhuma campanha anterior.**

> ⚠️ **STATUS: PRÉ-REGISTRO escrito ANTES de rodar; depois EXECUTADO (jun/2026).**
> **VEREDITO C — escala certa, equação de estado errada.** O relíquia forma-se na
> escala cosmológica (FM3-1, resolve o problema de escala de FM2) e é congelado
> super-horizonte (FM3-2/E3b) — mas w_eff=−0.43≈−1/3 (textura/monopolo global), **NÃO
> frio (w=0)**: "congelado por causalidade" é frio de POSIÇÃO, não de PRESSÃO. Logo
> não clusteriza como CDM nem suprime σ8 (FM3-3); fonte ativa de isocurvatura, só
> subdominante no Planck (FM3-4). Lição positiva: frio de posição ≠ frio de pressão.
> Ver `results/cmb/fm3/FM3_5_synthesis.md` e `README.md`. As predições/mortes abaixo
> foram fixadas ANTES de medir.

---

## CONTEXTO: por que esta é a candidata certa

FM1 e FM2 mapearam por que a TEIC+DEV **nua** não resolve S8 (ver
`results/cmb/SCALE_BOUNDARY.md`):
- a modificação MOND **realça** o crescimento (μ≥1), não freia (FM1);
- a estrutura de duas fases tem **obstrução estrutural** — MOND quer fase ordenada,
  Jeans quer ponto crítico, fases opostas (FM2);
- os botões internos vivem na **escala errada** (m_A → 17 pc, ~10⁶× abaixo de σ8).

A imagem mental (`TEIC_DEV_VISION.md`) sugere que a peça que falta **não** é um botão
da teoria estática — é um **relíquia dinâmica do universo jovem**:

```
universo jovem quente  → ferromagneto de orientação DESORDENADO (E1)
expansão/esfriamento   → cruza a transição de E1 → n⃗ se ALINHA
regiões fora de contato → alinham em direções diferentes → DOMÍNIOS (Kibble-Zurek)
fronteiras dos domínios → DEFEITOS / TEXTURA de n⃗ (monopolos globais π₂(S²), Hopf π₃)
super-horizonte        → CONGELADA por causalidade (E3b) → fria por princípio
re-entrada no horizonte → "descongela" → MODULA o crescimento
```

Por que escaparia das mortes anteriores:
- **Escala:** nasce do **horizonte na transição** → grande/cosmológica (não 17 pc).
- **Frio:** super-horizonte é frio por **congelamento causal** (E3b), não por c_s
  ajustado (que matou FM2-2).
- **Freio:** componente fria, suave em grande escala, com estrutura nas escalas de
  re-entrada → pode **suprimir** potência (direção certa de S8).

---

## A FÍSICA

Defeitos/texturas globais de campos O(N) são objetos cosmológicos reais. Para n⃗∈S²:
- **π₂(S²)=ℤ → monopolos globais** (Barriola–Vilenkin): déficit de ângulo sólido =
  efeito gravitacional; energia de gradiente ~ linear no raio.
- **π₃(S²)=ℤ → texturas de Hopf**: configurações suaves que colapsam e desenrolam.

A versão **scaling** (Turok: a rede mantém ~fração constante da energia do horizonte)
foi **excluída pelo Planck** como fonte dominante de estrutura (picos acústicos
errados, isocurvatura). A novidade da TEIC é E3b: o **cone causal congela** a textura
super-horizonte → ela é **não-scaling** (frozen), com equação de estado e assinatura
diferentes da de Turok. **A hipótese é que a versão frozen (a) é fria em grande
escala, (b) suprime potência ao re-entrar, (c) sobrevive ao Planck.**

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C) — qualquer uma:
  C1. A transição de E1 NÃO gera rede de domínios/defeitos com densidade apreciável
      (Kibble-Zurek dá n_def→0 no resfriamento lento) → sem relíquia.
  C2. A textura super-horizonte NÃO é congelada (w_eff não →0; evolui como a de
      Turok scaling) → reproduz a assinatura JÁ EXCLUÍDA pelo Planck.
  C3. A textura REALÇA σ8 (como FM1/FM2), em vez de suprimir.
  C4. A escala efetiva da relíquia sai sub-horizonte/galáctica (como m_A), não
      cosmológica → persiste o problema de escala.

SUCESSO PARCIAL (B):
  Suprime σ8 na direção certa mas insuficiente para KiDS, OU a relíquia é cosmológica
  e fria mas com incerteza grande demais para afirmar a supressão.

SUCESSO (A):
  Rede de defeitos forma-se na transição (Kibble); a textura é FRIA (w_eff≈0) e
  COSMOLÓGICA por congelamento causal (E3b); ao re-entrar SUPRIME σ8 para a faixa
  KiDS (0.746–0.786); e a assinatura no CMB (frozen, não-scaling) é CONSISTENTE com
  Planck. → A peça fria-e-grande emerge da TEIC sem ingrediente externo.
  → Verificação tripla obrigatória antes de afirmar.
```

**Anti-circularidade dura:** a transição (J_c) e a física de defeitos vêm da REDE
(E1/E3b); a₀ de SPARC; NENHUM valor de σ8/KiDS/Planck é inserido no gerador. Os
vínculos do Planck e a assinatura de Turok são COMPARISON ONLY. As janelas (frio,
cosmológico, suprime) foram fixadas ANTES de medir.

---

## TAREFAS

### FM3-V — Gate (obrigatório)
Reproduzir, nos motores reutilizados, (i) a transição de E1 (J_c≈0.693, ordem-
parâmetro) e (ii) o congelamento causal de E3b (textura super-horizonte pinçada).
Sem isso → parar.
**Output:** `results/cmb/fm3/FM3V_gate.md`.

### FM3-1 — Kibble–Zurek na rede (a relíquia se forma?)
Resfriar (quench) o ferromagneto de orientação através de J_c a **taxas variáveis** e
medir a densidade de defeitos n_def e o comprimento de coerência ξ_dom vs taxa de
quench. Testar a lei de Zurek (ξ_dom ∝ τ_quench^σ). Usa `fm2_core`/`orientation_core`
para a dinâmica e `e3b_core` (carga B / Delaunay) para contar defeitos.
**Predição P1:** quench rápido deixa rede densa; lento, esparsa; lei de potência de
Zurek com σ finito. n_def NÃO →0 para quench cosmologicamente plausível.
**Output:** `results/cmb/fm3/FM3_1_kibble.{py,md,json,png}`.

### FM3-2 — Congelamento causal e equação de estado
A textura super-horizonte é congelada (E3b)? Medir o w_eff(escala): frio (w≈0) acima
do horizonte, dinâmico ao re-entrar. Comparar com o comportamento scaling de Turok
(que NÃO congela).
**Predição P2:** w_eff→0 super-horizonte (frozen, não-scaling); a rigidez causal de
E3b é o que produz isso.
**Output:** `results/cmb/fm3/FM3_2_freezing.{py,md,json,png}`.

### FM3-3 — Modulação do crescimento (suprime ou realça?)
A textura re-entrante modula o crescimento de δ_m. Estende a maquinaria de FM1
(CAMB + ODE) adicionando a relíquia como componente. Medir σ8, S8, f(z).
**Critério de morte:** σ8 realçado (C3) ou escala errada (C4).
**Predição P3:** σ8 SUPRIMIDO na direção de KiDS.
**Output:** `results/cmb/fm3/FM3_3_growth.{py,md,json,png}`.

### FM3-4 — Assinatura no CMB (sobrevive ao Planck?)
A assinatura da textura **frozen** difere da de Turok **scaling** (excluída)?
Comparar (ordem de grandeza, ancorado em FM3-1/2) com vínculos do Planck
(isocurvatura, não-gaussianidade de textura, picos).
**Output:** `results/cmb/fm3/FM3_4_cmb_signature.md`.

### FM3-5 — Síntese honesta + veredito (template A/B/C)
**Output:** `results/cmb/fm3/FM3_5_synthesis.md` + `README.md`.

---

## PROTOCOLO

1. **FM3-V antes de tudo** (E1 + E3b reproduzidos).
2. **FM3-1 e FM3-2 antes de FM3-3:** a relíquia e seu congelamento vêm da REDE
   primeiro; só então entram no crescimento.
3. **Anti-circularidade:** J_c, defeitos, congelamento — da rede; a₀ de SPARC;
   nenhum σ8/Planck inserido. "matéria escura"/"resolve S8" — COMPARISON ONLY.
4. **Verificação tripla** se Veredito A: V1 (Kibble robusto sob refinamento e ≥20
   sementes); V2 (w_eff≈0 super-horizonte estável); V3 (σ8 em KiDS COM assinatura CMB
   consistente com Planck, simultâneos).
5. **Critério de morte pré-registrado:** C1–C4 acima. Não ajustar para escapar.
6. **20 sementes** para FM3-1 e FM3-2.

---

## O QUE FM3 DECIDE

```
SE VEREDITO A:
  A peça fria-e-grande de S8 é uma RELÍQUIA da transição de fase do vácuo
  orientacional — matéria escura cosmológica = textura primordial de n⃗ congelada
  por causalidade. Escala certa (horizonte da transição) e fria pelo motivo certo
  (E3b), não por ajuste.
  → reabre o setor cosmológico fechado por FM1/FM2.
  → Paper VI (textura primordial / S8) justificado.
  → matéria escura, MOND e o fóton, TODOS do mesmo campo n⃗ (E1/E2/E3b/FM3).

SE VEREDITO C:
  A fronteira de SCALE_BOUNDARY.md fica confirmada e mais forte: nem a teoria
  estática (FM1/FM2) nem a relíquia dinâmica (FM3) da TEIC+DEV fornecem a peça de
  S8. O setor cosmológico exige física genuinamente externa.
  → a previsão válida permanece BTFR (galáxias), com a origem microscópica do ν MOND
    (FM2-1) como o ganho desta linha.
```

---

## NOTA DE HONESTIDADE (no pré-registro)

Esta é a campanha mais ambiciosa e o desfecho **mais provável continua sendo B ou C**.
Texturas/monopolos globais scaling JÁ são excluídos pelo Planck; a aposta é
**inteiramente** na versão **frozen** (não-scaling) que a rigidez causal de E3b
produziria — e mesmo essa precisa, simultaneamente, ser fria, cosmológica, suprimir
σ8 na medida certa, e ter assinatura CMB compatível. São quatro condições
independentes; acertar todas a partir da rede, sem ajuste, é difícil — e é o que
torna o teste valioso. Diferente de FM1/FM2, porém, esta candidata tem a **escala** e
o **frio pelos motivos certos** (horizonte + causalidade), não por parâmetros
ajustados — por isso vale o pré-registro.
