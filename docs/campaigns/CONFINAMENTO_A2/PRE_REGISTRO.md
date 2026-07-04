# PRE-REGISTRO — A2 / C3 · Loops de Wilson SU(3) no substrato causal

> Campanha de organização TEIC (Fase 2), Frente A (CONSOLIDAR), item A2 = C3.
> **Maior risco de obsolescência da frente** (pode rebaixar/qualificar o claim de
> confinamento do Paper SU3). Gate A1 já VERDE (su3_core + causet sob a guarda).
> Fontes: `HIERARQUIA_EXPERIMENTOS.md` §C3, E5/E7 (obstrução de não-localidade),
> `paper/submission/su3_prd/PAPER_SU3.tex`. Pré-registro antes de rodar.

---

## 1. Pergunta

O confinamento SU(3) (V~σr, σ=Creutz>0) medido **vale no causet**, ou depende do
lattice cúbico de controle? Qual o erro sistemático da não-localidade do causal set
sobre σ?

**Fato verificado no paper (mitiga o risco):** o Paper SU3 já escopa o confinamento
ao **lattice cúbico 8⁴** explicitamente ("Wilson loops on an $8^4$ lattice"); só o
**ferromagnetismo** é reivindicado nos dois (cúbico E causet). Logo A2 não rebaixa um
claim publicado de "confina no causet" — esse claim **não existe**. A2 ou **promove**
(se o causet confinar de forma limpa) ou **confirma** o escopo cúbico-honesto (se a
obstrução E5/E7 se estende ao SU(3)).

## 2. Contexto E5/E7 (herdado, não re-descoberto)

E7 mediu Wilson loops **U(1)** no causet e bateu na **obstrução E5-1b**: o
discriminador padrão-ouro (razão de Creutz χ(R,T)) exige **retângulos R×T
controlados**, ausentes no causet não-local; o método de *patch* (surrogate)
**já rotula errado o ponto cúbico sabidamente confinante** → INCONCLUSIVO. Ponto
crítico para SU(3): o patch de E7 soma `coeff·θ` (**abeliano**); a holonomia SU(3)
é um **produto ORDENADO de matrizes** — o truque de cancelamento de links não se
estende ao não-abeliano. A obstrução tende a ser **pior** para SU(3).

## 3. Critério de sucesso / morte (congelado)

- **SUCESSO:** σ_causet > 0 com significância **E** concorda com σ_cúbico dentro de
  uma barra sistemática **quantificada** (origem na não-localidade grau∝L^~3) →
  claim "confina no causet" passa a ser suportado → **promover** o Paper SU3.
- **MORTE / FRONTEIRA:** σ_causet **indistinguível de 0**, OU a não-localidade
  impede qualquer estimador área-vs-perímetro limpo (como em E7: sem retângulo R×T
  controlado, holonomia não-abeliana de patch não-construível) → confinamento SU(3)
  fica **[FRONTEIRA] como E5/E7** no causet; o Paper SU3 **mantém** (correto) o
  confinamento como **cúbico-só** — sem rebaixamento, com a fronteira documentada.

## 4. Protocolo (anti-circular, duas etapas)

1. **MC de gauge SU(3) numa lista arbitrária de plaquetas** (links = matrizes SU(3),
   holonomia = produto ordenado U_l0^{s0}…U_l3^{s3}, ação β·Σ(1−⅓ReTr W)). Proposta
   near-identity via `su3_core.su3_from_coords`.
2. **STAGE A (validação, lattice 4D regular):** reproduzir o confinamento via Creutz
   χ(2,2)>0 (padrão-ouro em retângulos R×T controlados) em β forte — bate com FLC
   (σ=1.35 em β=4.0 etc.). Valida o MC + estimador.
3. **STAGE B (causet):** MC SU(3) nas plaquetas de diamante causal. Medir o
   plaqueta fundamental ⟨W₁⟩(β) (único loop SU(3) controlado no causet). Demonstrar
   **quantitativamente** que (i) não há retângulo R×T controlado (todas as plaquetas
   são diamantes de altura-2, área=1), e (ii) a holonomia não-abeliana de patch não
   fecha um loop limpo → **σ (declive de área-lei k≥2) é inmensurável** → obstrução.
4. Veredito por §3. Só grafo + ação de Wilson; nenhum σ/α_s/massa inserido.

## 5. Anti-circularidade

`su3_core.py` e o causet já sob a guarda A1. O novo driver passa as duas guardas
(dilatação + literais de escala); sem literais imaginários crus (matrizes via
su3_core). σ emerge da medida; β é varrido, nunca input. Palavra "quark" não entra.

## 6. Entregáveis

`a2_su3_causet.py`, `a2_su3_causet.json`, `SYNTHESIS.md`; atualização do RESEARCH_MAP
(linha confinamento / fronteira E5/E7) e nota de confirmação do escopo do Paper SU3.
