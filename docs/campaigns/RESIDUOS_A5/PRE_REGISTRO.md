# PRE-REGISTRO — A5 / C5 · Resíduos de medição baratos (débito §2 do inventário)

> Campanha de organização TEIC (Fase 2), Frente A, item A5 = C5. **Prioridade mais
> baixa de Tier 1** (barato, não destrava nada a jusante). Gate A1 já VERDE.
> Fontes: §C5, `results/matter/pi1_b2/` (FR/ε), `results/matter/mg/MG1`. Pré-registro
> antes de rodar. Fecha as últimas ressalvas do **Paper MG**.

---

## 1. Pergunta

Os resíduos menores conhecidos fecham?
- **(1) ε(2):** ε(2)=1 (a anomalia de framed-transfer no winding-2 swap) é
  **uniforme** entre **campos winding-2 distintos**, ou depende do campo específico?
  (PI4 declarou: "ε_swap medido num único calibrador; uniformidade ASSUMIDA, não
  provada"; PI5 estabeleceu a lei ε(n)=(n−1)mod2 em n=1,2,3 mas não re-mediu ε(2) com
  2º campo grau-2.)
- **(2) MG1-3D:** o resultado MG1 (θ=G_net·M/r, expoente exterior −1, G_net∝M),
  medido no solver **radial**, sobrevive numa malha **3D Cartesiana completa**
  (sem simetria radial imposta)?

## 2. Critério de sucesso

- **(1)** ≥2 calibradores winding-2 **distintos** de classe **conhecida 0** (Williams
  B mod 2 = 0), variando eixo de rotação-alvo / largura de perfil / resolução, todos
  com topologia swap (1 componente, winding 2) e leitura crua de classe **1** →
  **ε=1 uniforme** → a única ressalva de spin-estatística do bárion é removida; a
  correção ε(2)=1 do PI3 fica suportada por múltiplos campos.
- **(2)** MG1 com fonte Skyrmion na malha **3D Cartesiana** dá **expoente −1 ± 0.10**
  e **G_net=A/M constante** (CV<15%) ao varrer e_sk (massas distintas) → o resultado
  não é artefato de simetria radial.

## 3. Critério de morte

- **(1)** Um calibrador winding-2 distinto de classe 0 dá **ε≠1** (leitura crua ≠1,
  estável) → a anomalia **não é uniforme** na classe swap → a correção ε(2)=1 do PI3
  e a lei ε(n)=(n−1)mod2 / π₁=ℤ₂ precisam **revisão** (resultado de 1ª classe).
- **(2)** O expoente 3D-Cartesiano **não** reproduz −1 (|expo+1|>0.10) OU G_net varia
  com M (CV>15%) → o resultado MG1 era artefato de discretização radial (rebaixar).

## 4. Protocolo

1. **ε(2):** reusar `pi1_core` (axial_b2, loop_target_rotation, z2_class_multi). Rodar
   o calibrador base (PI0b: axial B=2, rotação-alvo isospin-z) + variantes distintas:
   (a) rotação-alvo isospin-**x** e **y** (eixo distinto); (b) **largura de perfil**
   diferente (W=1.5, 2.5); (c) **resolução** N=49. Cada um: classe conhecida 0,
   topologia swap (comps=1), 3 valores regulares, ε=(classe medida ≠ 0). Confirmar
   ε=1 em todos.
2. **MG1-3D:** fonte = densidade do Skyrmion (`su3_core.radial_relax` → eps(r)) numa
   malha **3D Cartesiana** (`d3_audit_core.grid3d/poisson3d_solve`, −K∇²θ=fonte, sem
   1/r inserido); ajustar θ~A/r no exterior → expoente; varrer e_sk → M distintas →
   G_net=A/M constante? Comparar com o radial (expo −0.992). Aspersão irregular
   genuína = **fronteira** (mesma não-localidade de A2/A4), registrada não tentada aqui.

## 5. Anti-circularidade

`pi1_core`, `su3_core`, `d3_audit_core` sob a guarda A1. ε de classe medida (não
inserida); nenhum 1/r ou G no gerador de MG1 (fonte é peso adimensional, expoente
medido). Classe verdadeira do calibrador = Williams (topologia algébrica geral, sem
input FR). Campos iniciais reais (sem fase complexa).

## 6. Entregáveis

`a5_residuos.py`, `a5_residuos.json`, `SYNTHESIS.md`; atualização do RESEARCH_MAP
(linhas ε(n)/π₁ e MG) e nota de fechamento das ressalvas do Paper MG.
