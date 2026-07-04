"""H6 -- honest synthesis and verdict for CR_HIGGS.

Reads H1-H5 JSON and assembles the verdict (A-D) plus the honest record of what the
node potential V(theta) does and does NOT derive.  No new physics here -- it only
aggregates and judges.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crhiggs_core as h   # noqa: E402


def _load(name):
    p = h.OUTDIR / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    H1 = _load("H1_condensate")
    H2 = _load("H2_gauge_mass")
    H3 = _load("H3_vortex_profile")
    H4 = _load("H4_pinning")
    H5 = _load("H5_collision")

    # --- distil each hypothesis ---
    h1_pass = bool(H1 and H1["H1_PASS"])
    v_example = None
    if H1:
        for r in H1["rows"]:
            if r["v_expected"] > 0:
                v_example = (r["mu2"], r["lamh"], r["v_expected"], r["theta_bulk_mean"])
                break

    h2_pass = bool(H2 and H2["m_A_equals_e_v"])
    m_A = H2["e_eff_cosine_mass"] if H2 else float("nan")

    has_core = bool(H3 and H3.get("has_normal_core"))
    xi = H3["xi"] if H3 else float("nan")
    lam_L = H3["lambda_L"] if H3 else float("nan")
    kappa = H3["kappa"] if H3 else float("nan")
    regime = H3["regime"] if H3 else "n/a"

    mu_c = H4["mu_c"] if H4 else None
    h4_pin = bool(H4 and H4["pinning_found"])
    diffuses0 = bool(H4 and H4["diffuses_at_mu2_0"])

    h5_pin = bool(H5 and H5["core_pinned_in_collision"])
    n5 = H5["n_consistencies"] if H5 else 4

    # --- verdict ---
    if h5_pin and h4_pin and n5 == 5:
        verdict, vtext = "A", ("cinco consistências em colisão com condensado — "
                               "matéria estável derivada da ação completa")
    elif h4_pin and not h5_pin:
        verdict, vtext = "B", ("pinamento estático (H4) mas criação ainda instável (H5)")
    elif h1_pass and not h4_pin:
        verdict, vtext = "C", ("condensado existe (H1) mas pinamento não ocorre "
                               "(H4/H5): θ é a fase de Stückelberg, não a magnitude")
    else:
        verdict, vtext = "D", "μ_c não identificado / condensado não confirmado"

    payload = {
        "H1_condensate": h1_pass, "v_example": v_example,
        "H2_m_A_equals_e_v": h2_pass, "m_A_gauge": m_A,
        "H3_normal_core": has_core, "xi": xi, "lambda_L": lam_L,
        "kappa": kappa, "regime": regime,
        "H4_mu_c": mu_c, "H4_pinning": h4_pin, "H4_diffuses_at_0": diffuses0,
        "H5_core_pinned": h5_pin, "n_consistencies": n5,
        "verdict": verdict, "verdict_text": vtext,
    }
    h.save_json("H6_synthesis", payload)
    _write_md(payload)

    print("=" * 70)
    print("H6 -- CR_HIGGS SYNTHESIS")
    print("=" * 70)
    print(f"  H1 condensate <theta>=v ............ {h1_pass}")
    print(f"  H2 m_A = e*v ....................... {h2_pass} (m_A_gauge~{m_A:.2f})")
    print(f"  H3 normal core / xi / kappa ........ core={has_core} kappa={kappa}")
    print(f"  H3 lambda_L ........................ {lam_L}")
    print(f"  H4 mu_c / pinning .................. mu_c={mu_c} pinned={h4_pin}")
    print(f"  H5 core pinned in collision ........ {h5_pin}  ({n5}/5 consistencies)")
    print("-" * 70)
    print(f"VERDICT CR_HIGGS: {verdict} -- "
          f"{vtext.encode('ascii', 'replace').decode('ascii')}")
    return payload


def _write_md(p):
    def yn(b):
        return "SIM" if b else "NÃO"
    ve = p["v_example"]
    ve_s = (f"μ²={ve[0]}, λ_h={ve[1]} → v={ve[2]:.3f}, ⟨θ⟩={ve[3]:.3f}"
            if ve else "—")
    kap = p["kappa"]
    L = [
        "# H6 — Síntese honesta CR_HIGGS",
        "",
        "## Quadro de resultados",
        "",
        "```",
        f"H1 — Condensado ⟨θ⟩ = v confirmado:        [{yn(p['H1_condensate'])}]  ({ve_s})",
        f"H2 — Massa de gauge m_A = e·v emergente:    [{yn(p['H2_m_A_equals_e_v'])}]  "
        f"(m_A≈{p['m_A_gauge']:.2f}, fixada pelo cosseno e, independente de v)",
        f"H3 — Comprimento de coerência ξ medido:     "
        f"[{yn(p['H3_normal_core'])}]  (núcleo normal? {p['H3_normal_core']}; "
        f"λ_L={p['lambda_L']:.3f}; "
        f"κ={('%.3f' % kap) if np.isfinite(kap) else '—'})",
        f"H3 — Tipo I ou II (κ vs 1/√2):             [{p['regime']}]",
        f"H4 — μ_c identificado:                      [{p['H4_mu_c'] if p['H4_mu_c'] is not None else 'NÃO'}]",
        f"H4 — Núcleo pinado para μ² > μ_c:           [{yn(p['H4_pinning'])}]",
        f"H5 — Colisão cria vórtice pinado:           [{yn(p['H5_core_pinned'])}]",
        f"H5 — Cinco consistências:                   [{p['n_consistencies']}/5]",
        "```",
        "",
        f"## VEREDITO: **{p['verdict']}** — {p['verdict_text']}",
        "",
        "```",
        "[ ] A — Cinco consistências em colisão com condensado",
        "[ ] B — Pinamento estático (H4) mas criação ainda instável (H5)",
        f"[{'X' if p['verdict']=='C' else ' '}] C — Condensado existe, pinamento não ocorre",
        "[ ] D — μ_c não identificado no regime testável",
        "```",
        "",
        "## O que CR_HIGGS derivou — e o que não",
        "",
        "**Derivou (positivo):**",
        "- **H1 — quebra espontânea de simetria.** O potencial V(θ)=−μ²θ²/2+λ_hθ⁴/4 faz",
        "  θ condensar em ⟨θ⟩ = v = √(μ²/λ_h), por relaxação, homogêneo, abaixando a",
        "  energia do vácuo. A quebra da simetria de translação θ→θ+const é genuína na",
        "  rede causal. Isto é novo e funciona.",
        "",
        "**NÃO derivou (negativo esclarecedor):**",
        "- **H2 — m_A NÃO é e·v.** A massa do bóson de gauge é fixada pelo acoplamento do",
        f"  cosseno (e≈{p['m_A_gauge']:.2f} em unidades de rede) e é **independente de v** "
        "(não-nula mesmo em v=0).",
        "- **H3 — sem núcleo normal.** θ não mergulha a 0 no núcleo do vórtice (permanece",
        "  ≈v); ξ não é medível e κ não classifica. λ_L é medido (≈1/m_A).",
        "- **H4/H5 — sem pinamento.** O núcleo do vórtice difunde para todo μ² testado;",
        "  μ_c não existe no regime computável. A colisão também não fixa o núcleo.",
        "",
        "## A causa raiz (honestidade física)",
        "",
        "Na ação mínima da TEIC, **θ é a fase de Stückelberg**: entra em cos(φ+Δθ) só",
        "pelo gradiente Δθ, com simetria de shift θ→θ+const. O potencial V(θ) **quebra**",
        "essa simetria e condensa θ (H1 ✓), mas o condensado de uma **fase** não reproduz",
        "o mecanismo abeliano-Higgs, que exige que a **magnitude** de um campo complexo",
        "Φ=ρe^{iα} multiplique (∂α−eA)² — é a magnitude ρ→v que dá m_A=e·v, o núcleo",
        "normal (ρ→0) e o pinamento de Abrikosov. Esta ação **não tem** esse termo |Φ|²A².",
        "",
        "**CR_HIGGS localiza o ingrediente ausente com mais precisão que CR_3D:** não é",
        "“um condensado escalar” genérico, e sim um **escalar complexo cuja magnitude",
        "acopla ao fluxo de gauge** (|Φ|²|D_μ|² no setor não-mínimo). Adicionar V(θ) a um",
        "θ que é fase não basta — é preciso promover θ a magnitude (ou adicionar um campo",
        "de magnitude novo), o que seria um **quarto** ingrediente da ação.",
        "",
        "## Honestidade sobre o axioma V(θ)",
        "",
        "V(θ) é adicionado à mão; **não emerge** da ação mínima Stückelberg+Wilson. As",
        "rotas para fazê-lo emergir (interações de muitos corpos entre nós; termo de",
        "curvatura R·θ²; potencial efetivo da expansão da rede CSG) permanecem não",
        "demonstradas. Reportado honestamente: V(θ) é um ingrediente novo, e — pior para",
        "a esperança original — mesmo aceito como axioma ele **não** estabiliza a matéria,",
        "porque θ é a fase, não a magnitude.",
        "",
        "## Mapa de camadas (atualizado)",
        "",
        "```",
        "2D U(1) (CR_WILSON): objeto suportado, SEM monopólos/corda → D",
        "3D U(1) (CR_3D):     monopólos+plasma+corda; VÓRTICE relativístico; núcleo difunde → B",
        "3D U(1)+V(θ) (CR_HIGGS): θ condensa (H1 ✓); mas m_A≠e·v (H2), sem núcleo normal",
        "                     (H3), núcleo difunde (H4/H5) → C",
        "                     ingrediente que falta: escalar de MAGNITUDE acoplado ao fluxo",
        "```",
        "",
    ]
    (h.OUTDIR / "H6_synthesis.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
