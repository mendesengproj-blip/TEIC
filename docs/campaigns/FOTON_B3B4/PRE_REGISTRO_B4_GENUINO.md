# PRÉ-REGISTRO — B4-genuíno · Bianchi-I na ORDEM causal: o setor magnético a baixa curvatura

> Campanha FOTON_B3B4 (Fase 3, Frente do Fóton). Versão fiel de B4, a última alavanca
> a baixa curvatura depois de B3b = MORTE_NOGAUGE.
> Gerado em: jun/2026. **Não executar antes da revisão do usuário.**
> Depende de: A1 (guarda verde ✓), E6c (gate isotrópico), `b3b_closure.py` (gate de gauge),
> `height_h_plaquettes`/`polygon_bivectors` (reuso verbatim).
> Posição: última porta aberta do fóton magnético a baixa curvatura.

---

## 1. Por que B4 original morreu, e o que "fiel" significa

B4 original (`b4_anisotropic.py`) = **DEATH_B4_COORD_ARTIFACT**. Pôs a anisotropia no
**embedding** (X_k = e^{H_k τ} x_k, H_1 = a·H_⊥) e manteve a **ordem causal isotrópica**
(Minkowski conforme). O controle decisivo expôs: o conteúdo magnético nos planos
**esticados** (12,13, que contêm x_1) explodiu **×6×10⁴**, enquanto o plano **não
esticado** (23) ficou **fixo ×1.00**. Isto é o fator de escala do embedding inflando
A^{1j} — **rescalar um eixo de coordenada** tilta bivetores trivialmente para ele.
Não é física; é unidade.

**O diagnóstico da própria síntese B4:** "uma B4 fiel exigiria a anisotropia na própria
ordem causal (cones de luz dependentes de direção, Bianchi-I genuíno), que quebra o
truque conformal-flat de E6c e é uma campanha maior." Este pré-registro É essa campanha.

**A mudança cirúrgica:**
- **Anisotropia entra SÓ na ORDEM causal** (quais pares são causalmente ligados),
  via cones de luz direcionais.
- **Classificação E/B fica em coordenadas planas isotrópicas** (t,x_1,x_2,x_3), o MESMO
  classificador de E6c — **nenhuma coordenada é esticada**. Logo não há fator de escala
  para inflar nada: se frac_B sobe, é porque a ordem anisotrópica **seleciona plaquetas
  diferentes** (cujas áreas planas são mais spacelike), não porque áreas foram rescaladas.

## 2. A pergunta exata

> Cones de luz direcionais (Bianchi-I genuíno na ordem causal) a baixa curvatura abrem
> o setor magnético — plaquetas de diamante B-type (b²>e²) acima do piso de E6c — e, se
> sim, essas plaquetas magnéticas formam um campo de gauge genuíno no setor de links de
> Hasse (o gate que B3b exigiu)?

B4-genuíno tem uma **vantagem estrutural sobre B3b**: as plaquetas são construídas por
`height_h_plaquettes` a partir de **caminhos de Hasse** — então, ao contrário dos
quads-de-relação de B3 (que morreram em B3b por estarem **fora** do substrato de links),
as células de B4 vivem **no** substrato de gauge por construção. O gate de gauge (Stage 2)
é, portanto, **informativo** aqui — não automático/trivial como foi em B3b.

## 3. A ordem causal anisotrópica (o único código novo)

Substrato: sprinkle de Poisson num box 4D (t, x_1, x_2, x_3), densidade ρ (= E6c).
Precedência **anisotrópica** (Bianchi-I espacialmente plano, cone dependente de direção):

```
p ≺ q   ⟺   dt > 0   E   dt² − (a²·dx_1² + dx_2² + dx_3²) > 0
```

- `a` = razão de anisotropia, **adimensional** (knob varrido: a ∈ {1, 2, 4, 8}).
- `a = 1` ⟹ Minkowski isotrópico ⟹ **reproduz E6c** (gate obrigatório).
- `a > 1` ⟹ cone **mais estreito** ao longo de x_1 (pares x_1-separados precisam de mais
  dt para conectar) ⟹ anisotropia genuína na causalidade.

Implementação: nova `causal_matrix_aniso(pts, a)` (variante de `src/causal_core.causal_matrix`,
que usa assinatura (−,+,+,+)); daí `causal_link_graph` (transitive reduction = Hasse)
e `height_h_plaquettes` **sem alteração**. O bivetor usa `polygon_bivectors(pts, V)` com
os **pts planos**, idêntico a E6c.

**Anti-circularidade:** `a` é adimensional, varrido, emerge como knob — **não** é
constante física (a guarda A1 bane literais que casam c/G/ℏ/…; `a∈{1,2,4,8}` não casa
nada). A forma `dt² − a²dx_1² − …` é o intervalo de Minkowski anisotrópico, **não** uma
fórmula de dilatação SR/GR (sem γ). Risco a verificar no Stage 0: confirmar que o
detector de dilatação da guarda não dá falso-positivo nessa linha (rotular se preciso,
como su3_core).

## 4. Protocolo (gate serial)

### Stage 0 — Reconstrução validada (gate bloqueante)

- **Gate isotrópico (a=1):** `causal_matrix_aniso(pts,1)` deve ser **byte-idêntico** a
  `causal_matrix(pts)` (assert), e frac_B(a=1) deve reproduzir E6c a baixa curvatura
  (~0.003, **< 0.01**). Se não reproduz: PARAR (construção suspeita = INVALID).
- **Self-consistência da ordem:** `causal_matrix_aniso(pts,a)` deve ser uma ordem
  parcial estrita válida (antissimétrica, transitiva) para todo a testado. Verificar
  transitividade num sub-bloco.
- **Guarda A1 verde** sobre o novo arquivo (CI) antes de qualquer medição.

### Stage 1 — frac_B(a) com os DOIS controles anti-artefato

Para a ∈ {1,2,4,8}, R̂ baixo (=8, regime do universo observável), altura h=3 (melhor
amostrada em E6b/E6c), N e seeds de E6c. Medir frac_B (Wilson) **e**:

- **Controle de plano (reuso de B4):** b_plane(12,13) vs b_plane(23). Na versão fiel,
  como **nenhuma coordenada é esticada**, os planos NÃO podem explodir ordens de
  magnitude. **Assinatura de morte por artefato residual:** se b_plane[12,13] estoura
  ×>10 enquanto b_plane[23] fica fixo ⇒ ainda há esticamento de coordenada escondido ⇒
  **DEATH_B4G_ARTIFACT** (a implementação vazou anisotropia para a classificação).
  Crescimento **limitado e comparável** entre planos é a assinatura genuína.
- **Null de ordem-embaralhada (decisivo, novo):** construir plaquetas a partir da ordem
  **isotrópica** (a=1) nos **mesmos pontos**, classificar com o mesmo bivetor plano.
  frac_B_null deve ficar no piso de E6c (~0.003). Se frac_B(a>1) − frac_B_null é
  consistente com zero ⇒ a ordem anisotrópica **não** abre o setor ⇒ a subida (se houver)
  é dos pontos/amostragem, não da causalidade.

**Critério Stage 1:**
- frac_B(a) sobe **acima de 0.01** (Wilson-lo) com a, gap sobre o null > piso, e SEM
  blow-up de plano ⇒ **candidato magnético genuíno** → prosseguir ao Stage 2.
- frac_B fica **< 0.01** mesmo a a=8 ⇒ **DEATH_B4_GENUINE**: cones direcionais não abrem
  o setor magnético a baixa curvatura. [FRONTEIRA] vira afirmação forte (nem curvatura
  isotrópica E6c, nem cones futuros B3b, nem Bianchi-I genuíno abrem o fóton magnético).
- Blow-up de plano ⇒ **DEATH_B4G_ARTIFACT** (vazamento; consertar antes de reivindicar).

### Stage 2 — GATE DE GAUGE (só se Stage 1 candidato): a lição de B3b

Aplicar a maquinaria de `b3b_closure.py` às **plaquetas magnéticas** (b²>e²) de B4:

- **Pertencimento ao substrato (esperado 100%):** as plaquetas são caminhos de Hasse,
  então `side_link_fraction ≈ 1.0` por construção — confirmar (distingue de B3b, onde
  era ~0.31). Se <1, há bug.
- **∂∂ = 0 + invariância de gauge** (incidência B, cobordo G): aqui o teste É
  informativo porque o complexo está no substrato. Reportar ∂∂ e ΔS/S.
- **Null cinemático** (B3b): plaquetas isotrópicas (a=1) pela MESMA maquinaria. O
  discriminante NÃO é ∂∂ (automático), é: o setor físico (rank B) das plaquetas
  magnéticas anisotrópicas é genuinamente mais rico que o do null isotrópico? E o
  complexo magnético é **conexo** (propaga) ou são células isoladas?

**Critério Stage 2:**
- Gauge genuíno no substrato + complexo conexo + setor físico > null ⇒ **GATE VERDE** →
  Stage 3 (dispersão), reusando E6_2.
- Caso contrário ⇒ **DEATH_B4G_NOGAUGE** (setor magnético existe mas não é gauge; eco
  de B3b um nível adiante).

### Stage 3 — Dispersão ω=ck (só se Stage 2 VERDE)

Reuso de `E6_2_dispersion.py` / `e6_bd_core.py`: símbolo do operador indefinido (E²−B²)
sobre o complexo magnético; c **fitado** ao cruzamento on-shell, nunca inserido. ω=ck a
~5%, massa→0 ⇒ tríade completa. Difusivo/massivo ⇒ DEATH_B4G_NODISP.

### Stage 4 — N-estabilidade (só se tríade completa)

Repetir Stage 1+2 em ≥2 N maiores; confirmar que frac_B(a), o gauge e (se houver) a
dispersão sobrevivem, e que o null não cresce junto. (A armadilha B5/B6/B3b: a fração
NÃO pode cair com N como caiu o `side_link_fraction` de B3b.)

## 5. Critérios de veredito

| Tag | Condição | Consequência |
|---|---|---|
| **INVALID** | a=1 ≠ E6c, ou ordem não é parcial estrita | construção suspeita; consertar |
| **DEATH_B4G_ARTIFACT** | blow-up de plano (12,13 ≫ 23) | vazou anisotropia p/ classificação |
| **DEATH_B4_GENUINE** | frac_B < 0.01 até a=8 | cones direcionais não abrem o setor; [FRONTEIRA] forte |
| **DEATH_B4G_NOGAUGE** | setor magnético existe mas não é gauge/conexo | eco de B3b um nível adiante |
| **DEATH_B4G_NODISP** | gauge sem ω=ck | gauge sem propagação de luz |
| **SUCCESS_B4_GENUINE** | tríade completa, N-estável, controles limpos | **charter de paper** (fóton magnético de Bianchi-I) |

**Regra de ouro (B3/B4/B3b):** frac_B alto NÃO é evidência de fóton. O controle é a
ciência; o número cru é a armadilha. Na dúvida entre SUCCESS e artefato → ramo
conservador.

## 6. O que B4-genuíno NÃO afirma

- Não reabre B4 original (morto, artefato de coordenada) — é uma construção diferente
  (anisotropia na ordem, não no embedding).
- Não toca os diamantes BD de E6 (gauge fiel elétrico, inalterado).
- Se DEATH_B4_GENUINE: não prova impossibilidade no universo — prova que **estas três
  alavancas** (curvatura isotrópica E6c, cones futuros B3, Bianchi-I genuíno B4) não
  abrem o setor magnético a baixa curvatura; o fóton magnético fica [FRONTEIRA]
  documentada, mais forte.

## 7. Código necessário

| Módulo | Status | Ação |
|---|---|---|
| `causal_matrix_aniso(pts, a)` | **novo** | variante anisotrópica de `causal_core.causal_matrix` |
| `height_h_plaquettes`, `polygon_bivectors` | existe (E6b) | reuso verbatim |
| controle de plano (12,13 vs 23) | existe (B4) | reuso |
| null de ordem-embaralhada | **novo** | plaquetas a=1 nos mesmos pontos |
| gate de gauge (Stage 2) | existe (`b3b_closure.py`) | reuso |
| dispersão (Stage 3) | existe (`E6_2`, `e6_bd_core`) | reuso |

Custo estimado: **1–3 CPU-dias** (o novo real é só `causal_matrix_aniso` + o null de
ordem; Stages 2/3 são reuso). Stages 0+1 são o gate bloqueante mais barato.

## 8. Anti-circularidade (guarda A1)

- Todo código sob guarda A1; CI verde antes de rodar.
- `a` adimensional, varrido, emerge; nenhum c/ω/escala inserido (Stage 3 fita c).
- Classificação E/B em coordenadas planas isotrópicas (E6c) — **nenhuma coordenada
  esticada** (a lição direta da morte de B4 original).
- Controles obrigatórios em todo número: gate a=1=E6c, controle de plano, null de
  ordem-embaralhada (Stage 1); null cinemático (Stage 2).
- Verificar que o detector de dilatação não dá falso-positivo no intervalo anisotrópico.

## 9. Posição na hierarquia

```
FASE 3 — Fóton (escalas fechada: B1/B5/B6/B7)

  E6/E6b/E6c: diamantes BD = ~100% ELÉTRICO; magnético só Planckiano
        │
        ├── B3 candidato (frac_B=0.84) → B3b GATE GAUGE = MORTE_NOGAUGE
        │      (cones futuros fecham mas fora do substrato de links)
        │
        ▼
  B4-genuíno ◄── ESTE (última alavanca a baixa curvatura)
        │        anisotropia na ORDEM causal (cones direcionais)
        │
   ┌─────┴───────────────────────────────────┐
 SUCCESS (tríade)                        DEATH (qual stage?)
 charter de paper                        fóton magnético [FRONTEIRA] forte
 (fóton de Bianchi-I)                    (3 alavancas esgotadas a baixa curvatura)
```

---

> **Instrução ao Claude Code:** Stage 0 e Stage 1 são bloqueantes. A anisotropia entra
> SÓ na ordem causal; a classificação E/B fica em coordenadas planas (a lição de B4
> original — nenhuma coordenada esticada). Rode os DOIS controles do Stage 1 (plano +
> null de ordem) em todo número; sem eles os frac_B crus enganam. O gate de gauge
> (Stage 2) só roda se Stage 1 der candidato, e reusa `b3b_closure.py` — aqui ele É
> informativo (plaquetas no substrato de links, ≠ B3b). Na dúvida, ramo conservador.
> Entregue SYNTHESIS_B4_genuino.md no formato das anteriores, com a tabela
> (frac_B, b_plane 12/13/23, null-gap, por a e por N) explícita.
