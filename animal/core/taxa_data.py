"""Phase AB-1.0 (round 217) — 30-entry animal-taxa catalogue.

Each entry carries typed cross-references into:
- ``orgchem.db.Molecule`` rows by name (animal-derived
  hormones, neurotransmitters, metabolites, vitamins).
- ``cellbio.core.cell_signaling`` ids (developmental +
  apoptosis + immune pathways characterised in animal models).
- ``biochem.core.enzymes`` ids (animal-source enzymes —
  chymotrypsin, ACE, etc.).

All cross-reference ids verified against destination
catalogues at write time; the round-217 catalogue tests gate
re-validation at every test run.
"""
from __future__ import annotations
from typing import Tuple

from animal.core.taxa import AnimalTaxon


# Universal-to-animals enzymes (every animal uses them).
_CORE_METABOLIC_ENZYMES: Tuple[str, ...] = (
    "hexokinase", "gapdh", "lactate-dehydrogenase",
    "atp-synthase", "cytochrome-c-oxidase",
)


ANIMAL_TAXA: Tuple[AnimalTaxon, ...] = (
    # ============================================================
    # Porifera (1) — sponges
    # ============================================================
    AnimalTaxon(
        id="amphimedon-queenslandica",
        name="Demosponge",
        full_taxonomic_name="Amphimedon queenslandica",
        phylum="porifera",
        animal_class="Demospongiae",
        body_plan="asymmetric",
        germ_layers="not-applicable",
        coelom_type="not-applicable",
        reproductive_strategy=(
            "Hermaphroditic; broadcast spawning; ciliated "
            "swimming larvae (parenchymella) settle + "
            "metamorphose; asexual reproduction via budding "
            "+ gemmules; remarkable cell-type plasticity."),
        ecological_role=(
            "Filter-feeding sessile benthic invertebrate of "
            "the Great Barrier Reef; pumps litres of seawater "
            "per gram per hour; lacks true tissues, organs, "
            "or nervous system."),
        model_organism=True,
        genome_size_or_mb="~190 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "tgf-beta-smad", "notch",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "First sponge genome (2010) — surprisingly "
            "encodes most of the metazoan signalling "
            "toolkit (Wnt, TGF-β, Notch).  Argues these "
            "pathways predate true tissues."),
    ),

    # ============================================================
    # Cnidaria (2) — diploblast radial outgroup
    # ============================================================
    AnimalTaxon(
        id="hydra-vulgaris",
        name="Hydra",
        full_taxonomic_name="Hydra vulgaris",
        phylum="cnidaria",
        animal_class="Hydrozoa",
        body_plan="radial",
        germ_layers="diploblast",
        coelom_type="not-applicable",
        reproductive_strategy=(
            "Asexual budding dominates in lab strains; "
            "sexual reproduction with broadcast spawning "
            "under stress; effectively biologically immortal "
            "via continuous interstitial-stem-cell turnover."),
        ecological_role=(
            "Freshwater predatory polyp; tentacle nematocysts "
            "harpoon Daphnia + small invertebrates."),
        model_organism=True,
        genome_size_or_mb="~1.3 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "hedgehog",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Classic regeneration model since Trembley 1744. "
            "Wnt/β-catenin establishes the head-organising "
            "centre — same molecular logic later co-opted by "
            "vertebrates."),
    ),
    AnimalTaxon(
        id="nematostella-vectensis",
        name="Starlet sea anemone",
        full_taxonomic_name="Nematostella vectensis",
        phylum="cnidaria",
        animal_class="Anthozoa",
        body_plan="radial",
        germ_layers="diploblast",
        coelom_type="not-applicable",
        reproductive_strategy=(
            "External fertilisation; planula larva → "
            "metamorphosis → polyp; asexual fragmentation; "
            "tractable in lab — can be spawned + microinjected."),
        ecological_role=(
            "Burrowing salt-marsh anemone of N. American + "
            "European Atlantic estuaries.  Lacks the medusa "
            "stage; entirely benthic polyp."),
        model_organism=True,
        genome_size_or_mb="~450 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "tgf-beta-smad",
            "hedgehog",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Reference cnidarian for evo-devo.  Proves the "
            "bilaterian developmental toolkit predates "
            "bilateral symmetry."),
    ),

    # ============================================================
    # Platyhelminthes (1) — acoelomate flatworms
    # ============================================================
    AnimalTaxon(
        id="schmidtea-mediterranea",
        name="Planarian",
        full_taxonomic_name="Schmidtea mediterranea",
        phylum="platyhelminthes",
        animal_class="Turbellaria",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="acoelomate",
        reproductive_strategy=(
            "Two strains: sexual hermaphrodite + asexual "
            "fissiparous; asexual strain reproduces by "
            "transverse fission + complete regeneration of "
            "missing body parts (head, tail, pharynx)."),
        ecological_role=(
            "Freshwater carnivore + scavenger; cosmopolitan "
            "in cool clean streams + ponds."),
        model_organism=True,
        genome_size_or_mb="~775 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "hedgehog", "notch",
            "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Hosts neoblasts — pluripotent adult stem cells "
            "that drive whole-body regeneration.  Wnt "
            "signalling sets the anterior-posterior axis "
            "during regeneration; β-catenin RNAi gives "
            "two-headed planarians."),
    ),

    # ============================================================
    # Nematoda (2) — pseudocoelomate roundworms
    # ============================================================
    AnimalTaxon(
        id="caenorhabditis-elegans",
        name="C. elegans",
        full_taxonomic_name="Caenorhabditis elegans",
        phylum="nematoda",
        animal_class="Chromadorea",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="pseudocoelomate",
        reproductive_strategy=(
            "Self-fertilising hermaphrodites + occasional "
            "males; ~ 3-day life cycle at 20 °C; transparent "
            "eutelic body — every adult has exactly 959 "
            "somatic cells with a fully mapped lineage."),
        ecological_role=(
            "Bacterivorous soil nematode of decomposing "
            "fruit + compost; cosmopolitan."),
        model_organism=True,
        genome_size_or_mb="~100 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "intrinsic-apoptosis", "tnf-extrinsic-apoptosis",
            "insulin", "wnt-beta-catenin", "notch",
            "tgf-beta-smad", "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(
            "caspase-3",
        ),
        notes=(
            "Nobels: 2002 (Brenner / Horvitz / Sulston — "
            "lineage + apoptosis), 2006 (Fire / Mello — "
            "RNAi), 2008 (Chalfie — GFP), 2024 (Ambros / "
            "Ruvkun — microRNAs).  Sydney Brenner picked it "
            "for its small fixed cell number + transparency."),
    ),
    AnimalTaxon(
        id="trichinella-spiralis",
        name="Trichinella",
        full_taxonomic_name="Trichinella spiralis",
        phylum="nematoda",
        animal_class="Enoplea",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="pseudocoelomate",
        reproductive_strategy=(
            "Viviparous; adults in small intestine produce "
            "live larvae that migrate through bloodstream + "
            "encyst in striated muscle (the ‘nurse cell’)."),
        ecological_role=(
            "Zoonotic parasite cycled through carnivorous + "
            "omnivorous mammals (pig, bear, wild boar); "
            "human trichinellosis from undercooked pork."),
        model_organism=False,
        genome_size_or_mb="~64 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "tlr",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "One of the most prevalent helminth infections "
            "globally; routine pork inspection has all but "
            "eradicated it from regulated farming."),
    ),

    # ============================================================
    # Mollusca (2) — coelomate, soft-bodied
    # ============================================================
    AnimalTaxon(
        id="loligo-pealeii",
        name="Squid (longfin inshore)",
        full_taxonomic_name="Doryteuthis (Loligo) pealeii",
        phylum="mollusca",
        animal_class="Cephalopoda",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Semelparous (single reproductive event); "
            "external fertilisation; egg masses anchored to "
            "substrate; ~ 1-year life cycle."),
        ecological_role=(
            "Pelagic predator of NW Atlantic continental "
            "shelf; commercial fishery; major food for fish "
            "+ marine mammals."),
        model_organism=True,
        genome_size_or_mb="~5.5 Gb",
        cross_reference_molecule_names=(
            "Glycine",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "na-k-atpase", "atp-synthase",
        ),
        notes=(
            "The giant axon (≈ 1 mm diameter, 3rd-order "
            "stellate ganglion) was Hodgkin + Huxley's "
            "preparation for the action-potential equations "
            "(1952 — Nobel 1963).  Action-potential "
            "biophysics IS squid biology."),
    ),
    AnimalTaxon(
        id="aplysia-californica",
        name="California sea hare",
        full_taxonomic_name="Aplysia californica",
        phylum="mollusca",
        animal_class="Gastropoda",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Hermaphroditic; copulating chains common; "
            "external fertilisation; ~ 1-year life cycle."),
        ecological_role=(
            "Large herbivorous sea slug grazing on red algae "
            "off Pacific coast of N. America; defensive "
            "ink-cloud; can grow > 30 cm."),
        model_organism=True,
        genome_size_or_mb="~927 Mb",
        cross_reference_molecule_names=(
            "Dopamine",
        ),
        cross_reference_signaling_pathway_ids=(
            "gpcr-camp-pka", "camkii",
        ),
        cross_reference_enzyme_ids=(
            "pka", "adenylate-cyclase",
        ),
        notes=(
            "Eric Kandel's 2000 Nobel for the molecular "
            "biology of memory came from work on the gill-"
            "withdrawal reflex circuit + the role of cAMP/"
            "PKA/CREB in long-term potentiation — Aplysia's "
            "giant easy-to-record neurons made it possible."),
    ),

    # ============================================================
    # Annelida (1) — segmented coelomate worms
    # ============================================================
    AnimalTaxon(
        id="hirudo-medicinalis",
        name="Medicinal leech",
        full_taxonomic_name="Hirudo medicinalis",
        phylum="annelida",
        animal_class="Clitellata",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Hermaphroditic; cocoon-laying clitellates; "
            "long-lived (multi-year) in lab + wild."),
        ecological_role=(
            "Freshwater + amphibious bloodfeeder of European "
            "wetlands; severely depleted by 19th-century "
            "medical demand; CITES-protected."),
        model_organism=False,
        genome_size_or_mb="~228 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "trypsin",
        ),
        notes=(
            "Source of hirudin — the prototypical direct "
            "thrombin inhibitor that gave us bivalirudin + "
            "lepirudin (anticoagulant drug class).  FDA-"
            "approved as a medical device for venous "
            "congestion in reattachment surgery."),
    ),

    # ============================================================
    # Arthropoda (5) — coelomate, segmented exoskeleton
    # ============================================================
    AnimalTaxon(
        id="drosophila-melanogaster",
        name="Fruit fly",
        full_taxonomic_name="Drosophila melanogaster",
        phylum="arthropoda",
        animal_class="Insecta",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Sexually dimorphic; ~ 10-day generation time at "
            "25 °C; female lays ~ 100 eggs/day; vast genetic "
            "toolkit (GAL4-UAS, FLP-FRT, CRISPR)."),
        ecological_role=(
            "Saprophagous — decaying fruit specialist; "
            "domesticated escape from wild African ancestor."),
        model_organism=True,
        genome_size_or_mb="~140 Mb",
        cross_reference_molecule_names=(
            "Dopamine",
        ),
        cross_reference_signaling_pathway_ids=(
            "hedgehog", "notch", "wnt-beta-catenin",
            "tgf-beta-smad", "jak-stat", "egfr-ras-raf",
            "tlr", "intrinsic-apoptosis",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Nobels: 1933 (Morgan — chromosomes), 1946 "
            "(Muller — radiation mutagenesis), 1995 (Lewis / "
            "Nüsslein-Volhard / Wieschaus — segment polarity "
            "+ patterning), 2004 (Axel — olfactory receptors "
            "in part), 2011 (Hoffmann — Toll/innate "
            "immunity), 2017 (Hall / Rosbash / Young — "
            "circadian clock).  Almost every developmental "
            "signalling pathway was first discovered or "
            "named in Drosophila (Hh, Wnt as wingless, "
            "Notch, Toll, Hippo, …)."),
    ),
    AnimalTaxon(
        id="apis-mellifera",
        name="Western honeybee",
        full_taxonomic_name="Apis mellifera",
        phylum="arthropoda",
        animal_class="Insecta",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Eusocial; haplodiploid sex determination; "
            "single reproductive queen + sterile worker "
            "caste + seasonal drones; mass-provisioning "
            "brood comb; queen-pheromone caste regulation."),
        ecological_role=(
            "Most economically important pollinator; "
            "domesticated ~ 7 000 years; collapse-disorder + "
            "varroa-mite + neonicotinoid pressures."),
        model_organism=True,
        genome_size_or_mb="~250 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "insulin",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Insulin / TOR signalling drives queen-vs-"
            "worker caste differentiation in response to "
            "royal-jelly nutrition.  Same conserved "
            "metabolic-sensing pathway as in mammals."),
    ),
    AnimalTaxon(
        id="bombyx-mori",
        name="Silkworm",
        full_taxonomic_name="Bombyx mori",
        phylum="arthropoda",
        animal_class="Insecta",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Fully domesticated; flightless adults; depends "
            "entirely on human husbandry to reproduce; "
            "single annual generation in temperate climates "
            "(univoltine) or several (multivoltine)."),
        ecological_role=(
            "Has no wild population — entirely domesticated "
            "from *B. mandarina* ~ 5 000 years ago in China; "
            "obligate mulberry-leaf herbivore."),
        model_organism=True,
        genome_size_or_mb="~432 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "Bombykol (the female sex pheromone) was the "
            "first pheromone ever characterised — "
            "Butenandt 1959, ~ 313 000 trapped female "
            "abdomens for 6.4 mg of pure compound.  Started "
            "all of chemical-ecology."),
    ),
    AnimalTaxon(
        id="daphnia-pulex",
        name="Common waterflea",
        full_taxonomic_name="Daphnia pulex",
        phylum="arthropoda",
        animal_class="Branchiopoda",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Cyclical parthenogenesis: clonal asexual "
            "reproduction in stable conditions, switches to "
            "sexual reproduction with resting eggs (ephippia) "
            "under stress."),
        ecological_role=(
            "Filter-feeding planktonic crustacean; key link "
            "between primary producers + planktivorous fish "
            "in freshwater food webs; standard model in "
            "ecotoxicology."),
        model_organism=True,
        genome_size_or_mb="~200 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "First crustacean genome sequenced (2011) — "
            "highest gene count of any sequenced animal at "
            "the time (~ 31 000); attributed to extensive "
            "tandem duplication of environmentally-"
            "responsive genes."),
    ),
    AnimalTaxon(
        id="limulus-polyphemus",
        name="Atlantic horseshoe crab",
        full_taxonomic_name="Limulus polyphemus",
        phylum="arthropoda",
        animal_class="Merostomata",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "External fertilisation on intertidal beaches "
            "during full + new-moon spring tides; ~ 9-12 "
            "moults to maturity; adults can live 20+ years."),
        ecological_role=(
            "Living-fossil chelicerate; little morphological "
            "change in 450 My; benthic predator + scavenger "
            "of soft-bottom Atlantic shelf."),
        model_organism=False,
        genome_size_or_mb="~2.7 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "Limulus amoebocyte lysate (LAL) is the gold-"
            "standard assay for endotoxin contamination of "
            "biologics + medical devices.  Recombinant "
            "factor C (rFC) is the synthetic replacement "
            "phasing in to relieve harvesting pressure on "
            "wild populations."),
    ),

    # ============================================================
    # Echinodermata (1) — coelomate, secondarily radial as adults
    # ============================================================
    AnimalTaxon(
        id="strongylocentrotus-purpuratus",
        name="Purple sea urchin",
        full_taxonomic_name="Strongylocentrotus purpuratus",
        phylum="echinodermata",
        animal_class="Echinoidea",
        body_plan="radial",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Dioecious; broadcast spawning; bilaterally-"
            "symmetric pluteus larva metamorphoses to "
            "pentaradial adult; can live > 50 years."),
        ecological_role=(
            "Major Pacific kelp-forest grazer; controls "
            "kelp standing stock; population explosion in "
            "absence of sea-otter predation creates ‘urchin "
            "barrens’."),
        model_organism=True,
        genome_size_or_mb="~814 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "tgf-beta-smad",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Classic developmental-biology preparation "
            "since the 19th C — easy to spawn, transparent "
            "embryos, large numbers of synchronous embryos "
            "per spawn.  The fertilisation envelope reaction "
            "+ block-to-polyspermy were all worked out here."),
    ),

    # ============================================================
    # Chordata — non-vertebrate (1)
    # ============================================================
    AnimalTaxon(
        id="ciona-intestinalis",
        name="Sea squirt",
        full_taxonomic_name="Ciona intestinalis",
        phylum="chordata",
        animal_class="Ascidiacea",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Hermaphroditic; broadcast spawning; tadpole-"
            "like swimming larva with a notochord + dorsal "
            "nerve cord (the chordate diagnostic features); "
            "metamorphoses into sessile filter-feeding adult."),
        ecological_role=(
            "Solitary tunicate of marine intertidal + "
            "subtidal hard substrates; cosmopolitan; often "
            "fouling species in harbours."),
        model_organism=True,
        genome_size_or_mb="~117 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "notch", "hedgehog", "wnt-beta-catenin",
            "tgf-beta-smad",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Sister to vertebrates; compact genome with "
            "minimal duplications.  Reference for "
            "reconstructing the ancestral chordate body "
            "plan + identifying vertebrate-specific gene-"
            "family expansions."),
    ),

    # ============================================================
    # Chordata — fish (3)
    # ============================================================
    AnimalTaxon(
        id="danio-rerio",
        name="Zebrafish",
        full_taxonomic_name="Danio rerio",
        phylum="chordata",
        animal_class="Actinopterygii",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "External fertilisation; transparent embryos "
            "develop ex utero; ~ 3-month generation time; "
            "200+ eggs per clutch; full transgenic + CRISPR "
            "toolkit; ENU mutagenesis screens characterised "
            "early-development phenotypes."),
        ecological_role=(
            "Freshwater shoaling cyprinid of the Ganges "
            "river basin; omnivorous; lab-domesticated "
            "since the 1960s."),
        model_organism=True,
        genome_size_or_mb="~1.4 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "hedgehog",
            "tgf-beta-smad", "jak-stat", "insulin",
            "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "George Streisinger established the model in "
            "the 1960s.  Transparent embryos make it the "
            "premier in vivo imaging vertebrate.  Fluorescent "
            "reporter lines for blood, vasculature, neural "
            "crest, etc., are off-the-shelf."),
    ),
    AnimalTaxon(
        id="takifugu-rubripes",
        name="Tiger pufferfish (fugu)",
        full_taxonomic_name="Takifugu rubripes",
        phylum="chordata",
        animal_class="Actinopterygii",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "External fertilisation; coastal spawner; "
            "demersal eggs; reaches sexual maturity at ~ 3 "
            "years."),
        ecological_role=(
            "NW Pacific coastal demersal fish; feeds on "
            "molluscs + crustaceans (which supply the "
            "tetrodotoxin precursor — TTX is bacterial in "
            "ultimate origin)."),
        model_organism=True,
        genome_size_or_mb="~390 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "na-k-atpase",
        ),
        notes=(
            "Reference vertebrate genome with the smallest "
            "known among true vertebrates (~ 1/8 of the "
            "human genome at similar gene count) — minimal "
            "introns + scant repetitive DNA.  Tetrodotoxin "
            "is a Na⁺-channel blocker; the puffer's own "
            "channels carry resistance mutations."),
    ),
    AnimalTaxon(
        id="oryzias-latipes",
        name="Medaka",
        full_taxonomic_name="Oryzias latipes",
        phylum="chordata",
        animal_class="Actinopterygii",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "External fertilisation; oviparous; female "
            "carries eggs on anal fin until they attach to "
            "vegetation; tolerates wide temperature range "
            "(4-40 °C)."),
        ecological_role=(
            "Small (~ 4 cm) freshwater + brackish ricefield "
            "fish of E. Asia; tolerates pollution + "
            "temperature extremes."),
        model_organism=True,
        genome_size_or_mb="~700 Mb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "Complementary vertebrate model to zebrafish; "
            "diverged ~ 110 Mya so cross-species comparison "
            "is informative.  XY sex-determination + "
            "sex-reversal experiments are tractable."),
    ),

    # ============================================================
    # Chordata — amphibian (2)
    # ============================================================
    AnimalTaxon(
        id="xenopus-laevis",
        name="African clawed frog",
        full_taxonomic_name="Xenopus laevis",
        phylum="chordata",
        animal_class="Amphibia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "External fertilisation; allotetraploid; "
            "ovulation can be induced by hCG injection "
            "(historic basis of the first reliable "
            "pregnancy test, the ‘frog test’ of the 1930s); "
            "thousands of large eggs per spawn."),
        ecological_role=(
            "Aquatic frog of sub-Saharan Africa; invasive "
            "in introduced ranges (California, France, UK)."),
        model_organism=True,
        genome_size_or_mb="~3.1 Gb (allotetraploid)",
        cross_reference_molecule_names=(
            "Progesterone",
        ),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "tgf-beta-smad", "notch",
            "hedgehog", "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Classic embryology + biochemistry preparation "
            "— large eggs let you microinject mRNA + "
            "proteins for in vivo translation studies.  The "
            "first cloned vertebrate (Gurdon 1962, Nobel "
            "2012) was a Xenopus."),
    ),
    AnimalTaxon(
        id="ambystoma-mexicanum",
        name="Axolotl",
        full_taxonomic_name="Ambystoma mexicanum",
        phylum="chordata",
        animal_class="Amphibia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Neotenic — retains larval features (external "
            "gills) into sexual maturity; obligate aquatic "
            "salamander; external fertilisation via "
            "spermatophore deposition."),
        ecological_role=(
            "Critically endangered in the wild — restricted "
            "to a remnant of Lake Xochimilco near Mexico "
            "City; abundant in lab + pet trade."),
        model_organism=True,
        genome_size_or_mb="~32 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "tgf-beta-smad",
            "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(),
        notes=(
            "Fully regenerates limbs, tail, spinal cord, "
            "retina, jaw, heart at any life stage — the "
            "deepest regenerative capacity of any "
            "tetrapod.  Largest sequenced animal genome "
            "as of mid-2020s (~ 32 Gb)."),
    ),

    # ============================================================
    # Chordata — reptile (1)
    # ============================================================
    AnimalTaxon(
        id="anolis-carolinensis",
        name="Green anole",
        full_taxonomic_name="Anolis carolinensis",
        phylum="chordata",
        animal_class="Reptilia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Oviparous; female lays single eggs at intervals "
            "in moist soil; ~ 1-year generation; territorial "
            "throat-fan (dewlap) display in males."),
        ecological_role=(
            "Arboreal insectivorous lizard of the SE United "
            "States + Caribbean; classic radiation model — "
            "Anolis genus has > 400 species across the "
            "Caribbean island arc."),
        model_organism=True,
        genome_size_or_mb="~1.8 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "First reptile reference genome (2011, Nature). "
            "Reference for reconstructing amniote evolution; "
            "the Anolis radiation is the textbook example of "
            "convergent evolution of ecomorphs across "
            "independent islands."),
    ),

    # ============================================================
    # Chordata — bird (2)
    # ============================================================
    AnimalTaxon(
        id="gallus-gallus",
        name="Chicken",
        full_taxonomic_name="Gallus gallus domesticus",
        phylum="chordata",
        animal_class="Aves",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Oviparous; large yolk-rich egg supports "
            "external embryonic development with no "
            "maternal nutrient transfer; ~ 21-day "
            "incubation; sexually mature at ~ 5 months."),
        ecological_role=(
            "Domesticated from the wild red junglefowl "
            "(*Gallus gallus*) ~ 8 000 years ago in SE "
            "Asia; world's most-numerous bird (~ 25 "
            "billion at any moment); essential meat + egg "
            "protein source."),
        model_organism=True,
        genome_size_or_mb="~1.2 Gb",
        cross_reference_molecule_names=(
            "Cholesterol", "Progesterone",
        ),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "hedgehog",
            "tgf-beta-smad", "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(
            "lysozyme",
        ),
        notes=(
            "Egg white lysozyme was the first enzyme "
            "X-ray-crystallographically solved (Phillips "
            "1965).  The chick embryo is the historical "
            "developmental-biology preparation — easy to "
            "candle, manipulate, microsurgery."),
    ),
    AnimalTaxon(
        id="taeniopygia-guttata",
        name="Zebra finch",
        full_taxonomic_name="Taeniopygia guttata",
        phylum="chordata",
        animal_class="Aves",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Socially monogamous; oviparous; cooperative "
            "biparental care; sexually mature at ~ 90 days; "
            "highly tractable for breeding in lab."),
        ecological_role=(
            "Common Australian grassland passerine; cosmo-"
            "politan in captivity; song-learning canonical "
            "model (juvenile males learn songs from adult "
            "tutors during a sensitive period)."),
        model_organism=True,
        genome_size_or_mb="~1.2 Gb",
        cross_reference_molecule_names=(),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(),
        notes=(
            "Zebra-finch song-learning + the FoxP2 / vocal-"
            "communication parallel with humans is the "
            "leading non-human model for vocal learning + "
            "the neurobiology of speech."),
    ),

    # ============================================================
    # Chordata — mammal (6)
    # ============================================================
    AnimalTaxon(
        id="mus-musculus",
        name="House mouse",
        full_taxonomic_name="Mus musculus",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Polyestrous; ~ 19-21-day gestation; large "
            "litters (5-12 pups); sexual maturity at ~ 6 "
            "weeks; vast inbred-strain panel (C57BL/6, "
            "BALB/c, …) + transgenic + knockout toolkit."),
        ecological_role=(
            "Cosmopolitan commensal of human dwellings; "
            "natural granivore; the dominant mammalian model "
            "for biomedical research."),
        model_organism=True,
        genome_size_or_mb="~2.8 Gb",
        cross_reference_molecule_names=(
            "Cortisol", "Cholesterol", "Glycine",
            "Dopamine", "Progesterone",
        ),
        cross_reference_signaling_pathway_ids=(
            "wnt-beta-catenin", "notch", "hedgehog",
            "tgf-beta-smad", "jak-stat", "insulin",
            "egfr-ras-raf", "p53", "intrinsic-apoptosis",
            "tnf-extrinsic-apoptosis", "tlr", "tcr",
            "nf-kb",
        ),
        cross_reference_enzyme_ids=(
            "ace", "atp-synthase", "cyp3a4",
            "cytochrome-c-oxidase",
        ),
        notes=(
            "ENCODE + IMPC consortium-scale knockout + "
            "expression atlas.  Conditional Cre-loxP + "
            "tamoxifen-inducible knockouts allow tissue- + "
            "time-restricted gene deletion.  Most clinical "
            "drug candidates pass through mouse efficacy + "
            "tox studies before human trials."),
    ),
    AnimalTaxon(
        id="rattus-norvegicus",
        name="Norway rat",
        full_taxonomic_name="Rattus norvegicus",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Polyestrous; ~ 21-day gestation; 6-12 pups "
            "per litter; sexual maturity at ~ 6 weeks; "
            "outbred (Sprague-Dawley, Wistar) + inbred "
            "(F344, Lewis) strains."),
        ecological_role=(
            "Cosmopolitan commensal; carries hantaviruses + "
            "Leptospira + plague historically; second-most-"
            "used biomedical mammal model after mouse."),
        model_organism=True,
        genome_size_or_mb="~2.8 Gb",
        cross_reference_molecule_names=(
            "Cortisol", "Dopamine",
        ),
        cross_reference_signaling_pathway_ids=(
            "insulin", "p53", "egfr-ras-raf",
        ),
        cross_reference_enzyme_ids=(
            "ace", "cyp3a4",
        ),
        notes=(
            "Larger than mouse → preferred for behavioural "
            "neuroscience + cardiovascular surgery + "
            "pharmacology.  The original ‘lab rat’ (Wistar "
            "1906) is the ancestor of every modern strain."),
    ),
    AnimalTaxon(
        id="macaca-mulatta",
        name="Rhesus macaque",
        full_taxonomic_name="Macaca mulatta",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Seasonal breeders; ~ 165-day gestation; "
            "single offspring; matrilineal social "
            "organisation; sexual maturity at 3-4 years."),
        ecological_role=(
            "Cosmopolitan Asian primate (Afghanistan → "
            "China); generalist omnivore; commensal with "
            "humans across much of urban India."),
        model_organism=True,
        genome_size_or_mb="~2.9 Gb",
        cross_reference_molecule_names=(
            "Cortisol", "Cholesterol", "Estradiol",
            "Progesterone",
        ),
        cross_reference_signaling_pathway_ids=(
            "insulin", "tcr", "nf-kb",
        ),
        cross_reference_enzyme_ids=(
            "ace", "cyp3a4",
        ),
        notes=(
            "Closest commonly-used animal model to human — "
            "94 % genome identity; Karl Landsteiner's "
            "discovery of the Rh blood-group system used "
            "rhesus blood (hence the name).  Critical "
            "preclinical model for HIV / SIV vaccines + "
            "neuroscience."),
    ),
    AnimalTaxon(
        id="canis-lupus-familiaris",
        name="Domestic dog",
        full_taxonomic_name="Canis lupus familiaris",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Monoestrous; ~ 63-day gestation; 1-12 "
            "puppies per litter; breed-defined extreme "
            "morphological diversity within one species."),
        ecological_role=(
            "First domesticated animal — diverged from "
            "grey wolf ~ 15 000-40 000 years ago; ~ 400 "
            "registered breeds; companion + working + "
            "service animal."),
        model_organism=True,
        genome_size_or_mb="~2.4 Gb",
        cross_reference_molecule_names=(
            "Cholesterol",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "trypsin", "chymotrypsin", "atp-synthase",
        ),
        notes=(
            "Banting + Best (1921) established insulin's "
            "role in glucose homeostasis using "
            "pancreatectomised dogs (Nobel 1923).  Modern "
            "dog-genomics work exploits breed differences "
            "as a natural genetic screen for trait + "
            "disease loci."),
    ),
    AnimalTaxon(
        id="bos-taurus",
        name="Cattle",
        full_taxonomic_name="Bos taurus",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Polyestrous (~ 21-day cycle); ~ 283-day "
            "gestation; usually single calf; sexual "
            "maturity at ~ 12-15 months; modern dairy "
            "breeds depend entirely on artificial "
            "insemination + embryo transfer."),
        ecological_role=(
            "Domesticated from wild aurochs (*Bos "
            "primigenius*) ~ 10 500 years ago; ruminant "
            "grazer; foundation of pastoral agriculture; "
            "~ 1.5 billion individuals globally."),
        model_organism=True,
        genome_size_or_mb="~2.7 Gb",
        cross_reference_molecule_names=(
            "Cholesterol", "Lactose", "Cholic acid",
        ),
        cross_reference_signaling_pathway_ids=(),
        cross_reference_enzyme_ids=(
            "chymotrypsin", "trypsin",
            "carbonic-anhydrase-ii", "atp-synthase",
            "cytochrome-c-oxidase",
        ),
        notes=(
            "Bovine pancreas + spinal cord + adrenal + "
            "muscle are the historical commercial source "
            "of every classical mammalian biochemistry "
            "preparation — chymotrypsin, trypsin, RNase A, "
            "F₁-ATPase, cytochrome c.  John Walker's "
            "ATP-synthase structure (Nobel 1997) used "
            "bovine F₁."),
    ),
    AnimalTaxon(
        id="homo-sapiens",
        name="Human",
        full_taxonomic_name="Homo sapiens sapiens",
        phylum="chordata",
        animal_class="Mammalia",
        body_plan="bilateral",
        germ_layers="triploblast",
        coelom_type="coelomate",
        reproductive_strategy=(
            "Iteroparous K-strategist; menstrual cycle "
            "(~ 28 days); ~ 280-day gestation; usually "
            "single offspring; extreme parental investment "
            "+ extended developmental dependence (~ 18 "
            "years)."),
        ecological_role=(
            "Cosmopolitan generalist + niche constructor; "
            "dominant ecosystem engineer of the Holocene + "
            "Anthropocene; ~ 8 billion individuals."),
        model_organism=True,
        genome_size_or_mb="~3.1 Gb",
        cross_reference_molecule_names=(
            "Cortisol", "Cholesterol", "Testosterone",
            "Estradiol", "Progesterone", "Dopamine",
            "L-DOPA (levodopa)", "Glycine",
            "ATP (adenosine-5'-triphosphate)",
            "Adenosine", "NADH", "FAD", "Acetyl-CoA",
            "Pyruvate", "Glutathione", "Urea",
            "Vitamin D3 (cholecalciferol)",
            "Retinol (vitamin A)", "Cholic acid",
            "Phosphatidylcholine (POPC-like)",
            "Sphingomyelin (C18)", "Lactose",
        ),
        cross_reference_signaling_pathway_ids=(
            "mapk-erk", "pi3k-akt-mtor", "jak-stat",
            "wnt-beta-catenin", "notch", "hedgehog",
            "nf-kb", "tgf-beta-smad", "gpcr-camp-pka",
            "gpcr-ip3-ca", "pkc-dag-ca", "camkii",
            "tlr", "cgas-sting", "hippo-yap", "ampk",
            "hif1a", "p53", "intrinsic-apoptosis",
            "tnf-extrinsic-apoptosis", "necroptosis",
            "pyroptosis", "mtorc1-aa-sensing", "insulin",
            "egfr-ras-raf", "tcr",
        ),
        cross_reference_enzyme_ids=(
            "alcohol-dehydrogenase",
            "lactate-dehydrogenase", "gapdh",
            "cytochrome-c-oxidase", "cyp3a4",
            "hexokinase", "pka", "egfr-tk", "comt",
            "ugt1a1", "chymotrypsin", "trypsin",
            "caspase-3", "ace",
            "carbonic-anhydrase-ii",
            "adenylate-cyclase", "tim",
            "phosphoglycerate-mutase", "cyclophilin-a",
            "dna-ligase-i", "glutamine-synthetase",
            "pyruvate-carboxylase", "acc",
            "na-k-atpase", "atp-synthase",
            "p-glycoprotein",
        ),
        notes=(
            "The ultimate cross-reference hub of the "
            "platform.  Almost every catalogue entry "
            "across all 6 studios traces back to human "
            "biology — every drug class targets human "
            "pathology, every signalling pathway was "
            "validated in mammalian cells, every metabolic "
            "pathway runs in human tissues.  Reference "
            "genome sequenced 2003; pangenome reference "
            "consortium 2023."),
    ),
)
