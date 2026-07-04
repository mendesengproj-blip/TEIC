# V4_1 — Fidelidade: o evolutor acoplado (f=0) reproduz CR_3D

Antes de testar a back-reaction de duas vias (V4_2), confirmamos que o evolutor de
gauge ponderado por ρ é **fiel**: em f=0 (ρ=1 uniforme) ele reproduz o resultado de
CR_3D/T3D5 — o enrolamento de um vórtice de gauge nu **difunde** sob a ação mínima
(o fluxo 2π do núcleo é invisível ao cosseno de Wilson, nada o pina).

- core_flux: 1.01 → **0.18 ± 0.00** em 16 ticks (6 sementes) — o núcleo afiado se espalha.
- enrolamento topológico no disco do núcleo: 1 → **0.00** — o vórtice deixa o núcleo (difusão).

**Difunde:** True.  **Fiel a CR_3D:** True.

Isto é a instabilidade basal de CR_3D (Veredito B daquele campanha). V4_2 mede se a
depleção espontânea de ρ (de PE4_V3), agora **realimentada** no gauge, altera este
destino.
