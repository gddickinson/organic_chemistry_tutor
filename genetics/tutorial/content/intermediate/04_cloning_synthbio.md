# Cloning + synthetic biology basics

Cloning is the act of physically constructing a
recombinant DNA molecule + propagating it in a host.
Synthetic biology builds on this foundation by
designing standardised + reusable + composable parts.

## The vector toolkit

### Plasmid vectors

- **High-copy** (pUC, pBluescript) — ~ 100-700
  copies / cell; for routine cloning, sub-cloning,
  sequence verification.
- **Low-copy** (pBR322, pSC101, pBBR1) — ~ 10-50
  copies; for toxic gene products + tight regulation.
- **Single-copy / BAC + PAC** — large inserts (50-
  300 kb); copy-number ~ 1.
- **Expression vectors** — host-specific promoter +
  RBS + tag + terminator; pET (T7), pGEX (GST), pBAD
  (arabinose-inducible).
- **Yeast vectors** — pYES (GAL1), pYEX (galactose);
  CEN / ARS for low copy or 2µ for high copy.
- **Mammalian vectors** — pcDNA (CMV), pCAG, pcDNA-
  GFP-tag fusions, pCDH (lentiviral).
- **Plant vectors** — Ti-plasmid-derived binary
  vectors (pCAMBIA, pBIN, pBI, pGreen).

### Selection markers

- **Antibiotic resistance** — ampicillin / kanamycin /
  chloramphenicol / spectinomycin / hygromycin /
  zeocin / blasticidin / puromycin / G418.
- **Auxotrophic complementation** — yeast HIS3 /
  LEU2 / TRP1 / URA3.
- **Visual** — eGFP / mCherry / lacZ blue/white.
- **Counterselection** — sacB (sucrose sensitivity),
  ccdB (lethal in non-resistant strains).

### Tags + fusion partners

- **Solubility / expression** — MBP, SUMO, GST,
  thioredoxin.
- **Affinity purification** — His6 / His10, FLAG /
  3xFLAG, HA, c-myc, V5, Strep-II, Streptag, Spot-
  tag.
- **Visualisation** — eGFP, mCherry, mScarlet,
  Halo-tag, SNAP-tag.
- **Degradation** — auxin-degron (AID), dTAG, FKBP-
  degron (Halo-PROTAC).
- **Localisation** — NLS, NES, SKL (peroxisome),
  myristoyl + palmitoyl (membrane).

## The major cloning approaches

### Restriction-enzyme cloning

The classical approach (covered in detail in the
GM-1.0 catalogue's `restriction-cloning` entry).
Pros: cheap, well-understood.  Cons: site-availability
limited, slow.

### Gibson assembly

Primer-based isothermal multi-fragment assembly with
designed homology arms.  See `gibson-assembly` entry.
The de-facto modern standard for one-off + multi-
fragment construction.

### Golden Gate + MoClo + GoldenBraid

Type-IIS-based assembly with destruction of recognition
sites → irreversible.  Modular, syntactic.  See
`golden-gate` entry.  The de-facto standard for
synthetic-biology pipelines + plant biotech.

### Gateway

Site-specific recombination via λ phage int + xis +
IHF (BP + LR clonase).  See `gateway-cloning` entry.
Scarred, proprietary, but unrivalled for parallel
destination-vector swapping in ORFeome workflows.

### Direct synthesis

For new constructs ≤ ~ 10 kb, gene synthesis (Twist,
IDT, Thermo, GeneArt) is increasingly competitive
with primer-based assembly.  Costs ~ $0.05-0.15 / bp
in 2026.  Ideal for codon-optimised + complex /
repetitive sequences that are hard to PCR.

## Construct design — the design phase

### Codon optimisation

- Match codon usage to expression host (E. coli,
  yeast, CHO, HEK293, *Pichia*, plant).
- Avoid:
  - Restriction sites that interfere with downstream
    cloning.
  - Repetitive sequences that recombine.
  - GC > 80 % runs (mRNA structure).
  - Ribosome-binding-like sequences in coding region.
  - Cryptic splice sites in mammalian work.
- Tools: GeneArt + Twist optimisers; OPTIMIZER;
  EnCODE.

### Promoter choice

- **Bacterial** — T7 (tightly inducible, IPTG); ara
  (arabinose); rha (rhamnose); λ pL/pR (heat-
  inducible).
- **Yeast** — GAL1 (galactose); MET25 (methionine
  off); GPD / TEF (constitutive).
- **Mammalian** — CMV (strong constitutive); EF1α
  (longer-lasting); Tet-On / Tet-Off (doxycycline);
  CAG (synthetic strong promoter).
- **Plant** — CaMV 35S (constitutive); ubiquitin
  (cereals); tissue-specific (RbcS, ABI3, SUC2).
- **Inducible vs constitutive** — inducible for
  toxic / regulated proteins; constitutive for
  routine expression.

### Tags + linker design

- **N- or C-terminal tag?** Consider protein-folding
  + functional implications.  Tags can disrupt
  signal peptides or membrane anchors.
- **Linker** — flexible (GS / GGGGS) or rigid (EAAAK
  α-helical) depending on need.  3-10 aa typical.
- **Cleavage site** — TEV (ENLYFQ↓G), 3C / PreScission
  (LEVLFQ↓GP), thrombin (LVPR↓GS), HRV-3C, SUMO
  (cleaved by SUMO protease).

### Polyadenylation + termination

- **Bacterial** — T7 terminator, rrnB T1.
- **Yeast** — CYC1 terminator, ADH1 terminator.
- **Mammalian** — bGH polyA, SV40 polyA, hGH polyA.
- **Plant** — Nos terminator, OCS terminator, 35S
  terminator.

### Internal ribosome entry sites (IRES) + 2A peptides

- For polycistronic mammalian expression:
  - **IRES** — EMCV, FMDV.  Independent translation
    of downstream ORF.  Often produces less
    downstream protein.
  - **2A peptides** — P2A, T2A, E2A, F2A.  Self-
    cleaving (ribosome skipping).  Equimolar
    expression; small residue scar.
- Plants: 2A peptides increasingly used.

## Construction workflow

### A typical Gibson assembly

1. **Design** — PCR primers with 20-30 bp homology
   arms via Benchling / SnapGene / NEBuilder
   Assembly Tool.
2. **PCR amplification** — Q5 / Phusion + designed
   primers + DpnI digest of template plasmid.
3. **Gel cleanup** — column or gel-extraction.
4. **Quantify** — Qubit / NanoDrop; use molar
   ratios (1:3 vector:insert typical).
5. **Assembly** — NEBuilder HiFi 50 °C / 15-60 min;
   2 µL transformation into chemically competent
   DH5α / NEB10β / NEB Stable.
6. **Plate** — appropriate antibiotic; overnight
   37 °C.
7. **Pick + miniprep** — 4-8 colonies; QIAprep /
   Monarch.
8. **Diagnostic digest** — restriction-enzyme cut
   to verify size + arrangement.
9. **Sanger sequencing** — verify the junction +
   any synthesized region.
10. **Sequence-verified glycerol stock** — long-
    term storage at -80 °C.

### Quality control

- **Resequence the entire insert + flanks** — many
  papers retracted because the deposit had a typo.
- **Test multiple isolates** — Gibson + Golden Gate
  occasionally yield mixed-population clones.
- **Check expression** — Western or fluorescence;
  silent mutations in promoter / RBS / tag can kill
  output.

## Synthetic biology — the design layer

Synbio applies engineering principles to biology:

### Standard parts (BioBricks, etc.)

- **Registry of Standard Biological Parts** (iGEM)
  — open library of characterised parts.
- **Cidar MoClo + Loop + EMMA + GreenGate** — plant
  + bacterial / yeast hierarchical assembly
  frameworks.
- **MIDORI** + **OpenMTA** — material-transfer
  agreements simplifying part exchange.

### Common circuits

- **Toggle switch** (Gardner et al. 2000) — bistable
  mutually-repressing TFs.
- **Repressilator** (Elowitz + Leibler 2000) —
  oscillator from 3 mutually-repressing TFs.
- **Riboswitches** — RNA-aptamer-controlled
  translation / transcription.
- **Tet-On / Tet-Off** — TetR-based small-molecule
  inducible.
- **Cre-loxP / FLP-FRT** — site-specific
  recombination switches.
- **Logic gates** (AND, OR, NOR) — engineered with
  TF cascades or CRISPR-dCas9.
- **Quorum-sensing** circuits — population-level
  control.

### Modern frontiers

- **Genome-scale design** — minimal genomes
  (Mycoplasma JCVI-syn3.0, *E. coli* Syn61), genome
  refactoring.
- **Codon-recoded organisms** — E. coli with one or
  more codons swapped → reassign for non-canonical
  amino-acid incorporation (Sc 2.0 / Syn61.Δ3).
- **CRISPR-based genome scale screens + circuits**.
- **ML-aided design** — generative models (RFdiffusion
  proteins; Inscripta + Twist + Synthego DNA
  composition optimisation).
- **Cell-free systems** — TX-TL, PURE, MyTXTL for
  rapid prototyping.

## Industrial + clinical applications

- **Recombinant protein production** — insulin
  (Genentech 1978; Humulin 1982), EPO, growth
  hormone, blood-clotting factors.
- **Monoclonal antibodies** — CHO-cell expression;
  fed-batch bioreactors at 100-15 000 L scale.
- **Industrial enzymes** — amylase, protease,
  cellulase, phytase for detergent + food + feed.
- **Biofuels** — engineered yeast for bioethanol;
  algae for biodiesel.
- **Living therapeutics** — engineered probiotics
  (Synlogic), engineered gut bacteria for IBD +
  PKU + IEMs.
- **Sustainable chemistry** — Genomatica BDO, Solugen
  H2O2 + glucaric acid.

## Skills + ecosystem

- **Cloning workhorses**: Benchling + SnapGene +
  Geneious for in-silico design + simulation.
- **Wet lab**: pipetting, sterile technique,
  competent-cell preparation (CaCl2 chemical, or
  electroporation), agar plating, miniprep,
  Gibson / Golden Gate / restriction setup.
- **Sequencing**: Sanger for verification (~ $5-10
  per reaction commercially); whole-plasmid Nanopore
  (Plasmidsaurus, plasmidsaurus.com — $15-25 per
  plasmid in 2026) increasingly preferred for
  full-construct verification.
- **Project management**: Benchling + Asana / Trello
  + git-LFS for design files.

## Pitfalls

- **Wrong vector chosen** for downstream
  application (e.g. mammalian expression in a
  bacterial-only vector).
- **Tag interferes with function** — N-terminal
  tag on a secreted protein may prevent secretion;
  C-terminal on a GPI-anchored.
- **Frame shift after fusion** — verify reading
  frame extends through tag + linker.
- **Cryptic splice site** in cDNA when expressed
  in mammalian → wrong protein product.
- **Codon optimisation that introduces restriction
  site** that downstream cloning needs to use.
- **Repeat sequences** that recombine in vector or
  during synthesis.

## Cross-link

The GM-1.0 catalogue's `restriction-cloning`,
`gibson-assembly`, `golden-gate`, and `gateway-cloning`
entries provide technology context.  This lesson is
the design + workflow + ecosystem layer.

## Try it in the app

- **Window → Genetics + Molecular Biology Studio →
  Techniques → cloning** — 4 cloning entries.
- **OrgChem → Tools → Lab reagents** — restriction
  enzymes + ligases + competent cells.

This concludes the GM-3.0 intermediate tier.  Next:
**Mendelian + polygenic disease genetics** (advanced).
