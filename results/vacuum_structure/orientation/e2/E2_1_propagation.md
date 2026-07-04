# E2-1 — Dispersão da flutuação de orientação via o operador BD

> Charter: `E2_MAGNON_BD.md` (E2-1). Roda só porque **E2-V PASSOU**. Código:
> `E2_1_propagation.py`; motor: `e2_core.py`; dados: `E2_1_propagation.json`;
> figura: `E2_1_propagation.png`. **NÃO modifica nenhuma campanha anterior.**

## O que E2-1 mede e por quê

E1 estabeleceu que o vácuo causal é um ferromagneto de orientação cujas
excitações suaves são as flutuações transversais δn⃗; E1-3 mostrou que o
Laplaciano de **links nus** dá S(k) plano e não-local (sem rigidez de gradiente,
sem ω=ck) e apontou o d'Alembertiano causal suavizado (Sorkin/BD, e10) como o
operador cinético relativístico que falta. E2-1 mede a dispersão que **B_ε** dá
à flutuação δn⃗.

**Como (validado em E2-V).** A receita literal do charter — propagar δn⃗ pelo
passo de Euler δn(t+dt)=δn(t)+dt·B_ε[δn] e fazer FFT de δn(x,t) — **não é
executável**: esse inverso explícito de B_ε é instável no causal set (E2-V B1:
o modo-zero constante explode a |φ|~1000, a variância pontual de BD documentada).
O observável **estável e equivalente** é o símbolo do operador
λ(k,ω)=⟨f,B_ε f⟩/⟨f,f⟩, f=cos(kx−ωt), cuja **crista de zero** em ω é a dispersão
on-shell ω*(k) (B_ε→□ no contínuo; o símbolo de □ se anula on-shell). Essa
crista de zero é a mesma dispersão que o pico de S(k,ω) traçaria — B_ε é o
propagador inverso, S é o propagador; partilham o lugar geométrico on-shell.

**U(1) vs O(3).** B_ε é um operador **escalar**: age igual na fase δφ (U(1)) e em
cada componente cartesiana de δn⃗ (O(3)). Logo a **dispersão é a mesma** para os
dois candidatos — a estrutura cinética relativística é propriedade do operador do
causal set, não do grupo de simetria interno. Mede-se o símbolo (de componente)
escalar com alta estatística; ele vale para ambos. A diferença U(1)/O(3) —
número e transversalidade das polarizações — é o objeto de E2-3.

## Configuração

```
rho=24  T=10  X=18  eps=0.15   (n≈8650 eventos/semente, 1+1D)
k ∈ [0.40, 1.45] (10 valores)   ω ∈ [0, 1.9] (48)   20 sementes
caixa grande (X=18) para k pequeno limpo; eps=0.15 (regime de E2-V B2)
```

## Resultado — dispersão linear, velocidade ≈ cone de luz

10/10 cruzamentos de zero encontrados; ω*(k) (média sobre 20 sementes ± SEM):

```
 k       ω*(k)          v=ω*/k
-----------------------------------
0.400   0.357 ± 0.047   0.892
0.517   0.423 ± 0.057   0.819
0.633   0.663 ± 0.058   1.047
0.750   0.708 ± 0.060   0.944
0.867   0.836 ± 0.065   0.964
0.983   0.976 ± 0.085   0.993
1.100   1.160 ± 0.083   1.055
1.217   1.213 ± 0.095   0.997
1.333   1.289 ± 0.106   0.966
1.450   1.439 ± 0.078   0.992
```

A velocidade de fase v=ω*/k oscila em torno de **~1.0** em toda a faixa, **sem
tendência sistemática** (⟨v⟩≈0.97). Não há subida em k pequeno (assinatura
massiva) nem subida em k grande (assinatura difusiva ω∝k²): a crista é
**linear**. A velocidade ≈1 é a do cone de luz e é **emergente** — c nunca entra
no gerador (ondas de prova reais, ω varrido livremente).

> Comparado ao aviso de E2-V B2: lá (caixa X=16) o ponto de menor k estava
> *acima* da reta (elevação de tamanho-finito). Aqui (X=18, caixa maior) essa
> elevação desaparece e os pontos de baixo-k caem ligeiramente *abaixo* — o
> resíduo é de tamanho-finito/estatístico, não uma massa. E2-2 quantifica.

## Anti-circularidade mantida

- c nunca inserido; o símbolo é medido do operador BD na rede de Poisson real.
- Ondas de prova são cos reais (sem literal complexo); sementes fixas (2000–2019).
- A forma da dispersão (linear/quadrática/com gap) é o discriminador; c_fit é
  parâmetro livre (E2-2), comparado a 1 só na síntese.

## Saída

`E2_1_propagation.json` guarda ω*(k), SEM, ω* por semente e a grade λ(k,ω); E2-2
faz o ajuste dos três modelos sobre esses dados. A figura mostra o mapa do
símbolo com a crista de zero sobre ω=k e uma reconstrução de δn(x,t) a partir do
ω*(k) medido (substituto estável da propagação direta instável), com o cone
x=±c_med·t.
