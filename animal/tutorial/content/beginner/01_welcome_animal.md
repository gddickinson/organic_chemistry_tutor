# Welcome to Animal Biology Studio

Animal Biology Studio is the **sixth + final sibling** in
the multi-studio life-sciences platform — and **completes
the platform**.  Six studios now sit alongside OrgChem
Studio, sharing one process, one Qt event loop, one SQLite
DB, one global glossary, and one agent registry.

This is **Phase AB-1.0** (round 217).  The full Animal-
Biology catalogue + tools + tutorials roll out over Phases
AB-2 → AB-6.

For the full **6-studio retrospective** — what shipped
where, why, in what order, with which architectural
decisions — see the second tutorial lesson:
*Platform retrospective — the 6-studio build chain*.

## What ships in Phase AB-1.0

Three tabs:

### 1. Animal taxa — 30-entry catalogue spanning all 9 major animal phyla

Indexed by **phylum** + **body plan**:

- **Porifera (1)** — *Amphimedon queenslandica* (model
  sponge — first sponge genome).
- **Cnidaria (2)** — *Hydra vulgaris* (regeneration),
  *Nematostella vectensis* (model cnidarian for evo-devo).
- **Platyhelminthes (1)** — *Schmidtea mediterranea*
  (planarian — neoblast-driven regeneration).
- **Nematoda (2)** — *Caenorhabditis elegans* (4 Nobels —
  apoptosis, RNAi, GFP, microRNAs), *Trichinella spiralis*
  (parasitic).
- **Mollusca (2)** — *Loligo / Doryteuthis* (squid giant
  axon — Hodgkin-Huxley action-potential biology),
  *Aplysia californica* (Kandel's learning-and-memory model).
- **Annelida (1)** — *Hirudo medicinalis* (medicinal leech;
  source of hirudin → bivalirudin/lepirudin drugs).
- **Arthropoda (5)** — *Drosophila melanogaster* (6 Nobels;
  almost every developmental signalling pathway named here),
  *Apis mellifera* (honeybee), *Bombyx mori* (silkworm —
  bombykol, the first pheromone), *Daphnia pulex* (waterflea
  — ecotoxicology), *Limulus polyphemus* (horseshoe crab —
  LAL endotoxin assay).
- **Echinodermata (1)** — *Strongylocentrotus purpuratus*
  (purple sea urchin — fertilisation biology).
- **Chordata (15)**: tunicate (*Ciona intestinalis*); fish
  (zebrafish *Danio rerio*, pufferfish *Takifugu rubripes*,
  medaka *Oryzias latipes*); amphibians (*Xenopus laevis*,
  axolotl *Ambystoma mexicanum*); reptile (green anole
  *Anolis carolinensis*); birds (chicken *Gallus gallus*,
  zebra finch *Taeniopygia guttata*); mammals (mouse,
  rat, rhesus macaque, dog, cattle *Bos taurus*, **Homo
  sapiens**).

Each entry carries: full taxonomic name, phylum, class,
body plan, germ-layer count (diploblast / triploblast /
not-applicable for sponges), coelom organisation
(acoelomate / pseudocoelomate / coelomate / not-
applicable), reproductive strategy, ecological role,
model-organism flag, genome size, and **typed cross-
references** to:

- OrgChem `Molecule` rows for animal-derived metabolites,
  hormones, and neurotransmitters (e.g. *Homo sapiens* →
  Cortisol + Cholesterol + ATP + Dopamine + L-DOPA + …;
  cattle → Cholesterol + Lactose + Cholic acid; squid →
  Glycine; honeybee → none in the v0.1 catalogue).
- Cell Bio `signaling-pathway` ids for pathways
  characterised in this animal model (e.g. *Drosophila*
  → hedgehog + notch + wnt-beta-catenin + Toll/TLR + …;
  *C. elegans* → intrinsic-apoptosis; *Aplysia* →
  gpcr-camp-pka + camkii).
- Biochem `enzyme` ids for animal-source enzymes
  (e.g. cattle → chymotrypsin + trypsin + ATP synthase;
  *Aplysia* → PKA + adenylate cyclase; chicken → lysozyme).

### 2. Cell signalling bridge — animal-relevant pathways

Read-only view of `cellbio.core.cell_signaling` filtered
to the **21 animal-developmental + apoptosis + immune
pathways**: developmental (Wnt/β-catenin, Notch, Hedgehog,
TGF-β/Smad, EGFR/RAS/RAF, MAPK/ERK, PI3K/Akt/mTOR,
JAK/STAT, insulin), apoptosis (intrinsic, extrinsic,
necroptosis, pyroptosis), immune (TLR, TCR, NF-κB, cGAS-
STING), stress (p53, Hippo-YAP, AMPK, mTORC1 amino-acid
sensing).

This is the **second sibling whose bridge reads
`cellbio.core.cell_signaling` directly** — the first was
Pharm Studio (PH-1.0).  AB-1.0 confirms the cellbio API
is stable enough to support multiple consumers — a key
sign that the platform's library boundaries are mature.

Click *Open in Cell Biology Studio…* to hand off to the
full Cell Bio Studio pathway browser pre-selected.

### 3. Tutorials — Animal Biology + Platform Retrospective

This Welcome lesson + the **Platform retrospective**
documenting the entire 6-studio build chain.  The deeper
~ 150-200-lesson Animal-Biology curriculum is planned for
Phase AB-4.

## How it sits in the platform — final form

| Studio | Status | Opener |
|--------|--------|--------|
| OrgChem Studio | Mature (rounds 1-211; 215 lessons) | Default main window |
| Cell Bio Studio | Phase CB-1.0 (round 212) | Window → Cell Biology Studio… (Ctrl+Shift+B) |
| Biochem Studio | Phase BC-1.0 (round 213) | Window → Biochem Studio… (Ctrl+Shift+Y) |
| Pharmacology Studio | Phase PH-1.0 (round 214) | Window → Pharmacology Studio… (Ctrl+Shift+H) |
| Microbiology Studio | Phase MB-1.0 (round 215) | Window → Microbiology Studio… (Ctrl+Shift+N) |
| Botany Studio | Phase BT-1.0 (round 216) | Window → Botany Studio… (Ctrl+Shift+V) |
| **Animal Biology Studio** | **Phase AB-1.0 (round 217)** — this | Window → Animal Biology Studio… (Ctrl+Shift+X) |

**The platform is now complete.**  Six sibling studios.

## Cross-studio links you can already see

Open the Animal taxa tab → select **Homo sapiens** → the
right pane shows the largest cross-reference profile in the
catalogue: ~ 22 OrgChem molecules, ~ 26 cellbio signalling
pathways, ~ 26 biochem enzymes — humans are the convergence
point of the entire platform's catalogues.

Compare with **C. elegans**:
- pathways: intrinsic-apoptosis, insulin, wnt, notch, …
- enzymes: caspase-3 (the worm gave us *ced-3*).

Compare with **Drosophila**:
- pathways: hedgehog, notch, wnt, TLR, JAK-STAT, … —
  almost every developmental + immune pathway named in
  fly genetics.

Open the Cell signalling bridge tab → click *Open in Cell
Biology Studio…* → Cell Bio window opens pre-selected to
the chosen pathway.

## What's next

- **Phase AB-2** — more catalogues: comparative anatomy,
  organ systems, behavioural neuroscience.
- **Phase AB-3** — interactive tools: cladogram builder,
  Hardy-Weinberg solver, allometric-scaling calculator.
- **Phase AB-4** — ~ 150-200 animal-biology tutorial
  lessons.
- **Phase AB-5** — formal cross-studio cross-reference
  audit.
- **Phase AB-6** — integration polish + screenshot tour.

The next priority across the **whole platform** pivots
from *"build sibling N"* to *"deepen each sibling's
catalogue / tools / tutorials / audits"* — every sibling
has its own -2 / -3 / -4 / -5 / -6 deeper-phase queue
waiting for incremental work.
