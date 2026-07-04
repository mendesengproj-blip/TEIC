# OP1 — Mapa operadores da rede ↔ exclusões observacionais

> Ataque 3 do `ROADMAP_REVOLUCAO.md`. Análise teórica + literatura (sem simulação).
> Pergunta: **os operadores que a rede proíbe (§9.5 do Paper I) coincidem com os que a
> observação excluiu? E o conjunto que a rede seleciona sobrevive aos limites atuais?**

## Veredito: **SIM nos dois sentidos** — a seleção da rede coincide com a seleção observacional

```
SELECIONADOS (5):  todos sobrevivem a GW170817 (|c_g/c−1| ≤ 5×10⁻¹⁶) e aos limites LIV
PROIBIDOS (5):     incluem as DUAS classes executadas observacionalmente:
                   Horndeski G4X/G5  ← GW170817 (2017)
                   frame preferencial ← Fermi-LAT E_QG,1 > 7.6 E_Planck (2013)
```

---

## 1. Os cinco operadores selecionados vs limites atuais

| Operador (Paper I, Tab. 1) | Classe EFT | Efeito em c_T | Limite relevante | Sobrevive? |
|---|---|---|---|---|
| X=(∂θ)² | k-essence / P(X) | nenhum (acoplamento mínimo) | GW170817 | ✅ |
| √(1−X/X₀) (DBI) | P(X) não-linear | nenhum — só o som *escalar* varia, não o tensor | GW170817 | ✅ |
| A_μ∂^μθ (Stückelberg) | vetor-escalar mínimo | nenhum (sem acoplamento não-mínimo à curvatura) | GW170817; Baker+17 cobre vetor-tensor | ✅ |
| F_μνF^μν | Maxwell | nenhum | — | ✅ |
| A_μA^μ (Proca) | massa vetorial | nenhum; m_A é escala galáctica ajustada (A_μ não é o fóton) | quinta força / fits galácticos | ✅ |

**Ponto estrutural:** o conjunto inteiro é *minimamente acoplado* — θ e A_μ entram sem
acoplamentos não-mínimos à curvatura (a relação de soldering proíbe θ independente de g,
e a rede não fornece termos G_μν A^μ A^ν). É exatamente o acoplamento não-mínimo que
altera c_T. **A rede não poderia ter escolhido um conjunto que viola GW170817 — os
termos perigosos estão na lista proibida por razões internas (causais/combinatórias),
não por ajuste pós-2017.**

## 2. Os cinco operadores proibidos vs exclusões observacionais

| Proibido (§9.5) | Razão interna (rede) | Exclusão externa (observação/teoria) |
|---|---|---|
| θ independente de g (Horndeski geral: G₄(θ,X), G₅) | soldering θ=(M/α)δρ/ρ₀ | **GW170817+GRB170817A**: \|c_g/c−1\| ≤ 5×10⁻¹⁶ mata G₄ₓ/G₅ (Ezquiaga–Zumalacárregui PRL 119 251304; Creminelli–Vernizzi 251302; Baker+ 251301; Sakstein–Jain 251303 — todos 2017) |
| n^μ∂_μθ com n fixo (Hořava–Lifshitz) | Poisson é LI; frame fixo quebra | **Fermi-LAT GRB 090510**: dispersão linear em E/M_Pl excluída, E_QG,1 > 7.6 E_Planck (Vasileiou+ 2013, arXiv:1308.6403); + GW170817 |
| ∂_t³θ | viola a ordem parcial causal | (sem análogo direto; exclusão estrutural) |
| □²θ (Weyl) | fantasma de Ostrogradsky | exclusão teórica padrão (instabilidade) |
| Yang–Mills não-abeliano *no setor gravitacional* | U(1) simples nos links | (sem análogo; nota: o setor de *matéria* do Paper II usa SU(2) — andar de cima) |

## 3. R1 é a contraparte microscópica do limite de Fermi-LAT

O contraste central de R1 — grade regular quebra a isotropia a **17%** vs **0.8%** de
Poisson — não é curiosidade numérica. Uma discretização regular do espaço-tempo produz
genericamente dispersão de fótons dependente de energia na escala da granularidade; se a
granularidade é Planckiana e o termo principal é linear, **Fermi-LAT já a executou**
(E_QG,1 > 7.6 E_Planck). A discretização de Poisson preserva LI *em distribuição* —
nenhuma dispersão sistemática na média.

**Isso converte a pergunta "por que Poisson?" (Q1 do revisor) em afirmação observacional:**

> Poisson não é uma conveniência: é a única discretização que sobrevive simultaneamente
> ao teste interno (R1) e ao limite externo (Fermi-LAT). Discreteness regular está
> observacionalmente morta; discreteness de Poisson é a sobrevivente única.

## 4. O conteúdo preditivo (para frente, não só pós-dição)

Honestidade: os itens 1–2 são **consistências/pós-dições** (GW170817 é de 2017). O
conteúdo *para frente* é a rigidez da seleção — a rede não tem botões para acomodar:

1. **c_T = c exatamente, para sempre.** Qualquer detecção futura confirmada de
   \|c_g/c−1\| ≠ 0 (e.g. LISA, ET) falsifica a seleção de operadores da rede inteira.
2. **Dispersão de vácuo de fótons exatamente nula na média.** Qualquer detecção
   sistemática de dispersão ∝E/M_Pl (CTA, LHAASO em GRBs) falsifica a discretização
   de Poisson — e com ela R1. Distingue TEIC/CST de Hořava e de fenomenologia LQG
   com dispersão.
3. **Sem quinta força de range infinito no setor vetorial** (massa de Proca m_A ≠ 0
   é estrutural: links finitos quebram U(1) — Paper I §9.4).

## 5. Limitações desta análise

- Análise de operadores em nível de árvore; loops podem gerar operadores proibidos com
  coeficientes suprimidos (padrão em EFT — não calculado aqui).
- A violação de Lorentz O(1) **não resolvida** do setor vetorial (E/B≈3, §13(9)) é a
  ameaça interna a este quadro inteiro: se a restauração por smearing falhar, o item 2
  acima vira *autofalsificação*. Ver "obrigação de sobrevivência" no roadmap.
- PRLs citadas conferidas por busca (jun/2026): o limite \|c_g/c−1\| ≤ 5×10⁻¹⁶ e
  E_QG,1 > 7.6 E_Planck (subluminal, GRB 090510) confirmados na literatura.

## Fontes

- LIGO/Virgo/Fermi, GW170817+GRB170817A (ApJL 848, L13, 2017)
- Ezquiaga & Zumalacárregui, PRL 119, 251304 (2017), arXiv:1710.05901
- Creminelli & Vernizzi, PRL 119, 251302 (2017), arXiv:1710.05877
- Baker et al., PRL 119, 251301 (2017), arXiv:1710.06394
- Sakstein & Jain, PRL 119, 251303 (2017), arXiv:1710.05893
- Vasileiou et al., PRD 87, 122001 (2013), arXiv:1308.6403 (Fermi-LAT, GRB 090510)
