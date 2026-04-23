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
    ("trans-Stilbene",           "C(/c1ccccc1)=C/c1ccccc1",            "intermediate"),
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
]


def seed_intermediates() -> int:
    """Additively insert intermediate molecules by name.

    Mirrors the additive-backfill logic in ``seed.py``: re-running on an
    existing DB is safe; pre-existing molecules (by name) are untouched.
    """
    with session_scope() as s:
        existing_names = {row.name for row in s.query(DBMol.name).all()}

    to_add = [e for e in _INTERMEDIATES if e[0] not in existing_names]
    if not to_add:
        log.info("All %d intermediate entries already seeded.", len(_INTERMEDIATES))
        return 0

    log.info("Seeding %d intermediate molecules.", len(to_add))
    added = 0
    with session_scope() as s:
        for name, smi, tag in to_add:
            try:
                m = ChemMol.from_smiles(smi, name=name, generate_3d=False)
                m.ensure_properties()
            except Exception as e:
                log.warning("Failed to seed intermediate %s (%r): %s",
                            name, smi, e)
                continue
            s.add(DBMol(
                name=m.name, smiles=m.smiles,
                inchi=m.inchi, inchikey=m.inchikey, formula=m.formula,
                properties_json=json.dumps(m.properties), source=tag,
            ))
            added += 1
    log.info("Seeded %d intermediate molecules.", added)
    return added
