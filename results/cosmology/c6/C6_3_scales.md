# C6-3 — Escala do núcleo do vórtice e separação entre vórtices

> Resultado: as escalas são **kpc-galácticas**, ~100–1000× MAIORES que λ_A=17.3 pc
> de FN4. Estrutura de vórtices **resolvível existe SÓ no topo da janela do Paper II**
> (m_A ~ 10⁻²² eV → d_v ~ 2.5 kpc, dezenas a centenas de vórtices por halo). No piso
> (m_A=3.7×10⁻²⁵ eV) o halo inteiro é ≤1 fragmento coerente — **nenhum vórtice**.
> Números de `c6_scales.py` (verificado: λ_C no piso = 17.28 pc ≈ λ_A de FN4).

---

## Raio do núcleo do vórtice (comprimento de healing / de Broglie)

```
ξ_vortex = ℏ/(m_A v)        (núcleo onde a pressão quântica regulariza n→0)
         = λ_C · (c/v),     λ_C = ℏ/(m_A c) = λ_A de FN4
```

O núcleo do vórtice é o comprimento de Compton **ampliado por c/v ≈ 1500** (v≈200 km/s).
Logo ξ_vortex é ~1500× MAIOR que a escala de blindagem MOND λ_A=17.3 pc — **não** sub-pc.

| m_A [eV] | λ_C = ℏ/m_A c [pc] | ξ_core = ℏ/m_A v [pc] | λ_dB = h/m_A v [pc] |
|---|---|---|---|
| 3.7×10⁻²⁵ (piso) | 17.3 (= λ_A FN4 ✓) | 2.6×10⁴ (26 kpc) | 1.6×10⁵ (163 kpc) |
| 1×10⁻²⁴ | 6.4 | 9.6×10³ (9.6 kpc) | 6.0×10⁴ |
| 1×10⁻²³ | 0.64 | 959 | 6023 |
| 1×10⁻²² | 0.064 | 96 | 602 |
| 1.2×10⁻²² (topo) | 0.053 | 80 | 502 |

(v = 200 km/s, virial típico de halo.)

**Leitura:** no piso, ξ_core (26 kpc) e λ_dB (163 kpc) são MAIORES que uma galáxia → o
halo é uma única "gota" coerente, sem estrutura interna de vórtice. No topo da janela,
ξ_core cai a ~80 pc e λ_dB a ~0.5 kpc → escala de **grânulo/solitón de fuzzy DM**,
sub-galáctica e potencialmente resolvível.

## Separação entre vórtices em halo em rotação (Feynman)

```
n_v = 2Ω/(h/m_A),   Ω = v_rot/R,   d_v = n_v^(−1/2)
N_vort = n_v · πR²   (nº de vórtices atravessando o halo)
```

Galáxia mediana tipo SPARC (v_rot=120 km/s, R_halo=15 kpc):

| m_A [eV] | d_v [kpc] | N_vort | d_v / λ_A |
|---|---|---|---|
| 3.7×10⁻²⁵ (piso) | 45 | 0.35 | 2607 |
| 1×10⁻²⁴ | 27 | 0.94 | 1586 |
| 1×10⁻²³ | 8.7 | 9.4 | 502 |
| 1×10⁻²² | 2.7 | 94 | 159 |
| 1.2×10⁻²² (topo) | 2.5 | 113 | 145 |

(Tendência idêntica para anã v=50/R=5 e espiral massiva v=200/R=30; ver
`C6_3_scales.json`.)

**Leitura:**
- **Piso → 1×10⁻²⁴ eV:** N_vort < 1 → **nenhuma rede de vórtices**; o halo não gira
  rápido o bastante para nuclear sequer um vórtice (toda a rotação cabe no fluxo
  irrotacional de fase). Sem estrutura observável.
- **Topo da janela (10⁻²² – 1.2×10⁻²² eV):** d_v ~ 2.5–2.7 kpc, N_vort ~ 90–380 →
  uma **rede de vórtices resolvível** em escala kpc.

## Comparação de escalas (figura `C6_3_scales.png`)

```
 sub-pc        pc          ~10 pc        100 pc       kpc          10 kpc
   |············|············|·············|············|············|·······>
        λ_C(topo)      λ_A=17.3 pc                 d_v(topo)   ξ_core(piso)
        (0.05 pc)      (FN4 screening)            (2.5 kpc)    (26 kpc)
                       aglom. globular
```

- **d_v ≫ λ_A em TODA a janela** (fator 130–2600). Os vórtices vivem em escala
  **galáctica (kpc)**, MUITO acima da escala de blindagem MOND de FN4 (17.3 pc).
  → cai no ramo **"d_v ≫ λ_A"** de C6-4: assinatura de sub-estrutura de halo, não o
  fenômeno sub-pc das binárias largas.
- Os vórtices NÃO coincidem com λ_A=17.3 pc: a blindagem MOND (λ_C, escala de Compton)
  e a rede de vórtices (ξ, escala de de Broglie) estão separadas por c/v≈1500.

## Regime observável?

**SIM, mas só no topo da janela do Paper II** (m_A ≳ 10⁻²² eV): d_v ~ 2.5 kpc,
ξ_core ~ 80 pc, λ_dB ~ 0.5 kpc — todas em sub-kpc–kpc, regime de sub-estrutura de halo
de fuzzy DM. Para o resto da janela (m_A ≲ 10⁻²³ eV) **não há estrutura resolvível**
(≤1 vórtice por halo). Isto reproduz e quantifica a observação da Fase 2: *"a previsão
de estrutura kpc só vive no topo da janela de massa"* (CONVERGENCE_MAP §2B).

→ Escala potencialmente observável existe (topo da janela). Prosseguir para **C6-4**.
