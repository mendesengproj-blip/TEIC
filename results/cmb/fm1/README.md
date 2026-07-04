# results/cmb/fm1 — campanha FM1_CMB_S8 (jun/2026)

> Charter: `FM1_CMB_S8.md` (raiz). Primeira campanha do setor CMB. Pergunta: a DEV
> (a₀∝H(z)) explica a tensão S8 (KiDS σ8≈0.75 vs Planck 0.83)? a₀ FIXO de SPARC
> (1.2×10⁻¹⁰ m/s²) ⇒ é **previsão**, não ajuste. **NÃO modifica campanhas anteriores.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **FM1-1** | μ(k,z) analítico, sinal de B_ε? | μ=ν(k/k_*(z)) da Poisson MOND; B_ε invariante no quase-estático; **μ≥1 (MOND realça)** | `FM1_1_perturbations.md` |
| **FM1-2** | módulo "CLASS", limite ΛCDM? | CAMB+ODE de crescimento (CLASS indisp.); **a₀→∞ ⇒ μ=1 exato** | `FM1_2_class_impl.{py,json}` |
| **FM1-3** | σ8_DEV < σ8_ΛCDM? | **NÃO — σ8_DEV=101 ≫ 0.81; S8_DEV=103.5 vs KiDS 0.766** | `FM1_3_sigma8.{py,md,json,png}` |
| **FM1-4** | C_ℓ^φφ vs Planck? | **NÃO** — realce de crescimento ~10⁴ (slip OK, crescimento não) | `FM1_4_lensing.md` |
| **FM1-5** | ISW vs obs? | **NÃO** — crescimento não estagna em z<1 | `FM1_5_isw.md` |
| **FM1-6** | síntese | **C — MORTE: DEV não reduz σ8 (piora a tensão)** | `FM1_6_synthesis.md` |

Motor: `FM1_2_class_impl.py` (`LCDMBaseline` = CAMB P(k)/σ8; `DevCosmology` = μ(k,z)
MOND da aceleração viva do modo + ODE de crescimento auto-consistente; `mu_MG`,
`Sigma_MG`=(1+η)/2 na interface `mg_parametrization` do CLASS; `sigma_R`).
Self-test/gate: `python FM1_2_class_impl.py`.

## Resultado de uma linha

**A DEV NÃO explica a tensão S8 — ela a piora.** A DEV é tipo-MOND ⇒ μ(k,z)≥1
(realça a gravidade). Como a aceleração peculiar de modos lineares é g~3×10⁻¹³ m/s²
≪ a₀ (todo modo cosmológico é **MOND profundo**, pela coincidência a₀≈cH₀/2π), o
crescimento dispara: σ8_DEV ≫ σ8_ΛCDM em todo z ⇒ **Veredito C** (critério de morte
acionado). f(z), C_ℓ^φφ e ISW vão todos na mesma direção. A premissa do charter
("gravidade mais fraca → σ8 menor") tem sinal **errado** para MOND. A previsão
observacional válida da DEV permanece **BTFR** (galáxias), não o CMB.

## Honestidade / engenharia

- **CLASS (`classy`) indisponível no host Windows** (precisa de build C). Usou-se
  **CAMB 1.6.6** para o baseline ΛCDM (σ8=0.811, S8=0.831 — reproduz Planck) + a
  ODE de crescimento DEV. Para σ8/S8/f(z) isso equivale a um run
  `mg_parametrization`; declarado, não escondido.
- **FM1-4/5 são ordem-de-grandeza** ancorados no realce de FM1-3 (não espectros
  Boltzmann completos — exigiriam CLASS). Direção robusta; números exatos ficariam
  para CLASS.
- **Robustez:** δ'' + ... − (3/2)Ωm μ δ = 0 é monótona em μ ⇒ **qualquer μ≥1 dá
  σ8_DEV≥σ8_ΛCDM**, independente de ν(y), de a₀ e de s (½ ou 1). A morte é
  estrutural, não numérica. σ8≈101 é runaway (linear quebra); só o sinal importa
  para o critério de morte.
- **a₀ NÃO ajustado ao CMB** (valor SPARC) ⇒ teste genuíno; a DEV falha no setor de
  perturbações cosmológicas. Reportado como falsificação parcial.
- **Sinal de B_ε (E2):** μ é invariante no crescimento quase-estático (ω=0); σ8
  idêntico para os dois sinais.

## Regras (as de sempre)

Kill criterion pré-registrado ("σ8_DEV ≥ σ8_ΛCDM = Veredito C", pontuado como
escrito — acionado, sem ajuste de parâmetros para escapar); gate de engenharia
(FM1-2: limite ΛCDM a₀→∞ ⇒ μ=1 antes de qualquer σ8); direção física honesta
declarada ANTES dos números (FM1-1: MOND realça, charter tem sinal errado);
limitações reportadas (CLASS ausente→CAMB; FM1-4/5 ordem-de-grandeza); a₀ de
galáxias, não do CMB (previsão, não ajuste); 20 realizações numéricas para o erro.
