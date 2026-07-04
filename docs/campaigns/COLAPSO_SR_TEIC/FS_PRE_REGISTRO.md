# PRÉ-REGISTRO — FS1 (ponte de Lindblad) + FS2 (Dyson Brownian / RMT)

> **Escrito ANTES de rodar qualquer simulação.** Extensão da campanha
> `COLAPSO_SR_TEIC` — as duas "alavancas que a SR oferece" registradas em
> `TEIC/FUTURE_EXPERIMENTS.md`. Os kill-criteria abaixo são definitivos; os números
> não serão alterados depois de ver o resultado. Congelado em 2026-06-22.
>
> Sequência de dependência: EXP1 sobreviveu (saturação emerge); EXP2 morto (seta
> imposta); FD1 morto (η não emerge robusto); FD2 = Classe A (assinatura SR-like
> σ_x⁻², com ressalva genérico-Laplaciano). FS1 e FS2 são as DUAS lentes restantes que
> a SR (`SR_v7_full-38.pdf`, §9.2 Dyson; §4 Lindblad) oferece e que TEIC nunca conectou.

---

## 0. O que a SR afirma (extraído fielmente, para não inventar alvo)

| objeto SR | afirmação no paper | onde |
|---|---|---|
| **Lindblad** | no limite contínuo, eq. mestra de Lindblad com operador de colapso L̂ = x̂/σ_x e taxa γ₀=4Gm²/(ℏd) | §4, Eq. (65) |
| **decoerência ∝ separação²** | taxa de localização Γ_dec(Δx) ∝ (Δx)²/σ_x² (assinatura universal de modelos de localização CSL/GRW/DP no limite de pequena separação) | §3.3, Tab. §7 |
| **Dyson Brownian Motion** | o ruído espectral da rede é EXATAMENTE um DBM: repulsão de autovalores 2Γ/(λ_k−λ_j); distribuição estacionária → d_s≈2 (UV) | §9.2 (novidade v7/v8 #2) |
| **RMT (linhagem)** | SR é em parte Random Matrix Theory (Dyson) + Tomita–Takesaki | Linhagem |

**Leitura honesta da fonte ANTES de medir:** a SR DERIVA o DBM (repulsão) como
propriedade do espectro do grafo. Para TEIC a questão é se o espectro do operador
causal *já validado* (adjacência de colapso / d'Alembertiano BD) **exibe** essa
repulsão (assinatura de caos quântico / gás de Coulomb de Dyson, classe GOE por ser
real-simétrico) ou **não** (espaçamento Poissoniano = espectro integrável/localizado).

---

## 1. Disciplina herdada (vinculante, idêntica a PRE_REGISTRO.md)

- Reusar engines validados (`sr_teic_core`, `c5_core`, `tier3_core`). NÃO reimplementar
  a rede causal. FS adiciona só **observáveis de análise espectral** por cima.
- **Anti-circularidade (CRÍTICO):**
  - **ZERO** parâmetros novos ajustados para fabricar colapso/repulsão.
  - **Seta NÃO injetada** (EXP2 morto): o dissipador de FS1 é construído do operador
    causal MEDIDO; a irreversibilidade não é manufaturada escolhendo direção de poda.
  - **Escala absoluta NÃO reivindicada:** mede-se FORMA — o EXPOENTE em Δx, a CLASSE de
    espaçamento (GOE/Poisson), o SINAL da positividade (CP sim/não). γ₀, ℏ, G, σ_x⁻²
    absolutos permanecem externos (cf. coluna C do PROGRAM_AUDIT).
  - **L = operador causal medido**, NÃO o L̂=x̂/σ_x postulado pela SR. A ponte sobrevive
    só se o operador da rede (não inserido à mão) reproduz a forma SR.
- Seeds fixas registradas. CPU local. Resultado primeiro, narrativa depois.
- **Morte pré-registrada é DEFINITIVA.** Sobrevivência marginal → ceticismo no passo
  seguinte. NÃO escrever paper; resultado → `RESEARCH_MAP.md` da campanha.

---

## 2. FS2 — Dyson Brownian Motion / Random Matrix Theory  *(roda PRIMEIRO; barato)*

**Pergunta.** A dinâmica espectral da rede causal é um Dyson Brownian Motion (repulsão
de autovalores tipo RMT), como a SR deriva — dando uma lei para a flutuação de χ_eff que
TEIC mede mas nunca conectou à Random Matrix Theory?

**Observável (estatística de espaçamento de níveis, SEM unfolding — robusto).**
Para o espectro ORDENADO {λ_i} de cada operador causal real-simétrico, espaçamentos
s_n = λ_{n+1} − λ_n, e a **razão de espaçamentos consecutivos** (Atas–Bohigas–Giraud–Le
Doussal–Roux, PRL 110, 084101, 2013):
```
r_n = min(s_n, s_{n-1}) / max(s_n, s_{n-1}),   ⟨r⟩ = média no bulk
```
Referências teóricas EXATAS (fixadas a priori; ⟨r⟩ é unfolding-free):
- **Poisson (integrável, sem repulsão):**  ⟨r⟩ = 2 ln 2 − 1 = **0.38629**
- **GOE (caótico, repulsão real-simétrica):** ⟨r⟩ = **0.5307**

**Operadores testados** (todos reais-simétricos ⇒ classe GOE se caóticos):
1. **A_sym** — adjacência causal simetrizada (operador de COLAPSO de SR, PRIMÁRIO).
2. **L_link** — Laplaciano dos links de Hasse (setor de geometria).
3. **M_BD** — d'Alembertiano causal suavizado, espectro COM SINAL (reconstruído da
   matriz de `c5`, não o `|λ|` de `bd_operator_eigs`).

**Protocolo.** dim ∈ {2,4}; N ∈ {100, 200, 400}; ≥ 12 seeds. Bulk = descartar os 10%
externos do espectro (bordas). Degenerescências exatas (s=0) são contadas e reportadas
(inflam Poisson artificialmente; se houver multiplicidade estrutural, reportar ⟨r⟩ com e
sem o bloco degenerado). Secundário: histograma P(s) unfolded (média local) — checar
repulsão P(s→0)→0 (GOE) vs P(0) finito (Poisson).

**KILL-CRITERION (verificado contra número, no operador PRIMÁRIO A_sym).**
```
MORTE        se ⟨r⟩ ≤ 0.42 (consistente com Poisson 0.386, longe de GOE), estável em N
             → espectro causal SEM repulsão de Dyson; NÃO é um DBM/RMT; a alavanca
             RMT da SR não está contida no espectro de TEIC.
SOBREVIVE    se ⟨r⟩ ≥ 0.50 (consistente com GOE 0.5307), N-estável (deriva |Δ⟨r⟩|<0.03
             entre N) e robusto a seeds → repulsão de autovalores = Dyson Brownian
             Motion confirmado no operador causal, como a SR deriva.
INTERMEDIÁRIO  0.42 < ⟨r⟩ < 0.50 → registrar o número (semi-Poisson / espectro misto),
             sem reivindicar nem RMT nem integrável.
```
**Previsão honesta (registrada antes de medir).** Tensão genuína: o limite contínuo do
M_BD é o d'Alembertiano LOCAL (□), cujo espectro num diamante é SEPARÁVEL/integrável →
empurra para Poisson; mas a desordem do sprinkling de Poisson injeta aleatoriedade →
empurra para GOE. Não tenho previsão forte; é por isso que o teste é revelador. A_sym
(grafo causal denso, ⟨deg⟩∝N) tende mais a GOE que o M_BD local.

---

## 3. FS1 — Ponte de Lindblad  *(roda depois; depende conceitualmente de FD2)*

**Pergunta.** A saturação espectral de TEIC se conecta a uma equação mestra de Lindblad
(L̂=x̂/σ_x na SR), dando dinâmica de decoerência REAL e não só um parâmetro de ordem
estático — gerador POSITIVO (CP) e taxa de decoerência ∝ separação²?

### FS1-A — Positividade (o gerador é de Lindblad/CP?)
Para o operador causal usado como operador de Lindblad L (Hermitiano), o dissipador
`D[ρ] = LρL − ½{L²,ρ}` é CP por construção sse as TAXAS de canal forem ≥ 0. Decompõe-se
o gerador causal em canais (autovalores do operador) e conta-se canais de taxa negativa
para DUAS continuações:
- **(i) Lorentziana** — espectro COM SINAL do M_BD (autovalores podem ser negativos);
- **(ii) Euclidiana** — `|λ|` (a continuação VALIDADA em c5/e10).

CP ⇔ zero taxas negativas (tolerância: |λ_neg| > 1% de λ_max, estável em seeds/N, conta
como negativo físico — abaixo disso é ruído numérico).

```
KILL-A: MORTE se NENHUMA continuação dá gerador CP (ambas têm taxa negativa O(1)
        robusta) → o operador causal não gera Lindblad positivo.
        SOBREVIVE se ≥1 continuação é CP. Registrar SE a CP exige a continuação
        Euclidiana (= a positividade é uma ESCOLHA de continuação, não automática do
        operador causal Lorentziano) — distinção honesta, não morte.
```

### FS1-B — Lei de decoerência ∝ separação² (taxa de localização)
Dois modos gaussianos espaciais ψ₁, ψ₂ (largura σ_x fixa, mesma construção de FD2
`spatial_mode`, centros separados por Δx ao longo de um eixo espacial). Taxa de
decoerência da coerência ρ₁₂ sob o dissipador de Lindblad de um operador Hermitiano L
(γ=1), fórmula EXATA do decaimento do elemento off-diagonal:
```
Γ_dec(Δx) = ½⟨ψ₁|L²|ψ₁⟩ + ½⟨ψ₂|L²|ψ₂⟩ − ⟨ψ₁|L|ψ₁⟩⟨ψ₂|L|ψ₂⟩
```
L = M_BD (primário) e A_sym. Varre-se Δx ∈ [espaçamento, ~½ sistema]; subtrai-se a linha
de base Γ₀=Γ_dec(Δx→0) (= variância do modo, a parte de FD2); ajusta-se a parte induzida
ΔΓ(Δx)=Γ_dec(Δx)−Γ₀ a uma potência ΔΓ ∝ Δx^q. dim∈{2,4}, N=400, ≥10 seeds.

```
KILL-B (lei de separação²):
MORTE        se q ∉ [1.7, 2.3], OU não há lei de potência limpa (R² < 0.80), OU ΔΓ é
             plana (|ΔΓ|/Γ₀ < 5% em toda a janela) → a taxa NÃO escala como separação²;
             o operador causal não localiza em posição como o L̂=x̂/σ_x da SR.
SOBREVIVE    se q ∈ [1.7, 2.3] com R² ≥ 0.90, robusto em σ_x, dim e seeds → decoerência
             ∝ Δx², a assinatura de localização de SR/CSL emerge do operador causal.
```

**KILL-CRITERION GERAL de FS1 (como em FUTURE_EXPERIMENTS):**
```
MORTE de FS1 se (A) nenhuma continuação dá gerador CP, OU (B) a taxa não escala ∝Δx².
SOBREVIVE se gerador CP (FS1-A) E decoerência ∝Δx² (FS1-B).
PARCIAL/B se um lado passa e o outro não (registrar exatamente qual).
```
**Previsão honesta (registrada antes de medir).** O operador causal é
translação-covariante (□ no contínuo) — não acopla à posição ABSOLUTA. Espero portanto:
FS1-A provavelmente CP só na continuação Euclidiana (positividade = escolha); FS1-B com
risco real de morte (ΔΓ plana em Δx, porque □ é cego à separação absoluta — a mesma lição
de E1-3/E2/HQ2: o operador causal propaga, não localiza). FD2 achou σ_x⁻² (escala de
LARGURA, genérica-Laplaciano); FS1-B testa o eixo COMPLEMENTAR (separação). Resultado
mais provável: **PARCIAL** — a ponte de Lindblad fecha na largura (σ⁻²) mas não na
posição (Δx²), porque a coleta causal é □ e não x̂. Pré-registro para que esse desfecho
conte como resultado honesto, não como ajuste.

---

## 4. Saída
- `fs_core.py` (helpers de análise; importa `sr_teic_core`/`c5_core`, não reimplementa rede).
- `fs2_rmt.py` → `fs2_rmt.json`; `fs1_lindblad.py` → `fs1_lindblad.json`.
- Vereditos → `RESEARCH_MAP.md` (campanha) + tabela de prioridades em FUTURE_EXPERIMENTS.
- Morte/parcial é resultado válido. Nada de ajuste para escapar de morte.
