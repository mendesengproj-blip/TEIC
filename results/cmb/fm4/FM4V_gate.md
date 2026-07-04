# FM4-V — Gate: dispersão do modo massivo ω²=c²k²+m²

> Parte de `FM4_run.py` → `FM4_run.json`. PASS.

E2 mediu o mágnon **sem massa** (ω=ck, m²<0). FM4 dá uma **massa** ao modo de
orientação → a dispersão ganha um **gap**:

$$\omega(k)=\sqrt{c^2k^2+m^2}\quad\Rightarrow\quad \omega(0)=m\ \ (\text{gap}),\qquad
\omega(k\gg m)\to ck\ \ (\text{limite de E2}).$$

| Verificação | Critério | Status |
|---|---|---|
| Gap em k=0 | ω(0)=m | ✅ |
| Limite massless | ω(k grande)=ck (E2) | ✅ |

O símbolo BD de E2, λ(k,ω)~−(k²−ω²), com um termo de massa vira −(k²−ω²)−m², cujo
zero é a dispersão massiva acima. O setor massivo da TEIC+DEV está bem-definido →
FM4-1/2/3 prosseguem.
