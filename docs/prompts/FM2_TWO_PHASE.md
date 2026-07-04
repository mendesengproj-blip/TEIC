# PROMPT — FM2_TWO_PHASE: matéria escura e MOND como duas fases do ferromagneto n⃗

> Charter PRÉ-REGISTRADO. Salvar na raiz do projeto TEIC.
> Continua FM1 (que matou o MOND-μ de fase única no setor de perturbações).
> Pergunta central: a TEIC+DEV *completa* — o ferromagneto de orientação do E1
> com a dinâmica de mágnon do E2 — fornece a **inversão** que MOND puro não dá,
> de modo que σ8 seja **suprimida** (resolvendo S8) em vez de realçada?
> Resultados em `results/cmb/fm2/`. Reutiliza os motores E1 (`orientation_core.py`),
> E2 (`e2_core.py`) e E3b (`e3b_core.py`). **NÃO modifica nenhuma campanha anterior.**

> ⚠️ **STATUS: PRÉ-REGISTRO escrito ANTES de rodar; depois EXECUTADO (jun/2026).**
> **VEREDITO C — MORTE: a estrutura de duas fases NÃO inverte S8 (obstrução
> estrutural). Resultado positivo: origem microscópica do ν MOND.**
> Ver `results/cmb/fm2/FM2_5_synthesis.md` e `README.md`. Predições e critérios de
> morte abaixo foram fixados ANTES de qualquer medição.
>
> **Resumo executado:** FM2-V PASS (J_c≈0.693, 2 motores concordam; mágnon c=1.014).
> FM2-1: ferromagneto reproduz deep-MOND (χ∥~h^(−0.4±0.1), origem Goldstone =
> ν=1/√(g/a₀)) MAS realce sustentado até g/a₀≲10⁻³, sem 2ª transição no gap
> (0.005,0.016) → C1/C4. FM2-2: c_s/c ∈ [0.14,6.4] O(1) → free-streama → C3; janela
> de Jeans (10⁻³) só com fine-tuning crítico. Obstrução estrutural: Botão 1 quer fase
> ORDENADA, Botão 2 quer ponto CRÍTICO — fases opostas, incompatíveis no mesmo J.
> **C.** Reabertura: a massa m_A (Paper II) dá ξ_A=ℏ/(m_A c)≈**17 pc** (= "L<17 pc"
> do Paper II) — **sub-galáctico, ~6 ordens abaixo da escala de σ8 (12 Mpc)** → NÃO
> altera o resultado cosmológico (corte no lado newtoniano, não no gap MOND). Um
> corte cosmológico exigiria m~5×10⁻³¹ eV, ~7×10⁵× mais leve, **excluído** pelo
> Paper II → seria escala nova, não o m_A. Botão 2 exigiria eq. de estado do
> condensado + ação relativística + CLASS.

---

## CONTEXTO: o que FM1 matou e o que deixou em aberto

FM1 testou a DEV no setor CMB/S8 e encontrou **Veredito C (morte)**: tratada como
**MOND de fase única, quase-estático, com μ(k,z) literal**, a DEV **realça** o
crescimento (todo modo linear é deep-MOND, g/a₀≈0.003–0.005, pela coincidência
a₀≈cH₀/2π) ⇒ σ8_DEV ≫ σ8_ΛCDM ⇒ piora a tensão S8.

O que FM1 **não** testou: a TEIC+DEV completa não é MOND de fase única. O E1
estabeleceu que o vácuo **é um ferromagneto de orientação com transição de fase**
(ordenado J>J_c, desordenado J<J_c). Isso abre a possibilidade — explorada
fenomenologicamente em superfluid-DM (Berezhiani–Khoury) e AeST (Skordis–Złośnik
2021, que **reproduz o CMB do Planck**) — de que **matéria escura e MOND sejam
duas fases do mesmo campo**:

```
fase ORDENADA   (galáxias, gradiente alinha n⃗)  → resposta coletiva → MOND
fase DESORDENADA/condensado (cosmologia)         → fluido tipo-DM no fundo
```

A TEIC fornece os ingredientes microscópicos que esses modelos *postulam*: E1 dá as
duas fases; E2 dá a velocidade de propagação (mágnon, c=0.98). FM2 testa se essa
estrutura **inverte** o sinal de FM1.

---

## A FÍSICA DA INVERSÃO

Para suprimir σ8 abaixo do ΛCDM (resolver S8) é preciso UMA de duas coisas:

1. **μ < 1** (gravidade efetiva mais fraca que Newton) nas escalas que fixam σ8, ou
2. **pressão / free-streaming**: uma componente com densidade certa no fundo
   (preserva BAO e picos do CMB) mas **velocidade do som** grande o bastante para
   apagar potência abaixo de uma escala de Jeans.

MOND puro não dá nenhuma. A TEIC pode dar via **dois botões**, cada um com uma
**janela estreita e falsificável** (é isso que torna FM2 um teste, não um ajuste):

### Botão 1 — Segunda transição de fase (saturação de ν em ultra-baixa aceleração)

ν(y)=1/√y → ∞ quando y=g/a₀→0 é uma **extrapolação** abaixo da faixa calibrada
(galáxias têm y≳0.016; a mais profunda confirmada é DGSAT-I em y=0.016). O ν é a
**susceptibilidade magnética** do ferromagneto E1 — e susceptibilidade real
**satura**, não diverge. Se há um segundo limiar a_c2 onde o ferromagneto
**desordena** (perde coerência MOND), ν vira/satura e o realce desliga em escalas
cosmológicas, **mantendo MOND nas galáxias**.

**Janela predita (falsificável):** o segundo limiar deve cair no **gap
observacional** entre a galáxia MOND mais profunda e os modos cosmológicos:
$$a_{c2}/a_0 \in (0.005,\ 0.016).$$
Acima de 0.016 → estraga ajustes de UDGs (DGSAT-I). Abaixo de 0.005 → não tame o
runaway cosmológico. A janela é apertada e testável por Euclid (UDGs ultra-baixa g).

### Botão 2 — Velocidade do som do condensado (supressão de Jeans)

A fase desordenada/condensado clusteriza como um fluido. Se sua velocidade do som
c_s for não-nula, há uma escala de Jeans k_J≈aH/c_s abaixo da qual o crescimento é
suprimido. Para suprimir na escala de σ8 (k≈0.1–0.2 h/Mpc) hoje:
$$c_s/c \sim 1.7\text{–}3.3\times10^{-3}.$$

**Os dois extremos são MORTE, e isso aperta a predição:**
- c_s ≈ c (=0.98, mágnon do vácuo do E2) → k_J≈3×10⁻⁴ h/Mpc → free-streama TUDO →
  nenhuma estrutura → morte.
- c_s = 0 (frio, como CDM) → clusteriza como CDM → σ8 ≥ ΛCDM → não resolve S8 →
  morte (seu próprio critério).
- A solução de S8 vive numa **janela estreita c_s/c ~ 10⁻³**. A TEIC tem que
  **prever** que c_s do condensado a densidade finita cai aí — c≈0.98 é o mágnon do
  **vácuo**, NÃO do condensado; são quantidades diferentes, e medir a do condensado
  é o coração de FM2.

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C) — qualquer uma destas:
  C1. ν(y) medido na rede DIVERGE monotonicamente (sem saturação/segunda transição)
      → runaway de FM1 persiste → MOND-completo falha na cosmologia igual.
  C2. Existe segunda transição mas a fase desordenada clusteriza FRIA (c_s_efetivo
      → 0) → σ8_FM2 ≥ σ8_ΛCDM → não resolve S8.
  C3. c_s do condensado ≈ c (vácuo) → free-streama tudo → sem estrutura (sem galáxias).
  C4. a_c2 cai FORA do gap (0.005, 0.016)·a₀ → contradiz dados de galáxias OU não
      tame o runaway.

SUCESSO PARCIAL (B):
  σ8_FM2 < σ8_ΛCDM (direção certa) mas fora de KiDS, OU os números (a_c2, c_s)
  saem da rede mas com incerteza grande demais para afirmar previsão.

SUCESSO (A):
  a_c2 ∈ (0.005,0.016)·a₀ E c_s/c ~ 10⁻³ EMERGEM da rede (E1/E2-style, NÃO
  ajustados ao CMB) E o crescimento resultante dá σ8_FM2 ∈ [0.746,0.786] (KiDS±2σ)
  ENQUANTO o fundo permanece ΛCDM-like (BAO + picos do CMB preservados).
  → A matéria escura e o MOND são duas fases do ferromagneto n⃗.
  → Verificação tripla obrigatória antes de afirmar.
```

**Anti-circularidade dura:** a₀ vem de SPARC; a_c2 e c_s vêm da REDE (E1/E2-style);
NADA é ajustado a σ8/KiDS. FM2 é teste, não ajuste. Se a janela for atingida, é
previsão; se não, é falsificação — reportada como tal.

---

## TAREFAS

### FM2-V — Gate (obrigatório antes de qualquer medida cosmológica)
Reproduzir, nos motores reutilizados, os resultados-âncora antes de estender:
E1 (transição ordem-desordem, J_c medido) e E2 (mágnon do vácuo c=0.98). Se os
motores não reproduzem os resultados publicados → parar.
**Output:** `results/cmb/fm2/FM2V_gate.md`.

### FM2-1 — Segunda transição: ν(y) e a_c2 (tipo-E1, com campo externo)
Acoplar o ferromagneto de orientação (`orientation_core.py`) a um **campo externo
h** que representa o gradiente gravitacional (h ∝ g). Medir a magnetização/
susceptibilidade m(h), χ(h) varrendo h por DÉCADAS abaixo da faixa de galáxias
(y = h/h₀ de 1 até 10⁻⁴). Procurar:
- ν(y)=χ(y) DIVERGE (1/√y) → C1, ou SATURA/vira em algum y_c.
- se vira: medir a_c2=y_c·a₀ e testar se ∈ (0.005,0.016).
**Predição P1:** existe saturação/segunda transição com a_c2/a₀ ∈ (0.005,0.016).
**Output:** `results/cmb/fm2/FM2_1_second_transition.{py,md,json,png}`.

### FM2-2 — Velocidade do som do condensado (tipo-E2, a densidade finita)
Reusar o estimador de dispersão de mágnon (`e2_core.py`) mas na fase
**ordenada/condensada a parâmetro de ordem finito** (m≠0), não no vácuo. Medir a
relação de dispersão das perturbações do condensado e extrair c_s. Comparar com o
vácuo (c=0.98).
**Predição P2:** c_s do condensado < c do vácuo; idealmente c_s/c ~ 10⁻³ (janela de
Jeans). Reportar honestamente onde cai — se ~c (C3) ou ~0 (C2), é morte.
**Output:** `results/cmb/fm2/FM2_2_condensate_cs.{py,md,json,png}`.

### FM2-3 — Crescimento com duas fases e σ8 (estende FM1-2/3)
Reescrever μ(k,z) de FM1 com (i) a saturação de ν medida em FM2-1 e (ii) a
supressão de Jeans com o c_s medido em FM2-2. Recalcular σ8, S8, f(z) DEV-duas-fases
vs ΛCDM vs KiDS. Mesmo baseline CAMB de FM1 (CLASS indisponível; declarado).
**Critério de morte:** σ8_FM2 ≥ σ8_ΛCDM = C (C1/C2).
**Output:** `results/cmb/fm2/FM2_3_sigma8_twophase.{py,md,json,png}`.

### FM2-4 — Consistência de fundo (a restrição AeST)
Verificar que a fase desordenada fornece densidade de energia tipo-poeira no fundo
(Ωm efetivo correto) de modo a **preservar** BAO e a posição/altura dos picos do
CMB. Uma supressão de σ8 que estrague o fundo é falsificação, não solução.
**Output:** `results/cmb/fm2/FM2_4_background.md`.

### FM2-5 — Síntese honesta + veredito (template A/B/C como acima)
**Output:** `results/cmb/fm2/FM2_5_synthesis.md` + `README.md`.

---

## PROTOCOLO

1. **FM2-V antes de tudo.** Os motores E1/E2 reutilizados devem reproduzir os
   resultados publicados antes de qualquer extensão.
2. **FM2-1 e FM2-2 antes de FM2-3.** Os números a_c2 e c_s vêm da REDE primeiro; só
   então entram no crescimento. O analítico de FM1-1 (μ=ν(k/k_*)) guia, mas ν e c_s
   são MEDIDOS, não postulados.
3. **Anti-circularidade:** a₀ de SPARC; a_c2 e c_s da rede; NUNCA ajustar a σ8/KiDS.
   "matéria escura"/"resolve S8" — COMPARISON ONLY até FM2-5.
4. **Verificação tripla** se Veredito A (como spin-½ e o exigido para E=mc²):
   V1 — a_c2 estável sob refinamento de rede e em ≥20 sementes;
   V2 — c_s estável sob refinamento e densidade do condensado;
   V3 — σ8_FM2 em KiDS COM fundo ΛCDM-like simultaneamente.
5. **Critério de morte pré-registrado:** qualquer C1–C4 acima. Não ajustar
   parâmetros para escapar.
6. **20 sementes** para FM2-1 e FM2-2; baseline CAMB declarado para FM2-3.

---

## O QUE FM2 DECIDE

```
SE VEREDITO A:
  A TEIC+DEV unifica o que ΛCDM e MOND fazem em separado:
    galáxias (fase ordenada)   → MOND, curvas planas (já: Paper I)
    cosmologia (fase desordenada) → fluido tipo-DM que resolve S8 via Jeans
  matéria escura = uma FASE do ferromagneto de orientação, não uma partícula nova.
  → previsão observacional dupla (BTFR já confirmado + S8) → análise sobe.
  → Paper VI (DEV cosmológico de duas fases) justificado.

SE VEREDITO C:
  A fronteira fica definitivamente mapeada:
    a DEV funciona onde foi calibrada (baixa aceleração, sistemas ligados),
    mas a fase cosmológica do ferromagneto NÃO fornece a supressão de S8.
  → a previsão válida da DEV permanece BTFR (galáxias), não o CMB.
  → kill-criterion honesto, teoria não inflada além do que mede.
```

---

## NOTA DE HONESTIDADE (registrada no pré-registro)

Este é o passo mais ambicioso da TEIC e o desfecho **mais provável é B ou C**, não
A: as duas janelas (a_c2 no gap, c_s~10⁻³) são estreitas e independentes, e a TEIC
teria que acertar AS DUAS a partir da rede, sem ajuste. Acertar uma e errar a outra
já é Veredito C. A força do teste está justamente nisso: é difícil de passar por
acaso. AeST mostra que *passar* na cosmologia é possível; *resolver* S8 (bater o
ΛCDM) é mais do que isso, e exige que c_s e a_c2 caiam nas janelas — uma previsão
genuína que a rede confirma ou nega.
