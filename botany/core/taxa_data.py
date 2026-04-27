"""Phase BT-1.0 (round 216) — 30-entry plant-taxa catalogue.

Each entry carries typed cross-references into:
- ``orgchem.db.Molecule`` rows by name (plant natural products /
  defence compounds / hormones).
- ``orgchem.core.metabolic_pathways`` ids (Calvin cycle is
  universal to every photosynthetic plant; glycolysis + TCA +
  ox-phos + fatty-acid biosynthesis universal to all plants).
- ``pharm.core.drug_classes`` ids (poppy → opioids; willow →
  NSAIDs; yew → taxanes).

All cross-reference ids verified against destination catalogues
at write time; the round-216 catalogue tests gate re-validation
at every test run.
"""
from __future__ import annotations
from typing import Tuple

from botany.core.taxa import PlantTaxon


# Universal pathways every photosynthetic vascular plant uses.
_CORE_PHOTO_PATHWAYS: Tuple[str, ...] = (
    "calvin_cycle", "glycolysis", "tca_cycle", "ox_phos",
)

# Lipid + carbohydrate housekeeping every plant uses.
_CORE_LIPID_PATHWAYS: Tuple[str, ...] = (
    "fatty_acid_synthesis", "beta_oxidation",
)


PLANT_TAXA: Tuple[PlantTaxon, ...] = (
    # ============================================================
    # Bryophytes (1 — model moss)
    # ============================================================
    PlantTaxon(
        id="physcomitrium-patens",
        name="Spreading earthmoss",
        full_taxonomic_name="Physcomitrium patens",
        division="bryophyta",
        plant_class="Bryopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Haploid-dominant alternation of generations; "
            "spores produced in capsules; antheridia + "
            "archegonia on gametophyte; flagellated sperm "
            "require water for fertilisation."),
        ecological_role=(
            "Pioneer species on bare disturbed soil; rapid "
            "colonisation; widespread in temperate Northern "
            "Hemisphere.  Indicator of soil moisture."),
        economic_importance=(
            "Premier model bryophyte for plant evo-devo; "
            "first fully sequenced moss (2008); "
            "homologous-recombination gene targeting works "
            "efficiently — the ‘Arabidopsis of mosses’."),
        model_organism=True,
        genome_size_or_mb="~480 Mb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Used to study the bryophyte → tracheophyte "
            "transition.  Lacks vascular tissue; relies on "
            "diffusion + capillary transport."),
    ),

    # ============================================================
    # Lycophytes (1)
    # ============================================================
    PlantTaxon(
        id="selaginella-moellendorffii",
        name="Spikemoss",
        full_taxonomic_name="Selaginella moellendorffii",
        division="lycopodiophyta",
        plant_class="Lycopodiopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Heterosporous; produces both microspores + "
            "megaspores in strobili; sporophyte-dominant; "
            "swimming sperm requires water film."),
        ecological_role=(
            "Native to subtropical China; dry-tolerant; some "
            "Selaginella species are ‘resurrection plants’ "
            "that survive complete desiccation."),
        economic_importance=(
            "Smallest known land-plant genome; reference "
            "lycophyte for studying the evolution of vascular "
            "tissue + roots + leaves; sequenced in 2011."),
        model_organism=True,
        genome_size_or_mb="~106 Mb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Lycophytes diverged from other vascular plants "
            "~ 400 Mya — they're our window onto ancestral "
            "vascular-plant biology."),
    ),

    # ============================================================
    # Pteridophytes / ferns (2)
    # ============================================================
    PlantTaxon(
        id="azolla-filiculoides",
        name="Water fern",
        full_taxonomic_name="Azolla filiculoides",
        division="pteridophyta",
        plant_class="Polypodiopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Heterosporous (mega + microspores); rapid "
            "vegetative spread by fragmentation in still "
            "water; symbiosis with the cyanobacterium "
            "*Anabaena azollae* in leaf cavities provides "
            "fixed N₂."),
        ecological_role=(
            "Free-floating aquatic fern; carpets pond + "
            "paddy-field surfaces.  The Azolla-Anabaena "
            "symbiosis is one of the most productive N-fixing "
            "systems in nature.  Implicated in the Eocene "
            "‘Azolla event’ — global cooling driven by "
            "Arctic Ocean Azolla blooms."),
        economic_importance=(
            "Used as a green-manure rice-paddy fertiliser "
            "in Asia for > 1000 years; under study as a "
            "biofuel + livestock-feed crop."),
        model_organism=False,
        genome_size_or_mb="~750 Mb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Cyanobacterial endosymbiont passed vertically — "
            "no free-living infection cycle.  Comparable to "
            "the ancient endosymbiotic origin of plastids."),
    ),
    PlantTaxon(
        id="pteridium-aquilinum",
        name="Bracken",
        full_taxonomic_name="Pteridium aquilinum",
        division="pteridophyta",
        plant_class="Polypodiopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Homosporous; sori on leaflet undersides release "
            "spores; gametophyte heart-shaped prothallus; "
            "extensive rhizome network drives clonal spread."),
        ecological_role=(
            "One of the world's most widely distributed "
            "vascular plants — every continent except "
            "Antarctica.  Aggressive coloniser of disturbed "
            "land + post-fire sites."),
        economic_importance=(
            "Major agricultural weed; carcinogenic "
            "ptaquiloside in young fronds + spores causes "
            "bovine + ovine bracken poisoning + elevated "
            "human gastric-cancer rates in chronic-exposure "
            "regions."),
        model_organism=False,
        genome_size_or_mb="~9.6 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Ptaquiloside is a norsesquiterpene glucoside — "
            "alkylates DNA after activation.  Classic example "
            "of a plant chemical defence with off-target "
            "mammalian toxicity."),
    ),

    # ============================================================
    # Gymnosperms (4)
    # ============================================================
    PlantTaxon(
        id="ginkgo-biloba",
        name="Ginkgo",
        full_taxonomic_name="Ginkgo biloba",
        division="gymnosperm",
        plant_class="Ginkgoopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Dioecious; ovules on female trees; motile sperm "
            "(unique among seed plants — primitive trait); "
            "fleshy outer seed coat (sarcotesta) smells "
            "rancid (butyric acid)."),
        ecological_role=(
            "Sole surviving member of an ancient lineage "
            "(Ginkgoales — extinct in the wild before "
            "cultivation); ‘living fossil’ — fossil record "
            "extends to ~ 270 Mya; deciduous despite being "
            "a gymnosperm."),
        economic_importance=(
            "Widely planted urban tree (males only — to "
            "avoid the smell); leaf extracts (ginkgolides + "
            "bilobalide) sold as memory-enhancing supplements "
            "(efficacy contested)."),
        model_organism=False,
        genome_size_or_mb="~10.6 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Ginkgolides are PAF-receptor antagonists — "
            "active research target for inflammation."),
    ),
    PlantTaxon(
        id="taxus-brevifolia",
        name="Pacific yew",
        full_taxonomic_name="Taxus brevifolia",
        division="gymnosperm",
        plant_class="Pinopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Dioecious; ovules in fleshy red aril (the only "
            "non-toxic part of the plant); wind pollination."),
        ecological_role=(
            "Slow-growing understory tree of Pacific NW old-"
            "growth conifer forests; shade-tolerant; "
            "ecologically vulnerable due to bark-stripping "
            "for paclitaxel extraction in the 1980s-90s."),
        economic_importance=(
            "Source of paclitaxel (Taxol®) — the original "
            "supply was extracted from yew bark; killed the "
            "tree.  Modern supply is semi-synthetic from "
            "10-deacetylbaccatin III in *Taxus baccata* "
            "needles + biotechnological cell-culture "
            "production."),
        model_organism=False,
        genome_size_or_mb="~10 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(
            "taxanes",
        ),
        notes=(
            "Paclitaxel stabilises microtubules → mitotic "
            "arrest → apoptosis.  First-line for ovarian + "
            "breast + lung + Kaposi-sarcoma chemotherapy."),
    ),
    PlantTaxon(
        id="pinus-taeda",
        name="Loblolly pine",
        full_taxonomic_name="Pinus taeda",
        division="gymnosperm",
        plant_class="Pinopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Monoecious; pollen + seed cones on same tree; "
            "wind pollination; winged seeds; ~ 18-month "
            "ovule-to-seed maturation."),
        ecological_role=(
            "Dominant softwood of southeastern USA; fast-"
            "growing pioneer species after disturbance; fire-"
            "adapted thick bark."),
        economic_importance=(
            "Most commercially important southern-US timber + "
            "pulpwood species; reference conifer genome (~ 22 "
            "Gb — one of the largest plant genomes "
            "sequenced); resin tapped for turpentine."),
        model_organism=True,
        genome_size_or_mb="~22 Gb",
        cross_reference_molecule_names=(
            "α-Pinene", "β-Pinene",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos", "fatty_acid_synthesis",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Pinene monoterpenes are the dominant volatile "
            "in pine resin — biosynthesised from GPP via "
            "pinene synthase, MEP/DOXP plastid pathway."),
    ),
    PlantTaxon(
        id="picea-abies",
        name="Norway spruce",
        full_taxonomic_name="Picea abies",
        division="gymnosperm",
        plant_class="Pinopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Monoecious; long needle-leaves; large pendant "
            "cones; wind-pollinated; can live 700-1000 years."),
        ecological_role=(
            "Dominant evergreen of European boreal + "
            "subalpine forests; stand-replacing fire + bark-"
            "beetle disturbance shape population dynamics."),
        economic_importance=(
            "Major European softwood for construction + "
            "musical instruments (violin tops — Stradivari "
            "favoured Picea abies); first conifer with full "
            "reference genome (2013 — Nature)."),
        model_organism=True,
        genome_size_or_mb="~19.6 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "‘Old Tjikko’ in Sweden — clonal Picea abies "
            "with root system dated > 9 500 years.  Genome "
            "rich in repetitive elements (~ 70 % LTR-"
            "retrotransposons)."),
    ),

    # ============================================================
    # Angiosperms — monocots (8)
    # ============================================================
    PlantTaxon(
        id="oryza-sativa",
        name="Rice",
        full_taxonomic_name="Oryza sativa",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating spikelets; panicle inflorescence; "
            "grass family Poaceae; semi-aquatic — paddy "
            "cultivation requires standing water."),
        ecological_role=(
            "Domesticated ~ 9 000 years ago in the Yangtze "
            "valley; the most consumed cereal grain on Earth "
            "(staple for ~ half of humanity)."),
        economic_importance=(
            "Reference monocot genome (japonica + indica); "
            "first crop genome fully sequenced (2002); "
            "Golden Rice (β-carotene biofortification) is "
            "the iconic GMO-for-nutrition project."),
        model_organism=True,
        genome_size_or_mb="~389 Mb",
        cross_reference_molecule_names=(
            "D-Glucose", "Sucrose",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos", "pentose_phosphate",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "C3 grass — energetically less efficient than C4 "
            "maize at high temperatures.  C4 rice engineering "
            "(C4 Rice Project) is an active long-term goal."),
    ),
    PlantTaxon(
        id="zea-mays",
        name="Maize / corn",
        full_taxonomic_name="Zea mays subsp. mays",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C4",
        reproductive_strategy=(
            "Monoecious; staminate tassel + pistillate ear; "
            "wind-pollinated; outcrossing; domesticated from "
            "*Zea mays subsp. parviglumis* (teosinte) in "
            "Mexico ~ 9 000 years ago."),
        ecological_role=(
            "Domesticated; one of three Mesoamerican ‘Three "
            "Sisters’ companion crops (maize / beans / "
            "squash); now grown on every continent except "
            "Antarctica."),
        economic_importance=(
            "Largest cereal crop by tonnage globally (~ 1.2 "
            "Gt/yr); reference C4 genome; classic genetics "
            "model (McClintock — transposons, 1983 Nobel); "
            "feedstock for ethanol biofuel + high-fructose "
            "corn syrup."),
        model_organism=True,
        genome_size_or_mb="~2.3 Gb",
        cross_reference_molecule_names=(
            "D-Glucose", "Sucrose", "D-Fructose",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos", "pentose_phosphate",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "C4 photosynthesis: PEP carboxylase fixes CO₂ "
            "in mesophyll cells → 4-C oxaloacetate → "
            "transported to bundle-sheath cells where Rubisco "
            "operates at high CO₂.  Suppresses photo-"
            "respiration."),
    ),
    PlantTaxon(
        id="saccharum-officinarum",
        name="Sugarcane",
        full_taxonomic_name="Saccharum officinarum",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C4",
        reproductive_strategy=(
            "Sterile triploid hybrid; propagated entirely by "
            "stem cuttings; sugarcane that does flower "
            "produces wind-dispersed silky panicles."),
        ecological_role=(
            "Tall tropical grass; native to New Guinea; one "
            "of the most efficient solar-energy harvesters "
            "(C4 + dense canopy + long growing season)."),
        economic_importance=(
            "~ 80 % of global sugar supply (sucrose); "
            "feedstock for Brazilian bioethanol industry; "
            "bagasse (fibrous residue) burnt for power + "
            "used in paper + bio-composites."),
        model_organism=False,
        genome_size_or_mb="~10 Gb",
        cross_reference_molecule_names=(
            "Sucrose", "D-Glucose", "D-Fructose",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Drives ~ 30 % of Brazilian transport fuel "
            "(ethanol).  Highly polyploid (> 100 chromosomes "
            "in commercial cultivars) — historically very "
            "hard to sequence."),
    ),
    PlantTaxon(
        id="triticum-aestivum",
        name="Bread wheat",
        full_taxonomic_name="Triticum aestivum",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Allohexaploid (AABBDD, 6 × 7 = 42 chromosomes); "
            "self-pollinating spikelets; arose ~ 8 000 years "
            "ago from spontaneous hybridisation of "
            "*Triticum turgidum* × *Aegilops tauschii*."),
        ecological_role=(
            "Domesticated cereal; Fertile Crescent origin; "
            "now the most widely grown crop on Earth by "
            "land area (~ 220 Mha)."),
        economic_importance=(
            "~ 770 Mt/yr; staple grain for ~ 1/3 of "
            "humanity; reference genome (IWGSC, 2018) — "
            "16 Gb, one of the most complex plant genomes; "
            "gluten proteins make leavened bread possible."),
        model_organism=True,
        genome_size_or_mb="~17 Gb (hexaploid)",
        cross_reference_molecule_names=(
            "Sucrose", "D-Glucose", "Amylose fragment "
            "(3 glucose, α-1,4)",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos", "pentose_phosphate",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Coeliac disease driven by gliadin fraction of "
            "gluten — 33-mer peptide resists proteolysis + "
            "triggers HLA-DQ2/DQ8 T-cell response."),
    ),
    PlantTaxon(
        id="musa-acuminata",
        name="Banana",
        full_taxonomic_name="Musa acuminata",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Commercial Cavendish + Gros Michel cultivars are "
            "sterile triploids — propagated entirely from "
            "rhizome suckers; wild diploid species are seed-"
            "propagated; flowers in pendulous inflorescence."),
        ecological_role=(
            "Tropical herbaceous monocot (the ‘trunk’ is a "
            "pseudostem of overlapping leaf bases); native "
            "to SE Asia + Australia; cultivated worldwide in "
            "tropics."),
        economic_importance=(
            "World's most-traded fruit + fourth-most-important "
            "food crop; threatened by Tropical Race 4 of "
            "*Fusarium oxysporum* f. sp. *cubense* (Panama "
            "disease) — same fungus that wiped out Gros "
            "Michel in the 1950s."),
        model_organism=False,
        genome_size_or_mb="~523 Mb (diploid)",
        cross_reference_molecule_names=(
            "Ethylene",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Climacteric ripening — autocatalytic ethylene "
            "burst triggers conversion of starch to sugar.  "
            "Bananas shipped green + gassed with C₂H₄ on "
            "arrival."),
    ),
    PlantTaxon(
        id="allium-sativum",
        name="Garlic",
        full_taxonomic_name="Allium sativum",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Bulb-forming geophyte; commercial garlic is "
            "sterile + propagated entirely from cloves "
            "(individual bulbils); wild ancestors flower + "
            "set seed."),
        ecological_role=(
            "Originated in central Asia; cultivated for ~ "
            "5 000 years; aggressive aroma deters herbivory + "
            "soil pathogens."),
        economic_importance=(
            "Major culinary crop; sulfur-containing alliin "
            "→ allicin chemistry on crushing (alliinase "
            "enzyme); allicin has antimicrobial + cardio-"
            "vascular effects in vitro; long folk-medicine "
            "history."),
        model_organism=False,
        genome_size_or_mb="~16 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Allicin is unstable + thermolabile — cooked "
            "garlic loses most allicin but converts to "
            "stable diallyl sulfides + ajoene."),
    ),
    PlantTaxon(
        id="vanilla-planifolia",
        name="Vanilla orchid",
        full_taxonomic_name="Vanilla planifolia",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="CAM",
        reproductive_strategy=(
            "Climbing terrestrial orchid; flowers open one "
            "day only; in native Mexico pollinated by "
            "*Melipona* bees; outside native range hand-"
            "pollinated; long green pod ferments to develop "
            "vanillin."),
        ecological_role=(
            "Native to Mexico + Central America; epiphytic "
            "on host trees in secondary tropical forest; "
            "facultative CAM under drought stress."),
        economic_importance=(
            "Source of natural vanillin (~ 2 % w/w of cured "
            "pods); second-most-expensive spice after saffron; "
            "synthetic vanillin from guaiacol or lignin "
            "supplies > 99 % of global market."),
        model_organism=False,
        genome_size_or_mb="~5 Gb",
        cross_reference_molecule_names=(
            "Vanillin",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Vanillin biosynthesised from ferulic acid via "
            "vanillin synthase (VpVAN, 2014).  CAM in "
            "Vanilla is facultative — switches with water "
            "availability."),
    ),
    PlantTaxon(
        id="aloe-vera",
        name="Aloe vera",
        full_taxonomic_name="Aloe vera (syn. A. barbadensis)",
        division="angiosperm-monocot",
        plant_class="Liliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="CAM",
        reproductive_strategy=(
            "Bird-pollinated tubular yellow flowers on "
            "inflorescence stalk; spreads vegetatively by "
            "offsets (pups); rarely sets seed in cultivation."),
        ecological_role=(
            "Xerophytic succulent; CAM photosynthesis allows "
            "stomatal closure during the day → minimises "
            "water loss; native to Arabian Peninsula but "
            "widely naturalised in arid zones."),
        economic_importance=(
            "Inner leaf gel used topically for burns + "
            "wound healing (anthraquinone-free fraction); "
            "outer-leaf yellow latex contains anthraquinone "
            "laxatives (aloin, barbaloin); $US-billion-scale "
            "cosmetics industry."),
        model_organism=False,
        genome_size_or_mb="~16 Gb",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "CAM cycle: stomata open at night → CO₂ fixed "
            "to malate by PEP carboxylase → stored in "
            "vacuole → released to Rubisco during the day "
            "with stomata closed."),
    ),

    # ============================================================
    # Angiosperms — eudicots (14)
    # ============================================================
    PlantTaxon(
        id="arabidopsis-thaliana",
        name="Thale cress",
        full_taxonomic_name="Arabidopsis thaliana",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating; tiny white cruciform flowers; "
            "rapid 6-week generation time; siliques release "
            "~ 5 000 seeds per plant."),
        ecological_role=(
            "Small weedy mustard-family plant native to "
            "Eurasia + Africa; common ruderal of disturbed "
            "ground; insignificant agriculturally."),
        economic_importance=(
            "Universal model dicot; first plant fully "
            "sequenced (2000); compact ~ 125 Mb genome; "
            "vast TAIR (The Arabidopsis Information "
            "Resource) database; transformation by *A. "
            "tumefaciens* floral-dip is routine."),
        model_organism=True,
        genome_size_or_mb="~125 Mb",
        cross_reference_molecule_names=(
            "Indole-3-acetic acid (IAA, auxin)", "Ethylene",
            "Salicylic acid",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos", "pentose_phosphate",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "All five major plant hormone classes (auxin, "
            "GA, CK, ABA, ethylene) and the defence "
            "hormones SA + JA were genetically dissected in "
            "Arabidopsis."),
    ),
    PlantTaxon(
        id="solanum-lycopersicum",
        name="Tomato",
        full_taxonomic_name="Solanum lycopersicum",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating yellow buzz-pollinated flowers "
            "(bumblebee-vibrated anthers in greenhouse "
            "production); fleshy berry fruit."),
        ecological_role=(
            "Domesticated in Mesoamerica from wild "
            "*Solanum pimpinellifolium*; spread globally "
            "after Columbian exchange; Solanaceae family."),
        economic_importance=(
            "Most-produced vegetable crop globally (~ 187 "
            "Mt/yr); reference genome (2012); model for "
            "fleshy-fruit ripening + climacteric ethylene "
            "biology; lycopene gives ripe fruit its red "
            "colour + is the most-studied dietary "
            "carotenoid antioxidant."),
        model_organism=True,
        genome_size_or_mb="~900 Mb",
        cross_reference_molecule_names=(
            "Lycopene", "Ethylene",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Lycopene is an acyclic C40 carotene "
            "biosynthesised from GGPP via phytoene → "
            "lycopene → β-carotene branch point.  Ripening "
            "fruit shifts plastid biology: chloroplasts → "
            "chromoplasts."),
    ),
    PlantTaxon(
        id="nicotiana-tabacum",
        name="Tobacco",
        full_taxonomic_name="Nicotiana tabacum",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating tubular flowers (hawkmoth-"
            "pollinated in wild relatives); allotetraploid "
            "from *N. sylvestris* × *N. tomentosiformis*; "
            "very small dust-like seeds."),
        ecological_role=(
            "Native to the Americas; widely naturalised; "
            "high foliar nicotine deters herbivory."),
        economic_importance=(
            "Cigarette + cigar industry — the dominant cash "
            "crop of historical colonial Virginia; nicotine "
            "addiction kills > 8 M people/yr globally; "
            "model plant for *Agrobacterium tumefaciens* "
            "transformation + transient protein expression "
            "(magnICON system); feedstock for several "
            "plant-made-pharmaceutical (PMP) projects."),
        model_organism=True,
        genome_size_or_mb="~4.5 Gb (allotetraploid)",
        cross_reference_molecule_names=(
            "Nicotine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Nicotine biosynthesised in roots from "
            "ornithine + nicotinic acid; transported to "
            "leaves; agonist of nicotinic acetylcholine "
            "receptors (cholinergic insect neurotoxin)."),
    ),
    PlantTaxon(
        id="papaver-somniferum",
        name="Opium poppy",
        full_taxonomic_name="Papaver somniferum",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Insect-pollinated showy 4-petalled flowers "
            "(white to red to purple); seed capsule (the "
            "‘poppy head’) source of latex on scoring."),
        ecological_role=(
            "Native to the eastern Mediterranean + western "
            "Asia; cultivated for > 5 000 years; tolerant "
            "of poor soils."),
        economic_importance=(
            "Sole natural source of morphine + codeine + "
            "thebaine + papaverine + noscapine; medicinal + "
            "illicit cultivation gave humanity the entire "
            "opioid pharmacopoeia; semi-synthetic derivatives "
            "include heroin, oxycodone, hydromorphone, "
            "buprenorphine."),
        model_organism=False,
        genome_size_or_mb="~2.7 Gb",
        cross_reference_molecule_names=(
            "Morphine", "Codeine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(
            "opioids",
        ),
        notes=(
            "Benzylisoquinoline-alkaloid biosynthesis "
            "elucidated in the 2010s; entire pathway can "
            "now be expressed in engineered yeast (Smolke "
            "et al., 2015)."),
    ),
    PlantTaxon(
        id="salix-alba",
        name="White willow",
        full_taxonomic_name="Salix alba",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Dioecious; wind-dispersed seeds with cottony "
            "tufts; readily propagated from cuttings (any "
            "broken twig will root)."),
        ecological_role=(
            "Riparian tree of European + North African "
            "river floodplains; rapid growth; salicylates "
            "in bark + leaves deter herbivory."),
        economic_importance=(
            "Bark has been used as an analgesic since "
            "Sumerian + Egyptian times; salicylic acid "
            "isolated 1828; acetylsalicylic acid (Aspirin) "
            "synthesised by Hoffmann at Bayer 1897 — the "
            "first NSAID + still one of the most-prescribed "
            "drugs on Earth."),
        model_organism=False,
        genome_size_or_mb="~340 Mb",
        cross_reference_molecule_names=(
            "Salicylic acid", "Aspirin",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(
            "nsaids",
        ),
        notes=(
            "Salicylic acid is also the principal plant-"
            "defence hormone — drives systemic acquired "
            "resistance against biotrophic pathogens.  Its "
            "human-pharmacology repurposing is one of "
            "biology's most economically successful."),
    ),
    PlantTaxon(
        id="coffea-arabica",
        name="Coffee",
        full_taxonomic_name="Coffea arabica",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating tetraploid (the only polyploid "
            "Coffea species); white fragrant flowers; red "
            "drupe fruit (‘cherries’) each bearing two "
            "seeds (the beans)."),
        ecological_role=(
            "Understory shrub of Ethiopian highland forests; "
            "shade-grown at altitude (1 000-2 000 m); "
            "vulnerable to *Hemileia vastatrix* (coffee leaf "
            "rust) + climate-change range shrinkage."),
        economic_importance=(
            "World's most-traded agricultural commodity by "
            "value; ~ 60 % of global coffee production "
            "(robusta from *C. canephora* the rest); "
            "caffeine biosynthesis pathway from xanthosine "
            "elucidated → engineering decaffeinated lines."),
        model_organism=False,
        genome_size_or_mb="~1.3 Gb (tetraploid)",
        cross_reference_molecule_names=(
            "Caffeine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Caffeine evolved independently in coffee, tea, "
            "+ cacao — convergent xanthine alkaloid "
            "biosynthesis.  Acts as natural pesticide + "
            "allelochemical."),
    ),
    PlantTaxon(
        id="cinchona-officinalis",
        name="Quinine bark",
        full_taxonomic_name="Cinchona officinalis",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Outcrossing tropical evergreen; tubular pink/"
            "white flowers in panicles; wind-dispersed seeds."),
        ecological_role=(
            "Native to the Andean cloud forests of Peru, "
            "Bolivia, Ecuador.  Bark cinchona alkaloids "
            "(quinine, quinidine, cinchonine, cinchonidine) "
            "deter herbivory."),
        economic_importance=(
            "Sole pre-1944 source of quinine — the first "
            "effective antimalarial drug; smuggled out of "
            "Andes by Dutch + British in 19th C, plantations "
            "established in Java + India.  Quinidine is a "
            "class Ia antiarrhythmic; tonic water uses "
            "quinine as a bitter agent."),
        model_organism=False,
        genome_size_or_mb="~1.1 Gb",
        cross_reference_molecule_names=(
            "Quinine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Quinine + quinidine are diastereomers — same "
            "atoms, different stereochemistry, dramatically "
            "different pharmacology.  Stereochemistry "
            "matters."),
    ),
    PlantTaxon(
        id="mentha-piperita",
        name="Peppermint",
        full_taxonomic_name="Mentha × piperita",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Sterile interspecific hybrid (M. aquatica × "
            "M. spicata); propagated entirely by stolons + "
            "rhizomes; rare seed sets are non-viable."),
        ecological_role=(
            "Aggressively spreads via underground rhizomes; "
            "moist temperate ground; insect-attracting "
            "lavender flowers; menthol is a feeding deterrent "
            "+ TRPM8 cold-receptor agonist in mammals."),
        economic_importance=(
            "Essential-oil crop (~ 50 % menthol); flavouring "
            "for confectionery + dental + pharma + cosmetic "
            "products; menthol is a topical analgesic + "
            "decongestant; entire monoterpene biosynthesis "
            "pathway elucidated by Croteau lab in the 1990s."),
        model_organism=False,
        genome_size_or_mb="~370 Mb",
        cross_reference_molecule_names=(
            "Menthol", "Limonene",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Menthol biosynthesis: GPP → limonene → trans-"
            "isopiperitenol → menthone → menthol (eight-step "
            "plastid + cytosol pathway).  Glandular "
            "trichomes on leaf surface secrete the oil."),
    ),
    PlantTaxon(
        id="theobroma-cacao",
        name="Cacao",
        full_taxonomic_name="Theobroma cacao",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Cauliflorous (flowers + fruits emerge directly "
            "from the trunk); tiny pink flowers pollinated "
            "by ceratopogonid midges; large oblong pods "
            "contain 30-50 seeds embedded in white pulp."),
        ecological_role=(
            "Native understory tree of Amazonian + Central "
            "American rainforest; shade-tolerant; frost-"
            "intolerant — restricted to ± 20° latitude."),
        economic_importance=(
            "Source of chocolate (cocoa solids from "
            "fermented + roasted seeds); ~ 5 Mt/yr global "
            "production; theobromine + caffeine give the "
            "stimulant kick; threatened by *Phytophthora* + "
            "frosty-pod-rot + child-labour issues in West "
            "African production chains."),
        model_organism=False,
        genome_size_or_mb="~430 Mb",
        cross_reference_molecule_names=(
            "Theobromine", "Caffeine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Theobromine = 3,7-dimethylxanthine — caffeine "
            "minus one methyl group on N1.  Toxic to dogs "
            "+ cats because they lack efficient hepatic "
            "demethylation."),
    ),
    PlantTaxon(
        id="atropa-belladonna",
        name="Deadly nightshade",
        full_taxonomic_name="Atropa belladonna",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Bell-shaped purple flowers; shiny black "
            "berries; bird-dispersed; entire plant + "
            "berries highly toxic to humans + most mammals "
            "(birds + some ruminants tolerate)."),
        ecological_role=(
            "Native to Europe + N. Africa + W. Asia; "
            "shaded woodland edges + waste ground; ‘bella "
            "donna’ — Renaissance women dilated their pupils "
            "with extracts."),
        economic_importance=(
            "Source of tropane alkaloids — atropine + "
            "scopolamine + hyoscyamine.  Atropine is the "
            "antidote for organophosphate (nerve-agent + "
            "insecticide) poisoning; scopolamine is a "
            "motion-sickness + pre-anaesthesia drug."),
        model_organism=False,
        genome_size_or_mb="~3 Gb",
        cross_reference_molecule_names=(
            "Atropine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Atropine = (RS)-hyoscyamine racemate.  "
            "Competitive muscarinic acetylcholine receptor "
            "antagonist — blocks parasympathetic + part of "
            "the central cholinergic system."),
    ),
    PlantTaxon(
        id="camellia-sinensis",
        name="Tea",
        full_taxonomic_name="Camellia sinensis",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Outcrossing self-incompatible; insect-pollinated "
            "white fragrant 5-petalled flowers; small woody "
            "capsule; commercial plantations propagated from "
            "cuttings of elite clones."),
        ecological_role=(
            "Native to SE Asian montane forests; cultivated "
            "as a small evergreen shrub on terraced "
            "plantations; new shoots (‘flush’) harvested "
            "every 1-2 weeks during the growing season."),
        economic_importance=(
            "Second-most-consumed beverage on Earth (after "
            "water); ~ 6 Mt/yr leaf production; processing "
            "differences (oxidation level) yield green / "
            "oolong / black / pu-erh variants from the same "
            "species; rich in catechins (EGCG) + caffeine "
            "+ L-theanine."),
        model_organism=False,
        genome_size_or_mb="~3.0 Gb",
        cross_reference_molecule_names=(
            "Caffeine",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "L-Theanine is a glutamate-analogue amino acid "
            "unique to *Camellia*; crosses BBB; partly "
            "explains the calming + alertness profile of "
            "tea distinct from pure caffeine."),
    ),
    PlantTaxon(
        id="capsicum-annuum",
        name="Chili pepper",
        full_taxonomic_name="Capsicum annuum",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="annual",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Self-pollinating; white star-shaped flowers; "
            "fleshy berry fruit; bird-dispersed (birds lack "
            "TRPV1 sensitivity to capsaicin → seeds pass "
            "through gut intact)."),
        ecological_role=(
            "Domesticated in Mesoamerica; sister species "
            "C. baccatum, C. chinense (habanero), "
            "C. frutescens (tabasco), C. pubescens cover the "
            "rest of the heat range."),
        economic_importance=(
            "Spice + vegetable crop; capsaicin used "
            "topically as analgesic (TRPV1 desensitisation) "
            "+ as basis for pepper-spray riot-control + as "
            "deer/wildlife deterrent on bird seed."),
        model_organism=False,
        genome_size_or_mb="~3.5 Gb",
        cross_reference_molecule_names=(
            "Capsaicin",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Capsaicin biosynthesis: vanillylamine + 8-"
            "methyl-6-nonenoyl-CoA → capsaicin (capsaicin "
            "synthase, AT3 in placenta tissue).  Pungency "
            "measured in Scoville heat units (SHU)."),
    ),
    PlantTaxon(
        id="hevea-brasiliensis",
        name="Rubber tree",
        full_taxonomic_name="Hevea brasiliensis",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="perennial",
        photosynthetic_strategy="C3",
        reproductive_strategy=(
            "Monoecious; insect- + wind-pollinated; "
            "explosive dehiscent fruit launches seeds up to "
            "30 m; commercial plantations propagated by "
            "bud-grafting."),
        ecological_role=(
            "Native to Amazonian rainforest; smuggled out "
            "by Henry Wickham in 1876, established in "
            "British SE Asian colonies (Malaya, Ceylon) "
            "where the Amazonian leaf-blight fungus is "
            "absent → tropical Asian plantations dominate "
            "global supply."),
        economic_importance=(
            "Sole commercial source of natural rubber "
            "(cis-1,4-polyisoprene); ~ 14 Mt/yr; latex "
            "tapped from incised bark; isoprene biosynthesis "
            "via MEP pathway in laticifer cells; remains "
            "irreplaceable for high-strength applications "
            "(tyres, gloves, condoms)."),
        model_organism=False,
        genome_size_or_mb="~1.5 Gb",
        cross_reference_molecule_names=(
            "Ethylene",
        ),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle", "glycolysis", "tca_cycle",
            "ox_phos",
        ),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Ethephon (an ethylene-releasing agrochemical) "
            "applied to bark to stimulate latex flow.  "
            "Ethylene = the ‘ripening hormone’ here repurposed "
            "as a productivity tool."),
    ),
    PlantTaxon(
        id="rafflesia-arnoldii",
        name="Corpse flower",
        full_taxonomic_name="Rafflesia arnoldii",
        division="angiosperm-eudicot",
        plant_class="Magnoliopsida",
        life_cycle="not-applicable",
        photosynthetic_strategy="not-applicable",
        reproductive_strategy=(
            "Holoparasite of *Tetrastigma* vines (no roots, "
            "no leaves, no stems); body reduced to mycelium-"
            "like haustorial threads inside host tissue; "
            "produces only the giant flower (~ 1 m diameter) "
            "+ rotting-flesh smell to attract carrion-fly "
            "pollinators."),
        ecological_role=(
            "Endemic to SW Sumatra + Borneo rainforest; "
            "produces the largest single flower in the "
            "world (record ~ 1.05 m); endangered — habitat "
            "loss + slow reproduction + dependence on host."),
        economic_importance=(
            "Tourism draw; subject of intense biological "
            "research (lost photosynthesis, lost genes, "
            "horizontal gene transfer from host); no "
            "agricultural or industrial use."),
        model_organism=False,
        genome_size_or_mb="unknown (~ 0.8-2 Gb estimated)",
        cross_reference_molecule_names=(),
        cross_reference_metabolic_pathway_ids=(),
        cross_reference_pharm_drug_class_ids=(),
        notes=(
            "Has lost its plastid genome entirely — one "
            "of only a handful of plants known to do so.  "
            "Acquires water + nutrients + much of its "
            "‘defence’ chemistry from the host vine."),
    ),
)
