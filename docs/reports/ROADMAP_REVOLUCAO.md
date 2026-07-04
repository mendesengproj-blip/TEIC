# ROADMAP_REVOLUCAO — da teoria interessante à teoria revolucionária

> Mapa de ataques em resposta à crítica de revisor (jun/2026): *"onde a teoria faz uma
> previsão que nenhuma teoria atual faz?"*. Cada ataque tem o que já existe no repo,
> o experimento concreto, o critério de morte e o esforço. Regra do projeto mantida:
> **nada é forçado; negativo é reportado como negativo; kill criteria pré-registrados.**

---

## 0. Diagnóstico

As 10 perguntas do revisor **já têm resposta honesta dentro do repo** — quase todas
"é entrada externa". O déficit é de **exclusividade**, não de rigor:

| Pergunta do revisor | Estado real no repo | Onde |
|---|---|---|
| Q1 Por que Poisson? | Axioma — mas R1 *mede* que grade regular falha (CV 17% vs 0.8%); Poisson é a única discretização LI (teorema BHS) | R1; `paper_I` §3 |
| Q2 Por que 3+1? | Entrada pura — evidência dispersa de que d=3 é especial (Ataque 2) | Open Questions (2) |
| Q3 Previsão observacional? | Existe e está enterrada: `Δlog v_flat = ¼ log[H(z)/H₀]` | `FALSIFICATION_BTFR_V2.md` |
| Q4 Diferença vs RG? | Geometria = CST = RG no contínuo; LIV O(1) no setor vetorial **não resolvida** (ameaça) | §13(9) |
| Q5 MOND inevitável? | Compatível, não inevitável — X₀∝ρ é UV; a₀∼cH não suportado (C3) | nota `paper_I` |
| Q6 Skyrme derivado? | Escolhido — vem do comutador do grupo mas "not derived" | `paper_II` §V.F |
| Q7 Por que SU(2)? | Semi-derivado: V4 provou U(1) insuficiente; SU(2) = mínimo com π₃=ℤ — falta formalizar | `PHI_EMERGE_V4` |
| Q8 Quantização fundamental? | Efetiva (ANW externo) | `paper_II` §VII |
| Q9 Regra de Born? | Não tentada; "dois andares" | e6–e11 |
| Q10 Previsão mais arriscada? | Existe (BTFR) mas não enquadrada como tal | idem Q3 |

A pergunta central — *"por que esta formulação se coincide com CST?"* — só ganha resposta
forte com resultados que a CST não tem. A CST **não tem setor de matéria nem ponte para
gravitação modificada**; é aí que os ataques se concentram.

---

## TIER 1 — viável agora, código existente, alto retorno

### Ataque 1 ⭐ — derivar o termo de Skyrme do coarse-graining SU(2)
**Status: ✅ EXECUTADO — `BRIDGE_SU2_COEFF.md`, veredito B (pré-registrado).**
O OPERADOR de Skyrme emerge da isotropia de Poisson (razão 5/9 confirmada a 0.06%;
grade cúbica exatamente cega; c_K=+a⁴/2880; λ_Sk=a/√120 = granularidade); a
DOMINÂNCIA não emerge (K≤⅔S trava o quártico líquido negativo; SC4 sem mínimo
interior). Paper II: 3 → 2 ingredientes. Liga Q1→Q6: Poisson gera o estabilizador.

O Paper I fez isso para U(1): plaqueta → F² com corr 1.0000 (W1–W2). O análogo SU(2)
nunca foi rodado. Em modelos quirais de rede, a ordem seguinte da expansão da ação de
Wilson não-abeliana gera precisamente um quártico tipo Skyrme — com coeficiente fixado
pela granularidade, não livre. Infraestrutura pronta (`su2_core`, 4 gates).

- **Se fechar:** Paper II passa de "3 ingredientes importados" para "1 (o grupo — e o
  grupo é forçado por minimalidade, Ataque 5)". Se o coeficiente depender do mesmo K
  de G∝1/K → **relação cruzada sem parâmetros livres** entre matéria e gravitação.
- **Morte:** o quártico emergente é o simétrico (A+∂θ)⁴, não o comutador |c_i×c_j|².
- **Risco:** a parede de ruído ρ^(3/4). Mitigação: campo constante primeiro (como W1).

### Ataque 2 — d=3+1 por exclusão estrutural (Nível 1 parcial do revisor)
**Status: ✅ EXECUTADO — `DIMENSION_SCAN.md`, veredito A.**
Perfil p=−(d−2) medido sem ansatz (d=1..4); d=2 prende tudo, d=4 não orbita nada,
d=3 único com ligado+escape; janela de Derrick = {3}; barreira π₃ medida (B salta,
pico ×1.86 sob refino) vs desenrolamento suave em 2D. Q2: "entrada pura" → "única
dimensão consistente" (atrator dinâmico segue Tier 3).

Evidência dispersa já existente: 1+1D sem monopólos/corda (CR_WILSON) e ponte preferindo
perfil blindado, não 1/r; 3+1D com plasma + lei de área + 1/r + sóliton estável. Falta:
rodar D3 (gravitação) e Derrick/sóliton em **d=2,4,5** (operadores BD generalizam em
qualquer d — Dowker–Glaser). Conjectura testável: **d=3 é a única dimensão com gravidade
de longo alcance não-confinante E matéria topológica pontual estável.**

- **Se fechar:** Q2 vira seleção por consistência (não atrator dinâmico — dizer isso).
- **Morte:** d=4 também funcionar em ambos os testes.
- **Esforço:** re-rodar campanhas existentes com d parametrizado.

### Ataque 3 — mapa operadores-proibidos ↔ exclusões observacionais
**Status: ✅ EXECUTADO — `PREDICTIONS.md` / `results/predictions/OP1_operator_map.md`**

A rede proíbe (§9.5) precisamente as classes que a observação executou: Horndeski
G₄ₓ/G₅ (soldering) ⟷ GW170817 |c_g/c−1|≤5×10⁻¹⁶; frame preferencial n^μ ⟷
Fermi-LAT E_QG,1>7.6 E_Pl; e R1 (grade falha LI a 17%) é a contraparte microscópica
da exclusão observacional de discretização regular. O conjunto selecionado
{P(X)/DBI, Stückelberg, Proca, Maxwell} sobrevive a c_T=c por acoplamento mínimo.

### Ataque 4 — promover a previsão arriscada (Q3+Q4+Q10)
**Status: ✅ EXECUTADO — `PREDICTIONS.md` / `results/predictions/F1_forecast.*`**

Forecast quantitativo do teste decisivo: em que z, com quantas galáxias e que piso
sistemático a previsão `Δlog v=¼log[H/H₀]` se separa de ΛCDM (=0). Resultado: o gargalo
é **sistemático, não estatístico** — com σ_sys=0.04 dex o teste satura em ~1.6σ em z=1
(exatamente a tensão tentativa de F_JWST); a decisão exige **z≳2 e σ_sys≲0.03 dex**,
onde ~10–25 rotadores ricos em gás bastam. Kill criterion pré-registrado no documento.
Segunda previsão (grátis, herdada da LI de Poisson): **dispersão de fótons exatamente
nula na média** — distingue de LQG/Hořava.

---

## TIER 2 — bem-posto, risco médio, meses

### Ataque 5 — teorema de minimalidade de SU(2) (Q7)
**Status: ✅ EXECUTADO — `MINIMALITY_SU2.md`, cadeia fechada.**
MIN1: cegueira de U(1) é UNIVERSAL (custo de núcleo = 0 exato para qualquer
harmônico/série — loophole de V4 fechado; B é índice de volume, imune). MIN2:
grupos discretos colapsam B (0.96→0.05) e viram paredes (E∝1/dx medido). MIN3:
cadeia escalar→discretos→U(1)→SU(2) com cada elo medido; acima de SU(2) nada é
necessário (Bott). Q7: "a estrutura escolheu, não o pesquisador."

### Ataque 6 — relações cruzadas sem parâmetros (a versão realista de "derivar G")
**Status: ✅ EXECUTADO (primeira relação) — `CROSS_RELATIONS.md`, veredito B.**
G_net·ρ²·r_c⁵ → 15/8π² confirmado a 2.5% no limite assintótico (morte literal em
grau baixo disparou e está reportada; correção O(1/deg) com b≈0.85 medido).
Relação cruzada gravitação↔matéria: G_net·ρ²·r_c³·λ²_Sk = 3/320π² — zero
parâmetros. Próximo elo: constantes puras de m_A e X₀ na mesma rede.

### Ataque 7 — FR por troca de dois Skyrmions (degrau honesto rumo ao Nível 4)
**Status: ✅ EXECUTADO — `MATTER_FR_EXCHANGE.md`.**
As três premissas mecânicas do FR medidas: loop de troca fecha (e^{−d/2}, razões
2.78/2.81; B e E conservados), troca = meia-volta rígida ∘ isospin global (erro
0.0 exato), e rotação 2π arrasta a coordenada coletiva ao antípoda (7e-16; W=1 —
o invariante de SU2_QUANT). Importado restante: só o passo de homotopia π₁
(FR 1968; Williams 1970) + a quantização. Fronteira estreitada, não cruzada.
Continuação natural: computar π₁(config B=2) na rede (aparato pronto).

### Ataque 8 — Λ "sempre-presente" com coeficiente medido
**Status: ✅ EXECUTADO — `LAMBDA_EVERPRESENT.md`.**
L1: δρ/ρ=1/√(ρV) coeficiente 0.971±0.05 (200 sementes). L2: fonte uniforme →
de Sitter estático puro (R²=0.9999) com β a 0.3% da calibração CR1b (3º uso da
mesma constante de transporte — loop fechado). L3: magnitude 10⁻¹²² e sinal
flutuante = herança CST (Sorkin; ADGS 2004), citada como tal. A contribuição
própria: os coeficientes medidos; o elo dinâmico (evolução temporal) fica aberto.

---

## TIER 3 — apostas revolucionárias (alto risco; kill criteria antes de abrir)

- **Poisson dinâmico (Q1):** e7 já validado (Bell-causal até N=7). Alvo intermediário
  mensurável: o crescimento ponderado-por-encontros **suprime posets KR** e estabiliza
  a dimensão MM? Qualquer progresso é citável pela comunidade CST inteira.
- **d=3+1 como atrator dinâmico (Nível 1 completo):** dimensão MM de causets *crescidos*
  pelo e7 vs N. Probabilidade baixa, custo moderado (infra existe).
- **ℏ como granularidade (reabrir Nível 3 por outra porta):** e11 fechou "ℏ da geometria"
  — respeitar. Conexão nunca testada entre dois resultados existentes: CC (massa = custo
  causal ∝ N) + e11 (k = θ₀√ρ). Teste: a escala de fase de uma estrutura de complexidade
  N escala como N? (k∝N ⟺ k∝m ⇒ ℏ = constante de conversão = granularidade.)
  **Morte:** k independente de N.

---

## NÃO FORÇAR — negativos fechados (o repo já pagou para sabê-los)

1. **ℏ da geometria pura** — e11, expoente −0.57 medido. Fechado.
2. **a₀∼cH de X₀** — C3: X₀∝ρ é UV. Fechado (manter a nota "coincidência dimensional").
3. **Regra de Born (Q9)** — fora do alcance; rota legítima = medida quântica de Sorkin
   sobre histórias causais (programa de anos). Resposta de paper: "dois andares".
4. **Ponte vetorial dilatônica** — negativo documentado (`docs/DEV_bridge_future.md`).

## OBRIGAÇÃO DE SOBREVIVÊNCIA (paralela a tudo)

**Status: ✅ EXECUTADA — `LIV_VECTOR.md` (LV1–LV4b), rota do observável global.**
Nenhuma LV intrínseca encontrada: toda plaqueta causal é plano tipo-tempo (e²>b²
invariante — teorema exato, LV1); o ensemble é covariante sob boost (z mediano 0.36,
LV2); o "3" é o truncamento do orbital LI pela caixa (monotônico no alcance L·ρ^¼,
curva universal, LV3); e a ação somada Σ(1−cos W) **ressoma a violação**: defeito de
boost 0.98→0.003 saindo do regime quadrático, com sensibilidade 40–54σ via seeds
pareados (a parede ρ^(3/4) não se aplica ao observável global — LV4). Aberto, com
kill honesto registrado: resíduo de ~12% no pico de sensibilidade ao campo,
independente de L (LV4b) = fração ainda-quadrática da população, controlada por
densidade ou pelo kernel BD, não por volume. A ameaça vira enunciado: **sem
referencial preferido na rede; a LV de W2 é artefato de expansão + regulador.**

---

## Sequência

1. ✅ **Ataques 3+4** (executados — `PREDICTIONS.md`).
2. **Ataque 1** (`BRIDGE_SU2_COEFF`) — maior promoção estrutural do Paper II.
3. **Ataque 2** (`DIMENSION_SCAN`) — responde Q2 no nível "muito bom".
4. **Ataques 5+6** consolidam; **7+8** são os papers seguintes; Tier 3 como exploração
   com kill criteria pré-registrados (estilo e7). **LIV vetorial em paralelo.**

## A tese, se Tiers 1–2 fecharem

> A CST não tem setor de matéria, não tem ação mínima e não prevê dinâmica galáctica.
> A TEIC deriva o conteúdo de operadores da EFT, amarra seus coeficientes à mesma
> granularidade que fixa G, seleciona d=3 por consistência, proíbe exatamente os
> operadores que GW170817 e Fermi-LAT excluíram — e morre se a evolução BTFR a alto-z
> for plana. Uma teoria com pontos vulneráveis nomeados.
