"""E6_3_bd_lorentzian.py -- gate H1 + H2 of the BD-gauge LORENTZIAN operator.

Pre-registered in E6_BD_GAUGE.md / E6_BD_GAUGE_LORENTZIAN. Builds the indefinite
(E^2-B^2) gauge operator M_L = B^T diag(w) B on causal-diamond plaquettes (e6_bd_core),
with w_P the Minkowski signature of each plaquette's area bivector (B-type +, E-type -).

Stages:
  STAGE 0 (mandatory validation): the SAME operator+symbol machinery on an OPEN regular
    4D lattice, where free Maxwell (omega=ck) is the known answer. The E/B split is exact
    there (axis-plane plaquettes). If the method does not recover ck on the lattice, no
    causal-set reading is trustworthy -- this isolates any causal-set failure as
    non-locality rather than a bug in the construction.
  H1 (causal sprinkling): gauge invariance of M_L to < 1e-10 (theta -> theta + G lam).
  H2 (causal sprinkling): the symbol lambda(k,omega)=<theta,M_L theta>/<theta,theta> for
    transverse plane-wave 1-forms; an INDEFINITE operator has a ZERO CROSSING (B^2=E^2),
    not a minimum -- we test whether the crossing follows omega=ck (c not inserted).
    The Euclidean naive action (mode='euclid', = E6-2) is run as the contrast control.

Central diagnostic figure: lambda(k,omega) for lattice (validation) and causal set.
c is the FITTED slope of the zero-crossing locus -- never inserted.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
E5 = HERE.parent / "e5"
ORI = HERE.parents[1] / "vacuum_structure" / "orientation"
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(E5)); sys.path.insert(0, str(ORI))
from e5_core import causal_diamond_plaquettes              # noqa: E402
from orientation_core import causal_link_graph             # noqa: E402
ROOT = HERE.parents[2]; sys.path.insert(0, str(ROOT / "src"))
from causal_core import sprinkle_box                       # noqa: E402
from e6_bd_core import (                                   # noqa: E402
    build_incidence, build_operator, plaquette_vertices, plaquette_bivectors,
    lorentzian_weights, transverse_pols, plane_wave_theta, zero_crossing)


# ====================================================================== #
# Open regular 4D lattice (validation substrate; time = axis 0)
# ====================================================================== #
def build_open_lattice(shape):
    shape = tuple(int(s) for s in shape); d = len(shape)
    coords = np.array(np.unravel_index(np.arange(int(np.prod(shape))), shape)).T
    pts = coords.astype(float)                              # (N,d), time = col 0
    nid = {tuple(c): i for i, c in enumerate(coords)}
    emap = {}; edges = []
    for i, c in enumerate(coords):
        for mu in range(d):
            cn = c.copy(); cn[mu] += 1
            if cn[mu] < shape[mu]:
                j = nid[tuple(cn)]
                lo, hi = (i, j) if i < j else (j, i)
                if (lo, hi) not in emap:
                    emap[(lo, hi)] = len(edges); edges.append((lo, hi))
    edges = np.array(edges, dtype=np.int64)

    def lid(u, v):
        return emap[(min(u, v), max(u, v))]
    plinks, psigns = [], []
    for i, c in enumerate(coords):
        for mu in range(d):
            for nu in range(mu + 1, d):
                cm = c.copy(); cm[mu] += 1
                cn = c.copy(); cn[nu] += 1
                cmn = c.copy(); cmn[mu] += 1; cmn[nu] += 1
                if cm[mu] >= shape[mu] or cn[nu] >= shape[nu]:
                    continue
                v0 = i; v1 = nid[tuple(cm)]; v2 = nid[tuple(cmn)]; v3 = nid[tuple(cn)]
                loop = [(v0, v1), (v1, v2), (v2, v3), (v3, v0)]
                plinks.append([lid(u, v) for (u, v) in loop])
                psigns.append([1.0 if u < v else -1.0 for (u, v) in loop])
    return pts, edges, np.array(plinks, np.int64), np.array(psigns, float)


# ====================================================================== #
# Symbol grid lambda(k,omega) via plaquette holonomies (no dense M needed)
# ====================================================================== #
def holonomies(plaq_links, plaq_signs, theta):
    return (plaq_signs * theta[plaq_links]).sum(axis=1)


def symbol_grid(edges, pts, plaq_links, plaq_signs, w, kmags, dirs, omegas):
    nk, nw = len(kmags), len(omegas)
    grid = np.zeros((nk, nw))
    for ik, km in enumerate(kmags):
        acc = np.zeros(nw); cnt = 0
        for dvec in dirs:
            kvec = km * dvec
            for eps in transverse_pols(dvec):
                for iw, om in enumerate(omegas):
                    th = plane_wave_theta(edges, pts, kvec, om, eps)
                    den = float(th @ th)
                    if den <= 1e-12:
                        continue
                    f = holonomies(plaq_links, plaq_signs, th)
                    acc[iw] += float(np.sum(w * f * f) / den)
                cnt += 1
        grid[ik] = acc / max(cnt, 1)
    cross = np.array([zero_crossing(omegas, grid[ik]) for ik in range(nk)])
    return grid, cross


def fit_c(kmags, cross):
    m = np.isfinite(cross)
    if m.sum() < 2:
        return np.nan, np.nan, int(m.sum())
    k = np.asarray(kmags)[m]; o = cross[m]
    c = float(np.sum(k * o) / np.sum(k * k))
    dev = float(np.sqrt(np.mean((o - c * k) ** 2)) / (np.sqrt(np.mean(o ** 2)) + 1e-12))
    return c, dev, int(m.sum())


# ====================================================================== #
def main():
    t0 = time.time()
    out = {}

    # ---------------- STAGE 0: regular-lattice validation ---------------- #
    pts_L, edges_L, pl_L, ps_L = build_open_lattice((8, 8, 8, 8))
    verts_L = plaquette_vertices(edges_L, pl_L, ps_L)
    _, e2_L, b2_L = plaquette_bivectors(pts_L, verts_L)
    w_L = lorentzian_weights(e2_L, b2_L, mode="sharp")     # exact on axis planes
    n_elec = int(np.sum(w_L < 0)); n_mag = int(np.sum(w_L > 0))
    # E/B classification sanity: electric planes (time involved) -> e2>0,b2=0
    cls_ok = bool(np.all((e2_L > 0) ^ (b2_L > 0)))         # each plaq purely E or B

    kmin_L = 2 * np.pi / 8
    kmags_L = np.linspace(kmin_L, 3.0 * kmin_L, 7)
    dirs = [np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), np.array([0, 0, 1.0]),
            np.array([1, 1, 0]) / np.sqrt(2)]
    omegas_L = np.linspace(0.0, 1.6 * np.pi, 60)
    grid_L, cross_L = symbol_grid(edges_L, pts_L, pl_L, ps_L, w_L, kmags_L, dirs, omegas_L)
    cL, devL, nL = fit_c(kmags_L, cross_L)
    stage0_pass = bool(np.isfinite(cL) and 0.7 < cL < 1.4 and devL < 0.25 and cls_ok)
    out["stage0_lattice"] = {
        "shape": [8, 8, 8, 8], "n_plaq": int(pl_L.shape[0]),
        "n_electric": n_elec, "n_magnetic": n_mag, "EB_split_clean": cls_ok,
        "kmags": kmags_L.tolist(), "zero_crossing": cross_L.tolist(),
        "c_fit": cL, "rel_dev": devL, "n_crossings": nL, "pass": stage0_pass}

    # ---------------- causal sprinkling (same as E6-1/E6-2) ---------------- #
    rho, L_box = 0.5, 4.6
    rng = np.random.default_rng(1)
    pts = sprinkle_box(rho, [(0.0, L_box)] * 4, rng)
    g = causal_link_graph(pts)
    edges = g.edges
    _, pl, ps = causal_diamond_plaquettes(g, max_per_pair=3, seed=1)
    N = g.n; L = edges.shape[0]; P = pl.shape[0]

    # E/B population of the causal diamonds (physically central: is there magnetic content?)
    verts = plaquette_vertices(edges, pl, ps)
    _, e2c, b2c = plaquette_bivectors(pts, verts)
    w_norm = lorentzian_weights(e2c, b2c, mode="norm")
    w_sharp = lorentzian_weights(e2c, b2c, mode="sharp")
    frac_E = float(np.mean(b2c < e2c)); frac_B = float(np.mean(b2c > e2c))
    mean_wn = float(np.mean(w_norm))

    # ---------------- H1: gauge invariance of M_L (< 1e-10) ---------------- #
    M_L, B, G, _, _, _ = build_operator(edges, pl, ps, pts, N, mode="norm")
    rng2 = np.random.default_rng(7)
    h1 = []
    for _ in range(5):
        lam = rng2.standard_normal(N)
        r = M_L @ (G @ lam)
        h1.append(float(np.max(np.abs(r))))
    # normalise by operator scale so the threshold is meaningful
    scale = float(np.max(np.abs(M_L))) + 1e-30
    h1_max = max(h1); h1_rel = h1_max / scale
    H1_pass = h1_rel < 1e-10
    out["H1"] = {"BG_check_maxabs": float(np.max(np.abs(B @ G))),
                 "M_gauge_maxabs": h1_max, "operator_scale": scale,
                 "M_gauge_relative": h1_rel, "pass": bool(H1_pass)}

    # ---------------- H2: symbol zero crossing vs omega=ck ---------------- #
    kmin = 2 * np.pi / L_box
    kmags = np.linspace(kmin, 3.0 * kmin, 6)
    omegas = np.linspace(0.0, 3.5 * kmags[-1], 70)
    grids, crossings, cfits = {}, {}, {}
    for mode, w in [("norm", w_norm), ("sharp", w_sharp),
                    ("euclid", np.ones(P))]:
        gmode, cr = symbol_grid(edges, pts, pl, ps, w, kmags, dirs, omegas)
        c, dev, nc = fit_c(kmags, cr)
        grids[mode] = gmode; crossings[mode] = cr; cfits[mode] = (c, dev, nc)

    c_n, dev_n, nc_n = cfits["norm"]
    # H2 PASS: indefinite operator crosses zero along omega=ck, c~1, most k crossing
    H2_pass = bool(np.isfinite(c_n) and 0.7 < c_n < 1.4 and dev_n < 0.25
                   and nc_n >= max(2, len(kmags) - 1))
    # contrast: does the Euclidean control fail to cross (stays one sign)?
    eu_no_cross = bool(np.sum(np.isfinite(crossings["euclid"])) < 2)

    out["H2"] = {
        "kmags": kmags.tolist(),
        "frac_E_type": frac_E, "frac_B_type": frac_B, "mean_w_norm": mean_wn,
        "norm":   {"c_fit": c_n, "rel_dev": dev_n, "n_cross": nc_n,
                   "zero_crossing": crossings["norm"].tolist()},
        "sharp":  {"c_fit": cfits["sharp"][0], "rel_dev": cfits["sharp"][1],
                   "n_cross": cfits["sharp"][2],
                   "zero_crossing": crossings["sharp"].tolist()},
        "euclid": {"zero_crossing": crossings["euclid"].tolist(),
                   "no_crossing": eu_no_cross},
        "pass": H2_pass}

    # ---------------- verdict ---------------- #
    if not stage0_pass:
        tag = "STAGE0_FAIL"
        verdict = (f"STAGE 0 (lattice validation) FAILED: the operator+symbol method did "
                   f"NOT recover omega=ck on a regular 4D lattice (c={cL}, dev={devL}, "
                   f"EB_clean={cls_ok}). The construction is not validated; no causal-set "
                   f"reading is trustworthy. Fix the operator before any physics claim.")
    elif not H1_pass:
        tag = "H1_FAIL"
        verdict = (f"H1 FAIL: M_L not gauge-invariant (relative {h1_rel:.0e}). Should be "
                   f"automatic (F=d theta); a non-zero value signals a construction bug.")
    elif H2_pass:
        tag = "H2_PHOTON"
        verdict = (f"H1 PASS, STAGE0 PASS (lattice c={cL:.2f}), and H2 PASS: the BD-gauge "
                   f"Lorentzian symbol on the CAUSAL SET crosses zero along omega=ck with "
                   f"c={c_n:.2f} (dev {100*dev_n:.0f}%) -- the indefinite (E^2-B^2) split "
                   f"yields a relativistic dispersion the Euclidean action (E6-2) could "
                   f"not. Proceed to H3 (polarisation).")
    else:
        tag = "H2_FRONTIER"
        verdict = (f"H1 PASS, STAGE0 PASS (lattice c={cL:.2f} validates the method), but "
                   f"H2 does NOT pass on the CAUSAL SET: norm-mode c={c_n} dev={dev_n} "
                   f"crossings={nc_n}/{len(kmags)} (E-type frac={frac_E:.2f}, B-type "
                   f"frac={frac_B:.2f}, mean w={mean_wn:+.2f}). The indefinite signature is "
                   f"correct and gauge-invariant, and works on a manifold lattice, but the "
                   f"causal diamonds do not furnish the balanced E/B bivector content the "
                   f"Lorentzian cancellation needs -- the E5/E6-1 non-locality persists. "
                   f"FRONTIER (technical): signature solved, non-locality not.")
    out["verdict"] = verdict; out["verdict_tag"] = tag
    out["config"] = {"rho": rho, "L_box": L_box, "N": N, "L": L, "P": P}
    out["runtime_s"] = time.time() - t0

    (HERE / "E6_3_bd_lorentzian.json").write_text(json.dumps(out, indent=2))

    # ---------------- central diagnostic figure: lambda(k,omega) ---------------- #
    make_figure(kmags_L, omegas_L, grid_L, cross_L, cL,
                kmags, omegas, grids["norm"], crossings["norm"], c_n,
                grids["euclid"], HERE / "E6_3_bd_lorentzian.png")

    print(f"STAGE0 lattice: c={cL:.3f} dev={100*devL:.0f}% EB_clean={cls_ok} "
          f"-> {'PASS' if stage0_pass else 'FAIL'}")
    print(f"causal set: N={N} L={L} P={P}  E-type={frac_E:.2f} B-type={frac_B:.2f} "
          f"mean_w={mean_wn:+.2f}")
    print(f"H1 gauge inv: relative {h1_rel:.1e} -> {'PASS' if H1_pass else 'FAIL'}")
    print(f"H2 norm:  c={c_n} dev={dev_n} crossings={nc_n}/{len(kmags)} -> "
          f"{'PASS' if H2_pass else 'no'}")
    print(f"H2 sharp: c={cfits['sharp'][0]} dev={cfits['sharp'][1]} "
          f"crossings={cfits['sharp'][2]}/{len(kmags)}")
    print(f"H2 euclid (control): no_crossing={eu_no_cross}")
    print("\nVERDICT:", verdict)
    print(f"[{tag}] runtime {out['runtime_s']:.0f}s -> E6_3_bd_lorentzian.json + .png")


def make_figure(kL, oL, gL, crL, cL, kC, oC, gC, crC, cC, gEu, path):
    fig, ax = plt.subplots(1, 3, figsize=(15, 4.6))
    for a, (k, o, g, cr, c, title) in zip(ax, [
            (kL, oL, gL, crL, cL, "STAGE 0: regular 4D lattice (validation)"),
            (kC, oC, gC, crC, cC, "H2: causal set, BD-gauge Lorentzian (norm)"),
            (kC, oC, gEu, None, None, "control: Euclidean action (E6-2)")]):
        vmax = np.nanmax(np.abs(g)) + 1e-12
        im = a.pcolormesh(k, o, g.T, shading="auto", cmap="RdBu_r",
                          vmin=-vmax, vmax=vmax)
        fig.colorbar(im, ax=a, label=r"$\lambda(k,\omega)$")
        kk = np.linspace(k.min(), k.max(), 50)
        a.plot(kk, kk, "k--", lw=1.2, label=r"$\omega=k$")
        if cr is not None:
            mfin = np.isfinite(cr)
            a.plot(np.asarray(k)[mfin], cr[mfin], "go", ms=7,
                   label=f"zero crossing (c={c:.2f})")
        a.set_xlabel("k"); a.set_ylabel(r"$\omega$"); a.set_title(title, fontsize=10)
        a.legend(loc="upper left", fontsize=8); a.set_ylim(o.min(), o.max())
    fig.suptitle(r"BD-gauge Lorentzian symbol $\lambda(k,\omega)$: red>0 (B$^2$>E$^2$), "
                 r"blue<0 (E$^2$>B$^2$); the indefinite operator's zero locus is the "
                 r"light cone", fontsize=10)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(path, dpi=130); plt.close(fig)


if __name__ == "__main__":
    main()
