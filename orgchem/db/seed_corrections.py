"""Correct seeded molecule rows whose structure was wrong in an earlier release.

Seeding is additive by name, so a DB created before a seed SMILES was fixed keeps the old structure forever. This
module rewrites those rows in place (matched by the InChIKey of the old, wrong SMILES, so user-edited rows are left
alone), then clears the cached 2D/3D molblocks so ``seed_coords.backfill_molblock_2d`` redraws them.

Current corrections (2026-11-12): Camphor, Codeine and Oxycodone carried stereo descriptors no 3D geometry can
satisfy (no 3D model could be built). Replacement SMILES come from their PubChem records (CIDs below).
Idempotent: once corrected, the old InChIKeys no longer match anything.
"""
from __future__ import annotations

import json
import logging
from typing import List, Tuple

from orgchem.core.molecule import Molecule as ChemMol
from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

# (InChIKey of the old wrong seed SMILES, corrected isomeric SMILES, source record)
CORRECTIONS: List[Tuple[str, str, str]] = [
    ("DSSYKIVIOFKYAU-GMSGAONNSA-N", "CC1(C)[C@@H]2CC[C@@]1(C)C(=O)C2",
     "(+)-camphor (1R,4R), PubChem CID 159055, ChEBI:15396"),
    ("OROGSEYTTFOCAN-HKAKVCCISA-N", "CN1CC[C@]23c4c5ccc(OC)c4O[C@H]2[C@@H](O)C=C[C@H]3[C@H]1C5",
     "codeine, PubChem CID 5284371, ChEBI:16714"),
    ("BRUQQQPBMZOVGD-BVPBIZIASA-N", "CN1CC[C@]23c4c5ccc(OC)c4O[C@H]2C(=O)CC[C@@]3(O)[C@H]1C5",
     "oxycodone, PubChem CID 5284603, ChEBI:7852"),
]


def apply_seed_corrections() -> int:
    """Rewrite rows still holding a known-wrong seed structure. Returns the number of rows corrected."""
    fixed = 0
    with session_scope() as s:
        for old_key, smiles, source in CORRECTIONS:
            rows = s.query(DBMol).filter(DBMol.inchikey == old_key).all()
            if not rows:
                continue
            m = ChemMol.from_smiles(smiles, generate_3d=False)
            m.ensure_properties()
            for row in rows:
                row.smiles, row.inchi, row.inchikey, row.formula = m.smiles, m.inchi, m.inchikey, m.formula
                row.properties_json = json.dumps(m.properties)
                row.molblock_2d = None
                row.molblock_3d = None
                fixed += 1
                log.info("Corrected seeded structure of %s (%s)", row.name, source)
    return fixed
