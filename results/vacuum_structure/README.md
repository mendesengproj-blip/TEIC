# results/vacuum_structure — campanha VACUUM_STRUCTURE (jun/2026)

> Charter: `VACUUM_STRUCTURE.md` (raiz). Documentos canônicos produzidos
> junto com a campanha: `TEIC_DEV_CORRESPONDENCE.md` (correspondência
> formal TEIC↔DEV, raiz) e `TEIC_NARRATIVE.md` (reestruturada nas 10
> perguntas).

| Experimento | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **VS5** | constantes de acoplamento dos 4 números puros? | **NEGATIVO** — matches = expectativa de acaso (controle look-elsewhere); α conteria ℏ (contradição dois-andares) | `VS5_coupling_constants.{py,md,json}` |
| **VS1** | condensado de Higgs espontâneo (⟨ρ⟩≠ρ₀ sem vórtice)? | **MORTE DISPARA** — resposta linear escravizada ao drive (ganho 0.43 const., corr −0.51); 3ª via depois de PE2/V4 | `VS1_higgs_condensate.{py,md,json}` |
| **VS2** | transição de fase do vácuo? | **MORTE DISPARA** — crossover suave em todos os parâmetros de ordem; onset de monopólos s≈1 sem salto | `VS2_phase_transition.{py,md,json}` |
| **VS3** | neutrino: quasi-defeito ℤ₂ sem carga de gauge? | **MORTE DISPARA** — marca ℤ₂ de spin-½ (π₁) sem carga topológica B (π₃) desenrola como perturbação trivial; spin-½ estável exige B≠0 (bárion) | `VS3_neutrino.{py,md,json}` |
| **VS4** | três gerações: múltiplos mínimos B=1? | **MORTE DISPARA** — bacia única (10 perfis → M=292.75 a 0.02%, virial-enforced); caminho geodésico sem mínimo interior (VS4b) | `VS4_generations.{py,md,json}`, `VS4b_path_scan.{py,json}` |

## Subprodutos (registrados nos MDs)

- **K_c como critério físico**: o vácuo uniforme só é estável para rigidez
  K > K_c ≈ 8.5 (VS1) — fixa um parâmetro antes livre da ponte.
- **Vácuo vítreo**: quench de desordem forte congela plasma de monopólos
  que não relaxa (VS1/VS2).
- **Notas numéricas para reuso**: `chiral_cool` exige rate ≤ 0.002 em
  dx=0.5/e_sk=4 (0.05 e 0.01 divergem); o estimador discreto de B alia
  com <5 pontos por enrolamento e vaza em dx ≥ 0.5; `evolve_rho` (v3_core)
  vaza massa total com fonte que preenche a caixa (usar `relax_density`);
  varreduras de bacias exigem imposição de virial E2=E4 (Derrick), senão
  otimizações estagnadas contam como falsos mínimos.

## Regras (as de sempre)

Kill criteria pré-registrados no charter antes de rodar; negativos
reportados como vereditos válidos; anti-circularidade (sem números
complexos nos geradores, sem constantes-alvo inseridas); sementes fixas.
