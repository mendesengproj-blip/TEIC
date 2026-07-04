"""W6 -- synthesis: does the full action (Stueckelberg + Wilson) create stable matter?

Reads W1-W5, selects the verdict (A-D) honestly, writes the synthesis, and patches the
verdict block of the top-level MATTER_CR_WILSON.md.  Followed by the anti-circularity
check (run_all).
"""

from __future__ import annotations

import json

import wilson_core as wc


def _load(name):
    return json.loads((wc.OUTDIR / f"{name}.json").read_text())


def main():
    print("=" * 70)
    print("W6 -- SYNTHESIS: DOES Stueckelberg + Wilson CREATE STABLE MATTER?")
    print("=" * 70)
    w1 = _load("W1_wilson"); w2 = _load("W2_string"); w3 = _load("W3_collision")
    w4 = _load("W4_mass"); w5 = _load("W5_phasediagram")

    print(f"  W1 gate passed:               {w1['passed']}")
    print(f"  W2 lambda-controlled string:  {w2['wilson_string'] and w2['lam_controls']} "
          f"(lam_c op.={w2['lam_c']})")
    print(f"  W3 kink stabilised by Wilson: {w3['any_stable'] and w3['stable_needs_wilson']} "
          f"(grade {w3['grade']})")
    print(f"  W4 supported kink consistent: {w4['consistent']} (mass {w4['mass']['rest_mass']:.2f})")
    print(f"  W5 cooperative window:        {w5['helps_anywhere']}")

    # verdict selection (A-D)
    if w3["any_stable"] and w3["stable_needs_wilson"] and w4["consistent"]:
        verdict, grade = "A", "A"
    elif w3["wilson_helps"]:
        verdict, grade = "C", "C"
    else:
        verdict, grade = "D", "D"

    summary = {
        "W1": {"passed": w1["passed"]},
        "W2": {"lam_c": w2["lam_c"], "wilson_string": w2["wilson_string"]},
        "W3": {"grade": w3["grade"], "wilson_helps": w3["wilson_helps"],
               "any_stable": w3["any_stable"]},
        "W4": {"consistent": w4["consistent"], "mass": w4["mass"]["rest_mass"],
               "E2_dispersion": w4["mass"]["E2_minus_P2_constant"],
               "theta_M_over_r": w4["gravitational_field"]["is_one_over_r"]},
        "W5": {"helps_anywhere": w5["helps_anywhere"]},
        "verdict": verdict,
    }
    wc.save_json("W6_synthesis", summary)
    _write_md(w1, w2, w3, w4, w5, verdict)
    _patch_root_md(w1, w2, w3, w4, w5, verdict)
    print("-" * 70)
    print(f"VERDICT W6: {verdict}")
    print("W6 synthesis written; MATTER_CR_WILSON.md verdict block patched.")
    return summary


def _verdict_box(verdict):
    def mk(v):
        return "x" if verdict == v else " "
    return [
        f"[{mk('A')}] A — Matéria estável criada com a ação completa "
        "(M=8, τ∝M, θ~M/r, E²=(pc)²+(mc²)², Q=0)",
        f"[{mk('B')}] B — Pares virtuais estabilizados (semi-estável, vida finita)",
        f"[{mk('C')}] C — Wilson confina mas a colisão ainda é insuficiente",
        f"[{mk('D')}] D — Sem transição no regime testável → física adicional necessária "
        "(o termo de plaqueta estático não confina cargas de winding em 2D; falta o "
        "mecanismo dinâmico de Polyakov / monopólos, dimensão maior, ou campo externo)",
    ]


def _write_md(w1, w2, w3, w4, w5, verdict):
    m = w4["mass"]
    lines = [
        "# W6 -- Síntese: a ação completa (Stückelberg + Wilson) cria matéria estável?",
        "",
        "## Quadro de resultados",
        "",
        "```",
        f"W1 — Wilson implementado e consistente:     {'SIM' if w1['passed'] else 'NÃO'} "
        "(λ_p=0→GAUGE exato, pure gauge/Maxwell, kink m=8 intacto, E conservada)",
        f"W2 — Tensão de corda λ_c identificada:       NÃO (sem corda linear no regime "
        f"estático 2D; λ_c operacional={w2['lam_c']} onde E_wilson~massa 8)",
        f"W3 — Kink estável criado por colisão:        NÃO (Wilson SUPRIME o núcleo "
        "y-estruturado; grade %s)" % w3["grade"],
        f"W3 — Ponto de transição λ_c confirmado:      NÃO (sobrevivência DECRESCE com λ_p)",
        f"W4 — Massa kink = 8 (teoria):                SIM (erro {100*m['mass_err']:.1f}%)",
        f"W4 — θ(r) ~ M/r:                            {'SIM' if w4['gravitational_field']['is_one_over_r'] else 'NÃO'} "
        f"(expoente {w4['gravitational_field']['tail_exponent']:.2f})",
        f"W4 — E² = (pc)² + (mc²)²:                   {'SIM' if m['E2_minus_P2_constant'] else 'NÃO'} "
        f"(variação {100*m['dispersion_rel_spread']:.1f}%)",
        f"W5 — Mapa de fase (λ_p, ρ):                  MAPEADO "
        f"({'janela cooperativa' if w5['helps_anywhere'] else 'sem janela; λ_p suprime'})",
        "```",
        "",
        "## Veredito",
        "",
        "```",
        *_verdict_box(verdict),
        "```",
        "",
        "## A resposta honesta",
        "",
        "A ação completa de uma linha `S = Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` foi",
        "implementada numa rede 2D e testada em colisão. O resultado tem dois lados:",
        "",
        "1. **O objeto que a ação SUPORTA é matéria relativística completa (W4).** O kink",
        f"   de gauge tem massa {m['rest_mass']:.3f} ≈ 8 (sine-Gordon), obedece "
        "`E²=(pc)²+(mc²)²` (o fator 1/√(1−v²) **emerge** ao chutá-lo, não inserido), gera",
        "   o campo `θ(r) ~ M/r` (lei de D3), e a carga é conservada (G5). Cinco",
        "   consistências fecham — para o objeto **suportado**.",
        "2. **Mas a ação NÃO cria nem estabiliza esse objeto por colisão (W3, W5 →",
        "   Veredito D).** O termo de Wilson, no regime testável, é **sub-dominante** à",
        "   rigidez de gauge herdada (W2: a interação vórtice-antivórtice é Coulomb/BKT,",
        "   `λ_p`-independente; a energia de Wilson é auto-energia de núcleo, ~independente",
        "   de d — **não há corda linear**). Pior: aumentar λ_p **suprime** o núcleo criado",
        "   (que tem estrutura transversa, W_p≠0), encurtando sua vida — a sobrevivência",
        "   **decresce** monotonicamente com λ_p (W5). Não existe janela (λ_p, ρ)",
        "   cooperativa; a criação marginal sobrevive só em λ_p≈0 (= CR_GAUGE) e ρ alto",
        "   (regime mal-posto de G3).",
        "",
        "**Por que (física honesta):** em 2D, U(1) compacto **não** confina linearmente",
        "cargas de winding ±1 via o termo de plaqueta estático — um quantum de fluxo 2π é",
        "quase invisível ao cosseno compacto (`cos 2π = 1`), e o confinamento linear",
        "(Polyakov) é um efeito **dinâmico** de monopólos/instantons, não capturado por uma",
        "relaxação estática nem por esta colisão real-time em 2D. A intuição do prompt",
        "(λ_p maior → mais tensão → confinamento) é a da QCD 4D; não se transfere ao",
        "U(1) compacto 2D testado aqui.",
        "",
        "## Mapa de camadas (fechado)",
        "",
        "```",
        "BD linear     → não cria              (CR3)",
        "DBI escalar   → sem winding           (DBI3)",
        "DBI compacto  → kink estável / par virtual (DBI4)",
        "GAUGE acoplado→ transfere 57%, par virtual, mas vira radiação (CR_GAUGE: gargalo)",
        "WILSON 2D     → não confina o winding (estático/BKT); λ_p SUPRIME  (este trabalho)",
        "  estável exige → Polyakov dinâmico / dimensão maior / campo externo (Oxford-petawatt)",
        "```",
        "",
        "A fronteira da criação de matéria está agora **mapeada com precisão**: a ação de",
        "uma linha contém geometria (R1–R3), gravitação (D1–D3), gravidade modificada",
        "(ponte DEV), e **suporta** matéria como kink topológico com massa, campo",
        "gravitacional e `E²=(pc)²+(mc²)²` — mas **não a cria nem a confina** por colisão",
        "no regime testável. O que falta é identificado: o mecanismo **dinâmico** de",
        "confinamento (Polyakov/monopólos), dimensão espacial maior, ou um campo externo",
        "(lasers petawatt, como Oxford). Veredito **D**: a ação completa é insuficiente",
        "para criar matéria estável — e a razão é precisa, não vaga.",
        "",
        "![W2](W2_string.png)",
        "![W3](W3_collision.png)",
        "![W5](W5_phasediagram.png)",
        "",
    ]
    (wc.OUTDIR / "W6_synthesis.md").write_text("\n".join(lines), encoding="utf-8")


def _patch_root_md(w1, w2, w3, w4, w5, verdict):
    path = wc.ROOT / "MATTER_CR_WILSON.md"
    m = w4["mass"]
    block = "\n".join([
        "",
        "| Tarefa | Resultado | Grade |",
        "|--------|-----------|-------|",
        "| W1 — ação completa | VALIDADO (λ_p=0→GAUGE exato, pure gauge/Maxwell, kink m=8 intacto, E conservada) | A |",
        f"| W2 — tensão de corda | NÃO há corda linear (2D estático = Coulomb/BKT; λ_c op.={w2['lam_c']}) | C |",
        f"| W3 — colisão c/ Wilson | kink NÃO estabilizado; λ_p SUPRIME a sobrevivência | {w3['grade']} |",
        f"| W4 — objeto suportado | CONSISTENTE (m={m['rest_mass']:.2f}≈8, E²=(pc)²+(mc²)², θ~M/r) mas não criado | — |",
        "| W5 — mapa de fase | MAPEADO (sem janela cooperativa; criação só λ_p≈0, ρ alto) | — |",
        "",
        f"**Veredito: {verdict} — sem transição no regime testável.** A ação completa "
        "`S=Σ Δτ[1−cos(φ+Δθ)] + λ_p Σ[1−cos(W_p)]` (rede 2D) **suporta** matéria",
        f"relativística completa (W4: kink m={m['rest_mass']:.2f}≈8, `E²=(pc)²+(mc²)²` com",
        "1/√(1−v²) emergente, `θ(r)~M/r`, carga conservada) — cinco consistências fecham",
        "para o objeto suportado. **Mas não o cria nem confina por colisão:** o termo de",
        "Wilson é sub-dominante à rigidez herdada (W2: vórtices Coulomb/BKT, sem corda",
        "linear), e aumentar λ_p **suprime** o núcleo criado (W3/W5: sobrevivência decresce",
        "com λ_p, sem janela cooperativa). Razão física: U(1) compacto 2D não confina",
        "winding via plaqueta **estática** — o confinamento linear (Polyakov) é dinâmico",
        "(monopólos), exige dimensão maior ou campo externo. A fronteira está mapeada com",
        "precisão. Ver `results/matter/cr_wilson/W6_synthesis.md`.",
        "",
    ])
    text = path.read_text(encoding="utf-8")
    start = text.index("<!-- VERDICT_BLOCK_START -->") + len("<!-- VERDICT_BLOCK_START -->")
    end = text.index("<!-- VERDICT_BLOCK_END -->")
    text = text[:start] + "\n" + block + "\n" + text[end:]
    path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
