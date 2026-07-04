"""T3C -- HBAR AS CAUSAL GRANULARITY: does the phase scale k grow with the
internal complexity N of a structure?  (TIER3_EXPLORATIONS.md, aposta T3C)

Background (both MEASURED results, reused unchanged):
  * CC2: tau(N) -- the longest causal chain through a structure of internal
    complexity N embedded in a Poisson medium -- is proportional to N.
  * e11: the phase per causal tick theta_0 is the ONLY postulate (e10's
    Sorkin alternation gives the FORM); the absolute scale k = theta_0
    sqrt(rho) is EXTERNAL to the geometry.

Hypothesis under test: a structure of complexity N has phase scale
    k(N) = theta_0 * tau(N) / X        (phase per unit displacement,
                                        X = total displacement of the
                                        trajectory template, fixed)
and k proportional to N would read, through k = m/hbar, as "hbar = action per
causal event".

T3C-1: measure k(N) for the CC structures (internal diamonds, N = 0..100,
       rho = 60, 20 medium seeds -- the CC2 protocol).
T3C-2: if k ~ N, extract the coefficient and cross-check against CC2's
       tau-per-loop coefficient (consistency, NOT a derivation of hbar --
       e11 already showed the absolute scale is external).
T3C-3: repeat for different structure types on the SAME trajectory template:
       diamonds (cycles), chains (timelike segments, no cycles), poisson
       (segments of random duration).  Universal k ~ N, or topology-specific?

PRE-REGISTERED KILL CRITERIA (from TIER3_EXPLORATIONS.md -- not to be altered):

    MORTE  : k independent of N.
    PARCIAL: k ~ N^alpha with alpha != 1.
    SUCESSO: k ~ N with a measurable coefficient, consistent with
             hbar = action-per-causal-event.

Operationalisation fixed BEFORE running (this docstring):
  * MORTE: |k(100) - k(1)| < 5 * typical sem  (CC2-style significance).
  * SUCESSO: |alpha - 1| <= 0.10 and R^2 >= 0.99 on the diamond type
    (log-log fit over N in {1, 3, 10, 30, 100}).
  * PARCIAL: otherwise.
  * Universality (T3C-3): universal iff |alpha_type - 1| <= 0.15 for all
    three types.

HONESTY, stated up front: for the diamond type this is CC2's tau ~ N read
through the e10/e11 phase postulate -- the genuinely NEW content is (a) the
interference reading (fringe spacing ~ 1/N, COMPARISON ONLY), (b) the
universality test across structure types, (c) the coefficient cross-check.

ANTI-CIRCULARITY: no m, no hbar, no de Broglie wavelength in any generator;
theta_0 = 1 is the dimensionless natural choice (e11).  Complex numbers only
inside e11's labelled COMPARISON ONLY block (we call e11's function; this file
contains none).  Scanned by tests/test_no_circularity.py.

Output: results/tier3/T3C_hbar_granularity/{T3C_phase_data.json, .md, .png}
Reproduce: python results/tier3/T3C_hbar_granularity/T3C_phase.py
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(ROOT / "results" / "matter" / "complexity"))
sys.path.insert(0, str(ROOT / "experiments"))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt                      # noqa: E402

import complexity_core as cc                         # noqa: E402
import e11_phase_scale as e11                        # noqa: E402
import tier3_core as t3                              # noqa: E402

RHO = 60.0                       # CC2's medium density
THETA0 = 1.0                     # phase per causal tick (e11: the only natural
                                 # dimensionless choice; scale is external)
N_LADDER = cc.N_LADDER           # [0, 1, 3, 10, 30, 100]
SEEDS = range(20)
N_EXT = 12                       # trajectory template: 12 external steps
X_DISP = 12.0                    # total displacement of the template
TYPES = ("diamond", "chain", "poisson")
FRINGE_DEMO_NS = (1, 10, 100)


# ---------------------------------------------------------------------------
# Structures on the SAME trajectory template (pure counting, no physics)
# ---------------------------------------------------------------------------
def build_segments(N, kind, build_seed=0):
    """Internal timelike segments [(A, B, halfwidth)] distributed over the
    N_EXT-step template, exactly like cc.build_structure distributes diamonds.

      chain  : N unit-duration timelike segments (dt=1, dx=0)  -- Betti 0.
      poisson: N segments of random duration U(0.5, 1.5) (mean 1), fixed per
               structure (build rng), random medium per seed -- Betti 0.
    """
    rng = np.random.default_rng(97 + 1000 * build_seed + N)
    segs = []
    t, x = 0.0, 0.0
    left = N
    for kstep in range(N_EXT):
        d_here = left // (N_EXT - kstep)
        left -= d_here
        for _ in range(d_here):
            dur = 1.0 if kind == "chain" else float(rng.uniform(0.5, 1.5))
            segs.append(((t, x), (t + dur, x), 0.3))
            t += dur
        t += 1.0
        x += 1.0
    return segs


def tau_segments(segs, rho, rng, pad=0.15):
    """Longest causal chain summed over the internal segments embedded in a
    Poisson medium -- the same measurement as cc.proper_time, generalised to
    plain timelike segments (uses cc.longest_chain; pure counting)."""
    total = 0
    for (A, B, w) in segs:
        box = [(A[0] - pad, B[0] + pad), (A[1] - w - pad, A[1] + w + pad)]
        pts = cc.sprinkle_box(rho, box, rng)
        if len(pts):
            dtA = pts[:, 0] - A[0]
            fa = (dtA > 0) & (dtA * dtA > (pts[:, 1] - A[1]) ** 2)
            dtB = B[0] - pts[:, 0]
            fb = (dtB > 0) & (dtB * dtB > (pts[:, 1] - B[1]) ** 2)
            pts = pts[fa & fb]
        core = (np.vstack([np.array(A), np.array(B), pts]) if len(pts)
                else np.vstack([np.array(A), np.array(B)]))
        total += cc.longest_chain(core)
    return int(total)


def measure_type(kind):
    """k(N) over the ladder for one structure type (20 medium seeds each)."""
    rows = []
    for N in N_LADDER:
        taus = []
        for seed in SEEDS:
            rng = np.random.default_rng(7000 + seed)     # CC2's seed scheme
            if kind == "diamond":
                s = cc.build_structure(N, n_ext=N_EXT)
                taus.append(cc.proper_time(s, RHO, rng))
            else:
                segs = build_segments(N, kind)
                taus.append(tau_segments(segs, RHO, rng))
        ks = [THETA0 * tval / X_DISP for tval in taus]
        st_t, st_k = cc.seed_stats(taus), cc.seed_stats(ks)
        rows.append({"N": int(N), "tau": st_t, "k": st_k})
        print(f"    {kind:>8} N={N:4d}: tau={st_t['mean']:8.2f} "
              f"+/- {st_t['sem']:.2f}   k={st_k['mean']:7.3f} "
              f"+/- {st_k['sem']:.3f}")
    return rows


def fit_alpha(rows):
    """Log-log fit k ~ N^alpha over N>0; returns alpha, R2, coefficient k/N."""
    N = np.array([r["N"] for r in rows], dtype=float)
    k = np.array([r["k"]["mean"] for r in rows], dtype=float)
    pos = N > 0
    lx, ly = np.log(N[pos]), np.log(k[pos])
    alpha, logc = np.polyfit(lx, ly, 1)
    pred = alpha * lx + logc
    ss_res = float(np.sum((ly - pred) ** 2))
    ss_tot = float(np.sum((ly - ly.mean()) ** 2))
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else float("nan")
    a_lin = float(np.sum(N[pos] * k[pos]) / np.sum(N[pos] ** 2))
    return {"alpha": float(alpha), "r2": float(r2),
            "k_per_N": a_lin, "logc": float(logc)}


def death_check(rows):
    """Pre-registered MORTE test: is k(100) - k(1) significant?"""
    by_n = {r["N"]: r["k"] for r in rows}
    diff = by_n[100]["mean"] - by_n[1]["mean"]
    sem_typ = float(np.mean([r["k"]["sem"] for r in rows if r["N"] > 0]))
    return {"k1": by_n[1]["mean"], "k100": by_n[100]["mean"],
            "diff": float(diff), "sem_typ": sem_typ,
            "significant": bool(abs(diff) > 5 * sem_typ)}


# ---------------------------------------------------------------------------
# Fringe reading (calls e11; the postulated-phase block lives THERE, labelled)
# ---------------------------------------------------------------------------
def fringe_demo(diamond_rows):
    # finer screen than e11's default: at N=100 the fringe spacing (~0.06)
    # is below e11's pixel (0.1) and peak counting would saturate -- a
    # resolution artefact, not physics.  Restored after use.
    n_screen0 = e11.N_SCREEN
    e11.N_SCREEN = 4800
    try:
        screen_x, L_L, L_R, dL = e11.double_slit_path_lengths()
    finally:
        e11.N_SCREEN = n_screen0
    by_n = {r["N"]: r["k"]["mean"] for r in diamond_rows}
    demo = []
    for N in FRINGE_DEMO_NS:
        kN = by_n[N]
        spacing, n_fr = e11.fringe_spacing(screen_x, dL, kN, THETA0)
        xd, Id = e11.comparison_intensity(screen_x, L_L, L_R, kN, THETA0)
        n_peaks, peak_spacing = e11.count_peaks(xd, Id)
        demo.append({"N": int(N), "k": float(kN),
                     "analytic_spacing": float(spacing),
                     "n_fringes": float(n_fr), "n_peaks": int(n_peaks),
                     "peak_spacing": float(peak_spacing)})
        print(f"    fringe demo N={N:4d}: k={kN:6.3f}  spacing={spacing:7.3f}"
              f"  peaks={n_peaks}")
    return demo, (screen_x, L_L, L_R)


# ---------------------------------------------------------------------------
def verdict(fits, death):
    fd = fits["diamond"]
    if not death["significant"]:
        v, box = "MORTE", "k independente de N"
    elif abs(fd["alpha"] - 1.0) <= 0.10 and fd["r2"] >= 0.99:
        v, box = "SUCESSO", "k proporcional a N (coeficiente mensuravel)"
    else:
        v, box = "PARCIAL", f"k ~ N^{fd['alpha']:.2f} (alpha != 1)"
    universal = all(abs(f["alpha"] - 1.0) <= 0.15 for f in fits.values())
    return {"verdict": v, "synthesis_box": box,
            "alpha_diamond": fd["alpha"], "r2_diamond": fd["r2"],
            "k_per_N_diamond": fd["k_per_N"],
            "alphas": {t: f["alpha"] for t, f in fits.items()},
            "universal_across_types": bool(universal),
            "death_check": death}


def cc2_crosscheck(fits):
    """Coefficient consistency with CC2 (same machinery): k/N = theta0*a/X."""
    p = ROOT / "results" / "matter" / "complexity" / "CC2_cost.json"
    if not p.exists():
        return None
    a_cc2 = json.loads(p.read_text())["fit"]["tau_per_loop_a"]
    expected = THETA0 * a_cc2 / X_DISP
    measured = fits["diamond"]["k_per_N"]
    return {"a_cc2_tau_per_loop": float(a_cc2),
            "k_per_N_expected_from_cc2": float(expected),
            "k_per_N_measured": float(measured),
            "ratio": float(measured / expected) if expected else float("nan")}


def figure(data, fits, demo, geom, out_png):
    fig, ax = plt.subplots(1, 3, figsize=(16, 4.6))
    colors = {"diamond": "tab:red", "chain": "tab:blue",
              "poisson": "tab:green"}
    for kind, rows in data.items():
        N = np.array([r["N"] for r in rows], dtype=float)
        k = np.array([r["k"]["mean"] for r in rows])
        ke = np.array([r["k"]["sem"] for r in rows])
        pos = N > 0
        ax[0].errorbar(N[pos], k[pos], yerr=ke[pos], fmt="o",
                       color=colors[kind], capsize=3,
                       label=f"{kind} (alpha={fits[kind]['alpha']:.3f})")
        xs = np.geomspace(1, 100, 50)
        f = fits[kind]
        ax[0].plot(xs, np.exp(f["logc"]) * xs ** f["alpha"], "-",
                   color=colors[kind], alpha=0.5)
    ax[0].set_xscale("log")
    ax[0].set_yscale("log")
    ax[0].set_xlabel("internal complexity N")
    ax[0].set_ylabel("phase scale k = theta0 tau / X")
    ax[0].set_title("T3C: k(N) per structure type")
    ax[0].legend(fontsize=8)

    Ns = np.array([d["N"] for d in demo], dtype=float)
    sp = np.array([d["analytic_spacing"] for d in demo])
    ax[1].loglog(Ns, sp, "o-", color="tab:purple", label="measured spacing")
    ax[1].loglog(Ns, sp[0] * Ns[0] / Ns, "k:", label="1/N (k ~ N)")
    ax[1].set_xlabel("N")
    ax[1].set_ylabel("fringe spacing")
    ax[1].set_title("fringe spacing ~ 1/N (COMPARISON ONLY reading)")
    ax[1].legend(fontsize=8)

    screen_x, L_L, L_R = geom
    for d in demo:
        xd, Id = e11.comparison_intensity(screen_x, L_L, L_R, d["k"], THETA0)
        ax[2].plot(xd, Id, "-", alpha=0.8, label=f"N={d['N']}")
    ax[2].set_xlabel("screen position x")
    ax[2].set_ylabel("intensity (postulated phase, e11 block)")
    ax[2].set_title("two-slit patterns per complexity (COMPARISON ONLY)")
    ax[2].legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def report(out, path):
    v = out["verdict"]
    L = ["# T3C -- hbar como granularidade causal: k proporcional a N?", "",
         "Escala de fase k(N) = theta0 tau(N) / X de estruturas de",
         "complexidade interna N embebidas num meio de Poisson (rho=60, 20",
         "sementes -- protocolo CC2), lida em franjas pela maquinaria de e11.",
         "Criterios pre-registrados em TIER3_EXPLORATIONS.md e no docstring.",
         "", "## k(N) por tipo de estrutura", ""]
    for kind, rows in out["data"].items():
        f = out["fits"][kind]
        L += [f"### {kind} (alpha = {f['alpha']:.3f}, R2 = {f['r2']:.5f}, "
              f"k/N = {f['k_per_N']:.4f})", "",
              "| N | tau (mean +/- sem) | k (mean +/- sem) |", "|---|---|---|"]
        for r in rows:
            L.append(f"| {r['N']} | {r['tau']['mean']:.2f} +/- "
                     f"{r['tau']['sem']:.2f} | {r['k']['mean']:.3f} +/- "
                     f"{r['k']['sem']:.3f} |")
        L.append("")
    dc = v["death_check"]
    L += ["## Teste de morte pre-registrado", "",
          f"k(100) - k(1) = {dc['diff']:.3f} vs 5 x sem tipico = "
          f"{5 * dc['sem_typ']:.3f} -> "
          f"{'SIGNIFICATIVO (nao morre)' if dc['significant'] else 'NAO significativo (MORTE)'}",
          "", "## Leitura em franjas (COMPARISON ONLY -- fase postulada em e11)",
          "", "| N | k | espacamento analitico | picos contados | espacamento "
          "dos picos |", "|---|---|---|---|---|"]
    for d in out["fringe_demo"]:
        L.append(f"| {d['N']} | {d['k']:.3f} | {d['analytic_spacing']:.3f} | "
                 f"{d['n_peaks']} | {d['peak_spacing']:.3f} |")
    cx = out.get("cc2_crosscheck")
    if cx:
        L += ["", "## T3C-2 -- coeficiente e consistencia com CC2", "",
              f"- CC2 mediu tau/N = {cx['a_cc2_tau_per_loop']:.3f} links/loop "
              f"(rho=60).",
              f"- Esperado k/N = theta0 (tau/N)/X = "
              f"{cx['k_per_N_expected_from_cc2']:.4f}; medido "
              f"{cx['k_per_N_measured']:.4f} (razao {cx['ratio']:.3f}).",
              "- ATENCAO: a razao e 1.000 POR CONSTRUCAO -- este modulo reusa",
              "  deliberadamente o protocolo de CC2 (mesmas sementes, mesma",
              "  maquinaria), entao isto e uma verificacao de coerencia",
              "  interna, NAO uma confirmacao independente.",
              "- Leitura: com theta0 = acao-por-tick/hbar, k = m/hbar da "
              "m c^2 proporcional a tau(N) -- consistente com CC2 (m c^2 = "
              "atualizacoes internas). NAO e derivacao de hbar: e11 mostrou "
              "que a escala absoluta e EXTERNA a geometria; aqui so a "
              "ESTRUTURA (k ~ N) e medida."]
    L += ["", "## VEREDITO (criterio pre-registrado)", "",
          f"**{v['verdict']}** -- {v['synthesis_box']}.",
          f"- alpha (diamantes) = {v['alpha_diamond']:.3f}  "
          f"(R2 = {v['r2_diamond']:.5f})",
          f"- alphas por tipo: " + ", ".join(
              f"{t}={a:.3f}" for t, a in v["alphas"].items()),
          f"- universal entre tipos (|alpha-1| <= 0.15 em todos): "
          f"{'SIM' if v['universal_across_types'] else 'NAO'}", "",
          "### Honestidade", "",
          "Para o tipo 'diamond' isto e CC2 (tau ~ N) relido pela fase de",
          "e10/e11 -- nao e uma descoberta independente. Alem disso, os tipos",
          "'diamond' e 'chain' produzem numeros IDENTICOS ate o ultimo digito:",
          "o estimador tau (de CC2) usa apenas os ENDPOINTS de cada regiao",
          "interna + o meio de Poisson -- os eventos de ramificacao do",
          "diamante nunca entram na cadeia. Logo 'chain' NAO e confirmacao",
          "independente; e a mesma medicao. Isso e em si um achado honesto:",
          "o driver de tau (e de k) e a DURACAO TIPO-TEMPO interna, nao a",
          "topologia de ciclos (Betti). O teste de tipo genuinamente distinto",
          "e o 'poisson' (duracoes aleatorias), que mantem a linearidade.",
          "O conteudo novo deste modulo:",
          "(a) a leitura interferometrica (espacamento de franjas ~ 1/N);",
          "(b) k segue o conteudo de tempo proprio, nao a topologia (acima);",
          "(c) o coeficiente bate com CC2. A escala ABSOLUTA de hbar continua",
          "externa a geometria (veredito e11, inalterado).", "",
          "![T3C](T3C_phase.png)", ""]
    Path(path).write_text("\n".join(L), encoding="utf-8")


def main():
    print("=" * 70)
    print("T3C -- HBAR AS CAUSAL GRANULARITY: k(N) ~ N?")
    print("=" * 70)
    t0 = time.perf_counter()
    data, fits = {}, {}
    for kind in TYPES:
        print(f"  T3C-{1 if kind == 'diamond' else 3}: type = {kind}")
        rows = measure_type(kind)
        data[kind] = rows
        fits[kind] = fit_alpha(rows)
    death = death_check(data["diamond"])
    print("  fringe reading (COMPARISON ONLY, e11 machinery):")
    demo, geom = fringe_demo(data["diamond"])
    v = verdict(fits, death)
    cx = cc2_crosscheck(fits)
    # honesty flag: diamond and chain are THE SAME measurement (the tau
    # estimator sees only segment endpoints + medium, never the branch events)
    chain_identical = all(
        abs(a["tau"]["mean"] - b["tau"]["mean"]) < 1e-12
        for a, b in zip(data["diamond"], data["chain"]))
    out = {"params": {"rho": RHO, "theta0": THETA0, "n_ladder": N_LADDER,
                      "n_seeds": len(list(SEEDS)), "n_ext": N_EXT,
                      "X_disp": X_DISP, "types": list(TYPES)},
           "chain_identical_to_diamond": bool(chain_identical),
           "data": data, "fits": fits, "fringe_demo": demo,
           "cc2_crosscheck": cx, "verdict": v,
           "runtime_s": time.perf_counter() - t0}
    t3.save_json(HERE, "T3C_phase_data", out)
    figure(data, fits, demo, geom, HERE / "T3C_phase.png")
    report(out, HERE / "T3C_phase.md")
    print("-" * 70)
    print(f"VERDICT T3C: {v['verdict']} -- {v['synthesis_box']}")
    print(f"  alphas: " + ", ".join(f"{t}={a:.3f}"
                                    for t, a in v["alphas"].items())
          + f"  universal={'SIM' if v['universal_across_types'] else 'NAO'}")
    print(f"[{out['runtime_s']:.1f}s]")


if __name__ == "__main__":
    main()
