# Welcome to Microbiology Studio

Microbiology Studio is the **fourth sibling** in the multi-
studio life-sciences platform — a dedicated workspace for
microbes (bacteria + archaea + fungi + viruses + protists)
and how their cell biology, genetics, and enzymology drive
infection + treatment.

This is **Phase MB-1.0** (round 215). The full Microbio
catalogue + tools + tutorials roll out over Phases MB-2 → MB-6.

## What ships in Phase MB-1.0

Three tabs:

### 1. Microbes — 30-entry catalogue across the 5 microbial kingdoms

Indexed by **kingdom** + **Gram type**:

- **Bacteria** (17 entries):
  - **Gram-positive (6)**: Staphylococcus aureus,
    Streptococcus pyogenes, S. pneumoniae, Enterococcus
    faecalis, Clostridioides difficile, Listeria
    monocytogenes.
  - **Gram-negative (6)**: E. coli, Klebsiella pneumoniae,
    Pseudomonas aeruginosa, Neisseria meningitidis,
    Helicobacter pylori, Salmonella typhi.
  - **Atypical (3)**: Mycoplasma pneumoniae, Chlamydia
    trachomatis, Treponema pallidum.
  - **Acid-fast (2)**: Mycobacterium tuberculosis, M. leprae.
- **Archaea (2)**: Methanobrevibacter smithii (gut
  methanogen), Sulfolobus acidocaldarius (extremophile).
- **Fungi (3)**: Candida albicans, Aspergillus fumigatus,
  Cryptococcus neoformans.
- **Viruses (6)**: SARS-CoV-2, HIV-1, Influenza A, HBV,
  HSV-1, Norovirus — Baltimore I → VII covered.
- **Protists (2)**: Plasmodium falciparum (malaria),
  Toxoplasma gondii.

Each entry carries: full taxonomic name, kingdom, Gram type,
Baltimore class (viruses), morphology, key metabolism /
replication, pathogenesis summary, antimicrobial
susceptibility, genome size, Bergey / ICTV reference, and
**typed cross-references** to:

- OrgChem `CellComponent` ids (e.g. gram-positive bacteria
  → `peptidoglycan-gram-positive` + `bacterial-plasma-
  membrane` + `70s-ribosome`; archaea → `archaeal-plasma-
  membrane` + `pseudopeptidoglycan`).
- Pharm `DrugClass` ids (e.g. S. aureus →
  `beta-lactams` + `macrolides`; HIV-1 → `hiv-pis` +
  `nrtis`; M. tuberculosis → none of the standard catalogue,
  needs the future first-line tuberculosis class).
- Biochem enzyme ids (e.g. E. coli → `dna-ligase-i` (target
  of fluoroquinolone-adjacent topo II); HIV-1 →
  `hiv-protease`; SARS-CoV-2 → `cyp3a4` (Paxlovid is
  ritonavir-boosted)).

### 2. Antibiotic spectrum — bridge into Pharm Studio

Read-only view of `pharm.core.drug_classes` filtered to the
**six antimicrobial classes**: β-lactams, macrolides,
fluoroquinolones, aminoglycosides, HIV PIs, NRTIs. Click
*Open in Pharmacology Studio…* to hand off to the full Pharm
Studio drug-class browser pre-selected.

This is **another multi-hop cross-studio data sharing edge**:
Microbio imports Pharm directly via Python — and the Microbe
catalogue reverses the link by carrying
`cross_reference_pharm_drug_class_ids` on each organism so the
*"what drugs treat this bug?"* lookup is one field-read away.

### 3. Tutorials — Microbio-specific curriculum

This welcome lesson + the planned ~ 150-200 lessons over
Phase MB-4.

## How it sits in the platform

Five studios live together as of round 215:

| Studio | Status | Opener |
|--------|--------|--------|
| OrgChem Studio | Mature (rounds 1-211; 215 lessons) | Default main window |
| Cell Bio Studio | Phase CB-1.0 (round 212) | Window → Cell Biology Studio… (Ctrl+Shift+B) |
| Biochem Studio | Phase BC-1.0 (round 213) | Window → Biochem Studio… (Ctrl+Shift+Y) |
| Pharmacology Studio | Phase PH-1.0 (round 214) | Window → Pharmacology Studio… (Ctrl+Shift+H) |
| **Microbiology Studio** | **Phase MB-1.0 (round 215)** — this | Window → Microbiology Studio… (Ctrl+Shift+N) |
| Botany Studio | Planned (next) | — |
| Animal Biology Studio | Planned | — |

All five share **one process, one Qt event loop, one SQLite
DB, one global glossary, one agent registry**.

## Cross-studio links you can already see

Open the Microbes tab → select **Mycobacterium tuberculosis**
→ the right pane shows:

- *Cross-reference: OrgChem cell components*: the Mycobacterial
  cell wall is unusual (mycolic-acid mycomembrane); listed
  cross-refs include `bacterial-plasma-membrane` + `70s-
  ribosome`.
- *Cross-reference: Pharm drug classes*: empty — the standard
  TB regimen (RIPE = rifampicin + isoniazid + pyrazinamide +
  ethambutol) lives outside the PH-1.0 catalogue and is queued
  for Phase PH-2.
- *Cross-reference: Biochem enzymes*: empty for Mtb — TB-
  specific targets (InhA, KatG, RNA polymerase β-subunit)
  belong in a future biochem expansion.

Compare with **HIV-1**:

- *Cell components*: empty (viruses don't have their own
  cell structures).
- *Pharm drug classes*: `hiv-pis` + `nrtis`.
- *Biochem enzymes*: `hiv-protease`.

Open the Antibiotic spectrum tab → β-lactams → click *Open in
Pharmacology Studio…* → Pharm window opens pre-selected to
β-lactams.

## What's next

- **Phase MB-2** — more catalogues: virulence factors,
  toxins, antibiotic-resistance mechanisms, biofilm biology.
- **Phase MB-3** — interactive tools: antibiogram simulator,
  Gram-stain trainer, microbial-growth-curve calculator.
- **Phase MB-4** — ~ 150-200 microbio tutorial lessons.
- **Phase MB-5** — cross-studio cross-reference audit.
- **Phase MB-6** — integration polish + screenshot tour.
