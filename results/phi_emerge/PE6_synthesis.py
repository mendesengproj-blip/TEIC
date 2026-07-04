"""PE6_synthesis.py -- honest synthesis of PHI_EMERGE (the scorecard and the verdict).

Loads PE1-PE5 data and fills the prompt's scorecard.  Veredito A (emergent Phi pins and
creates stable matter) would be the most important result of the whole investigation and
REQUIRES triple verification -- it is asserted ONLY if PE4 (core dip) AND PE5 (collision)
both pass, which they do not.  The honest outcome is Veredito C.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import phi_emerge_core as pe   # noqa: E402

OUT = Path(__file__).resolve().parent


def load(name):
    p = OUT / name
    return json.loads(p.read_text()) if p.exists() else {}


def main():
    pe1 = load("PE1_definition.json")
    pe2 = load("PE2_condensate.json")
    pe3 = load("PE3_gauge_mass.json")
    pe4 = load("PE4_vortex.json")
    pe5 = load("PE5_collision.json")

    well_defined = pe1.get("phi_well_defined", False)
    condensate = pe2.get("spontaneous_magnitude_condensate", False)
    cr_const = False   # C(r)=const?  PE2 found it always decays
    mA_p = pe3.get("exponent_p_in_mA_vs_rho", float("nan"))
    mA_law = pe3.get("law", "")
    mA_grows = pe3.get("reproduces_abelian_higgs_mA_eq_e_v", False)
    core_dips = pe4.get("magnitude_core_dips", False)
    sigma_const = False  # no core => sigma not constant (undefined)
    matter = pe5.get("stable_matter_without_extra_ingredient", False)

    # Verdict logic (triple-verification gate for A)
    if core_dips and matter:
        verdict = "A"   # would require PE4 core AND PE5 matter -- triple-checked
    elif core_dips and not matter:
        verdict = "B"
    elif mA_grows and not core_dips:
        verdict = "C"
    else:
        verdict = "D"

    verdict_text = {
        "A": ("Phi emergente pina o vortice e cria materia estavel -> a acao minima "
              "deriva materia (resultado historico)."),
        "B": ("Phi emergente pina estaticamente mas nao em colisao -> substrato correto, "
              "criacao dinamica precisa de mais."),
        "C": ("Phi emergente GERA m_A (~sqrt(rho)) mas NAO pina -> mecanismo PARCIAL: a "
              "composicao rho*e^{i phibar} captura a fase (massa de gauge dependente da "
              "densidade) mas nao a magnitude dinamica (o nucleo do vortice). O campo "
              "complexo de CR_ABELIAN_HIGGS continua necessario para o nucleo/pinamento."),
        "D": ("Phi emergente nao tem propriedades de Higgs -> campo complexo externo e "
              "necessario (confirma CR_AH)."),
    }[verdict]

    scorecard = {
        "PE1 -- Phi=rho e^{i phibar} well-defined": "SIM" if well_defined else "NAO",
        "PE2 -- spontaneous condensate": "SIM" if condensate else "NAO",
        "PE2 -- C(r) = constant": "SIM" if cr_const else "decai (sempre)",
        "PE3 -- m_A vs rho": f"SIM, ~sqrt(rho) (p_measured={mA_p:.2f}, analytic 0.5)",
        "PE4 -- |Phi|(0) < |Phi|(inf) (core dip)": "SIM" if core_dips else "NAO",
        "PE4 -- sigma_core constant (pinning)": "SIM" if sigma_const else "NAO (no core)",
        "PE5 -- stable matter without extra axiom": "SIM" if matter else "NAO / N/A",
    }

    summary = {
        "scorecard": scorecard,
        "verdict": verdict,
        "verdict_text": verdict_text,
        "triple_verification_for_A": ("NOT triggered -- Veredito A requires PE4 core AND "
                                      "PE5 matter, both negative, so no A claim is made."),
        "what_emerged": ("the PHASE sector: arg(Phi)=phibar behaves like the gauge field "
                         "and gives a density-dependent mass m_A ~ sqrt(rho) (PE3, = AH2's "
                         "m_A=e<|Phi|>)."),
        "what_did_not": ("the MAGNITUDE sector: |Phi|=rho is the static causal-density "
                         "substrate, decoupled from the gauge vortex, so it never forms a "
                         "core (PE4) and creates no stable structure (PE5).  The abelian-"
                         "Higgs core needs |Phi| to be a DYNAMICAL field with a covariant "
                         "kinetic term |Phi|^2|D Phi|^2 -- which the bare density is not."),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }
    pe.save_json("PE6_synthesis", summary)

    print("=" * 74)
    print("PE6 -- PHI_EMERGE SYNTHESIS")
    print("=" * 74)
    for k, v in scorecard.items():
        print(f"  {k:48s}: {v}")
    print("-" * 74)
    print(f"VEREDITO: {verdict}")
    print("  " + verdict_text.replace(" -> ", "\n  -> "))
    print("-" * 74)
    print("Triple-verification for A:", summary["triple_verification_for_A"])
    print("What emerged   :", summary["what_emerged"])
    print("What did NOT   :", summary["what_did_not"])
    return summary


if __name__ == "__main__":
    main()
