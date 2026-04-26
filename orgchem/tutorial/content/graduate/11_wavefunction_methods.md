# Wavefunction methods deeper — beyond Hartree-Fock

The graduate computational-chemistry lesson (10) covered DFT
+ basis sets + when to trust calculations. This lesson goes
deeper into **wavefunction-based methods** — the systematic
ladder from Hartree-Fock to coupled cluster that lets you
*calibrate* your DFT functional choice.

## The Hartree-Fock starting point

HF treats each electron as moving in the *averaged* field
of all other electrons (mean-field approximation). The
total wavefunction is a single Slater determinant.

What HF gets right:

- ~ 99 % of the total energy.
- Decent geometries (often within 0.02 Å + 2°).
- Reasonable dipole moments + charges.

What HF misses: **electron correlation** — the instantaneous
e⁻–e⁻ avoidance not captured by a mean field. The remaining
~ 1 % of energy IS the chemistry (bond breaking, dispersion,
weak interactions).

## Two types of correlation

- **Static (non-dynamical)** — multiple Slater determinants
  contribute roughly equally. Bond dissociation, biradicals,
  metal-O₂ binding need multireference treatment.
- **Dynamical** — the dominant contributor for closed-shell
  systems near equilibrium geometry.

Different methods target each.

## The systematically improvable ladder

### Møller-Plesset perturbation theory (MP2, MP3, MP4)

Add electron correlation as a perturbation on top of HF.

- **MP2**: cheap (N⁵ scaling), recovers ~ 80 % of correlation
  energy. Workhorse for medium molecules. Decent
  thermochemistry.
- **MP4 / MP5**: diminishing returns + occasionally diverges
  for small-gap systems.
- **SCS-MP2** (Grimme spin-component scaling) — re-weights
  same-spin / opposite-spin contributions, much better
  thermochemistry for the same cost as MP2.

### Coupled cluster

Instead of perturbation, exponentiate excitation operators:

```
|ψ_CC⟩ = exp(T) |ψ_HF⟩
```

- **CCSD** — singles + doubles excitations, N⁶ scaling.
- **CCSD(T)** — perturbative triples added. **Gold
  standard** for closed-shell molecules at equilibrium.
  N⁷ scaling — limits to ~ 20 heavy atoms with current
  hardware.
- **CCSDT, CCSDTQ** — full triples, full quadruples.
  Calibration only; ~ 10 heavy atoms.

CCSD(T) at the complete-basis-set limit gives chemical
accuracy (~ 1 kcal/mol thermochemistry, ~ 10 cm⁻¹ frequencies).

### Multireference (for static correlation)

- **CASSCF (Complete Active Space SCF)** — choose an active
  space of "important" orbitals + electrons; do full CI
  within it. Captures static correlation; misses dynamic.
- **CASPT2 / NEVPT2** — perturbative correction on top of
  CASSCF; covers both static + dynamic.
- **MRCI, MRCC** — even more accurate; tiny molecules only.

Use cases: Cr₂ (multiple Cr-Cr bonds), bond dissociation
curves, transition-metal d-d gaps, photochemistry.

## Local + linear-scaling methods

Conventional CC methods scale steeply with system size. The
modern frontier:

- **DLPNO-CCSD(T)** (Neese) — domain-based local pair natural
  orbital approach. ~ N¹·⁵ scaling, same accuracy. Now
  routine on 100-atom systems.
- **MP2-F12 / CCSD(T)-F12** — explicit r₁₂ correlation
  factor accelerates basis-set convergence; chemical
  accuracy at triple-zeta basis instead of quadruple-zeta.
- **Stochastic methods** — FCIQMC (Alavi) does full CI on
  systems too big for deterministic methods.

## Composite methods

Designed packages combining multiple levels:

- **G4, G4(MP2)** (Curtiss et al.) — empirical recipes
  combining several levels for thermochemistry. ~ 1 kcal /
  mol accuracy, much cheaper than CCSD(T)/CBS.
- **CBS-QB3** (Petersson) — similar.
- **W1, W2, W3, W4** (Martin, Karton) — calibration-grade
  thermochemistry; "weak" methods (W4 reaches sub-kJ/mol).
- **HEAT** (Stanton, Gauss) — high-accuracy with
  spin-orbit + relativistic corrections; used to revise
  enthalpies-of-formation in NIST.

## Choosing the right method

| Task | Recommended | Reason |
|------|-------------|--------|
| Geometry of organic molecule | DFT (B3LYP-D3 / ωB97X-D, def2-TZVP) | Cheap, ~ 99 % of true |
| Reaction barrier (organic) | DLPNO-CCSD(T)/cc-pVTZ on DFT geom | Gold standard, affordable |
| Open-shell metal complex | CASSCF/NEVPT2 with active space | Static correlation |
| Vibrational frequencies | CCSD(T)/cc-pVTZ | If feasible; else B3LYP × 0.97 |
| Conformer search | DFT or semiempirical | Sample ensemble first |
| Excited states | TD-DFT with correct functional + EOM-CCSD | Validate against experiment |

## What you still cannot trust

- **Dispersion-only complexes** without a dispersion
  correction (-D3, -D4, VV10).
- **Charge-transfer excited states** in TD-DFT with
  conventional functionals.
- **Bond breaking** with single-reference methods.
- **Heavy-element relativistic effects** without explicit
  ECPs or DKH / X2C scalar relativistic Hamiltonians.

## Try it in the app

- **Reactions tab** → load any reaction → energy profile —
  see how reported Ea / ΔH compare to DFT or CC values.
- **Tools → Spectroscopy…** → predicted IR + NMR shifts are
  empirical; CCSD(T)/CBS frequencies would be the
  reference.
- **Glossary** → search *Coupled cluster*, *Møller-Plesset
  perturbation theory (MP2)*, *Multireference*, *Composite
  method*.

Next: **High-throughput experimentation + automation**.
