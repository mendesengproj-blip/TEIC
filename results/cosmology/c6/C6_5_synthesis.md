# C6-5 — Síntese honesta e veredito

> **VEREDITO B (quantização física REAL + previsão condicional) — tocando A só no
> topo da janela do Paper II.** A relação `v_TEIC = (ℏ/m_A)∇θ` é identificável e
> estrutural (Madelung do condensado m_A de FM4), com `κ = ℏ/m_A` por construção e
> circulação física `∮v·dl = n·h/m_A`. A escala de vórtices cai em regime observável
> (kpc) **só** no topo da janela (m_A ≳ 10⁻²² eV), e só como fração subdominante da DM.
> A circulação **topológica** 2πn já era [DERIVADO]; C6 promove a parte **física** de
> [ESPECULATIVO] para [DERIVADO em forma, condicional em escala].

---

## Quadro-resumo

```
C6-1 (campo de velocidade):
  v_TEIC = κ∇φ identificável?              SIM
  Candidato usado:                          m_A (condensado de onda, Madelung)
  Candidato rejeitado:                      ferromagneto (κ clássico, sem ℏ)

C6-2 (κ vs ℏ/m_A):
  κ_TEIC bate com ℏ/m_A?                   SIM (por construção, não ajuste)
  Valor de κ:                               κ = ℏ/m_A ; quantum ∮v·dl = n·h/m_A
                                            (h/m_A: 3.1×10²⁴ – 1.0×10²⁷ m²/s na janela)

C6-3 (escalas):
  ξ_vortex (núcleo) =                       80 pc (topo) … 26 kpc (piso)   [v=200 km/s]
  λ_dB =                                    0.5 kpc (topo) … 163 kpc (piso)
  d_v (separação, halo mediano) =           2.5 kpc (topo) … 45 kpc (piso)
  d_v / λ_A (FN4) =                         130 – 2600  (sempre ≫ λ_A=17.3 pc)
  Regime observável?                        SIM, só no topo da janela (m_A≳10⁻²² eV);
                                            piso → N_vort ≤1/halo, sem rede

C6-4 (previsão):
  Previsão formulável e falsificável?       SIM (condicional ao topo da janela)
  Compatível com FN4 (λ_A)?                SIM — fenômenos distintos (d_v≫λ_A,
                                            ramo "sub-estrutura de halo kpc"),
                                            co-implicados pelo mesmo m_A
```

## Veredito (template A/B/C)

```
[~] B — QUANTIZAÇÃO FÍSICA REAL, ESCALA OBSERVÁVEL SÓ NO TOPO DA JANELA
    v_TEIC = (ℏ/m_A)∇θ identificado estruturalmente (Madelung do condensado m_A);
    κ=ℏ/m_A por construção; ∮v·dl = n·h/m_A (forma idêntica a Khoury/Onsager-Feynman).
    A circulação FÍSICA deixa de ser [ESPECULATIVO]: é [DERIVADO em forma] no setor
    massivo. PORÉM a previsão de estrutura observável (kpc) é CONDICIONAL:
      • vive só no topo do Paper II (m_A≳10⁻²² eV); m_A≲10⁻²³ eV ⇒ ≤1 vórtice/halo;
      • m_A é fração subdominante (FM4/Lyman-α) ⇒ assinatura diluída;
      • ℏ é input externo (não derivado).
    → Registrado como resultado teórico SÓLIDO + previsão condicional falsificável,
      não como "estrutura kpc grandiosa garantida".
    → Toca o veredito A apenas no canto m_A≳10⁻²² eV da janela.

[ ] A — exigiria a escala observável em TODA (ou na maior parte da) janela. Não é o
        caso: só no topo, e como fração subdominante.
[ ] C — DESCARTADO: o campo de velocidade v∝∇φ EXISTE (candidato 1). Não há morte.
```

## O que C6 acrescenta ao programa

1. **Fecha a Verificação 3 da Fase 2.** O CONVERGENCE_MAP §2B deixou a circulação
   física `nℏ/m` como [ESPECULATIVO] ("depende de o vácuo ser um superfluido-ℏ genuíno,
   que a TEIC nua não é"). C6 resolve: **o vácuo de orientação nu NÃO é** (candidato 2,
   κ clássico) — mas **o setor massivo m_A É** um superfluido-ℏ genuíno (candidato 1,
   κ=ℏ/m_A). A ponte com Khoury no setor de **vórtices** existe, e mora no m_A, não no
   ferromagneto.

2. **Terceiro pilar da conexão TEIC↔Khoury**, ao lado de:
   - deep-MOND `L∝X^{3/2}` compartilhado [DERIVADO] (CONVERGENCE_MAP §2B Ver.1);
   - Goldstone do ferromagneto = mecanismo de Khoury, `χ∥~h^{−1/2}` (FM2-1, Ver.2);
   - **agora: vórtices quantizados `∮v·dl=n·h/m_A` no condensado m_A (C6).**

3. **Terceiro front observacional**, ao lado de BTFR (galáxias) e FN4 (binárias largas
   sub-pc): sub-estrutura de vórtice em escala kpc, co-implicada com FN4 pelo mesmo m_A.

## O que C6 NÃO faz (limites honestos)

- **Não deriva ℏ** (input externo declarado; consistente com T3C/VS5).
- **Não garante a estrutura kpc** — ela é condicional ao topo da janela e a m_A ser
  fração ≳0.1 da DM.
- **Não resolve S8** (nem tentou; FM4 já fechou S8 como morte em todos os setores).
- **Não muda nenhuma campanha anterior** — consome m_A (Paper II), ℏ (externo), λ_A
  (FN4), o condensado m_A (FM4); não recalibra nada.

## Status final das circulações

| Circulação | Antes de C6 | Depois de C6 |
|---|---|---|
| Topológica `∮∇φ·dl = 2πn` | [DERIVADO] | [DERIVADO] (inalterado) |
| Física `∮v·dl = n·h/m_A` (forma) | [ESPECULATIVO] | **[DERIVADO em forma]** (setor m_A) |
| Estrutura kpc nos halos | [ESPECULATIVO] | **[CONDICIONAL]** (só topo da janela, fração subdominante) |
| Valor absoluto de ℏ | externo | externo (inalterado) |
