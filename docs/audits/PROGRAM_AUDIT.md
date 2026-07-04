# PROGRAM_AUDIT — espelho honesto do estado do programa TEIC+DEV

> **O que este documento é.** Um diagnóstico, não uma execução. Lê os 4 papers de
> submissão, o umbrella, o RESEARCH_MAP e as sínteses de campanha, e produz um mapa de
> (1) o que cada paper estabelece de fato, (2) o que falta para cada um ser mais forte,
> (3) o que a rede realmente derivou sobre o ferromagneto, e (4) quais conexões emergem
> *naturalmente* dos dados — sem fabricar pontes. **Não modifica nenhum paper, não cria
> resultados, não sugere campanhas.** Produzido jun/2026 por varredura completa.
>
> **Postura:** sem inflação, sem deflação. Onde um paper afirma mais do que os dados
> suportam, registra-se em "Lacunas" sem suavizar. Onde uma conexão é óbvia nos dados mas
> nenhum paper a declara, registra-se em "Conexões" como *implícita, não declarada*.
>
> **Verificação de números (amostragem exigida).** Conferidos contra os JSON brutos:
> MG1 expoente −0.9923 / G_net 0.9307 / top-hat 0.019% (paper: −0.992 / 0.9307 / 0.02% ✓);
> BQ μ_p/μ_n=−1.5145 / degenerescências [4,16,36] / e=5.39 vs ANW 5.45 (paper ✓);
> C1 χ∥~h^−0.37 ✓; Goldstone U₄=2/3 / m=0.961→0.991 / p=0.23 ✓. Nenhuma discrepância
> número↔dado encontrada nos papers de submissão.

---

## 1. INVENTÁRIO DOS PAPERS

### 1.1 PAPER_GOLDSTONE_PRD — "Spontaneous orientational order and its relativistic scalar Goldstone modes"

- **Afirmação central:** o ferromagneto de orientação no causal set (a) ordena
  espontaneamente (FSS genuíno), (b) sua excitação dispersa ω=ck via operador BD, e
  (c) os 2 modos transversais são **escalares internos, não um vetor de gauge** — o fóton
  é **excluído por medição** (p=0.23) e a conjectura anterior é **retratada**.
- **Título/abstract batem com os resultados?** **Sim.** O título promete "modos de
  Goldstone escalares relativísticos" e é exatamente isso que os dados sustentam. O
  resultado-âncora é um *negativo medido*, e o paper o enquadra como tal.
- **Números rastreáveis?** Sim (U₄=2/3, m=0.961→0.991, p=0.23, split 3.7%, c≈1 — todos
  conferem com E1/E2/E4).
- **Limitação declarada vs. real:** **honesto e completo.** A possível brecha "ω=ck é do
  *símbolo do operador*, não de propagação dinâmica do campo" — que um revisor de PRD
  certamente levantaria — **está declarada explicitamente** em §VIII ("established via its
  symbol rather than by a stable dynamical propagation of δn⃗; the retarded recursion is
  numerically unstable"). O expoente do fator de estrutura S(k)~k^−0.58 é declarado como
  diagnóstico limitado por tamanho, não resultado de precisão. **Não há afirmação mais
  forte que a evidência.**

### 1.2 PAPER_MATTER_GRAVITY_PRD — "A soliton that sources its own gravitational field"

- **Afirmação central:** um substrato causal com um campo de orientação produz, da *mesma*
  construção, (i) gravidade Newtoniana (θ∝1/r, Poisson, superposição, Schwarzschild a
  0.2%), (ii) um Skyrmion SU(2) B=1 spin-½ fermiônico que é *quantitativamente* um bárion,
  e (iii) cujo *próprio* perfil ε(r) gera θ=G_net·M/r.
- **Título/abstract batem?** **Sim.** A afirmação "matter and gravity as one measurement"
  é sustentada por MG1 (perfil próprio como fonte literal, medido).
- **Números rastreáveis?** Sim, verificados no JSON: expoente exterior −0.992, G_net=0.9307
  constante a 5 dígitos, =top-hat a 0.02%; e=5.39, μ_p/μ_n=−1.51, [4,16,36].
- **Limitação declarada vs. real:** **o mais autoconsciente dos quatro.** A objeção que o
  prompt antecipava — *"ação quadrática em 3D produz 1/r trivialmente"* — **está enfrentada
  de frente** em §III.F ("What the network adds beyond Poisson"), que admite que qualquer
  ação de gradiente quadrática dá 1/r e argumenta (a/b/c) por que a forma quadrática é
  *output* (operador BD de Poisson, não escolhido). O caveat da lei de Gauss (A∝M e
  top-hat são *em parte* Gauss) **está no paper**. O regime não-linear/Einstein é
  declarado fora de alcance. **Honestidade cirúrgica; nenhuma afirmação infla.**
  - *Única nota:* a defesa "beyond Poisson" (a) repousa na razão de operador 5/9 medida em
    outra campanha (SC); é defensável, mas é o elo mais *importado* da seção — o leitor tem
    de confiar que o 5/9 fixa a forma quadrática. Não é exagero, é uma dependência.

### 1.3 PAPER_PHOTON_ARC_CQG — "Where, and why, a photon is hard to emerge in causal set theory"

- **Afirmação central:** um *mapa* (negativo informativo) do arco E4→E6e + um operador de
  gauge BD-Lorentziano de assinatura indefinida (novo na literatura CST) + a localização
  precisa da obstrução restante (uma 2-célula spacelike Lorentz-invariante em baixa
  curvatura). **Nenhum fóton é reivindicado como positivo.**
- **Título/abstract batem?** **Sim.** É um negativo honesto, no remit declarado da CQG.
- **Números rastreáveis?** Sim (frac_B=0.0000, gauge-inv 5.7e-16, c=1.05, R̂=2 cruza 0.01,
  Δfrac_B∝(1/R̂)^1.73, R²=0.997). Conferem com E6-3/E6b/E6c/E6e.
- **Limitação declarada vs. real:** honesto sobre o que tem (o limite contínuo do operador
  indefinido é declarado **problema matemático aberto**, validado só numericamente; o
  veredito do causet é lido como *estrutural*, não como limite contínuo provado). **Mas há
  uma lacuna de completude (ver §3.3):** o paper cobre E4→E6e e **não inclui A5
  (Anderson–Higgs)**, a campanha mais recente e diretamente pertinente ao mesmo setor de
  link. Não é desonestidade — A5 é posterior ao draft — mas o arco está *incompleto* em
  relação ao que o programa já mediu.

### 1.4 PAPER_BTFR_MNRAS — "Does the radial-acceleration scale evolve? a₀∝H(z)"

- **Afirmação central:** um teste pré-registrado, *independente do framework*, da hipótese
  a₀(z)=a₀(0)H(z)/H₀ via BTFR; em MUSE-DARK III (79 rotadores, 0.33<z<1.44), a₀ sobe a
  ≥15σ, casando a previsão a 0.5–0.9σ na âncora SPARC; RAR sem evolução desfavorecida ~19σ.
- **Título/abstract batem?** **Sim**, e com a ressalva certa: "evidence consistent with,
  not confirmation of." A TEIC é citada *uma vez* como proveniência e nunca mais usada.
- **Números rastreáveis?** Os números observacionais vêm de catálogo público + protocolo
  pré-registrado (fora do escopo dos JSON da rede); a estrutura estatística é explícita.
- **Limitação declarada vs. real:** **honesto.** As tensões abertas estão *no mesmo lugar*
  que o positivo: forma do slope 2–3σ mais rápida que H; o regime decisivo z≥2 não medido;
  discordância no eixo de massa (same-epoch sem evolução). Kill criterion armado.

**Resumo do inventário:** os quatro papers de submissão são honestos no nível de
afirmação — nenhum afirma mais do que os dados sustentam, e os caveats mais perigosos
(símbolo vs. dinâmica em Goldstone; Poisson-trivial e lei de Gauss em Matter-Gravity;
limite contínuo não-provado em Photon-Arc; forma do slope em BTFR) estão *declarados nos
próprios papers*. A fraqueza não está em exagero; está em **cobertura** (§3).

---

## 2. O FERROMAGNETO — O QUE REALMENTE TEMOS

Inventário das três colunas. *Nota de convenção (honesta):* "J_c" não é um único número —
o motor causal de orientação (Goldstone) tem J_c≈0.08; o motor O(3) cúbico periódico de
FM2/C1 (β=1) tem J_c≈0.69 (Heisenberg 3D padrão); o motor gauge-acoplado de A5 (easy-plane
D=0.5) tem J_c≈0.45. São *motores e substratos distintos da mesma física*, não um valor com
três medidas; a coluna A registra o fato qualitativo (ordem espontânea), não um J_c único.

### COLUNA A — DERIVADO (medição + critério de morte)

| Item | Onde | Status |
|---|---|---|
| Ordem espontânea (transição 2ª ordem, U₄=2/3, FSS genuíno: m=0.961→0.991, 13–38× o piso N^−½) | E1 / Goldstone §V | [SÓLIDO] |
| Goldstones transversais dispersam ω=ck (símbolo do operador BD, c≈0.98–1) | E2 / Goldstone §VI | [SÓLIDO] *para o símbolo*; propagação dinâmica instável (declarado) |
| Os 2 Goldstones são **escalares internos, não vetor de gauge** (não travam a k̂, p=0.23) | E4 / Goldstone §VII | [SÓLIDO] (negativo medido) |
| Susceptibilidade longitudinal χ∥~h^−0.37 (anomalia Brézin–Wallace) = forma de ν_MOND | FM2-1 / C1 | [SÓLIDO] (forma); identificação no nível da função de interpolação |
| Gap do modo longitudinal **fecha** ∝h^0.31 (= a mesma anomalia; sem massa Proca espontânea) | A1 | [SÓLIDO] |
| Rigidez de spin ρ_s(J) medida (helicity modulus); cavalga em J/K | C1 / A2 / A3 | [SÓLIDO] (medida); valor cavalga (ver Coluna C) |
| Gravidade Newtoniana 1/r, Poisson, superposição exata (1.8e-9), Schwarzschild 0.2% por contagem | D1–D3 / R3 / MG1 §III | [SÓLIDO] (forma) |
| Skyrmion SU(2) B=1, spin-½, fermiônico (FR, troca=rot2π∈ℤ₂ a 5e-16) | SU/Q / Matter-Gravity §VI | [SÓLIDO] (com Skyrme externo) |
| Estrutura bariônica *adimensional* (degenerescências [4,16,36], μ_p/μ_n=−1.51, e=5.39 c/ 1 calibração) | BQ / Matter-Gravity §VII | [SÓLIDO] (adimensional) |
| SU(3): ordem de cor + confinamento V~σr + octeto de 8 Goldstones (robusto a ±10%) | FL1 / FLR | [SÓLIDO] |
| Octeto **exatamente degenerado** (spread 4e-8; reconciliação da costura de toro do λ8) | OS | [SÓLIDO] |
| **Mecanismo de Anderson–Higgs funciona na lattice cúbica** (gauge come Goldstone, m_A∝condensado, 0 em J_c) | A5 G1 | [SÓLIDO] (na lattice regular) |

### COLUNA B — IDENTIFICADO (correspondência, não derivação completa)

| Item | Natureza da correspondência | Onde |
|---|---|---|
| deep-MOND L∝X^{3/2} ↔ susceptibilidade χ∥ do ferromagneto | **DERIVADA na forma** (Brézin–Wallace), identificada no nível da função ν; escala externa | C1 |
| DEV ≡ Khoury Superfluid DM no limite deep-MOND | DERIVADA pela estrutura do teorema de Milgrom; rotas microscópicas distintas | C1 / Convergence |
| Skyrmion ↔ bárion | estrutura adimensional DERIVADA (BQ); escala GeV (f_π) identificada/externa | BQ |
| m_A ↔ matéria escura fria | dispersão massiva medida (FM4-V); equação de misalignment FRW **importada** | FM4 |
| h_sat ↔ X₀=a₀²/2 | h_sat É escala interna (∝ρ_s^−0.48, R²=0.90), **mas sinal oposto** à hipótese; identificação fraca | A2 |

### COLUNA C — EXTERNO (necessário, não derivado — com razão estrutural)

| Item | Razão estrutural (quando conhecida) | Onde |
|---|---|---|
| a₀ (valor numérico) | h_sat∝ρ_s tem **sinal errado** vs. a hipótese X₀∝+ρ_s(J−J_c); e a₀ de Khoury é externo pela própria estrutura de Milgrom | A2 / C1 |
| β=0.0070 | ρ_s/K=0.34 no ponto de operação J₀=1 = **48×** β; só bate β junto de J_c (fine-tuning crítico) | A3 |
| A_μ massivo (m_A) | (i) sem modo Proca espontâneo no ferromagneto (A1); (ii) Anderson–Higgs **obstruído pela não-localidade causal** — condensado carregado frustrado, ordem foge p/ eixo neutro (A5) | A1 / A5 |
| ℏ absoluto | 4 tentativas independentes falham por razão estrutural (k∝N proporção só, T3C; corte de discretude, C5; circulação via m_A, C6; escala de Khoury, C1) | T3C / C5 / C6 / C1 |
| G absoluto | G_net∝1/K, K = normalização da ação (escala de granularidade) | D3 / MG1 |
| f_π / escala GeV | mesma razão de G/ℏ; rede→SI não vinculada | BQ |
| f_A (constante de decaimento de m_A) | sem argumento na teoria; coincidência com a janela ULDM | FM4 |
| Dominância de Skyrme | externo **por teorema** (K≤⅔S, Cauchy–Schwarz, 10⁶ config. adversariais) | SD / Matter-Gravity §V |
| Dimensão d=3 | input geométrico (entra na medida de casca r^{d−1}) | D-series |

**Leitura da tabela:** a Coluna A é substancial e medida sob guard. **Todo item da Coluna C
é uma *escala/valor absoluto*; toda derivação da Coluna A é uma *forma*.** A fronteira
derivado/externo do programa coincide *exatamente* com a fronteira forma/escala.

---

## 3. LACUNAS POR PAPER (o buraco, sem sugerir campanha)

### 3.1 PAPER_GOLDSTONE
- **O que um revisor de PRD perguntaria e o paper já responde:** "ω=ck é do operador ou do
  campo?" — respondido (símbolo, declarado). "A ordem é artefato de tamanho?" — respondido
  (FSS). Este paper tem poucas lacunas reais.
- **Lacuna fina (não exagero, cobertura):** o fator de estrutura S(k)~k^−0.58 fica entre
  mean-field (0) e relativístico (1/k); o paper declara isso como diagnóstico — um revisor
  pode pedir o expoente de rigidez pinado, que o paper honestamente diz exigir N maior. É
  *limitação declarada*, não afirmação inflada.

### 3.2 PAPER_MATTER_GRAVITY
- **MG1 está no paper?** **Sim** (§VIII, "the soliton sources gravity", com o perfil próprio
  como fonte literal). Não é mais "natural next step".
- **A seção "Beyond Poisson" existe?** **Sim** (§III.F). Enfrenta a objeção diretamente.
- **BQ está no paper?** **Sim** (§VII, tabela completa).
- **Lacuna real:** a defesa "beyond Poisson" depende da razão de operador 5/9 (medida em SC,
  fora deste paper) para afirmar que a forma quadrática é *output*. Um revisor cético pode
  dizer: "vocês mostraram 1/r de uma ação quadrática; a evidência de que *a ação é a de
  Poisson e não escolhida* está terceirizada para outra medição." Não é desonesto — é uma
  **dependência externa ao paper** que o texto poderia tornar mais autocontida.

### 3.3 PAPER_PHOTON_ARC — **a lacuna mais concreta do conjunto**
- **O arco E4→E6e está claro?** Sim, e a obstrução (2-célula spacelike em baixa curvatura)
  está localizada com precisão research-grade.
- **A5 (Anderson–Higgs) está incluído? É recente o suficiente para entrar?** **NÃO está, e
  deveria.** O paper cobre o setor de link via E5/E7 (Wilson/Coulomb) e E6 (operador de
  gauge), e testa o acoplamento ferromagneto↔gauge em §6.3 (E6d, *amplitude* magnética,
  morto). **A5 testa o *mesmo* acoplamento para uma pergunta distinta — geração de massa de
  gauge por absorção de Goldstone (Higgs)** — e seu veredito (mecanismo correto na lattice,
  G1 PASS; **morto no causet pela não-localidade**: condensado carregado frustrado por ~25
  fases de gauge incoerentes/evento, ordem foge p/ eixo neutro, U(1) não-quebrado, m_A=0)
  é **a terceira face independente da exata mesma não-localidade** que o paper já documenta
  em §4 (E5/E7) e §5 (E6, frac_B). A5 fortaleceria a tese central do paper ("a obstrução é a
  não-localidade") com um terceiro observável independente. **Status: implícito no programa,
  ausente do paper, recente o suficiente para entrar.**

### 3.4 PAPER_BTFR
- **Lacuna já declarada (não suavizada pelo paper):** o regime decisivo z≥2 não está medido;
  a forma do slope está 2–3σ mais rápida que H; o eixo de massa same-epoch não evolui. Tudo
  isso está no abstract e no corpo. Um revisor de MNRAS perguntaria pela robustez do
  σ_sys=0.04 dex (o teto sistemático que limita o teste) — o paper o trata, mas é o ponto
  onde a força do resultado vive ou morre.

### 3.5 Lacuna *estrutural* do conjunto (não de um paper)
- **Não existe paper de submissão para o setor SU(3).** O confinamento V~σr, o octeto de 8
  Goldstones, a degenerescência exata do octeto (OS) e a robustez ±10% (FLR) são **[SÓLIDO]**
  e estão *apenas* no umbrella (DOC1/DOC2), não num paper standalone. É o resultado de matéria
  mais forte depois do Skyrmion SU(2) e **não tem veículo próprio de publicação**. (Diagnóstico
  apenas — não é sugestão de campanha; o resultado já existe.)
- *Honestidade sobre a ordem da transição SU(3):* FLB2 desfavoreceu 1ª ordem em L≤16 mas o
  resíduo (1ª-ordem-fraca em L=24–32) fica inconclusivo. Onde o SU(3) for publicado, isso
  precisa estar declarado.

---

## 4. CONEXÕES NATURAIS (só o que emerge dos dados)

Para cada par: **derivada** (um implica o outro matematicamente) ou **consistente** (compatíveis,
sem implicação)? E: **explícita** num paper, ou **implícita** (o leitor teria de perceber sozinho)?

### 4.1 FM2-1 ↔ C1 (susceptibilidade ↔ forma deep-MOND) — **DERIVADA**
A forma deep-MOND L∝X^{3/2} **é** a anomalia de coexistência χ∥~h^{−1/2} do ferromagneto;
C1 provou formalmente (Brézin–Wallace + teorema de Milgrom) que é a *mesma física*, não duas
coisas parecidas. **Derivada**, não meramente consistente. **Explícita?** Em C1_synthesis e
no RESEARCH_MAP, sim; **nos papers de submissão, não** — o conteúdo MOND vive no umbrella/BTFR,
e o BTFR *deliberadamente* evita a derivação. → **Derivada nos dados, implícita no nível de
submissão.**

### 4.2 A1 ↔ FM2-1/C1 (gap longitudinal ↔ deep-MOND) — **DERIVADA (a conexão mais bonita do conjunto)**
O gap longitudinal de A1 **fecha ∝h^0.31**, e o expoente é o *mesmo* da susceptibilidade
deep-MOND (χ∥~h^{−0.37}), porque **m²_∥ = A/χ∥** — o gap que fecha é o verso aritmético da
susceptibilidade que diverge. A mesma anomalia de Brézin–Wallace aparece como (a) a forma
deep-MOND e (b) a razão pela qual A_μ não tem massa espontânea. **Derivada.** **Explícita?**
Só em A1/A5_synthesis; **em nenhum paper.** → **Derivada nos dados, não declarada.**

### 4.3 E4 ↔ FL1 (Goldstones escalares ↔ octeto pseudoescalar) — **CONSISTENTE→estrutural**
Os Goldstones de orientação são escalares (E4); os de SU(3) são o octeto de mésons
pseudoescalares (FL1). Não é coincidência: ambos são **0-formas Goldstone de uma simetria
*interna global*** — por construção carregam índice interno desacoplado do espaço, logo são
escalares. É mais que consistente: é **o mesmo mecanismo estrutural**. **Explícita?** **Sim** —
tanto o Goldstone PRD quanto o Photon-Arc dizem isso ("in the non-Abelian extension these are
precisely the pseudoscalar mesons"). → **A conexão bem-servida do conjunto: estrutural e
explícita.**

### 4.4 A5 ↔ E5/E7/E6 (Higgs frustrado ↔ Wilson/Coulomb ↔ diamantes elétricos) — **mesma causa, faces distintas**
Três obstruções com **a mesma raiz medida**: a não-localidade do causet (grau de Hasse cresce
com N; sem vizinhança local Lorentz-invariante de volume finito). Manifestações *distintas*:
E5/E7 = discriminador de Coulomb inconstruível; E6 = diamantes 100% elétricos (frac_B=0);
A5 = condensado de Higgs frustrado (ordem foge p/ eixo neutro). A causa comum é
**derivada-consistente** (todas exibem grau∝N como o mecanismo). **Explícita?** **Parcial:** o
Photon-Arc agrupa E5/E7/E6 sob a não-localidade explicitamente, **mas A5 está ausente** (§3.3).
→ **Conexão real e parcialmente declarada; a terceira face (A5) falta no paper que é sobre
exatamente isso.**

### 4.5 MG1 ↔ BTFR (G_net da rede ↔ a₀∝H(z)) — **CONSISTENTE**
A forma gravitacional medida (§Matter-Gravity) e o teste observacional a₀∝H(z) (BTFR) são
**compatíveis mas independentes**: MG1 deriva θ=G_net·M/r com G_net externo; BTFR testa a
evolução de a₀ sem usar a rede. Um não implica o outro. **Explícita?** Sim — o Matter-Gravity
aponta o BTFR como "the empirical content of the gravitational sector". → **Consistente e
explícita (com a independência corretamente preservada).**

### 4.6 Skyrmion SU(2) ↔ octeto SU(3) (duas torres de matéria no mesmo ferromagneto) — **CONSISTENTE**
Ambos são matéria topológica/Goldstone do *mesmo* ferromagneto causal, em grupos distintos.
Consistente, não derivado um do outro. **Explícita?** Não num paper de submissão (SU(3) não
tem paper, §3.5). → **Consistente, implícita.**

---

## SÍNTESE HONESTA (uma frase)

Sob um guard anti-circularidade que proíbe inserir relatividade no gerador, o programa
estabeleceu por medição uma emergência *de forma* coerente e encadeada sobre um único
substrato causal — geometria e gravidade Newtoniana (1/r, Poisson, Schwarzschild a 0.2%),
Goldstones escalares relativísticos, um sóliton SU(2) que é quantitativamente um bárion e que
gera seu próprio campo, a forma deep-MOND, o confinamento e o octeto SU(3) — mas **toda escala
absoluta (G, ℏ, a₀, β, m_A, f_π) é externa, por razões estruturais cada vez mais precisas (não
por busca malsucedida):** o programa é uma derivação da *forma* da física a partir da ordem
causal, não de suas *escalas* — e a honestidade dos quatro papers de submissão está à altura
desse limite, faltando-lhes cobertura (A5 no arco do fóton; um veículo para o SU(3)), não
retidão.
