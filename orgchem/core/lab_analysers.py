"""Phase 40a (round 146) — major lab analysers catalogue.

Headless reference data for the *Tools → Lab analysers…*
dialog.  Each entry is a capital-equipment-tier instrument
that a clinical / research wet lab will encounter — the layer
above the Phase-38a bench-glassware catalogue.

Categories
----------
- ``"clinical-chemistry"`` — Roche cobas / Siemens Atellica /
  Beckman AU / Abbott Architect c / Alinity c — the workhorse
  instruments running BMP / CMP panels (Phase 37b) at
  hundreds of samples per hour.
- ``"hematology"`` — Sysmex XN-series / Beckman DxH 900 /
  Siemens ADVIA / Abbott CELL-DYN — automated CBC + 5-part
  differential.
- ``"coagulation"`` — Stago STA Compact / Sysmex CS series
  / Werfen ACL TOP — PT / aPTT / fibrinogen / d-dimer.
- ``"immunoassay"`` — Roche cobas e801 / Abbott Architect i /
  Siemens Atellica IM / Beckman Access — chemiluminescent
  / fluorescent immunoassay for TSH / troponin / cancer
  markers / hormone panels.
- ``"molecular"`` — Roche cobas 8800 / Hologic Panther /
  BD MAX / Cepheid GeneXpert / Illumina NovaSeq / Oxford
  Nanopore — DNA / RNA quantitation + variant calling.
- ``"mass-spec"`` — clinical triple-quad LC-MS/MS, MALDI-TOF
  microbial ID, ICP-MS clinical, Orbitrap proteomics.
- ``"functional"`` — FLIPR Ca²⁺ / membrane-potential
  screening, high-content imagers, automated patch-clamp.
- ``"microscopy"`` — confocal / super-resolution /
  light-sheet / cryo-EM.
- ``"automation"`` — Hamilton STAR / Tecan Fluent / Beckman
  Biomek / Opentrons OT-2 liquid handlers.
- ``"storage"`` — Hamilton BiOS / Thermo Galileo automated
  -80 °C / LN₂ sample storage.

Reference data only — same shape as the Phase-37c
chromatography catalogue.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class LabAnalyser:
    id: str
    name: str
    manufacturer: str
    category: str
    function: str
    typical_throughput: str
    sample_volume: str
    detection_method: str
    typical_assays: str
    strengths: str
    limitations: str
    notes: str = ""


VALID_CATEGORIES: tuple = (
    "clinical-chemistry", "hematology", "coagulation",
    "immunoassay", "molecular", "mass-spec",
    "functional", "microscopy", "automation", "storage",
)


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[LabAnalyser]:
    return [
        # ---- Clinical chemistry ----
        LabAnalyser(
            id="cobas_c702",
            name="Roche cobas c 702",
            manufacturer="Roche Diagnostics",
            category="clinical-chemistry",
            function=(
                "High-volume hospital clinical-chemistry "
                "analyser running the BMP / CMP / lipid /"
                " liver / renal panel set."
            ),
            typical_throughput=(
                "≥ 2 000 photometric tests / hour"
            ),
            sample_volume="2-100 µL per test from a primary tube",
            detection_method=(
                "Photometric (UV-Vis 340-700 nm) + ISE for "
                "Na / K / Cl"
            ),
            typical_assays=(
                "Glucose / urea / creatinine / electrolytes "
                "/ ALT / AST / ALP / bilirubin / CK / CK-MB / "
                "albumin / total protein / cholesterol / "
                "HDL / LDL / triglycerides — every analyte "
                "in the Phase-37b BMP + CMP + Lipid panels"
            ),
            strengths=(
                "Hospital-scale throughput with full-track "
                "automation integration; broad assay menu "
                "(>200 IVD-cleared tests); ISE module "
                "skips the photometric chemistry for Na/K/Cl"
            ),
            limitations=(
                "Capital cost ($300-500k); reagent vendor "
                "lock-in to Roche Cobas chemistries; large "
                "footprint requires dedicated lab bay"
            ),
            notes=(
                "Forms the chemistry workstation in a "
                "Roche cobas pro modular system (chemistry "
                "+ immunoassay on shared track).  Smaller "
                "siblings: cobas c 311 (low-volume), c 503 "
                "(mid-volume)."
            ),
        ),
        LabAnalyser(
            id="atellica_ch",
            name="Siemens Atellica CH 930",
            manufacturer="Siemens Healthineers",
            category="clinical-chemistry",
            function=(
                "Mid-to-high-volume clinical chemistry "
                "analyser; the chemistry module of the "
                "Atellica Solution platform."
            ),
            typical_throughput=(
                "1 800 photometric / 600 ISE tests / hour"
            ),
            sample_volume="1.5-35 µL per test",
            detection_method="Photometric + ISE",
            typical_assays=(
                "Same BMP / CMP / lipid panel coverage as "
                "the cobas c 702; >120 IVD-cleared assays"
            ),
            strengths=(
                "Magnetic transport (no hooks / belts) "
                "delivers fast random-access throughput; "
                "compact footprint; integrates with the "
                "Atellica IM immunoassay module on a single "
                "track"
            ),
            limitations=(
                "Vendor-specific reagent kits; assay "
                "harmonisation across Atellica + legacy "
                "ADVIA platforms required upgrade work"
            ),
        ),
        LabAnalyser(
            id="beckman_au5800",
            name="Beckman AU5800",
            manufacturer="Beckman Coulter",
            category="clinical-chemistry",
            function=(
                "High-volume clinical chemistry analyser "
                "(reference-lab tier)."
            ),
            typical_throughput=(
                "Up to 9 800 photometric + ISE tests / hour "
                "(four-module configuration)"
            ),
            sample_volume="1.6-25 µL per test",
            detection_method="Photometric + ISE",
            typical_assays="Standard chemistry panel set",
            strengths=(
                "Highest throughput in the clinical "
                "chemistry market — designed for reference "
                "labs running > 100 000 tests / day; modular "
                "scaling (1-4 analytical modules)"
            ),
            limitations=(
                "Footprint + capital cost match the "
                "throughput; primarily a reference-lab "
                "rather than hospital-bench platform"
            ),
        ),
        LabAnalyser(
            id="abbott_alinity_c",
            name="Abbott Alinity c",
            manufacturer="Abbott Diagnostics",
            category="clinical-chemistry",
            function=(
                "Successor to the Architect c series; "
                "high-throughput clinical chemistry."
            ),
            typical_throughput="1 800 tests / hour",
            sample_volume="0.7-25 µL per test",
            detection_method="Photometric + ISE",
            typical_assays=(
                "Full chemistry panel + cardiac markers "
                "(troponin I / BNP) on the integrated "
                "Alinity i immunoassay module"
            ),
            strengths=(
                "Compact footprint relative to throughput; "
                "shared sample-loading interface across "
                "Alinity c / i / s / h (chemistry, "
                "immunoassay, urine, hematology)"
            ),
            limitations=(
                "Vendor-specific Alinity reagent menu; "
                "platform consolidation across legacy "
                "Architect installations is non-trivial"
            ),
        ),

        # ---- Hematology ----
        LabAnalyser(
            id="sysmex_xn1000",
            name="Sysmex XN-1000",
            manufacturer="Sysmex",
            category="hematology",
            function=(
                "Automated CBC + 5-part WBC differential + "
                "reticulocyte count; the modern hospital "
                "hematology workhorse."
            ),
            typical_throughput="100 samples / hour",
            sample_volume="88 µL per CBC + diff",
            detection_method=(
                "Hydrodynamic-focusing flow cytometry (DC + "
                "RF impedance + side fluorescence) + "
                "SLS-haemoglobin colorimetry"
            ),
            typical_assays=(
                "RBC + WBC + hemoglobin + hematocrit + "
                "platelet + MCV / MCH / MCHC + 5-part "
                "differential (neut / lymph / mono / eos / "
                "baso) + reticulocyte count + NRBC + "
                "immature platelet fraction"
            ),
            strengths=(
                "Excellent platelet + retic + NRBC analysis; "
                "fluorescence-channel diff outperforms "
                "impedance-only systems on abnormal "
                "morphology; flagging algorithms are the "
                "industry reference"
            ),
            limitations=(
                "Manual review of flagged samples still "
                "needed (no fully-automated abnormal "
                "morphology classification); body-fluid "
                "mode requires a separate XN-BF analyser"
            ),
            notes=(
                "Larger XN-2000 / 3000 / 9000 modular "
                "systems for higher throughput; XN-450 / "
                "XN-550 are compact bench versions for "
                "low-volume sites + POC."
            ),
        ),
        LabAnalyser(
            id="beckman_dxh900",
            name="Beckman DxH 900",
            manufacturer="Beckman Coulter",
            category="hematology",
            function=(
                "Hematology analyser with VCSn (Volume / "
                "Conductivity / Scatter / fluorescence) "
                "WBC analysis."
            ),
            typical_throughput="100 samples / hour",
            sample_volume="165 µL per CBC + diff",
            detection_method=(
                "VCSn flow cytometry + Coulter principle "
                "(impedance) for cell counting"
            ),
            typical_assays=(
                "Same CBC + diff + retic + NRBC menu as "
                "the Sysmex XN-1000"
            ),
            strengths=(
                "Coulter principle is the reference method "
                "for absolute cell counting; VCSn diff "
                "differentiates abnormal cell populations "
                "(leukaemia blasts, atypical lymphocytes)"
            ),
            limitations=(
                "Higher sample-volume requirement than "
                "Sysmex (165 vs 88 µL); body-fluid mode "
                "requires DxH 520 add-on"
            ),
        ),

        # ---- Coagulation ----
        LabAnalyser(
            id="stago_sta_r_max",
            name="Stago STA R Max 3",
            manufacturer="Stago",
            category="coagulation",
            function=(
                "Hospital-scale coagulation analyser running "
                "the standard PT / aPTT / fibrinogen / "
                "d-dimer test set."
            ),
            typical_throughput=(
                "Up to 240 PT tests / hour"
            ),
            sample_volume="50-200 µL plasma per test",
            detection_method=(
                "Mechanical clot detection (steel-ball "
                "viscosity change) for PT / aPTT; "
                "immunoturbidimetric for d-dimer"
            ),
            typical_assays=(
                "PT (INR) / aPTT / fibrinogen (Clauss) / "
                "d-dimer / antithrombin / protein C / "
                "protein S / lupus anticoagulant / specific "
                "factor assays (FII / V / VII / VIII / IX / "
                "X / XI)"
            ),
            strengths=(
                "Mechanical detection is interference-free "
                "(no haemolysis / lipaemia / icterus "
                "artefact); broad coagulation menu including "
                "specialty assays"
            ),
            limitations=(
                "Mechanical method has slightly lower "
                "throughput than optical / chromogenic "
                "methods; reagent cost is high vs Sysmex CS "
                "/ Werfen ACL"
            ),
        ),
        LabAnalyser(
            id="sysmex_cs5100",
            name="Sysmex CS-5100",
            manufacturer="Sysmex",
            category="coagulation",
            function=(
                "High-throughput hemostasis analyser using "
                "optical clot detection."
            ),
            typical_throughput=(
                "Up to 400 PT tests / hour"
            ),
            sample_volume="50-100 µL plasma per test",
            detection_method=(
                "Optical (turbidimetric) clot detection + "
                "chromogenic / immunoturbidimetric"
            ),
            typical_assays=(
                "PT / aPTT / fibrinogen / d-dimer / "
                "specialty assays (lupus anticoagulant, "
                "factor levels, anti-Xa)"
            ),
            strengths=(
                "PSI (Pre-Sample Integrity) check detects "
                "haemolysis / icterus / lipaemia BEFORE the "
                "test runs — eliminates wasted reagents; "
                "best-in-class chromogenic anti-Xa for "
                "LMWH / fondaparinux monitoring"
            ),
            limitations=(
                "Optical methods susceptible to lipaemic / "
                "icteric samples (PSI mitigates); needs "
                "regular calibration of optical channels"
            ),
        ),

        # ---- Immunoassay ----
        LabAnalyser(
            id="cobas_e801",
            name="Roche cobas e 801",
            manufacturer="Roche Diagnostics",
            category="immunoassay",
            function=(
                "Electrochemiluminescent immunoassay "
                "(ECLIA) module — the immunoassay "
                "workstation in cobas pro modular systems."
            ),
            typical_throughput="300 tests / hour",
            sample_volume="5-50 µL serum per test",
            detection_method=(
                "ECLIA — ruthenium-tris(bipyridyl) tag + "
                "tripropylamine co-reactant generating light "
                "at 620 nm at the magnetic-bead surface"
            ),
            typical_assays=(
                "TSH / fT4 / fT3 (thyroid panel from "
                "Phase 37b); cardiac troponin T / I "
                "(high-sensitivity) / NT-proBNP; tumour "
                "markers (PSA / CEA / AFP / CA-125 / "
                "CA-19-9 / CA-15-3); fertility hormones "
                "(LH / FSH / estradiol / progesterone / "
                "β-hCG); HBV / HIV / HCV serology"
            ),
            strengths=(
                "Excellent dynamic range + analytical "
                "sensitivity (high-sensitivity troponin "
                "down to 1 ng/L LoD); shared sample track "
                "with cobas c chemistry analysers"
            ),
            limitations=(
                "Vendor-specific reagent menu; ECLIA is "
                "Roche-proprietary so direct lab-to-lab "
                "harmonisation across vendors is poor"
            ),
        ),
        LabAnalyser(
            id="abbott_alinity_i",
            name="Abbott Alinity i",
            manufacturer="Abbott Diagnostics",
            category="immunoassay",
            function=(
                "Chemiluminescent microparticle immunoassay "
                "(CMIA) — successor to the Architect i."
            ),
            typical_throughput="200 tests / hour",
            sample_volume="20-100 µL per test",
            detection_method=(
                "CMIA with acridinium-ester tag; "
                "magnetic-microparticle separation"
            ),
            typical_assays=(
                "Standard immunoassay menu (thyroid, "
                "cardiac, tumour markers, fertility, "
                "infectious disease serology) + STAT "
                "high-sensitivity troponin"
            ),
            strengths=(
                "Same sample-loading interface as Alinity "
                "c; CMIA acridinium chemistry has very "
                "fast (2-3 min) signal acquisition"
            ),
            limitations=(
                "Vendor-specific reagent menu; "
                "harmonisation work needed when migrating "
                "from legacy Architect"
            ),
        ),
        LabAnalyser(
            id="atellica_im",
            name="Siemens Atellica IM 1600",
            manufacturer="Siemens Healthineers",
            category="immunoassay",
            function=(
                "Immunoassay module of the Atellica Solution "
                "platform; chemiluminescent detection."
            ),
            typical_throughput="440 tests / hour",
            sample_volume="3-100 µL per test",
            detection_method=(
                "Acridinium-ester chemiluminescence + "
                "paramagnetic-particle separation"
            ),
            typical_assays=(
                "Same broad immunoassay menu as cobas e801 "
                "/ Alinity i"
            ),
            strengths=(
                "Highest single-module immunoassay "
                "throughput in the segment; magnetic "
                "transport shared with Atellica CH chemistry"
            ),
            limitations=(
                "Vendor-specific reagent menu; assay "
                "harmonisation across Atellica vs legacy "
                "ADVIA Centaur platforms required work"
            ),
        ),

        # ---- Molecular ----
        LabAnalyser(
            id="cobas_8800",
            name="Roche cobas 8800",
            manufacturer="Roche Diagnostics",
            category="molecular",
            function=(
                "High-throughput molecular diagnostic "
                "platform — automated sample prep + qPCR for "
                "viral load + screening assays."
            ),
            typical_throughput=(
                "Up to 960 results in 8 hours (HIV / HBV / "
                "HCV viral load) — ~120 results per hour"
            ),
            sample_volume="500 µL plasma typical",
            detection_method=(
                "Real-time qPCR with TaqMan probes + "
                "automated nucleic-acid extraction"
            ),
            typical_assays=(
                "HIV-1 viral load + HCV / HBV viral load + "
                "HPV genotyping + CT/NG STI panel + SARS-"
                "CoV-2 (FDA EUA); blood-screening assays "
                "for transfusion services (HIV / HCV / HBV / "
                "WNV / ZIKA NAT)"
            ),
            strengths=(
                "True walk-away automation — load samples + "
                "reagents, walk away.  IVD-cleared assay "
                "menu eliminates LDT validation burden in "
                "the clinical lab."
            ),
            limitations=(
                "Capital cost ($500k+); IVD reagent "
                "lock-in.  Cobas 6800 (sibling) is the "
                "lower-throughput option for mid-sized labs."
            ),
            notes=(
                "Dominant high-volume HIV / HBV / HCV "
                "viral-load platform globally."
            ),
        ),
        LabAnalyser(
            id="hologic_panther",
            name="Hologic Panther + Panther Fusion",
            manufacturer="Hologic",
            category="molecular",
            function=(
                "Molecular IVD platform with continuous "
                "random-access loading; runs both Hologic "
                "Aptima TMA assays + Panther Fusion qPCR."
            ),
            typical_throughput=(
                "Up to 1 000 results per 24 hours"
            ),
            sample_volume="710 µL primary tube",
            detection_method=(
                "Aptima: transcription-mediated "
                "amplification (TMA) + hybridisation-"
                "protection chemiluminescent detection.  "
                "Fusion module: real-time qPCR."
            ),
            typical_assays=(
                "STI panel (CT / NG / TV / MG); HPV "
                "genotyping; HIV / HCV viral load; "
                "respiratory panel (Flu A/B + RSV + "
                "SARS-CoV-2); BV / CV / TV vaginitis panel"
            ),
            strengths=(
                "Continuous random-access loading + STAT "
                "samples; the de-facto STI screening "
                "platform in US clinical labs"
            ),
            limitations=(
                "Aptima TMA chemistry is Hologic-"
                "proprietary (no third-party assays); "
                "Panther Fusion adds qPCR but at "
                "incremental capex"
            ),
        ),
        LabAnalyser(
            id="cepheid_genexpert",
            name="Cepheid GeneXpert",
            manufacturer="Cepheid",
            category="molecular",
            function=(
                "Cartridge-based qPCR — the dominant "
                "near-patient molecular diagnostic platform."
            ),
            typical_throughput=(
                "1-80 cartridges in parallel (configurable "
                "1- to 80-module instruments); ~45 min per "
                "cartridge for most assays"
            ),
            sample_volume="Variable per assay (cartridge "
                          "self-contains the prep)",
            detection_method=(
                "Cartridge-integrated nucleic-acid "
                "extraction + real-time qPCR with "
                "fluorogenic probes"
            ),
            typical_assays=(
                "Xpert MTB/RIF (TB + rifampin resistance — "
                "WHO-endorsed POC test); Xpert Carba-R "
                "(carbapenem-resistance genes); SARS-CoV-2 "
                "(FDA EUA); GBS / MRSA / C. difficile / "
                "Flu / RSV / norovirus"
            ),
            strengths=(
                "Sample-to-result in 30-60 min; minimal "
                "training required (load cartridge, walk "
                "away); CLIA-waived assays for POC use"
            ),
            limitations=(
                "Per-test cartridge cost is high ($15-100 "
                "depending on assay); single-sample "
                "cartridges aren't suited to high-throughput "
                "central-lab work"
            ),
            notes=(
                "GeneXpert Edge is a 1-module portable "
                "version; GeneXpert Infinity-80 is the "
                "core-lab automation tier."
            ),
        ),
        LabAnalyser(
            id="illumina_novaseq_x",
            name="Illumina NovaSeq X / X Plus",
            manufacturer="Illumina",
            category="molecular",
            function=(
                "Production-scale next-generation sequencer "
                "— the dominant whole-genome / whole-"
                "exome / RNA-seq platform in research + "
                "clinical sequencing labs."
            ),
            typical_throughput=(
                "Up to 16 Tbp per 48-hour run (NovaSeq X "
                "Plus, dual-flowcell mode) — equivalent to "
                "~128 whole human genomes (30× coverage) "
                "per run"
            ),
            sample_volume=(
                "~1 nM library loading volume; library "
                "prep needs 100 ng-1 µg DNA / RNA"
            ),
            detection_method=(
                "Sequencing-by-synthesis (SBS) chemistry "
                "with reversible-terminator nucleotides; "
                "two-channel (XLEAP-SBS) imaging on the "
                "NovaSeq X"
            ),
            typical_assays=(
                "Whole-genome sequencing; whole-exome; "
                "RNA-seq + total RNA; single-cell RNA-seq "
                "library sequencing; targeted panels "
                "(cancer, hereditary disease); methylation "
                "/ ChIP-seq / ATAC-seq library sequencing"
            ),
            strengths=(
                "Lowest per-base sequencing cost in the "
                "industry; XLEAP-SBS chemistry doubles "
                "throughput at lower reagent cost vs the "
                "NovaSeq 6000"
            ),
            limitations=(
                "Capital cost > $1M; infrastructure (cooling, "
                "power, data networking) requires a "
                "dedicated sequencing core; 48 h/run + flow-"
                "cell yield economics force batched runs"
            ),
            notes=(
                "Lower-throughput tiers in the same family: "
                "NextSeq 1000 / 2000 (mid-volume), MiSeq i100 "
                "/ MiniSeq (low-volume / clinical)."
            ),
        ),
        LabAnalyser(
            id="oxford_promethion",
            name="Oxford Nanopore PromethION",
            manufacturer="Oxford Nanopore Technologies",
            category="molecular",
            function=(
                "Long-read nanopore sequencer — drives DNA / "
                "RNA through protein nanopores embedded in a "
                "flow cell membrane and reads the ionic-"
                "current signature in real time."
            ),
            typical_throughput=(
                "Up to 290 Gbp per flow cell over 72 hours; "
                "PromethION 48 = 48 flow cells in parallel "
                "→ up to 14 Tbp per run"
            ),
            sample_volume=(
                "Library loading 75 µL; library prep "
                "preserves long DNA fragments (10-100+ kb "
                "reads achievable)"
            ),
            detection_method=(
                "Ion-current modulation through CsgG-derived "
                "protein nanopores; ASIC-based real-time "
                "base-calling on the PromethION GPU rack"
            ),
            typical_assays=(
                "Whole-genome de novo assembly; structural-"
                "variant detection; methylation profiling "
                "(direct, no bisulfite conversion); long-"
                "amplicon sequencing; metagenomics"
            ),
            strengths=(
                "Read lengths > 100 kb resolve repetitive / "
                "structural-variant regions where short-read "
                "sequencing fails; native modification "
                "detection (5mC / 6mA) without bisulfite "
                "conversion; real-time data analysis"
            ),
            limitations=(
                "Higher per-base error rate than Illumina "
                "(~95-99 % depending on chemistry version); "
                "needs balanced library input (depleted DNA "
                "shortens reads); flow-cell pore yield "
                "varies"
            ),
            notes=(
                "Lower-throughput Oxford siblings: GridION "
                "(5 flow cells), MinION (1 flow cell, "
                "USB-thumb-drive size — used for field / "
                "POC sequencing during the 2014 Ebola + "
                "2020 SARS-CoV-2 outbreaks)."
            ),
        ),

        # ---- Mass spec ----
        LabAnalyser(
            id="sciex_qtrap_7500",
            name="SCIEX Triple Quad / QTRAP 7500",
            manufacturer="SCIEX",
            category="mass-spec",
            function=(
                "Clinical / research triple-quadrupole "
                "LC-MS/MS for quantitative bioanalysis."
            ),
            typical_throughput=(
                "Method-dependent; ~100-200 samples per day "
                "for clinical assays (5-15 min per LC run)"
            ),
            sample_volume=(
                "5-50 µL plasma; SPE / protein-precipitation "
                "extraction typical"
            ),
            detection_method=(
                "Atmospheric-pressure ionisation (ESI / APCI) "
                "→ triple-quadrupole mass selection (Q1 + "
                "Q3) with CID fragmentation in q2; multiple-"
                "reaction-monitoring (MRM) for quantitation"
            ),
            typical_assays=(
                "Vitamin D 25(OH) (the clinical-LC-MS/MS "
                "killer app); steroid panels (testosterone, "
                "estradiol, cortisol); immunosuppressants "
                "(tacrolimus, cyclosporin, sirolimus); "
                "newborn-screening expanded panel; therapeutic-"
                "drug monitoring"
            ),
            strengths=(
                "MRM specificity + sensitivity (pg/mL LoD) "
                "better than immunoassay for low-MW "
                "analytes; multi-analyte panels in single "
                "run; gold-standard reference method for "
                "vitamin D + steroid panels"
            ),
            limitations=(
                "Method development requires MS expertise; "
                "throughput much lower than chemistry / "
                "immunoassay analysers; capital cost "
                "($300-500k); not suitable for STAT testing"
            ),
        ),
        LabAnalyser(
            id="bruker_biotyper",
            name="Bruker MALDI Biotyper",
            manufacturer="Bruker",
            category="mass-spec",
            function=(
                "MALDI-TOF mass spectrometer for microbial "
                "identification via ribosomal-protein "
                "fingerprinting."
            ),
            typical_throughput=(
                "~96 isolates per plate, 30-60 min per "
                "plate — vs traditional biochem ID 16-48 h"
            ),
            sample_volume=(
                "Direct deposit of an isolated colony onto "
                "a stainless-steel target + 1 µL matrix "
                "(α-CHCA)"
            ),
            detection_method=(
                "Matrix-assisted laser-desorption ionisation "
                "(MALDI) + time-of-flight mass analyser; "
                "spectra compared to a reference library of "
                "~3 500 species"
            ),
            typical_assays=(
                "Bacterial + fungal species ID from "
                "isolates; mycobacteria ID (with extended "
                "extraction protocol); growing menu for "
                "AMR-marker detection (carbapenemases, "
                "ESBLs)"
            ),
            strengths=(
                "Reduces ID turnaround from days to "
                "minutes; per-sample reagent cost ~ $0.50 "
                "vs $10+ for biochemical strips; "
                "transformative for sepsis / "
                "bloodstream-infection workflows"
            ),
            limitations=(
                "Library coverage gaps for rare / "
                "fastidious organisms; pure isolate "
                "required (mixed cultures fail); cannot "
                "perform AST directly (still need "
                "downstream susceptibility testing)"
            ),
            notes=(
                "Direct competitor: bioMérieux VITEK MS.  "
                "Both have gradually displaced biochemical "
                "ID strips (API, Vitek 2 cards) for "
                "routine bacterial ID."
            ),
        ),

        # ---- Functional / cell-based ----
        LabAnalyser(
            id="flipr_penta",
            name="Molecular Devices FLIPR Penta",
            manufacturer="Molecular Devices",
            category="functional",
            function=(
                "Real-time intracellular Ca²⁺ + membrane-"
                "potential imaging system for GPCR / ion-"
                "channel functional screening."
            ),
            typical_throughput=(
                "96 / 384 / 1 536-well plate formats — 1 "
                "plate per ~2-5 minutes for standard Ca²⁺ "
                "/ membrane-potential reads"
            ),
            sample_volume=(
                "Cells loaded in 96/384/1536-well "
                "microplates; reagent injectors deliver "
                "test-compound additions"
            ),
            detection_method=(
                "EMCCD camera + bandpass filters captures "
                "fluorescent dye signal (Fluo-4 / Calcium "
                "5 / Calcium 6 for Ca²⁺; FMP-Tyrode for "
                "membrane potential) at 1-second time "
                "resolution"
            ),
            typical_assays=(
                "GPCR-mediated Ca²⁺ release (Gq-coupled "
                "receptor screening); voltage-gated ion-"
                "channel modulators (Na_V / K_V / Ca_V "
                "agonists / antagonists / inhibitors); "
                "transporter-mediated K⁺ uptake; cardiac-"
                "safety hERG screening"
            ),
            strengths=(
                "Plate-format throughput (1 536-well) for "
                "primary HTS campaigns; integrated reagent "
                "injectors enable real-time dose-response "
                "in seconds; gold-standard cardiac-safety "
                "screening platform"
            ),
            limitations=(
                "Functional readout alone — biochemical "
                "mechanism (binding affinity, kinetics) "
                "needs orthogonal assays; dye-loading "
                "variability is the main reproducibility "
                "challenge"
            ),
        ),
        LabAnalyser(
            id="operetta_cls",
            name="PerkinElmer Operetta CLS",
            manufacturer="PerkinElmer (Revvity)",
            category="functional",
            function=(
                "High-content imager — automated wide-field "
                "or confocal fluorescence microscopy of 96 "
                "/ 384 / 1 536-well plates with image-based "
                "quantitative phenotyping."
            ),
            typical_throughput=(
                "1 plate per 5-30 minutes depending on "
                "objective + channel count + tile coverage"
            ),
            sample_volume=(
                "Cells in standard high-content plates; "
                "fixed (immunofluorescence) or live "
                "(fluorogenic / GFP-expressing)"
            ),
            detection_method=(
                "Sourced from a robotic microscope (4-63× "
                "objectives) + sCMOS camera + 4-5 "
                "fluorescence channels (DAPI / FITC / "
                "TRITC / Cy5 typical); confocal option via "
                "spinning-disk module"
            ),
            typical_assays=(
                "Phenotypic screening (cell-cycle, "
                "apoptosis, autophagy, neurite outgrowth, "
                "mitotic-defect detection); 3D-organoid "
                "imaging; antibody / staining-pattern "
                "characterisation; high-content "
                "compound-profiling (Cell Painting protocol)"
            ),
            strengths=(
                "Image-based phenotypic readout — capture "
                "subtle morphological changes that "
                "biochemical readouts miss; 1 536-well "
                "compatibility for industrial HTS"
            ),
            limitations=(
                "Image-analysis pipeline development "
                "(Harmony / CellProfiler / custom) is the "
                "primary bottleneck; storage costs for "
                "image data scale linearly with plate "
                "count"
            ),
        ),

        # ---- Microscopy ----
        LabAnalyser(
            id="zeiss_lsm_980",
            name="Zeiss LSM 980 / LSM 980 Airyscan 2",
            manufacturer="Carl Zeiss",
            category="microscopy",
            function=(
                "Point-scanning laser confocal microscope "
                "for fluorescence imaging of fixed + live "
                "cells / tissues / organoids."
            ),
            typical_throughput=(
                "Single-cell to small tissue (5 mm² tile "
                "scan) — minutes to hours per acquisition"
            ),
            sample_volume=(
                "Coverslip-mounted cells / tissue / "
                "organoid; live imaging in 35 mm dishes "
                "+ environmental control"
            ),
            detection_method=(
                "Multi-line laser excitation (405 / 488 / "
                "561 / 633 nm typical) + GaAsP PMT "
                "detectors; Airyscan 2 super-resolution "
                "module (1.7× resolution improvement) via "
                "32-element detector array"
            ),
            typical_assays=(
                "Co-localisation imaging; FRAP / FLIP / "
                "FRET; Z-stack 3D reconstruction; live-cell "
                "time-lapse; multiplex immunofluorescence "
                "(4-5 colour standard, more with spectral "
                "unmixing)"
            ),
            strengths=(
                "Optical sectioning rejects out-of-focus "
                "light → clean 3D images; spectral "
                "detection (Lambda mode) separates >5 "
                "fluorophores; Airyscan brings sub-"
                "diffraction resolution (~120 nm lateral)"
            ),
            limitations=(
                "Slower than spinning-disk confocal for "
                "live-cell time-lapse; photobleaching + "
                "phototoxicity from the focused laser; "
                "capital cost ($300-500k base, $700k+ for "
                "Airyscan)"
            ),
        ),
        LabAnalyser(
            id="zeiss_lattice_lightsheet",
            name="Zeiss Lattice Lightsheet 7",
            manufacturer="Carl Zeiss",
            category="microscopy",
            function=(
                "Lattice light-sheet microscope for "
                "long-duration high-resolution live-cell "
                "imaging."
            ),
            typical_throughput=(
                "1-100 Hz volume rate per sample (depending "
                "on volume size + Z-step); single-sample "
                "imaging only"
            ),
            sample_volume=(
                "Coverslip-mounted live cells / spheroids "
                "/ organoids; environmental control "
                "(temperature, CO₂, humidity)"
            ),
            detection_method=(
                "Lattice-pattern excitation light sheet "
                "(thin sheet of light orthogonal to the "
                "detection objective); sCMOS camera "
                "captures one Z-plane at a time; minimal "
                "photo-exposure"
            ),
            typical_assays=(
                "Long-duration (hours-days) live-cell "
                "imaging; embryo development; intracellular "
                "trafficking; mitosis dynamics; organoid "
                "morphogenesis"
            ),
            strengths=(
                "Photo-toxicity / photobleaching ~10-100× "
                "lower than confocal — enables overnight "
                "live-cell experiments that would kill "
                "cells under confocal illumination"
            ),
            limitations=(
                "Single-sample throughput (no plate "
                "format); image processing (deskewing + "
                "deconvolution) is computationally "
                "expensive; capital cost > $1M"
            ),
        ),
        LabAnalyser(
            id="thermo_krios_g4",
            name="Thermo Krios G4 cryo-TEM",
            manufacturer="Thermo Fisher Scientific",
            category="microscopy",
            function=(
                "Cryo-electron microscope for single-"
                "particle analysis + electron tomography "
                "of macromolecular structures at near-"
                "atomic resolution."
            ),
            typical_throughput=(
                "100-1 000 micrographs per overnight "
                "session; one structure per 1-3 weeks of "
                "data collection + processing"
            ),
            sample_volume=(
                "3-5 µL of purified protein sample (0.1-1 "
                "mg/mL); plunge-frozen in liquid ethane "
                "onto grid"
            ),
            detection_method=(
                "300 kV field-emission electron source; "
                "K3 / Falcon-4 direct-electron detector "
                "(<1 e/pixel/frame) for high-resolution "
                "imaging"
            ),
            typical_assays=(
                "Single-particle analysis (SPA) for protein "
                "/ RNA / ribonucleoprotein structure "
                "determination at 2-3 Å resolution; "
                "cryo-electron tomography of organelles + "
                "viruses; sub-tomogram averaging"
            ),
            strengths=(
                "The dominant method for membrane-protein + "
                "large-complex structures (>100 kDa) where "
                "X-ray crystallography fails; revolutionary "
                "for SARS-CoV-2 spike + ribosome + "
                "transcription-complex structures over the "
                "last decade"
            ),
            limitations=(
                "Capital + installation cost > $5M; "
                "dedicated facility (cryostat, "
                "vibration-isolated room, dedicated power) "
                "required; sample-prep + data-collection "
                "expertise non-trivial; small molecules "
                "(<60 kDa) below the practical resolution "
                "limit"
            ),
            notes=(
                "Glacios + Tundra are lower-cost siblings "
                "(200 kV / 100 kV) for screening + smaller "
                "facilities."
            ),
        ),

        # ---- Liquid-handling automation ----
        LabAnalyser(
            id="hamilton_star",
            name="Hamilton Microlab STAR / STARplus",
            manufacturer="Hamilton",
            category="automation",
            function=(
                "Automated liquid-handling workstation — "
                "pipetting + sample prep + integration with "
                "downstream instruments."
            ),
            typical_throughput=(
                "Method-dependent — typical NGS library "
                "prep on STARplus: 96 samples in 4-6 hours"
            ),
            sample_volume=(
                "1 µL-1 mL pipetting range; CO-RE "
                "(Compressed-Open-Re-Sealable) tip "
                "engagement"
            ),
            detection_method=(
                "Capacitive + pressure-based liquid-level "
                "detection on each channel; clot detection; "
                "no native assay readout (the STAR moves "
                "samples to + from external readers)"
            ),
            typical_assays=(
                "NGS library prep (Illumina TruSeq / Nextera); "
                "qPCR plate setup; ELISA workflows; "
                "compound-management; cell-based assay "
                "preparation; NA extraction integration "
                "with bead-handling protocols"
            ),
            strengths=(
                "Industry-leading reliability + accuracy "
                "(<2 % CV at low volumes); sterile-pipetting "
                "options for clinical / diagnostic use; "
                "MFX cabinet integrates a robotic arm for "
                "plate hand-off between modules"
            ),
            limitations=(
                "Capital cost ($150-500k depending on "
                "configuration); CO-RE tips are "
                "Hamilton-proprietary (vendor lock-in); "
                "method development requires Venus "
                "scripting expertise"
            ),
            notes=(
                "Smaller siblings: STARlet (compact 6-"
                "channel), Vantage (modular high-throughput)."
            ),
        ),
        LabAnalyser(
            id="tecan_fluent",
            name="Tecan Fluent",
            manufacturer="Tecan",
            category="automation",
            function=(
                "Modular liquid-handling automation "
                "platform — direct competitor to Hamilton "
                "STAR."
            ),
            typical_throughput="Method-dependent; same "
                               "scale as STAR class",
            sample_volume="1 µL-5 mL pipetting range",
            detection_method=(
                "Integrated capacitive + pressure-based "
                "liquid-level detection; compatible "
                "downstream readers (incubators, "
                "magnetic-bead stations, sealers)"
            ),
            typical_assays=(
                "NGS library prep, qPCR plate setup, "
                "ELISA, cell culture, NA extraction, "
                "compound dispensing"
            ),
            strengths=(
                "Touch-screen front-end is more accessible "
                "than Hamilton's Venus IDE for non-"
                "programmer biologists; FluentControl "
                "scripting language; broad consumable "
                "options"
            ),
            limitations=(
                "Comparable capital cost to STAR; some "
                "advanced pipetting features (variable-"
                "spacing channels) cost extra"
            ),
        ),
        LabAnalyser(
            id="opentrons_ot2",
            name="Opentrons OT-2 / Flex",
            manufacturer="Opentrons",
            category="automation",
            function=(
                "Open-source liquid handler — Python-"
                "scripted protocols, unit-cost ~10× lower "
                "than STAR / Fluent class."
            ),
            typical_throughput=(
                "Slower per-step than Hamilton STAR but "
                "still hours-not-days for typical 96-well "
                "workflows"
            ),
            sample_volume="1 µL-1 mL pipetting range",
            detection_method=(
                "No built-in liquid-level detection on the "
                "OT-2 (Flex adds gripper + capacitive "
                "sensors); compatible with magnetic + "
                "thermo + temperature-control modules"
            ),
            typical_assays=(
                "qPCR plate setup; NA extraction with bead "
                "modules; basic NGS library prep; "
                "academic-research pipetting tasks"
            ),
            strengths=(
                "$10-15k capital cost (OT-2) / $25-40k "
                "(Flex) — opens automation to single-PI "
                "academic labs; full Python protocol "
                "scripting; growing community + open-source "
                "protocol library; CSV-driven worklist "
                "execution"
            ),
            limitations=(
                "Lower precision than STAR / Fluent at low "
                "volumes; OT-2 has no built-in liquid "
                "detection; 8-channel max (vs 96-channel "
                "STAR); limited integration with downstream "
                "readers"
            ),
        ),

        # ---- Sample storage ----
        LabAnalyser(
            id="hamilton_bios",
            name="Hamilton BiOS L / BIONanoArchive",
            manufacturer="Hamilton",
            category="storage",
            function=(
                "Automated -80 °C / -20 °C sample-storage "
                "system with robotic retrieval — biobank-"
                "scale sample management."
            ),
            typical_throughput=(
                "Capacity 10 000 - 1 000 000 samples "
                "depending on configuration; retrieval "
                "<1 min per sample request"
            ),
            sample_volume=(
                "0.2 mL - 50 mL sample tubes / cryo vials; "
                "barcoded SBS-format racks"
            ),
            detection_method=(
                "1D / 2D barcode scanning at the storage "
                "interface; integration with LIMS for "
                "sample-tracking metadata; no analytical "
                "readout"
            ),
            typical_assays=(
                "Biobank cold-chain storage (clinical "
                "samples, biospecimens); compound libraries "
                "(small-molecule + biologics); cell-line "
                "banks; reagent storage"
            ),
            strengths=(
                "Eliminates manual freezer pulls (biggest "
                "biobank labour cost); door-open events "
                "minimised → temperature stability + "
                "sample integrity"
            ),
            limitations=(
                "Capital + installation cost > $1M for "
                "large-capacity systems; once committed, "
                "expansion requires hardware additions"
            ),
        ),
        LabAnalyser(
            id="thermo_galileo",
            name="Thermo Galileo LN₂ vapor storage",
            manufacturer="Thermo Fisher Scientific",
            category="storage",
            function=(
                "Automated liquid-nitrogen-vapor (-196 °C) "
                "sample storage for cells / tissues "
                "requiring cryogenic preservation."
            ),
            typical_throughput=(
                "30 000 - 150 000 vial capacity per unit; "
                "robotic retrieval ~2 min per request"
            ),
            sample_volume=(
                "Cryo-vials (1.5 - 4.5 mL) in barcoded "
                "racks"
            ),
            detection_method=(
                "Vial barcode scanning + LIMS integration"
            ),
            typical_assays=(
                "Master / working cell-bank storage; "
                "patient-derived organoid banks; iPSC + "
                "ES cell repositories; CAR-T product "
                "storage; vaccine seed-bank storage"
            ),
            strengths=(
                "LN₂ vapor (-196 °C) preserves cell "
                "viability indefinitely; vapor phase (not "
                "submerged) eliminates cross-contamination "
                "risk between vials"
            ),
            limitations=(
                "Capital + LN₂ supply infrastructure; vial "
                "format restricted to cryo-vials (no "
                "deep-well plates)"
            ),
        ),
    ]


_ANALYSERS: List[LabAnalyser] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_analysers(category: Optional[str] = None
                   ) -> List[LabAnalyser]:
    if category is None:
        return list(_ANALYSERS)
    if category not in VALID_CATEGORIES:
        return []
    return [a for a in _ANALYSERS if a.category == category]


def get_analyser(analyser_id: str) -> Optional[LabAnalyser]:
    for a in _ANALYSERS:
        if a.id == analyser_id:
            return a
    return None


def find_analysers(needle: str) -> List[LabAnalyser]:
    """Case-insensitive substring search across id + name +
    manufacturer + category."""
    if not needle:
        return []
    n = needle.lower().strip()
    return [a for a in _ANALYSERS
            if n in a.id.lower() or n in a.name.lower()
            or n in a.manufacturer.lower()
            or n in a.category.lower()]


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def to_dict(a: LabAnalyser) -> Dict[str, str]:
    return {
        "id": a.id,
        "name": a.name,
        "manufacturer": a.manufacturer,
        "category": a.category,
        "function": a.function,
        "typical_throughput": a.typical_throughput,
        "sample_volume": a.sample_volume,
        "detection_method": a.detection_method,
        "typical_assays": a.typical_assays,
        "strengths": a.strengths,
        "limitations": a.limitations,
        "notes": a.notes,
    }
