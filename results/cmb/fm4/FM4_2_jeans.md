# FM4-2 — Escala de de Broglie/Jeans vs massa

> `FM4_run.py` → `FM4_run.json`. Escala de meia-supressão (half-mode) da transfer
> function fuzzy (Hu–Barkana–Gruzinov).

## A escala de Jeans cai na banda de σ8 perto do piso do m_A

```
m_A (eV)        k_half (1/Mpc)     λ supressão (Mpc)
1.0e-22         4.600              1.4   (galáxia; fuzzy clássico)
1.0e-23         1.653              3.8
1.0e-24         0.594              10.6
3.7e-25 (piso)  0.382              16.5   ← banda de σ8 (k~0.15–0.3/Mpc)
1.0e-25         0.214              29.4
```

- A escala de σ8 é k ~ 0.1–0.2 h/Mpc ≈ 0.15–0.3 /Mpc.
- **Para m_A perto do piso do Paper II (3.7×10⁻²⁵–10⁻²⁴ eV), k_half cai na banda de
  σ8** — exatamente onde S8 pediria um freio. À primeira vista, **encorajador**: a
  escala está certa, diferente do m_A de Yukawa (17 pc) que matou FM2.

Mas "a escala certa" só ajuda se a supressão **na escala de σ8** for forte o
suficiente **sem** estragar escalas menores (Lyman-α). FM4-3 mede o primeiro; FM4-4,
o segundo — e é aí que a coisa desmorona.
