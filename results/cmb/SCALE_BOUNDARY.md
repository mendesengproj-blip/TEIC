# A fronteira de escalas da TEIC+DEV — por que o setor cosmológico (S8) não fecha

> Síntese transversal do setor CMB. Junta FM1 (MOND-μ ingênuo) + FM2 (duas fases) +
> o cálculo do m_A, no quadro maior da TEIC (R1, E1, E2, E3/E3b) e da DEV (Papers I/II).
> Mapa honesto da fronteira: onde a teoria reina e onde precisa de completamento.
> Resultados-fonte: `results/cmb/fm1/`, `results/cmb/fm2/`. Não modifica nada.

---

## 1. O que significa "resolver S8" — a direção importa

A tensão S8 é uma **discrepância de amplitude**: o CMB (Planck/ΛCDM) prevê estruturas
mais encaroçadas hoje (σ8≈0.83) do que o lensing fraco mede (KiDS: σ8≈0.75).

**Resolver S8 = prever MENOS crescimento → σ8 MENOR.** A palavra-chave é **supressão**.
Precisamos de um **freio**, não de um acelerador.

---

## 2. Por que a TEIC+DEV não resolve — ela é um acelerador (duas mortes)

A DEV é **tipo-MOND**: realça a gravidade em baixa aceleração (é assim que explica
curvas de rotação sem matéria escura). MOND é, por natureza, um **acelerador** de
crescimento.

**Morte 1 — FM1 (MOND-μ ingênuo).** G_eff=G_N·μ com μ≥1 ⇒ σ8 **dispara** (101 ≫ 0.81).
Não fecha — **piora** a tensão. A premissa "gravidade mais fraca → σ8 menor" tem o
**sinal trocado** para MOND. → Veredito C.

**Morte 2 — FM2 (duas fases).** A saída elegante: "matéria escura e MOND são duas
fases do campo n⃗" (E1: vácuo = ferromagneto com transição). Medido na rede, há uma
**obstrução estrutural**:
- realce MOND mora na fase **ordenada** (divergência de Goldstone, χ∥~h^(−1/2));
- supressão por pressão (Jeans) precisa do **ponto crítico** (c_s→0);
- são **fases opostas** — não coexistem no mesmo ponto.

O condensado ordenado tem c_s ~ c (relativístico, travado pela Lorentz da R1) →
**free-streama**, não clusteriza como DM fria. → Veredito C.

---

## 3. O coração: por que as escalas não se encontram

Escada de escalas, do pequeno ao grande:

```
  ESCALA          O QUE A TEIC+DEV TEM LÁ              REGIME
  ──────────────────────────────────────────────────────────────────
  ~17 pc     ←  m_A (massa do vetor, Paper II)        sub-galáctico
             ←  ξ_A = ℏ/(m_A c) = 17 pc               (blinda MOND)
  ──────────────────────────────────────────────────────────────────
  ~kpc       ←  transição g = a₀                       GALÁXIAS  ✓
             ←  MOND, BTFR, curvas planas               (a DEV vive aqui)
  ──────────────────────────────────────────────────────────────────
  ~Mpc       ←  ......... NADA derivado .........       ⚠  VAZIO
  ──────────────────────────────────────────────────────────────────
  ~12 Mpc    ←  escala de σ8                            COSMOLOGIA
             ←  só "μ≥1 que dispara" (sem freio)        (precisa de freio)
  ──────────────────────────────────────────────────────────────────
  ~c/H₀      ←  horizonte;  a₀ ≈ cH₀/2π
```

Três fatos fazem as escalas **não se encontrarem**:

**(a) Coincidência a₀ ≈ cH₀.** A aceleração MOND é a aceleração do horizonte cósmico.
Isso ancora a MOND nas **bordas de galáxias** (g cai até a₀ em ~kpc). Lindo para
galáxias — mas calibra toda a teoria nesse regime.

**(b) Modos cosmológicos são deep-MOND TOTAL.** A aceleração própria de uma
perturbação linear é g ~ 3×10⁻¹³ m/s² ≪ a₀ (g/a₀ ~ 0.003) em TODAS as escalas de σ8.
Todo o crescimento está abaixo de a₀, onde a única prescrição é "realça
monotonicamente". Nada diz "pare aqui". → runaway (FM1).

**(c) Os parâmetros internos da DEV estão no lado errado.** O único comprimento de
correlação da teoria é o do vetor: ξ_A = ℏ/(m_A c) ≈ **17 pc** — **sub-galáctico**,
~6 ordens **abaixo** de σ8 (12 Mpc; ξ_A/R₈ ≈ 1.5×10⁻⁶), e corta no lado de **alta**
aceleração (newtoniano), oposto ao que a cosmologia precisa.

**Conclusão:** a teoria tem física rica em ~17 pc (estabilidade) e ~kpc (MOND), mas a
escala que governa S8 (~12 Mpc) cai num **vão sem estrutura derivada** — só o realce
que dispara. As escalas onde a teoria "sabe o que faz" e a escala de S8 estão
separadas por ~10⁶.

---

## 4. Por que falta uma segunda camada — e o que evoluiria da TEIC+DEV

Não é vergonha — é a **assinatura de todo programa de gravidade modificada**:

> **ΛCDM** funciona na cosmologia, mas "inventa" feedback bariônico para galáxias.
> **MOND** funciona em galáxias, mas "inventa" um setor invisível para a cosmologia.

Cada teoria tem um **domínio de validade** + uma **física de completamento** fora dele.
A TEIC+DEV é validada no regime ligado/baixa-aceleração (galáxias). O regime de
**perturbações cosmológicas** exige física que a versão nua **não contém**.

O que **evoluiria** da TEIC+DEV (sem trair o sucesso em galáxias): um **completamento
relativístico** que adicione **uma componente FRIA e clusterizante (c_s→0) em ≥Mpc**,
mantendo MOND nas galáxias. Prova de existência: a **AeST** (Skordis–Złośnik 2021)
faz isso e **reproduz o CMB do Planck**. A semente está na TEIC (E1 dá as duas fases),
mas a rede nua dá o oposto (FM2-2: c_s~c, quente). Faltaria:

- **uma escala nova muito mais leve** (m ~ 5×10⁻³¹ eV, ξ ~ Mpc) — e o **próprio
  Paper II EXCLUI** essa massa para o vetor (m_A é ~10⁶× mais pesado). Não é "ajustar
  m_A"; seria **campo/escala novo**; ou
- uma **equação de estado do condensado a densidade finita** que separe c_s do mágnon
  do vácuo — não derivada na teoria atual.

Isso é a "segunda camada" que falta, e exige a **ação relativística completa da DEV +
um Boltzmann (CLASS)** — fora do escopo da rede E1/E2.

---

## 5. Resumo: o que eles TÊM vs o que FALTA

### TÊM (sólido, validado)

| Domínio | Resultado |
|---|---|
| Espaço-tempo | R1: relatividade especial emerge da contagem causal (Lorentz de Poisson) |
| Vácuo | E1: vácuo = ferromagneto de orientação O(3) com transição de fase |
| Luz | E2: fóton = mágnon BD, ω=ck, c≈0.98, 2 polarizações |
| **Galáxias** | **DEV: MOND, curvas planas, BTFR (χ²ν≈1.3, 167 galáxias SPARC)** |
| **Origem da MOND** | **FM2-1: ν=1/√(g/a₀) EMERGE da resposta de Goldstone do ferromagneto E1 (liga Paper I ↔ E1)** |
| Sub-galáctico | Paper II: blindagem da MOND abaixo de ~17 pc (testável: binárias largas) |

### FALTA (a fronteira)

| Lacuna | O que seria preciso |
|---|---|
| Matéria estável | ainda exige SU(2)+Skyrme externos (E3/E3b: defeitos só metaestáveis) |
| **Cosmologia (σ8, ~Mpc)** | **componente FRIA e clusterizante (c_s→0) em ≥Mpc — a rede nua dá c_s~c (quente)** |
| A escala que falta | campo/escala novo ~10⁻³⁰ eV (ξ~Mpc) — **excluído como m_A** → física nova |
| Ferramentas | ação relativística completa da DEV + Boltzmann (CLASS) para perturbações |

---

## Em uma frase

**A TEIC+DEV resolve o "perto" (galáxias, ~kpc) e deriva o vácuo/luz, mas o "longe"
(perturbações cosmológicas ~Mpc, onde mora S8) cai num regime que a teoria nua só sabe
ACELERAR, não FREAR — e a escala que poderia frear (Mpc) está ~10⁶× longe de qualquer
estrutura que a teoria possui. Falta o completamento relativístico que dê uma fase
fria e clusterizante nessa escala: uma segunda camada de física que a versão atual não
contém, e cujo ingrediente óbvio (o m_A) está ~6 ordens de grandeza fora.**

É a mesma lição de ΛCDM e MOND: cada uma reina no seu regime e precisa de socorro no
outro. A TEIC+DEV mapeou honestamente essa fronteira — e, de quebra, descobriu *por que*
a MOND existe (Goldstones do vácuo orientacional, FM2-1).

---

## Atualização — a rota da relíquia primordial também foi testada (FM3)

A terceira rota imaginada (`TEIC_DEV_VISION.md` §6) — uma **textura primordial** da
transição de E1, congelada por causalidade (E3b) na escala do horizonte — foi
executada em `results/cmb/fm3/`. **Veredito C, por um motivo novo:** o relíquia tem a
**escala certa** (cosmológica, resolvendo o problema de separação de escala que matou
FM2) e é **congelado super-horizonte** (E3b) — MAS sua equação de estado é
**w≈−1/3** (textura/monopolo global), **não w=0** (frio CDM). **"Congelado por
causalidade" é frio de POSIÇÃO, não de PRESSÃO.** Logo não clusteriza como matéria
fria nem suprime σ8. Mapa completo das mortes:

| Rota | Por que morre |
|---|---|
| FM1 (MOND-μ) | **realça** σ8 (sinal errado) |
| FM2 (duas fases) | **escala errada** (m_A → 17 pc) + obstrução estrutural |
| FM3 (relíquia primordial) | **escala certa, equação de estado errada** (w=−1/3, não fria) |

## Atualização 2 — o setor MASSIVO foi testado (FM4): tem matéria escura, mas não S8

FM1/FM2/FM3 viviam no setor de **orientação (Goldstone, sem massa)** — que
estruturalmente não dá w=0. FM4 (`results/cmb/fm4/`) testou o setor **MASSIVO** (o
vetor m_A como matéria escura de onda/fuzzy via misalignment) e encontrou:
- ✅ **w=0 frio** (FM4-1: w=−0.04, ρ~a⁻³) — **a TEIC+DEV TEM um candidato a matéria
  escura: o m_A massivo.** A peça que faltava.
- ❌ **mas não resolve S8** (4ª morte): σ8 mal se move no intervalo de massa permitido
  (FM4-3), e a massa leve+fração que ajudaria super-suprime o Lyman-α (FM4-4). Não há
  janela.

**Mapa final das QUATRO portas:**

| Rota | Setor | Por que morre (para S8) |
|---|---|---|
| FM1 (MOND-μ) | Goldstone | realça σ8 |
| FM2 (duas fases) | Goldstone | escala errada (17pc) + obstrução |
| FM3 (textura) | Goldstone | escala certa, w=−1/3 (não frio) |
| FM4 (vetor massivo fuzzy) | **Massivo** | **w=0 frio ✓ (é DM!)** mas S8 morto pelo Lyman-α |

**Conclusão definitiva:** o setor de Goldstone nunca dá w=0 (estrutural); o setor
massivo **dá matéria escura fria (m_A)** — então a TEIC+DEV tem fóton (E2), MOND/
galáxias (origem micro do ν em FM2-1) E matéria escura (m_A frio). **Mas NENHUM setor
resolve a tensão S8 especificamente:** a supressão que S8 exige ou vai na direção
errada (FM1/2/3) ou é excluída pelo Lyman-α (FM4). S8 permanece não resolvido por
TEIC+DEV; exigiria um mecanismo de supressão que sobreviva ao Lyman-α (nenhum conhecido)
ou matéria escura com propriedades além de fria.

## Próximos passos possíveis (não pré-registrados aqui)

1. **Completação relativística + CLASS** (em WSL/Linux): único caminho que poderia
   reabrir S8 — precisaria de um setor de poeira (w=0) que a rede nua não dá.
2. **FN4 (TEIC):** termo de Skyrme dinâmico (a escala que falta para matéria estável).
3. **Teste sub-galáctico do m_A:** blindagem da MOND abaixo de ~17 pc (binárias
   largas, Chae et al.) — previsão *testável* da DEV independente da cosmologia.
