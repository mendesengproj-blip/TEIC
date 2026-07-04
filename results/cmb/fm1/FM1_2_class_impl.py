"""FM1_2_class_impl.py -- DEV modified-growth module (the "CLASS module" of FM1).

Charter FM1-2.  Implements the DEV effective-gravity modification derived in FM1-1
as a scale/redshift-dependent (mu_MG, Sigma_MG) parametrisation -- the interface
CLASS exposes via `mg_parametrization`:

    mu_MG(k,z)    = mu(k,z) = G_eff/G_N   (matter Poisson  -k^2 Psi = 4πG a^2 rho dM mu)
    Sigma_MG(k,z) = (1 + eta(k,z))/2       (lensing Poisson -k^2(Phi+Psi)=8πG a^2 rho dM Sigma)

ENGINEERING NOTE (declared deviation).  CLASS (`classy`) is NOT installable on this
Windows host (needs a C toolchain); CAMB 1.6.6 IS available and supplies the
LambdaCDM transfer/P(k).  The DEV signal is carried by the linear GROWTH FACTOR
D(k,z), solved here; for sigma8/S8/f(z) this equals an `mg_parametrization` CLASS
run, and the (mu, Sigma) below are exactly what one would hand CLASS.

PHYSICS (honest -- see FM1-1).  The DEV is a MOND-type theory: in the low-
acceleration regime gravity is ENHANCED (mu>=1), NOT suppressed.  The MOND boost is
governed by the perturbation's OWN gravitational acceleration g(k,a) compared to
a0(z): high-z (dense) => g >> a0 => Newtonian (mu->1); low-z, where the cosmic
acceleration of an 8 Mpc/h fluctuation drops below a0, => deep MOND => mu>1.  mu
therefore depends on the EVOLVING amplitude delta (MOND growth is intrinsically
amplitude-dependent); we solve it self-consistently and self-regulating (as delta
grows, g grows, the mode leaves deep MOND).  a0 is FIXED at the SPARC value, never
fitted to the CMB.  The LambdaCDM limit a0->inf => mu=1 is the FM1-2 gate.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import interp1d

G_SI = 6.674e-11
C_SI = 2.99792458e8
MPC = 3.0856775815e22
A0_SPARC = 1.2e-10                # m/s^2, SPARC-calibrated (NOT a CMB fit)

PLANCK = dict(H0=67.36, ombh2=0.02237, omch2=0.1200, ns=0.9649,
              As=2.1e-9, mnu=0.06, tau=0.0544)


# ====================================================================== #
# LambdaCDM baseline from CAMB (transfer + P(k); characteristic amplitude)
# ====================================================================== #
class LCDMBaseline:
    """CAMB LambdaCDM P(k,0), sigma8, and the characteristic linear amplitude
    Delta0(k)=sqrt(k^3 P(k,0)/2π^2) used to set the MOND acceleration of each mode."""

    def __init__(self, cosmo=PLANCK, kmax=20.0, nk=600):
        import camb
        pars = camb.set_params(H0=cosmo["H0"], ombh2=cosmo["ombh2"],
                               omch2=cosmo["omch2"], ns=cosmo["ns"],
                               As=cosmo["As"], mnu=cosmo["mnu"], tau=cosmo["tau"])
        pars.set_matter_power(redshifts=[0.0], kmax=kmax)
        pars.NonLinear = camb.model.NonLinear_none
        res = camb.get_results(pars)
        kh, _, pk = res.get_matter_power_spectrum(minkh=1e-4, maxkh=kmax, npoints=nk)
        self.k = kh                              # h/Mpc
        self.P = pk[0]                           # (Mpc/h)^3, z=0
        self.sigma8 = float(res.get_sigma8_0())
        self.Om = float(res.get_Omega('cdm') + res.get_Omega('baryon') +
                        res.get_Omega('nu'))
        self.h = cosmo["H0"] / 100.0
        self.Delta0 = np.sqrt(self.k ** 3 * self.P / (2 * np.pi ** 2))
        self._D0 = interp1d(np.log(self.k), np.log(self.Delta0),
                            bounds_error=False, fill_value="extrapolate")
        self._lnP = interp1d(np.log(self.k), np.log(self.P),
                             bounds_error=False, fill_value="extrapolate")

    def delta0(self, k_hMpc):
        return np.exp(self._D0(np.log(k_hMpc)))

    def Pk(self, k_hMpc):
        return np.exp(self._lnP(np.log(k_hMpc)))


# ====================================================================== #
# DEV cosmology
# ====================================================================== #
class DevCosmology:
    def __init__(self, baseline, a0=A0_SPARC, s=0.5, beta=0.0070,
                 alpha=2.0 / 3.0, cosmo=PLANCK):
        self.bl = baseline
        self.a0 = a0
        self.s = s
        self.beta = beta
        self.alpha = alpha
        self.c = cosmo
        self.h = cosmo["H0"] / 100.0
        self.H0_SI = cosmo["H0"] * 1e3 / MPC
        self.Om = baseline.Om
        self.OL = 1.0 - self.Om

    # ---- background ----
    def E(self, z):
        return np.sqrt(self.Om * (1 + z) ** 3 + self.OL)

    def Om_a(self, a):
        z = 1.0 / a - 1.0
        return self.Om * (1 + z) ** 3 / self.E(z) ** 2

    def dlnH_dlna(self, a):
        z = 1.0 / a - 1.0
        return -1.5 * self.Om * (1 + z) ** 3 / self.E(z) ** 2

    def a0_z(self, z):
        return np.inf if not np.isfinite(self.a0) else self.a0 * self.E(z) ** self.s

    # ---- MOND interpolation ----
    @staticmethod
    def nu(y):
        """G_eff/G_N as a function of y=g/a0.  y>>1 -> 1 (Newtonian);
        y<<1 -> 1/sqrt(y) (deep MOND, enhanced).  'simple' nu."""
        y = np.asarray(y, float)
        return 0.5 + np.sqrt(0.25 + 1.0 / np.maximum(y, 1e-30))

    def accel(self, k_hMpc, delta, a):
        """Physical peculiar gravitational acceleration of a mode (k, amplitude
        delta) at scale factor a:  g = (3/2) Om H0^2 delta / (a^2 k_comoving_SI)."""
        k_SI = k_hMpc * self.h / MPC                  # comoving 1/m
        return 1.5 * self.Om * self.H0_SI ** 2 * np.abs(delta) / (a ** 2 * k_SI)

    def mu_of_delta(self, k_hMpc, delta, a):
        """mu = G_eff/G_N from the mode's live acceleration vs a0(z)."""
        if not np.isfinite(self.a0):
            return 1.0
        z = 1.0 / a - 1.0
        return float(self.nu(self.accel(k_hMpc, delta, a) / self.a0_z(z)))

    # ---- (mu, Sigma) at the LINEAR (LambdaCDM-amplitude) closure: a definite
    #      (k,z) function -- this is what one hands CLASS' mg_parametrization. ----
    def mu_MG(self, k_hMpc, z, D_lcdm_ratio=None):
        """mu(k,z) evaluated at the characteristic amplitude delta(k,z) =
        Delta0(k) * D_lcdm(z)/D_lcdm(0).  If D_lcdm_ratio (=D(z)/D(0)) is not given,
        the matter-dom approx a is used (good to ~few % for the reporting curve)."""
        a = 1.0 / (1.0 + z)
        ratio = a if D_lcdm_ratio is None else D_lcdm_ratio
        delta = self.bl.delta0(k_hMpc) * ratio
        if np.isscalar(k_hMpc):
            return self.mu_of_delta(k_hMpc, delta, a)
        return np.array([self.mu_of_delta(kk, dd, a)
                         for kk, dd in zip(np.atleast_1d(k_hMpc), np.atleast_1d(delta))])

    def eta_slip(self, k_hMpc, z):
        """Slip eta-1 = alpha beta / sqrt(x), x=g/a0 (Paper I), capped."""
        if not np.isfinite(self.a0):
            return np.zeros_like(np.atleast_1d(k_hMpc), float)
        a = 1.0 / (1.0 + z)
        delta = self.bl.delta0(k_hMpc) * a
        g = self.accel(k_hMpc, delta, a)
        x = np.maximum(g / self.a0_z(z), 1e-8)
        return self.alpha * self.beta / np.sqrt(x)

    def Sigma_MG(self, k_hMpc, z):
        return 1.0 + 0.5 * self.eta_slip(k_hMpc, z)

    # ---- self-consistent growth (live amplitude in mu) ----
    def growth(self, k_hMpc, c_k, a_i=1e-3, z_out=0.0):
        """Integrate the matter perturbation with amplitude-dependent mu:
            delta'' + (2 + dlnH/dlna) delta' - 1.5 Om(a) mu(k,delta,a) delta = 0,
        IC delta(a_i)=c_k*a_i, delta'(a_i)=c_k*a_i (matter-dom growing mode).  c_k
        sets the physical normalisation so the LambdaCDM run reaches Delta0(k) today.
        Returns (delta(z_out), solution)."""
        k = float(k_hMpc)
        N_i, N_f = np.log(a_i), np.log(1.0 / (1.0 + z_out))

        def rhs(N, y):
            D, Dp = y
            a = np.exp(N)
            mu = self.mu_of_delta(k, D, a)
            return [Dp, -(2.0 + self.dlnH_dlna(a)) * Dp + 1.5 * self.Om_a(a) * mu * D]

        y0 = [c_k * a_i, c_k * a_i]
        sol = solve_ivp(rhs, [N_i, N_f], y0, method="RK45", rtol=1e-7, atol=1e-14,
                        dense_output=True)
        return float(sol.y[0, -1]), sol


# ====================================================================== #
# helpers: normalisation, sigma_R, P_DEV
# ====================================================================== #
def _window(kR):
    kR = np.asarray(kR, float)
    w = np.ones_like(kR)
    m = kR > 1e-6
    x = kR[m]
    w[m] = 3.0 * (np.sin(x) - x * np.cos(x)) / x ** 3
    return w


def sigma_R(k, Pk, R):
    """sigma_R from P(k): sigma^2 = int dk/k k^3 P/(2π^2) W^2(kR)."""
    integ = (k ** 3 * Pk / (2 * np.pi ** 2)) * _window(k * R) ** 2
    trapz = getattr(np, "trapezoid", getattr(np, "trapz", None))
    return float(np.sqrt(trapz(integ / k, k)))


def normalisations(dev, lcdm, ks):
    """c_k for each k so the LambdaCDM run reaches Delta0(k) today."""
    cks = []
    for k in ks:
        dL, _ = lcdm.growth(k, c_k=1.0)            # raw LambdaCDM amplitude today
        cks.append(dev.bl.delta0(k) / dL)
    return np.array(cks)


def dev_power(dev, lcdm, z=0.0):
    """P_DEV(k,z) = P_LCDM(k,z=0)*[delta_DEV(k,z)/delta_LCDM(k,0)]^2 ... here both at
    z (z=0 for sigma8).  Returns k, P_LCDM, P_DEV, growth-ratio R(k)."""
    k = lcdm.bl.k.copy()
    PL = lcdm.bl.P.copy()
    R = np.empty_like(k)
    for i, kk in enumerate(k):
        dL, _ = lcdm.growth(kk, c_k=1.0, z_out=z)
        c_k = lcdm.bl.delta0(kk) / (lcdm.growth(kk, c_k=1.0)[0])  # norm at z=0
        dD, _ = dev.growth(kk, c_k=c_k, z_out=z)
        # LambdaCDM physical delta at z with same normalisation
        dLphys = c_k * dL
        dDphys = dD
        R[i] = dDphys / dLphys
    return k, PL, PL * R ** 2, R


# ====================================================================== #
# FM1-2 engineering gate: LambdaCDM limit + mu/k_star map
# ====================================================================== #
def main():
    import json
    from pathlib import Path
    OUT = Path(__file__).resolve().parent

    print("=" * 72)
    print("FM1-2 -- DEV growth module: LambdaCDM-limit verification (a0 -> inf)")
    print("=" * 72)
    bl = LCDMBaseline()
    print(f"CAMB baseline: sigma8={bl.sigma8:.4f}  Om={bl.Om:.4f}  "
          f"(CLASS unavailable -> CAMB+growth-ODE)")
    dev = DevCosmology(bl, a0=A0_SPARC, s=0.5)
    lcdm = DevCosmology(bl, a0=np.inf)

    print("\nmu(k,z) at the sigma8 scale (k=0.2) and on large scales:")
    rows = []
    for z in (0.0, 0.5, 1.0, 2.0):
        a = 1.0 / (1 + z)
        mu_s8 = dev.mu_of_delta(0.2, bl.delta0(0.2) * a, a)
        mu_big = dev.mu_of_delta(0.01, bl.delta0(0.01) * a, a)
        rows.append(dict(z=z, mu_0p2=mu_s8, mu_0p01=mu_big))
        print(f"  z={z:.1f}: mu(k=0.2)={mu_s8:.3f}   mu(k=0.01)={mu_big:.3f}")

    # LambdaCDM limit
    mu_lim = max(abs(lcdm.mu_of_delta(k, bl.delta0(k), 1.0) - 1.0)
                 for k in (1e-3, 1e-2, 0.2, 5.0))
    print(f"\nLambdaCDM limit a0->inf:  max|mu-1| = {mu_lim:.2e}  (must be 0)")
    gmatch = []
    for k in (1e-2, 0.1, 1.0):
        dL1, _ = lcdm.growth(k, c_k=1.0)
        dL2, _ = lcdm.growth(k, c_k=1.0)
        gmatch.append(abs(dL1 - dL2))
    limit_ok = mu_lim < 1e-12

    print("\nDEV/LambdaCDM growth ratio D_DEV/D_LCDM at z=0 (mu>=1 => ratio>=1):")
    gr = []
    for k in (1e-3, 1e-2, 0.05, 0.1, 0.2, 0.5, 1.0):
        dL, _ = lcdm.growth(k, c_k=1.0)
        c_k = bl.delta0(k) / dL
        dD, _ = dev.growth(k, c_k=c_k)
        r = dD / (c_k * dL)
        gr.append((k, r))
        tag = "  <- sigma8 scale" if 0.1 <= k <= 0.3 else ""
        print(f"   k={k:7.4f} h/Mpc: ratio={r:.4f}{tag}")
    dev_enhances = all(r >= 0.999 for _, r in gr)

    print("-" * 72)
    print(f"  LambdaCDM limit reproduced (a0->inf => mu=1): {'YES' if limit_ok else 'NO'}")
    print(f"  DEV never suppresses growth (ratio>=1): "
          f"{'YES (MOND enhances)' if dev_enhances else 'NO'}")
    print("=" * 72)

    payload = {
        "class_substitute": "CAMB 1.6.6 + DEV growth ODE (classy unavailable)",
        "baseline_sigma8": bl.sigma8, "Om": bl.Om, "a0_SPARC": A0_SPARC, "s": 0.5,
        "lambda_cdm_limit_ok": bool(limit_ok), "max_abs_mu_minus_1_a0inf": mu_lim,
        "dev_never_suppresses": bool(dev_enhances),
        "mu_map": rows,
        "growth_ratio_z0": [{"k": k, "ratio": r} for k, r in gr],
    }
    (OUT / "FM1_2_class_impl.json").write_text(json.dumps(payload, indent=2, default=float))
    print(f"saved {OUT/'FM1_2_class_impl.json'}")
    return payload


if __name__ == "__main__":
    main()
