# SÍNTESE — B4-genuíno · Bianchi-I na ORDEM causal: o setor magnético não abre

> Campanha FOTON_B3B4 (Fase 3, Frente do Fóton). Versão fiel de B4 (cones de luz
> direcionais na ordem causal), última alavanca a baixa curvatura.
> Driver: `b4_genuino.py`. Resultado: `b4_genuino.json`. Pré-registro:
> `PRE_REGISTRO_B4_GENUINO.md`. jun/2026.
>
> **Decisão do usuário: rodar SÓ os gates bloqueantes (Stage 0+1), parar no 1º veredito.**
>
> **Veredito: DEATH_B4_GENUINE.** Anisotropia genuína na **ordem causal** (cones de luz
> direcionais, dt² > a²dx₁²+dx₂²+dx₃², a até 8) **não abre o setor magnético** a baixa
> curvatura: frac_B fica pregado no piso elétrico-dominado de E6 (~0.002–0.003) para todo
> a, com gap desprezível (≤0.0008, até negativo a a=2) sobre o null de ordem-isotrópica
> nos **mesmos pontos**. A ordem anisotrópica **redistribui** o conteúdo magnético entre
> planos espaciais (efeito real, não artefato) mas **não** torna as plaquetas
> spacelike-dominadas. **Stages 2 e 3 (gauge, dispersão) não rodaram.** Combinado com E6c
> (curvatura isotrópica) e B3b (cones futuros), as **três alavancas a baixa curvatura
> estão esgotadas** — o fóton magnético fica [FRONTEIRA], agora afirmação forte.

---

## 1. A cirurgia (e por que ela é limpa)

B4 original morreu (DEATH_B4_COORD_ARTIFACT) por pôr a anisotropia no **embedding** com
ordem isotrópica: esticar x₁ inflava A^{1j} ×6×10⁴ (artefato de unidade). B4-genuíno faz
a cirurgia pré-registrada: anisotropia **só na ordem causal**, classificação E/B em
**coordenadas planas** (o classificador de E6c, nenhuma coordenada esticada).

```
p ≺ q  ⟺  dt > 0  E  dt² > a²·dx₁² + dx₂² + dx₃²      (a adimensional; a=1 = flat)
```

Se frac_B subisse, seria porque cones anisotrópicos **selecionam** plaquetas diferentes
(áreas planas mais spacelike), não porque áreas foram rescaladas. Não subiu.

## 2. Stage 0 — reconstrução validada: PASSA

- **a=1 ≡ isotrópico:** `causal_matrix_aniso(pts,1)` byte-idêntico a `causal_matrix(pts)`
  (✓ `array_equal`).
- **Ordem parcial estrita** (antissimétrica, irreflexiva, transitiva) para todo a∈{1,2,4,8}
  (✓ verificado em sub-bloco).

## 3. Stage 1 — frac_B(a) com os dois controles anti-artefato

| a | frac_B [Wilson] | null (ordem iso, mesmos pts) | gap | b_plane (12, 13, 23) |
|---|---|---|---|---|
| **1** (gate) | **0.00283** [0.0022,0.0036] | 0.00283 | +0.0000 | 0.279, 0.278, 0.268 |
| 2 | 0.00121 [0.0008,0.0017] | 0.00204 | **−0.0008** | 0.099, 0.104, 0.368 |
| 4 | 0.00271 [0.0021,0.0035] | 0.00200 | +0.0007 | 0.036, 0.034, 0.489 |
| 8 | 0.00233 [0.0015,0.0035] | 0.00192 | +0.0004 | 0.011, 0.011, **0.629** |

*(b_plane do null-iso fica plano ~0.27–0.29 em todo a — confirma que a redistribuição
abaixo vem da ORDEM, não dos pontos. P=24000 por linha, exceto a=8 com P=9451: cone
estreito gera menos caminhos de altura-3.)*

**Três leituras:**

1. **frac_B não abre.** Fica em ~0.002–0.003 para todo a — nunca se aproxima de 0.01.
   Os diamantes permanecem **timelike-dominados** (elétricos) por mais estreito que seja
   o cone em x₁. **Gate a=1 = 0.00283 reproduz o flat E6 elétrico** (✓ <0.01).

2. **O efeito da ordem é real, mas não é magnetização.** O conteúdo magnético **migra**
   dos planos que contêm x₁ (12,13: 0.279 → **0.011**) inteiramente para o plano 23
   (0.268 → **0.629**) à medida que a→8. Isto é o **oposto** do artefato de B4 original
   (lá os planos esticados *explodiam*); aqui eles *encolhem*, porque estreitar o cone em
   x₁ suprime links x₁-separados. A geometria muda genuinamente — mas a **fração** de
   plaquetas com b²>e² não sobe, porque o total continua dominado pelo eixo temporal.

3. **Controles limpos.** Sem blow-up de plano (stretched ×1.0, unstretched ×1.0 —
   `is_coordinate_artifact=False`). Gap sobre o null-iso ≤0.0008 e **negativo a a=2**
   (anisotropia até *reduz* frac_B). Nenhuma assinatura de setor magnético emergente.

## 4. Veredito

**DEATH_B4_GENUINE.** Cones de luz direcionais (Bianchi-I genuíno) não fornecem um fóton
magnético a baixa curvatura. A morte é **forte e limpa**: a ordem anisotrópica restrutura
de fato a geometria (a migração de b_plane prova que não é nulo trivial), e mesmo assim o
setor magnético não abre. Como pré-registrado, **Stages 2 (gauge) e 3 (dispersão) não
rodaram** — bloqueados pelo gate.

## 5. O mapa do fóton magnético a baixa curvatura está fechado

| Alavanca | Campanha | Resultado |
|---|---|---|
| Curvatura isotrópica | E6c | magnético só a curvatura **Planckiana** (frac_B<0.01 a R̂≥8) |
| Intersecção de cones futuros | B3 → **B3b** | candidato (frac_B=0.84) **morto** no gate de gauge (fora do substrato de links) |
| Anisotropia (Bianchi-I) na ordem | **B4-genuíno** | frac_B não abre (~0.003); redistribui, não magnetiza |

As **três** alavancas a baixa curvatura estão esgotadas. O fóton magnético no causet
permanece **[FRONTEIRA]** — não mais uma lacuna não-testada, mas uma **fronteira
mapeada**: o setor de gauge fiel (diamantes BD de E6) é elétrico, e nenhuma das três vias
a baixa curvatura o tilta para magnético. Nenhum charter de paper congelado; o Paper
Photon-Arc ganha o fechamento do mapa.

## 6. O que B4-genuíno NÃO afirma

- Não prova impossibilidade no universo — prova que **estas três construções** não abrem
  o setor a baixa curvatura. O magnético existe a curvatura Planckiana (E6c); só não no
  regime observável por estas vias.
- Não toca os diamantes BD de E6 (gauge fiel elétrico, inalterado).
- A migração de b_plane (§3.2) é um sub-resultado físico genuíno (anisotropia
  redistribui conteúdo magnético entre planos espaciais), registrado, mas **não** é fóton.

## 7. Anti-circularidade

Guarda A1 **verde** (`pytest tests/ -q` = 2 passed; `SCAN_DIRS` cobre `docs/campaigns/**`
→ varreu `b4_genuino.py`; sem dilatação, sem literal de escala). `a` adimensional, varrido,
emerge; nenhum c/ω inserido (Stage 3 nem rodou). Classificação E/B em coordenadas planas
isotrópicas (a lição de B4 original — nenhuma coordenada esticada). Controles obrigatórios
em todo número: gate a=1≡E6 flat, controle de plano (12,13 vs 23), null de ordem-isotrópica
nos mesmos pontos. O detector de dilatação não deu falso-positivo no intervalo anisotrópico.
