"""Extended molecule seed — Phase 6a content expansion (target 200+).

This module contributes the **additional** seeded molecules beyond the 40
in `seed.py`. Kept separate so `seed.py` stays small and manageable.

All SMILES are canonical / taken from PubChem. Each row is additively
inserted by name: if a molecule with the same name is already present the
row is skipped, so re-running seed on an existing DB never duplicates.

Categories (for source tagging + future filtering):

- ``amino-acid``           — the canonical 20 (15 added here)
- ``reagent``              — named laboratory reagents
- ``drug``                 — pharmaceutical molecules
- ``biomolecule``          — sugars, nucleosides, fatty acids, etc.
- ``dye``                  — organic dyes and stains
- ``pah``                  — polycyclic aromatic hydrocarbons
- ``heterocycle``          — aromatic / saturated N, O, S heterocycles
- ``alkane`` / ``alkene``  — functional-group ladder entries
- ``alcohol`` / ``aldehyde`` / ``ketone`` / ``acid`` / ``amine``
"""
from __future__ import annotations
import json
import logging
from typing import List, Tuple

from orgchem.core.molecule import Molecule as ChemMol
from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)


# (name, SMILES, source-tag)
_EXTENDED: List[Tuple[str, str, str]] = [
    # ------------------------------------------------------------------
    # Remaining 15 canonical amino acids (5 seeded already: Glycine,
    # L-Alanine, L-Phenylalanine, L-Tryptophan, L-Cysteine).
    ("L-Valine",        "CC(C)[C@@H](N)C(=O)O",                       "amino-acid"),
    ("L-Leucine",       "CC(C)C[C@@H](N)C(=O)O",                      "amino-acid"),
    ("L-Isoleucine",    "CC[C@H](C)[C@@H](N)C(=O)O",                  "amino-acid"),
    ("L-Methionine",    "CSCC[C@@H](N)C(=O)O",                        "amino-acid"),
    ("L-Proline",       "O=C(O)[C@@H]1CCCN1",                         "amino-acid"),
    ("L-Serine",        "OC[C@@H](N)C(=O)O",                          "amino-acid"),
    ("L-Threonine",     "C[C@H](O)[C@@H](N)C(=O)O",                   "amino-acid"),
    ("L-Asparagine",    "NC(=O)C[C@@H](N)C(=O)O",                     "amino-acid"),
    ("L-Glutamine",     "NC(=O)CC[C@@H](N)C(=O)O",                    "amino-acid"),
    ("L-Aspartic acid", "OC(=O)C[C@@H](N)C(=O)O",                     "amino-acid"),
    ("L-Glutamic acid", "OC(=O)CC[C@@H](N)C(=O)O",                    "amino-acid"),
    ("L-Lysine",        "NCCCC[C@@H](N)C(=O)O",                       "amino-acid"),
    ("L-Arginine",      "NC(=N)NCCC[C@@H](N)C(=O)O",                  "amino-acid"),
    ("L-Histidine",     "O=C(O)[C@@H](N)Cc1cnc[nH]1",                 "amino-acid"),
    ("L-Tyrosine",      "N[C@@H](Cc1ccc(O)cc1)C(=O)O",                "amino-acid"),

    # ------------------------------------------------------------------
    # Named reagents / bases / protecting-group chemistry
    ("LDA",              "CC(C)[N-]C(C)C.[Li+]",                      "reagent"),
    ("Lithium aluminium hydride", "[Li+].[Al-]([H])([H])([H])[H]",    "reagent"),
    ("Sodium borohydride","[B-]([H])([H])([H])[H].[Na+]",             "reagent"),
    ("Sodium hydride",   "[H-].[Na+]",                                "reagent"),
    ("DBU",              "C1CCC2=NCCCN2CC1",                          "reagent"),
    ("DIPEA",            "CCN(C(C)C)C(C)C",                           "reagent"),
    ("TBS chloride",     "CC(C)(C)[Si](C)(C)Cl",                      "reagent"),
    ("mCPBA",            "OOC(=O)c1cccc(Cl)c1",                       "reagent"),
    ("Boc anhydride",    "CC(C)(C)OC(=O)OC(=O)OC(C)(C)C",             "reagent"),
    ("Cbz chloride",     "O=C(Cl)OCc1ccccc1",                         "reagent"),
    ("Dess-Martin periodinane",
        "CC(=O)OI1(OC(C)=O)(OC(C)=O)OC(=O)c2ccccc21",                 "reagent"),
    ("Tosyl chloride",   "O=S(=O)(Cl)c1ccc(C)cc1",                    "reagent"),
    ("Mesyl chloride",   "CS(=O)(=O)Cl",                              "reagent"),
    ("Sodium methoxide", "[Na+].[O-]C",                               "reagent"),
    ("Potassium tert-butoxide", "CC(C)(C)[O-].[K+]",                  "reagent"),
    ("TMS chloride",     "C[Si](C)(C)Cl",                             "reagent"),
    ("Acetic anhydride", "CC(=O)OC(C)=O",                             "reagent"),
    ("Benzoyl chloride", "O=C(Cl)c1ccccc1",                           "reagent"),
    ("NBS",              "O=C1CCC(=O)N1Br",                           "reagent"),
    ("Oxalyl chloride",  "O=C(Cl)C(=O)Cl",                            "reagent"),

    # ------------------------------------------------------------------
    # Drug library expansion (beyond the 5 already seeded).
    ("Penicillin G",
        "CC1(C)S[C@@H]2[C@H](NC(=O)Cc3ccccc3)C(=O)N2[C@H]1C(=O)O",    "drug"),
    ("Amoxicillin",
        "CC1(C)S[C@@H]2[C@H](NC(=O)[C@@H](N)c3ccc(O)cc3)C(=O)N2[C@H]1C(=O)O",
                                                                       "drug"),
    ("Oseltamivir",
        "CCOC(=O)C1=C[C@H](OC(CC)CC)[C@@H](NC(C)=O)[C@H](N)C1",       "drug"),
    ("Acyclovir",
        "Nc1nc2n(COCCO)cnc2c(=O)[nH]1",                               "drug"),
    ("Fluoxetine",
        "CNCCC(Oc1ccc(C(F)(F)F)cc1)c1ccccc1",                         "drug"),
    ("Citalopram",
        "CN(C)CCCC1(c2ccc(F)cc2)OCc2cc(C#N)ccc21",                    "drug"),
    ("Atorvastatin",
        "CC(C)c1c(C(=O)Nc2ccccc2)c(-c2ccccc2)c(-c2ccc(F)cc2)n1CC[C@@H](O)C[C@@H](O)CC(=O)O",
                                                                       "drug"),
    ("Simvastatin",
        "CCC(C)(C)C(=O)O[C@@H]1C[C@@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@@H]12",
                                                                       "drug"),
    ("Lovastatin",
        "CC[C@@H](C)C(=O)O[C@@H]1C[C@@H](C)C=C2C=C[C@@H](C)[C@H](CC[C@@H]3C[C@H](O)CC(=O)O3)[C@@H]12",
                                                                       "drug"),
    ("Propranolol",      "CC(C)NCC(O)COc1cccc2ccccc12",               "drug"),
    ("Metformin",        "CN(C)C(=N)N=C(N)N",                         "drug"),
    ("Warfarin",         "CC(=O)CC(c1ccccc1)C1=C(O)c2ccccc2OC1=O",    "drug"),
    ("Omeprazole",
        "CC1=CN=C(CS(=O)C2=NC3=CC(OC)=CC=C3N2)C(C)=C1OC",             "drug"),
    ("Sildenafil",
        "CCCc1nn(C)c2c1nc([nH]c2=O)-c1cc(S(=O)(=O)N2CCN(C)CC2)ccc1OCC","drug"),
    ("Captopril",        "SC[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O",         "drug"),
    ("Enalapril",
        "CCOC(=O)[C@@H](CCc1ccccc1)N[C@@H](C)C(=O)N1CCC[C@H]1C(=O)O", "drug"),
    ("Losartan",
        "CCCCc1nc(Cl)c(CO)n1Cc1ccc(-c2ccccc2-c2nnn[nH]2)cc1",         "drug"),
    ("Morphine",
        "CN1CC[C@]23c4c5ccc(O)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5",   "drug"),
    ("Diphenhydramine",  "CN(C)CCOC(c1ccccc1)c1ccccc1",               "drug"),
    ("Lidocaine",        "CCN(CC)CC(=O)Nc1c(C)cccc1C",                "drug"),
    ("Atropine",
        "CN1[C@@H]2CC[C@H]1C[C@H](C2)OC(=O)C(CO)c1ccccc1",            "drug"),
    ("Quinine",
        "C=C[C@H]1CN2CCC1C[C@H]2[C@@H](O)c1ccnc2ccc(OC)cc12",         "drug"),
    ("Dopamine",         "NCCc1ccc(O)c(O)c1",                         "drug"),

    # ------------------------------------------------------------------
    # Biomolecules: nucleosides, sugars, fatty acids, peptides, steroids.
    ("Adenosine",
        "Nc1ncnc2c1ncn2[C@@H]1O[C@H](CO)[C@@H](O)[C@H]1O",            "biomolecule"),
    ("Guanosine",
        "Nc1nc2c(ncn2[C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)[nH]1",   "biomolecule"),
    ("Thymidine",
        "Cc1cn([C@H]2C[C@H](O)[C@@H](CO)O2)c(=O)[nH]c1=O",            "biomolecule"),
    ("Cytidine",
        "Nc1ccn([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)c(=O)n1",           "biomolecule"),
    ("Uridine",
        "O=c1[nH]c(=O)n([C@@H]2O[C@H](CO)[C@@H](O)[C@H]2O)cc1",       "biomolecule"),
    ("D-Ribose",         "OC[C@H]1O[C@H](O)[C@H](O)[C@@H]1O",         "biomolecule"),
    ("D-Fructose",
        "OC[C@H]1O[C@](O)(CO)[C@@H](O)[C@@H]1O",                      "biomolecule"),
    ("Sucrose",
        "OC[C@H]1O[C@@H](O[C@]2(CO)O[C@H](CO)[C@@H](O)[C@@H]2O)[C@H](O)[C@@H](O)[C@@H]1O",
                                                                       "biomolecule"),
    ("Maltose",
        "OC[C@H]1O[C@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O",
                                                                       "biomolecule"),
    ("Palmitic acid",    "CCCCCCCCCCCCCCCC(=O)O",                     "biomolecule"),
    ("Oleic acid",       "CCCCCCCC/C=C\\CCCCCCCC(=O)O",               "biomolecule"),
    ("Arachidonic acid",
        "CCCCC/C=C\\C/C=C\\C/C=C\\C/C=C\\CCCC(=O)O",                  "biomolecule"),
    ("Glutathione",
        "N[C@@H](CCC(=O)N[C@@H](CS)C(=O)NCC(=O)O)C(=O)O",             "biomolecule"),
    ("Testosterone",
        "C[C@]12CC[C@H]3[C@@H](CCC4=CC(=O)CC[C@@]34C)[C@@H]1CC[C@@H]2O",
                                                                       "biomolecule"),
    ("Estradiol",
        "C[C@]12CCC3c4ccc(O)cc4CC[C@H]3[C@@H]1CC[C@@H]2O",            "biomolecule"),

    # ------------------------------------------------------------------
    # Dyes & stains (subset; complex ones skipped).
    ("Indigo",
        "O=C1/C(=C2\\Nc3ccccc3C2=O)Nc2ccccc21",                       "dye"),
    ("Methyl orange",
        "CN(C)c1ccc(/N=N/c2ccc(S(=O)(=O)[O-])cc2)cc1.[Na+]",          "dye"),
    ("Phenolphthalein",
        "OC1=CC=C(C2(c3ccc(O)cc3)OC(=O)c3ccccc32)C=C1",               "dye"),
    ("Crystal violet",
        "CN(C)c1ccc(C(=C2C=CC(=[N+](C)C)C=C2)c2ccc(N(C)C)cc2)cc1",    "dye"),
    ("Malachite green",
        "CN(C)c1ccc(C(=C2C=CC(=[N+](C)C)C=C2)c2ccccc2)cc1",           "dye"),
    ("Fluorescein",
        "OC(=O)c1ccccc1-c1c2ccc(=O)cc-2oc2cc(O)ccc12",                "dye"),
    ("Rhodamine B",
        "CCN(CC)c1ccc2c(-c3ccccc3C(=O)O)c3ccc(=[N+](CC)CC)cc-3oc2c1", "dye"),
    ("Eosin Y",
        "[O-]C(=O)c1ccccc1-c1c2cc(Br)c(=O)c(Br)c2oc2c(Br)c([O-])c(Br)cc12.[Na+].[Na+]",
                                                                       "dye"),

    # ------------------------------------------------------------------
    # Polycyclic aromatic hydrocarbons (beyond the 2 seeded).
    ("Naphthalene",      "c1ccc2ccccc2c1",                            "pah"),
    ("Anthracene",       "c1ccc2cc3ccccc3cc2c1",                      "pah"),
    ("Phenanthrene",     "c1ccc2ccc3ccccc3c2c1",                      "pah"),
    ("Pyrene",           "c1cc2ccc3cccc4ccc(c1)c2c34",                "pah"),
    ("Chrysene",         "c1ccc2c(c1)ccc1ccc3ccccc3c12",              "pah"),
    ("Triphenylene",     "c1ccc2c(c1)c1ccccc1c1ccccc21",              "pah"),
    ("Fluorene",         "c1ccc2c(c1)Cc1ccccc1-2",                    "pah"),
    ("Biphenyl",         "c1ccc(-c2ccccc2)cc1",                       "pah"),
    ("Perylene",         "c1cc2cccc3c2c(c1)-c1cccc2cccc-3c12",        "pah"),
    ("Acenaphthylene",   "C1=Cc2cccc3cccc1c23",                       "pah"),

    # ------------------------------------------------------------------
    # Heterocycles / functional exemplars.
    ("Pyridine",         "c1ccncc1",                                  "heterocycle"),
    ("Pyrrole",          "c1cc[nH]c1",                                "heterocycle"),
    ("Furan",            "c1ccoc1",                                   "heterocycle"),
    ("Thiophene",        "c1ccsc1",                                   "heterocycle"),
    ("Imidazole",        "c1cnc[nH]1",                                "heterocycle"),
    ("Pyrazole",         "c1cc[nH]n1",                                "heterocycle"),
    ("Oxazole",          "c1ocnc1",                                   "heterocycle"),
    ("Thiazole",         "c1scnc1",                                   "heterocycle"),
    ("1,2,3-Triazole",   "c1cn[nH]n1",                                "heterocycle"),
    ("1,2,4-Triazole",   "c1ncn[nH]1",                                "heterocycle"),
    ("Pyrimidine",       "c1cncnc1",                                  "heterocycle"),
    ("Pyrazine",         "c1cnccn1",                                  "heterocycle"),
    ("Piperidine",       "C1CCNCC1",                                  "heterocycle"),
    ("Morpholine",       "C1COCCN1",                                  "heterocycle"),
    ("Piperazine",       "C1CNCCN1",                                  "heterocycle"),
    ("Indole",           "c1ccc2[nH]ccc2c1",                          "heterocycle"),
    ("Quinoline",        "c1ccc2ncccc2c1",                            "heterocycle"),
    ("Isoquinoline",     "c1ccc2cnccc2c1",                            "heterocycle"),
    ("Purine",           "c1ncc2[nH]cnc2n1",                          "heterocycle"),
    ("Benzofuran",       "c1ccc2occc2c1",                             "heterocycle"),
    ("Benzothiophene",   "c1ccc2sccc2c1",                             "heterocycle"),

    # Ethers / epoxides
    ("Dimethyl ether",   "COC",                                       "ether"),
    ("1,4-Dioxane",      "C1COCCO1",                                  "ether"),
    ("Dimethoxyethane",  "COCCOC",                                    "ether"),
    ("Ethylene oxide",   "C1CO1",                                     "epoxide"),
    ("Propylene oxide",  "CC1CO1",                                    "epoxide"),
    ("Styrene oxide",    "C1OC1c1ccccc1",                             "epoxide"),
    ("Aziridine",        "C1CN1",                                     "heterocycle"),

    # ------------------------------------------------------------------
    # Functional-group ladder — alkanes, alkenes, alcohols, ketones,
    # aldehydes, acids, amines of the same backbone lengths so students
    # can flip through and watch property / name changes.
    ("Propane",          "CCC",                                       "alkane"),
    ("Butane",           "CCCC",                                      "alkane"),
    ("Pentane",          "CCCCC",                                     "alkane"),
    ("Hexane",           "CCCCCC",                                    "alkane"),
    ("Heptane",          "CCCCCCC",                                   "alkane"),
    ("Octane",           "CCCCCCCC",                                  "alkane"),
    ("Cyclopropane",     "C1CC1",                                     "alkane"),
    ("Cyclobutane",      "C1CCC1",                                    "alkane"),
    ("Cyclopentane",     "C1CCCC1",                                   "alkane"),
    ("Cyclohexane",      "C1CCCCC1",                                  "alkane"),

    ("Ethylene",         "C=C",                                       "alkene"),
    ("Propylene",        "CC=C",                                      "alkene"),
    ("1-Butene",         "CCC=C",                                     "alkene"),
    ("trans-2-Butene",   "C/C=C/C",                                   "alkene"),
    ("cis-2-Butene",     "C/C=C\\C",                                  "alkene"),
    ("Isobutylene",      "CC(=C)C",                                   "alkene"),
    ("1,3-Butadiene",    "C=CC=C",                                    "alkene"),

    ("Acetylene",        "C#C",                                       "alkyne"),
    ("Propyne",          "CC#C",                                      "alkyne"),
    ("1-Butyne",         "CCC#C",                                     "alkyne"),

    ("Methanol",         "CO",                                        "alcohol"),
    ("Propan-1-ol",      "CCCO",                                      "alcohol"),
    ("Propan-2-ol",      "CC(C)O",                                    "alcohol"),
    ("Butan-1-ol",       "CCCCO",                                     "alcohol"),
    ("tert-Butanol",     "CC(C)(C)O",                                 "alcohol"),
    ("Phenol",           "Oc1ccccc1",                                 "alcohol"),

    ("Acetone",          "CC(=O)C",                                   "ketone"),
    ("2-Butanone",       "CCC(=O)C",                                  "ketone"),
    ("Cyclohexanone",    "O=C1CCCCC1",                                "ketone"),
    ("Acetophenone",     "CC(=O)c1ccccc1",                            "ketone"),

    ("Formaldehyde",     "C=O",                                       "aldehyde"),
    ("Acetaldehyde",     "CC=O",                                      "aldehyde"),
    ("Propanal",         "CCC=O",                                     "aldehyde"),
    ("Benzaldehyde",     "O=Cc1ccccc1",                               "aldehyde"),

    ("Formic acid",      "OC=O",                                      "acid"),
    ("Propanoic acid",   "CCC(=O)O",                                  "acid"),
    ("Butanoic acid",    "CCCC(=O)O",                                 "acid"),
    ("Benzoic acid",     "OC(=O)c1ccccc1",                            "acid"),
    ("Oxalic acid",      "OC(=O)C(=O)O",                              "acid"),

    ("Methyl acetate",   "COC(=O)C",                                  "ester"),
    ("Ethyl acetate",    "CCOC(=O)C",                                 "ester"),
    ("Methyl benzoate",  "COC(=O)c1ccccc1",                           "ester"),

    ("Methylamine",      "CN",                                        "amine"),
    ("Ethylamine",       "CCN",                                       "amine"),
    ("Dimethylamine",    "CNC",                                       "amine"),
    ("Trimethylamine",   "CN(C)C",                                    "amine"),
    ("Aniline",          "Nc1ccccc1",                                 "amine"),

    ("Formamide",        "NC=O",                                      "amide"),
    ("Acetamide",        "CC(=O)N",                                   "amide"),
    ("Urea",             "NC(=O)N",                                   "amide"),

    # ---- Phase 31a content expansion (2026-04-23) ---------------------
    # Terpenes — monoterpenes + sesquiterpene + diterpene skeletons
    ("α-Pinene",         "CC1=CC[C@@H]2CC1[C@]2(C)C",                 "terpene"),
    ("β-Pinene",         "C=C1CC[C@H]2CC1[C@@]2(C)C",                 "terpene"),
    ("Limonene",         "CC(=C)[C@@H]1CC=C(C)CC1",                   "terpene"),
    ("Myrcene",          "CC(=CCCC(=C)C=C)C",                         "terpene"),
    ("Camphor",          "CC1(C)[C@@H]2CC[C@]1(C)C(=O)C2",            "terpene"),
    ("Menthol",          "CC(C)[C@@H]1CC[C@@H](C)C[C@H]1O",           "terpene"),
    ("Geraniol",         "CC(=CCC/C(C)=C/CO)C",                       "terpene"),
    ("Farnesol",         "CC(=CCC/C(C)=C/CC/C(C)=C/CO)C",             "terpene"),
    # Macrocycles — crown ethers + porphyrin (free base)
    ("18-Crown-6",       "O1CCOCCOCCOCCOCCOCC1",                      "macrocycle"),
    ("15-Crown-5",       "O1CCOCCOCCOCCOCC1",                         "macrocycle"),
    ("Porphine (free-base porphyrin)",
        "C1=CC2=CC3=CC=C(N3)C=C4C=CC(=N4)C=C5C=CC(=N5)C=C1N2",        "macrocycle"),
    # Polymers / monomers
    ("Styrene",          "C=Cc1ccccc1",                               "monomer"),
    ("Vinyl chloride",   "C=CCl",                                     "monomer"),
    ("Ethylene glycol",  "OCCO",                                      "monomer"),
    ("Bisphenol-A",      "CC(C)(c1ccc(O)cc1)c1ccc(O)cc1",             "monomer"),
    ("Caprolactam",      "O=C1CCCCCN1",                               "monomer"),
    # Agrochemicals
    ("Glyphosate",       "OC(=O)CNCP(=O)(O)O",                        "agrochemical"),
    ("Atrazine",         "CCNc1nc(Cl)nc(NC(C)C)n1",                   "agrochemical"),
    ("DDT",              "ClC(Cl)(Cl)C(c1ccc(Cl)cc1)c1ccc(Cl)cc1",    "agrochemical"),
    # Common solvents and simple dye — fills gaps in the solvent catalogue
    ("Glycerol",         "OCC(O)CO",                                  "solvent"),
    ("HMPA (hexamethylphosphoramide)",
        "CN(C)P(=O)(N(C)C)N(C)C",                                     "solvent"),
    ("Diglyme (diethylene glycol dimethyl ether)",
        "COCCOCCOC",                                                  "solvent"),
    ("Indigo",           "O=C1/C(=C2/C(=O)c3ccccc3N2)Nc2ccccc21",     "dye"),
    ("Methylene blue",
        "CN(C)c1ccc2nc3ccc(N(C)C)cc3[s+]c2c1",                        "dye"),
]


def seed_extended_molecules() -> int:
    """Insert any extended molecule whose name isn't already in the table.

    Mirrors the additive-backfill logic in ``seed.py``: safe to re-run on
    an existing DB; skips anything already seeded by name.
    """
    with session_scope() as s:
        existing_names = {row.name for row in s.query(DBMol.name).all()}

    to_add = [e for e in _EXTENDED if e[0] not in existing_names]
    if not to_add:
        log.info("Extended molecule set already fully seeded (%d entries).",
                 len(_EXTENDED))
        return 0

    log.info("Seeding %d extended molecules.", len(to_add))
    added = 0
    with session_scope() as s:
        for name, smi, tag in to_add:
            try:
                m = ChemMol.from_smiles(smi, name=name, generate_3d=False)
                m.ensure_properties()
            except Exception as e:
                log.warning("Failed to seed extended %s (%r): %s", name, smi, e)
                continue
            s.add(DBMol(
                name=m.name, smiles=m.smiles,
                inchi=m.inchi, inchikey=m.inchikey, formula=m.formula,
                properties_json=json.dumps(m.properties), source=tag,
            ))
            added += 1
    log.info("Seeded %d extended molecules.", added)
    return added
