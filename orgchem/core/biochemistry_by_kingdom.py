"""Phase 47a (round 166) — biochemistry-by-kingdom catalogue.

A second top-level Macromolecules-window-style explorer that
organises biochemistry **by kingdom of life** rather than **by
molecular class** (the existing Macromolecules window).  Users
get a side-by-side comparison of how the same biochemical
themes (membranes, ribosomes, energy metabolism, genetic code,
signalling) play out differently across **Eukarya / Bacteria /
Archaea** plus the optional **Viruses** tab — with each kingdom
tab having sub-tabs for **Structure**, **Physiology +
Development**, **Genetics + Evolution**.

Each topic cross-references the existing Phase-43 cell-component
catalogue, the Phase-42 metabolic-pathways catalogue, and the
seeded molecule database, surfacing the molecules + reactions
involved inline rather than asking the user to chase them across
existing tools.

Pure-headless: no Qt imports.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


KINGDOMS: Tuple[str, ...] = (
    "eukarya", "bacteria", "archaea", "viruses",
)

SUBTABS: Tuple[str, ...] = (
    "structure",     # cellular architecture, membranes, walls
    "physiology",    # energy, growth, division, signalling
    "genetics",      # genome organisation, replication, evolution
)

#: Round 169 — sub-domain tags within a kingdom.  For Eukarya
#: this is the traditional kingdoms-within-the-domain view
#: (animal / plant / fungus / protist).  For Bacteria the
#: gram-positive / gram-negative split.  For Archaea the major
#: phyla.  For Viruses the viral-classification split.  Empty
#: string in a topic means "applies to the whole kingdom".
SUB_DOMAINS: Tuple[str, ...] = (
    "animal", "plant", "fungus", "protist",          # eukarya
    "gram-positive", "gram-negative",                # bacteria
    "euryarchaeota", "crenarchaeota", "asgard",      # archaea
    "dna-virus", "rna-virus", "retrovirus",          # viruses
)


@dataclass(frozen=True)
class KingdomTopic:
    """One topic in the biochemistry-by-kingdom catalogue."""
    id: str
    kingdom: str
    subtab: str
    title: str
    body: str
    # Cross-references to other catalogues (resolved at render
    # time by the dialog).  Empty tuples mean "no cross-ref".
    cross_reference_cell_component_ids: Tuple[str, ...] = ()
    cross_reference_pathway_ids: Tuple[str, ...] = ()
    cross_reference_molecule_names: Tuple[str, ...] = ()
    notes: str = ""
    # Round 169 — Phase 47d.  Sub-domain tag within the
    # kingdom.  For Eukarya this is animal / plant / fungus /
    # protist; for Bacteria gram-positive / gram-negative;
    # etc.  Empty string means "applies to the whole kingdom"
    # — the topic surfaces under any sub-domain filter.
    sub_domain: str = ""


_TOPICS: List[KingdomTopic] = [

    # ============================================================
    # EUKARYA — Structure
    # ============================================================
    KingdomTopic(
        id="eukarya-structure-membrane-architecture",
        kingdom="eukarya",
        subtab="structure",
        title="Plasma membrane architecture (eukaryotic)",
        body=(
            "The eukaryotic plasma membrane is a fluid mosaic of "
            "phospholipid bilayer + ~30 wt-% membrane proteins + "
            "cholesterol modulator + glycolipid / glycoprotein "
            "outer-leaflet glycocalyx.  Defining features vs the "
            "bacterial / archaeal membranes: (a) **cholesterol** "
            "as a fluidity modulator (absent in bacteria, replaced "
            "by hopanoids); (b) **sphingomyelin + glycolipids** "
            "in the outer leaflet (membrane-raft microdomains); "
            "(c) phosphatidylserine asymmetry — confined to the "
            "inner leaflet, flips outward as an apoptosis 'eat-"
            "me' signal."
        ),
        cross_reference_cell_component_ids=(
            "eukaryotic-plasma-membrane",),
        cross_reference_molecule_names=("Cholesterol",),
    ),
    KingdomTopic(
        id="eukarya-structure-organelles",
        kingdom="eukarya",
        subtab="structure",
        title="Compartmentalisation: organelles + endomembrane "
              "system",
        body=(
            "Eukaryotic cells are defined by **membrane-bound "
            "compartmentalisation**.  The endomembrane system "
            "(nuclear envelope ↔ rough ER ↔ smooth ER ↔ Golgi ↔ "
            "lysosomes / vacuoles ↔ secretory + endocytic "
            "vesicles) physically separates protein synthesis + "
            "post-translational modification + sorting + "
            "degradation steps.  Mitochondria + chloroplasts are "
            "**endosymbiotic** organelles with their own genomes "
            "+ ribosomes.  The cytoskeleton (actin + microtubules "
            "+ intermediate filaments) gives shape, motility, + "
            "intracellular transport tracks."
        ),
        cross_reference_cell_component_ids=(
            "endoplasmic-reticulum-rough",
            "endoplasmic-reticulum-smooth",
            "golgi-apparatus", "mitochondrion", "lysosome",
            "actin-microfilament", "microtubule",
        ),
    ),
    KingdomTopic(
        id="eukarya-structure-nucleus",
        kingdom="eukarya",
        subtab="structure",
        title="Nucleus + nuclear pore complex",
        body=(
            "The nucleus is the eukaryotic compartment that holds "
            "the genome, separated from the cytoplasm by a "
            "**double membrane** (nuclear envelope) studded with "
            "~ 2 000-3 000 nuclear pore complexes (NPCs) per "
            "cell.  Each NPC is ~ 125 MDa of ~ 30 nucleoporins "
            "and forms a selectivity barrier: small molecules "
            "and proteins < 40 kDa diffuse passively, larger "
            "cargo is transported actively via importin-α/β + "
            "Ran-GTP gradient.  The nuclear lamina (lamin A/B/C "
            "intermediate filaments) anchors the inner membrane."
        ),
        cross_reference_cell_component_ids=(
            "nuclear-envelope", "nucleolus", "chromatin",
        ),
        cross_reference_molecule_names=(
            "GTP (guanosine-5'-triphosphate)",
        ),
    ),
    KingdomTopic(
        id="eukarya-structure-ecm-and-cell-walls",
        kingdom="eukarya",
        subtab="structure",
        title="ECM (animal) + cell walls (plant + fungus)",
        body=(
            "Animal eukaryotes secrete an **extracellular matrix "
            "(ECM)** of collagen + fibronectin + laminin + "
            "elastin + glycosaminoglycans + proteoglycans — a "
            "load-bearing scaffold + signalling reservoir.  Plant "
            "eukaryotes wall themselves in **cellulose "
            "microfibrils** + hemicellulose + pectin (+ lignin in "
            "secondary walls), resisting turgor pressure.  Fungal "
            "eukaryotes use **chitin** (β-1,4-N-acetylglucosamine) "
            "+ β-1,3-glucan + β-1,6-glucan + mannoproteins — the "
            "echinocandin antifungals selectively block β-1,3-"
            "glucan synthase since humans have no equivalent "
            "pathway."
        ),
        cross_reference_cell_component_ids=(
            "ecm-animal", "plant-cell-wall", "fungal-cell-wall",
        ),
    ),
    KingdomTopic(
        id="eukarya-structure-cytoskeleton",
        kingdom="eukarya",
        subtab="structure",
        title="Three-filament cytoskeleton",
        body=(
            "Eukaryotes uniquely have a **three-filament "
            "cytoskeleton**: (a) **actin microfilaments** "
            "(7 nm, dynamic, ATP-driven; cell shape + motility + "
            "cytokinesis); (b) **microtubules** (25 nm hollow "
            "tubes of α/β-tubulin, GTP-driven; mitotic spindle + "
            "vesicle / organelle transport via kinesin + dynein "
            "motors; cilia / flagella axoneme); (c) "
            "**intermediate filaments** (10 nm, tissue-specific "
            "— keratin in epithelia, vimentin in mesenchyme, "
            "neurofilament in neurons, lamin in nucleus; "
            "mechanical strength).  Pharmacological probes: "
            "phalloidin stains F-actin; taxol stabilises + "
            "vincristine destabilises microtubules — both "
            "anti-mitotic anti-cancer drugs."
        ),
        cross_reference_cell_component_ids=(
            "actin-microfilament", "microtubule",
            "intermediate-filament",
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
            "GTP (guanosine-5'-triphosphate)",
        ),
    ),

    # ============================================================
    # EUKARYA — Physiology + Development
    # ============================================================
    KingdomTopic(
        id="eukarya-physiology-aerobic-respiration",
        kingdom="eukarya",
        subtab="physiology",
        title="Aerobic respiration in mitochondria",
        body=(
            "Eukaryotes generate ATP via **oxidative "
            "phosphorylation** in mitochondria: glucose → "
            "pyruvate (glycolysis, cytoplasm) → acetyl-CoA + "
            "CO₂ + NADH (PDH, mitochondrial matrix) → 2 CO₂ + "
            "NADH + FADH₂ + GTP per acetyl-CoA (TCA cycle, "
            "matrix) → 32-38 ATP per glucose via electron "
            "transport chain Complexes I-IV pumping protons + "
            "ATP synthase Complex V using the Δμ_H⁺ to "
            "synthesise ATP.  Net yield: ~ 30 ATP per glucose "
            "in vivo (textbook 38 is a stoichiometric maximum)."
        ),
        cross_reference_cell_component_ids=("mitochondrion",),
        cross_reference_pathway_ids=(
            "glycolysis", "tca_cycle", "ox_phos",
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
            "NADH",
            "FAD",
            "Pyruvate",
            "GTP (guanosine-5'-triphosphate)",
            "Coenzyme A (CoA-SH)",
            "Acetyl-CoA",
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-photosynthesis",
        kingdom="eukarya",
        subtab="physiology",
        title="Photosynthesis (plant + algal)",
        body=(
            "Plant + algal eukaryotes harvest light energy in "
            "**chloroplasts**.  Light reactions in the thylakoid "
            "membrane: Photosystem II splits water → O₂ + e⁻ + "
            "H⁺ (Mn₄CaO₅ cluster); electron flow through the "
            "Z-scheme via plastoquinone + cytb₆f + plastocyanin "
            "+ Photosystem I + ferredoxin + ferredoxin-NADP⁺ "
            "reductase generates NADPH; ATP synthase uses the "
            "thylakoid Δμ_H⁺.  Dark reactions in the stroma — "
            "**Calvin cycle** — fixes CO₂ via RuBisCO (most "
            "abundant protein on Earth) and uses the NADPH + ATP "
            "to build glyceraldehyde-3-phosphate sugars."
        ),
        cross_reference_cell_component_ids=("chloroplast",),
        cross_reference_pathway_ids=("calvin_cycle",),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
            "NADPH",
            "Plastoquinone-9",
            "Glyceraldehyde-3-phosphate (G3P)",
        ),
        sub_domain="plant",
    ),
    KingdomTopic(
        id="eukarya-physiology-cell-cycle-mitosis",
        kingdom="eukarya",
        subtab="physiology",
        title="Cell cycle + mitosis",
        body=(
            "Eukaryotic cell division proceeds through 4 phases "
            "— **G1** (growth) → **S** (DNA replication) → **G2** "
            "(growth + repair check) → **M** (mitosis + "
            "cytokinesis) — gated by **cyclin / CDK** check-"
            "points.  Mitosis: prophase (chromosome "
            "condensation) → prometaphase (nuclear envelope "
            "breakdown) → metaphase (chromosome alignment on "
            "spindle) → anaphase (sister-chromatid separation "
            "by separase cleaving cohesin) → telophase (nuclear "
            "envelope reforms) → cytokinesis (actomyosin "
            "contractile ring in animals; cell-plate phragmoplast "
            "in plants).  Failure of the spindle-assembly "
            "checkpoint causes aneuploidy — a hallmark of "
            "cancer."
        ),
        cross_reference_cell_component_ids=(
            "microtubule", "centrosome", "centromere-kinetochore",
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-signalling-gpcr",
        kingdom="eukarya",
        subtab="physiology",
        title="GPCR signalling cascades",
        body=(
            "**G-protein-coupled receptors (GPCRs)** are the "
            "largest superfamily of membrane receptors in "
            "eukaryotes (~ 800 in humans) and the target of "
            "~ 35% of FDA-approved drugs.  Heptahelical 7-TM "
            "receptors couple to heterotrimeric Gαβγ proteins "
            "in the inner leaflet — agonist binding triggers "
            "GDP/GTP exchange on Gα, dissociation from Gβγ, and "
            "downstream activation of adenylyl cyclase (Gαs → "
            "cAMP → PKA), phospholipase C (Gαq → IP3 + DAG → "
            "Ca²⁺ + PKC), or Rho-GEFs (Gα12/13 → cytoskeletal "
            "rearrangement).  β-arrestin recruitment desensitises "
            "the receptor + initiates clathrin-mediated "
            "internalisation."
        ),
        cross_reference_cell_component_ids=(
            "eukaryotic-plasma-membrane",),
        cross_reference_molecule_names=(
            "GTP (guanosine-5'-triphosphate)",
            "cAMP (3',5'-cyclic AMP)",
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-development-multicellularity",
        kingdom="eukarya",
        subtab="physiology",
        title="Multicellular development + morphogen gradients",
        sub_domain="animal",
        body=(
            "Multicellular eukaryotes (animals + plants + most "
            "fungi) coordinate development via **morphogen "
            "gradients** — diffusible signalling molecules whose "
            "concentration decay across a tissue specifies "
            "different cell fates at different positions.  "
            "Canonical morphogens: Sonic hedgehog (Shh, neural "
            "tube + limb patterning), Wnt (gut + body-axis "
            "patterning), BMP / TGF-β (dorsoventral patterning), "
            "FGF (limb-bud outgrowth + organogenesis).  In "
            "plants, auxin (indole-3-acetic acid) drives "
            "phototropism + apical dominance via the same "
            "concentration-gradient principle.  Hox genes encode "
            "transcription factors that read morphogen gradients "
            "to establish anterior-posterior body plans."
        ),
        cross_reference_molecule_names=(
            "Indole-3-acetic acid (IAA, auxin)",
        ),
    ),

    # ============================================================
    # EUKARYA — Genetics + Evolution
    # ============================================================
    KingdomTopic(
        id="eukarya-genetics-chromatin-histones",
        kingdom="eukarya",
        subtab="genetics",
        title="Chromatin + nucleosome packaging",
        body=(
            "Eukaryotic DNA is packaged with **histone** proteins "
            "into **nucleosomes** — 147 bp of DNA wrapped 1.65 "
            "turns around an octamer of (H2A · H2B · H3 · H4)₂.  "
            "Linker histone H1 stabilises the higher-order "
            "30-nm fibre.  Histone tails carry post-translational "
            "modifications (acetylation, methylation, "
            "phosphorylation, ubiquitination) that act as the "
            "**'histone code'** read by chromatin remodellers — "
            "the molecular basis of epigenetics.  HDAC inhibitors "
            "like vorinostat were the first epigenetic "
            "anti-cancer drugs."
        ),
        cross_reference_cell_component_ids=("chromatin",),
    ),
    KingdomTopic(
        id="eukarya-genetics-rna-splicing",
        kingdom="eukarya",
        subtab="genetics",
        title="RNA splicing + intron-exon architecture",
        body=(
            "Eukaryotic protein-coding genes are split into "
            "**exons** (coding) + **introns** (non-coding) — a "
            "feature absent in bacteria.  The **spliceosome** "
            "(snRNPs U1 + U2 + U4 + U5 + U6 + ~ 200 protein "
            "factors) catalyses two SN2-like trans-esterification "
            "steps to remove introns + ligate exons.  "
            "**Alternative splicing** dramatically expands the "
            "proteome — a single gene can yield dozens of "
            "different mRNA isoforms (extreme example: "
            "Drosophila Dscam can theoretically generate "
            "~ 38 000 isoforms).  Splicing defects underlie "
            "many genetic diseases (β-thalassemia, spinal "
            "muscular atrophy)."
        ),
    ),
    KingdomTopic(
        id="eukarya-genetics-meiosis-recombination",
        kingdom="eukarya",
        subtab="genetics",
        title="Meiosis + genetic recombination",
        body=(
            "Sexually-reproducing eukaryotes use **meiosis** to "
            "halve chromosome number for gametogenesis.  Two "
            "consecutive divisions (meiosis I + II) follow one "
            "round of DNA replication, generating four haploid "
            "gametes from one diploid precursor.  **Crossing "
            "over** in prophase I — initiated by SPO11-induced "
            "double-strand breaks + repaired via the homologous-"
            "recombination machinery (RAD51, DMC1, MSH4/5) — "
            "shuffles genetic information between maternal and "
            "paternal chromosomes, generating the genetic "
            "diversity that fuels Darwinian selection.  Errors "
            "in meiotic chromosome segregation → aneuploid "
            "embryos (trisomies 13/18/21)."
        ),
    ),
    KingdomTopic(
        id="eukarya-genetics-telomeres-aging",
        kingdom="eukarya",
        subtab="genetics",
        title="Telomeres + replicative senescence",
        body=(
            "Linear eukaryotic chromosomes terminate in "
            "**telomeres** — tandem (TTAGGG)ₙ vertebrate "
            "repeats coated by the **shelterin** complex (TRF1, "
            "TRF2, POT1, TIN2, TPP1, RAP1) and capped in a "
            "**T-loop** structure where the 3' G-rich overhang "
            "invades the duplex.  Each somatic-cell division "
            "shortens the telomere ~ 50-200 bp because of the "
            "end-replication problem — eventually triggering "
            "replicative senescence (the **Hayflick limit**).  "
            "Stem cells + germline cells re-extend telomeres via "
            "**telomerase** (hTERT reverse transcriptase + hTR "
            "RNA template).  Telomerase is up-regulated in "
            "~ 90% of cancers — Blackburn / Greider / Szostak "
            "Nobel 2009."
        ),
        cross_reference_cell_component_ids=("telomere",),
    ),
    KingdomTopic(
        id="eukarya-genetics-endosymbiotic-origin",
        kingdom="eukarya",
        subtab="genetics",
        title="Endosymbiotic origin of eukaryotes",
        body=(
            "The **endosymbiotic theory** (Margulis 1967) holds "
            "that eukaryotic mitochondria descended from an "
            "α-proteobacterium engulfed by an archaeal host, and "
            "chloroplasts descended from a cyanobacterium "
            "engulfed by a primordial photosynthetic eukaryote.  "
            "Evidence: (a) mitochondrial + chloroplast genomes "
            "are circular like bacterial chromosomes; (b) their "
            "ribosomes are 70S like bacteria, sensitive to "
            "macrolides + tetracyclines that don't touch "
            "cytoplasmic 80S; (c) their inner membranes lack "
            "cholesterol; (d) phylogenetic placement of "
            "mitochondrial 16S rRNA within α-proteobacteria; "
            "(e) double membranes (engulfment signature)."
        ),
        cross_reference_cell_component_ids=(
            "mitochondrion", "chloroplast",
        ),
        cross_reference_molecule_names=(
            "Cholesterol",
        ),
    ),

    # ============================================================
    # EUKARYA — Round 169 sub-domain expansion (plant / animal /
    # fungus topics that the original 15 eukarya entries didn't
    # cover at the kingdom-within-Eukarya level)
    # ============================================================
    KingdomTopic(
        id="eukarya-structure-animal-tight-junctions",
        kingdom="eukarya",
        subtab="structure",
        title="Animal cell-cell junctions (tight + adherens "
              "+ desmosomes + gap)",
        sub_domain="animal",
        body=(
            "Animal cells form four canonical junction types "
            "with their neighbours: (a) **tight junctions** "
            "(claudin + occludin transmembrane proteins; ZO-1/2/3 "
            "scaffold) seal epithelial-cell apical-basal "
            "polarity by blocking paracellular diffusion — the "
            "molecular basis of the blood-brain + intestinal "
            "barriers; (b) **adherens junctions** (E-cadherin "
            "Ca²⁺-dependent homotypic binding + α/β-catenin + "
            "actin) provide mechanical adhesion + signal "
            "Wnt/β-catenin destabilisation when broken (a "
            "hallmark of epithelial-mesenchymal transition in "
            "cancer); (c) **desmosomes** (desmoglein + "
            "desmocollin + plakoglobin + plakophilin + "
            "desmoplakin + intermediate filaments) — spot-welds "
            "for mechanical strength, especially in skin + "
            "cardiac muscle (pemphigus = autoimmune attack on "
            "desmoglein 3); (d) **gap junctions** (connexin "
            "hexamers forming hemichannels that dock into "
            "complete channels) for direct cytoplasmic continuity "
            "+ electrical / metabolic coupling — essential for "
            "cardiac action-potential propagation."
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-animal-nervous-system",
        kingdom="eukarya",
        subtab="physiology",
        title="Animal nervous system + neurotransmission",
        sub_domain="animal",
        body=(
            "Animals (and only animals) have a **nervous "
            "system** of electrically-excitable neurons.  The "
            "**resting potential** (~ −70 mV) is set by the "
            "Na⁺/K⁺ ATPase + leaky K⁺ channels.  An **action "
            "potential** is a self-propagating depolarisation "
            "via voltage-gated Na⁺ channels (rapid opening + "
            "inactivation) followed by repolarisation via "
            "voltage-gated K⁺ channels.  At the synaptic "
            "terminal, depolarisation opens voltage-gated Ca²⁺ "
            "channels → Ca²⁺ influx → SNARE-mediated synaptic-"
            "vesicle fusion → neurotransmitter release.  Major "
            "small-molecule neurotransmitters: glutamate "
            "(excitatory, AMPA + NMDA receptors), GABA "
            "(inhibitory, GABA-A Cl⁻ channel + GABA-B GPCR), "
            "acetylcholine (NMJ + parasympathetic), dopamine + "
            "noradrenaline + serotonin (monoamine modulators).  "
            "Drug targets: GABA-A benzodiazepines (Phase 31k SAR "
            "series); SERT SSRIs; D2 antipsychotics; ACh "
            "esterase inhibitors for Alzheimer's."
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-plant-auxin-photoperiodism",
        kingdom="eukarya",
        subtab="physiology",
        title="Plant hormones + photoperiodism",
        sub_domain="plant",
        body=(
            "Plants coordinate growth + development with **five "
            "classical phytohormones**: (a) **auxin** (indole-"
            "3-acetic acid, IAA) drives apical dominance + "
            "phototropism + gravitropism via polar transport "
            "(PIN protein efflux carriers establish "
            "concentration gradients across tissues); (b) "
            "**cytokinin** promotes cell division + delays "
            "senescence — the auxin / cytokinin ratio dictates "
            "shoot-vs-root differentiation in tissue culture; "
            "(c) **gibberellins** trigger stem elongation + "
            "seed germination + flowering; (d) **abscisic acid** "
            "enforces dormancy + stomatal closure under drought; "
            "(e) **ethylene** (the simplest hormone — C₂H₄ gas) "
            "ripens fruit + induces leaf abscission.  "
            "**Photoperiodism**: phytochrome (red / far-red "
            "switch) + cryptochrome (blue light) photoreceptors "
            "let plants sense daylength + season — critical for "
            "flowering time, dormancy, + tropism responses.  "
            "Florigen (FT protein) is the long-distance "
            "flowering signal that travels phloem → shoot apical "
            "meristem."
        ),
        cross_reference_molecule_names=(
            "Indole-3-acetic acid (IAA, auxin)",
        ),
    ),
    KingdomTopic(
        id="eukarya-structure-plant-vascular-tissue",
        kingdom="eukarya",
        subtab="structure",
        title="Plant vascular tissue (xylem + phloem)",
        sub_domain="plant",
        body=(
            "Vascular plants (tracheophytes) evolved two "
            "**conducting-tissue systems** that solved the "
            "problem of moving water + nutrients between roots + "
            "leaves of upright land plants.  **Xylem** carries "
            "water + dissolved minerals UP from roots — composed "
            "of dead, hollow tracheids + vessel elements with "
            "lignified cell walls forming continuous tubes "
            "driven by transpiration-pull (negative pressure at "
            "leaf stomata) + cohesion-tension (hydrogen-bonded "
            "water columns).  **Phloem** carries sucrose + amino "
            "acids + signalling molecules in BOTH directions "
            "(source → sink, e.g. mature leaves → developing "
            "fruits) — composed of living sieve-tube elements + "
            "companion cells + the pressure-flow mechanism "
            "(Münch hypothesis: source loading raises sieve-tube "
            "osmotic pressure; sink unloading lowers it; bulk "
            "flow follows the gradient).  The xylem / phloem "
            "vascular bundle organisation defines monocot vs "
            "dicot anatomy."
        ),
        cross_reference_molecule_names=(
            "Sucrose",
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-fungus-hyphal-growth",
        kingdom="eukarya",
        subtab="physiology",
        title="Fungal hyphal growth + secondary metabolism",
        sub_domain="fungus",
        body=(
            "Fungi grow as **hyphae** — long, branching, "
            "tubular cells that extend at their tips by "
            "**Spitzenkörper-mediated polarised secretion** of "
            "new cell-wall material.  The aggregate of branching "
            "hyphae is the **mycelium** — the largest known "
            "organism on Earth is a single Armillaria ostoyae "
            "mycelium covering 9.6 km² in Oregon's Malheur "
            "National Forest.  Reproductive structures rise from "
            "the mycelium: **mushrooms** (basidiomycete "
            "fruiting bodies), **moulds** (conidiophores), or "
            "**yeasts** (which grow as single cells).  Fungi "
            "are second only to bacteria as natural-product-"
            "drug sources: penicillins from *Penicillium*, "
            "cyclosporine + ergot alkaloids from *Claviceps* + "
            "*Tolypocladium*, lovastatin (the prototype statin) "
            "from *Aspergillus terreus*, griseofulvin "
            "antifungal from *Penicillium*.  Many fungi form "
            "**mycorrhizal symbioses** with > 80% of plant "
            "species — exchanging fixed phosphate / nitrogen "
            "for plant-derived sugars at the root interface."
        ),
    ),
    KingdomTopic(
        id="eukarya-genetics-fungus-mating-types",
        kingdom="eukarya",
        subtab="genetics",
        title="Fungal mating types + sexual reproduction",
        sub_domain="fungus",
        body=(
            "Fungi don't have male / female sexes — they have "
            "**mating types** (MAT loci) that determine "
            "compatibility for sexual reproduction.  In "
            "*Saccharomyces cerevisiae* there are two mating "
            "types (MATa and MATα) that fuse to form a "
            "**diploid** that can sporulate via meiosis to "
            "regenerate haploid offspring.  Many basidiomycetes "
            "have **tetrapolar mating systems** — two unlinked "
            "MAT loci create 4 + mating types per species "
            "(*Schizophyllum commune* has > 23 000 mating "
            "types from this combinatorial logic).  The "
            "**parasexual cycle** (Pontecorvo 1956) in "
            "filamentous fungi like *Aspergillus* allows "
            "haploid-diploid-haploid genetic exchange WITHOUT "
            "meiosis — somatic cell fusion → diploid hyphal "
            "cell → mitotic crossing-over → haploidisation by "
            "sequential chromosome loss.  Drives fungicide "
            "resistance in agricultural pathogens."
        ),
    ),
    KingdomTopic(
        id="eukarya-physiology-animal-immune-system",
        kingdom="eukarya",
        subtab="physiology",
        title="Animal immune system — innate + adaptive",
        sub_domain="animal",
        body=(
            "Animals (especially vertebrates) defend against "
            "pathogens with a two-arm **immune system**.  "
            "**Innate immunity** is fast (minutes-hours) + "
            "non-specific: PAMP-recognising Toll-like receptors "
            "(TLRs) on macrophages + dendritic cells trigger "
            "phagocytosis + cytokine release; the complement "
            "cascade (C1-C9) opsonises pathogens + assembles "
            "MAC pores; NK cells kill virus-infected + tumour "
            "cells via missing-self recognition.  **Adaptive "
            "immunity** is slow (days-weeks) but pathogen-"
            "specific + memory-forming: **B cells** make "
            "antibodies (IgM → IgG class-switched + affinity-"
            "matured by somatic hypermutation in germinal "
            "centres), **CD4⁺ T-helper cells** orchestrate the "
            "response, **CD8⁺ cytotoxic T cells** kill "
            "infected cells via MHC-I peptide presentation.  "
            "Vaccines exploit memory B + T cells; checkpoint-"
            "inhibitor cancer immunotherapy (anti-PD-1 / "
            "anti-CTLA-4) releases T cells from tumour-induced "
            "exhaustion (Honjo + Allison Nobel 2018)."
        ),
    ),
    KingdomTopic(
        id="eukarya-genetics-plant-polyploidy",
        kingdom="eukarya",
        subtab="genetics",
        title="Plant polyploidy + genome doubling",
        sub_domain="plant",
        body=(
            "**Polyploidy** — having more than two complete sets "
            "of chromosomes — is **rare in animals** (lethal in "
            "most vertebrate embryos) but **extremely common in "
            "plants**: ~ 70% of all flowering-plant species "
            "have undergone at least one round of whole-genome "
            "duplication in their evolutionary history.  Modern "
            "wheat is **hexaploid** (AABBDD, 6 × 7 = 42 "
            "chromosomes — three ancestral diploid genomes "
            "fused over ~ 10 000 years of agriculture).  "
            "Modern strawberry is **octoploid**.  Polyploidy "
            "drives **plant speciation** + **agronomic "
            "improvement** (larger fruits, increased vigour, "
            "abiotic-stress tolerance).  Two mechanisms: "
            "**autopolyploidy** (genome doubling within a "
            "species, e.g. unreduced gametes) and "
            "**allopolyploidy** (interspecific hybrid + "
            "subsequent genome doubling — accounts for wheat, "
            "cotton, oilseed rape).  Polyploidy is the "
            "evolutionary fast lane plants use that animals "
            "can't tolerate."
        ),
    ),

    # ============================================================
    # BACTERIA — Structure
    # ============================================================
    KingdomTopic(
        id="bacteria-structure-gram-stain-divide",
        kingdom="bacteria",
        subtab="structure",
        title="Gram-positive vs Gram-negative envelope",
        body=(
            "The **gram stain** (Christian Gram 1884) divides "
            "bacteria by envelope architecture.  **Gram-positive** "
            "bacteria have a thick (~ 20-80 nm) peptidoglycan "
            "sacculus outside a single plasma membrane, retain "
            "crystal violet, and are typically vulnerable to "
            "β-lactams + vancomycin.  **Gram-negative** bacteria "
            "have a thin (~ 7-8 nm) peptidoglycan layer in a "
            "**periplasmic space** between an inner plasma "
            "membrane and an outer membrane studded with porins "
            "+ LPS endotoxin — they don't retain crystal violet "
            "and are intrinsically resistant to many "
            "antibiotics that can't cross the outer membrane."
        ),
        cross_reference_cell_component_ids=(
            "peptidoglycan-gram-positive",
            "peptidoglycan-gram-negative",
            "outer-membrane-gram-negative",
        ),
    ),
    KingdomTopic(
        id="bacteria-structure-no-organelles",
        kingdom="bacteria",
        subtab="structure",
        title="Prokaryotic minimalism — no membrane-bound "
              "organelles",
        body=(
            "Bacteria have **no membrane-bound organelles**: "
            "transcription + translation are coupled in the "
            "cytoplasm (the ribosome can begin translating an "
            "mRNA before RNA polymerase has finished "
            "transcribing it), the genome sits unenveloped in "
            "the **nucleoid**, and ATP is generated at the "
            "plasma membrane (no mitochondria — the membrane IS "
            "the ETC + ATP-synthase host).  Rare exceptions: "
            "magnetotactic bacteria with **magnetosomes** (Fe₃O₄ "
            "crystals in lipid vesicles), photosynthetic "
            "cyanobacteria with **carboxysomes** (RuBisCO + "
            "carbonic-anhydrase compartments), and acidocalcisomes "
            "in some pathogens."
        ),
        cross_reference_cell_component_ids=(
            "bacterial-plasma-membrane", "bacterial-nucleoid",
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
    ),
    KingdomTopic(
        id="bacteria-structure-flagellum-motor",
        kingdom="bacteria",
        subtab="structure",
        title="Bacterial flagellar rotary motor",
        body=(
            "The **bacterial flagellum** is a self-assembling "
            "rotary motor — ~ 100 Hz in *E. coli* — driven by "
            "the proton-motive force (or, in marine species, "
            "Na⁺-motive force) across the inner membrane.  Three "
            "structural domains: (a) the **basal body** (MotA/B "
            "stator + FliG/M/N rotor + bushings through both "
            "membranes); (b) the **hook** (FlgE flexible "
            "universal joint); (c) the **filament** (FliC self-"
            "assembling helical tube, ~ 20 µm long).  Switching "
            "between counter-clockwise (smooth swimming) + "
            "clockwise (tumbling) rotation underlies "
            "chemotaxis.  Behe's irreducible-complexity poster-"
            "child has been thoroughly rebutted by stepwise "
            "evolution from a Type-III secretion ancestor."
        ),
        cross_reference_cell_component_ids=("bacterial-flagellum",),
    ),
    KingdomTopic(
        id="bacteria-structure-biofilms",
        kingdom="bacteria",
        subtab="structure",
        title="Biofilms + extracellular polymeric substances",
        body=(
            "Most bacteria in nature live in **biofilms** — "
            "dense surface-attached communities embedded in a "
            "self-produced matrix of **extracellular polymeric "
            "substances (EPS)**: exopolysaccharides (Pel, Psl, "
            "alginate in Pseudomonas), extracellular DNA "
            "(eDNA), amyloid-like fimbriae proteins, and water "
            "channels.  Biofilm cells are typically 100-1 000 "
            "× more antibiotic-tolerant than planktonic cells "
            "of the same species — partly via slow growth + "
            "physical drug exclusion + persister-cell physiology.  "
            "Medically critical biofilms: dental plaque, "
            "indwelling-catheter infections, chronic-wound "
            "polymicrobial communities, cystic-fibrosis lung "
            "*P. aeruginosa*, prosthetic-joint infections."
        ),
        cross_reference_cell_component_ids=("biofilm-eps",),
    ),
    KingdomTopic(
        id="bacteria-structure-capsule-virulence",
        kingdom="bacteria",
        subtab="structure",
        title="Capsule + virulence",
        body=(
            "Many pathogenic bacteria secrete a **polysaccharide "
            "capsule** outside the cell wall that blocks "
            "phagocytosis + complement deposition.  Capsular "
            "polysaccharides are **strain-defining**: "
            "*Streptococcus pneumoniae* has > 90 distinct "
            "capsular serotypes, the basis of the PCV13 / "
            "PCV20 conjugate vaccines that target the most "
            "invasive serotypes.  Other notable capsules: "
            "*Haemophilus influenzae* type b (Hib vaccine), "
            "*Neisseria meningitidis* groups A/B/C/W/Y "
            "(meningococcal vaccines), *Klebsiella pneumoniae* "
            "K1/K2 hypervirulent capsules, *Bacillus anthracis* "
            "**poly-γ-glutamate** (the only bacterial capsule "
            "that's protein-based, not polysaccharide)."
        ),
        cross_reference_cell_component_ids=("bacterial-capsule",),
    ),

    # ============================================================
    # BACTERIA — Physiology + Development
    # ============================================================
    KingdomTopic(
        id="bacteria-physiology-anaerobic-fermentation",
        kingdom="bacteria",
        subtab="physiology",
        title="Anaerobic fermentation + diverse electron "
              "acceptors",
        body=(
            "Bacteria collectively evolved every metabolic "
            "strategy life uses on Earth.  Beyond the eukaryotic "
            "O₂ / NADH-respiratory paradigm, bacteria can "
            "respire anaerobically using nitrate, sulfate, "
            "iron(III), CO₂, fumarate, and even toxic metals as "
            "terminal electron acceptors.  Fermentative bacteria "
            "regenerate NAD⁺ by reducing pyruvate → lactate "
            "(*Lactobacillus*, muscle), pyruvate → acetaldehyde "
            "→ ethanol + CO₂ (*Saccharomyces* — yeast — "
            "actually a eukaryote, but the same chemistry runs "
            "in *Zymomonas*), pyruvate → propionate / butyrate / "
            "acetate (gut microbiome short-chain fatty acids "
            "with documented host-physiology effects)."
        ),
        cross_reference_pathway_ids=("glycolysis",),
        cross_reference_molecule_names=(
            "NADH",
            "Pyruvate",
            "Ethanol",
            "Fumarate",
        ),
    ),
    KingdomTopic(
        id="bacteria-physiology-binary-fission",
        kingdom="bacteria",
        subtab="physiology",
        title="Binary fission + FtsZ-Z-ring division",
        body=(
            "Bacteria divide by **binary fission**: replicated "
            "daughter chromosomes segregate to opposite cell "
            "poles, then a **FtsZ-Z-ring** assembles at midcell "
            "and drives constriction of the inner membrane + "
            "peptidoglycan synthesis machinery (the divisome) "
            "to pinch the cell in two.  FtsZ is the bacterial "
            "homologue of eukaryotic tubulin — same GTPase fold, "
            "different polymerisation geometry.  Doubling times "
            "vary across 3 orders of magnitude: *V. natriegens* "
            "~ 10 min, *E. coli* in rich medium ~ 20 min, "
            "*M. tuberculosis* ~ 24 h, *M. leprae* ~ 14 days "
            "(slowest known among free-living bacteria — "
            "drives the year-long leprosy treatment regimens)."
        ),
    ),
    KingdomTopic(
        id="bacteria-physiology-quorum-sensing",
        kingdom="bacteria",
        subtab="physiology",
        title="Quorum sensing + density-dependent group "
              "behaviour",
        body=(
            "Bacteria coordinate density-dependent behaviours "
            "(biofilm formation, virulence-factor secretion, "
            "antibiotic + bioluminescent compound production, "
            "competence for DNA uptake) by **quorum sensing** — "
            "secreting + sensing diffusible **autoinducer** "
            "molecules whose accumulated concentration reports "
            "local cell density.  Gram-negative species use "
            "**N-acyl homoserine lactones (AHLs)** like 3-oxo-"
            "C12-HSL in *P. aeruginosa*; gram-positives use "
            "**autoinducing peptides (AIPs)** like the *S. "
            "aureus* agr quorum-sensing peptides; both kingdoms "
            "share **autoinducer-2 (AI-2 / DPD)** as a cross-"
            "species signal.  Quorum-quenching enzymes + "
            "quorum-blocking small molecules are an active anti-"
            "virulence drug-discovery space."
        ),
    ),
    KingdomTopic(
        id="bacteria-physiology-sporulation",
        kingdom="bacteria",
        subtab="physiology",
        title="Endospore formation + dormancy",
        body=(
            "Some Gram-positive genera (*Bacillus*, "
            "*Clostridium*, *Geobacillus*) survive lethal "
            "conditions by forming **endospores** — dormant, "
            "dehydrated, multi-coated cells that resist heat "
            "(autoclaving 121 °C for ≥ 15 min is the standard "
            "endospore-kill cycle), UV, desiccation, + many "
            "disinfectants.  Sporulation is a 7-stage "
            "developmental programme triggered by nutrient "
            "limitation: asymmetric division → forespore "
            "engulfment → cortex + coat synthesis → mother-cell "
            "lysis → mature endospore.  Endospores contain "
            "**dipicolinic acid (DPA)** chelated to Ca²⁺ — "
            "~ 10% of dry weight — that displaces water + "
            "stabilises macromolecules.  Anthrax + tetanus + "
            "botulism + *C. difficile* infections all rely on "
            "endospore persistence."
        ),
    ),
    KingdomTopic(
        id="bacteria-physiology-secondary-metabolites",
        kingdom="bacteria",
        subtab="physiology",
        title="Secondary metabolism + natural-product "
              "antibiotics",
        body=(
            "Bacteria — especially soil-dwelling actinomycetes "
            "(*Streptomyces*) — produce vast libraries of "
            "**secondary metabolites** that don't directly "
            "support growth but mediate inter-species competition "
            "and defence.  This biosynthetic capacity is the "
            "single largest historical source of human medicines: "
            "penicillins (*Penicillium*, technically a fungus), "
            "cephalosporins (*Acremonium*), tetracyclines + "
            "macrolides + aminoglycosides + glycopeptides "
            "(vancomycin) + polyketides (rapamycin → mTOR "
            "inhibitor sirolimus + everolimus + temsirolimus) + "
            "non-ribosomal peptides (cyclosporine — fungal — and "
            "actinomycin D) + ansamycins (rifampin) all come "
            "from microbial secondary metabolism."
        ),
    ),

    # ============================================================
    # BACTERIA — Genetics + Evolution
    # ============================================================
    KingdomTopic(
        id="bacteria-genetics-circular-genome",
        kingdom="bacteria",
        subtab="genetics",
        title="Circular chromosome + nucleoid organisation",
        body=(
            "Bacterial genomes are typically a **single circular "
            "chromosome** (1-10 Mbp; *E. coli* K-12 ~ 4.6 Mbp) "
            "supercoiled by **DNA gyrase** (topoisomerase II — "
            "fluoroquinolone target) + relaxed by topoisomerase I "
            "and packaged with nucleoid-associated proteins (HU, "
            "IHF, Fis, H-NS) into ~ 400 topological domains.  "
            "Replication initiates at a single **oriC** site and "
            "proceeds bidirectionally to converge at the "
            "**terC** terminator.  No introns + no histones + "
            "polycistronic operons → coupled transcription-"
            "translation: the ribosome can begin synthesising "
            "the protein before the mRNA is finished."
        ),
        cross_reference_cell_component_ids=("bacterial-nucleoid",),
    ),
    KingdomTopic(
        id="bacteria-genetics-horizontal-gene-transfer",
        kingdom="bacteria",
        subtab="genetics",
        title="Horizontal gene transfer (HGT) — transformation, "
              "transduction, conjugation",
        body=(
            "Bacterial evolution is dominated by **horizontal "
            "gene transfer** between unrelated species — vertical "
            "Darwinian descent is supplemented (sometimes "
            "overshadowed) by lateral acquisition of fitness "
            "genes.  Three mechanisms: (a) **transformation** — "
            "uptake of naked environmental DNA via competence "
            "machinery (*S. pneumoniae*, *B. subtilis*, "
            "*N. gonorrhoeae*); (b) **transduction** — DNA "
            "transfer via bacteriophage particles (generalised "
            "+ specialised); (c) **conjugation** — direct "
            "cell-to-cell DNA transfer via a sex pilus + Type-IV "
            "secretion system, encoded by conjugative plasmids "
            "(F-factor) or integrative + conjugative elements "
            "(ICEs).  HGT is the engine of **antibiotic-"
            "resistance spread** (β-lactamases, NDM-1 carbapenem-"
            "resistance, mcr-1 colistin-resistance all dispersed "
            "globally on plasmids in < 5 years)."
        ),
        cross_reference_cell_component_ids=(
            "bacterial-plasmid", "pilus-fimbria",
        ),
    ),
    KingdomTopic(
        id="bacteria-genetics-crispr-defence",
        kingdom="bacteria",
        subtab="genetics",
        title="CRISPR-Cas adaptive immunity",
        body=(
            "Bacteria + archaea defend against bacteriophages + "
            "plasmid invasion using **CRISPR-Cas adaptive "
            "immunity**: short fragments (~ 30 bp 'spacers') "
            "of invading DNA are integrated into the host's "
            "**CRISPR (Clustered Regularly Interspaced Short "
            "Palindromic Repeats)** locus, transcribed into "
            "guide RNAs, and used by Cas nucleases to cleave any "
            "future invader carrying a matching protospacer.  "
            "Repurposed as a **genome-editing tool** by Doudna + "
            "Charpentier 2012 (Nobel 2020) — Cas9 + a programmed "
            "guide RNA can introduce a double-strand break at "
            "any genomic locus that carries a matching 20 bp + "
            "PAM motif, revolutionising biology + (in 2023) "
            "achieving the first FDA-approved CRISPR therapy "
            "(Casgevy for sickle-cell disease)."
        ),
    ),
    KingdomTopic(
        id="bacteria-genetics-restriction-modification",
        kingdom="bacteria",
        subtab="genetics",
        title="Restriction-modification systems",
        body=(
            "Bacteria + archaea evolved **restriction-"
            "modification (R-M) systems** — bacterial 'innate "
            "immunity' against foreign DNA — long before CRISPR.  "
            "The host **methylates** specific recognition "
            "sequences in its own genome (typically 4-8 bp "
            "palindromes) using a methyltransferase; a paired "
            "**restriction endonuclease** cleaves any unmethylated "
            "DNA at the same recognition sequence — typically "
            "phage DNA from a non-self host.  Biology's first "
            "molecular-cloning workhorses: EcoRI (G^AATTC), "
            "BamHI (G^GATCC), HindIII (A^AGCTT), NotI (GC^GGCCGC) "
            "all come from R-M systems.  Smith + Nathans + "
            "Arber Nobel 1978 for the discovery."
        ),
    ),
    KingdomTopic(
        id="bacteria-genetics-evolutionary-rate",
        kingdom="bacteria",
        subtab="genetics",
        title="Evolutionary rate + mutation generation",
        body=(
            "Bacteria evolve rapidly because they (a) have "
            "short generation times (20 min for *E. coli* in "
            "rich medium → 72 generations / day → 25 000 "
            "generations / year, vs ~ 4 human generations / "
            "century), (b) have huge population sizes (10^9 "
            "*E. coli* per gram of human stool → mutation "
            "frequency ~ 10⁻⁹ per bp per division means EVERY "
            "single-nucleotide variant is generated daily within "
            "one human gut), and (c) acquire pre-evolved fitness "
            "genes via HGT.  These three forces explain why "
            "antibiotic resistance emerges within ~ 1-5 years of "
            "any new antibiotic's clinical introduction — "
            "inevitable given the math."
        ),
    ),

    # ============================================================
    # ARCHAEA — Structure
    # ============================================================
    KingdomTopic(
        id="archaea-structure-ether-lipids",
        kingdom="archaea",
        subtab="structure",
        title="Ether-linked isoprenoid lipids — the lipid divide",
        body=(
            "**The lipid divide is the single strongest "
            "molecular argument for the three-domain phylogeny.** "
            "Bacterial + eukaryotic membranes are bilayers of "
            "**ester-linked** acyl-glycerol-3-phosphate "
            "phospholipids; archaeal membranes are bilayers (or "
            "monolayers, in hyperthermophiles) of **ether-linked** "
            "phytanyl-glycerol-1-phosphate phospholipids — "
            "**different stereochemistry of the glycerol "
            "backbone, different hydrocarbon tails (isoprenoid "
            "vs fatty acid), different linkage chemistry**.  "
            "Ether bonds + branched isoprenoid tails are far "
            "more stable than ester-fatty-acid combinations under "
            "extreme heat (110 °C+), pH (1-12), or salinity, "
            "explaining why so many extremophiles are archaea."
        ),
        cross_reference_cell_component_ids=(
            "archaeal-plasma-membrane",),
    ),
    KingdomTopic(
        id="archaea-structure-pseudopeptidoglycan",
        kingdom="archaea",
        subtab="structure",
        title="Pseudopeptidoglycan + S-layer envelopes",
        body=(
            "Archaea evolved alternative cell-wall chemistries "
            "to bacterial peptidoglycan.  Methanogens use "
            "**pseudopeptidoglycan (pseudomurein)** — N-acetyl-"
            "talosaminuronic acid (NAT) instead of N-acetyl-"
            "muramic acid (NAM), β-1,3 instead of β-1,4 "
            "glycosidic linkages, L-amino acids instead of "
            "D-amino acids in the stem peptide.  These changes "
            "make pseudopeptidoglycan **resistant to lysozyme + "
            "β-lactam antibiotics**, both of which target "
            "bacterial NAM-NAG-D-AA chemistry.  Many archaea "
            "lack a sacculus altogether and rely on a 2D "
            "crystalline **S-layer** of glycoprotein subunits — "
            "the most abundant cell envelope on Earth, present "
            "in many bacteria too."
        ),
        cross_reference_cell_component_ids=(
            "pseudopeptidoglycan", "s-layer",
        ),
    ),
    KingdomTopic(
        id="archaea-structure-extremophile-adaptations",
        kingdom="archaea",
        subtab="structure",
        title="Extremophile adaptations across archaea",
        body=(
            "Many archaea inhabit conditions lethal to most "
            "bacteria + every eukaryote.  **Hyperthermophiles** "
            "(*Pyrolobus fumarii* growth limit 113 °C; "
            "*Methanopyrus kandleri* 122 °C) use ether-linked "
            "tetraether monolayer membranes + thermostable "
            "histone-like proteins + reverse gyrase to maintain "
            "DNA integrity.  **Halophiles** (*Halobacterium* up "
            "to 5 M NaCl) accumulate K⁺ to 4 M intracellular + "
            "use 'salt-in' acidic-residue-rich proteins.  "
            "**Acidophiles** (*Picrophilus* growth optimum "
            "pH 0.7) maintain near-neutral cytoplasm via active "
            "proton extrusion + impermeable membranes.  "
            "**Methanogens** are exclusively archaeal (no known "
            "bacterial methanogens) — the largest source of "
            "atmospheric CH₄."
        ),
    ),
    KingdomTopic(
        id="archaea-structure-archaellum",
        kingdom="archaea",
        subtab="structure",
        title="The archaellum — convergent rotary motor",
        body=(
            "Archaeal motility uses the **archaellum** — once "
            "called the 'archaeal flagellum' but renamed once it "
            "became clear it's not homologous to the bacterial "
            "flagellum at all.  The bacterial flagellum is "
            "related to the Type-III secretion injectisome + "
            "uses proton-motive force; the archaellum is "
            "evolutionarily related to **Type-IV pili** + "
            "uses **ATP** (FlaI ATPase) for rotation.  Filament "
            "assembly grows from the base (opposite of bacterial "
            "flagella, which grow from the tip via secreted "
            "monomers travelling through the central channel).  "
            "**Convergent evolution** of rotary nano-motors — "
            "two completely distinct molecular machines doing "
            "the same job."
        ),
        cross_reference_cell_component_ids=("archaeal-flagellum",),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
    ),
    KingdomTopic(
        id="archaea-structure-no-organelles",
        kingdom="archaea",
        subtab="structure",
        title="Cellular minimalism (like bacteria)",
        body=(
            "Like bacteria, archaea lack membrane-bound "
            "organelles.  Their cytoplasm contains a free "
            "nucleoid + 70S ribosomes + a single plasma "
            "membrane that hosts the electron-transport "
            "machinery (in respiratory species) + ATP synthase.  "
            "Yet many of their molecular details are **eukaryote-"
            "like**: archaeal histones + RNA polymerase + DNA "
            "replication factors (the MCM helicase, the "
            "Replication Factor C clamp loader, PCNA sliding "
            "clamp) all share homology with their eukaryotic "
            "counterparts rather than with bacterial equivalents."
        ),
        cross_reference_cell_component_ids=(
            "archaeal-nucleoid", "archaeal-ribosome",
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
    ),

    # ============================================================
    # ARCHAEA — Physiology + Development
    # ============================================================
    KingdomTopic(
        id="archaea-physiology-methanogenesis",
        kingdom="archaea",
        subtab="physiology",
        title="Methanogenesis — exclusively archaeal energy "
              "metabolism",
        body=(
            "**Methanogenesis** — the reduction of CO₂, acetate, "
            "or methylamines to **methane** as the terminal "
            "step of energy metabolism — is the only metabolic "
            "pathway found ONLY in archaea.  All known "
            "methanogens are members of Euryarchaeota: "
            "*Methanobacteriales*, *Methanococcales*, "
            "*Methanomicrobiales*, *Methanosarcinales*.  Three "
            "substrate classes: (a) CO₂ + H₂ "
            "(hydrogenotrophic — most cattle rumen + termite gut "
            "methanogens), (b) acetate "
            "(acetoclastic — *Methanosarcina*, dominant in "
            "anaerobic digesters), (c) methylated compounds "
            "(methylotrophic — methanol, methylamines).  Global "
            "scale: methanogens generate ~ 1 Gt CH₄ / year — "
            "the dominant atmospheric methane source + a major "
            "climate-change driver."
        ),
        cross_reference_molecule_names=(
            "Methane",
        ),
    ),
    KingdomTopic(
        id="archaea-physiology-no-pathogens",
        kingdom="archaea",
        subtab="physiology",
        title="No known archaeal human pathogens",
        body=(
            "**No verified archaeal human pathogens have ever "
            "been described** — a remarkable epidemiological "
            "anomaly given that archaea are present in human "
            "gut + oral + skin microbiomes (*Methanobrevibacter "
            "smithii* is the dominant archaeal gut commensal).  "
            "Hypotheses for this immunological invisibility "
            "include (a) lack of pathogen-associated molecular "
            "patterns recognised by Toll-like receptors, (b) "
            "absence of secreted toxins, (c) slower growth "
            "than competing bacterial pathogens, (d) tight "
            "metabolic specialisation that doesn't fit any "
            "human-tissue niche.  Methanogens are weakly "
            "implicated in periodontitis + bowel diseases as "
            "syntrophic partners of bacterial pathogens, but "
            "no direct archaeal disease has been proven."
        ),
    ),
    KingdomTopic(
        id="archaea-physiology-syntrophic-partners",
        kingdom="archaea",
        subtab="physiology",
        title="Syntrophic partnerships with bacteria",
        body=(
            "Many archaeal methanogens live as obligate "
            "**syntrophs** with H₂-producing bacterial partners "
            "— neither species can grow alone, but together "
            "they create a thermodynamically favourable "
            "metabolism.  **Anaerobic oxidation of methane "
            "(AOM)** at deep-sea cold seeps is the inverse "
            "syntrophy: ANME-1/2/3 archaea oxidise methane, "
            "transferring electrons to sulfate-reducing "
            "bacterial partners that reduce SO₄²⁻ to HS⁻.  "
            "Together they consume an estimated 80% of the "
            "methane produced in marine sediments — the largest "
            "atmospheric-methane filter on Earth.  These "
            "obligate-syntrophic + obligate-anaerobic lifestyles "
            "explain why archaeal cultures took decades longer "
            "than bacterial cultures to bring into the lab."
        ),
        cross_reference_molecule_names=(
            "Methane",
        ),
    ),
    KingdomTopic(
        id="archaea-physiology-bacteriorhodopsin",
        kingdom="archaea",
        subtab="physiology",
        title="Bacteriorhodopsin + light-driven proton pumps",
        body=(
            "Halophilic archaea like *Halobacterium salinarum* "
            "express **bacteriorhodopsin** — a 7-TM membrane "
            "protein with a covalently-bound retinal chromophore "
            "that pumps protons across the membrane in response "
            "to green light (~ 568 nm absorption).  This is the "
            "**simplest known light-driven energy-conversion "
            "system in biology** — a single protein generates a "
            "proton gradient that ATP synthase converts to ATP, "
            "no complex electron-transport chain required.  "
            "Bacteriorhodopsin is the founder of the rhodopsin "
            "superfamily — homologous to vertebrate visual "
            "rhodopsin + the channelrhodopsins that revolutionised "
            "neuroscience as **optogenetics tools** (Boyden + "
            "Deisseroth + Nagel et al. 2005)."
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
    ),
    KingdomTopic(
        id="archaea-physiology-cold-loving-psychrophiles",
        kingdom="archaea",
        subtab="physiology",
        title="Psychrophilic + acidophilic archaea",
        body=(
            "Although archaea are famous for thermophily, many "
            "thrive at the OPPOSITE extreme.  **Psychrophilic** "
            "archaea like *Methanococcoides burtonii* (Antarctic "
            "Ace Lake) grow at -2 to 28 °C using cold-adapted "
            "ribosomes + cold-shock proteins + unsaturated "
            "ether-lipid tails for membrane fluidity at low "
            "temperatures.  **Acidophilic** archaea like "
            "*Picrophilus oshimae* + *Ferroplasma acidiphilum* "
            "grow at pH 0.7 (more acidic than gastric juice) by "
            "actively pumping protons out + using cytoplasmic "
            "pH-buffering systems + acid-stable enzymes.  "
            "*Ferroplasma acidiphilum* lives in acid-mine drainage "
            "and is studied as a model for acid-tolerance "
            "engineering of industrial fermentation hosts."
        ),
    ),

    # ============================================================
    # ARCHAEA — Genetics + Evolution
    # ============================================================
    KingdomTopic(
        id="archaea-genetics-eukaryote-like-machinery",
        kingdom="archaea",
        subtab="genetics",
        title="Eukaryote-like transcription + translation "
              "machinery",
        body=(
            "Archaea look bacterial on the outside (no organelles, "
            "single circular chromosome, 70S ribosome) but are "
            "**eukaryote-like** in their information-processing "
            "machinery: (a) RNA polymerase has 12-13 subunits "
            "homologous to eukaryotic RNA Pol II, not the "
            "5-subunit bacterial RNAP; (b) transcription factors "
            "TBP + TFB are eukaryotic homologues; (c) translation "
            "initiation factors (aIF1, aIF2, aIF5, aIF6) are "
            "eukaryote-like; (d) DNA replication uses MCM "
            "helicase + RFC clamp loader + PCNA sliding clamp + "
            "FEN1 flap endonuclease — all eukaryotic homologues, "
            "not bacterial DnaB / β-clamp.  This is part of the "
            "evidence that **eukaryotes evolved from within "
            "the Archaea** (the **eocyte tree** + the recent "
            "**Asgard-archaea** discovery)."
        ),
        cross_reference_cell_component_ids=("archaeal-ribosome",),
    ),
    KingdomTopic(
        id="archaea-genetics-archaeal-histones",
        kingdom="archaea",
        subtab="genetics",
        title="Archaeal histones + chromatin precursors",
        body=(
            "Many archaea (Euryarchaeota especially) package "
            "their DNA with **archaeal histones** (HMfA / HMfB "
            "in *Methanothermus fervidus*) that form **tetrameric "
            "mini-nucleosomes** wrapping ~ 60 bp of DNA.  "
            "Structural superposition shows archaeal histones are "
            "homologous to the eukaryotic (H3-H4)₂ tetramer "
            "core — without the H2A/H2B addition.  This makes "
            "archaeal histones the likely **evolutionary "
            "precursor of eukaryotic chromatin**.  Archaea "
            "also have a **homopolymeric Alba protein** that "
            "binds dsDNA non-specifically + acts as a chromatin "
            "scaffold in lineages without histones.  Recent "
            "Asgard-archaea genomes encode H3 + H4 + H2A + H2B "
            "homologues — the closest known prokaryotic "
            "approach to eukaryotic chromatin."
        ),
        cross_reference_cell_component_ids=("archaeal-nucleoid",),
    ),
    KingdomTopic(
        id="archaea-genetics-asgard-eocyte",
        kingdom="archaea",
        subtab="genetics",
        title="Asgard archaea + the eocyte hypothesis of "
              "eukaryogenesis",
        body=(
            "**The eocyte hypothesis** — that eukaryotes "
            "**evolved from within the archaeal domain** rather "
            "than as a sister group — was proposed in the 1980s "
            "by James Lake but only definitively supported in "
            "2015-2017 by the discovery of **Asgard archaea** "
            "(*Lokiarchaeota*, *Thorarchaeota*, *Odinarchaeota*, "
            "*Heimdallarchaeota*) in deep-sea sediments.  Asgard "
            "genomes encode > 100 'eukaryotic-signature proteins' "
            "(actins, profilins, tubulins, ESCRT membrane-"
            "remodelling complex, ubiquitin-system components, "
            "small GTPases, Sec23/24 vesicle-coat proteins) that "
            "were previously thought to be eukaryote-only.  In "
            "2020, Imachi et al. cultured the first Asgard "
            "archaeon — *Prometheoarchaeum syntrophicum* MK-D1 — "
            "in the lab, observing tentacle-like cell projections "
            "consistent with primitive phagocytosis."
        ),
    ),
    KingdomTopic(
        id="archaea-genetics-crispr-defence",
        kingdom="archaea",
        subtab="genetics",
        title="Archaeal CRISPR-Cas systems",
        body=(
            "**CRISPR-Cas immunity is widespread in archaea** — "
            "in fact about 90% of archaeal genomes carry CRISPR "
            "arrays vs ~ 40% of bacterial genomes.  The "
            "**Cas9 enzyme** repurposed for genome editing came "
            "from *Streptococcus pyogenes* (a bacterium), but "
            "many alternative Cas-protein families with "
            "different PAM requirements + cleavage geometries "
            "(Cas12a / Cpf1, Cas13 RNA-targeting, Cas3 "
            "processive degradation, Cascade complex) come from "
            "archaea + bacterial lineages with different defence "
            "strategies against their own viruses.  The "
            "diversity of archaeal viruses (rod-, spindle-, "
            "lemon-, droplet-shaped morphologies unknown in "
            "bacteriophages) drove evolution of equally diverse "
            "CRISPR variants."
        ),
    ),
    KingdomTopic(
        id="archaea-genetics-evolutionary-ancientness",
        kingdom="archaea",
        subtab="genetics",
        title="Deep evolutionary roots + LUCA reconstructions",
        body=(
            "Archaea are typically the deepest-branching domain "
            "in **rooted Tree-of-Life** reconstructions, "
            "consistent with **LUCA** (Last Universal Common "
            "Ancestor) being a thermophilic chemoautotroph "
            "resembling modern hydrothermal-vent archaea.  "
            "Comparative-genomics inference of LUCA's gene "
            "content (Weiss et al. 2016 used the criterion of "
            "presence in both deep-branching bacterial + archaeal "
            "lineages) yielded ~ 355 genes consistent with an "
            "anaerobic, thermophilic, autotrophic lifestyle "
            "near alkaline hydrothermal vents — supporting the "
            "**alkaline-vent hypothesis** of life's origin "
            "(Russell + Martin)."
        ),
    ),

    # ============================================================
    # VIRUSES — Structure
    # ============================================================
    KingdomTopic(
        id="viruses-structure-capsid-architectures",
        kingdom="viruses",
        subtab="structure",
        title="Capsid architectures — icosahedral, helical, "
              "complex",
        body=(
            "Viruses package their genome inside a **protein "
            "capsid** built from many copies of one or a few "
            "structural proteins.  Three canonical "
            "architectures: (a) **icosahedral** (T = 1 to T = "
            "169) — adenovirus, picornaviruses, hepatitis B + C, "
            "papillomaviruses; (b) **helical** — TMV, influenza, "
            "rabies, Ebola; (c) **complex** with multiple "
            "morphological domains — bacteriophage T4 with its "
            "icosahedral head + helical tail + base plate + tail "
            "fibers; poxviruses; mimiviruses.  **Caspar-Klug "
            "quasi-equivalence** (1962) explained how a single "
            "small protein can build a closed shell with "
            "icosahedral symmetry through multiple distinct "
            "(but quasi-equivalent) interactions."
        ),
    ),
    KingdomTopic(
        id="viruses-structure-envelope-vs-naked",
        kingdom="viruses",
        subtab="structure",
        title="Enveloped vs naked viruses",
        body=(
            "**Enveloped viruses** acquire a host-derived lipid "
            "membrane studded with viral glycoproteins as they "
            "bud through host membranes (HIV, influenza, "
            "coronaviruses, herpes, hepatitis B/C, Ebola, "
            "rabies).  The envelope's fluidity makes them "
            "inactivated by detergents + alcohols + lipid "
            "solvents — easier to disinfect.  **Naked / "
            "non-enveloped viruses** have only a protein capsid "
            "(adenovirus, rotavirus, norovirus, polio, hepatitis "
            "A, papillomaviruses) and are far more environmentally "
            "stable + resistant to detergents — explaining why "
            "norovirus + rotavirus dominate winter-vomiting "
            "outbreaks in poorly-disinfected settings (cruise "
            "ships, daycare centres)."
        ),
    ),
    KingdomTopic(
        id="viruses-structure-spike-glycoproteins",
        kingdom="viruses",
        subtab="structure",
        title="Spike glycoproteins + receptor binding",
        body=(
            "Enveloped viruses display **spike glycoproteins** "
            "on their surface that bind specific host-cell "
            "receptors and trigger membrane fusion.  Famous "
            "examples: HIV gp120/gp41 binding CD4 + CCR5/CXCR4; "
            "influenza haemagglutinin (HA) binding sialic acid + "
            "neuraminidase (NA) cleaving it for budding (the H + "
            "N in 'H1N1' nomenclature); SARS-CoV-2 spike binding "
            "ACE2 with TMPRSS2 priming the S2 fusion subunit; "
            "Ebola GP1/GP2 binding NPC1.  Spike glycoproteins are "
            "the main **vaccine antigens** + **neutralising "
            "antibody targets** because they're surface-exposed "
            "and essential for entry — antibodies that block "
            "spike-receptor interaction prevent infection."
        ),
    ),
    KingdomTopic(
        id="viruses-structure-genome-types",
        kingdom="viruses",
        subtab="structure",
        title="Genome diversity — Baltimore classification",
        body=(
            "Viruses uniquely use every possible genome chemistry "
            "— the **Baltimore classification** divides them into "
            "7 groups based on relationship to mRNA: (I) "
            "double-strand DNA (poxviruses, herpesviruses, "
            "adenoviruses); (II) single-strand DNA (parvoviruses, "
            "bacteriophages); (III) double-strand RNA "
            "(rotaviruses, reoviruses); (IV) positive-sense "
            "single-strand RNA (poliovirus, hepatitis C, "
            "coronaviruses, Zika); (V) negative-sense "
            "single-strand RNA (influenza, rabies, Ebola); (VI) "
            "RNA reverse-transcribed (retroviruses — HIV, HTLV); "
            "(VII) DNA reverse-transcribed (hepatitis B).  "
            "This diversity drives the **massive variability in "
            "antiviral mechanisms** + drug-discovery strategies."
        ),
    ),
    KingdomTopic(
        id="viruses-structure-bacteriophage-architecture",
        kingdom="viruses",
        subtab="structure",
        title="Bacteriophage architectures",
        body=(
            "**Bacteriophages** are viruses that infect "
            "bacteria — the most numerous biological entities on "
            "Earth (~ 10³¹ phage particles globally, exceeding "
            "all other organisms combined by orders of "
            "magnitude).  Three major morphologies: (a) "
            "**Caudovirales** (tailed phages — Myoviridae, "
            "Siphoviridae, Podoviridae) with icosahedral heads + "
            "helical tails — phage T4, λ, P22; (b) **filamentous "
            "phages** (Inoviridae) like M13 + fd — used as "
            "phage-display + nanofibre scaffolds; (c) **small "
            "isometric ssRNA phages** like Qβ + MS2 used as "
            "mRNA-replicase models for in-vitro evolution.  "
            "Phage therapy is being revived as an antibiotic-"
            "resistance counter-strategy (Eastern-European "
            "tradition + recent FDA emergency-use authorisations)."
        ),
    ),

    # ============================================================
    # VIRUSES — Physiology + Development
    # ============================================================
    KingdomTopic(
        id="viruses-physiology-life-cycle",
        kingdom="viruses",
        subtab="physiology",
        title="Generic viral life cycle (6 stages)",
        body=(
            "Every virus passes through 6 generic stages: (1) "
            "**attachment** of capsid / spike to host receptor; "
            "(2) **entry** via membrane fusion (enveloped) or "
            "endocytosis + endosomal escape (naked); (3) "
            "**uncoating** to release the genome; (4) "
            "**replication + transcription** of the genome + "
            "**translation** of viral proteins on host "
            "ribosomes; (5) **assembly** of new virions in the "
            "cytoplasm or nucleus or specialised replication "
            "compartments; (6) **release** by lysis (naked "
            "phages, polio) or budding (enveloped — HIV, "
            "influenza).  Antiviral drugs target each stage: "
            "entry inhibitors (maraviroc), uncoating inhibitors "
            "(amantadine), nucleoside analogues (acyclovir, "
            "remdesivir), protease inhibitors (HIV ritonavir, "
            "SARS-CoV-2 paxlovid), neuraminidase inhibitors "
            "(oseltamivir)."
        ),
    ),
    KingdomTopic(
        id="viruses-physiology-lytic-vs-lysogenic",
        kingdom="viruses",
        subtab="physiology",
        title="Lytic vs lysogenic bacteriophage cycles",
        body=(
            "Bacteriophages typically choose between two life-"
            "cycle programs: (a) **lytic** — replicate, package, "
            "lyse the host cell, release ~ 100-1 000 progeny; "
            "(b) **lysogenic** — integrate the phage genome into "
            "the host chromosome as a **prophage**, replicate "
            "passively along with the host until a stress "
            "signal (DNA damage → SOS response → RecA-mediated "
            "cleavage of the lambda CI repressor) triggers "
            "induction back to the lytic cycle.  The **lambda "
            "phage decision circuit** (CI / Cro bistable switch) "
            "is the canonical molecular-biology textbook example "
            "of stochastic cell-fate decisions in a 2-gene "
            "regulatory network.  Some prophages encode "
            "virulence factors (cholera toxin, diphtheria toxin "
            "are both phage-encoded), making lysogenic conversion "
            "a major bacterial-pathogenicity driver."
        ),
    ),
    KingdomTopic(
        id="viruses-physiology-mutation-quasispecies",
        kingdom="viruses",
        subtab="physiology",
        title="High mutation rates + quasispecies",
        body=(
            "RNA viruses replicate with **mutation rates ~ 10⁴-"
            "10⁶ × higher than DNA-based organisms** (no "
            "proofreading on viral RNA polymerases — error rate "
            "~ 10⁻⁴ per base per replication cycle).  Combined "
            "with short generation times + huge population sizes, "
            "this generates a **quasispecies** — a swarm of "
            "closely-related variants around a master sequence.  "
            "The quasispecies provides standing variation that "
            "lets viruses **escape immune pressure** (annual "
            "influenza H + N drift) + **escape antiviral drugs** "
            "(HIV resistance to single-drug therapy emerges "
            "within weeks — driving combination ART) + **adapt "
            "to new hosts** (SARS-CoV-2 spike Omicron evolution "
            "in immunocompromised hosts).  Coronaviruses are an "
            "exception with proofreading nsp14 ExoN — explains "
            "their ~ 30 kbp 'large' RNA genomes."
        ),
    ),
    KingdomTopic(
        id="viruses-physiology-cell-tropism",
        kingdom="viruses",
        subtab="physiology",
        title="Cell + tissue tropism",
        body=(
            "Each virus infects a specific subset of host cells "
            "— **tropism** — determined primarily by the "
            "match between viral surface proteins + host-cell "
            "receptors.  HIV is restricted to CD4⁺ cells "
            "(T-helper lymphocytes + macrophages); influenza A "
            "haemagglutinin binds α2,6-linked sialic acid "
            "(human upper respiratory tract) or α2,3-linked "
            "(avian + human lower respiratory tract); rabies "
            "virus binds nicotinic acetylcholine receptor + "
            "p75NTR + NCAM at neuromuscular junctions, then "
            "moves retrograde-axonally up to the CNS; "
            "hepatitis B binds NTCP (sodium taurocholate "
            "co-transporter) on hepatocytes.  Cell tropism "
            "explains tissue-specific disease patterns + "
            "limits the host-cell range that vaccines + "
            "antivirals must protect."
        ),
    ),
    KingdomTopic(
        id="viruses-physiology-host-immune-evasion",
        kingdom="viruses",
        subtab="physiology",
        title="Host immune evasion strategies",
        body=(
            "Viruses evolved diverse strategies to evade host "
            "immunity: (a) **antigenic drift / shift** "
            "(influenza HA/NA point mutations + segment "
            "reassortment between human + avian + swine "
            "lineages); (b) **latency** (herpesviruses HSV-1/2 "
            "+ VZV + EBV + CMV establish life-long latent "
            "infections in neurons or B cells, hiding from CD8 "
            "T cells until immune-competence drops); (c) "
            "**glycan-shielding** of conserved epitopes (HIV "
            "Env trimer densely glycosylated to mask broadly-"
            "neutralising-antibody targets); (d) "
            "**immunosuppression** (HIV depletes CD4⁺ T cells; "
            "EBV LMP1 mimics CD40 to manipulate B-cell "
            "signalling); (e) **MHC-I down-regulation** (CMV + "
            "Kaposi's sarcoma herpesvirus encode viral "
            "ubiquitin ligases that destroy host MHC-I, evading "
            "CD8 T cells)."
        ),
    ),

    # ============================================================
    # VIRUSES — Genetics + Evolution
    # ============================================================
    KingdomTopic(
        id="viruses-genetics-not-a-domain",
        kingdom="viruses",
        subtab="genetics",
        title="Are viruses alive?  Why they're not a domain",
        body=(
            "Viruses are **NOT a kingdom or domain of life** in "
            "the formal three-domain phylogeny, because they "
            "(a) lack ribosomes + their own translation "
            "machinery — every virus is an obligate intracellular "
            "parasite of a host cell's ribosomes; (b) lack a "
            "single common ancestor — viruses are **polyphyletic**, "
            "with multiple independent origins from different "
            "cellular lineages over evolutionary time; (c) lack "
            "metabolism + cannot reproduce outside a host.  Most "
            "biologists therefore treat viruses as 'biological "
            "entities' rather than 'living organisms' — but "
            "they're included in this catalogue tab because "
            "**they shape every aspect of cellular life on "
            "Earth**: from horizontal gene transfer to "
            "endogenous-retrovirus contributions to mammalian "
            "placenta development."
        ),
    ),
    KingdomTopic(
        id="viruses-genetics-endogenous-retroviruses",
        kingdom="viruses",
        subtab="genetics",
        title="Endogenous retroviruses + host-genome contributions",
        body=(
            "**Endogenous retroviruses (ERVs)** make up ~ 8% of "
            "the human genome — fossil retroviral integrations in "
            "germline cells that became fixed in the host "
            "lineage over millions of years.  Most ERVs are "
            "transcriptionally inactive, but some have been "
            "**co-opted into mammalian biology**: the "
            "**syncytin** genes (ERVW-1 + ERVFRD-1) encode "
            "envelope glycoproteins that drive trophoblast cell-"
            "cell fusion to form the placental syncytiotrophoblast "
            "— without these viral-derived proteins, mammalian "
            "placentation would not exist.  ERV regulatory "
            "sequences also contribute to interferon-response "
            "promoters + brain-development gene-regulatory "
            "networks.  Viruses are not just disease agents — "
            "they're a **major source of novel host genes**."
        ),
    ),
    KingdomTopic(
        id="viruses-genetics-virus-host-coevolution",
        kingdom="viruses",
        subtab="genetics",
        title="Virus-host arms race + Red Queen evolution",
        body=(
            "Virus-host coevolution is the textbook example of "
            "**Red Queen evolution** — both partners must "
            "continually evolve just to maintain their relative "
            "fitness.  Hosts evolve restriction factors (TRIM5α "
            "binds + degrades incoming HIV capsids; APOBEC3G "
            "deaminates HIV minus-strand cDNA; SAMHD1 depletes "
            "dNTPs needed for reverse transcription); viruses "
            "counter-evolve antagonists (HIV Vif degrades "
            "APOBEC3G via Cul5 E3 ligase recruitment; HIV Vpu "
            "degrades CD4 + tetherin).  At the population level, "
            "**MHC polymorphism** is maintained by viral "
            "selection — heterozygotes present more peptide "
            "diversity to T cells + are less likely to be "
            "wiped out by any single viral strain (HLA-B*57 is "
            "associated with HIV elite-controller status)."
        ),
    ),
    KingdomTopic(
        id="viruses-genetics-rna-world-relics",
        kingdom="viruses",
        subtab="genetics",
        title="Viroids + RNA-world relics",
        body=(
            "**Viroids** are tiny single-strand circular RNA "
            "molecules (~ 246-401 nucleotides) that replicate "
            "autonomously in plant cells **without encoding any "
            "protein** — rolling-circle replication via host RNA "
            "polymerase II + self-cleaving ribozyme activity.  "
            "Potato spindle tuber viroid (PSTVd) was the first "
            "discovered (Diener 1971).  Viroids are widely "
            "considered **RNA-world relics** — possible living "
            "fossils of pre-cellular replicating RNA molecules.  "
            "Hepatitis Delta virus (HDV) is a related 'satellite "
            "virus' that uses a viroid-like circular RNA + a "
            "single protein (Delta antigen) but requires "
            "hepatitis B for envelope proteins.  These minimal-"
            "genome agents anchor the lower bound of biological "
            "complexity."
        ),
    ),
    KingdomTopic(
        id="viruses-genetics-pandemic-evolution",
        kingdom="viruses",
        subtab="genetics",
        title="Pandemic emergence + spillover events",
        body=(
            "Most novel human viral pathogens emerge by "
            "**zoonotic spillover** — a virus jumping from an "
            "animal reservoir to humans.  Recent landmark "
            "events: HIV-1 from chimpanzee SIVcpz (~ 1920s "
            "Cameroon); SARS-CoV-1 from horseshoe-bat "
            "coronaviruses via civet intermediate (2002 "
            "Guangdong); MERS-CoV from dromedary camels (2012); "
            "Ebola from fruit bats; SARS-CoV-2 from horseshoe-"
            "bat coronaviruses with possible pangolin "
            "intermediate (late 2019 Wuhan); H5N1 + H7N9 "
            "influenza from poultry.  Successful adaptation "
            "requires the virus to (a) bind a human cell-"
            "surface receptor, (b) replicate efficiently at "
            "human body temperature + tissue conditions, (c) "
            "transmit person-to-person.  Pandemic preparedness "
            "now monitors animal-virus diversity + receptor-"
            "binding evolution proactively."
        ),
    ),
]


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------
_BY_ID: Dict[str, KingdomTopic] = {t.id: t for t in _TOPICS}


def list_topics(
    kingdom: Optional[str] = None,
    subtab: Optional[str] = None,
    sub_domain: Optional[str] = None,
) -> List[KingdomTopic]:
    """Return topics, optionally filtered by kingdom, sub-tab,
    and / or sub-domain.  Returns empty for unknown filter
    values.

    Sub-domain filter (round 169 / Phase 47d): topics with empty
    `sub_domain` are pan-domain — they match ANY sub-domain
    query within their kingdom (so e.g. mitochondria appear
    under sub_domain="animal" even though mitochondria are
    eukaryote-wide).  This mirrors the Phase-43 cell-component
    sub-domain query semantics.
    """
    if kingdom is not None and kingdom != "":
        if kingdom not in KINGDOMS:
            return []
        out = [t for t in _TOPICS if t.kingdom == kingdom]
    else:
        out = list(_TOPICS)
    if subtab is not None and subtab != "":
        if subtab not in SUBTABS:
            return []
        out = [t for t in out if t.subtab == subtab]
    if sub_domain is not None and sub_domain != "":
        if sub_domain not in SUB_DOMAINS:
            return []
        out = [
            t for t in out
            if not t.sub_domain or t.sub_domain == sub_domain
        ]
    return out


def get_topic(topic_id: str) -> Optional[KingdomTopic]:
    """Return the topic with this id, or None."""
    return _BY_ID.get(topic_id)


def find_topics(needle: str) -> List[KingdomTopic]:
    """Case-insensitive substring search across id + title +
    body + cross-reference fields."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out = []
    for t in _TOPICS:
        haystacks = [t.id, t.title, t.body, t.notes]
        haystacks.extend(t.cross_reference_cell_component_ids)
        haystacks.extend(t.cross_reference_pathway_ids)
        haystacks.extend(t.cross_reference_molecule_names)
        if n in " ".join(haystacks).lower():
            out.append(t)
    return out


def kingdoms() -> Tuple[str, ...]:
    return KINGDOMS


def subtabs() -> Tuple[str, ...]:
    return SUBTABS


def sub_domains() -> Tuple[str, ...]:
    """Round 169 / Phase 47d — full sub-domain tuple."""
    return SUB_DOMAINS


def sub_domains_for_kingdom(kingdom: str) -> Tuple[str, ...]:
    """Return only the sub-domains that are pedagogically
    meaningful for a given kingdom — for the GUI's per-tab
    sub-domain combo population."""
    if kingdom == "eukarya":
        return ("animal", "plant", "fungus", "protist")
    if kingdom == "bacteria":
        return ("gram-positive", "gram-negative")
    if kingdom == "archaea":
        return ("euryarchaeota", "crenarchaeota", "asgard")
    if kingdom == "viruses":
        return ("dna-virus", "rna-virus", "retrovirus")
    return ()


def topic_to_dict(t: KingdomTopic) -> Dict[str, object]:
    """JSON-serialisable view of a single topic."""
    return asdict(t)
