"""Phase 45 (round 149) — lab-reagents reference catalogue.

A reference catalogue of the chemicals + biologicals routinely
ordered as off-the-shelf lab reagents.  Distinct from the Phase-6
*molecule database* (which is structure-first) by keying entries
to **how the reagent is used in the lab**: typical working
concentration, storage, hazards, preparation tips, CAS number,
representative usage notes.

Pure-headless: no Qt imports.  Lookup helpers `list_reagents`,
`get_reagent`, `find_reagents`, `categories()`, plus a
`reagent_to_dict` JSON-serialiser.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Dict, List, Optional, Tuple

VALID_CATEGORIES: Tuple[str, ...] = (
    "buffer",
    "acid-base",
    "detergent",
    "reducing-agent",
    "salt",
    "protein-prep",
    "stain",
    "solvent",
    "cell-culture",
    "molecular-biology",
)


@dataclass(frozen=True)
class LabReagent:
    """One off-the-shelf lab reagent."""
    id: str
    name: str
    category: str
    typical_concentration: str
    storage: str
    hazards: str
    preparation_notes: str
    cas_number: str
    typical_usage: str
    notes: str = ""


# ----------------------------------------------------------------
# Catalogue
# ----------------------------------------------------------------
_REAGENTS: List[LabReagent] = [

    # ---------------- Buffers ----------------
    LabReagent(
        id="tris-hcl",
        name="Tris-HCl",
        category="buffer",
        typical_concentration="10–100 mM (working), 1 M (stock)",
        storage="Room temperature; sterile-filter for cell work",
        hazards="Skin / eye irritant in solid form",
        preparation_notes="Dissolve Tris base in water, titrate "
                          "to target pH with conc. HCl at 25 °C "
                          "(pH drifts ~0.03/°C, so always pH at "
                          "the use temperature)",
        cas_number="77-86-1",
        typical_usage="Most common protein-biochemistry buffer; "
                      "useful pH range 7.0–9.0 (pKa 8.10)",
        notes="Avoid Tris with primary-amine-reactive chemistry "
              "(e.g. NHS-esters, glutaraldehyde) — the amine "
              "group in Tris will quench the reaction.",
    ),
    LabReagent(
        id="hepes",
        name="HEPES",
        category="buffer",
        typical_concentration="10–50 mM (working), 1 M (stock)",
        storage="Room temperature; sterile-filter for cell work",
        hazards="Mild irritant",
        preparation_notes="Dissolve free acid or sodium salt, "
                          "adjust pH 7.0–8.0 with NaOH; less "
                          "T-dependent than Tris",
        cas_number="7365-45-9",
        typical_usage="Good's buffer for cell culture and protein "
                      "biochemistry; useful pH 6.8–8.2 (pKa 7.55)",
        notes="Generates H₂O₂ under intense light + Fe²⁺ — "
              "store solutions away from light.",
    ),
    LabReagent(
        id="mops",
        name="MOPS",
        category="buffer",
        typical_concentration="10–50 mM (working)",
        storage="Room temperature, dark",
        hazards="Mild irritant",
        preparation_notes="Adjust pH 6.5–7.9 with NaOH",
        cas_number="1132-61-2",
        typical_usage="Good's buffer for RNA electrophoresis "
                      "(MOPS-EDTA-Na acetate) and bacterial "
                      "culture; useful pH 6.5–7.9 (pKa 7.20)",
    ),
    LabReagent(
        id="mes",
        name="MES",
        category="buffer",
        typical_concentration="10–50 mM (working)",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Adjust pH 5.5–6.7 with NaOH",
        cas_number="4432-31-9",
        typical_usage="Good's buffer for the lower pH range "
                      "(5.5–6.7, pKa 6.10); used in IEC, "
                      "carboxypeptidase reactions",
    ),
    LabReagent(
        id="pbs",
        name="PBS (phosphate-buffered saline)",
        category="buffer",
        typical_concentration="1× (137 mM NaCl / 2.7 mM KCl / "
                              "10 mM Na₂HPO₄ / 1.8 mM KH₂PO₄)",
        storage="Room temperature; autoclave or sterile-filter",
        hazards="None at working strength",
        preparation_notes="Make 10× stock and dilute as needed; "
                          "pH 7.4 ± 0.1 by formulation",
        cas_number="(formulation; no single CAS)",
        typical_usage="Universal isotonic wash for cells, "
                      "antibodies, ELISA, IHC; mild and "
                      "physiological",
    ),
    LabReagent(
        id="tbs",
        name="TBS (Tris-buffered saline)",
        category="buffer",
        typical_concentration="1× (50 mM Tris-HCl pH 7.5 / "
                              "150 mM NaCl)",
        storage="Room temperature",
        hazards="None at working strength",
        preparation_notes="Often used as TBST (TBS + 0.05–0.1 % "
                          "Tween 20) for Western-blot washes",
        cas_number="(formulation)",
        typical_usage="Substitute for PBS when phosphate "
                      "interferes (e.g. assays detecting "
                      "phosphate, alkaline-phosphatase work)",
    ),
    LabReagent(
        id="citrate-buffer",
        name="Sodium citrate buffer",
        category="buffer",
        typical_concentration="10 mM (antigen retrieval), "
                              "100 mM (general)",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Mix citric acid + sodium citrate to "
                          "target pH (3.0–6.2); pKa values 3.13 "
                          "/ 4.76 / 6.40",
        cas_number="6132-04-3",
        typical_usage="IHC heat-induced antigen retrieval "
                      "(pH 6.0); FPLC ion exchange; food-acid "
                      "model",
    ),
    LabReagent(
        id="carbonate-buffer",
        name="Sodium carbonate-bicarbonate buffer",
        category="buffer",
        typical_concentration="50–100 mM (ELISA coating)",
        storage="Room temperature",
        hazards="Mild alkaline irritant",
        preparation_notes="Mix Na₂CO₃ + NaHCO₃; pH 9.6 standard "
                          "for ELISA coating",
        cas_number="497-19-8",
        typical_usage="ELISA capture-antibody coating buffer; "
                      "Western-blot transfer (CAPS variant)",
    ),
    LabReagent(
        id="glycine-hcl",
        name="Glycine-HCl",
        category="buffer",
        typical_concentration="100 mM (elution)",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Dissolve glycine, adjust to pH 2.5 "
                          "or 2.8 with HCl",
        cas_number="6000-43-7",
        typical_usage="Acidic elution of antibodies from "
                      "Protein A/G affinity columns; "
                      "neutralise to Tris pH 8.5 immediately",
    ),
    LabReagent(
        id="mcilvaine",
        name="McIlvaine (citrate-phosphate) buffer",
        category="buffer",
        typical_concentration="Variable (citric acid + "
                              "Na₂HPO₄ in defined ratios)",
        storage="Room temperature",
        hazards="None at working strength",
        preparation_notes="Mix 0.1 M citric acid + 0.2 M "
                          "Na₂HPO₄ to ratio for desired pH "
                          "(2.2–8.0)",
        cas_number="(formulation)",
        typical_usage="Wide-pH-range buffer (2.2–8.0) for "
                      "enzyme kinetics; spans both citrate "
                      "and phosphate pKas",
    ),
    LabReagent(
        id="bis-tris",
        name="BIS-TRIS",
        category="buffer",
        typical_concentration="50 mM (NuPAGE running)",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Adjust to pH 6.0–7.0; pKa 6.50",
        cas_number="6976-37-0",
        typical_usage="Invitrogen NuPAGE neutral-pH SDS-PAGE; "
                      "preserves acid-labile proteins",
    ),

    # ---------------- Acids and bases ----------------
    LabReagent(
        id="hcl-1m",
        name="Hydrochloric acid (1 M)",
        category="acid-base",
        typical_concentration="1 M (pH-adjustment); 6 N for "
                              "amino-acid hydrolysis",
        storage="Room temperature, vented cabinet",
        hazards="Corrosive (skin / eye / respiratory); "
                "GHS05 + GHS07",
        preparation_notes="Dilute conc. HCl (12 N) into water "
                          "(NEVER reverse); always add acid to "
                          "water",
        cas_number="7647-01-0",
        typical_usage="Buffer pH adjustment; protein "
                      "hydrolysis (6 N at 110 °C); wash "
                      "glassware",
    ),
    LabReagent(
        id="h2so4-conc",
        name="Sulfuric acid (conc., 18 M)",
        category="acid-base",
        typical_concentration="2 N (ELISA stop), conc. "
                              "(piranha cleaning)",
        storage="Room temperature, vented cabinet",
        hazards="Highly corrosive + dehydrating; piranha "
                "is explosive with organics",
        preparation_notes="Always slowly into water, with "
                          "stirring + ice bath",
        cas_number="7664-93-9",
        typical_usage="ELISA TMB stop solution (2 N); "
                      "piranha (3:1 H₂SO₄ / 30 % H₂O₂) "
                      "for glassware",
    ),
    LabReagent(
        id="hno3-conc",
        name="Nitric acid (conc., 16 N)",
        category="acid-base",
        typical_concentration="2 % (ICP-MS); conc. (metal "
                              "etching)",
        storage="Room temperature, vented cabinet, away "
                "from organics",
        hazards="Strong oxidiser + corrosive; produces "
                "NOx fumes",
        preparation_notes="Trace-metal-grade for ICP-MS",
        cas_number="7697-37-2",
        typical_usage="ICP-MS / ICP-OES sample matrix "
                      "(2 %); metal-trace cleaning",
    ),
    LabReagent(
        id="acetic-acid-glacial",
        name="Acetic acid (glacial)",
        category="acid-base",
        typical_concentration="100 % (glacial); 50 mM "
                              "(working)",
        storage="Room temperature, vented",
        hazards="Corrosive; pungent; flammable above 39 °C",
        preparation_notes="Dilute with water for buffers",
        cas_number="64-19-7",
        typical_usage="Glacial freezes at 17 °C — keep "
                      "warm; stop solution for some assays; "
                      "Coomassie destain",
    ),
    LabReagent(
        id="naoh-1m",
        name="Sodium hydroxide (1 M / 10 N)",
        category="acid-base",
        typical_concentration="1 M (pH adjust); 10 N "
                              "(stock)",
        storage="Room temperature, plastic bottle (etches "
                "glass)",
        hazards="Corrosive (skin / eye); GHS05",
        preparation_notes="Dissolve NaOH in water — strongly "
                          "exothermic (use ice bath); avoid "
                          "atmospheric CO₂ uptake by capping",
        cas_number="1310-73-2",
        typical_usage="Buffer pH adjust; column regeneration; "
                      "0.5 M for general column sanitisation",
    ),
    LabReagent(
        id="koh",
        name="Potassium hydroxide",
        category="acid-base",
        typical_concentration="1 M",
        storage="Room temperature, dry, plastic",
        hazards="Corrosive",
        preparation_notes="Same handling as NaOH; sometimes "
                          "preferred for K-based buffers",
        cas_number="1310-58-3",
        typical_usage="K-form buffers; ethanolic-KOH for "
                      "saponification of fats",
    ),
    LabReagent(
        id="nh4oh-conc",
        name="Ammonium hydroxide (conc., 28 %)",
        category="acid-base",
        typical_concentration="28 % (conc.); 1 % – 5 % "
                              "(working)",
        storage="Cold (4 °C) to reduce vapour loss; vented "
                "cabinet",
        hazards="Corrosive; pungent NH₃ vapour",
        preparation_notes="Dilute in fume hood",
        cas_number="1336-21-6",
        typical_usage="DNA precipitation cleanup; "
                      "MS-friendly mobile-phase modifier; "
                      "metal sulfide dissolution",
    ),

    # ---------------- Detergents ----------------
    LabReagent(
        id="sds",
        name="SDS (sodium dodecyl sulfate)",
        category="detergent",
        typical_concentration="0.1 % (running buffer); 1 % "
                              "(sample buffer); 10 % (stock)",
        storage="Room temperature; precipitates < 15 °C "
                "(rewarm)",
        hazards="Irritant; respiratory sensitiser if powder "
                "inhaled — weigh in fume hood",
        preparation_notes="Anionic; CMC ~ 8 mM in water; "
                          "use 10 % stock",
        cas_number="151-21-3",
        typical_usage="SDS-PAGE; Laemmli sample buffer; "
                      "harsh protein-denaturing detergent; "
                      "interferes with mass spec",
    ),
    LabReagent(
        id="triton-x100",
        name="Triton X-100",
        category="detergent",
        typical_concentration="0.1–1 % (cell lysis, "
                              "permeabilisation)",
        storage="Room temperature; viscous liquid",
        hazards="Endocrine disruptor (4-tert-octylphenol "
                "residues); EU REACH-restricted",
        preparation_notes="Non-ionic; CMC ~ 0.2 mM",
        cas_number="9036-19-5",
        typical_usage="IF / IHC permeabilisation; mild "
                      "non-denaturing lysis; avoid in "
                      "downstream MS",
    ),
    LabReagent(
        id="tween-20",
        name="Tween 20 (polysorbate 20)",
        category="detergent",
        typical_concentration="0.05–0.1 % (Western blot, "
                              "ELISA)",
        storage="Room temperature; viscous liquid",
        hazards="Mild irritant",
        preparation_notes="Non-ionic; use 10 % stock",
        cas_number="9005-64-5",
        typical_usage="Block + wash buffers (TBST / PBST); "
                      "reduces non-specific antibody binding",
    ),
    LabReagent(
        id="np40",
        name="NP-40 / Igepal CA-630",
        category="detergent",
        typical_concentration="0.1–1 % (cell lysis)",
        storage="Room temperature, viscous",
        hazards="Mild irritant",
        preparation_notes="Non-ionic; nearly identical to "
                          "Igepal CA-630 (modern equivalent)",
        cas_number="9016-45-9",
        typical_usage="Co-IP lysis buffer; preserves most "
                      "protein-protein interactions",
    ),
    LabReagent(
        id="chaps",
        name="CHAPS",
        category="detergent",
        typical_concentration="0.5–2 % (membrane "
                              "solubilisation)",
        storage="Room temperature, dry",
        hazards="Mild irritant",
        preparation_notes="Zwitterionic; CMC ~ 8 mM",
        cas_number="75621-03-3",
        typical_usage="Membrane-protein solubilisation in "
                      "IEF / 2D-PAGE; preserves activity",
    ),
    LabReagent(
        id="n-octyl-glucoside",
        name="n-Octyl-β-D-glucoside",
        category="detergent",
        typical_concentration="1–2 % (above CMC 25 mM)",
        storage="4 °C; hygroscopic",
        hazards="Mild irritant",
        preparation_notes="Non-ionic; high CMC means "
                          "easy dialysis removal",
        cas_number="29836-26-8",
        typical_usage="Membrane-protein crystallography; "
                      "removable by dialysis (high CMC)",
    ),

    # ---------------- Reducing agents ----------------
    LabReagent(
        id="dtt",
        name="DTT (dithiothreitol)",
        category="reducing-agent",
        typical_concentration="1–10 mM (working); 1 M "
                              "(stock in water)",
        storage="−20 °C (stock); make fresh each day "
                "for working",
        hazards="Mild irritant; thiol smell",
        preparation_notes="Aliquot 1 M in water at −20 °C; "
                          "aerial oxidation halves potency "
                          "in days at room temperature",
        cas_number="3483-12-3",
        typical_usage="Reduce disulfide bonds in protein "
                      "samples; SDS-PAGE sample buffer; "
                      "Cys-targeted chemistry",
    ),
    LabReagent(
        id="bme",
        name="β-Mercaptoethanol (BME)",
        category="reducing-agent",
        typical_concentration="1–5 % v/v (sample buffer); "
                              "neat 14.3 M",
        storage="4 °C, vented; pungent",
        hazards="Toxic + foul smell — handle in fume hood",
        preparation_notes="Add fresh to Laemmli buffer "
                          "before use",
        cas_number="60-24-2",
        typical_usage="Cheaper, more volatile DTT "
                      "alternative; SDS-PAGE sample "
                      "buffer (5 % v/v)",
    ),
    LabReagent(
        id="tcep",
        name="TCEP (tris(2-carboxyethyl)phosphine)",
        category="reducing-agent",
        typical_concentration="1–10 mM",
        storage="4 °C (stock); odourless and stable",
        hazards="Mild irritant",
        preparation_notes="Solid stable indefinitely; "
                          "neutralise to pH 7 with NaOH if "
                          "needed",
        cas_number="51805-45-9",
        typical_usage="Maleimide / Cys chemistry "
                      "compatible (unlike DTT); MS-friendly",
    ),
    LabReagent(
        id="glutathione",
        name="Reduced glutathione (GSH)",
        category="reducing-agent",
        typical_concentration="10 mM (GST elution); "
                              "1–5 mM (refold redox)",
        storage="−20 °C powder; freshly dissolved",
        hazards="None at working strength",
        preparation_notes="Adjust to pH 8.0 with NaOH for "
                          "GST elution",
        cas_number="70-18-8",
        typical_usage="Elute GST-tagged proteins from "
                      "glutathione-Sepharose; refold "
                      "buffer redox couple (GSH / GSSG)",
    ),

    # ---------------- Salts ----------------
    LabReagent(
        id="nacl",
        name="Sodium chloride",
        category="salt",
        typical_concentration="150 mM (physiological); "
                              "300–500 mM (high-salt wash); "
                              "5 M (stock)",
        storage="Room temperature",
        hazards="None",
        preparation_notes="5 M stock filter-sterilises "
                          "easily",
        cas_number="7647-14-5",
        typical_usage="Universal ionic-strength reagent; "
                      "all buffers; salt-gradient elution",
    ),
    LabReagent(
        id="kcl",
        name="Potassium chloride",
        category="salt",
        typical_concentration="100–150 mM (physiological "
                              "intracellular)",
        storage="Room temperature",
        hazards="None",
        preparation_notes="Substitute for NaCl when K-form "
                          "is preferred (e.g. cytoplasmic "
                          "buffers)",
        cas_number="7447-40-7",
        typical_usage="Cytoplasmic-mimic buffers; "
                      "ribosome assays; MS-friendly "
                      "alternative to Na",
    ),
    LabReagent(
        id="mgcl2",
        name="Magnesium chloride (MgCl₂·6H₂O)",
        category="salt",
        typical_concentration="1–10 mM (most enzymes); "
                              "50 mM (PCR optimisation)",
        storage="Room temperature, dry (hygroscopic)",
        hazards="Mild irritant",
        preparation_notes="1 M stock filter-sterilise",
        cas_number="7791-18-6",
        typical_usage="Cofactor for polymerases / kinases; "
                      "PCR Mg²⁺ titration (typical 1.5 mM)",
    ),
    LabReagent(
        id="cacl2",
        name="Calcium chloride (CaCl₂·2H₂O)",
        category="salt",
        typical_concentration="100 mM (E. coli "
                              "transformation); 1–5 mM "
                              "(cell-culture supplement)",
        storage="Room temperature, dry (hygroscopic)",
        hazards="Mild irritant; exothermic dissolution",
        preparation_notes="Always add to water with "
                          "stirring",
        cas_number="10035-04-8",
        typical_usage="Chemical transformation of E. coli "
                      "competent cells; clotting + many "
                      "cellular signalling assays",
    ),
    LabReagent(
        id="mgso4",
        name="Magnesium sulfate (MgSO₄·7H₂O)",
        category="salt",
        typical_concentration="1–10 mM",
        storage="Room temperature",
        hazards="None",
        preparation_notes="Substitute when SO₄²⁻ is "
                          "preferred over Cl⁻ (e.g. "
                          "Drosophila Schneider's medium)",
        cas_number="10034-99-8",
        typical_usage="Bacterial / insect-cell media; LB "
                      "agar plate supplement",
    ),
    LabReagent(
        id="ammonium-sulfate",
        name="Ammonium sulfate (AmSO₄)",
        category="salt",
        typical_concentration="0–80 % saturation "
                              "(precipitation); 4.1 M ≡ "
                              "100 % at 25 °C",
        storage="Room temperature, dry",
        hazards="Mild irritant",
        preparation_notes="Add solid slowly with stirring "
                          "to keep in solution; pre-saturated "
                          "stock simpler",
        cas_number="7783-20-2",
        typical_usage="Salt-cut protein precipitation "
                      "(0–30 %, 30–60 %, 60–80 % standard "
                      "fractions); HIC mobile phase",
    ),
    LabReagent(
        id="edta",
        name="EDTA (Na₂EDTA·2H₂O)",
        category="salt",
        typical_concentration="0.5 mM – 5 mM (chelation); "
                              "0.5 M (stock pH 8.0)",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Solid won't fully dissolve "
                          "until pH > 7 — add NaOH while "
                          "stirring to reach pH 8.0",
        cas_number="6381-92-6",
        typical_usage="Chelate divalent metals (Mg²⁺ / "
                      "Ca²⁺) to inhibit nucleases / "
                      "metalloproteases",
    ),
    LabReagent(
        id="egta",
        name="EGTA",
        category="salt",
        typical_concentration="0.5–5 mM",
        storage="Room temperature",
        hazards="Mild irritant",
        preparation_notes="Same dissolution issue as EDTA; "
                          "adjust pH 8.0 with NaOH",
        cas_number="67-42-5",
        typical_usage="Selective Ca²⁺ chelator (much weaker "
                      "for Mg²⁺ than EDTA); mitotic "
                      "spindle / Ca-signalling assays",
    ),

    # ---------------- Protein-prep ----------------
    LabReagent(
        id="bsa",
        name="BSA (bovine serum albumin)",
        category="protein-prep",
        typical_concentration="0.1–5 % (blocking); "
                              "1 mg/mL (Bradford std)",
        storage="4 °C powder; dissolved 4 °C short-term, "
                "−20 °C aliquots long-term",
        hazards="None; lot-to-lot variability",
        preparation_notes="Use IgG-free, fatty-acid-free, "
                          "or fraction V grades "
                          "depending on assay",
        cas_number="9048-46-8",
        typical_usage="Blocking buffer for Western / ELISA / "
                      "IHC; protein-quantitation standard; "
                      "carrier protein",
    ),
    LabReagent(
        id="protease-inhibitor-cocktail",
        name="Protease inhibitor cocktail (PIC)",
        category="protein-prep",
        typical_concentration="1× (per manufacturer)",
        storage="−20 °C; one freeze-thaw OK",
        hazards="PMSF + leupeptin + pepstatin + "
                "aprotinin + AEBSF — toxic mixture",
        preparation_notes="Add fresh to lysis buffer "
                          "immediately before use",
        cas_number="(mixture)",
        typical_usage="Inhibit serine / cysteine / aspartic "
                      "proteases during lysis to preserve "
                      "protein integrity",
    ),
    LabReagent(
        id="phosphatase-inhibitor-cocktail",
        name="Phosphatase inhibitor cocktail",
        category="protein-prep",
        typical_concentration="1× (per manufacturer); "
                              "10 mM NaF / 1 mM Na₃VO₄ / "
                              "10 mM β-glycerophosphate (homemade)",
        storage="−20 °C aliquots",
        hazards="Vanadate is acutely toxic; NaF moderately",
        preparation_notes="Vanadate must be activated "
                          "(boil + adjust pH 10 → cool) for "
                          "max potency",
        cas_number="(mixture)",
        typical_usage="Preserve protein phosphorylation "
                      "during lysis; essential for "
                      "phospho-Western blots",
    ),

    # ---------------- Stains and dyes ----------------
    LabReagent(
        id="coomassie-r250",
        name="Coomassie Brilliant Blue R-250",
        category="stain",
        typical_concentration="0.1 % w/v in 40 % methanol "
                              "/ 10 % acetic acid",
        storage="Room temperature solution; dark",
        hazards="Methanol-acetic acid mix is flammable + "
                "toxic — fume hood",
        preparation_notes="Filter before use; destain in "
                          "same solvent without dye",
        cas_number="6104-59-2",
        typical_usage="SDS-PAGE staining (sensitivity "
                      "~50 ng/band); slow but classic",
    ),
    LabReagent(
        id="coomassie-g250",
        name="Coomassie G-250 (Bradford reagent)",
        category="stain",
        typical_concentration="Per Bradford-assay "
                              "manufacturer formulation",
        storage="Room temperature, dark",
        hazards="Phosphoric acid present — irritant",
        preparation_notes="Often purchased pre-made "
                          "(Bio-Rad / Pierce)",
        cas_number="6104-58-1",
        typical_usage="Bradford protein assay (A595); "
                      "also colloidal Coomassie (more "
                      "sensitive than R-250)",
    ),
    LabReagent(
        id="ethidium-bromide",
        name="Ethidium bromide",
        category="stain",
        typical_concentration="0.5 µg/mL in agarose gels",
        storage="Room temperature, dark; restricted "
                "waste stream",
        hazards="Mutagen / suspected carcinogen; gloves "
                "+ dedicated waste",
        preparation_notes="Pre-stain (in gel) or "
                          "post-stain options",
        cas_number="1239-45-8",
        typical_usage="Classic DNA stain for agarose gels; "
                      "increasingly replaced by SYBR Safe "
                      "for safety",
    ),
    LabReagent(
        id="sybr-safe",
        name="SYBR Safe DNA gel stain",
        category="stain",
        typical_concentration="1× (per Invitrogen "
                              "formulation)",
        storage="4 °C, dark",
        hazards="Far less toxic than EtBr; handle with "
                "gloves",
        preparation_notes="Add directly to molten agarose "
                          "before pouring gel",
        cas_number="(proprietary)",
        typical_usage="Replacement for ethidium bromide; "
                      "blue-light visualisation safer for "
                      "cloning workflows",
    ),
    LabReagent(
        id="silver-nitrate",
        name="Silver nitrate (AgNO₃)",
        category="stain",
        typical_concentration="0.1–0.2 % w/v",
        storage="Dark, dry; light-sensitive",
        hazards="Severe skin / eye burns; staining; "
                "oxidiser",
        preparation_notes="Many published silver-stain "
                          "protocols (e.g. Shevchenko et al.)",
        cas_number="7761-88-8",
        typical_usage="Silver-staining SDS-PAGE gels "
                      "(~1 ng/band); MS-compatible "
                      "variants exist",
    ),
    LabReagent(
        id="methylene-blue",
        name="Methylene blue",
        category="stain",
        typical_concentration="0.1 % aqueous (cell stain); "
                              "0.5 % saline",
        storage="Room temperature",
        hazards="Mild irritant; intense persistent staining",
        preparation_notes="Filter for histology",
        cas_number="61-73-4",
        typical_usage="Cell nuclei stain; bacteriology; "
                      "redox indicator",
    ),
    LabReagent(
        id="crystal-violet",
        name="Crystal violet",
        category="stain",
        typical_concentration="0.1 % w/v in methanol or "
                              "20 % EtOH (cell viability)",
        storage="Room temperature",
        hazards="Mild irritant; persistent staining",
        preparation_notes="Wash with water repeatedly to "
                          "remove background",
        cas_number="548-62-9",
        typical_usage="Gram stain (Gram-positive); "
                      "adherent-cell colony / viability "
                      "quantitation by A590",
    ),

    # ---------------- Solvents ----------------
    LabReagent(
        id="dmso",
        name="DMSO (dimethyl sulfoxide)",
        category="solvent",
        typical_concentration="< 0.1 % (cell-culture "
                              "vehicle); 100 % stock",
        storage="Room temperature; freezes at 18.5 °C "
                "(rewarm)",
        hazards="Skin permeator — gloves change "
                "frequently; carries chemicals across skin",
        preparation_notes="Anhydrous + cell-culture grade "
                          "for compound stocks",
        cas_number="67-68-5",
        typical_usage="Universal small-molecule vehicle "
                      "(10 mM compound stocks); cell "
                      "freezing media (10 % v/v)",
    ),
    LabReagent(
        id="dmf",
        name="DMF (N,N-dimethylformamide)",
        category="solvent",
        typical_concentration="100 % (peptide synthesis)",
        storage="Room temperature, dry, vented",
        hazards="Reproductive toxin; readily absorbed "
                "through skin",
        preparation_notes="Anhydrous for SPPS; protect "
                          "from moisture",
        cas_number="68-12-2",
        typical_usage="Solid-phase peptide synthesis "
                      "(SPPS) coupling solvent; resin "
                      "swelling",
    ),
    LabReagent(
        id="ethanol",
        name="Ethanol (absolute, 100 %)",
        category="solvent",
        typical_concentration="70 % (DNA wash, surface "
                              "disinfection); 100 %",
        storage="Room temperature, away from ignition",
        hazards="Highly flammable",
        preparation_notes="200-proof for molecular "
                          "biology (no methanol "
                          "denaturant)",
        cas_number="64-17-5",
        typical_usage="DNA / RNA precipitation wash; "
                      "70 % spray for hood / surface "
                      "disinfection",
    ),
    LabReagent(
        id="methanol",
        name="Methanol",
        category="solvent",
        typical_concentration="100 % (HPLC / fixation)",
        storage="Room temperature, away from ignition",
        hazards="Toxic if ingested (causes blindness); "
                "flammable",
        preparation_notes="HPLC grade for chromatography",
        cas_number="67-56-1",
        typical_usage="HPLC mobile phase; cell fixation "
                      "(−20 °C); Bligh-Dyer lipid "
                      "extraction",
    ),
    LabReagent(
        id="acetone",
        name="Acetone",
        category="solvent",
        typical_concentration="100 %; 80 % aqueous "
                              "(protein precipitation)",
        storage="Room temperature, away from ignition",
        hazards="Highly flammable; defats skin",
        preparation_notes="HPLC grade for spectroscopy",
        cas_number="67-64-1",
        typical_usage="Protein precipitation (cold "
                      "acetone); cleaning + "
                      "degreasing glassware",
    ),
    LabReagent(
        id="chloroform",
        name="Chloroform",
        category="solvent",
        typical_concentration="100 %; 25:24:1 "
                              "phenol:chloroform:IAA",
        storage="Room temperature, dark, vented",
        hazards="Suspected carcinogen; "
                "narcotic vapour — fume hood",
        preparation_notes="Stabilised with ~0.75 % "
                          "ethanol for storage",
        cas_number="67-66-3",
        typical_usage="DNA / RNA extraction; lipid "
                      "extraction (Bligh-Dyer, "
                      "Folch)",
    ),
    LabReagent(
        id="hexane",
        name="Hexane",
        category="solvent",
        typical_concentration="100 %",
        storage="Room temperature, away from ignition",
        hazards="Highly flammable; neurotoxic — fume "
                "hood",
        preparation_notes="HPLC grade for normal-phase "
                          "chromatography",
        cas_number="110-54-3",
        typical_usage="Normal-phase chromatography; "
                      "non-polar lipid extraction",
    ),
    LabReagent(
        id="thf",
        name="THF (tetrahydrofuran)",
        category="solvent",
        typical_concentration="100 %",
        storage="Room temperature, dry, dark; peroxide "
                "test before use",
        hazards="Highly flammable; forms explosive "
                "peroxides on storage",
        preparation_notes="Inhibitor-free (BHT) for "
                          "GPC / SEC; dry over molecular "
                          "sieves",
        cas_number="109-99-9",
        typical_usage="GPC / SEC mobile phase; organic "
                      "synthesis solvent (Grignard, etc.)",
    ),
    LabReagent(
        id="dcm",
        name="Dichloromethane (DCM)",
        category="solvent",
        typical_concentration="100 %",
        storage="Room temperature, dark, vented",
        hazards="Suspected carcinogen — fume hood; "
                "EU REACH-restricted in many uses",
        preparation_notes="Use stabilised grade for "
                          "synthesis",
        cas_number="75-09-2",
        typical_usage="Organic-extraction workup; "
                      "TLC mobile phase; SPPS "
                      "Fmoc deprotection (with TFA)",
    ),
    LabReagent(
        id="acetonitrile",
        name="Acetonitrile (MeCN)",
        category="solvent",
        typical_concentration="100 %; common HPLC "
                              "mobile-phase modifier",
        storage="Room temperature, dry",
        hazards="Toxic; flammable",
        preparation_notes="HPLC / LC-MS grade for "
                          "chromatography",
        cas_number="75-05-8",
        typical_usage="Reverse-phase HPLC + LC-MS "
                      "mobile phase (with 0.1 % FA / "
                      "TFA modifier)",
    ),

    # ---------------- Cell-culture media ----------------
    LabReagent(
        id="dmem",
        name="DMEM (Dulbecco's Modified Eagle Medium)",
        category="cell-culture",
        typical_concentration="1× (per formulation)",
        storage="4 °C, dark; 1 month after "
                "supplementation",
        hazards="None at working strength",
        preparation_notes="Add 10 % FBS + 1 % "
                          "Pen-Strep + 1 % L-glutamine "
                          "(or GlutaMAX) for general use",
        cas_number="(formulation)",
        typical_usage="Workhorse mammalian-cell medium "
                      "(HEK293, HeLa, MEFs); "
                      "high-glucose 4.5 g/L variant most "
                      "common",
    ),
    LabReagent(
        id="rpmi-1640",
        name="RPMI-1640",
        category="cell-culture",
        typical_concentration="1× (per formulation)",
        storage="4 °C, dark",
        hazards="None at working strength",
        preparation_notes="Add 10 % FBS + Pen-Strep + "
                          "L-glutamine; HEPES-buffered "
                          "variants sold separately",
        cas_number="(formulation)",
        typical_usage="Suspension cell culture (Jurkat, "
                      "K562); lymphocyte work; many "
                      "hybridoma protocols",
    ),
    LabReagent(
        id="mem",
        name="MEM (Eagle's Minimum Essential Medium)",
        category="cell-culture",
        typical_concentration="1× with Earle's salts",
        storage="4 °C",
        hazards="None at working strength",
        preparation_notes="Add 10 % FBS, NEAA, glutamine",
        cas_number="(formulation)",
        typical_usage="Adherent cell lines requiring "
                      "minimal medium (Vero, HepG2); less "
                      "common than DMEM",
    ),
    LabReagent(
        id="f12",
        name="Ham's F-12",
        category="cell-culture",
        typical_concentration="1× (per formulation)",
        storage="4 °C",
        hazards="None at working strength",
        preparation_notes="Often used as 1:1 DMEM/F-12 "
                          "for serum-reduced or stem-cell "
                          "work",
        cas_number="(formulation)",
        typical_usage="CHO cells; primary cell culture; "
                      "DMEM/F-12 1:1 widely used base",
    ),
    LabReagent(
        id="opti-mem",
        name="Opti-MEM I",
        category="cell-culture",
        typical_concentration="1× (per formulation)",
        storage="4 °C",
        hazards="None at working strength",
        preparation_notes="Reduced-serum medium (~2.5 %); "
                          "no need for FBS during "
                          "transfection",
        cas_number="(formulation)",
        typical_usage="Lipofectamine transfection "
                      "vehicle; reduces serum-protein "
                      "interference with cationic lipids",
    ),
    LabReagent(
        id="fbs",
        name="FBS (fetal bovine serum)",
        category="cell-culture",
        typical_concentration="10 % v/v in growth media",
        storage="−20 °C aliquots; thawed batch 4 °C "
                "for 1 month",
        hazards="Lot-to-lot variability — qualify each "
                "lot for sensitive assays",
        preparation_notes="Heat-inactivate at 56 °C "
                          "for 30 min if complement "
                          "needs killing",
        cas_number="(biological)",
        typical_usage="Mammalian-cell growth supplement; "
                      "provides growth factors, hormones, "
                      "carrier proteins",
    ),
    LabReagent(
        id="trypsin-edta",
        name="Trypsin-EDTA (0.05 % / 0.5 mM)",
        category="cell-culture",
        typical_concentration="0.05 % trypsin / 0.5 mM "
                              "EDTA in PBS",
        storage="−20 °C aliquots; 4 °C working stock "
                "1 week",
        hazards="Mild irritant",
        preparation_notes="Pre-warm to 37 °C; quench "
                          "with serum-containing medium "
                          "after detachment",
        cas_number="9002-07-7 (trypsin)",
        typical_usage="Detach adherent mammalian cells "
                      "for passaging; EDTA chelates Ca²⁺ "
                      "to weaken cadherins",
    ),
    LabReagent(
        id="pen-strep",
        name="Penicillin-Streptomycin (100×)",
        category="cell-culture",
        typical_concentration="1× = 100 U/mL Pen + "
                              "100 µg/mL Strep",
        storage="−20 °C aliquots",
        hazards="Mild irritant",
        preparation_notes="Add to medium to 1×; avoid "
                          "long-term use (selects for "
                          "resistance)",
        cas_number="(mixture)",
        typical_usage="Antibiotic supplement to suppress "
                      "bacterial contamination in cell "
                      "culture",
    ),
    LabReagent(
        id="l-glutamine",
        name="L-glutamine (200 mM, 100×)",
        category="cell-culture",
        typical_concentration="2 mM final (1× from 100×)",
        storage="−20 °C aliquots; thawed 4 °C 2 weeks",
        hazards="None",
        preparation_notes="Decomposes in solution; replace "
                          "every 2 weeks or use GlutaMAX",
        cas_number="56-85-9",
        typical_usage="Essential amino acid for most "
                      "mammalian cell media; energy + "
                      "nitrogen source",
    ),

    # ---------------- Molecular-biology reagents ----------------
    LabReagent(
        id="dntps",
        name="dNTP mix (10 mM each)",
        category="molecular-biology",
        typical_concentration="200 µM each in PCR "
                              "reaction (final)",
        storage="−20 °C aliquots; freeze-thaw < 5×",
        hazards="None",
        preparation_notes="Equal-molar mix of dATP / "
                          "dGTP / dCTP / dTTP; pH 7–8",
        cas_number="(mixture)",
        typical_usage="PCR substrate; dNTP imbalance "
                      "increases polymerase error rate",
    ),
    LabReagent(
        id="agarose",
        name="Agarose (molecular-biology grade)",
        category="molecular-biology",
        typical_concentration="0.5 % (large fragments) "
                              "to 3 % (small fragments) "
                              "w/v in TAE / TBE",
        storage="Room temperature, dry",
        hazards="None as solid; molten gel ~65 °C burn "
                "hazard",
        preparation_notes="Dissolve in TAE / TBE by "
                          "microwave + swirl; cool to "
                          "60 °C before adding stain + "
                          "pouring",
        cas_number="9012-36-6",
        typical_usage="DNA / RNA gel-electrophoresis matrix",
    ),
    LabReagent(
        id="taq-polymerase",
        name="Taq DNA polymerase",
        category="molecular-biology",
        typical_concentration="5 U/µL (stock); 1.25 U / "
                              "50 µL reaction",
        storage="−20 °C; one-time freeze-thaw OK",
        hazards="None",
        preparation_notes="Buffered with 10× supplied "
                          "buffer + Mg²⁺",
        cas_number="(enzyme)",
        typical_usage="Standard PCR; no proof-reading "
                      "(error rate ~1e-4); add A-overhang "
                      "for TA cloning",
    ),
    LabReagent(
        id="phusion-polymerase",
        name="Phusion DNA polymerase",
        category="molecular-biology",
        typical_concentration="2 U/µL (stock); 1 U / "
                              "50 µL reaction",
        storage="−20 °C",
        hazards="None",
        preparation_notes="HF + GC buffers supplied; "
                          "DMSO 3 % for difficult "
                          "templates",
        cas_number="(enzyme)",
        typical_usage="High-fidelity PCR (~50× lower "
                      "error than Taq); blunt-end product "
                      "for cloning",
    ),
    LabReagent(
        id="ecori",
        name="EcoRI restriction enzyme",
        category="molecular-biology",
        typical_concentration="20 U/µL",
        storage="−20 °C",
        hazards="None",
        preparation_notes="Use supplied 10× CutSmart or "
                          "rCutSmart buffer (NEB)",
        cas_number="(enzyme)",
        typical_usage="Recognition: G^AATTC (5' overhang); "
                      "workhorse cloning enzyme",
    ),
    LabReagent(
        id="bamhi",
        name="BamHI restriction enzyme",
        category="molecular-biology",
        typical_concentration="20 U/µL",
        storage="−20 °C",
        hazards="None",
        preparation_notes="CutSmart buffer compatible",
        cas_number="(enzyme)",
        typical_usage="Recognition: G^GATCC (5' "
                      "overhang); often paired with "
                      "EcoRI for double-cut cloning",
    ),
    LabReagent(
        id="t4-dna-ligase",
        name="T4 DNA ligase",
        category="molecular-biology",
        typical_concentration="400 U/µL (NEB); 1–5 U "
                              "/ reaction",
        storage="−20 °C",
        hazards="None",
        preparation_notes="Supplied 10× buffer contains "
                          "ATP — sensitive to freeze-thaw",
        cas_number="(enzyme)",
        typical_usage="Ligate cohesive- or blunt-end DNA "
                      "fragments; standard cloning step",
    ),
    LabReagent(
        id="rnase-a",
        name="RNase A",
        category="molecular-biology",
        typical_concentration="10 mg/mL (stock); 100 "
                              "µg/mL (working)",
        storage="4 °C; pre-boil to inactivate any "
                "DNase contamination",
        hazards="Mild irritant; aerosols a contamination "
                "risk in RNA labs",
        preparation_notes="Boil 15 min in 10 mM "
                          "Tris-HCl pH 7.5 / 15 mM NaCl "
                          "to destroy contaminating "
                          "DNase",
        cas_number="9001-99-4",
        typical_usage="Plasmid prep clean-up; remove "
                      "RNA contamination from DNA preps",
    ),
    LabReagent(
        id="dnase-i",
        name="DNase I (RNase-free)",
        category="molecular-biology",
        typical_concentration="2 U/µL (NEB); per "
                              "manufacturer for kits",
        storage="−20 °C; sensitive to freeze-thaw",
        hazards="None",
        preparation_notes="Activated by Mg²⁺ + Ca²⁺; "
                          "EDTA stops digestion",
        cas_number="9003-98-9",
        typical_usage="Remove genomic DNA from RNA preps "
                      "(critical before RT-PCR)",
    ),
    LabReagent(
        id="proteinase-k",
        name="Proteinase K",
        category="molecular-biology",
        typical_concentration="10–20 mg/mL (stock); "
                              "50–200 µg/mL (working)",
        storage="−20 °C aliquots",
        hazards="None",
        preparation_notes="Active in SDS / urea — "
                          "useful in harsh nucleic-acid "
                          "extraction",
        cas_number="39450-01-6",
        typical_usage="Digest proteins during DNA / RNA "
                      "extraction; tissue dissociation",
    ),
]


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------
_BY_ID: Dict[str, LabReagent] = {r.id: r for r in _REAGENTS}


def list_reagents(
    category: Optional[str] = None,
) -> List[LabReagent]:
    """Return every reagent, optionally filtered by category.

    Returns empty for unknown categories.  Callers that want
    an explicit error path should pre-validate against
    :data:`VALID_CATEGORIES`.
    """
    if category is None or category == "":
        return list(_REAGENTS)
    if category not in VALID_CATEGORIES:
        return []
    return [r for r in _REAGENTS if r.category == category]


def get_reagent(reagent_id: str) -> Optional[LabReagent]:
    """Return the reagent with this id, or None."""
    return _BY_ID.get(reagent_id)


def find_reagents(needle: str) -> List[LabReagent]:
    """Case-insensitive substring search across id + name +
    category + typical_usage + cas_number."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out = []
    for r in _REAGENTS:
        hay = " ".join([
            r.id, r.name, r.category, r.typical_usage,
            r.cas_number,
        ]).lower()
        if n in hay:
            out.append(r)
    return out


def categories() -> Tuple[str, ...]:
    """Return the canonical category tuple."""
    return VALID_CATEGORIES


def reagent_to_dict(r: LabReagent) -> Dict[str, str]:
    """JSON-serialisable view of a single reagent."""
    return asdict(r)
