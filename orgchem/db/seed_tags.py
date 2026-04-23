"""Phase 28a backfill: write auto-tags into the new columns on every
seeded molecule.

Called automatically from :func:`seed_if_empty` — one-shot and
idempotent. Rows whose tags are already populated are skipped unless
``force=True``. No-op for molecules with invalid SMILES.
"""
from __future__ import annotations
import json
import logging
from typing import Optional

from sqlalchemy import select

from orgchem.core.molecule_tags import auto_tag
from orgchem.db.models import Molecule
from orgchem.db.session import session_scope

log = logging.getLogger(__name__)

#: Bump when the tag-format changes so existing DBs re-backfill on
#: next launch instead of keeping stale tags. The version is embedded
#: at the end of each row's JSON as a trailing token so a simple
#: substring check can spot old payloads.
SEED_VERSION = 2


def _is_current_version(payload: str) -> bool:
    tag = f'"__v{SEED_VERSION}__"'
    return tag in (payload or "")


def backfill_tags(force: bool = False) -> int:
    """Populate the Phase 28a tag columns on every molecule row.

    Returns the number of rows updated.
    """
    updated = 0
    with session_scope() as s:
        rows = list(s.scalars(select(Molecule)).all())
        for row in rows:
            if (not force
                    and row.functional_group_tags_json
                    and _is_current_version(
                        row.functional_group_tags_json)):
                continue       # already tagged at current version
            if not row.smiles:
                continue
            try:
                tags = auto_tag(row.smiles)
            except Exception as e:  # noqa: BLE001
                log.warning("auto_tag failed for %s: %s", row.name, e)
                continue
            # Functional groups + composition flags + zwitterion
            # marker all live in the same JSON string so the
            # filter-query can substring-match any of them.
            auto_tokens = list(tags.functional_groups) + list(
                tags.composition_flags)
            if tags.charge_category == "zwitterion":
                auto_tokens.append("zwitterion")
            # Version marker — last token lets `_is_current_version`
            # detect stale payloads next time round.
            auto_tokens.append(f"__v{SEED_VERSION}__")
            row.functional_group_tags_json = json.dumps(auto_tokens)
            # source_tags are preserved — they come from the seed
            # files or user edits, not from auto-tagging. Initialise
            # to an empty list when missing.
            if not row.source_tags_json:
                row.source_tags_json = json.dumps([])
            row.heavy_atom_count = tags.heavy_atom_count
            row.formal_charge = tags.formal_charge
            row.n_rings = tags.n_rings
            row.has_stereo = tags.has_stereo
            updated += 1
    if updated:
        log.info("Phase 28a backfill: tagged %d molecule(s)", updated)
    return updated
