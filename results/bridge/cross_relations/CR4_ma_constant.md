# CR4 — a constante pura de m_A: a herança PE3 morre; o número puro que sobrevive é escala-invariante

> Tarefa CR4 de `CROSS_RELATIONS_II.md`. Kill criteria pré-registrados na
> docstring de `CR4_ma_constant.py` ANTES de rodar; nenhum critério alterado
> após ver dados. Mesmas sprinklings do CR3 (condição "mesma rede" literal).
> Dados: `CR4_ma_constant_data.json`; figura `CR4_ma_constant.png`.

## Veredito: **B — a herança PE3 (m²∝√ρ) MORRE no substrato causal (9.5σ); a entrada da tabela fecha com expoente ~0: m²_iso·λ_p é um número puro escala-invariante (CV 5.3%)**

| Critério (pré-registrado) | Limite | Medido | Resultado |
|---|---|---|---|
| herança PE3: s_m = +0.5 | \|s_m−0.5\| ≤ 3σ | s_m = **0.068 ± 0.045** (9.5σ) | **MORTE da entrada herdada** |
| tabela fecha: CV do número puro (s medido) | < 20% | **5.3%** | ✅ fecha |
| regulador de caixa: \|razão−1\| | ≤ 0.20 | 1.087 (E=2.56 vs 3.2) | ✅ não é IR-regulado |

## Os números

| ρ | links bulk | plaq bulk | m²_iso·λ_p (média±sem) | Π_E/Π_B |
|---|---|---|---|---|
| 16 | ~14 500 | ~292 | 518.7 ± 41 | 4.11 ± 0.12 |
| 27 | ~33 000 | ~608 | 479.5 ± 19 | 3.86 ± 0.07 |
| 45 | ~73 000 | ~1168 | 509.7 ± 23 | 3.58 ± 0.05 |
| 75 | ~159 000 | ~2045 | 561.8 ± 18 | 3.47 ± 0.02 |

```
expoente:        m²_iso·λ_p ∝ ρ^(0.068 ± 0.045)   — consistente com ZERO (1.5σ)
número puro:     P_iso = m²_iso·λ_p·ρ^(−s_med) = 406 ± 22  (CV 5.3% na varredura)
                 com s=0 cru: m²_iso·λ_p ≈ 517 ± 34         (CV 6.5%)
por canal:       P_E ≈ 244 (CV 5.6%)   P_B ≈ 915 (CV 7.7%)
caixa:           m²_iso(E=2.56)/m²_iso(E=3.2) = 1.087 — fraca, dentro do limite
λ_p declarado:   1  (peso livre, = K da DEV — W4); fatores O(1) de convenção
                 declarados na docstring
```

## Leitura honesta

1. **A morte (reportada como morte).** A tradução dimensional ingênua de PE3
   (proxy de rede 3D, m_A∝√ρ → s_m=+1/2 em unidades causais ρ^{1/4}) **não
   sobrevive** no substrato causal: 9.5σ. O motivo provável é o conhecido da
   campanha C1: os links de cobertura são dominados pelo **sliver não-local**
   (escala de caixa), não pela escala de granularidade ρ^{-1/4} — a premissa
   de "uma única escala UV" falha para momentos de link crus. A tabela CR2
   será corrigida: a entrada "m_A∝√ρ" vira "expoente causal medido s_m≈0".
2. **O que sobrevive é mais forte que o esperado.** O quociente
   m²_iso·λ_p = 4(C2_t+3C2_x)/(Π_E+Π_B) é **invariante de escala**: constante
   sobre ρ variando 4.7× (CV 5.3%) E quase invariante de caixa (+8.7% sob
   E 3.2→2.56, com sliver dominante — não trivial). Massa de Stückelberg e
   rigidez de plaqueta escalam JUNTAS; a razão é um número puro do substrato
   (~520, condicionado a λ_p=1 e convenções declaradas) — análogo estrutural
   das razões (1,2) de C2: **calculável, não ajustável**.
3. **Split E/B**: 4.11 → 3.47, decrescendo com ρ em direção ao valor W2
   (2.97) — o artefato de regulador já resolvido em LIV_VECTOR; reportado por
   canal, não escondido. O número puro isotrópico é o registrado; P_E e P_B
   ficam na tabela como canais do artefato.
4. **Honestidade dimensional**: m_A em unidades físicas segue não derivado
   (inalterado); o derivado é a **relação** massa↔rigidez na mesma rede.

## Reproduzir

```
python results/bridge/cross_relations/CR4_ma_constant.py
```
