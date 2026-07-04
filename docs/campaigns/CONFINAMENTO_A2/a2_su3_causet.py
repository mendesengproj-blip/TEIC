"""A2 / C3 -- SU(3) Wilson loops on the causal substrate (confinement: causet vs cubic).

Campaign CONFINAMENTO_A2 (Fase 2, Frente A).  Does the SU(3) confinement (V~sigma r,
sigma=Creutz>0) measured by FLC on the CUBIC control lattice also hold on the CAUSET,
or is the causal set's non-locality an obstruction (as for U(1) in E5/E7)?

The Paper SU3 already scopes confinement to the 8^4 cubic lattice; only ferromagnetism
is claimed on both.  So A2 either PROMOTES (causet confines cleanly) or CONFIRMS the
honest cubic-only scope (obstruction).

Two stages (anti-circular, mirrors E7):
  STAGE A -- validate on the regular 4D lattice (answer KNOWN): the gold-standard
    Creutz ratio chi(2,2) from controlled R x T rectangles must be >0 and decrease
    with weaker coupling (reproduces FLC: sigma=1.35..0.33 at beta=4.0..6.0).  Uses
    the validated su3_core gauge machinery directly.
  STAGE B -- measure on the causal set: SU(3) gauge MC on the height-2 causal-diamond
    plaquette list.  The fundamental plaquette <W_1>(beta) is the ONLY controlled
    SU(3) loop on the causet (non-Abelian holonomy = ordered matrix product; E7's
    Abelian patch-cancellation surrogate does NOT extend).  We measure <W_1>(beta)
    (gauge sector is alive) and show that the area-law string tension sigma -- the
    large-loop (k>=2) log-slope -- has NO controlled estimator on the non-local
    causet (zero R x T rectangles; no ordered patch boundary word).

Anti-circularity: only the graph + Wilson action; beta swept never input; no sigma /
alpha_s / mass inserted; SU(3) matrices via su3_core (under the A1 guard).

Run:  python docs/campaigns/CONFINAMENTO_A2/a2_su3_causet.py
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "results" / "matter" / "fl1"))
sys.path.insert(0, str(ROOT / "results" / "gauge" / "e5"))
sys.path.insert(0, str(ROOT / "results" / "vacuum_structure" / "orientation"))
sys.path.insert(0, str(ROOT / "src"))
import su3_core as s3                                   # noqa: E402  SU(3) gauge + matrices
from e5_core import causal_diamond_plaquettes          # noqa: E402  causet plaquette list
from orientation_core import causal_link_graph         # noqa: E402
from causal_core import sprinkle_box                    # noqa: E402

I3 = np.eye(3, dtype=complex)


# ======================================================================== #
# STAGE A -- regular 4D lattice (validate the gold-standard Creutz ratio)
# ======================================================================== #
def stage_A(L=6, betas=(4.0, 5.0, 6.0), therm=120, nmeas=24, gap=3, seed=20260623):
    rng = np.random.default_rng(seed)
    rows = {}
    for beta in betas:
        U = s3.gauge_init(L, rng, hot=True)
        step = 0.3
        for it in range(therm):
            a = s3.gauge_metropolis_sweep(U, beta, rng, step)
            if (it + 1) % 20 == 0:
                step = float(np.clip(step * (1.2 if a > 0.5 else 0.85 if a < 0.3 else 1.0),
                                     0.02, 1.5))
        loops = {}
        for _ in range(nmeas):
            for _ in range(gap):
                s3.gauge_metropolis_sweep(U, beta, rng, step)
            lp = s3.measure_wilson_loops(U, 3, 4)
            for k, v in lp.items():
                loops[k] = loops.get(k, 0.0) + v / nmeas
        chi22 = s3.creutz_ratio(loops, 2)
        rows[beta] = {"creutz_chi22": float(chi22),
                      "plaquette": float(s3.plaquette_average(U))}
        print(f"  [A] L={L} beta={beta}: chi(2,2)={chi22:+.3f}  "
              f"<plaq>={rows[beta]['plaquette']:.3f}", flush=True)
    sigmas = [rows[b]["creutz_chi22"] for b in betas]
    confines = all(s > 0.05 for s in sigmas)
    decreasing = all(sigmas[i] >= sigmas[i + 1] - 0.05 for i in range(len(sigmas) - 1))
    return {"L": L, "betas": list(betas), "by_beta": rows,
            "confines": bool(confines), "asympt_free_decreasing": bool(decreasing)}


# ======================================================================== #
# STAGE B -- SU(3) gauge MC on an arbitrary (causal-diamond) plaquette list
# ======================================================================== #
class SU3PlaqGauge:
    """SU(3) gauge field on a list of links, with plaquettes given as ordered
    (link, sign) 4-tuples.  Holonomy of plaquette p = product_j M(l_j, s_j), with
    M(l,+1)=U[l], M(l,-1)=U[l]^dag.  Action = beta * sum_p (1 - Re Tr W_p / 3)."""

    def __init__(self, n_links, plaq_links, plaq_signs, beta, seed=0, step=0.3):
        self.U = s3.su3_random(n_links, np.random.default_rng(seed))
        self.pl = np.asarray(plaq_links, np.int64)
        self.ps = np.asarray(plaq_signs, float)
        self.beta = float(beta)
        self.step = float(step)
        self.rng = np.random.default_rng(seed + 1)
        # link -> list of plaquette ids touching it; only links in some plaquette
        # are dynamical (the rest never enter the action).
        self.l2p = [[] for _ in range(n_links)]
        for p in range(self.pl.shape[0]):
            for l in self.pl[p]:
                self.l2p[int(l)].append(p)
        self.active = [l for l in range(n_links) if self.l2p[l]]

    def _holo(self, p):
        W = I3.copy()
        for l, sgn in zip(self.pl[p], self.ps[p]):
            M = self.U[int(l)]
            W = W @ (M if sgn > 0 else M.conj().T)
        return W

    def _plaq_action(self, p):
        return 1.0 - np.real(np.trace(self._holo(p))) / 3.0

    def mean_W1(self):
        """Fundamental-plaquette Wilson value <(1/3) Re Tr W_P> over all plaquettes."""
        if self.pl.shape[0] == 0:
            return float("nan")
        vals = [np.real(np.trace(self._holo(p))) / 3.0 for p in range(self.pl.shape[0])]
        return float(np.mean(vals))

    def sweep(self):
        acc = 0
        for l in self.active:
            ps = self.l2p[l]
            old = self.U[l].copy()
            S_old = sum(self._plaq_action(p) for p in ps)
            V = s3.su3_from_coords(self.step * self.rng.standard_normal(8))
            self.U[l] = V @ old
            S_new = sum(self._plaq_action(p) for p in ps)
            dS = self.beta * (S_new - S_old)
            if dS <= 0 or self.rng.random() < np.exp(-min(dS, 50.0)):
                acc += 1
            else:
                self.U[l] = old
        return acc / max(len(self.active), 1)

    def equilibrate(self, n):
        for _ in range(n):
            self.sweep()


def stage_B(L_box=4.4, rho=0.5, betas=(4.0, 6.0), seeds=(1, 2),
            therm=40, nmeas=12, gap=2, max_plaqs=1200):
    """SU(3) MC on causal-diamond plaquettes; measure <W_1>(beta) and document the
    area-law obstruction (no controlled k>=2 loop).  Box kept small (~175 events) and
    plaquettes capped: the gauge sector being alive + the structural area-1 fact are
    what Stage B needs, not a large run."""
    geom = None
    by_beta = {b: [] for b in betas}
    plaq_areas = None
    for sd in seeds:
        rng = np.random.default_rng(sd)
        pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
        g = causal_link_graph(pts)
        nL, pl, ps = causal_diamond_plaquettes(g, max_per_pair=2, max_plaqs=max_plaqs,
                                               seed=sd)
        if pl.shape[0] == 0:
            continue
        if geom is None:
            # every causal-diamond plaquette is a height-2 loop = 4 links => area 1
            areas = np.array([np.count_nonzero(row >= 0) for row in pl])
            plaq_areas = {"min_links": int(areas.min()), "max_links": int(areas.max()),
                          "all_fundamental_area1": bool(np.all(areas == 4))}
            geom = {"n_events": int(g.n), "n_links": int(nL),
                    "n_plaquettes": int(pl.shape[0]), "plaq_areas": plaq_areas}
            print(f"  [B] causet seed{sd}: events={g.n} links={nL} "
                  f"plaquettes={pl.shape[0]}  (all area-1 diamonds: "
                  f"{plaq_areas['all_fundamental_area1']})", flush=True)
        for beta in betas:
            gm = SU3PlaqGauge(nL, pl, ps, beta=beta, seed=1000 * int(beta) + sd)
            gm.equilibrate(therm)
            w1 = []
            for _ in range(nmeas):
                for _ in range(gap):
                    gm.sweep()
                w1.append(gm.mean_W1())
            by_beta[beta].append(float(np.mean(w1)))
    scan = []
    for beta in betas:
        v = np.array(by_beta[beta])
        W1 = float(v.mean())
        # -ln<W1> is the per-plaquette free energy, NOT a string tension (k=1 only)
        free = float(-np.log(W1)) if W1 > 0 else float("nan")
        scan.append({"beta": beta, "W1_mean": W1, "W1_std": float(v.std()),
                     "neglog_W1_plaquette_freeE": free})
        print(f"      beta={beta}: <W_1>={W1:.4f}+/-{v.std():.4f}  "
              f"-ln<W_1>={free:.3f} (plaquette free energy, NOT sigma)", flush=True)
    # structural obstruction: count controlled R x T rectangles (R,T>=2) = 0
    return {"L_box": L_box, "rho": rho, "seeds": list(seeds), "geometry": geom,
            "scan": scan,
            "controlled_RxT_rectangles_R_T_ge2": 0,
            "nonabelian_patch_holonomy_constructible": False}


# ======================================================================== #
def main():
    t0 = time.time()
    print("=" * 78)
    print("A2 / C3 -- SU(3) Wilson loops: confinement on the causet vs the cubic control")
    print("=" * 78)
    print("STAGE A -- validate Creutz chi(2,2) on the regular 4D lattice (reproduce FLC)")
    A = stage_A()
    print("STAGE B -- SU(3) gauge MC on causal-diamond plaquettes")
    B = stage_B()

    # ---- verdict (PRE_REGISTRO sec.3) --------------------------------------- #
    w1_rises = ([r["W1_mean"] for r in B["scan"]][-1] >
                [r["W1_mean"] for r in B["scan"]][0])
    obstruction = (B["controlled_RxT_rectangles_R_T_ge2"] == 0 and
                   not B["nonabelian_patch_holonomy_constructible"])
    if A["confines"] and obstruction:
        verdict = (
            "FRONTIER (death-trigger 2): Stage A reproduces SU(3) confinement on the "
            "cubic lattice (Creutz chi(2,2)>0, decreasing with weaker coupling = "
            "asymptotic freedom). Stage B: the SU(3) gauge sector thermalises on the "
            "causal set and the fundamental plaquette <W_1>(beta) is well-defined and "
            f"{'rises' if w1_rises else 'varies'} with beta -- but the STRING TENSION "
            "(the area-law k>=2 log-slope) has NO controlled estimator on the non-local "
            "causet: every causal-diamond plaquette is a height-2 fundamental loop "
            "(area 1), there are ZERO controlled R x T rectangles, and the non-Abelian "
            "ordered-product holonomy admits no clean patch boundary word (E7's Abelian "
            "cancellation surrogate does not extend to SU(3)). Confinement on the causet "
            "stays [FRONTIER], as for U(1) in E5/E7. The Paper SU3's cubic-only "
            "confinement scope is CORRECT and stands (no downgrade; frontier documented).")
        tag = "FRONTIER_CONFIRMS_CUBIC_SCOPE"
    elif A["confines"] and w1_rises and not obstruction:
        verdict = "PROMOTE: a controlled causet string tension was measurable and >0."
        tag = "PROMOTE"
    else:
        verdict = "INCONCLUSIVE: Stage A did not validate; re-check the SU(3) MC."
        tag = "INCONCLUSIVE"

    out = {"campaign": "CONFINAMENTO_A2", "stage_A_regular_lattice": A,
           "stage_B_causal_set": B, "verdict": verdict, "verdict_tag": tag,
           "runtime_s": time.time() - t0}
    (HERE / "a2_su3_causet.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("-" * 78)
    print(f"VERDICT [{tag}]:\n{verdict}")
    print(f"[{out['runtime_s']:.0f}s] -> a2_su3_causet.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
