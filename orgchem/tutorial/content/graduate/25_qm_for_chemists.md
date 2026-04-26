# Quantum mechanics primer for chemists

You can't avoid quantum mechanics if you want to understand
chemistry. This lesson covers the conceptual core: what
operators, wavefunctions, eigenvalues, and orbital theory
actually mean. Pre-requisite for the wavefunction-methods
lesson.

## The postulates (in chemist-friendly form)

1. **State** of a system is a wavefunction Ψ(r, t) —
   complex-valued, not directly observable. **|Ψ|² is the
   probability density** of finding the system at r.
2. **Observables** correspond to Hermitian operators
   (position x̂, momentum p̂, energy Ĥ).
3. **Measurement** of observable A on state Ψ returns one
   of the eigenvalues of Â; Ψ then collapses to the
   corresponding eigenfunction.
4. **Time evolution** follows the Schrödinger equation:
   ```
   iℏ ∂Ψ/∂t = Ĥ Ψ
   ```
   Equivalent, time-independent: Ĥ Ψ = E Ψ.
5. **Composite systems**: states tensor; identical fermions
   → antisymmetrise (Pauli); identical bosons → symmetrise.

## The hydrogen atom

The exactly solvable starting point. Three quantum numbers
emerge:

- **n** (principal): 1, 2, 3, ... → energy (E ∝ -1/n²).
- **ℓ** (azimuthal): 0, 1, ..., n-1 → angular momentum;
  spectroscopic labels s, p, d, f, g.
- **m_ℓ** (magnetic): -ℓ, -ℓ+1, ..., +ℓ → orbital
  orientation in a magnetic field.
- **m_s** (spin): ±½ → electron spin.

The hydrogen 1s wavefunction:

```
ψ_1s = (1/√π) (1/a₀)^(3/2) exp(-r/a₀)
```

a₀ = Bohr radius (0.529 Å). Sphere; no nodes; max at
nucleus.

The 2p wavefunctions have a node at the nucleus + an
angular dependence (px, py, pz directions).

## Multielectron atoms

The exact wavefunction is intractable. The **orbital
approximation** says treat each electron in an averaged
field of all others (Hartree-Fock):

- Build atomic orbitals (1s, 2s, 2p, 3s, 3p, 3d, ...).
- Fill them following:
  - **Aufbau** (low energy first).
  - **Pauli exclusion** (max 2 electrons per orbital,
    opposite spins).
  - **Hund's rule** (same-spin electrons preferred in
    degenerate orbitals).

This recovers the periodic table. Limitations: HF misses
electron correlation (post-HF methods correct).

## Molecular orbitals

For molecules, build MOs by **linear combination of atomic
orbitals (LCAO)**:

```
ψ_MO = c₁ φ_A + c₂ φ_B + ...
```

The coefficients c_i are found by minimising the energy.
For H₂:

- ψ_+ = (φ_A + φ_B) / √2 — bonding (lower E than free atom).
- ψ_- = (φ_A - φ_B) / √2 — antibonding (higher E).

Bond order = ½ (electrons in bonding − electrons in
antibonding).

## Symmetry + group theory

A molecule's point group (C_s, C_2v, C_3v, D_∞h, T_d,
O_h, I_h) restricts which AOs can mix. Symmetry-adapted
linear combinations (SALCs) of AOs form basis for MOs.

Useful for:

- Predicting MO degeneracy (e.g. benzene: e₁g + e₂u
  patterns).
- Vibrational spectroscopy selection rules.
- Allowed / forbidden electronic transitions (parity rules).
- Crystal-field splitting in transition-metal complexes.

## Frontier molecular orbital (FMO) theory

Fukui's idea (1981 Nobel): chemistry happens between the
HOMO of the donor + LUMO of the acceptor.

- **Soft-soft** interactions (HOMO ≈ LUMO) → covalent,
  orbital-controlled.
- **Hard-hard** (large HOMO-LUMO gap) → electrostatic,
  charge-controlled.

Examples of FMO predictions:

- **Diels-Alder**: HOMO(diene) + LUMO(dienophile) overlap;
  EWG on dienophile lowers LUMO → faster.
- **EAS regioselectivity**: positions where HOMO has large
  coefficient → electrophile attacks there.
- **W-H rules**: orbital symmetries match if (4n+2) π
  electrons (suprafacial / disrotatory).

## Spin + electronic excited states

A molecule with closed-shell singlet ground state (S₀) can
absorb a photon → singlet excited state (S₁). Selection
rules:

- **Δ S = 0** (no spin change at first order; intersystem
  crossing to T₁ is slower).
- **Δ ℓ = ±1** (electric-dipole-allowed transitions).
- **Spatial-symmetry-allowed** (Laporte rule for
  centrosymmetric molecules).

States and processes for photochemistry:

```
S₀ + hν → S₁ → fluorescence (emit photon, return to S₀)
                ↓
                ISC (intersystem crossing) → T₁
                T₁ → phosphorescence (slow emission)
                T₁ → energy transfer (sensitisation)
                T₁ → electron transfer (photoredox)
                T₁ → reactive (Diels-Alder, [2+2]
                     cycloadditions)
```

## Spin-orbit coupling

Mixes singlet + triplet states; small for light atoms (H,
C, N, O — nm to ps ISC), large for heavy atoms (S, Cl, Br,
I, transition metals — fast ISC).

This is why heavy-atom phosphors (Ir(ppy)₃) work well for
photoredox + OLEDs — efficient ISC populates the long-
lived triplet state.

## Tunnelling

Quantum particles can cross potential barriers higher than
their classical energy. Probability:

```
P ∝ exp(-2 ∫ √(2m(V-E))/ℏ dx)
```

Light particles (H, D, e⁻) tunnel orders of magnitude more
than heavy ones. Examples:

- **STM (scanning tunnelling microscopy)** — electron
  tunnels through vacuum gap → measures the local
  density of states.
- **H/D kinetic isotope effect** in enzyme catalysis —
  large KIE (> 6) often indicates tunnelling.
- **NH₃ inversion** — tunnels through pyramidal barrier
  + gives 23 GHz microwave splitting (the maser).

## Practical numerics

For day-to-day calculations:

- **Energy units**: 1 hartree = 27.211 eV = 627.5 kcal/mol
  = 2625 kJ/mol.
- **Length units**: 1 bohr = 0.529 Å.
- **Frequency**: 1 cm⁻¹ = 0.0029979 THz = 0.012 kJ/mol.
- **kT at 298 K** = 0.025 eV = 0.59 kcal/mol = 207 cm⁻¹.

Memorise these so you can convert Eₐ + ΔG + ν between
units.

## Try it in the app

- **Tools → Orbitals (Hückel/W-H)…** → Hückel tab —
  numerical solution for any conjugated π system.
- **Glossary** → search *Wavefunction*, *Schrödinger
  equation*, *HOMO*, *LUMO*, *Frontier molecular orbital*,
  *Spin-orbit coupling*, *Tunnelling*.

Next: **Molecular dynamics simulations**.
