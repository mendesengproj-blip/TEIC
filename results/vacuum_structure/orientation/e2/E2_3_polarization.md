# E2-3 — Polarização da flutuação de orientação

> Charter: `E2_MAGNON_BD.md` (E2-3). Roda só porque **E2-2 confirmou dispersão
> linear** (ω=ck). Código: `E2_3_polarization.py` (reusa o gerador de E1
> `orientation_core.py` sem modificação); dados: `E2_3_polarization.json`;
> figura: `E2_3_polarization.png`. **NÃO modifica nenhuma campanha anterior.**

## O que se mede

No estado O(3) ordenado ⟨n⃗⟩=m̂ (vácuo ferromagnético de E1, J=2.0≫J_c), a
flutuação do vetor unitário separa em:

- **Transversal a ⟨n⃗⟩**: dois componentes δn⃗_⊥ no plano tangente de S² — as
  direções de Goldstone da simetria quebrada (O(3)→O(2): 3−1 = **2** modos);
- **Longitudinal a ⟨n⃗⟩**: δn_∥ = (n⃗·m̂) − ⟨n⃗·m̂⟩, a amplitude.

Mede-se a **potência de flutuação** (variância) em cada setor, média sobre 8
sementes × 40 amostras de equilíbrio, no causal set real (⟨grau⟩≈130, M≈0.996).

## Resultado

```
potência transversal-a-⟨n⟩ (por componente):  4.29e-03 ± 4e-06
potência longitudinal-a-⟨n⟩               :  2.34e-05 ± 9e-08
razão transversal/longitudinal            :  183 : 1
modos transversais dominam (setor suave)?  SIM
contagem de Goldstone: O(3)→O(2) = 2   (= polarizações do fóton);  U(1) = 1
```

Os modos **suaves (sem massa) são os dois Goldstones transversais**; a amplitude
longitudinal é rígida (gap), com potência ~180× menor. A **contagem (2)** bate
com as duas polarizações do fóton.

## Escopo honesto (declarado, não escondido)

"Transversal" aqui é transversal-a-⟨n⃗⟩ no **espaço interno** S² (sentido de
Goldstone). O teste de polarização do fóton no charter (δn⃗ ⊥ à direção de
propagação k⃗) é uma transversalidade **diferente**, no espaço real. Num sigma
model O(3) simples os dois Goldstones são dois **escalares internos**; sua
**contagem (2)** iguala as polarizações do fóton, mas a transversalidade de gauge
plena a k⃗ (k⃗·A⃗=0) exige identificar o índice interno com o índice de
espaço-tempo — estrutura que o sigma model nu **não** fornece sozinho.

## Veredito

```
VEREDITO (E2-3): TRANSVERSAL-DOMINANTE.
  Os modos suaves são os dois Goldstones transversais (razão 183:1); a amplitude
  longitudinal tem gap. A contagem (2) iguala as duas polarizações do fóton.
  CAVEAT: transversalidade INTERNA; a transversalidade de gauge a k⃗ precisa de
  uma identificação interno↔espaço-tempo não fornecida pelo sigma model nu.
```
