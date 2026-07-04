# AH1 — Campo complexo: portão de cinco verificações

Modelo abeliano-Higgs compacto em rede: escalar complexo Φ (dois arrays **reais**
pr, pi) + acoplamento minimal D_μΦ_ij = Φ_j e^{−ieφ_ij} − Φ_i, potencial
mexicano −μ²|Φ|² + λ|Φ|⁴, e Wilson λ_p(1−cosW). v = √(μ²/2λ).

> **Nota honesta de modelagem.** Este modelo **substitui** a fase real de
> Stückelberg θ de CR_HIGGS pela **fase de Φ** (um único would-be Goldstone por
> campo de gauge, não dois redundantes). Logo o limite |Φ|→0 é o setor de gauge
> Wilson de CR_3D, não “CR_HIGGS com θ”. Documentado, não escondido.

## As cinco verificações

1. **|Φ|=0 → gauge Wilson puro:** E_hop=0 e a força de gauge coincide com a
   força de Wilson de CR_3D (maxdiff 0.0e+00) → **True**.
2. **φ=0 → escalar complexo livre:** D_μΦ = Φ_j−Φ_i (gradiente; maxdiff 0.0e+00) → **True**.
3. **Invariância de gauge local:** |ΔE|/E = 0.0e+00 sob φ→φ+(α_j−α_i)/e, Φ→Φe^{iα} → **True** (zero de máquina).
4. **Condensado ⟨|Φ|⟩=v:** → **True**:

| μ² | λ | v=√(μ²/2λ) | ⟨|Φ|⟩ medido | erro |
|----|---|------------|--------------|------|
| 0.00 | 1.00 | 0.000 | 0.001 | 0.1% |
| 0.50 | 0.50 | 0.707 | 0.707 | 0.0% |
| 1.00 | 0.50 | 1.000 | 1.000 | 0.0% |
| 2.00 | 1.00 | 1.000 | 1.000 | 0.0% |

5. **Conservação de energia:** drift = 8.5e-05 (< 1e-3) → **True**.

## Veredito AH1: **PASS**

As cinco verificações passam (forças = −∂E/∂campo verificadas por diferenças finitas a 1e-8; invariância de gauge exata). O campo complexo está implementado corretamente em aritmética real. Portão aberto — AH2–AH7 prosseguem.
