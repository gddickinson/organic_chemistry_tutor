"""Phase MB-2.0 (round 221) — 30-entry microbial virulence-
factor + toxin catalogue.

Each entry carries typed cross-references into:
- ``microbio.core.microbes`` ids (the MB-1.0 catalogue —
  source organisms; left empty for toxins whose source isn't
  yet seeded — diphtheria, cholera, pertussis, anthrax, the
  clostridial toxins).
- ``biochem.core.enzymes`` ids (where the toxin IS an
  enzyme; mostly empty since toxin-specific enzymes are not
  in BC-1.0 — but adenylate-cyclase appears for cholera +
  edema-factor entries; pka for the cAMP-amplification
  cascade).
- ``cellbio.core.cell_signaling`` ids (host pathways the
  toxin hijacks — gpcr-camp-pka for cholera/pertussis,
  intrinsic-apoptosis or pyroptosis for cytotoxins, tlr +
  nf-kb for LPS, jak-stat for some superantigens).

All cross-reference ids verified against destination
catalogues at write time; the round-221 catalogue tests gate
re-validation at every test run.
"""
from __future__ import annotations
from typing import Tuple

from microbio.core.virulence_factors import VirulenceFactor


VIRULENCE_FACTORS: Tuple[VirulenceFactor, ...] = (
    # ============================================================
    # AB-toxins (8)
    # ============================================================
    VirulenceFactor(
        id="diphtheria-toxin",
        name="Diphtheria toxin (DT)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "AB-type single polypeptide cleaved into A + B "
            "fragments held by a disulfide bond.  B fragment "
            "binds heparin-binding EGF (HB-EGF) on host "
            "cells.  Encoded by lysogenic β-corynephage tox "
            "gene.",
        ),
        target_tissue_or_cell=(
            "Pharyngeal epithelium",
            "Cardiac myocytes (toxic myocarditis)",
            "Peripheral nerves (demyelinating neuropathy)",
        ),
        mode_of_action=(
            "A fragment ADP-ribosylates diphthamide residue "
            "of eukaryotic elongation factor 2 (eEF2) → "
            "irreversible block of protein synthesis → host-"
            "cell death",
        ),
        clinical_syndrome=(
            "Diphtheria: pseudomembranous pharyngitis, "
            "myocarditis, peripheral neuropathy",
        ),
        vaccine_or_antitoxin=(
            "DTP / DTaP / Tdap toxoid (formaldehyde-"
            "inactivated DT)",
            "Equine diphtheria antitoxin (DAT) for active "
            "disease",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis",
        ),
        notes=(
            "DT was the first toxin used in immunotoxin "
            "engineering (denileukin diftitox = IL-2-DT "
            "fusion for CTCL).  Source organism "
            "Corynebacterium diphtheriae not yet in MB-1.0."),
    ),
    VirulenceFactor(
        id="cholera-toxin",
        name="Cholera toxin (CT / CTX)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "AB₅ holotoxin: 1 A subunit + pentameric B ring "
            "that binds GM1 ganglioside.  Encoded by "
            "lysogenic CTXφ phage.",
        ),
        target_tissue_or_cell=(
            "Small-intestinal enterocytes (apical brush "
            "border)",
        ),
        mode_of_action=(
            "A1 subunit ADP-ribosylates Arg201 of Gαs → "
            "permanent GTP-bound state → constitutive "
            "adenylate cyclase activation → massive cAMP "
            "rise → CFTR-mediated Cl⁻ secretion → osmotic "
            "diarrhoea",
        ),
        clinical_syndrome=(
            "Cholera: profuse rice-water diarrhoea, "
            "dehydration, hypokalaemic acidosis (untreated "
            "mortality > 50 %)",
        ),
        vaccine_or_antitoxin=(
            "Oral inactivated whole-cell cholera vaccine "
            "(Dukoral) + recombinant CTB subunit",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        notes=(
            "Recombinant CTB is widely used as a mucosal "
            "vaccine adjuvant + as a research probe for GM1+ "
            "lipid rafts.  Source organism Vibrio cholerae "
            "not in MB-1.0."),
    ),
    VirulenceFactor(
        id="pertussis-toxin",
        name="Pertussis toxin (PT / PTX)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "AB₅ heterohexamer (S1 = A; S2-S5 = B).  S2/S3 "
            "bind sialic-acid glycoconjugates on respiratory "
            "epithelium + leukocytes.",
        ),
        target_tissue_or_cell=(
            "Respiratory epithelium",
            "Leukocytes (lymphocytosis-promoting factor)",
        ),
        mode_of_action=(
            "S1 ADP-ribosylates Cys of Gαi → locked GDP-"
            "bound state → loss of inhibitory GPCR signalling "
            "→ unopposed cAMP rise + impaired chemotaxis",
        ),
        clinical_syndrome=(
            "Whooping cough (pertussis): paroxysmal cough, "
            "inspiratory whoop, post-tussive emesis; severe "
            "in infants → apnoea + death",
        ),
        vaccine_or_antitoxin=(
            "Acellular pertussis vaccine (DTaP / Tdap) "
            "containing chemically-inactivated PT + FHA + "
            "pertactin + fimbrial agglutinogens",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        notes=(
            "PT is a workhorse research tool — laboratory "
            "Gαi inactivator for dissecting GPCR coupling.  "
            "Source organism Bordetella pertussis not in "
            "MB-1.0."),
    ),
    VirulenceFactor(
        id="shiga-toxin",
        name="Shiga toxin (Stx) / Shiga-like toxin (Stx1, Stx2)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "AB₅ holotoxin.  B pentamer binds globotri"
            "aosylceramide (Gb3) on glomerular endothelium "
            "+ neurons.  Stx1/Stx2 are phage-encoded in "
            "EHEC / STEC strains (e.g. O157:H7).",
        ),
        target_tissue_or_cell=(
            "Glomerular + intestinal microvascular endo"
            "thelium",
            "CNS neurons",
        ),
        mode_of_action=(
            "A subunit is an N-glycosidase — depurinates a "
            "single A4324 in 28S rRNA → block of protein "
            "synthesis → endothelial apoptosis + "
            "microthrombi",
        ),
        clinical_syndrome=(
            "Bloody diarrhoea + haemolytic-uraemic syndrome "
            "(HUS): microangiopathic haemolytic anaemia + "
            "thrombocytopenia + acute kidney injury",
        ),
        vaccine_or_antitoxin=(
            "No licensed vaccine.  Eculizumab (anti-C5 mAb) "
            "trialled for STEC-HUS — modest benefit",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis",
        ),
        notes=(
            "Antibiotics are CONTRAINDICATED in EHEC because "
            "they up-regulate phage induction + Stx release "
            "→ increased HUS risk.  Source organisms "
            "Shigella + EHEC not in MB-1.0."),
    ),
    VirulenceFactor(
        id="anthrax-lethal-factor",
        name="Anthrax lethal factor (LF)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "Zinc metalloprotease A subunit; uses protective "
            "antigen (PA) as the B-component receptor / pore.  "
            "PA + LF = lethal toxin (LeTx); PA + EF = oedema "
            "toxin (EdTx); both require PA octamer pore.",
        ),
        target_tissue_or_cell=(
            "Macrophages + monocytes (pyroptotic death)",
            "Vascular endothelium (collapse → shock)",
        ),
        mode_of_action=(
            "Cleaves N-termini of MAP2K1-7 (MAPK kinase "
            "family) → blockade of MAPK / ERK + p38 + JNK "
            "signalling → impaired innate immunity + sepsis-"
            "like syndrome",
        ),
        clinical_syndrome=(
            "Anthrax: cutaneous (eschar), inhalation "
            "(haemorrhagic mediastinitis + meningitis), GI",
        ),
        vaccine_or_antitoxin=(
            "AVA / BioThrax (PA-based vaccine for at-risk + "
            "post-exposure)",
            "Raxibacumab + obiltoxaximab (anti-PA mAbs)",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pyroptosis",
        ),
        notes=(
            "LF cleaves MAP2K right at the docking groove "
            "for ERK → exquisitely-targeted disruption.  "
            "Source organism Bacillus anthracis not in "
            "MB-1.0."),
    ),
    VirulenceFactor(
        id="anthrax-oedema-factor",
        name="Anthrax oedema factor (EF)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "Calmodulin-activated adenylate cyclase A "
            "subunit; PA delivers it via the same octamer "
            "pore that delivers LF.",
        ),
        target_tissue_or_cell=(
            "Phagocytes + endothelium",
        ),
        mode_of_action=(
            "Massive cAMP elevation in target cells → "
            "phagocyte dysfunction + tissue oedema",
        ),
        clinical_syndrome=(
            "Cutaneous anthrax oedema (massive non-pitting); "
            "contributes to GI + inhalation-anthrax shock",
        ),
        vaccine_or_antitoxin=(
            "AVA + anti-PA mAbs (same as for LF)",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        notes=(
            "EF is the 'foreign adenylate cyclase' — joins "
            "Bordetella pertussis CyaA + Pseudomonas ExoY "
            "as bacterial calmodulin-activated cyclases."),
    ),
    VirulenceFactor(
        id="tetanus-toxin",
        name="Tetanus toxin (tetanospasmin, TeNT)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "Single polypeptide cleaved to heavy chain (B = "
            "binding + translocation) + light chain (A = "
            "zinc-endopeptidase).  Heavy chain binds GT1b / "
            "GD1b gangliosides on motor-neuron axon terminals "
            "+ undergoes retrograde axonal transport to the "
            "spinal cord.",
        ),
        target_tissue_or_cell=(
            "Spinal-cord inhibitory interneurons (Renshaw "
            "cells)",
        ),
        mode_of_action=(
            "Light chain cleaves VAMP / synaptobrevin → "
            "blocks release of GABA + glycine from inhibitory "
            "interneurons → unopposed motor-neuron firing → "
            "spastic paralysis",
        ),
        clinical_syndrome=(
            "Tetanus: lockjaw, opisthotonus, autonomic "
            "instability, generalised spasms; case-fatality "
            "10-30 % even with treatment",
        ),
        vaccine_or_antitoxin=(
            "Tetanus toxoid (formaldehyde-inactivated TeNT) "
            "in DTaP / Tdap / Td schedules",
            "Human tetanus immune globulin (TIG) for active "
            "disease",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Same SNARE-cleavage mechanism as botulinum "
            "toxins, but different tissue targeting "
            "(retrograde transport to spinal cord vs "
            "peripheral neuromuscular junction).  Source "
            "organism Clostridium tetani not in MB-1.0."),
    ),
    VirulenceFactor(
        id="botulinum-toxin",
        name="Botulinum toxin (BoNT-A through G)",
        mechanism_class="ab-toxin",
        structural_notes=(
            "Same dichain heavy + light architecture as "
            "tetanus toxin.  Seven serotypes (A-G); BoNT-A "
            "+ BoNT-B are clinically used.  Heavy chain "
            "binds presynaptic nerve-terminal receptors "
            "(SV2 + gangliosides for BoNT-A).",
        ),
        target_tissue_or_cell=(
            "Peripheral cholinergic motor + autonomic nerve "
            "terminals",
        ),
        mode_of_action=(
            "Light chain (zinc endopeptidase) cleaves SNARE "
            "proteins (SNAP-25 for BoNT-A, VAMP for BoNT-B/D/"
            "F/G, syntaxin for BoNT-C) → blocks acetylcholine "
            "release → flaccid paralysis",
        ),
        clinical_syndrome=(
            "Botulism: descending flaccid paralysis, "
            "bilateral cranial nerve palsies, respiratory "
            "failure",
        ),
        vaccine_or_antitoxin=(
            "Equine heptavalent botulism antitoxin (HBAT)",
            "BabyBIG human botulism immune globulin for "
            "infant botulism",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Cosmetic + therapeutic uses (Botox / Dysport / "
            "Xeomin / Myobloc).  Most lethal substance per "
            "unit mass known.  Source organism Clostridium "
            "botulinum not in MB-1.0."),
    ),

    # ============================================================
    # Pore-forming cytolysins (5)
    # ============================================================
    VirulenceFactor(
        id="alpha-toxin-staph",
        name="alpha-toxin (Hla)",
        mechanism_class="pore-forming",
        structural_notes=(
            "Heptameric beta-barrel transmembrane pore (~ 1.4 nm "
            "internal diameter).  ADAM10 metalloprotease is "
            "the high-affinity cellular receptor.",
        ),
        target_tissue_or_cell=(
            "Erythrocytes (beta-haemolysis on blood agar)",
            "Platelets, monocytes, lymphocytes, endothelium",
            "Airway + skin epithelium",
        ),
        mode_of_action=(
            "Monomers bind ADAM10 -> heptamerise -> insert into "
            "membrane -> osmotic lysis + Ca2+ influx -> "
            "downstream pyroptosis + tissue necrosis",
        ),
        clinical_syndrome=(
            "Skin + soft-tissue infection, necrotising "
            "pneumonia, bacteraemia",
        ),
        vaccine_or_antitoxin=(
            "Suvratoxumab (anti-alpha-toxin mAb) trialled "
            "for ventilated-patient pneumonia",
        ),
        cross_reference_microbe_ids=(
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "pyroptosis", "intrinsic-apoptosis",
        ),
        notes=(
            "Original textbook beta-barrel pore-forming toxin "
            "(Song crystal structure 1996) + the model for "
            "the entire family of bacterial cytolysins."),
    ),
    VirulenceFactor(
        id="streptolysin-o",
        name="Streptolysin O (SLO)",
        mechanism_class="pore-forming",
        structural_notes=(
            "Cholesterol-dependent cytolysin (CDC family).  "
            "Monomers bind membrane cholesterol -> "
            "oligomerise -> mega-pores (~ 25-30 nm).",
        ),
        target_tissue_or_cell=(
            "Any cholesterol-containing eukaryotic membrane",
            "Erythrocytes (beta-haemolysis on blood agar)",
        ),
        mode_of_action=(
            "Massive transmembrane pore formation -> "
            "uncontrolled ion + macromolecule flux -> cell "
            "lysis",
        ),
        clinical_syndrome=(
            "Streptococcal pharyngitis, scarlet fever, "
            "necrotising fasciitis, invasive GAS",
        ),
        vaccine_or_antitoxin=(
            "Anti-streptolysin O (ASO) titre is the "
            "diagnostic serology marker for recent GAS "
            "infection (rheumatic fever workup)",
        ),
        cross_reference_microbe_ids=(
            "streptococcus-pyogenes",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "pyroptosis",
        ),
        notes=(
            "Used as a research reagent to permeabilise "
            "cell membranes selectively for protein delivery."),
    ),
    VirulenceFactor(
        id="pneumolysin",
        name="Pneumolysin (Ply)",
        mechanism_class="pore-forming",
        structural_notes=(
            "Cholesterol-dependent cytolysin (CDC family) - "
            "homologue of streptolysin O.  Released "
            "primarily by autolysis (not active secretion).",
        ),
        target_tissue_or_cell=(
            "Respiratory + meningeal epithelium",
            "Cardiomyocytes (pneumococcal myocardial damage)",
        ),
        mode_of_action=(
            "Cholesterol-binding -> oligomeric pore formation "
            "-> host-cell lysis + complement activation via "
            "antibody-independent classical pathway",
        ),
        clinical_syndrome=(
            "Pneumonia, otitis media, meningitis, sepsis",
        ),
        vaccine_or_antitoxin=(
            "Indirect protection via pneumococcal conjugate "
            "vaccines (PCV13 / PCV15 / PCV20) targeting "
            "capsular polysaccharide",
        ),
        cross_reference_microbe_ids=(
            "streptococcus-pneumoniae",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "pyroptosis", "tlr",
        ),
        notes=(
            "Sub-lytic pneumolysin activates TLR4 + "
            "inflammasome -> contributes to neuro"
            "inflammation in pneumococcal meningitis."),
    ),
    VirulenceFactor(
        id="pvl",
        name="Panton-Valentine leukocidin (PVL)",
        mechanism_class="pore-forming",
        structural_notes=(
            "Bicomponent leukocidin: LukS-PV + LukF-PV "
            "monomers heterodimerise + further oligomerise "
            "into octameric beta-barrel pores on PMN "
            "membranes.  Encoded on lysogenic phage; CA-MRSA "
            "USA300 famously carries it.",
        ),
        target_tissue_or_cell=(
            "Polymorphonuclear leukocytes",
        ),
        mode_of_action=(
            "Selective lysis of human leukocytes via C5aR1 "
            "receptor binding -> reduced phagocytic clearance",
        ),
        clinical_syndrome=(
            "Recurrent skin + soft-tissue infections, "
            "necrotising pneumonia (often post-influenza)",
        ),
        vaccine_or_antitoxin=(),
        cross_reference_microbe_ids=(
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "pyroptosis",
        ),
        notes=(
            "PVL+ MRSA is the molecular signature of the "
            "USA300 community-acquired clone."),
    ),
    VirulenceFactor(
        id="listeriolysin-o",
        name="Listeriolysin O (LLO)",
        mechanism_class="pore-forming",
        structural_notes=(
            "Cholesterol-dependent cytolysin (CDC family).  "
            "Uniquely pH-tuned: maximal activity at "
            "phagosomal pH 5.5; rapidly inactivated at "
            "cytosolic pH 7.4 -> safety mechanism that lets "
            "Listeria escape phagosome without lysing the "
            "host cell.",
        ),
        target_tissue_or_cell=(
            "Macrophage + epithelial-cell phagosomal "
            "membrane",
        ),
        mode_of_action=(
            "Perforates phagosomal membrane -> bacterium "
            "escapes into cytosol -> ActA-driven actin-comet "
            "intracellular motility + cell-to-cell spread",
        ),
        clinical_syndrome=(
            "Listeriosis: febrile gastroenteritis, "
            "meningoencephalitis, foetal infection / "
            "stillbirth",
        ),
        vaccine_or_antitoxin=(
            "No human vaccine.  LLO scaffold used in "
            "experimental cancer-vaccine platform (ADXS-HPV).",
        ),
        cross_reference_microbe_ids=(
            "listeria-monocytogenes",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis",
        ),
        notes=(
            "LLO is the prototypical 'phagosomal escape' "
            "virulence factor."),
    ),

    # ============================================================
    # Superantigens (3)
    # ============================================================
    VirulenceFactor(
        id="tsst-1",
        name="Toxic-shock-syndrome toxin 1 (TSST-1)",
        mechanism_class="superantigen",
        structural_notes=(
            "Single ~ 22-kDa polypeptide.  Bridges MHC-II "
            "(alpha-chain outside the peptide-binding "
            "groove) + the V-beta region of TCR -- bypassing "
            "antigen specificity.",
        ),
        target_tissue_or_cell=(
            "T lymphocytes + antigen-presenting cells",
        ),
        mode_of_action=(
            "Polyclonal T-cell activation (~ 5-30 % of "
            "T-cell repertoire vs ~ 0.001 % for conventional "
            "antigen) -> massive cytokine storm",
        ),
        clinical_syndrome=(
            "Staphylococcal toxic shock syndrome: fever, "
            "diffuse erythrodermic rash, hypotension, "
            "multi-organ dysfunction; classic association "
            "with super-absorbent tampons (1980s)",
        ),
        vaccine_or_antitoxin=(
            "IVIG for severe cases",
        ),
        cross_reference_microbe_ids=(
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "tcr", "jak-stat", "nf-kb",
        ),
        notes=(
            "TSST-1 was the molecular driver of the 1980 "
            "tampon-associated TSS epidemic."),
    ),
    VirulenceFactor(
        id="staphylococcal-enterotoxins",
        name="Staphylococcal enterotoxins (SEA-SEE)",
        mechanism_class="superantigen",
        structural_notes=(
            "Family of ~ 25-kDa heat-stable polypeptides; "
            "six classical (SEA-SEE) + many newer "
            "serotypes.",
        ),
        target_tissue_or_cell=(
            "GI mucosa (when ingested as preformed toxin)",
            "T lymphocytes (when systemic)",
        ),
        mode_of_action=(
            "Vagal stimulation in gut -> emesis (within "
            "hours of ingestion); polyclonal T-cell "
            "activation when systemic",
        ),
        clinical_syndrome=(
            "Staphylococcal food poisoning: rapid-onset "
            "(2-6 h) vomiting + diarrhoea after ingestion",
        ),
        vaccine_or_antitoxin=(),
        cross_reference_microbe_ids=(
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "tcr", "nf-kb",
        ),
        notes=(
            "SE family members are heat-stable: they survive "
            "cooking even when the producing bacteria are "
            "killed."),
    ),
    VirulenceFactor(
        id="strep-pyrogenic-exotoxin-a",
        name="Streptococcal pyrogenic exotoxin A (SpeA)",
        mechanism_class="superantigen",
        structural_notes=(
            "~ 25-kDa superantigen homologous to staph SEs; "
            "phage-encoded.",
        ),
        target_tissue_or_cell=(
            "T lymphocytes + APCs",
        ),
        mode_of_action=(
            "Same V-beta-MHC-II bridging mechanism -> "
            "polyclonal T-cell activation",
        ),
        clinical_syndrome=(
            "Scarlet fever + Streptococcal toxic shock "
            "syndrome (STSS)",
        ),
        vaccine_or_antitoxin=(
            "IVIG for severe STSS",
        ),
        cross_reference_microbe_ids=(
            "streptococcus-pyogenes",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "tcr", "nf-kb",
        ),
        notes=(
            "SpeB is a different beast -- a cysteine "
            "protease, not a superantigen."),
    ),

    # ============================================================
    # Adhesins (3)
    # ============================================================
    VirulenceFactor(
        id="upec-fimbriae",
        name="Type-1 + P fimbriae (UPEC adhesins)",
        mechanism_class="adhesin",
        structural_notes=(
            "Type-1: FimH adhesin tip on a FimA pilus shaft, "
            "binds mannose residues on uroplakin Ia.  P "
            "(pap): PapG adhesin tip, binds Gal-alpha-1,4-Gal "
            "of uroepithelial glycolipids.",
        ),
        target_tissue_or_cell=(
            "Bladder + ureter + renal-pelvic uroepithelium",
        ),
        mode_of_action=(
            "Bacterial attachment to host glycoconjugates "
            "-> resists urinary flow shear -> biofilm "
            "formation + intracellular bacterial communities",
        ),
        clinical_syndrome=(
            "Cystitis + ascending pyelonephritis",
        ),
        vaccine_or_antitoxin=(
            "FimH-vaccine candidates in trials",
        ),
        cross_reference_microbe_ids=(
            "escherichia-coli",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "FimH antagonists (mannose-based glycomimetics) "
            "are an emerging anti-virulence drug strategy."),
    ),
    VirulenceFactor(
        id="m-protein",
        name="M protein",
        mechanism_class="adhesin",
        structural_notes=(
            "Coiled-coil alpha-helical surface protein; the "
            "major protective antigen of S. pyogenes.  "
            "~ 100 M-types encoded by emm gene; basis of "
            "epidemiological strain typing.",
        ),
        target_tissue_or_cell=(
            "Pharyngeal + skin epithelium",
            "Plasma + complement components",
        ),
        mode_of_action=(
            "Binds plasminogen + factor H + fibrinogen -> "
            "antiphagocytic surface coat + complement "
            "evasion + plasmin recruitment",
        ),
        clinical_syndrome=(
            "Pharyngitis, scarlet fever, impetigo, "
            "necrotising fasciitis, post-streptococcal "
            "glomerulonephritis + rheumatic fever",
        ),
        vaccine_or_antitoxin=(
            "Multivalent M-protein vaccines (StreptAnova) "
            "in clinical development",
        ),
        cross_reference_microbe_ids=(
            "streptococcus-pyogenes",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Anti-M-protein antibodies cross-react with "
            "cardiac myosin -> drive carditis of acute "
            "rheumatic fever (molecular mimicry)."),
    ),
    VirulenceFactor(
        id="yersinia-yada-invasin",
        name="YadA + Invasin (Yersinia adhesins)",
        mechanism_class="adhesin",
        structural_notes=(
            "YadA: trimeric autotransporter.  Invasin: "
            "outer-membrane beta-barrel that engages host "
            "beta-1 integrins.",
        ),
        target_tissue_or_cell=(
            "Intestinal M cells + Peyer's-patch lymphoid "
            "follicles",
        ),
        mode_of_action=(
            "Invasin binds beta-1 integrins -> high-affinity "
            "uptake into M cells.  YadA mediates collagen + "
            "fibronectin binding + serum-resistance",
        ),
        clinical_syndrome=(
            "Yersinia enterocolitica enteritis + mesenteric "
            "adenitis + reactive arthritis; Y. pestis plague",
        ),
        vaccine_or_antitoxin=(
            "F1 + LcrV subunit vaccines under development "
            "for plague",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Invasin-beta-1-integrin engagement is the "
            "textbook example of bacterial protein "
            "hijacking a host ECM-receptor.  Source genus "
            "Yersinia not in MB-1.0."),
    ),

    # ============================================================
    # Capsules (3)
    # ============================================================
    VirulenceFactor(
        id="hyaluronic-acid-capsule",
        name="Hyaluronic-acid capsule",
        mechanism_class="capsule",
        structural_notes=(
            "Linear polymer of [beta-1,4-glucuronate-beta-"
            "1,3-N-acetylglucosamine] -- chemically identical "
            "to host hyaluronate.  Encoded by hasABC operon.",
        ),
        target_tissue_or_cell=(
            "Phagocyte-rich tissues",
        ),
        mode_of_action=(
            "Molecular mimicry: capsule looks like host "
            "hyaluronate -> poorly immunogenic + resists "
            "phagocytosis + complement deposition",
        ),
        clinical_syndrome=(
            "Required virulence determinant for S. pyogenes "
            "invasive disease",
        ),
        vaccine_or_antitoxin=(),
        cross_reference_microbe_ids=(
            "streptococcus-pyogenes",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "The only bacterial capsule that's immune to a "
            "vaccination strategy because targeting it would "
            "auto-immunise the host vs its own ECM."),
    ),
    VirulenceFactor(
        id="pneumococcal-polysaccharide-capsule",
        name="Pneumococcal polysaccharide capsule",
        mechanism_class="capsule",
        structural_notes=(
            "~ 100 distinct chemical serotypes (chains of "
            "different sugar repeat units).  Encoded by cps "
            "locus; serotype determines virulence + "
            "epidemiology.",
        ),
        target_tissue_or_cell=(
            "Nasopharyngeal + alveolar epithelium",
        ),
        mode_of_action=(
            "Anionic capsule blocks complement deposition + "
            "opsonophagocytosis; antibody to capsule is the "
            "gold-standard correlate of protection",
        ),
        clinical_syndrome=(
            "Pneumonia, meningitis, otitis media, sinusitis, "
            "bacteraemia (especially in asplenic + sickle-"
            "cell patients)",
        ),
        vaccine_or_antitoxin=(
            "PCV13 -> PCV15 -> PCV20 conjugate vaccines",
            "PPSV23 polysaccharide-only vaccine for adults",
        ),
        cross_reference_microbe_ids=(
            "streptococcus-pneumoniae",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Serotype replacement: PCV use suppresses "
            "vaccine serotypes but allows non-vaccine "
            "serotypes to expand."),
    ),
    VirulenceFactor(
        id="anthrax-poly-glutamate-capsule",
        name="Anthrax poly-gamma-D-glutamate capsule",
        mechanism_class="capsule",
        structural_notes=(
            "Unusual peptide capsule (not polysaccharide) -- "
            "polymer of D-glutamate joined by gamma-carboxyl "
            "amide bonds.  Encoded by capBCAD operon on "
            "pXO2 plasmid.",
        ),
        target_tissue_or_cell=(
            "Phagocytes",
        ),
        mode_of_action=(
            "Anti-phagocytic + poorly immunogenic (D-amino "
            "acids resist host proteases); also resists "
            "complement",
        ),
        clinical_syndrome=(
            "Required virulence determinant for B. anthracis "
            "alongside the LF + EF toxins",
        ),
        vaccine_or_antitoxin=(
            "AVA / BioThrax doesn't target the capsule -- "
            "PA-based.",
        ),
        cross_reference_microbe_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "pXO2-encoded capsule + pXO1-encoded tripartite "
            "toxin together define fully virulent B. "
            "anthracis."),
    ),

    # ============================================================
    # Secretion systems (3)
    # ============================================================
    VirulenceFactor(
        id="t3ss",
        name="Type-III secretion system (T3SS / injectisome)",
        mechanism_class="secretion-system",
        structural_notes=(
            "Multi-protein needle complex spanning bacterial "
            "inner + outer membranes.  Hollow needle pierces "
            "host plasma membrane to inject effector "
            "proteins directly into the host cytosol.  "
            "Evolutionarily related to bacterial flagellum.",
        ),
        target_tissue_or_cell=(
            "Intestinal epithelium (Salmonella, Shigella, "
            "EPEC)",
            "Macrophages + neutrophils (Yersinia, "
            "Pseudomonas)",
        ),
        mode_of_action=(
            "Direct injection of bacterial effector "
            "proteins into host cytosol -> hijack actin "
            "cytoskeleton (membrane ruffling for invasion), "
            "block phagocytosis, induce / suppress "
            "apoptosis depending on the strain",
        ),
        clinical_syndrome=(
            "Salmonella enteritis + typhoid; Shigella "
            "dysentery; Yersinia plague; Pseudomonas "
            "respiratory + ocular infections",
        ),
        vaccine_or_antitoxin=(
            "Anti-T3SS-needle vaccines + anti-effector "
            "antibodies in development for several pathogens",
        ),
        cross_reference_microbe_ids=(
            "salmonella-typhi", "pseudomonas-aeruginosa",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis", "pyroptosis",
        ),
        notes=(
            "T3SS is the textbook bacterial 'molecular "
            "syringe' + a major focus of anti-virulence drug "
            "discovery."),
    ),
    VirulenceFactor(
        id="t4ss-caga",
        name="Type-IV secretion system (T4SS) -- H. pylori cag",
        mechanism_class="secretion-system",
        structural_notes=(
            "Multi-component conjugation-system-like machine "
            "that delivers CagA effector + peptidoglycan "
            "into gastric epithelium.  Encoded by cag "
            "pathogenicity island (cag-PAI).",
        ),
        target_tissue_or_cell=(
            "Gastric epithelial cells",
        ),
        mode_of_action=(
            "Inject CagA -> tyrosine-phosphorylated by host "
            "Src/Abl kinases -> binds SHP2 phosphatase + "
            "perturbs MAPK + Wnt signalling -> chronic "
            "inflammation + epithelial proliferation",
        ),
        clinical_syndrome=(
            "Chronic gastritis, peptic ulcer, gastric "
            "adenocarcinoma, MALT lymphoma (H. pylori is a "
            "WHO Group-1 carcinogen)",
        ),
        vaccine_or_antitoxin=(
            "H. pylori vaccines under development; "
            "eradication therapy uses combination antibiotics "
            "+ PPI",
        ),
        cross_reference_microbe_ids=(
            "helicobacter-pylori",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "wnt-beta-catenin",
        ),
        notes=(
            "CagA was the first bacterial 'oncoprotein' -- "
            "directly injected into a host cell to drive "
            "neoplastic transformation."),
    ),
    VirulenceFactor(
        id="t6ss",
        name="Type-VI secretion system (T6SS)",
        mechanism_class="secretion-system",
        structural_notes=(
            "Bacterial contractile injection apparatus -- "
            "evolutionarily related to T4 phage tail.  Sheath "
            "contracts to fire an inner tube tipped with "
            "effector + VgrG/PAAR spike into target cells.",
        ),
        target_tissue_or_cell=(
            "Other bacteria (interbacterial competition)",
            "Eukaryotic cells (some pathogens -- "
            "Vibrio cholerae, Pseudomonas aeruginosa)",
        ),
        mode_of_action=(
            "Effectors include muramidases + amidases + "
            "nucleases + pore-formers; inject into rivals "
            "-> kill or disable",
        ),
        clinical_syndrome=(
            "Indirect: shapes microbiome composition + "
            "drives intra-host competition",
        ),
        vaccine_or_antitoxin=(),
        cross_reference_microbe_ids=(
            "pseudomonas-aeruginosa",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "T6SS is the molecular weapon of bacterial "
            "warfare -- used by ~ 25 % of Gram-negatives to "
            "kill competitors directly."),
    ),

    # ============================================================
    # Immune-evasion factors (3)
    # ============================================================
    VirulenceFactor(
        id="iga-protease",
        name="IgA1 protease",
        mechanism_class="immune-evasion",
        structural_notes=(
            "Serine protease (some) or zinc metallo"
            "protease (other) family.  Convergent evolution "
            "in S. pneumoniae, H. influenzae, N. meningitidis, "
            "N. gonorrhoeae.",
        ),
        target_tissue_or_cell=(
            "Mucosal surfaces (respiratory + genital "
            "tracts)",
        ),
        mode_of_action=(
            "Cleaves human IgA1 in the hinge region -> "
            "inactivates secretory IgA -> bacterium can "
            "colonise mucosal surfaces despite specific "
            "antibody response",
        ),
        clinical_syndrome=(
            "Required for mucosal colonisation by all four "
            "producing pathogens -> contributes to "
            "respiratory + meningococcal + gonorrhoeal "
            "infections",
        ),
        vaccine_or_antitoxin=(),
        cross_reference_microbe_ids=(
            "streptococcus-pneumoniae",
            "neisseria-meningitidis",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Convergent evolution of IgA1-specificity in 4 "
            "unrelated pathogens proves IgA1 is the "
            "limiting host defence at mucosal surfaces."),
    ),
    VirulenceFactor(
        id="protein-a",
        name="Staphylococcal protein A (SpA)",
        mechanism_class="immune-evasion",
        structural_notes=(
            "Cell-wall-anchored 5-domain protein.  Each "
            "domain binds the Fc region of IgG (IgG1/2/4 "
            "but not IgG3).  Also binds the Fab variable "
            "regions of VH3-family antibodies as a B-cell "
            "superantigen.",
        ),
        target_tissue_or_cell=(
            "Host IgG + B lymphocytes",
        ),
        mode_of_action=(
            "Coats bacterial surface with IgG bound 'wrong-"
            "way-around' (Fc-out) -> blocks Fc-receptor-"
            "mediated phagocytosis + complement activation; "
            "also crosslinks B-cell receptors -> apoptosis "
            "of VH3+ B cells",
        ),
        clinical_syndrome=(
            "Required for full S. aureus virulence in "
            "bacteraemia + skin + soft-tissue + endocarditis",
        ),
        vaccine_or_antitoxin=(
            "Mutant non-Ig-binding SpA in trials as a "
            "vaccine antigen + as a B-cell tolerance "
            "research tool",
        ),
        cross_reference_microbe_ids=(
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "SpA is the workhorse affinity ligand for "
            "purifying IgG (Protein-A Sepharose) -- the "
            "same property that makes it virulent makes it "
            "indispensable for biotech."),
    ),
    VirulenceFactor(
        id="opa-antigenic-variation",
        name="Neisseria Opa + pilin antigenic variation",
        mechanism_class="immune-evasion",
        structural_notes=(
            "Multiple silent gene cassettes recombine into "
            "the expression locus -> continuous shuffling "
            "of surface-exposed Opa proteins + pilin "
            "subunits.  Phase variation via slipped-strand "
            "mispairing in poly-G tracts.",
        ),
        target_tissue_or_cell=(
            "CD66 family receptors on epithelial + immune "
            "cells",
        ),
        mode_of_action=(
            "Antibody to one Opa variant doesn't cross-"
            "protect against the next variant -> chronic + "
            "recurrent infection possible despite host "
            "immune response",
        ),
        clinical_syndrome=(
            "Gonorrhoea + meningococcal disease; explains "
            "lack of vaccine for N. gonorrhoeae despite "
            "100+ years of effort",
        ),
        vaccine_or_antitoxin=(
            "Bexsero (4CMenB) + MenACWY conjugate vaccines "
            "for meningococcal disease; no licensed "
            "gonorrhoea vaccine",
        ),
        cross_reference_microbe_ids=(
            "neisseria-meningitidis",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Antigenic variation in Neisseria is the "
            "textbook example of bacterial diversity-"
            "generation as immune-evasion strategy."),
    ),

    # ============================================================
    # Biofilm (1)
    # ============================================================
    VirulenceFactor(
        id="biofilm-eps-quorum-sensing",
        name="Biofilm EPS + quorum sensing",
        mechanism_class="biofilm",
        structural_notes=(
            "Extracellular polymeric substance (EPS) matrix "
            "of polysaccharides + proteins + extracellular "
            "DNA.  Quorum-sensing systems: LuxR/LuxI in "
            "Vibrio fischeri; AHL (acyl-homoserine-lactone) "
            "based in Pseudomonas; staphylococcal agr uses "
            "auto-inducing peptides (AIPs).",
        ),
        target_tissue_or_cell=(
            "Implanted medical devices (catheters, "
            "prostheses, heart valves)",
            "Cystic-fibrosis lung, chronic wounds, otitis "
            "media, dental plaque",
        ),
        mode_of_action=(
            "EPS matrix shields bacteria from antibiotics "
            "(diffusion + persister-cell formation) + from "
            "host immune effectors.  Quorum sensing "
            "synchronises virulence-gene expression at high "
            "cell density",
        ),
        clinical_syndrome=(
            "Recurrent + chronic infections of indwelling "
            "devices + colonised mucosal sites; refractory "
            "to even appropriate antibiotic therapy",
        ),
        vaccine_or_antitoxin=(
            "Quorum-sensing inhibitors (QSIs) + biofilm-"
            "dispersing agents in development; "
            "anti-PsiAB antibodies for Pseudomonas",
        ),
        cross_reference_microbe_ids=(
            "pseudomonas-aeruginosa",
            "staphylococcus-aureus",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(),
        notes=(
            "Biofilm-mediated antibiotic tolerance is the "
            "leading mechanism of treatment failure in "
            "cystic-fibrosis Pseudomonas + foreign-body "
            "infections."),
    ),

    # ============================================================
    # Endotoxin (1)
    # ============================================================
    VirulenceFactor(
        id="lps-endotoxin",
        name="LPS / lipid A (endotoxin)",
        mechanism_class="endotoxin",
        structural_notes=(
            "Outer leaflet of Gram-negative outer membrane.  "
            "Three regions: lipid A (membrane anchor + the "
            "toxic moiety), core oligosaccharide, O-antigen "
            "polysaccharide.  Released on bacterial lysis "
            "(antibiotic-induced lysis can paradoxically "
            "exacerbate sepsis).",
        ),
        target_tissue_or_cell=(
            "Macrophages + monocytes + endothelium",
        ),
        mode_of_action=(
            "Lipid A binds CD14 + TLR4-MD2 on host cells "
            "-> NF-kappaB + IRF3 activation -> massive "
            "TNF-alpha + IL-1beta + IL-6 release -> "
            "septic-shock cascade",
        ),
        clinical_syndrome=(
            "Gram-negative sepsis: fever, hypotension, "
            "DIC, multi-organ dysfunction",
        ),
        vaccine_or_antitoxin=(
            "Anti-LPS antibodies (HA-1A, E5) failed in "
            "phase-3 sepsis trials; lipid-A-binding "
            "polymyxins (polymyxin B + colistin) remain "
            "last-line antibiotics for MDR Gram-negatives",
            "LAL endotoxin assay (from Limulus polyphemus -- "
            "see AB-1.0 catalogue) is the gold standard for "
            "endotoxin detection in injectables",
        ),
        cross_reference_microbe_ids=(
            "escherichia-coli", "klebsiella-pneumoniae",
            "pseudomonas-aeruginosa",
            "neisseria-meningitidis", "salmonella-typhi",
            "helicobacter-pylori",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_signaling_pathway_ids=(
            "tlr", "nf-kb", "pyroptosis",
        ),
        notes=(
            "LPS is the molecular trigger of meningococcal "
            "purpura fulminans -- the rapidly-evolving "
            "petechial rash that's the visible signature of "
            "fulminant meningococcal sepsis."),
    ),
)
