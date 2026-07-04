# FN3b — DEV com segunda escala para a matéria escura

Segue FN3 (que fechou em Verdict B: Ω~0.12 alcançável com f_A~10¹⁷ GeV **livre**).
FN3b pergunta: a DEV **fornece** essa escala GUT naturalmente, sem mexer em galáxias?
Três caminhos, com critério de morte por caminho.

Charter: [`FN3b_SECOND_FIELD.md`](../../../FN3b_SECOND_FIELD.md) (raiz do TEIC).

## Veredito: **um caminho viável (A-massa-livre ≡ C), mas NÃO derivado da DEV**

As rotas que usam os campos **existentes** da DEV morrem: **B** (modos de A_μ acoplados
pelo vev de Stückelberg) e **A-como-slip-mediator** (energia escura + overclosure ×8×10⁷).
A única rota viável **acrescenta um campo/escala novos** (m~2×10⁻²¹ eV, f~10¹⁷ GeV) e
ainda pede fine-tuning leve (θ₀~4×10⁻³ = 0.7% do natural medido na rede). A escala GUT
da DM **continua não-derivada** — confirma e refina o Verdict B de FN3.

## Protocolo seguido

**FN3b-0 (gate analítico) rodou ANTES de qualquer código** e identificou o caminho a
focar (A/C compartilhado), matando B e A-slip analiticamente.

## Arquivos

| Item | Arquivo |
|---|---|
| Gate analítico (obrigatório 1º) | [`FN3b_0_estimate.md`](FN3b_0_estimate.md) |
| Caminho A (campo θ) | [`A_theta_candidate.md`](A_theta_candidate.md) |
| Caminho B (dois modos A_μ) | [`B_two_modes.md`](B_two_modes.md) |
| Caminho C (escalar extra χ) | [`C_extra_scalar.md`](C_extra_scalar.md) |
| Síntese + veredito | [`FN3b_synthesis.md`](FN3b_synthesis.md) |
| Motor de física | `fn3b_core.py` |
| Código do caminho promissor + figura | `FN3b_path_AC.py` → `.json` + `.png` |

## Reproduzir

```bash
cd TEIC/results/cosmology/fn3b
python fn3b_core.py        # self-test (relic + epoch + overclosure + Stueckelberg vev)
python FN3b_path_AC.py     # lattice theta0 (orientation_core) + janela viável + figura
```

## Números-chave

```
θ₀_natural (rede E1, O(3) desordenado):   0.58  (rms de componente, = 1/√3)
θ₀_req no ponto viável (m=2e-21 eV):       3.9×10⁻³   (fine-tune = 0.7% do natural)
A como slip mediator (m=6.4e-30 eV):       z_osc=190 (energia escura) + overclosure ×8×10⁷ → MORTE
B (vev de Stückelberg v=m_A/e):            3.3×10⁻³¹ GeV → 48 ordens curto → MORTE
C (χ=|⟨n⃗⟩|):                               modo radial ~M_Pl, não 10⁻²¹ eV → identificação falha
```
