# Wnt / β-catenin — from embryo to colon cancer

The Wnt pathway is one of the most-rewarding stories in
modern molecular biology — same molecular logic drives
embryonic axis specification, adult stem-cell maintenance,
*and* > 90 % of colorectal cancers.

## The canonical pathway in two states

### Off state (no Wnt ligand)

Cytoplasmic β-catenin is constitutively phosphorylated by
the **destruction complex**: Axin + APC (adenomatous
polyposis coli) + GSK3β + CK1α. Phospho-β-catenin gets
ubiquitinated by SCF^β-TrCP and degraded by the
proteasome. Cytosolic [β-catenin] stays low; nuclear
TCF/LEF transcription factors sit on Wnt-target genes
bound to the Groucho/TLE corepressor and keep them OFF.

### On state (Wnt ligand present)

Wnt binds the seven-pass Frizzled receptor + LRP5/6 co-
receptor at the plasma membrane. Frizzled-bound
Dishevelled recruits Axin away from the destruction
complex. The complex falls apart; β-catenin is no longer
phosphorylated, accumulates in cytoplasm, translocates to
nucleus, displaces Groucho from TCF/LEF, recruits BCL9 +
Pygopus + p300/CBP coactivators, drives Wnt-target gene
expression (cyclin D1, Myc, CD44, MMPs, axin2 negative-
feedback regulator).

The genius of the off-state mechanism is that the
"resting" state is actively maintained by continuous
β-catenin destruction. Removing any one piece (Axin, APC,
GSK3β) gives constitutive Wnt signalling without a
ligand.

## Wnt in development

Wnt signalling sets up:

- **Body-axis polarity** — *Xenopus* β-catenin nuclear
  accumulation on the dorsal side after sperm entry.
- **Anterior-posterior patterning** — gradient of Wnt
  activity from posterior (high) to anterior (low) in
  vertebrate gastrulation.
- **Limb-bud patterning** — Wnt5a + Wnt7a from posterior
  + dorsal limb bud regions.
- **Stem-cell niches** — intestinal-crypt + hair-follicle
  + haematopoietic + neural stem cells all require Wnt
  signalling.

The intestinal crypt is the textbook adult Wnt-stem-cell
niche: Paneth cells secrete Wnt3 → Lgr5+ stem cells at
crypt base → divide upward → as they leave the Wnt-rich
crypt they differentiate.

## Wnt in colon cancer

> 90 % of colorectal cancers have a mutation in the
canonical Wnt pathway. The most common (~ 80 %) is
loss-of-function APC truncation:

1. APC is part of the destruction complex.
2. Truncating APC mutation removes the β-catenin-binding
   region.
3. β-catenin is no longer destroyed.
4. Constitutive Wnt-target gene expression.
5. Continuous proliferation of crypt-base cells →
   adenoma → adenoma-carcinoma sequence.

Less common: **β-catenin** activating mutations (CTNNB1
exon 3 — removes the GSK3β phosphorylation sites). Same
end result: constitutive Wnt signalling.

Hence APC's name — **familial adenomatous polyposis**
(FAP) syndrome carriers inherit one mutant APC allele +
develop hundreds-thousands of colonic polyps in young
adulthood + invariably progress to colon cancer without
prophylactic colectomy.

## Therapeutic challenges

Wnt is one of the *hardest* pathways to drug:

- The cytoplasmic destruction complex is buried in
  intracellular interactions, not a classic enzyme
  pocket.
- Tankyrase inhibitors (XAV939) stabilise Axin →
  preclinical activity but narrow therapeutic window.
- Porcupine inhibitors (LGK974) block Wnt-ligand
  acylation + secretion → only works in tumours that
  depend on autocrine Wnt (RNF43-mutant pancreatic +
  colorectal).
- Frizzled-binding antibodies (vantictumab) +
  anti-Wnt antibodies were tried but bone-toxicity
  (Wnt-dependent osteoblast biology) limits.

The undruggable Wnt pathway remains a hot target — newer
strategies include β-catenin / TCF protein-protein
interaction blockers + degrader-based approaches.

## Non-canonical Wnt

Wnt signalling has non-canonical branches that don't go
through β-catenin:

- **Planar-cell-polarity (PCP) Wnt** — Frizzled +
  Dishevelled → Rho/Rac/JNK → cytoskeletal polarity. Sets
  up the orientation of vertebrate inner-ear hair cells +
  *Drosophila* wing-hair direction.
- **Wnt/Ca²⁺** — Frizzled + Dishevelled → PLC → IP3 +
  Ca²⁺ → PKC + CamKII + NFAT. Embryonic ventral fate.

Same Wnt ligands can drive different branches in different
contexts depending on receptor + co-receptor + downstream-
factor availability.

## Try it in the app

- **Cell Bio → Signalling** — `wnt-beta-catenin` entry.
- **Cell Bio → Cell cycle** — `cyclin-d-cdk4-cdk6` entry
  shows how Wnt drives Cyclin D1 expression → G1/S
  transition.

Next: **DNA damage response + the cell-cycle checkpoint
machinery**.
