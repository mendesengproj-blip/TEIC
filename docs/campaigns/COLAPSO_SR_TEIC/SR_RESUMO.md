# Resumo fiel da Stochastic Rupture (SR)

> Digest de `SR_v7_full-38.pdf` — G. Zambuzi, *Stochastic Rupture as an
> Information-Bounded Mechanism for Objective Wave-Function Collapse* (v8: "Fisher
> Action, Dyson Convergence, Thermodynamic Cycle"). Resumo descritivo, não-crítico;
> a avaliação contra TEIC está em `RESEARCH_MAP.md`. Distingue o que a SR **deriva**
> do que ela **postula/importa** (o próprio paper é honesto sobre isso).

---

## 1. A ideia central (uma frase)
Um sistema quântico torna-se objetivamente clássico quando a **complexidade de
emaranhamento** do seu diamante causal **satura a capacidade holográfica de
informação** (o limite de Bousso). Quando a razão entropia/limite atinge um valor
crítico **η**, a dinâmica "poda" todos os ramos menos um. Colapso = limiar físico, não
interpretação. A escolha não é ruído — é consequência de geometria informacional.

## 2. A rede microscópica
- Realizada como **rede cúbica simples**: folhas 2D (quadradas, coordenação z=4)
  empilhadas a intervalos de comprimento de Planck ℓ_P (motivação holográfica:
  informação em superfícies 2D). Dispersão exata da rede dá d_s=2 (folha) → 3 (cúbica).
- Os graus de liberdade vivem nos **links** entre N "eventos informacionais"; cada
  link (i,j) carrega um sistema de 2 níveis. dim ℋ = 2^{N(N−1)/2}.
- O **grafo de emaranhamento** é construído do estado quântico pela correlação conexa
  w_ij = |⟨σ_z^i σ_z^j⟩ − ⟨σ_z^i⟩⟨σ_z^j⟩| (não é suposição; é medida do estado).

## 3. O parâmetro de ordem χ_eff (e seus DOIS setores)
χ_eff = **λ_max / N** (maior autovalor do espectro do grafo, normalizado). **Mede
concentração relacional / dominância global (formação de hubs ou integração all-to-all),
NÃO densidade** (Corr(χ,k_max)=0.88; estrela e clique ambos dão χ→1). Dois operadores:

| setor | operador | uso |
|---|---|---|
| **COLAPSO** | adjacência A: χ_eff = λ_max(A)/N | GHZ (K_N) → (N−1)/N→1; Bell → 1/N |
| **geometria** (d_s) | Laplaciano L: χ_eff = λ_max(L)/N | núcleo do heat kernel / dimensão espectral |

(Para Erdős–Rényi os dois coincidem ≈ p.) χ_eff substitui o campo escalar postulado
χ(x^μ) das versões SR v1–v5.

## 4. O mecanismo de colapso
- **Gatilho:** colapso dispara quando **χ_eff ≥ η** (Eq. 88).
- **Poda:** taxa Γ(x) = γ₀/x com x = 1−χ (diverge na saturação). Vem de um fluxo de
  gradiente do potencial V(χ) = η·γ₀·S_rel(χ), S_rel(χ)=−χ−ln(1−χ) ≥ 0.
- **Ciclo termodinâmico:** poda SOZINHA fragmenta a rede (d_s→0); o ciclo completo
  precisa de **restauração** (evolução de Schrödinger restaura conexões quando χ<η).
  Poda → calor de Unruh → campo gravitacional (esfria) → Schrödinger restaura.
- **Colapso = perda de RIGIDEZ ESPECTRAL, não fragmentação** (descoberta numérica
  central, Eq. 170): redes GHZ mantêm conectividade global G_f=G_i=N enquanto χ_eff cai;
  o que colapsa é o modo coletivo global (gap Δλ=λ_max−λ_2; GHZ Δλ~25, Bell ~0.02).
- **Forma quântica:** no limite contínuo, equação mestra de Lindblad com operador de
  colapso L̂ = x̂/σ_x e taxa γ₀ = 4Gm²/(ℏd).

## 5. O parâmetro η (limiar)
- **Definição (Casini):** η ≡ sup_D S_rel(ρ_D‖σ_D)/(A(D)/4Gℏ) — máximo, sobre diamantes
  causais, da entropia relativa sobre o limite holográfico. Bousso garante η ≤ 1;
  colapso quando η→1. Estendido a estados não-Gaussianos via operador modular de
  **Tomita–Takesaki** K=−ln Δ_D.
- **Valores:** η ≈ **0.1** (macroscópico: He-4, supercondutores, calibrado via Casini);
  η ≈ **0.99** (NISQ, usado em simulações). Para um qubit de lab isolado η~10⁻⁶⁸ → sem
  colapso. **A derivação de η de 1º princípios permanece ABERTA.**
- **Cheque de percolação (consistência, não derivação):** p_c·N = −ln(1−√η)/√η ≈ 1+√η.
  p_c(cúbica, ligação)=0.2488 ≈ e_0 (parâmetro cosmológico S8 do paper-companheiro ICR).
  SR opera no regime **sub-percolante** (colapso é local, não global).

## 6. Separação GHZ/Bell (o teste mais acessível)
Para N qubits: χ_GHZ=(N−1)/N≈1, χ_Bell=1/N. Janela de separação **N > 1/η**: GHZ colapsa
(χ≥η), Bell fica estável. η=0.1→N>10; η=0.99→N>100 (com colapso confiável em N≈125,
correção de tamanho finito N_stable≈1.25/(1−η)).
- **Tempo de colapso (predição nativa, Path B):** **τ_Bell/τ_GHZ ~ N²** (do limiar
  espectral). N=32, η=0.99 → ≈5569.
- **Avalanches (criticalidade auto-organizada):** GHZ ⟨s⟩≈5–6, s_max=N (cascatas
  globais); Bell ⟨s⟩≈2 (dissipação local). P(s)~s^{−τ}, τ≈2.05 (3D) ou 3/2 (ER).

## 7. O discriminador experimental central: escala σ_x⁻²
| modelo | taxa Γ | escala σ_x | escala m |
|---|---|---|---|
| **SR** | Gm²/(4ℏσ_x²) | **σ_x⁻²** | m² |
| CSL | … | σ_x⁻³ | m² |
| Diósi–Penrose | Gm²/(ℏ|Δρ|) | flat | m² |
SR e CSL têm a mesma escala de massa (m²) mas diferem em σ_x: este é o discriminador
limpo, acessível no regime de massa do **MAQRO** (10⁹–10¹⁰ amu). SR evita as restrições
de aquecimento CMB/Lyman-α (que pressionam CSL em 27–39 ordens) porque o gatilho só
dispara perto da saturação.

## 8. Setor geométrico (CONDICIONAL — caveat declarado pelo autor)
SR tem **dois setores logicamente independentes**: o de **colapso** (§3–5, autônomo,
falsificável) e o **geométrico** (§6–7, gravidade/Einstein). O geométrico é **condicional
a um fluxo dimensional d_s: 2→4** (ponto de sela SR dá o UV holográfico d_s≈2 =
Asymptotic Safety / CDT; o 4D clássico deve emergir no IR). **A derivação RG desse fluxo é
um problema ABERTO.** Condicional a isso, emergem por seis cadeias: lei de Newton
(F=GM/r², G_SR=γ₀r_s/M), assinatura de Lorentz, invariância de difeomorfismo (de
invariância de permutação), equações de Einstein, propagador spin-2 (Fierz–Pauli),
temperatura de Unruh. Cosmologia: fluxo de Hubble da dinâmica de poda; Λ_eff=3γ₀²/4.

## 9. Novidades da v7/v8 (4 derivações novas)
1. **Ação de Fisher:** o termo cinético ½g^μν∂_μχ∂_νχ emerge da contração do tensor de
   informação de Fisher (antes ad-hoc).
2. **Movimento Browniano de Dyson:** o ruído espectral da rede é exatamente um DBM
   (repulsão de autovalores 2Γ/(λ_k−λ_j)); distribuição estacionária → d_s≈2 (UV).
3. **Ciclo termodinâmico:** poda fragmenta (d_s→0); Schrödinger restaura — o ciclo
   completo dirige d_s→3–4.
4. **Fundação Tomita–Takesaki:** estende η a estados quânticos arbitrários.

## 10. Contabilidade honesta de parâmetros (Tabela 1 do paper)
| parâmetro | status | origem |
|---|---|---|
| η | **calibrado** (dep. de sistema) | cosmológico p_c=0.2488≈e_0; lab Casini |
| λ_q (restauração) | derivado até 1 passo geométrico aberto | λ_q/γ₀=1/√π≈0.564 |
| γ₀ | input experimental | 4Gm²/ℏd |
| κ, Γ_ζ, α(GW) | livres | condutância/ruído da rede; dispersão GW |
As **duas predições mais falsificáveis** (σ_x⁻² e τ_Bell/τ_GHZ~N²) são **independentes
de todos os parâmetros livres**.

## 11. Predições falsificáveis (13–14, Tabela 1)
σ_x⁻² (MAQRO); τ_Bell/τ_GHZ~N² (NISQ); p_c·N=1+√η; F∝r⁻² exato; dispersão de GW
v_g≈1+(3/2)αk² (LISA); potencial de Newton V∝(1−e^{−r/√α})/r (sub-mm); T_U=ℏa/(2πck_B);
correções da regra de Born perto de horizontes; Λ_eff=3γ₀²/4; distribuição de avalanche
P(s)~s^{−τ} para GHZ (item 13, testável por simulação de rede).

## 12. Problemas abertos (declarados pelo autor)
- Provar que o ciclo SR completo dirige d_s:2→4 (resolver a equação integral singular de
  Dyson/Wasserstein).
- η_GHZ exato de Tomita–Takesaki para estados não-Gaussianos.
- **Setor do Modelo Padrão** (U(1), SU(N), férmions de defeitos topológicos) — aberto.
- **A SETA DO TEMPO é POSTULADA**, não derivada: "a 4ª dimensão (tempo) emerge da
  estrutura causal imposta pela **poda irreversível**" (§2.1, "3→4 step", declarado
  aberto). [É exatamente o ponto que a campanha COLAPSO_SR_TEIC isolou.]

---

## Linhagem (para situar contra TEIC)
SR é uma **síntese horizontal** de quatro tradições: (1) colapso objetivo (CSL/GRW,
Diósi–Penrose); (2) gravidade entrópica (Jacobson, Verlinde, Padmanabhan); (3) Asymptotic
Safety (Reuter) + CDT (Ambjørn–Loll); (4) Random Matrix Theory (Dyson) + Tomita–Takesaki.
Faz colapso + (condicionalmente) geometria, mas **sem setor de matéria derivado** e com a
seta do tempo postulada. Contraste com TEIC (extensão VERTICAL de Causal Set Theory:
SU(3)+confinamento+matéria de uma raiz única, eixo de tempo estrutural).
