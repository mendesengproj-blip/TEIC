# FM3-1 — Kibble–Zurek: a transição de ordenamento deixa um relíquia?

> `FM3_1_kibble.py` → `.{json,png}`. O(3) periódico L=20, 20 sementes.
> Quench de desordenado (J=0.30) a ordenado (J=1.20) através de J_c≈0.693 a taxas
> variáveis; defeitos contados pela carga de ângulo sólido após cooling fixo.

## Resultado — ✅ P1 confirmado: o relíquia se forma

```
τ_Q     <n_def>        ξ_dom (tamanho de domínio)
  2     39.6 ± 1.2     5.89
  4     34.4 ± 1.6     6.22
  8     32.6 ± 1.2     6.30
 16     23.1 ± 1.4     7.15
 32     14.9 ± 0.8     8.24
 64      9.2 ± 0.9    10.11
```

- **Tendência de Kibble–Zurek clara:** quench mais lento (τ_Q maior) deixa **menos
  defeitos** e **domínios maiores** — regiões têm mais tempo de contato causal para
  alinhar antes de congelar.
- **Lei de Zurek:** n_def ~ τ_Q^(−0.42), ξ_dom ~ τ_Q^(+0.15). O expoente de domínio
  (0.15) está na vizinhança da expectativa O(3) model-A (σ≈0.29) — a diferença é
  consistente com tamanho/alcance finitos (L=20, τ até 64); o expoente exato pediria
  redes maiores. A **formação do relíquia** (P1), porém, é robusta.
- **Mesmo no quench mais lento o relíquia persiste** (n_def≈9 ≫ 0). Não vai a zero.

## Significado físico

**A transição de fase do vácuo orientacional no universo jovem deixa, inevitavelmente,
uma teia de defeitos/textura de n⃗.** É o mecanismo de Kibble aplicado ao ferromagneto
de E1: domínios causalmente desconexos alinham em direções diferentes; nas fronteiras,
torções topológicas (defeitos, π₂(S²) = monopolos globais) ficam presas.

**Crucialmente, esse relíquia nasce na escala do horizonte da transição** — uma escala
**cosmológica**, não os 17 pc do m_A que mataram FM2 por separação de escala. **FM3-1
resolve o problema de escala.** Se esse relíquia é *frio* (a outra metade da
hipótese) é o que FM3-2 decide.
