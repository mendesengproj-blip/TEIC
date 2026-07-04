# PROMPT — VACUUM_STRUCTURE: Estrutura do Vácuo TEIC-DEV

> Charter da campanha (salvo na raiz por instrução do prompt; índice de
> charters em `docs/prompts/README.md`).
> Dois objetivos:
> 1. Formalizar a correspondência TEIC↔DEV como documento canônico
> 2. Identificar os experimentos que probam a estrutura do vácuo
> Resultados em `results/vacuum_structure/`.

---

## PARTE 1 — Documento Canônico: A Correspondência TEIC↔DEV

### O que criar

`TEIC_DEV_CORRESPONDENCE.md` — o documento mais importante
da teoria, que nenhum paper isolado contém completamente.

Este documento deve responder:

**O que é o vácuo DEV na linguagem microscópica da TEIC?**

A resposta já foi derivada em fragmentos por toda a investigação.
O trabalho aqui é consolidar, não descobrir.

Construir a tabela de correspondência completa:

```
TEIC (microscópico)    →    DEV (efetivo)    →    Física observada
```

Para cada objeto:
- eventos causais
- links causais
- densidade ρ
- fase de gauge φ
- campo θ = δρ/ρ₀
- isotropia de Poisson
- saturação DBI
- defeitos topológicos U(1)
- defeitos topológicos SU(2)
- condensado ρ_dinâmico

Mostrar onde cada correspondência foi DERIVADA (com referência
ao experimento) e onde é IDENTIFICAÇÃO (proposta mas não derivada).

### Os campos hidrodinâmicos

Definir formalmente os campos hidrodinâmicos da rede:

$$\rho(x) = \text{densidade local de eventos causais}$$
$$J^\mu(x) = \text{fluxo causal}$$
$$Q(x) = \text{conectividade média (links por evento)}$$
$$\Phi(x) = \rho_{\rm din} \cdot e^{i\bar\phi} \quad
  \text{(campo complexo emergente, de PHI\_EMERGE)}$$

Esses são os "campos de ordem" do vácuo.

### As fases do vácuo

Identificar as três fases da rede:

**Fase normal** (ρ = ρ₀ uniforme, sem defeitos):
- Fótons = perturbações propagantes □θ = 0
- Gravidade = deformação lenta de θ ao redor de matéria
- DEV no regime fraco

**Fase condensada** (⟨|Φ|⟩ = v ≠ 0):
- Campo vetorial massivo m_A = e·v
- Vórtices estáveis existem
- Matéria = defeitos topológicos estáveis
- DEV no regime de campo médio

**Fase saturada** (local, |θ| > θ_c):
- Regime DBI não-linear
- Criação de defeitos topológicos possível
- Análogo do plasma de QED em campo forte
- Experimento de Oxford: vacuum four-wave mixing

### A hierarquia completa

Escrever a hierarquia de 6 níveis:

```
Nível 0: Rede causal (eventos + links)
Nível 1: Hidrodinâmica causal (ρ, J^μ, Q)
Nível 2: DEV — teoria efetiva (θ, A_μ, DBI)
Nível 3: Defeitos topológicos (vórtice, Skyrmion)
Nível 4: Modelo Padrão (em aberto)
Nível 5: Cosmologia
```

Para cada nível: o que foi DERIVADO, o que foi IDENTIFICADO,
o que está EM ABERTO.

---

## PARTE 2 — Experimentos que Probam a Estrutura do Vácuo

### VS1 — O Higgs como condensado causal

**Pergunta:** ⟨ρ_dinâmico⟩ ≠ ρ₀ espontaneamente?

PHI_EMERGE_V2/V3 mostrou que ρ_dinâmico se depleta no núcleo
do vórtice quando inicializado. A questão aberta é se essa
depleção ocorre espontaneamente — sem inicialização — em
regime de alta densidade.

**O que testar:**
Rodar a rede em regime de alta densidade ρ >> ρ₀ sem nenhum
vórtice inicializado. Medir ⟨ρ_local⟩ vs ρ₀.

Se ⟨ρ_local⟩ ≠ ρ₀ espontaneamente em alguma região:
→ condensado espontâneo
→ Higgs como propriedade do vácuo, não partícula adicionada

**Critério de morte:** ⟨ρ_local⟩ = ρ₀ em todos os regimes.

**Output:** `results/vacuum_structure/VS1_higgs_condensate.md`

---

### VS2 — As fases do vácuo: transição de fase

**Pergunta:** existe uma transição de fase na rede causal
entre fase normal e fase condensada?

Em matéria condensada: transição de Bose-Einstein, superfluidez,
supercondutividade têm transições de fase bem definidas.

Se a rede causal tem transição de fase em função de ρ ou T:
→ o vácuo da DEV tem estrutura termodinâmica
→ a "temperatura do vácuo" é identificável na rede

**O que testar:**
Medir ⟨|Φ|⟩ em função de ρ. Há uma transição abrupta?
Ou a variação é suave?

**Critério de morte:** sem transição — ⟨|Φ|⟩ varia suavemente.

**Output:** `results/vacuum_structure/VS2_phase_transition.md`

---

### VS3 — Neutrinos como quasi-defeitos

**Pergunta:** a rede suporta defeitos topológicos quasi-estáveis
(instáveis mas com tempo de vida longo) sem carga de gauge?

Neutrinos: spin-½, sem carga elétrica, massa muito pequena.

Na linguagem da rede: um defeito topológico no campo escalar θ
que tem winding no setor temporal mas não no setor espacial
(ou vice-versa).

**O que testar:**
Criar uma perturbação localizada que tem estrutura de spin-½
(cobertura dupla) mas não tem winding de gauge U(1).
Medir o tempo de vida.

Se existe um objeto quasi-estável sem carga de gauge:
→ candidato natural a neutrino na rede

**Critério de morte:** todo objeto com spin-½ requer winding
de gauge — sem neutrino sem carga.

**Output:** `results/vacuum_structure/VS3_neutrino.md`

---

### VS4 — Três gerações: há degenerescência topológica?

**Pergunta:** a rede suporta três configurações topologicamente
distintas com os mesmos números quânticos?

As três gerações (elétron/múon/tau, quarks u/c/t, d/s/b)
têm números quânticos idênticos mas massas diferentes.

Na linguagem topológica: seriam três maneiras de enrolar
a mesma deformação, com energias diferentes.

**O que testar:**
Para o Skyrmion SU(2) com B=1, existem múltiplas
configurações estáveis com energias diferentes mas
mesmo número topológico?

Variar a configuração inicial do hedgehog e verificar
se há múltiplos mínimos de energia com B=1.

**Critério de morte:** apenas uma configuração estável com B=1.

**Output:** `results/vacuum_structure/VS4_generations.md`

---

### VS5 — Constantes de acoplamento dos quatro números puros

**Pergunta:** os quatro números puros
(G·ρ²·r_c⁵ = 15/8π², λ²_Sk/⟨a²⟩ = 1/120,
X₀·Δθ²/(ρH²) = π/ln2, m²·λ_p ≈ 520)
determinam as constantes de acoplamento do Modelo Padrão?

A constante de estrutura fina α ≈ 1/137 deveria emergir
de alguma razão adimensional desses quatro números.

**O que calcular:**
Verificar razões entre os quatro números puros e comparar
com α, sin²θ_W (ângulo de mistura eletrofraco = 0.231),
e g_s (acoplamento forte ≈ 1.2 em escala de 1 GeV).

**Critério de morte:** nenhuma combinação dos quatro números
dá as constantes do Modelo Padrão na ordem de magnitude certa.

**Output:** `results/vacuum_structure/VS5_coupling_constants.md`

---

## PARTE 3 — A Narrativa Canônica Completa

Após criar os documentos acima, escrever `TEIC_NARRATIVE.md`
que responde em linguagem física (não matemática):

1. O que é a rede? De que é feita?
2. O que é o vácuo?
3. O que é um fóton?
4. O que é a energia de um fóton?
5. O que acontece na colisão?
6. O que é a matéria?
7. O que é a massa?
8. O que é a carga elétrica?
9. O que é o spin-½?
10. O que está além da rede?

Esta narrativa é o documento que um físico sem conhecimento
prévio da TEIC leria para entender o que a teoria diz.

---

## Honestidade obrigatória em todos os documentos

Para cada correspondência TEIC↔DEV, marcar explicitamente:

**[DERIVADO]:** correspondência demonstrada por experimento
com resultado numérico verificável.

**[IDENTIFICADO]:** correspondência proposta como hipótese
consistente com os dados, mas não derivada.

**[EM ABERTO]:** correspondência ainda não investigada.

Nenhum documento deve fazer parecer que tudo foi derivado.
A distinção é o valor científico principal da investigação.

---

## Prioridade dos sub-experimentos

```
VS5 (constantes de acoplamento): calculável hoje, sem código
VS1 (condensado Higgs): usa infraestrutura existente
VS2 (transição de fase): usa infraestrutura existente
VS3 (neutrino): novo experimento, prazo médio
VS4 (três gerações): novo experimento, prazo médio
```

VS5 primeiro — é um cálculo analítico que pode ser feito
imediatamente com os quatro números já medidos.
