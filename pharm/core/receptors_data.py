"""Phase PH-2.0 (round 220) — 28-entry receptor pharmacology
catalogue.

Each entry carries typed cross-references into:
- ``pharm.core.drug_classes`` ids (PH-1.0 drug classes that
  target this receptor).
- ``cellbio.core.cell_signaling`` ids (CB-1.0 pathways the
  receptor activates).
- ``biochem.core.enzymes`` ids (where the receptor itself is
  an enzyme — RTKs, P-glycoprotein, etc.).
- ``orgchem.db.Molecule`` rows by exact name (endogenous
  ligands present in the seeded DB).

All cross-reference ids verified against destination
catalogues at write time; the round-220 catalogue tests gate
re-validation at every test run.
"""
from __future__ import annotations
from typing import Tuple

from pharm.core.receptors import Receptor


RECEPTORS: Tuple[Receptor, ...] = (
    # ============================================================
    # GPCR — aminergic (5)
    # ============================================================
    Receptor(
        id="adrenergic-beta1",
        name="β₁-adrenergic receptor",
        receptor_family="gpcr-aminergic",
        receptor_subtype="β1",
        structural_summary=(
            "Class-A 7-TM GPCR; primarily Gαs-coupled.  "
            "Crystal structure of turkey β1-AR bound to "
            "cyanopindolol (Warne 2008) was a landmark of "
            "structural pharmacology."),
        endogenous_ligands=(
            "Adrenaline (epinephrine)",
            "Noradrenaline (norepinephrine)",
        ),
        signalling_output=(
            "Gαs → adenylate cyclase → ↑cAMP → PKA",
        ),
        tissue_distribution=(
            "Cardiac myocytes (~ 75 % of cardiac β receptors)",
            "Juxtaglomerular cells (drives renin release)",
            "Adipocytes",
        ),
        clinical_relevance=(
            "Hypertension + heart failure + post-MI mortality "
            "reduction — antagonised by β1-selective blockers "
            "(metoprolol, bisoprolol, atenolol)",
            "Sympathetic tone marker in shock + sepsis",
        ),
        cross_reference_drug_class_ids=(
            "beta-blockers",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "β1-selectivity is dose-dependent: at clinical "
            "doses metoprolol is ~ 75 % β1-selective but "
            "loses selectivity at higher exposure — explains "
            "the bronchospasm risk at high doses."),
    ),
    Receptor(
        id="adrenergic-beta2",
        name="β₂-adrenergic receptor",
        receptor_family="gpcr-aminergic",
        receptor_subtype="β2",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαs-coupled (with Gαi cross-"
            "talk after PKA-mediated phosphorylation switch). "
            "First GPCR with crystal structure (Kobilka 2007, "
            "Nobel 2012)."),
        endogenous_ligands=(
            "Adrenaline (epinephrine)",
            "Noradrenaline (lower affinity)",
        ),
        signalling_output=(
            "Gαs → adenylate cyclase → ↑cAMP → PKA",
            "Gαi (after βARK / GRK phosphorylation switch)",
        ),
        tissue_distribution=(
            "Bronchial smooth muscle (relaxation)",
            "Uterine smooth muscle (tocolysis)",
            "Skeletal muscle (vasodilation, glycogenolysis)",
            "Hepatocytes (glycogenolysis)",
        ),
        clinical_relevance=(
            "Asthma + COPD bronchodilation via β2-agonists "
            "(salbutamol, salmeterol, formoterol)",
            "Pre-term labour suppression (ritodrine, "
            "terbutaline)",
        ),
        cross_reference_drug_class_ids=(
            "beta2-agonists",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Functional desensitisation via GRK2/3 phospho-"
            "rylation + β-arrestin recruitment is the "
            "molecular basis of tachyphylaxis to short-"
            "acting β2-agonist overuse."),
    ),
    Receptor(
        id="adrenergic-alpha1",
        name="α₁-adrenergic receptor",
        receptor_family="gpcr-aminergic",
        receptor_subtype="α1",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαq-coupled.  Three subtypes "
            "(α1A, α1B, α1D) with differential tissue "
            "distribution + drug selectivity."),
        endogenous_ligands=(
            "Noradrenaline (preferred)",
            "Adrenaline",
        ),
        signalling_output=(
            "Gαq → PLCβ → IP₃ + DAG → ↑Ca²⁺ + PKC",
        ),
        tissue_distribution=(
            "Vascular smooth muscle (vasoconstriction)",
            "Prostatic + bladder-neck smooth muscle (urinary "
            "outflow)",
            "Iris dilator muscle (mydriasis)",
        ),
        clinical_relevance=(
            "BPH symptom relief via α1A-selective blockers "
            "(tamsulosin, silodosin)",
            "Resistant hypertension (doxazosin, prazosin)",
            "Mydriatic eye drops (phenylephrine — α1 agonist)",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca", "pkc-dag-ca",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "ALLHAT trial (2002) showed α1-blocker doxazosin "
            "doubled heart-failure incidence vs chlorthal-"
            "idone — α1 blockade is no longer first-line for "
            "uncomplicated HTN."),
    ),
    Receptor(
        id="muscarinic-m3",
        name="Muscarinic M₃ receptor",
        receptor_family="gpcr-aminergic",
        receptor_subtype="M3",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαq-coupled.  Five muscarinic "
            "subtypes (M1-M5); M1/M3/M5 are Gαq, M2/M4 are "
            "Gαi."),
        endogenous_ligands=(
            "Acetylcholine",
        ),
        signalling_output=(
            "Gαq → PLCβ → IP₃ + DAG → ↑Ca²⁺ + PKC",
        ),
        tissue_distribution=(
            "Bronchial smooth muscle (bronchoconstriction)",
            "Bladder detrusor (contraction)",
            "Salivary + lacrimal + GI exocrine glands "
            "(secretion)",
            "Iris sphincter (miosis)",
        ),
        clinical_relevance=(
            "COPD long-acting M3 antagonism (tiotropium, "
            "umeclidinium)",
            "Overactive bladder (oxybutynin, solifenacin)",
            "Atropine remains the first-line antidote for "
            "organophosphate (cholinesterase-inhibitor) "
            "poisoning",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca", "pkc-dag-ca",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Allosteric M3 ligands (e.g. AC-42 family) are an "
            "active area — unprecedented subtype selectivity "
            "via the extracellular vestibule rather than the "
            "highly-conserved orthosteric ACh pocket."),
    ),
    Receptor(
        id="dopamine-d2",
        name="Dopamine D₂ receptor",
        receptor_family="gpcr-aminergic",
        receptor_subtype="D2",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαi/o-coupled.  Five dopamine "
            "subtypes (D1-D5) split into D1-like (D1, D5; "
            "Gαs) and D2-like (D2, D3, D4; Gαi)."),
        endogenous_ligands=(
            "Dopamine",
        ),
        signalling_output=(
            "Gαi/o → ↓adenylate cyclase → ↓cAMP",
            "βγ → GIRK K⁺ channel opening (hyperpolar"
            "isation)",
        ),
        tissue_distribution=(
            "Striatum + substantia nigra (motor control)",
            "Mesolimbic + mesocortical projections (reward, "
            "cognition)",
            "Anterior pituitary lactotrophs (prolactin "
            "tonic inhibition)",
            "Chemoreceptor trigger zone (CTZ — emesis)",
        ),
        clinical_relevance=(
            "Schizophrenia: D2-antagonist antipsychotics "
            "remain the dominant pharmacology",
            "Parkinson's disease: D2-agonists (pramipexole, "
            "ropinirole) + dopamine precursor L-DOPA",
            "Hyperprolactinaemia: D2-agonists (cabergoline, "
            "bromocriptine) restore tonic inhibition",
            "Antiemetic (domperidone, metoclopramide)",
        ),
        cross_reference_drug_class_ids=(
            "atypical-antipsychotics",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Dopamine", "L-DOPA (levodopa)",
        ),
        notes=(
            "Atypical antipsychotics achieve their lower "
            "extra-pyramidal side-effect profile through "
            "rapid D2 dissociation kinetics + 5-HT2A "
            "antagonism (Kapur + Seeman model)."),
    ),

    # ============================================================
    # GPCR — peptide (4)
    # ============================================================
    Receptor(
        id="opioid-mu",
        name="μ-opioid receptor",
        receptor_family="gpcr-peptide",
        receptor_subtype="μ (MOR)",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαi/o-coupled.  Three opioid "
            "subtypes (μ, κ, δ) plus the orphan ORL1 (NOP).  "
            "Crystal structure of murine μ-OR bound to "
            "antagonist β-FNA solved 2012."),
        endogenous_ligands=(
            "β-Endorphin", "Enkephalins (Met-, Leu-)",
            "Endomorphins-1/2",
        ),
        signalling_output=(
            "Gαi/o → ↓adenylate cyclase → ↓cAMP",
            "βγ → GIRK K⁺ opening + Cav inhibition → "
            "neuronal hyperpolarisation",
        ),
        tissue_distribution=(
            "CNS pain pathways (peri-aqueductal grey, "
            "thalamus, dorsal horn)",
            "Brainstem respiratory centres (the "
            "respiratory-depression liability)",
            "GI smooth muscle (constipation)",
            "Reward circuitry (ventral tegmental area, "
            "nucleus accumbens)",
        ),
        clinical_relevance=(
            "Acute + chronic pain: morphine, oxycodone, "
            "fentanyl, methadone",
            "Opioid use disorder: methadone + buprenorphine "
            "agonist therapy; naltrexone (μ antagonist) for "
            "abstinence",
            "Opioid overdose: naloxone (parenteral), "
            "nalmefene, nasal naloxone",
        ),
        cross_reference_drug_class_ids=(
            "opioids",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Morphine",
        ),
        notes=(
            "Biased agonism (G-protein vs β-arrestin) was "
            "the basis of oliceridine's FDA approval (2020) "
            "as a putatively safer μ-agonist — the clinical "
            "advantage in respiratory depression remains "
            "controversial."),
    ),
    Receptor(
        id="angiotensin-at1",
        name="Angiotensin II type 1 receptor (AT₁)",
        receptor_family="gpcr-peptide",
        receptor_subtype="AT1",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαq + Gαi-coupled.  Two AT "
            "subtypes (AT1 + AT2); virtually all clinical "
            "biology runs through AT1."),
        endogenous_ligands=(
            "Angiotensin II",
        ),
        signalling_output=(
            "Gαq → PLCβ → IP₃ + DAG → ↑Ca²⁺ + PKC",
            "Gαi → ↓cAMP",
            "β-arrestin → MAPK activation (proliferative + "
            "fibrotic)",
        ),
        tissue_distribution=(
            "Vascular smooth muscle (vasoconstriction)",
            "Adrenal zona glomerulosa (aldosterone release)",
            "Renal proximal tubule (Na⁺ reabsorption)",
            "Cardiac myocytes + fibroblasts (hypertrophy + "
            "fibrosis)",
        ),
        clinical_relevance=(
            "Hypertension + heart failure + diabetic "
            "nephropathy + post-MI remodelling — antagonised "
            "by ARBs (losartan, valsartan, candesartan, "
            "olmesartan)",
            "Indirect inhibition by ACE inhibitors "
            "(reducing AT II production)",
        ),
        cross_reference_drug_class_ids=(
            "arbs", "ace-inhibitors",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca", "mapk-erk",
        ),
        cross_reference_enzyme_ids=(
            "ace",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "AT2 receptor is largely vasodilatory + "
            "antiproliferative — opposing AT1 — but no AT2-"
            "selective drug has reached the clinic."),
    ),
    Receptor(
        id="glp1-receptor",
        name="GLP-1 receptor",
        receptor_family="gpcr-peptide",
        receptor_subtype="GLP-1R",
        structural_summary=(
            "Class-B 7-TM GPCR; Gαs-coupled.  Class-B GPCRs "
            "have a distinctive large extracellular N-terminal "
            "domain that binds the C-terminus of the peptide "
            "ligand."),
        endogenous_ligands=(
            "Glucagon-like peptide-1 (7-36 amide)",
            "GLP-1 (7-37)",
        ),
        signalling_output=(
            "Gαs → adenylate cyclase → ↑cAMP → PKA + Epac",
            "β-arrestin recruitment + cytoskeletal effects",
        ),
        tissue_distribution=(
            "Pancreatic β cells (glucose-dependent insulin "
            "release)",
            "Hypothalamic feeding centres (satiety)",
            "Stomach (delayed gastric emptying)",
            "Cardiomyocytes + endothelium",
        ),
        clinical_relevance=(
            "Type-2 diabetes + obesity: liraglutide, "
            "semaglutide, dulaglutide, tirzepatide (GIP/GLP-1 "
            "co-agonist)",
            "Cardiovascular outcome benefits demonstrated in "
            "LEADER, SUSTAIN-6, REWIND trials — GLP-1RA now "
            "recommended in diabetes + ASCVD",
        ),
        cross_reference_drug_class_ids=(
            "glp1-agonists",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "DPP-4 inhibitors (sitagliptin, linagliptin) "
            "extend native GLP-1 half-life by inhibiting its "
            "principal degrading enzyme — same axis, different "
            "drug class."),
    ),
    Receptor(
        id="histamine-h1",
        name="Histamine H₁ receptor",
        receptor_family="gpcr-peptide",
        receptor_subtype="H1",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαq-coupled.  Four histamine "
            "subtypes (H1-H4); H1 + H2 are clinically "
            "dominant."),
        endogenous_ligands=(
            "Histamine",
        ),
        signalling_output=(
            "Gαq → PLCβ → IP₃ + DAG → ↑Ca²⁺ + PKC",
        ),
        tissue_distribution=(
            "Vascular endothelium (capillary leak, oedema)",
            "Bronchial smooth muscle (constriction)",
            "Sensory nerve endings (itch)",
            "CNS (wakefulness — sedation when blocked)",
        ),
        clinical_relevance=(
            "Allergic rhinitis + urticaria: 1st-gen "
            "(diphenhydramine, chlorpheniramine — sedating) "
            "+ 2nd-gen (cetirizine, loratadine, fexofenadine "
            "— non-sedating)",
            "Anaphylaxis adjunct (after IM adrenaline)",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-ip3-ca",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Diphenhydramine + doxylamine are the active "
            "ingredients of common OTC sleep aids — the "
            "‘sedating side effect’ is the marketed effect."),
    ),

    # ============================================================
    # GPCR — other (1)
    # ============================================================
    Receptor(
        id="cannabinoid-cb1",
        name="Cannabinoid CB₁ receptor",
        receptor_family="gpcr-other",
        receptor_subtype="CB1",
        structural_summary=(
            "Class-A 7-TM GPCR; Gαi/o-coupled.  Two cannabinoid "
            "receptors (CB1 + CB2); CB1 is the most-abundant "
            "GPCR in the brain."),
        endogenous_ligands=(
            "Anandamide (N-arachidonoyl-ethanolamide)",
            "2-Arachidonoylglycerol (2-AG)",
        ),
        signalling_output=(
            "Gαi/o → ↓cAMP",
            "Retrograde signalling at synapses → presynaptic "
            "Cav inhibition → reduced neurotransmitter release",
        ),
        tissue_distribution=(
            "CNS (basal ganglia, cerebellum, hippocampus, "
            "cortex)",
            "Adipocytes + hepatocytes (CB1 in metabolic "
            "syndrome)",
        ),
        clinical_relevance=(
            "Δ⁹-THC partial agonist (psychoactive component "
            "of cannabis)",
            "CBD (cannabidiol) is a low-affinity allosteric "
            "modulator + non-psychoactive",
            "Rimonabant (CB1 inverse agonist) was withdrawn "
            "in 2008 for psychiatric adverse effects "
            "(depression, suicidality)",
            "Nabilone (synthetic CB1 agonist) approved for "
            "chemotherapy-induced nausea + vomiting",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "FAAH (fatty-acid amide hydrolase) inhibitors aim "
            "to potentiate endogenous anandamide tone without "
            "the central side effects of direct CB1 agonism — "
            "the BIA 10-2474 trial (2016) tragically caused "
            "one death + several serious neurological events."),
    ),

    # ============================================================
    # NHR — steroid (4)
    # ============================================================
    Receptor(
        id="glucocorticoid-receptor",
        name="Glucocorticoid receptor (GR)",
        receptor_family="nhr-steroid",
        receptor_subtype="GR (NR3C1)",
        structural_summary=(
            "Cytoplasmic ligand-binding nuclear hormone "
            "receptor; ligand binding releases HSP90 + "
            "translocates to the nucleus.  Acts as homodimer "
            "(transactivation) or monomer (transrepression of "
            "NF-κB / AP-1)."),
        endogenous_ligands=(
            "Cortisol",
            "Corticosterone (rodents)",
        ),
        signalling_output=(
            "Glucocorticoid response element (GRE) "
            "transcriptional activation",
            "Tethered repression of NF-κB + AP-1 (anti-"
            "inflammatory)",
        ),
        tissue_distribution=(
            "Ubiquitous — almost every nucleated cell",
        ),
        clinical_relevance=(
            "Anti-inflammatory + immunosuppressant therapy "
            "(prednisolone, dexamethasone, hydrocortisone, "
            "budesonide)",
            "Replacement therapy in adrenal insufficiency",
            "Asthma + IBD + autoimmune disease + transplant "
            "rejection",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "nf-kb",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Cortisol",
        ),
        notes=(
            "Selective glucocorticoid-receptor agonists "
            "(SEGRAs) try to dissociate transrepression "
            "(anti-inflammatory) from transactivation "
            "(side-effect-driving) — partial clinical "
            "success."),
    ),
    Receptor(
        id="oestrogen-receptor-alpha",
        name="Oestrogen receptor α (ERα)",
        receptor_family="nhr-steroid",
        receptor_subtype="ERα (ESR1)",
        structural_summary=(
            "Nuclear hormone receptor; ligand-binding domain "
            "+ DNA-binding zinc-finger domain.  Acts as "
            "homodimer or heterodimer with ERβ on oestrogen "
            "response elements (ERE)."),
        endogenous_ligands=(
            "17β-Estradiol",
            "Estrone (postmenopausal)",
            "Estriol (pregnancy)",
        ),
        signalling_output=(
            "ERE-driven transcription",
            "Non-genomic (membrane ERα) MAPK + PI3K "
            "activation in some tissues",
        ),
        tissue_distribution=(
            "Mammary gland (proliferative driver)",
            "Endometrium + ovary",
            "Bone (anti-resorptive)",
            "Cardiovascular endothelium",
            "Liver (metabolic regulation)",
        ),
        clinical_relevance=(
            "ER+ breast cancer: tamoxifen (SERM), fulvestrant "
            "(SERD), aromatase inhibitors (letrozole, "
            "anastrozole, exemestane — block oestrogen "
            "synthesis)",
            "Postmenopausal hormone replacement therapy",
            "Contraception (combined oral contraceptive)",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Estradiol",
        ),
        notes=(
            "ESR1 mutations (D538G, Y537S/N/C) drive endocrine "
            "resistance in metastatic breast cancer + are now "
            "biomarker-tracked by ctDNA assays (Guardant360, "
            "FoundationOne Liquid)."),
    ),
    Receptor(
        id="androgen-receptor",
        name="Androgen receptor (AR)",
        receptor_family="nhr-steroid",
        receptor_subtype="AR (NR3C4)",
        structural_summary=(
            "Cytoplasmic ligand-binding NHR.  Ligand binding "
            "→ HSP90 dissociation + nuclear translocation + "
            "homodimerisation on androgen response elements."),
        endogenous_ligands=(
            "Testosterone",
            "5α-Dihydrotestosterone (DHT — higher AR affinity)",
        ),
        signalling_output=(
            "Androgen response element (ARE) transcription",
        ),
        tissue_distribution=(
            "Prostate (epithelial proliferation)",
            "Skeletal muscle (anabolic)",
            "Hair follicles (terminal-hair conversion)",
            "Bone (sexual dimorphism)",
            "CNS (libido, mood)",
        ),
        clinical_relevance=(
            "Prostate cancer: AR antagonists (enzalutamide, "
            "apalutamide, darolutamide), androgen-deprivation "
            "therapy (LHRH agonists / antagonists), "
            "abiraterone (CYP17 inhibitor — blocks androgen "
            "synthesis)",
            "Benign prostatic hyperplasia: 5α-reductase "
            "inhibitors (finasteride, dutasteride)",
            "Androgenetic alopecia: oral / topical 5α-"
            "reductase inhibition + topical minoxidil",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Testosterone",
        ),
        notes=(
            "AR splice variant 7 (AR-V7) lacks the ligand-"
            "binding domain → constitutively active → "
            "primary mechanism of resistance to enzalutamide "
            "+ abiraterone in metastatic CRPC."),
    ),
    Receptor(
        id="progesterone-receptor",
        name="Progesterone receptor (PR)",
        receptor_family="nhr-steroid",
        receptor_subtype="PR (NR3C3)",
        structural_summary=(
            "Cytoplasmic NHR with two isoforms (PR-A + PR-B) "
            "from alternative promoter use; opposing "
            "transcriptional outputs at many genes."),
        endogenous_ligands=(
            "Progesterone",
        ),
        signalling_output=(
            "Progesterone response element transcription",
            "Non-genomic membrane signalling (oocyte "
            "maturation)",
        ),
        tissue_distribution=(
            "Endometrium + myometrium",
            "Mammary gland (lobulo-alveolar development)",
            "Ovary (corpus luteum)",
            "CNS (anxiolytic effects of allopregnanolone)",
        ),
        clinical_relevance=(
            "Combined hormonal contraception (progestin "
            "component)",
            "Hormone-replacement therapy in women with "
            "intact uterus (endometrial protection from "
            "unopposed oestrogen)",
            "Mifepristone (RU-486) is a PR antagonist used "
            "for medical abortion + Cushing syndrome",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Progesterone",
        ),
        notes=(
            "Allopregnanolone is a positive allosteric "
            "modulator of GABA-A — the basis of brexanolone "
            "(IV) + zuranolone (oral) for postpartum "
            "depression.  Steroid pharmacology is rarely "
            "limited to ‘its own’ receptor."),
    ),

    # ============================================================
    # NHR — other (3)
    # ============================================================
    Receptor(
        id="thyroid-receptor-alpha",
        name="Thyroid hormone receptor α",
        receptor_family="nhr-other",
        receptor_subtype="TRα (NR1A1)",
        structural_summary=(
            "Nuclear hormone receptor; heterodimerises with "
            "RXR on thyroid response elements.  Two genes "
            "(THRA + THRB) + multiple isoforms with "
            "differential tissue distribution."),
        endogenous_ligands=(
            "Triiodothyronine (T3)",
            "Thyroxine (T4 — much lower affinity; converted "
            "to T3 by deiodinases)",
        ),
        signalling_output=(
            "Thyroid response element transcription "
            "(activated when ligand-bound; repressed when "
            "unliganded)",
        ),
        tissue_distribution=(
            "Cardiac myocytes (chronotropy + inotropy)",
            "Skeletal muscle",
            "Brown adipose tissue",
            "CNS (development)",
        ),
        clinical_relevance=(
            "Hypothyroidism replacement: levothyroxine (T4) "
            "± liothyronine (T3)",
            "Hyperthyroidism + thyroid cancer: "
            "thionamides (carbimazole, methimazole, "
            "propylthiouracil) inhibit hormone synthesis; "
            "TR-β agonists (resmetirom — Madrigal, FDA-"
            "approved 2024) for non-alcoholic steato"
            "hepatitis (NASH/MASH)",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Resmetirom's selectivity for TR-β over TR-α was "
            "the key to avoiding cardiac side effects + "
            "achieving liver-targeted lipid + fibrotic "
            "improvement in NASH."),
    ),
    Receptor(
        id="vitamin-d-receptor",
        name="Vitamin D receptor (VDR)",
        receptor_family="nhr-other",
        receptor_subtype="VDR (NR1I1)",
        structural_summary=(
            "Nuclear hormone receptor; heterodimerises with "
            "RXR on vitamin D response elements."),
        endogenous_ligands=(
            "1α,25-Dihydroxyvitamin D₃ (calcitriol)",
        ),
        signalling_output=(
            "Vitamin D response element transcription",
            "Non-genomic membrane VDR effects (rapid Ca²⁺ "
            "responses)",
        ),
        tissue_distribution=(
            "Intestinal epithelium (Ca²⁺ + Pi absorption)",
            "Renal proximal tubule",
            "Bone osteoblasts",
            "Immune cells (T-cell tolerance)",
            "Many epithelia (cell-cycle arrest + anti"
            "proliferative effects)",
        ),
        clinical_relevance=(
            "Vitamin D deficiency / rickets / osteomalacia "
            "treatment: cholecalciferol (D3), ergocalciferol "
            "(D2), calcitriol (active form)",
            "Secondary hyperparathyroidism in CKD: paricalcitol "
            "+ cinacalcet",
            "Plaque psoriasis topical: calcipotriol",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Vitamin D3 (cholecalciferol)",
        ),
        notes=(
            "Vitamin D3 is technically a prohormone — it "
            "requires hepatic 25-hydroxylation (CYP2R1) + "
            "renal 1α-hydroxylation (CYP27B1) to become the "
            "active VDR ligand calcitriol."),
    ),
    Receptor(
        id="ppar-gamma",
        name="Peroxisome proliferator-activated receptor γ",
        receptor_family="nhr-other",
        receptor_subtype="PPARγ (NR1C3)",
        structural_summary=(
            "Nuclear hormone receptor; heterodimerises with "
            "RXR on PPAR response elements."),
        endogenous_ligands=(
            "15-deoxy-Δ¹²,¹⁴-prostaglandin J₂ (15d-PGJ2)",
            "Long-chain fatty acids + oxidised LDL",
        ),
        signalling_output=(
            "PPRE transcriptional activation of adipogenic + "
            "insulin-sensitising genes",
        ),
        tissue_distribution=(
            "Adipocytes (master regulator of adipogenesis)",
            "Macrophages (anti-inflammatory polarisation)",
            "Skeletal muscle + liver (insulin sensitisation)",
        ),
        clinical_relevance=(
            "Type-2 diabetes: thiazolidinediones "
            "(pioglitazone, rosiglitazone — partial "
            "agonists)",
            "Rosiglitazone was withdrawn (EU) / restricted "
            "(US) over CV risk; pioglitazone remains "
            "available with bladder-cancer warning",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "PPARα is the molecular target of fibrates "
            "(gemfibrozil, fenofibrate) for hyper"
            "triglyceridaemia.  PPARδ agonists remain "
            "investigational despite strong preclinical "
            "data."),
    ),

    # ============================================================
    # RTK (4)
    # ============================================================
    Receptor(
        id="egfr",
        name="EGFR (ErbB1, HER1)",
        receptor_family="rtk",
        receptor_subtype="EGFR",
        structural_summary=(
            "Single-pass type-I receptor tyrosine kinase.  "
            "Ligand binding → homo- or heterodimerisation "
            "(with HER2/3/4) → trans-autophosphorylation of "
            "C-terminal tyrosines → adaptor + signal-amplifier "
            "recruitment."),
        endogenous_ligands=(
            "EGF", "TGF-α", "Amphiregulin", "Heparin-binding "
            "EGF",
        ),
        signalling_output=(
            "RAS-RAF-MEK-ERK proliferation",
            "PI3K-Akt-mTOR survival + growth",
            "STAT3", "PLCγ-DAG-IP3",
        ),
        tissue_distribution=(
            "Epithelia (skin, lung, GI, kidney) — basal + "
            "regenerative compartments",
        ),
        clinical_relevance=(
            "EGFR-mutant NSCLC (exon 19 deletion + L858R): "
            "1st-gen erlotinib, gefitinib; 2nd-gen "
            "afatinib; 3rd-gen osimertinib (covalent, "
            "T790M-resistant)",
            "Colorectal cancer (KRAS-WT): cetuximab, "
            "panitumumab (mAbs)",
            "Head + neck SCC: cetuximab",
        ),
        cross_reference_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_signaling_pathway_ids=(
            "egfr-ras-raf", "mapk-erk", "pi3k-akt-mtor",
            "jak-stat",
        ),
        cross_reference_enzyme_ids=(
            "egfr-tk",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "EGFR was the first oncogenic RTK identified + "
            "the first RTK structure solved.  Lapatinib + "
            "neratinib are dual EGFR/HER2 inhibitors used "
            "in HER2+ breast cancer."),
    ),
    Receptor(
        id="her2",
        name="HER2 (ErbB2)",
        receptor_family="rtk",
        receptor_subtype="HER2",
        structural_summary=(
            "ErbB-family RTK with no known endogenous ligand "
            "— exists in a constitutively-active extended "
            "conformation, making it the preferred dimerisation "
            "partner for the other ErbB receptors."),
        endogenous_ligands=(),
        signalling_output=(
            "RAS-RAF-MEK-ERK", "PI3K-Akt-mTOR",
        ),
        tissue_distribution=(
            "Epithelia (mammary, gastric, etc.)",
        ),
        clinical_relevance=(
            "HER2+ breast cancer: trastuzumab + pertuzumab "
            "(complementary epitopes) + ADC trastuzumab-"
            "emtansine (T-DM1) + ADC trastuzumab-deruxtecan "
            "(T-DXd)",
            "HER2+ gastric cancer: trastuzumab",
            "HER2-low breast cancer (a 2022 paradigm shift): "
            "T-DXd (DESTINY-Breast04)",
        ),
        cross_reference_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_signaling_pathway_ids=(
            "egfr-ras-raf", "mapk-erk", "pi3k-akt-mtor",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "HER2 amplification was the molecular basis of "
            "trastuzumab — Dennis Slamon's UCLA work + the "
            "first targeted-therapy approval for solid tumours "
            "(1998)."),
    ),
    Receptor(
        id="vegfr2",
        name="VEGFR-2 (KDR)",
        receptor_family="rtk",
        receptor_subtype="VEGFR2",
        structural_summary=(
            "Type-V single-pass RTK; the dominant VEGF "
            "receptor on endothelial cells.  Family includes "
            "VEGFR-1 (FLT1), VEGFR-2 (KDR), VEGFR-3 (FLT4 — "
            "lymphangiogenesis)."),
        endogenous_ligands=(
            "VEGF-A", "VEGF-C / D (lower affinity)",
        ),
        signalling_output=(
            "PLCγ-PKC-MAPK proliferation",
            "PI3K-Akt-eNOS vasodilation",
            "Rho-GTPase migration",
        ),
        tissue_distribution=(
            "Vascular endothelium",
            "Lymphatic endothelium (VEGFR-3)",
        ),
        clinical_relevance=(
            "Anti-VEGF mAbs (bevacizumab) + VEGF-trap "
            "(aflibercept) — colorectal, NSCLC, ovarian, "
            "renal-cell carcinoma",
            "Multi-targeted tyrosine-kinase inhibitors "
            "(sunitinib, sorafenib, axitinib, pazopanib, "
            "lenvatinib) hit VEGFR2 + several other RTKs",
            "Wet age-related macular degeneration + diabetic "
            "macular oedema: ranibizumab, aflibercept, "
            "faricimab (intravitreal)",
        ),
        cross_reference_drug_class_ids=(
            "kinase-inhibitors",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Judah Folkman's anti-angiogenesis hypothesis "
            "(1971) was vindicated by bevacizumab's 2004 "
            "FDA approval for metastatic colorectal cancer."),
    ),
    Receptor(
        id="insulin-receptor",
        name="Insulin receptor (IR)",
        receptor_family="rtk",
        receptor_subtype="IR (INSR)",
        structural_summary=(
            "Tetrameric (α₂β₂) RTK held together by disulfide "
            "bridges.  Insulin binding induces structural "
            "rearrangement → trans-autophosphorylation of the "
            "intracellular β subunit kinase domains."),
        endogenous_ligands=(
            "Insulin",
            "IGF-2 (lower affinity)",
        ),
        signalling_output=(
            "IRS1/2 → PI3K-Akt → GLUT4 translocation + "
            "glycogen synthesis + protein synthesis",
            "Ras-MAPK (mitogenic arm)",
        ),
        tissue_distribution=(
            "Skeletal muscle (glucose disposal)",
            "Adipocytes (lipogenesis)",
            "Hepatocytes (gluconeogenesis suppression)",
            "CNS (cognitive + appetite effects)",
        ),
        clinical_relevance=(
            "Type-1 + insulin-requiring type-2 diabetes: "
            "rapid (lispro, aspart, glulisine), short "
            "(regular), intermediate (NPH), long "
            "(glargine, detemir, degludec), ultra-long "
            "(insulin icodec)",
            "Insulin resistance underlies type-2 diabetes, "
            "metabolic syndrome, NAFLD, PCOS",
        ),
        cross_reference_drug_class_ids=(
            "insulin",
        ),
        cross_reference_signaling_pathway_ids=(
            "insulin", "pi3k-akt-mtor", "mtorc1-aa-sensing",
            "mapk-erk",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "The 2024 ONWARDS trials of weekly insulin "
            "icodec (~ 7-day half-life) re-set patient "
            "expectations of how often basal insulin needs "
            "to be injected."),
    ),

    # ============================================================
    # Voltage-gated ion channels (3)
    # ============================================================
    Receptor(
        id="nav1-7",
        name="Voltage-gated Na⁺ channel Nav1.7",
        receptor_family="ion-channel-vg",
        receptor_subtype="Nav1.7 (SCN9A)",
        structural_summary=(
            "Single α-subunit forms the channel pore (4 "
            "homologous 6-TM domains).  Four voltage-sensor "
            "modules (the S4 helices) drive activation.  "
            "β-subunits modulate kinetics + trafficking."),
        endogenous_ligands=(
            "Voltage gradient (depolarisation)",
        ),
        signalling_output=(
            "Na⁺ influx → action-potential upstroke",
        ),
        tissue_distribution=(
            "Peripheral sensory neurons (DRG)",
            "Olfactory + sympathetic neurons",
        ),
        clinical_relevance=(
            "Loss-of-function: congenital insensitivity to "
            "pain (CIP)",
            "Gain-of-function: inherited erythromelalgia + "
            "paroxysmal extreme pain disorder",
            "Local anaesthetics (lidocaine, bupivacaine, "
            "ropivacaine) block Nav non-selectively",
            "Tetrodotoxin (pufferfish) + saxitoxin (PSP) are "
            "canonical Nav site-1 blockers",
            "Nav1.7-selective blockers (suzetrigine — Vertex, "
            "FDA-approved Jan 2025 for moderate/severe acute "
            "pain) are a paradigm-shifting non-opioid "
            "analgesic class",
        ),
        cross_reference_drug_class_ids=(
            "antiepileptics",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Suzetrigine (VX-548) is the first non-opioid "
            "Nav1.7-selective blocker ever approved — "
            "decades of effort across many companies."),
    ),
    Receptor(
        id="herg-kv11-1",
        name="hERG (Kv11.1) potassium channel",
        receptor_family="ion-channel-vg",
        receptor_subtype="Kv11.1 (KCNH2)",
        structural_summary=(
            "Tetrameric voltage-gated K⁺ channel; carries "
            "the rapid component (IKr) of cardiac repolar"
            "isation."),
        endogenous_ligands=(
            "Voltage gradient",
        ),
        signalling_output=(
            "K⁺ efflux → cardiac action-potential phase 3 "
            "repolarisation",
        ),
        tissue_distribution=(
            "Cardiac ventricular myocytes",
            "CNS",
        ),
        clinical_relevance=(
            "Loss-of-function (genetic LQT2 or drug block): "
            "QT prolongation → torsades de pointes",
            "Drug-induced QT prolongation is the dominant "
            "cardiac safety risk in modern drug development "
            "— ICH-E14 + S7B guidelines mandate hERG screening",
            "Withdrawn drugs (terfenadine, astemizole, "
            "cisapride, grepafloxacin) all hit hERG at "
            "clinically-relevant exposures",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "hERG's spacious aromatic-ring-lined inner "
            "vestibule binds an unusually broad chemotype "
            "range — the molecular basis of the universal "
            "‘hERG liability’ concern."),
    ),
    Receptor(
        id="cav1-2",
        name="L-type Ca²⁺ channel Cav1.2",
        receptor_family="ion-channel-vg",
        receptor_subtype="Cav1.2 (CACNA1C)",
        structural_summary=(
            "Single α1 subunit (4 6-TM domain homologues) + "
            "auxiliary β + α2δ + γ subunits.  The "
            "dihydropyridine-binding pocket sits in domain III "
            "+ IV S6 helices."),
        endogenous_ligands=(
            "Voltage gradient",
        ),
        signalling_output=(
            "Ca²⁺ influx → cardiac contraction (excitation-"
            "contraction coupling) + smooth-muscle "
            "contraction + neurotransmitter release",
        ),
        tissue_distribution=(
            "Cardiac myocytes (driver of phase-2 plateau)",
            "Vascular smooth muscle",
            "Pancreatic β cells (glucose-stimulated insulin "
            "release)",
            "Neurons (presynaptic neurotransmitter release "
            "+ dendritic Ca²⁺)",
        ),
        clinical_relevance=(
            "Hypertension + angina + Raynaud's: dihydro"
            "pyridines (amlodipine, nifedipine, felodipine)",
            "Rate control in atrial fibrillation: non-DHPs "
            "(verapamil, diltiazem)",
            "Subarachnoid haemorrhage vasospasm prophylaxis: "
            "nimodipine",
        ),
        cross_reference_drug_class_ids=(
            "ccbs",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Different drug classes bind distinct + "
            "allosterically-coupled sites: dihydropyridines, "
            "phenylalkylamines (verapamil), benzothiazepines "
            "(diltiazem) — the Goldman / Triggle classical "
            "characterisation."),
    ),

    # ============================================================
    # Ligand-gated ion channels (3)
    # ============================================================
    Receptor(
        id="nicotinic-achr",
        name="Nicotinic acetylcholine receptor (nAChR)",
        receptor_family="ion-channel-lg",
        receptor_subtype="nAChR (Cys-loop)",
        structural_summary=(
            "Pentameric Cys-loop receptor; muscle (α1)₂β1δε "
            "vs neuronal (α / β subtype combinations).  Each "
            "subunit has 4 TM helices; M2 lines the channel "
            "pore."),
        endogenous_ligands=(
            "Acetylcholine",
        ),
        signalling_output=(
            "Cation influx (Na⁺ / K⁺ / some Ca²⁺) → "
            "depolarisation",
        ),
        tissue_distribution=(
            "Neuromuscular junction (muscle nAChR)",
            "Autonomic ganglia (Nn neuronal)",
            "CNS reward + cognition circuits (α4β2, α7)",
        ),
        clinical_relevance=(
            "Smoking cessation: varenicline (α4β2 partial "
            "agonist), bupropion, nicotine replacement",
            "Depolarising neuromuscular blockade: "
            "succinylcholine (nAChR agonist → desensitisation)",
            "Non-depolarising NMB: rocuronium, vecuronium "
            "(competitive antagonists)",
            "Myasthenia gravis: autoimmune nAChR antibodies "
            "→ acetylcholinesterase inhibitor + rituximab / "
            "complement-pathway inhibitor therapy",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Bungarotoxin (snake α-toxin) labels the muscle "
            "nAChR with extraordinary specificity — historic "
            "tool for purifying + structurally characterising "
            "the receptor."),
    ),
    Receptor(
        id="gaba-a",
        name="GABA-A receptor",
        receptor_family="ion-channel-lg",
        receptor_subtype="GABA-A (Cys-loop)",
        structural_summary=(
            "Pentameric Cys-loop receptor; typical subunit "
            "composition 2α + 2β + 1γ (γ confers benzo"
            "diazepine sensitivity).  Cl⁻-permeable when "
            "open."),
        endogenous_ligands=(
            "GABA",
            "Allopregnanolone (positive allosteric modulator)",
        ),
        signalling_output=(
            "Cl⁻ influx → hyperpolarisation → inhibition",
        ),
        tissue_distribution=(
            "CNS — the dominant inhibitory neurotransmission "
            "across cortex, striatum, thalamus, cerebellum",
        ),
        clinical_relevance=(
            "Anxiety + insomnia + epilepsy + alcohol "
            "withdrawal: benzodiazepines (PAMs of GABA-A; "
            "diazepam, lorazepam, alprazolam, midazolam)",
            "‘Z-drugs’ (zolpidem, zopiclone) bind same site "
            "with subunit-selectivity",
            "Anaesthetic induction: propofol, etomidate "
            "(direct GABA-A activators at high concentrations)",
            "Postpartum depression: brexanolone (IV) + "
            "zuranolone (oral) — synthetic neurosteroids",
        ),
        cross_reference_drug_class_ids=(
            "benzodiazepines", "antiepileptics",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Flumazenil is the specific benzodiazepine "
            "antagonist — used to reverse iatrogenic over-"
            "sedation but not toxicological overdose "
            "(seizure risk)."),
    ),
    Receptor(
        id="nmda",
        name="NMDA glutamate receptor",
        receptor_family="ion-channel-lg",
        receptor_subtype="NMDA (iGluR)",
        structural_summary=(
            "Tetrameric ionotropic glutamate receptor; "
            "obligate co-agonism by glutamate + glycine (or "
            "D-serine).  Voltage-dependent Mg²⁺ block makes "
            "it a coincidence detector."),
        endogenous_ligands=(
            "L-Glutamic acid (glutamate, primary agonist)",
            "Glycine (co-agonist at GluN1 subunit)",
            "D-Serine (alternative co-agonist)",
        ),
        signalling_output=(
            "Na⁺ + K⁺ + Ca²⁺ flux (high Ca²⁺ permeability) "
            "→ excitation + LTP induction",
        ),
        tissue_distribution=(
            "CNS — nearly all excitatory synapses",
        ),
        clinical_relevance=(
            "NMDA antagonists: ketamine (anaesthetic + "
            "rapid-onset antidepressant esketamine), "
            "memantine (Alzheimer's adjunct), dextrometh"
            "orphan (cough; in dextromethorphan-bupropion "
            "for depression)",
            "PCP + ketamine recreational use → dissociative "
            "psychosis",
            "Anti-NMDA-receptor encephalitis (paraneoplastic "
            "or post-infectious autoimmune)",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(
            "camkii",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "L-Glutamic acid", "Glycine",
        ),
        notes=(
            "NMDA-receptor-mediated Ca²⁺ influx activates "
            "CaMKII → AMPAR insertion → synaptic potentiation "
            "— the cellular basis of associative learning + "
            "memory in Bliss + Lømo's classical LTP model."),
    ),

    # ============================================================
    # Monoamine transporters (3)
    # ============================================================
    Receptor(
        id="sert",
        name="Serotonin transporter (SERT)",
        receptor_family="transporter-monoamine",
        receptor_subtype="SERT (SLC6A4)",
        structural_summary=(
            "Na⁺/Cl⁻-coupled neurotransmitter transporter "
            "(NSS family).  12-TM helices.  Crystal "
            "structures of bacterial homologue LeuT + later "
            "human SERT bound to escitalopram (Coleman 2016) "
            "transformed the structural pharmacology of "
            "antidepressants."),
        endogenous_ligands=(
            "Serotonin (5-hydroxytryptamine, 5-HT) — "
            "substrate",
        ),
        signalling_output=(
            "Na⁺/Cl⁻-coupled re-uptake of synaptic serotonin "
            "back into the presynaptic neuron",
        ),
        tissue_distribution=(
            "Serotonergic neuron presynaptic terminals "
            "(raphe nuclei + their projections)",
            "Platelets (the only peripheral source of "
            "5-HT-uptake; basis of platelet-5-HT clinical "
            "test)",
            "Enterocytes",
        ),
        clinical_relevance=(
            "Depression + anxiety + OCD: SSRIs (fluoxetine, "
            "sertraline, citalopram, escitalopram, "
            "paroxetine); SNRIs (venlafaxine, duloxetine — "
            "SERT + NET); TCAs (mostly SERT + NET)",
            "Migraine prophylaxis: SNRI venlafaxine off-"
            "label",
        ),
        cross_reference_drug_class_ids=(
            "ssris",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "5-HT₂ₐ-receptor partial agonists (psilocybin, "
            "LSD) are the active centre of the psychedelic "
            "renaissance — same monoamine system, different "
            "pharmacological lever."),
    ),
    Receptor(
        id="net",
        name="Norepinephrine transporter (NET)",
        receptor_family="transporter-monoamine",
        receptor_subtype="NET (SLC6A2)",
        structural_summary=(
            "Na⁺/Cl⁻-coupled NSS-family transporter; close "
            "homologue of SERT + DAT."),
        endogenous_ligands=(
            "Noradrenaline / norepinephrine — substrate",
            "Dopamine (also a substrate at NET in cortex)",
        ),
        signalling_output=(
            "Re-uptake of synaptic noradrenaline (+ "
            "dopamine in cortex)",
        ),
        tissue_distribution=(
            "Noradrenergic neuron presynaptic terminals "
            "(locus coeruleus + sympathetic)",
            "Adrenal medulla",
        ),
        clinical_relevance=(
            "Depression: SNRIs (venlafaxine, duloxetine); "
            "atomoxetine (selective NET — first non-"
            "stimulant ADHD treatment)",
            "Pheochromocytoma imaging: ¹²³I-MIBG (NET-"
            "avidly internalised radio-tracer)",
            "Cocaine + amphetamine block / reverse NET",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Atomoxetine (Strattera) was approved 2002 + "
            "remains the only NET-selective ADHD drug — "
            "non-controlled scheduling unlike "
            "methylphenidate / amphetamines."),
    ),
    Receptor(
        id="dat",
        name="Dopamine transporter (DAT)",
        receptor_family="transporter-monoamine",
        receptor_subtype="DAT (SLC6A3)",
        structural_summary=(
            "Na⁺/Cl⁻-coupled NSS-family transporter; "
            "Drosophila DAT crystal structures (Penmatsa "
            "2013) gave the first eukaryotic snapshots."),
        endogenous_ligands=(
            "Dopamine — substrate",
        ),
        signalling_output=(
            "Re-uptake of synaptic dopamine into presynaptic "
            "terminals",
        ),
        tissue_distribution=(
            "Dopaminergic neurons (substantia nigra + "
            "ventral tegmental area + their projections)",
        ),
        clinical_relevance=(
            "ADHD + narcolepsy: methylphenidate, "
            "dextroamphetamine, modafinil (DAT inhibitors / "
            "releasers)",
            "Cocaine binding site",
            "Parkinson's disease: dopamine-transporter "
            "imaging (¹²³I-FP-CIT / DaTscan) confirms "
            "presynaptic deficit",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_molecule_names=(
            "Dopamine",
        ),
        notes=(
            "MPTP (a meperidine analogue contaminant) is "
            "selectively taken up by DAT into nigrostriatal "
            "neurons + metabolised to MPP+ → mitochondrial "
            "Complex I inhibition → drug-induced "
            "Parkinsonism.  Langston's 1983 paper launched "
            "modern Parkinson's research."),
    ),

    # ============================================================
    # Other transporters (2)
    # ============================================================
    Receptor(
        id="sglt2",
        name="Sodium-glucose co-transporter 2 (SGLT2)",
        receptor_family="transporter-other",
        receptor_subtype="SGLT2 (SLC5A2)",
        structural_summary=(
            "Secondary-active Na⁺-glucose co-transporter.  "
            "Couples Na⁺ down its electrochemical gradient "
            "(maintained by Na⁺/K⁺-ATPase) to drive uphill "
            "glucose reabsorption."),
        endogenous_ligands=(
            "Glucose (substrate)", "Na⁺ (co-substrate)",
        ),
        signalling_output=(
            "Reabsorption of ~ 90 % of filtered glucose "
            "(SGLT2 in proximal tubule S1/S2 segment)",
        ),
        tissue_distribution=(
            "Renal proximal convoluted tubule (S1 + S2 "
            "segments)",
        ),
        clinical_relevance=(
            "Type-2 diabetes: SGLT2 inhibitors "
            "(empagliflozin, dapagliflozin, canagliflozin, "
            "ertugliflozin)",
            "Heart failure (reduced + preserved EF) — class-"
            "level CV benefit independent of glycaemic "
            "control (EMPA-REG / DAPA-HF / EMPEROR-Reduced "
            "/ EMPEROR-Preserved)",
            "CKD progression slowing (DAPA-CKD, EMPA-KIDNEY)",
        ),
        cross_reference_drug_class_ids=(
            "sglt2-inhibitors",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "na-k-atpase",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Phlorizin (apple-tree-bark glucoside) was the "
            "natural-product lead — the entire SGLT2-"
            "inhibitor class derives from medicinal-"
            "chemistry optimisation of phlorizin's β-glucoside "
            "scaffold."),
    ),
    Receptor(
        id="p-glycoprotein",
        name="P-glycoprotein efflux pump",
        receptor_family="transporter-other",
        receptor_subtype="P-gp (ABCB1, MDR1)",
        structural_summary=(
            "ATP-binding-cassette (ABC) family efflux "
            "transporter.  12-TM helices + 2 nucleotide-"
            "binding domains.  ATP hydrolysis drives "
            "extrusion of a remarkably broad substrate "
            "range."),
        endogenous_ligands=(
            "(no single ‘endogenous ligand’ — broad "
            "substrate specificity)",
        ),
        signalling_output=(
            "ATP-dependent efflux of xenobiotic + drug "
            "substrates",
        ),
        tissue_distribution=(
            "Intestinal enterocyte apical membrane "
            "(absorption barrier)",
            "Hepatocyte canalicular membrane (biliary "
            "excretion)",
            "Renal proximal tubule (urinary excretion)",
            "Blood-brain barrier capillary endothelium "
            "(CNS exclusion)",
            "Tumour cells (multi-drug resistance — MDR)",
        ),
        clinical_relevance=(
            "MDR phenotype in cancer chemotherapy: P-gp over"
            "expression refluxes anthracyclines, vinca "
            "alkaloids, taxanes",
            "Drug-drug interactions: ketoconazole, verapamil, "
            "amiodarone are P-gp inhibitors → ↑ digoxin / "
            "DOAC / cyclosporine exposure",
            "BBB exclusion — many CNS-active candidates fail "
            "in development because P-gp keeps them out of "
            "the brain",
        ),
        cross_reference_drug_class_ids=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "p-glycoprotein",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Tariquidar + zosuquidar (3rd-generation P-gp "
            "inhibitors) failed in oncology trials despite "
            "reversing MDR in vitro — the clinical chemo-"
            "sensitisation strategy is essentially defunct."),
    ),
)
