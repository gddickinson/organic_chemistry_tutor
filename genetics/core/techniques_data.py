"""Phase GM-1.0 (round 230) — molecular-biology-techniques
catalogue data.

~ 36 entries spanning every major class of molecular-biology
technique.  Each entry is a long-form bench card.

Cross-references resolve to:
- biochem.core.enzymes ids (DNA polymerases / ligases / etc.;
  BC-1.0 catalogue is sparse on nucleic-acid enzymes — only
  ``dna-ligase-i`` is currently catalogued; the GM-1.0 entries
  reference what's there + leave hooks for future BC catalogue
  additions).
- cellbio.core.cell_cycle ids (chromatin / DDR / replication
  context).
- cellbio.core.cell_signaling ids (apoptosis / DDR / immunity
  pathways).
- animal.core.taxa ids (model organisms used to develop +
  validate techniques).
- orgchem.db.Molecule names (nucleobases + nucleosides +
  cofactors + dyes).

All cross-reference IDs verified at write time.  Validated
at test time so a future rename in any sibling catalogue
surfaces the broken edge immediately.
"""
from __future__ import annotations
from typing import Tuple

from genetics.core.techniques import MolecularBiologyTechnique


TECHNIQUES: Tuple[MolecularBiologyTechnique, ...] = (
    # ====================================================
    # PCR family
    # ====================================================
    MolecularBiologyTechnique(
        id="endpoint-pcr",
        name="Endpoint PCR (conventional PCR)",
        abbreviation="PCR",
        category="pcr",
        principle="Cyclic in-vitro DNA amplification using "
                  "a thermostable DNA polymerase, two flanking "
                  "primers, dNTPs + buffer.  Each cycle "
                  "(denature ~ 95 °C / anneal ~ 55-65 °C / "
                  "extend ~ 72 °C) doubles the target → "
                  "exponential amplification over 25-40 cycles.",
        sample_types="Genomic DNA, plasmids, cDNA, "
                     "environmental DNA, FFPE-derived DNA "
                     "(degraded).",
        throughput="96-384 reactions per thermocycler; "
                   "minutes-to-hours per run.",
        typical_readout="Agarose gel (presence / absence "
                        "+ size) or downstream sequencing / "
                        "cloning.",
        key_reagents="Taq DNA polymerase (or Phusion / "
                     "Q5 high-fidelity for cloning), dNTPs, "
                     "Mg²⁺, primers.",
        representative_platforms="Bio-Rad C1000 Touch, "
                                 "Eppendorf Mastercycler, "
                                 "Applied Biosystems "
                                 "ProFlex / SimpliAmp.",
        year_introduced="1985 (Mullis); commercial "
                        "thermocyclers ~ 1988.",
        key_references="Saiki et al. 1985 *Science*; "
                       "Mullis 1993 Nobel Prize in Chemistry.",
        strengths="Cheap, fast, exquisitely sensitive; can "
                  "amplify single template molecules.  "
                  "Foundation of every other amplification-"
                  "based technique.",
        limitations="Length-limited (~ 10 kb routinely; "
                    "~ 30 kb with long-range polymerases).  "
                    "Inhibited by SDS / EDTA / heparin / "
                    "haemoglobin.  Contamination risk → "
                    "dedicated workspace + UDG dUTP "
                    "anti-carryover system.",
        notes="The original molecular-biology workhorse.  "
              "Underpins cloning, diagnostic PCR, microbial "
              "ID, ancient DNA, COVID-19 testing.",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=("s-phase",),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(
            "Adenine", "Guanine", "Cytosine", "Thymine",
        ),
    ),
    MolecularBiologyTechnique(
        id="qpcr",
        name="Quantitative real-time PCR",
        abbreviation="qPCR / RT-qPCR",
        category="pcr",
        principle="PCR with continuous fluorescence "
                  "monitoring (SYBR Green double-strand "
                  "intercalator, or sequence-specific TaqMan "
                  "/ molecular-beacon probes).  Cycle "
                  "threshold (Ct) at which signal exceeds "
                  "baseline is inversely proportional to "
                  "log(starting template) → quantitative "
                  "over 6-7 orders of magnitude.",
        sample_types="DNA (cDNA after reverse "
                     "transcription) for gene-expression "
                     "studies; pathogen genomes for "
                     "diagnostic load monitoring.",
        throughput="96-384-1536-well plates; ~ 1-2 hours "
                   "per run.",
        typical_readout="Ct values; relative quantification "
                        "(2^-ΔΔCt) or absolute (standard "
                        "curve).",
        key_reagents="Reverse transcriptase (for RT-qPCR), "
                     "Taq polymerase, SYBR Green or TaqMan "
                     "probes, ROX passive reference.",
        representative_platforms="Applied Biosystems "
                                 "QuantStudio 7 Pro, "
                                 "Bio-Rad CFX96 / CFX384, "
                                 "Roche LightCycler 480, "
                                 "Qiagen RotorGene.",
        year_introduced="1992 (Higuchi); TaqMan 1996.",
        key_references="Higuchi et al. 1992; Heid et al. "
                       "1996; Bustin et al. 2009 MIQE "
                       "guidelines.",
        strengths="Quantitative + sensitive (~ 10 copies); "
                  "closed-tube → no contamination after "
                  "amplification; the workhorse of clinical "
                  "molecular diagnostics + gene-expression "
                  "validation.",
        limitations="Restricted to relatively short "
                    "amplicons (~ 70-150 bp).  Requires "
                    "reference-gene normalisation for "
                    "expression studies.  Probe design + "
                    "validation non-trivial.",
        notes="Backbone of clinical viral-load monitoring "
              "(HIV, HCV, HBV, CMV, SARS-CoV-2), microbial "
              "diagnostics (TB / chlamydia / gonorrhoea), "
              "pharmacogenomic genotyping, copy-number "
              "variation.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(
            "Adenine", "Methylene blue",
        ),
    ),
    MolecularBiologyTechnique(
        id="digital-pcr",
        name="Digital PCR",
        abbreviation="dPCR",
        category="pcr",
        principle="Sample is partitioned into thousands-"
                  "millions of nL-sized droplets / chambers; "
                  "each contains 0 or 1 (Poisson distribution) "
                  "template molecules.  Endpoint PCR + binary "
                  "fluorescence readout per partition + Poisson "
                  "math gives ABSOLUTE quantification without "
                  "standard curves.",
        sample_types="Cell-free DNA, viral DNA / RNA, rare "
                     "mutation alleles, copy-number variants.",
        throughput="~ 96 samples / instrument / day; ~ 20 K "
                   "droplets per sample (BioRad ddPCR).",
        typical_readout="Absolute concentration "
                        "(copies / µL).  Allele frequency "
                        "for mutation detection.",
        key_reagents="Taq polymerase, primers, TaqMan probes, "
                     "droplet-generation oil + surfactant.",
        representative_platforms="Bio-Rad QX600 ddPCR, "
                                 "Stilla naica, Qiagen "
                                 "QIAcuity, Thermo Absolute Q.",
        year_introduced="1999 (Vogelstein + Kinzler concept); "
                        "commercial droplet platforms ~ 2011.",
        key_references="Vogelstein + Kinzler 1999 *PNAS*; "
                       "Hindson et al. 2011 *Anal Chem*.",
        strengths="Absolute quantification + tolerance to PCR "
                  "inhibitors + rare-allele detection at "
                  "0.01-0.1 % vs background; gold standard "
                  "for liquid-biopsy MRD.",
        limitations="Higher per-sample cost; lower dynamic "
                    "range than qPCR for high-concentration "
                    "samples; instrument-vendor lock-in.",
        notes="Increasingly central to circulating-tumour-DNA "
              "monitoring + viral-load standards + GMO "
              "quantification.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="isothermal-amplification",
        name="Isothermal nucleic-acid amplification "
             "(LAMP / RPA / NASBA)",
        abbreviation="LAMP / RPA",
        category="pcr",
        principle="Amplifies DNA / RNA at a constant "
                  "temperature without thermocycling.  LAMP "
                  "(Loop-mediated, ~ 60-65 °C, Bst polymerase, "
                  "4-6 primers, dumbbell intermediate); RPA "
                  "(Recombinase Polymerase, ~ 37-42 °C, T4 "
                  "uvsX recombinase + strand-displacing "
                  "polymerase); NASBA (RNA-specific via "
                  "reverse transcriptase + RNase H + T7 "
                  "polymerase).",
        sample_types="Crude lysates + minimally-processed "
                     "samples (saliva, swabs, plant tissue).",
        throughput="Single-tube + portable; minutes per "
                   "reaction.",
        typical_readout="Turbidity (Mg-pyrophosphate "
                        "precipitate), fluorescence, "
                        "lateral-flow strip.",
        key_reagents="Bst polymerase (LAMP), recombinases + "
                     "Sau polymerase (RPA); reverse "
                     "transcriptase for RT-LAMP / NASBA.",
        representative_platforms="OptiGene + Eiken (LAMP), "
                                 "TwistDx + Abbott ID NOW "
                                 "(RPA / variant), Premier "
                                 "Biosoft + multiple POC "
                                 "instruments.",
        year_introduced="LAMP — 2000 (Notomi); RPA — 2006 "
                        "(Piepenburg); NASBA — 1991 "
                        "(Compton).",
        key_references="Notomi et al. 2000 *NAR*; "
                       "Piepenburg et al. 2006 *PLoS Biol*; "
                       "Compton 1991 *Nature*.",
        strengths="No thermocycler → battery / handheld "
                  "deployment in field + clinic + low-resource "
                  "settings.  COVID-19 LAMP tests (Lucira, "
                  "Mammoth-CRISPR-coupled).",
        limitations="Less specific than PCR; primer design "
                    "more constrained (4-6 primers for LAMP); "
                    "narrower published assay literature.",
        notes="Foundation of point-of-care molecular "
              "diagnostics + a complementary partner to "
              "CRISPR-Cas12 / Cas13 detection chemistry "
              "(SHERLOCK / DETECTR).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="sanger-sequencing",
        name="Sanger dideoxy sequencing",
        abbreviation="Sanger",
        category="sequencing",
        principle="DNA polymerase extends a primer along a "
                  "template; chain-terminating dideoxy-"
                  "nucleotides (ddNTPs, each labelled with a "
                  "distinct fluorophore in modern formats) "
                  "stop synthesis at every position → "
                  "fragments of every length.  Capillary "
                  "electrophoresis sorts by size; fluorescence "
                  "readout gives the base at each position.",
        sample_types="Plasmids, PCR amplicons, BAC inserts; "
                     "any clean dsDNA template.",
        throughput="~ 96-384 reactions per capillary instrument "
                   "per day; 600-1 000 bp per read.",
        typical_readout="Trace chromatogram + base-called "
                        "sequence.  Heterozygous SNPs visible "
                        "as overlapping peaks.",
        key_reagents="Thermostable DNA polymerase, ddNTPs "
                     "(four distinct dyes), primers.",
        representative_platforms="Applied Biosystems 3500 / "
                                 "3730 / SeqStudio; multiple "
                                 "service-lab providers.",
        year_introduced="1977 (Sanger + Coulson); fluorescent "
                        "+ capillary versions ~ 1986-1995.",
        key_references="Sanger et al. 1977 *PNAS*; Sanger 1980 "
                       "Nobel (his second!).",
        strengths="Long read (600-1 000 bp), high accuracy "
                  "(99.99 %), gold standard for clinical "
                  "variant confirmation.  Cheap per sample "
                  "(~ $5-10 from commercial labs).",
        limitations="Low throughput compared to NGS; "
                    "single-template-per-reaction (won't "
                    "deconvolute mixtures); ~ 10 % failure "
                    "rate on difficult templates.",
        notes="Drove the original Human Genome Project "
              "(completed 2003 with Sanger).  Still the "
              "REFERENCE method for clinical-grade "
              "variant confirmation in many labs.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(
            "Adenine", "Guanine", "Cytosine", "Thymine",
        ),
    ),
    MolecularBiologyTechnique(
        id="illumina-short-read",
        name="Illumina short-read sequencing-by-synthesis",
        abbreviation="Illumina SBS",
        category="sequencing",
        principle="Library DNA fragments are clonally "
                  "amplified into clusters on a flowcell via "
                  "bridge amplification.  Each cycle: a "
                  "single reversible-terminator dNTP "
                  "(blocked at 3'-OH) incorporated by "
                  "engineered polymerase; fluorescent label + "
                  "block removed before next cycle.  ~ 100-300 "
                  "cycles per read.",
        sample_types="Genomic DNA, cDNA, ChIP-DNA, ATAC-DNA, "
                     "amplicons; size-selected to 200-800 bp "
                     "library.",
        throughput="NovaSeq X Plus ~ 16 Tb / run / 2 days; "
                   "MiSeq ~ 15 Gb / run / 1 day.",
        typical_readout="FASTQ files; per-base quality scores "
                        "(Q30+); read lengths 75-300 bp; "
                        "paired-end common.",
        key_reagents="Reversible-terminator dNTPs (4 "
                     "fluorophores), engineered DNA "
                     "polymerase, cluster-generation reagents, "
                     "sequencing primers.",
        representative_platforms="Illumina NovaSeq X / X Plus, "
                                 "NextSeq 1000 / 2000, MiSeq, "
                                 "iSeq 100, NovaSeq 6000.",
        year_introduced="2006 (Solexa launch; Illumina "
                        "acquired 2007); modern dual-flow-cell "
                        "machines from ~ 2014.",
        key_references="Bentley et al. 2008 *Nature* "
                       "(method); Mardis 2008 *Annu Rev*.",
        strengths="Highest accuracy short-read platform "
                  "(Q30+ > 90 % of bases); cheapest per Gb "
                  "(~ $1-2 / Gb on NovaSeq X); broadest "
                  "ecosystem of library-prep kits + "
                  "bioinformatic pipelines.",
        limitations="Short reads (typically ≤ 300 bp) "
                    "struggle with structural variants, "
                    "repeats, phasing, full-isoform mRNAs.  "
                    "PCR-induced GC bias.  Index-hopping in "
                    "patterned-flowcell machines.",
        notes="Dominates the human genomics + transcriptomics "
              "+ population-scale sequencing landscape.  "
              "Foundation of UK Biobank, gnomAD, AllOfUs, "
              "TCGA.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="pacbio-hifi",
        name="PacBio HiFi (single-molecule real-time, "
             "circular consensus)",
        abbreviation="PacBio HiFi",
        category="sequencing",
        principle="Single DNA polymerase immobilised in a "
                  "zero-mode waveguide (ZMW); fluorescent "
                  "phospholinked dNTPs incorporated one at a "
                  "time, releasing pyrophosphate-fluorophore "
                  "into solution.  Circular template (SMRTbell "
                  "with hairpin adaptors) is read multiple "
                  "times → consensus sequence (HiFi) at "
                  "Q30+.",
        sample_types="High-molecular-weight gDNA (10-25 kb "
                     "library, sometimes 50 kb); Iso-Seq "
                     "for full-length cDNA.",
        throughput="Revio ~ 360 Gb / run, 4 SMRT cells; ~ 24 "
                   "hours.  Sequel IIe ~ 100 Gb.",
        typical_readout="HiFi reads of 10-25 kb at Q30+; "
                        "BAM with per-base methylation "
                        "calls (5mC + 6mA + 5hmC) "
                        "concurrent with sequence.",
        key_reagents="Phi29 polymerase derivative, "
                     "phospholinked dNTPs (4 colours), "
                     "SMRTbell adaptors.",
        representative_platforms="PacBio Revio (2023), "
                                 "Sequel IIe (2020), Onso "
                                 "(2023, short-read).",
        year_introduced="2010 (commercial PacBio RS); HiFi "
                        "2019 (Wenger et al.).",
        key_references="Eid et al. 2009 *Science* (SMRT); "
                       "Wenger et al. 2019 *Nat Biotechnol* "
                       "(HiFi).",
        strengths="Long + accurate (Q30+ at 10-25 kb); "
                  "concurrent native-DNA methylation calls; "
                  "ideal for de novo assembly, structural "
                  "variants, full-length isoform "
                  "transcriptomics.",
        limitations="Higher per-Gb cost than Illumina; "
                    "needs HMW DNA input; bioinformatic "
                    "ecosystem smaller than Illumina's.",
        notes="Underpins the modern T2T (telomere-to-"
              "telomere) human reference assembly + many "
              "non-human reference genomes; standard for "
              "structural-variant + repeat-region resolution.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="ont-nanopore",
        name="Oxford Nanopore Technologies sequencing",
        abbreviation="ONT",
        category="sequencing",
        principle="Single-stranded DNA (or RNA) is ratcheted "
                  "through a nanopore by a motor protein; "
                  "ionic-current modulation as each base "
                  "passes is interpreted by a basecaller "
                  "neural net.  Native DNA (no PCR) → reads "
                  "preserve methylation marks.",
        sample_types="HMW gDNA (any input length up to Mb-"
                     "scale ultra-long); native RNA "
                     "(direct-RNA-seq).",
        throughput="PromethION 48 ~ 14 Tb / run / 72 hrs; "
                   "MinION ~ 50 Gb / 72 hrs; portable + "
                   "USB-powered.",
        typical_readout="FASTQ / BAM; reads up to 4 Mb "
                        "demonstrated; Q20+ on R10.4 + "
                        "Dorado v0.5+ models; concurrent "
                        "modified-base calls.",
        key_reagents="Pore proteins (CsgG-derived R10.4), "
                     "motor enzyme, sequencing buffers, "
                     "library-prep kits (LSK + RAD + ULK + "
                     "etc.).",
        representative_platforms="ONT MinION, GridION, "
                                 "PromethION 24 / 48, Flongle, "
                                 "MK1C.",
        year_introduced="2014 (MinION early access); "
                        "PromethION 2017; R10.4 chemistry "
                        "+ Dorado basecaller 2022-2023.",
        key_references="Jain et al. 2018 *Nat Biotechnol*; "
                       "Wang et al. 2021 *Nat Methods* "
                       "(direct-RNA review).",
        strengths="Real-time base calling; very long reads; "
                  "portable (MinION fits in a pocket); "
                  "native modifications detected; cheap "
                  "instrument entry-cost.",
        limitations="Higher per-base error than Illumina or "
                    "PacBio HiFi (Q20 vs Q30+); per-Gb cost "
                    "competitive but variable; flow-cell "
                    "lifetime + reusability challenges.",
        notes="Excelled in pandemic surveillance (SARS-CoV-2 "
              "ARTIC + MinION amplicon sequencing in "
              "outbreaks; field-portable Ebola in West "
              "Africa 2014).  Foundation of T2T human + "
              "chimp assemblies via ultra-long reads.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="restriction-cloning",
        name="Restriction-enzyme cloning",
        abbreviation="REase cloning",
        category="cloning",
        principle="Cut insert + vector with the same "
                  "restriction enzyme(s) → compatible "
                  "cohesive or blunt ends → ligate with T4 "
                  "DNA ligase.  Classical recombinant DNA "
                  "approach since the 1970s.",
        sample_types="Plasmid + insert DNA (PCR product or "
                     "digested genomic).",
        throughput="Per-construct manual workflow; one "
                   "afternoon for digest + ligation + "
                   "transformation.",
        typical_readout="Transformed colonies → plasmid mini-"
                        "prep → diagnostic restriction digest "
                        "+ Sanger sequencing of the junction.",
        key_reagents="Type II restriction enzymes (EcoRI / "
                     "BamHI / HindIII / XhoI / SalI / NotI / "
                     "etc.), T4 DNA ligase, alkaline "
                     "phosphatase (CIP / SAP).",
        representative_platforms="NEB + Promega + Thermo "
                                 "restriction-enzyme catalogues "
                                 "(> 250 commercial Type II "
                                 "enzymes).",
        year_introduced="1973 (Cohen + Boyer + Berg "
                        "recombinant-DNA work); 1978 Nobel.",
        key_references="Cohen et al. 1973 *PNAS*; Berg, "
                       "Gilbert + Sanger 1980 Nobel; Maniatis "
                       "*Molecular Cloning* (book editions "
                       "from 1982).",
        strengths="Battle-tested + cheap.  Multi-piece "
                  "cloning + scarless options exist.  No "
                  "scarless requirement when sequence-tag "
                  "is acceptable.",
        limitations="Site-availability limited (must avoid "
                    "internal sites); slow for combinatorial "
                    "+ high-throughput libraries; "
                    "scarred junctions.",
        notes="The original recombinant-DNA technology — "
              "still routine for single-construct work + "
              "where scarless cloning isn't required.",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="gibson-assembly",
        name="Gibson assembly",
        abbreviation="Gibson",
        category="cloning",
        principle="Three enzymes in one isothermal (50 °C) "
                  "reaction: 5'→3' exonuclease chews back "
                  "ends → ssDNA overhangs anneal between "
                  "homologous regions → DNA polymerase + "
                  "DNA ligase repair → seamless multi-"
                  "fragment assembly.",
        sample_types="PCR-amplified fragments with "
                     "engineered ~ 20-40 bp homology arms "
                     "designed at every junction.",
        throughput="Multi-fragment (3-15+ pieces) in one "
                   "tube; ~ 1 hour incubation.",
        typical_readout="Transformed clones → mini-prep → "
                        "junction Sanger sequencing.",
        key_reagents="T5 exonuclease, Phusion polymerase, "
                     "Taq DNA ligase (the NEB master mix); "
                     "plus DpnI to remove parental template.",
        representative_platforms="NEB Gibson Assembly Master "
                                 "Mix (commercial standard); "
                                 "open-source homemade "
                                 "recipes ubiquitous.",
        year_introduced="2009 (Gibson et al., JCVI).",
        key_references="Gibson et al. 2009 *Nat Methods*; "
                       "Gibson 2011 *Methods Enzymol*.",
        strengths="Scarless, multi-fragment, sequence-"
                  "independent (no restriction sites needed).  "
                  "Foundation of the Synthetic Biology era.",
        limitations="Requires homology-arm primer design; "
                    "junctions with secondary structure or "
                    "high GC can fail; expensive at scale.",
        notes="Made the JCVI synthetic *M. mycoides* genome "
              "(2010) feasible.  Now the workhorse of "
              "synthetic-biology pathway assembly.",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="golden-gate",
        name="Golden Gate cloning + MoClo / GoldenBraid",
        abbreviation="Golden Gate",
        category="cloning",
        principle="Type IIS restriction enzymes (BsaI / "
                  "BsmBI / BbsI) cut OUTSIDE their recognition "
                  "sites → custom 4-nt overhangs.  All "
                  "fragments + destination vector cut + "
                  "ligated in one tube; T4 DNA ligase + "
                  "BsaI cycle alternately → recognition sites "
                  "DESTROYED in the assembly → favours "
                  "irreversible product formation.",
        sample_types="PCR-amplified or synthetic DNA parts "
                     "with BsaI / BsmBI sites + 4-nt "
                     "overhang design.",
        throughput="Multi-fragment (5-25+ pieces) in one "
                   "tube; ~ 1 hour cycle.  Hierarchical "
                   "assembly (level 0 → 1 → 2) for very "
                   "large constructs.",
        typical_readout="Transformed clones; standardised "
                        "MoClo / GoldenBraid syntactic "
                        "frameworks for plant + microbial "
                        "synthetic biology.",
        key_reagents="BsaI / BsmBI / BbsI (Type IIS), T4 DNA "
                     "ligase, ATP-containing buffer.",
        representative_platforms="NEB Golden Gate Assembly "
                                 "Kit; multiple academic "
                                 "MoClo / GoldenBraid / "
                                 "Loop / Mobius / GreenGate "
                                 "frameworks.",
        year_introduced="2008 (Engler et al.); MoClo 2011; "
                        "GoldenBraid 2011.",
        key_references="Engler et al. 2008 *PLoS ONE*; "
                       "Weber et al. 2011 *PLoS ONE* "
                       "(MoClo); Sarrion-Perdigones et al. "
                       "2013 *Plant Physiol* (GoldenBraid).",
        strengths="Modular + standardised + scalable to "
                  "many parts + cheap.  Plant + bacterial "
                  "synthetic-biology workhorse.",
        limitations="Forbidden internal Type IIS sites must "
                    "be domesticated out of every part; "
                    "framework-specific overhang grammar "
                    "required.",
        notes="Foundation of plant-synbio pipelines + "
              "increasingly mammalian (mClo) syntactic "
              "frameworks.",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="gateway-cloning",
        name="Gateway recombination cloning",
        abbreviation="Gateway",
        category="cloning",
        principle="Bacteriophage λ site-specific "
                  "recombination (att sites + Int + IHF + "
                  "Xis enzymes) shuffles inserts between "
                  "ENTRY clones + DESTINATION vectors via "
                  "BP + LR clonase reactions.  No "
                  "restriction enzymes; high efficiency; "
                  "the workhorse for parallel-construct "
                  "expression-vector swapping.",
        sample_types="PCR products or oligo-cloned ENTRY "
                     "clones with attB sites.",
        throughput="One-pot multi-construct shuffling; "
                   "high-throughput compatible.",
        typical_readout="Transformed clones with "
                        "destination-specific markers "
                        "(amp + ccdB negative selection).",
        key_reagents="BP clonase II + LR clonase II "
                     "enzyme mixes (proprietary), DNA "
                     "with attB / attP / attL / attR sites.",
        representative_platforms="Thermo / Invitrogen "
                                 "Gateway technology; many "
                                 "destination-vector "
                                 "collections (mammalian, "
                                 "yeast, plant, "
                                 "bacterial).",
        year_introduced="1997 (Hartley et al., "
                        "Invitrogen).",
        key_references="Hartley et al. 1997 *Genome Res*; "
                       "Walhout et al. 2000 *Methods "
                       "Enzymol* (large-scale ORFeome).",
        strengths="Scalable, modular destination-vector "
                  "library, no restriction-enzyme "
                  "constraints.  Underpins many "
                  "ORFeome libraries (HUMORFOME, "
                  "human-protein-cDNA collections).",
        limitations="att-site scars left in final "
                    "construct; proprietary enzymes; "
                    "expensive at scale; mostly "
                    "supplanted by Gibson / Golden Gate "
                    "for new construction.",
        notes="Still the dominant system for large "
              "academic ORFeome collections.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="crispr-cas9",
        name="CRISPR-Cas9 genome editing",
        abbreviation="CRISPR-Cas9",
        category="crispr",
        principle="A 20-nt single-guide RNA (sgRNA) "
                  "directs the Cas9 nuclease to a "
                  "complementary genomic site flanked by "
                  "an NGG protospacer-adjacent motif "
                  "(PAM).  Cas9 makes a blunt double-"
                  "strand break ~ 3 bp 5' of the PAM; "
                  "cellular repair (NHEJ → indel "
                  "knockouts; HDR → templated edits) "
                  "produces the engineered allele.",
        sample_types="Cell lines, primary cells, embryos, "
                     "in-vivo organs (delivery-method-"
                     "dependent), microbial cultures.",
        throughput="Per-target single experiment to "
                   "10⁵-target arrayed / pooled libraries "
                   "(Brunello / Brie / TKOv3 lentivirus "
                   "screens).",
        typical_readout="Editing efficiency by Sanger "
                        "(TIDE / ICE deconvolution), "
                        "amplicon-NGS, ddPCR, or "
                        "phenotypic screen.",
        key_reagents="SpCas9 protein or expression "
                     "plasmid / mRNA / lentivirus, sgRNA "
                     "(synthetic / IVT / cloned), "
                     "delivery vehicle (lipofection / "
                     "electroporation / virus / LNP).",
        representative_platforms="IDT Alt-R Cas9 RNP, "
                                 "Synthego, Aldevron Cas9, "
                                 "Genscript, Addgene "
                                 "vector deposits.",
        year_introduced="2012 (Doudna + Charpentier); "
                        "Doudna + Charpentier 2020 Nobel "
                        "Prize in Chemistry.",
        key_references="Jinek et al. 2012 *Science* "
                       "(method); Cong + Mali et al. "
                       "2013 *Science* (mammalian).",
        strengths="Programmable + cheap + scalable; "
                  "transformed every area of biology.  "
                  "Pooled CRISPR screens are now standard.  "
                  "Now FDA-approved as a therapeutic "
                  "(Casgevy for SCD + β-thal, Dec 2023).",
        limitations="Off-target cleavage (mitigated by "
                    "high-fidelity variants); imprecise "
                    "indel outcomes from NHEJ; HDR "
                    "low-efficiency in non-dividing cells; "
                    "PAM-availability constraint.",
        notes="See also AB-3.0 graduate \"Modern animal "
              "biotech + One Health\" lesson + MB-3.0 "
              "graduate \"CRISPR + microbial molecular "
              "biology\" lesson for therapeutic + "
              "evolutionary context.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(
            "g2-m-checkpoint", "intra-s-checkpoint",
        ),
        cross_reference_signaling_pathway_ids=(
            "p53",
        ),
        cross_reference_animal_taxon_ids=(
            "mus-musculus", "danio-rerio",
            "caenorhabditis-elegans",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="crispr-cas12a",
        name="CRISPR-Cas12a (Cpf1) genome editing",
        abbreviation="Cas12a",
        category="crispr",
        principle="Cas12a (formerly Cpf1) — a Class 2 "
                  "Type V effector — uses a single crRNA "
                  "(no tracrRNA needed), recognises "
                  "T-rich PAMs (TTTV), cleaves with "
                  "STAGGERED 5-nt 5' overhangs (vs Cas9's "
                  "blunt cuts), processes its own pre-"
                  "crRNA → multiplex from a single "
                  "transcript.",
        sample_types="Same as Cas9; particularly used in "
                     "AT-rich genomes (Plasmodium, "
                     "Drosophila intronic regions).",
        throughput="Same single-target to pooled-screen "
                   "scale as Cas9.",
        typical_readout="Same as Cas9.",
        key_reagents="LbCas12a (Lachnospiraceae) or "
                     "AsCas12a (Acidaminococcus) protein "
                     "/ mRNA; crRNA only.",
        representative_platforms="IDT Alt-R Cas12a RNP, "
                                 "academic Addgene "
                                 "deposits.",
        year_introduced="2015 (Zetsche + Zhang lab).",
        key_references="Zetsche et al. 2015 *Cell*; "
                       "Fonfara et al. 2016 *Nature* "
                       "(crRNA processing).",
        strengths="Multiplex from single transcript, "
                  "T-rich PAM expands targetable space, "
                  "smaller protein than Cas9 (~ 1 300 aa), "
                  "lower off-target rate in some studies.  "
                  "Basis of DETECTR diagnostics.",
        limitations="Less mature ecosystem than Cas9; "
                    "PAM still limits some loci; lower "
                    "nuclease activity in some cell types.",
        notes="DETECTR (Cas12-based diagnostic) + "
              "multiplex editing applications + plant "
              "biotech embraced Cas12a for crop trait "
              "stacking.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(
            "g2-m-checkpoint",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="base-editor",
        name="CRISPR base editors (CBE + ABE)",
        abbreviation="BE",
        category="crispr",
        principle="Catalytically-impaired Cas9 nickase "
                  "fused to a cytidine (CBE) or adenine "
                  "(ABE) deaminase.  Targets a 20-nt "
                  "site via sgRNA; deaminase converts "
                  "C → U (CBE; DNA repair fixes as C → "
                  "T) or A → I (ABE; fixes as A → G) "
                  "within a 5-7-nt activity window.  No "
                  "DSB → safer profile than nuclease "
                  "Cas9.",
        sample_types="Same as Cas9; widely used in HSCs "
                     "+ T cells + in-vivo liver + heart.",
        throughput="Per-target experiment to pooled "
                   "screens; clinical-stage in HSC + "
                   "in-vivo applications.",
        typical_readout="Editing % at target by amplicon "
                        "NGS; bystander-edit profiling; "
                        "off-target evaluation.",
        key_reagents="ABE7.10 / ABE8e / SpCas9-NG-ABE; "
                     "BE3 / BE4max / AID / APOBEC1-CBE; "
                     "+ sgRNA + delivery vehicle.",
        representative_platforms="Beam Therapeutics + "
                                 "Verve Therapeutics + "
                                 "Prime Medicine + "
                                 "academic deposits.",
        year_introduced="CBE — 2016 (Komor et al., Liu "
                        "lab); ABE — 2017 (Gaudelli et "
                        "al., Liu lab).",
        key_references="Komor et al. 2016 *Nature*; "
                       "Gaudelli et al. 2017 *Nature*; "
                       "Liu lab reviews.",
        strengths="Single-base precision without DSB; "
                  "better safety profile than nuclease "
                  "Cas9; clinical translation underway "
                  "(BEAM-101 SCD, VERVE-101 + 102 "
                  "PCSK9 FH).",
        limitations="Only 4 of 12 base substitutions "
                    "directly accessible (C↔T + A↔G); "
                    "bystander edits within window; PAM "
                    "constraints inherited from Cas9.",
        notes="The clinical breakthrough — first "
              "in-human in-vivo CRISPR drug (Verve VERVE-"
              "101 IND filed 2022, Phase 1b ongoing).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "mus-musculus", "homo-sapiens",
        ),
        cross_reference_molecule_names=(
            "Adenine", "Cytosine", "Guanine", "Thymine",
        ),
    ),
    MolecularBiologyTechnique(
        id="prime-editor",
        name="CRISPR prime editors (PE)",
        abbreviation="PE",
        category="crispr",
        principle="Cas9 nickase fused to a Moloney-MLV "
                  "reverse transcriptase + an extended "
                  "pegRNA (prime-editing guide RNA) "
                  "carrying both the spacer + a 3' "
                  "extension encoding the desired edit.  "
                  "Nicked target strand is reverse-"
                  "transcribed using the pegRNA template "
                  "→ all 12 base substitutions + small "
                  "insertions / deletions accessible "
                  "without DSB or donor template.",
        sample_types="Same as Cas9; in-vivo + ex-vivo "
                     "trials in liver + HSCs + retina.",
        throughput="Per-target single-experiment to "
                   "moderate-scale; iterative pegRNA "
                   "optimisation common.",
        typical_readout="Editing % + indel profile by "
                        "amplicon NGS.",
        key_reagents="PE2 / PE3 / PE4 / PE5 / PEmax / "
                     "TwinPE constructs; engineered "
                     "pegRNA.",
        representative_platforms="Prime Medicine "
                                 "(PM359 CGD trial), "
                                 "academic Addgene "
                                 "deposits.",
        year_introduced="2019 (Anzalone + Liu lab); "
                        "PE3 / PE4 / PE5 + PEmax 2020-"
                        "2022.",
        key_references="Anzalone et al. 2019 *Nature*; "
                       "Chen et al. 2021 *Cell* (PE4 / "
                       "PE5 + MMR evasion).",
        strengths="All 12 substitutions + small indels "
                  "without DSB or HDR; safer + more "
                  "versatile than base editors.  Prime "
                  "Medicine PM359 CGD CYBB editing — "
                  "first prime-editor clinical trial.",
        limitations="Lower efficiency than base editors "
                    "or nuclease Cas9; pegRNA design "
                    "non-trivial; large delivery payload "
                    "(~ 6.3 kb for PE2) constrains AAV.",
        notes="The flexible follow-on to base editors; "
              "complete the precision-editing toolkit.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="crispr-diagnostics",
        name="CRISPR diagnostics (SHERLOCK + DETECTR)",
        abbreviation="SHERLOCK / DETECTR",
        category="crispr",
        principle="Cas13 (RNA-targeting; SHERLOCK) or "
                  "Cas12 (DNA-targeting; DETECTR) bind a "
                  "specific nucleic-acid target via crRNA + "
                  "trigger COLLATERAL non-specific cleavage "
                  "of nearby reporter ssRNA / ssDNA → "
                  "fluorescent or lateral-flow signal.  "
                  "Coupled with isothermal amplification "
                  "(RPA + LAMP) for attomolar sensitivity.",
        sample_types="Crude clinical samples (saliva, swabs, "
                     "blood, urine); minimal pre-processing "
                     "for some assays.",
        throughput="Single-tube + portable + minutes-scale; "
                   "amenable to lateral-flow + microfluidic "
                   "+ paper-based formats.",
        typical_readout="Fluorescence (microplate) or "
                        "lateral-flow strip (binary) or "
                        "chip-based.",
        key_reagents="Cas13a (LwaCas13a) + Cas12a (LbCas12a) "
                     "+ ssRNA / ssDNA reporters + RPA / LAMP "
                     "amplification reagents.",
        representative_platforms="Sherlock Biosciences "
                                 "(SHERLOCK), Mammoth "
                                 "Biosciences (DETECTR + "
                                 "Cas14), academic "
                                 "deposits.",
        year_introduced="SHERLOCK — 2017 (Gootenberg + "
                        "Zhang); DETECTR — 2018 (Chen + "
                        "Doudna).",
        key_references="Gootenberg et al. 2017 *Science*; "
                       "Chen et al. 2018 *Science*; "
                       "Kaminski et al. 2021 *Nat Biomed "
                       "Eng* review.",
        strengths="Attomolar sensitivity + single-base "
                  "discrimination; portable + low-cost; "
                  "EUA-cleared for SARS-CoV-2 (multiple "
                  "platforms).",
        limitations="Sample-prep + amplification still "
                    "needed for crude samples; lateral-flow "
                    "format limits multiplexing; regulatory "
                    "approval pace.",
        notes="Pandemic-driven proof-of-concept; broader "
              "clinical adoption pending cost optimisation "
              "+ regulatory + lab integration.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="southern-blot",
        name="Southern blot",
        abbreviation="Southern",
        category="blot",
        principle="Genomic DNA is digested with restriction "
                  "enzymes, separated by agarose-gel "
                  "electrophoresis, denatured, transferred "
                  "(blotted) to a nylon membrane by capillary "
                  "action, then probed with a labelled DNA "
                  "/ RNA fragment.  Hybridisation to the "
                  "complementary band reveals presence + "
                  "size of the target.",
        sample_types="High-quality genomic DNA, BAC inserts; "
                     "5-20 µg per lane.",
        throughput="One gel + one membrane → 1-20 lanes; "
                   "1-3 days per blot.",
        typical_readout="Autoradiograph (³²P) or chemi-"
                        "luminescence (DIG / biotin); "
                        "single + multiple bands per "
                        "lane.",
        key_reagents="Restriction enzymes, denaturing + "
                     "neutralising buffers, nylon membrane, "
                     "labelled probe (random-primed, nick-"
                     "translated, or end-labelled).",
        representative_platforms="Mostly DIY workflows; "
                                 "GE / Roche DIG kits; "
                                 "membrane vendors "
                                 "(Hybond, Zeta-Probe).",
        year_introduced="1975 (Edwin Southern, *J Mol "
                        "Biol*).",
        key_references="Southern 1975 *J Mol Biol* (the "
                       "namesake paper); the workflow has "
                       "barely changed in 50 years.",
        strengths="Definitive for genomic restriction-"
                  "fragment-length polymorphism (RFLP), "
                  "transgene copy-number, restriction-"
                  "enzyme-site disruption + clonal "
                  "integration verification.",
        limitations="Slow + insensitive vs PCR; large DNA "
                    "input; declining usage with NGS.",
        notes="The Southern blot LIVES ON for transgene "
              "+ insertional-mutagenesis copy-number "
              "verification + RFLP + integration mapping "
              "where digital PCR / WGS aren't appropriate.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="northern-blot",
        name="Northern blot",
        abbreviation="Northern",
        category="blot",
        principle="RNA samples (total / poly-A) are "
                  "denatured + size-separated by formaldehyde "
                  "+ MOPS agarose gel, transferred to nylon "
                  "membrane, hybridised to a labelled "
                  "DNA / RNA probe.  Reveals transcript size "
                  "+ abundance + alternative splicing "
                  "products.",
        sample_types="Total RNA (5-20 µg) or poly-A-enriched "
                     "mRNA.",
        throughput="One gel + one membrane → 1-20 lanes; "
                   "2-3 days per blot.",
        typical_readout="Autoradiograph or chemi-"
                        "luminescence.  Multiple bands → "
                        "alternative isoforms or unspliced "
                        "vs spliced.",
        key_reagents="Formaldehyde-MOPS denaturing gel, "
                     "RNase-free everything, labelled probe.",
        representative_platforms="Mostly DIY; commercial "
                                 "membrane + kit options.",
        year_introduced="1977 (Alwine + Kemp + Stark).",
        key_references="Alwine et al. 1977 *PNAS*.",
        strengths="Direct visualisation of full-length "
                  "transcripts + alternative isoforms + "
                  "abundance estimation.",
        limitations="Insensitive (~ 0.1-1 ng / lane); "
                    "supplanted by qPCR + RNA-seq for most "
                    "purposes.  Still occasionally used for "
                    "non-coding-RNA + isoform validation.",
        notes="Less common today; lncRNA + microRNA labs "
              "still use occasionally.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="western-blot",
        name="Western blot (immunoblot)",
        abbreviation="Western",
        category="blot",
        principle="Proteins are SDS-denatured + size-"
                  "separated by PAGE, transferred (blotted) "
                  "to a PVDF or nitrocellulose membrane, "
                  "blocked, probed with a primary antibody, "
                  "then a labelled secondary antibody → "
                  "chemiluminescence / fluorescence "
                  "detection of the target protein band.",
        sample_types="Cell + tissue lysates; serum + plasma; "
                     "purified-protein fractions.",
        throughput="10-15 lanes per gel; 1-2 days per blot.",
        typical_readout="Band at expected MW + intensity "
                        "(qualitative / semi-quantitative); "
                        "loading-control normalisation; "
                        "imaging digitised by ChemiDoc / "
                        "Odyssey / similar.",
        key_reagents="SDS-PAGE running buffer, primary + "
                     "secondary antibodies (HRP / fluor-"
                     "conjugated), blocking buffers (BSA / "
                     "milk), ECL or fluorescent detection.",
        representative_platforms="Bio-Rad ChemiDoc + V3 "
                                 "Western blotting; "
                                 "LI-COR Odyssey Fc; "
                                 "automated systems "
                                 "(Wes / Sally Sue / "
                                 "iBright).",
        year_introduced="1979 (Towbin et al.; Renart "
                        "et al.).",
        key_references="Towbin et al. 1979 *PNAS* (the "
                       "method); Burnette 1981 *Anal "
                       "Biochem* (\"Western\" naming).",
        strengths="Specific + quantitative + workhorse "
                  "for protein-expression validation, "
                  "post-translational modification "
                  "detection (phospho-specific Abs), "
                  "biomarker quantification.",
        limitations="Antibody-dependent (validation a "
                    "perennial problem); semi-quantitative "
                    "at best; multiplexing limited "
                    "(Odyssey two-channel; capillary-"
                    "based 2-3 channel).",
        notes="Universal in molecular-biology labs.  "
              "Capillary-based automated systems (Wes) "
              "increasingly replace traditional "
              "membranes for routine work.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="fish",
        name="Fluorescence in-situ hybridisation",
        abbreviation="FISH",
        category="in-situ",
        principle="Fluorescently-labelled DNA / RNA probes "
                  "hybridise to complementary sequences in "
                  "fixed cells / tissue / chromosome "
                  "spreads.  Probe-target colocalisation "
                  "visualised by epifluorescence / "
                  "confocal microscopy reveals chromosome "
                  "structure, gene copy number, "
                  "translocation breakpoints.",
        sample_types="Fixed metaphase chromosome spreads, "
                     "interphase cells, paraffin-embedded "
                     "tissue (FFPE), embryos.",
        throughput="Slide-by-slide manual + microscope-"
                   "intensive; days per assay.",
        typical_readout="Fluorescence images with discrete "
                        "spots; counting ploidy or copy-"
                        "number; co-localisation revealing "
                        "translocations.",
        key_reagents="Labelled probes (BACs / fosmids / "
                     "synthesised oligonucleotide pools), "
                     "denaturing + hybridisation buffers, "
                     "DAPI counterstain.",
        representative_platforms="Multiple academic + "
                                 "commercial probe kits "
                                 "(Vysis / Abbott PathVysion "
                                 "for HER2, Oncor + Cytocell "
                                 "for clinical).",
        year_introduced="1980s (Pinkel et al.); routinely "
                        "diagnostic since ~ 1990s.",
        key_references="Pinkel et al. 1986 *PNAS*; Lichter "
                       "et al. 1990 *Hum Genet* (clinical "
                       "applications).",
        strengths="Single-molecule-resolution chromosome "
                  "+ gene-copy mapping; clinical workhorse "
                  "for HER2 amplification (breast cancer), "
                  "BCR-ABL translocation (CML), MLL / KMT2A "
                  "rearrangements (leukaemia).",
        limitations="Slow + low-throughput; antibody / "
                    "probe-design requires expertise; "
                    "limited multiplexing (4-7 colours "
                    "typical).",
        notes="The clinical-cytogenetics workhorse; "
              "increasingly complemented by chromosomal "
              "microarrays + WGS karyotyping.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(
            "m-phase",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="smfish-merfish",
        name="Single-molecule + multiplexed FISH "
             "(smFISH / MERFISH / seqFISH)",
        abbreviation="smFISH / MERFISH",
        category="in-situ",
        principle="smFISH — multiple short fluorescent "
                  "oligonucleotide probes tile a single "
                  "transcript → single-molecule punctate "
                  "spots.  MERFISH / seqFISH — combinatorial "
                  "barcoding across multiple imaging rounds "
                  "encodes hundreds-thousands of distinct "
                  "RNAs in the same sample.",
        sample_types="Fixed cells + tissue sections; "
                     "compatible with most cell types + "
                     "many tissue preparations.",
        throughput="MERFISH — ~ 10K cells × ~ 1 K genes "
                   "per imaging session; weeks-months for "
                   "atlas-scale work.",
        typical_readout="Sub-cellular RNA-spot maps + "
                        "quantification; spatial cell-type "
                        "identification.",
        key_reagents="Massive oligonucleotide-probe pools "
                     "(IDT / Twist), encoding + readout "
                     "probes, fluorescent secondary probes.",
        representative_platforms="Vizgen MERSCOPE "
                                 "(commercial MERFISH), "
                                 "Resolve Biosciences "
                                 "Molecular Cartography, "
                                 "academic imaging "
                                 "setups.",
        year_introduced="smFISH — 1998 (Femino + Singer); "
                        "MERFISH — 2015 (Chen + Zhuang); "
                        "seqFISH — 2014 (Lubeck + Cai).",
        key_references="Femino et al. 1998 *Science*; "
                       "Chen et al. 2015 *Science* "
                       "(MERFISH).",
        strengths="Single-molecule spatial transcriptomics "
                  "at sub-cellular resolution; preserves "
                  "tissue context; quantitative.",
        limitations="Slow imaging (hours-days per sample); "
                    "expensive instrument + reagents; "
                    "library design + analysis "
                    "computationally intensive.",
        notes="Foundational technology for the spatial-"
              "transcriptomics revolution.  Increasingly "
              "embedded in tissue atlases (HuBMAP, BICCN, "
              "Allen Brain).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="chip-seq",
        name="Chromatin immunoprecipitation sequencing",
        abbreviation="ChIP-seq",
        category="chromatin",
        principle="Cells are crosslinked (formaldehyde) → "
                  "chromatin sheared (sonication or MNase) "
                  "→ specific TF / histone-modification "
                  "antibody pulls down associated DNA "
                  "fragments → reverse crosslinks → DNA "
                  "purified → NGS library + sequencing.  "
                  "Read pile-up identifies bound genomic "
                  "regions.",
        sample_types="10⁵-10⁷ fixed cells; recently as low "
                     "as 10² with low-input variants.",
        throughput="~ 1-10 samples per ChIP setup; days-"
                   "to-weeks per dataset.",
        typical_readout="Genome-wide bedGraph / bigWig of "
                        "ChIP signal + called peaks; "
                        "differential ChIP between "
                        "conditions.",
        key_reagents="Formaldehyde, ChIP-grade antibodies "
                     "(validated!), Protein A / G "
                     "magnetic beads, library-prep kit.",
        representative_platforms="Mostly DIY workflows; "
                                 "commercial automated kits "
                                 "from Diagenode, Active "
                                 "Motif.",
        year_introduced="ChIP — late 1980s; ChIP-seq — "
                        "2007 (Robertson + Mikkelsen et "
                        "al.).",
        key_references="Johnson et al. 2007 *Science*; "
                       "Mikkelsen et al. 2007 *Nature*; "
                       "ENCODE Consortium standards.",
        strengths="Genome-wide mapping of transcription-"
                  "factor binding + histone modifications "
                  "+ chromatin states.  Foundation of "
                  "ENCODE + Roadmap Epigenomics + IHEC "
                  "consortia.",
        limitations="Antibody-dependent; high input + "
                    "crosslinking artefacts + signal-to-"
                    "noise issues; supplanted by CUT&RUN "
                    "/ CUT&Tag for many uses.",
        notes="Traditional + still widely-cited but "
              "increasingly replaced by lower-input + "
              "higher-resolution successors (CUT&RUN / "
              "CUT&Tag).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(
            "g1-phase", "s-phase",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="cut-and-run",
        name="CUT&RUN + CUT&Tag chromatin profiling",
        abbreviation="CUT&RUN / CUT&Tag",
        category="chromatin",
        principle="CUT&RUN — primary antibody binds "
                  "specific TF / histone mark in "
                  "permeabilised cells; protein A / G — MNase "
                  "fusion is recruited + cleaves nearby "
                  "chromatin → small fragments diffuse out; "
                  "CUT&Tag — protein A — Tn5 transposase "
                  "fusion tagments DNA in situ → ready-to-"
                  "sequence libraries.  Lower input + "
                  "background than ChIP-seq.",
        sample_types="10²-10⁵ cells (CUT&Tag); single-cell "
                     "(scCUT&Tag); fresh / lightly-fixed "
                     "tissue.",
        throughput="High; days-scale workflow; amenable to "
                   "single-cell + 96-well automation.",
        typical_readout="Same as ChIP-seq (peaks, signal "
                        "tracks, differential binding).",
        key_reagents="pA-MNase (CUT&RUN) or pA-Tn5 "
                     "(CUT&Tag) fusion proteins; "
                     "antibodies; NGS library prep "
                     "(simpler than ChIP-seq).",
        representative_platforms="EpiCypher CUTANA, Active "
                                 "Motif, academic "
                                 "Henikoff-lab protocols.",
        year_introduced="CUT&RUN — 2017 (Skene + "
                        "Henikoff); CUT&Tag — 2019 (Kaya-"
                        "Okur + Henikoff).",
        key_references="Skene + Henikoff 2017 *eLife*; "
                       "Kaya-Okur et al. 2019 *Nat "
                       "Commun*.",
        strengths="100-1000× lower input + lower background "
                  "than ChIP-seq; faster + cheaper; "
                  "compatible with single-cell.  Now the "
                  "de-facto standard in many chromatin "
                  "labs.",
        limitations="MNase digestion bias; antibody "
                    "validation still important; less "
                    "mature analysis pipelines than ChIP-"
                    "seq.",
        notes="Henikoff lab's chromatin-profiling "
              "successor lineage; rapidly displacing "
              "ChIP-seq for new work.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="atac-seq",
        name="Assay for transposase-accessible chromatin "
             "by sequencing",
        abbreviation="ATAC-seq",
        category="chromatin",
        principle="Hyperactive Tn5 transposase "
                  "preferentially inserts sequencing-"
                  "adaptor cassettes into open / accessible "
                  "chromatin in living or lightly-fixed "
                  "cells.  Resulting fragments are PCR-"
                  "amplified + sequenced; read pile-up maps "
                  "open-chromatin regions genome-wide.",
        sample_types="50 K-100 K cells (bulk); 1 K cells "
                     "(low-input); single-cell scATAC-seq "
                     "(10x Multiome, sci-ATAC).",
        throughput="Bulk: 8-16 samples per day; single-"
                   "cell: 10K cells per run.",
        typical_readout="Genome-wide open-chromatin peaks; "
                        "TF-binding-site footprints; "
                        "differential accessibility between "
                        "states.",
        key_reagents="Tn5 transposase loaded with adaptors "
                     "(Illumina Nextera-style); lysis "
                     "buffer; PCR amplification.",
        representative_platforms="Illumina Nextera + Tn5 "
                                 "(in-house) for bulk; "
                                 "10x Genomics Chromium "
                                 "Multiome / Single Cell "
                                 "ATAC for single-cell.",
        year_introduced="2013 (Buenrostro + Greenleaf "
                        "lab).",
        key_references="Buenrostro et al. 2013 *Nat "
                       "Methods*; Buenrostro et al. 2015 "
                       "*Nature* (single-cell).",
        strengths="Low input + fast (~ 4 hours from cells "
                  "to library); single-cell-compatible; "
                  "infers TF binding via footprinting; "
                  "cleaner than DNase-seq for many "
                  "applications.",
        limitations="Per-base resolution ~ 10-20 nt; "
                    "tagmentation bias; mitochondrial-DNA "
                    "contamination; PCR amplification "
                    "duplicates.",
        notes="The dominant chromatin-accessibility assay "
              "since ~ 2015; single-cell ATAC is the "
              "epigenomic complement to scRNA-seq in "
              "modern atlases.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="bulk-rna-seq",
        name="Bulk RNA sequencing",
        abbreviation="bulk RNA-seq",
        category="transcriptomics",
        principle="Total RNA extracted from a sample → "
                  "rRNA depletion (Ribo-Zero / RNase H) "
                  "or poly-A enrichment → cDNA synthesis → "
                  "library prep + Illumina sequencing.  "
                  "Read alignment + counting per gene → "
                  "expression matrix.",
        sample_types="100 ng-1 µg total RNA from cells / "
                     "tissue; FFPE-compatible with "
                     "specialised library prep.",
        throughput="96-384 samples per Illumina run; "
                   "~ 30 M reads / sample typical.",
        typical_readout="Gene-expression matrix (counts "
                        "per gene per sample); "
                        "differential expression analysis "
                        "(DESeq2 / edgeR / limma).",
        key_reagents="rRNA-depletion or poly-A capture "
                     "kit (NEBNext / Illumina TruSeq / "
                     "Lexogen QuantSeq), reverse "
                     "transcriptase, library-prep enzymes.",
        representative_platforms="Illumina NovaSeq + "
                                 "NextSeq for sequencing; "
                                 "library kits from "
                                 "NEBNext / Illumina / "
                                 "Lexogen / Tecan.",
        year_introduced="2008 (Mortazavi et al.; Cloonan "
                        "et al.; Marioni et al.; Nagalakshmi "
                        "et al.).",
        key_references="Mortazavi et al. 2008 *Nat "
                       "Methods*; Conesa et al. 2016 "
                       "*Genome Biol* (best-practice "
                       "review).",
        strengths="Genome-wide expression; quantitative; "
                  "isoform + splicing analysis (with "
                  "longer reads); the foundation of modern "
                  "transcriptomics.",
        limitations="Bulk averages obscure cell-type "
                    "heterogeneity; sample-prep effects "
                    "(rRNA depletion vs poly-A bias); "
                    "computationally non-trivial at "
                    "scale.",
        notes="The workhorse for differential-expression "
              "studies + clinical transcriptomics + "
              "ENCODE / GTEx / TCGA / FANTOM consortia.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="scrna-seq",
        name="Single-cell RNA sequencing",
        abbreviation="scRNA-seq",
        category="transcriptomics",
        principle="Cells are partitioned (droplet, "
                  "well-plate, or split-pool) → each cell's "
                  "mRNA is barcoded with a unique cellular "
                  "+ molecular identifier (CB + UMI) → "
                  "pooled reverse transcription + library "
                  "prep + sequencing → gene-by-cell "
                  "expression matrix.",
        sample_types="Dissociated single-cell suspensions "
                     "from tissues, cultured cells, blood, "
                     "tumour samples.",
        throughput="10× Chromium ~ 10 K cells / channel; "
                   "Parse Bio ~ 1 M cells / experiment "
                   "(combinatorial barcoding); BD Rhapsody "
                   "+ many academic platforms.",
        typical_readout="Gene-by-cell expression matrix; "
                        "cell-type clustering (UMAP / "
                        "Leiden); marker-gene analysis; "
                        "trajectory inference; integration "
                        "across samples.",
        key_reagents="10x Chromium chip + reagents (V3 / "
                     "V4 chemistry); Parse Bio Pipeline-V3 "
                     "kit (split-pool); BD Rhapsody "
                     "cartridge.",
        representative_platforms="10x Chromium Connect / "
                                 "X / Next; Parse Bio "
                                 "Evercode; BD Rhapsody "
                                 "Express; Singleron.",
        year_introduced="Drop-seq + InDrops + 10x "
                        "Chromium — 2015-2016; Smart-seq "
                        "earlier (2013).",
        key_references="Macosko et al. 2015 *Cell* "
                       "(Drop-seq); Klein et al. 2015 "
                       "*Cell* (InDrops); Zheng et al. "
                       "2017 *Nat Commun* (10x).",
        strengths="Cell-type discovery + cell-state "
                  "transitions + tissue heterogeneity at "
                  "scale; foundation of HCA + BICCN + "
                  "HuBMAP atlases + tumour heterogeneity "
                  "studies.",
        limitations="Sparse data per cell (1-10 K "
                    "transcripts); doublet contamination; "
                    "dissociation stress alters "
                    "expression; computationally "
                    "intensive analysis.",
        notes="The technology that revolutionised cell "
              "biology in the late 2010s; > 5 000 single-"
              "cell mammalian cell types catalogued.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "mus-musculus", "homo-sapiens",
            "danio-rerio", "drosophila-melanogaster",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="ribo-seq",
        name="Ribosome profiling (Ribo-seq)",
        abbreviation="Ribo-seq",
        category="transcriptomics",
        principle="In-cell translation snapshot: "
                  "cycloheximide arrest → cell lysis → "
                  "RNase digestion of unprotected mRNA "
                  "→ ribosome-protected ~ 28-30-nt "
                  "fragments isolated by sucrose gradient "
                  "→ rRNA depletion + library prep + "
                  "sequencing → genome-wide map of "
                  "translating ribosomes at codon "
                  "resolution.",
        sample_types="Living cells (~ 10⁶-10⁷); "
                     "drug-perturbation studies common.",
        throughput="One sample per day-per-person; "
                   "8-12 samples per Illumina run.",
        typical_readout="Codon-resolution ribosome "
                        "occupancy; novel ORFs (uORFs, "
                        "non-canonical proteome); "
                        "translation efficiency.",
        key_reagents="Cycloheximide / harringtonine / "
                     "lactimidomycin (initiator codon "
                     "trapping); RNase I / micrococcal "
                     "nuclease; sucrose gradient.",
        representative_platforms="Mostly DIY workflows "
                                 "based on Ingolia + "
                                 "Weissman protocols.",
        year_introduced="2009 (Ingolia + Weissman).",
        key_references="Ingolia et al. 2009 *Science*; "
                       "Brar + Weissman 2015 *Nat Rev "
                       "Mol Cell Biol* (review).",
        strengths="Direct readout of translation (vs "
                  "RNA abundance); reveals uORFs + non-"
                  "canonical ORFs + ribosome stalling + "
                  "translation regulation.",
        limitations="Technically demanding; "
                    "cycloheximide-induced artefacts; "
                    "computationally intensive (read-"
                    "frame analysis, P-site offset "
                    "calling).",
        notes="Foundation of the \"non-canonical "
              "proteome\" discovery era; > 10 K novel "
              "small ORFs catalogued in human + mouse.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="visium-spatial",
        name="10x Genomics Visium spatial transcriptomics",
        abbreviation="Visium",
        category="spatial",
        principle="Tissue section placed on a slide with "
                  "~ 5 K barcoded poly-T capture spots "
                  "(55 µm diameter, 100 µm centre-to-"
                  "centre).  Tissue permeabilised in situ "
                  "→ poly-A mRNA hybridises to nearest "
                  "spot → reverse transcription captures "
                  "the spatial barcode → library prep + "
                  "sequencing → expression matrix indexed "
                  "by spatial coordinates.",
        sample_types="Fresh-frozen + FFPE tissue sections "
                     "(7-10 µm thick); CytAssist + Visium "
                     "HD enable broader sample types + "
                     "higher resolution.",
        throughput="2-4 samples per slide; ~ 5 K spots "
                   "per sample; days-scale workflow.",
        typical_readout="Spatially-indexed gene-expression "
                        "matrix; histology-overlaid "
                        "expression maps; spatially-"
                        "variable genes; cell-type "
                        "deconvolution per spot.",
        key_reagents="Visium Spatial Gene Expression "
                     "slides + reagent kits.",
        representative_platforms="10x Genomics Visium + "
                                 "Visium HD + Visium "
                                 "CytAssist.",
        year_introduced="Spatial Transcriptomics — 2016 "
                        "(Ståhl et al.); 10x Visium — "
                        "2019; Visium HD — 2024.",
        key_references="Ståhl et al. 2016 *Science*; "
                       "Marx 2021 *Nat Methods* "
                       "(spatial-transcriptomics review).",
        strengths="Whole-transcriptome spatial coverage; "
                  "preserves tissue morphology; species-"
                  "agnostic; integrates with histology.",
        limitations="Spot-level (vs cell-level) "
                    "resolution in standard Visium "
                    "(~ 1-10 cells per spot); "
                    "expensive (~ $4-7K per slide).",
        notes="The spot-based-spatial workhorse; "
              "complemented by image-based MERFISH / "
              "Xenium / CosMx for sub-cellular "
              "resolution.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="bottom-up-proteomics",
        name="Bottom-up shotgun proteomics (LC-MS/MS)",
        abbreviation="LC-MS/MS",
        category="proteomics",
        principle="Proteins extracted, denatured, reduced "
                  "+ alkylated, digested with trypsin → "
                  "peptide mixture → LC separation → ESI "
                  "ionisation → MS1 mass spectrum + MS2 "
                  "fragmentation → peptide identification "
                  "via database search; protein inference "
                  "from peptide hits.",
        sample_types="Cell + tissue lysates; "
                     "immunoprecipitates; subcellular "
                     "fractions; serum / plasma; "
                     "FFPE-compatible with specialised "
                     "extraction.",
        throughput="~ 1-3 samples per day per LC-MS; "
                   "DIA + TMT multiplexing accelerate; "
                   "Evosep One ~ 60-300 samples / day "
                   "high-throughput.",
        typical_readout="Identified + quantified "
                        "proteins (~ 5-10 K per sample "
                        "in deep proteomes); PTM "
                        "localisation + quantification "
                        "with enrichment.",
        key_reagents="Trypsin / LysC, MS-grade water + "
                     "ACN, TMT / iTRAQ for multiplexing, "
                     "stable-isotope-labelled standards "
                     "for absolute quant.",
        representative_platforms="Thermo Orbitrap "
                                 "Astral + Eclipse + "
                                 "Exploris; Bruker "
                                 "timsTOF Pro / SCP / "
                                 "Ultra; SCIEX QTRAP / "
                                 "ZenoTOF.",
        year_introduced="Foundational MS work 1990s; "
                        "Orbitrap 2005; modern proteomics "
                        "from ~ 2010.",
        key_references="Aebersold + Mann 2003 *Nature*; "
                       "Aebersold + Mann 2016 *Nature* "
                       "(decade-on review).",
        strengths="Genome-scale protein identification + "
                  "PTM mapping + interaction-partner "
                  "identification; the only direct readout "
                  "of the proteome.",
        limitations="Stochastic data-dependent "
                    "acquisition; dynamic-range "
                    "limitations; missing-value "
                    "imputation; expensive instrument.",
        notes="Complementary to RNA-seq.  Single-cell "
              "proteomics + spatial proteomics emerging "
              "via SCP-Orbitrap + DVP (Mann lab) + "
              "Evosep + timsTOF SCP.",
        cross_reference_enzyme_ids=(
            "trypsin", "chymotrypsin",
        ),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="proximity-labelling",
        name="Proximity-dependent biotin labelling "
             "(BioID + TurboID + APEX)",
        abbreviation="BioID / TurboID / APEX",
        category="proteomics",
        principle="A promiscuous biotin ligase (BioID — "
                  "BirA*; TurboID — directed-evolution "
                  "fast variant) or peroxidase (APEX2) "
                  "fused to a bait protein → biotinylates "
                  "proteins within ~ 10 nm radius in "
                  "living cells → streptavidin pulldown + "
                  "MS/MS identifies proximal proteome.  "
                  "Captures transient + weak interactions "
                  "missed by AP-MS.",
        sample_types="Living cells expressing the bait "
                     "fusion; tissue (limited).",
        throughput="Per-bait single-experiment to "
                   "moderate-scale (10-100 baits per "
                   "atlas project).",
        typical_readout="Biotinylated proteome list with "
                        "quantitative proximity scores; "
                        "compartment + complex topology.",
        key_reagents="BioID / BioID2 / TurboID / miniTurbo "
                     "/ APEX2 fusion-bait constructs; "
                     "biotin (BioID + TurboID) or biotin-"
                     "phenol + H2O2 (APEX); streptavidin "
                     "beads.",
        representative_platforms="Mostly DIY workflows; "
                                 "Addgene deposits; "
                                 "expert labs (Roux + "
                                 "Ting).",
        year_introduced="BioID — 2012 (Roux + Burke); "
                        "APEX — 2013 (Rhee + Ting); "
                        "TurboID — 2018 (Branon + Ting).",
        key_references="Roux et al. 2012 *J Cell Biol*; "
                       "Rhee et al. 2013 *Science*; "
                       "Branon et al. 2018 *Nat "
                       "Biotechnol*.",
        strengths="Captures transient + low-affinity + "
                  "compartment-specific interactions; "
                  "in-vivo labelling possible (TurboID "
                  "in flies + worms + zebrafish + mouse).",
        limitations="Bait-fusion expression artefacts; "
                    "biotin background in serum / media; "
                    "spatial resolution ~ 10 nm; "
                    "non-quantitative for absolute "
                    "stoichiometry.",
        notes="The proximity-labelling field is "
              "expanding rapidly; spatial proteomics "
              "via APEX-MS + tissue-tomography "
              "applications.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="yeast-two-hybrid",
        name="Yeast two-hybrid + variants",
        abbreviation="Y2H",
        category="interaction",
        principle="Two proteins (X + Y) fused respectively "
                  "to a transcription-factor DNA-binding "
                  "domain (DBD) + activation domain (AD).  "
                  "Interaction in yeast nucleus reconstitutes "
                  "a functional TF → activates a reporter "
                  "(HIS3 / ADE2 / lacZ) → growth on "
                  "selective medium or colour change.",
        sample_types="cDNA libraries (random) or curated "
                     "ORFeome libraries against bait "
                     "proteins of interest.",
        throughput="Library-vs-bait screens against "
                   "10⁵-10⁷ prey clones; high-throughput "
                   "automated.",
        typical_readout="List of interactor proteins "
                        "(yeast colonies sequenced); "
                        "validated by complementary "
                        "methods.",
        key_reagents="Yeast strains (Y2H Gold, AH109); "
                     "bait + prey vector pairs (pGBKT7 + "
                     "pGADT7); cDNA libraries.",
        representative_platforms="Hybrigenics + DualSystems "
                                 "+ academic high-throughput "
                                 "consortia (Vidal lab "
                                 "ORFeome + interactome).",
        year_introduced="1989 (Fields + Song).",
        key_references="Fields + Song 1989 *Nature*; "
                       "Rolland et al. 2014 *Cell* (HuRI "
                       "human reference interactome).",
        strengths="Genome-wide interactome screening; "
                  "binary interaction calls; cheap + "
                  "scalable; live-cell context.",
        limitations="High false-positive + false-negative "
                    "rates (~ 50 % validation); "
                    "membrane / mitochondrial proteins "
                    "challenging; misses transient "
                    "interactions.",
        notes="Foundation of HuRI (~ 64 K human protein-"
              "protein interactions).  Increasingly "
              "complemented by AP-MS + BioID + "
              "AlphaFold-Multimer predictions.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="hi-c",
        name="Hi-C + Micro-C 3D-genome conformation "
             "capture",
        abbreviation="Hi-C / Micro-C",
        category="structural",
        principle="Crosslink chromatin → digest with "
                  "restriction enzyme (Hi-C) or MNase "
                  "(Micro-C) → biotinylate cut ends → "
                  "ligate adjacent fragments → enrich "
                  "biotinylated junctions → NGS library + "
                  "sequencing → contact-frequency matrix "
                  "between every pair of genomic loci → "
                  "TADs, compartments, loops.",
        sample_types="10⁵-10⁷ fixed cells; single-cell "
                     "Hi-C also published.",
        throughput="One sample per ~ 1-2 weeks; deep "
                   "sequencing (~ 1-2 Bn reads) needed for "
                   "loop-resolution.",
        typical_readout="Contact matrix at 1-50 kb "
                        "resolution; TAD calls; A/B "
                        "compartments; chromatin loops + "
                        "anchors.",
        key_reagents="Restriction enzyme (HindIII / DpnII "
                     "/ MboI for Hi-C; MNase for Micro-C); "
                     "biotin-dCTP / dATP; T4 DNA ligase; "
                     "biotin pulldown beads.",
        representative_platforms="Mostly DIY; Arima "
                                 "Genomics + Phase Genomics "
                                 "+ Dovetail kits "
                                 "(in-solution + "
                                 "scaffolding for "
                                 "assembly).",
        year_introduced="Hi-C — 2009 (Lieberman-Aiden et "
                        "al.); Micro-C — 2015 (Hsieh et "
                        "al.).",
        key_references="Lieberman-Aiden et al. 2009 "
                       "*Science*; Rao et al. 2014 *Cell* "
                       "(deep Hi-C + loop calling).",
        strengths="Genome-wide 3D organisation; "
                  "complements ATAC + ChIP for "
                  "regulatory-landscape interpretation; "
                  "supports genome-assembly scaffolding.",
        limitations="Deep sequencing needed; "
                    "computationally intensive; "
                    "single-cell Hi-C is sparse + "
                    "challenging.",
        notes="Foundation of TAD + compartment "
              "concepts.  4D Nucleome consortium + "
              "ENCODE phase 4 generated reference "
              "datasets.",
        cross_reference_enzyme_ids=("dna-ligase-i",),
        cross_reference_cell_cycle_ids=(
            "g1-phase", "m-phase",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="bisulfite-seq",
        name="Bisulfite sequencing (DNA methylation "
             "profiling)",
        abbreviation="BS-seq / WGBS",
        category="epigenetics",
        principle="Sodium bisulfite deaminates "
                  "unmethylated cytosines to uracil → "
                  "PCR-amplified as thymine; methylated "
                  "(5-mC) cytosines unaffected → remain "
                  "as cytosine.  NGS sequencing + "
                  "alignment-aware methylation calling "
                  "identifies CpG (and non-CpG) "
                  "methylation at single-base resolution.",
        sample_types="High-quality genomic DNA (1-5 µg "
                     "for WGBS; less for RRBS); FFPE "
                     "compatible.",
        throughput="WGBS → 100 Gb / sample for 30× human "
                   "coverage; RRBS targets ~ 10 % of "
                   "CpGs at lower depth.",
        typical_readout="Per-CpG methylation "
                        "(unmethylated / partially / "
                        "fully methylated); "
                        "differentially methylated "
                        "regions (DMRs); methylome "
                        "atlases.",
        key_reagents="Sodium bisulfite (or EM-seq "
                     "alternative — TET2 enzymatic "
                     "methylation conversion; Vaisvila et "
                     "al. 2021); library-prep kit.",
        representative_platforms="Zymo EZ DNA Methylation "
                                 "Gold / Lightning kits; "
                                 "NEB EM-seq (enzymatic "
                                 "alternative without DNA "
                                 "damage); Illumina "
                                 "Methylation EPIC array "
                                 "for cost-effective "
                                 "genome-scale.",
        year_introduced="Bisulfite — 1992 (Frommer et "
                        "al.); WGBS — 2008 (Lister et "
                        "al.); EM-seq — 2021.",
        key_references="Frommer et al. 1992 *PNAS*; "
                       "Lister et al. 2008 *Cell*; "
                       "Vaisvila et al. 2021 *Genome Res* "
                       "(EM-seq).",
        strengths="Single-base 5-mC + 5-hmC resolution; "
                  "WGBS the gold standard for methylome "
                  "studies (ENCODE, Roadmap Epigenomics, "
                  "IHEC).",
        limitations="Bisulfite damages DNA → fragmentation "
                    "+ uneven coverage; expensive at WGS "
                    "scale; 5-mC vs 5-hmC distinguished "
                    "only by oxBS or TAB-seq.",
        notes="EM-seq (NEB enzymatic methyl-seq) is the "
              "modern bisulfite-free alternative — "
              "cleaner data + lower input + same per-CpG "
              "resolution.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(
            "Cytosine",
        ),
    ),
    MolecularBiologyTechnique(
        id="lipid-nanoparticle-delivery",
        name="Lipid-nanoparticle (LNP) RNA delivery",
        abbreviation="LNP",
        category="delivery",
        principle="Synthetic mRNA / sgRNA / siRNA "
                  "encapsulated in lipid nanoparticles "
                  "composed of an ionisable lipid + "
                  "cholesterol + helper phospholipid + "
                  "PEG-lipid.  Microfluidic mixing "
                  "produces ~ 80-100 nm particles that "
                  "fuse with endosomes after uptake → "
                  "release cargo into cytoplasm.",
        sample_types="In-vitro: cell lines + primary cells; "
                     "in-vivo: most often hepatocytes (LNPs "
                     "drain to liver after IV); IM injection "
                     "for vaccines.",
        throughput="Pre-clinical screens of 10²-10³ "
                   "candidate LNPs; clinical-scale "
                   "manufacturing scaled to billions of "
                   "doses (COVID-19).",
        typical_readout="Cargo delivery efficiency + "
                        "biodistribution + protein-"
                        "expression / editing readout.",
        key_reagents="Ionisable lipids (MC3 / SM-102 / "
                     "ALC-0315 / SM-86 / ATX series); "
                     "cholesterol; DSPC / DOPE; PEG-lipid "
                     "(DMG-PEG2000 / ALC-0159).",
        representative_platforms="Acuitas + Genevant + "
                                 "Arcturus + Replicate + "
                                 "academic LNPs.",
        year_introduced="Patisiran (Onpattro) — first "
                        "approved siRNA-LNP, 2018; "
                        "BNT162b2 + mRNA-1273 mRNA-LNP "
                        "COVID vaccines, 2020.",
        key_references="Adams et al. 2018 *NEJM* "
                       "(patisiran trial); Polack et al. "
                       "2020 *NEJM* (BNT162b2); Hou et al. "
                       "2021 *Nat Rev Mater* review.",
        strengths="Non-viral, non-immunogenic (mostly), "
                  "scalable manufacturing, programmable "
                  "via cargo design.  Pandemic-vaccine "
                  "engine; CRISPR therapeutic delivery "
                  "(VERVE-101 + NTLA-2001 + 2002).",
        limitations="Liver tropism dominant for IV; "
                    "tissue-specific targeting "
                    "challenging; cold-chain "
                    "requirements; limited re-dosing "
                    "after immunogenic responses.",
        notes="The breakout delivery modality of the "
              "2020s.  Engineering tissue-selective LNPs "
              "(SORT lipids — Siegwart lab) is an active "
              "area.  See PH-3.0 graduate \"Modern "
              "modalities\" for clinical context.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="aav-delivery",
        name="Adeno-associated virus (AAV) gene-therapy "
             "delivery",
        abbreviation="AAV",
        category="delivery",
        principle="A non-pathogenic, replication-deficient "
                  "AAV vector packages a transgene "
                  "(promoter + cargo + polyA in single-"
                  "stranded DNA up to ~ 4.7 kb).  Capsid "
                  "serotype defines tissue tropism (e.g. "
                  "AAV9 → CNS + heart; AAV8 → liver; "
                  "AAVrh10 → lung; AAV-PHP.B → mouse "
                  "brain).  Long-term episomal expression "
                  "in non-dividing cells.",
        sample_types="In-vivo intramuscular + intravenous "
                     "+ subretinal + intracerebroventricular "
                     "+ direct-organ injection.",
        throughput="Pre-clinical: 10²-10³ engineered capsids "
                   "screened per project; clinical-grade "
                   "manufacturing in HEK293 transient "
                   "transfection or insect-Sf9 baculovirus.",
        typical_readout="Long-term transgene expression "
                        "(~ years in non-dividing tissue); "
                        "biodistribution mapping; "
                        "neutralising-antibody "
                        "monitoring.",
        key_reagents="AAV capsid (natural serotype or "
                     "engineered variant); transgene "
                     "vector plasmid; helper plasmids; "
                     "HEK293 or Sf9 producer cells.",
        representative_platforms="Spark / Roche (Luxturna), "
                                 "Novartis (Zolgensma), "
                                 "BioMarin (Roctavian + "
                                 "Hemgenix), Sarepta "
                                 "(Elevidys), PTC "
                                 "(Upstaza).",
        year_introduced="First gene-therapy AAV — Glybera "
                        "(2012, lipoprotein lipase "
                        "deficiency, withdrawn); modern "
                        "era from Luxturna 2017.",
        key_references="Maguire et al. 2008 *NEJM* "
                       "(Luxturna trial); Mendell et al. "
                       "2017 *NEJM* (Zolgensma); Wang et "
                       "al. 2019 *Nat Rev Drug Discov* "
                       "review.",
        strengths="Long-lasting expression in non-"
                  "dividing tissue; FDA-approved for "
                  "multiple indications; broad capsid "
                  "engineering toolkit.",
        limitations="Limited cargo (~ 4.7 kb); "
                    "pre-existing neutralising antibodies "
                    "(~ 30-70 % seroprevalence); cannot "
                    "be re-dosed (anti-capsid immunity); "
                    "expensive ($1-3.5 M / dose); "
                    "hepatotoxicity + complement "
                    "activation at high doses.",
        notes="Six FDA-approved AAV gene therapies as "
              "of 2026: Luxturna + Zolgensma + Hemgenix "
              "+ Roctavian + Elevidys + Upstaza.  See "
              "PH-3.0 graduate \"Modern modalities\" for "
              "clinical context.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="snrna-seq",
        name="Single-nucleus RNA sequencing",
        abbreviation="snRNA-seq",
        category="transcriptomics",
        principle="Tissue cryosectioned + nuclei isolated "
                  "by mechanical / detergent dissociation + "
                  "sucrose-gradient or FACS purification "
                  "(no enzymatic dissociation → no "
                  "protoplasting / dissociation stress) → "
                  "droplet-based capture (10x Multiome / "
                  "BD Rhapsody) → barcoded library + "
                  "sequencing.  Reads from intronic + "
                  "nascent transcripts.",
        sample_types="Frozen / archived tissue (the "
                     "killer feature); samples that don't "
                     "tolerate enzymatic dissociation "
                     "(brain, adipose, muscle, plant).",
        throughput="10K-100K nuclei per channel; "
                   "atlas-scale projects > 1 M nuclei.",
        typical_readout="Same as scRNA-seq but with "
                        "intronic-read-rich profiles; "
                        "transcripts/nucleus typically "
                        "30-50 % lower than scRNA-seq.",
        key_reagents="Nuclei-isolation buffers (Triton / "
                     "NP-40 / Tween-20 + sucrose), "
                     "RNase inhibitors, droplet-capture "
                     "kits.",
        representative_platforms="10x Chromium Single "
                                 "Cell + Multiome (RNA + "
                                 "ATAC), Parse Bio "
                                 "Evercode, BD Rhapsody.",
        year_introduced="DroNc-seq + sNuc-Seq — 2017 "
                        "(Habib + McCarroll labs); 10x "
                        "Multiome — 2020.",
        key_references="Habib et al. 2017 *Nat Methods* "
                       "(DroNc-seq); Bakken et al. 2018 "
                       "*PLoS ONE* (snRNA-seq protocol); "
                       "10x Multiome documentation.",
        strengths="Works with frozen / archived tissue + "
                  "tissues resistant to dissociation; no "
                  "enzymatic-stress artefacts; multi-modal "
                  "compatible (snRNA + snATAC).",
        limitations="Lower transcript counts vs scRNA-"
                    "seq; cytoplasmic / mitochondrial RNA "
                    "missed; intronic / nascent reads "
                    "make analysis subtly different.",
        notes="The standard for human-tissue-bank "
              "transcriptomics + cryopreserved-sample "
              "atlases.  Allen Brain Cell Atlas + HCA "
              "kidney + heart + lung atlases use snRNA-"
              "seq alongside scRNA-seq.",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "mus-musculus", "homo-sapiens",
        ),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="slide-seq",
        name="Slide-seqV2 high-resolution spatial "
             "transcriptomics",
        abbreviation="Slide-seqV2",
        category="spatial",
        principle="DNA-barcoded ~ 10-µm beads packed onto "
                  "a glass slide → tissue cryosection "
                  "placed on top → mRNA captured by "
                  "bead-bound poly-T → reverse "
                  "transcription preserves bead-barcode + "
                  "transcript identity → spatial "
                  "coordinates of every bead pre-mapped "
                  "by SOLiD-derived sequencing → "
                  "expression-by-location matrix at "
                  "near-cellular resolution.",
        sample_types="Fresh-frozen tissue cryosections "
                     "(10-20 µm thick).",
        throughput="One slide per experiment; ~ 50 K "
                   "beads per slide.",
        typical_readout="Bead-resolution gene-expression "
                        "matrix; cell-type assignment via "
                        "deconvolution; spatial gradients "
                        "+ niches.",
        key_reagents="DNA-barcoded beads; reverse "
                     "transcriptase + library-prep "
                     "kits.",
        representative_platforms="Slide-seqV2 (academic — "
                                 "Macosko + Chen labs); "
                                 "commercial Curio "
                                 "Bioscience Curio "
                                 "Seeker / Trekker.",
        year_introduced="Slide-seq — 2019 (Rodriques + "
                        "Stickels et al.); V2 — 2020.",
        key_references="Rodriques et al. 2019 *Science*; "
                       "Stickels et al. 2020 *Nat "
                       "Biotechnol* (V2).",
        strengths="Higher spatial resolution than Visium "
                  "(~ 10 µm vs 55 µm); whole-"
                  "transcriptome.  Curio's commercial "
                  "rebrand offers turnkey workflows.",
        limitations="Lower per-bead transcript capture "
                    "than Visium; requires bead-array "
                    "preparation; analysis pipelines "
                    "less mature.",
        notes="Complemented by image-based MERFISH / "
              "Xenium / CosMx for sub-cellular "
              "resolution; Stereo-seq (BGI) is the "
              "highest-resolution sequencing-based "
              "spatial method (~ 500 nm).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="ap-ms",
        name="Affinity purification + mass spectrometry",
        abbreviation="AP-MS",
        category="interaction",
        principle="A bait protein (tagged with FLAG / "
                  "HA / Myc / GFP / SBP / Strep) is "
                  "expressed in cells; cell lysate "
                  "incubated with affinity beads (anti-"
                  "tag antibody / streptavidin / GFP-"
                  "trap); washed extensively → bait + "
                  "co-purified interactors eluted → "
                  "trypsin digest + LC-MS/MS → list of "
                  "interacting proteins quantified.",
        sample_types="Cell + tissue lysates expressing "
                     "tagged bait (transient transfection "
                     "/ stable line / endogenous CRISPR-"
                     "knock-in).",
        throughput="10s-100s of baits per project; "
                   "BioPlex + DepMap + OpenCell + Human "
                   "Cell Map atlas-scale efforts.",
        typical_readout="Quantitative + statistically-"
                        "scored interactor lists; "
                        "background-subtracted via "
                        "control AP-MS (CRAPome / SAINT "
                        "scoring).",
        key_reagents="Affinity matrices (FLAG-M2 "
                     "agarose, anti-HA, GFP-Trap, "
                     "streptavidin); detergent + buffer "
                     "optimisation; LC-MS/MS.",
        representative_platforms="DIY workflows; SAINT "
                                 "+ CompPASS + ProHits-"
                                 "viz analysis tools; "
                                 "BioPlex + OpenCell + "
                                 "Human Cell Map "
                                 "consortia.",
        year_introduced="Mature since the early 2000s; "
                        "BioPlex 3.0 — 2021 (Huttlin et "
                        "al.).",
        key_references="Aebersold + Mann 2003 *Nature*; "
                       "Huttlin et al. 2021 *Cell* "
                       "(BioPlex 3.0); Cho et al. 2022 "
                       "*Cell* (OpenCell).",
        strengths="Direct + indirect interactions in "
                  "near-native conditions; "
                  "quantitative; large + reproducible "
                  "data; complements Y2H + BioID.",
        limitations="Misses transient + weak "
                    "interactions; tag artefacts; "
                    "wash-stringency-dependent "
                    "results; sample-prep + MS "
                    "expertise required.",
        notes="The MS-based protein-interaction "
              "workhorse; OpenCell + BioPlex + Human "
              "Cell Map are the modern atlas-scale "
              "AP-MS efforts.",
        cross_reference_enzyme_ids=(
            "trypsin",
        ),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(),
        cross_reference_molecule_names=(),
    ),
    MolecularBiologyTechnique(
        id="methylation-array",
        name="Illumina Methylation EPIC + MSA arrays",
        abbreviation="EPIC array",
        category="epigenetics",
        principle="Bisulfite-converted DNA hybridised to "
                  "an Illumina BeadChip carrying ~ 850 K "
                  "(EPIC v1) or ~ 935 K (EPIC v2 / MSA) "
                  "CpG-specific probe pairs.  Single-base "
                  "extension assay reports methylation "
                  "(C) vs unmethylation (T) per CpG.  "
                  "Cost-effective genome-scale methylome "
                  "compared to WGBS.",
        sample_types="Genomic DNA from blood, tissue, "
                     "FFPE, saliva, buccal swab; ~ 250-"
                     "500 ng input.",
        throughput="96 samples per batch; days-scale "
                   "workflow.",
        typical_readout="Per-CpG β-value (0-1 "
                        "methylation fraction); "
                        "differentially-methylated CpGs "
                        "+ regions; epigenetic clocks; "
                        "tumour-class predictors.",
        key_reagents="Illumina Infinium "
                     "MethylationEPIC v2 BeadChip; "
                     "bisulfite-conversion kit (Zymo / "
                     "EZ DNA Methylation).",
        representative_platforms="Illumina iScan + "
                                 "BeadArray Reader; "
                                 "data-analysis pipeline "
                                 "(minfi, ChAMP, "
                                 "SeSAMe).",
        year_introduced="HumanMethylation27 — 2008; "
                        "450K — 2011; EPIC v1 — 2016; "
                        "EPIC v2 — 2023; MSA — 2024.",
        key_references="Bibikova et al. 2011 *Genomics* "
                       "(450K); Pidsley et al. 2016 "
                       "*Genome Biol* (EPIC); Horvath "
                       "2013 *Genome Biol* (epigenetic "
                       "clock).",
        strengths="Cost-effective (~ $200-300 / sample) "
                  "epigenome-wide profiling at single-"
                  "CpG resolution; standard for EWAS + "
                  "epigenetic-clock + tumour-classifier "
                  "studies.",
        limitations="Only covers ~ 3 % of human CpGs "
                    "(targeted to gene + regulatory + "
                    "enhancer regions); WGBS / EM-seq "
                    "needed for unbiased methylome.",
        notes="Foundation of epigenetic-clock research "
              "(Horvath / Hannum / GrimAge / DunedinPACE) "
              "+ CNS-tumour methylation classifier "
              "(Capper et al. 2018 *Nature*).",
        cross_reference_enzyme_ids=(),
        cross_reference_cell_cycle_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens",
        ),
        cross_reference_molecule_names=(
            "Cytosine",
        ),
    ),
)
