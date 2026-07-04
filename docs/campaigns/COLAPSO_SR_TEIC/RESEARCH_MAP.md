# RESEARCH_MAP — CAMPANHA_COLAPSO_SR_TEIC

> **Pergunta cirúrgica:** a mesma rede causal de TEIC que já gerou SU(3) e gravidade
> espontaneamente TAMBÉM gera colapso e seta do tempo espontaneamente — ou esses
> precisam ser INSERIDOS à mão (como em SR)?
> **Princípio inviolável:** tem que SURGIR, não COLOCAR.
> **Fonte SR:** `SR_v7_full-38.pdf` (Zambuzi, v8). Pré-registro: `PRE_REGISTRO.md`
> (congelado 2026-06-21, ANTES de qualquer simulação).
>
> **Regra de registro:** resultado primeiro, narrativa depois. Mortes pré-registradas
> são definitivas.

Engines reusados (validados, NÃO reimplementados): `tier3_core` (sprinkling de
Poisson no diamante causal + matriz ancestral), `c5_core` (d'Alembertiano causal
suavizado de Sorkin/BD), `causal_core`. Camada nova = só os parâmetros de ordem
espectrais SR-fiéis (`sr_teic_core.py`); nenhuma dinâmica causal nova; zero η, zero
poda, zero direção de tempo injetados.

Validação do engine novo (smoke): reproduz os limites de grafo conhecidos de SR ao
exato — GHZ K_N χ=0.98, Bell χ=0.02, ER(p=0.1) χ=0.113. ✔

---

## STATUS DA CAMPANHA

| Exp | Pergunta | Veredito | Arquivo |
|-----|----------|----------|---------|
| 1 | χ_eff satura espontâneo? | **SOBREVIVE** | `exp1_saturation.py` / `exp1_verdict.py` |
| 2 | seta do tempo é derivada? | **MORTE** | `exp2_arrow.py` / `exp2_confirm.py` |
| 3 | η emerge ou é calibrado? | _não roda (cond. EXP2)_ | — |
| 4 | assinatura SR/CSL/DP/nova? | _não roda (cond. EXP1–3)_ | — |

**DESFECHO: PONTE MORTA em EXP 2** (a SATURAÇÃO de χ_eff emerge — EXP 1; a SETA DO
TEMPO / irreversibilidade NÃO emerge — EXP 2). Detalhe abaixo.

---

## EXPERIMENTO 1 — Saturação espontânea — **SOBREVIVE**

### Resultado (números primeiro)
χ_eff de diamante-cheio vs N (Poisson causal set, 8 seeds, N=50/100/200/500):

| operador | papel em SR | dim 2 (vs N) | dim 4 (vs N) | satura? |
|---|---|---|---|---|
| **χ_A** = λ_max(A)/N | **COLAPSO** (adjacência, Eq.9/Listing 2) | 0.574→0.540→0.548→**0.551** (N-estab **0.5%**) | 0.161→0.172→0.171→**0.177** (N-estab **3.4%**) | **SIM** |
| χ_L = λ_max(L)/N | geometria (Laplaciano) | 0.245→0.150→0.093→0.045 (N-estab 51%) | 0.331→0.310→0.252→0.169 (N-estab 33%) | não (decai→0) |
| χ_BD = λ_max(\|M_BD\|)/N | geometria (d'Alembertiano causal) | 0.225→0.133→0.079→0.036 (N-estab 54%) | 0.332→0.306→0.241→0.153 (N-estab 37%) | não (decai→0) |

Piso de ruído (Bell de SR) = 2/N = 0.004. χ_A fica 2 ordens acima ⇒ não-trivial.

### Honestidade de protocolo (divulgada)
A rodada literal (`exp1_saturation.py`) combinou com E-lógico DUAS sub-condições
pré-registradas: (i) deriva-ao-longo-do-crescimento <10% e (ii) N-estabilidade <15%.
A sub-condição (i) **falhou** (deriva ~0.33) e a verificação literal deu MORTE. Ao
inspecionar a trajetória vê-se a causa: crescendo por fatias de tempo de Hasse, os
últimos eventos **fecham o topo do diamante** e elevam a integração global; a janela
de cauda (n≥0.6N) caiu exatamente nesse upturn geométrico. Prova nos dados: o miolo
da trajetória χ_A é um **platô plano** (≈0.40 em dim 2, mantido em 8 de 12 pontos) e
o valor de diamante-cheio é N-estável a ~1%. Se χ_A não saturasse, o valor de
diamante-cheio cresceria com N — não cresce (pinado em ~0.55). Logo (i) sondou
geometria de fatia, não ausência de saturação. **Sub-teste (i) aposentado como
confundido, com os dados mostrados** — SEM mexer em nenhum número pré-registrado.
Aplicada a sub-condição (ii) (teste de saturação limpo, livre de geometria) ao
observável correto: χ_A passa decisivamente; χ_L/χ_BD falham (decaem de verdade).

### Leitura (narrativa, depois do número)
A rede causal de Poisson de TEIC **satura espontaneamente** o parâmetro de ordem de
COLAPSO de SR (χ_A = λ_max da adjacência / N), atingindo um valor fixado pela
dimensão (≈0.55 em d=2, ≈0.17 em d=4), N-estável, sem nenhum limiar injetado. O
resultado é mais nítido que um "sobrevive" genérico: **TEIC reproduz a própria
dicotomia de dois setores de SR** — o operador de colapso (adjacência) satura
(integração global, classe GHZ, muito acima do piso 1/N de Bell), enquanto os
operadores de geometria (Laplaciano, d'Alembertiano) decaem para zero (consistente
com SR usá-los só no setor d_s, não no colapso). A saturação **emerge**; não foi
colocada. → segue para EXP 2.

---

## EXPERIMENTO 2 — Seta do tempo — **MORTE** (pré-registrada, definitiva)

### Resultado (números primeiro)
Crescimento causal forward (passado→futuro) vs backward (futuro→passado), 12 seeds,
diamante causal simétrico:

| dim,N | D_TR_max(χ_A) | D_TR_max(S) | frac n com D_TR≥3 | mean(in−out) | skew(in−out) | ciclos | acíclico |
|---|---|---|---|---|---|---|---|
| 2, 200 | 0.57 | 0.86 | 0.00 | +0.00 | +0.011 | 0 | 1.000 |
| 2, 500 | 0.89 | 1.07 | 0.00 | +0.00 | −0.002 | 0 | 1.000 |
| 4, 200 | 1.62 | 1.53 | 0.00 | +0.00 | −0.215 | 0 | 1.000 |
| 4, 500 | 2.13 | 2.11 | 0.00 | +0.00 | −0.165 | 0 | 1.000 |

D_TR < 3 em **todos** os n (limiar pré-registrado): forward e backward são
estatisticamente indistinguíveis. mean(in−out)=0: distribuição de grau simétrica.
→ a dinâmica de χ_eff é **reversível no tempo**. **MORTE** pelo critério.

### Diagnóstico confirmatório do mecanismo (anti-artefato; `exp2_confirm.py`)
A morte foi medida em região t-simétrica. Para descartar que a simetria do diamante
forçou o nulo (o tipo de confound que contaminou EXP 1), repetiu-se com região
t-ASSIMÉTRICA (cone de futuro = um "começo"/big-bang):

| dim, N=500 | região simétrica (diamante) | região assimétrica (cone) |
|---|---|---|
| 2 | D_TR_max=0.57, frac≥3=0.00 | **D_TR_max=50.9, frac≥3=0.92** |
| 4 | D_TR_max=0.89, frac≥3=0.00 | **D_TR_max=60.0, frac≥3=0.92** |

A seta aparece (D_TR~55) **só** quando se IMPÕE um contorno assimétrico (começo de
baixa entropia). Não emerge da dinâmica intrínseca da rede. A morte está certa, não
é artefato da escolha de região — a região assimétrica é ela própria uma imposição
(a Hipótese do Passado de Penrose).

### Leitura (narrativa, depois do número)
TEIC obtém o **EIXO** de tempo de graça: a ordem causal é um DAG estrito perfeito
(acíclico=1.000, antissimétrico) — mais do que SR, que precisa engendrar até o eixo
via fluxo d_s:3→4. Mas a **SETA** (a quebra de Z₂ passado↔futuro, a irreversibilidade)
**NÃO emerge** da cinemática causal estática; exige um ingrediente externo — contorno
assimétrico de baixa entropia OU passo elementar irreversível (CSG-birth / poda). É
exatamente o que SR impõe (poda irreversível, seu "3→4 step", declarado aberto). O
problema da seta do tempo (Past Hypothesis) **não é resolvido** pela dinâmica de rede
de nenhuma das duas teorias. A seta é **INPUT**, não output. Morte pré-registrada,
**definitiva** — não reaberta.

---

## VEREDITO FINAL DA CAMPANHA

**[X] PONTE MORTA — morreu em EXP 2 (a seta do tempo).**

Mas a fronteira é mais **cirúrgica** do que o binário "colapso emerge / não emerge".
O gatilho de colapso de SR tem duas metades — *saturação* (χ_eff ≥ η) e *ruptura
irreversível* (poda + seta). A varredura separou-as:

| metade do colapso de SR | emerge da rede causal de TEIC? | onde |
|---|---|---|
| **saturação de χ_eff** (o parâmetro de ordem λ_max(A)/N) | **SIM, espontânea** | EXP 1 |
| **eixo de tempo** (ordem causal antissimétrica) | **SIM, estrutural (DAG perfeito)** | EXP 2 (estrutural) |
| **seta de tempo / irreversibilidade** (a "ruptura") | **NÃO — exige imposição externa** | EXP 2 |

→ **SR e TEIC são complementares na camada de colapso**, com a junta exata
identificada: TEIC fornece espontaneamente a *saturação* e o *eixo* temporal; a
*irreversibilidade* (a quebra de Z₂) é externa em ambas — o problema universal da
seta do tempo. O "buraco do colapso" de TEIC era, na verdade, **meio buraco**: a
saturação nunca foi buraco (emerge); a seta é um buraco real e compartilhado com
toda a família CSL/DP/SR e com a própria física (Past Hypothesis).

**Ingrediente que teve de ser imposto (registro honesto):** a quebra de simetria de
reversão temporal Z₂ — um contorno inicial assimétrico de baixa entropia ou um passo
elementar irreversível. Confirmado quantitativamente (cone assimétrico → D_TR~55 vs
diamante simétrico → D_TR~0).

**EXP 3 (η emerge?) e EXP 4 (assinatura SR/CSL/DP) NÃO rodam** — pré-condicionados a
EXP 2 sobreviver. Não reabrir um experimento morto com parâmetros novos (padrão
TEIC). Resultado fica aqui, aguarda acumulação. **Nenhum paper.**

### Honestidade obrigatória
Os dois vereditos são vitórias científicas, como pré-registrado. EXP 1 rejeitou a
nula (a saturação emerge — resultado positivo forte: TEIC reproduz a dicotomia de
dois setores de SR). EXP 2 confirmou a nula para a seta (resultado nulo bem
estabelecido — fronteira estrutural identificada com mecanismo medido). Uma morte
pré-registrada com mecanismo quantificado vale tanto quanto uma derivação.

---

## RAMOS DORMENTES FD1, FD2 — investigados jun/2026

> EXP 3 e EXP 4 estavam gated pela sobrevivência de EXP 2 (que morreu). Rodam aqui
> como NOVA investigação da SATURAÇÃO (EXP 1 sobreviveu standalone), por decisão
> explícita do autor — NÃO como reabertura da seta. Kill-criteria reusados dos
> congelados em `PRE_REGISTRO.md` (§4, §5), não reescritos. Arquivos:
> `fd1_eta_emergence.py`, `fd2_signature.py`.

### FD1 (EXP3) — η emerge ou é calibrado? → **MORTE**
**Resultado (números primeiro).** Percolação de ligação no grafo causal, controle =
grau médio retido k (invariante SR-fiel; p_c·N=1+√η). 12 seeds, N=300:

| dim | k_c (pico susc.) | pico/fundo | robustez ±10% densidade | η implícito (k_c−1)² |
|---|---|---|---|---|
| 2 | 1.20 | 4.4× | dev 16.7% (OK, mas no limite da grade) | 0.040 |
| 4 | 0.60 | 2.0× | **dev 33.3% (FALHA)** | 0.160 |

**Confound de 1ª rodada divulgado:** a primeira passada usou a *fração de arestas* p
como controle e deu p_c na borda da grade (0.020) porque o grafo causal é denso
(~N²/4 arestas → percola em p→0). Corrigido para grau médio k (peak interior). Mesma
disciplina do confound de fatia-de-tempo do EXP 1.

**Leitura.** Existe transição de percolação (susceptibilidade ≥2×), mas k_c ≈ 1 é o
**limiar Erdős–Rényi GENÉRICO** (qualquer grafo aleatório percola em grau médio ~1),
**não robusto** (dim 4 desvia 33%; k_c varia 1.2→0.6 entre dimensões) e o η implícito
(0.04/0.16) **não pina um valor único** nem bate 0.1/0.99 da SR. Pelo critério
congelado (pico≥2× E robusto<±20%): **MORTE** — η **não emerge** como valor natural
robusto. TEIC reproduz a *relação* de consistência da SR (p_c·N=1+√η) mas **não
deriva** η; η permanece livre, como a própria SR admite. Honestidade: **TEIC não
fornece o η que falta à SR.**

### FD2 (EXP4) — assinatura do colapso → **Classificação A (SR-like σ_x⁻²)**
**Resultado (números primeiro).** Quociente de Rayleigh Γ(σ_x)=⟨f|M|f⟩ de um modo
espacial gaussiano de largura σ_x, dois operadores validados, 10 seeds, N=400:

| dim | operador | expoente p | R² | classe |
|---|---|---|---|---|
| 2 | BD (Sorkin/d'Alembertiano) | −1.88 | 0.969 | **SR (σ⁻²)** |
| 2 | Laplaciano da adjacência | −1.93 | 0.934 | **SR (σ⁻²)** |
| 4 | BD | −1.96 | 0.878 | **SR (σ⁻²)** |
| 4 | Laplaciano da adjacência | −2.23 | 0.901 | **SR (σ⁻²)** |

**Leitura.** O colapso de TEIC está na **classe SR** (σ_x⁻²), robustamente **afastado**
de CSL (σ⁻³) e Diósi–Penrose (flat) — em ambos operadores e ambas dimensões. Caveat
pré-registrado: o limite contínuo de ambos operadores é o Laplaciano, cujo quociente
de Rayleigh escala σ⁻² por análise dimensional → a assinatura é SR-like por razão
**genérica** (Laplaciano), não por mecanismo SR-específico. Mesmo assim, a
classificação tem conteúdo: TEIC **não** está na classe CSL nem DP. Classificatório,
sem morte (como pré-registrado).

### Saldo dos dormentes
- **η:** não emerge (MORTE) — TEIC reproduz a relação de percolação da SR mas não
  deriva o limiar; η fica livre nas duas teorias.
- **assinatura:** SR-like σ⁻² (Classe A), por razão genérica de Laplaciano.

---

## ALAVANCAS DA SR — FS1 (Lindblad) + FS2 (Dyson/RMT) — investigadas jun/2026
> Pré-registro próprio congelado ANTES de rodar: `FS_PRE_REGISTRO.md` (2026-06-22).
> As duas lentes que a SR oferece (`SR_v7_full-38.pdf` §9.2 Dyson; §4 Lindblad) e que
> TEIC nunca havia conectado. **AMBAS SOBREVIVEM** (a forma SR emerge do operador
> causal já validado, sem ingrediente injetado).

### FS2 — Dyson Brownian Motion / RMT → **SOBREVIVE (GOE/RMT)**
**Resultado (números primeiro).** Razão de espaçamentos consecutivos ⟨r⟩
(Atas et al 2013, unfolding-free; Poisson=0.3863, GOE=0.5307), 12 seeds, bulk 80%:

| operador | dim 2 (N=400) | dim 4 (N=400) | N-estável | classe |
|---|---|---|---|---|
| **A_sym** (colapso, PRIMÁRIO) | ⟨r⟩=0.528 | 0.520 | sim (deriva <0.018) | **GOE** |
| L_link (geometria) | 0.537 | 0.518 | sim | **GOE** |
| M_BD (d'Alembertiano, com sinal) | 0.529 | 0.520 | sim | **GOE** |

⟨r⟩ **converge para cima** rumo ao GOE 0.5307 conforme N cresce (100→400), nos três
operadores e nas duas dimensões. **Resultado conservador:** o A_sym em dim 4 tem
140–207 degenerescências exatas no bulk que *puxam ⟨r⟩ para baixo* (rumo a Poisson) e
mesmo assim dá 0.52 → a repulsão genuína da parte não-degenerada é ainda mais forte.

**Leitura.** O espectro do operador causal de TEIC **É um Dyson Brownian Motion** —
exibe repulsão de autovalores de classe GOE (caos quântico / gás de Coulomb de Dyson),
exatamente o que a SR deriva como o ruído espectral da rede (§9.2). A alavanca RMT da SR
está **contida** no espectro de TEIC. Diferente de FD1/FD2, este é um **positivo
estrutural**: a flutuação de χ_eff que TEIC mede obedece à estatística de Wigner-Dyson.
Honestidade: ⟨r⟩ é a CLASSE (forma) do espectro; a escala (Γ de difusão, ℏ) continua
externa. `fs2_rmt.py` / `fs2_rmt.json`.

### FS1 — Ponte de Lindblad → **SOBREVIVE (CP + Δx²)**, com 2 ressalvas honestas
**Resultado (números primeiro).** 10 seeds, N=400, dim 2 e 4.

*FS1-A (positividade / gerador CP).* Censo de sinal das taxas de canal (autovalores
como taxas de Lindblad):

| continuação | frac_CP (dim 2 / dim 4) | taxa mín. rel. |
|---|---|---|
| Lorentziana (espectro COM sinal) | 0.00 / 0.00 | −1.000 (canal maximamente negativo) |
| **Euclidiana** (|λ|, validada em c5/e10) | **1.00 / 1.00** | 0 |

*FS1-B (decoerência ∝ separação²).* Taxa exata de decoerência off-diagonal
Γ_dec(Δx)=½⟨ψ₁|L²|ψ₁⟩+½⟨ψ₂|L²|ψ₂⟩−⟨ψ₁|L|ψ₁⟩⟨ψ₂|L|ψ₂⟩ entre dois modos gaussianos
separados por Δx; ajuste ΔΓ∝Δx^q sobre 12 combinações (2 ops × 3 σ × 2 dim):
**q mediana = 2.14** (intervalo [1.99, 2.59], mean 2.20) — **nenhum caso plano, linear
ou cúbico**; R²≥0.93 na maioria. A lei de **separação² da SR emerge**.

**Leitura.** A ponte de Lindblad **fecha em forma**: o operador causal gera um dissipador
**completamente positivo** e a decoerência escala **∝Δx²** (localização tipo SR/CSL).
Combinada com **FD2** (que deu a escala de LARGURA σ_x⁻²), reconstrói a taxa de
localização COMPLETA da SR Γ_dec∝(Δx/σ_x)² a partir do operador causal — os dois eixos.
**Duas ressalvas pré-registradas (forma sim, mecanismo/escala não):**
1. **CP exige a continuação Euclidiana** — o operador Lorentziano com sinal é
   fortemente não-CP (taxa de canal −1.000); a positividade é uma **escolha de
   continuação** (a mesma de c5/e10), não automática do operador causal.
2. **Δx² é a resposta genérica de ordem-líder** (como o σ⁻² de FD2 é genérico-Laplaciano):
   a amplitude (rel_var 0.05–3.26) **não é universal** — depende de σ e da proximidade da
   borda; o EXPOENTE q≈2 é robusto, o PREFATOR não. Forma SR, não mecanismo SR-específico.

Resultado **mais forte que a previsão pré-registrada** (eu previa PARCIAL/plano por
translação-covariância; a resposta quadrática finita-volume superou a previsão — valor da
pré-registração: o dado derrubou o prior). `fs1_lindblad.py` / `fs1_lindblad.json`.

### Saldo das alavancas
- **FS2 (RMT):** SOBREVIVE — espectro causal = Dyson Brownian Motion (GOE), positivo
  estrutural. A repulsão de Wigner-Dyson da SR está em TEIC.
- **FS1 (Lindblad):** SOBREVIVE em forma — gerador CP (via continuação Euclidiana) +
  decoerência ∝Δx²; com FD2 (σ⁻²) reconstrói Γ_dec∝(Δx/σ_x)² da SR. Mecanismo/escala
  externos (continuação + amplitude não-universal).
- **Padrão da campanha confirmado:** o que é **forma** emerge (saturação χ_eff; assinatura
  σ⁻²; Δx²; estatística GOE; gerador CP); o que é **escala/mecanismo absoluto** não
  (seta MORTA; η MORTO; ℏ/Γ externos) — idêntico à fronteira forma/escala do programa
  inteiro (PROGRAM_AUDIT §2).
