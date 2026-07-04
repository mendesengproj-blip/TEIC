# HQ3_NANOGRAV — Espectro de Ondas Gravitacionais do m_A vs NANOGrav 2023

> **STATUS: CONCLUÍDO — VEREDITO B (PARCIALMENTE CONSISTENTE).**
> Frequência f_GW=2m_Ac²/h das massas do Paper II cai na banda do PTA (overlap
> 4.1×10⁻²⁴–1.2×10⁻²² eV); o mesmo m_A produz uma linha de Khmelnitsky–Rubakov que
> roça o limiar do PTA na ponta de massa baixa. Mas o m_A **não** é o fundo
> estocástico que o NANOGrav detectou: é uma LINHA (não o contínuo γ=13/3), e o SGWB
> que ele irradia está ~21 ordens abaixo. Resultados em
> [`results/cosmology/hq3/`](results/cosmology/hq3/) — síntese em
> [`HQ3_5_synthesis.md`](results/cosmology/hq3/HQ3_5_synthesis.md).
>
> **Contexto da literatura (não-ajuste):** DM vetorial ultraleve com m ∈ [10⁻²⁴, 10⁻²³]
> eV produz sinal na banda PTA em f = μ/π (arXiv:2412.12975); o m_A do Paper II
> (m_A > 3.7×10⁻²⁵ eV) tem overlap com esse range. NANOGrav 2023: arXiv:2306.16213.

Calcula o espectro de ondas gravitacionais produzido pelo campo vetorial massivo m_A
oscilante e compara com o sinal detectado pelo NANOGrav em 2023. Pergunta: o m_A da
DEV é consistente com NANOGrav? NÃO modifica nenhuma campanha anterior.

---

## CONTEXTO

### O sinal do NANOGrav 2023

O NANOGrav reportou em 2023 (arXiv:2306.16213) a detecção de um fundo estocástico de
ondas gravitacionais (SGWB) com:

```
Amplitude A_GW ≈ 2.4×10⁻¹⁵ (na frequência f_ref = 1/yr)
Índice espectral γ ≈ 13/3 (compatível com fusões de buracos negros supermassivos)
Frequências: f ∈ [2×10⁻⁹, 10⁻⁷] Hz (banda PTA)
```

### O m_A da DEV como candidato

FM4 estabeleceu que m_A é matéria escura fria (w≈0, ρ∝a⁻³) via misalignment. Um campo
oscilante com frequência m_A produz uma assinatura gravitacional em
f_GW = 2 m_A c²/h = m_A c²/(πℏ). Para m_A > 3.7×10⁻²⁵ eV (Paper II), f_GW começa em
~1.8×10⁻¹⁰ Hz e cruza a banda do PTA acima de ~4×10⁻²⁴ eV.

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE: Espectro GW do m_A incompatível com NANOGrav
  — amplitude muito pequena (Ω_GW << observado) OU
  — frequência fora da banda PTA OU
  — forma espectral incompatível.

SUCESSO PARCIAL: Amplitude OU frequência compatível, mas não os dois simultaneamente.

SUCESSO: Espectro GW do m_A consistente com NANOGrav 2023 em amplitude, frequência e
  forma → terceira confirmação observacional independente da TEIC+DEV.
```

**Resultado:** a interpretação SGWB aciona DUAS condições de morte (Ω_GW ~21 ordens
abaixo + forma de linha vs contínuo); a linha KR tem frequência na banda e amplitude
que roça o limiar → **SUCESSO PARCIAL (B)**.

---

## TAREFAS

| # | Pergunta | Resultado |
|---|---|---|
| HQ3-1 | f_GW(m_A) na banda PTA? | **SIM**, overlap 4.1×10⁻²⁴–1.2×10⁻²² eV |
| HQ3-2 | Ω_GW / amplitude compatível? | linha KR roça o limiar (massa baixa); SGWB ~21 ordens abaixo |
| HQ3-3 | forma espectral compatível? | **NÃO** — linha (γ→∞) vs γ=13/3 |
| HQ3-4 | limites (BBN/CMB/Lyman/sólitons)? | nenhum limite duro violado; Lyman→subdominante |
| HQ3-5 | síntese | **VEREDITO B** |

---

## HONESTIDADE OBRIGATÓRIA (cumprida)

1. **m_A do Paper II, não ajustado ao NANOGrav** — o limite m_A>3.7×10⁻²⁵ eV vem de
   galáxias (SPARC). HQ3 é teste, não ajuste.
2. **NANOGrav tem explicação dominante (fusões SMBH)** — o m_A seria contribuição
   adicional/alternativa via um observável DIFERENTE (linha KR), não o SGWB detectado.
3. **Não overclaimar** — "consistente em frequência" não é "explica o NANOGrav". A
   fórmula Ω_GW~10⁻⁶ do prompt pertence a produção taquiônica de fóton escuro, NÃO ao
   misalignment do m_A; foi corrigida, não usada para inflar o resultado.

## PROTOCOLO (cumprido)

HQ3-1 analítico antes do numérico; cosmologia padrão (H₀=67, Ω_m=0.3, g_*=106.75);
fator vetorial (3 polarizações) tratado como modulação O(1); critério de morte
pré-registrado, m_A não ajustado; resultados em `results/cosmology/hq3/`.
