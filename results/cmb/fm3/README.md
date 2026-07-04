# results/cmb/fm3 — campanha FM3_PRIMORDIAL_TEXTURE (jun/2026)

> Charter: `FM3_PRIMORDIAL_TEXTURE.md` (raiz). Nasce da imagem mental
> `TEIC_DEV_VISION.md` §6. Pergunta: a relíquia da transição ferromagnética do
> universo jovem (Kibble), congelada por causalidade (E3b), é a peça fria-e-grande
> que faltou em S8? **NÃO modifica campanhas anteriores.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **FM3-V** | E1 transição + E3b congelamento + Kibble? | **PASS** — J_c≈0.693; B 1→1; quench lento → menos defeitos | `FM3V_gate.{py,json}` |
| **FM3-1** | relíquia se forma (Kibble-Zurek)? | **SIM** — n_def 40→9, n_def~τ^−0.42, **escala cosmológica** | `FM3_1_kibble.{py,md,json,png}` |
| **FM3-2** | é frio e congelado? | congelado super-horizonte (E3b) MAS **w_eff=−0.43≈−1/3, NÃO frio (w=0)**; coarsena t^−1.75 | `FM3_2_freezing.{py,md,json,png}` |
| **FM3-3** | suprime σ8? | **NÃO** — w=−1/3 é ativa/suave, não CDM frio | `FM3_3_growth.md` |
| **FM3-4** | sobrevive ao Planck? | difere de Turok scaling, mas isocurvatura ativa → só subdominante | `FM3_4_cmb_signature.md` |
| **FM3-5** | síntese | **C — escala certa, equação de estado errada** | `FM3_5_synthesis.md` |

Motor: `fm3_core.py` (quench Kibble–Zurek através de J_c via `fm2_core`; contagem de
defeitos pela carga de ângulo sólido de `e3_core` após cooling fixo; comprimento de
coerência; equação de estado w_eff via escala de gradiente sob dilatação; coarsening).
Self-test: `python fm3_core.py`.

## Resultado de uma linha

**O relíquia primordial tem a ESCALA certa mas a EQUAÇÃO DE ESTADO errada.** A
transição de E1 deixa, via Kibble–Zurek, uma teia de defeitos de n⃗ **cosmológica**
(FM3-1) — resolvendo o problema de escala que matou FM2 — e congelada super-horizonte
pela rigidez causal de E3b (FM3-2). **Mas a textura congelada é w≈−1/3 (tipo monopolo
global), não w=0 (frio CDM):** "congelado por causalidade" é **frio de posição**, não
**frio de pressão**. Logo não clusteriza como matéria fria nem suprime σ8 (FM3-3); como
fonte ativa de isocurvatura só sobrevive ao Planck como subdominante (FM3-4).
**Veredito C — mas por um motivo novo e informativo**, completando o mapa
FM1(realça)→FM2(escala errada)→FM3(equação de estado errada).

## Honestidade / engenharia

- **FM3-V valida** o motor (E1 J_c≈0.693; E3b congela B; Kibble qualitativo).
- **Lição conceitual** (resultado positivo): **frio de posição (congelado) ≠ frio de
  pressão (w=0)**. Uma textura de orientação congelada tem w=−1/3; CDM de verdade
  exigiria componente massiva que clusteriza.
- **Anti-circularidade:** J_c, n_def, w_eff, coarsening — da rede; a₀ de SPARC; nenhum
  σ8/Planck/Turok inserido. Janelas (fria, grande, suprime, CMB-OK) fixadas antes.
- **Caveats:** expoente de Zurek (0.15 vs O(3) ~0.29) por L=20 finito — formação do
  relíquia robusta, expoente exato pede redes maiores; FM3-3/4 são direção (CLASS +
  fonte de defeitos para números exatos). Carga em torus: total≈0, conta-se Σ|q|
  (pares) após cooling.

## Regras (as de sempre)

Charter pré-registrado com predições + morte ANTES do código; gate de engenharia
(FM3-V) reproduz E1/E3b; negativos reportados (w errado, não suprime) E positivos
(relíquia forma na escala certa; lição posição≠pressão); anti-circularidade (medido
na rede, nada de σ8/Planck inserido); 20 sementes em FM3-1/2. Veredito C registrado
sem inflar a teoria. Ver `FM3_5_synthesis.md`.
