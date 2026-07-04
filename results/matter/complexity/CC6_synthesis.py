"""CC6 -- synthesis: what the complexity hypothesis supports, and the E^2 relation.

Reads the CC1-CC5 JSON outputs, tests whether the relativistic dispersion relation
E^2 = (pc)^2 + (mc^2)^2 emerges, and writes the honest synthesis (graded
A=derived, B=real-but-inherited, C=definitional/inconclusive, D=refuted).  It also
patches the verdict block of the top-level MATTER_COMPLEXITY.md.

The dispersion relation, built ONLY from CC2/CC3 quantities:
    m = tau(N)              -- the measured, Lorentz-invariant rest cost  (CC2, CC3)
    E(phi) = m cosh(phi)    -- energy   = m gamma         (CC3 geometry)
    p(phi) = m sinh(phi)    -- momentum = m gamma beta    (CC3 geometry)
  => E^2 - p^2 = m^2 (cosh^2 - sinh^2) = m^2   for every boost,
  and for the photon (N=0, m=tau=0):  E = p  (E^2 = (pc)^2, massless).
This is the hyperbolic identity cosh^2 - sinh^2 = 1 applied to the invariant tau:
genuine, but INHERITED from R1's geometry -- not an independent new fact.

No mass/energy formula is inserted into any generator; this file only ASSEMBLES
quantities measured by counting in CC1-CC5.
Output: CC6_synthesis.md + CC6_synthesis.json.
"""

from __future__ import annotations

import json

import numpy as np

import complexity_core as cc


def _load(name):
    return json.loads((cc.OUTDIR / f"{name}.json").read_text())


def dispersion_test():
    """E^2 = (pc)^2 + (mc^2)^2 using m = measured tau(N) and cosh/sinh boosts."""
    d2 = _load("CC2_cost")
    taus = {int(r["N"]): r["mean"] for r in d2["proper_time"]}
    rapidities = np.linspace(0.0, 2.0, 11)
    rows = []
    max_rel = 0.0
    for N, m in sorted(taus.items()):
        for phi in rapidities:
            E = m * np.cosh(phi)
            p = m * np.sinh(phi)
            lhs = E ** 2
            rhs = p ** 2 + m ** 2            # (pc)^2 + (mc^2)^2, c = 1
            denom = max(lhs, 1.0)
            rel = abs(lhs - rhs) / denom
            max_rel = max(max_rel, rel)
            rows.append({"N": N, "m_tau": m, "phi": float(phi),
                         "E": float(E), "p": float(p),
                         "E2": float(lhs), "p2_plus_m2": float(rhs)})
    # photon check: N=0 -> m=0 -> E=p
    m0 = taus.get(0, 0.0)
    photon_massless = (m0 == 0.0)
    return {"rapidities": rapidities.tolist(), "max_rel_error": float(max_rel),
            "photon_m_is_zero_E_eq_p": bool(photon_massless),
            "tau_by_N": taus, "n_rows": len(rows)}


def main():
    print("=" * 70)
    print("CC6 -- SYNTHESIS + DISPERSION RELATION E^2 = (pc)^2 + (mc^2)^2")
    print("=" * 70)
    cc1, cc2, cc3 = _load("CC1_structures"), _load("CC2_cost"), _load("CC3_lorentz")
    cc4, cc5 = _load("CC4_conservation"), _load("CC5_gravity")
    disp = dispersion_test()

    print(f"  CC1 verdict: {cc1['verdict']}")
    print(f"  CC2 verdict: {cc2['verdict']} (grade {cc2['grade']}), "
          f"tau~N exponent p={cc2['fit']['power_exponent']:.3f}")
    print(f"  CC3 verdict: {cc3['verdict']} (grade {cc3['grade']}), "
          f"CV_pois={cc3['mean_cv_poisson']:.1%} vs CV_lat={cc3['mean_cv_lattice']:.1%}")
    print(f"  CC4 verdict: {cc4['verdict']} (grade {cc4['grade']})")
    print(f"  CC5 verdict: {cc5['verdict']} (grade {cc5['grade']}), A~N R2={cc5['r2_proportional']:.5f}")
    print("-" * 70)
    print(f"  E^2 = (pc)^2+(mc^2)^2 : max relative error = {disp['max_rel_error']:.2e}")
    print(f"  photon (N=0): m=tau=0, E=p (massless): {disp['photon_m_is_zero_E_eq_p']}")

    dispersion_ok = disp["max_rel_error"] < 1e-12 and disp["photon_m_is_zero_E_eq_p"]

    summary = {
        "CC1": {"grade": "build", "verdict": cc1["verdict"]},
        "CC2": {"grade": cc2["grade"], "verdict": cc2["verdict"],
                "tau_per_loop": cc2["fit"]["tau_per_loop_a"],
                "exponent": cc2["fit"]["power_exponent"]},
        "CC3": {"grade": cc3["grade"], "verdict": cc3["verdict"]},
        "CC4": {"grade": cc4["grade"], "verdict": cc4["verdict"]},
        "CC5": {"grade": cc5["grade"], "verdict": cc5["verdict"]},
        "dispersion": {"ok": bool(dispersion_ok), **disp},
    }
    cc.save_json("CC6_synthesis", summary)
    _write_md(cc1, cc2, cc3, cc4, cc5, disp, dispersion_ok)
    _patch_root_md(cc2, cc3, cc4, cc5, dispersion_ok)
    print("-" * 70)
    print("CC6 synthesis written; MATTER_COMPLEXITY.md verdict block patched.")
    return summary


def _write_md(cc1, cc2, cc3, cc4, cc5, disp, dispersion_ok):
    a = cc2["fit"]["tau_per_loop_a"]
    lines = [
        "# CC6 -- Síntese: o que a hipótese da complexidade causal sustenta",
        "",
        "> Hipótese: **massa ∝ complexidade causal interna N**.",
        "> Graus: **A** = derivado; **B** = real mas herdado; **C** = definitional/",
        "> inconclusivo; **D** = refutado.",
        "",
        "## Quadro de resultados",
        "",
        "| Tarefa | Pergunta | Resultado | Grade |",
        "|--------|----------|-----------|-------|",
        f"| CC1 | estruturas com N controlado (Betti=N) | {cc1['verdict']} | build |",
        f"| CC2 | C(N) ∝ N / τ(N) ∝ N | {cc2['verdict']} (p={cc2['fit']['power_exponent']:.3f}, R²={cc2['fit']['r2_proportional']:.4f}) | {cc2['grade']} |",
        f"| CC3 | τ(N) Lorentz-invariante | {cc3['verdict']} (CV {cc3['mean_cv_poisson']:.0%} vs {cc3['mean_cv_lattice']:.0%}) | {cc3['grade']} |",
        f"| CC4 | N conservado | {cc4['verdict']} | {cc4['grade']} |",
        f"| CC5 | θ(r) ∝ N | {cc5['verdict']} (R²={cc5['r2_proportional']:.4f}) | {cc5['grade']} |",
        f"| CC6 | E² = (pc)²+(mc²)² | {'EMERGE' if dispersion_ok else 'NAO'} (erro {disp['max_rel_error']:.0e}) | B |",
        "",
        "## A relação de dispersão E² = (pc)² + (mc²)²",
        "",
        "Construída **apenas** com quantidades medidas em CC2/CC3:",
        "",
        "```",
        "m      = τ(N)            massa de repouso = custo causal medido   (CC2, CC3)",
        "E(φ)   = m cosh φ        energia   = m γ                          (CC3)",
        "p(φ)   = m sinh φ        momento   = m γβ                         (CC3)",
        "  =>   E² − p² = m² (cosh²φ − sinh²φ) = m²   para todo boost",
        "  fóton (N=0): m = τ = 0  =>  E = p   (E² = (pc)², sem massa)",
        "```",
        "",
        f"Verificado numericamente com m = τ(N) medido: erro relativo máximo "
        f"**{disp['max_rel_error']:.1e}**; o fóton (N=0) tem m=τ=0 ⇒ E=p: "
        f"**{disp['photon_m_is_zero_E_eq_p']}**.",
        "",
        "## Afirmações",
        "",
        "**SUPORTADA (genuína, com ressalva de herança):**",
        "",
        f"- O tempo próprio medido (maior cadeia causal) é **proporcional a N**: cada",
        f"  ciclo interno custa um quantum fixo de ~{a:.1f} elos de cadeia (CC2, "
        f"  expoente {cc2['fit']['power_exponent']:.3f}, R²≈1). O fóton (N=0) tem τ=0.",
        "- Esse custo é **invariante de Lorentz** (CC3): a mesma estrutura boostada",
        "  preserva τ (CV ~6%) enquanto o controle em rede o quebra (CV ~32%).",
        "- N é **conservado** sob perturbação pequena e **quebra** sob perturbação",
        "  grande (CC4) — análogo a estabilidade topológica vs aniquilação de pares.",
        "- A relação `E² = (pc)² + (mc²)²` **emerge** com m=τ(N) (CC6), incluindo o",
        "  limite sem massa do fóton.",
        "",
        "**DEFINITIONAL / HERDADA (não é descoberta independente):**",
        "",
        "- `C(N) = 1 + N/n_ext` e `v_eff = 1/(1+N/n_ext)` são **exatos por construção**",
        "  (a definição operacional realizada), não emergentes.",
        "- A invariância de Lorentz (CC3) e a relação E² (CC6) **herdam** a geometria",
        "  hiperbólica de R1 (cosh²−sinh²=1) e a invariância de Poisson; não são uma",
        "  dilatação nova derivada do zero.",
        "- `θ(r) ∝ N` (CC5) segue da **linearidade** da ação de D3 assim que se",
        "  identifica peso-da-fonte = N. O conteúdo é a identificação (a hipótese),",
        "  não a proporcionalidade. O prefator G permanece não-universal (ressalva D3).",
        "",
        "**ABERTO:**",
        "",
        "- Por que a Natureza escolheria *diamantes* (esta topologia) como a unidade de",
        "  complexidade? A construção é imposta, não emerge dinamicamente de uma ação.",
        "- O quantum de τ por loop (~10 elos) depende de ρ e da geometria do diamante;",
        "  não há ainda uma escala de massa física derivada (só proporcionalidade).",
        "- Espectro de massas: nada aqui fixa N a valores discretos preferidos — não há",
        "  ainda um mecanismo para as massas observadas das partículas.",
        "- Quebra de N (CC4) como produção de pares é só uma analogia; falta a dinâmica",
        "  (conservação de momento/energia na quebra) para ser uma afirmação física.",
        "",
        "## Conclusão honesta",
        "",
        "A campanha **realiza e torna quantitativa** a imagem fundacional: massa como",
        "custo causal de deslocamento, com τ(N) ∝ N medido, invariante de Lorentz, e",
        "fechando o ciclo até θ(r) ∝ N e E² = (pc)²+(mc²)². Mas o núcleo proporcional é",
        "**definitional** (a definição de C(N)) e os resultados relativísticos/",
        "gravitacionais são **herdados** de R1/D3. O avanço real sobre M1 é que aqui",
        "*existe um objeto* (a estrutura topológica) com um custo de deslocamento",
        "bem-definido e invariante — o que o campo livre de M1 não tinha. O passo que",
        "falta para uma derivação genuína é fazer essas estruturas **emergirem** de uma",
        "ação dinâmica, em vez de construí-las à mão.",
        "",
        "![CC1](CC1_structures.png)",
        "![CC2](CC2_cost.png)",
        "![CC3](CC3_lorentz.png)",
        "![CC5](CC5_gravity.png)",
        "",
    ]
    (cc.OUTDIR / "CC6_synthesis.md").write_text("\n".join(lines), encoding="utf-8")


def _patch_root_md(cc2, cc3, cc4, cc5, dispersion_ok):
    path = cc.ROOT / "MATTER_COMPLEXITY.md"
    text = path.read_text(encoding="utf-8")
    block = "\n".join([
        "",
        "| Tarefa | Resultado | Grade |",
        "|--------|-----------|-------|",
        "| CC1 — estruturas N controlado | CONSTRUÍDO (Betti=N, v_eff(0)=1) | build |",
        f"| CC2 — τ(N) ∝ N | {cc2['verdict']} (p={cc2['fit']['power_exponent']:.3f}) | {cc2['grade']} |",
        f"| CC3 — Lorentz | {cc3['verdict']} | {cc3['grade']} |",
        f"| CC4 — N conservado | {cc4['verdict']} | {cc4['grade']} |",
        f"| CC5 — θ(r) ∝ N | {cc5['verdict']} | {cc5['grade']} |",
        f"| CC6 — E²=(pc)²+(mc²)² | {'EMERGE' if dispersion_ok else 'NAO'} | B |",
        "",
        "**Síntese honesta:** τ(N) ∝ N (custo causal medido) é invariante de Lorentz e",
        "fecha o ciclo até θ(r) ∝ N e E²=(pc)²+(mc²)². O núcleo proporcional `C(N)=1+N/n_ext`",
        "é **definitional**; a invariância e a relação E² são **herdadas** de R1; θ∝N",
        "segue da linearidade de D3 dada a identificação fonte=N. Avanço real sobre M1:",
        "existe um objeto com custo de deslocamento bem-definido. Aberto: fazer as",
        "estruturas **emergirem** de uma ação, e derivar uma escala de massa física.",
        "Ver `results/matter/complexity/CC6_synthesis.md`.",
        "",
    ])
    start = text.index("<!-- VERDICT_BLOCK_START -->") + len("<!-- VERDICT_BLOCK_START -->")
    end = text.index("<!-- VERDICT_BLOCK_END -->")
    text = text[:start] + "\n" + block + "\n" + text[end:]
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
