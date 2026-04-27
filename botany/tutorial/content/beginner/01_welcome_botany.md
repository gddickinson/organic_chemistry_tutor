# Welcome to Botany Studio

Botany Studio is the **fifth sibling** in the multi-studio
life-sciences platform — a dedicated workspace for plant
biology + plant chemistry + the cross-references between
plants and the drug chemistry humans extracted from them.

This is **Phase BT-1.0** (round 216). The full Botany
catalogue + tools + tutorials roll out over Phases BT-2 →
BT-6.

## What ships in Phase BT-1.0

Three tabs:

### 1. Plant taxa — 30-entry catalogue spanning all 6 major plant divisions

Indexed by **division** + **photosynthetic strategy** (C3 /
C4 / CAM / not-applicable):

- **Bryophyta (1)** — *Physcomitrium patens* (model moss).
- **Lycopodiophyta (1)** — *Selaginella moellendorffii*
  (model spikemoss).
- **Pteridophyta (2)** — *Azolla filiculoides* (N₂-fixing
  water fern), *Pteridium aquilinum* (bracken).
- **Gymnosperms (4)** — *Ginkgo biloba* (living fossil),
  *Taxus brevifolia* (Pacific yew → paclitaxel), *Pinus
  taeda* (loblolly pine), *Picea abies* (Norway spruce).
- **Angiosperms — monocots (8)** — *Oryza sativa* (rice),
  *Zea mays* (maize, **C4**), *Saccharum officinarum*
  (sugarcane, **C4**), *Triticum aestivum* (wheat),
  *Musa acuminata* (banana), *Allium sativum* (garlic),
  *Vanilla planifolia* (vanilla, **CAM**), *Aloe vera*
  (**CAM**).
- **Angiosperms — eudicots (14)** — *Arabidopsis thaliana*
  (model dicot), *Solanum lycopersicum* (tomato →
  Lycopene), *Nicotiana tabacum* (tobacco → Nicotine),
  *Papaver somniferum* (opium poppy → Morphine, Codeine →
  the **opioid** drug class), *Salix alba* (white willow →
  Salicylic acid → Aspirin → the **NSAID** class),
  *Coffea arabica* (coffee → Caffeine), *Cinchona
  officinalis* (quinine bark → Quinine), *Mentha piperita*
  (peppermint → Menthol), *Theobroma cacao* (cacao →
  Theobromine), *Atropa belladonna* (deadly nightshade →
  Atropine), *Camellia sinensis* (tea → Caffeine + EGCG +
  L-theanine), *Capsicum annuum* (chili → Capsaicin),
  *Hevea brasiliensis* (rubber tree → Ethylene biology),
  *Rafflesia arnoldii* (the holoparasite — **not-
  applicable** photosynthesis, no leaves, no roots).

Each entry carries: full taxonomic name, division, class,
life cycle, photosynthetic strategy, reproductive strategy,
ecological role, economic importance, model-organism flag,
genome size, and **typed cross-references** to:

- OrgChem `Molecule` rows (e.g. opium poppy → Morphine +
  Codeine; willow → Salicylic acid + Aspirin; tomato →
  Lycopene; tea + cacao + coffee → Caffeine).
- OrgChem `metabolic-pathway` ids (Calvin cycle is universal
  across all photosynthetic taxa; glycolysis + TCA + ox-phos
  + fatty-acid biosynthesis universal across all plants).
- Pharm `drug-class` ids (poppy → opioids; willow → NSAIDs;
  yew → taxanes).

### 2. Plant secondary metabolites — live DB-read bridge

Read-only view of `orgchem.db.Molecule` filtered by
`source_tags_json` to plant-derived natural products:
`natural-product` (11 rows), `terpene` (6 rows), `alkaloid`
(3 rows), `steroid` (2 rows).

This is the **first sibling whose bridge reads SQLite
directly** — earlier siblings (Pharm, Microbio) bridged to
other Python catalogues. Botany validates that the cross-
studio pattern works cleanly for live database rows too.

The *Open in Molecule Workspace* button fires
`bus().molecule_selected` so the OrgChem main window jumps
to the molecule tab pre-loaded with the chosen metabolite.

### 3. Tutorials — Botany-specific curriculum

This welcome lesson + the planned ~ 150-200 lessons over
Phase BT-4.

## How it sits in the platform

Six studios live together as of round 216:

| Studio | Status | Opener |
|--------|--------|--------|
| OrgChem Studio | Mature (rounds 1-211; 215 lessons) | Default main window |
| Cell Bio Studio | Phase CB-1.0 (round 212) | Window → Cell Biology Studio… (Ctrl+Shift+B) |
| Biochem Studio | Phase BC-1.0 (round 213) | Window → Biochem Studio… (Ctrl+Shift+Y) |
| Pharmacology Studio | Phase PH-1.0 (round 214) | Window → Pharmacology Studio… (Ctrl+Shift+H) |
| Microbiology Studio | Phase MB-1.0 (round 215) | Window → Microbiology Studio… (Ctrl+Shift+N) |
| **Botany Studio** | **Phase BT-1.0 (round 216)** — this | Window → Botany Studio… (Ctrl+Shift+V) |
| Animal Biology Studio | Planned (final sibling) | — |

All five sibling studios + OrgChem share **one process, one
Qt event loop, one SQLite DB, one global glossary, one agent
registry**.

## Cross-studio links you can already see

Open the Plant taxa tab → select **Papaver somniferum** →
the right pane shows:

- *Cross-reference: OrgChem molecules*: **Morphine**,
  **Codeine**.
- *Cross-reference: metabolic pathways*: `calvin_cycle`,
  `glycolysis`, `tca_cycle`, `ox_phos` (universal core).
- *Cross-reference: Pharm drug classes*: **opioids**.

Compare with **Salix alba** (willow):
- molecules: **Salicylic acid** + **Aspirin**.
- drug class: **NSAIDs**.

Compare with **Taxus brevifolia** (Pacific yew):
- drug class: **taxanes** (paclitaxel — the original
  supply was bark-extracted, killing the tree).

Open the Plant secondary metabolites tab → category combo →
**Alkaloids** → see Morphine + Atropine + Quinine pulled
live from the molecule DB → click *Open in Molecule
Workspace* to land in OrgChem's main window with the
compound loaded.

## What's next

- **Phase BT-2** — more catalogues: plant tissues + organ
  anatomy, plant hormones, mycorrhizal partnerships,
  pollination biology, seed dormancy + germination.
- **Phase BT-3** — interactive tools: Punnett-square solver,
  C3/C4/CAM photosynthesis simulator, plant-defence pathway
  visualiser.
- **Phase BT-4** — ~ 150-200 botany tutorial lessons.
- **Phase BT-5** — formal cross-studio cross-reference
  audit.
- **Phase BT-6** — integration polish + screenshot tour.
