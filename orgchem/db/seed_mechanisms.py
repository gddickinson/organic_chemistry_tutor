"""Seed textbook mechanisms into the ``Reaction.mechanism_json`` column.

This module is the entry point — it owns the seed logic, the
``SEED_VERSION`` sentinel, and the ``_MECH_MAP`` name-substring →
builder table.  The builders themselves live in three themed
sub-modules so no file exceeds the 500-line cap:

* :mod:`orgchem.db.seed_mechanisms_classic` — SN1/SN2/E1/E2,
  Diels-Alder, aldol, Grignard, Wittig, Michael.
* :mod:`orgchem.db.seed_mechanisms_enzyme`  — chymotrypsin,
  class-I aldolase, HIV protease, RNase A.
* :mod:`orgchem.db.seed_mechanisms_extra`   — Phase 31c expansion
  batch (rounds 59-62): Fischer esterification, NaBH₄ reduction,
  nitration of benzene, Claisen condensation, pinacol rearrangement,
  **bromination of ethene**, **Friedel-Crafts alkylation**.

Atom indices in the builder SMILES were verified against RDKit's
canonical parse order — changing a SMILES here reshuffles indices
silently, so re-verify after any edit.
"""
from __future__ import annotations
import logging

from sqlalchemy import select

from orgchem.db.models import Reaction as DBRxn
from orgchem.db.seed_mechanisms_classic import BUILDERS as _CLASSIC
from orgchem.db.seed_mechanisms_enzyme import (
    BUILDERS as _ENZYME,
    _aldolase_class_I,
    _chymotrypsin,
    _hiv_protease,
    _rnase_a,
)
from orgchem.db.seed_mechanisms_extra import BUILDERS as _EXTRA
from orgchem.db.session import session_scope

# Re-export enzyme builders that existing tests import by name.
__all__ = [
    "SEED_VERSION",
    "seed_mechanisms_if_empty",
    "_MECH_MAP",
    "_aldolase_class_I",
    "_chymotrypsin",
    "_hiv_protease",
    "_rnase_a",
]

log = logging.getLogger(__name__)


# Name-substring → builder function.  Preserves round-by-round
# ordering (classic → enzyme → round-59/60/61 → round-62) so that
# the seed iteration order stays stable.
_MECH_MAP = {**_CLASSIC, **_ENZYME, **_EXTRA}


#: Current mechanism-seed format version. Bump whenever the seed data
#: changes meaningfully (labels, arrow indices, added/removed steps) so
#: stale JSON on existing databases is overwritten on next startup.
SEED_VERSION = 11


def seed_mechanisms_if_empty(force: bool = False) -> int:
    """Attach mechanism JSON to seeded reactions that match a known pattern.

    Overwrites existing JSON if its embedded ``seed_version`` is older than
    :data:`SEED_VERSION` (so users picking up a new app version get the
    fresh mechanisms without a manual migration). Pass ``force=True`` to
    rewrite unconditionally.
    """
    import json as _json
    updated = 0
    with session_scope() as s:
        for name_substr, builder in _MECH_MAP.items():
            stmt = select(DBRxn).where(DBRxn.name.like(f"%{name_substr}%"))
            for row in s.scalars(stmt):
                if row.mechanism_json and not force:
                    try:
                        existing = _json.loads(row.mechanism_json)
                    except Exception:
                        existing = {}
                    if existing.get("seed_version", 0) >= SEED_VERSION:
                        continue
                mech = builder()
                mech.reaction_id = row.id
                payload = mech.to_dict()
                payload["seed_version"] = SEED_VERSION
                row.mechanism_json = _json.dumps(payload, indent=2)
                updated += 1
    log.info("Seeded %d mechanisms (version %d)", updated, SEED_VERSION)
    return updated
