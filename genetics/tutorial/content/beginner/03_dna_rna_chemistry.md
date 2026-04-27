# DNA + RNA chemistry basics

The chemistry of nucleic acids is the structural
foundation of every molecular-biology technique.  This
lesson covers the primary chemical features that drive
hybridisation, replication, transcription, and the
biophysics of every nucleic-acid manipulation.

## The four bases

Nucleic acids are linear polymers of nucleotides;
each nucleotide is a base + a sugar + a phosphate.

### Purines (two-ring)

- **Adenine (A)** — 6-aminopurine.  Pairs with T (DNA)
  or U (RNA) via 2 hydrogen bonds.
- **Guanine (G)** — 2-amino-6-oxopurine.  Pairs with
  C via 3 hydrogen bonds.

### Pyrimidines (one-ring)

- **Cytosine (C)** — 4-amino-2-oxopyrimidine.  Pairs
  with G.
- **Thymine (T)** — 5-methyl-uracil.  DNA only.
  Pairs with A.
- **Uracil (U)** — RNA only (and DNA-uracil from
  spontaneous deamination of cytosine — repaired).
  Pairs with A.

The 5-methyl on thymine vs uracil's H is the only
chemical difference that distinguishes DNA from RNA at
the base level — but it's mechanistically critical
(below).

## The sugars

- **2'-Deoxyribose (DNA)** — ribose with H instead of
  OH at the 2' carbon.
- **Ribose (RNA)** — has the 2'-OH.

The 2'-OH affects:
- **Reactivity** — RNA is chemically less stable than
  DNA (2'-OH catalyses backbone hydrolysis under
  alkaline / metal-ion conditions).
- **Conformation** — RNA preferentially adopts A-form
  helix (C3'-endo sugar pucker); DNA preferentially
  adopts B-form (C2'-endo).
- **Storage role** — DNA's stability suits long-term
  genomic storage; RNA's instability suits short-term
  signalling roles.

## Phosphodiester backbone

Nucleotides are joined 3'-5' by phosphodiester bonds:
- Each linkage spans phosphate + sugar + phosphate.
- The backbone has a directionality — 5' end (free
  phosphate) to 3' end (free hydroxyl).
- All polymerases extend in the 5' → 3' direction.
- Backbone is highly negatively charged (one negative
  per phosphate at physiological pH) — drives
  electrostatic interactions with positively-charged
  proteins (histones, transcription factors, viral
  capsids).

## Watson-Crick base pairing

The classic complementarity:
- A:T (DNA) / A:U (RNA) — 2 H-bonds (N1-N3, N6-O4).
- G:C — 3 H-bonds (N1-N3, N2-O2, O6-N4).

GC content matters for:
- **Stability** — G:C pairs are more stable than A:T;
  GC-rich DNA has higher Tm.
- **PCR + sequencing** — high-GC regions amplify
  poorly; ONT + PacBio handle them better than
  Illumina.
- **Codon usage** — organisms have characteristic GC
  content; *Plasmodium* AT-rich (~ 80 % AT);
  *Streptomyces* GC-rich (~ 70 % GC).

## Non-canonical pairing

- **Wobble pairs** — G:U + I (inosine):A / C / U.
  Allows tRNA flexibility (one tRNA reads multiple
  codons).
- **Hoogsteen pairing** — A:T using the major-groove
  N7 of A; basis of triplex DNA.
- **Reverse Watson-Crick + reverse Hoogsteen** — RNA
  tertiary structure motifs.
- **G-quadruplex (G4)** — four G's stacked via
  Hoogsteen-like H-bonds + K⁺ coordination; found at
  telomeres + ~ 700 K putative sites in human genome;
  regulatory roles.
- **i-motif** — C-rich sequences; protonation-
  dependent.

## Strand orientation + the helix

DNA double helix:
- Two strands antiparallel (one 5'-3', the other
  3'-5').
- Right-handed helix (B-form).
- ~ 10.4 base pairs per turn (B-form).
- Diameter ~ 2.0 nm; rise per base ~ 0.34 nm.
- Major groove + minor groove (asymmetric backbone
  geometry).
- Most sequence-specific protein binding (TFs)
  reads the major groove.

DNA polymorphism:
- **B-form** (most common; physiological).
- **A-form** (RNA, RNA-DNA hybrids; dehydrated).
- **Z-form** (alternating purine-pyrimidine, GC-rich;
  left-handed).

## Tm + denaturation

The melting temperature (Tm) at which 50 % of duplexes
are denatured:

- **Wallace rule** (short oligos): Tm ≈ 4(G+C) + 2(A+T).
- **Nearest-neighbor** (more accurate; SantaLucia 1998):
  factors in stacking interactions.
- **Tm depends on**: length, GC content, salt
  concentration ([Na⁺] / [Mg²⁺]), formamide, pH.

Tm matters for:
- **PCR primer design** — anneal at Tm − 5 °C
  typically.
- **Hybridisation** (Northern + Southern + microarray)
  — wash stringency calibrated to Tm.
- **DNase footprinting** + **EMSA** + **SELEX** — all
  exploit hybridisation under controlled conditions.

## Modified bases

In nature:
- **5-methylcytosine (5mC)** — major DNA
  methylation in mammals (CpG context).
- **5-hydroxymethylcytosine (5hmC)** — TET-oxidation
  intermediate; high in brain.
- **N6-methyladenine (6mA)** — bacterial defence;
  archaeal restriction; recently reported in some
  eukaryotes.
- **N1-methyladenosine (m1A)** + **N6-methyl-2'-O-
  methyladenosine (m6Am)** — RNA modifications.
- **m6A** — most-abundant mRNA internal modification;
  > 100 distinct RNA modifications catalogued
  ("epitranscriptome").
- **Pseudouridine (Ψ)** — most-abundant RNA modification
  overall; in tRNA + rRNA + mRNA.
- **2'-O-methyl** — cap structure + spliceosomal
  snRNAs.

In synthesis (chemistry):
- **Deoxyuracil** (dU) — used in PCR carryover
  prevention.
- **Inosine (I)** — degenerate base.
- **Phosphorothioate backbones** — nuclease-resistant
  ASOs.
- **2'-O-Me + 2'-MOE + LNA + cEt** — sugar
  modifications for hybridisation specificity +
  nuclease resistance.
- **Pseudouridine + N1-methylpseudouridine** — used
  in mRNA vaccines (Karikó-Weissman) to dampen TLR /
  innate-immune activation.

## Damage + repair

DNA damage occurs constantly:
- **Spontaneous depurination** (loss of A or G) —
  ~ 10 K events / cell / day.
- **Cytosine deamination** (C → U) — ~ 100 events /
  cell / day; UDG repairs.
- **Oxidative damage** — 8-oxo-G is the most common
  oxidative lesion; repaired by OGG1.
- **UV-induced cyclobutane pyrimidine dimers (CPD)
  + 6-4 photoproducts** — repaired by NER.
- **Alkylation damage** — repaired by direct
  reversal (MGMT) + BER.
- **Double-strand breaks** — repaired by NHEJ +
  HDR.

DNA-damage-response (DDR) pathways are covered in
detail in **Cell Biology Studio → DNA damage response**
+ **CB-3.0 advanced "DNA damage response" lesson**.

## RNA secondary + tertiary structure

Single-stranded RNA folds extensively via intramolecular
base pairing:

- **Stems + loops** — hairpins (terminator hairpins,
  sRNA structures, miRNA precursors).
- **Pseudoknots** — interleaved stem pairs (frame-
  shifting elements; ribozyme cores).
- **G-quadruplex** in mRNA UTRs.
- **Internal ribosome entry sites (IRES)** — viral +
  cellular cap-independent translation.
- **Riboswitches** — bacterial 5'-UTR aptamers
  controlling translation in response to small-
  molecule binding.

## Why this all matters for techniques

- PCR efficiency ↔ Tm + GC + secondary structure.
- Hybridisation specificity ↔ base pairing thermodynamics.
- Restriction enzymes ↔ specific palindromic
  recognition.
- Methylation profiling ↔ 5mC + 5hmC chemistry.
- mRNA-vaccine design ↔ Ψ / m1Ψ modification +
  cap-1 chemistry.
- ASO + siRNA design ↔ phosphorothioate +
  2'-modification chemistry.
- CRISPR sgRNA design ↔ chemical synthesis at scale +
  modification stability.

Every molecular-biology technique in the GM-1.0
catalogue rests on these chemical foundations.

## Try it in the app

- **OrgChem → Database** — Adenine, Guanine,
  Cytosine, Thymine, Uracil + the nucleosides
  Adenosine, Cytidine, Guanosine, Uridine, Thymidine.
- **OrgChem → Macromolecules → Nucleic acids** —
  natural + modified base catalogue.
- **Window → Genetics + Molecular Biology Studio →
  Techniques** — see how every technique exploits
  these chemical features.

Next: **Mendelian genetics + classical chromosomes**.
