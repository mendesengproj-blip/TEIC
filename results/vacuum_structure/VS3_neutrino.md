# VS3 — Neutrino como quasi-defeito sem carga de gauge?

> Charter: `VACUUM_STRUCTURE.md` (VS3). Pergunta: a rede suporta um defeito
> quasi-estável (instável, mas de vida longa) que carrega a marca de spin-½
> (cobertura dupla) **sem** winding de gauge?
> Código: `VS3_neutrino.py`; dados: `VS3_neutrino.json`.
> Infraestrutura: su2_core (SU3) — não modificada.

## Construção (a "bola de torção π")

Na rede quiral SU(2) (quaternions, sem Pauli, sem complexo):

    U(x) = exp(i F(r) σ₃),   F(0) = π,  F(∞) = 0.

Uma torção de **eixo fixo** (embutida em U(1)) cujo centro fica no
antípoda −1. Contabilidade topológica:

- **Marcador ℤ₂ (spin-½):** uma linha radial percorre o caminho 1→−1, que
  projeta no laço **não-contrátil** de SO(3) = o gerador de π₁(SO(3)) = ℤ₂
  — exatamente a estrutura de cobertura dupla que a quantização FR lê
  (MATTER_FR_EXCHANGE, PI1_B2).
- **Sem winding de gauge:** F depende só de r → fase azimutal sem winding
  (gradiente analítico zero).
- **B = 0:** a corrente bariônica é um determinante de comutador,
  identicamente nula numa configuração de eixo fixo (abeliana) — medido.
- **Não-protegida:** mapas S³→S³ com B=0 são conectados ao vácuo. Se houver
  estabilidade, ela é **dinâmica** (mínimo local / vida longa), não
  topológica — precisamente a pergunta do charter.

**Controles:** (i) bump trivial F(0)=π/2 (mesma forma, sem antípoda, sem
marca ℤ₂); (ii) hedgehog B=1 (mesmo perfil radial, eixo radial) — controle
positivo topologicamente protegido.

## Nota de validade (primeira rodada descartada)

A rodada inicial em dx=0.5 foi **inválida**: o controle protegido (hedgehog)
*também* desenrolou (B 0.88→0, τ_flow=28) — o vazamento de B em rede grossa
que VS4 documentou. Sem um controle que se mantém, não há comparação. Refeita
em **dx≈1/3** (a classe de resolução de SU3), rate=0.001 (testado: 0.002
diverge). Aí o hedgehog se mantém e a comparação é significativa.

## Resultado (fluxo de gradiente, 500 iterações, dx=1/3)

```
objeto       τ_flow   a0_min(final)   E: inicial→final   plateau?
hedgehog     None     −0.97           319 → 347 (const)  SIM (marcador preso ∀ it)
π-twist       75      +0.41            86 →  34 (desce)   NÃO (descida monótona)
half_bump      5      +0.84            22 →   9 (desce)   NÃO (descida monótona)
```

Os *tracks* são decisivos:

- **hedgehog:** E em plateau (330–347), a0_min travado em −0.96 por **todas
  as 500 iterações**; B conservado ~0.53. O antípoda **nunca** se perde —
  protegido topologicamente (π₃).
- **π-twist:** E desce monotonicamente 86→34; a0_min sobe monotonicamente
  −0.98→+0.41, cruzando −0.5 em it≈75. **Nenhum plateau, nenhuma barreira** —
  desenrola continuamente para o vácuo, B≡0 o tempo todo.
- **half_bump:** mesma descida monótona, começando de a0_min=+0.1.

## O confound e por que a conclusão sobrevive

O π-twist dura 15× mais que o bump trivial (τ_flow 75 vs 5) — mas isso é
**só amplitude inicial**, não metaestabilidade: ele parte de um antípoda
cheio (a0=−1, mais deformação a dissipar) contra o a0=0 do bump. O
discriminador correto é *amplitude-independente*: a presença de **plateau**.
O hedgehog tem plateau (marcador preso enquanto o campo relaxa); o π-twist
não tem — sua curva a0_min(it) é qualitativamente idêntica à do bump
trivial, só deslocada. A marca ℤ₂ não fornece barreira alguma.

## Veredito

```
[x] CRITÉRIO DE MORTE DISPARA: a marca ℤ₂ de spin-½ SEM winding topológico
    (B=0) não produz objeto quasi-estável — desenrola para o vácuo
    exatamente como uma perturbação trivial (monótono, sem plateau de
    energia), distinguindo-se dela só pela amplitude inicial. Todo objeto
    spin-½ estável da rede exige a proteção topológica π₃ (B≠0) que o
    hedgehog tem e o π-twist não.
[ ] Quasi-defeito neutro de vida longa — NÃO encontrado.
```

**Não há neutrino sem carga na rede, neste probe.** A lição estrutural: a
marca de spin-½ vive em π₁(SO(3))=ℤ₂ (o caminho 1→−1), mas é a **carga
π₃=ℤ (B)** que confere estabilidade — e B só vem do hedgehog completo, que
na correspondência carrega os números quânticos de um bárion. O único
objeto da rede capaz de spin-½ estável é o Skyrmion B=1, **carregado**.
Spin-½ e estabilidade estão amarrados à carga topológica; separá-los
(o que um neutrino exigiria) não funciona aqui.

## Escopo honesto (o residual)

- O probe testa a torção de **eixo fixo** (a realização ℤ₂ mais simples sem
  gauge). Não exclui que um setor *além* de SU(2) (p.ex. SU(2)×U(1) com
  quebra, FL2) tenha um modo neutro de vida longa por outro mecanismo —
  registrado como direção, não afirmação.
- "Vida longa" foi medida por fluxo (relaxação) e por tempo real (leapfrog
  geodésico, w₀=0); ambos concordam (π-twist decai, hedgehog se mantém no
  fluxo). A dinâmica de tempo real é menos limpa para o marcador (o campo
  oscila com w₀=0); o peso está no fluxo.

Anti-circularidade: quaternions (4 reais); "neutrino"/"spin" só como nomes;
nenhuma massa/vida-alvo inserida; dados iniciais determinísticos; e_sk=4,
grade fixados de antemão.
