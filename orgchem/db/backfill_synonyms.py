"""Phase 35c (round 120) — bulk PubChem synonym backfill.

Walks every ``Molecule`` row whose ``synonyms_json`` is empty (or
below a caller-supplied threshold), queries PubChem by InChIKey
via the round-113 helper, filters the returned strings through
the round-109 registry-ID regex so only natural-language names
survive, and writes the merged list back to the DB.

Network-heavy + rate-limited — at the default 200 ms/request
pacing the full ~415-molecule catalogue takes ~85 s.  Designed
to be invoked as a one-shot utility via
``scripts/backfill_molecule_synonyms.py``, **not** from
``seed_if_empty``: it does network I/O every launch and that's
the wrong place for it.

Safe properties:

- Idempotent — re-running after new imports only hits the rows
  that still have empty synonyms.
- Pollution-safe — ``Tutor-test…`` rows are skipped outright.
- Best-effort — any per-row failure (HTTP error, no hit, InChI
  missing) logs and moves on; the overall run never aborts.
- Dependency-gated — if ``pubchempy`` isn't installed the helper
  returns zero and the run exits with a counts of zero fetched.
"""
from __future__ import annotations

import json
import logging
import time
from dataclasses import dataclass
from typing import List, Optional

log = logging.getLogger(__name__)


#: Rate-limiter default: 5 requests / sec is PubChem's free-tier
#: ceiling.  200 ms/req stays comfortably below it.
DEFAULT_REQUEST_INTERVAL_S = 0.2


@dataclass
class BackfillCounts:
    inspected: int = 0      # rows considered
    queried: int = 0        # rows where a PubChem request was made
    fetched: int = 0        # rows where ≥1 synonym was added
    skipped_tutor: int = 0  # rows whose name starts with Tutor-test
    skipped_no_key: int = 0  # rows without an InChIKey (can't query)
    added_total: int = 0    # total synonym strings appended

    def total(self) -> int:
        return self.added_total

    def __str__(self) -> str:
        return (f"BackfillCounts(inspected={self.inspected}, "
                f"queried={self.queried}, fetched={self.fetched}, "
                f"skipped_tutor={self.skipped_tutor}, "
                f"skipped_no_key={self.skipped_no_key}, "
                f"added_total={self.added_total})")


def backfill_synonyms(
    *,
    limit: Optional[int] = None,
    rate_delay_s: float = DEFAULT_REQUEST_INTERVAL_S,
    min_existing: int = 1,
    fetch_fn=None,
    skip_test_prefix: bool = True,
) -> BackfillCounts:
    """Populate ``Molecule.synonyms_json`` across the seeded DB.

    Parameters
    ----------
    limit:
        Cap on the number of rows actually queried against PubChem
        (use for a dry-run-ish probe or to stay under a per-session
        network budget).  ``None`` means no cap.
    rate_delay_s:
        Seconds to sleep *between* PubChem requests.  Set to 0 to
        disable the rate-limiter (e.g. in tests with mocked
        network).
    min_existing:
        Rows whose existing synonym count is **≥ this** are skipped
        as already-filled.  Default 1 — any existing synonym counts
        as filled.  Set to 0 to force a refresh of every row.
    fetch_fn:
        Test-injectable stand-in for
        :func:`orgchem.sources.pubchem.fetch_synonyms_by_inchikey`.
        Signature ``(inchikey: str) -> list[str]``.  Useful so
        tests can avoid network calls entirely.

    Returns
    -------
    BackfillCounts
        Per-category tallies suitable for log lines or CLI output.
    """
    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.session import session_scope

    if fetch_fn is None:
        from orgchem.sources.pubchem import fetch_synonyms_by_inchikey
        fetch_fn = fetch_synonyms_by_inchikey

    # Registry-ID filter lives in the palette module; the helper is
    # pure-regex so it's safe to pull into a DB-layer path too.
    from orgchem.gui.dialogs.command_palette import (
        _looks_like_registry_id,
    )

    counts = BackfillCounts()
    queried_budget = limit if limit is not None else float("inf")

    with session_scope() as s:
        rows: List[DBMol] = s.query(DBMol).all()
        for row in rows:
            counts.inspected += 1
            # Pollution guard — default ON.  Tests opt out by
            # passing `skip_test_prefix=False` so they can target
            # the Tutor-test rows they just inserted.
            if skip_test_prefix and row.name \
                    and row.name.startswith("Tutor-test"):
                counts.skipped_tutor += 1
                continue
            # Existing-synonym threshold.
            try:
                existing = (json.loads(row.synonyms_json)
                            if row.synonyms_json else [])
            except Exception:  # noqa: BLE001
                existing = []
            # `min_existing=0` means "don't skip on existing-
            # synonym count — refresh every row".
            if min_existing > 0 and len(existing) >= min_existing:
                continue
            # InChIKey presence gate.
            key = (row.inchikey or "").strip()
            if not key:
                counts.skipped_no_key += 1
                continue
            if counts.queried >= queried_budget:
                break
            counts.queried += 1
            try:
                raw = fetch_fn(key) or []
            except Exception as e:  # noqa: BLE001 — never abort the run
                log.warning("PubChem backfill failed for %s (%s): %s",
                            row.name, key, e)
                raw = []
            if rate_delay_s > 0:
                time.sleep(rate_delay_s)
            # Scrub to natural-language synonyms only + cap at 10.
            cleaned: List[str] = []
            name_lower = (row.name or "").lower()
            seen = {name_lower}
            for s_ in raw:
                if not isinstance(s_, str):
                    continue
                s_ = s_.strip()
                if not s_ or s_.lower() in seen:
                    continue
                if _looks_like_registry_id(s_):
                    continue
                seen.add(s_.lower())
                cleaned.append(s_)
                if len(cleaned) >= 10:
                    break
            if not cleaned:
                continue
            added = _merge_into_row(row, cleaned)
            if added:
                counts.fetched += 1
                counts.added_total += added
    log.info("Phase 35c bulk-backfill: %s", counts)
    return counts


def _merge_into_row(row, new_synonyms: List[str]) -> int:
    """Deduplicated append of *new_synonyms* onto
    ``row.synonyms_json``.  Mirrors the round-58 seed_synonyms
    helper — kept local so this module stays self-contained."""
    try:
        existing = (json.loads(row.synonyms_json)
                    if row.synonyms_json else [])
    except Exception:  # noqa: BLE001
        existing = []
    name_lower = (row.name or "").lower()
    existing_lower = {s.lower() for s in existing if isinstance(s, str)}
    existing_lower.add(name_lower)
    added = 0
    for s in new_synonyms:
        if not s or s.lower() in existing_lower:
            continue
        existing.append(s)
        existing_lower.add(s.lower())
        added += 1
    if added:
        row.synonyms_json = json.dumps(existing)
    return added
