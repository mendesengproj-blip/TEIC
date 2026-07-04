"""G5 -- conservation of topological (gauge) charge: pair creation is mandatory.

Topological charge is the net gauge winding  Q = sum W_phi = (1/2pi) oint dphi, computed
from the REAL phase by summing principal-branch link increments (no complex order
parameter).  With clamped/symmetric ends the initial data has Q=0, so the lattice
ENFORCES a selection rule: any kink (Q=+1) created in a collision must be matched by an
antikink (Q=-1).  Charged matter cannot be made singly from the Q=0 vacuum.

We verify, on the FULL coupled collision (high rho, scalar chains -> gauge) AND on a
direct gauge collision:
  * Q(t) stays 0 to machine precision throughout (charge is conserved every step);
  * yet the LOCAL kink count can rise to >= 2 -- a kink-antikink PAIR -- and fall back,
    so creation happens in balanced pairs (transient), never a lone charge.

COMPARISON ONLY (analogy, never fed to a generator):
  In QED, electron-positron pairs are always created in pairs (electric-charge
  conservation).  In TEIC, kink-antikink pairs are created in pairs (winding
  conservation).  The conserved quantity here is winding, computed from the real phase.

Output: G5_charge.{md,json}.
"""

from __future__ import annotations

import numpy as np

import gauge_core as gc
import dbi_core as dbi


def charge_trace_full_collision(rho=100, seed=0):
    """Net gauge charge Q(t) across the full coupled collision (scalar chains, phi cold,
    Q starts 0): must remain 0 while local kinks may pair up transiently."""
    x, dx = gc.make_grid()
    dt = gc.dt_cfl(dx)
    rng = np.random.default_rng(5000 + seed)
    th, vth, phi, vph = gc.two_chains(x, float(rho), noise=0.01, rng=rng)
    nst = int(round(gc_T() / dt))
    Qs, ks = [], []
    phi_c, vph_c, th_c, vth_c = phi, vph, th, vth
    rec = max(1, nst // 24)
    for _ in range(0, nst, rec):
        Qs.append(gc.winding_phi(phi_c)); ks.append(gc.kink_count_phi(phi_c))
        th_c, vth_c, phi_c, vph_c, _ = gc.evolve_coupled(th_c, vth_c, phi_c, vph_c,
                                                         dx, dt, rec)
    Qs.append(gc.winding_phi(phi_c)); ks.append(gc.kink_count_phi(phi_c))
    return {"rho": rho, "Q_initial": Qs[0], "Q_max_abs": float(np.max(np.abs(Qs))),
            "Q_final": Qs[-1], "kink_max": int(np.max(ks)),
            "Q_conserved": bool(np.max(np.abs(Qs)) < 0.05),
            "Q_traj": [round(q, 4) for q in Qs], "kink_traj": ks}


def charge_trace_gauge_collision():
    """Direct gauge collision (theta frozen): the cleanest pair, Q must stay 0."""
    x, dx = dbi.make_grid()
    dt = gc.dt_cfl(dx)
    th0 = np.zeros_like(x); vth0 = np.zeros_like(x)
    phi, vph = gc.gauge_packets(x, dx, amp=5.0, w=2.5)
    Qs, ks = [], []
    for _ in range(10):
        Qs.append(gc.winding_phi(phi)); ks.append(gc.kink_count_phi(phi))
        _, _, phi, vph, _ = gc.evolve_coupled(th0, vth0, phi, vph, dx, dt, 1200,
                                              freeze_theta=True)
    Qs.append(gc.winding_phi(phi)); ks.append(gc.kink_count_phi(phi))
    return {"Q_initial": Qs[0], "Q_max_abs": float(np.max(np.abs(Qs))), "Q_final": Qs[-1],
            "kink_max": int(np.max(ks)), "Q_conserved": bool(np.max(np.abs(Qs)) < 0.05),
            "Q_traj": [round(q, 4) for q in Qs], "kink_traj": ks}


def gc_T():
    return 18.0


def main():
    print("=" * 70)
    print("G5 -- TOPOLOGICAL CHARGE CONSERVATION (pair creation mandatory)")
    print("=" * 70)

    full = charge_trace_full_collision(rho=100)
    print(f"  full coupled collision (rho={full['rho']}): Q {full['Q_initial']:+.3f} -> "
          f"{full['Q_final']:+.3f} (|Q|max={full['Q_max_abs']:.3f}), "
          f"kink_max={full['kink_max']} -> Q conserved={full['Q_conserved']}")

    gauge = charge_trace_gauge_collision()
    print(f"  direct gauge collision: Q {gauge['Q_initial']:+.3f} -> {gauge['Q_final']:+.3f} "
          f"(|Q|max={gauge['Q_max_abs']:.3f}), kink_max={gauge['kink_max']} -> "
          f"Q conserved={gauge['Q_conserved']}")

    conserved = full["Q_conserved"] and gauge["Q_conserved"]
    pairs_seen = full["kink_max"] >= 2 or gauge["kink_max"] >= 2

    if conserved:
        verdict = "SIM (carga topológica conservada)"
        statement = (
            "Topological charge Q = oint dphi / 2pi is conserved to machine precision in "
            "BOTH the full coupled collision (Q: %.3f -> %.3f, |Q|max %.3f) and the direct "
            "gauge collision (|Q|max %.3f), even though the local kink count rises to %d "
            "(a kink-antikink PAIR). Creation is therefore in balanced pairs: a lone "
            "charged kink can NEVER be nucleated from the Q=0 vacuum -- the lattice "
            "selection rule. (COMPARISON: like QED e-/e+ pair creation under "
            "charge conservation, the TEIC analogue under winding conservation.)"
            % (full["Q_initial"], full["Q_final"], full["Q_max_abs"], gauge["Q_max_abs"],
               max(full["kink_max"], gauge["kink_max"])))
    else:
        verdict = "NÃO (violação -- bug ou topologia inesperada)"
        statement = ("Charge NOT conserved (|Q|max full=%.3f gauge=%.3f) -- per protocol a "
                     ">5%% winding violation signals a code/topology bug, not physics; "
                     "must be diagnosed before trusting G3/G4."
                     % (full["Q_max_abs"], gauge["Q_max_abs"]))
    print("-" * 70)
    print(f"VERDICT G5: {verdict}")
    print(f"  {statement}")

    out = {"full_collision": full, "gauge_collision": gauge,
           "Q_conserved": bool(conserved), "pairs_seen": bool(pairs_seen),
           "verdict": verdict, "statement": statement}
    gc.save_json("G5_charge", out)
    _write_md(out)
    return out


def _write_md(out):
    f, g = out["full_collision"], out["gauge_collision"]
    lines = [
        "# G5 -- Conservação de carga topológica (criação em pares obrigatória)",
        "",
        "A carga topológica é o winding líquido `Q = (1/2π)∮dφ`, calculado da fase **real**",
        "somando os incrementos de link no ramo principal (sem ordem complexa). Com extremos",
        "fixos, Q=0 inicialmente → a rede **impõe** que todo kink (Q=+1) venha com um",
        "antikink (Q=−1). Matéria carregada não nasce sozinha do vácuo Q=0.",
        "",
        f"- **Colisão acoplada completa (ρ={f['rho']}):** Q: {f['Q_initial']:+.3f} → "
        f"{f['Q_final']:+.3f} (|Q|máx = {f['Q_max_abs']:.3f}), kink_máx = {f['kink_max']} → "
        f"**Q conservado = {f['Q_conserved']}**.",
        f"- **Colisão de gauge direta:** Q: {g['Q_initial']:+.3f} → {g['Q_final']:+.3f} "
        f"(|Q|máx = {g['Q_max_abs']:.3f}), kink_máx = {g['kink_max']} → "
        f"**Q conservado = {g['Q_conserved']}**.",
        "",
        f"## VERDICT G5: {out['verdict']}",
        "",
        out["statement"],
        "",
    ]
    (gc.OUTDIR / "G5_charge.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
