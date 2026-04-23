# Molecular-Orbital Theory & Reactivity

An atom has orbitals; a molecule has **molecular orbitals** that span
many atoms. Every organic reaction, at the deepest level, is an
interaction between filled and unfilled MOs. Lewis structures and
arrow-pushing are a convenient shorthand, but when you want to
explain *why* a reaction picks one pathway over another — why
Diels-Alder is thermally allowed but [2+2] isn't, why SN2 happens at
the back face of the LG, why aromatic systems are unusually stable —
you reach for MO theory.

This lesson covers the MO framework at graduate depth, with examples
you can compute live in the app.

## MO from LCAO: the recipe

For a molecule with n atomic orbitals (AOs) that span a common
symmetry / energy range, MO theory says:

1. Build a basis set of n AOs.
2. Combine them linearly: MO_i = Σ c_ij · AO_j.
3. Solve the eigenvalue problem HC = SCε for the coefficients `c_ij`
   and orbital energies `ε_i`.
4. Fill MOs bottom-up according to aufbau + Hund's rule.

For conjugated π systems we can make a drastic simplification: treat
only the p_z orbitals (one per sp² atom), assume every on-diagonal
matrix element = α (Coulomb integral), every nearest-neighbour
off-diagonal = β (resonance integral), and zero elsewhere. This is
**simple Hückel theory**, and it reduces to eigendecomposing the
**adjacency matrix** of the π-atom graph.

The `orgchem.core.huckel` module does exactly this:

```python
from orgchem.core.huckel import huckel_for_smiles
huckel_for_smiles("c1ccccc1")
# ↳ energies = [+2.0, +1.0, +1.0, -1.0, -1.0, -2.0]  (units of β)
```

Call `huckel_mos(smiles=...)` in the tutor — same engine.

## FMO theory: HOMO and LUMO drive reactivity

Fukui (Nobel 1981) reformulated the question "why does this reaction
happen?" as "which MOs overlap to form the new bond?". The answer,
almost always: the **HOMO** (highest-occupied MO) of the nucleophile /
donor and the **LUMO** (lowest-unoccupied MO) of the electrophile /
acceptor.

Two rules flow from that:

1. **Small HOMO-LUMO gap → fast reaction**. Overlap lowers the
   transition-state energy; a smaller gap means more stabilisation.
2. **Phase matching at the reacting atoms matters**. The lobes on the
   two atoms that are about to bond must have the **same phase** (both
   positive, or both negative). Opposite phases give antibonding
   overlap — the reaction is forbidden.

### Worked example 1: Diels-Alder HOMO-LUMO

Run:

```python
butadiene = huckel_for_smiles("C=CC=C")
ethylene  = huckel_for_smiles("C=C")
```

- Butadiene: 4 π electrons, MOs at +1.618, +0.618, −0.618, −1.618 β.
  HOMO is ψ₂ at +0.618 β (two electrons, second-highest bonding).
- Ethylene: 2 π electrons, MOs at +1, −1 β. LUMO is π* at −1 β.

The phases of the butadiene HOMO at atoms 1 and 4 are **opposite**
(node between them). The ethylene LUMO at atoms 1 and 2 is also
**opposite** (node between them). Rotating so the "outer" lobes of
butadiene align with the "outer" lobes of ethylene: bottom-positive
meets top-positive at one end, bottom-negative meets top-negative at
the other. **Good overlap on both sides** — the [4+2] is allowed
thermally.

For [2+2]: the HOMO of ethylene-A and LUMO of ethylene-B would have
to align, but their phases at the reacting atoms are **mismatched**.
Good overlap at one end forces bad overlap at the other. **Forbidden**
thermally.

That's the MO-level explanation for `check_wh_allowed("cycloaddition",
6, "thermal")` returning True and `check_wh_allowed("cycloaddition",
4, "thermal")` returning False.

### Worked example 2: SN2 backside attack

The LUMO of an alkyl halide is the σ* of the C–X bond: a big lobe on
carbon pointing **away** from X. The HOMO of a nucleophile (hydroxide)
is a lone pair. For maximum overlap, the nucleophile hits the carbon
**from the opposite side of X** — backside attack. The resulting
inversion of stereochemistry is a direct consequence of LUMO geometry.

### Worked example 3: regiochemistry of electrophilic aromatic substitution

When nitrobenzene reacts with a second electrophile, the **meta**
position dominates. Why? Look at the LUMO of an ortho/para-attacked
arenium intermediate: the cation is stabilised more at meta (no direct
through-space destabilisation by the adjacent NO₂). Put differently,
the HOMO of nitrobenzene has the biggest coefficient at meta — that's
where a random electrophile finds the most electron density.

Run:

```python
huckel_for_smiles("[O-][N+](=O)c1ccccc1")
```

The MO coefficient pattern at the ortho / meta / para carbons is
the quantitative basis for "meta-directing".

## HOMO / LUMO energies predict specific outcomes

### Hammett plots (Phase 17)

A series of substituted substrates, plotted log(k/k₀) vs Hammett σ,
gives a straight line with slope ρ. The slope's **sign** tells you
whether the rate-determining TS prefers electron-rich or electron-
poor substrates. HOMO / LUMO interpretation:

- ρ > 0: LUMO of substrate is involved in the RDS (substrate is
  electrophile; electron-withdrawers lower LUMO → faster).
- ρ < 0: HOMO of substrate is involved (substrate is nucleophile;
  electron-donors raise HOMO → faster).

### Photochemistry

UV absorption promotes an electron from HOMO to LUMO. The promoted
LUMO has phases that are **opposite** to the former HOMO — that's
why photochemical pericyclic selectivity inverts the thermal rules.
`check_wh_allowed("electrocyclic", 6, "photochemical")` returns
"conrotatory"; the thermal counterpart was "disrotatory".

## Beyond Hückel: ab initio and DFT

Simple Hückel is quantitatively wrong — MO energies don't match
experiment, and 3D geometry effects aren't captured. For **real**
calculations, chemists use:

- **Semi-empirical** (AM1, PM3, PM6, PM7, GFN2-xTB): parameterised
  approximations; seconds per molecule; useful for large systems or
  screening.
- **Hartree-Fock** (HF): mean-field self-consistent MO solution; too
  approximate for bond energies but qualitative shapes are right.
- **Post-HF** (MP2, CCSD(T)): gold standard for small molecules;
  expensive (CCSD(T) scales as N⁷).
- **DFT**: density-functional theory; most popular for medium
  molecules. Functionals (B3LYP, M06-2X, ωB97X-D) trade speed for
  accuracy.

PySCF + Gaussian + Q-Chem + ORCA are the common packages; a future
Phase 14b+ integration will let the tutor run real MO calculations
on a selected molecule (currently deferred — needs optional deps).

## Key MO concepts to command

1. **Symmetry** (σ, π, δ, d-type). Two orbitals only interact if
   they share a symmetry element; otherwise they stay orthogonal.
2. **Nodes**. Higher-energy MOs have more nodes. Rule of thumb:
   for a linear π system of n atoms, ψ_i has (i−1) nodes.
3. **Degeneracy**. Symmetric molecules have degenerate MO pairs
   (benzene's HOMO ψ₂/ψ₃, LUMO ψ₄/ψ₅ at ±1 β). Can be broken by
   substituent.
4. **Frontier orbitals**. Only HOMO/LUMO participate in low-energy
   reactions; deep MOs are thermodynamic ballast.
5. **Koopmans' theorem**. Ionisation potential ≈ −ε(HOMO), electron
   affinity ≈ −ε(LUMO). The *signs* are reliable; absolute values are
   approximate.

## Practice

1. Export MO diagrams for butadiene, hexatriene, benzene, pyrrole,
   Cp⁻ via `export_mo_diagram(smiles=…, path=…)`. Compare the HOMO /
   LUMO gap against UV absorption (benzene 254 nm, larger-gap →
   shorter λ; polyenes red-shift as the chain grows).
2. Ask the tutor: "Use Hückel to predict which regioisomer dominates
   in the nitration of aniline vs nitrobenzene." (Aniline: ortho/para
   dominant, because the NH₂ HOMO puts high coefficient at those
   positions. Nitrobenzene: meta.)
3. Read **wh_rules.py** (`list_wh_rules()`) — every rule in there is a
   corollary of a HOMO-LUMO phase argument.
4. (Optional, deep) Look up the PES (photoelectron spectrum) of
   benzene: the 6 π MO ionisation potentials line up with Hückel
   predictions once you add the Koopmans' correction.

## Further reading

- Fleming, I. *Molecular Orbitals and Organic Chemical Reactions*
  (Student ed., 2009). The textbook.
- Woodward, R. B. & Hoffmann, R. *The Conservation of Orbital
  Symmetry* (1970). Short; historically foundational.
- Albright, Burdett, Whangbo, *Orbital Interactions in Chemistry*
  (2nd ed., 2013). For inorganic + metal fragment MOs.
- Jensen, F. *Introduction to Computational Chemistry* (3rd ed., 2017).
  Bridge to ab initio / DFT.

Next (final graduate lesson): **Case studies in total synthesis** —
apply the whole toolkit (MO, retrosynthesis, asymmetric catalysis,
protecting groups) to Taxol, Vitamin B₁₂, and Strychnine.
