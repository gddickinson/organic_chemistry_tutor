"""Phase CB-1.0 (round 212) — cell-signalling pathway catalogue.

25 canonical signalling pathways covering the major modules taught
in undergraduate + graduate cell biology.  Each entry carries:

- Receptor class + key downstream components (in pathway order).
- Canonical biological function.
- Disease associations.
- Drug targets (drug + target tuples) — bridges Cell Bio Studio
  to the future Pharmacology Studio.
- Cross-references to ``orgchem`` molecule names — bridges to
  OrgChem Studio's small-molecule catalogue.
- Cross-references to other cellbio signalling pathways — supports
  the multi-studio link audit.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


CATEGORIES: Tuple[str, ...] = (
    "growth-factor",        # MAPK, PI3K-Akt, EGFR, insulin
    "cytokine",             # JAK-STAT, TGF-β
    "morphogen",            # Wnt, Notch, Hedgehog
    "second-messenger",     # GPCR/cAMP/PKA, GPCR/IP3/Ca²⁺, PKC, CaMKII
    "stress-response",      # NF-κB, p53, HIF-1α, Hippo-YAP
    "nutrient-energy",      # AMPK, mTORC1
    "innate-immunity",      # TLR, cGAS-STING
    "adaptive-immunity",    # TCR
    "cell-death",           # apoptosis (intrinsic + extrinsic), necroptosis, pyroptosis
)

RECEPTOR_CLASSES: Tuple[str, ...] = (
    "RTK",                  # receptor tyrosine kinase
    "GPCR",                 # G-protein-coupled receptor
    "cytokine-receptor",    # JAK-coupled
    "TGF-β-receptor",       # serine-threonine kinase
    "Frizzled",             # Wnt
    "Notch",                # Notch
    "Patched-Smoothened",   # Hh
    "TNF-receptor",         # death receptors
    "Toll-like-receptor",   # TLR
    "cytosolic-sensor",     # cGAS, NLRP3
    "TCR",                  # T-cell receptor
    "intracellular-sensor", # AMPK, mTOR (kinases not receptors)
    "transcription-factor", # p53, HIF-1α (act as the effector)
    "GTPase-cascade",       # Ras-Raf, RhoA
)


@dataclass(frozen=True)
class SignalingPathway:
    """One canonical cell-signalling pathway."""
    id: str
    name: str
    category: str
    receptor_class: str
    key_components: Tuple[str, ...]
    canonical_function: str
    disease_associations: Tuple[str, ...]
    # Tuples of (drug-name, target) — drug names also cross-
    # reference orgchem.db.Molecule rows when seeded.
    drug_targets: Tuple[Tuple[str, str], ...]
    # Names of orgchem molecules referenced (drugs, second
    # messengers).  Empty tuple = no orgchem cross-ref.
    cross_reference_molecule_names: Tuple[str, ...]
    # Ids of sister cellbio signalling pathways.
    cross_reference_pathway_ids: Tuple[str, ...]
    notes: str = ""


# ----------------------------------------------------------------
# 25-pathway catalogue
# ----------------------------------------------------------------
_PATHWAYS: List[SignalingPathway] = [

    SignalingPathway(
        id="mapk-erk",
        name="MAPK / ERK pathway",
        category="growth-factor",
        receptor_class="RTK",
        key_components=("Ras", "Raf", "MEK1/2", "ERK1/2",
                        "RSK", "Elk-1"),
        canonical_function="Growth-factor-induced cell "
                           "proliferation, survival, "
                           "differentiation.",
        disease_associations=("RAS-mutant cancer",
                              "BRAF-mutant melanoma",
                              "RASopathies (Noonan, "
                              "cardiofaciocutaneous)"),
        drug_targets=(("Vemurafenib", "BRAF V600E"),
                      ("Trametinib", "MEK1/2"),
                      ("Cobimetinib", "MEK1/2")),
        cross_reference_molecule_names=("Vemurafenib",
                                        "Trametinib"),
        cross_reference_pathway_ids=("pi3k-akt-mtor",
                                     "egfr-ras-raf",
                                     "p53"),
        notes="~30 % of human cancers harbour RAS or RAF "
              "mutations; the pathway is the textbook example "
              "of a kinase cascade.",
    ),
    SignalingPathway(
        id="pi3k-akt-mtor",
        name="PI3K / Akt / mTOR pathway",
        category="growth-factor",
        receptor_class="RTK",
        key_components=("PI3K", "PIP3", "Akt (PKB)", "TSC1/2",
                        "Rheb", "mTORC1", "S6K1", "4E-BP1"),
        canonical_function="Growth-factor-induced anabolism + "
                           "cell growth + survival; integrates "
                           "with nutrient signals via mTORC1.",
        disease_associations=("PIK3CA-mutant cancer",
                              "PTEN-loss cancer",
                              "Cowden syndrome",
                              "tuberous sclerosis"),
        drug_targets=(("Alpelisib", "PI3Kα"),
                      ("Idelalisib", "PI3Kδ"),
                      ("Everolimus", "mTORC1"),
                      ("Sirolimus", "mTORC1")),
        cross_reference_molecule_names=("Sirolimus",
                                        "Everolimus"),
        cross_reference_pathway_ids=("mapk-erk",
                                     "ampk",
                                     "mtorc1-aa-sensing",
                                     "insulin"),
        notes="PTEN is a tumour suppressor that opposes PI3K; "
              "loss of PTEN is among the most common cancer "
              "mutations.",
    ),
    SignalingPathway(
        id="jak-stat",
        name="JAK / STAT pathway",
        category="cytokine",
        receptor_class="cytokine-receptor",
        key_components=("Cytokine receptor (e.g. IFNAR, IL-6R)",
                        "JAK1/2/3 / TYK2", "STAT1-6",
                        "phosphotyrosine SH2 docking",
                        "STAT dimerisation",
                        "nuclear translocation"),
        canonical_function="Cytokine + interferon + growth-"
                           "hormone signalling → transcription "
                           "of immune-response + haematopoiesis "
                           "genes.",
        disease_associations=("Myeloproliferative neoplasms "
                              "(JAK2 V617F)",
                              "rheumatoid arthritis",
                              "psoriasis",
                              "inflammatory bowel disease"),
        drug_targets=(("Tofacitinib", "JAK1/3"),
                      ("Ruxolitinib", "JAK1/2"),
                      ("Baricitinib", "JAK1/2"),
                      ("Upadacitinib", "JAK1")),
        cross_reference_molecule_names=("Tofacitinib",
                                        "Ruxolitinib"),
        cross_reference_pathway_ids=("nf-kb", "tlr"),
        notes="JAK inhibitors are a major modern class for "
              "autoimmune disease; black-box warning for "
              "thrombosis + infection.",
    ),
    SignalingPathway(
        id="wnt-beta-catenin",
        name="Wnt / β-catenin pathway",
        category="morphogen",
        receptor_class="Frizzled",
        key_components=("Wnt ligand", "Frizzled receptor",
                        "LRP5/6 co-receptor", "Dishevelled",
                        "destruction complex (APC, Axin, GSK-3β, "
                        "CK1)", "β-catenin stabilisation",
                        "TCF / LEF transcription"),
        canonical_function="Stem-cell self-renewal + body-axis "
                           "patterning + intestinal-crypt "
                           "homeostasis.",
        disease_associations=("Familial adenomatous polyposis "
                              "(APC mutations)",
                              "colorectal cancer (APC, "
                              "β-catenin)",
                              "hepatocellular carcinoma"),
        drug_targets=(("Porcupine inhibitors (LGK974)",
                       "Wnt acylation"),
                      ("Tankyrase inhibitors (XAV939)",
                       "Axin stabilisation")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("notch", "hedgehog",
                                     "tgf-beta-smad"),
        notes="APC mutations are the second-most-common "
              "tumour-suppressor lesion (after p53); drive "
              "> 80 % of colorectal cancers.",
    ),
    SignalingPathway(
        id="notch",
        name="Notch signalling",
        category="morphogen",
        receptor_class="Notch",
        key_components=("Notch ligand (Delta, Jagged)",
                        "Notch receptor", "ADAM10 (S2 cleavage)",
                        "γ-secretase (S3 cleavage)",
                        "NICD (Notch intracellular domain)",
                        "CSL (RBPJ) transcription factor",
                        "MAML co-activator"),
        canonical_function="Cell-fate decisions via lateral "
                           "inhibition; T-cell vs B-cell fate; "
                           "neuronal vs glial fate; vascular "
                           "patterning.",
        disease_associations=("T-ALL (NOTCH1 activating "
                              "mutations)",
                              "CADASIL (NOTCH3 mutation)",
                              "Alagille syndrome"),
        drug_targets=(("γ-secretase inhibitors (e.g. MK-0752)",
                       "Notch S3 cleavage"),),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("wnt-beta-catenin",
                                     "hedgehog"),
        notes="γ-secretase is the same enzyme that cleaves "
              "APP to generate amyloid-β; γ-sec inhibitors "
              "explored for both Notch-driven cancer + "
              "Alzheimer's.",
    ),
    SignalingPathway(
        id="hedgehog",
        name="Hedgehog (Hh) signalling",
        category="morphogen",
        receptor_class="Patched-Smoothened",
        key_components=("Hh ligand (Sonic / Indian / Desert)",
                        "Patched (PTCH1) receptor",
                        "Smoothened (SMO) GPCR-family",
                        "SUFU", "Gli1/2/3 transcription factors"),
        canonical_function="Embryonic patterning (limb bud, "
                           "neural tube); adult tissue "
                           "regeneration.",
        disease_associations=("Basal-cell carcinoma "
                              "(PTCH1 loss / SMO activation)",
                              "medulloblastoma (SHH subgroup)",
                              "Gorlin syndrome"),
        drug_targets=(("Vismodegib", "SMO"),
                      ("Sonidegib", "SMO"),
                      ("Glasdegib", "SMO")),
        cross_reference_molecule_names=("Vismodegib",),
        cross_reference_pathway_ids=("wnt-beta-catenin",
                                     "notch"),
        notes="First Hh inhibitor (vismodegib) approved 2012 "
              "for basal-cell carcinoma — proof-of-concept "
              "that targeting a developmental pathway can "
              "treat adult cancer.",
    ),
    SignalingPathway(
        id="nf-kb",
        name="NF-κB pathway (canonical)",
        category="stress-response",
        receptor_class="TNF-receptor",
        key_components=("TNFα / IL-1 / LPS",
                        "TNFR1 / IL-1R / TLR4", "MyD88 / TRADD",
                        "IKKβ / IKKα / NEMO", "IκBα phosphorylation",
                        "p50/p65 nuclear translocation",
                        "NF-κB-dependent transcription"),
        canonical_function="Inflammation; immune-cell activation; "
                           "anti-apoptotic gene expression "
                           "(BCL-XL, IAPs).",
        disease_associations=("Rheumatoid arthritis",
                              "inflammatory bowel disease",
                              "many cancers (constitutive "
                              "activation)",
                              "ectodermal dysplasia"),
        drug_targets=(("Bortezomib", "26S proteasome → IκBα "
                                     "degradation block"),
                      ("Anti-TNF biologics (infliximab, "
                       "adalimumab, etanercept)", "TNFα")),
        cross_reference_molecule_names=("Bortezomib",),
        cross_reference_pathway_ids=("tlr", "tnf-extrinsic-apoptosis",
                                     "jak-stat"),
        notes="Constitutively active in many lymphomas + "
              "carcinomas; non-canonical NF-κB pathway "
              "(p100/RelB) handles lymphoid-organ development.",
    ),
    SignalingPathway(
        id="tgf-beta-smad",
        name="TGF-β / Smad pathway",
        category="cytokine",
        receptor_class="TGF-β-receptor",
        key_components=("TGF-β ligand", "TβRII (constitutively "
                        "active kinase)",
                        "TβRI (ALK5)", "Smad2/3 phosphorylation",
                        "Smad4 partner", "nuclear import + "
                        "DNA binding"),
        canonical_function="Cytostasis in epithelial cells; "
                           "EMT in development + cancer; "
                           "fibrosis; immune suppression.",
        disease_associations=("Pancreatic cancer (SMAD4 loss)",
                              "Marfan syndrome (FBN1 → "
                              "altered TGF-β release)",
                              "fibrosis (lung, liver, kidney)",
                              "scleroderma"),
        drug_targets=(("Galunisertib", "TβRI / ALK5"),
                      ("Fresolimumab", "TGF-β1/2/3")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("wnt-beta-catenin",
                                     "p53", "intrinsic-apoptosis"),
        notes="Dual role in cancer — tumour suppressor early "
              "(growth arrest), then driver of EMT + invasion "
              "later (the *TGF-β paradox*).",
    ),
    SignalingPathway(
        id="gpcr-camp-pka",
        name="GPCR / cAMP / PKA pathway",
        category="second-messenger",
        receptor_class="GPCR",
        key_components=("GPCR (e.g. β-adrenergic, glucagon, "
                        "vasopressin)", "Gαs",
                        "adenylyl cyclase", "cAMP", "PKA",
                        "CREB phosphorylation", "EPAC"),
        canonical_function="Heart-rate + force (β1-AR), "
                           "bronchodilation (β2-AR), "
                           "lipolysis, gluconeogenesis, water "
                           "retention.",
        disease_associations=("Heart failure",
                              "asthma",
                              "Cushing's syndrome (PRKACA "
                              "mutations)",
                              "MEN1"),
        drug_targets=(("Salbutamol", "β2-AR agonist"),
                      ("Propranolol", "β1/β2-AR antagonist"),
                      ("Metoprolol", "β1-AR antagonist"),
                      ("Glucagon", "GCGR agonist")),
        cross_reference_molecule_names=("Salbutamol",
                                        "Propranolol",
                                        "Metoprolol",
                                        "cAMP",
                                        "ATP"),
        cross_reference_pathway_ids=("gpcr-ip3-ca",
                                     "pkc-dag-ca", "camkii"),
        notes="Most-targeted single signalling pathway in "
              "modern pharmacology — > 30 % of all approved "
              "drugs hit a GPCR.",
    ),
    SignalingPathway(
        id="gpcr-ip3-ca",
        name="GPCR / IP₃ / Ca²⁺ pathway",
        category="second-messenger",
        receptor_class="GPCR",
        key_components=("GPCR (e.g. M1/3 muscarinic, α1-AR, "
                        "AT1, V1)", "Gαq",
                        "PLCβ", "IP₃ + DAG", "IP₃R on ER",
                        "Ca²⁺ release", "calmodulin",
                        "MLCK, calcineurin, CaMKII"),
        canonical_function="Smooth-muscle contraction "
                           "(vasoconstriction, GI motility), "
                           "exocytosis, gene transcription via "
                           "NFAT.",
        disease_associations=("Hypertension",
                              "irritable bowel syndrome",
                              "neurodegeneration (Ca²⁺ "
                              "dyshomeostasis)"),
        drug_targets=(("Losartan", "AT1 receptor antagonist"),
                      ("Doxazosin", "α1-AR antagonist"),
                      ("Atropine", "M1/M3 muscarinic "
                                   "antagonist")),
        cross_reference_molecule_names=("Losartan",
                                        "Atropine"),
        cross_reference_pathway_ids=("gpcr-camp-pka",
                                     "pkc-dag-ca", "camkii"),
        notes="DAG also activates PKC; IP₃ + DAG arms split "
              "from a single PIP₂ hydrolysis event so "
              "downstream Ca²⁺ + PKC arrive together.",
    ),
    SignalingPathway(
        id="pkc-dag-ca",
        name="PKC family signalling",
        category="second-messenger",
        receptor_class="GPCR",
        key_components=("DAG (from PIP₂)", "Ca²⁺ (for cPKC)",
                        "PKC (cPKC, nPKC, aPKC isoforms)",
                        "MARCKS, Raf, GSK-3β substrates"),
        canonical_function="Diverse: cell proliferation "
                           "(cPKC), apoptosis (nPKC), polarity "
                           "(aPKC), neuronal plasticity.",
        disease_associations=("Cancer (PKC isoforms diverge — "
                              "some pro-, some anti-tumour)",
                              "diabetes (PKCβ → diabetic "
                              "complications)"),
        drug_targets=(("Ruboxistaurin", "PKCβ"),
                      ("Sotrastaurin", "pan-PKC")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("gpcr-ip3-ca",
                                     "mapk-erk"),
        notes="Phorbol esters (TPA) are tumour promoters "
              "because they bypass DAG regulation + "
              "constitutively activate cPKC + nPKC isoforms.",
    ),
    SignalingPathway(
        id="camkii",
        name="Ca²⁺ / Calmodulin / CaMKII pathway",
        category="second-messenger",
        receptor_class="GPCR",
        key_components=("Ca²⁺ rise", "calmodulin",
                        "CaMKII (12-subunit holoenzyme)",
                        "T286 autophosphorylation",
                        "AMPA receptors, CREB, MEF2 substrates"),
        canonical_function="Synaptic plasticity (LTP), cardiac "
                           "excitation-contraction coupling, "
                           "memory formation.",
        disease_associations=("Heart failure (CaMKIIδ "
                              "hyperactivation)",
                              "atrial fibrillation",
                              "intellectual disability "
                              "(CAMK2A/B mutations)"),
        drug_targets=(("KN-93", "CaMKII (research tool)"),
                      ("Ryanodine-receptor stabilisers "
                       "(rycals)", "RyR2-CaMKII axis")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("gpcr-ip3-ca", "pkc-dag-ca"),
        notes="T286 autophosphorylation makes CaMKII a "
              "molecular memory — once activated by a Ca²⁺ "
              "transient, stays active until phosphatases "
              "(PP1, PP2A) reset it.",
    ),
    SignalingPathway(
        id="tlr",
        name="Toll-like receptor (TLR) pathway",
        category="innate-immunity",
        receptor_class="Toll-like-receptor",
        key_components=("PAMP (LPS, dsRNA, CpG DNA, flagellin)",
                        "TLR1-10",
                        "MyD88 (or TRIF)", "IRAK1/4", "TRAF6",
                        "TAK1", "IKK", "NF-κB + IRF3/7",
                        "type I IFN + cytokines"),
        canonical_function="First-line innate immune detection "
                           "of microbial molecules; bridges to "
                           "adaptive immunity via dendritic "
                           "cells.",
        disease_associations=("Sepsis",
                              "autoimmune disease (TLR7 in "
                              "lupus)",
                              "inflammatory cancer microenv."),
        drug_targets=(("Hydroxychloroquine", "TLR7/9 (endosomal "
                                              "acidification)"),
                      ("Vidofludimus + IRAK4 inhibitors",
                       "IRAK4")),
        cross_reference_molecule_names=("Hydroxychloroquine",),
        cross_reference_pathway_ids=("nf-kb", "cgas-sting",
                                     "jak-stat"),
        notes="TLR4 was the first innate-immune receptor "
              "characterised (Beutler / Hoffmann, 2011 Nobel "
              "with Steinman).",
    ),
    SignalingPathway(
        id="cgas-sting",
        name="cGAS / STING pathway",
        category="innate-immunity",
        receptor_class="cytosolic-sensor",
        key_components=("cytosolic dsDNA (viral or self)",
                        "cGAS", "2'3'-cGAMP",
                        "STING (ER → Golgi)", "TBK1",
                        "IRF3 phosphorylation",
                        "type I IFN-β"),
        canonical_function="Cytosolic DNA sensing → type I "
                           "interferon response → antiviral + "
                           "antitumour immunity.",
        disease_associations=("Aicardi-Goutières syndrome "
                              "(self-DNA inflammation)",
                              "STING-associated vasculopathy",
                              "cancer immune-evasion (cGAS "
                              "loss)"),
        drug_targets=(("STING agonists (ADU-S100, MK-1454)",
                       "STING (cancer immunotherapy)"),
                      ("STING antagonists (in dev for SAVI)",
                       "STING")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("tlr", "nf-kb",
                                     "intrinsic-apoptosis"),
        notes="Discovered ~ 2013 (Chen, Vance, Barber); "
              "STING agonists are a major modern cancer-"
              "immunotherapy class.",
    ),
    SignalingPathway(
        id="hippo-yap",
        name="Hippo / YAP-TAZ pathway",
        category="stress-response",
        receptor_class="intracellular-sensor",
        key_components=("contact inhibition / mechanical cues",
                        "MST1/2 kinase", "LATS1/2 kinase",
                        "YAP / TAZ phosphorylation",
                        "14-3-3 cytoplasmic retention",
                        "TEAD-family transcription"),
        canonical_function="Organ-size control; contact "
                           "inhibition; mechanotransduction; "
                           "regeneration.",
        disease_associations=("Mesothelioma (NF2 / Merlin loss)",
                              "hepatocellular carcinoma",
                              "uveal melanoma"),
        drug_targets=(("Verteporfin", "YAP-TEAD interaction"),
                      ("VT3989 + IAG933", "TEAD palmitoylation"),),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("wnt-beta-catenin",
                                     "tgf-beta-smad",
                                     "pi3k-akt-mtor"),
        notes="The cell-size + organ-size sensor — discovered "
              "in Drosophila as the *hippo* mutant (organs grew "
              "to giant size).  Converging evidence ties it "
              "to mechanobiology + tissue stiffness.",
    ),
    SignalingPathway(
        id="ampk",
        name="AMPK pathway",
        category="nutrient-energy",
        receptor_class="intracellular-sensor",
        key_components=("AMP / ADP rise (low-energy)", "LKB1 "
                        "kinase", "AMPK (αβγ heterotrimer)",
                        "T172 phosphorylation",
                        "ACC, HMG-CoA reductase, mTORC1, "
                        "TBC1D1 substrates"),
        canonical_function="Master metabolic switch — turns "
                           "ON catabolism (β-oxidation, "
                           "glucose uptake), turns OFF "
                           "anabolism (FA synthesis, "
                           "cholesterol synthesis, mTORC1).",
        disease_associations=("Type 2 diabetes",
                              "obesity",
                              "cancer (AMPK suppresses Warburg "
                              "effect)"),
        drug_targets=(("Metformin", "AMPK (indirect — mitochondrial "
                                     "complex I → ↑AMP/ATP)"),
                      ("AICAR", "AMPK (direct AMP mimetic)"),
                      ("MK-8722", "direct AMPK activator")),
        cross_reference_molecule_names=("Metformin",
                                        "ATP", "ADP", "AMP"),
        cross_reference_pathway_ids=("pi3k-akt-mtor",
                                     "mtorc1-aa-sensing",
                                     "insulin"),
        notes="Metformin is the most-prescribed diabetes drug "
              "globally; AMPK is also the target of many "
              "polyphenols (resveratrol, EGCG) — clinical "
              "evidence is mixed.",
    ),
    SignalingPathway(
        id="hif1a",
        name="HIF-1α / hypoxia response",
        category="stress-response",
        receptor_class="transcription-factor",
        key_components=("oxygen tension", "PHD1/2/3 prolyl "
                        "hydroxylases", "VHL E3 ligase",
                        "HIF-1α stabilisation under hypoxia",
                        "HIF-1β (ARNT) dimerisation",
                        "HRE-element transcription "
                        "(VEGF, EPO, GLUT1)"),
        canonical_function="Adaptive response to low O₂ — "
                           "angiogenesis (VEGF), "
                           "erythropoiesis (EPO), glycolytic "
                           "shift (GLUT1, LDHA).",
        disease_associations=("Clear-cell renal cell carcinoma "
                              "(VHL loss)",
                              "polycythaemia",
                              "ischaemic heart disease",
                              "Warburg effect in cancer"),
        drug_targets=(("Roxadustat / Daprodustat / "
                       "Vadadustat", "PHD inhibitors → "
                                     "boost EPO in CKD anaemia"),
                      ("Belzutifan", "HIF-2α antagonist for "
                                     "VHL-disease cancers")),
        cross_reference_molecule_names=("Roxadustat",
                                        "Belzutifan"),
        cross_reference_pathway_ids=("p53", "ampk"),
        notes="2019 Nobel: Kaelin / Ratcliffe / Semenza for "
              "the O₂-sensing mechanism (PHD-mediated proline "
              "hydroxylation requires O₂ as a substrate).",
    ),
    SignalingPathway(
        id="p53",
        name="p53 stress-response pathway",
        category="stress-response",
        receptor_class="transcription-factor",
        key_components=("DNA damage / oncogene stress / hypoxia",
                        "ATM / ATR / DNA-PK kinases",
                        "p53 phosphorylation + stabilisation",
                        "MDM2 antagonism", "p21 (cell-cycle "
                        "arrest)", "PUMA + BAX (apoptosis)",
                        "GADD45 (DNA repair)"),
        canonical_function="Genome-guardian — arrests cell "
                           "cycle for repair, or triggers "
                           "apoptosis if damage too great.",
        disease_associations=("Most common tumour-suppressor "
                              "lesion (~ 50 % of all cancers "
                              "have TP53 mutation)",
                              "Li-Fraumeni syndrome "
                              "(germline TP53)"),
        drug_targets=(("Nutlin-3 / Idasanutlin",
                       "MDM2-p53 interaction"),
                      ("APR-246 (eprenetapopt)",
                       "mutant p53 reactivator")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("intrinsic-apoptosis",
                                     "mapk-erk", "hif1a"),
        notes="The original tumour suppressor.  MDM2 is its "
              "main negative regulator; restoring p53 by "
              "blocking MDM2 is a major drug-discovery target.",
    ),
    SignalingPathway(
        id="intrinsic-apoptosis",
        name="Intrinsic (mitochondrial) apoptosis",
        category="cell-death",
        receptor_class="intracellular-sensor",
        key_components=("BH3-only proteins (BIM, BID, PUMA, "
                        "NOXA)", "BAX / BAK pore formation",
                        "MOMP (mitochondrial outer-membrane "
                        "permeabilisation)", "cytochrome c "
                        "release", "APAF1 + caspase-9 "
                        "apoptosome", "executioner caspase-3/7"),
        canonical_function="Programmed cell death triggered by "
                           "internal stress — DNA damage, "
                           "growth-factor withdrawal, ER stress, "
                           "oxidative stress.",
        disease_associations=("Cancer (BCL-2 overexpression)",
                              "neurodegeneration (excessive "
                              "neuronal death)",
                              "ischaemia-reperfusion injury"),
        drug_targets=(("Venetoclax", "BCL-2 (CLL, AML)"),
                      ("Navitoclax", "BCL-2 / BCL-XL"),
                      ("BH3 mimetics (S64315 / MIK665)",
                       "MCL-1")),
        cross_reference_molecule_names=("Venetoclax",),
        cross_reference_pathway_ids=("p53",
                                     "tnf-extrinsic-apoptosis",
                                     "necroptosis", "tgf-beta-smad"),
        notes="BCL-2 family balance (pro-apoptotic vs anti-"
              "apoptotic) is the key gate.  Venetoclax was the "
              "first approved BH3-mimetic, transforming CLL "
              "treatment.",
    ),
    SignalingPathway(
        id="tnf-extrinsic-apoptosis",
        name="Extrinsic (death-receptor) apoptosis",
        category="cell-death",
        receptor_class="TNF-receptor",
        key_components=("FasL / TNF / TRAIL", "Fas / TNFR1 / "
                        "DR4-5", "FADD", "DISC formation",
                        "caspase-8 + caspase-10", "BID "
                        "cleavage (cross-talk to intrinsic)",
                        "executioner caspase-3/7"),
        canonical_function="Immune-mediated killing (CTL of "
                           "infected / tumour cells), liver "
                           "homeostasis, immune-privilege "
                           "tissue protection.",
        disease_associations=("Autoimmune lymphoproliferative "
                              "syndrome (FAS mutation)",
                              "fulminant hepatic failure",
                              "TRAIL resistance in cancer"),
        drug_targets=(("TRAIL receptor agonists "
                       "(dulanermin, conatumumab)",
                       "DR4 / DR5"),
                      ("FLIP-targeting agents (in dev)",
                       "cFLIP")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("intrinsic-apoptosis",
                                     "necroptosis", "nf-kb"),
        notes="Cross-talks with intrinsic via caspase-8 → BID → "
              "tBID → MOMP — *type II* cells need this "
              "amplification loop.",
    ),
    SignalingPathway(
        id="necroptosis",
        name="Necroptosis",
        category="cell-death",
        receptor_class="TNF-receptor",
        key_components=("TNF + caspase-8 inhibition",
                        "RIPK1", "RIPK3", "MLKL "
                        "phosphorylation + oligomerisation",
                        "membrane rupture"),
        canonical_function="Backup death pathway when caspase-8 "
                           "is blocked (e.g. viral infection, "
                           "caspase-inhibitor drugs); highly "
                           "inflammatory.",
        disease_associations=("Multiple sclerosis",
                              "ALS",
                              "ischaemia-reperfusion (heart, "
                              "kidney, brain)",
                              "inflammatory bowel disease"),
        drug_targets=(("Necrostatin-1s", "RIPK1 (research tool)"),
                      ("GSK2982772", "RIPK1 (clinical trials "
                                      "for psoriasis, RA)")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("tnf-extrinsic-apoptosis",
                                     "intrinsic-apoptosis",
                                     "pyroptosis", "nf-kb"),
        notes="Discovered ~ 2005 (Yuan, Vandenabeele); the "
              "modern view is that all three lytic deaths "
              "(necroptosis, pyroptosis, ferroptosis) are "
              "highly regulated, not accidental.",
    ),
    SignalingPathway(
        id="pyroptosis",
        name="Pyroptosis (inflammasome death)",
        category="cell-death",
        receptor_class="cytosolic-sensor",
        key_components=("PAMP / DAMP detection (LPS, ATP, "
                        "uric acid)", "NLRP3 / AIM2 / NLRC4 "
                        "inflammasome", "caspase-1 / 4 / 5 / 11 "
                        "activation", "gasdermin D cleavage",
                        "GSDMD-N pore", "IL-1β + IL-18 release",
                        "membrane rupture"),
        canonical_function="Inflammatory cell death + cytokine "
                           "release in response to intracellular "
                           "pathogens or sterile danger signals.",
        disease_associations=("Cryopyrin-associated periodic "
                              "syndromes (CAPS — NLRP3 gain-of-"
                              "function)",
                              "gout (uric-acid → NLRP3)",
                              "Alzheimer's (Aβ → NLRP3)",
                              "sepsis"),
        drug_targets=(("Anakinra", "IL-1 receptor antagonist"),
                      ("Canakinumab", "IL-1β neutralisation"),
                      ("MCC950 / OLT1177",
                       "NLRP3 inhibitor (clinical trials)")),
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=("tlr", "cgas-sting",
                                     "necroptosis", "nf-kb"),
        notes="Gasdermin D pore identified ~ 2015; revolutionised "
              "the inflammasome field by giving the long-sought "
              "lytic effector a name + structure.",
    ),
    SignalingPathway(
        id="mtorc1-aa-sensing",
        name="mTORC1 amino-acid sensing",
        category="nutrient-energy",
        receptor_class="intracellular-sensor",
        key_components=("leucine + arginine + methionine",
                        "Sestrin1/2 (leucine sensor)",
                        "CASTOR1/2 (arginine sensor)",
                        "SAMTOR (methionine sensor)",
                        "GATOR1 (GAP) + GATOR2",
                        "Rag GTPase heterodimer",
                        "Ragulator on lysosome",
                        "mTORC1 recruitment"),
        canonical_function="Translation rate + cell growth "
                           "responsive to amino-acid availability "
                           "via lysosomal sensing.",
        disease_associations=("Cancer (mTORC1 hyperactivation)",
                              "tuberous sclerosis",
                              "PTEN hamartoma syndromes"),
        drug_targets=(("Rapamycin (sirolimus)", "FKBP12-mTORC1"),
                      ("Everolimus", "FKBP12-mTORC1"),
                      ("Torin1 / Torin2",
                       "ATP-competitive mTOR inhibitor")),
        cross_reference_molecule_names=("Sirolimus",
                                        "Everolimus",
                                        "L-Leucine",
                                        "L-Arginine"),
        cross_reference_pathway_ids=("pi3k-akt-mtor", "ampk",
                                     "insulin"),
        notes="The lysosome is now recognised as a central "
              "metabolic-signalling hub — Sabatini group's "
              "discovery of the Ragulator complex (~ 2010-2014) "
              "rewrote textbook accounts.",
    ),
    SignalingPathway(
        id="insulin",
        name="Insulin signalling",
        category="growth-factor",
        receptor_class="RTK",
        key_components=("insulin", "insulin receptor (IR)",
                        "IRS1/2 phosphorylation",
                        "PI3K → Akt", "GLUT4 translocation",
                        "GSK-3β inhibition → glycogen synthesis",
                        "FoxO inhibition", "mTORC1 activation"),
        canonical_function="Glucose uptake (muscle, adipose), "
                           "glycogen synthesis, lipogenesis, "
                           "anabolism after a meal.",
        disease_associations=("Type 2 diabetes (insulin "
                              "resistance)",
                              "type 1 diabetes (insulin "
                              "deficiency)",
                              "PCOS",
                              "metabolic syndrome"),
        drug_targets=(("Insulin (exogenous)", "IR agonist"),
                      ("Metformin", "indirect via AMPK"),
                      ("GLP-1 agonists (semaglutide, "
                       "liraglutide)", "GLP-1R → insulin "
                                       "secretion")),
        cross_reference_molecule_names=("Metformin",
                                        "Glucose"),
        cross_reference_pathway_ids=("pi3k-akt-mtor", "ampk",
                                     "mtorc1-aa-sensing"),
        notes="GLP-1 agonists have transformed obesity + "
              "diabetes treatment since 2020 (Wegovy, Mounjaro, "
              "Zepbound).",
    ),
    SignalingPathway(
        id="egfr-ras-raf",
        name="EGFR / RAS / RAF signalling",
        category="growth-factor",
        receptor_class="RTK",
        key_components=("EGF / TGF-α / amphiregulin",
                        "EGFR (HER1) dimerisation",
                        "autophosphorylation",
                        "Grb2 + SOS recruitment",
                        "Ras-GTP loading",
                        "Raf → MEK → ERK"),
        canonical_function="Epithelial proliferation + survival; "
                           "wound healing; major oncogenic "
                           "driver in lung + colon + head-neck "
                           "+ glioblastoma.",
        disease_associations=("Non-small-cell lung cancer "
                              "(EGFR L858R, exon-19 deletions)",
                              "colorectal cancer (KRAS, "
                              "NRAS, BRAF mutations)",
                              "glioblastoma (EGFRvIII)"),
        drug_targets=(("Gefitinib / Erlotinib / Osimertinib",
                       "EGFR ATP site"),
                      ("Cetuximab / Panitumumab",
                       "EGFR extracellular"),
                      ("Sotorasib / Adagrasib", "KRAS G12C")),
        cross_reference_molecule_names=("Gefitinib",
                                        "Erlotinib",
                                        "Sotorasib"),
        cross_reference_pathway_ids=("mapk-erk", "pi3k-akt-mtor",
                                     "p53"),
        notes="KRAS was 'undruggable' for 40 years until "
              "sotorasib (2021) — irreversibly traps KRAS-G12C "
              "in its inactive state via covalent bond to "
              "Cys12.  First-in-class for the most common "
              "human oncogene.",
    ),
    SignalingPathway(
        id="tcr",
        name="T-cell receptor (TCR) signalling",
        category="adaptive-immunity",
        receptor_class="TCR",
        key_components=("peptide-MHC + TCR engagement",
                        "CD4 / CD8 co-receptor",
                        "Lck (Src-family kinase)",
                        "ITAM phosphorylation on CD3 chains",
                        "ZAP-70 recruitment + activation",
                        "LAT scaffold",
                        "PLCγ → DAG + IP₃",
                        "Ras + PKC → NFAT, NF-κB, AP-1"),
        canonical_function="T-cell activation upon antigen "
                           "recognition; differentiation into "
                           "effector + memory subsets.",
        disease_associations=("Autoimmune disease (when "
                              "self-tolerance fails)",
                              "primary immunodeficiency "
                              "(ZAP-70, LAT, RAG mutations)",
                              "T-cell lymphomas"),
        drug_targets=(("Cyclosporin A", "calcineurin → NFAT"),
                      ("Tacrolimus", "FKBP12-calcineurin"),
                      ("Abatacept", "CTLA-4-Ig → CD80/86"),
                      ("Anti-PD-1 / anti-PD-L1 "
                       "(pembrolizumab, nivolumab, atezolizumab)",
                       "checkpoint inhibition")),
        cross_reference_molecule_names=("Tacrolimus",
                                        "Cyclosporine"),
        cross_reference_pathway_ids=("nf-kb", "gpcr-ip3-ca",
                                     "pkc-dag-ca", "jak-stat"),
        notes="Checkpoint inhibitors (anti-PD-1 / anti-CTLA-4) "
              "won the 2018 Nobel (Allison + Honjo) — the "
              "modern revolution in cancer immunotherapy.",
    ),
]


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def list_pathways(
    category: Optional[str] = None,
    receptor_class: Optional[str] = None,
) -> List[SignalingPathway]:
    """Return pathways, optionally filtered by category +
    receptor_class."""
    out = list(_PATHWAYS)
    if category:
        out = [p for p in out if p.category == category]
    if receptor_class:
        out = [p for p in out if p.receptor_class == receptor_class]
    return out


def get_pathway(pathway_id: str) -> Optional[SignalingPathway]:
    """Return one pathway by id, or ``None`` if unknown."""
    for p in _PATHWAYS:
        if p.id == pathway_id:
            return p
    return None


def find_pathways(needle: str) -> List[SignalingPathway]:
    """Case-insensitive substring search across id + name +
    canonical_function + key_components + disease_associations
    + drug_targets."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[SignalingPathway] = []
    for p in _PATHWAYS:
        hay_parts = [p.id, p.name, p.canonical_function]
        hay_parts.extend(p.key_components)
        hay_parts.extend(p.disease_associations)
        for drug, target in p.drug_targets:
            hay_parts.append(drug)
            hay_parts.append(target)
        hay = " ".join(hay_parts).lower()
        if n in hay:
            out.append(p)
    return out


def pathway_to_dict(p: SignalingPathway) -> Dict[str, object]:
    """Serialise to JSON-friendly dict for agent actions."""
    return asdict(p)


def categories() -> Tuple[str, ...]:
    return CATEGORIES


def receptor_classes() -> Tuple[str, ...]:
    return RECEPTOR_CLASSES
