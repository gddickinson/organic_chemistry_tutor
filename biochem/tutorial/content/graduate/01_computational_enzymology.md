# Computational enzymology

How can we compute, simulate, or predict what an enzyme
does?  The field has matured from cartoon mechanisms to
QM/MM transition-state characterisation good enough to
design rational mutations.

## Levels of theory

The challenge: enzyme reactions involve bond-breaking +
bond-forming (quantum), but happen inside a 5 000-50 000-
atom protein + tens of thousands of solvent molecules
(classical-scale problem).

Treatments at different cost / accuracy:

- **Pure QM** — full ab-initio or DFT.  Gold-standard
  accuracy.  Limit: ≲ 100-200 atoms.  Used for
  active-site-only "cluster" models.
- **Pure MM** (molecular mechanics, force fields) —
  CHARMM / AMBER / OPLS.  Tractable for full proteins +
  solvent + nanoseconds-microseconds of dynamics.  Limit:
  doesn't handle bond breaking.
- **QM/MM** — partition the system: ~ 50-200 atoms in
  the active site treated quantum-mechanically; the rest
  with MM.  The 2013 Nobel Prize in Chemistry to
  **Karplus, Levitt, Warshel** recognised the founding
  of this field.

## Transition-state theory in enzymes

Eyring rate constant: k = (k_B T / h) · exp(-ΔG‡/RT).

A 10× rate enhancement = 5.7 kJ/mol lower ΔG‡.  Most
enzymes accelerate reactions by 10⁶-10¹⁷-fold over the
uncatalysed solution rate ⇒ they cut ΔG‡ by 35-100
kJ/mol.

Where does this come from?  Several decades of debate
have settled on:

1. **Electrostatic preorganisation** (Warshel) — the
   active site provides a pre-built electrostatic
   environment optimised for the TRANSITION STATE
   geometry / charge distribution.  The substrate
   pays no reorganisation cost when traversing the
   reaction.  This is the largest single factor for
   most enzymes.
2. **Substrate desolvation** — moving substrate from
   bulk water into the active site removes water
   reorganisation costs.
3. **Geometric strain + ground-state destabilisation** —
   secondary; classical "Pauling strain" idea is mostly
   discarded for major catalysis.
4. **Covalent intermediates** — in classes like serine
   proteases, the multi-step path lowers each
   individual barrier.
5. **Tunnelling** — relevant for H/D/T transfer in
   alcohol dehydrogenase, dihydrofolate reductase,
   methylamine dehydrogenase.  Klinman + Schwartz +
   Hammes-Schiffer have built rigorous theory.

## QM/MM workflow

Modern QM/MM enzyme simulations follow this rough
pipeline:

1. **Structure preparation** — clean a crystal /
   AlphaFold structure; protonate (PROPKA + manual
   review of catalytic residues); add missing loops;
   parameterise non-standard residues / cofactors /
   substrates.
2. **MM equilibration** — solvate in TIP3P water,
   neutralise, energy-minimise, NVT then NPT
   equilibration to 300 K + 1 atm, 10-100 ns of MD to
   relax.
3. **QM/MM single-point** — define the QM region
   (~ catalytic residues + substrate ± nearest active-
   site waters); pick a QM method (DFT B3LYP / ωB97X-D /
   M06-2X with 6-31G(d) or def2-SVP starting basis).
4. **Reaction coordinate scan** — scan a chosen RC
   (e.g. nucleophile-electrophile distance + leaving-
   group bond), or use **string method** / **NEB**
   (nudged elastic band) for higher dimensions.
5. **TS optimisation** — find first-order saddle on the
   QM/MM PES; verify by frequency analysis (one
   imaginary mode along RC).
6. **Free-energy correction** — umbrella sampling /
   metadynamics / TI on the RC so ΔG‡ is the free-
   energy barrier (not just enthalpy).

Realistic deliverables: ΔG‡ to ± 2-5 kcal/mol, ratios
of competing pathways within a factor of 10-100, KIE
predictions.

## Software ecosystem

- **AMBER** + **GROMACS** + **CHARMM** + **NAMD** — MM
  workhorses.
- **Q-Chem** + **ORCA** + **Gaussian** + **TeraChem** +
  **Psi4** — QM engines.
- **Open-source QM/MM**: chemshell + sander.QMMM +
  pDynamo + ParmEd + multiscale frameworks.
- **PLUMED** — collective-variable + free-energy
  sampling library that plugs into most MD engines.

## Worked examples in the literature

- **Chorismate mutase** — Hammes-Schiffer / Bruice's
  benchmark study; ΔG‡ enzymatic vs aqueous = 11 vs 22
  kcal/mol; the 11-kcal/mol acceleration mostly from
  electrostatic stabilisation of the [3,3] TS dipole.
- **Dihydrofolate reductase (DHFR)** — H-transfer
  tunnelling; Klinman + Hammes-Schiffer KIE temperature
  dependence work.
- **Cytochrome P450 Compound I** — Shaik's group has
  published > 100 papers on the multistate-reactivity
  picture of CYP-catalysed C-H hydroxylation.
- **HIV protease inhibitors** — QM/MM TS analogues
  drove early structure-based design (Wlodawer +
  collaborators).
- **Enzyme design** — Baker lab's Kemp eliminase + Diels-
  Alderase + retro-aldolase de-novo enzymes used a TS-
  theozyme-then-Rosetta workflow.

## Free-energy methods for substrate / inhibitor binding

Drug discovery now routinely uses physics-based
binding-affinity prediction:

- **Free-energy perturbation (FEP+)** — Schrödinger's
  commercial implementation; ~ 1 kcal/mol RMSE on
  congeneric series.  Used by med-chem teams to rank
  analogues.
- **Thermodynamic integration (TI)** — older method,
  similar physics.
- **Alchemical absolute binding free energies (ABFE)** —
  more demanding but anchor-free.
- **MM-GBSA / MM-PBSA** — fast end-state estimators;
  qualitative ranking only.

## Machine learning enters

The 2020s have seen ML subsume classical physics in
several niches:

- **AlphaFold2 + ESMFold** — protein structure
  prediction at near-experimental accuracy.  Made every
  enzyme structurally tractable for QM/MM seeding.
- **Neural-network potentials** (ANI, MACE, AIMNet,
  Allegro) — QM-accuracy energies + forces at MM cost.
  Enable µs-scale dynamics with bond-breaking / forming
  in some cases.
- **Equivariant graph nets** for binding affinity (DiffDock,
  Boltz, AlphaFold-Multimer) + active-site prediction.
- **Protein language models** (ESM-2 + ESM3) for
  zero-shot variant-effect prediction → guide enzyme
  engineering.

## Limitations + open problems

- QM/MM still treats QM region as a "magic island" with
  link-atom or LSCF boundary-atom artefacts.
- Sampling the right conformational ensemble is hard —
  rare events at second-or-longer timescales remain
  inaccessible to brute-force MD.
- Multi-reference electronic structure (transition
  metals, multi-radical states, π-cation radicals) is
  not well-handled by standard DFT.
- Allosteric coupling + slow-loop motions bridge
  ns-µs-ms timescales we can't fully sample.
- Polarisable + reactive force fields (AMOEBA, ReaxFF,
  MACE) are emerging as next-generation MM but adoption
  lags.

## Try it in the app

- **OrgChem → Tools → Mechanism player** — compare
  textbook arrow-pushing against TS geometry intuition.
- **Window → Biochem Studio → Enzymes** — pick any
  classical enzyme + read its mechanism description as
  a starting point for a QM/MM workflow.
- **OrgChem → Tools → Orbitals (Hückel / W-H)** — see
  how MO theory underlies the simplest QM-level
  reactivity argument.

Next: **Enzyme engineering + directed evolution**.
