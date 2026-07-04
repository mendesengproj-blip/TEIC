# PRÉ-REGISTRO — CAMPANHA_COLAPSO_SR_TEIC

> **Escrito ANTES de rodar qualquer simulação**, depois de ler o paper-fonte
> (`SR_v7_full-38.pdf`, Zambuzi, v8 "Fisher Action, Dyson Convergence,
> Thermodynamic Cycle"). Os números dos kill-criteria abaixo são definitivos.
> Não serão alterados depois de ver o resultado. Congelado em 2026-06-21.

---

## 0. O que diz a fonte (extraído fielmente do paper SR, para não inventar alvo)

| objeto SR | definição no paper | onde |
|---|---|---|
| **χ_eff (colapso)** | `λ_max(A)/N`, A = matriz de **adjacência** simétrica do grafo de emaranhamento | Eq. (9), Listing 2, "Definitional note" p.8 |
| **χ_eff (geometria)** | `λ_max(L)/N`, L = Laplaciano (setor d_s, separado) | §2.1, "Definitional note" |
| natureza de χ_eff | **concentração relacional / dominância global** (hub *ou* all-to-all), **NÃO densidade**; Corr(χ,k_max)=0.88 | Remark 3 |
| grafo de emaranhamento | `w_ij = \|⟨σ_z^i σ_z^j⟩ − ⟨σ_z^i⟩⟨σ_z^j⟩\|`; GHZ→K_N (χ→1), Bell→arestas isoladas (χ=1/N) | Eq. (79–81) |
| **gatilho de colapso** | dispara quando **χ_eff ≥ η** | Eq. (88) |
| **colapso = perda de rigidez espectral** | gap Δλ = λ_max − λ₂; NÃO é fragmentação (GHZ mantém G_f=G_i=N) | Eq. (170), §9.2 |
| **η** | `sup_D S_rel/(A/4Gℏ)` (Casini); ≈ **0.1** macroscópico, **0.99** NISQ; derivação 1º-princípios ABERTA | §5.1, Remark 22 |
| percolação | `p_c·N = −ln(1−√η)/√η ≈ 1+√η`; p_c(cúbica,liga)=**0.2488**, p_c(quadrada)=1/2 | Eq. (96), Remark 27 |
| poda | `Γ(x)=γ₀/x`, x=1−χ (diverge na saturação); restauração λ_q; poda sozinha fragmenta (d_s→0) | §3.5, §1 |
| **seta do tempo** | "a 4ª dimensão (tempo) emerge da estrutura causal imposta pela **poda irreversível** da SR" — **problema aberto** | §2.1 "3→4 step" |
| assinatura espacial | **σ_x⁻²** (SR) vs σ_x⁻³ (CSL) vs flat (Diósi–Penrose); Γ_SR=Gm²/(4ℏσ_x²) | §3.3, Eq. (65) |
| discriminador GHZ/Bell | **τ_Bell/τ_GHZ ~ N²** (Path B, nativa); N=32,η=0.99→≈5569 | Teorema 1, Eq. (86) |
| avalanches | GHZ ⟨s⟩≈5–6, s_max=N; Bell ⟨s⟩≈2; P(s)~s^{−τ}, τ≈2.05 (3D) ou 3/2 (ER) | Eq. (168–171) |

**Linhagem (define onde procurar):** TEIC herda de Causal Set Theory (Sorkin):
eventos discretos, ordem causal de Hasse, sprinkling de Poisson, Lorentz emergente.
SR realiza-se como **rede cúbica simples** (folhas 2D empilhadas a ℓ_P) com um
**grafo de emaranhamento quântico** por cima. A diferença estrutural-chave: em SR a
seta do tempo é IMPOSTA pela poda irreversível (aberto); em TEIC a ordem parcial de
Hasse já É a seta (estrutural). É exatamente isso que EXP 2 testa.

---

## 1. Definições operacionais da campanha

### 1.1 "EMERGIR" (a ponte SOBREVIVE naquele ponto)
χ_eff de saturação, a seta do tempo e o limiar η devem aparecer usando **apenas**:
- a rede causal de TEIC já validada (sprinkling de Poisson no diamante causal de
  Minkowski + ordem de Hasse / matriz ancestral) — `causal_core.py`, `tier3_core.py`;
- os operadores espectrais **já validados** — matriz causal ancestral e o
  d'Alembertiano causal suavizado de Sorkin/Benincasa–Dowker (`c5_core.py`, e10);
- **ZERO** parâmetros novos ajustados para produzir colapso.

### 1.2 "COLOCAR" (a ponte MORRE naquele ponto)
Se em qualquer experimento for necessário injetar um η a posteriori, OU adicionar
poda Γ=γ₀/(1−χ) não derivada da dinâmica causal, OU impor a seta do tempo
escolhendo à mão a direção de pruning → o colapso é declarado **EXTERNO** ali.

### 1.3 Hipótese nula declarada
> "O colapso NÃO emerge da rede causal de TEIC; χ_eff permanece sub-crítico, ou a
> saturação/transição/irreversibilidade exige ingrediente imposto." A campanha tenta
> REJEITAR a nula e relata honestamente se não conseguir.

### 1.4 Ordens-parâmetro medidos (NÃO impostos) — definição SR-fiel
Para cada rede causal de N eventos mede-se:

| símbolo | definição | operador | papel em SR |
|---|---|---|---|
| **χ_A**  | λ_max(A_sym)/N | matriz causal ancestral simetrizada A∨Aᵀ | **operador de COLAPSO (primário)** |
| **χ_L**  | λ_max(L_link)/N | Laplaciano dos links de Hasse | setor de geometria |
| **χ_BD** | λ_max(\|M_BD\|)/N | d'Alembertiano causal suavizado (validado) | operador causal local |
| **R**    | (λ_max − λ₂)/λ_max do operador de colapso | gap espectral normalizado | **rigidez espectral** (o que colapsa em SR) |

Seeds fixas registradas. CPU local, N ≤ 500. dim ∈ {2, 4}.

---

## 2. EXPERIMENTO 1 — Saturação espontânea (teste de morte precoce)

**Pergunta.** Rodando a rede causal SEM critério de colapso embutido, χ_eff atinge
regime de saturação por conta própria conforme a rede cresce em ordem causal?

**Protocolo.** Sprinkle de N eventos no diamante causal (dim 2 e 4). A "evolução sob
a dinâmica causal própria" = adicionar eventos em ordem de tempo de Hasse (prefixos
n = 10%…100% de N — a ordem de crescimento causal sequencial de CST). Para cada
prefixo medir χ_A, χ_L, χ_BD (=λ_max/n) e a rigidez R. Varrer N = 50, 100, 200, 500;
≥ 8 seeds cada. (Comparar com SR: ER → χ≈p; GHZ/clique → χ→1; Bell → χ→0.)

**Teste de platô (operacional).** χ_eff "satura" se, na cauda (n de 0.6·N a N):
- deriva relativa |χ(N) − χ(0.6N)| / χ(0.6N) < **0.10**, **E**
- valor de platô N-estável: |χ̄(500) − χ̄(200)| / χ̄(200) < **0.15**, **E**
- não-trivialidade: χ_platô > **2/N** (acima do piso difuso 1/N de SR Bell).

**KILL-CRITERION (verificado contra número).**
```
MORTE  se NENHUMA das ordens-parâmetro (χ_A, χ_L, χ_BD) satisfaz o teste de platô
       em NENHUM N — todas crescem >10% por duplicação na cauda, OU ficam no piso
       de ruído (χ < 2/N) sem estrutura.
SOBREVIVE se ≥1 ordem-parâmetro satura (cauda <10%, N-estável <15%, χ_platô>2/N)
       em ≥1 escala N, SEM limiar injetado.
SOBREVIVE MARGINALMENTE se satura só em 1 das 3, só na maior N, ou com deriva 8–10%.
```

---

## 3. EXPERIMENTO 2 — A seta do tempo é derivada ou imposta?
*(só roda se EXP 1 sobreviver)*

**Pergunta.** A irreversibilidade emerge da ordem de Hasse, ou tem de ser escolhida
à mão (como SR faz na poda irreversível, seu "3→4 step" aberto)?

**Protocolo.**
1. Produção de "entropia" estrutural σ(n) = d/dn[−Σ pᵢ ln pᵢ], pᵢ=λᵢ/Σλ do operador
   de colapso (proxy de ∇·j>0), na rede crescendo em ordem de Hasse, SEM impor poda.
2. **Reversão temporal**: rodar o crescimento "para trás" (remover eventos do futuro
   causal) e comparar trajetórias χ(n) e σ(n) forward vs backward. Estatística:
   D_TR = |⟨X_fwd⟩ − ⟨X_bwd⟩| / SEM_combinado por n.
3. Assimetria intrínseca de Hasse: distribuição de in-degree (passado) vs out-degree
   (futuro) por evento; razão de "irreversibilidade" da ordem parcial.

**KILL-CRITERION.**
```
MORTE  se a dinâmica de χ_eff é estatisticamente simétrica sob reversão temporal
       (D_TR < 3 em TODOS os n) E a distribuição in/out-degree é simétrica,
       OU se for preciso escolher manualmente a direção de pruning. Seta = INPUT.
SOBREVIVE se a ordem de Hasse impõe assimetria mensurável (D_TR ≥ 3 numa fração
       robusta dos n, estável sob seeds) SEM escolha externa de direção.
```
*(Nota: SR declara este passo aberto/imposto; se TEIC sobrevive, é vantagem de TEIC.)*

---

## 4. EXPERIMENTO 3 — η emerge ou é calibrado?
*(só roda se EXP 1 e 2 sobreviverem — teste mais duro)*

**Pergunta.** O limiar η tem valor NATURAL na rede causal, ou é livre (como SR admite)?

**Protocolo.**
1. Procurar transição de fase espontânea varrendo um controle interno (densidade ρ
   via N no diamante; e/ou o acoplamento J do ferromagneto causal de FLB). Detectar
   onde o comportamento muda qualitativamente: (a) percolação do gigante componente
   do grafo de links; (b) **pico de susceptibilidade** dχ/d(controle); (c) salto da
   rigidez espectral R (o sinal de colapso da própria SR).
2. **Anti-circularidade (CRÍTICO).** Medir η_emergente CEGO: o detector usa só
   critério interno (inflexão/percolação/pico de susceptibilidade). Comparar com SR
   (0.1, 0.99) e pc=0.2488 **só depois** de registrar o medido. O prompt já expôs
   esses números → a comparação é **pós-dição**, registrada como tal, não predição.
3. **Robustez ±10%.** Variar ±10% a ação microscópica (peso BD eps; e J) e ver se
   η_emergente é estável.

**KILL-CRITERION.**
```
MORTE  se não há valor natural de transição — χ_eff(controle) varia suavemente sem
       ponto crítico (susceptibilidade sem pico ≥ 2× o fundo), OU o "η emergente"
       muda > ±20% sob a variação ±10% da ação. η é parâmetro livre; o colapso de SR
       não está contido em TEIC.
SOBREVIVE se há η_emergente robusto (estável <±20% sob ação ±10%) como transição
       natural, medido cegamente, com pico de susceptibilidade ≥ 2× o fundo.
```

---

## 5. EXPERIMENTO 4 — Discriminação de linhagem (SR / CSL / DP / novo?)
*(só roda se EXP 1–3 sobreviverem; CLASSIFICATÓRIO, sem morte)*

**Pergunta.** Se o colapso emerge, qual a assinatura: σ_x⁻² (SR), σ_x⁻³ (CSL),
flat (Diósi–Penrose), ou nova?

**Protocolo.** Preparar análogos de superposição espacial de largura de coerência
σ_x variável na rede causal (perturbação localizada do modo espectral dominante de
largura σ_x); medir a taxa de relaxação Γ(σ_x) do modo (taxa de poda implícita pela
rigidez). Ajustar expoente p em Γ ∝ σ_x^p. Medir também τ_Bell/τ_GHZ vs N construindo
os grafos de emaranhamento GHZ (K_N) e Bell na MESMA rede e aplicando o gatilho χ≥η.

**Classificação (sem kill).**
```
A: p ≈ −2  → assinatura SR. Unificação específica (mais forte p/ ponte).
B: p ≈ −3 ou flat → colapso tipo CSL/DP. TEIC tem colapso próprio.
C: p novo (≠ −2, −3, flat) → classe NOVA. Resultado mais original.
Registrar qual, com incerteza estatística e o expoente de τ_Bell/τ_GHZ.
```

---

## 6. Disciplina de execução (vinculante)
- Reusar engines validados (`causal_core`, `tier3_core`, `c5_core`, `su3_core`).
  NÃO reimplementar a rede do zero (evita colapso acidental no código novo).
- Seeds fixas registradas. Cada kill-criterion verificado contra o NÚMERO acima.
- Resultado primeiro, narrativa depois, em `RESEARCH_MAP.md`.
- Morte pré-registrada é DEFINITIVA. Não reabrir experimento morto com parâmetros
  novos. Sobrevivência marginal → ceticismo no passo seguinte.
- NÃO escrever paper. Resultado → `RESEARCH_MAP.md`, aguarda acumulação.
