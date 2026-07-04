# V3 — confronto a₀(z) 2026: a previsão sobrevive; ΛCDM-sem-evolução é quem sangra

> Fecha `FALSIFICATION_BTFR_V3.md`. Determinístico (números publicados +
> H(z) plano, Ωm=0.30±0.02; H₀ cancela). Dados: `V3_confront_data.json`;
> figura `V3_confront.png`. Regras R1–R4 pré-registradas no charter.

## Fonte primária

Ciocan, Bouché, Fensch, Krajnović, Freundlich, Desmond, Famaey, Techi —
**MUSE-DARK III**, A&A 708 A112 (abr/2026), arXiv:2604.22613. 79 SFGs,
0.33<z<1.44, 8.8<log M*<11, mass-complete, **regime de baixa aceleração**
(submaximais, >50% DM em R_e), 3D forward modelling com suporte de pressão,
robusto a DC14/NFW e a um framework MOND autoconsistente.
Âncoras locais: SPARC (McGaugh+16) 1.20±0.26; MIGHTEE-HI (Vărășteanu+25,
z<0.08) 1.69±0.13.

## Resultado por regra

| Regra | Resultado |
|---|---|
| R1 kill F1 | **NÃO disparado** — nenhuma amostra z≥2 qualificante existe; o sinal disponível tem sinal OPOSTO ao da morte |
| R2 direção | **+15.1σ** (a₁=1.59±0.11 > 0); paper reporta ~30σ |
| R3 amplitude | previsto +0.052…+0.061; SPARC **+0.074±0.024 (0.5–0.9σ ✓)**; MIGHTEE +0.037±0.010 (−1.3 a −2.3σ); spread de âncoras 0.029 dex = o σ_sys de F1 |
| R4 forma | a₁ medido 1.2–1.7× a secante de H (2.0σ MIGHTEE, 3.0σ SPARC); fit linear extrapolado (3.29 em z=1.44) excede o próprio bin (2.71); a₀∝H-SPARC dá 2.50 vs bin 2.71 em z~1.3 |

## Leitura honesta

1. **O que mudou desde a V2 (2017/Übler):** a tensão de 7.2σ "tendência
   interna oposta" veio de galáxias massivas em regime Newtoniano — o regime
   onde a previsão é fraca (ressalva B5). O primeiro dataset do regime CERTO
   (baixa aceleração, anãs/discos DM-dominados) mede evolução **positiva** de
   a₀ com z — a direção que a previsão `Δlog v=¼log[H/H₀]` exige e que
   ΛCDM/RAR-constante proíbe. A ameaça da V2 está dissolvida.
2. **Amplitude:** com a âncora SPARC (a calibração canônica da RAR), a
   previsão fecha a 0.5–0.9σ. A divergência entre âncoras locais
   (1.20 vs 1.69, mutuamente ~1.7σ) é o sistemático dominante — 0.029 dex,
   exatamente o piso σ_sys≈0.03 que o forecast F1 identificou como gargalo.
   F1 previu que o gargalo seria esse; é.
3. **Forma:** a inclinação linear publicada é mais rápida que H(z) por fator
   1.2–1.7 (âncora-dependente, 2–3σ). Mas a parametrização linear é
   declaradamente fenomenológica (os autores), o fit extrapolado excede o
   próprio bin mais alto, e o bin mais alto está a 8% de a₀∝H ancorado em
   SPARC. Indecidível hoje; decidível no critério F1 (z≥2, σ_sys≤0.03).
4. **Quem sofreu com este dado:** evolução nula (ΛCDM com RAR constante) — o
   valor local está a ~19σ (estat.) do valor em z~1 no regime certo. A
   previsão da TEIC/DEV não só sobrevive: o dado mede a existência do efeito
   que ela exige, na direção certa, com amplitude compatível.

## Ressalvas declaradas

- A identificação a₀∝H(z) é herdada da camada fenomenológica (DEV); a rede
  NÃO a deriva (C3: X₀∝ρ é UV) — inalterado desde F1. Se morrer em z≥2,
  morre o setor galáctico da EFT, não a geometria (R1–R4).
- a₀|z~1 e a₀(0)=1.0 do fit linear saem do MESMO MCMC: a linha A3 é nota de
  consistência interna do paper, não tensão independente.
- z_eff da amostra completa tratado como faixa [0.85, 1.0] (o paper rotula
  "z~1" sem publicar a mediana exata).
- Jeanneau+2026 (bTFR sem evolução em z~1 via gás por relações de escala)
  mantém viva a discordância massa-eixo vs aceleração-eixo — o mesmo
  sistemático da V2; vigília declarada no charter.

## Reproduzir

```
python results/falsification/btfr_v3/V3_confront.py
```
