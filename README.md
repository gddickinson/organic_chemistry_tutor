# OrgChem Studio

An interactive PySide6 desktop application for **learning and teaching
organic chemistry**. Built on RDKit + 3Dmol.js + SQLAlchemy/SQLite, with
**415 seeded molecules** in the main database (plus **89 curated
macromolecule entries** across carbohydrates / lipids / nucleic acids),
**35 named reactions**, **20 multi-step mechanisms** (including enzyme
active sites — HIV protease, RNase A, chymotrypsin — plus the canonical
bromonium-ion alkene halogenation + Friedel-Crafts EAS), **25 classical
synthesis pathways**, **15 reaction-coordinate energy profiles**,
**80 glossary terms**, **30 tutorial lessons** across beginner /
intermediate / advanced / graduate tiers, **6 SAR series** for
medicinal-chemistry teaching (NSAIDs, statins, β-blockers, ACE-Is,
SSRIs, β-lactam penicillins), and an integrated **protein / small-
molecule interaction stack** that fetches from RCSB and AlphaFold DB.

Every feature is reachable from the GUI — the audit gate pins
**100 % coverage** (every registered agent action has a corresponding
menu / panel / dialog entry — **127 / 127**). The full regression suite
is **964 tests** green as of round 101 (2026-04-24).

![Main window — molecule workspace](screenshots/tour/01_caffeine.png)

## Feature tour

### Molecule workspace
High-quality RDKit 2D rendering + an interactive 3Dmol.js WebGL
viewer, linked to the database via the left-dock Molecule browser
and the right-dock Properties pane (MW, logP, TPSA, HBD/HBA,
Lipinski violations, QED, rotatable bonds).

![2D viewer](screenshots/tour/05_viewer_2d.png)
![3D viewer](screenshots/tour/06_viewer_3d_3dmol.png)

### Reactions + mechanisms
Reactions tab lists every seeded reaction with the full scheme and
description. Mechanism player steps through curly- and fishhook-arrow
overlays atom-by-atom, with lone-pair dots and bond-midpoint
arrows — used by the seeded HIV-protease and RNase-A enzyme
mechanisms, plus the bromonium-ion and Friedel-Crafts cases.

![Reactions tab](screenshots/tour/10_reactions.png)

Energy-profile diagrams per reaction with Ea / ΔH annotations.
The **15** seeded profiles now span every textbook shape class:

- **Single-TS addition/elimination**: SN2, E2, Diels-Alder.
- **Two-TS ionisation**: SN1, E1 (carbocation well between).
- **Multi-step addition-elimination**: Aldol, Grignard, Wittig,
  Michael.
- **Catalytic cycles**: Sonogashira (OA as RDS), HWE, Mitsunobu.
- **Acyl substitution**: Fischer esterification (thermoneutral
  equilibrium), Claisen condensation (final deprotonation drives
  equilibrium).
- **Electrophilic aromatic substitution**: nitration of benzene
  (canonical σ-complex / Wheland valley shape).

![Energy profile — Diels-Alder](screenshots/tour/energy_diels-alder.png)
![Energy profile — Claisen condensation](screenshots/tour/energy_claisen.png)
![Energy profile — Fischer esterification](screenshots/tour/energy_fischer.png)
![Energy profile — Nitration of benzene (EAS)](screenshots/tour/energy_nitration.png)

### Synthesis pathways
**25** multi-step teaching routes — pharmaceutical (Aspirin,
Paracetamol, BHC Ibuprofen, L-DOPA Knowles Rh-DIPAMP asymmetric,
Procaine, Lidocaine, Benzocaine, Sulfanilamide, Saccharin, Aspartame
Z-peptide), polymer commodity (Nylon-6, Nylon-6,6, Adipic acid
DuPont), bio-organic (Met-enkephalin Fmoc SPPS, Vanillin from
eugenol), and historic (Wöhler urea) — each rendered as a vertical
step scheme with reagents above arrows and conditions / yield below.

![Synthesis tab](screenshots/tour/12_synthesis.png)
![Aspirin pathway (Kolbe-Schmitt)](screenshots/pathway_aspirin_kolbe.png)
![Paracetamol 3-step](screenshots/pathway_paracetamol_3step.png)

### Protein / ligand stack (Phase 24)
Proteins tab fetches from RCSB (cached locally) or AlphaFold DB
(pLDDT colour overlay auto-enabled), then provides:

- Grid-based binding-pocket detector.
- Geometric H-bond / salt-bridge / π-stacking / hydrophobic contact
  analyser (with optional PLIP bridge if installed).
- Protein-protein interface analysis across chain pairs.
- DNA / RNA-ligand contact analyser with intercalation / groove /
  phosphate classification.
- Interactive 3Dmol.js viewer with click-to-inspect (picked residue
  bounces back to Qt via QWebChannel), cartoon / trace / surface
  styles, auto-rotation export, and a 2D PoseView-style interaction
  map exporter.

### Compare
Drop any molecules into slots, get a side-by-side descriptor +
structure comparison. Accepts bare SMILES, molecule names, or
molecule IDs; cross-panel drag-and-drop from the Molecule browser.

![Compare tab](screenshots/tour/11_compare.png)

### Glossary
**80** searchable terms across bonding, stereochem, mechanism,
reactions, synthesis, spectroscopy, lab-technique, enzyme-
mechanism, and medicinal-chemistry categories. Anchor terms ship
with example SMILES rendered on click via the *View figure*
button. Continued-expansion entries (Hammond, Bürgi-Dunitz, KIE,
HOMO/LUMO, pharmacophore, prodrug, J-coupling, Markovnikov,
Saytzeff, Walden inversion, anomer, …) live in
`seed_glossary_extra.py` to keep the main seed module near the
500-line cap.

![Glossary tab](screenshots/tour/13_glossary.png)

### Medicinal chemistry — SAR series
**6** teaching SAR series (Phase 31k — target 15): **NSAIDs** (COX),
**Statins** (HMG-CoA), **β-blockers** (β₁/β₂), **ACE inhibitors**,
**SSRIs** (SERT / NET + chiral-switch case study), **β-lactam
penicillins** (MIC / β-lactamase-stability / oral-bioavailability).
Each variant carries SMILES + activity data + clinical / historical
notes; matrix renderer colour-codes descriptor + activity columns
for side-by-side inspection.

![SSRI SAR matrix](screenshots/tour/sar_ssri.png)
![β-lactam SAR matrix](screenshots/tour/sar_beta_lactams.png)

### Macromolecules window (Phase 30)
All four macromolecule workspaces — **Proteins**, **Carbohydrates**,
**Lipids**, **Nucleic acids** — live in a dedicated top-level
window accessed via *Window → Macromolecules…* (Ctrl+Shift+M) —
the main tabbar stays focused on small-molecule workflows.
Single persistent instance; geometry + last-active tab persist
across sessions.

- **Proteins** — 9 seeded targets (A2A-caffeine, COX-1-ibuprofen,
  HMG-CoA-atorvastatin, HIV protease dimer + ritonavir, insulin
  hexamer, doxorubicin-DNA, lysozyme, myoglobin, GFP) + any PDB
  ID via RCSB + any UniProt via AlphaFold DB.
- **Carbohydrates** — **25** entries: monosaccharides (aldoses /
  ketoses, α/β/open-chain), aminosugars (glucosamine, GlcNAc),
  uronic acid (glucuronic), deoxy sugars (fucose, rhamnose),
  sugar alcohols (sorbitol, mannitol, xylitol), disaccharides
  (sucrose, lactose, maltose, cellobiose, trehalose),
  polysaccharide fragments (amylose, cellulose).
- **Lipids** — **31** entries spanning fatty acids (C8 caprylic →
  C22 DHA, ω-3 / ω-6 / ω-9 tags), eicosanoids (PGE2, TXA2),
  triglycerides, phospholipids (POPC, POPE, phosphatidic acid),
  sphingolipids (ceramide, sphingomyelin), sterols + bile acids
  (cholesterol, ergosterol, cholic, taurocholic), steroid
  hormones (testosterone, estradiol, progesterone, cortisol),
  fat-soluble vitamins (D₃, A retinol, E α-tocopherol).
- **Nucleic acids** — **33** entries: bases (A/G/C/T/U + m6A /
  m5C + hypoxanthine / xanthine), nucleosides (adenosine,
  inosine, pseudouridine Ψ, …), nucleotides (ATP, cAMP, GTP,
  NAD⁺ / NADH / NADPH, FAD, CoA, SAM), oligonucleotides, plus
  canonical PDB motifs (1BNA B-DNA, 1EHZ tRNA-Phe, 143D
  G-quadruplex, 1HMH hammerhead ribozyme). *Fetch PDB*
  button for any PDB-motif entry jumps directly into the
  Proteins inner tab.

### Cross-surface full-text search (Phase 33)
Two complementary search surfaces, sharing one ranking core:

- **Ctrl+F** opens a modal find dialog with live-updating results
  across every seeded row (molecule / reaction / mechanism-step /
  pathway / glossary), filterable by kind.
- **"Full text" checkbox** on the Reactions + Synthesis tab
  filter bars extends the in-tab search from name-substring to
  a ranked hit list over descriptions, step notes, reagents,
  and conditions — so a query like *"Raney"* lands on the BHC
  Ibuprofen pathway via step-2 reagents, and *"Wheland"* finds
  nitration of benzene even though no reaction name contains it.

### Scripting workbench + dynamic scene composer (Phase 32)
A *Python REPL + editor* dialog (`Tools → Script editor…`,
Ctrl+Shift+E) lets users / agents drive the full registry from
scratch:

```python
from orgchem.scene import current_scene
scene = current_scene()
scene.add_protein("2YDO")        # A2A adenosine receptor
scene.add_molecule("CN1C=NC2=C1C(=O)N(C(=O)N2C)C",
                    track="caffeine", style="stick")
```

Writes directly into the detachable **Workbench** viewer — a
hybrid-placement tab / window that hosts an observable `Scene`
of composable **tracks** (small molecule or protein) with
per-track visibility / style / colour-swatch / opacity /
remove controls.

### Tools menu
A single-click path to every core capability, each as its own
dialog:

| Menu item                                 | Closes                                   |
|-------------------------------------------|------------------------------------------|
| Empirical / Molecular Formula Calculator… | Verma 2024 Section A                     |
| HRMS formula candidate guesser…           | Phase 4 MS candidate enumerator          |
| EI-MS fragmentation sketch…               | Common-neutral-loss predictor            |
| Retrosynthesis…                           | 8 SMARTS templates + multi-step tree     |
| Orbitals (Hückel / W-H)…                  | Hückel MOs + Woodward-Hoffmann rules     |
| Lab techniques…                           | TLC / recrystallisation / distillation / extraction |
| Medicinal chemistry (SAR / Bioisosteres)… | Seeded SAR series + bioisostere suggester |
| IUPAC naming rules…                       | 22-rule catalogue browser                |
| Periodic table…                           | Clickable 118-element table              |
| Spectroscopy (IR / NMR / MS)…             | Stick-spectrum predictor + save          |
| Stereochemistry…                          | R/S + E/Z table with Flip + Mirror       |
| Green metrics (atom economy)…             | Reaction AE + pathway overall AE         |
| Script editor (Python)…                   | REPL + editor driving the full registry  |

### Conformational dynamics
Rotatable-bond dihedral scans and conformer morphs render as
interactive HTML trajectories through the Phase 2c.2 3Dmol.js
player.

![Butane dihedral scan (interactive HTML)](screenshots/tour/dynamics_butane.html)

### Molecule browser: multi-category filters (Phase 28)
Two rolling combo boxes over the tag taxonomy (functional group /
source / composition / charge / size / ring count / has-stereo) AND
together with the free-text field. Each seeded molecule is auto-
tagged with SMARTS-based functional groups and hand-curated
source / drug-class labels (NSAID, statin, alkaloid, hormone,
steroid, fatty acid, …).

## Quickstart

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

For developer tooling (tests / ruff / mypy / pre-commit):

```bash
pip install -r requirements-dev.txt
pre-commit install   # optional: ruff + mypy on every commit
pytest tests/
```

## Headless / LLM-driven operation

Every GUI action is also an agent action via the `@action` registry.
Drive the app from Python:

```python
from orgchem.agent.headless import HeadlessApp
with HeadlessApp() as app:
    app.call("fetch_pdb", pdb_id="2YDO")
    app.call("analyse_binding", pdb_id="2YDO", ligand_name="CAF")
    app.call("export_interaction_map",
             pdb_id="2YDO", ligand_name="CAF",
             path="caffeine_a2a.png")
```

Or from any external process (including a Claude Code session) via
the JSON-over-stdio bridge:

```bash
python main.py --agent-stdio
# then write one JSON request per line, read one JSON response per line
```

## Project orientation

- [`INTERFACE.md`](INTERFACE.md) — navigation map for the codebase. **Read this first.**
- [`CLAUDE.md`](CLAUDE.md) — coding rules enforced by the project.
- [`PROJECT_STATUS.md`](PROJECT_STATUS.md) — what works *today*, with
  metrics and known issues.
- [`ROADMAP.md`](ROADMAP.md) — phased plan through v1.0 and beyond.
- [`SESSION_LOG.md`](SESSION_LOG.md) — rolling development log across
  101+ autonomous-loop rounds.

## Requires
Python 3.11+, RDKit, PySide6 (with QtWebEngine + QtWebChannel),
SQLAlchemy, PubChemPy, platformdirs, PyYAML. See `requirements.txt`
for the full list; `requirements-dev.txt` adds pytest / ruff / mypy
/ pytest-qt / imagehash.

## Reference
Empirical → molecular-formula calculation reimplements and extends
Verma, Singh & Passey, *Rasayan J. Chem.* 17(4): 1460–1472 (2024),
exposed as both a library call (`orgchem/core/formula.py`) and a
Tools menu dialog.

## Status (round 101 — 2026-04-24)

**Catalogue.**  415 molecules · 35 reactions · 20 mechanisms ·
25 pathways · 15 energy profiles · 80 glossary terms · 30 tutorial
lessons · 6 SAR series · 25 carbohydrates · 31 lipids · 33 nucleic
acids · 9 seeded proteins.

**Code health.**  **964 tests** green (0 skipped). **100 % GUI
coverage** (127 / 127 agent actions reachable from a menu, panel, or
dialog — pinned by `tests/test_gui_audit.py`).  Pollution-safe test
fixtures (`Tutor-test` prefix purge auto-runs at session end) +
fragment-consistency audit on every pathway keep the seeded DB
clean.

**Completed phases.**  1, 2a/b/c1/c2, 3a/b, 4 (IR/NMR/MS + HRMS +
fragmentation), 8a-d (synthesis pathways), 10a (MD), 11a-d (glossary
+ autolink + command palette), 13a-e (energy profiles + composite
mechanism), 14a/b (Hückel + Woodward-Hoffmann), 15a-c (lab
techniques), 17a/e / 18a / 19a/b/c (SAR + bioisosteres + Hammett +
KIE), 20a-e (offline 3Dmol, golden baselines, session state, batch
renders), 21a (pericyclic tutorials), 22a (dev tooling + CI),
24a-l (full protein/ligand stack — PDB + AlphaFold + pockets +
contacts + PPI + NA + PLIP bridge + 3Dmol viewer + click-to-inspect),
25a/b (GUI audit + dialog closures), 26a-c (glossary figures),
27a-c (periodic table), 28a-e (molecule browser filters),
29a-c (carb/lipid/NA siblings), 30 (macromolecules window),
31c/d/f/g (mechanisms + pathways + glossary + tutorials at
target counts), 32a-e (scripting workbench + script library),
33a-c (cross-surface full-text search).

**Actively shipping.**  Phase 31 long-running content expansion —
remaining sub-items to hit targets: 31a (molecules 415/400 — done),
31b (reactions 35/50), 31e (energy profiles 15/20), 31h
(carbohydrates 25/40), 31i (lipids 31/40), 31j (nucleic acids
33/40), 31k (SAR series 6/15), 31l (proteins 9/15).
