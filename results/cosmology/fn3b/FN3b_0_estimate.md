# FN3b-0 — Estimativa analítica (o gate obrigatório, sem código)

> Ordem de grandeza para os três caminhos ANTES de codificar. Identifica o caminho
> mais promissor para focar o código. Números de `fn3_core` (FN3) + cálculos diretos.

## Ponto de partida (de FN3)

Para Ω h² = 0.12, a constante de decaimento necessária é (invertendo a forma canônica):

```
f_req(m) = 10¹⁷ GeV · (m/10⁻²² eV)^{-1/4}
θ₀_req(m) = f_req/M_Pl = 8.2×10⁻³ · (m/10⁻²² eV)^{-1/4}    (M_Pl = 1.22×10¹⁹ GeV)
```

Duas escalas físicas independentes entram como **filtros externos** (COMPARISON ONLY):

```
Frio na recombinação:   3H(z=1100) ≈ 8.6×10⁻²⁹ eV  →  m ≳ 10⁻²⁸ eV para oscilar
                        (virar matéria) ANTES de z~1100; senão é energia escura.
Lyman-α como 100% DM:   m ≳ 2×10⁻²¹ eV (limite padrão, reproduzido em FM4/FN3).
```

---

## Caminho A — campo θ (estimativa)

θ₀ necessário e a época de oscilação, varrendo m_θ:

```
  m_θ [eV]    θ₀_req     z_osc      frio em z>1100?   Lyα-100%(m>2e-21)?
  4.5e-31     1.00       32         NÃO (energia escura)    NÃO
  6.4e-30     0.52       194        NÃO (energia escura)    NÃO   ← bound do slip mediator
  1.0e-28     0.26       1.2e3      SIM (marginal)          NÃO
  1.0e-24     2.6e-2     5.7e5      SIM                     NÃO   ← Lyα exclui (fuzzy demais)
  1.0e-22     8.2e-3     1.2e7      SIM                     NÃO
  2.0e-21     3.9e-3     9.0e7      SIM                     SIM (no piso) ← MELHOR CASO
  1.0e-20     2.6e-3     2.6e8      SIM                     SIM
```

**Sobre-fechamento (overclosure) no regime de energia escura.** Se m_θ é leve (não
oscila antes de z~1100), o campo fica frozen como Λ com ρ = ½m²θ₀²M_Pl². No bound do
slip mediator (m=6.4×10⁻³⁰ eV) com θ₀~1 isso dá **ρ_frozen/ρ_crit ≈ 8×10⁷** —
sobre-fecha por 8 ordens. Para não sobre-fechar, **θ₀ < 1.1×10⁻⁴** (e ainda seria
energia escura, não DM).

### Leitura de A
- **Se θ = o slip mediator da DEV (m_θ ≲ 6.4×10⁻³⁰ eV):** oscila tarde demais
  (z_osc ≤ 194) → comporta-se como **energia escura**, não DM fria; e sobre-fecha a
  menos de θ₀<10⁻⁴ → **MORTE A** (critério θ₀<10⁻³ disparado **e** época errada).
- **Se θ tem massa livre mais pesada (m_θ ≳ 2×10⁻²¹ eV, Lyα-safe):** θ₀_req ≈ 3.9×10⁻³
  (fine-tuning **leve**, ~0.4%, **acima** da linha de morte 10⁻³), frio e Lyα-safe →
  **VIÁVEL com tuning leve** — mas essa massa é uma **nova escala** (acima do teto do
  vetor do Paper II, e não é o slip mediator). Isto é fisicamente o **Caminho C**.

**Veredito preliminar A:** o θ **existente** da DEV (slip mediator) → MORTE; o θ com
**massa livre** → viável, mas é uma nova escala (≈ C). A pergunta codeável decisiva:
qual θ₀ é **natural** (medir na rede), e onde a linha Ω=0.12 cruza a banda natural.

---

## Caminho B — dois modos de A_μ (estimativa, decide sem código)

A massa do vetor na DEV é de **Stückelberg/Higgs**: m_A = e·v, com v o vev da quebra
U(1). O campo físico vive num **círculo de raio v** — a amplitude de qualquer
configuração (inclusive a oscilação homogênea de misalignment) é **limitada por v**:

```
v = m_A/e = (10⁻²² eV)/0.303 = 3.3×10⁻²² eV = 3.3×10⁻³¹ GeV
amplitude de misalignment ≤ v = 3.3×10⁻³¹ GeV  →  48 ordens abaixo de 10¹⁷ GeV
```

O modo cosmológico (homogêneo) e o modo galáctico (sourced por θ) são soluções da
**mesma** equação de Proca com o **mesmo** v. v fixa simultaneamente a massa (m_A=ev)
**e** a amplitude máxima (v). **Não há liberdade** para um f_A cosmológico grande:
fixar o galáctico fixa o cosmológico. Ω_misalignment ~ 0.12·(v/10¹⁷)² ~ **10⁻⁹⁵**.

A única fuga seria uma massa de Proca "dura" (sem vev, amplitude livre) — mas isso
**abandona o mecanismo de Stückelberg da DEV** (e reabre problemas de invariância de
gauge/forte acoplamento). Dentro da DEV-como-é, os modos são **acoplados via v**.

**Veredito preliminar B: MORTE** (modos acoplados pelo vev de Stückelberg; f_A
cosmológico **não** é livre). Decidido analiticamente — não precisa de código.

---

## Caminho C — campo escalar extra χ (estimativa)

Por construção χ é um campo oculto novo com f_χ ~ M_GUT (amplitude grande no
primordial), m_χ na banda fuzzy, sem acoplar a bárions. Filtros:

```
Ω_χ=0.12:        f_χ ~ 10¹⁷ GeV em m_χ ~ 10⁻²² eV (idêntico a FN3-1, mas f_χ é de um
                 CAMPO NOVO, livre para ser GUT por construção).
Screening galáctico:  escala galáctica = (kpc)⁻¹ = 6.4×10⁻²⁷ eV. Para χ ser "pesado"
                 (de Broglie ≪ kpc) basta m_χ ≫ 6.4×10⁻²⁷ eV — satisfeito por
                 m_χ ~ 10⁻²² (≈10⁴× mais pesado) → χ age como CDM comum em galáxias.
λ (screening):   λ ≲ m_χ²/M_gal² = (10⁻²²/6.4×10⁻²⁷)² ≈ 2×10⁸ → vínculo FRACO; quase
                 qualquer λ funciona. Lyα-safe como 100% DM exige m_χ ≳ 2×10⁻²¹ eV.
```

A janela **existe** trivialmente — mas é "adicionar um áxion fuzzy" com f_χ posto à
mão na escala GUT. **A identificação natural χ = |⟨n⃗⟩| FALHA:** o módulo do condensado
(modo radial/"Higgs" do ferromagneto) tem massa ~ a escala microscópica da rede
(≫ eV, ~M_Pl), **não** 10⁻²² eV. Logo χ teria de ser um campo leve **genuinamente
novo**, não-relacionado a |⟨n⃗⟩| → **não derivado da DEV, apenas acrescentado**.

**Veredito preliminar C:** janela existe (não-morto), mas **por construção, não
derivado**; a identificação com o condensado de E1 falha por ~30 ordens na massa.

---

## Identificação do caminho mais promissor (a decisão do gate)

```
B: MORTE analítica limpa (vev de Stückelberg acopla os modos). Sem código.
A (θ = slip mediator da DEV):  MORTE (energia escura + overclosure, θ₀<10⁻⁴).
A (θ com massa livre) ≡ C:     MESMA relíquia física — um escalar de misalignment com
                               f = θ₀M_Pl ~ 10¹⁷ GeV (θ₀ ~ poucos×10⁻³) e
                               m ~ 2×10⁻²¹–10⁻²⁰ eV (Lyα-safe). VIÁVEL com tuning leve.
```

**Os caminhos A (massa livre) e C convergem para a MESMA relíquia.** O caminho mais
promissor a **codificar** é essa relíquia compartilhada A/C, e as perguntas decisivas
são **computáveis**:
1. **Qual θ₀ é natural?** Medir a amplitude rms de flutuação de orientação no vácuo
   desordenado/crítico de E1 (`orientation_core`) — aterra θ₀ na rede, anti-circular.
2. **Onde está a janela viável?** Mapear o plano (m_θ, θ₀) sob Ω=0.12 ∧ frio(z_osc>1100)
   ∧ Lyα(m>2×10⁻²¹) ∧ não-overclosure ∧ banda natural de θ₀ → achar o ponto de
   tuning mínimo e reportar o fine-tuning = θ₀_req/θ₀_natural honestamente.

→ **FOCO DO CÓDIGO: a relíquia A/C, com θ₀ medido na rede.** B fica como morte
analítica; A-como-slip-mediator fica como morte analítica (ambas mostradas, não
codadas além do necessário).
