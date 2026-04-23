"""Backfill ``Molecule.molblock_2d`` on every DB row — Phase 6f.2.

The ORM column has existed from the start but was never populated for
seeded molecules. This job walks the table, computes canonical 2D
coordinates with `rdDepictor.SetPreferCoordGen(True)` + `Compute2DCoords`,
and writes the MolBlock back. Idempotent — existing molblocks are left
alone unless ``force=True``.
"""
from __future__ import annotations
import logging

from rdkit import Chem
from rdkit.Chem import rdDepictor

from orgchem.db.models import Molecule as DBMol
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

def backfill_molblock_2d(force: bool = False) -> int:
    """Populate ``molblock_2d`` on DB molecules. Returns rows updated.

    Uses CoordGen for layout, but flips the preference back after
    processing so the flag isn't sticky across modules. (Leaving it
    globally ON used to cause test-order-dependent drift in the
    `test_golden_renders` baselines — see round-52 fix.)
    """
    updated = 0
    # Flip-and-restore keeps the global CoordGen preference from
    # leaking into other renderers / tests after this job runs.
    try:
        rdDepictor.SetPreferCoordGen(True)
    except Exception:  # noqa: BLE001
        pass
    with session_scope() as s:
        for row in s.query(DBMol).all():
            if row.molblock_2d and not force:
                continue
            if not row.smiles:
                continue
            mol = Chem.MolFromSmiles(row.smiles)
            if mol is None:
                continue
            try:
                rdDepictor.Compute2DCoords(mol)
            except Exception as e:
                log.warning("Compute2DCoords failed for %s: %s", row.name, e)
                continue
            row.molblock_2d = Chem.MolToMolBlock(mol)
            updated += 1
    # Restore the default depictor preference so the flag isn't
    # sticky for later RDKit renders in the same process.
    try:
        rdDepictor.SetPreferCoordGen(False)
    except Exception:  # noqa: BLE001
        pass
    if updated:
        log.info("Backfilled molblock_2d on %d molecules.", updated)
    return updated
