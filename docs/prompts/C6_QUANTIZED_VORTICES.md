# C6_QUANTIZED_VORTICES — vórtices quantizados e a ponte com Superfluid Dark Matter

> Charter PRÉ-REGISTRADO. Campanha CONVERGENCE, caminho **C6** (rank 3,
> `CONVERGENCE_PATHS.md`). Investiga se os vórtices U(1) da TEIC têm circulação
> FÍSICA quantizada `∮v·dl = n·ℏ/m`, conectando a circulação topológica `∮∇φ·dl=2πn`
> ([DERIVADO]) à estrutura de vórtices do Superfluid Dark Matter de Khoury.
> Resultados em `results/cosmology/c6/`. **NÃO modifica nenhuma campanha anterior**
> (consome m_A do Paper II, λ_A de FN4, o condensado m_A de FM4, ℏ externo).

> ⚠️ **STATUS: PRÉ-REGISTRO escrito ANTES de rodar; depois EXECUTADO (jun/2026).**
> **VEREDITO B — quantização física REAL + previsão condicional, tocando A só no topo
> da janela do Paper II.** C6-1: `v_TEIC=(ℏ/m_A)∇θ` identificável via Candidato 1
> (condensado de onda m_A de FM4, Madelung); Candidato 2 (ferromagneto) dá `v∝∇φ`
> formal mas com `κ=ρ_s/M` clássico, **sem ℏ** → rejeitado. C6-2: `κ=ℏ/m_A` por
> construção; `∮v·dl=n·h/m_A`. C6-3: ξ_core≈80 pc, d_v≈2.5 kpc no topo da janela
> (m_A≳10⁻²² eV); no piso ≤1 vórtice/halo. Sempre `d_v≫λ_A=17.3 pc`. C6-4: previsão
> falsificável de sub-estrutura de halo em kpc, **condicional** ao topo da janela e a
> m_A fração subdominante; co-implicada com FN4. ℏ **externo** (não derivado).
> A circulação física deixa de ser [ESPECULATIVO] → [DERIVADO em forma] no setor m_A.
> Ver `results/cosmology/c6/C6_5_synthesis.md`. Predições/mortes fixadas ANTES de medir.

---

## CRITÉRIO DE MORTE (PRÉ-REGISTRADO)

```
MORTE (C): não existe nenhuma relação v_TEIC ∝ ∇φ identificável na estrutura da
  TEIC — a circulação topológica 2πn não se traduz em circulação física com
  unidades sensatas. NÃO inventar um terceiro candidato para escapar.

SUCESSO PARCIAL (B): a relação existe mas a escala (núcleo/separação) cai fora do
  regime observável OU só num canto da janela de massa.

SUCESSO (A): v_TEIC=(ℏ/m_A)∇φ identificável, escala em regime observável
  (sub-kpc a Mpc), previsão nova e falsificável.
```

## TAREFAS (decisão sequencial — C6-1 é o teste)

1. **C6-1** (decisivo): testar dois candidatos JÁ existentes — (1) corrente do campo
   m_A (FM4/FN3), (2) corrente do ferromagneto causal (E1/HQ2). Se nenhum der
   `v∝∇φ` limpo → morte. → `results/cosmology/c6/C6_1_velocity_field.md`
2. **C6-2** (se C6-1 ✓): extrair κ estruturalmente, comparar com ℏ/m_A (ℏ externo).
   → `C6_2_kappa.md`
3. **C6-3** (se C6-2 ✓): ξ_vortex, d_v para galáxia SPARC típica; comparar com
   λ_A=17.3 pc. → `C6_3_scales.{md,json,png}`
4. **C6-4** (se escala observável): previsão falsificável; elo com FN4.
   → `C6_4_prediction.md`
5. **C6-5**: síntese honesta + veredito A/B/C. → `C6_5_synthesis.md`

## PROTOCOLO / HONESTIDADE

- ℏ e m_A são **inputs DECLARADOS** (ℏ externo; m_A do Paper II, não recalibrado).
  C6 testa **consistência**, não deriva ℏ.
- Usar só estruturas existentes (m_A de FM4/FN3, ferromagneto de E1/HQ2) — sem campo
  novo, sem motor Monte Carlo novo (maioria analítica).
- Critério de morte pré-registrado: ausência de v∝∇φ = C.

## RESULTADO (resumo — detalhe em `results/cosmology/c6/`)

```
C6-1  v=κ∇φ?           SIM (Candidato 1 m_A, Madelung) — Cand. 2 rejeitado (κ clássico)
C6-2  κ = ℏ/m_A        SIM (por construção); ∮v·dl = n·h/m_A
C6-3  ξ≈80 pc, d_v≈2.5 kpc (topo); ≤1 vórtice/halo (piso); d_v≫λ_A sempre
C6-4  previsão SIM (condicional ao topo da janela); compatível com FN4
VEREDITO: B (físico real + previsão condicional), toca A só em m_A≳10⁻²² eV
```

**Terceiro pilar da conexão TEIC↔Khoury** (junto de deep-MOND L∝X^{3/2} e do
Goldstone χ∥~h^{−1/2}): os vórtices físicos `∮v·dl=n·h/m_A` moram no setor massivo
m_A (superfluido-ℏ genuíno), **não** no vácuo de orientação clássico — fechando a
Verificação 3 da Fase 2 (CONVERGENCE_MAP §2B).
