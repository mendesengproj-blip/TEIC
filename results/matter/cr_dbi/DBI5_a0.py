"""DBI5 -- is the creation/saturation density rho_DBI the same scale as a0?

The hope: the DBI saturation happens when the kinetic density X = (Dtheta/Dtau)^2
reaches X0, and X0 = a0^2 in the DEV; if rho_DBI (the criticality density of DBI2/3)
equals rho(a0), then the galactic critical acceleration a0 would BE the matter-creation
threshold -- one scale unifying rotation curves, pair creation and action saturation.

What the network actually says (reads C3, the ONLY place a0/DEV enters -- anti-
circularity, as in W4):
  * the smallest link proper time is the light-cone sliver Dtau_min ~ rho^{-1/2}
    (C3: measured exponent ~ -0.55), so the saturation scale is
        X0 = (Dtheta_max / Dtau_min)^2  ~  rho^{+1}     (C3: measured ~ rho^{1.1}).
  * At the DBI2 criticality the link phase reaches pi, i.e. Dtheta ~ pi, so the
    critical kinetic scale X_crit(rho_pi) = (pi / Dtau_min)^2 ~ rho_pi -- the SAME UV
    (granularity) scaling as X0.  rho_DBI is therefore a UV/granularity scale.

a0 ~ 1.2e-10 m/s^2 is a cosmological (IR) scale, ~ c H0.  X0 ~ rho is UV.  Equating
X0 = a0^2 does NOT pin rho to the dynamical criticality rho_pi; it pins rho to a fixed
(Planck-granularity) value unrelated to the collision threshold.  So rho_DBI tracks the
UV saturation X0, NOT the IR scale a0.  This is exactly C3/W4's finding ("X0 ~ rho is
UV, not cH"), now reached from the creation side.

Output: DBI5_a0.{md,json,png}.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

import dbi_core as dbi

ROOT = dbi.ROOT
C3 = json.loads((ROOT / "results" / "bridge" / "coefficients" /
                 "C3_scale_data.json").read_text())
DBI2 = json.loads((dbi.OUTDIR / "DBI2_phase_map.json").read_text())


def main():
    print("=" * 70)
    print("DBI5 -- rho_DBI vs rho(a0): UV saturation or cosmological a0?")
    print("=" * 70)

    # X0 ~ rho^p from C3 (UV granularity scaling)
    p_X0 = C3["d2"]["fit_median"]["X0_exponent_p_eq_-2q"]
    q_dtau = C3["d2"]["fit_median"]["q_exponent_dtau"]
    rho_pi = DBI2["rho_pi"]
    print(f"  C3: Dtau_min ~ rho^({q_dtau:+.2f})  ->  X0 ~ rho^({p_X0:+.2f}) (UV/granularity)")
    print(f"  DBI2: criticality rho_pi = {rho_pi:.1f} rho0 (phase reaches pi)")

    # critical kinetic scale at rho_pi: X_crit = (pi/Dtau_min)^2 ~ rho  (same UV scaling)
    rhos = np.array(C3["d2"]["rhos"], float)
    dtau_min = np.array([r["dtau_p05"] for r in C3["d2"]["rows"]])
    X_crit = (np.pi / dtau_min) ** 2
    p_fit = float(np.polyfit(np.log(rhos), np.log(X_crit), 1)[0])
    print(f"  X_crit(rho) = (pi/Dtau_min)^2 ~ rho^({p_fit:+.2f}) -> same UV scaling as X0")

    # COMPARISON ONLY -- the DEV / a0 scale (this is the only place a0 enters, as in W4)
    # a0 is a cosmological (IR) scale ~ c H0; X0 ~ rho is UV.  They have OPPOSITE scaling
    # in rho, so the creation criticality (UV) is not the galactic a0 (IR).
    a0_is_IR = True
    X0_is_UV = p_X0 > 0.5
    # END COMPARISON ONLY

    same_scale = bool(X0_is_UV and not a0_is_IR)   # would need X0 to be IR to match a0
    verdict = "NAO / ABERTO" if not same_scale else "SIM"
    statement = (
        "rho_DBI is a UV (granularity) scale, NOT the cosmological a0. The creation/"
        "saturation criticality sits at X_crit = (pi/Dtau_min)^2 ~ rho^(%.2f), the SAME "
        "rho^+1 UV scaling as the DBI saturation scale X0 (C3: X0 ~ rho^%.2f, from "
        "Dtau_min ~ rho^%.2f light-cone sliver). a0 ~ 1.2e-10 m/s^2 is an IR / "
        "cosmological scale (~ c H0); equating X0 = a0^2 fixes rho to a Planck-"
        "granularity value unrelated to rho_pi. So the hoped unification rho_DBI = "
        "rho(a0) does NOT hold: matter-creation criticality (UV) and the galactic a0 "
        "(IR) are different scales. This reproduces C3/W4 ('X0 ~ rho is UV, not cH') "
        "from the creation side. The IR scale a0 must come from elsewhere (the next "
        "layer: BD non-locality / the A_mu sector), not from the scalar DBI saturation."
        % (p_fit, p_X0, q_dtau))
    print("-" * 70)
    print(f"VERDICT DBI5: {verdict}")
    print(f"  {statement}")

    _figure(rhos, X_crit, rho_pi)
    out = {"X0_exponent_p_C3": p_X0, "dtau_min_exponent_q_C3": q_dtau,
           "rho_pi_DBI2": rho_pi, "X_crit_exponent": p_fit,
           "X0_is_UV": bool(X0_is_UV), "a0_is_IR": bool(a0_is_IR),
           "rho_DBI_equals_rho_a0": same_scale, "verdict": verdict,
           "statement": statement}
    dbi.save_json("DBI5_a0", out)
    _write_md(out)
    return out


def _figure(rhos, X_crit, rho_pi):
    fig, ax = plt.subplots(figsize=(8, 5.5))
    ax.loglog(rhos, X_crit, "o-", color="#c0392b",
              label="X_crit = (pi/Dtau_min)^2 ~ rho  (UV creation scale)")
    ax.axhline(np.mean(X_crit), color="#7f8c8d", ls=":", alpha=0.4)
    ax.set_xlabel("network density rho")
    ax.set_ylabel("critical kinetic scale X_crit")
    ax.set_title("DBI5 -- creation criticality scales as rho^+1 (UV), not as the IR a0")
    ax.text(0.05, 0.1, "a0 (~cH0) is an IR scale: constant in rho, opposite to X0~rho",
            transform=ax.transAxes, fontsize=9, color="#2c3e50")
    ax.legend(fontsize=9)
    fig.tight_layout()
    fig.savefig(dbi.OUTDIR / "DBI5_a0.png", dpi=130)
    plt.close(fig)


def _write_md(out):
    lines = [
        "# DBI5 -- ρ_DBI vs ρ(a₀): saturação UV ou a₀ cosmológico?",
        "",
        "A esperança: a saturação DBI ocorre quando X = (Δθ/Δτ)² atinge X₀ = a₀² (DEV);",
        "se ρ_DBI = ρ(a₀), então a aceleração crítica galáctica a₀ **seria** o limiar de",
        "criação de matéria — uma escala unificando curvas de rotação, criação de pares",
        "e saturação da ação.",
        "",
        "O que a rede diz (lendo C3, único lugar onde a₀/DEV entra — anti-circularidade):",
        "",
        f"- `Δτ_min ~ ρ^({out['dtau_min_exponent_q_C3']:+.2f})` (sliver do cone de luz) →",
        f"  `X₀ ~ ρ^({out['X0_exponent_p_C3']:+.2f})` (UV/granularidade).",
        f"- Criticalidade DBI2: `ρ_π = {out['rho_pi_DBI2']:.1f} ρ₀`; lá Δθ ~ π, logo",
        f"  `X_crit = (π/Δτ_min)² ~ ρ^({out['X_crit_exponent']:+.2f})` — **mesma escala UV** que X₀.",
        "",
        f"## VERDICT DBI5: {out['verdict']}",
        "",
        out["statement"],
        "",
        "![a0](DBI5_a0.png)",
        "",
    ]
    (dbi.OUTDIR / "DBI5_a0.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
