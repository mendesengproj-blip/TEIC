"""AH7 -- honest synthesis and verdict for CR_ABELIAN_HIGGS.

Reads AH1-AH6 JSON, assembles the verdict (A-D), and writes the MANDATORY honesty
declaration: the complex scalar with minimal coupling is a FOURTH ingredient added by
hand -- the result is 'the extended theory is consistent and supports stable matter',
NOT 'the minimal action derives matter'.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import crahiggs_core as a   # noqa: E402


def _load(name):
    p = a.OUTDIR / f"{name}.json"
    return json.loads(p.read_text()) if p.exists() else None


def main():
    AH1 = _load("AH1_setup"); AH2 = _load("AH2_mass"); AH3 = _load("AH3_vortex")
    AH4 = _load("AH4_pinning"); AH5 = _load("AH5_collision"); AH6 = _load("AH6_annihilation")

    ah1 = bool(AH1 and AH1["AH1_PASS"])
    ah2 = bool(AH2 and AH2["AH2_PASS"])
    e_slope = AH2["slope_e"] if AH2 else float("nan")
    core0 = bool(AH3 and AH3["has_normal_core"])
    kappa = AH3["kappa"] if AH3 else float("nan")
    regime = AH3["regime"] if AH3 else "n/a"
    ah4 = bool(AH4 and AH4["AH4_PASS"])
    n5 = AH5["n_consistencies"] if AH5 else 4
    ah5_pin = bool(AH5 and AH5["core_pinned_in_collision"])
    ah6 = bool(AH6 and AH6["AH6_PASS"])
    ratio = AH6["E_pair_over_M"] if AH6 else float("nan")

    if ah1 and ah2 and core0 and ah4 and n5 == 5 and ah5_pin:
        verdict, vtext = "A", ("cinco consistências + criação estável + aniquilação — "
                               "matéria estável com o campo complexo")
    elif ah4 and not ah5_pin:
        verdict, vtext = "B", "pinamento estático (AH4) mas criação turbulenta (AH5)"
    elif ah2 and not ah4:
        verdict, vtext = "C", "m_A correto (AH2) mas sem pinamento"
    elif not ah1:
        verdict, vtext = "D", "condensado complexo não converge"
    else:
        verdict, vtext = "B", "resultado parcial"

    payload = {
        "AH1_setup_pass": ah1, "AH2_m_A_linear": ah2, "AH2_slope_e": e_slope,
        "AH3_normal_core": core0, "AH3_kappa": kappa, "AH3_regime": regime,
        "AH4_pinning": ah4, "AH5_n_consistencies": n5, "AH5_core_pinned": ah5_pin,
        "AH6_annihilation": ah6, "AH6_E_pair_over_M": ratio,
        "verdict": verdict, "verdict_text": vtext,
    }
    a.save_json("AH7_synthesis", payload)
    _write_md(payload)

    print("=" * 70)
    print("AH7 -- CR_ABELIAN_HIGGS SYNTHESIS")
    print("=" * 70)
    print(f"  AH1 setup (5-check gate) ........... {ah1}")
    print(f"  AH2 m_A = e*v (slope e~{e_slope:.2f}) .... {ah2}")
    print(f"  AH3 |Phi|(0)->0 core; kappa={kappa:.2f} .. core={core0} ({regime})")
    print(f"  AH4 vortex pinned (winding stable) . {ah4}")
    print(f"  AH5 collision: {n5}/5; pinned ....... {ah5_pin}")
    print(f"  AH6 annihilation E_pair~2M ......... {ah6} (ratio {ratio:.2f})")
    print("-" * 70)
    print(f"VERDICT CR_ABELIAN_HIGGS: {verdict} -- "
          f"{vtext.encode('ascii','replace').decode('ascii')}")
    return payload


def _write_md(p):
    def yn(b):
        return "SIM" if b else "NÃO"
    kap = p["AH3_kappa"]
    L = [
        "# AH7 — Síntese honesta CR_ABELIAN_HIGGS",
        "",
        "## Quadro de resultados",
        "",
        "```",
        f"AH1 — Campo complexo implementado, portão:   [{'PASS' if p['AH1_setup_pass'] else 'FAIL'}]",
        f"AH2 — m_A = e·v (linear em v):               [{yn(p['AH2_m_A_linear'])}]  "
        f"(inclinação e≈{p['AH2_slope_e']:.2f}; contraste com CR_HIGGS: m_A const)",
        f"AH3 — |Φ|(0)=0, κ vs 1/√2:                  [{yn(p['AH3_normal_core'])} "
        f"κ={('%.2f' % kap) if np.isfinite(kap) else '—'}]  ({p['AH3_regime']})",
        f"AH4 — Pinamento (enrolamento estável):       [{yn(p['AH4_pinning'])}]",
        f"AH5 — Cinco consistências em colisão:        [{p['AH5_n_consistencies']}/5]",
        f"AH6 — Aniquilação E_par≈2·M:                [{yn(p['AH6_annihilation'])} "
        f"(razão {p['AH6_E_pair_over_M']:.2f})]",
        "```",
        "",
        f"## VEREDITO: **{p['verdict']}** — {p['verdict_text']}",
        "",
        "```",
        f"[{'X' if p['verdict']=='A' else ' '}] A — Cinco consistências + criação estável + aniquilação",
        f"[{'X' if p['verdict']=='B' else ' '}] B — Pinamento estático (AH4) mas criação turbulenta (AH5)",
        f"[{'X' if p['verdict']=='C' else ' '}] C — m_A correto (AH2) mas sem pinamento",
        f"[{'X' if p['verdict']=='D' else ' '}] D — Sem convergência do condensado complexo",
        "```",
        "",
        "## DECLARAÇÃO HONESTA OBRIGATÓRIA (independente do veredito)",
        "",
        "> O campo escalar complexo Φ com acoplamento minimal |D_μΦ|² é um **quarto",
        "> ingrediente adicionado à ação**. Não emerge da ação mínima",
        "> S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]. O resultado reportado é: **\"a teoria",
        "> estendida com este ingrediente é consistente e suporta matéria estável\"**. Não:",
        "> \"a ação mínima deriva matéria\".",
        "",
        "## O que foi derivado vs. o que foi adicionado",
        "",
        "```",
        "DERIVADO da ação mínima (uma linha):",
        "  Geometria, SR, Schwarzschild          [R1-R3]",
        "  Gravitação newtoniana                 [D1-D3]",
        "  Estrutura da DEV (gravidade modif.)   [ponte]",
        "  Plasma de monopólos no vácuo          [T3D2]",
        "  Tensão de corda E(d)∝d               [T3D3]",
        "",
        "ADICIONADO À MÃO (hipóteses extras):",
        "  V(θ): potencial de fase              [CR_HIGGS]  (não pina — θ é fase)",
        "  |D_μΦ|² + V(|Φ|): campo complexo     [CR_ABELIAN_HIGGS]  (quarto ingrediente)",
        "",
        "COM O CAMPO COMPLEXO (esta campanha):",
        f"  Condensado ⟨|Φ|⟩ = v                  [AH1]  {yn(p['AH1_setup_pass'])}",
        f"  m_A = e·v (não constante)            [AH2]  {yn(p['AH2_m_A_linear'])}",
        f"  Núcleo normal |Φ|→0, κ Type II       [AH3]  {yn(p['AH3_normal_core'])}",
        f"  Vórtice pinado (enrolamento estável) [AH4]  {yn(p['AH4_pinning'])}",
        f"  Matéria criada por colisão           [AH5]  {p['AH5_n_consistencies']}/5",
        f"  Aniquilação com E conservada         [AH6]  {yn(p['AH6_annihilation'])}",
        "```",
        "",
        "## A diferença física vs CR_HIGGS (fase real)",
        "",
        "| | CR_HIGGS (fase θ) | CR_ABELIAN_HIGGS (Φ complexo) |",
        "|--|-------------------|------------------------------|",
        "| acoplamento | cos(φ+Δθ): θ entra por ∇θ | \\|D_μΦ\\|²: \\|Φ\\| acopla ao gauge |",
        "| m_A | ≈0.99 **constante** | **= e·v** (linear, →0 em v=0) |",
        "| núcleo do vórtice | θ≈v (sem núcleo) | **\\|Φ\\|→0** (núcleo normal) |",
        "| pinamento | **não** (enrolamento desfaz) | **sim** (enrolamento estável) |",
        "| veredito | C | " + p["verdict"] + " |",
        "",
        ("**Conclusão.** O ingrediente que CR_HIGGS localizou — um escalar complexo cuja "
         "magnitude acopla ao fluxo de gauge — **fecha as cinco consistências** quando "
         "adicionado. A campanha de matéria está encerrada: o que é derivado da ação "
         "mínima (geometria, gravitação, vácuo topológico) é sólido; matéria estável "
         "exige o campo complexo como ingrediente extra, reportado com honestidade."
         if p["verdict"] == "A" else
         "**Conclusão.** Ver veredito acima; a fronteira está localizada e documentada."),
        "",
    ]
    (a.OUTDIR / "AH7_synthesis.md").write_text("\n".join(L), encoding="utf-8")


if __name__ == "__main__":
    main()
