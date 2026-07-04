# C6_QUANTIZED_VORTICES — vórtices quantizados e a ponte com Superfluid DM

Investiga se os vórtices U(1) da TEIC têm **circulação física quantizada**
`∮v·dl = n·h/m_A` (análoga aos vórtices de Khoury), e se isso prevê estrutura
observável nos halos. Campanha CONVERGENCE, caminho **C6** (rank 3).

**Pré-registro de morte:** ausência de qualquer `v_TEIC ∝ ∇φ` identificável na
estrutura existente ⇒ Veredito C. Não inventar um terceiro candidato.

## Veredito: **B** (quantização física REAL + previsão condicional), tocando A só no topo da janela do Paper II

- `v_TEIC = (ℏ/m_A)∇θ` **existe** — via Candidato 1 (condensado de onda m_A de FM4,
  descrição de Madelung). Candidato 2 (ferromagneto E1/HQ2) dá `v∝∇φ` formal mas com
  `κ=ρ_s/M` **clássico, sem ℏ** → rejeitado para quantização física.
- `κ = ℏ/m_A` por construção; circulação `∮v·dl = n·h/m_A` (forma idêntica a Khoury).
- Escala de vórtices: **kpc** (d_v≈2.5 kpc, ξ≈80 pc) — observável **só no topo da
  janela** (m_A≳10⁻²² eV); no piso, ≤1 vórtice/halo. Sempre `d_v ≫ λ_A=17.3 pc` (FN4).
- Previsão falsificável formulada (sub-estrutura de halo em kpc), **condicional** ao
  topo da janela e a m_A ser fração subdominante da DM. ℏ é input **externo**.

## Documentos

| arquivo | conteúdo |
|---|---|
| `C6_1_velocity_field.md` | **teste decisivo**: v=κ∇φ via m_A (sim) vs ferromagneto (não) |
| `C6_2_kappa.md` | κ=ℏ/m_A estrutural; ∮v·dl=n·h/m_A; ℏ externo declarado |
| `C6_3_scales.md` | ξ_core, λ_dB, d_v, N_vort vs m_A; comparação com λ_A=17.3 pc |
| `C6_4_prediction.md` | previsão condicional (kpc, sub-estrutura de halo) + elo com FN4 |
| `C6_5_synthesis.md` | síntese + veredito A/B/C |
| `c6_scales.py` | calculadora analítica das escalas (verificável) |
| `C6_3_scales.json` | números brutos |
| `C6_3_scales.png` | figura log-log das escalas vs m_A |

Reproduzir: `python results/cosmology/c6/c6_scales.py` (analítico, ~2 s; sem motor
Monte Carlo novo). Verificação âncora embutida: λ_C(m_A=piso)=17.28 pc ≈ λ_A de FN4.

## Anti-circularidade

ℏ e m_A são **inputs declarados** (ℏ externo; m_A da janela do Paper II
[3.7×10⁻²⁵, 1.2×10⁻²²] eV, não recalibrado). C6 testa **consistência** da estrutura de
vórtices com o ℏ conhecido — **não** deriva ℏ. Nenhuma campanha anterior é modificada;
C6 consome m_A (Paper II), λ_A (FN4) e o condensado m_A (FM4).
