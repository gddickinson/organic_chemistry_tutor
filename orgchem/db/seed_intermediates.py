"""Seed **intermediate** molecules that appear in reactions / pathways — Phase 6f.3.

When a student explores a reaction scheme or a pathway, every fragment
they see should be clickable / browsable in the molecule DB. Today the
main-compound set (reactants, products, reference compounds) is well
covered but short-lived **intermediates** (carbocations, enolates,
tetrahedral intermediates, protected amino acids for SPPS, cofactor
substrates for enzyme mechanisms, etc.) are often absent — so the
"where does this molecule live?" link breaks in mid-scheme.

This module adds a curated list of those intermediates with the
``source='intermediate'`` tag. Additive by name — re-running seed is safe.
"""
from __future__ import annotations
import json
import logging
from typing import List, Tuple

from orgchem.core.molecule import Molecule as ChemMol
from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# (name, SMILES, source-tag) — tag distinguishes these from main-compound seeds.
_INTERMEDIATES: List[Tuple[str, str, str]] = [
    # ---- SN1 / E1 carbocations ---------------------------------------
    ("tert-Butyl cation",        "C[C+](C)C",                          "intermediate"),
    ("Isopropyl cation",         "C[CH+]C",                            "intermediate"),
    ("Benzyl cation",            "[CH2+]c1ccccc1",                     "intermediate"),
    ("Allyl cation",             "[CH2+]C=C",                          "intermediate"),
    ("Methyl cation",            "[CH3+]",                             "intermediate"),

    # ---- Enolates (aldol / Michael / Claisen) ------------------------
    ("Acetone enolate",          "[CH2-]C(=O)C",                       "intermediate"),
    ("Acetaldehyde enolate",     "[CH2-]C=O",                          "intermediate"),
    ("Ethyl acetate enolate",    "[CH2-]C(=O)OCC",                     "intermediate"),
    ("Methyl vinyl ketone",      "C=CC(=O)C",                          "intermediate"),

    # ---- SN2 / E2 leaving groups -------------------------------------
    ("Methyl bromide",           "CBr",                                "intermediate"),
    ("2-Bromobutane",            "CCC(C)Br",                           "intermediate"),
    ("tert-Butyl bromide",       "CC(C)(C)Br",                         "intermediate"),
    ("Hydroxide",                "[OH-]",                              "intermediate"),
    ("Bromide",                  "[Br-]",                              "intermediate"),

    # ---- Aldol / Grignard intermediates ------------------------------
    ("Isobutylene",              "CC(=C)C",                            "intermediate"),
    ("3-Hydroxybutanal (aldol adduct)", "CC(O)CC=O",                   "intermediate"),
    ("Magnesium methoxide",      "CO[Mg]",                             "intermediate"),
    ("Methyl magnesium bromide", "C[Mg]Br",                            "intermediate"),
    ("Ethyl magnesium bromide",  "CC[Mg]Br",                           "intermediate"),

    # ---- Nitration / EAS intermediates -------------------------------
    ("Nitrobenzene",             "[O-][N+](=O)c1ccccc1",               "intermediate"),
    ("Benzyl bromide",           "BrCc1ccccc1",                        "intermediate"),
    ("Acetyl chloride",          "CC(=O)Cl",                           "intermediate"),
    ("Methyl chloride",          "CCl",                                "intermediate"),
    ("Chloromethane (electrophile)", "[CH3+]",                         "intermediate"),

    # ---- Pathway-specific intermediates ------------------------------
    # Aspirin route (phenol + AcOH / Kolbe-Schmitt)
    ("Sodium salicylate",        "[Na+].[O-]C(=O)c1ccccc1O",           "intermediate"),
    # Ibuprofen BHC intermediate: 4-isobutylacetophenone
    ("4-Isobutylacetophenone",   "CC(C)Cc1ccc(C(C)=O)cc1",             "intermediate"),
    # Paracetamol Hoechst intermediate: 4-nitrophenol, 4-aminophenol
    ("4-Nitrophenol",            "[O-][N+](=O)c1ccc(O)cc1",            "intermediate"),
    ("4-Aminophenol",            "Nc1ccc(O)cc1",                       "intermediate"),
    # Vanillin-from-eugenol intermediate: isoeugenol
    ("Isoeugenol",               "COc1cc(/C=C/C)ccc1O",                "intermediate"),
    # Caffeine from theobromine
    ("Theobromine",              "Cn1c(=O)c2[nH]cnc2n(C)c1=O",         "intermediate"),

    # ---- Fmoc / SPPS intermediates -----------------------------------
    ("Fmoc-Gly-OH",              "O=C(OCC1c2ccccc2-c2ccccc21)NCC(=O)O", "intermediate"),
    ("Fmoc-Phe-OH",
        "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](Cc1ccccc1)C(=O)O",         "intermediate"),
    ("Fmoc-Met-OH",
        "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](CCSC)C(=O)O",              "intermediate"),
    ("Fmoc-Tyr-OH",
        "O=C(OCC1c2ccccc2-c2ccccc21)N[C@@H](Cc1ccc(O)cc1)C(=O)O",      "intermediate"),
    ("Dibenzofulvene",
        "C=C1c2ccccc2-c2ccccc21",                                      "intermediate"),
    ("9-Fluorenylmethanol",
        "OCC1c2ccccc2-c2ccccc21",                                      "intermediate"),

    # ---- Enzyme substrates / cofactors -------------------------------
    ("DHAP (dihydroxyacetone phosphate)",
        "OCC(=O)COP(=O)(O)O",                                          "intermediate"),
    ("G3P (glyceraldehyde-3-phosphate)",
        "O=C[C@@H](O)COP(=O)(O)O",                                     "intermediate"),
    ("Fructose-1,6-bisphosphate",
        "OP(=O)(O)OC[C@@H](O)[C@H](O)[C@@H](O)C(=O)COP(=O)(O)O",       "intermediate"),
    ("Pyruvate",                 "CC(=O)C(=O)[O-]",                    "intermediate"),
    ("Phosphate",                "OP(=O)(O)O",                         "intermediate"),
    ("N-acetylglycine (chymotrypsin substrate analogue)",
        "CC(=O)NCC(=O)O",                                              "intermediate"),

    # ---- Pericyclic / small building blocks --------------------------
    ("1,3-Butadiene",            "C=CC=C",                             "intermediate"),
    ("Ethylene (dienophile)",    "C=C",                                "intermediate"),
    ("Cyclohexene",              "C1=CCCCC1",                          "intermediate"),
    ("1,3-Cyclohexadiene",       "C1=CC=CCC1",                         "intermediate"),
    ("Hexatriene",               "C=CC=CC=C",                          "intermediate"),

    # ---- Reagents that appear in reaction schemes but aren't reagents -
    ("Hydrogen bromide",         "Br",                                 "intermediate"),
    ("Hydrogen chloride",        "Cl",                                 "intermediate"),
    ("Hydrogen iodide",          "I",                                  "intermediate"),
    ("Ammonia",                  "N",                                  "intermediate"),
    ("Cyanide",                  "[C-]#N",                             "intermediate"),

    # ---- Oxidation intermediates -------------------------------------
    ("Propan-2-ol",              "CC(C)O",                             "intermediate"),
    ("Acetic acid ethyl ester enolate",
        "[CH2-]C(=O)OCC",                                              "intermediate"),

    # ---- Wittig --------------------------------------------------------
    ("Triphenylphosphine",       "c1ccc(P(c2ccccc2)c2ccccc2)cc1",      "intermediate"),
    ("Triphenylphosphine oxide", "O=P(c1ccccc1)(c1ccccc1)c1ccccc1",    "intermediate"),
    ("Methylenetriphenylphosphorane (ylide)",
        "[CH2-][P+](c1ccccc1)(c1ccccc1)c1ccccc1",                      "intermediate"),

    # ---- Small-molecule reagents (second wave, from Phase 6f.4 audit) -
    ("Ethane",                   "CC",                                 "alkane"),
    ("Molecular hydrogen",       "[H][H]",                             "intermediate"),
    ("Molecular bromine",        "BrBr",                               "intermediate"),
    ("Molecular chlorine",       "ClCl",                               "intermediate"),
    ("Molecular iodine",         "II",                                 "intermediate"),
    ("1,2-Dibromoethane",        "BrCCBr",                             "intermediate"),
    ("Chloroethane",             "CCCl",                               "intermediate"),
    ("2-Butene (unspecified)",   "CC=CC",                              "intermediate"),
    ("N-Methylacetamide",        "CNC(C)=O",                           "intermediate"),
    ("N-Ethylacetamide",         "CCNC(C)=O",                          "intermediate"),
    ("Ethylamine",               "CCN",                                "intermediate"),
    ("Ribose 2',3'-cyclic phosphate (simplified)",
                                 "O=P1(O)OCC(O)CO1",                   "intermediate"),
    ("Mesityl oxide",            "CC(=O)C=C(C)C",                      "intermediate"),
    ("Ethyl acetoacetate",       "CCOC(=O)CC(C)=O",                    "intermediate"),
    ("Benzyl alcohol",           "OCc1ccccc1",                         "alcohol"),
    ("Benzoate",                 "O=C([O-])c1ccccc1",                  "intermediate"),
    ("2,5-Hexanedione",          "CC(=O)CCC(C)=O",                     "intermediate"),
    ("Peracetic acid",           "CC(=O)OO",                           "reagent"),
    ("Bromobenzene",             "Brc1ccccc1",                         "intermediate"),
    ("Phenylboronic acid",       "OB(O)c1ccccc1",                      "reagent"),
    ("Boric acid",               "OB(O)O",                             "intermediate"),
    ("Ethylbenzene",             "CCc1ccccc1",                         "intermediate"),
    ("Isopropylbenzene (cumene)", "CC(C)c1ccccc1",                     "intermediate"),
    ("Nitric acid",              "O=[N+]([O-])O",                      "reagent"),
    ("Magnesium bromide hydroxide",
        "[OH][Mg][Br]",                                                "intermediate"),
    ("Bromomagnesium oxide (Grignard alkoxide)",
        "[O-][Mg]Br",                                                  "intermediate"),
    ("Acetophenone cation (EAS intermediate)",
        "CC(=O)c1ccccc1",                                              "intermediate"),
    ("Acetyl ester (generic)",   "CC(C)=O",                            "intermediate"),
    # Aldol / condensation related
    ("2-Methyl-2-pentenal",      "CC(=O)C=C(C)C",                      "intermediate"),
    ("Ethyl 3-oxobutanoate",     "CCOC(=O)CC(C)=O",                    "intermediate"),
    # Common small organics that appear in schemes
    ("Carbon dioxide",           "O=C=O",                              "intermediate"),
    ("Carbon monoxide",          "[C-]#[O+]",                          "intermediate"),
    ("Formate",                  "[O-]C=O",                            "intermediate"),
    ("Acetate",                  "CC(=O)[O-]",                         "intermediate"),
    ("Methoxide",                "[O-]C",                              "intermediate"),
    ("Ethoxide",                 "[O-]CC",                             "intermediate"),
    ("Sulfuric acid",            "OS(=O)(=O)O",                        "reagent"),
    ("Hydroxylamine",            "NO",                                 "intermediate"),
    ("Hydrazine",                "NN",                                 "intermediate"),
    # Common isomers that show up in reactions as minor products
    ("trans-Stilbene",           "C(=C\\c1ccccc1)/c1ccccc1",           "intermediate"),
    ("Styrene",                  "C=Cc1ccccc1",                        "intermediate"),
    ("Cinnamaldehyde",           "O=C/C=C/c1ccccc1",                   "intermediate"),
    ("Acrolein",                 "O=CC=C",                             "intermediate"),

    # ---- Third-wave gap-fillers (from Phase 6f.4 audit) --------------
    ("Pinacol (2,3-dimethyl-2,3-butanediol)",
        "CC(C)(O)C(C)(C)O",                                            "intermediate"),
    ("Pinacolone",               "CC(=O)C(C)(C)C",                     "intermediate"),
    ("α-Bromopropanoic acid",    "CC(Br)C(=O)O",                       "intermediate"),
    ("Isobutylbenzene",          "CC(C)Cc1ccccc1",                     "intermediate"),
    ("1-(4-Isobutylphenyl)ethanol",
        "CC(C)Cc1ccc(C(C)O)cc1",                                       "intermediate"),
    ("Caffeine (protonated intermediate)",
        "Cn1cnc2c1c(=O)[nH]c(=O)n2C",                                  "intermediate"),
    ("Methyl iodide",            "CI",                                 "reagent"),
    ("Iodide",                   "[I-]",                               "intermediate"),
    ("Phenacetin (ethoxy intermediate)",
        "CCOc1ccc(NC(C)=O)cc1",                                        "intermediate"),
    ("4-Vinylguaiacol",          "C=Cc1ccc(O)c(OC)c1",                 "intermediate"),
    ("Isoeugenol (alt SMILES)",  "CC=Cc1ccc(O)c(OC)c1",                "intermediate"),
    ("Ethyl bromide",            "CCBr",                               "reagent"),
    ("Magnesium (metal)",        "[Mg]",                               "reagent"),
    ("2-Methyl-2-butanol",       "CCC(C)(C)O",                         "alcohol"),
    ("Silver cation",            "[Ag+]",                              "intermediate"),
    ("Cyanate",                  "N#C[O-]",                            "intermediate"),
    ("Ammonium",                 "[NH4+]",                             "intermediate"),
    ("Chloride",                 "[Cl-]",                              "intermediate"),
    ("Proton",                   "[H+]",                               "intermediate"),
    ("Oxygen atom",              "[O]",                                "intermediate"),
    ("Hydroxyl radical",         "[OH]",                               "intermediate"),
    ("Fructose-1,6-bisphosphate (ketone form)",
        "O=C(CO)[C@@H](O)[C@H](O)[C@@H](O)COP(=O)(O)O",                "intermediate"),

    # ---- SPPS growing-chain intermediates ----------------------------
    # After Fmoc deprotection of Met-resin (the starting compound of
    # step 1 is actually the deprotected resin-bound Met).
    ("H-Met-OH (free methionine)", "CSCC[C@H](N)C(=O)O",               "intermediate"),
    # Fmoc-Phe-Met dipeptide (after step 2 coupling).
    ("Fmoc-Phe-Met-OH",
        "CSCC[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)OCC1c2ccccc2-c2ccccc21)C(=O)O",
                                                                       "intermediate"),
    # Fmoc-Gly-Phe-Met tripeptide (after step 3).
    ("Fmoc-Gly-Phe-Met-OH",
        "CSCC[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)CNC(=O)OCC1c2ccccc2-c2ccccc21)C(=O)O",
                                                                       "intermediate"),
    # Fmoc-Gly-Gly-Phe-Met tetrapeptide (after step 4).
    ("Fmoc-Gly-Gly-Phe-Met-OH",
        "CSCC[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)CNC(=O)CNC(=O)OCC1c2ccccc2-c2ccccc21)C(=O)O",
                                                                       "intermediate"),
    # H-Tyr-Gly-Gly-Phe-Met-OH — final Met-enkephalin with N-terminal Tyr
    # deprotected (same as Met-enkephalin but listed as intermediate so
    # the audit records it for the SPPS step).
    ("H-Tyr-Gly-Gly-Phe-Met-OH (Met-enkephalin)",
        "CSCC[C@H](NC(=O)[C@H](Cc1ccccc1)NC(=O)CNC(=O)CNC(=O)[C@@H](N)Cc1ccc(O)cc1)C(=O)O",
                                                                       "intermediate"),
    # The carbonate by-product liberated by TFA cleavage / the original
    # Fmoc protecting-group base residue.
    ("Fmoc-OH (9-fluorenylmethyl carbonate)",
        "O=C(O)OCC1c2ccccc2-c2ccccc21",                                "intermediate"),

    # ---- Phase 31b reaction-fragment backfill (2026-04-23) ------------
    # Products / byproducts referenced by the five new reactions so the
    # fragment-consistency audit stays clean.
    ("4-Phenylmorpholine",
        "c1ccc(N2CCOCC2)cc1",                                          "intermediate"),
    ("Iodobenzene",
        "Ic1ccccc1",                                                   "intermediate"),
    ("Phenylacetylene",
        "C#Cc1ccccc1",                                                 "intermediate"),
    ("Diphenylacetylene (tolan)",
        "C(#Cc1ccccc1)c1ccccc1",                                       "intermediate"),
    # ---- Phase 31b round 134 — CuAAC click chemistry fragments -------
    ("Benzyl azide",
        "[N-]=[N+]=NCc1ccccc1",                                        "intermediate"),
    ("1-Benzyl-4-phenyl-1,2,3-triazole",
        "c1ccc(Cn2cc(-c3ccccc3)nn2)cc1",                               "intermediate"),
    ("Isopropyl acetate",
        "CC(=O)OC(C)C",                                                "intermediate"),
    ("1-Octanol",
        "CCCCCCCCO",                                                   "intermediate"),
    ("Octanal",
        "CCCCCCCC=O",                                                  "intermediate"),
    ("Triethyl phosphonoacetate",
        "CCOC(=O)CP(=O)(OCC)OCC",                                      "intermediate"),
    ("Ethyl (E)-cinnamate",
        "CCOC(=O)/C=C/c1ccccc1",                                       "intermediate"),
    ("Diethyl phosphate",
        "CCOP(=O)(O)OCC",                                              "intermediate"),

    # ---- Phase 31d pathway-fragment backfill (2026-04-23) ----------
    # Benzocaine route
    ("p-Nitrotoluene",
        "Cc1ccc([N+](=O)[O-])cc1",                                     "intermediate"),
    ("p-Nitrobenzoic acid",
        "O=C(O)c1ccc([N+](=O)[O-])cc1",                                "intermediate"),
    ("p-Aminobenzoic acid (PABA)",
        "Nc1ccc(C(=O)O)cc1",                                           "intermediate"),
    ("Benzocaine",
        "CCOC(=O)c1ccc(N)cc1",                                         "drug"),
    # Lidocaine route
    ("2,6-Dimethylaniline (2,6-xylidine)",
        "Cc1cccc(C)c1N",                                               "intermediate"),
    ("Chloroacetyl chloride",
        "O=C(Cl)CCl",                                                  "intermediate"),
    ("α-Chloro-N-(2,6-xylyl)acetamide",
        "Cc1cccc(C)c1NC(=O)CCl",                                       "intermediate"),
    ("Diethylamine",
        "CCNCC",                                                       "intermediate"),
    ("Lidocaine",
        "CCN(CC)CC(=O)Nc1c(C)cccc1C",                                  "drug"),
    # Procaine route (round 65)
    ("Thionyl chloride",
        "ClS(=O)Cl",                                                   "reagent"),
    ("4-Aminobenzoyl chloride",
        "Nc1ccc(C(=O)Cl)cc1",                                          "intermediate"),
    ("Sulfur dioxide",
        "O=S=O",                                                       "reagent"),
    ("2-(Diethylamino)ethanol",
        "CCN(CC)CCO",                                                  "intermediate"),
    ("Procaine",
        "CCN(CC)CCOC(=O)c1ccc(N)cc1",                                  "drug"),
    # Sulfanilamide route (round 75)
    ("Acetanilide",
        "CC(=O)Nc1ccccc1",                                             "intermediate"),
    ("Chlorosulfonic acid",
        "OS(=O)(=O)Cl",                                                "reagent"),
    ("4-Acetamidobenzenesulfonyl chloride",
        "CC(=O)Nc1ccc(S(=O)(=O)Cl)cc1",                                "intermediate"),
    ("Ammonia",
        "N",                                                           "reagent"),
    ("4-Acetamidobenzenesulfonamide",
        "CC(=O)Nc1ccc(S(=O)(=O)N)cc1",                                 "intermediate"),
    ("Sulfanilamide",
        "Nc1ccc(S(=O)(=O)N)cc1",                                       "drug"),
    # Phenolphthalein route (round 75)
    ("Phthalic anhydride",
        "O=C1OC(=O)c2ccccc12",                                         "intermediate"),
    ("Phenol",
        "Oc1ccccc1",                                                   "intermediate"),
    ("Phenolphthalein",
        "OC1=CC=C(C=C1)C1(c2ccc(O)cc2)OC(=O)c2ccccc21",                "dye"),
    # Saccharin + acetanilide routes (round 76)
    ("Toluene",
        "Cc1ccccc1",                                                   "solvent"),
    ("2-Methylbenzenesulfonyl chloride",
        "Cc1ccccc1S(=O)(=O)Cl",                                        "intermediate"),
    ("2-Methylbenzenesulfonamide",
        "Cc1ccccc1S(=O)(=O)N",                                         "intermediate"),
    ("Potassium permanganate",
        "[K+].O=[Mn](=O)(=O)[O-]",                                     "reagent"),
    ("Permanganate ion",
        "O=[Mn](=O)(=O)[O-]",                                          "reagent"),
    ("Potassium cation",
        "[K+]",                                                        "reagent"),
    ("Manganese dioxide",
        "O=[Mn]=O",                                                    "reagent"),
    ("Hydroxide ion",
        "[OH-]",                                                       "intermediate"),
    ("Saccharin",
        "O=C1NS(=O)(=O)c2ccccc21",                                     "drug"),
    ("Acetic anhydride",
        "CC(=O)OC(=O)C",                                               "reagent"),
    # L-DOPA + Dopamine routes (round 78)
    ("Veratraldehyde (3,4-dimethoxybenzaldehyde)",
        "O=Cc1ccc(OC)c(OC)c1",                                         "intermediate"),
    ("N-Acetylglycine",
        "CC(=O)NCC(=O)O",                                              "intermediate"),
    ("(Z)-2-Acetamido-3-(3,4-dimethoxyphenyl)acrylic acid",
        "CC(=O)N/C(=C\\c1ccc(OC)c(OC)c1)/C(=O)O",                      "intermediate"),
    ("N-Acetyl-(S)-3,4-dimethoxyphenylalanine",
        "CC(=O)N[C@@H](Cc1ccc(OC)c(OC)c1)C(=O)O",                      "intermediate"),
    ("L-DOPA (levodopa)",
        "N[C@@H](Cc1ccc(O)c(O)c1)C(=O)O",                              "drug"),
    ("Dopamine",
        "NCCc1ccc(O)c(O)c1",                                           "neurotransmitter"),
    ("Hydrogen gas",
        "[H][H]",                                                      "reagent"),
    ("Hydrogen bromide",
        "[H]Br",                                                       "reagent"),
    ("Methyl bromide",
        "CBr",                                                         "intermediate"),
    ("Carbon dioxide",
        "O=C=O",                                                       "reagent"),
    # Adipic acid + Nylon-6,6 routes (round 79)
    ("Cyclohexane",
        "C1CCCCC1",                                                    "solvent"),
    ("Oxygen (O₂)",
        "O=O",                                                         "reagent"),
    ("Cyclohexanol",
        "OC1CCCCC1",                                                   "intermediate"),
    ("Cyclohexanone",
        "O=C1CCCCC1",                                                  "intermediate"),
    ("Nitric acid",
        "O[N+](=O)[O-]",                                               "reagent"),
    ("Adipic acid",
        "OC(=O)CCCCC(=O)O",                                            "intermediate"),
    ("Nitrous oxide (N₂O)",
        "[N-]=[N+]=O",                                                 "reagent"),
    ("1,6-Diaminohexane (HMDA)",
        "NCCCCCCN",                                                    "intermediate"),
    ("Nylon-6,6 salt (AH salt)",
        "[NH3+]CCCCCC[NH3+].[O-]C(=O)CCCCC(=O)[O-]",                   "intermediate"),
    ("Nylon-6,6 (model dimer)",
        "NCCCCCCNC(=O)CCCCC(=O)NCCCCCCN",                              "polymer"),
    # Counter-ion fragments the fragment-consistency audit wants
    # separately (same pattern as the KMnO₄ round-76 gotcha).
    ("Hexamethylenediammonium dication",
        "[NH3+]CCCCCC[NH3+]",                                          "intermediate"),
    ("Adipate dianion",
        "[O-]C(=O)CCCCC(=O)[O-]",                                      "intermediate"),
    # Nylon-6 / caprolactam route (round 80)
    ("Hydroxylamine",
        "ON",                                                          "reagent"),
    ("Cyclohexanone oxime",
        "ON=C1CCCCC1",                                                 "intermediate"),
    ("ε-Caprolactam",
        "O=C1CCCCCN1",                                                 "intermediate"),
    ("Sulfuric acid",
        "OS(=O)(=O)O",                                                 "reagent"),
    ("Nylon-6 (model dimer)",
        "NCCCCCC(=O)NCCCCCC(=O)O",                                     "polymer"),
    # Aspartame route (round 80)
    ("L-Aspartic acid",
        "N[C@@H](CC(=O)O)C(=O)O",                                      "intermediate"),
    ("Z-L-Aspartic acid (Cbz protected)",
        "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)O",                       "intermediate"),
    ("L-Phenylalanine methyl ester",
        "COC(=O)[C@@H](N)Cc1ccccc1",                                   "intermediate"),
    ("Z-Aspartame",
        "O=C(OCc1ccccc1)N[C@@H](CC(=O)O)C(=O)N[C@@H](Cc1ccccc1)C(=O)OC",
        "intermediate"),
    ("Aspartame",
        "COC(=O)[C@@H](Cc1ccccc1)NC(=O)[C@@H](N)CC(=O)O",              "drug"),

    # ---- Phase 31b round 121 — Heck reaction fragments -------------
    ("Methyl acrylate",
        "C=CC(=O)OC",                                                  "reagent"),
    ("Methyl cinnamate (trans)",
        "COC(=O)/C=C/c1ccccc1",                                        "intermediate"),

    # ---- Phase 31b round 123 — Negishi coupling fragments ----------
    ("Phenylzinc chloride",
        "[Cl][Zn][c]1ccccc1",                                          "reagent"),
    ("Zinc bromochloride",
        "[Cl][Zn][Br]",                                                "intermediate"),

    # ---- Phase 31b round 152 — Birch reduction fragments -----------
    ("Sodium metal",
        "[Na]",                                                        "reagent"),
    ("Sodium cation",
        "[Na+]",                                                       "intermediate"),
    ("1,4-Cyclohexadiene",
        "C1=CCC=CC1",                                                  "intermediate"),

    # ---- Phase 31b round 153 — Sharpless + CBS fragments -----------
    ("trans-Crotyl alcohol (E-2-buten-1-ol)",
        "C/C=C/CO",                                                    "intermediate"),
    ("tert-Butyl hydroperoxide (TBHP)",
        "CC(C)(C)OO",                                                  "reagent"),
    ("(2R,3R)-2,3-Epoxybutan-1-ol",
        "C[C@@H]1O[C@H]1CO",                                           "intermediate"),
    ("Borane (BH3)",
        "B",                                                           "reagent"),
    ("(R)-1-Phenylethanol",
        "C[C@H](O)c1ccccc1",                                           "intermediate"),

    # ---- Phase 31b round 154 — Sharpless AD + Jacobsen fragments ---
    # (trans-Stilbene already seeded at the top; SMILES corrected
    # round 154 to the canonical E-isomer.)
    ("Osmium tetroxide (OsO4)",
        "O=[Os](=O)(=O)=O",                                            "reagent"),
    ("Osmium dioxide (OsO2)",
        "O=[Os]=O",                                                    "intermediate"),
    ("(1R,2R)-1,2-Diphenylethane-1,2-diol",
        "O[C@@H](c1ccccc1)[C@H](O)c1ccccc1",                           "intermediate"),
    ("cis-β-Methylstyrene (Z-1-phenyl-1-propene)",
        "C/C=C\\c1ccccc1",                                             "intermediate"),
    ("Hypochlorite (OCl-)",
        "[O-]Cl",                                                      "reagent"),
    ("(2R,3S)-2-Methyl-3-phenyloxirane",
        "C[C@H]1O[C@@H]1c1ccccc1",                                     "intermediate"),

    # ---- Phase 31b round 155 — Mukaiyama + Evans aldol fragments ---
    ("Trimethylsilyl enol ether of acetone",
        "C=C(C)O[Si](C)(C)C",                                          "intermediate"),
    ("(R)-4-Hydroxy-4-phenylbutan-2-one (Mukaiyama aldol product)",
        "CC(=O)C[C@H](O)c1ccccc1",                                     "intermediate"),
    ("Trimethylsilanol (TMS-OH)",
        "C[Si](C)(C)O",                                                "intermediate"),
    ("N-Propionyl-(S)-4-benzyl-2-oxazolidinone (Evans auxiliary acylated)",
        "CCC(=O)N1C(=O)OC[C@@H]1Cc1ccccc1",                            "reagent"),
    ("Evans syn-aldol (N-acyl-(2S,3R)-3-hydroxy-2-methylpentanoyl)",
        "CC[C@H](O)[C@@H](C)C(=O)N1C(=O)OC[C@@H]1Cc1ccccc1",           "intermediate"),

    # ---- Phase 31b round 156 — Stille + Corey-Chaykovsky fragments
    ("Tributyl(vinyl)stannane",
        "C=C[Sn](CCCC)(CCCC)CCCC",                                     "reagent"),
    ("Tributyltin bromide (Bu3SnBr)",
        "CCCC[Sn](CCCC)(CCCC)Br",                                      "intermediate"),
    ("Dimethylsulfonium methylide (Corey ylide)",
        "C[S+](C)[CH2-]",                                              "reagent"),
    ("Dimethyl sulfide (DMS)",
        "CSC",                                                         "intermediate"),

    # ---- Phase 31b round 157 — Appel + Jones fragments -------------
    ("Carbon tetrachloride (CCl4)",
        "ClC(Cl)(Cl)Cl",                                               "reagent"),
    ("1-Chlorooctane",
        "CCCCCCCCCl",                                                  "intermediate"),
    ("Chloroform (CHCl3)",
        "ClC(Cl)Cl",                                                   "intermediate"),
    ("Chromium trioxide (CrO3, Jones reagent)",
        "O=[Cr](=O)=O",                                                "reagent"),
    ("Octanoic acid (caprylic acid)",
        "CCCCCCCC(=O)O",                                               "intermediate"),
    ("Chromium dioxide (CrO2)",
        "O=[Cr]=O",                                                    "intermediate"),

    # ---- Phase 31b round 164 — Wacker + Brown fragments ------------
    ("1-Methylcyclohexene",
        "CC1=CCCCC1",                                                  "intermediate"),
    ("Hydrogen peroxide (H2O2)",
        "OO",                                                          "reagent"),
    ("trans-2-Methylcyclohexanol",
        "C[C@@H]1CCCC[C@H]1O",                                         "intermediate"),

    # ---- Phase 31b round 165 — Robinson + Knoevenagel fragments ----
    ("Δ1,9-Octalin-2-one (Robinson annulation product)",
        "O=C1C=C2CCCCC2CC1",                                           "intermediate"),
    ("Diethyl malonate",
        "CCOC(=O)CC(=O)OCC",                                           "reagent"),
    ("Diethyl benzylidene malonate",
        "CCOC(=O)/C(=C\\c1ccccc1)C(=O)OCC",                            "intermediate"),

    # ---- Phase 31b round 175 — Henry + Hantzsch fragments ----------
    ("Nitromethane",
        "C[N+](=O)[O-]",                                               "reagent"),
    ("2-Nitro-1-phenylethanol (Henry product)",
        "O=[N+]([O-])CC(O)c1ccccc1",                                   "intermediate"),
    ("Hantzsch 1,4-dihydropyridine "
     "(diethyl 4-phenyl-2,6-dimethyl-DHP-3,5-dicarboxylate)",
        "CCOC(=O)C1=C(C)NC(C)=C(C(=O)OCC)C1c1ccccc1",                  "intermediate"),

    # ---- Phase 31b round 182 — Grubbs / Hofmann / ozonolysis -------
    ("1-Hexene",
        "C=CCCCC",                                                     "reagent"),
    ("1-Phenyl-1-hexene (Grubbs cross-metathesis product)",
        "CCCCC=Cc1ccccc1",                                             "intermediate"),
    ("2-Pentyltrimethylammonium (Hofmann substrate)",
        "CCCC(C)[N+](C)(C)C",                                          "intermediate"),
    ("1-Pentene",
        "C=CCCC",                                                      "reagent"),
    ("Ozone",
        "O=[O+][O-]",                                                  "reagent"),
]


#: Round 154 — one-shot SMILES-fix backfill.  Applies ONLY to rows
#: in this dict (keyed by name) where the stored SMILES doesn't
#: match the source-of-truth.  Gentle: never touches a row whose
#: stored SMILES already canonicalises to the target.  Idempotent.
_SMILES_FIXES: dict = {
    # The pre-round-154 row stored cis-stilbene (`C(/c1ccccc1)=C/c1ccccc1`)
    # under the name "trans-Stilbene" — a real bug.  Round 154's
    # Sharpless asymmetric dihydroxylation reaction needs the actual
    # E-isomer, so backfill the row to canonical trans-stilbene.
    "trans-Stilbene": "C(=C\\c1ccccc1)/c1ccccc1",
}


def seed_intermediates() -> int:
    """Additively insert intermediate molecules by name + apply
    one-shot SMILES backfills for known buggy historical rows.

    Mirrors the additive-backfill logic in ``seed.py``: re-running on an
    existing DB is safe; pre-existing molecules (by name) are untouched
    UNLESS the name appears in ``_SMILES_FIXES`` AND the stored SMILES
    does not canonicalise to the target.
    """
    with session_scope() as s:
        existing_names = {row.name for row in s.query(DBMol.name).all()}

    to_add = [e for e in _INTERMEDIATES if e[0] not in existing_names]
    added = 0
    if to_add:
        log.info("Seeding %d intermediate molecules.", len(to_add))
        with session_scope() as s:
            for name, smi, tag in to_add:
                try:
                    m = ChemMol.from_smiles(smi, name=name,
                                            generate_3d=False)
                    m.ensure_properties()
                except Exception as e:
                    log.warning(
                        "Failed to seed intermediate %s (%r): %s",
                        name, smi, e)
                    continue
                s.add(DBMol(
                    name=m.name, smiles=m.smiles,
                    inchi=m.inchi, inchikey=m.inchikey,
                    formula=m.formula,
                    properties_json=json.dumps(m.properties),
                    source=tag,
                ))
                added += 1
        log.info("Seeded %d intermediate molecules.", added)
    else:
        log.info("All %d intermediate entries already seeded.",
                 len(_INTERMEDIATES))

    # ---- One-shot SMILES backfill for known buggy historical rows --
    fixed = 0
    if _SMILES_FIXES:
        from rdkit import Chem as _RDChem
        with session_scope() as s:
            for name, target_smi in _SMILES_FIXES.items():
                row = s.query(DBMol).filter_by(name=name).one_or_none()
                if row is None or not row.smiles:
                    continue
                try:
                    cur_canon = _RDChem.CanonSmiles(row.smiles)
                    tgt_canon = _RDChem.CanonSmiles(target_smi)
                except Exception:
                    continue
                if cur_canon == tgt_canon:
                    continue
                try:
                    m = ChemMol.from_smiles(target_smi, name=name,
                                            generate_3d=False)
                    m.ensure_properties()
                except Exception as e:
                    log.warning(
                        "Failed to backfill SMILES for %s "
                        "(target %r): %s", name, target_smi, e)
                    continue
                row.smiles = m.smiles
                row.inchi = m.inchi
                row.inchikey = m.inchikey
                row.formula = m.formula
                row.properties_json = json.dumps(m.properties)
                fixed += 1
        if fixed:
            log.info(
                "Backfilled SMILES for %d intermediate rows.", fixed)

    return added + fixed
