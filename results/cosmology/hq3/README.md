# HQ3 — Espectro de GW do m_A vs NANOGrav 2023

Campanha de cosmologia que segue FM4 (m_A é DM fria, w=0) e FN3 (Ω_{m_A}~0.12
alcançável). HQ3 pergunta o **observacional**: o condensado oscilante de m_A imprime
um sinal na banda dos Pulsar Timing Arrays? É consistente com o fundo de GW detectado
pelo NANOGrav em 2023 (arXiv:2306.16213)?

Charter: [`HQ3_NANOGRAV.md`](../../../HQ3_NANOGRAV.md) (raiz do TEIC).

## Veredito: **B** — frequência na banda, mas não é o SGWB do NANOGrav

A **frequência** f_GW = 2m_A c²/h das massas do Paper II cai na banda do PTA
(overlap 4.1×10⁻²⁴–1.2×10⁻²² eV). O **mesmo** m_A produz uma oscilação métrica
monocromática de Khmelnitsky–Rubakov cuja amplitude **roça** o limiar do PTA na ponta
de massa baixa (se 100% da DM local). Mas o fundo estocástico que o NANOGrav detectou
(γ=13/3, banda larga) **não** é o m_A: um condensado homogêneo não irradia gráviton
on-shell, o SGWB fica ~21 ordens abaixo, e o m_A é uma **linha**, não um contínuo.
Lyman-α (FM4/FN3) ainda empurra o m_A para subdominante, rebaixando a amplitude.
Nenhum limite duro violado. Critério de morte: acionado para a interpretação SGWB,
**não** para a linha KR → **B**.

## Arquivos

| Tarefa | Relatório | Código | Saída |
|---|---|---|---|
| HQ3-1 frequência | [`HQ3_1_frequency.md`](HQ3_1_frequency.md) | `HQ3_1_frequency.py` | `.json` + `.png` |
| HQ3-2 amplitude | [`HQ3_2_amplitude.md`](HQ3_2_amplitude.md) | `HQ3_2_amplitude.py` | `.json` + `.png` |
| HQ3-3 forma espectral | [`HQ3_3_spectrum.md`](HQ3_3_spectrum.md) | `HQ3_3_spectrum.py` | `.json` + `.png` |
| HQ3-4 limites | [`HQ3_4_constraints.md`](HQ3_4_constraints.md) | `HQ3_4_constraints.py` | `.json` + `.png` |
| HQ3-5 síntese | [`HQ3_5_synthesis.md`](HQ3_5_synthesis.md) | — | — |
| motor de física | — | `hq3_core.py` | — |

## Reproduzir

```bash
cd TEIC/results/cosmology/hq3
python hq3_core.py            # self-test do motor
python HQ3_1_frequency.py     # f_GW(m_A) vs banda PTA + figura
python HQ3_2_amplitude.py     # linha KR + SGWB vs NANOGrav + figura
python HQ3_3_spectrum.py      # forma espectral (linha vs γ=13/3) + figura
python HQ3_4_constraints.py   # BBN / CMB / Lyman-α / sólitons + figura
```

Cosmologia (fixa, charter): H₀=67, Ω_m=0.3, g_*=106.75. NANOGrav (COMPARISON ONLY):
A_yr=2.4×10⁻¹⁵, γ=13/3, banda [2×10⁻⁹, 10⁻⁷] Hz. Janela de massa do Paper II:
3.7×10⁻²⁵–1.2×10⁻²² eV. ρ_DM local = 0.4 GeV/cm³.

## Números-chave

```
f_GW = 2 m_A c²/h:        m_A∈[4.1e-24, 1.2e-22] eV → f_GW∈[2, 58] nHz (NA BANDA)
Linha KR (Ψ_c=πGρ/ω²):   ~10⁻¹⁴ (m=4e-24) a ~10⁻¹⁷ (m=1e-22), 100% DM local
Ψ_c / h_c(NANOGrav):     ~0.25 (1ºpr) a ~1 (KR-lit) na ponta de massa baixa
SGWB que se propaga:     teto Ω_GW ~ 1.4e-29  vs  NANOGrav 8.1e-9  → ~21 ordens abaixo
Forma:                   linha (γ→∞, Δf/f~10⁻⁶)  vs  γ=13/3 (banda larga, SMBH)
Lyman-α / sólitons:      banda subdominante (rebaixa amplitude) / não afetada
```
