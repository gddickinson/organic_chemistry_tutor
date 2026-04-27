"""Phase BC-1.0 (round 213) — 30-entry enzyme catalogue.

Spans all 7 IUBMB EC classes.  Cross-references use:
- ``cross_reference_molecule_names`` → orgchem ``Molecule.name`` rows
- ``cross_reference_pathway_ids`` → ``orgchem.core.metabolic_pathways`` ids
  (e.g. ``"glycolysis"``, ``"tca_cycle"``, ``"ox_phos"``)
- ``cross_reference_signaling_pathway_ids`` → ``cellbio.core.cell_signaling`` ids
  (e.g. ``"egfr-ras-raf"``, ``"insulin"``, ``"intrinsic-apoptosis"``)
"""
from __future__ import annotations
from typing import List

from biochem.core.enzymes import Enzyme


ENZYMES: List[Enzyme] = [

    # ============================================================
    # EC 1 — Oxidoreductases (5 entries)
    # ============================================================
    Enzyme(
        id="alcohol-dehydrogenase",
        name="Alcohol dehydrogenase (ADH)",
        ec_number="1.1.1.1",
        ec_class=1,
        mechanism_class="Zn²⁺-dependent NAD⁺ dehydrogenase",
        substrates=("Ethanol", "NAD⁺"),
        products=("Acetaldehyde", "NADH", "H⁺"),
        cofactors=("Zn²⁺ (active site)", "NAD⁺"),
        regulators=("Inhibited by fomepizole (4-MP) — used "
                    "clinically for methanol / ethylene glycol "
                    "poisoning",
                    "Competitively inhibited by ethanol vs "
                    "methanol — basis of ethanol antidote"),
        disease_associations=("ALDH2 polymorphism (Asian "
                              "alcohol-flush response)",
                              "Alcoholic liver disease",
                              "Methanol + ethylene glycol "
                              "poisoning"),
        drug_targets=(("Fomepizole", "ADH"),
                      ("Disulfiram (Antabuse)",
                       "ALDH (downstream)")),
        structural_family="MDR (medium-chain dehydrogenase / "
                          "reductase) zinc-binding family",
        cross_reference_molecule_names=("Ethanol", "NAD⁺",
                                        "NADH"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="One of the oldest enzymes characterised "
              "(1937).  Class I ADH1B*2 allele common in East "
              "Asians produces > 100× faster ethanol oxidation.",
    ),
    Enzyme(
        id="lactate-dehydrogenase",
        name="Lactate dehydrogenase (LDH)",
        ec_number="1.1.1.27",
        ec_class=1,
        mechanism_class="NAD⁺-dependent dehydrogenase",
        substrates=("Pyruvate", "NADH", "H⁺"),
        products=("L-Lactate", "NAD⁺"),
        cofactors=("NAD⁺ / NADH",),
        regulators=("Allosteric LDH-A inhibitors (oxamate, "
                    "FX11) explored as anticancer (Warburg "
                    "effect)",),
        disease_associations=("Cardiac LDH-1 release in MI "
                              "(legacy biomarker)",
                              "Cancer Warburg effect — LDH-A "
                              "overexpression → lactate "
                              "production",
                              "Exercise-induced lactate "
                              "accumulation"),
        drug_targets=(("FX11", "LDH-A (preclinical)"),
                      ("Oxamate", "LDH-A (research tool)")),
        structural_family="LDH/MDH-like NAD-binding fold",
        cross_reference_molecule_names=("Pyruvate", "Lactate",
                                        "NAD⁺", "NADH"),
        cross_reference_pathway_ids=("glycolysis",),
        cross_reference_signaling_pathway_ids=("hif1a",),
        notes="LDH-A (M-form) favours pyruvate→lactate; LDH-B "
              "(H-form) favours the reverse.  Tetrameric "
              "enzyme; isozyme ratios are tissue-specific.",
    ),
    Enzyme(
        id="gapdh",
        name="Glyceraldehyde-3-phosphate dehydrogenase (GAPDH)",
        ec_number="1.2.1.12",
        ec_class=1,
        mechanism_class="NAD⁺-dependent oxidative "
                        "phosphorylation of an aldehyde to an "
                        "acyl-phosphate",
        substrates=("Glyceraldehyde-3-phosphate", "NAD⁺",
                    "Pi"),
        products=("1,3-Bisphosphoglycerate", "NADH", "H⁺"),
        cofactors=("NAD⁺", "Active-site Cys (covalent "
                   "thiohemiacetal intermediate)"),
        regulators=("Iodoacetate covalently inhibits the "
                    "active-site Cys (classical biochemistry "
                    "tool)",
                    "Moonlights in apoptosis: nuclear "
                    "translocation upon SNO-modification → "
                    "pro-apoptotic"),
        disease_associations=("Neurodegeneration (Huntington, "
                              "Alzheimer — aggregation)",
                              "Cancer (used as housekeeping "
                              "gene; itself dysregulated)"),
        drug_targets=(("Koningic acid",
                       "GAPDH (covalent active-site "
                       "inhibitor)"),),
        structural_family="Rossmann fold (NAD-binding) + "
                          "C-terminal catalytic domain",
        cross_reference_molecule_names=("NAD⁺", "NADH",
                                        "1,3-Bisphosphoglycerate"),
        cross_reference_pathway_ids=("glycolysis",),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis",),
        notes="Rate-couples carbon flux to redox poise (NAD⁺/"
              "NADH ratio).  Universal house-keeping gene in "
              "qPCR — but its 'moonlighting' nuclear roles "
              "make it actively regulated in many states.",
    ),
    Enzyme(
        id="cytochrome-c-oxidase",
        name="Cytochrome c oxidase (Complex IV)",
        ec_number="1.9.3.1",
        ec_class=1,
        mechanism_class="Heme + Cu binuclear-centre terminal "
                        "oxidase",
        substrates=("Reduced cytochrome c (×4)", "O₂", "H⁺"),
        products=("Oxidised cytochrome c (×4)",
                  "H₂O (×2)"),
        cofactors=("Heme a + heme a3", "Cu_A + Cu_B centres"),
        regulators=("Inhibited by cyanide (CN⁻) at heme a3-"
                    "Cu_B — basis of cyanide poisoning",
                    "Inhibited by carbon monoxide + azide + "
                    "H₂S",
                    "Tissue-specific subunit composition tunes "
                    "activity"),
        disease_associations=("Cyanide poisoning",
                              "Leigh syndrome (mitochondrial "
                              "encephalopathy)",
                              "MELAS",
                              "Cytochrome-c-oxidase deficiency"),
        drug_targets=(("Hydroxocobalamin", "CN⁻ "
                                           "scavenger (rescue)"),
                      ("Methylene blue", "alternative e⁻ "
                                          "acceptor in cyanide "
                                          "rescue")),
        structural_family="Heme-Cu oxygen reductase superfamily",
        cross_reference_molecule_names=("Cyanide",
                                        "Carbon monoxide",
                                        "ATP"),
        cross_reference_pathway_ids=("ox_phos",),
        cross_reference_signaling_pathway_ids=(),
        notes="Reduces O₂ → H₂O (the 'terminal oxidase' of "
              "aerobic life).  Pumps 4 H⁺ per O₂ → contributes "
              "to the proton-motive force.  Cyanide kills "
              "by stalling this step.",
    ),
    Enzyme(
        id="cyp3a4",
        name="Cytochrome P450 3A4 (CYP3A4)",
        ec_number="1.14.14.1",
        ec_class=1,
        mechanism_class="Heme-thiolate monooxygenase "
                        "(O₂-activating)",
        substrates=("Drug substrate (varies)", "O₂", "NADPH"),
        products=("Hydroxylated drug + H₂O", "NADP⁺"),
        cofactors=("Heme b (via Cys-thiolate ligand)",
                   "NADPH (via cytochrome P450 reductase)"),
        regulators=("Induced by rifampin, phenytoin, St John's "
                    "Wort (PXR / CAR transcriptional)",
                    "Inhibited by ketoconazole, ritonavir, "
                    "grapefruit juice furanocoumarins (suicide "
                    "inhibition)"),
        disease_associations=("Drug-drug interactions (~ 50 % "
                              "of all clinical DDIs are "
                              "CYP3A4-mediated)",
                              "Genetic polymorphisms affect "
                              "drug metabolism rates"),
        drug_targets=(("Ketoconazole", "CYP3A4 (azole "
                                       "antifungal)"),
                      ("Ritonavir", "CYP3A4 (boosting agent "
                                    "for PI antivirals)"),
                      ("Cobicistat", "CYP3A4 (HIV regimen "
                                     "booster)")),
        structural_family="Cytochrome P450 fold (heme-thiolate "
                          "monooxygenase superfamily)",
        cross_reference_molecule_names=("NADPH", "NADP⁺",
                                        "Ritonavir",
                                        "Ketoconazole"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Metabolises ~ 30-50 % of clinically used drugs.  "
              "Located in the smooth ER + intestinal "
              "enterocytes.  Industrial use also: hydroxylates "
              "steroid intermediates in pharmaceutical "
              "biocatalysis.",
    ),

    # ============================================================
    # EC 2 — Transferases (5 entries)
    # ============================================================
    Enzyme(
        id="hexokinase",
        name="Hexokinase",
        ec_number="2.7.1.1",
        ec_class=2,
        mechanism_class="ATP-dependent kinase (induced-fit)",
        substrates=("D-Glucose", "ATP"),
        products=("Glucose-6-phosphate", "ADP"),
        cofactors=("Mg²⁺",),
        regulators=("Hexokinase I/II/III: inhibited by "
                    "G6P (product)",
                    "Hexokinase IV (glucokinase, liver / β-"
                    "cell): NOT inhibited by G6P; high Km for "
                    "glucose → 'glucose sensor'"),
        disease_associations=("Maturity-onset diabetes of the "
                              "young (MODY2 — glucokinase "
                              "mutations)",
                              "Hexokinase II overexpression in "
                              "many cancers — Warburg effect"),
                drug_targets=(("Lonidamine",
                               "HK2 (anticancer, mostly "
                               "preclinical)"),),
        structural_family="Actin-fold ATPase (HSP70/sugar-"
                          "kinase superfamily)",
        cross_reference_molecule_names=("Glucose", "ATP",
                                        "ADP",
                                        "Glucose-6-phosphate"),
        cross_reference_pathway_ids=("glycolysis",
                                     "pentose_phosphate"),
        cross_reference_signaling_pathway_ids=("insulin",),
        notes="Classic example of induced fit (Koshland "
              "1958): glucose binding triggers a 12° hinge "
              "rotation that buries ATP.  HK4 (glucokinase) "
              "is the β-cell glucose sensor that triggers "
              "insulin release.",
    ),
    Enzyme(
        id="pka",
        name="Protein kinase A (PKA, cAMP-dependent kinase)",
        ec_number="2.7.11.11",
        ec_class=2,
        mechanism_class="Ser/Thr protein kinase; "
                        "tetrameric R₂C₂ holoenzyme",
        substrates=("Protein-Ser/Thr", "ATP"),
        products=("Protein-Ser-PO₄ / Protein-Thr-PO₄", "ADP"),
        cofactors=("Mg²⁺",),
        regulators=("Activated by cAMP binding to R subunits "
                    "→ release of active C subunits",
                    "Spatially anchored by AKAPs (A-kinase "
                    "anchoring proteins)",
                    "PKI peptide inhibitor"),
        disease_associations=("Carney complex (PRKAR1A loss-"
                              "of-function)",
                              "PRKACA hot-spot mutations in "
                              "Cushing syndrome adenomas"),
        drug_targets=(("H89", "PKA (research tool)"),
                      ("KT5720", "PKA (research tool)")),
        structural_family="Eukaryotic protein kinase fold "
                          "(canonical N + C lobe; 'PKA "
                          "structure' was the first kinase "
                          "X-ray, 1991)",
        cross_reference_molecule_names=("cAMP", "ATP", "ADP"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",),
        notes="The first protein kinase structure solved "
              "(Knighton + Sowadski 1991) — defined the "
              "canonical kinase fold for the 518 kinases of "
              "the human kinome.",
    ),
    Enzyme(
        id="egfr-tk",
        name="Epidermal growth factor receptor tyrosine "
             "kinase (EGFR)",
        ec_number="2.7.10.1",
        ec_class=2,
        mechanism_class="Receptor tyrosine kinase (RTK)",
        substrates=("Self (autophosphorylation) + downstream "
                    "substrates (Grb2, Shc, PLCγ)", "ATP"),
        products=("Phosphotyrosine + ADP",),
        cofactors=("Mg²⁺",),
        regulators=("Activated by EGF / TGFα / amphiregulin → "
                    "ligand-induced dimerisation → trans-"
                    "autophosphorylation",
                    "Down-regulated by Cbl-mediated "
                    "ubiquitination + endocytosis"),
        disease_associations=("NSCLC (L858R, exon 19 deletion, "
                              "T790M resistance)",
                              "Glioblastoma (EGFRvIII)",
                              "Head + neck squamous cell "
                              "carcinoma"),
        drug_targets=(("Gefitinib", "EGFR ATP site (1st gen)"),
                      ("Erlotinib", "EGFR ATP site (1st gen)"),
                      ("Osimertinib", "EGFR T790M (3rd gen)"),
                      ("Cetuximab", "EGFR ECD"),
                      ("Panitumumab", "EGFR ECD")),
        structural_family="Type-I single-pass transmembrane "
                          "RTK; canonical kinase fold + "
                          "PEST-rich C-terminal tail",
        cross_reference_molecule_names=("Gefitinib",
                                        "Erlotinib",
                                        "Osimertinib", "ATP"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=("egfr-ras-raf",
                                               "mapk-erk",
                                               "pi3k-akt-mtor"),
        notes="The first solid-tumour RTK targeted "
              "successfully (gefitinib 2003).  Modern 4th-gen "
              "inhibitors target acquired C797S mutations.",
    ),
    Enzyme(
        id="comt",
        name="Catechol-O-methyltransferase (COMT)",
        ec_number="2.1.1.6",
        ec_class=2,
        mechanism_class="SAM-dependent methyltransferase",
        substrates=("Catechol substrate (dopamine, "
                    "L-DOPA, norepinephrine, epinephrine)",
                    "S-Adenosyl methionine (SAM)"),
        products=("3-O-methyl product",
                  "S-Adenosyl homocysteine (SAH)"),
        cofactors=("Mg²⁺", "SAM (methyl donor)"),
        regulators=("Inhibited by entacapone, tolcapone, "
                    "opicapone (clinical Parkinson's "
                    "adjuncts)",
                    "Val158Met polymorphism affects activity "
                    "+ prefrontal cortex dopamine"),
        disease_associations=("Parkinson's disease (limits "
                              "L-DOPA bioavailability)",
                              "Schizophrenia susceptibility "
                              "(Val158Met)"),
        drug_targets=(("Entacapone", "COMT (peripheral)"),
                      ("Tolcapone", "COMT (CNS-penetrant; "
                                    "hepatotoxicity warning)"),
                      ("Opicapone", "COMT (once-daily)")),
        structural_family="Class I SAM-binding "
                          "methyltransferase fold",
        cross_reference_molecule_names=("L-DOPA", "Dopamine",
                                        "SAM",
                                        "Entacapone"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="In Parkinson's, peripheral COMT degrades "
              "L-DOPA before it reaches the brain; entacapone "
              "blocks this + prolongs L-DOPA action.",
    ),
    Enzyme(
        id="ugt1a1",
        name="UDP-glucuronosyltransferase 1A1 (UGT1A1)",
        ec_number="2.4.1.17",
        ec_class=2,
        mechanism_class="UDP-glucuronic acid-dependent "
                        "glycosyltransferase (Phase II drug "
                        "metabolism)",
        substrates=("Bilirubin / drug aglycone",
                    "UDP-glucuronic acid"),
        products=("Glucuronide conjugate", "UDP"),
        cofactors=("UDP-glucuronic acid (donor)",),
        regulators=("Induced by phenobarbital + rifampin "
                    "(PXR / CAR)",
                    "Inhibited by atazanavir + indinavir"),
        disease_associations=("Gilbert's syndrome (UGT1A1*28 "
                              "polymorphism — mild "
                              "unconjugated "
                              "hyperbilirubinaemia)",
                              "Crigler-Najjar syndrome "
                              "(severe deficiency)",
                              "Irinotecan toxicity (UGT1A1*28 "
                              "→ SN-38 accumulation)"),
        drug_targets=(("Phenobarbital", "UGT1A1 induction "
                                         "(used for Crigler-"
                                         "Najjar II)"),),
        structural_family="GT-B fold (Rossmann-like)",
        cross_reference_molecule_names=("Bilirubin",
                                        "Phenobarbital"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The single most important glucuronidation "
              "enzyme in humans; mutations cause neonatal "
              "jaundice + influence chemotherapy dosing.",
    ),

    # ============================================================
    # EC 3 — Hydrolases (6 entries)
    # ============================================================
    Enzyme(
        id="chymotrypsin",
        name="Chymotrypsin",
        ec_number="3.4.21.1",
        ec_class=3,
        mechanism_class="Serine protease; classical Ser-His-"
                        "Asp catalytic triad",
        substrates=("Protein bond C-terminal to Phe / Trp / "
                    "Tyr (large hydrophobic P1)", "H₂O"),
        products=("Two peptide fragments",),
        cofactors=("None (catalytic triad uses substrate-"
                   "free chemistry)",),
        regulators=("Activated from chymotrypsinogen by "
                    "trypsin cleavage",
                    "Inhibited by PMSF + DFP (irreversible "
                    "Ser195 acylation)",
                    "Inhibited by chymostatin, TPCK "
                    "(reversible)"),
        disease_associations=("Chronic pancreatitis (auto-"
                              "digestion)",
                              "Pancreatic insufficiency "
                              "(replacement therapy with "
                              "Creon, Zenpep)"),
        drug_targets=(("Aprotinin", "trypsin / chymotrypsin "
                                    "(historical use in "
                                    "pancreatitis + cardiac "
                                    "surgery)"),),
        structural_family="Trypsin-like β-barrel serine "
                          "protease",
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Textbook example of serine-protease catalysis: "
              "the Ser-His-Asp triad performs general acid-"
              "base catalysis through a covalent acyl-enzyme "
              "intermediate.  Seeded as one of OrgChem's "
              "active-site mechanisms.",
    ),
    Enzyme(
        id="trypsin",
        name="Trypsin",
        ec_number="3.4.21.4",
        ec_class=3,
        mechanism_class="Serine protease (Ser-His-Asp triad)",
        substrates=("Protein bond C-terminal to Lys / Arg "
                    "(positive P1 specificity pocket)", "H₂O"),
        products=("Two peptide fragments",),
        cofactors=("Ca²⁺ (stability)",),
        regulators=("Activated from trypsinogen by "
                    "enteropeptidase + autoactivation",
                    "Inhibited by SBTI (soybean trypsin "
                    "inhibitor) — a classical lab tool",
                    "Endogenous inhibitor: SPINK1"),
        disease_associations=("Hereditary pancreatitis "
                              "(PRSS1 R122H gain-of-function)",
                              "SPINK1 mutations + pancreatitis"),
        drug_targets=(("Aprotinin", "trypsin (broad "
                                    "spectrum)"),
                      ("Camostat", "trypsin (anti-COVID-19 "
                                   "TMPRSS2 testing route)")),
        structural_family="Trypsin-like β-barrel serine "
                          "protease",
        cross_reference_molecule_names=("Calcium",),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The 'master activator' of pancreatic enzymes "
              "— activates chymotrypsinogen, "
              "procarboxypeptidase, proelastase.  Indispensable "
              "lab reagent for proteomics digests.",
    ),
    Enzyme(
        id="hiv-protease",
        name="HIV-1 protease",
        ec_number="3.4.23.16",
        ec_class=3,
        mechanism_class="Aspartic protease (homodimer; two "
                        "Asp25 active-site residues, one from "
                        "each monomer)",
        substrates=("HIV Gag-Pol polyprotein", "H₂O"),
        products=("Mature viral structural + enzymatic "
                  "proteins",),
        cofactors=("None — water is the nucleophile",),
        regulators=("Inhibited by clinical PIs: ritonavir, "
                    "lopinavir, atazanavir, darunavir",
                    "Drug resistance arises from "
                    "compensatory mutations (V82A, I84V, "
                    "L90M)"),
        disease_associations=("HIV/AIDS — protease cleaves the "
                              "Gag-Pol polyprotein to mature "
                              "the virion",
                              "Drug resistance evolution"),
        drug_targets=(("Ritonavir", "HIV protease (also CYP3A4 "
                                    "boosting in modern "
                                    "regimens)"),
                      ("Darunavir", "HIV protease (high "
                                    "barrier to resistance)"),
                      ("Lopinavir", "HIV protease")),
        structural_family="Pepsin-like fold homodimer "
                          "(retroviral / aspartic protease)",
        cross_reference_molecule_names=("Ritonavir",
                                        "Darunavir",
                                        "Lopinavir"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The first protease to be drug-targeted at "
              "scale (saquinavir 1995); transformed HIV from "
              "death sentence to chronic illness.  Seeded as "
              "one of OrgChem's enzyme-mechanism walks.",
    ),
    Enzyme(
        id="caspase-3",
        name="Caspase-3",
        ec_number="3.4.22.56",
        ec_class=3,
        mechanism_class="Cysteine protease; cleaves C-terminal "
                        "to Asp (DEVD↓ recognition)",
        substrates=("Cellular substrates with DEVD sequence "
                    "(PARP-1, ICAD, gelsolin, lamin A/C, "
                    "actin)", "H₂O"),
        products=("Cleaved substrates",),
        cofactors=("None — Cys163 nucleophile",),
        regulators=("Activated by initiator caspases-8/9 "
                    "(cleavage of pro-form)",
                    "Inhibited by IAPs (XIAP, c-IAP1) until "
                    "Smac/DIABLO release relieves the block",
                    "Pan-caspase inhibitors: Z-VAD-FMK "
                    "(research)"),
        disease_associations=("Cancer (apoptosis evasion)",
                              "Neurodegeneration (excessive "
                              "caspase-3 activation)",
                              "Liver injury",
                              "Ischaemia / reperfusion"),
        drug_targets=(("Emricasan (IDN-6556)", "pan-caspase, "
                                                "tested in "
                                                "NASH"),
                      ("Z-DEVD-FMK", "caspase-3 (research)")),
        structural_family="Caspase fold (CD = caspase / "
                          "metacaspase / paracaspase clan)",
        cross_reference_molecule_names=("Venetoclax",),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis",
            "tnf-extrinsic-apoptosis"),
        notes="The 'executioner' apoptotic caspase — cleaves "
              "hundreds of substrates including PARP-1 (the "
              "classical western-blot apoptosis marker).",
    ),
    Enzyme(
        id="ace",
        name="Angiotensin-converting enzyme (ACE)",
        ec_number="3.4.15.1",
        ec_class=3,
        mechanism_class="Zn²⁺ metallopeptidase "
                        "(carboxypeptidase removing C-terminal "
                        "His-Leu)",
        substrates=("Angiotensin I (DRVYIHPFHL)",
                    "Bradykinin (cleaved + inactivated)",
                    "H₂O"),
        products=("Angiotensin II (DRVYIHPF)",
                  "Inactive bradykinin metabolite"),
        cofactors=("Zn²⁺ (active site)", "Cl⁻ (allosteric "
                   "activator)"),
        regulators=("Inhibited by ACE inhibitors (captopril, "
                    "lisinopril, ramipril, enalapril)",
                    "ACE2 is the SARS-CoV-2 entry receptor — "
                    "a related but distinct enzyme"),
        disease_associations=("Hypertension",
                              "Heart failure",
                              "Diabetic nephropathy",
                              "Angioedema (ACE-i side effect "
                              "via bradykinin)"),
        drug_targets=(("Captopril", "ACE (first ACEi, 1981)"),
                      ("Lisinopril", "ACE"),
                      ("Ramipril", "ACE"),
                      ("Enalapril", "ACE (prodrug)")),
        structural_family="Zincin metallopeptidase clan; "
                          "thermolysin-like fold",
        cross_reference_molecule_names=("Captopril",
                                        "Lisinopril",
                                        "Ramipril",
                                        "Enalapril"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca",),
        notes="ACE inhibitors were among the first "
              "structure-based drugs (Cushman + Ondetti, "
              "captopril 1981; modelled on snake-venom "
              "peptide BPP9a).",
    ),
    Enzyme(
        id="lysozyme",
        name="Lysozyme",
        ec_number="3.2.1.17",
        ec_class=3,
        mechanism_class="Glycoside hydrolase (GH22 family); "
                        "Glu35 + Asp52 catalytic residues",
        substrates=("Bacterial peptidoglycan (β-1,4 bond "
                    "between NAM + NAG)", "H₂O"),
        products=("Cleaved muropeptide fragments",),
        cofactors=("None — substrate-distorted catalysis",),
        regulators=("Inhibited by chitobiose / chitotriose "
                    "(competitive)",
                    "Conserved across animal saliva, tears, "
                    "egg white"),
        disease_associations=("Lysozyme amyloidosis (familial "
                              "hereditary)",
                              "Marker of monocyte/macrophage "
                              "activity"),
        drug_targets=(("None — itself is therapeutic in "
                       "topical / antimicrobial use",
                       "—"),),
        structural_family="Lysozyme fold (one of the smallest "
                          "globular protein folds)",
        cross_reference_molecule_names=(),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The first enzyme structure ever solved by "
              "X-ray crystallography (Phillips 1965).  "
              "Discovered by Fleming (1922) — same researcher "
              "who later found penicillin.",
    ),

    # ============================================================
    # EC 4 — Lyases (4 entries)
    # ============================================================
    Enzyme(
        id="aldolase-a",
        name="Fructose-1,6-bisphosphate aldolase (Class I)",
        ec_number="4.1.2.13",
        ec_class=4,
        mechanism_class="Schiff-base aldolase (Lys-imine "
                        "intermediate; Class I = animals + "
                        "plants; Class II = bacteria + fungi "
                        "use Zn²⁺)",
        substrates=("Fructose-1,6-bisphosphate",),
        products=("Dihydroxyacetone phosphate (DHAP)",
                  "Glyceraldehyde-3-phosphate (G3P)"),
        cofactors=("None for Class I (Lys229 forms Schiff "
                   "base)", "Zn²⁺ for Class II"),
        regulators=("Aldolase A: muscle isozyme",
                    "Aldolase B: liver — fructose-1-phosphate "
                    "preferred substrate; HFI (hereditary "
                    "fructose intolerance)",
                    "Aldolase C: brain"),
        disease_associations=("Hereditary fructose intolerance "
                              "(aldolase B deficiency)",
                              "Cancer Warburg effect "
                              "(aldolase A overexpression)"),
        drug_targets=(("Naphthol AS-E phosphate",
                       "aldolase A (research)"),),
        structural_family="TIM barrel (α/β)₈",
        cross_reference_molecule_names=("Fructose-1,6-"
                                        "bisphosphate",
                                        "DHAP",
                                        "Glyceraldehyde-3-"
                                        "phosphate"),
        cross_reference_pathway_ids=("glycolysis",
                                     "calvin_cycle"),
        cross_reference_signaling_pathway_ids=(),
        notes="One of two enzymes in glycolysis with a Schiff-"
              "base intermediate (the other is class-I "
              "aldolases in transketolase reactions).  "
              "Classical TIM-barrel + textbook Schiff-base "
              "mechanism.",
    ),
    Enzyme(
        id="carbonic-anhydrase-ii",
        name="Carbonic anhydrase II",
        ec_number="4.2.1.1",
        ec_class=4,
        mechanism_class="Zn²⁺ metalloenzyme; CO₂ hydration "
                        "via Zn-OH⁻ nucleophile",
        substrates=("CO₂", "H₂O"),
        products=("HCO₃⁻", "H⁺"),
        cofactors=("Zn²⁺ (3 His ligands + OH⁻)",),
        regulators=("Inhibited by sulphonamides (acetazolamide, "
                    "dorzolamide, methazolamide, brinzolamide)",
                    "CO₂ partial pressure regulates "
                    "physiological flux"),
        disease_associations=("Glaucoma (CA-II in ciliary body "
                              "produces HCO₃⁻ → aqueous "
                              "humour)",
                              "Altitude sickness "
                              "(acetazolamide acid load "
                              "drives ventilation)",
                              "Osteopetrosis (CA-II "
                              "deficiency)"),
        drug_targets=(("Acetazolamide", "CA-II + CA-IV "
                                        "(diuretic, "
                                        "altitude prophylaxis, "
                                        "epilepsy)"),
                      ("Dorzolamide", "CA-II topical "
                                      "(glaucoma)"),
                      ("Brinzolamide", "CA-II topical "
                                       "(glaucoma)")),
        structural_family="α-carbonic-anhydrase fold",
        cross_reference_molecule_names=("Carbon dioxide",
                                        "Bicarbonate",
                                        "Acetazolamide"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="One of the **fastest enzymes known** "
              "(kcat ≈ 10⁶ s⁻¹; near diffusion limit).  "
              "First Zn metalloenzyme characterised; "
              "critical for CO₂ transport in blood + acid-"
              "base balance.",
    ),
    Enzyme(
        id="adenylate-cyclase",
        name="Adenylate cyclase (transmembrane)",
        ec_number="4.6.1.1",
        ec_class=4,
        mechanism_class="ATP cyclase (intramolecular "
                        "transferase yielding 3',5'-cyclic "
                        "phosphodiester)",
        substrates=("ATP",),
        products=("3',5'-cyclic AMP (cAMP)", "PPi"),
        cofactors=("Mg²⁺ (×2)",),
        regulators=("Activated by Gαs (GPCR cascade)",
                    "Inhibited by Gαi",
                    "Forskolin: direct activator (research + "
                    "occasional clinical)",
                    "Cholera toxin locks Gαs ON → "
                    "constitutive cAMP rise"),
        disease_associations=("Cholera (toxin → AC over-"
                              "activation in gut → secretory "
                              "diarrhoea)",
                              "Pertussis (toxin blocks Gαi → "
                              "AC stays ON in respiratory "
                              "epithelium)"),
        drug_targets=(("Forskolin", "AC (direct activator, "
                                    "research tool)"),),
        structural_family="Class III adenylyl / guanylyl "
                          "cyclase fold (mammalian)",
        cross_reference_molecule_names=("ATP", "cAMP"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",),
        notes="9 transmembrane isoforms in mammals, each "
              "with distinct Gα/Gβγ regulation.  cAMP is the "
              "first second messenger discovered (Sutherland, "
              "1971 Nobel).",
    ),
    Enzyme(
        id="pyruvate-decarboxylase",
        name="Pyruvate decarboxylase (yeast)",
        ec_number="4.1.1.1",
        ec_class=4,
        mechanism_class="Thiamine-pyrophosphate (TPP)-"
                        "dependent decarboxylase",
        substrates=("Pyruvate",),
        products=("Acetaldehyde", "CO₂"),
        cofactors=("Thiamine pyrophosphate (TPP / vitamin "
                   "B1-derived)", "Mg²⁺"),
        regulators=("Allosteric activation by substrate "
                    "(pyruvate)",
                    "Inhibited by thiamine-deficient diets "
                    "(beriberi)"),
        disease_associations=("Brewing + bread fermentation "
                              "(industrial use, not a human "
                              "disease)",
                              "Thiamine deficiency → impaired "
                              "carbohydrate metabolism (humans "
                              "use the related PDH-E1, not "
                              "PDC, but the cofactor "
                              "requirement is shared)"),
        drug_targets=(("None clinically — yeast enzyme",
                       "—"),),
        structural_family="TPP-binding (transketolase-like) "
                          "fold",
        cross_reference_molecule_names=("Pyruvate",
                                        "Acetaldehyde",
                                        "Carbon dioxide"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The defining enzyme of alcoholic fermentation "
              "— produces the acetaldehyde that ADH then "
              "reduces to ethanol.  Absent in humans (we have "
              "PDH instead, which oxidatively decarboxylates "
              "pyruvate to acetyl-CoA).",
    ),

    # ============================================================
    # EC 5 — Isomerases (3 entries)
    # ============================================================
    Enzyme(
        id="tim",
        name="Triose phosphate isomerase (TIM)",
        ec_number="5.3.1.1",
        ec_class=5,
        mechanism_class="Intramolecular oxidoreductase via "
                        "enediol-like intermediate (Glu165 + "
                        "His95)",
        substrates=("Dihydroxyacetone phosphate (DHAP)",),
        products=("Glyceraldehyde-3-phosphate (G3P)",),
        cofactors=("None",),
        regulators=("Inhibited by 2-phosphoglycolate "
                    "(transition-state analogue)",
                    "Substrate-channelled with GAPDH in "
                    "some organisms"),
        disease_associations=("TIM deficiency (rare autosomal "
                              "recessive — haemolytic anaemia "
                              "+ neurodegeneration)",),
        drug_targets=(("None clinically — universal "
                       "housekeeping",
                       "—"),),
        structural_family="**The original TIM barrel** "
                          "((α/β)₈ — most common protein "
                          "fold, named after this enzyme)",
        cross_reference_molecule_names=("DHAP",
                                        "Glyceraldehyde-3-"
                                        "phosphate"),
        cross_reference_pathway_ids=("glycolysis",),
        cross_reference_signaling_pathway_ids=(),
        notes="A 'perfect enzyme' (Knowles + Albery, 1976) — "
              "kcat/Km approaches the diffusion limit "
              "(~10⁹ M⁻¹s⁻¹).  Its (α/β)₈ fold is so common "
              "it is called the 'TIM barrel' across all "
              "structural-biology textbooks.",
    ),
    Enzyme(
        id="phosphoglycerate-mutase",
        name="Phosphoglycerate mutase (PGAM)",
        ec_number="5.4.2.11",
        ec_class=5,
        mechanism_class="Cofactor-dependent (2,3-BPG-"
                        "dependent) phosphohistidine "
                        "intermediate",
        substrates=("3-Phosphoglycerate",),
        products=("2-Phosphoglycerate",),
        cofactors=("2,3-Bisphosphoglycerate (priming "
                   "phosphate donor)",),
        regulators=("PGAM2 (muscle isoform): rate-limited "
                    "step in fast glycolysis",
                    "BPGM (a bypass enzyme) generates 2,3-BPG "
                    "for haemoglobin O₂ release"),
        disease_associations=("Glycogen storage disease X "
                              "(PGAM2 deficiency)",
                              "Hexokinase / pyruvate-kinase / "
                              "PGAM forms haematological "
                              "panel"),
        drug_targets=(("MJE3", "PGAM1 inhibitor (research)"),),
        structural_family="Phosphoglycerate-mutase fold "
                          "(histidine-phosphatase clan)",
        cross_reference_molecule_names=("3-Phosphoglycerate",
                                        "2-Phosphoglycerate",
                                        "1,3-Bisphospho"
                                        "glycerate"),
        cross_reference_pathway_ids=("glycolysis",),
        cross_reference_signaling_pathway_ids=(),
        notes="A surprisingly subtle reaction — a 'true' "
              "intramolecular swap requires an external "
              "phosphate donor (2,3-BPG) primed onto a "
              "catalytic His.",
    ),
    Enzyme(
        id="cyclophilin-a",
        name="Cyclophilin A (peptidyl-prolyl cis-trans "
             "isomerase, PPIA)",
        ec_number="5.2.1.8",
        ec_class=5,
        mechanism_class="Peptidyl-prolyl cis ↔ trans "
                        "isomerase (catalyses Xaa-Pro bond "
                        "rotation)",
        substrates=("Protein with Xaa-Pro bond",),
        products=("Same protein, isomerised Pro",),
        cofactors=("None",),
        regulators=("**Inhibited by cyclosporin A** "
                    "(immunosuppressant)",
                    "Inhibited by sanglifehrin"),
        disease_associations=("Transplant rejection "
                              "(cyclosporin A's clinical "
                              "use)",
                              "HCV replication (cyclophilin "
                              "A is a host factor; "
                              "alisporivir tested)"),
        drug_targets=(("Cyclosporin A", "PPIA-calcineurin "
                                       "complex (T-cell "
                                       "suppression)"),
                      ("Alisporivir", "cyclophilin A (HCV; "
                                      "discontinued)")),
        structural_family="Cyclophilin / cyclosporin-binding "
                          "fold (β-barrel with 3 helices)",
        cross_reference_molecule_names=("Cyclosporine",),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=("tcr",),
        notes="Pro is the only AA that's stable in both cis "
              "and trans peptide bonds (~ 6 % cis at "
              "equilibrium).  Cyclosporin A binds CypA + the "
              "complex blocks calcineurin → T-cell activation.",
    ),

    # ============================================================
    # EC 6 — Ligases (4 entries)
    # ============================================================
    Enzyme(
        id="dna-ligase-i",
        name="DNA ligase I (mammalian)",
        ec_number="6.5.1.1",
        ec_class=6,
        mechanism_class="ATP-dependent DNA-nick-sealing ligase "
                        "(via Lys-AMP intermediate)",
        substrates=("DNA nick (3'-OH + 5'-phosphate)",
                    "ATP"),
        products=("Sealed phosphodiester bond", "AMP", "PPi"),
        cofactors=("Mg²⁺",),
        regulators=("Loaded onto DNA by PCNA",
                    "Defective in LIG1 deficiency syndrome"),
        disease_associations=("LIG1 deficiency (immunodeficiency "
                              "+ developmental delay)",
                              "Cancer chemotherapy resistance "
                              "(DNA repair pathway)"),
        drug_targets=(("L82 + L189 (research-grade)",
                       "DNA ligase I"),),
        structural_family="Adenylation domain + OB fold + "
                          "DNA-binding domain (ATP-dependent "
                          "ligase superfamily)",
        cross_reference_molecule_names=("ATP", "AMP"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=("p53",),
        notes="T4 DNA ligase is the molecular-biology "
              "workhorse for cloning; the eukaryotic LIG1 / "
              "LIG3 / LIG4 family seals nicks during "
              "replication + repair.",
    ),
    Enzyme(
        id="glutamine-synthetase",
        name="Glutamine synthetase (GS / GLUL)",
        ec_number="6.3.1.2",
        ec_class=6,
        mechanism_class="ATP-dependent amide-bond ligase "
                        "(γ-glutamyl phosphate intermediate)",
        substrates=("L-Glutamate", "NH₃ / NH₄⁺", "ATP"),
        products=("L-Glutamine", "ADP", "Pi"),
        cofactors=("Mg²⁺ / Mn²⁺",),
        regulators=("In bacteria: cumulative feedback by 9 "
                    "different downstream products (textbook "
                    "example of allosteric integration)",
                    "In bacteria: covalent regulation by "
                    "adenylation (UMP-attachment)",
                    "In animals: less complex"),
        disease_associations=("Hyperammonaemia (GLUL "
                              "deficiency)",
                              "Hepatic encephalopathy (urea-"
                              "cycle dysfunction)"),
        drug_targets=(("Methionine sulfoximine (MSO)",
                       "GS (causes seizures — research "
                       "only)"),
                      ("Phosphinothricin",
                       "plant GS (Liberty / glufosinate "
                       "herbicide)")),
        structural_family="GS dodecameric fold (12 subunits "
                          "in two stacked hexagonal rings)",
        cross_reference_molecule_names=("L-Glutamate",
                                        "L-Glutamine", "ATP",
                                        "ADP"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The textbook example of cumulative feedback "
              "inhibition in bacterial regulation — discovered "
              "in the 1960s as the first allosteric enzyme "
              "with multiple co-regulators.",
    ),
    Enzyme(
        id="pyruvate-carboxylase",
        name="Pyruvate carboxylase (PC)",
        ec_number="6.4.1.1",
        ec_class=6,
        mechanism_class="ATP-dependent biotin-dependent "
                        "carboxylase",
        substrates=("Pyruvate", "HCO₃⁻", "ATP"),
        products=("Oxaloacetate", "ADP", "Pi"),
        cofactors=("Biotin (covalently attached)", "Mg²⁺",
                   "Mn²⁺", "Acetyl-CoA (allosteric "
                   "activator)"),
        regulators=("**Allosterically activated by acetyl-"
                    "CoA** (signal: high mitochondrial "
                    "energy)",
                    "Inhibited by ADP",
                    "Mitochondrial localisation"),
        disease_associations=("Pyruvate carboxylase deficiency "
                              "(lactic acidosis + "
                              "neurological deterioration)",
                              "Loss → impaired "
                              "gluconeogenesis"),
        drug_targets=(("None clinically",
                       "—"),),
        structural_family="Biotin-dependent carboxylase "
                          "(N-term BC + central CT + C-term "
                          "BCCP domain)",
        cross_reference_molecule_names=("Pyruvate",
                                        "ATP", "ADP",
                                        "Bicarbonate",
                                        "Biotin"),
        cross_reference_pathway_ids=("tca_cycle",),
        cross_reference_signaling_pathway_ids=("ampk",),
        notes="Refills the TCA cycle (anaplerosis) by "
              "converting pyruvate to OAA when intermediates "
              "are drained for biosynthesis (e.g. citrate "
              "export for fatty-acid synthesis).",
    ),
    Enzyme(
        id="acc",
        name="Acetyl-CoA carboxylase (ACC)",
        ec_number="6.4.1.2",
        ec_class=6,
        mechanism_class="Biotin-dependent ATP-dependent "
                        "carboxylase",
        substrates=("Acetyl-CoA", "HCO₃⁻", "ATP"),
        products=("Malonyl-CoA", "ADP", "Pi"),
        cofactors=("Biotin (covalently attached)", "Mg²⁺"),
        regulators=("**Inhibited by AMPK phosphorylation** "
                    "(low energy → no fatty-acid synthesis)",
                    "Allosterically activated by citrate "
                    "(high carbon)",
                    "Allosterically inhibited by long-chain "
                    "acyl-CoAs (product feedback)",
                    "Polymerises on activation"),
        disease_associations=("Obesity / metabolic syndrome "
                              "(ACC inhibitors tested for "
                              "NAFLD / NASH)",
                              "Cancer Warburg effect (lipogenic "
                              "phenotype)"),
        drug_targets=(("Firsocostat (GS-0976)", "ACC1 "
                                                 "(NASH "
                                                 "phase II)"),
                      ("MK-4074", "ACC1 (NASH)"),
                      ("Soraphen A", "ACC (research tool, "
                                     "natural product)")),
        structural_family="Biotin-dependent carboxylase "
                          "(BC + BT + CT domains)",
        cross_reference_molecule_names=("Acetyl-CoA",
                                        "Malonyl-CoA",
                                        "ATP", "ADP",
                                        "Citrate", "Biotin"),
        cross_reference_pathway_ids=("fatty_acid_synthesis",),
        cross_reference_signaling_pathway_ids=("ampk",
                                               "insulin"),
        notes="The committed step of fatty-acid synthesis. "
              "ACC1 (cytosolic): lipogenesis substrate. "
              "ACC2 (mitochondrial outer membrane): produces "
              "malonyl-CoA that inhibits CPT-1 to stop "
              "β-oxidation when fed.",
    ),

    # ============================================================
    # EC 7 — Translocases (3 entries)
    # ============================================================
    Enzyme(
        id="na-k-atpase",
        name="Na⁺/K⁺-ATPase",
        ec_number="7.2.2.13",
        ec_class=7,
        mechanism_class="P-type ATPase; phosphorylated "
                        "intermediate; 3 Na⁺ out / 2 K⁺ in "
                        "per ATP",
        substrates=("ATP", "3 Na⁺ (cytosol)",
                    "2 K⁺ (extracellular)"),
        products=("ADP", "Pi", "3 Na⁺ (extracellular)",
                  "2 K⁺ (cytosol)"),
        cofactors=("Mg²⁺",),
        regulators=("**Inhibited by cardiac glycosides** "
                    "(digoxin, digitoxin, ouabain) at the "
                    "extracellular K⁺ site",
                    "Phosphorylation by PKA, PKC modulates "
                    "activity",
                    "Hormones (T3, aldosterone) regulate "
                    "expression"),
        disease_associations=("Heart failure (digoxin therapy)",
                              "Familial hemiplegic migraine "
                              "type 2 (ATP1A2 mutations)",
                              "Rapid-onset dystonia + "
                              "parkinsonism (ATP1A3)"),
        drug_targets=(("Digoxin", "Na⁺/K⁺-ATPase α-subunit "
                                  "(extracellular site)"),
                      ("Digitoxin", "same"),
                      ("Ouabain", "same (research tool + "
                                  "endogenous candidate)")),
        structural_family="P-type ATPase (P2C subfamily)",
        cross_reference_molecule_names=("ATP", "ADP",
                                        "Digoxin"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="Consumes ~ 25 % of resting ATP in most "
              "animal cells; ~ 70 % in neurons.  The Na⁺ "
              "gradient drives every secondary-active "
              "transporter (Na⁺/glucose, Na⁺/Ca²⁺ exchange, "
              "etc.).  Drug discovery target since the 1700s "
              "(Withering's foxglove → digitalis 1785).",
    ),
    Enzyme(
        id="atp-synthase",
        name="F₁F₀-ATP synthase (Complex V)",
        ec_number="7.1.2.2",
        ec_class=7,
        mechanism_class="Rotary motor enzyme; H⁺ flux through "
                        "F₀ rotates F₁ → conformational "
                        "ATP synthesis (binding-change "
                        "mechanism)",
        substrates=("ADP", "Pi", "H⁺ (intermembrane → matrix)"),
        products=("ATP", "H⁺ released into matrix"),
        cofactors=("Mg²⁺",),
        regulators=("Inhibited by oligomycin (F₀ — classical "
                    "tool)",
                    "Inhibited by aurovertin (F₁)",
                    "Inhibited by IF1 protein in low-pH "
                    "conditions",
                    "Reverses to ATP hydrolysis under "
                    "ischaemia (depletes ATP)"),
        disease_associations=("Mitochondrial diseases (MILS, "
                              "NARP — ATP6 mutations)",
                              "Anti-cancer (bedaquiline-class "
                              "explored)",
                              "Bedaquiline targets the "
                              "**bacterial** ATP synthase — "
                              "anti-TB"),
        drug_targets=(("Bedaquiline (Sirturo)",
                       "Mycobacterium tuberculosis ATP "
                       "synthase c-ring"),
                      ("Oligomycin", "F₀ ATP synthase "
                                     "(research tool)")),
        structural_family="F-type ATPase (F₁ catalytic "
                          "α₃β₃γδε head + F₀ membrane c-ring "
                          "+ ab₂ stator)",
        cross_reference_molecule_names=("ATP", "ADP"),
        cross_reference_pathway_ids=("ox_phos",),
        cross_reference_signaling_pathway_ids=(),
        notes="The world's smallest rotary motor — Walker / "
              "Boyer / Skou shared the 1997 Nobel for working "
              "out the binding-change mechanism (3 catalytic "
              "sites cycle through 3 conformations as the "
              "γ-shaft rotates 120° per ATP).",
    ),
    Enzyme(
        id="p-glycoprotein",
        name="P-glycoprotein (MDR1 / ABCB1)",
        ec_number="7.6.2.2",
        ec_class=7,
        mechanism_class="ABC transporter; ATP-driven efflux "
                        "of broad-spectrum xenobiotics + "
                        "drugs",
        substrates=("Drug substrate (vinblastine, "
                    "doxorubicin, paclitaxel, digoxin, "
                    "many)", "ATP (×2)"),
        products=("Drug exported to extracellular space",
                  "ADP + Pi (×2)"),
        cofactors=("Mg²⁺",),
        regulators=("Induced by rifampin, St John's Wort "
                    "(PXR / CAR transcriptional)",
                    "Inhibited by cyclosporine, verapamil, "
                    "tariquidar, elacridar",
                    "Constitutively expressed at blood-brain "
                    "barrier + intestinal apical membrane"),
        disease_associations=("Multi-drug resistance in cancer "
                              "(P-gp overexpression pumps "
                              "chemotherapy out)",
                              "Drug-drug interactions "
                              "(altered absorption + brain "
                              "penetration)",
                              "Inflammatory bowel disease (ABCB1 "
                              "polymorphisms)"),
        drug_targets=(("Tariquidar", "P-gp (resensitisation "
                                     "trials)"),
                      ("Elacridar", "P-gp (research)"),
                      ("Cyclosporine", "P-gp (off-target "
                                       "effect)")),
        structural_family="ABC-transporter superfamily; 12-"
                          "TM topology with 2 NBDs",
        cross_reference_molecule_names=("ATP", "ADP",
                                        "Doxorubicin",
                                        "Paclitaxel",
                                        "Digoxin",
                                        "Cyclosporine"),
        cross_reference_pathway_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes="The first multi-drug-resistance ABC "
              "transporter cloned (1985, Ling).  Promiscuous "
              "binding pocket accommodates hundreds of "
              "structurally diverse substrates — explains "
              "why so many drugs are effluxed from CNS / "
              "tumours.",
    ),
]
