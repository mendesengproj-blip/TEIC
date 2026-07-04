# Caminho A — o campo θ como candidato ao misalignment

> `fn3b_core.py` + `FN3b_path_AC.py` → `FN3b_path_AC.json/.png`. θ₀ natural medido na
> rede de E1 (`orientation_core`); janela viável sob Ω=0.12 ∧ frio ∧ Lyman-α ∧ não-overclosure.

## θ₀ natural — medido na rede (anti-circular)

No vácuo de orientação O(3) de E1 (rede cúbica periódica 12³, fase desordenada),
medi a amplitude rms de flutuação de orientação:

```
   J=0.00:  order_param=0.013   rms_component=0.584   θ₀(ângulo/π)=0.549
   J=0.04:  order_param=0.009   rms_component=0.584   θ₀(ângulo/π)=0.549
   J=0.08:  order_param=0.012   rms_component=0.582   θ₀(ângulo/π)=0.549
```

**θ₀_natural ≈ 0.58** (a rms de uma componente de spin no vácuo desordenado, = 1/√3
para O(3) aleatório). O parâmetro de ordem ~0.01 confirma a fase desordenada. Ou seja:
a amplitude inicial **natural** de θ no vácuo primordial é **O(1)** — como esperado
para flutuação máxima de orientação. Isto **aterra θ₀ na rede**, não numa suposição.

## A questão: que m_θ, e o θ₀ exigido por Ω=0.12

θ₀ exigido para Ω=0.12 é θ₀_req = 8.2×10⁻³·(m_θ/10⁻²²)^{−1/4}. Cruzando com as duas
escalas físicas externas (época de frio; Lyman-α):

```
   m_θ [eV]    θ₀_req     z_osc       frio(z>1100)   Lyα-100%(m>2e-21)
   6.4e-30     0.52       190         NÃO (DE)        NÃO     ← bound do slip mediator
   1.0e-28     0.26       1.1e3       SIM (marginal)  NÃO
   1.0e-22     8.2e-3     1.6e6       SIM             NÃO
   2.0e-21     3.9e-3     7.0e6       SIM             SIM     ← ponto de tuning mínimo
   1.0e-20     2.6e-3     1.6e7       SIM             SIM
```

## O θ **da DEV** (slip mediator) — MORTE

Se θ é o escalar de slip da DEV (m_θ ≲ 6.4×10⁻³⁰ eV), ele:
- **oscila tarde demais**: z_osc = 190 < 1100 → fica frozen como **energia escura**
  (w=−1) através da recombinação e da formação de estrutura — **não é matéria fria**;
- **sobre-fecha**: com θ₀ natural ~0.58 (ou 1), ρ_frozen/ρ_crit ≈ **8×10⁷** —
  sobre-fecha o universo por ~8 ordens; só não sobre-fecha se **θ₀ < 1.1×10⁻⁴**.

Ou seja, o θ existente da DEV exige **θ₀ < 10⁻⁴** (muito além da linha de morte 10⁻³)
**e** ainda assim seria energia escura, não DM. **Critério de morte A disparado.**

## O θ com **massa livre** — viável, mas é uma nova escala

Se a θ se permite uma massa **livre** mais pesada (m_θ ≳ 2×10⁻²¹ eV, para ser
Lyman-α-safe como 100% da DM), então no ponto de tuning mínimo (m_θ = 2×10⁻²¹ eV):

```
   θ₀_req = 3.9×10⁻³      (ACIMA da linha de morte 10⁻³ → não morto)
   θ₀_req / θ₀_natural = 6.6×10⁻³   → tuning de ~0.7% da amplitude natural
   frio antes da recombinação: SIM ;  Lyman-α-safe: SIM (no piso)
```

**Fine-tuning honesto:** o θ₀ exigido (3.9×10⁻³) é **0.66% do θ₀ natural** medido na
rede (0.58). Isto é **fine-tuning leve** — não a morte catastrófica (<10⁻³ absoluto),
mas também **não uma "previsão natural"**: a amplitude inicial precisa ser ajustada a
~10⁻² do seu valor típico. E essa massa (≳2×10⁻²¹ eV) está **acima do teto do vetor do
Paper II (1.2×10⁻²²)** e **não é o slip mediator** → é uma **nova escala**, fisicamente
o Caminho C.

## Veredito A

```
θ₀ necessário (ponto viável):       3.9×10⁻³  (m_θ=2×10⁻²¹ eV)
Fine-tuning necessário:              ~0.7% da amplitude natural (θ₀_nat=0.58)
Mecanismo natural para θ₀?           NÃO para o θ da DEV (slip → DE + overclosure, morte);
                                     PARCIAL para massa livre (tuning leve + nova escala)
Veredito A:   o θ EXISTENTE da DEV = MORTE (energia escura, θ₀<10⁻⁴);
              o θ com MASSA LIVRE = viável com tuning leve, mas ≡ Caminho C (nova escala).
```
