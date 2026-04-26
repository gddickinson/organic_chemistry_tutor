"""Seed the SQLite database with a starter molecule set.

Includes the 15 reference compounds from Verma et al. 2024 (Rasayan J. Chem.
17(4):1460–1472, `refs/4325_pdf.pdf`) so the GUI is immediately useful and
students can reproduce the paper's table 1-click."""
from __future__ import annotations
import json
import logging
from typing import List, Tuple

from orgchem.config import AppConfig
from orgchem.core.molecule import Molecule as ChemMol
from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope
from orgchem.db.queries import count_molecules

log = logging.getLogger(__name__)


# (name, SMILES, source_tag) — tag "reference-set" marks the Verma et al. compounds.
_STARTER: List[Tuple[str, str, str]] = [
    # Foundational basics for the earliest tutorials
    ("Methane",       "C",                       "basics"),
    ("Ethanol",       "CCO",                     "basics"),
    ("Acetic acid",   "CC(=O)O",                 "basics"),
    ("Benzene",       "c1ccccc1",                "basics"),
    ("Water",         "O",                       "basics"),
    # ---- Verma et al. 2024 reference set ----
    ("Nicotine",      "CN1CCCC1c1cccnc1",                                                   "reference-set"),
    ("Caffeine",      "Cn1cnc2n(C)c(=O)n(C)c(=O)c12",                                       "reference-set"),
    ("Efavirenz",     "C#Cc1ccc2c(c1)C(c1cc(Cl)ccc1)(C(F)(F)F)OC(=O)N2",                    "reference-set"),
    ("Sulfasalazine", "OC(=O)c1cc(/N=N/c2ccc(S(=O)(=O)Nc3ccccn3)cc2)ccc1O",                 "reference-set"),
    ("Lycopene",      "CC(=CCCC(C)=CC=CC(C)=CC=CC=C(C)C=CC=C(C)C=CC=C(C)CCC=C(C)C)C",       "reference-set"),
    ("D-Glucose",     "OC[C@H]1OC(O)[C@H](O)[C@@H](O)[C@@H]1O",                             "reference-set"),
    ("beta-Lactose",  "OC[C@H]1O[C@@H](O[C@H]2[C@H](O)[C@@H](O)[C@@H](O)O[C@@H]2CO)[C@H](O)[C@@H](O)[C@@H]1O", "reference-set"),
    ("Coronene",      "c1cc2ccc3ccc4ccc5ccc6ccc1c1c2c3c4c5c61",                             "reference-set"),
    ("Corannulene",   "C1=CC2=CC=C3C=CC4=CC=C5C=CC1=C1C5=C4C3=C21",                         "reference-set"),
    ("Porphyrin",     "c1cc2cc3ccc(cc4ccc(cc5ccc(cc1n2)[nH]5)n4)[nH]3",                     "reference-set"),
    ("Methylene Blue","CN(C)c1ccc2nc3ccc(N(C)C)cc3[s+]c2c1",                                "reference-set"),
    ("Thiamine",      "Cc1ncc(C[n+]2csc(CCO)c2C)c(N)n1",                                    "reference-set"),
    ("Cholesterol",   "C[C@H](CCCC(C)C)[C@H]1CC[C@H]2[C@@H]3CC=C4C[C@@H](O)CC[C@]4(C)[C@H]3CC[C@]12C", "reference-set"),
    ("Codeine",       "COc1ccc2C[C@H]3[C@@H]4C=C[C@@H](O)[C@H]5Oc1c2[C@]45CCN3C",           "reference-set"),
    ("Cocaine",       "COC(=O)[C@H]1[C@@H](OC(=O)c2ccccc2)C[C@@H]2CC[C@H]1N2C",             "reference-set"),
    # ---- +20 content expansion, Phase 6 (2026-04-22) ----
    # Amino acids
    ("Glycine",        "NCC(=O)O",                                                        "amino-acid"),
    ("L-Alanine",      "C[C@@H](N)C(=O)O",                                                "amino-acid"),
    ("L-Phenylalanine","N[C@@H](Cc1ccccc1)C(=O)O",                                        "amino-acid"),
    ("L-Tryptophan",   "N[C@@H](Cc1c[nH]c2ccccc12)C(=O)O",                                "amino-acid"),
    ("L-Cysteine",     "N[C@@H](CS)C(=O)O",                                               "amino-acid"),
    # Drugs
    ("Aspirin",        "CC(=O)Oc1ccccc1C(=O)O",                                           "drug"),
    ("Ibuprofen",      "CC(C)Cc1ccc(cc1)C(C)C(=O)O",                                      "drug"),
    ("Acetaminophen",  "CC(=O)Nc1ccc(O)cc1",                                              "drug"),
    ("Naproxen",       "C[C@H](C(=O)O)c1ccc2cc(OC)ccc2c1",                                "drug"),
    ("Diazepam",       "O=C1CN=C(c2ccccc2)c2cc(Cl)ccc2N1C",                               "drug"),
    # Solvents / reagents
    ("DMSO",           "CS(=O)C",                                                         "solvent"),
    ("DMF",            "O=CN(C)C",                                                        "solvent"),
    ("THF",            "C1CCOC1",                                                         "solvent"),
    ("Diethyl ether",  "CCOCC",                                                           "solvent"),
    ("Acetonitrile",   "CC#N",                                                            "solvent"),
    # Natural products / aromatics
    ("Menthol",        "CC(C)[C@@H]1CC[C@@H](C)C[C@H]1O",                                 "natural-product"),
    ("Camphor",        "CC1(C)[C@@H]2CC[C@]1(C)C(=O)C2",                                  "natural-product"),
    ("Salicylic acid", "OC(=O)c1ccccc1O",                                                 "natural-product"),
    ("Vanillin",       "COc1cc(C=O)ccc1O",                                                "natural-product"),
    ("Capsaicin",      "COc1cc(CNC(=O)CCCC/C=C/C(C)C)ccc1O",                              "natural-product"),
]


def seed_if_empty(cfg: AppConfig) -> int:
    """Populate molecule and reaction tables, additively.

    Molecules present in ``_STARTER`` but missing from the DB are always
    backfilled (matched by name). Existing molecules are left alone so
    user-imported data is never clobbered.
    """
    from orgchem.db.seed_reactions import seed_reactions_if_empty
    from orgchem.db.seed_molecules_extended import seed_extended_molecules
    from orgchem.db.seed_intermediates import seed_intermediates

    mol_added = _seed_molecules_additive()
    mol_added += seed_extended_molecules()
    mol_added += seed_intermediates()
    rxn_added = seed_reactions_if_empty()

    from orgchem.db.seed_mechanisms import seed_mechanisms_if_empty
    mech_added = seed_mechanisms_if_empty()

    from orgchem.db.seed_pathways import seed_pathways_if_empty
    path_added = seed_pathways_if_empty()

    from orgchem.db.seed_energy_profiles import seed_energy_profiles_if_empty
    ep_added = seed_energy_profiles_if_empty()

    from orgchem.db.seed_glossary import seed_glossary_if_empty
    g_added = seed_glossary_if_empty()

    # Phase 6f.2 — persist canonical 2D coords for every molecule so the
    # same layout is reused anywhere it's drawn.
    from orgchem.db.seed_coords import backfill_molblock_2d
    backfill_molblock_2d()

    # Phase 28a — backfill functional-group / size / charge / ring
    # tags on every seeded molecule so the filter-bar query runs fast.
    from orgchem.db.seed_tags import backfill_tags
    backfill_tags()

    # Phase 28b — curated source / drug-class taxonomy for the filter
    # bar's *composition* axis.
    from orgchem.db.seed_source_tags import backfill_source_tags
    backfill_source_tags()

    # Round 58 — common-name synonyms (Retinol ↔ Vitamin A, Aspirin
    # ↔ Acetylsalicylic acid, etc.) + cross-catalogue reconciliation
    # with the Lipids / Carbs / NA Python dataclasses via InChIKey.
    from orgchem.db.seed_synonyms import seed_synonyms_if_needed
    seed_synonyms_if_needed()

    # Round 177 — Phase 49b.  Backfill catalogue molecules
    # (Phase-29 lipid/carb/NA + Phase-31k SAR variants) that
    # aren't already in the molecule DB.  Generalises the
    # round-58 InChIKey reconciliation by ADDING missing rows
    # rather than only adding aliases.
    from orgchem.db.seed_catalogue_molecules import (
        seed_catalogue_molecules_if_needed,
    )
    seed_catalogue_molecules_if_needed()

    return mol_added + rxn_added + mech_added + path_added + ep_added + g_added


def _seed_molecules_additive() -> int:
    """Insert any starter molecule whose name isn't already in the table."""
    with session_scope() as s:
        existing_names = {row.name for row in s.query(DBMol.name).all()}

    if not existing_names:
        log.info("Molecule table is empty — seeding full starter set")
    else:
        missing = [e for e in _STARTER if e[0] not in existing_names]
        if not missing:
            log.info("Molecule table has all %d starter entries", len(_STARTER))
            return 0
        log.info("Backfilling %d missing starter molecules", len(missing))

    added = 0
    to_add = _STARTER if not existing_names else [e for e in _STARTER
                                                   if e[0] not in existing_names]
    with session_scope() as s:
        for name, smi, tag in to_add:
            try:
                m = ChemMol.from_smiles(smi, name=name, generate_3d=False)
                m.ensure_properties()
            except Exception as e:
                log.warning("Failed to seed %s (%r): %s", name, smi, e)
                continue
            s.add(DBMol(
                name=m.name,
                smiles=m.smiles,
                inchi=m.inchi,
                inchikey=m.inchikey,
                formula=m.formula,
                properties_json=json.dumps(m.properties),
                source=tag,
            ))
            added += 1
    log.info("Seeded %d molecules (total in DB now = %d)",
             added, len(existing_names) + added)
    return added
