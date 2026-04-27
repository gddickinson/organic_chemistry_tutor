"""Phase BC-2.0 (round 219) — 28-entry cofactors / coenzymes
catalogue.

Each entry carries typed cross-references into:
- ``biochem.core.enzymes`` ids (enzymes that use this cofactor
  as substrate or prosthetic group).
- ``orgchem.core.metabolic_pathways`` ids (pathways where this
  cofactor is consumed / regenerated).
- ``orgchem.db.Molecule`` rows by exact name (verified against
  the seeded molecule DB at write time — the trailing-comma
  validator on the dataclass guarantees these stay tuples).

All cross-reference ids verified against destination
catalogues at write time; the round-219 catalogue tests gate
re-validation at every test run.
"""
from __future__ import annotations
from typing import Tuple

from biochem.core.cofactors import Cofactor


COFACTORS: Tuple[Cofactor, ...] = (
    # ============================================================
    # Nicotinamide cofactors (4)
    # ============================================================
    Cofactor(
        id="nad-plus",
        name="NAD+",
        cofactor_class="nicotinamide",
        chemical_summary=(
            "Nicotinamide adenine dinucleotide, oxidised "
            "form.  Hydride acceptor at C4 of the "
            "nicotinamide ring."),
        primary_role=(
            "2-electron + 1-proton (hydride) acceptor in "
            "catabolic dehydrogenase reactions",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻) — i.e. 2 e⁻ + 1 H⁺",
        ),
        key_features=(
            "E°' = -0.32 V (relative to SHE)",
            "Cellular [NAD+]/[NADH] ratio is high (~ 700 in "
            "cytosol) → drives catabolic oxidation thermo"
            "dynamically",
            "Substrate (not prosthetic group) — diffuses "
            "between enzymes",
        ),
        vitamin_origin=(
            "Niacin (vitamin B3 / nicotinic acid)",
        ),
        deficiency_disease=(
            "Pellagra: dermatitis, diarrhoea, dementia, death "
            "(the four Ds) — historic deficiency syndrome of "
            "maize-monoculture diets",
        ),
        cross_reference_enzyme_ids=(
            "alcohol-dehydrogenase",
            "lactate-dehydrogenase", "gapdh",
            "pyruvate-carboxylase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "glycolysis", "tca_cycle", "ox_phos",
            "beta_oxidation", "pentose_phosphate",
        ),
        cross_reference_molecule_names=(
            "NAD+ (nicotinamide adenine dinucleotide)",
        ),
        notes=(
            "NAD+ is also the substrate for sirtuins (NAD+-"
            "dependent deacetylases) + PARP enzymes (poly(ADP-"
            "ribose) polymerases) — links metabolism to "
            "epigenetics + DNA repair."),
    ),
    Cofactor(
        id="nadh",
        name="NADH",
        cofactor_class="nicotinamide",
        chemical_summary=(
            "Reduced form of NAD+.  Carries a hydride on C4 "
            "of the nicotinamide ring."),
        primary_role=(
            "2-electron donor for the mitochondrial electron-"
            "transport chain (Complex I)",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻)",
        ),
        key_features=(
            "Absorbs strongly at 340 nm (the basis of every "
            "NAD-coupled spectrophotometric enzyme assay)",
            "Each cytosolic NADH yields ~ 1.5-2.5 ATP via "
            "the malate-aspartate or glycerol-3-phosphate "
            "shuttle + ETC",
        ),
        vitamin_origin=(
            "Niacin (vitamin B3)",
        ),
        deficiency_disease=(
            "Pellagra (see NAD+)",
        ),
        cross_reference_enzyme_ids=(
            "alcohol-dehydrogenase",
            "lactate-dehydrogenase", "gapdh",
            "cytochrome-c-oxidase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "glycolysis", "tca_cycle", "ox_phos",
            "beta_oxidation",
        ),
        cross_reference_molecule_names=(
            "NADH",
        ),
        notes=(
            "Lehninger's elegant insight: the 340-nm shift on "
            "NAD+ → NADH reduction makes whole biochemistry "
            "an absorbance-readable kinetic experiment."),
    ),
    Cofactor(
        id="nadp-plus",
        name="NADP+",
        cofactor_class="nicotinamide",
        chemical_summary=(
            "Phosphorylated NAD+ analogue (2'-phosphate on "
            "the adenine ribose).  The phosphate is the "
            "recognition handle that distinguishes NADP+ from "
            "NAD+ for enzyme-active-site binding."),
        primary_role=(
            "Anabolic 2-electron acceptor (kept oxidised)",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻)",
        ),
        key_features=(
            "Same redox chemistry as NAD+, different cellular "
            "role: anabolism vs catabolism",
            "The 2'-phosphate distinguishes the two pools",
        ),
        vitamin_origin=(
            "Niacin (vitamin B3)",
        ),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "pentose_phosphate", "fatty_acid_synthesis",
            "cholesterol_biosynthesis",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Cells maintain [NADP+]/[NADPH] ~ 0.005 (mostly "
            "reduced) — the opposite of NAD+/NADH (mostly "
            "oxidised).  The phosphate label keeps the two "
            "redox pools kinetically separate."),
    ),
    Cofactor(
        id="nadph",
        name="NADPH",
        cofactor_class="nicotinamide",
        chemical_summary=(
            "Reduced NADP+.  Hydride donor for reductive "
            "biosynthesis."),
        primary_role=(
            "Hydride donor for reductive anabolism",
            "Reducing equivalents for antioxidant defence "
            "(glutathione + thioredoxin systems)",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻)",
        ),
        key_features=(
            "Pentose phosphate pathway is the major NADPH "
            "source (~ 60 %) in most cells; malic enzyme + "
            "isocitrate dehydrogenase contribute the rest",
            "Drives fatty-acid + cholesterol + nucleotide "
            "biosynthesis + reductive amination",
        ),
        vitamin_origin=(
            "Niacin (vitamin B3)",
        ),
        deficiency_disease=(
            "G6PD deficiency: insufficient pentose phosphate "
            "→ low erythrocyte NADPH → glutathione depletion "
            "→ haemolysis on oxidative stress (favism)",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "pentose_phosphate", "fatty_acid_synthesis",
            "cholesterol_biosynthesis",
        ),
        cross_reference_molecule_names=(
            "NADPH",
        ),
        notes=(
            "Quote: ‘NADPH is the currency of biosynthesis; "
            "NADH is the currency of catabolism’ — a useful "
            "mnemonic for the redox-pool partitioning."),
    ),

    # ============================================================
    # Flavin cofactors (3)
    # ============================================================
    Cofactor(
        id="fad",
        name="FAD",
        cofactor_class="flavin",
        chemical_summary=(
            "Flavin adenine dinucleotide.  Tightly bound (often "
            "covalently) to the apoenzyme; a true prosthetic "
            "group rather than a diffusible substrate."),
        primary_role=(
            "1- or 2-electron acceptor for oxidoreductases "
            "where 2 H atoms must move together",
            "Membrane-anchored Complex II of the ETC",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻) → FADH⁻ semiquinone or 2H → FADH₂",
        ),
        key_features=(
            "E°' = -0.22 V (typical, varies with apoenzyme "
            "environment)",
            "Yellow colour (absorbs ~ 450 nm) — gives the "
            "flavoproteins their name (Latin flavus = yellow)",
            "Can do single-electron chemistry too (semi"
            "quinone intermediate) — bridges two-electron + "
            "one-electron worlds",
        ),
        vitamin_origin=(
            "Riboflavin (vitamin B2)",
        ),
        deficiency_disease=(
            "Ariboflavinosis: cheilitis, glossitis, sebor"
            "rhoeic dermatitis (uncommon in the developed "
            "world)",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "ox_phos", "beta_oxidation",
        ),
        cross_reference_molecule_names=(
            "FAD",
        ),
        notes=(
            "Succinate dehydrogenase (TCA Complex II) carries "
            "covalently-bound FAD via 8α-N(3)-histidyl-FAD "
            "linkage."),
    ),
    Cofactor(
        id="fadh2",
        name="FADH₂",
        cofactor_class="flavin",
        chemical_summary=(
            "Fully reduced FAD (2 e⁻ + 2 H⁺).  Donates "
            "electrons directly to coenzyme Q in the ETC."),
        primary_role=(
            "Electron donor to Complex II + electron-"
            "transferring flavoprotein (ETF)",
        ),
        carriers_or_substrates=(
            "2 H atoms (2 e⁻ + 2 H⁺)",
        ),
        key_features=(
            "Lower-energy electron carrier than NADH — yields "
            "~ 1.5 ATP per molecule via ox-phos",
            "Almost always remains protein-bound; rarely "
            "diffusible",
        ),
        vitamin_origin=(
            "Riboflavin (vitamin B2)",
        ),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "ox_phos", "beta_oxidation",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Fatty-acid β-oxidation generates 1 FADH₂ per "
            "cycle (acyl-CoA dehydrogenase step)."),
    ),
    Cofactor(
        id="fmn",
        name="FMN",
        cofactor_class="flavin",
        chemical_summary=(
            "Flavin mononucleotide — riboflavin-5'-phosphate.  "
            "FAD minus the AMP moiety."),
        primary_role=(
            "Prosthetic group of Complex I (NADH dehydrogenase) "
            "+ several other flavoenzymes",
        ),
        carriers_or_substrates=(
            "Hydride (H⁻)",
        ),
        key_features=(
            "First electron acceptor in Complex I — receives "
            "the hydride from NADH",
            "Used in commercial firefly-luciferase reactions + "
            "blue-light photoreceptors (cryptochromes, "
            "phototropins)",
        ),
        vitamin_origin=(
            "Riboflavin (vitamin B2)",
        ),
        deficiency_disease=(
            "Ariboflavinosis (see FAD)",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "ox_phos",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Cryptochromes (FMN-containing flavoproteins) are "
            "the leading candidate for the magneto-receptor "
            "in migratory birds — radical-pair quantum-"
            "biology mechanism."),
    ),

    # ============================================================
    # Acyl carriers (2)
    # ============================================================
    Cofactor(
        id="coa",
        name="Coenzyme A (CoA / CoA-SH)",
        cofactor_class="acyl-carrier",
        chemical_summary=(
            "Pantothenate + cysteamine + ADP-3'-phosphate.  "
            "Terminal thiol forms thioester bonds with acyl "
            "groups."),
        primary_role=(
            "Acyl-group carrier via high-energy thioester bond",
        ),
        carriers_or_substrates=(
            "Acyl groups (acetyl, propionyl, succinyl, "
            "palmitoyl, …)",
        ),
        key_features=(
            "Thioester ΔG° hydrolysis ~ -31.5 kJ/mol — "
            "comparable to ATP",
            "Activated form: R-CO-S-CoA",
            "Cellular CoA + acyl-CoA pool ≈ 100 µM",
        ),
        vitamin_origin=(
            "Pantothenate (vitamin B5)",
        ),
        deficiency_disease=(
            "Pantothenate deficiency is rare in humans; "
            "Hallervorden-Spatz disease (PKAN) results from "
            "defective CoA biosynthesis → brain iron "
            "accumulation",
        ),
        cross_reference_enzyme_ids=(
            "acc",
        ),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "beta_oxidation",
            "fatty_acid_synthesis",
            "cholesterol_biosynthesis", "heme_biosynthesis",
        ),
        cross_reference_molecule_names=(
            "Coenzyme A (CoA-SH)",
        ),
        notes=(
            "CoA was discovered + named by Fritz Lipmann "
            "(Nobel 1953); A stands for ‘activation’ of "
            "acetate."),
    ),
    Cofactor(
        id="acetyl-coa",
        name="Acetyl-CoA",
        cofactor_class="acyl-carrier",
        chemical_summary=(
            "CoA esterified with an acetyl group; the central "
            "metabolic intermediate connecting carbohydrate, "
            "lipid, amino-acid catabolism, + biosynthesis."),
        primary_role=(
            "Universal 2-carbon donor for the TCA cycle, "
            "fatty-acid + cholesterol biosynthesis, and "
            "histone acetylation",
        ),
        carriers_or_substrates=(
            "Acetyl group (CH₃-CO-)",
        ),
        key_features=(
            "Generated by pyruvate dehydrogenase (carb), "
            "β-oxidation (lipid), + amino-acid catabolism "
            "(some AAs)",
            "Mitochondrial acetyl-CoA cannot cross the inner "
            "membrane — exported to cytosol as citrate (the "
            "citrate shuttle) for fatty-acid synthesis",
            "Cytosolic + nuclear acetyl-CoA also drives "
            "histone H3K9 / H3K14 / H3K27 acetylation — links "
            "metabolism to epigenetics",
        ),
        vitamin_origin=(
            "Pantothenate (vitamin B5)",
        ),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(
            "acc",
        ),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "beta_oxidation",
            "fatty_acid_synthesis",
            "cholesterol_biosynthesis",
        ),
        cross_reference_molecule_names=(
            "Acetyl-CoA",
        ),
        notes=(
            "ATP-citrate lyase (ACLY) regenerates cytosolic "
            "acetyl-CoA from citrate — a major drug target in "
            "metabolic disease + cancer."),
    ),

    # ============================================================
    # Methyl donor (1)
    # ============================================================
    Cofactor(
        id="sam",
        name="SAM (S-adenosyl methionine)",
        cofactor_class="methyl-donor",
        chemical_summary=(
            "Methionine activated by attachment to 5'-deoxy"
            "adenosyl group via a sulfonium centre.  The "
            "high-energy methyl bond to the positively-charged "
            "sulfur drives essentially every methyl-transfer "
            "reaction in the cell."),
        primary_role=(
            "Universal methyl-group donor for DNA / RNA / "
            "protein / small-molecule methylation",
            "Precursor to polyamines + biotin biosynthesis "
            "via 5'-deoxyadenosyl radicals",
        ),
        carriers_or_substrates=(
            "Methyl group (CH₃-)",
            "5'-deoxyadenosyl radical (radical-SAM enzymes)",
        ),
        key_features=(
            "Sulfonium centre is what makes the methyl group "
            "electrophilic + transferable",
            "Becomes SAH (S-adenosyl homocysteine) after "
            "methyl transfer — SAH is a strong product "
            "inhibitor of methyltransferases, so the SAM/SAH "
            "ratio sets methylation capacity",
        ),
        vitamin_origin=(
            "Methionine + ATP (no direct vitamin link, but "
            "methionine resynthesis depends on B12 + folate)",
        ),
        deficiency_disease=(
            "Hyperhomocysteinaemia (high SAH / low SAM) "
            "associated with cardiovascular + neuro"
            "developmental disease",
        ),
        cross_reference_enzyme_ids=(
            "comt",
        ),
        cross_reference_metabolic_pathway_ids=(
            "urea_cycle",
        ),
        cross_reference_molecule_names=(
            "S-Adenosyl-L-methionine (SAM)",
        ),
        notes=(
            "Radical-SAM enzymes (~ 100 000 in known "
            "proteomes) homolytically cleave the C5'-S bond "
            "to generate 5'-deoxyadenosyl radicals — the "
            "largest enzyme superfamily by sequence."),
    ),

    # ============================================================
    # Phosphate-energy currency (4)
    # ============================================================
    Cofactor(
        id="atp",
        name="ATP (adenosine-5'-triphosphate)",
        cofactor_class="phosphate-energy",
        chemical_summary=(
            "Adenosine + 3 phosphates linked by 2 high-energy "
            "phosphoanhydride bonds.  The universal cellular "
            "energy currency."),
        primary_role=(
            "Phosphoryl-group donor for kinases",
            "Energy currency for biosynthesis, transport, "
            "muscle contraction, + signalling",
        ),
        carriers_or_substrates=(
            "Phosphoryl group (-PO₃²⁻)",
            "AMP + PPi (when used as nucleotide donor)",
        ),
        key_features=(
            "ΔG°' hydrolysis to ADP + Pi: -30.5 kJ/mol; "
            "intracellular ΔG ≈ -55 kJ/mol due to mass-action",
            "Cellular [ATP] ~ 2-10 mM with rapid turnover "
            "(~ 0.1 sec half-life)",
            "Adult human turns over ~ body-weight ATP / day",
        ),
        vitamin_origin=(),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(
            "hexokinase", "pka", "egfr-tk", "atp-synthase",
            "na-k-atpase", "adenylate-cyclase",
            "glutamine-synthetase", "pyruvate-carboxylase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "glycolysis", "tca_cycle", "ox_phos",
            "fatty_acid_synthesis",
            "cholesterol_biosynthesis", "urea_cycle",
            "glycogen_metabolism", "calvin_cycle",
        ),
        cross_reference_molecule_names=(
            "ATP (adenosine-5'-triphosphate)",
        ),
        notes=(
            "ATP synthase (Complex V) was structurally + "
            "mechanistically solved by John Walker (Nobel "
            "1997) — the rotary F₁ catalytic head was "
            "Boyer's 1997 binding-change hypothesis confirmed "
            "in atomic detail."),
    ),
    Cofactor(
        id="adp",
        name="ADP (adenosine-5'-diphosphate)",
        cofactor_class="phosphate-energy",
        chemical_summary=(
            "Adenosine + 2 phosphates.  The 'spent' form of "
            "ATP after one phosphoryl transfer."),
        primary_role=(
            "Substrate for ATP synthase regeneration",
            "Allosteric activator of glycolysis (signals low "
            "energy state)",
        ),
        carriers_or_substrates=(
            "Phosphate group (acceptor in ATP regeneration)",
        ),
        key_features=(
            "AMPK is activated by AMP / ADP rise (low energy "
            "state) — central energy-stress sensor",
            "Mitochondrial ADP/ATP ratio gates ox-phos rate",
        ),
        vitamin_origin=(),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(
            "atp-synthase", "pyruvate-carboxylase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "glycolysis", "ox_phos",
        ),
        cross_reference_molecule_names=(
            "ADP (adenosine-5'-diphosphate)",
        ),
        notes=(
            "Platelets are activated by extracellular ADP "
            "binding to P2Y₁ + P2Y₁₂ receptors — clopidogrel "
            "/ ticagrelor block P2Y₁₂."),
    ),
    Cofactor(
        id="amp-cyclic",
        name="cAMP (3',5'-cyclic AMP)",
        cofactor_class="phosphate-energy",
        chemical_summary=(
            "Cyclic phosphodiester linking 3'-OH + 5'-OH of "
            "the adenosine ribose.  Generated from ATP by "
            "adenylate cyclase; degraded by phosphodiesterases."),
        primary_role=(
            "Universal second messenger downstream of Gαs-"
            "coupled GPCRs",
            "Activator of PKA + Epac",
        ),
        carriers_or_substrates=(
            "Information signal (not a chemical group "
            "transferred)",
        ),
        key_features=(
            "First second messenger discovered (Earl "
            "Sutherland, Nobel 1971)",
            "Concentration-amplification cascade: 1 receptor "
            "→ 100 cAMP → 100 PKA → 1000s of targets",
        ),
        vitamin_origin=(),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(
            "adenylate-cyclase", "pka",
        ),
        cross_reference_metabolic_pathway_ids=(),
        cross_reference_molecule_names=(
            "cAMP (3',5'-cyclic AMP)",
        ),
        notes=(
            "Cholera toxin ADP-ribosylates Gαs → constitutive "
            "adenylate cyclase activity → massive cAMP rise "
            "in enterocytes → CFTR Cl⁻ secretion → secretory "
            "diarrhoea."),
    ),
    Cofactor(
        id="gtp",
        name="GTP (guanosine-5'-triphosphate)",
        cofactor_class="phosphate-energy",
        chemical_summary=(
            "Guanine analogue of ATP.  Same 2 high-energy "
            "phosphoanhydride bonds; preferred phosphoryl "
            "donor for some specific niches."),
        primary_role=(
            "Substrate for protein synthesis (peptide-bond + "
            "translocation steps on the ribosome)",
            "Energy + binary-switch for small + heterotrimeric "
            "G-proteins (Ras, Rho, Rab, Gα)",
            "Substrate for succinyl-CoA synthetase in the TCA "
            "cycle",
        ),
        carriers_or_substrates=(
            "Phosphoryl group",
        ),
        key_features=(
            "Binary on/off switch: GTP-bound = active, GDP-"
            "bound = inactive (for G-proteins)",
            "Intrinsic GTPase activity is slow → GAPs + GEFs "
            "regulate the on/off cycle",
        ),
        vitamin_origin=(),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "calvin_cycle",
        ),
        cross_reference_molecule_names=(
            "GTP (guanosine-5'-triphosphate)",
        ),
        notes=(
            "Oncogenic Ras mutations (G12, G13, Q61) impair "
            "GTPase activity → constitutive Ras-GTP → "
            "uncontrolled growth signalling.  Sotorasib + "
            "adagrasib trap KRAS-G12C in the GDP state."),
    ),

    # ============================================================
    # Vitamin-prosthetic-group cofactors (5)
    # ============================================================
    Cofactor(
        id="biotin",
        name="Biotin (vitamin B7)",
        cofactor_class="biotin-vitamin",
        chemical_summary=(
            "Bicyclic ureido-thiophane attached covalently via "
            "ε-amino-lysine amide on the apoenzyme.  The "
            "tethered ‘swinging arm’ shuttles a CO₂ group "
            "between two active-site lobes."),
        primary_role=(
            "Carboxyl-group carrier for ATP-dependent "
            "carboxylases",
        ),
        carriers_or_substrates=(
            "CO₂ (as carboxybiotin intermediate)",
        ),
        key_features=(
            "Covalently linked via biotin protein ligase "
            "(holocarboxylase synthetase)",
            "Avidin (egg-white protein) binds biotin "
            "essentially irreversibly (Kd ~ 10⁻¹⁵ M) — "
            "the basis of countless biochemistry assays",
        ),
        vitamin_origin=(
            "Biotin (vitamin B7 / vitamin H)",
        ),
        deficiency_disease=(
            "Biotin deficiency (rare): dermatitis, alopecia, "
            "encephalopathy.  Holocarboxylase synthetase or "
            "biotinidase deficiency → multi-carboxylase "
            "deficiency in newborns",
        ),
        cross_reference_enzyme_ids=(
            "acc", "pyruvate-carboxylase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "fatty_acid_synthesis", "tca_cycle",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Streptavidin-biotin technology (Wilchek + Bayer, "
            "1988) is the most-used affinity chemistry in "
            "biology — pull-downs, ELISAs, microscopy, "
            "proteomics, sequencing."),
    ),
    Cofactor(
        id="tpp",
        name="TPP (thiamine pyrophosphate, vitamin B1)",
        cofactor_class="tpp-vitamin",
        chemical_summary=(
            "Thiamine + diphosphate.  Catalytically active C2 "
            "of the thiazolium ring (acidic carbanion) attacks "
            "α-keto carbon → stabilises ‘active aldehyde’ "
            "intermediate."),
        primary_role=(
            "Decarboxylation of α-keto acids + transketolase "
            "transfer of 2-carbon (glycolaldehyde) units",
        ),
        carriers_or_substrates=(
            "α-Keto-acid carbanion intermediate",
            "Glycolaldehyde (transketolase)",
        ),
        key_features=(
            "Without TPP, decarboxylation of α-keto acids "
            "would be near-impossible at body temperature",
            "Pyruvate dehydrogenase + α-ketoglutarate "
            "dehydrogenase + branched-chain α-keto acid "
            "dehydrogenase + transketolase + pyruvate "
            "decarboxylase all share TPP",
        ),
        vitamin_origin=(
            "Thiamine (vitamin B1)",
        ),
        deficiency_disease=(
            "Beriberi: peripheral neuropathy + cardio"
            "myopathy; Wernicke-Korsakoff syndrome in chronic "
            "alcoholism (alcohol blocks thiamine absorption)",
        ),
        cross_reference_enzyme_ids=(
            "pyruvate-decarboxylase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle", "pentose_phosphate",
        ),
        cross_reference_molecule_names=(
            "Thiamine",
        ),
        notes=(
            "First vitamin discovered (Funk, 1912 — coined "
            "‘vitamine’ as ‘vital amine’).  Eijkman's chicken "
            "polyneuritis experiment (Nobel 1929) was the "
            "founding deficiency-disease study."),
    ),
    Cofactor(
        id="plp",
        name="PLP (pyridoxal-5'-phosphate, vitamin B6)",
        cofactor_class="plp-vitamin",
        chemical_summary=(
            "Pyridoxal + 5'-phosphate.  Aldehyde at C4 forms "
            "a Schiff base (internal aldimine) with an active-"
            "site lysine.  The ε-amino of the lysine is then "
            "displaced by the substrate amino group → external "
            "aldimine → quinonoid intermediate that supports "
            "almost every reaction class for amino acids."),
        primary_role=(
            "Universal cofactor for amino-acid transamination, "
            "decarboxylation, racemisation, β-elimination, "
            "γ-elimination, and aldol-type cleavage",
        ),
        carriers_or_substrates=(
            "Amino group (aminotransferase reactions)",
            "Carbanion stabilisation (decarboxylase reactions)",
        ),
        key_features=(
            "Most chemically-versatile cofactor known — "
            "supports > 5 distinct reaction types",
            "Catalytic mechanism elucidated by Esmond Snell "
            "+ Alexander Braunstein in the 1950s",
        ),
        vitamin_origin=(
            "Pyridoxine (vitamin B6)",
        ),
        deficiency_disease=(
            "Peripheral neuropathy + sideroblastic anaemia + "
            "microcytic anaemia (heme biosynthesis depends on "
            "PLP-dependent ALA synthase)",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "urea_cycle", "heme_biosynthesis",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Isoniazid (anti-tuberculosis) sequesters PLP → "
            "supplemental pyridoxine routinely co-prescribed "
            "to prevent peripheral neuropathy."),
    ),
    Cofactor(
        id="lipoate",
        name="Lipoic acid",
        cofactor_class="lipoate",
        chemical_summary=(
            "8-carbon dithiol (C6 + C8 disulfide bond) "
            "covalently attached via lysine ε-amino group.  "
            "Reduced + oxidised forms shuttle acyl groups + "
            "electrons between active-site lobes."),
        primary_role=(
            "Acyl carrier + reductant for the E2 component of "
            "α-keto-acid dehydrogenase complexes",
        ),
        carriers_or_substrates=(
            "Acyl groups", "Electrons (via dithiol/disulfide "
            "interconversion)",
        ),
        key_features=(
            "Pyruvate dehydrogenase + α-ketoglutarate "
            "dehydrogenase + branched-chain α-keto acid "
            "dehydrogenase + glycine cleavage system all "
            "share lipoamide on E2",
            "Lipoamide is the prosthetic-group form (lipoyl-"
            "lysine amide)",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Lipoic acid synthase deficiency: severe neonatal "
            "encephalopathy + lactic acidosis (rare inborn "
            "error)",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "tca_cycle",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Sold as a dietary supplement for putative "
            "antioxidant + insulin-sensitising effects — "
            "evidence base in healthy adults is weak."),
    ),

    # ============================================================
    # Cobalamin + Folate (2)
    # ============================================================
    Cofactor(
        id="cobalamin",
        name="Cobalamin (vitamin B12)",
        cofactor_class="cobalamin-vitamin",
        chemical_summary=(
            "Corrin-ring-coordinated cobalt centre.  Two "
            "active forms: methylcobalamin (methyl ligand on "
            "Co) for methionine synthase + adenosylcobalamin "
            "(5'-deoxyadenosyl ligand on Co) for methylmalonyl-"
            "CoA mutase."),
        primary_role=(
            "Methyl donor for methionine resynthesis + "
            "intramolecular rearrangement of methylmalonyl-CoA "
            "→ succinyl-CoA",
        ),
        carriers_or_substrates=(
            "Methyl group (methylcobalamin)",
            "5'-deoxyadenosyl radical (adenosylcobalamin)",
        ),
        key_features=(
            "Only vitamin synthesised exclusively by "
            "microorganisms — humans depend entirely on "
            "dietary intake (or microbial gut synthesis)",
            "Absorption requires intrinsic factor (gastric "
            "parietal-cell glycoprotein) + ileal receptor",
            "Cobalt is the only biological role for cobalt "
            "in mammals",
        ),
        vitamin_origin=(
            "Cobalamin (vitamin B12)",
        ),
        deficiency_disease=(
            "Megaloblastic anaemia + subacute combined "
            "degeneration of the spinal cord (peripheral "
            "neuropathy + posterior column dysfunction)",
            "Pernicious anaemia: autoimmune destruction of "
            "intrinsic-factor-secreting parietal cells",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "urea_cycle",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "The structural elucidation by Dorothy Hodgkin "
            "(X-ray crystallography, Nobel 1964) was a "
            "landmark — at ~ 90 atoms, B12 was the largest "
            "structure solved before computer methods."),
    ),
    Cofactor(
        id="tetrahydrofolate",
        name="Tetrahydrofolate (THF, vitamin B9)",
        cofactor_class="folate",
        chemical_summary=(
            "Pteridine + p-aminobenzoate + glutamate "
            "(typically poly-glutamylated in cells).  Carries "
            "1-carbon units at the N5 + N10 positions in "
            "various oxidation states (methyl, methylene, "
            "methenyl, formyl, formimino)."),
        primary_role=(
            "Universal one-carbon donor for nucleotide "
            "biosynthesis (purine ring + thymidylate) + "
            "methionine resynthesis",
        ),
        carriers_or_substrates=(
            "1-carbon units in 5 oxidation states "
            "(-CH₃ / -CH₂- / =CH- / -CHO / -CHNH-)",
        ),
        key_features=(
            "Most cellular folate is poly-γ-glutamylated for "
            "retention",
            "Direct biosynthetic target of antifolate drugs "
            "(methotrexate → DHFR; trimethoprim → bacterial "
            "DHFR; sulfonamides → bacterial DHPS)",
            "Folinic acid (5-formyl-THF, leucovorin) bypasses "
            "DHFR + rescues methotrexate toxicity",
        ),
        vitamin_origin=(
            "Folate (vitamin B9)",
        ),
        deficiency_disease=(
            "Megaloblastic anaemia (similar to B12)",
            "Neural-tube defects (anencephaly, spina bifida) "
            "in fetuses of folate-deficient mothers — driver "
            "of mandatory folate fortification of grain "
            "products in many countries",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Methotrexate (Sidney Farber, 1948) was the first "
            "rationally-designed antimetabolite + the first "
            "drug to put childhood acute lymphoblastic "
            "leukaemia into remission."),
    ),

    # ============================================================
    # Metal cofactors (3)
    # ============================================================
    Cofactor(
        id="heme",
        name="Heme (iron-protoporphyrin IX)",
        cofactor_class="metal-cluster",
        chemical_summary=(
            "Tetrapyrrole macrocycle (protoporphyrin IX) "
            "coordinating a central Fe²⁺ / Fe³⁺ ion.  Several "
            "axial-ligand variants (b, c, a, …) tune redox + "
            "spectral properties."),
        primary_role=(
            "Reversible O₂ binding (haemoglobin, myoglobin)",
            "Electron transfer (cytochromes b / c)",
            "Oxygen activation (cytochrome P450s, catalase, "
            "peroxidase)",
        ),
        carriers_or_substrates=(
            "O₂", "Electrons", "Oxygen-atom transfer (P450s)",
        ),
        key_features=(
            "Heme b (in haemoglobin + cytochrome b)",
            "Heme c (covalently attached via 2 Cys-thioether "
            "bonds; cytochrome c)",
            "Heme a (Complex IV; isoprenoid tail + formyl group)",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Porphyrias: defects in heme biosynthesis enzymes "
            "→ accumulation of toxic intermediates",
            "Iron-deficiency anaemia (heme synthesis limited "
            "by Fe supply)",
        ),
        cross_reference_enzyme_ids=(
            "cytochrome-c-oxidase", "cyp3a4",
        ),
        cross_reference_metabolic_pathway_ids=(
            "ox_phos", "heme_biosynthesis",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Cytochrome P450s carry > 80 % of clinical drug "
            "metabolism (CYP3A4 alone ~ 50 %).  Heme spin-state "
            "transitions are detectable by absorbance + drive "
            "the iconic Soret band assay."),
    ),
    Cofactor(
        id="magnesium-ion",
        name="Magnesium (Mg²⁺)",
        cofactor_class="metal-cluster",
        chemical_summary=(
            "Divalent cation; essential metal cofactor for "
            "every kinase + phosphatase (the substrate is "
            "actually the Mg²⁺-bound form of ATP / ADP).  "
            "Also stabilises ribosomal RNA + DNA polymerase "
            "active sites."),
        primary_role=(
            "Charge-screening + transition-state stabilisation "
            "for phosphoryl transfer",
            "Structural cofactor for ribosomes + polymerases",
            "Activator of ~ 600 + enzymes",
        ),
        carriers_or_substrates=(
            "(structural / catalytic role — not a chemical "
            "carrier)",
        ),
        key_features=(
            "ATP in solution exists ~ 99 % as Mg²⁺-ATP; the "
            "free [Mg²⁺] in cells is ~ 0.5-1 mM",
            "Two-metal-ion catalysis in DNA / RNA polymerases "
            "(Steitz model)",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Hypomagnesaemia: arrhythmias, neuromuscular "
            "irritability, refractory hypocalcaemia + "
            "hypokalaemia (Mg is needed for K-channel + Ca-"
            "handling)",
        ),
        cross_reference_enzyme_ids=(
            "hexokinase", "atp-synthase", "egfr-tk",
        ),
        cross_reference_metabolic_pathway_ids=(
            "glycolysis", "ox_phos",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Chlorophyll's central ion is Mg²⁺ — the same "
            "divalent cation drives photosynthesis + every "
            "kinase reaction in the cell.  Useful symmetry "
            "to teach by."),
    ),
    Cofactor(
        id="zinc-ion",
        name="Zinc (Zn²⁺)",
        cofactor_class="metal-cluster",
        chemical_summary=(
            "Divalent cation; the most-common transition "
            "metal in the human proteome (~ 10 % of human "
            "proteins are Zn-binding).  Strong Lewis acid "
            "with no redox activity at biological potentials "
            "→ ideal for catalysis without side reactions."),
        primary_role=(
            "Lewis-acid catalysis in hydrolases (carbonic "
            "anhydrase, carboxypeptidase, matrix metallo"
            "proteinases, alcohol dehydrogenase)",
            "Structural cofactor in zinc-finger transcription "
            "factors + RING + LIM + PHD domains",
        ),
        carriers_or_substrates=(
            "(catalytic / structural role)",
        ),
        key_features=(
            "Carbonic anhydrase II achieves k_cat ~ 10⁶ s⁻¹ "
            "— one of the fastest enzymes known",
            "Matrix metalloproteinases (MMPs) drive ECM "
            "remodelling + are key targets in cancer + "
            "inflammation",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Acrodermatitis enteropathica (autosomal-"
            "recessive ZIP4 transporter loss)",
            "Acquired zinc deficiency: alopecia, dermatitis, "
            "diarrhoea, immunodeficiency",
        ),
        cross_reference_enzyme_ids=(
            "carbonic-anhydrase-ii", "alcohol-dehydrogenase",
        ),
        cross_reference_metabolic_pathway_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "Zn-finger transcription factors (~ 1 000 in the "
            "human genome) are the largest TF family; "
            "TALEN + ZFN gene-editing tools exploit the "
            "tunable DNA-recognition specificity."),
    ),

    # ============================================================
    # Quinone electron carriers (2)
    # ============================================================
    Cofactor(
        id="ubiquinone",
        name="Ubiquinone (CoQ10)",
        cofactor_class="quinone",
        chemical_summary=(
            "Benzoquinone with a 50-carbon (10-isoprene-unit) "
            "lipophilic tail.  Anchored in the inner mito"
            "chondrial membrane.  Cycles between quinone + "
            "semiquinone + quinol forms."),
        primary_role=(
            "Mobile 2-electron + 2-proton carrier between "
            "Complex I / II and Complex III in the ETC",
        ),
        carriers_or_substrates=(
            "2 e⁻ + 2 H⁺ (between membrane-embedded "
            "complexes)",
        ),
        key_features=(
            "Q-cycle (Mitchell) at Complex III pumps 4 H⁺ "
            "per 2 electrons — proton-motive amplification",
            "Cellular site of action for statins' mevalonate-"
            "depletion side-effect — myopathy + ‘CoQ10 "
            "depletion’ debate",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Primary CoQ10 deficiencies: encephalo-myopathy, "
            "nephrotic syndrome, ataxia, intellectual "
            "disability (rare)",
        ),
        cross_reference_enzyme_ids=(
            "cytochrome-c-oxidase",
        ),
        cross_reference_metabolic_pathway_ids=(
            "ox_phos", "cholesterol_biosynthesis",
        ),
        cross_reference_molecule_names=(),
        notes=(
            "Sold as a heart + anti-aging supplement; "
            "evidence in heart failure is weak but "
            "consistent enough that it remains in some "
            "guideline footnotes."),
    ),
    Cofactor(
        id="plastoquinone",
        name="Plastoquinone",
        cofactor_class="quinone",
        chemical_summary=(
            "Plant-chloroplast analogue of ubiquinone.  "
            "Benzoquinone with a 9-isoprene lipophilic tail.  "
            "Mobile electron carrier in the photosynthetic "
            "thylakoid membrane."),
        primary_role=(
            "Electron carrier between Photosystem II and the "
            "cytochrome b₆f complex",
        ),
        carriers_or_substrates=(
            "2 e⁻ + 2 H⁺",
        ),
        key_features=(
            "Q-cycle at cyt b₆f mirrors mitochondrial "
            "Complex III architecture — convergent design",
            "DCMU + atrazine herbicides bind the plastoquinone "
            "QB pocket of PSII → block electron flow → "
            "kill the plant",
        ),
        vitamin_origin=(),
        deficiency_disease=(),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "calvin_cycle",
        ),
        cross_reference_molecule_names=(
            "Plastoquinone-9",
        ),
        notes=(
            "Plastoquinone synthesis is targeted by HPPD "
            "inhibitors (mesotrione, tembotrione, isoxa"
            "flutole) — bleaching herbicides used on maize."),
    ),

    # ============================================================
    # Redox-buffer small molecules (2)
    # ============================================================
    Cofactor(
        id="glutathione",
        name="Glutathione (GSH / GSSG)",
        cofactor_class="redox-buffer",
        chemical_summary=(
            "Tripeptide γ-Glu-Cys-Gly.  The unusual γ-glutamyl "
            "linkage protects it from peptidase digestion.  "
            "Cysteine thiol cycles between reduced (GSH) + "
            "oxidised disulfide-bridged dimer (GSSG)."),
        primary_role=(
            "Major cellular redox buffer (mM concentration)",
            "Substrate for glutathione peroxidase + "
            "glutathione-S-transferase in xenobiotic + "
            "lipid-peroxide detoxification",
        ),
        carriers_or_substrates=(
            "2 H atoms (reduction equivalents)",
            "Sulfhydryl group (conjugation reactions)",
        ),
        key_features=(
            "Cellular [GSH] ≈ 5 mM; [GSH]/[GSSG] ratio > 100 "
            "in healthy cytosol",
            "Drug conjugation via mercapturate pathway "
            "(GSH → cysteine conjugate → N-acetylcysteine "
            "metabolite → urine)",
            "Acetaminophen overdose depletes GSH → NAPQI "
            "buildup → hepatocellular necrosis; N-acetyl"
            "cysteine treatment replenishes precursors",
        ),
        vitamin_origin=(),
        deficiency_disease=(
            "Inherited γ-glutamyl-cysteine synthetase "
            "deficiency (rare): haemolytic anaemia",
            "G6PD deficiency: secondary GSH depletion → "
            "haemolysis on oxidative stress",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(
            "pentose_phosphate",
        ),
        cross_reference_molecule_names=(
            "Glutathione",
        ),
        notes=(
            "Selenium is required for glutathione peroxidase "
            "(Se-cysteine in the active site) — Keshan disease "
            "is the cardiomyopathy of selenium deficiency."),
    ),
    Cofactor(
        id="ascorbate",
        name="Ascorbate (vitamin C)",
        cofactor_class="redox-buffer",
        chemical_summary=(
            "Lactone with an enediol that ionises to a stable "
            "ascorbate radical (semidehydroascorbate) on "
            "1-electron oxidation."),
        primary_role=(
            "Cofactor for Fe²⁺-dependent dioxygenases "
            "(prolyl + lysyl hydroxylases, JmjC histone "
            "demethylases, TET DNA demethylases) — keeps the "
            "active-site iron in the reduced state",
            "Major aqueous-phase antioxidant",
        ),
        carriers_or_substrates=(
            "Single electrons (recycles iron in dioxygenase "
            "active sites)",
        ),
        key_features=(
            "Humans + great apes + guinea pigs cannot "
            "synthesise vitamin C (loss-of-function "
            "L-gulonolactone oxidase pseudogene) → dietary "
            "requirement",
            "Critical for collagen post-translational "
            "modification — without it, collagen triple-helix "
            "stability fails",
        ),
        vitamin_origin=(
            "Ascorbate (vitamin C)",
        ),
        deficiency_disease=(
            "Scurvy: defective collagen → bleeding gums, "
            "loose teeth, poor wound healing, perifollicular "
            "haemorrhages, fatigue.  Historic killer of long-"
            "voyage sailors before James Lind's 1747 lemon-"
            "juice trial",
        ),
        cross_reference_enzyme_ids=(),
        cross_reference_metabolic_pathway_ids=(),
        cross_reference_molecule_names=(),
        notes=(
            "TET enzymes (10-11 translocation) hydroxylate "
            "5-methylcytosine → 5-hydroxymethylcytosine — "
            "the active DNA-demethylation pathway, ascorbate-"
            "dependent."),
    ),
)
