# Welcome to Cell Biology Studio

Cell Biology Studio is a **sibling to OrgChem Studio** — a
dedicated workspace for learning + teaching cell biology, with
the same interactive-GUI-plus-curriculum-plus-agent-registry
pattern you already know from OrgChem.

This is a **Phase CB-1.0 prototype** (round 212). The full Cell
Bio curriculum + catalogue + tools are planned to roll out over
the next ~ 9 months as Phases CB-2 → CB-6.

## What cell biology covers

Modern cell biology rests on five conceptual pillars:

1. **Compartments + membranes** — organelles, lipid bilayer,
   intracellular + extracellular transport.
2. **Information flow** — transcription, translation,
   signalling, post-translational modification.
3. **Energy + metabolism** — at the cell level (mitochondria,
   chloroplasts; biochemistry detail lives in the planned Biochem
   Studio).
4. **Dynamics + mechanics** — cytoskeleton, motor proteins,
   division, motility, adhesion.
5. **Decisions + fate** — cell cycle, differentiation,
   apoptosis, autophagy, senescence.

Plus an **integrative track** for cancer / neurodegen /
regenerative biology that pulls all five pillars together.

## What ships in Phase CB-1.0

A single 25-pathway **Signalling** catalogue:

- **Growth-factor pathways**: MAPK / ERK, PI3K / Akt / mTOR,
  EGFR / RAS / RAF, Insulin.
- **Cytokine pathways**: JAK / STAT, TGF-β / Smad.
- **Morphogen pathways**: Wnt / β-catenin, Notch, Hedgehog.
- **Second-messenger pathways**: GPCR / cAMP / PKA, GPCR / IP₃ /
  Ca²⁺, PKC, Ca²⁺ / CaMKII.
- **Stress response**: NF-κB, p53, Hippo / YAP-TAZ, HIF-1α.
- **Nutrient + energy**: AMPK, mTORC1 amino-acid sensing.
- **Innate immunity**: TLR, cGAS / STING.
- **Adaptive immunity**: TCR signalling.
- **Cell death**: intrinsic apoptosis, extrinsic apoptosis,
  necroptosis, pyroptosis.

Each pathway carries:

- Receptor class + key downstream components.
- Disease associations (cancer, autoimmunity, neurodegen, etc.).
- Drug targets (where applicable) — bridging Cell Bio Studio to
  the planned Pharmacology Studio.
- Cross-references to OrgChem molecules (e.g. metformin →
  AMPK, vemurafenib → BRAF, sirolimus → mTORC1).

## How it cross-references OrgChem

When you open the Signalling tab + select **MAPK / ERK**, you'll
see a **Cross-reference: OrgChem molecules** section listing
*Vemurafenib* + *Trametinib*. These are real `Molecule` rows in
OrgChem's database — same molecules you can already inspect via
OrgChem's molecule browser, drug-likeness calculator, retro-
synthesis tool, etc.

The longer-term plan (Phase CB-5):

- Click a drug name in Cell Bio → opens it in OrgChem's molecule
  workspace.
- Cross-studio search: query "MAPK" → finds the Cell Bio pathway
  + every OrgChem reaction whose mechanism touches a kinase.
- Tutor backend (Tools menu) sees both studios' agent surfaces
  + can answer questions across them.

## How it sits in the platform

Cell Bio Studio is the **first sibling studio** in a planned
6-studio life-sciences platform:

| Studio | Status |
|--------|--------|
| OrgChem Studio | ✅ Mature (rounds 1-211, 215 lessons) |
| **Cell Bio Studio** | 🚧 **Phase CB-1.0 prototype (this!)** |
| Biochem Studio | Planned |
| Pharmacology Studio | Planned |
| Microbiology Studio | Planned |
| Botany Studio | Planned |
| Animal Biology Studio | Planned |

All six studios share one process, one Qt event loop, one
SQLite database, one global glossary, one agent registry. Each
studio owns its own catalogues + panels + tutorials, and links
to its siblings via typed cross-references audited by tests.

## Try it now

- **Signalling tab** → category combo (top-left) → pick
  *cell-death* → see intrinsic apoptosis, extrinsic apoptosis,
  necroptosis, pyroptosis side by side.
- **Receptor combo** → pick *RTK* → see all 4 RTK pathways
  (MAPK, PI3K, EGFR, Insulin) and how they share key components
  (Ras → Raf → MEK → ERK appears in 2 of them).
- **Free-text filter** → type *vemurafenib* → see the 1 pathway
  whose drug targets list it.
- **Right pane** → on any selected pathway, scroll to the
  *Cross-reference: OrgChem molecules* section. Those are real
  rows in OrgChem's database.

## Next

Phase CB-2 will add catalogues for cell-cycle, cytoskeleton,
motor proteins, membrane transporters, receptor families. Phase
CB-3 will add interactive simulators (cell-cycle, action
potential, membrane transport, signal pathway visualiser).
Phase CB-4 will populate the curriculum (~ 170 lessons across
4 tiers).
