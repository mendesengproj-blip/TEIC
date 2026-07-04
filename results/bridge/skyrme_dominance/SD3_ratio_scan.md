# SD3 — K/S em função de (d, ρ, tipo de link)

> Gerador: `SD3_ratio_scan.py` → `SD3_ratio_scan.json` + `.png`.
> Pré-registro: adendo itens 2, 3, 5, 9. Sprinklings de Poisson REAIS em
> diamante causal de M³⁺¹ com relação de cobertura (links) exata, 20 sementes.

## Dimensão: a fração cresce, o gap não fecha

Fração de canal cruzado por link κ(e) = 1 − Σ(e^μ)⁴, MC 4·10⁵ direções:

| d | κ medido | 1 − 3/(d+2) | limite de campo 1−1/d | gap líquido (1+2/d) |
|---|---|---|---|---|
| 1 | 0.0000 | 0 | 0 | 3.0 |
| 2 | 0.2500 | 1/4 | 1/2 | 2.0 |
| 3 | 0.4003 | **2/5** | **2/3** | **5/3** |
| 4 | 0.5004 | 1/2 | 3/4 | 3/2 |
| 5 | 0.5711 | 4/7 | 4/5 | 7/5 |
| 8 | 0.6999 | 7/10 | 7/8 | 5/4 |

Ambas as razões crescem com d e tendem a 1 — mas o gap líquido
3S−2K ≥ (1+2/d)·S nunca cai abaixo de S (limite d→∞). **Crescer com d não
compra dominância em dimensão nenhuma** (SD1, item 3). E nós estamos em d=3,
fixado por DS1–DS3.

## Densidade: não move absolutamente nada

Sprinklings em diamante causal, links = relações de cobertura:

| ρ | links/realização | κ₃ causal | κ₃ tipo-espaço | r₄(B)/r₄(A) medido |
|---|---|---|---|---|
| 10 | 25 | 0.415 ± 0.009 | 0.400 | 0.63 ± 0.06 |
| 50 | 376 | 0.398 ± 0.002 | 0.399 | 0.552 ± 0.007 |
| 200 | 4 112 | 0.3996 ± 0.0005 | 0.3996 | 0.560 ± 0.003 |
| 1000 | 60 380 | 0.4000 ± 0.0001 | 0.4003 | 0.555 ± 0.001 |

- **κ₃ = 2/5 em todo ρ** — a isotropia espacial de Poisson é exata por
  simetria, independente da densidade; só o ruído ∝ N_links^{−1/2} muda.
- **r₄(B)/r₄(A) = 5/9 em todo ρ** com as direções MEDIDAS dos links reais —
  a previsão SC2 vale na rede de verdade, não só na medida idealizada.
- **Links causais vs pares tipo-espaço: idênticos em κ₃** (0.4000 vs 0.4003
  em ρ=1000). A componente temporal dominante dos links causais aparece só na
  fração 4-componente κ₄ (0.47→0.55 com ρ, vs 0.5 isotrópico) — e essa
  quantidade não entra no quártico do sóliton, que vive nas direções
  espaciais.

## Veredito SD3: **K/S constante em ρ; cresce com d mas fica abaixo de 2/3 — e o 2/3 não bastaria**

Nenhum regime medido se aproxima da dominância. O parâmetro que faz a razão
crescer (d) está fixado em 3 pela própria teoria, e mesmo seu limite d→∞ não
flipa o sinal (SD1). MORTE PARCIAL no sentido do pré-registro — o parâmetro é
d, o limite assintótico é K/S → 1⁻ com gap líquido → S — mas sem caminho:
o crescimento nunca cruza o limiar em dimensão finita nem infinita.

Reprodução: `python SD3_ratio_scan.py` (~3 min; ρ=1000 domina o custo).
