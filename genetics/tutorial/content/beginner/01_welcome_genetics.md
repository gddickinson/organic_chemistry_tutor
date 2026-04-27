# Welcome to Genetics + Molecular Biology Studio

You are looking at the **seventh** sibling studio in
the multi-studio life-sciences platform built atop
OrgChem Studio.  After OrgChem, Cell Biology,
Biochemistry, Pharmacology, Microbiology, Botany, and
Animal Biology, the platform now has **a dedicated
home for the experimental TOOLBOX of modern molecular
biology**.

## What this studio offers

The flagship Phase **GM-1.0** catalogue is
**40 molecular-biology techniques** spanning every
major class:

- **PCR family** — endpoint PCR, qPCR, digital PCR,
  isothermal amplification (LAMP / RPA / NASBA).
- **Sequencing** — Sanger, Illumina short-read,
  PacBio HiFi, Oxford Nanopore.
- **Cloning** — restriction-enzyme, Gibson assembly,
  Golden Gate / MoClo / GoldenBraid, Gateway.
- **CRISPR** — Cas9, Cas12a, base editors, prime
  editors, SHERLOCK / DETECTR diagnostics.
- **Blots** — Southern, Northern, Western.
- **In-situ hybridisation** — FISH + smFISH /
  MERFISH.
- **Chromatin profiling** — ChIP-seq, CUT&RUN /
  CUT&Tag, ATAC-seq.
- **Transcriptomics** — bulk RNA-seq, scRNA-seq,
  snRNA-seq, ribosome profiling (Ribo-seq).
- **Spatial transcriptomics** — Visium, Slide-seqV2.
- **Proteomics** — bottom-up LC-MS/MS, BioID /
  TurboID / APEX proximity labelling.
- **Interactions** — yeast two-hybrid, AP-MS.
- **Structural / 3D-genome** — Hi-C / Micro-C.
- **Epigenetics** — bisulfite sequencing,
  Methylation EPIC arrays.
- **Delivery** — lipid nanoparticles (LNPs), AAV
  gene therapy.

Each entry is a long-form bench card: principle,
sample types, throughput, key reagents, typical
readouts, limitations, representative platforms,
year of introduction, key references.

## How this studio cross-references the platform

GM-1.0's strength is its **typed cross-reference
graph** to every other sibling.  Each technique
entry can carry edges to:

- **Biochem (BC-1.0) enzymes** — the molecular
  workhorses (DNA / RNA polymerases, ligases,
  restriction enzymes, reverse transcriptases,
  proteases used in proteomics sample prep).
- **Cell Biology (CB-2.0) cell-cycle** — chromatin /
  DDR / replication context (S phase + G2/M
  checkpoint for ChIP-seq / ATAC-seq / CRISPR
  context).
- **Cell Biology (CB-1.0) signalling pathways** —
  apoptosis + DDR pathways relevant to CRISPR
  outcomes + replication stress.
- **Animal Biology (AB-1.0) taxa** — the model
  organisms in which each technique was developed,
  validated, or routinely applied (worm + fly +
  zebrafish + mouse + human).
- **OrgChem molecules** — nucleobases (Adenine,
  Guanine, Cytosine, Thymine), nucleosides
  (Adenosine, Cytidine, Guanosine, Uridine,
  Thymidine), cofactors (NADH, NADPH, FAD), and
  intercalators / dyes (Methylene blue).

These cross-references are validated at test time —
a future rename in any sibling catalogue surfaces
immediately as a broken edge.

## How to use this studio

The main window opens via *Window → Genetics +
Molecular Biology Studio…* (Ctrl+Alt+G).  Three
inner tabs:

- **Techniques** — full 40-entry catalogue with
  category combo + free-text filter + HTML
  detail card showing principle / sample types /
  throughput / readouts / strengths / limitations /
  cross-references.
- **Cross-references** — bridge panel reading
  ``biochem.core.enzymes`` filtered to nucleic-
  acid-acting enzymes (DNA polymerases, ligases,
  restriction enzymes, reverse transcriptases,
  exonucleases, helicases — the molecular workhorses).
  Hand-off button to *Open in Biochem Studio…* takes
  you to the full enzyme detail.
- **Tutorials** — this lesson.

Or use the agent actions:
- ``list_genetics_techniques(category="")`` — full
  catalogue or category-filtered list.
- ``get_genetics_technique(id)`` — single entry by
  id.
- ``find_genetics_techniques(needle)`` — case-
  insensitive substring search.
- ``genetics_techniques_for_application(application)``
  — filter by application keyword.
- ``open_genetics_studio(tab="")`` — open the main
  window + optionally focus a tab.

## The 7-sibling-platform context

The platform is now **complete in its v0.1 form for
all 7 siblings**:

| Sibling | Phase | Window-menu shortcut |
|---------|-------|----------------------|
| OrgChem (root) | various | (default tabs in main window) |
| Cell Biology | CB-1.0 + CB-2.0 + CB-3.0 | Ctrl+Shift+B |
| Biochem | BC-1.0 + BC-2.0 + BC-3.0 | Ctrl+Shift+Y |
| Pharmacology | PH-1.0 + PH-2.0 + PH-3.0 | Ctrl+Shift+H |
| Microbiology | MB-1.0 + MB-2.0 + MB-3.0 | Ctrl+Shift+N |
| Botany | BT-1.0 + BT-2.0 + BT-3.0 | Ctrl+Shift+V |
| Animal Biology | AB-1.0 + AB-2.0 + AB-3.0 | Ctrl+Shift+X |
| **Genetics + Molecular Biology** | **GM-1.0** | **Ctrl+Alt+G** |

The first 6 siblings each ship 2 catalogues
(-1 + -2 deep-phase) plus an expanded ~ 13-14-
lesson tutorial (-3 chain).  GM-1.0 ships the
techniques catalogue + this welcome lesson; the
GM-2.0 deep-phase catalogue (Mendelian disorders +
gene-disease associations) and GM-3.0 tutorial
expansion are queued for future rounds.

## Try it now

- Open the **Techniques tab** + filter by category
  to see how each class of technique is
  catalogued.
- Open the **Cross-references tab** + see how
  ``biochem.core.enzymes`` integrates with the
  techniques layer.
- Search for ``"crispr"`` in the techniques filter
  box — see the 5 CRISPR-family entries side-by-
  side.

Welcome to the seventh sibling.
