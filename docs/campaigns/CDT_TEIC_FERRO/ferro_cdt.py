"""ferro_cdt.py -- CDT x TEIC: ferromagneto O(3) sobre o 1-esqueleto do CDT 3D (F1b).

Pre-registro: PRE_REGISTRO.md (criterios A e B congelados). Driver layer: reusa
orientation_core (O3Model, measure_correlation, fit_forms) e xi_suite (build_lattice_3d,
measure_point) SEM reimplementar; cdt_substrate.build_cdt entrega o grafo CDT verbatim.

Duas perguntas, vereditos SEPARADOS:
  A (reproducao): LRO genuino por FSS (m, U4, C(r)) -- igual GOLDSTONE_A3?
  B (universalidade): escapa do mean-field? (U4(J)-crossing, chi_max ~ N^x, xi_g/L)
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
TEIC_ROOT = HERE.parents[2]
sys.path.insert(0, str(TEIC_ROOT / "results" / "vacuum_structure" / "orientation"))
sys.path.insert(0, str(TEIC_ROOT / "docs" / "campaigns" / "ESCALA_XI"))

from orientation_core import (O3Model, lattice_periodic, measure_correlation,  # noqa: E402
                              fit_forms)
from xi_suite import build_lattice_3d, measure_point                          # noqa: E402
from cdt_substrate import build_cdt                                           # noqa: E402

J_A = 2.0                       # acoplamento de reproducao (GOLDSTONE_A3)
N_BURN, N_MEAS, MEAS_EVERY = 300, 40, 2


# ============================================================== #
# medicao coordenada-livre num conjunto de grafos CDT (1 tamanho)
# ============================================================== #
def measure_cdt_point(graphs, J, n_burn=N_BURN, n_meas=N_MEAS, meas_every=MEAS_EVERY,
                      with_corr=False, seed0=0):
    """m, U4, chi=N*Var(m) sobre varios grafos CDT (snapshots). Coordenada-livre.
    Se with_corr, mede C(r) por distancia de grafo no 1o grafo e ajusta fit_forms."""
    ms, m2_acc, m4_acc, n_samp = [], 0.0, 0.0, 0
    Ns, zs = [], []
    corr = None
    for s, G in enumerate(graphs):
        Ns.append(G.n); zs.append(float(G.degree.mean()))
        model = O3Model(G, J=J, seed=4000 + seed0 + s)
        model.equilibrate(n_burn, adapt=True)
        seed_ms, taken, sw = [], 0, 0
        while taken < n_meas:
            model.sweep(); sw += 1
            if sw % meas_every == 0:
                seed_ms.append(model.order_parameter()); taken += 1
        seed_ms = np.asarray(seed_ms)
        ms.append(seed_ms.mean())
        m2_acc += np.sum(seed_ms ** 2); m4_acc += np.sum(seed_ms ** 4); n_samp += seed_ms.size
        if with_corr and corr is None:
            r, C, w, _ = measure_correlation(model, n_burn=40, n_meas=n_meas,
                                             n_sources=32, r_max=18)
            corr = (r, C, w)
    ms = np.asarray(ms)
    m_mean = float(ms.mean())
    m2, m4 = m2_acc / n_samp, m4_acc / n_samp
    U4 = float(1.0 - m4 / (3.0 * m2 ** 2)) if m2 > 0 else float("nan")
    N0 = float(np.mean(Ns))
    chi = float(N0 * (m2 - m_mean ** 2))
    row = {"J": J, "N0_mean": N0, "z_mean": float(np.mean(zs)),
           "m": m_mean, "m_sem": float(ms.std(ddof=1) / np.sqrt(len(ms))) if len(ms) > 1
           else float("nan"),
           "m2": float(m2), "U4": U4, "chi": chi,
           "random_floor": float(1.0 / np.sqrt(N0)), "n_seeds": len(graphs)}
    if corr is not None:
        r, C, w = corr
        ff = fit_forms(r, C)
        # xi de grafo: comprimento de correlacao exponencial (fit_forms) e plateau
        xi_g = ff["exp"]["xi"] if np.isfinite(ff["exp"]["xi"]) else float("inf")
        L_g = N0 ** (1.0 / 3.0)
        row["corr"] = {"r": r.tolist(), "C": C.tolist(), "winner": ff["winner"],
                       "C_long": ff["C_long"], "xi_g": float(xi_g),
                       "xi_g_over_Lg": float(xi_g / L_g) if np.isfinite(xi_g) else float("inf"),
                       "L_g": float(L_g)}
    return row


# ============================================================== #
# GATE de validacao
# ============================================================== #
def validation_gate():
    print("=== GATE DE VALIDACAO (orientation_core sobre anchors classicos) ===", flush=True)
    out = {}
    # positivo: rede cubica 3D -> LRO + U4 ordenado (reusa build_lattice_3d + measure_point)
    pos = []
    for m in (6, 8, 10):
        g, xs = build_lattice_3d(m)
        r = measure_point([(g, xs)], J=J_A, n_burn=200, n_meas=30, meas_every=2, L_s=float(m))
        pos.append((m, r["N_mean"], r["m"], r["U4"]))
        print(f"  [POS rede 3D m={m}] N={r['N_mean']:.0f} m={r['m']:.3f} U4={r['U4']:.3f}",
              flush=True)
    out["positive_lattice3d"] = [{"m": m, "N": N, "m": mm, "U4": u} for m, N, mm, u in pos]
    pos_ok = pos[-1][2] > 0.5 and pos[-1][3] > 0.55          # ordenado no maior
    # negativo: rede 2D -> Mermin-Wagner, m decai com N (sem LRO de simetria continua)
    neg = []
    for m in (8, 16, 24):
        g = lattice_periodic((m, m))
        model = O3Model(g, J=J_A, seed=1)
        model.equilibrate(200, adapt=True)
        vals = []
        for _ in range(60):
            model.sweep()
            vals.append(model.order_parameter())
        mm = float(np.mean(vals))
        neg.append((m, g.n, mm))
        print(f"  [NEG rede 2D m={m}] N={g.n} m={mm:.3f}  (Mermin-Wagner: deve cair c/ N)",
              flush=True)
    out["negative_lattice2d"] = [{"m": m, "N": N, "m_val": mm} for m, N, mm in neg]
    neg_ok = neg[-1][2] < neg[0][2]                          # m menor no maior
    out["positive_ok"] = bool(pos_ok)
    out["negative_ok"] = bool(neg_ok)
    out["GATE_GREEN"] = bool(pos_ok and neg_ok)
    print(f"  >>> GATE {'VERDE' if out['GATE_GREEN'] else 'VERMELHO'} "
          f"(pos_ok={pos_ok}, neg_ok={neg_ok})", flush=True)
    return out


# ============================================================== #
# construcao dos substratos CDT (uma vez por (k0, Vt), reusada)
# ============================================================== #
def build_cdt_ladder(k0, volumes, n_seeds, therm=140):
    ladder = {}
    for Vt in volumes:
        graphs, infos = [], []
        for s in range(n_seeds):
            G, times, info = build_cdt(k0, Vt, seed=700 + 13 * s + int(Vt), therm=therm)
            graphs.append(G); infos.append(info)
        ladder[Vt] = (graphs, infos)
        print(f"    [CDT k0={k0} Vt={Vt}] N0~{np.mean([i['N0'] for i in infos]):.0f} "
              f"<z>={np.mean([i['z_mean'] for i in infos]):.1f} "
              f"frac_sp={np.mean([i['frac_links_spatial'] for i in infos]):.2f} "
              f"({n_seeds} seeds)", flush=True)
    return ladder


# ============================================================== #
# PERGUNTA A -- reproducao (LRO por FSS)
# ============================================================== #
def question_A(ladder, k0):
    print(f"=== PERGUNTA A (reproducao) k0={k0}, J={J_A} ===", flush=True)
    rows = []
    for Vt, (graphs, infos) in ladder.items():
        r = measure_cdt_point(graphs, J_A, with_corr=True)
        r["Vt"] = Vt
        rows.append(r)
        c = r.get("corr", {})
        print(f"  Vt={Vt} N0~{r['N0_mean']:.0f} m={r['m']:.4f}+/-{r['m_sem']:.4f} "
              f"U4={r['U4']:.3f} floor={r['random_floor']:.4f} m/floor={r['m']/r['random_floor']:.1f} "
              f"C(r):{c.get('winner','-')} C_long={c.get('C_long',float('nan')):.3f}", flush=True)
    Ns = np.array([r["N0_mean"] for r in rows])
    ms = np.array([r["m"] for r in rows])
    floors = np.array([r["random_floor"] for r in rows])
    U4s = np.array([r["U4"] for r in rows])
    m_trend = float(np.polyfit(np.log(Ns), np.log(ms), 1)[0])
    above = bool(np.all(ms / floors > 3.0))
    plateau = all(r.get("corr", {}).get("winner") == "const" for r in rows)
    reproduces = above and (m_trend > -0.15) and bool(np.all(U4s > 0.55))
    verdict = ("REPRODUZ_LRO" if reproduces else
               ("NAO_REPRODUZ" if (not above and m_trend < -0.35) else "PARCIAL"))
    print(f"  >>> A: {verdict} (m-trend dlnm/dlnN={m_trend:+.3f}, above_floor={above}, "
          f"U4>0.55={bool(np.all(U4s>0.55))}, C(r)-plateau={plateau})", flush=True)
    return {"k0": k0, "rows": rows, "m_trend": m_trend, "above_floor": above,
            "all_plateau": plateau, "verdict": verdict}


# ============================================================== #
# PERGUNTA B -- universalidade (escapa do mean-field?)
# ============================================================== #
def question_B(ladder, k0, Js):
    print(f"=== PERGUNTA B (universalidade) k0={k0} ===", flush=True)
    per_size = {}
    for Vt, (graphs, infos) in ladder.items():
        scan = []
        Jc_guess = 0.20            # perto do pico de chi (sonda) -> mede xi_g de grafo la'
        for J in Js:
            r = measure_cdt_point(graphs, J, n_burn=260, n_meas=36,
                                  with_corr=(abs(J - Jc_guess) < 1e-9))
            scan.append(r)
        chi = np.array([r["chi"] for r in scan])
        jmax = int(np.argmax(chi))
        per_size[Vt] = {"scan": scan, "chi_max": float(chi[jmax]),
                        "Jc": float(Js[jmax]), "N0": scan[0]["N0_mean"]}
        print(f"  Vt={Vt} N0~{scan[0]['N0_mean']:.0f}: chi_max={chi[jmax]:.2f} @ Jc={Js[jmax]:.2f} "
              f"U4@Jc={scan[jmax]['U4']:.3f}", flush=True)
    # chi_max ~ N^x
    Ns = np.array([per_size[Vt]["N0"] for Vt in ladder])
    chimax = np.array([per_size[Vt]["chi_max"] for Vt in ladder])
    x_exp = float(np.polyfit(np.log(Ns), np.log(chimax), 1)[0])
    Jcs = [per_size[Vt]["Jc"] for Vt in ladder]
    Jc_drift = float(Jcs[-1] - Jcs[0])
    print(f"  >>> B: chi_max ~ N^{x_exp:.2f}  (MF<=0.5, 3D-geom~0.66); Jc por tamanho={Jcs} "
          f"(drift={Jc_drift:+.2f})", flush=True)
    return {"k0": k0, "per_size": {str(k): v for k, v in per_size.items()},
            "Js": list(Js), "chi_max_exponent": x_exp, "Jc_per_size": Jcs,
            "Jc_drift": Jc_drift}


def main():
    t0 = time.time()
    smoke = "--smoke" in sys.argv
    out = {"config": {"J_A": J_A, "phase": "extended k0=1,3", "coupling": "uniform"}}
    out["gate"] = validation_gate()

    volumes = [1500, 3000] if smoke else [1500, 3000, 6000]
    n_seeds = 2 if smoke else 4
    therm = 60 if smoke else 140
    # J_c ~ 0.20 localizado por sonda (z~13 -> ordena com J fraco); cerca o pico de chi
    Js = [0.12, 0.18, 0.22, 0.30] if smoke else \
         [0.10, 0.13, 0.16, 0.18, 0.20, 0.22, 0.25, 0.28]

    out["A"], out["B"] = {}, {}
    for k0 in (1.0, 3.0):
        print(f"\n########## k0 = {k0} ##########", flush=True)
        ladder = build_cdt_ladder(k0, volumes, n_seeds, therm=therm)
        out["A"][str(k0)] = question_A(ladder, k0)
        out["B"][str(k0)] = question_B(ladder, k0, Js)

    out["runtime_s"] = time.time() - t0
    name = "ferro_cdt_smoke.json" if smoke else "ferro_cdt.json"
    (HERE / name).write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[{out['runtime_s']:.0f}s] -> {name}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
