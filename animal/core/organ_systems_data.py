"""Phase AB-2.0 (round 223) — animal organ-systems catalogue.

Each entry carries 4-way typed cross-references to:
- ``orgchem.db.Molecule`` rows by exact name (system-relevant
  hormones, neurotransmitters, metabolites).
- ``cellbio.core.cell_signaling`` ids (CB-1.0 pathways).
- ``biochem.core.enzymes`` ids (BC-1.0 enzymes).
- ``animal.core.taxa`` ids (AB-1.0 animal-taxa where the
  system is the canonical model).

This is the FINAL deep-phase catalogue (round 223 of the
-2 chain).  All cross-reference ids verified at write time.
"""
from __future__ import annotations
from typing import Tuple

from animal.core.organ_systems import OrganSystem


ORGAN_SYSTEMS: Tuple[OrganSystem, ...] = (
    # ============================================================
    # Cardiovascular (1) — closed-loop pump + circulation
    # ============================================================
    OrganSystem(
        id="cardiovascular-mammalian",
        name="Cardiovascular system (mammalian)",
        system_category="cardiovascular",
        short_summary=(
            "Closed-loop circulatory system: a 4-chambered "
            "heart pumps blood through arteries -> arterioles "
            "-> capillaries (gas + solute exchange) -> venules "
            "-> veins -> right atrium.  Pulmonary + systemic "
            "circuits in series; each cardiac cycle ~ 0.8 s "
            "at rest."),
        representative_organs=(
            "Heart (4 chambers + 4 valves + AV + SA nodes)",
            "Aorta + arteries + arterioles",
            "Capillary beds (~ 10 micrometre diameter)",
            "Venules + veins (with valves)",
        ),
        key_cell_types=(
            "Cardiomyocytes (working + pacemaker SA/AV nodal)",
            "Vascular smooth-muscle cells",
            "Endothelial cells (NO + endothelin secretion)",
            "Erythrocytes + leukocytes + platelets",
        ),
        functional_anatomy=(
            "SA node -> AV node -> bundle of His -> Purkinje "
            "fibres conduction system",
            "Frank-Starling mechanism: stroke volume scales "
            "with end-diastolic volume",
            "Baroreflex: carotid + aortic baroreceptors -> "
            "brainstem nucleus tractus solitarius -> autonomic "
            "BP control",
        ),
        evolutionary_origin=(
            "Three-chambered hearts in amphibians + most "
            "reptiles; four-chambered hearts evolved "
            "independently in crocodilians + birds + mammals "
            "to fully separate pulmonary + systemic circuits",
        ),
        characteristic_disorders=(
            "Coronary artery disease (atherosclerosis)",
            "Heart failure (HFrEF + HFpEF)",
            "Atrial fibrillation + other arrhythmias",
            "Hypertension (the primary cardiovascular risk "
            "factor)",
            "Valvular heart disease",
        ),
        cross_reference_molecule_names=(
            "Cholesterol",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka", "gpcr-ip3-ca",
        ),
        cross_reference_enzyme_ids=(
            "ace", "atp-synthase", "na-k-atpase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
            "rattus-norvegicus", "canis-lupus-familiaris",
            "bos-taurus",
        ),
        notes=(
            "ACE inhibitors + beta-blockers + statins drove "
            "the second-half-of-the-20th-century decline in "
            "cardiovascular mortality (~ 50 % reduction in "
            "age-adjusted CV death from 1950 to 2020 in the "
            "developed world)."),
    ),
    OrganSystem(
        id="respiratory-mammalian",
        name="Respiratory system (mammalian)",
        system_category="respiratory",
        short_summary=(
            "Air-conducting + gas-exchange architecture: "
            "nose / pharynx / larynx -> trachea -> bronchi -> "
            "bronchioles -> alveoli (~ 500 million per adult "
            "lung, ~ 70 m^2 surface area).  Diaphragm + "
            "intercostals drive ventilation."),
        representative_organs=(
            "Lungs (alveoli + bronchial tree)",
            "Diaphragm + intercostal muscles",
            "Trachea + larynx + pharynx",
        ),
        key_cell_types=(
            "Type-I alveolar pneumocytes (gas-exchange "
            "surface)",
            "Type-II alveolar pneumocytes (surfactant-"
            "producing)",
            "Ciliated columnar epithelium + goblet cells "
            "(mucociliary escalator)",
            "Alveolar macrophages",
        ),
        functional_anatomy=(
            "Tidal volume ~ 500 mL; vital capacity ~ 4-5 L; "
            "respiratory rate ~ 12-20 / min at rest",
            "Carbonic anhydrase II in erythrocytes + lung "
            "endothelium drives CO2 transport via the "
            "bicarbonate buffer + chloride shift",
            "Boyle's law: diaphragm contraction -> increased "
            "thoracic volume -> decreased intra-pleural "
            "pressure -> air inflow",
        ),
        evolutionary_origin=(
            "Lungs evolved from primitive vertebrate gas-"
            "filled swim bladders / pharyngeal pouches.  "
            "Avian respiratory system (parabronchi + air "
            "sacs) is unique among vertebrates -- "
            "unidirectional air flow + 9 air sacs + no "
            "alveoli",
        ),
        characteristic_disorders=(
            "Asthma + COPD",
            "Pneumonia (bacterial / viral / fungal)",
            "Pulmonary fibrosis (incl. IPF)",
            "Lung cancer (NSCLC + SCLC)",
            "Acute respiratory distress syndrome (ARDS)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka", "tlr",
        ),
        cross_reference_enzyme_ids=(
            "carbonic-anhydrase-ii",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
            "gallus-gallus",
        ),
        notes=(
            "Surfactant (DPPC + SP-A/B/C/D) lowers alveolar "
            "surface tension + prevents collapse on "
            "expiration -- the molecular basis of neonatal "
            "respiratory distress in premature infants who "
            "haven't yet started surfactant production."),
    ),
    OrganSystem(
        id="digestive-mammalian",
        name="Digestive system (mammalian)",
        system_category="digestive",
        short_summary=(
            "GI tract from oral cavity to anus + accessory "
            "organs (liver, pancreas, gallbladder, salivary "
            "glands).  ~ 9 m total in human adults; "
            "specialised regions for mechanical + enzymatic "
            "digestion + nutrient absorption."),
        representative_organs=(
            "Stomach (HCl-secreting parietal cells + pepsin)",
            "Small intestine (duodenum, jejunum, ileum -- "
            "the absorptive surface, ~ 250 m^2 with villi + "
            "microvilli)",
            "Large intestine + microbiome (~ 10^14 bacteria)",
            "Liver (the body's metabolic + detoxification "
            "centre)",
            "Pancreas (exocrine: digestive enzymes + "
            "bicarbonate; endocrine: insulin + glucagon)",
        ),
        key_cell_types=(
            "Enterocytes (apical brush border + nutrient "
            "transporters)",
            "Goblet cells (mucin secretion)",
            "Paneth cells (antimicrobial peptides at the "
            "crypt base)",
            "Hepatocytes (the liver's parenchymal cell)",
            "Pancreatic acinar cells (zymogen secretion)",
        ),
        functional_anatomy=(
            "Pancreatic zymogens (trypsinogen, chymotrypsino"
            "gen, etc.) activated in duodenal lumen by "
            "enteropeptidase + autocatalysis",
            "Bile acids (primary + secondary) emulsify "
            "lipids; cholic + taurocholic + glycocholic acid "
            "are the major species",
            "Liver is the only organ that can simultaneously "
            "sit in both the systemic + portal circulations",
        ),
        evolutionary_origin=(
            "Coelomate gut tube evolved from sponge water "
            "channels + cnidarian gastrovascular cavity.  "
            "Complete one-way gut + accessory organs are the "
            "bilaterian innovation",
        ),
        characteristic_disorders=(
            "Inflammatory bowel disease (Crohn's + UC)",
            "Coeliac disease",
            "Colorectal cancer",
            "Cirrhosis (alcoholic, viral, MASH/NASH)",
            "Type-2 diabetes (pancreatic beta-cell + insulin "
            "resistance)",
        ),
        cross_reference_molecule_names=(
            "Cholic acid", "Lactose", "Acetyl-CoA",
        ),
        cross_reference_signaling_pathway_ids=(
            "insulin", "wnt-beta-catenin",
        ),
        cross_reference_enzyme_ids=(
            "chymotrypsin", "trypsin", "cyp3a4",
            "alcohol-dehydrogenase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus", "bos-taurus",
        ),
        notes=(
            "CYP3A4 in hepatocyte + intestinal-enterocyte "
            "smooth ER metabolises ~ 50 % of clinical drugs "
            "-- the dominant first-pass + drug-drug "
            "interaction enzyme."),
    ),
    OrganSystem(
        id="urinary-mammalian",
        name="Urinary system (mammalian)",
        system_category="urinary",
        short_summary=(
            "Kidneys filter ~ 180 L plasma per day in human "
            "adults via ~ 2 million glomeruli; reabsorb ~ 99 "
            "% of the filtrate to produce ~ 1.5 L of urine "
            "carrying nitrogenous waste + excess solutes."),
        representative_organs=(
            "Kidneys (cortex + medulla; ~ 1 million nephrons "
            "per kidney)",
            "Ureters",
            "Urinary bladder + urethra",
        ),
        key_cell_types=(
            "Glomerular podocytes (filtration barrier with "
            "endothelium + GBM)",
            "Proximal tubule cells (bulk reabsorption)",
            "Loop of Henle thick-ascending limb "
            "(countercurrent multiplier)",
            "Principal + intercalated cells of the collecting "
            "duct (ADH-mediated water reabsorption + acid-"
            "base balance)",
        ),
        functional_anatomy=(
            "Three filtration steps: filtration (glomerulus) "
            "+ reabsorption (tubule) + secretion (tubule) -> "
            "urine",
            "Renin-angiotensin-aldosterone system (RAAS) "
            "regulates blood pressure + Na+/K+ balance",
            "ADH (vasopressin) from posterior pituitary "
            "drives collecting-duct aquaporin-2 insertion",
        ),
        evolutionary_origin=(
            "Vertebrate kidney evolved from segmental "
            "nephrotomes; mammalian metanephric kidney is "
            "the most-derived form with the loop of Henle "
            "enabling concentrated urine (independently "
            "evolved in birds with shorter loops)",
        ),
        characteristic_disorders=(
            "Chronic kidney disease (diabetic + hypertensive "
            "nephropathy)",
            "Acute kidney injury",
            "Nephrolithiasis (kidney stones)",
            "Glomerulonephritis (post-streptococcal, IgA, "
            "lupus)",
            "Polycystic kidney disease",
        ),
        cross_reference_molecule_names=(
            "Urea",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        cross_reference_enzyme_ids=(
            "ace", "carbonic-anhydrase-ii", "na-k-atpase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
            "rattus-norvegicus",
        ),
        notes=(
            "SGLT2 inhibitors (gliflozins) work in the "
            "proximal tubule + cause renal-protective + CV-"
            "protective effects beyond simple glycaemic "
            "control -- one of the biggest practice changes "
            "in CKD + heart-failure care of the 2020s."),
    ),

    OrganSystem(
        id="nervous-mammalian",
        name="Nervous system (mammalian)",
        system_category="nervous",
        short_summary=(
            "CNS (brain + spinal cord) + PNS (somatic + "
            "autonomic divisions; autonomic = sympathetic + "
            "parasympathetic + enteric).  ~ 86 billion "
            "neurons in the human brain + comparable glia.  "
            "Action-potential conduction + chemical-synapse "
            "transmission."),
        representative_organs=(
            "Brain (cerebrum + cerebellum + brainstem)",
            "Spinal cord",
            "Peripheral nerves + ganglia",
            "Sense organs (eye, ear, olfactory + gustatory)",
        ),
        key_cell_types=(
            "Neurons (excitatory pyramidal + inhibitory "
            "interneurons + motor + sensory)",
            "Astrocytes (synaptic + metabolic support)",
            "Oligodendrocytes (CNS myelination) + Schwann "
            "cells (PNS myelination)",
            "Microglia (resident immune + synaptic pruning)",
        ),
        functional_anatomy=(
            "Action potential: Nav1.x channels open -> Na+ "
            "influx -> Kv channels open -> K+ efflux -> "
            "repolarisation (Hodgkin-Huxley 1952)",
            "Chemical synapse: vesicular release -> "
            "neurotransmitter binds postsynaptic receptors -> "
            "ionic + metabotropic responses",
            "NMDA-receptor-mediated long-term potentiation -> "
            "associative learning + memory storage",
        ),
        evolutionary_origin=(
            "Cnidarian nerve net -> bilaterian centralisation "
            "-> vertebrate / cephalopod brain evolution.  The "
            "octopus + squid brain (~ 500 M neurons in Octopus "
            "vulgaris) is the most-complex invertebrate "
            "nervous system",
        ),
        characteristic_disorders=(
            "Stroke (the dominant cause of CNS disability)",
            "Alzheimer's disease + other dementias",
            "Parkinson's disease",
            "Multiple sclerosis (autoimmune demyelination)",
            "Epilepsy",
            "Major depressive disorder",
        ),
        cross_reference_molecule_names=(
            "Dopamine", "L-DOPA (levodopa)",
            "Glycine", "L-Glutamic acid",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka", "gpcr-ip3-ca", "camkii",
        ),
        cross_reference_enzyme_ids=(
            "comt", "pka", "adenylate-cyclase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus", "loligo-pealeii",
            "aplysia-californica",
        ),
        notes=(
            "Levodopa is the gold-standard Parkinson's "
            "treatment + the textbook example of a CNS pro-"
            "drug -- crosses the BBB then is decarboxylated "
            "to dopamine in striatal neurons (peripheral "
            "decarboxylase inhibitor carbidopa co-administered "
            "to spare dopamine for the brain)."),
    ),
    OrganSystem(
        id="endocrine-mammalian",
        name="Endocrine system (mammalian)",
        system_category="endocrine",
        short_summary=(
            "Network of ductless glands secreting hormones "
            "into the bloodstream for distant target-cell "
            "signalling.  Hierarchical: hypothalamus -> "
            "anterior pituitary -> peripheral target glands "
            "(thyroid, adrenal cortex, gonads); plus "
            "autonomous islands (pancreatic islets, parathyroid, "
            "pineal, adrenal medulla)."),
        representative_organs=(
            "Pituitary gland (anterior + posterior lobes)",
            "Thyroid + parathyroids",
            "Adrenal cortex (mineralocorticoids, "
            "glucocorticoids, androgens) + medulla "
            "(catecholamines)",
            "Pancreatic islets (alpha = glucagon, beta = "
            "insulin, delta = somatostatin)",
            "Gonads (testes, ovaries) + corpus luteum",
            "Pineal gland (melatonin)",
        ),
        key_cell_types=(
            "Anterior-pituitary somatotrophs / corticotrophs / "
            "thyrotrophs / lactotrophs / gonadotrophs",
            "Thyroid follicular cells",
            "Adrenocortical cells (zona glomerulosa + "
            "fasciculata + reticularis)",
            "Pancreatic beta cells (insulin secretion)",
        ),
        functional_anatomy=(
            "Negative-feedback loops: cortisol suppresses "
            "ACTH; thyroid hormone suppresses TSH",
            "Glucose-stimulated insulin release: high "
            "glucose -> glycolysis -> ATP rise -> KATP "
            "channel closes -> depolarisation -> voltage-"
            "gated Ca2+ -> insulin granule exocytosis",
        ),
        evolutionary_origin=(
            "Pituitary derives from Rathke's pouch + "
            "infundibulum embryonically; its anterior + "
            "posterior lobes have distinct developmental + "
            "functional origins.  Endocrine signalling is "
            "ancient -- jellyfish + worms have hormone-like "
            "peptide signals",
        ),
        characteristic_disorders=(
            "Type-1 + type-2 diabetes mellitus",
            "Hypo- + hyperthyroidism",
            "Cushing's + Addison's syndromes",
            "Acromegaly + dwarfism",
            "PCOS + reproductive endocrinopathies",
        ),
        cross_reference_molecule_names=(
            "Cortisol", "Estradiol", "Testosterone",
            "Progesterone", "Vitamin D3 (cholecalciferol)",
        ),
        cross_reference_signaling_pathway_ids=(
            "insulin", "gpcr-camp-pka", "jak-stat",
        ),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "GLP-1 + dual GIP/GLP-1 receptor agonists "
            "(semaglutide, tirzepatide) reshaped the "
            "endocrine + metabolic-disease therapeutic "
            "landscape from 2017 onward -- weight loss + "
            "CV + renal benefit + Alzheimer's + addiction "
            "trials all running."),
    ),
    OrganSystem(
        id="immune-mammalian",
        name="Immune system (mammalian)",
        system_category="immune",
        short_summary=(
            "Innate (rapid + non-specific) + adaptive (slow + "
            "antigen-specific + memory) arms.  Distributed "
            "across primary lymphoid organs (bone marrow + "
            "thymus) + secondary lymphoid organs (lymph nodes, "
            "spleen, MALT)."),
        representative_organs=(
            "Bone marrow (haematopoiesis + B-cell maturation)",
            "Thymus (T-cell selection + maturation)",
            "Spleen (blood-filtering immune organ)",
            "Lymph nodes + lymphatic vessels",
            "Mucosa-associated lymphoid tissue (GALT, BALT, "
            "NALT)",
        ),
        key_cell_types=(
            "Macrophages + dendritic cells (innate + antigen-"
            "presenting)",
            "Neutrophils (acute infection)",
            "B lymphocytes (antibody production)",
            "T lymphocytes (CD4+ helper, CD8+ cytotoxic, "
            "regulatory)",
            "Natural-killer cells (innate cytotoxicity)",
        ),
        functional_anatomy=(
            "Pattern recognition: TLRs + NLRs + RLRs + "
            "cGAS-STING detect microbial PAMPs + host DAMPs",
            "Adaptive memory: clonal selection + somatic "
            "hypermutation + class switching in germinal "
            "centres",
            "Tolerance: thymic negative selection + "
            "peripheral Tregs prevent autoimmunity",
        ),
        evolutionary_origin=(
            "Innate immunity is ancient (TLR signalling found "
            "in flies + cnidarians + sponges).  Adaptive "
            "immunity (RAG-mediated V(D)J recombination of "
            "Ig + TCR loci) is a vertebrate innovation",
        ),
        characteristic_disorders=(
            "Autoimmune disease (RA, SLE, T1DM, MS, IBD)",
            "Primary immunodeficiencies (SCID, CVID, CGD)",
            "HIV / AIDS",
            "Allergic disease + asthma",
            "Sepsis (cytokine storm)",
        ),
        cross_reference_molecule_names=(
            "Cortisol",
        ),
        cross_reference_signaling_pathway_ids=(
            "tlr", "tcr", "nf-kb", "jak-stat",
            "cgas-sting", "intrinsic-apoptosis",
            "tnf-extrinsic-apoptosis", "pyroptosis",
        ),
        cross_reference_enzyme_ids=(
            "lysozyme", "caspase-3",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "Immune-checkpoint inhibitors (anti-CTLA-4 + "
            "anti-PD-1 / anti-PD-L1) won the 2018 Nobel "
            "(Allison + Honjo) + transformed oncology -- "
            "first time the immune system was unleashed "
            "rather than suppressed for therapy."),
    ),
    OrganSystem(
        id="musculoskeletal-mammalian",
        name="Musculoskeletal system (mammalian)",
        system_category="musculoskeletal",
        short_summary=(
            "~ 206 bones + ~ 600 skeletal muscles + their "
            "connective tissues (cartilage, tendons, "
            "ligaments) form the body's structural framework "
            "+ generate movement.  Skeletal muscle is ~ 40 % "
            "of adult body mass."),
        representative_organs=(
            "Bones + joints",
            "Skeletal muscle (striated, voluntary)",
            "Tendons (muscle -> bone) + ligaments (bone -> "
            "bone)",
            "Articular cartilage (hyaline)",
        ),
        key_cell_types=(
            "Osteoblasts + osteocytes + osteoclasts (bone "
            "remodelling)",
            "Chondrocytes (cartilage)",
            "Skeletal-muscle fibres (Type I slow oxidative + "
            "Type II fast glycolytic)",
            "Satellite cells (muscle stem cells)",
            "Tenocytes + fibroblasts (tendon + ligament)",
        ),
        functional_anatomy=(
            "Sliding-filament mechanism: actin + myosin "
            "thin/thick filaments; Ca2+ release from SR "
            "triggers troponin/tropomyosin shift -> myosin "
            "head binds actin -> ATP-driven cross-bridge "
            "cycling",
            "Bone is constantly remodelled (~ 10 % per year): "
            "RANK / RANKL / OPG axis controls osteoclast "
            "activity",
        ),
        evolutionary_origin=(
            "Vertebrate endoskeleton derived from neural-"
            "crest + mesodermal precursors.  Mineralised "
            "bone first appeared in jawless ostracoderm fish "
            "(~ 500 Mya).  Insect exoskeleton is convergent "
            "with vertebrate endoskeleton in functional role "
            "but distinct embryonic origin",
        ),
        characteristic_disorders=(
            "Osteoporosis + fragility fractures",
            "Osteoarthritis",
            "Rheumatoid arthritis",
            "Muscular dystrophies (Duchenne, Becker)",
            "Sarcopenia (age-related muscle loss)",
        ),
        cross_reference_molecule_names=(
            "Vitamin D3 (cholecalciferol)",
        ),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "tgf-beta-smad",
        ),
        cross_reference_enzyme_ids=(
            "atp-synthase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "Wnt/beta-catenin signalling is critical for bone "
            "mass -- LRP5 gain-of-function -> high bone mass; "
            "loss-of-function -> osteoporosis-pseudoglioma.  "
            "Sclerostin (SOST) is the key Wnt antagonist -- "
            "anti-sclerostin mAb romosozumab boosts bone "
            "formation in osteoporosis."),
    ),
    OrganSystem(
        id="integumentary-mammalian",
        name="Integumentary system (mammalian)",
        system_category="integumentary",
        short_summary=(
            "The body's largest organ (~ 2 m^2 + ~ 4 kg in "
            "adults).  Three layers: epidermis (stratified "
            "squamous epithelium), dermis (collagen + elastin "
            "+ vasculature + nerves), hypodermis (adipose).  "
            "Plus accessory structures: hair follicles, nails, "
            "sebaceous + sweat + mammary glands."),
        representative_organs=(
            "Skin (epidermis + dermis + hypodermis)",
            "Hair + nails",
            "Sebaceous + eccrine + apocrine sweat glands",
            "Mammary glands (specialised in females)",
        ),
        key_cell_types=(
            "Keratinocytes (the bulk of the epidermis)",
            "Melanocytes (pigmentation)",
            "Langerhans cells (epidermal dendritic cells)",
            "Merkel cells (mechanoreceptors)",
            "Fibroblasts + adipocytes (dermis + hypodermis)",
        ),
        functional_anatomy=(
            "Barrier: stratum corneum cornified envelope + "
            "lipid lamellae prevent water loss + microbial "
            "ingress",
            "Thermoregulation: vasodilation / vasoconstriction "
            "+ eccrine sweating (latent heat of evaporation)",
            "Vitamin D3 photosynthesis: 7-dehydrocholesterol "
            "+ UVB -> previtamin D3 -> vitamin D3",
        ),
        evolutionary_origin=(
            "Vertebrate skin evolved from the ectodermal "
            "outer layer.  Hair is a synapsid (mammalian-"
            "lineage) innovation; feathers an archosaur "
            "(theropod -> bird) innovation.  Mammary glands "
            "derive from sweat glands",
        ),
        characteristic_disorders=(
            "Skin cancer (basal cell, squamous cell, melanoma)",
            "Psoriasis + atopic dermatitis (eczema)",
            "Acne vulgaris",
            "Alopecia (androgenetic + autoimmune)",
        ),
        cross_reference_molecule_names=(
            "Vitamin D3 (cholecalciferol)", "Cholesterol",
        ),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "hedgehog", "notch",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "Hedgehog signalling drives basal-cell carcinoma "
            "tumorigenesis (PTCH1 + SMO mutations) -- "
            "vismodegib + sonidegib are SMO inhibitors "
            "approved for advanced BCC."),
    ),
    OrganSystem(
        id="reproductive-female-mammalian",
        name="Female reproductive system (mammalian)",
        system_category="reproductive-female",
        short_summary=(
            "Ovaries (oogenesis + steroid-hormone "
            "production), uterine (Fallopian) tubes "
            "(fertilisation site), uterus (implantation + "
            "gestation), cervix + vagina, breast (mammary "
            "gland for postnatal nutrition).  Hypothalamic-"
            "pituitary-ovarian axis drives the ~ 28-day "
            "menstrual cycle."),
        representative_organs=(
            "Ovaries",
            "Fallopian (uterine) tubes",
            "Uterus",
            "Cervix + vagina",
            "Breast (mammary gland)",
        ),
        key_cell_types=(
            "Oocytes + granulosa cells + theca cells "
            "(ovarian follicle)",
            "Endometrial epithelial + stromal cells",
            "Decidual cells (gestational endometrium)",
            "Lactational alveolar epithelial cells "
            "(mammary)",
        ),
        functional_anatomy=(
            "Menstrual cycle: follicular -> ovulation -> "
            "luteal phase, controlled by LH / FSH + estrogen "
            "/ progesterone feedback",
            "Female meiosis is arrested at prophase I from "
            "fetal life until ovulation -- decades of "
            "diplotene rest before metaphase II completion",
        ),
        evolutionary_origin=(
            "Mammalian viviparity + placentation evolved "
            "from amniote-egg ancestry.  Eutherian "
            "(placental) vs metatherian (marsupial) vs "
            "prototherian (monotreme egg-laying) "
            "reproductive strategies",
        ),
        characteristic_disorders=(
            "Polycystic ovary syndrome (PCOS)",
            "Endometriosis",
            "Cervical + endometrial + ovarian cancers",
            "Breast cancer (BRCA1/2 + ER/PR/HER2 subtyping)",
        ),
        cross_reference_molecule_names=(
            "Estradiol", "Progesterone",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "ER-positive breast cancer (~ 70 % of cases) is "
            "the leading driver of endocrine therapy in "
            "oncology -- tamoxifen + aromatase inhibitors + "
            "fulvestrant + CDK4/6 inhibitors transformed "
            "outcomes from the 1980s onward."),
    ),
    OrganSystem(
        id="reproductive-male-mammalian",
        name="Male reproductive system (mammalian)",
        system_category="reproductive-male",
        short_summary=(
            "Testes (continuous spermatogenesis + "
            "testosterone production), epididymis (sperm "
            "maturation + storage), vas deferens, seminal "
            "vesicles + prostate + bulbourethral glands "
            "(seminal-fluid contributions), penis "
            "(intromission)."),
        representative_organs=(
            "Testes",
            "Epididymis",
            "Vas deferens + seminal vesicles + prostate + "
            "bulbourethral glands",
            "Penis",
        ),
        key_cell_types=(
            "Spermatogonial stem cells -> spermatocytes "
            "(meiosis) -> spermatids -> spermatozoa",
            "Sertoli cells (spermatogenesis support + "
            "blood-testis barrier)",
            "Leydig cells (testosterone production)",
            "Prostate epithelial cells",
        ),
        functional_anatomy=(
            "Spermatogenesis is continuous (~ 75 days per "
            "wave; ~ 100 million sperm produced daily)",
            "5alpha-reductase converts testosterone to "
            "dihydrotestosterone (DHT, ~ 10x AR-affinity) -- "
            "the prostate-active androgen",
        ),
        evolutionary_origin=(
            "Internal fertilisation + descended testes are "
            "the mammalian pattern.  Sperm competition + "
            "post-copulatory sexual selection has shaped "
            "testis size + sperm morphology across mammals "
            "(largest testes per body mass: chimpanzees + "
            "right whales)",
        ),
        characteristic_disorders=(
            "Benign prostatic hyperplasia + prostate cancer",
            "Testicular cancer (germ-cell tumours)",
            "Erectile dysfunction (organic + psychogenic)",
            "Male infertility (azoospermia, "
            "oligoasthenoteratospermia)",
        ),
        cross_reference_molecule_names=(
            "Testosterone", "Cholesterol",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "PDE5 inhibitors (sildenafil + tadalafil + "
            "vardenafil) for erectile dysfunction were "
            "originally developed for angina (sildenafil's "
            "Pfizer phase-2 trials) -- one of the most "
            "famous accidental indications in pharmacology."),
    ),
    OrganSystem(
        id="lymphatic-mammalian",
        name="Lymphatic system (mammalian)",
        system_category="lymphatic",
        short_summary=(
            "Network of lymphatic capillaries -> collecting "
            "vessels -> trunks -> ducts (thoracic + right "
            "lymphatic) emptying into the subclavian veins.  "
            "Returns ~ 3 L of interstitial fluid + protein to "
            "the bloodstream daily; carries lymphocytes + "
            "antigens to lymph nodes; transports dietary "
            "lipids via intestinal lacteals."),
        representative_organs=(
            "Lymphatic capillaries + collecting vessels",
            "Lymph nodes",
            "Thoracic duct + right lymphatic duct",
            "Spleen + tonsils + GALT (overlaps with immune "
            "system)",
        ),
        key_cell_types=(
            "Lymphatic endothelial cells (LECs)",
            "Resident lymph-node fibroblastic reticular "
            "cells (FRCs)",
            "Trafficking T + B lymphocytes + dendritic cells",
        ),
        functional_anatomy=(
            "Lymph nodes filter incoming lymph + present "
            "antigen to recirculating lymphocytes -> "
            "germinal-centre reactions on antigen exposure",
            "Intestinal lacteals carry chylomicrons (dietary "
            "triglyceride + cholesterol) into systemic "
            "circulation via the thoracic duct",
        ),
        evolutionary_origin=(
            "Discovered in the 17th C (Asellius 1622, the "
            "intestinal lacteals) -- the last major organ "
            "system identified anatomically.  Lymphangiogenic "
            "VEGFR-3 + Prox1 are the master molecular "
            "regulators",
        ),
        characteristic_disorders=(
            "Lymphoedema (primary + post-surgical / radiation)",
            "Lymphoma (Hodgkin + non-Hodgkin)",
            "Cat-scratch disease + filariasis",
        ),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "tlr",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
        ),
        notes=(
            "Sentinel-lymph-node biopsy revolutionised "
            "breast + melanoma cancer staging in the 1990s -- "
            "drains the tumour bed first, predicts wider "
            "nodal involvement."),
    ),

    # ============================================================
    # Comparative-anatomy entries (12)
    # ============================================================
    OrganSystem(
        id="circulation-comparative",
        name="Open vs closed circulation (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Open circulation: blood (haemolymph) bathes "
            "tissues directly through sinuses; pumped by a "
            "tubular dorsal heart.  Found in arthropods + "
            "most molluscs.  Closed circulation: blood "
            "confined to vessels; faster + higher-pressure "
            "transport.  Found in vertebrates, cephalopods, "
            "annelids."),
        representative_organs=(
            "Open: insect dorsal tube heart + ostia + "
            "haemocoel",
            "Closed: cephalopod 3 hearts (1 systemic + 2 "
            "branchial)",
            "Closed annelid: 5 'hearts' (lateral aortic "
            "arches in earthworm)",
        ),
        key_cell_types=(
            "Haemocytes (insects)",
            "Cephalopod haemocyanin-carrying haemolymph cells",
        ),
        functional_anatomy=(
            "Cephalopods (squid, octopus) evolved closed "
            "circulation independently of vertebrates -- the "
            "oxygen demand of jet-propulsion-active "
            "predators",
        ),
        evolutionary_origin=(
            "Open circulation is ancestral; closed evolved "
            "convergently in cephalopods + annelids + "
            "vertebrates",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "drosophila-melanogaster", "apis-mellifera",
            "loligo-pealeii", "hirudo-medicinalis",
        ),
        notes=(
            "Cephalopod blood is blue (copper-based "
            "haemocyanin, not iron-based haemoglobin) + the "
            "3-heart system pumps it through gills then body "
            "in series."),
    ),
    OrganSystem(
        id="respiratory-comparative",
        name="Gills / book lungs / tracheae / air sacs (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Animal respiration evolved multiple parallel "
            "solutions to gas exchange: gills (fish + larval "
            "amphibians + many invertebrates), book lungs "
            "(arachnids + horseshoe crabs), tracheal system "
            "(insects + myriapods), bird-style air sacs + "
            "parabronchi (most-efficient vertebrate lung "
            "design)."),
        representative_organs=(
            "Gills (fish, axolotl)",
            "Book lungs (Limulus + spiders)",
            "Tracheal system + spiracles (insects)",
            "Avian air sacs + parabronchi (no alveoli)",
        ),
        key_cell_types=(
            "Gill lamellar epithelium",
            "Tracheal epithelium",
        ),
        functional_anatomy=(
            "Bird respiration is unidirectional through 9 air "
            "sacs + parabronchi -- the most-efficient "
            "vertebrate gas exchange (essential for high-"
            "altitude flight)",
            "Insect tracheae deliver O2 directly to tissues -- "
            "no respiratory pigment needed",
        ),
        evolutionary_origin=(
            "Tracheae + book lungs are sister chelicerate / "
            "tracheate inventions; air sacs are an archosaur "
            "(theropod -> avian) trait",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "danio-rerio", "ambystoma-mexicanum",
            "drosophila-melanogaster", "limulus-polyphemus",
            "gallus-gallus", "taeniopygia-guttata",
        ),
        notes=(
            "Insect body size is fundamentally limited by "
            "tracheal diffusion -- the giant Carboniferous "
            "dragonflies (Meganeura, ~ 70 cm wingspan) lived "
            "during atmospheric O2 peaks of ~ 30 %."),
    ),
    OrganSystem(
        id="digestive-comparative",
        name="Ruminant / avian / hindgut digestion (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Herbivorous animals evolved diverse strategies "
            "for digesting cellulose: foregut fermentation "
            "(ruminants -- 4-chambered stomach), avian "
            "gizzard + crop, hindgut fermentation (horses, "
            "rabbits, lagomorphs)."),
        representative_organs=(
            "Ruminant: rumen + reticulum + omasum + abomasum",
            "Avian: crop (food storage) + proventriculus "
            "(glandular) + gizzard (mechanical)",
            "Hindgut: enlarged caecum + colon (rabbit, horse)",
        ),
        key_cell_types=(
            "Rumen + caecum microbiota (cellulolytic "
            "anaerobes -- Bacteroides, Ruminococcus, "
            "methanogenic archaea)",
        ),
        functional_anatomy=(
            "Rumen produces ~ 200-400 L methane / cow / day "
            "(via Methanobrevibacter ruminantium) -- a major "
            "anthropogenic CH4 source",
            "Coprophagy in rabbits + rodents (eating night "
            "soft caecotrophs) recovers microbial protein + "
            "B-vitamins from hindgut fermentation",
        ),
        evolutionary_origin=(
            "Foregut fermentation evolved independently in "
            "ruminants + colobine monkeys + hoatzin (an "
            "exclusively-fermenting bird)",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "bos-taurus", "gallus-gallus",
        ),
        notes=(
            "Bovine rumen methanogenesis is a major "
            "agricultural greenhouse-gas source -- 3-NOP "
            "(Bovaer) feed additive + seaweed-based "
            "interventions reduce CH4 output by 30-80 %."),
    ),
    OrganSystem(
        id="nervous-comparative",
        name="Nerve net / centralisation / cephalopod brain (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Evolution of nervous-system organisation: "
            "cnidarian diffuse nerve nets -> bilaterian "
            "centralisation (ganglia + nerve cord) -> "
            "vertebrate dorsal hollow neural tube + brain -> "
            "cephalopod massively-developed CNS (the most "
            "complex invertebrate brain)."),
        representative_organs=(
            "Cnidarian: diffuse nerve net (no brain)",
            "Planarian: cephalic ganglia + ventral nerve cord",
            "Cephalopod: ~ 500 M neuron CNS (octopus)",
            "Vertebrate: hollow dorsal neural tube + cranial "
            "+ spinal nerves",
        ),
        key_cell_types=(
            "Cnidarian nerve-net neurons (no glia)",
            "Cephalopod neurons (largest known in Loligo "
            "giant axon, ~ 1 mm diameter)",
        ),
        functional_anatomy=(
            "Octopus has 2/3 of its neurons in arm ganglia, "
            "1/3 in central brain -- distributed cognition + "
            "arm-autonomous reflexes",
        ),
        evolutionary_origin=(
            "Bilaterian centralisation is one of the major "
            "transitions; the octopus camera eye + brain "
            "evolved independently from those of vertebrates",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "hydra-vulgaris", "nematostella-vectensis",
            "schmidtea-mediterranea", "loligo-pealeii",
            "aplysia-californica",
            "caenorhabditis-elegans",
        ),
        notes=(
            "C. elegans has exactly 302 neurons in the "
            "hermaphrodite -- the only fully-wired nervous "
            "system known (every synapse mapped, White et "
            "al. 1986 -- 'the mind of a worm')."),
    ),
    OrganSystem(
        id="excretory-comparative",
        name="Protonephridia / metanephridia / Malpighian tubules (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Invertebrate excretory diversity: protonephridia "
            "(planarian flame cells), metanephridia (annelid + "
            "molluscan kidneys-of-Bowman), Malpighian tubules "
            "(insects + arachnids -- branch off the gut + "
            "function in air-breathing dry-environment "
            "nitrogen-waste excretion)."),
        representative_organs=(
            "Protonephridia: flame cell + duct (planarian)",
            "Metanephridia: ciliated funnel + tubule + bladder "
            "+ nephridiopore (earthworm)",
            "Malpighian tubules: blind-ended diverticula off "
            "midgut/hindgut junction (insect)",
        ),
        key_cell_types=(
            "Flame cells (protonephridia)",
            "Solenocytes",
            "Insect Malpighian principal + stellate cells",
        ),
        functional_anatomy=(
            "Insect Malpighian-tubule excretion produces uric "
            "acid (almost insoluble + low water cost) -- key "
            "to terrestrial life",
        ),
        evolutionary_origin=(
            "Vertebrate metanephric kidney is highly derived; "
            "invertebrates explore wider design space + "
            "haven't been constrained to a single body plan",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "schmidtea-mediterranea", "hirudo-medicinalis",
            "drosophila-melanogaster",
        ),
        notes=(
            "Drosophila Malpighian tubules are a tractable "
            "model for vertebrate epithelial transport + "
            "renal disease (e.g. polycystic kidney disease "
            "homologues)."),
    ),
    OrganSystem(
        id="regeneration-comparative",
        name="Regeneration outliers (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Some animals regenerate body parts most cannot: "
            "planarian whole-body regeneration (any small "
            "fragment regrows the whole animal), axolotl limb "
            "+ heart + spinal cord regeneration, hydra "
            "biological-immortality (continuous interstitial "
            "stem-cell turnover)."),
        representative_organs=(
            "Planarian neoblasts (pluripotent adult stem "
            "cells)",
            "Axolotl blastema (limb regrowth tissue)",
            "Hydra interstitial cells",
        ),
        key_cell_types=(
            "Neoblasts (Schmidtea -- the only known adult "
            "pluripotent stem cells)",
            "Axolotl mesenchymal blastema cells",
        ),
        functional_anatomy=(
            "Planarian regeneration polarity is set by Wnt/"
            "beta-catenin: high beta-catenin -> tail; low -> "
            "head.  beta-catenin RNAi gives two-headed "
            "planarians",
        ),
        evolutionary_origin=(
            "Regeneration capacity correlates inversely with "
            "evolutionary derivedness in vertebrates (fish + "
            "amphibians > reptiles > birds > mammals) -- "
            "linked to immune-cell + scarring trade-offs",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "hedgehog", "notch",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "schmidtea-mediterranea", "ambystoma-mexicanum",
            "hydra-vulgaris",
        ),
        notes=(
            "Hydra is biologically immortal in the wild -- "
            "no detectable senescence + continuous cell "
            "renewal.  Lifespan studies under controlled "
            "conditions estimate > 1 400-year half-life."),
    ),
    OrganSystem(
        id="eyes-comparative",
        name="Eye evolution (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Photoreceptive structures evolved at least 40 "
            "times independently across animals.  The full "
            "spectrum: cnidarian eyespot (no image) -> "
            "cup eye (planarian) -> pinhole eye (Nautilus) -> "
            "camera eye (vertebrate + cephalopod -- one of "
            "biology's most striking convergences) -> "
            "compound eye (arthropods -- ommatidia)."),
        representative_organs=(
            "Cup eye (planarian -- ocellus)",
            "Pinhole eye (Nautilus -- no lens)",
            "Camera eye (vertebrate + cephalopod -- "
            "convergent)",
            "Compound eye (Drosophila -- ~ 800 ommatidia per "
            "eye)",
        ),
        key_cell_types=(
            "Photoreceptors (rods + cones in vertebrates; "
            "rhabdomeric in invertebrates)",
            "Lens cells (transparent crystallins)",
            "Retinal pigment epithelium",
        ),
        functional_anatomy=(
            "Vertebrate retina is inverted (photoreceptors at "
            "back); cephalopod retina is non-inverted (everted) "
            "-- biology's textbook example of convergent "
            "design with non-converging details",
            "Fly compound eye: each ommatidium has 6 outer + "
            "2 central photoreceptors + a fixed wavelength-"
            "tuning crystalline cone",
        ),
        evolutionary_origin=(
            "Conserved Pax6 / eyeless master-regulator gene "
            "drives eye specification across phyla -- "
            "Walter Gehring's 1995 Drosophila eyeless "
            "ectopic-expression experiment generated extra "
            "eyes on antennae + legs, then a mouse Pax6 "
            "homologue did the same in flies",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "hydra-vulgaris", "schmidtea-mediterranea",
            "loligo-pealeii", "drosophila-melanogaster",
            "homo-sapiens",
        ),
        notes=(
            "Cephalopod photoreceptors carry multiple opsin "
            "genes that may give them colour vision via "
            "wavelength-dependent chromatic aberration in "
            "their pupils -- despite being colour-blind in "
            "the conventional sense."),
    ),
    OrganSystem(
        id="cardiovascular-fish",
        name="Single-circuit fish heart (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Fish cardiovascular system: 2-chambered heart "
            "(1 atrium + 1 ventricle) -> ventral aorta -> "
            "gills (gas exchange + venous-to-arterial "
            "transition) -> dorsal aorta -> body -> heart.  "
            "A single circuit -- fundamentally different "
            "from the dual-circuit mammalian heart."),
        representative_organs=(
            "Two-chambered heart (sinus venosus + atrium + "
            "ventricle + bulbus arteriosus)",
            "Gill arches (branchial circulation)",
        ),
        key_cell_types=(
            "Cardiomyocytes (capable of regeneration in "
            "zebrafish -- unlike mammals)",
        ),
        functional_anatomy=(
            "Single circuit means systemic blood pressure "
            "drops dramatically across the gill capillary bed "
            "-- limits maximum sustained activity",
        ),
        evolutionary_origin=(
            "Tetrapod 3- + 4-chambered hearts evolved by "
            "septation of the fish ventricle to separate "
            "pulmonary + systemic returns",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "danio-rerio", "takifugu-rubripes",
            "oryzias-latipes",
        ),
        notes=(
            "Zebrafish cardiac regeneration is the leading "
            "model for understanding why mammalian hearts "
            "can't repair themselves after MI -- active "
            "research target for cardiac regenerative "
            "medicine."),
    ),
    OrganSystem(
        id="immune-invertebrate",
        name="Invertebrate innate immunity (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Invertebrates lack adaptive immunity (no "
            "Ig + TCR + RAG) but have rich innate defences: "
            "Drosophila Toll + IMD pathways (Hoffmann's "
            "Nobel-winning work); horseshoe-crab amoebocyte "
            "lysate (LAL endotoxin assay); insect cellular "
            "(haemocyte phagocytosis + nodulation + "
            "encapsulation) + humoral (antimicrobial peptides) "
            "responses."),
        representative_organs=(
            "Insect haemolymph + fat body (analog of "
            "vertebrate liver + adipose + immune cells)",
            "Horseshoe-crab amoebocytes",
        ),
        key_cell_types=(
            "Drosophila plasmatocytes + crystal cells + "
            "lamellocytes",
            "Limulus amoebocytes (LAL test)",
        ),
        functional_anatomy=(
            "Drosophila Toll pathway: Spaetzle ligand binds "
            "Toll receptor -> MyD88-like adaptor -> Dorsal "
            "(NF-kB-like) translocates to nucleus -> "
            "antimicrobial-peptide gene transcription "
            "(drosomycin, attacin, cecropin)",
        ),
        evolutionary_origin=(
            "Toll-like receptors are conserved from "
            "Drosophila to mammals -- Hoffmann's discovery "
            "(1996) opened the entire mammalian TLR field",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "tlr", "nf-kb",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "drosophila-melanogaster", "limulus-polyphemus",
        ),
        notes=(
            "Hoffmann's 2011 Nobel was shared with Beutler "
            "(mammalian TLR4) + Steinman (dendritic cells) -- "
            "the entire prize for innate immunity."),
    ),
    OrganSystem(
        id="endocrine-invertebrate",
        name="Insect ecdysone signalling (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Insect moulting + metamorphosis are driven by "
            "the steroid hormone ecdysone (and 20-hydroxy"
            "ecdysone, the bioactive form), with juvenile "
            "hormone (JH) determining whether moults are "
            "larval-larval, larval-pupal, or pupal-adult.  "
            "Ecdysone receptor EcR is a nuclear hormone "
            "receptor."),
        representative_organs=(
            "Prothoracic gland (ecdysone production)",
            "Corpora allata (juvenile hormone production)",
            "Ring gland (Drosophila composite endocrine "
            "organ)",
        ),
        key_cell_types=(
            "Prothoracic gland steroidogenic cells",
        ),
        functional_anatomy=(
            "Ecdysone-EcR-USP heterodimer binds ecdysone-"
            "response elements -> early-response genes "
            "(Br-C, E74, E75) -> late-response moulting "
            "genes",
        ),
        evolutionary_origin=(
            "Ecdysteroids are the ancestral arthropod "
            "hormone; ecdysone-receptor architecture is "
            "homologous to vertebrate steroid receptors",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "drosophila-melanogaster", "bombyx-mori",
        ),
        notes=(
            "Insect-growth-regulator insecticides "
            "(diflubenzuron, methoxyfenozide) target "
            "ecdysone signalling -- selective for arthropods, "
            "low vertebrate toxicity."),
    ),
    OrganSystem(
        id="muscular-comparative",
        name="Smooth / cardiac / skeletal / cnidarian muscle (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Three vertebrate muscle types (skeletal striated "
            "voluntary, cardiac striated involuntary, smooth "
            "involuntary) all use the same actomyosin sliding-"
            "filament mechanism but with distinct regulation "
            "(troponin vs caldesmon vs MLCK).  Cnidarian "
            "epitheliomuscular cells are evolutionarily "
            "ancestral."),
        representative_organs=(
            "Vertebrate skeletal + cardiac + smooth muscle",
            "Cnidarian epitheliomuscular cell layer",
            "Insect indirect flight muscle (oscillatory)",
        ),
        key_cell_types=(
            "Striated muscle fibres (sarcomeric)",
            "Smooth muscle cells (no sarcomere)",
            "Cnidarian epitheliomuscular cells (epithelium + "
            "contractile actomyosin in one cell)",
        ),
        functional_anatomy=(
            "Insect indirect flight muscle is the fastest "
            "muscle known -- oscillatory + asynchronous; ~ "
            "1 kHz wing-beat frequency in mosquitoes",
        ),
        evolutionary_origin=(
            "Cnidarian epitheliomuscular cells suggest "
            "muscle is older than the bilaterian split + "
            "evolved from epithelial contractility",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "atp-synthase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "drosophila-melanogaster",
            "hydra-vulgaris",
        ),
        notes=(
            "ATP synthase regenerates ATP at ~ 100 / sec / "
            "molecule under maximum load -- the muscle ATP "
            "demand of sustained exercise is met by "
            "mitochondrial throughput, not stored ATP "
            "(which suffices for ~ 2 sec of activity)."),
    ),
    OrganSystem(
        id="reproductive-invertebrate",
        name="Hermaphroditism + parthenogenesis (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Invertebrates explore reproductive strategies "
            "rare in vertebrates: simultaneous hermaphroditism "
            "(C. elegans XX hermaphrodites + occasional "
            "males), parthenogenesis (Daphnia cyclical, "
            "aphids facultative), eusociality with sterile "
            "castes (honeybees + ants + termites)."),
        representative_organs=(
            "C. elegans gonad (single tube with "
            "spermatogenesis at L4 + oogenesis lifelong)",
            "Daphnia ovarian + ephippial-egg apparatus "
            "(seasonal)",
            "Honeybee queen ovaries (~ 2 000 eggs / day)",
        ),
        key_cell_types=(
            "C. elegans germline stem cells",
            "Insect royal-jelly-fed queen-larva primordium",
        ),
        functional_anatomy=(
            "C. elegans XX hermaphrodites self-fertilise + "
            "produce isogenic broods -- the basis of forward-"
            "genetic screens that mapped most signalling "
            "pathways in the worm",
        ),
        evolutionary_origin=(
            "Eusociality evolved independently in "
            "Hymenoptera + termites (Isoptera) + naked mole "
            "rats -- Hamilton's kin-selection inclusive-"
            "fitness theory explains the haplodiploid "
            "Hymenopteran case",
        ),
        characteristic_disorders=(),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "insulin",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_animal_taxon_ids=(
            "caenorhabditis-elegans", "daphnia-pulex",
            "apis-mellifera",
        ),
        notes=(
            "Honeybee queen vs worker caste fate is set by "
            "differential royal-jelly nutrition driving "
            "insulin / TOR + DNA-methylation differences in "
            "the larva -- a clean epigenetic-developmental "
            "switch."),
    ),

    OrganSystem(
        id="thermoregulation-comparative",
        name="Ectothermy vs endothermy (comparative)",
        system_category="comparative-anatomy",
        short_summary=(
            "Two fundamentally different thermal-regulation "
            "strategies: ectotherms (most invertebrates + "
            "fish + amphibians + reptiles) rely on external "
            "heat sources + behavioural thermoregulation; "
            "endotherms (mammals + birds) maintain stable "
            "core temperature by metabolic heat production "
            "with ~ 5-10x higher resting metabolic rate."),
        representative_organs=(
            "Mammalian brown adipose tissue (UCP1-mediated "
            "non-shivering thermogenesis)",
            "Reptile + insect thermoregulatory behaviour "
            "(basking + shade-seeking)",
            "Avian + mammalian skin vasculature + sweat / "
            "panting heat-loss systems",
        ),
        key_cell_types=(
            "Brown adipocytes (UCP1+ multilocular)",
            "Beige / brite adipocytes (recruitable from "
            "white-adipose precursors)",
        ),
        functional_anatomy=(
            "UCP1 (uncoupling protein 1) short-circuits the "
            "mitochondrial proton gradient -> chemical "
            "energy released as heat instead of ATP",
            "Endothermic core temperature ~ 37 deg C in "
            "mammals + ~ 40 deg C in birds; "
            "ectotherm body temperature tracks ambient",
        ),
        evolutionary_origin=(
            "Endothermy evolved independently in synapsid "
            "(mammalian) + archosaur (avian + theropod-"
            "dinosaur) lineages; molecular convergence on "
            "high mitochondrial density + UCP1 (mammals) "
            "or muscle non-shivering mechanisms (birds)",
        ),
        characteristic_disorders=(
            "Heat stroke + hyperthermia",
            "Cold-induced hypothermia",
            "Mitochondrial-disease-driven cold intolerance",
        ),
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "atp-synthase",
        ),
        cross_reference_animal_taxon_ids=(
            "homo-sapiens", "mus-musculus",
            "anolis-carolinensis", "danio-rerio",
            "drosophila-melanogaster",
        ),
        notes=(
            "Adult-human brown-fat depots (paravertebral + "
            "supraclavicular) were re-discovered by FDG-PET "
            "in 2009 -- previously thought to disappear after "
            "infancy.  Pharmacological brown-fat activation "
            "is an active obesity / metabolic-disease drug "
            "target."),
    ),
)
