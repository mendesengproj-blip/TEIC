# E4-1 — Polarisation locking: gauge vector vs two scalars (DECISIVE)

> Pre-registered in `E4_PHOTON_DISCRIMINATOR.md` (E4-1). Code: `E4_1_locking.py`
> (reuses `orientation_core.py` unmodified); data: `E4_1_locking.json`. Decides
> whether the two transverse O(3) Goldstone modes are an emergent gauge vector
> (photon) or two decoupled internal scalars. Run jun/2026.

## Method

Ordered state (J=2.0) on the 3+1D causal link graph. Transverse frame (e1,e2) perp
to <n>; transverse components a_1=n.e1, a_2=n.e2. For 32 spatial directions x 5
magnitudes (160 k-vectors) form the 2x2 polarisation tensor
P_ab(k)=<Re_a Re_b + Im_a Im_b>, averaged over 16 seeds x 40 samples. Two nulls:
(i) position-shuffle (isotropic floor for the anisotropy magnitude); (ii) a
permutation null that randomises the khat<->P pairing (confound-free test of
whether the polarisation axis tracks khat -- the actual locking signature).

## Result

```
r(real)    = 0.0615 +/- 0.0294       anisotropy of P_ab(k)
r(shuffle) = 0.0443 +/- 0.0241       position-shuffled isotropic floor
anisotropy excess         = +9.0 sigma   <- real-space field coherence, NOT locking
eigvec-khat circular corr = +0.098
  permutation p-value     = 0.227         <- consistent with random khat<->axis pairing
  significance vs null    = +0.7 sigma
```

The principal polarisation axis does **not** track the spatial wavevector khat: the
eigvec-khat correlation (+0.098) is consistent with random pairing (p=0.23,
+0.7sigma). The anisotropy excess over the position-shuffle baseline (+9sigma) is a
real-space-coherence artefact of that baseline (the ordered field has genuine
spatial coherence the position-shuffle destroys); it is NOT a locking signal, as the
confound-free permutation test makes explicit.

## Verdict

```
PHOTON DIES (two scalars). The two transverse Goldstone modes of the O(3)
orientation ferromagnet are DECOUPLED INTERNAL SCALARS (pion-like: Goldstone bosons
of a broken internal symmetry), NOT a spatial gauge vector A_i locked to k. The
internal index does not lock to the spacetime index -- exactly the symmetry
expectation for a bare sigma model whose global O(3) is decoupled from the spacetime
Lorentz group.
```

## What this settles, and where it points

1. The naive identification "photon = orientation Goldstone magnon" is **falsified
   by measurement**. The modes are scalars.
2. This is internally **consistent** with the SU(3) sector (Paper V), where the
   broken-generator Goldstones are the pseudoscalar meson octet -- i.e. this
   mechanism makes pion-like scalars, not photons.
3. The photon, if it is emergent in this framework, must come from the **gauge-
   connection (link-variable) sector** (a U(1) connection on the Hasse links, where
   the excitation carries a genuine spacetime index and a gauge redundancy), not
   from the orientation Goldstone sector. That is a separate, untested campaign (E5).
4. To make the orientation field itself yield a vector would require an added
   spin-orbit (internal<->spatial) locking term -- an external ingredient, not
   forced by the substrate.

Consequence for the manuscript: the PAPER_PHOTON draft must be reframed from
"emergent photon" to "spontaneous orientational order + a relativistic SCALAR
Goldstone sector", with E4-1 reported as the measurement that excludes the gauge-
vector (photon) identification. E4-0 (long-range order genuine) and the relativistic
dispersion of the causal d'Alembertian remain as supporting results.
