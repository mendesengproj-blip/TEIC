# MAPA DE ACOPLAMENTO B9 — existe acoplamento honesto TEIC↔DEV? (Fase 1)

> Construído sobre `INVENTARIO_B9.md` (Fase 0). Responde (A) há acoplamento honesto?,
> (B) o gate do expoente, (C) recomendação de escopo. **Nenhum experimento é rodado
> aqui** — esta é varredura + mapa + recomendação, como o charter exige.
>
> **Veredito de uma linha:** **B9-INVIÁVEL** — a hipótese do "piano no vácuo" fecha-se
> **no nível do mapa, com mecanismo**, por composição de resultados já medidos (C1, A1,
> A5, V2, A2, A3, B7). O meio-DEV não é o ar errado por incompatibilidade de frequência;
> é o ar errado porque **não tem o que fornecer**: o expoente que falta não falta, o
> setor vetorial não existe, e a escala é externa dos dois lados.

---

## (A) Existe um acoplamento honesto TEIC ↔ DEV?

Um acoplamento honesto (definição do charter): uma quantidade que a **DEV postula**
(a₀, β, X₀, m_A) é **fixada por uma quantidade que a TEIC deriva** (razão de grafo,
expoente, escala de resposta) — **sem inserir a escala à mão** e **sem ser tautológico**
(a lição de B1: M_Sk·G_net = A não é acoplamento, é definição).

Varredura de **todos os candidatos** de acoplamento (do INVENTÁRIO §1–2):

| Candidato | Quantidade DEV | Quantidade TEIC | Resultado | Por que falha como acoplamento honesto |
|---|---|---|---|---|
| **a₀ ← rigidez de grafo** | a₀ | `h_sat ∝ ρ_s^−0.48` | correlato R²=0.90 mas **sinal oposto**; escala absoluta externa | A2: a lei hipotetizada `X₀∝+ρ_s(J−J_c)` é **wrong-signed**; a₀ fica [EXTERNO-B] |
| **X₀ ← saturação DBI da rede** | X₀=a₀²/2 | const pura π/ln2 | forma [DERIVADO], **escala ∝ρ (UV), não a₀** | C3/CR3: identificação X₀↔a₀ **morta**; a escala é UV, não MOND |
| **β ← ρ_s/K** | β≈0.0070 | ρ_s/K=0.336 | **48× off** no ponto físico; casa só em J_c | A3: exige tuning quase-crítico (ρ_s→0); não-natural |
| **m_A ← modo longitudinal** | m_A (Proca) | gap longitudinal | gap **fecha** ∝h^0.31 | A1: sem modo Proca espontâneo; massa seria field-induced |
| **m_A ← Anderson–Higgs** | m_A | U(1)_z + Goldstone | **m_A=0** (fuga p/ eixo neutro) | A5: mecanismo correto (cubic gate PASS) mas **obstruído pela não-localidade** do causal set |
| **A_μ ← gauge de Wilson (plaqueta)** | A_μ acoplado a θ | F_μν de plaqueta | **F_μν≡0 no regime galáctico** | V2: o A_μ–θ da DEV é Stückelberg/corrente (dim-4), não dilatônico (dim-5); operadores diferentes, sem concordância em 1ª ordem |
| **η ← slip do Skyrmion** | η−1∈[2.2%,4.1%] | platô O(1) (61%) | slip real mas **~15× a janela**, falloffs diferentes | A4: é slip de **bárion local**, não de **galáxia**; precisa do A_μ ausente |
| **ρ_vac ← Λ flutuante** | ρ_vac=a₀²/16πG | Λ~10^−122 | coincidência fator 1.5 | a própria DEV marca **[SUGESTIVO]**; promover sem o acoplamento explícito seria desonesto |

**Resposta (A): NÃO há acoplamento honesto.** Todo candidato cai em um de três baldes:
- **externo/sinal-errado** (a₀ via A2, X₀ via C3, β via A3) — a escala não vem do grafo;
- **análogo inexistente** (m_A/A_μ via A1+A5+V2) — o setor que forneceria o índice
  spacelike do fóton **não emerge** na TEIC e, do lado DEV, vive num operador
  (Stückelberg, F²=0) que **não se sobrepõe** ao setor de gauge de plaqueta da TEIC;
- **sugestivo/não-promovível** (ρ_vac).

Nenhum candidato é tautológico no sentido de B1 — mas isso não os salva: eles são
**externos** ou **vazios de análogo**, que é a outra forma de morte.

---

## (B) O GATE DO EXPOENTE (bloqueante) — magnon-quadrático → phonon-X^(3/2)?

Este é o coração do B9. O resultado de 1ª classe:

### O gate, como posto no prompt, é um **binário mal-posto**
O prompt oferece duas saídas: **(SIM)** o meio leva ∝X → X^(3/2); **(NÃO)** as duas
teorias vibram em frequências incompatíveis. **C1 mostra que a dicotomia omite o eixo
real.** A comparação "magnon transverso (∝X) vs phonon (X^(3/2))" cruza **dois setores
diferentes**:

| | Setor transverso (magnon) | Setor longitudinal (resposta) |
|---|---|---|
| TEIC | `L=½ρ_s(∂π)²` → **∝X**, ω=ck, **Goldstone** | `χ∥~h^−0.37` (Brezin–Wallace), **anomalia IR emergente** |
| DEV | (não tem Goldstone microscópico) | `μ(x)` do DBI → forma **X^(3/2)** deep-MOND |
| Forma deep-MOND `L∝|∇Φ|³≡X^(3/2)` | **ausente** (proibida) | **presente nos dois** (teorema de Milgrom) |

### As duas leituras de 1ª classe, ambas verdadeiras simultaneamente:

**(B-i) NÃO, o magnon transverso não vira X^(3/2) — por estrutura fixa.**
O termo cinético transverso é quadrático **por proteção de Goldstone** (teorema de
Goldstone: o modo é massless e a ação de árvore é ∝X). Nenhum acoplamento a um meio
externo transmuta isso — integrar o modo longitudinal massivo gera **só correções
analíticas** (X², derivadas superiores), **nunca X^(3/2)** (C1, K1.1-2). Esta é a
**mesma estrutura de morte por sinal/propriedade fixa** que matou HE1/HE2/HE3 (memória):
uma propriedade que nenhuma intensidade/acoplamento inverte.

**(B-ii) E o X^(3/2) que o meio "forneceria" **já existe na TEIC** — internamente.**
A forma fracionária deep-MOND **não falta** ao piano. Ela vive na **anomalia longitudinal
χ∥~h^−0.37** (efeito IR de loop, as flutuações de Goldstone vestindo a susceptibilidade
longitudinal). Pelo teorema de Milgrom, é **a mesma forma** `X^(3/2)` que a DEV põe por
axioma — alcançada por rota diferente, **sem meio nenhum** (C1, K1.3-4 + Fase 2).

### Conclusão do gate (a peça que fecha o B9)
> O meio-DEV **não tem onde inserir o expoente que falta, porque ele não falta.**
> No setor onde o X^(3/2) *poderia* ser inserido (transverso), ele é **proibido** por
> Goldstone — fixo. No setor onde o X^(3/2) *existe* (longitudinal), ele **já está lá**,
> emergente e interno — o meio é redundante. Sobra ao meio fornecer apenas a **escala
> absoluta** — e é exatamente o que **B7 (campo-médio, sem divergência de ξ)** e
> **A2/A3** dizem ser inacessível e de correlato errado.

O gate **dispara NÃO**, mas pela razão estrutural correta (não "frequências
incompatíveis" — e sim "a transmutação é desnecessária no setor onde a forma já existe,
e proibida no setor onde ela falta"). O B9 morre no mapa, **antes de gastar CPU** — e
isso é um resultado, não uma falha, exatamente como B1+B5+B6+B7 fecharam a escala interna
com mecanismo.

---

## (C) Recomendação de escopo

### Veredito: **B9-INVIÁVEL** — resultado negativo de 1ª classe

A hipótese do "piano no vácuo" fecha-se no nível do mapa. O que falha, nomeado
explicitamente (como o charter exige):

1. **O expoente (gate B):** mal-posto. A transmutação quadrático→X^(3/2) é **proibida
   por Goldstone** no setor transverso e **desnecessária** no longitudinal (a forma já é
   interna, C1). O meio não fornece expoente novo.
2. **O setor vetorial (PC2/opção irmãos):** o A_μ coerente que forneceria o índice
   spacelike do fóton **não tem análogo na TEIC** (A1: sem Proca espontâneo; A5:
   Anderson–Higgs obstruído pela não-localidade, m_A=0) e, do lado DEV, vive num operador
   Stückelberg com **F_μν≡0 no regime relevante** (V2) — não se sobrepõe ao setor de
   plaqueta da TEIC. A opção **B9-irmãos não tem pilar**.
3. **A escala (a₀, β):** externa dos dois lados; correlato de grafo **fraco/sinal-errado**
   (A2) ou **48× off** (A3); substrato **campo-médio** sem transmutação dimensional (B7).

**O culpado estrutural é o mesmo das quatro mortes anteriores** (diagnóstico do prompt
confirmado pela varredura): a **alta conectividade do causal set Poissoniano** (grau de
Hasse ~25, crescendo com N). Ela (a) preenche tudo de timelike → mata o setor magnético
spacelike do fóton; (b) frustra o condensado carregado → mata o A_μ (A5); (c) suprime
flutuações críticas (campo-médio) → mata a transmutação de escala (B7). O meio-DEV não
neutraliza nenhuma dessas três porque seu único acréscimo seria a **escala**, e a escala
não é o que a conectividade aniquila — a conectividade aniquila o **setor spacelike** e a
**criticalidade**, que o meio (uma EFT calibrada, sem substrato próprio) não restaura.

### Por que NÃO é B9-escala nem B9-irmãos
- **B9-escala** exigiria um acoplamento honesto a₀←grafo. A2/A3/B7 já o negaram com
  mecanismo. Rodá-lo seria repetir DEV_FROM_TEIC.
- **B9-irmãos** exigiria que o A_μ coerente da DEV fornecesse o índice spacelike do
  fóton. A1+A5+V2 negam o análogo dos dois lados. Sem pilar vetorial, a opção cai.

### Fichas de experimento
**Nenhuma ficha de 1ª classe é justificada.** O B9 fecha por **composição de campanhas já
medidas** (C1+A1+A5+V2+A2+A3+B7) — não por uma lacuna não-testada. Propor um experimento
novo seria re-rodar mortes existentes ou inserir a₀ à mão (tautológico, proibido pela
guarda).

**Contingência opcional (registrada, não recomendada):** a única micro-pergunta nunca
medida diretamente é se um **campo externo coerente genérico** acoplado ao modo
longitudinal (mimetizando um "meio" **sem inserir a₀**) desloca o expoente de Brezin–
Wallace `χ∥~h^−0.37`. Ficha mínima em `docs/campaigns/B9_CONTINGENCIA.md` (esboço abaixo).
Ela **converteria a morte de mapa em morte medida**, mas o mapa já fecha por composição;
só vale se o usuário quiser o número explícito. **Gate do expoente é bloqueante: se o
campo externo não desloca −0.37, B9 morre medido; se deslocar, reabre só o setor
longitudinal — nunca o transverso (Goldstone) nem o vetorial (ausente).**

---

## Ficha de contingência (opcional) — B9-C1: campo coerente externo desloca χ∥?

- **Pergunta exata:** acoplar o ferromagneto O(3) (fm2_core) a um **campo vetorial
  externo coerente genérico** `b⃗·⟨n⃗⟩` (amplitude varrida, **sem a₀, sem m_A** — número
  puro de rede) desloca o expoente longitudinal de `χ∥~h^−0.37` (Brezin–Wallace) em
  direção a um expoente fracionário diferente (assinatura de transmutação pelo meio)?
- **Sucesso (pré-registrado, verbatim):** "o expoente de χ∥ desloca-se de −0.37 de modo
  monotônico e **estatisticamente significativo** (>3σ, 12+ seeds) com a amplitude do
  campo externo, na direção de X^(3/2) (i.e. para −0.5), **sem** o campo externo carregar
  qualquer escala física → o meio genérico transmuta o setor longitudinal."
- **Morte (pré-registrada, verbatim):** "o expoente de χ∥ permanece em −0.37 ± erro
  (Brezin–Wallace robusto) sob qualquer amplitude do campo externo → o meio **não**
  transmuta o expoente; B9 morre **medido**, confirmando a leitura de mapa (gate B-ii: a
  forma longitudinal é interna e fixa, não responde a um meio)."
- **Gate do expoente (bloqueante):** o setor **transverso** NÃO entra (Goldstone-protegido,
  ∝X fixo — não medir, é teorema). Só o longitudinal χ∥ é o observável.
- **Código:** adaptar `dev_from_teic/A1_longitudinal_mode.py` + `C1_khoury_equivalence.py`
  (estimador Ward + V·Var(m_par)); engine `fm2_core` (E1). **Novo:** termo `−b·(n̂·ê_ext)`
  no Metropolis (número puro). Sob `TEIC/results/b9/` (varrido pela guarda); a₀/β/m_A só
  em `# COMPARISON ONLY`.
- **Custo:** baixo (L=16, ~12 seeds, varredura de 4–5 amplitudes × 4 h — reaproveita
  infra A1/C1; ~horas de CPU).
- **O que destrava:** nada novo se morrer (confirma o mapa); se **passar**, reabre
  **apenas** o canal longitudinal-com-meio — e ainda assim deixaria escala (a₀) e setor
  vetorial mortos. Por isso é contingência, não recomendação.
- **Anti-tautologia:** o campo externo é número puro de rede; **não** é a₀ nem m_A. Não há
  identidade definicional (≠ B1).

---

## Disciplina e próximos passos

- **RESEARCH_MAP primeiro:** registrar B9 como **campanha de mapa fechada NEGATIVA**
  (não experimento) — nova linha: "B9 piano-no-vácuo = INVIÁVEL no mapa; gate do expoente
  mal-posto e já resolvido por C1; setor vetorial morto 3× (A1/A5/V2); escala externa
  (A2/A3/B7); o meio-DEV não restaura nem o índice spacelike nem a criticalidade que a
  conectividade aniquila".
- **Coincidência ρ_vac~ρ_Λ** permanece **[SUGESTIVO]**, não promovida.
- **Guarda:** manter B9 (se a contingência rodar) sob `TEIC/results/b9/`; estender
  `SCAN_DIRS` para `DEV/` apenas se um gerador importar módulo DEV.
- **A fresta honesta (registrada com trava):** tratar a₀ como **condição de contorno
  externa literal** imposta dinamicamente à rede (um "meio" de fronteira real) nunca foi
  testado — mas **qualquer inserção de a₀ é tautológica/proibida**; não há versão honesta.
  Registrado como fronteira fechada, no mesmo espírito da fresta de Janus (COLAPSO_SR).
