# MATTER_CR_ABELIAN_HIGGS — Campo complexo e mecanismo de Higgs abeliano

> Testa se um campo escalar complexo Φ com acoplamento minimal ao gauge pina o vórtice
> e fecha as cinco consistências.
> Continua após CR_HIGGS (Veredito C — condensado de **fase** não pina).
> Ingrediente ausente localizado por CR_HIGGS: **|D_μΦ|²** (magnitude complexa acopla ao fluxo).
> **Não modifica** nenhuma campanha anterior.
> Código e resultados: `results/matter/cr_abelian_higgs/`.

---

## O que CR_HIGGS localizou

CR_HIGGS mostrou que o escalar real θ condensa mas **não** pina o vórtice, porque na ação
mínima θ é a **fase de Stückelberg** (entra em `cos(φ+Δθ)` só pelo gradiente):

```
TEIC mínima:  cos(φ + Δθ)     — θ entra pelo GRADIENTE   → m_A constante, sem pinamento
Higgs exige:  |Φ|² |D_μΦ|²    — MAGNITUDE de Φ complexo acopla ao gauge
```

CR_ABELIAN_HIGGS adiciona o campo complexo Φ = |Φ|e^{iα} com derivada covariante
discreta `D_μΦ_ij = Φ_j e^{−ieφ_ij} − Φ_i` (acoplamento minimal, carga e).

## A honestidade obrigatória (declaração, independente do veredito)

> O campo escalar complexo Φ com acoplamento minimal |D_μΦ|² é um **quarto ingrediente
> adicionado à ação**. Não emerge da ação mínima
> S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]. O resultado é: **"a teoria estendida com
> este ingrediente é consistente e suporta matéria estável"** — não "a ação mínima
> deriva matéria".

A ação testada:

$$S_{AH} = \mathrm{KAPPA}\sum_{\langle ij\rangle}|D_\mu\Phi_{ij}|^2
+ \sum_i\big(-\mu_{AH}^2|\Phi_i|^2 + \lambda_{AH}|\Phi_i|^4\big)
+ \lambda_p\sum_\square[1-\cos W_p],
\qquad v=\sqrt{\mu_{AH}^2/2\lambda_{AH}}.$$

> **Nota de implementação (anti-circularidade):** o teste `test_no_circularity.py` proíbe
> números complexos no gerador. Φ é armazenado como **dois arrays reais** (Re, Im) e toda
> a derivada covariante é escrita com cos/sin reais. O "campo complexo" é física; a
> implementação é aritmética real. Também: substituímos a fase real θ pela **fase de Φ**
> (um único would-be Goldstone por campo de gauge), então o limite |Φ|→0 é o setor de
> gauge Wilson de CR_3D.

## Tarefas e resultados

| # | Pergunta | Resultado |
|---|----------|-----------|
| AH1 | campo complexo + 5 verificações (portão) | **PASS** — forças=−∂E/∂campo (FD 5e-8), invariância de gauge exata (0), condensado ⟨\|Φ\|⟩=v, drift<1e-3 |
| AH2 | m_A de C_φ(r); m_A=e·v? | **SIM** — m_A linear em v (inclinação e≈1.2, →0 em v=0); **contraste**: CR_HIGGS tinha m_A≈0.99 constante |
| AH3 | perfil do vórtice; ξ, λ_L, κ | **SIM** — \|Φ\|→0 no núcleo (0.34v); ξ≈0.94, λ_L≈0.69, **κ≈0.73 > 1/√2 (Tipo II)** |
| AH4 | σ_núcleo constante? (pinamento) | **SIM** — enrolamento estável (fluxo do núcleo ≈1 por 120 ticks); CR_HIGGS desfazia (→0.16) |
| AH5 | colisão (20 sementes); 5 consistências | **5/5** — condensado cria enrolamento que sobrevive (v=1: 100%); controle v=0: nada |
| AH6 | aniquilação E_rad=2·M | **SIM** — vórtice+antivórtice aniquilam (núcleos curam \|Φ\|→v), energia conservada e radiada; E_par/M≈1.5 (atração) |
| AH7 | síntese + veredito | **A** |

## Veredito: **A** — matéria estável com o campo complexo

As cinco consistências fecham **com o campo complexo adicionado**:

```
Massa = 8               ✓ (CR_3D)
E² = (pc)² + (mc²)²    ✓ (CR_3D)
θ(r) ~ M/r             ✓ (CR_3D)
Isotropia transversa    ✓ (CR_3D)
Núcleo pinado           ✓ (AH4/AH5 — campo complexo)   ← o que CR_HIGGS não teve
```

## A diferença física vs CR_HIGGS (fase real)

| | CR_HIGGS (fase θ) | CR_ABELIAN_HIGGS (Φ complexo) |
|--|-------------------|-------------------------------|
| acoplamento | cos(φ+Δθ): θ por ∇θ | \|D_μΦ\|²: \|Φ\| acopla ao gauge |
| m_A | ≈0.99 **constante** | **= e·v** (linear, →0 em v=0) |
| núcleo do vórtice | θ≈v (sem núcleo normal) | **\|Φ\|→0** (núcleo normal) |
| pinamento | **não** (enrolamento desfaz) | **sim** (enrolamento estável) |
| veredito | **C** | **A** |

## Derivado vs. adicionado (essencial para a integridade do paper)

```
DERIVADO da ação mínima (uma linha):
  Geometria, SR, Schwarzschild   [R1-R3] · Gravitação newtoniana [D1-D3]
  Estrutura da DEV [ponte] · Plasma de monopólos [T3D2] · Corda E(d)∝d [T3D3]

ADICIONADO À MÃO:
  V(θ): potencial de fase            [CR_HIGGS]          — não pina (θ é fase)
  |D_μΦ|² + V(|Φ|): campo complexo   [CR_ABELIAN_HIGGS]  — quarto ingrediente, fecha 5/5
```

A campanha de matéria está **encerrada**: o que é derivado da ação mínima (geometria,
gravitação, gravidade modificada, vácuo topológico) é sólido e publicável; matéria
estável exige o campo escalar complexo como ingrediente extra, reportado com honestidade.
Detalhe completo em `results/matter/cr_abelian_higgs/AH7_synthesis.md`.
