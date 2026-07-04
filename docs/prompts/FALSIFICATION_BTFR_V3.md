# FALSIFICATION_BTFR_V3 — confronto 2026: a₀(z) medido no regime certo (MUSE-DARK III)

> Continuação de `FALSIFICATION_BTFR_V2.md` (Übler+2017, regime errado) e do
> forecast `results/predictions/F1_forecast.md` (kill criterion pré-registrado).
> Campanha OBSERVACIONAL: confronto de números publicados — sem simulação, sem
> parâmetro ajustável. Resultados em `results/falsification/btfr_v3/`.
>
> **Pré-registro desta campanha:** as regras de decisão R1–R4 e a matriz de
> âncoras abaixo foram fixadas ANTES de computar o confronto. O kill criterion
> de F1 NÃO é alterado.

## O dado novo (jun/2026)

**MUSE-DARK III** (Ciocan, Bouché, Fensch et al., A&A 708 A112, abr/2026;
arXiv:2604.22613): RAR de **79 SFGs em 0.33<z<1.44**, 8.8<log M*<11,
mass-complete, **regime de baixa aceleração** (discos submaximais, >50% DM
dentro de R_e — ao contrário de SPARC/KMOS³D), modelagem 3D forward com
correção de suporte de pressão, robusto a perfis ΛCDM E a framework MOND
autoconsistente:

```
a₀|z~1 = 2.38 +0.12/−0.10 ×10⁻¹⁰ m/s²   (~19σ acima de SPARC z=0: 1.2±0.26;
                                          5σ acima de MIGHTEE-HI z<0.08: 1.69±0.13)
a₀(z) = a₀(0) + a₁·z:  a₀(0) = 1.00 +0.04/−0.04,  a₁ = 1.59 +0.11/−0.10  (~30σ)
bins: 1.99 → 2.71 ×10⁻¹⁰ (z baixo → alto); robusto a DC14/NFW/MOND
Os autores: evolução "mais rápida que H(z) (Milgrom 1983a)".
```

Contexto adicional citado pelo paper: Vărășteanu+2025 (MIGHTEE-HI, z≲0.08):
a₁ = 4.47±1.88 (consistente a 1.5σ); Jeanneau et al. 2026 (arXiv:2603.28856):
**bTFR sem evolução em z~1** quando o gás neutro entra por relações de escala
— a leitura "eixo de massa" e a "eixo de aceleração" ainda discordam (mesma
discordância de sistemáticos da V2).

## Regras de decisão (fixadas antes do cômputo)

```
R1 (kill F1): existe amostra publicada cumprindo o critério F1 (z≥2, N≥25,
    rica em gás, a≲a₀, σ_sys≤0.03 dex) com Δlog v ≤ 0?  → morte do setor
    galáctico. [Levantamento: NÃO existe tal amostra até jun/2026 — o kill
    permanece não-executável; nada de rebaixar o critério para forçar veredito.]
R2 (direção): sinal de da₀/dz no regime certo. A previsão exige +.
    (a₀ ∝ H(z) ⟺ Δlog v = ¼log[H/H₀] > 0 e crescente.)
R3 (amplitude em z~1): Δlog v_obs = ¼·log[a₀(z~1)/a₀(âncora)] vs previsto
    +0.0614 (F1, z=1). Matriz de âncoras DECLARADA (a divergência entre
    âncoras locais é ela própria o sistemático dominante):
      A1 SPARC (McGaugh+16):      1.20 ± 0.26
      A2 MIGHTEE-HI (Văr.+25):    1.69 ± 0.13
      A3 própria (fit a₀(0)):     1.00 ± 0.04
    Leitura: consistente se |obs−prev| < 2σ em ao menos uma âncora defensável,
    com o spread inter-âncoras reportado como σ_sys.
R4 (forma): a₁ medido vs linearização de a₀∝H (a₁_H = a₀(0)·[dE/dz]_{z̄},
    E=H/H₀) — fator de tensão reportado; sem veredito de morte por forma
    (a parametrização linear é fenomenológica, dito pelos próprios autores).
```

## ✅ VEREDITO (preenchido após o cômputo — `results/falsification/btfr_v3/V3_confront.*`)

```
R1  KILL NÃO DISPARADO — nenhuma amostra z≥2 no regime certo existe (jun/2026);
    e no regime certo disponível (z≲1.44) o sinal tem o sinal OPOSTO ao da
    morte: Δlog v > 0 robusto.
R2  DIREÇÃO CONFIRMADA — a₁/σ = 15.1σ (estat., dos números publicados; o paper
    reporta ~30σ na análise completa) no regime de baixa aceleração; a ameaça
    da V2 (tendência interna oposta, 7.2σ, KMOS³D regime errado) está
    DISSOLVIDA pelo dado de regime certo.
R3  AMPLITUDE CONSISTENTE DENTRO DO SISTEMÁTICO DE ÂNCORA (z_eff ∈ [0.85, 1.0]):
      A1 SPARC (indep.):   Δlog v = +0.0743 ± 0.0241  → +0.5σ a +0.9σ ✓
      A2 MIGHTEE (indep.): Δlog v = +0.0372 ± 0.0097  → −1.3σ a −2.3σ
      A3 própria (CORRELACIONADA, nota de consistência): +0.0941 ± 0.0066
         → +4.9σ a +6.4σ — covariância com o numerador; não é tensão indep.
    spread inter-âncoras 0.029 dex ≈ o próprio σ_sys≈0.03 que F1 exige —
    a previsão está DENTRO do leque das âncoras independentes; a âncora local
    é o gargalo, exatamente como F1 previu.
R4  FORMA EM TENSÃO MODERADA — a₁ = 1.59±0.11 vs a₁_H (secante 0→1):
    0.91 (SPARC, 3.0σ, fator 1.74) · 1.31 (MIGHTEE, 2.0σ, fator 1.22) ·
    0.76 (própria, 7.6σ correlacionada, fator 2.09). MAS: (i) o fit linear
    extrapolado a z=1.44 (3.29) excede o próprio bin medido (2.71) — a forma
    linear força a inclinação; (ii) a₀∝H ancorado em SPARC dá 2.50 em z=1.3
    vs bin 2.71 (8%). Forma: indecidida por sistemáticos de âncora; direção e
    ordem de grandeza: certas.
```

### A frase honesta

> O kill de F1 segue armado e intacto para z≥2. No regime certo (baixa
> aceleração, 79 galáxias, 3D, robusto a ΛCDM e MOND), o dado de 2026 mede
> exatamente o que a previsão precisa que exista — a₀ crescendo com z — e a
> amplitude em z~1 é consistente com ¼log[H/H₀] dentro do sistemático de
> âncora local. Quem está sob fogo neste dado é a evolução NULA (ΛCDM/RAR
> constante, 19σ) — não a previsão. A forma exata (linear vs H) permanece
> indecidida; a decisão continua onde F1 a colocou: z≥2, σ_sys≤0.03
> (SKA deep HI / JWST+ALMA de anãs gasosas).

## Vigília (o que observar a seguir)

1. **SKA deep HI** — os próprios autores apontam: o teste crítico de bTFR+RAR.
2. **Jeanneau+2026 vs Ciocan+2026** — a discordância massa-eixo vs
   aceleração-eixo em z~1 precisa se resolver; é o mesmo sistemático que
   impediu veredito na V2.
3. Qualquer amostra **z≥2** de rotadores ricos em gás com N≥25: executar F1
   imediatamente, sem alterar o critério.

## Artefatos

`results/falsification/btfr_v3/V3_confront.{py,json,png,md}` — determinístico
(números publicados + H(z) plano Ωm=0.3±0.02; H₀ cancela).
