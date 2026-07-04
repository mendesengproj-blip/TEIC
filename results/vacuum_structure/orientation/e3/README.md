# results/vacuum_structure/orientation/e3 — campanha E3_DEFECTS (jun/2026)

> Charter: `E3_DEFECTS.md` (raiz). Terceira campanha executada de
> `NIVEL4_ORIENTATION.md` (entrada FN3). Continua E1+E2. Pergunta central: os
> defeitos topológicos de n⃗ (hedgehog, B=1) são estáveis sem SU(2) nem Skyrme?
> **NÃO modifica nenhuma campanha anterior.**

| Sub-exp | Pergunta | Veredito | Arquivos |
|---|---|---|---|
| **E3-V** | B medido corretamente (hedgehog +1, vácuo 0)? | **PASS** — +1/−1/0 a 1e-6, O(3)-invariante (\|dB\|=2e-16), local/aditivo, inteiro em L=8..40 | `E3V_gate.{py,md,json,png}` |
| **E3-1** | hedgehog B=1 sobrevive à relaxação? | **Cenário B (metaestável)** — B=1 preservado no gradiente T=0; r_eff→0.32·L; MC térmico des-enrola B→0 em ~2700–2800 sw (20 sementes, sobrev. 20–30%) | `E3_1_stability.{py,md,json,png}` |
| **E3-2** | E(λ) tem mínimo de Derrick? | **NÃO** — parede em λ<1, platô em λ>1; E∝L (R²=1.0, marginal); curvatura não estabiliza | `E3_2_derrick.{py,md,json,png}` |
| **E3-3** | defeito gravita (θ~M/r)? | **PARCIAL** — ρ~1/r² e θ ajusta 1/r (R²=0.99) mas M(r)~r não satura (massa não-localizada) | `E3_3_gravity.{py,md,json,png}` |
| **E3-4** | catálogo | anti-hedgehog B=−1 sobrevive; dipolo (+1,−1) **aniquila** (E:1192→0); toroidal B=0, decai | `E3_4_catalog.{py,md,json,png}` |
| **E3-5** | síntese | **B — METAESTÁVEL** | `E3_5_synthesis.md` |

Motor: `e3_core.py` (rede cúbica L³ **aberta** com grade de coordenadas; texturas
hedgehog/anti/dipolo/toroidal; carga B = grau por ângulo sólido de Berg–Lüscher
— 12 triângulos esféricos por cubo, Van Oosterom–Strackee; gradiente descendente
em S² e Monte Carlo checkerboard de BC livre; funcional de Derrick Σ(1−n_i·n_j);
dilatação trilinear). Self-test: `python e3_core.py`.

## Resultado de uma linha

**O ferromagneto causal nu dá um defeito topológico METAESTÁVEL, não matéria
estável.** O hedgehog B=1 sobrevive ao gradiente descendente (a discretização
regulariza o colapso de Derrick e segura uma carga de ponto), mas E(λ) não tem
mínimo confinante (E∝L, marginal de escala), a barreira que o protege é finita
(des-enrola termicamente em ~2700 sweeps), a curvatura induzida não estabiliza, e
a "massa" não localiza (θ~1/r só aparente). E2 deu o **fóton** limpo do
ferromagneto; E3 mostra que a **matéria estável ainda precisa de SU(2)+Skyrme**
(Paper II permanece). Pares (+1,−1) aniquilam; anti-hedgehog B=−1 existe.

## Notas numéricas para reuso

- **Rede ABERTA, não periódica:** um toro não carrega carga de ponto líquida (Σ
  de cubos = grau da fronteira = 0). BC livre permite o des-enrolamento; é o
  substrato correto para um único defeito.
- **B precisa de COOLING sob MC:** a T finita o estimador de ângulo sólido capta
  ângulo fracionário espúrio de cada ruga térmica. Medir B após ~30 passos de
  gradiente (protocolo padrão de carga topológica na rede). Sem cooling, B oscila
  ±5 e é inútil; com cooling, inteiro limpo.
- **Gradiente descendente Jacobi:** dt≤0.15 é monótono; dt=0.2 explode
  (E:84→324). Default dt=0.1.
- **Dilatação:** usar interpolação **trilinear**; vizinho-mais-próximo injeta
  energia de gradiente espúria por subamostragem em λ>1 (faz uma textura
  marginal parecer ter mínimo interior). Bug do teste, não da física.
- **Sinal de Derrick:** perfil assimétrico — parede UV em λ<1 (regulariza o
  colapso, mecanismo 1) + platô plano em λ>1 (marginal). Não confundir o
  argmin≈0.85 (pé da parede) com mínimo confinante: checar subida nos DOIS lados.
- **Medida decisiva e sem artefato:** E(hedgehog)∝L (R²=1.0) ⇒ marginal de
  escala. Single eval, barato até L=80.

## Regras (as de sempre)

Kill criteria pré-registrados no charter antes de rodar ("B(t)→0 = Veredito C",
pontuado como escrito — B não colapsa no gradiente, só des-enrola termicamente ⇒
metaestável, não morte); gate de engenharia (E3-V) antes de medição física;
negativos/limitações reportados (curvatura não estabiliza; θ~1/r só aparente;
mecanismo 3 / topologia causal não explorado — rodou no substrato espacial de
E1); anti-circularidade (B = ângulo sólido; E = funcional de ligações;
"matéria"/"partícula"/"massa" só na síntese, COMPARISON ONLY; sementes fixas).
