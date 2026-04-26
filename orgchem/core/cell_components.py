"""Phase 43 (round 151) — cell-component explorer.

Catalogue of cellular components keyed to the three domains of
life (Eukarya / Bacteria / Archaea) plus optional sub-domain
specialisations (animal / plant / fungus / protist / gram-
positive / gram-negative).  Each component carries its
molecular constituents — links by canonical name back to the
Phase-6 molecule database where the molecule is seeded.

Pure-headless: no Qt imports.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple


DOMAINS: Tuple[str, ...] = ("eukarya", "bacteria", "archaea")

SUB_DOMAINS: Tuple[str, ...] = (
    "animal", "plant", "fungus", "protist",
    "gram-positive", "gram-negative",
)

CATEGORIES: Tuple[str, ...] = (
    "membrane",         # plasma + organelle membranes
    "organelle",        # cytoplasmic organelles
    "nuclear",          # nucleus + sub-structures
    "cytoskeleton",     # actin / microtubule / IF
    "envelope",         # cell wall + outer envelope layers
    "appendage",        # cilia / flagella / pili
    "extracellular",    # ECM, biofilm, capsule
    "ribosome",         # ribosomes + translation machinery
    "genome",           # chromatin / nucleoid / plasmid
)


@dataclass(frozen=True)
class MolecularConstituent:
    """One molecular building block of a cell component."""
    name: str
    role: str
    notes: str = ""
    # If non-empty, the canonical name of a row in the
    # Phase-6 molecule database (e.g. "Cholesterol", "ATP").
    cross_reference_molecule_name: str = ""


@dataclass(frozen=True)
class CellComponent:
    """One cellular component anchored to a domain."""
    id: str
    name: str
    domain: str
    sub_domains: Tuple[str, ...]    # empty tuple = applies to whole domain
    category: str
    location: str
    function: str
    constituents: Tuple[MolecularConstituent, ...]
    notable_diseases: str = ""
    notes: str = ""


_COMPONENTS: List[CellComponent] = [

    # ============================================================
    # Eukarya — membranes
    # ============================================================
    CellComponent(
        id="eukaryotic-plasma-membrane",
        name="Plasma membrane (eukaryotic)",
        domain="eukarya",
        sub_domains=(),
        category="membrane",
        location="Cell boundary",
        function="Selective permeability barrier; signalling "
                 "platform; cell-cell adhesion; endo-/exocytosis "
                 "interface.",
        constituents=(
            MolecularConstituent(
                name="Phosphatidylcholine",
                role="Major phospholipid (outer leaflet)",
                cross_reference_molecule_name=
                    "Phosphatidylcholine (POPC-like)"),
            MolecularConstituent(
                name="Phosphatidylethanolamine",
                role="Major phospholipid (inner leaflet)",
                cross_reference_molecule_name=
                    "Phosphatidylethanolamine (POPE-like)"),
            MolecularConstituent(
                name="Phosphatidylserine",
                role="Inner-leaflet anionic; flips outward "
                     "during apoptosis (eat-me signal)"),
            MolecularConstituent(
                name="Sphingomyelin",
                role="Outer leaflet; raft component",
                cross_reference_molecule_name=
                    "Sphingomyelin (C18)"),
            MolecularConstituent(
                name="Cholesterol",
                role="Modulates fluidity; raft component",
                cross_reference_molecule_name="Cholesterol"),
            MolecularConstituent(
                name="Membrane proteins (~30 % of mass)",
                role="Receptors, transporters, ion channels, "
                     "GPCRs, integrins"),
            MolecularConstituent(
                name="Glycolipids + glycoproteins",
                role="Glycocalyx; cell recognition + ABO "
                     "blood-group antigens"),
        ),
        notable_diseases="Niemann-Pick disease (sphingomyelin "
                         "accumulation); Tay-Sachs (ganglioside "
                         "accumulation).",
        notes="The fluid-mosaic model (Singer + Nicolson 1972) "
              "established the lipid-bilayer + embedded-protein "
              "view that still organises the field.",
    ),
    CellComponent(
        id="endoplasmic-reticulum-rough",
        name="Rough endoplasmic reticulum (RER)",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="Continuous with nuclear envelope; cisternae "
                 "throughout cytoplasm",
        function="Co-translational protein synthesis + folding + "
                 "N-glycosylation + disulfide bond formation; "
                 "ER-stress / UPR sensing.",
        constituents=(
            MolecularConstituent(
                name="80S ribosomes (membrane-bound)",
                role="Translate secreted + membrane proteins"),
            MolecularConstituent(
                name="BiP / GRP78 chaperone",
                role="Folds nascent ER proteins; UPR sensor"),
            MolecularConstituent(
                name="Calnexin / Calreticulin",
                role="N-glycoprotein quality-control"),
            MolecularConstituent(
                name="Protein disulfide isomerase (PDI)",
                role="Forms + reshuffles -S-S- bonds in folding"),
        ),
        notable_diseases="Cystic fibrosis (ΔF508 CFTR misfolding "
                         "→ ERAD degradation).",
    ),
    CellComponent(
        id="endoplasmic-reticulum-smooth",
        name="Smooth endoplasmic reticulum (SER)",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="Tubular cisternae throughout cytoplasm",
        function="Lipid + steroid biosynthesis; xenobiotic "
                 "detoxification (CYP450); Ca²⁺ storage "
                 "(specialised SR in muscle).",
        constituents=(
            MolecularConstituent(
                name="Cytochrome P450 enzymes",
                role="Phase-I drug metabolism oxidations"),
            MolecularConstituent(
                name="HMG-CoA reductase",
                role="Cholesterol biosynthesis rate-limiting "
                     "step (statin target)"),
            MolecularConstituent(
                name="SERCA Ca²⁺-ATPase",
                role="Pumps Ca²⁺ into SR/ER lumen"),
        ),
    ),
    CellComponent(
        id="golgi-apparatus",
        name="Golgi apparatus",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="cis (RER-facing) → medial → trans (cell-"
                 "surface-facing) cisternae",
        function="Post-translational modification of secretory "
                 "proteins (O-glycosylation, sulfation, lipid "
                 "anchoring); sorting + packaging into vesicles "
                 "destined for membrane / secretion / lysosome.",
        constituents=(
            MolecularConstituent(
                name="Glycosyltransferases",
                role="Build N-/O-linked glycans"),
            MolecularConstituent(
                name="Mannose-6-phosphate receptor",
                role="Targets lysosomal hydrolases"),
            MolecularConstituent(
                name="Coatomer (COPI / COPII)",
                role="Vesicle coat for retro-/anterograde "
                     "transport"),
        ),
        notable_diseases="I-cell disease (mucolipidosis II — "
                         "loss of mannose-6-phosphate tagging).",
    ),
    CellComponent(
        id="mitochondrion",
        name="Mitochondrion",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="Cytoplasm; densest in skeletal muscle / "
                 "cardiomyocytes / hepatocytes",
        function="Cellular ATP production via TCA cycle + "
                 "oxidative phosphorylation; β-oxidation; "
                 "haem + Fe-S cluster biosynthesis; apoptosis "
                 "initiation (cytochrome-c release).",
        constituents=(
            MolecularConstituent(
                name="Inner-membrane phospholipids (cardiolipin)",
                role="Cristae structure; electron-transport-"
                     "chain organisation"),
            MolecularConstituent(
                name="Complex I-V (electron transport chain)",
                role="Generate proton gradient → ATP synthesis",
                cross_reference_molecule_name=""),
            MolecularConstituent(
                name="ATP synthase (Complex V)",
                role="Uses Δμ_H⁺ to synthesise ATP from ADP + Pᵢ"),
            MolecularConstituent(
                name="mtDNA (~16 569 bp circular)",
                role="Encodes 13 ETC subunits + 22 tRNAs + 2 rRNAs"),
            MolecularConstituent(
                name="55S mitochondrial ribosomes",
                role="Translate the 13 mtDNA-encoded proteins"),
        ),
        notable_diseases="Leber's hereditary optic neuropathy "
                         "(LHON, mtDNA mutations); MELAS "
                         "syndrome.  Maternal inheritance.",
        notes="Endosymbiotic origin from an α-proteobacterium "
              "ancestor (Margulis 1967).",
    ),
    CellComponent(
        id="chloroplast",
        name="Chloroplast",
        domain="eukarya",
        sub_domains=("plant",),
        category="organelle",
        location="Mesophyll cells of green plant tissues + "
                 "algae",
        function="Photosynthesis: light reactions in thylakoid "
                 "membrane, Calvin cycle in stroma; starch "
                 "storage.",
        constituents=(
            MolecularConstituent(
                name="Chlorophyll a + b",
                role="Light absorption (Soret + Q bands)"),
            MolecularConstituent(
                name="Photosystem II + Photosystem I",
                role="Charge-separation + water splitting + "
                     "NADP⁺ reduction"),
            MolecularConstituent(
                name="RuBisCO",
                role="CO₂ fixation in Calvin cycle (most "
                     "abundant protein on Earth)"),
            MolecularConstituent(
                name="Carotenoids (β-carotene + xanthophylls)",
                role="Accessory pigments + photoprotection"),
        ),
        notes="Endosymbiotic origin from a cyanobacterial "
              "ancestor.",
    ),
    CellComponent(
        id="lysosome",
        name="Lysosome",
        domain="eukarya",
        sub_domains=("animal",),
        category="organelle",
        location="Cytoplasm",
        function="Acidic (~pH 4.5) digestion of macromolecules "
                 "from endocytosis / autophagy / phagocytosis; "
                 "recycle building blocks.",
        constituents=(
            MolecularConstituent(
                name="V-type H⁺ ATPase",
                role="Acidifies lumen to pH 4.5"),
            MolecularConstituent(
                name="Acid hydrolases (~50 enzymes)",
                role="Proteases, lipases, glycosidases, "
                     "nucleases — all pH-4.5 optima"),
            MolecularConstituent(
                name="LAMP-1 / LAMP-2 membrane glycoproteins",
                role="Protect membrane from internal hydrolases"),
        ),
        notable_diseases="Lysosomal storage diseases — Gaucher "
                         "(glucocerebrosidase), Tay-Sachs "
                         "(hexosaminidase A), Pompe (acid "
                         "maltase), MPS-I Hurler (α-iduronidase).",
    ),
    CellComponent(
        id="vacuole-plant",
        name="Vacuole (plant)",
        domain="eukarya",
        sub_domains=("plant",),
        category="organelle",
        location="Single large central vacuole occupies "
                 "most of plant-cell volume",
        function="Turgor maintenance; pigment + secondary-"
                 "metabolite storage; degradation similar to "
                 "lysosome; ion homeostasis.",
        constituents=(
            MolecularConstituent(
                name="Tonoplast (vacuolar membrane)",
                role="Lipid bilayer with V-ATPase + transporters"),
            MolecularConstituent(
                name="Anthocyanins / flavonoids",
                role="Storage of secondary-metabolite pigments"),
        ),
    ),
    CellComponent(
        id="peroxisome",
        name="Peroxisome",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="Cytoplasm",
        function="β-oxidation of very-long-chain fatty acids; "
                 "H₂O₂ generation + catabolism; plasmalogen "
                 "synthesis; bile-acid + plasmalogen biosynth.",
        constituents=(
            MolecularConstituent(
                name="Catalase",
                role="2 H₂O₂ → 2 H₂O + O₂"),
            MolecularConstituent(
                name="Acyl-CoA oxidase",
                role="First step of peroxisomal β-oxidation"),
        ),
        notable_diseases="Zellweger syndrome (PEX gene defects "
                         "— peroxisomes fail to form).",
    ),
    CellComponent(
        id="proteasome",
        name="Proteasome (26S)",
        domain="eukarya",
        sub_domains=(),
        category="organelle",
        location="Cytoplasm + nucleus",
        function="ATP-dependent degradation of ubiquitin-tagged "
                 "proteins; central to cell-cycle, immune-MHC "
                 "antigen processing, transcription regulation.",
        constituents=(
            MolecularConstituent(
                name="20S core particle",
                role="α₇β₇β₇α₇ barrel with 3 catalytic "
                     "activities (chymotrypsin / trypsin / "
                     "caspase-like)"),
            MolecularConstituent(
                name="19S regulatory particle (lid + base)",
                role="Recognises poly-Ub chain, deubiquitinates, "
                     "unfolds, threads substrate"),
            MolecularConstituent(
                name="Ubiquitin",
                role="76-AA tag, K48-linked chain → degradation"),
        ),
        notes="Bortezomib (Velcade) inhibits the chymotrypsin-"
              "like activity — first proteasome-inhibitor drug "
              "(multiple myeloma).",
    ),
    CellComponent(
        id="80s-ribosome",
        name="80S ribosome (cytoplasmic)",
        domain="eukarya",
        sub_domains=(),
        category="ribosome",
        location="Free in cytosol or membrane-bound to RER",
        function="Translation of mRNA → polypeptide.  60S + "
                 "40S subunits assemble on mRNA.",
        constituents=(
            MolecularConstituent(
                name="60S subunit (28S + 5.8S + 5S rRNA + "
                     "~ 47 ribosomal proteins)",
                role="Peptidyl transferase centre + exit tunnel"),
            MolecularConstituent(
                name="40S subunit (18S rRNA + ~ 33 ribosomal "
                     "proteins)",
                role="mRNA decoding centre"),
        ),
        notes="Targeted by many antibiotics that bind the 70S "
              "bacterial form selectively (tetracycline / "
              "macrolides / aminoglycosides).",
    ),

    # ============================================================
    # Eukarya — nuclear
    # ============================================================
    CellComponent(
        id="nuclear-envelope",
        name="Nuclear envelope",
        domain="eukarya",
        sub_domains=(),
        category="nuclear",
        location="Surrounds nucleoplasm",
        function="Double membrane separating nucleus from "
                 "cytoplasm; nuclear pores mediate selective "
                 "transport.",
        constituents=(
            MolecularConstituent(
                name="Nuclear pore complex (NPC, ~125 MDa)",
                role="~30 nucleoporins; passive diffusion < 40 "
                     "kDa, active import/export of larger cargo"),
            MolecularConstituent(
                name="Lamin A/B/C",
                role="Nuclear lamina filaments (intermediate-"
                     "filament family)"),
            MolecularConstituent(
                name="Importin α/β + Ran-GTP",
                role="Cargo-recognition + GTP-driven transport"),
        ),
        notable_diseases="Hutchinson-Gilford progeria (LMNA "
                         "mutation → progerin); Emery-Dreifuss "
                         "muscular dystrophy.",
    ),
    CellComponent(
        id="nucleolus",
        name="Nucleolus",
        domain="eukarya",
        sub_domains=(),
        category="nuclear",
        location="Sub-nuclear region (no membrane — phase-"
                 "separated condensate)",
        function="rRNA transcription (RNA Pol I) + processing "
                 "+ ribosome subunit assembly.",
        constituents=(
            MolecularConstituent(
                name="RNA polymerase I",
                role="Transcribes 47S pre-rRNA"),
            MolecularConstituent(
                name="snoRNAs",
                role="Guide rRNA pseudouridylation + "
                     "2'-O-methylation"),
            MolecularConstituent(
                name="Fibrillarin / Nucleolin",
                role="Marker proteins; processing factors"),
        ),
        notes="A textbook example of biomolecular phase-"
              "separation (membraneless organelle).",
    ),
    CellComponent(
        id="chromatin",
        name="Chromatin (nucleosome)",
        domain="eukarya",
        sub_domains=(),
        category="genome",
        location="Nucleoplasm",
        function="Packages DNA into a regulated, transcribable "
                 "form; epigenetic regulation via histone "
                 "modification.",
        constituents=(
            MolecularConstituent(
                name="Histone octamer (H2A · H2B · H3 · H4)₂",
                role="Wraps 147 bp of DNA per nucleosome"),
            MolecularConstituent(
                name="Histone H1 (linker)",
                role="Stabilises higher-order 30-nm fibre"),
            MolecularConstituent(
                name="Genomic DNA",
                role="Genetic material (~ 3.2 Gbp human haploid)"),
            MolecularConstituent(
                name="Histone-modifying enzymes (HATs, HDACs, "
                     "KMTs, KDMs)",
                role="Write / read / erase epigenetic marks"),
        ),
        notes="Vorinostat (HDAC inhibitor) was the first "
              "epigenetic anti-cancer drug approved.",
    ),
    CellComponent(
        id="telomere",
        name="Telomere",
        domain="eukarya",
        sub_domains=(),
        category="genome",
        location="Chromosome ends",
        function="Protects chromosome ends from being "
                 "recognised as DNA damage; loop-back T-loop "
                 "structure.",
        constituents=(
            MolecularConstituent(
                name="(TTAGGG)ₙ tandem repeat (vertebrate)",
                role="3' G-rich overhang invades duplex to "
                     "form T-loop"),
            MolecularConstituent(
                name="Shelterin complex (TRF1, TRF2, POT1, "
                     "TIN2, TPP1, RAP1)",
                role="End-protection + telomerase regulation"),
            MolecularConstituent(
                name="Telomerase (hTERT + hTR)",
                role="Reverse transcriptase that adds TTAGGG "
                     "repeats; up-regulated in 90 % of cancers"),
        ),
        notes="Blackburn / Greider / Szostak — 2009 Nobel.",
    ),
    CellComponent(
        id="centromere-kinetochore",
        name="Centromere / kinetochore",
        domain="eukarya",
        sub_domains=(),
        category="genome",
        location="Constricted region of mitotic chromosome",
        function="Site of sister-chromatid cohesion + "
                 "attachment to mitotic spindle.",
        constituents=(
            MolecularConstituent(
                name="CENP-A nucleosome",
                role="H3 variant marks centromeric chromatin"),
            MolecularConstituent(
                name="Inner + outer kinetochore complex (Ndc80, "
                     "MIS12, KNL1)",
                role="Microtubule attachment + spindle-"
                     "checkpoint signalling"),
        ),
    ),

    # ============================================================
    # Eukarya — cytoskeleton
    # ============================================================
    CellComponent(
        id="actin-microfilament",
        name="Actin microfilament (F-actin)",
        domain="eukarya",
        sub_domains=(),
        category="cytoskeleton",
        location="Cortical cytoplasm; stress fibres; "
                 "lamellipodia / filopodia leading edge",
        function="Cell shape, motility, cytokinesis, muscle "
                 "contraction; dynamic ATP-driven "
                 "polymerisation.",
        constituents=(
            MolecularConstituent(
                name="G-actin monomer (42 kDa)",
                role="ATP-bound monomer adds at + end"),
            MolecularConstituent(
                name="Myosin II",
                role="Actin-based motor; muscle + cytokinetic "
                     "ring"),
            MolecularConstituent(
                name="Profilin / cofilin / Arp2/3",
                role="Polymerisation regulation + branching"),
        ),
        notes="Phalloidin (death-cap toxin) stabilises F-actin "
              "— used as fluorescent stain in microscopy.",
    ),
    CellComponent(
        id="microtubule",
        name="Microtubule",
        domain="eukarya",
        sub_domains=(),
        category="cytoskeleton",
        location="Centrosome-emanating throughout cytoplasm; "
                 "mitotic spindle; cilia / flagella axoneme",
        function="Vesicle + organelle transport; mitotic "
                 "spindle; axonal transport; cilia / flagella "
                 "motility.",
        constituents=(
            MolecularConstituent(
                name="α/β-tubulin heterodimer (50 kDa each)",
                role="GTP-bound; polymerises into 13-protofilament "
                     "hollow tube"),
            MolecularConstituent(
                name="γ-tubulin (γ-TuRC)",
                role="Microtubule nucleation at MTOC"),
            MolecularConstituent(
                name="Kinesin (+ end) / dynein (− end)",
                role="ATP-driven motors"),
        ),
        notes="Taxol (paclitaxel) stabilises microtubules → "
              "mitotic arrest → anti-cancer.  Vincristine "
              "destabilises them — same therapeutic effect "
              "via opposite mechanism.",
    ),
    CellComponent(
        id="intermediate-filament",
        name="Intermediate filament",
        domain="eukarya",
        sub_domains=("animal",),
        category="cytoskeleton",
        location="Cytoplasm + nuclear lamina",
        function="Mechanical strength; tissue-specific (keratin "
                 "in epithelia, vimentin in mesenchyme, "
                 "neurofilament in neurons, lamin in nucleus).",
        constituents=(
            MolecularConstituent(
                name="Keratin (cytokeratin)",
                role="Epithelial-cell IF; hair / nail / horn"),
            MolecularConstituent(
                name="Vimentin",
                role="Mesenchymal-cell IF (fibroblasts)"),
            MolecularConstituent(
                name="Neurofilament L/M/H",
                role="Axonal IF — defines neuronal calibre"),
            MolecularConstituent(
                name="Lamin A/B/C",
                role="Nuclear lamina"),
        ),
        notable_diseases="Epidermolysis bullosa simplex "
                         "(keratin 5/14 mutations); ALS "
                         "(neurofilament aggregation).",
    ),
    CellComponent(
        id="centrosome",
        name="Centrosome / MTOC",
        domain="eukarya",
        sub_domains=("animal",),
        category="cytoskeleton",
        location="Perinuclear",
        function="Primary microtubule-organising centre; "
                 "duplicates once per cell cycle to template "
                 "bipolar mitotic spindle.",
        constituents=(
            MolecularConstituent(
                name="Two centrioles (mother + daughter)",
                role="Cylinders of 9 microtubule triplets"),
            MolecularConstituent(
                name="γ-tubulin ring complex (γ-TuRC)",
                role="Templates microtubule (-) ends"),
            MolecularConstituent(
                name="Pericentriolar material (PCM)",
                role="Proteinaceous matrix recruiting γ-TuRC + "
                     "regulators"),
        ),
    ),
    CellComponent(
        id="cilium-flagellum-eukaryotic",
        name="Cilium / flagellum (eukaryotic)",
        domain="eukarya",
        sub_domains=(),
        category="appendage",
        location="Apical cell surface",
        function="Beating-based fluid movement (motile cilia of "
                 "trachea); cell motility (sperm flagellum); "
                 "sensory role (primary cilium).",
        constituents=(
            MolecularConstituent(
                name="Axoneme (9+2 microtubule arrangement)",
                role="9 outer doublets + 2 central singlets"),
            MolecularConstituent(
                name="Dynein arms",
                role="ATP-driven sliding of adjacent doublets → "
                     "ciliary bend"),
            MolecularConstituent(
                name="Basal body",
                role="Nucleates the axoneme; identical structure "
                     "to a centriole"),
        ),
        notable_diseases="Primary ciliary dyskinesia "
                         "(Kartagener syndrome — situs "
                         "inversus / bronchiectasis / "
                         "infertility).",
    ),

    # ============================================================
    # Eukarya — extracellular
    # ============================================================
    CellComponent(
        id="ecm-animal",
        name="Extracellular matrix (animal)",
        domain="eukarya",
        sub_domains=("animal",),
        category="extracellular",
        location="Outside cells; abundant in connective "
                 "tissue / cartilage / bone",
        function="Mechanical support; cell-cell signalling "
                 "platform; reservoir for growth factors; "
                 "tissue boundary; tensile + compressive "
                 "strength.",
        constituents=(
            MolecularConstituent(
                name="Collagen (type I → IV)",
                role="Triple-helical structural fibres; most "
                     "abundant protein in mammals"),
            MolecularConstituent(
                name="Fibronectin",
                role="Multi-domain glycoprotein; RGD motif "
                     "binds integrins"),
            MolecularConstituent(
                name="Laminin",
                role="Cross-shaped basement-membrane organiser"),
            MolecularConstituent(
                name="Elastin",
                role="Reversible extensibility (skin, lung, "
                     "blood vessels)"),
            MolecularConstituent(
                name="Glycosaminoglycans (hyaluronic acid, "
                     "chondroitin sulfate, heparan sulfate)",
                role="Hydrate the matrix; resist compression"),
            MolecularConstituent(
                name="Proteoglycans (aggrecan, syndecan, "
                     "perlecan)",
                role="Core protein + multiple GAG chains"),
        ),
        notable_diseases="Ehlers-Danlos (collagen); osteogenesis "
                         "imperfecta (collagen type I); "
                         "fibrodysplasia ossificans progressiva.",
    ),
    CellComponent(
        id="plant-cell-wall",
        name="Plant cell wall",
        domain="eukarya",
        sub_domains=("plant",),
        category="envelope",
        location="External to plasma membrane",
        function="Resists turgor pressure; structural support; "
                 "controls cell shape + growth.",
        constituents=(
            MolecularConstituent(
                name="Cellulose microfibrils (β-1,4 glucan)",
                role="Tensile-strength scaffold; ~20 nm "
                     "microfibrils crystalline cores"),
            MolecularConstituent(
                name="Hemicellulose (xyloglucans, xylans)",
                role="Cross-link cellulose microfibrils"),
            MolecularConstituent(
                name="Pectin (homogalacturonan + RG-I/II)",
                role="Hydrated gel matrix; cell-cell adhesion"),
            MolecularConstituent(
                name="Lignin (in secondary walls only)",
                role="Cross-linked polyphenol → wood rigidity"),
        ),
    ),
    CellComponent(
        id="fungal-cell-wall",
        name="Fungal cell wall",
        domain="eukarya",
        sub_domains=("fungus",),
        category="envelope",
        location="External to plasma membrane",
        function="Mechanical strength + osmotic protection.",
        constituents=(
            MolecularConstituent(
                name="Chitin (β-1,4-N-acetylglucosamine)",
                role="Microfibrillar strength layer"),
            MolecularConstituent(
                name="β-1,3-glucan + β-1,6-glucan",
                role="Major polysaccharide matrix"),
            MolecularConstituent(
                name="Mannoproteins",
                role="Outer-layer glycoproteins; antigenic"),
        ),
        notes="Echinocandins (caspofungin) inhibit β-1,3-glucan "
              "synthase — selective antifungal target since "
              "humans lack this pathway.",
    ),

    # ============================================================
    # Bacteria
    # ============================================================
    CellComponent(
        id="bacterial-plasma-membrane",
        name="Bacterial plasma membrane",
        domain="bacteria",
        sub_domains=(),
        category="membrane",
        location="Beneath cell wall",
        function="Selective barrier; site of ETC + ATP "
                 "synthase (no mitochondria); secretion "
                 "system anchor.",
        constituents=(
            MolecularConstituent(
                name="Phosphatidylethanolamine + "
                     "phosphatidylglycerol + cardiolipin",
                role="Major phospholipids (no cholesterol)"),
            MolecularConstituent(
                name="Hopanoids",
                role="Pentacyclic-triterpene functional "
                     "analogue of sterols"),
        ),
    ),
    CellComponent(
        id="peptidoglycan-gram-positive",
        name="Peptidoglycan cell wall (gram-positive)",
        domain="bacteria",
        sub_domains=("gram-positive",),
        category="envelope",
        location="External to plasma membrane",
        function="Multi-layered (~ 20-80 nm) thick murein "
                 "sacculus; resists turgor; gram-stain "
                 "positive.",
        constituents=(
            MolecularConstituent(
                name="N-acetylglucosamine (NAG)",
                role="Glycan-strand monomer",
                cross_reference_molecule_name=
                    "N-Acetylglucosamine (GlcNAc)"),
            MolecularConstituent(
                name="N-acetylmuramic acid (NAM)",
                role="Glycan-strand monomer alternating with "
                     "NAG"),
            MolecularConstituent(
                name="Pentaglycine cross-bridge",
                role="Cross-links L-Lys of adjacent stem "
                     "peptides (Staphylococcus)"),
            MolecularConstituent(
                name="Teichoic acid + lipoteichoic acid",
                role="Anionic polymers spanning the wall"),
        ),
        notes="β-lactams (penicillin / cephalosporins) block "
              "peptidoglycan cross-linking by acylating PBP "
              "transpeptidases.  Vancomycin binds the D-Ala-"
              "D-Ala terminus to block transpeptidation.",
    ),
    CellComponent(
        id="peptidoglycan-gram-negative",
        name="Peptidoglycan cell wall (gram-negative)",
        domain="bacteria",
        sub_domains=("gram-negative",),
        category="envelope",
        location="Periplasmic space between inner and outer "
                 "membranes",
        function="Single thin layer (~ 7-8 nm) sandwiched "
                 "in periplasm.",
        constituents=(
            MolecularConstituent(
                name="N-acetylglucosamine + N-acetylmuramic "
                     "acid",
                role="Glycan-strand backbone"),
            MolecularConstituent(
                name="Direct meso-DAP cross-link",
                role="No pentaglycine bridge — direct DAP "
                     "to D-Ala cross-link"),
        ),
    ),
    CellComponent(
        id="outer-membrane-gram-negative",
        name="Outer membrane (gram-negative)",
        domain="bacteria",
        sub_domains=("gram-negative",),
        category="envelope",
        location="Outside thin peptidoglycan layer",
        function="Permeability barrier; LPS-mediated immune "
                 "evasion; antibiotic resistance via porin "
                 "selectivity + efflux pumps.",
        constituents=(
            MolecularConstituent(
                name="Lipopolysaccharide (LPS)",
                role="Lipid A (endotoxin) + core + O-antigen "
                     "polysaccharide"),
            MolecularConstituent(
                name="Porins (OmpF, OmpC)",
                role="Selectivity-filter channels for small "
                     "hydrophiles"),
            MolecularConstituent(
                name="Lipoproteins (Lpp / Braun's lipoprotein)",
                role="Anchor outer membrane to peptidoglycan"),
        ),
        notable_diseases="Septic shock (LPS / endotoxin → "
                         "TLR4 signalling cascade).",
    ),
    CellComponent(
        id="bacterial-nucleoid",
        name="Bacterial nucleoid",
        domain="bacteria",
        sub_domains=(),
        category="genome",
        location="Cytoplasm (no membrane envelope)",
        function="Houses the bacterial chromosome; supercoiled "
                 "+ condensed by NAPs (nucleoid-associated "
                 "proteins).",
        constituents=(
            MolecularConstituent(
                name="Single circular chromosome",
                role="~ 4.6 Mbp in E. coli K-12"),
            MolecularConstituent(
                name="DNA gyrase (topoisomerase II)",
                role="Introduces negative supercoils — "
                     "fluoroquinolone target"),
            MolecularConstituent(
                name="Nucleoid-associated proteins (HU, IHF, "
                     "Fis, H-NS)",
                role="Compact + organise the nucleoid"),
        ),
    ),
    CellComponent(
        id="bacterial-plasmid",
        name="Plasmid",
        domain="bacteria",
        sub_domains=(),
        category="genome",
        location="Cytoplasm; independent of chromosome",
        function="Extra-chromosomal circular DNA; carries "
                 "antibiotic resistance + virulence + "
                 "conjugation machinery.",
        constituents=(
            MolecularConstituent(
                name="Circular dsDNA (1–400 kbp)",
                role="Self-replicating origin (oriV) + "
                     "selection marker"),
            MolecularConstituent(
                name="β-lactamase (e.g. blaTEM-1)",
                role="Common antibiotic-resistance cassette"),
        ),
        notes="Plasmids are the molecular-cloning workhorse "
              "(pUC19, pET, pBR322).",
    ),
    CellComponent(
        id="bacterial-flagellum",
        name="Bacterial flagellum",
        domain="bacteria",
        sub_domains=(),
        category="appendage",
        location="Surface (cell pole or peritrichous)",
        function="Rotary motor (~ 100 Hz) drives swimming + "
                 "chemotaxis.",
        constituents=(
            MolecularConstituent(
                name="Flagellin (FliC)",
                role="Self-assembling helical filament"),
            MolecularConstituent(
                name="Hook (FlgE)",
                role="Universal joint between filament + "
                     "basal body"),
            MolecularConstituent(
                name="Basal body (MotA/B stator + FliG/M/N "
                     "rotor)",
                role="Proton-motive-force-driven rotary motor"),
        ),
        notes="Behe's 'irreducible complexity' poster-child "
              "rebutted by stepwise evolution from Type-III "
              "secretion ancestor.",
    ),
    CellComponent(
        id="pilus-fimbria",
        name="Pilus / fimbria",
        domain="bacteria",
        sub_domains=(),
        category="appendage",
        location="Surface",
        function="Adhesion to host cells (fimbriae); "
                 "conjugation tube (sex pilus); twitching "
                 "motility.",
        constituents=(
            MolecularConstituent(
                name="Pilin subunits",
                role="Self-assembling tube"),
            MolecularConstituent(
                name="Tip adhesin (e.g. FimH)",
                role="Carbohydrate-binding tip; key UPEC "
                     "uropathogenicity factor"),
        ),
    ),
    CellComponent(
        id="bacterial-capsule",
        name="Bacterial capsule",
        domain="bacteria",
        sub_domains=(),
        category="extracellular",
        location="Outside outer membrane (gram-) or "
                 "peptidoglycan (gram+)",
        function="Anti-phagocytic; immune evasion; biofilm "
                 "formation.",
        constituents=(
            MolecularConstituent(
                name="Polysaccharide capsule (e.g. type-3 "
                     "Streptococcus pneumoniae)",
                role="Major virulence + serotype determinant; "
                     "vaccine target"),
            MolecularConstituent(
                name="Poly-γ-glutamate (Bacillus anthracis)",
                role="Protein-based capsule"),
        ),
        notes="Pneumococcal conjugate vaccines (PCV13, PCV20) "
              "target capsular polysaccharides.",
    ),
    CellComponent(
        id="biofilm-eps",
        name="Biofilm extracellular polymeric substances (EPS)",
        domain="bacteria",
        sub_domains=(),
        category="extracellular",
        location="Outside cells in biofilm matrix",
        function="Holds biofilm together; nutrient + signalling "
                 "channels; antibiotic + immune resistance.",
        constituents=(
            MolecularConstituent(
                name="Exopolysaccharides (Pel, Psl, alginate)",
                role="Matrix scaffold (Pseudomonas)"),
            MolecularConstituent(
                name="Extracellular DNA (eDNA)",
                role="Structural + horizontal-gene-transfer "
                     "substrate"),
            MolecularConstituent(
                name="Extracellular proteins (amyloid-like "
                     "fimbriae)",
                role="Adhesion + matrix integrity"),
        ),
    ),
    CellComponent(
        id="70s-ribosome",
        name="70S ribosome (bacterial)",
        domain="bacteria",
        sub_domains=(),
        category="ribosome",
        location="Cytoplasm",
        function="Translation of mRNA → polypeptide.  50S + "
                 "30S subunits.",
        constituents=(
            MolecularConstituent(
                name="50S subunit (23S + 5S rRNA + ~ 33 "
                     "ribosomal proteins)",
                role="Peptidyl transferase centre"),
            MolecularConstituent(
                name="30S subunit (16S rRNA + ~ 21 ribosomal "
                     "proteins)",
                role="mRNA decoding"),
        ),
        notes="Selectively targeted by macrolides "
              "(erythromycin), tetracyclines, "
              "aminoglycosides (gentamicin), oxazolidinones "
              "(linezolid), chloramphenicol.",
    ),

    # ============================================================
    # Archaea
    # ============================================================
    CellComponent(
        id="archaeal-plasma-membrane",
        name="Archaeal plasma membrane",
        domain="archaea",
        sub_domains=(),
        category="membrane",
        location="Cell boundary",
        function="Selective barrier; resists extreme "
                 "temperature / pH / salinity in extremophiles.",
        constituents=(
            MolecularConstituent(
                name="Ether-linked isoprenoid (phytanyl) "
                     "lipids",
                role="Replace bacterial / eukaryotic ester "
                     "linkages — chemically far more stable"),
            MolecularConstituent(
                name="Glycerol-1-phosphate backbone",
                role="Opposite stereochemistry to bacterial / "
                     "eukaryotic glycerol-3-phosphate"),
            MolecularConstituent(
                name="Tetraether monolayer "
                     "(in hyperthermophiles)",
                role="Spans the entire membrane — single layer "
                     "instead of bilayer"),
        ),
        notes="The lipid divide is the strongest single-marker "
              "argument for the three-domain phylogeny.",
    ),
    CellComponent(
        id="pseudopeptidoglycan",
        name="Pseudopeptidoglycan (pseudomurein)",
        domain="archaea",
        sub_domains=(),
        category="envelope",
        location="External to plasma membrane "
                 "(some methanogens)",
        function="Structural cell-wall analogue resistant to "
                 "lysozyme + β-lactams (different glycosidic "
                 "linkages from bacterial peptidoglycan).",
        constituents=(
            MolecularConstituent(
                name="N-acetylglucosamine (NAG)",
                role="Glycan-strand monomer",
                cross_reference_molecule_name=
                    "N-Acetylglucosamine (GlcNAc)"),
            MolecularConstituent(
                name="N-acetyltalosaminuronic acid (NAT)",
                role="Replaces NAM; β-1,3 linkage replaces "
                     "β-1,4 — explains lysozyme + β-lactam "
                     "resistance"),
            MolecularConstituent(
                name="L-amino acid stem peptide",
                role="L- not D-amino acids — another "
                     "antibiotic-resistance feature"),
        ),
    ),
    CellComponent(
        id="s-layer",
        name="S-layer (surface layer)",
        domain="archaea",
        sub_domains=(),
        category="envelope",
        location="Outermost cell-surface layer (also in some "
                 "bacteria)",
        function="Two-dimensional crystalline lattice of "
                 "glycoprotein subunits; protective + "
                 "molecular sieve.",
        constituents=(
            MolecularConstituent(
                name="S-layer glycoprotein (40-200 kDa)",
                role="Self-assembles into ~ 5-15 nm-thick "
                     "p1 / p2 / p3 / p4 / p6 lattice"),
        ),
        notes="The most abundant cell envelope on Earth — "
              "present in many archaea + bacteria.",
    ),
    CellComponent(
        id="archaeal-ribosome",
        name="Archaeal ribosome (70S, eukaryote-like)",
        domain="archaea",
        sub_domains=(),
        category="ribosome",
        location="Cytoplasm",
        function="Translation; 70S overall like bacteria but "
                 "translation factors + ribosomal-protein "
                 "complement closer to eukaryotic 80S.",
        constituents=(
            MolecularConstituent(
                name="50S subunit (23S + 5S rRNA)",
                role="Peptidyl transferase centre"),
            MolecularConstituent(
                name="30S subunit (16S rRNA)",
                role="mRNA decoding"),
        ),
        notes="Sensitive to anisomycin (eukaryote inhibitor) + "
              "diphtheria toxin (eukaryote-like elongation "
              "factor 2) but resistant to most "
              "bacteria-targeting antibiotics — diagnostic "
              "of the eukaryote-like translation machinery.",
    ),
    CellComponent(
        id="archaeal-nucleoid",
        name="Archaeal nucleoid",
        domain="archaea",
        sub_domains=(),
        category="genome",
        location="Cytoplasm (no membrane)",
        function="Single circular chromosome packaged with "
                 "histone-like proteins (in many archaea — "
                 "another eukaryotic affinity).",
        constituents=(
            MolecularConstituent(
                name="Circular dsDNA",
                role="~ 1-6 Mbp"),
            MolecularConstituent(
                name="Archaeal histones (HMfA/B in some "
                     "lineages)",
                role="Form tetrameric mini-nucleosomes — "
                     "evolutionary precursor to eukaryotic "
                     "(H3-H4)₂ tetramer"),
        ),
    ),
    CellComponent(
        id="archaeal-flagellum",
        name="Archaeal flagellum (archaellum)",
        domain="archaea",
        sub_domains=(),
        category="appendage",
        location="Surface",
        function="ATP-driven rotary motor; analogous function "
                 "to bacterial flagellum but evolutionarily "
                 "distinct (related to Type-IV pili, not "
                 "Type-III secretion).",
        constituents=(
            MolecularConstituent(
                name="Archaellins (FlaA/B subunits)",
                role="Filament — assembled at the base, not "
                     "the tip (opposite of bacterial flagella)"),
            MolecularConstituent(
                name="FlaI ATPase",
                role="ATP-driven rotation (vs PMF in bacteria)"),
        ),
        notes="The archaellum was renamed from 'archaeal "
              "flagellum' once it became clear it shares no "
              "homology with the bacterial structure.",
    ),
]


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------
_BY_ID: Dict[str, CellComponent] = {c.id: c for c in _COMPONENTS}


def list_components(
    domain: Optional[str] = None,
    sub_domain: Optional[str] = None,
) -> List[CellComponent]:
    """Return components, optionally filtered by domain and/or
    sub-domain.  Returns empty for unknown filter values.

    A component with empty ``sub_domains`` matches **any**
    sub-domain query within its domain (e.g. mitochondrion has
    sub_domains=() but still surfaces under sub_domain="animal").
    """
    if domain is not None and domain != "":
        if domain not in DOMAINS:
            return []
        out = [c for c in _COMPONENTS if c.domain == domain]
    else:
        out = list(_COMPONENTS)
    if sub_domain is not None and sub_domain != "":
        if sub_domain not in SUB_DOMAINS:
            return []
        out = [
            c for c in out
            if not c.sub_domains or sub_domain in c.sub_domains
        ]
    return out


def get_component(component_id: str) -> Optional[CellComponent]:
    """Return the component with this id, or None."""
    return _BY_ID.get(component_id)


def find_components(needle: str) -> List[CellComponent]:
    """Case-insensitive substring search across id + name +
    function + constituent names + notes."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out = []
    for c in _COMPONENTS:
        haystacks = [
            c.id, c.name, c.function, c.location, c.notes,
            c.notable_diseases,
        ]
        haystacks.extend(m.name for m in c.constituents)
        haystacks.extend(m.role for m in c.constituents)
        if n in " ".join(haystacks).lower():
            out.append(c)
    return out


def components_for_category(category: str) -> List[CellComponent]:
    """Return components of a given category (membrane /
    organelle / nuclear / cytoskeleton / envelope / appendage /
    extracellular / ribosome / genome)."""
    if not category or category not in CATEGORIES:
        return []
    return [c for c in _COMPONENTS if c.category == category]


def domains() -> Tuple[str, ...]:
    return DOMAINS


def sub_domains() -> Tuple[str, ...]:
    return SUB_DOMAINS


def categories() -> Tuple[str, ...]:
    return CATEGORIES


def component_to_dict(c: CellComponent) -> Dict[str, object]:
    """JSON-serialisable view of a component (incl. nested
    constituents)."""
    return asdict(c)
