# PHI_EMERGE_V3 — Back-reaction espontânea na criação do vórtice

PE4_V2 (Veredito B) mostrou que a densidade causal **dinâmica** depleta no núcleo de
um vórtice e o pina (σ_core=3.73 constante) — mas com ρ **inicializado** já com o dip
e a profundidade controlada pela rigidez K. PE4_V3 testa a pergunta mais aguda: com ρ
um campo genuinamente dinâmico (`□ρ = J`, o mesmo operador de onda que D1–D3 usam
para a gravitação), partindo de ρ **uniforme**, o dip **emerge espontaneamente**
quando uma colisão cria o vórtice — e em que tempo?

Código/dados: `results/phi_emerge/v3/`. 20 sementes em S2; verificação tripla da
emergência. Anti-circularidade: ρ é densidade real que evolui sob ação; J é a ação de
gauge real; nenhum literal complexo; "condensado/Higgs/Cooper" só em COMPARISON ONLY.

## A diferença PE4_V2 → PE4_V3

```
PE4_V2:  t=0 vórtice presente, ρ JÁ depleto (inicializado) → o dip persiste? SIM
PE4_V3:  t=0 ρ UNIFORME → colisão cria vórtice → ρ dinâmico back-reage? → a verificar
```
PE4_V2 testou **persistência**. PE4_V3 testa **emergência**.

## Scorecard

```
S1 — Protocolo ρ dinâmico (□ρ=J):       SIM (J=0→uniforme; fonte M→1/r, r²=0.9992)
S1 — τ_vortex (colisão real):           3.9±0.6 ticks
S2 — Dip emerge espontaneamente:        SIM (razão a V2 = 0.994)
S2 — τ_dip:                             2.3 ticks (< τ_vortex → dip forma COM o vórtice)
S2 — σ_core constante:                  SIM (3.72±0.10, 100% def.; = PE4_V2 3.73)
S3 — K_c(ρ):                            K_c≈8.5 (CONSTANTE em ρ — escala de acoplamento física)
S4 — Cinco consistências (ρ dinâmico):  5/5
```

## A cadeia (e exatamente onde é condicional)

```
ρ uniforme → colisão cria vórtice W=1 (τ_vortex≈3.9) ............. S1 ✓
  → ação de gauge [1−cos(u)] pica no núcleo (fonte J_ρ)
  → ρ dinâmico back-reage: dip EMERGE de ρ uniforme ............. S2: razão a V2 ≈ 1.00 ✓
  → rápido: τ_dip≈2.3 < τ_vortex≈3.9 (dip forma com o vórtice) ... S2 ✓
  → núcleo pinado, σ_core=3.72 constante (= PE4_V2) ............. S2/S4 ✓
  → |Φ|=ρ → 0 no núcleo (depleção TOTAL) ........................ só para K ≲ K_c≈8.5  ⟵ condicional
  → cinco consistências com ρ dinâmico .......................... S4: 5/5 ✓
  → estabilização do ENROLAMENTO de gauge ....................... NÃO (basal CR_3D)  ⟵ resíduo
```

## Veredito: **B** (reforçado) — emergência espontânea, fechamento condicional

> A rarefação **emerge espontaneamente** a partir de ρ uniforme quando a colisão cria
> o vórtice, rápido o bastante (τ_dip < τ_vortex) para se formar junto com ele,
> atingindo o equilíbrio de PE4_V2 com um núcleo pinado de largura constante
> (σ_core=3.72, idêntico a PE4_V2), e as cinco
> consistências passam com ρ dinâmico (5/5). O fechamento **completo** (|Φ|(0)→0) é
> condicionado a K ≲ K_c≈8.5 — a condição de rigidez suave de PE4_V2, agora mapeada e
> mostrada **independente da densidade** (uma escala de acoplamento física). O quarto
> ingrediente de CR_AH é **reduzido** (a magnitude |Φ|=ρ emerge de ρ dinâmico, sem
> campo novo nem parâmetro novo), **não eliminado**: a estabilização do enrolamento de
> gauge permanece como ingrediente do setor de gauge. Veredito A (incondicional) **não**
> é afirmado.

## Por que não A, C, ou D

- **Não C** (sem emergência): refutado — o dip emerge de ρ uniforme e atinge o
  equilíbrio de PE4_V2 (razão ≈1.00), com τ_dip < τ_vortex. Verificação tripla (S5).
- **Não D** (ρ desestabiliza): refutado — ρ é sourced unidirecionalmente (`□ρ=J`, sem
  retroação no gauge); o enrolamento difunde igual em CR_3D, com ou sem ρ. ρ não
  desestabiliza nem estabiliza o enrolamento.
- **Não A** (incondicional): retido — (i) depleção total exige K ≲ K_c≈8.5; (ii) o
  enrolamento de gauge ainda precisa de fixação (setor de gauge). V3 fecha a
  **magnitude**, não o **enrolamento**.

## A jornada PHI_EMERGE, completa

```
PHI_EMERGE     [C]:  |Φ|=ρ_Poisson reproduz a FASE (massa de gauge ∝√ρ), não a MAGNITUDE
PHI_EMERGE_V2  [B]:  com ρ DINÂMICO inicializado, a magnitude fecha (|Φ|(0)→0, pinado),
                     condicionada a ρ dinâmico + K suave
PHI_EMERGE_V3  [B]:  com ρ dinâmico ESPONTÂNEO (de ρ uniforme), a magnitude EMERGE rápido
                     (τ_dip<τ_vortex), 5/5 consistências; K_c≈8.5 mapeado, indep. de ρ;
                     enrolamento de gauge é o resíduo → quarto ingrediente REDUZIDO
```

A investigação sobre a emergência da magnitude de Higgs na TEIC está **completa e
precisa**: a magnitude `|Φ|=ρ` emerge espontaneamente da densidade causal dinâmica
(a mesma de D1–D3), sem axioma extra de magnitude, dentro do regime de rigidez suave
K ≲ K_c≈8.5; o que resta para matéria plenamente estável é a fixação do enrolamento de
gauge — localizado com máxima precisão, e honestamente não superafirmado.

## Reprodução

`python results/phi_emerge/v3/S1_protocol.py` … `S5_synthesis.py`. Detalhe por tarefa
em `S1_protocol.md` … `S5_synthesis.md`, com JSON e figuras (`S1_protocol.png`, `S2_emergence.png`, `S3_phasemap.png`).
