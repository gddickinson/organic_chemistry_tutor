"""Phase 42a (round 147) — metabolic-pathways catalogue.

Headless reference data for the *Tools → Metabolic pathways…*
dialog.  Three frozen dataclasses:

- :class:`RegulatoryEffector` — one allosteric / hormonal /
  metabolite regulator of a pathway step.
- :class:`PathwayStep` — one enzymatic reaction within a
  pathway (substrate(s) → enzyme + EC → product(s) +
  reversibility + ΔG (kJ/mol where literature values
  exist) + regulators + notes).
- :class:`Pathway` — a named pathway (id / name / category /
  cellular_compartment / overview / ordered list of
  PathwayStep records / overall ΔG / textbook reference).

Categories
----------
- ``"central-carbon"`` — glycolysis, gluconeogenesis,
  pentose-phosphate, TCA cycle, ox-phos / electron transport.
- ``"lipid"`` — β-oxidation, fatty-acid biosynthesis,
  cholesterol biosynthesis (high-level).
- ``"amino-acid"`` — urea cycle.
- ``"nucleotide"`` — purine + pyrimidine de novo (high-level).
- ``"specialised"`` — heme biosynthesis, photosynthesis
  Calvin cycle, glycogen synthesis + breakdown.

Reference data only.  ΔG values from Nelson & Cox *Lehninger
Principles of Biochemistry* (8th ed., 2021); EC numbers from
the IUBMB / BRENDA databases.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass(frozen=True)
class RegulatoryEffector:
    name: str                  # "ATP", "Citrate", "Insulin"
    mode: str                  # "activator" / "inhibitor"
    mechanism: str = ""        # free-text mechanism note


@dataclass(frozen=True)
class PathwayStep:
    step_number: int
    substrates: Tuple[str, ...]
    enzyme_name: str
    ec_number: str             # e.g. "2.7.1.1" for hexokinase
    products: Tuple[str, ...]
    reversibility: str         # "reversible" / "irreversible"
    delta_g_kjmol: Optional[float] = None
    regulatory_effectors: Tuple[RegulatoryEffector, ...] = ()
    notes: str = ""


@dataclass(frozen=True)
class Pathway:
    id: str
    name: str
    category: str              # see module docstring
    cellular_compartment: str
    overview: str
    overall_delta_g_kjmol: Optional[float] = None
    textbook_reference: str = ""
    steps: Tuple[PathwayStep, ...] = ()


VALID_CATEGORIES: tuple = (
    "central-carbon", "lipid", "amino-acid",
    "nucleotide", "specialised",
)
# Note: ``"nucleotide"`` is reserved for purine + pyrimidine
# de-novo pathways (Phase 42a follow-up); the current 11
# seeded pathways cover the other 4 categories.


# ------------------------------------------------------------------
# Catalogue
# ------------------------------------------------------------------

def _build_catalogue() -> List[Pathway]:
    out: List[Pathway] = []

    # ---- Glycolysis -------------------------------------------------
    out.append(Pathway(
        id="glycolysis",
        name="Glycolysis (Embden-Meyerhof-Parnas pathway)",
        category="central-carbon",
        cellular_compartment="Cytoplasm (all cells)",
        overview=(
            "10-step conversion of glucose (6C) into two "
            "pyruvate (3C), generating net 2 ATP + 2 NADH per "
            "glucose.  Catabolic, exergonic, conserves part of "
            "the glucose oxidation energy as ATP + NADH.  "
            "Steps 1-5 are the energy-investment phase (2 ATP "
            "consumed); steps 6-10 are the energy-payoff phase "
            "(4 ATP + 2 NADH produced)."
        ),
        overall_delta_g_kjmol=-85.0,
        textbook_reference="Nelson & Cox 8e, Ch. 14",
        steps=(
            PathwayStep(
                1, ("Glucose", "ATP"), "Hexokinase / Glucokinase",
                "2.7.1.1", ("Glucose-6-phosphate", "ADP"),
                "irreversible", -16.7,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Glucose-6-phosphate", "inhibitor",
                        "Product inhibition of hexokinase "
                        "(NOT glucokinase)"),
                    RegulatoryEffector(
                        "Insulin", "activator",
                        "Induces glucokinase transcription "
                        "in liver"),
                ),
                notes=(
                    "Glucokinase (liver / β-cells) has higher "
                    "K_m + no product inhibition vs hexokinase "
                    "(other tissues) — the two-isozyme system "
                    "underlies hepatic-glucose buffering."
                ),
            ),
            PathwayStep(
                2, ("Glucose-6-phosphate",),
                "Phosphoglucose isomerase",
                "5.3.1.9", ("Fructose-6-phosphate",),
                "reversible", +1.7,
            ),
            PathwayStep(
                3, ("Fructose-6-phosphate", "ATP"),
                "Phosphofructokinase-1 (PFK-1)",
                "2.7.1.11", ("Fructose-1,6-bisphosphate", "ADP"),
                "irreversible", -14.2,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "ATP", "inhibitor",
                        "Allosteric — high cellular ATP "
                        "shuts down further glycolysis"),
                    RegulatoryEffector(
                        "Citrate", "inhibitor",
                        "Cross-talk: TCA-cycle saturation "
                        "feeds back to slow glycolysis"),
                    RegulatoryEffector(
                        "AMP", "activator",
                        "Allosteric — low energy charge "
                        "speeds up glycolysis"),
                    RegulatoryEffector(
                        "Fructose-2,6-bisphosphate",
                        "activator",
                        "Most-potent allosteric activator; "
                        "controls hepatic glycolysis vs "
                        "gluconeogenesis"),
                ),
                notes=(
                    "Rate-limiting step; the regulatory "
                    "control point of glycolysis."
                ),
            ),
            PathwayStep(
                4, ("Fructose-1,6-bisphosphate",),
                "Aldolase A / B / C",
                "4.1.2.13",
                ("Glyceraldehyde-3-phosphate (G3P)",
                 "Dihydroxyacetone phosphate (DHAP)"),
                "reversible", +23.8,
                notes=(
                    "Class-I aldolase (animal isoforms) uses a "
                    "Schiff-base mechanism — see the Phase-31c "
                    "aldolase mechanism JSON for the full "
                    "arrow-pushing."
                ),
            ),
            PathwayStep(
                5, ("Dihydroxyacetone phosphate",),
                "Triose phosphate isomerase",
                "5.3.1.1", ("Glyceraldehyde-3-phosphate",),
                "reversible", +7.5,
                notes=(
                    "Catalytically perfect enzyme (k_cat / K_m "
                    "near the diffusion limit ~10⁹ M⁻¹s⁻¹).  "
                    "Now both 3C halves are G3P → enter the "
                    "payoff phase."
                ),
            ),
            PathwayStep(
                6, ("Glyceraldehyde-3-phosphate", "NAD+",
                    "Pi"),
                "Glyceraldehyde-3-phosphate dehydrogenase "
                "(GAPDH)",
                "1.2.1.12",
                ("1,3-Bisphosphoglycerate", "NADH"),
                "reversible", +6.3,
                notes=(
                    "Energy of oxidation captured as a high-"
                    "energy acyl-phosphate (the only payoff-"
                    "phase substrate-level phosphorylation "
                    "precursor) + 1 NADH per G3P."
                ),
            ),
            PathwayStep(
                7, ("1,3-Bisphosphoglycerate", "ADP"),
                "Phosphoglycerate kinase",
                "2.7.2.3", ("3-Phosphoglycerate", "ATP"),
                "reversible", -18.5,
                notes=(
                    "First substrate-level phosphorylation — "
                    "yields the first ATP of glycolysis."
                ),
            ),
            PathwayStep(
                8, ("3-Phosphoglycerate",),
                "Phosphoglycerate mutase",
                "5.4.2.11", ("2-Phosphoglycerate",),
                "reversible", +4.4,
            ),
            PathwayStep(
                9, ("2-Phosphoglycerate",),
                "Enolase",
                "4.2.1.11", ("Phosphoenolpyruvate (PEP)",
                              "H₂O"),
                "reversible", +7.5,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Fluoride", "inhibitor",
                        "F⁻ + Mg²⁺ + Pi forms a transition-"
                        "state-analogue Mg-fluorophosphate "
                        "complex — basis for blood-collection-"
                        "tube glycolysis inhibition"),
                ),
            ),
            PathwayStep(
                10, ("Phosphoenolpyruvate", "ADP"),
                "Pyruvate kinase",
                "2.7.1.40", ("Pyruvate", "ATP"),
                "irreversible", -31.4,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Fructose-1,6-bisphosphate",
                        "activator",
                        "Feed-forward activation from PFK-1 "
                        "product"),
                    RegulatoryEffector(
                        "ATP", "inhibitor",
                        "Allosteric — high energy charge "
                        "shuts down pyruvate output"),
                    RegulatoryEffector(
                        "Alanine", "inhibitor",
                        "Cross-talk from amino-acid "
                        "catabolism"),
                ),
                notes=(
                    "Second substrate-level phosphorylation; "
                    "yields the second ATP per G3P (4 total "
                    "in the payoff phase, 2 net per glucose).  "
                    "Pyruvate then feeds into PDH → TCA, "
                    "lactate fermentation, or ethanol "
                    "fermentation depending on the cell type "
                    "+ O₂ status."
                ),
            ),
        ),
    ))

    # ---- TCA cycle (Krebs cycle) ----------------------------------
    out.append(Pathway(
        id="tca_cycle",
        name="TCA cycle (Krebs / citric-acid cycle)",
        category="central-carbon",
        cellular_compartment=(
            "Mitochondrial matrix (eukaryotes); cytoplasm "
            "(prokaryotes)"
        ),
        overview=(
            "8-step cyclic oxidation of acetyl-CoA (2C) to 2 "
            "CO₂, generating 3 NADH + 1 FADH₂ + 1 GTP per "
            "turn.  Central metabolic hub: feeds the "
            "electron-transport chain (NADH / FADH₂ → ~9-10 "
            "ATP via ox-phos), supplies biosynthetic "
            "intermediates (oxaloacetate / α-KG / succinyl-CoA "
            "→ amino acids, heme, glucose).  Discovered by "
            "Krebs in 1937 (Nobel 1953)."
        ),
        overall_delta_g_kjmol=-29.7,
        textbook_reference="Nelson & Cox 8e, Ch. 16",
        steps=(
            PathwayStep(
                1, ("Acetyl-CoA", "Oxaloacetate", "H₂O"),
                "Citrate synthase",
                "2.3.3.1", ("Citrate", "CoA-SH"),
                "irreversible", -32.2,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "ATP", "inhibitor",
                        "Allosteric — high energy charge "
                        "slows TCA"),
                    RegulatoryEffector(
                        "Citrate", "inhibitor",
                        "Product inhibition; also feeds "
                        "back to PFK-1 in glycolysis"),
                    RegulatoryEffector(
                        "Succinyl-CoA", "inhibitor",
                        "Downstream-product feedback"),
                ),
            ),
            PathwayStep(
                2, ("Citrate",), "Aconitase",
                "4.2.1.3", ("Isocitrate",),
                "reversible", +13.3,
                notes=(
                    "Reaction proceeds via a cis-aconitate "
                    "intermediate; uses an Fe-S cluster (no "
                    "obvious redox role — rare structural "
                    "Fe-S use)."
                ),
            ),
            PathwayStep(
                3, ("Isocitrate", "NAD+"),
                "Isocitrate dehydrogenase (IDH3)",
                "1.1.1.41",
                ("α-Ketoglutarate", "NADH", "CO₂"),
                "irreversible", -8.4,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "ADP / Ca²⁺", "activator",
                        "High-demand allosteric activation"),
                    RegulatoryEffector(
                        "ATP / NADH", "inhibitor",
                        "Energy-charge feedback"),
                ),
                notes=(
                    "Rate-limiting step of the TCA cycle.  "
                    "First CO₂ released."
                ),
            ),
            PathwayStep(
                4, ("α-Ketoglutarate", "NAD+", "CoA-SH"),
                "α-Ketoglutarate dehydrogenase complex",
                "1.2.4.2",
                ("Succinyl-CoA", "NADH", "CO₂"),
                "irreversible", -33.5,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Ca²⁺", "activator",
                        "Cardiac + muscle TCA flux during "
                        "high contraction demand"),
                    RegulatoryEffector(
                        "Succinyl-CoA / NADH", "inhibitor",
                        "Product feedback"),
                ),
                notes=(
                    "Multi-enzyme complex analogous to "
                    "pyruvate dehydrogenase; uses TPP + "
                    "lipoamide + FAD + NAD as cofactors.  "
                    "Second CO₂."
                ),
            ),
            PathwayStep(
                5, ("Succinyl-CoA", "GDP", "Pi"),
                "Succinyl-CoA synthetase / "
                "Succinate-CoA ligase",
                "6.2.1.4 (GTP-forming)",
                ("Succinate", "GTP", "CoA-SH"),
                "reversible", -2.9,
                notes=(
                    "Substrate-level phosphorylation (the "
                    "only one in TCA) — GTP can be "
                    "interconverted to ATP by nucleoside "
                    "diphosphate kinase."
                ),
            ),
            PathwayStep(
                6, ("Succinate", "FAD"),
                "Succinate dehydrogenase (Complex II)",
                "1.3.5.1", ("Fumarate", "FADH₂"),
                "reversible", 0.0,
                notes=(
                    "Embedded in the inner mitochondrial "
                    "membrane — TCA's only membrane-bound "
                    "enzyme + the only enzyme shared between "
                    "TCA + ETC."
                ),
            ),
            PathwayStep(
                7, ("Fumarate", "H₂O"), "Fumarase",
                "4.2.1.2", ("Malate",),
                "reversible", -3.8,
            ),
            PathwayStep(
                8, ("Malate", "NAD+"),
                "Malate dehydrogenase",
                "1.1.1.37", ("Oxaloacetate", "NADH"),
                "reversible", +29.7,
                notes=(
                    "Highly endergonic in vitro but "
                    "drained forward by the consumption of "
                    "OAA in step 1 (Le Chatelier)."
                ),
            ),
        ),
    ))

    # ---- Oxidative phosphorylation (high-level) -------------------
    out.append(Pathway(
        id="ox_phos",
        name="Oxidative phosphorylation (electron transport + ATP synthase)",
        category="central-carbon",
        cellular_compartment=(
            "Inner mitochondrial membrane (eukaryotes); "
            "plasma membrane (prokaryotes)"
        ),
        overview=(
            "Five complexes (I-V) embedded in the inner "
            "mitochondrial membrane.  NADH + FADH₂ from "
            "glycolysis / TCA donate electrons that "
            "Complexes I-IV pump down a redox cascade, "
            "extruding H⁺ across the inner membrane to "
            "build a proton-motive force (Δp ~ 220 mV).  "
            "Complex V (ATP synthase) lets H⁺ flow back, "
            "rotating the c-ring and synthesising ATP from "
            "ADP + Pi (chemiosmotic coupling, Mitchell 1961, "
            "Nobel 1978).  Stoichiometry: ~2.5 ATP / NADH, "
            "~1.5 ATP / FADH₂."
        ),
        overall_delta_g_kjmol=-220.0,   # per NADH
        textbook_reference="Nelson & Cox 8e, Ch. 19",
        steps=(
            PathwayStep(
                1, ("NADH", "Q (ubiquinone)"),
                "Complex I (NADH:ubiquinone oxidoreductase)",
                "7.1.1.2",
                ("NAD+", "QH₂", "4 H⁺_out"),
                "irreversible", -69.5,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Rotenone", "inhibitor",
                        "Classic Complex I inhibitor — used "
                        "as an insecticide / fish poison + a "
                        "research tool (Parkinson's disease "
                        "model)"),
                ),
                notes=(
                    "L-shaped membrane embedded complex with "
                    "FMN cofactor + 8 Fe-S clusters.  Pumps "
                    "4 H⁺ per NADH oxidised."
                ),
            ),
            PathwayStep(
                2, ("FADH₂", "Q"),
                "Complex II (succinate dehydrogenase / "
                "succinate:ubiquinone oxidoreductase)",
                "1.3.5.1", ("FAD", "QH₂"),
                "irreversible", 0.0,
                notes=(
                    "Same enzyme as TCA cycle step 6.  "
                    "Doesn't pump protons — that's why "
                    "FADH₂ yields fewer ATP than NADH."
                ),
            ),
            PathwayStep(
                3, ("QH₂", "Cytochrome c (Fe³⁺)"),
                "Complex III (cytochrome bc₁ / "
                "ubiquinol:cytochrome c oxidoreductase)",
                "7.1.1.8",
                ("Q", "Cytochrome c (Fe²⁺)", "4 H⁺_out"),
                "irreversible", -36.7,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Antimycin A", "inhibitor",
                        "Blocks the Q_i site of Complex III"),
                ),
                notes=(
                    "Q-cycle mechanism: the bifurcated "
                    "electron pathway pumps an extra 2 H⁺ "
                    "per QH₂ on top of the 2 transferred to "
                    "cyt c."
                ),
            ),
            PathwayStep(
                4, ("Cytochrome c (Fe²⁺)", "O₂"),
                "Complex IV (cytochrome c oxidase)",
                "7.1.1.9",
                ("Cytochrome c (Fe³⁺)", "H₂O", "2 H⁺_out"),
                "irreversible", -110.0,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Cyanide", "inhibitor",
                        "CN⁻ binds the Fe³⁺ in cyt a₃ — the "
                        "biochemical basis of cyanide "
                        "poisoning"),
                    RegulatoryEffector(
                        "Carbon monoxide", "inhibitor",
                        "CO binds the same site — basis of "
                        "CO toxicity"),
                ),
                notes=(
                    "Reduces O₂ to 2 H₂O — the terminal "
                    "electron acceptor that makes aerobic "
                    "respiration possible.  4 H⁺ consumed "
                    "from matrix (chemical equation), 2 H⁺ "
                    "pumped (vectorial)."
                ),
            ),
            PathwayStep(
                5, ("ADP", "Pi", "n H⁺_in"),
                "Complex V (F₀F₁ ATP synthase)",
                "7.1.2.2", ("ATP", "H₂O"),
                "reversible", -30.5,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Oligomycin", "inhibitor",
                        "Blocks the F₀ proton channel"),
                    RegulatoryEffector(
                        "DCCD", "inhibitor",
                        "Covalently modifies the c-ring "
                        "carboxylate"),
                ),
                notes=(
                    "Rotary motor: 8-15 H⁺ per turn drive "
                    "synthesis of 3 ATP per rotation "
                    "(Boyer's binding-change mechanism, "
                    "Nobel 1997).  Mammalian c-ring has 8 "
                    "subunits → ~2.7 H⁺ per ATP."
                ),
            ),
        ),
    ))

    # ---- β-oxidation (Lynen helix) --------------------------------
    out.append(Pathway(
        id="beta_oxidation",
        name="β-oxidation of fatty acids (Lynen helix)",
        category="lipid",
        cellular_compartment="Mitochondrial matrix",
        overview=(
            "4-step repeating cycle that shortens a "
            "fatty-acyl-CoA by 2 carbons per turn, "
            "releasing acetyl-CoA + 1 NADH + 1 FADH₂ per "
            "cycle.  Palmitoyl-CoA (C16) → 8 acetyl-CoA + "
            "7 NADH + 7 FADH₂ across 7 spirals = ~106 ATP "
            "after ox-phos.  Discovered by Lynen 1964 "
            "(Nobel)."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 17",
        steps=(
            PathwayStep(
                1, ("Acyl-CoA", "FAD"),
                "Acyl-CoA dehydrogenase",
                "1.3.8.7",
                ("trans-Δ²-Enoyl-CoA", "FADH₂"),
                "reversible", -5.0,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Malonyl-CoA", "inhibitor",
                        "Indirect — blocks CPT1 carnitine "
                        "shuttle, preventing entry of fatty "
                        "acid into the matrix when "
                        "biosynthesis is active"),
                ),
                notes=(
                    "Different chain-length-specific "
                    "isoforms (VLCAD / LCAD / MCAD / SCAD); "
                    "MCAD deficiency is the most common "
                    "inherited fatty-acid-oxidation disorder."
                ),
            ),
            PathwayStep(
                2, ("trans-Δ²-Enoyl-CoA", "H₂O"),
                "Enoyl-CoA hydratase",
                "4.2.1.17",
                ("L-3-Hydroxyacyl-CoA",),
                "reversible", -16.0,
            ),
            PathwayStep(
                3, ("L-3-Hydroxyacyl-CoA", "NAD+"),
                "L-3-Hydroxyacyl-CoA dehydrogenase",
                "1.1.1.35",
                ("3-Ketoacyl-CoA", "NADH"),
                "reversible", +7.0,
            ),
            PathwayStep(
                4, ("3-Ketoacyl-CoA", "CoA-SH"),
                "Thiolase / β-ketothiolase",
                "2.3.1.16",
                ("Acyl-CoA (n-2 carbons)", "Acetyl-CoA"),
                "irreversible", -28.0,
                notes=(
                    "Releases an acetyl-CoA + an acyl-CoA "
                    "two carbons shorter — feeds back to "
                    "step 1 for the next spiral."
                ),
            ),
        ),
    ))

    # ---- Fatty-acid biosynthesis (FAS) ---------------------------
    out.append(Pathway(
        id="fatty_acid_synthesis",
        name="Fatty-acid biosynthesis (FAS)",
        category="lipid",
        cellular_compartment=(
            "Cytoplasm — fatty-acid synthase complex (FAS)"
        ),
        overview=(
            "Cytoplasmic biosynthesis of palmitate (C16) "
            "from acetyl-CoA via the multifunctional "
            "fatty-acid synthase (FAS) complex.  Each "
            "elongation cycle adds 2 carbons (from "
            "malonyl-CoA) at the expense of 2 NADPH + 1 "
            "ATP (consumed earlier to make malonyl-CoA).  "
            "Starts from acetyl-CoA + malonyl-CoA + 14 "
            "NADPH for full C16 palmitate (7 cycles)."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 21",
        steps=(
            PathwayStep(
                1, ("Acetyl-CoA", "ATP", "HCO₃⁻"),
                "Acetyl-CoA carboxylase (ACC)",
                "6.4.1.2",
                ("Malonyl-CoA", "ADP", "Pi"),
                "irreversible", -10.0,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Citrate", "activator",
                        "High citrate (TCA full) → fat "
                        "storage signal"),
                    RegulatoryEffector(
                        "Palmitoyl-CoA", "inhibitor",
                        "End-product feedback inhibition"),
                    RegulatoryEffector(
                        "AMPK", "inhibitor",
                        "AMPK phosphorylation inactivates "
                        "ACC during low energy charge"),
                    RegulatoryEffector(
                        "Insulin", "activator",
                        "Hormonal — promotes fat storage"),
                ),
                notes=(
                    "Rate-limiting step of FAS.  The biotin-"
                    "carboxylase + biotin-carboxyl-carrier-"
                    "protein + carboxyltransferase domains "
                    "together accomplish the 2-step ATP-"
                    "dependent CO₂ activation + transfer."
                ),
            ),
            PathwayStep(
                2, ("Acetyl-CoA + Malonyl-CoA bound to "
                    "ACP arm of FAS", "NADPH × 2"),
                "Fatty acid synthase (mammalian — single "
                "multifunctional polypeptide; bacterial — "
                "FabH/D/G/Z/I separate enzymes)",
                "2.3.1.85 (FAS-I, mammalian)",
                ("Butyryl-S-ACP (4C)", "CO₂", "NADP+ × 2",
                 "H₂O"),
                "irreversible", -65.0,
                notes=(
                    "Each elongation cycle consists of 4 "
                    "sub-steps: condensation (β-ketoacyl-ACP "
                    "synthase) → reduction (β-ketoacyl-ACP "
                    "reductase, NADPH) → dehydration "
                    "(β-hydroxyacyl-ACP dehydratase) → "
                    "reduction (enoyl-ACP reductase, "
                    "NADPH).  Mirror image of β-oxidation "
                    "but with NADPH (not NAD/FAD) + ACP "
                    "(not CoA) + cytoplasmic (not "
                    "mitochondrial)."
                ),
            ),
            PathwayStep(
                3, ("Butyryl-ACP + 6 × Malonyl-CoA",
                    "12 NADPH"),
                "FAS (additional 6 cycles of the same "
                "4-step elongation)",
                "—", ("Palmitoyl-ACP (C16)", "6 CO₂",
                       "12 NADP+", "6 H₂O"),
                "irreversible", -390.0,
                notes=(
                    "Six more elongation cycles bring chain "
                    "length to C16 (palmitate).  Thioesterase "
                    "domain releases free palmitate by "
                    "hydrolysing the ACP thioester."
                ),
            ),
        ),
    ))

    # ---- Cholesterol biosynthesis (high level) -------------------
    out.append(Pathway(
        id="cholesterol_biosynthesis",
        name="Cholesterol biosynthesis (mevalonate pathway → squalene → cholesterol)",
        category="lipid",
        cellular_compartment="Cytoplasm + endoplasmic reticulum",
        overview=(
            "30+ enzyme steps from acetyl-CoA → cholesterol.  "
            "Three stages: (1) HMG-CoA → mevalonate (the "
            "rate-limiting step, statin target); (2) "
            "mevalonate → squalene (a C30 isoprenoid); (3) "
            "squalene cyclisation → lanosterol → cholesterol "
            "(20+ tailoring steps)."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 21",
        steps=(
            PathwayStep(
                1, ("3 Acetyl-CoA",),
                "HMG-CoA synthase + thiolase",
                "2.3.3.10 (HMGCS1, cytosolic)",
                ("HMG-CoA (3-hydroxy-3-methylglutaryl-CoA)",
                 "2 CoA-SH"),
                "irreversible", -7.0,
            ),
            PathwayStep(
                2, ("HMG-CoA", "2 NADPH"),
                "HMG-CoA reductase",
                "1.1.1.34",
                ("Mevalonate", "2 NADP+", "CoA-SH"),
                "irreversible", -25.0,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Cholesterol / oxysterols",
                        "inhibitor",
                        "End-product transcriptional + "
                        "ERAD-mediated degradation feedback"),
                    RegulatoryEffector(
                        "AMPK", "inhibitor",
                        "Phosphorylation inactivates HMGCR"),
                    RegulatoryEffector(
                        "Statins", "inhibitor",
                        "Competitive — the most prescribed "
                        "drug class in history; $20+ B/year "
                        "in 2000s"),
                ),
                notes=(
                    "Rate-limiting step.  Statin binding "
                    "structure is the seeded protein 1HWK "
                    "in the Phase 31l catalogue (HMG-CoA "
                    "reductase + atorvastatin)."
                ),
            ),
            PathwayStep(
                3, ("6 Mevalonate", "ATP", "decarboxylation",
                    "isomerase steps"),
                "Mevalonate kinase + phospho-mevalonate "
                "kinase + mevalonate-5-pyrophosphate "
                "decarboxylase + IPP isomerase + farnesyl "
                "pyrophosphate synthase",
                "(multi-step)",
                ("Farnesyl pyrophosphate (FPP, C15)",),
                "irreversible", None,
                notes=(
                    "Builds the C5 isopentenyl + dimethylallyl "
                    "pyrophosphate (IPP / DMAPP) units, then "
                    "head-to-tail-couples them through "
                    "geranyl-PP (C10) to FPP (C15)."
                ),
            ),
            PathwayStep(
                4, ("2 FPP", "NADPH"),
                "Squalene synthase",
                "2.5.1.21",
                ("Squalene (C30)", "NADP+", "2 PPi"),
                "irreversible", -30.0,
                notes=(
                    "Tail-to-tail coupling of two FPP "
                    "molecules — first dedicated cholesterol-"
                    "branch step.  Squalene synthase "
                    "inhibitors (e.g. lapaquistat) were "
                    "explored as next-gen lipid-lowering "
                    "drugs but didn't reach approval."
                ),
            ),
            PathwayStep(
                5, ("Squalene", "O₂", "NADPH"),
                "Squalene monooxygenase + lanosterol "
                "synthase",
                "1.14.14.17 (epoxidase) + 5.4.99.7 "
                "(cyclase)",
                ("Lanosterol",),
                "irreversible", None,
                notes=(
                    "Cyclisation cascade: 2,3-epoxy-squalene "
                    "→ chair-chair-chair-boat conformation "
                    "→ tetracyclic lanosterol via a "
                    "concerted carbocation-rearrangement "
                    "cascade.  One of the most beautiful "
                    "biosynthetic transformations known."
                ),
            ),
            PathwayStep(
                6, ("Lanosterol", "many enzymatic steps"),
                "~19 enzymatic steps (demethylations, "
                "double-bond rearrangements, side-chain "
                "saturation)",
                "(multi-enzyme)", ("Cholesterol",),
                "irreversible", None,
                notes=(
                    "The post-lanosterol pathway has 19+ "
                    "steps; mutations in any cause "
                    "cholesterol-synthesis disorders "
                    "(Smith-Lemli-Opitz syndrome, "
                    "X-linked chondrodysplasia)."
                ),
            ),
        ),
    ))

    # ---- Urea cycle ---------------------------------------------
    out.append(Pathway(
        id="urea_cycle",
        name="Urea cycle",
        category="amino-acid",
        cellular_compartment=(
            "Mitochondrial matrix (steps 1-2) + cytoplasm "
            "(steps 3-5)"
        ),
        overview=(
            "5-step cycle that detoxifies ammonia (from "
            "amino-acid catabolism) into urea for renal "
            "excretion.  Liver-only in humans.  Each turn "
            "consumes 4 ATP equivalents (3 ATP) and "
            "incorporates one nitrogen from NH₄⁺ + one "
            "from aspartate.  Discovered by Krebs + "
            "Henseleit 1932 — predates the TCA cycle "
            "discovery.  Defects cause hyperammonaemia + "
            "encephalopathy."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 18",
        steps=(
            PathwayStep(
                1, ("NH₄⁺", "HCO₃⁻", "2 ATP"),
                "Carbamoyl phosphate synthetase I (CPS-I)",
                "6.3.4.16",
                ("Carbamoyl phosphate", "2 ADP", "Pi"),
                "irreversible", None,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "N-acetylglutamate", "activator",
                        "Allosteric — couples cycle activity "
                        "to amino-acid breakdown rate"),
                ),
                notes=(
                    "Rate-limiting step.  Mitochondrial; "
                    "specifically CPS-I (mitochondrial, urea-"
                    "cycle) vs CPS-II (cytoplasmic, "
                    "pyrimidine biosynthesis)."
                ),
            ),
            PathwayStep(
                2, ("Carbamoyl phosphate", "Ornithine"),
                "Ornithine transcarbamylase (OTC)",
                "2.1.3.3",
                ("Citrulline", "Pi"),
                "irreversible", None,
                notes=(
                    "Mitochondrial.  Citrulline then "
                    "exported to cytoplasm.  OTC deficiency "
                    "is the most common urea-cycle disorder "
                    "(X-linked)."
                ),
            ),
            PathwayStep(
                3, ("Citrulline", "Aspartate", "ATP"),
                "Argininosuccinate synthetase",
                "6.3.4.5",
                ("Argininosuccinate", "AMP", "PPi"),
                "irreversible", None,
                notes=(
                    "Cytoplasmic.  Second nitrogen enters "
                    "via aspartate (from glutamate "
                    "transamination of OAA)."
                ),
            ),
            PathwayStep(
                4, ("Argininosuccinate",),
                "Argininosuccinate lyase",
                "4.3.2.1",
                ("Arginine", "Fumarate"),
                "reversible", None,
                notes=(
                    "Fumarate connects to TCA cycle; "
                    "regenerated to OAA → aspartate to "
                    "feed the next cycle turn."
                ),
            ),
            PathwayStep(
                5, ("Arginine", "H₂O"), "Arginase",
                "3.5.3.1", ("Urea", "Ornithine"),
                "irreversible", None,
                notes=(
                    "Urea diffuses out → blood → kidney → "
                    "excreted.  Ornithine returns to "
                    "mitochondrion to start the next cycle."
                ),
            ),
        ),
    ))

    # ---- Pentose phosphate pathway -------------------------------
    out.append(Pathway(
        id="pentose_phosphate",
        name="Pentose phosphate pathway (PPP / hexose monophosphate shunt)",
        category="central-carbon",
        cellular_compartment="Cytoplasm",
        overview=(
            "Two-branch pathway parallel to glycolysis: "
            "(1) **oxidative branch** generates NADPH (for "
            "biosynthesis + redox defence) + ribose-5-"
            "phosphate (nucleotide precursor); (2) "
            "**non-oxidative branch** interconverts pentose "
            "and hexose sugars via transketolase + "
            "transaldolase.  Especially active in liver, "
            "adipose, mammary gland, RBCs (NADPH for "
            "glutathione)."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 14",
        steps=(
            PathwayStep(
                1, ("Glucose-6-phosphate", "NADP+"),
                "Glucose-6-phosphate dehydrogenase (G6PD)",
                "1.1.1.49",
                ("6-Phosphogluconolactone", "NADPH"),
                "irreversible", None,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "NADPH/NADP+ ratio",
                        "inhibitor",
                        "G6PD activity inversely "
                        "proportional to NADPH/NADP+; "
                        "self-balancing"),
                ),
                notes=(
                    "Rate-limiting step.  G6PD deficiency "
                    "is the most common human enzyme "
                    "deficiency (~400 M people, X-linked) — "
                    "RBCs lose NADPH-dependent glutathione "
                    "regeneration → oxidative haemolysis "
                    "from fava beans, primaquine, sulfa "
                    "drugs."
                ),
            ),
            PathwayStep(
                2, ("6-Phosphogluconolactone", "H₂O"),
                "6-Phosphogluconolactonase",
                "3.1.1.31",
                ("6-Phosphogluconate",),
                "irreversible", None,
            ),
            PathwayStep(
                3, ("6-Phosphogluconate", "NADP+"),
                "6-Phosphogluconate dehydrogenase",
                "1.1.1.44",
                ("Ribulose-5-phosphate", "NADPH", "CO₂"),
                "irreversible", None,
                notes=(
                    "Second NADPH per G6P entered.  Net "
                    "oxidative branch: G6P + 2 NADP+ → "
                    "ribulose-5-P + 2 NADPH + CO₂."
                ),
            ),
            PathwayStep(
                4, ("Ribulose-5-phosphate",),
                "Ribose-5-phosphate isomerase + "
                "ribulose-5-phosphate epimerase",
                "5.3.1.6 + 5.1.3.1",
                ("Ribose-5-phosphate", "Xylulose-5-phosphate"),
                "reversible", None,
                notes=(
                    "Branch point: ribose-5-P heads to "
                    "nucleotide synthesis; xylulose-5-P "
                    "feeds the non-oxidative shuffle."
                ),
            ),
            PathwayStep(
                5, ("3 Pentose-5-phosphates",),
                "Transketolase + transaldolase + "
                "transketolase (a 2-3-2 carbon shuffle)",
                "2.2.1.1 + 2.2.1.2",
                ("2 Fructose-6-phosphate + "
                 "1 Glyceraldehyde-3-phosphate",),
                "reversible", None,
                notes=(
                    "Non-oxidative branch — converts excess "
                    "pentoses back to glycolytic "
                    "intermediates so the pathway can run "
                    "in 'NADPH-only' mode without "
                    "stockpiling pentose."
                ),
            ),
        ),
    ))

    # ---- Heme biosynthesis ----------------------------------------
    out.append(Pathway(
        id="heme_biosynthesis",
        name="Heme biosynthesis (porphyrin ring assembly)",
        category="specialised",
        cellular_compartment=(
            "Mitochondrion + cytoplasm shuttle (8-step "
            "cycle crossing both compartments)"
        ),
        overview=(
            "8-step assembly of heme b (the prosthetic group "
            "of haemoglobin / myoglobin / cytochromes / "
            "Complex IV) from succinyl-CoA + glycine.  Most "
            "active in bone marrow (haemoglobin synthesis) + "
            "liver (cytochrome P450).  Defects = porphyrias "
            "(8 distinct disease entities, one per enzyme)."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 22",
        steps=(
            PathwayStep(
                1, ("Succinyl-CoA", "Glycine"),
                "ALA synthase (ALAS1/ALAS2)",
                "2.3.1.37",
                ("δ-Aminolevulinic acid (ALA)", "CoA-SH",
                 "CO₂"),
                "irreversible", None,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Heme", "inhibitor",
                        "End-product feedback at translation + "
                        "transcription level (ALAS1)"),
                    RegulatoryEffector(
                        "Iron", "activator",
                        "ALAS2 (erythroid) translation + "
                        "stability"),
                ),
                notes=(
                    "Rate-limiting + mitochondrial.  ALAS2 "
                    "(erythroid-specific) deficiency causes "
                    "X-linked sideroblastic anaemia."
                ),
            ),
            PathwayStep(
                2, ("2 ALA",),
                "Porphobilinogen synthase / ALA dehydratase "
                "(ALAD)",
                "4.2.1.24", ("Porphobilinogen (PBG)",),
                "irreversible", None,
                notes=(
                    "Cytoplasmic.  Lead poisoning inhibits "
                    "ALAD — explains some lead-toxicity "
                    "haematological symptoms."
                ),
            ),
            PathwayStep(
                3, ("4 PBG",),
                "Porphobilinogen deaminase (HMBS)",
                "2.5.1.61",
                ("Hydroxymethylbilane (linear tetrapyrrole)",),
                "irreversible", None,
                notes=(
                    "HMBS deficiency = acute intermittent "
                    "porphyria (most common acute porphyria; "
                    "neurovisceral attacks)."
                ),
            ),
            PathwayStep(
                4, ("Hydroxymethylbilane",),
                "Uroporphyrinogen III synthase (UROS)",
                "4.2.1.75",
                ("Uroporphyrinogen III (cyclised "
                 "tetrapyrrole)",),
                "irreversible", None,
            ),
            PathwayStep(
                5, ("Uroporphyrinogen III",),
                "Uroporphyrinogen decarboxylase (UROD)",
                "4.1.1.37",
                ("Coproporphyrinogen III", "4 CO₂"),
                "irreversible", None,
                notes=(
                    "Cytoplasmic.  UROD deficiency = "
                    "porphyria cutanea tarda (most common "
                    "porphyria; photosensitivity + "
                    "blistering)."
                ),
            ),
            PathwayStep(
                6, ("Coproporphyrinogen III", "O₂"),
                "Coproporphyrinogen oxidase (CPOX)",
                "1.3.3.3",
                ("Protoporphyrinogen IX", "2 CO₂"),
                "irreversible", None,
                notes=(
                    "Mitochondrial — substrate must be "
                    "imported back."
                ),
            ),
            PathwayStep(
                7, ("Protoporphyrinogen IX", "O₂"),
                "Protoporphyrinogen oxidase (PPOX)",
                "1.3.3.4",
                ("Protoporphyrin IX",),
                "irreversible", None,
                notes=(
                    "Acifluorfen-type herbicides target "
                    "this enzyme in plants."
                ),
            ),
            PathwayStep(
                8, ("Protoporphyrin IX", "Fe²⁺"),
                "Ferrochelatase (FECH)",
                "4.99.1.1",
                ("Heme b",),
                "irreversible", None,
                notes=(
                    "Inserts Fe²⁺ into the porphyrin ring.  "
                    "FECH deficiency = erythropoietic "
                    "protoporphyria."
                ),
            ),
        ),
    ))

    # ---- Calvin cycle (photosynthesis carbon fixation) -----------
    out.append(Pathway(
        id="calvin_cycle",
        name="Calvin cycle (photosynthetic carbon fixation)",
        category="specialised",
        cellular_compartment="Chloroplast stroma (plants); cytoplasm (cyanobacteria)",
        overview=(
            "Light-independent reactions of photosynthesis.  "
            "13-step cycle that fixes 3 CO₂ molecules into "
            "1 G3P (which can leave for sucrose / starch "
            "synthesis), consuming 9 ATP + 6 NADPH from the "
            "light reactions per G3P.  Three phases: "
            "carboxylation (RuBisCO), reduction (G3P "
            "production), regeneration (RuBP "
            "regeneration).  Calvin won the 1961 Nobel."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 20",
        steps=(
            PathwayStep(
                1, ("3 RuBP (ribulose-1,5-bisphosphate)",
                    "3 CO₂"),
                "RuBisCO (ribulose-1,5-bisphosphate "
                "carboxylase / oxygenase)",
                "4.1.1.39",
                ("6 3-Phosphoglycerate (3-PGA)",),
                "irreversible", -35.0,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Mg²⁺ + carbamylation",
                        "activator",
                        "Light-induced stromal pH rise + "
                        "Mg²⁺ release activate RuBisCO via "
                        "Lys201 carbamylation"),
                    RegulatoryEffector(
                        "RuBisCO activase", "activator",
                        "ATP-dependent ratchet that removes "
                        "inhibitory sugar phosphates from "
                        "the active site"),
                ),
                notes=(
                    "The most abundant protein on Earth.  "
                    "Carboxylation rate is slow + RuBisCO "
                    "also catalyses photo-respiration "
                    "(O₂ instead of CO₂) — drove the "
                    "evolution of C4 / CAM photosynthesis "
                    "to concentrate CO₂."
                ),
            ),
            PathwayStep(
                2, ("6 3-PGA", "6 ATP"),
                "Phosphoglycerate kinase",
                "2.7.2.3",
                ("6 1,3-Bisphosphoglycerate", "6 ADP"),
                "reversible", None,
                notes="Same enzyme as glycolysis step 7 (reverse).",
            ),
            PathwayStep(
                3, ("6 1,3-BPG", "6 NADPH"),
                "G3P dehydrogenase (chloroplast isoform)",
                "1.2.1.13",
                ("6 G3P", "6 NADP+", "6 Pi"),
                "reversible", None,
                notes=(
                    "Reduction phase complete.  1 of 6 G3P "
                    "leaves for biosynthesis; the other 5 "
                    "regenerate 3 RuBP."
                ),
            ),
            PathwayStep(
                4, ("5 G3P (rearranged via aldolase + "
                    "transketolase + sedoheptulose-1,7-"
                    "bisphosphatase + ribulose-5-phosphate "
                    "epimerase)",),
                "Multi-enzyme regeneration phase",
                "(multi-enzyme)",
                ("3 Ribulose-5-phosphate",),
                "irreversible", None,
                notes=(
                    "Sugar-rearrangement chain that gets the "
                    "5 G3P back into the right number of "
                    "C5 sugars to remake 3 RuBP."
                ),
            ),
            PathwayStep(
                5, ("3 Ribulose-5-phosphate", "3 ATP"),
                "Phosphoribulokinase",
                "2.7.1.19",
                ("3 RuBP", "3 ADP"),
                "irreversible", None,
                notes="Closes the cycle.",
            ),
        ),
    ))

    # ---- Glycogen metabolism ------------------------------------
    out.append(Pathway(
        id="glycogen_metabolism",
        name="Glycogen synthesis + breakdown",
        category="specialised",
        cellular_compartment=(
            "Cytoplasm (liver + skeletal muscle, with "
            "tissue-specific isozymes)"
        ),
        overview=(
            "Reciprocally regulated synthesis "
            "(glycogenesis: glucose-6-P → glycogen for "
            "storage) + breakdown (glycogenolysis: glycogen "
            "→ G1P → G6P → glycolysis or release).  Hormonal "
            "control via cAMP-PKA cascade: glucagon + "
            "epinephrine activate breakdown, insulin "
            "activates synthesis.  Defects (glycogen-"
            "storage diseases I-XIV) cause hypoglycaemia / "
            "muscle weakness."
        ),
        textbook_reference="Nelson & Cox 8e, Ch. 15",
        steps=(
            PathwayStep(
                1, ("Glucose-6-phosphate",),
                "Phosphoglucomutase",
                "5.4.2.2",
                ("Glucose-1-phosphate",),
                "reversible", None,
                notes="Bidirectional (glycogen → glucose AND glucose → glycogen).",
            ),
            PathwayStep(
                2, ("Glucose-1-phosphate", "UTP"),
                "UDP-glucose pyrophosphorylase",
                "2.7.7.9",
                ("UDP-glucose", "PPi"),
                "irreversible", None,
                notes=(
                    "PPi hydrolysis pulls reaction "
                    "forward.  UDP-glucose is the activated "
                    "donor for glycogen synthesis."
                ),
            ),
            PathwayStep(
                3, ("UDP-glucose", "Glycogen(n) primer"),
                "Glycogen synthase",
                "2.4.1.11",
                ("Glycogen(n+1)", "UDP"),
                "irreversible", None,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Insulin → PP1 → dephosphorylation",
                        "activator",
                        "Active form is dephosphorylated; "
                        "PKA phosphorylation inactivates"),
                    RegulatoryEffector(
                        "Glucose-6-phosphate", "activator",
                        "Allosteric — feed-forward signal "
                        "for storage"),
                    RegulatoryEffector(
                        "Glucagon / epinephrine → PKA → "
                        "phosphorylation", "inhibitor",
                        "Hormonal off-switch during fasting "
                        "/ fight-or-flight"),
                ),
                notes=(
                    "Adds α-1,4 glycosidic bonds to the "
                    "non-reducing end of an existing "
                    "glycogen primer.  Branching enzyme "
                    "(glycogen branching enzyme, 2.4.1.18) "
                    "adds α-1,6 branches every ~10 "
                    "residues to keep glycogen compact."
                ),
            ),
            PathwayStep(
                4, ("Glycogen(n)", "Pi"),
                "Glycogen phosphorylase (PYGM muscle / "
                "PYGL liver / PYGB brain)",
                "2.4.1.1",
                ("Glycogen(n-1)", "Glucose-1-phosphate"),
                "irreversible", None,
                regulatory_effectors=(
                    RegulatoryEffector(
                        "Glucagon / epinephrine → PKA → "
                        "phosphorylation", "activator",
                        "Phosphorylated 'a' form is active"),
                    RegulatoryEffector(
                        "AMP", "activator",
                        "Allosteric activation of the "
                        "muscle isozyme during contraction"),
                    RegulatoryEffector(
                        "ATP / Glucose-6-P / Glucose",
                        "inhibitor",
                        "Allosteric — high energy / glucose "
                        "= no need to break down glycogen"),
                    RegulatoryEffector(
                        "Insulin → PP1 → dephosphorylation",
                        "inhibitor",
                        "Switches off glycogenolysis"),
                ),
                notes=(
                    "Phosphorolysis (NOT hydrolysis) — "
                    "energetically efficient because the "
                    "G1P product is already activated for "
                    "the next step (mutase → G6P → "
                    "glycolysis)."
                ),
            ),
            PathwayStep(
                5, ("Glucose-1-phosphate",),
                "Phosphoglucomutase (reverse direction)",
                "5.4.2.2",
                ("Glucose-6-phosphate",),
                "reversible", None,
                notes=(
                    "G6P now feeds into glycolysis (muscle, "
                    "brain) OR is dephosphorylated by "
                    "glucose-6-phosphatase (liver, kidney) "
                    "to free glucose for export to the "
                    "bloodstream."
                ),
            ),
        ),
    ))

    return out


_PATHWAYS: List[Pathway] = _build_catalogue()


# ------------------------------------------------------------------
# Public lookup helpers
# ------------------------------------------------------------------

def list_pathways(category: Optional[str] = None
                  ) -> List[Pathway]:
    if category is None:
        return list(_PATHWAYS)
    if category not in VALID_CATEGORIES:
        return []
    return [p for p in _PATHWAYS if p.category == category]


def get_pathway(pathway_id: str) -> Optional[Pathway]:
    for p in _PATHWAYS:
        if p.id == pathway_id:
            return p
    return None


def find_pathways(needle: str) -> List[Pathway]:
    if not needle:
        return []
    n = needle.lower().strip()
    out: List[Pathway] = []
    for p in _PATHWAYS:
        if (n in p.id.lower() or n in p.name.lower()
                or n in p.category.lower()
                or n in p.overview.lower()):
            out.append(p)
    return out


def categories() -> List[str]:
    return list(VALID_CATEGORIES)


def pathway_to_dict(p: Pathway) -> Dict[str, object]:
    return {
        "id": p.id,
        "name": p.name,
        "category": p.category,
        "cellular_compartment": p.cellular_compartment,
        "overview": p.overview,
        "overall_delta_g_kjmol": p.overall_delta_g_kjmol,
        "textbook_reference": p.textbook_reference,
        "n_steps": len(p.steps),
        "steps": [step_to_dict(s) for s in p.steps],
    }


def step_to_dict(s: PathwayStep) -> Dict[str, object]:
    return {
        "step_number": s.step_number,
        "substrates": list(s.substrates),
        "enzyme_name": s.enzyme_name,
        "ec_number": s.ec_number,
        "products": list(s.products),
        "reversibility": s.reversibility,
        "delta_g_kjmol": s.delta_g_kjmol,
        "regulatory_effectors": [
            {
                "name": r.name,
                "mode": r.mode,
                "mechanism": r.mechanism,
            } for r in s.regulatory_effectors
        ],
        "notes": s.notes,
    }
