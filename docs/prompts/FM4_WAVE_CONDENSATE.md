# PROMPT — FM4_WAVE_CONDENSATE: o vetor massivo m_A como matéria escura de onda (a porta encostada)

> Charter PRÉ-REGISTRADO. Salvar na raiz do projeto TEIC.
> Continua FM1/FM2/FM3 (três mortes no setor de ORIENTAÇÃO/Goldstone; ver
> `results/cmb/SCALE_BOUNDARY.md`). Nasce da análise de `TEIC_DEV_VISION.md`: a peça
> fria w=0 não pode vir do setor sem massa (Goldstone) — tem que vir do setor
> **MASSIVO**, que NUNCA testamos.
> Pergunta central: o campo vetorial massivo da DEV (m_A, Paper II), frozen por
> fricção de Hubble e oscilando coerentemente no universo jovem (misalignment), forma
> uma **matéria escura de onda (fuzzy)** fria (w=0) cuja escala de de Broglie/Jeans
> **suprime σ8** — fechando, ao mesmo tempo, o problema de equação de estado (FM3) e
> o de escala (FM2)?
> Resultados em `results/cmb/fm4/`. Reutiliza `e2_core` (dispersão de mágnon).
> **NÃO modifica nenhuma campanha anterior.**

> ⚠️ **STATUS: PRÉ-REGISTRO escrito ANTES de rodar; depois EXECUTADO (jun/2026).**
> **VEREDITO C para S8 — MAS o setor massivo É matéria escura fria (w=0), o maior
> positivo do programa.** FM4-V PASS; FM4-1: misalignment dá w=−0.04≈0, ρ~a⁻³ → **o
> m_A massivo É CDM** (a peça w=0 que FM3 não tinha); FM4-2: Jeans no piso na banda de
> σ8; FM4-3: σ8 mal se move (0.811→0.807, não alcança KiDS 0.766); FM4-4: a massa
> leve+fração que ajudaria σ8 super-suprime o Lyman-α (f=0.1 no piso → 19% supp) →
> **4ª morte (C3)**. Não há janela: ajudar σ8 e sobreviver ao Lyman-α são exclusivos.
> **A TEIC+DEV TEM matéria escura (m_A frio) mas NÃO resolve S8 em nenhum setor.**
> Ver `results/cmb/fm4/FM4_5_synthesis.md`. Predições/mortes fixadas ANTES de medir.

---

## CONTEXTO: por que esta é a única porta que sobrou (e por que é diferente)

FM1/FM2/FM3 morreram, e o mapa de `SCALE_BOUNDARY.md` mostra o fio comum: **as três
trabalharam no setor de ORIENTAÇÃO (Goldstone)** — e Goldstones são, por construção,
**sem massa**:
- realçam (MOND, FM1) ou
- são quentes (c_s~c, FM2) ou
- congelados têm gradiente (w=−1/3, FM3).

**Nenhum dá w=0 frio**, porque "frio de pressão, em repouso, clusterizando" exige
**MASSA**. A TEIC+DEV tem um setor massivo que jamais testamos: o **vetor massivo
m_A** (Paper II, m_A > 3.7×10⁻²⁵ eV/c²). Em FM2 o descartamos como *alcance de Yukawa*
(ξ=17 pc, escala errada). Mas há uma segunda leitura, nunca explorada: um campo
massivo pode formar um **condensado coerente que oscila** → matéria escura de **onda
(fuzzy/ultraleve)**, que é **w=0 fria** com uma **escala de Jeans que SUPRIME** a
estrutura.

---

## A FÍSICA

Um campo massivo deslocado do mínimo é **frozen por fricção de Hubble** enquanto
H > m_A; quando H cai abaixo de m_A, ele **oscila** coerentemente. Um campo massivo
oscilando tem, na média, **w = 0** (energia cinética e potencial se alternam) →
comporta-se como **matéria fria** (ρ ∝ a⁻³). É o mecanismo de misalignment (áxion/ULDM).

Crucial para S8 — a **escala de de Broglie/Jeans**:

| m_A (eV) | k_½ (1/Mpc) | λ supressão (Mpc) |
|---|---|---|
| 10⁻²² | 4.6 | 1.4 (escala de galáxia, fuzzy clássico) |
| 10⁻²³ | 1.65 | 3.8 |
| 10⁻²⁴ | 0.59 | 10.6 |
| **3.7×10⁻²⁵ (piso Paper II)** | **0.38** | **16.5** |
| 10⁻²⁵ | 0.21 | 29.4 |

A escala de σ8 é k ~ 0.1–0.2 h/Mpc (~0.15–0.3 /Mpc). **m_A perto do piso do Paper II
(10⁻²⁴–10⁻²⁵ eV) coloca a supressão exatamente na escala de σ8** — onde S8 pede um
freio. **Esta é a primeira candidata com w=0 (fixa FM3) E a escala certa (fixa FM2),
porque vive no setor massivo.**

**A tensão honesta (e o kill-criterion externo):** Lyman-α exclui ULDM como **100%**
da matéria escura para m < ~2×10⁻²¹ eV — m_A é ~10⁴× mais leve, então como DM **único**
ele **super-suprime** e está excluído. A saída viável é ser uma **fração** f da DM
(f ~ 0.1–0.3): uma supressão **suave** na escala de σ8 que baixa σ8 rumo a KiDS sem
matar a estrutura de pequena escala. (Essa "fração ultraleve que resolve S8" é uma
proposta real e viva na literatura.)

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C) — qualquer uma:
  C1. O modo massivo NÃO se comporta como frio (w não → 0 ao oscilar).
  C2. A escala de Jeans cai no lugar errado: pequena demais (k_½ ≫ 1/Mpc → indistinto
      de CDM, não ajuda S8) OU grande demais (suprime banda larga / BAO / forma do P(k)).
  C3. Lyman-α exclui a massa+fração necessária (a supressão que ajuda σ8 também mata a
      estrutura de pequena escala, mesmo como fração).
  C4. O misalignment NÃO produz uma fração plausível (Ω_fuzzy/Ω_DM fora de 0.05–0.5).

SUCESSO PARCIAL (B):
  Suprime σ8 na direção certa como fração, mas insuficiente para KiDS, OU a janela
  (massa, fração) existe mas com incerteza grande (precisa de CLASS para confirmar).

SUCESSO (A):
  m_A no intervalo permitido (Paper II + Lyman-α) forma condensado frio (w≈0,
  misalignment) com Jeans na escala de σ8; uma fração f~0.1–0.3 suprime σ8 para a
  faixa KiDS (0.746–0.786) SEM violar Lyman-α nem o P(k) banda-larga/BAO.
  → A matéria escura é o setor MASSIVO da TEIC+DEV (m_A como ULDM), e a fração
    ultraleve resolve S8. → reabre o setor cosmológico fechado por FM1/FM2/FM3.
  → Verificação tripla obrigatória antes de afirmar.
```

**Anti-circularidade dura:** m_A vem do Paper II (galáxias/estabilidade, NÃO do CMB);
w, a escala de Jeans e a abundância vêm da dinâmica do campo; NENHUM valor de
σ8/KiDS/Lyman-α é inserido no gerador. Os limites do Planck/Lyman-α são COMPARISON
ONLY. As janelas (w=0, Jeans na escala de σ8, fração) foram fixadas ANTES de medir.

---

## TAREFAS

### FM4-V — Gate (obrigatório)
Estender E2: o modo de orientação **com massa** tem dispersão ω² = c²k² + m_A²
(gapped), não o ω=ck sem massa (E2 mediu m²<0, massless). Reproduzir a dispersão
massiva no `e2_core` (símbolo BD com um termo de massa) e recuperar o gap. Sem isso →
parar. **Lattice-mensurável.**
**Output:** `results/cmb/fm4/FM4V_gate.md`.

### FM4-1 — Misalignment → frio (w=0)
Evoluir um campo massivo com fricção de Hubble (Klein-Gordon/Proca em fundo FRW): mostrar
que ele **freezes** (H>m_A) e depois **oscila** com ⟨w⟩→0 (ρ∝a⁻³). Medir w_eff(a).
**Predição P1:** ⟨w⟩→0 ao oscilar (frio de pressão — o que FM3 não tinha).
**Output:** `results/cmb/fm4/FM4_1_misalignment.{py,md,json,png}`.

### FM4-2 — Escala de de Broglie/Jeans vs massa
Calcular k_J(m_A) (de Broglie + Jeans quântico) e confirmar que, para m_A no intervalo
permitido, a supressão cai na escala de σ8 (k~0.1–0.6/Mpc). **Analítico + transfer
function de ULDM.**
**Predição P2:** k_½ ≈ 0.4–0.6 /Mpc para m_A ~ 10⁻²⁴–3.7×10⁻²⁵ eV (tabela acima).
**Output:** `results/cmb/fm4/FM4_2_jeans.{py,md,json,png}`.

### FM4-3 — Supressão de σ8 como fração f
Estender a maquinaria de FM1 (CAMB + crescimento) adicionando uma componente ULDM de
fração f com a transfer function fuzzy (corte em k_J). Medir σ8(f, m_A), S8.
**Critério de morte:** sem supressão (C2) ou só com f implausível.
**Predição P3:** f~0.1–0.3 com m_A no intervalo baixa σ8 rumo a KiDS.
**Output:** `results/cmb/fm4/FM4_3_sigma8_fraction.{py,md,json,png}`.

### FM4-4 — Lyman-α + abundância (o critério de morte externo)
Verificar se a (massa, fração) que ajuda σ8 sobrevive ao Lyman-α (que exclui ULDM
leve como 100%) e se o misalignment dá Ω_fuzzy/Ω_DM ~ f plausível.
**Output:** `results/cmb/fm4/FM4_4_lyman_abundance.md`.

### FM4-5 — Síntese honesta + veredito (template A/B/C)
**Output:** `results/cmb/fm4/FM4_5_synthesis.md` + `README.md`.

---

## PROTOCOLO

1. **FM4-V antes de tudo** (dispersão massiva reproduzida).
2. **FM4-1 e FM4-2 antes de FM4-3:** w=0 e a escala de Jeans vêm da física do campo
   primeiro; só então entram no crescimento.
3. **Anti-circularidade:** m_A do Paper II; w/Jeans/abundância da dinâmica; nenhum
   σ8/Lyman-α inserido. "matéria escura"/"resolve S8" — COMPARISON ONLY.
4. **Verificação tripla** se Veredito A: V1 (w→0 robusto sob refinamento), V2 (Jeans na
   escala de σ8 para o intervalo de massa, estável), V3 (σ8 em KiDS COM Lyman-α e P(k)
   banda-larga simultaneamente OK).
5. **Critério de morte pré-registrado:** C1–C4. Não ajustar para escapar.
6. **Onde a rede mede vs onde precisa de CLASS:** FM4-V/FM4-1 são lattice/dinâmica;
   FM4-2 é analítico; FM4-3/FM4-4 estendem FM1 (CAMB) e usam a transfer function ULDM
   conhecida — os números finais de Lyman-α/banda-larga pediriam CLASS+axionCAMB,
   declarado.

---

## O QUE FM4 DECIDE

```
SE VEREDITO A:
  A matéria escura é o setor MASSIVO da TEIC+DEV — o vetor m_A como condensado de onda
  (ULDM/fuzzy via misalignment). w=0 (fixa FM3), Jeans na escala de σ8 (fixa FM2), e a
  fração ultraleve SUPRIME σ8 (fecha S8). Tudo de um ingrediente JÁ na teoria (m_A),
  só num mecanismo novo (oscilação coerente).
  → reabre o setor cosmológico fechado por FM1/FM2/FM3.
  → fóton (E2), matéria/MOND (galáxias), E matéria escura (m_A fuzzy) — todos do mesmo
    vácuo. → Paper VI justificado.

SE VEREDITO C:
  As QUATRO rotas (Goldstone realça/quente/textura + massivo fuzzy) estão fechadas. A
  TEIC+DEV não fornece a peça de S8 em nenhum setor → exige física genuinamente externa
  (partícula de DM não relacionada ao vácuo orientacional). A fronteira fica definitiva.
  → a previsão válida permanece BTFR (galáxias).
```

---

## NOTA DE HONESTIDADE (no pré-registro)

Esta é **a última porta** e a **única no setor massivo** — por isso é a mais
promissora desde FM1: é a primeira candidata que ataca **simultaneamente** o problema
de escala (FM2) e o de equação de estado (FM3), porque w=0 e a escala de Jeans vêm
**ambos** da massa. Os números de de Broglie (tabela) caem **exatamente** na escala de
σ8 para m_A perto do piso do Paper II — o que é encorajador e não-trivial. MAS o risco
é real e específico: m_A é leve demais para ser 100% da DM (Lyman-α), então tudo
depende de funcionar como **fração** — e se a fração necessária para mover σ8 já
super-suprime o Lyman-α, é a 4ª morte. O desfecho honesto mais provável é **B** (ajuda
como fração, números finais pedem CLASS) ou um **A estreito**; mas, diferente das três
anteriores, esta porta tem w=0 e a escala certa pelos motivos certos — vale abrir.
