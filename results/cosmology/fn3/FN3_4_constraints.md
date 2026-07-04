# FN3-4 — Comparação com limites observacionais

> `FN3_4_constraints.py` → `FN3_4_constraints.json` + `FN3_4_constraints.png`.
> Para cada (m_A, f_A): Ω≤0.12, Lyman-α (k~3/Mpc), subdominância em z>z_eq, Jeans z~0.
> Reusa a transfer de Lyman-α de FM4 (limite = COMPARISON ONLY).

## 1. Ω ≤ 0.12 (não super-produzir DM)

A linha de Ω=0.12 corre por f_A=(1–4)×10¹⁷ GeV (FN3-1). Acima dela (f_A≳10¹⁷·⁵ GeV
→ Ω>0.12) há **sobreprodução** — excluído. Abaixo (f_A<10¹⁷ GeV → Ω<0.12) m_A é DM
**subdominante** — permitido, coexistindo com outra DM. **Não há sobreprodução
inevitável**: o critério Ω≤0.12 é satisfeito ajustando f_A para baixo.

## 2. Lyman-α (k~3/Mpc) — o muro de FM4 reaparece

Supressão de P(k=3/Mpc) com m_A como **100% da DM** (precisa ≥ 0.95):

```
   m_A = 3.70e-25 eV:  P_supp = 0.000   → EXCLUÍDO como 100% DM
   m_A = 1.00e-24 eV:  P_supp = 0.000   → EXCLUÍDO como 100% DM
   m_A = 1.00e-23 eV:  P_supp = 0.000   → EXCLUÍDO como 100% DM
   m_A = 1.00e-22 eV:  P_supp = 0.963   → MARGINALMENTE SEGURO (no teto da janela)
```

- O **piso de 100%-DM do Lyman-α é ~2×10⁻²¹ eV** — **acima do teto do Paper II
  (1.2×10⁻²²)**. Logo a maior parte da janela é excluída **como DM dominante**.
- **Nuance honesta:** o **topo** da janela (m_A ~ 10⁻²² eV, perto do teto 1.2×10⁻²²)
  fica **marginalmente seguro** (P=0.963 ≥ 0.95). Ou seja, há uma fresta estreita no
  canto superior onde m_A pode ser ~100% da DM e sobreviver ao Lyman-α. Para massas
  ≤10⁻²³ eV não há fresta — só subdominante.

Isto reproduz o resultado de FM4-4: a massa leve que ajudaria estrutura é morta pelo
Lyman-α; a massa segura vive no topo/acima da janela.

## 3. CMB primordial — subdominância antes da igualdade

m_A não pode dominar antes de z_eq ≈ 3400 (a_eq = 2.94×10⁻⁴). Onset das oscilações:

```
   m_A = 3.70e-25 eV:  a_osc = 1.06e-05  ≪ a_eq  → frio (CDM) antes da igualdade ✓
   m_A = 1.00e-24 eV:  a_osc = 6.45e-06  ≪ a_eq  ✓
   m_A = 1.00e-23 eV:  a_osc = 2.03e-06  ≪ a_eq  ✓
   m_A = 1.00e-22 eV:  a_osc = 6.42e-07  ≪ a_eq  ✓
```

**Todas as massas oscilam (viram frias) muito antes da igualdade** → m_A redshifta
como CDM (a⁻³) desde bem antes de z_eq, não perturba o CMB primordial. Sua fração da
DM é constante após o onset (= Ω_{m_A}/0.12). **Compatível.** ✓

## 4. Estrutura em z~0 — massa de Jeans

Massa de Jeans ULDM (suprime halos abaixo dela):

```
   m_A = 3.70e-25 eV:  M_J = 6.7e10 Msun  → suprime anãs observadas (tensão se 100% DM)
   m_A = 1.00e-24 eV:  M_J = 1.5e10 Msun  → suprime anãs observadas (tensão se 100% DM)
   m_A = 1.00e-23 eV:  M_J = 4.7e08 Msun  → OK
   m_A = 1.00e-22 eV:  M_J = 1.5e07 Msun  → OK
```

Para m_A < 10⁻²³ eV como **100% da DM**, M_J ~ 10¹⁰·⁵ Msun apagaria halos anões
(~10⁹–10¹⁰ Msun) que são observados → tensão. Para m_A ≥ 10⁻²³ eV, ou como fração
subdominante, sem problema.

## Região permitida em (m_A, f_A) — síntese de FN3-4

```
                          como 100% da DM            como fração subdominante
  m_A ~ 10⁻²² eV (teto):  fresta marginal (Lyα 0.963, Jeans OK)   permitido
  m_A = 10⁻²³ eV:         EXCLUÍDO (Lyα)              permitido (f_A < 10¹⁷ GeV)
  m_A ≤ 10⁻²⁴ eV (piso):  EXCLUÍDO (Lyα + Jeans)      permitido (subdominante)
```

```
Compatível com Lyman-α?         como 100% DM: só no topo (~10⁻²² eV); senão NÃO.
                                como fração subdominante: SIM.
Compatível com CMB primordial?  SIM (frio antes de z_eq, toda a janela).
Compatível com estrutura z~0?   SIM para m_A≥10⁻²³ eV ou subdominante; tensão de
                                Jeans para m_A≤10⁻²⁴ como 100% DM.
```

**Conclusão FN3-4:** a relíquia Ω~0.12 é alcançável e **não** super-produz, mas
**como DM dominante só sobrevive no topo da janela** (m_A~10⁻²² eV) — o muro de
Lyman-α de FM4. Para o resto da janela, m_A é **matéria escura fria subdominante**
(Ω<0.12, f_A<10¹⁷ GeV), coexistindo com outra componente.
