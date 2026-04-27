"""Phase BT-2.0 (round 222) — plant-hormones catalogue.

Each entry carries typed cross-references to:
- ``orgchem.db.Molecule`` rows by exact name (only 4 plant
  hormones currently in the seeded molecule DB: IAA, SA,
  Aspirin, Ethylene; most entries' cross_reference_molecule_
  names tuple is empty pending a future molecule-DB seed
  expansion).
- ``botany.core.taxa`` ids (the plant-taxa entries from the
  BT-1.0 catalogue where the hormone signalling was
  characterised — most signalling work pivots on
  arabidopsis-thaliana).

All cross-reference ids verified against destination
catalogues at write time.
"""
from __future__ import annotations
from typing import Tuple

from botany.core.plant_hormones import PlantHormone


PLANT_HORMONES: Tuple[PlantHormone, ...] = (
    # ============================================================
    # Auxins (4)
    # ============================================================
    PlantHormone(
        id="iaa",
        name="Indole-3-acetic acid (IAA)",
        hormone_class="auxin",
        structural_class=(
            "Indole-acetic-acid; the principal natural plant "
            "auxin.  Carboxylic acid + indole ring; weakly "
            "acidic + readily oxidised."),
        biosynthesis_precursor=(
            "L-Tryptophan via the indole-3-pyruvic acid (IPA) "
            "pathway: TAA1 / TAR aminotransferases generate "
            "IPA; YUCCA flavin monooxygenases oxidise IPA to "
            "IAA",
        ),
        perception_mechanism=(
            "TIR1 / AFB F-box receptors form a co-receptor "
            "complex with Aux/IAA repressors when IAA is "
            "present -> Aux/IAA poly-ubiquitination + "
            "proteasomal destruction -> ARF transcription "
            "factors freed to activate auxin-response genes",
        ),
        primary_physiological_effect=(
            "Apical dominance, phototropism + gravitropism, "
            "lateral-root initiation, vascular differentiation, "
            "embryonic patterning",
        ),
        antagonisms=(
            "Cytokinins (root vs shoot balance); strigolactones "
            "(branching suppression interacts with auxin)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (yucca + tir1 mutants)",
            "Maize (Cholodny-Went 1937 phototropism + "
            "Avena-coleoptile bioassay)",
        ),
        cross_reference_molecule_names=(
            "Indole-3-acetic acid (IAA, auxin)",
        ),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "zea-mays",
        ),
        notes=(
            "First plant hormone to be chemically identified "
            "(Kogl + Haagen-Smit, 1934).  The TIR1 + Aux/IAA "
            "co-receptor mechanism was elucidated by Estelle "
            "lab (Dharmasiri et al., Nature 2005)."),
    ),
    PlantHormone(
        id="2-4-d",
        name="2,4-D (2,4-dichlorophenoxyacetic acid)",
        hormone_class="auxin",
        structural_class=(
            "Synthetic phenoxyacetic-acid auxin; chlorinated "
            "aromatic ring + acetic-acid side chain"),
        biosynthesis_precursor=(
            "Synthetic — manufactured industrially from "
            "2,4-dichlorophenol + chloroacetic acid",
        ),
        perception_mechanism=(
            "Same TIR1 / AFB receptors as IAA — but 2,4-D "
            "metabolism + transport are slower, giving "
            "sustained auxin signalling that is lethal to "
            "broadleaf plants",
        ),
        primary_physiological_effect=(
            "Selective broadleaf herbicide: induces over-"
            "production of ethylene + abscisic acid -> "
            "uncontrolled growth + tissue collapse in "
            "dicots; monocots largely unaffected (different "
            "metabolism + auxin responses)",
        ),
        antagonisms=(),
        key_model_plants=(
            "Selectively kills dicotyledonous weeds in "
            "monocot crops (cereals, lawns)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(),
        notes=(
            "Co-developed during WW2 by US + UK programs as "
            "the first selective herbicide.  Component of "
            "Agent Orange (with 2,4,5-T) used as a "
            "defoliant in Vietnam — the contaminating dioxin "
            "(TCDD) drove the human-health legacy, not 2,4-D "
            "itself."),
    ),
    PlantHormone(
        id="naa",
        name="1-Naphthaleneacetic acid (NAA)",
        hormone_class="auxin",
        structural_class=(
            "Synthetic naphthalene-acetic-acid auxin; "
            "naphthalene ring + acetic-acid side chain"),
        biosynthesis_precursor=(
            "Synthetic — manufactured from naphthalene + "
            "chloroacetic acid",
        ),
        perception_mechanism=(
            "Same TIR1 / AFB co-receptor system as IAA",
        ),
        primary_physiological_effect=(
            "Adventitious-root formation in cuttings (the "
            "active ingredient of commercial rooting "
            "hormones); fruit-thinning in apple + olive "
            "production",
        ),
        antagonisms=(),
        key_model_plants=(
            "Used on cuttings of nearly every "
            "horticulturally-propagated species",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(),
        notes=(
            "Resists IAA-degrading enzymes (IAA-oxidases, "
            "amidohydrolases) so it persists longer in tissue "
            "than IAA itself — practical advantage for "
            "exogenous application."),
    ),
    PlantHormone(
        id="iba",
        name="Indole-3-butyric acid (IBA)",
        hormone_class="auxin",
        structural_class=(
            "Indole-butyric-acid; same indole ring as IAA "
            "but with a 4-carbon butyric-acid side chain "
            "instead of 2-carbon acetic acid"),
        biosynthesis_precursor=(
            "Endogenous: chain-extension of IAA by "
            "peroxisomal beta-oxidation (in reverse) — "
            "still partly debated mechanistically",
        ),
        perception_mechanism=(
            "Converted in planta to IAA by peroxisomal "
            "beta-oxidation -> acts as a slow-release pro-"
            "hormone for IAA",
        ),
        primary_physiological_effect=(
            "Adventitious-root formation; lateral-root "
            "development; preferred over NAA for "
            "horticultural rooting because endogenous IAA "
            "conversion gives a more 'natural' response",
        ),
        antagonisms=(),
        key_model_plants=(
            "Arabidopsis thaliana (ibr / pxa1 mutants in "
            "peroxisomal beta-oxidation)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "Long thought to be only synthetic, then re-"
            "discovered as an endogenous Arabidopsis auxin "
            "in the 1980s — chain-extension biology that "
            "took decades to nail down."),
    ),

    # ============================================================
    # Cytokinins (3)
    # ============================================================
    PlantHormone(
        id="trans-zeatin",
        name="trans-Zeatin",
        hormone_class="cytokinin",
        structural_class=(
            "Adenine derivative with a hydroxylated isoprenoid "
            "side chain on N6.  Most-active naturally-occurring "
            "cytokinin."),
        biosynthesis_precursor=(
            "Adenine + dimethylallyl-PP via IPT (isopentenyl-"
            "transferase) -> isopentenyl-adenine -> trans-zeatin "
            "after CYP735A hydroxylation",
        ),
        perception_mechanism=(
            "AHK2 / AHK3 / CRE1 (AHK4) two-component histidine-"
            "kinase receptors -> AHP phospho-relay -> ARR "
            "transcription factors",
        ),
        primary_physiological_effect=(
            "Promotes cell division (cytokinesis); shoot-meristem "
            "maintenance; delays leaf senescence; antagonises "
            "auxin to determine root vs shoot fate in tissue "
            "culture (Skoog + Miller 1957 ratio rule)",
        ),
        antagonisms=(
            "Auxin (root vs shoot identity)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (ahk receptor + ipt biosynthesis "
            "mutants)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "Skoog + Miller's auxin-cytokinin ratio rule is the "
            "founding principle of plant tissue culture + the "
            "basis of every commercial micropropagation protocol."),
    ),
    PlantHormone(
        id="kinetin",
        name="Kinetin (6-furfurylaminopurine)",
        hormone_class="cytokinin",
        structural_class=(
            "Adenine derivative with a furfuryl side chain on "
            "N6.  Synthetic — not a natural plant hormone but "
            "binds + activates plant cytokinin receptors."),
        biosynthesis_precursor=(
            "Synthetic — originally isolated as a degradation "
            "product of autoclaved herring-sperm DNA",
        ),
        perception_mechanism=(
            "Binds AHK / CRE1 cytokinin receptors with affinity "
            "comparable to trans-zeatin",
        ),
        primary_physiological_effect=(
            "Same as natural cytokinins: cell division + shoot "
            "regeneration in tissue culture",
        ),
        antagonisms=(
            "Auxin",
        ),
        key_model_plants=(
            "Tobacco pith assay (Skoog 1955) was the original "
            "kinetin discovery context",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(),
        notes=(
            "Discovered serendipitously by Miller + Skoog (1955) "
            "in autoclaved DNA — the founding member of the "
            "cytokinin class.  Naming honours its cytokinetic "
            "(cell-division) activity."),
    ),
    PlantHormone(
        id="bap",
        name="6-Benzylaminopurine (BAP / BA)",
        hormone_class="cytokinin",
        structural_class=(
            "Adenine derivative with a benzyl side chain on N6"),
        biosynthesis_precursor=(
            "Synthetic; also a minor natural metabolite in some "
            "plants",
        ),
        perception_mechanism=(
            "Same AHK / CRE1 receptors",
        ),
        primary_physiological_effect=(
            "Most widely used commercial cytokinin in micro-"
            "propagation + horticulture; promotes shoot "
            "multiplication + delays senescence in cut flowers",
        ),
        antagonisms=(),
        key_model_plants=(
            "Standard reagent across all tissue-culture systems",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(),
        notes=(
            "Cheaper + more stable than zeatin -> de-facto "
            "default cytokinin for commercial plant tissue "
            "culture."),
    ),

    # ============================================================
    # Gibberellins (2)
    # ============================================================
    PlantHormone(
        id="ga3",
        name="Gibberellin A3 (GA3 / gibberellic acid)",
        hormone_class="gibberellin",
        structural_class=(
            "Tetracyclic diterpenoid carboxylic acid; ent-"
            "gibberellane skeleton.  136 known natural "
            "gibberellins; only ~ 4 (GA1, GA3, GA4, GA7) are "
            "bioactive."),
        biosynthesis_precursor=(
            "Geranylgeranyl-PP -> ent-kaurene (CPS + KS) -> "
            "GA12 (KO + KAO) -> GA12 oxidation cascade by "
            "GA20-oxidases + GA3-oxidases yielding bioactive "
            "GAs",
        ),
        perception_mechanism=(
            "GID1 soluble nuclear receptor binds bioactive GA "
            "-> recruits + ubiquitinates DELLA-protein "
            "repressors via SCF^SLY1/GID2 -> DELLAs degraded "
            "-> GA-response transcription factors freed",
        ),
        primary_physiological_effect=(
            "Stem elongation (internode growth); seed "
            "germination (alpha-amylase induction in cereal "
            "aleurone); flowering induction in long-day plants; "
            "fruit-set + fruit growth",
        ),
        antagonisms=(
            "Abscisic acid (germination vs dormancy balance)",
            "DELLA proteins (constitutive negative regulators)",
        ),
        key_model_plants=(
            "Oryza sativa (Green Revolution sd1 dwarfing allele "
            "= GA20-oxidase-2 loss-of-function)",
            "Triticum aestivum (Rht-B1b/Rht-D1b = DELLA gain-"
            "of-function)",
            "Arabidopsis thaliana (ga1 / gai mutants)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "oryza-sativa",
            "triticum-aestivum",
        ),
        notes=(
            "First isolated from Gibberella fujikuroi -- the "
            "fungus that causes 'foolish-seedling' (bakanae) "
            "disease in rice via overproduction of gibberellin. "
            " Norman Borlaug's Green Revolution (Nobel Peace "
            "1970) used GA-insensitive Rht alleles to short-"
            "stalk wheat."),
    ),
    PlantHormone(
        id="ga4",
        name="Gibberellin A4 (GA4)",
        hormone_class="gibberellin",
        structural_class=(
            "ent-Gibberellane diterpenoid; differs from GA3 by "
            "lacking a 13-OH"),
        biosynthesis_precursor=(
            "Same upstream pathway as GA3, branching at the "
            "GA12 / GA9 step",
        ),
        perception_mechanism=(
            "Same GID1 / DELLA system; GA4 is the most potent "
            "bioactive form in Arabidopsis",
        ),
        primary_physiological_effect=(
            "Stem elongation, germination, flowering -- "
            "essentially same outputs as GA3 but is the "
            "predominant active GA in many dicots",
        ),
        antagonisms=(
            "Abscisic acid; DELLA repressors",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (predominant bioactive GA)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "GA3 vs GA4 dominance varies by species + tissue -- "
            "the 'most active' gibberellin is plant-specific."),
    ),

    # ============================================================
    # Abscisic acid (1)
    # ============================================================
    PlantHormone(
        id="aba",
        name="Abscisic acid (ABA)",
        hormone_class="abscisic-acid",
        structural_class=(
            "Sesquiterpenoid carboxylic acid; cleaved from C40 "
            "carotenoid precursor"),
        biosynthesis_precursor=(
            "Beta-carotene -> zeaxanthin -> violaxanthin -> "
            "neoxanthin -> 9'-cis-neoxanthin cleaved by NCED "
            "(rate-limiting step) -> xanthoxin -> ABA via "
            "ABA2 + AAO3",
        ),
        perception_mechanism=(
            "PYR / PYL / RCAR soluble receptors bind ABA + "
            "encapsulate the catalytic centre of PP2C "
            "phosphatases (ABI1/2 family) -> PP2C inhibition "
            "-> SnRK2 kinases freed to phosphorylate ABF / "
            "AREB transcription factors + SLAC1 anion channel",
        ),
        primary_physiological_effect=(
            "Stomatal closure under drought (the textbook "
            "rapid response); seed dormancy + maturation; "
            "stress-tolerance gene induction (LEAs, "
            "dehydrins)",
        ),
        antagonisms=(
            "Gibberellins (germination)",
            "Cytokinins (senescence balance)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (abi1 / abi2 PP2C mutants + "
            "PYR1 receptor cloning -- Cutler 2009 + Ma 2009 "
            "back-to-back papers)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "The PYR / PYL / RCAR receptor was the most-sought "
            "missing piece of plant signalling for ~ 20 years "
            "before its 2009 discovery -- now a textbook "
            "example of a 'gate-and-latch' allosteric receptor."),
    ),

    # ============================================================
    # Ethylene (1)
    # ============================================================
    PlantHormone(
        id="ethylene",
        name="Ethylene",
        hormone_class="ethylene",
        structural_class=(
            "C2H4; the simplest hormone known.  Gaseous at "
            "physiological temperature."),
        biosynthesis_precursor=(
            "S-adenosyl methionine -> 1-aminocyclopropane-1-"
            "carboxylic acid (ACC) by ACC synthase (ACS) -> "
            "ethylene by ACC oxidase (ACO) (the Yang cycle "
            "regenerates SAM from MTA)",
        ),
        perception_mechanism=(
            "ETR1 / ETR2 / EIN4 / ERS1 / ERS2 ER-membrane "
            "receptors bind ethylene via a copper cofactor "
            "in a histidine-kinase-like architecture; in "
            "absence of ethylene the receptors actively "
            "inhibit downstream EIN2 -> CTR1 Raf-like kinase "
            "phosphorylates EIN2 -> EIN2 stays at the ER.  "
            "Ethylene binding inactivates the receptors -> "
            "EIN2 cleaved + transported to nucleus -> EIN3 / "
            "EIL1 transcription factors stabilised",
        ),
        primary_physiological_effect=(
            "Climacteric fruit ripening (autocatalytic); "
            "leaf + flower abscission; senescence; triple "
            "response of dark-grown seedlings (shortened + "
            "thickened hypocotyl + apical hook); root-hair "
            "formation",
        ),
        antagonisms=(
            "Auxin (in some root contexts, additive in others)",
            "Silver ion (Ag+ via STS) blocks ethylene receptors "
            "-- horticultural floricultural longevity treatment",
        ),
        key_model_plants=(
            "Solanum lycopersicum (tomato Never-ripe = ETR3 "
            "gain-of-function)",
            "Musa acuminata (banana commercial gassing with "
            "C2H4 to ripen fruit)",
            "Arabidopsis thaliana (etr1 ein2 ein3 mutants -- "
            "the entire pathway was mapped via ethylene-"
            "insensitive seedling triple-response screens)",
        ),
        cross_reference_molecule_names=(
            "Ethylene",
        ),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "solanum-lycopersicum",
            "musa-acuminata",
        ),
        notes=(
            "The first plant hormone identified -- Russian "
            "scientist Dimitry Neljubow showed in 1901 that "
            "illuminating gas (containing ethylene) caused the "
            "horizontal growth of pea seedlings in his lab."),
    ),

    # ============================================================
    # Brassinosteroids (2)
    # ============================================================
    PlantHormone(
        id="brassinolide",
        name="Brassinolide (BL)",
        hormone_class="brassinosteroid",
        structural_class=(
            "Polyhydroxylated steroid lactone; first isolated "
            "from Brassica napus pollen (giving the class its "
            "name)"),
        biosynthesis_precursor=(
            "Campesterol via the C6-oxidation + C22 / C23 "
            "hydroxylation pathway through 6-deoxocastasterone "
            "+ castasterone",
        ),
        perception_mechanism=(
            "BRI1 single-pass leucine-rich-repeat receptor "
            "kinase at the plasma membrane binds BL in its "
            "extracellular island domain -> heterodimerises "
            "with BAK1 co-receptor -> trans-autophosphorylation "
            "-> BSK / CDG1 cascade -> BSU1 phosphatase -> "
            "BIN2 GSK3-like kinase inactivated -> BZR1 / BES1 "
            "transcription factors dephosphorylated + nuclear "
            "-> BR-responsive transcription",
        ),
        primary_physiological_effect=(
            "Cell elongation + division; vascular "
            "differentiation; pollen development; tolerance "
            "to abiotic stress (heat, salt, cold)",
        ),
        antagonisms=(
            "Auxin (largely synergistic in growth, but "
            "context-dependent)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (bri1 dwarf phenotype was "
            "the founding genetic discovery -- Clouse + Chory "
            "1996)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "Most-active known brassinosteroid; isolated 1979 "
            "from rapeseed pollen by Mitchell + Grove at USDA "
            "Beltsville from 200 kg of pollen yielding 4 mg of "
            "BL.  First plant steroid hormone."),
    ),
    PlantHormone(
        id="castasterone",
        name="Castasterone (CS)",
        hormone_class="brassinosteroid",
        structural_class=(
            "Polyhydroxylated steroid; immediate biosynthetic "
            "precursor of brassinolide (CS lacks the B-ring "
            "lactone)"),
        biosynthesis_precursor=(
            "6-deoxocastasterone via BR6ox enzyme; converted "
            "to brassinolide by BR6ox-mediated B-ring "
            "lactonisation",
        ),
        perception_mechanism=(
            "Same BRI1 / BAK1 receptor system as BL, with "
            "lower potency",
        ),
        primary_physiological_effect=(
            "Same as brassinolide; functionally redundant with "
            "BL in many tissues",
        ),
        antagonisms=(),
        key_model_plants=(
            "Arabidopsis thaliana, rice (the dominant "
            "endogenous BR in some Poaceae)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "oryza-sativa",
        ),
        notes=(
            "In rice + maize, castasterone is the dominant "
            "endogenous BR -- BL is the dominant form in "
            "Arabidopsis + tomato.  Functional equivalence "
            "but quantitative dominance varies by species."),
    ),

    # ============================================================
    # Jasmonates (2)
    # ============================================================
    PlantHormone(
        id="jasmonic-acid",
        name="Jasmonic acid (JA)",
        hormone_class="jasmonate",
        structural_class=(
            "Cyclopentanone-based oxylipin derived from "
            "alpha-linolenic acid"),
        biosynthesis_precursor=(
            "alpha-Linolenic acid in chloroplast membrane -> "
            "13-hydroperoxide (LOX) -> 12,13-EOT (AOS) -> "
            "OPDA (AOC) -> peroxisomal beta-oxidation -> JA",
        ),
        perception_mechanism=(
            "JA itself is largely INACTIVE -- conjugated to "
            "isoleucine by JAR1 to form JA-Ile (the bioactive "
            "ligand).  COI1 F-box receptor binds JA-Ile + "
            "JAZ repressors -> JAZ ubiquitinated + degraded -> "
            "MYC2 transcription factor freed",
        ),
        primary_physiological_effect=(
            "Wound response + chewing-insect defence; trichome "
            "formation; pollen + anther development; senescence; "
            "tendril coiling",
        ),
        antagonisms=(
            "Salicylic acid (SA / JA cross-talk: chewing-insect "
            "vs biotrophic-pathogen response trade-off)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (coi1 + jar1 mutants)",
            "Solanum lycopersicum (tomato wound response is "
            "JA + systemin synergy)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "solanum-lycopersicum",
        ),
        notes=(
            "Jasmonate name from jasmine -- methyl jasmonate is "
            "a key fragrance component of jasmine flowers + "
            "drives the floral note in perfumery."),
    ),
    PlantHormone(
        id="methyl-jasmonate",
        name="Methyl jasmonate (MeJA)",
        hormone_class="jasmonate",
        structural_class=(
            "Methyl ester of jasmonic acid; volatile -- the "
            "airborne signal form"),
        biosynthesis_precursor=(
            "Jasmonic acid + S-adenosyl methionine via JMT "
            "(jasmonic acid carboxyl methyltransferase)",
        ),
        perception_mechanism=(
            "Hydrolysed back to JA in receiving tissues -> "
            "conjugated to JA-Ile -> COI1 / JAZ system",
        ),
        primary_physiological_effect=(
            "Inter-plant + intra-plant volatile signalling of "
            "wound + herbivory status (the textbook 'plants "
            "talk' airborne signal)",
        ),
        antagonisms=(
            "Salicylic acid",
        ),
        key_model_plants=(
            "Tobacco + sagebrush airborne-signalling field "
            "studies (Karban + Baldwin)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "nicotiana-tabacum",
        ),
        notes=(
            "Karban + Baldwin's tobacco / sagebrush studies "
            "(1990s onward) established that MeJA airborne "
            "signalling primes neighbouring plants for "
            "herbivore defence -- now-standard inter-plant "
            "communication paradigm."),
    ),

    # ============================================================
    # Salicylic acid (1)
    # ============================================================
    PlantHormone(
        id="sa",
        name="Salicylic acid (SA)",
        hormone_class="salicylic-acid",
        structural_class=(
            "Phenolic acid; 2-hydroxybenzoic acid"),
        biosynthesis_precursor=(
            "Chorismate via ICS (isochorismate synthase) -> "
            "isochorismate -> SA (the dominant ICS pathway in "
            "Arabidopsis); minor PAL phenylalanine pathway "
            "contributes in some tissues",
        ),
        perception_mechanism=(
            "NPR1 cytosolic receptor binds SA via a copper "
            "cofactor + undergoes conformational change + "
            "monomerisation + nuclear translocation; in "
            "nucleus interacts with TGA transcription factors "
            "-> PR (pathogenesis-related) gene activation",
        ),
        primary_physiological_effect=(
            "Systemic acquired resistance (SAR) to biotrophic "
            "+ hemibiotrophic pathogens; basal disease "
            "resistance; thermogenesis (Arum lily heat "
            "production from SA-induced AOX)",
        ),
        antagonisms=(
            "Jasmonic acid (SA / JA antagonism; ETI hormone "
            "trade-off)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (npr1 mutant defines SA "
            "signalling)",
            "Salix alba (white willow -- the original source of "
            "salicylates that gave us aspirin)",
        ),
        cross_reference_molecule_names=(
            "Salicylic acid", "Aspirin",
        ),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "salix-alba",
        ),
        notes=(
            "Same molecule that humans use as aspirin (after "
            "acetylation) is the master pathogen-defence "
            "hormone in plants -- a stunning case of "
            "convergent + parallel pharmacology across two "
            "kingdoms."),
    ),

    # ============================================================
    # Strigolactones (2)
    # ============================================================
    PlantHormone(
        id="strigol",
        name="Strigol",
        hormone_class="strigolactone",
        structural_class=(
            "Tetracyclic sesquiterpene lactone with a "
            "characteristic D-ring butenolide"),
        biosynthesis_precursor=(
            "All-trans-beta-carotene -> 9-cis-beta-carotene "
            "(D27 isomerase) -> carlactone (CCD7 + CCD8) -> "
            "carlactonoic acid -> strigol via species-specific "
            "MAX1 cytochrome P450 enzymes",
        ),
        perception_mechanism=(
            "DWARF14 (D14) alpha/beta-hydrolase receptor "
            "hydrolyses the strigolactone D-ring + covalently "
            "attaches a fragment to a catalytic histidine -> "
            "recruits + ubiquitinates D53 / SMXL repressors "
            "via SCF-D3 -> repressors degraded -> branching-"
            "suppression transcription program",
        ),
        primary_physiological_effect=(
            "Suppression of axillary-bud outgrowth (shoot "
            "branching); root architecture remodelling; "
            "rhizosphere signal that induces arbuscular-"
            "mycorrhizal hyphal branching",
        ),
        antagonisms=(
            "Auxin (strigolactone + auxin together suppress "
            "branching; cytokinins promote branching)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (max mutants -- 'more "
            "axillary branching')",
            "Oryza sativa (d3 / d14 dwarf mutants)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana", "oryza-sativa",
        ),
        notes=(
            "Originally isolated from cotton-root exudate as "
            "the seed-germination signal for Striga (witchweed) "
            "+ Orobanche (broomrape) parasitic plants -- only "
            "established as an endogenous hormone in 2008 "
            "(Gomez-Roldan + Umehara, Nature)."),
    ),
    PlantHormone(
        id="orobanchol",
        name="Orobanchol",
        hormone_class="strigolactone",
        structural_class=(
            "Sesquiterpene lactone; same butenolide D-ring as "
            "strigol but stereochemically distinct C-ring + "
            "B-ring fusion"),
        biosynthesis_precursor=(
            "Carlactone (same upstream as strigol) via "
            "Solanaceae-specific OsMAX1 / SlCYP722C variants",
        ),
        perception_mechanism=(
            "Same D14 hydrolytic-receptor mechanism as strigol",
        ),
        primary_physiological_effect=(
            "Same outputs as strigol; orobanchol is the "
            "predominant endogenous SL in tomato + tobacco + "
            "many Solanaceae",
        ),
        antagonisms=(),
        key_model_plants=(
            "Solanum lycopersicum (orobanchol is the dominant "
            "endogenous SL)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "solanum-lycopersicum",
        ),
        notes=(
            "Demonstrates that the strigolactone family is "
            "structurally diverse + species-specific -- not a "
            "single 'plant strigol' but a chemo-diverse hormone "
            "class."),
    ),

    # ============================================================
    # Peptide hormones (3)
    # ============================================================
    PlantHormone(
        id="cle-peptides",
        name="CLE peptides (CLAVATA3 / CLE family)",
        hormone_class="peptide-hormone",
        structural_class=(
            "Short (12-13 aa) post-translationally modified "
            "peptides cleaved from longer precursors; central "
            "CLE motif + arabinosylation of conserved hydroxy"
            "prolines"),
        biosynthesis_precursor=(
            "Precursor proteins of 80-120 aa with N-terminal "
            "signal peptide + C-terminal CLE motif; processed "
            "by subtilisin-like proteases + tyrosine sulfation "
            "+ proline hydroxylation + arabinosylation",
        ),
        perception_mechanism=(
            "CLAVATA1 (CLV1) / BAM family LRR-RLKs + CLAVATA2 "
            "(CLV2) / CRN co-receptors; CLE peptide binds the "
            "extracellular LRR pocket -> kinase activation -> "
            "WUSCHEL transcription-factor repression -> shoot "
            "+ root meristem size restriction",
        ),
        primary_physiological_effect=(
            "Shoot apical meristem (SAM) size control via "
            "CLAVATA-WUSCHEL feedback (the textbook plant "
            "stem-cell circuit); root meristem size; vascular "
            "patterning (TDIF / CLE41)",
        ),
        antagonisms=(
            "WUSCHEL transcription factor (positive regulator "
            "of stem cells; CLV3 represses it)",
        ),
        key_model_plants=(
            "Arabidopsis thaliana (clv1 / clv3 + wus mutants -- "
            "Clark + Meyerowitz characterised the CLAVATA-WUS "
            "circuit in the 1990s)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "Major-domestication trait: tomato fruit size + "
            "maize ear architecture both involve loss-of-"
            "function alleles in CLE / CLAVATA-pathway genes "
            "selected during domestication."),
    ),
    PlantHormone(
        id="systemin",
        name="Systemin",
        hormone_class="peptide-hormone",
        structural_class=(
            "18-aa peptide; first peptide hormone identified "
            "in plants (Pearce + Ryan 1991)"),
        biosynthesis_precursor=(
            "Pro-systemin (200 aa precursor) wound-induced "
            "in tomato leaves; cleaved at the C-terminus to "
            "release the active 18-mer",
        ),
        perception_mechanism=(
            "SYR1 / SYR2 LRR-RLK receptor (identified 2018 "
            "after a 27-year search) -> BAK1 co-receptor -> "
            "MAPK + JA-biosynthesis cascade",
        ),
        primary_physiological_effect=(
            "Systemic wound response: amplifies + propagates "
            "JA biosynthesis from wound site to distant "
            "leaves; induces protease-inhibitor genes that "
            "deter chewing-insect digestion",
        ),
        antagonisms=(),
        key_model_plants=(
            "Solanum lycopersicum (tomato -- systemin is "
            "tomato-/Solanaceae-specific; not present in "
            "Arabidopsis)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "solanum-lycopersicum",
        ),
        notes=(
            "Confounded the field for decades because "
            "systemin is not conserved across plants -- only "
            "Solanaceae use this peptide; other plants use "
            "different mobile wound signals (HypSys, GLVs, "
            "electric + Ca2+ waves)."),
    ),
    PlantHormone(
        id="ralf-peptides",
        name="RALF peptides (rapid alkalinisation factor)",
        hormone_class="peptide-hormone",
        structural_class=(
            "~ 50-aa cysteine-rich peptides with conserved "
            "YISY + cysteine-pair motifs; ~ 40 RALF genes in "
            "Arabidopsis"),
        biosynthesis_precursor=(
            "Pre-pro-peptide processed by S1P (subtilase-1 "
            "protease) -> mature secreted RALF",
        ),
        perception_mechanism=(
            "FERONIA + ANXUR family Catharanthus-RLK1L-like "
            "receptors (CrRLK1L family) bind RALF + dimerise "
            "with LLG / LRE GPI-anchored co-receptors -> "
            "kinase-cascade activation",
        ),
        primary_physiological_effect=(
            "Apoplastic alkalinisation (the eponymous output) "
            "-- pollen-tube reception by the synergid cell + "
            "rejection of foreign pollen tubes (FERONIA-"
            "mediated speciation barrier); root-hair "
            "development; cell-wall integrity sensing",
        ),
        antagonisms=(),
        key_model_plants=(
            "Arabidopsis thaliana (feronia mutants; pollen-tube "
            "reception defects)",
        ),
        cross_reference_molecule_names=(),
        cross_reference_plant_taxon_ids=(
            "arabidopsis-thaliana",
        ),
        notes=(
            "FERONIA was the first plant receptor identified "
            "as a guardian of pollen-tube-female reception -- "
            "wrong-species pollen tubes are not received -- a "
            "molecular speciation barrier."),
    ),
)
