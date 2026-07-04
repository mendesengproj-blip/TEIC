# Caminho B — hierarquia de escalas: dois modos de A_μ

> Decidido **analiticamente** em FN3b-0 (o gate). Não precisou de código além da
> checagem do vev de Stückelberg em `fn3b_core.stueckelberg_vev_GeV`.

## A hipótese

O campo vetorial A_μ teria dois regimes independentes:
- **modo cosmológico** (homogêneo, escala Hubble): oscila por misalignment com
  amplitude grande f_A^cosmo ~ M_GUT → faz a DM;
- **modo galáctico** (sourced pelo θ, escala kpc): amplitude pequena v = m_A/e →
  faz MOND.

Se desacoplados, f_A^cosmo poderia ser grande **independentemente** do modo galáctico.

## O cálculo — os modos compartilham o vev de Stückelberg

A massa do vetor na DEV vem do mecanismo de **Stückelberg/Higgs**: m_A = e·v, onde v
é o vev da quebra da simetria U(1). O campo físico A_μ vive num **círculo de raio v**
— a amplitude de **qualquer** configuração do campo (inclusive a oscilação homogênea
de misalignment) é **limitada por v**:

```
v = m_A/e = (10⁻²² eV)/0.303 = 3.3×10⁻²² eV = 3.3×10⁻³¹ GeV
amplitude de misalignment ≤ v = 3.3×10⁻³¹ GeV   →   48 ordens abaixo de 10¹⁷ GeV
Ω_misalignment ~ 0.12·(v/10¹⁷ GeV)² ~ 10⁻⁹⁵   (desprezível)
```

O modo homogêneo cosmológico e o modo galáctico são soluções da **mesma** equação de
Proca, com a **mesma** constante v. v fixa simultaneamente:
- a **massa** (m_A = e·v) — calibrada por MOND galáctico;
- a **amplitude máxima** (v) — o raio do círculo do campo.

**Não há liberdade** para um f_A cosmológico grande: fixar o modo galáctico (v=m_A/e,
da fenomenologia de galáxias) **fixa automaticamente** a amplitude máxima cosmológica.
Os dois modos estão **fortemente acoplados via v** — exatamente o critério de morte B.

## A única fuga — e por que não vale

A amplitude só seria livre se m_A fosse uma massa de **Proca "dura"** (sem vev,
amplitude não-compacta). Mas isso:
1. **abandona o mecanismo de Stückelberg** que é a origem da massa do vetor na DEV;
2. reabre problemas de invariância de gauge / forte acoplamento no UV (um vetor
   massivo "duro" acoplado a uma corrente não-conservada não é renormalizável);
3. seria, de fato, **postular uma nova física** — não uma extensão natural da DEV.

## Veredito B

```
Modos são desacoplados?           NÃO (compartilham o vev v de Stückelberg)
f_A cosmológico livre?            NÃO (amplitude ≤ v = m_A/e = 3.3×10⁻³¹ GeV)
Consistente com MOND galáctico?   SIM, mas é justamente o que ACOPLA os modos
Veredito B:   MORTE — o vev de Stückelberg que dá a massa (m_A=ev, calibrada por MOND)
              também limita a amplitude de misalignment a v; não há f_A grande livre.
              Decidido analiticamente; a fuga (Proca duro) abandona o mecanismo da DEV.
```
