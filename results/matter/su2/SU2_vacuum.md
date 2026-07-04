# SU2 — O vácuo SU(2): monopolos e lei de área de Wilson

## Veredito: **SIM — confinamento (lei de área), monopolos em todo acoplamento**

```
β     <½TrU_p>   ρ_M     W(1×1)   W(2×2)   χ(2,2)
0.5    0.107    0.446    0.101    0.006    −2.33   (laços saturam ~0: χ mal-definido)
1.0    0.221    0.391    0.223    0.008    +0.45
1.5    0.331    0.316    0.332    0.017    +0.85
2.0    0.428    0.234    0.428    0.036    +0.78
2.5    0.524    0.158    0.524    0.091    +0.50
3.0    0.600    0.094    0.598    0.153    +0.39
```

Amostrado por Metropolis xadrez vetorizado sobre links-quaternion numa rede periódica
8³, ação de Wilson `S=β Σ(1−½Tr U_p)`.

## O que o vácuo SU(2) mostra

1. **Plaqueta média.** `⟨½Tr U_p⟩ → β/4` no acoplamento forte (β=0.5: 0.107≈0.125) e
   `→1` no fraco — a curva padrão de Yang-Mills SU(2). `W(1×1)=⟨½Tr U_p⟩` confere.

2. **Monopolos em todo β.** Densidade de monopolo (projeção Abeliana de 't Hooft) `ρ_M`
   de 0.45 (forte) a 0.09 (fraco): o defeito magnético existe em todo acoplamento,
   como em CR_3D mas agora dentro de um grupo não-Abeliano.

3. **Lei de área = confinamento.** A razão de Creutz `χ(2,2)>0` em toda a janela
   resolvida `β∈[1, 2.5]` (0.39–0.85): os laços de Wilson decaem com a ÁREA, `W∝e^{−σA}`,
   com tensão de corda `σ>0`. **Isto é confinamento** — e ao contrário de U(1) 3D, SU(2)
   confina em todo o volume (sem transição de desconfinamento no bulk).

## Nota honesta

- Em `β=0.5` (acoplamento muito forte) os laços 2×2/3×3 **subfluem para ~0** (ruído
  estatístico): a razão de Creutz fica mal-definida (−2.3) ali. É exatamente onde a
  lei de área é mais forte, mas os laços pequenos saturam — por isso a janela
  confiável é `β∈[1, 2.5]`.
- `χ(2,2)` tem um pico em `β≈1.5` e cai para `β` grande (rumo ao contínuo, σ→0 em
  unidades de rede) e satura no forte (laços ~0). O crescimento monotônico de σ rumo ao
  acoplamento forte não é visível em `χ(2,2)` por essa saturação — uma limitação da
  rede 8³, não da física.

A diferença decisiva com a fronteira U(1): em CR_3D a janela confinante estava
**invertida** (forte) e o objeto era um vórtice (linha). Aqui SU(2) confina
genuinamente, e (SU3) o objeto suportado é um sóliton **pontual** estável.

## Anti-circularidade

Links = quaternions unitários, produto de Hamilton (sem Pauli, sem complexo); laço de
Wilson = componente `a₀`. "Quark"/"cor"/"QCD" só em notas COMPARISON ONLY.
`results/matter/su2/SU2_vacuum.{json,png}` + `SU2_vacuum.py`.
