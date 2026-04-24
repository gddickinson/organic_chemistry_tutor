"""Phase 35c round 120 — bulk-backfill core tests.

Network is mocked via an injected `fetch_fn` so the tests run
offline + exhaustively exercise the edge cases (empty hit,
registry-ID scrub, rate limiter zero, Tutor-test skip, no-InChIKey
skip, min-existing threshold).
"""
from __future__ import annotations
import json
import os
import uuid

import pytest


pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def _insert_test_row(name: str, smiles: str, *,
                     inchikey: str = "", synonyms_json=None) -> int:
    """Helper — insert a `Tutor-test…` molecule via raw SQLAlchemy
    so the bulk-backfill can operate on it (bypasses the
    `add_molecule` authoring gate's dedup so we can prime rows
    that simulate specific shapes)."""
    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.session import session_scope
    with session_scope() as s:
        row = DBMol(
            name=name, smiles=smiles, inchikey=inchikey,
            synonyms_json=(json.dumps(synonyms_json)
                           if synonyms_json else None),
        )
        s.add(row)
        s.flush()
        return row.id


def _load_synonyms(mol_id: int) -> list:
    from orgchem.db.models import Molecule as DBMol
    from orgchem.db.session import session_scope
    with session_scope() as s:
        row = s.get(DBMol, mol_id)
        if row is None or not row.synonyms_json:
            return []
        return json.loads(row.synonyms_json) or []


def _uuid8() -> str:
    return uuid.uuid4().hex[:8]


# ---- happy path -------------------------------------------------

def test_backfill_populates_empty_rows(app, monkeypatch):
    """A mocked PubChem hit must land on every empty row +
    filter out registry-ID noise."""
    from orgchem.db.backfill_synonyms import backfill_synonyms

    # NB: the Tutor-test prefix will keep these rows out of the
    # real user's DB thanks to the round-94 session-end purge.
    mid = _insert_test_row(
        f"Tutor-test-backfill-{_uuid8()}",
        smiles="CCN", inchikey="QUSNBJAOOMFDIB-UHFFFAOYSA-N")

    def _fake_fetch(key):
        assert key == "QUSNBJAOOMFDIB-UHFFFAOYSA-N"
        return ["Ethylamine", "1-Aminoethane",
                "75-04-7",         # CAS — filter out
                "Monoethylamine"]

    counts = backfill_synonyms(fetch_fn=_fake_fetch, rate_delay_s=0,
                               skip_test_prefix=False)
    assert counts.queried >= 1
    assert counts.fetched >= 1
    assert counts.added_total >= 3

    stored = _load_synonyms(mid)
    assert "Ethylamine" in stored
    assert "Monoethylamine" in stored
    assert "75-04-7" not in stored


def test_backfill_respects_min_existing(app):
    """A row with ≥ min_existing synonyms is skipped outright —
    no network call, no counts bump."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    mid = _insert_test_row(
        f"Tutor-test-min-{_uuid8()}",
        smiles="CCCN", inchikey="WGYKZJWCGVVSQN-UHFFFAOYSA-N",
        synonyms_json=["existing-alias"])

    calls = []
    def _fake_fetch(key):
        calls.append(key)
        # Return [] so other empty rows walked by the backfill
        # don't get test-only pollution strings written onto them.
        return []

    counts = backfill_synonyms(fetch_fn=_fake_fetch, rate_delay_s=0,
                               min_existing=1,
                               skip_test_prefix=False)
    # This row's InChIKey is unique to the fresh insert so it
    # shouldn't have been called (min_existing guard, not prefix).
    assert "WGYKZJWCGVVSQN-UHFFFAOYSA-N" not in calls
    stored = _load_synonyms(mid)
    assert stored == ["existing-alias"]


def test_backfill_min_existing_zero_refreshes(app):
    """With min_existing=0, even rows that already have synonyms
    get hit (so a user can force-refresh)."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    mid = _insert_test_row(
        f"Tutor-test-refresh-{_uuid8()}",
        smiles="CCCCN", inchikey="HQABUPZFAYXKJW-UHFFFAOYSA-N",
        synonyms_json=["existing-alias"])

    called_with = []
    def _fake_fetch(key):
        called_with.append(key)
        return (["new-alias-1", "new-alias-2"]
                if key == "HQABUPZFAYXKJW-UHFFFAOYSA-N" else [])

    backfill_synonyms(fetch_fn=_fake_fetch, rate_delay_s=0,
                      min_existing=0, skip_test_prefix=False)
    assert "HQABUPZFAYXKJW-UHFFFAOYSA-N" in called_with
    stored = _load_synonyms(mid)
    assert "existing-alias" in stored
    assert "new-alias-1" in stored
    assert "new-alias-2" in stored


# ---- safety gates ----------------------------------------------

def test_backfill_skips_tutor_test_rows(app):
    """Tutor-test prefix rows must never hit the network —
    otherwise a CI run with seeded test pollution would eat
    PubChem budget for nothing."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    # Insert a Tutor-test row with a real-looking empty synonym field.
    tutor_key = "ZZZZZZZZZZZZZZ-UHFFFAOYSA-N"
    _insert_test_row(f"Tutor-test-skip-{_uuid8()}",
                     smiles="NCO", inchikey=tutor_key)

    calls = []
    def _fake_fetch(key):
        calls.append(key)
        # Return [] so any incidental calls (on real seeded rows
        # with empty synonyms) don't pollute the dev DB.
        return []

    counts = backfill_synonyms(fetch_fn=_fake_fetch, rate_delay_s=0)
    assert tutor_key not in calls
    assert counts.skipped_tutor >= 1


def test_backfill_skips_rows_without_inchikey(app):
    """InChIKey-less rows can't be queried — count as
    skipped_no_key, no crash."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    mid = _insert_test_row(f"Tutor-test-nokey-{_uuid8()}",
                           smiles="C#N", inchikey="")

    def _fake_fetch(key):
        # Return [] so any incidental calls on real seeded empty
        # rows (walked because skip_test_prefix=False) don't
        # pollute the dev DB.  The Tutor-test row under test is
        # no-key so it's skipped before the fetch runs anyway.
        return []

    counts = backfill_synonyms(fetch_fn=_fake_fetch, rate_delay_s=0,
                               skip_test_prefix=False)
    assert counts.skipped_no_key >= 1
    assert _load_synonyms(mid) == []


def test_backfill_tolerates_fetch_exception(app):
    """A raising fetch must be caught per-row; the overall run
    carries on."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    mid = _insert_test_row(f"Tutor-test-boom-{_uuid8()}",
                           smiles="[OH-]",
                           inchikey="XLYOFNOQVPJJNP-UHFFFAOYSA-N")

    def _boom(key):
        raise RuntimeError("simulated HTTP error")

    counts = backfill_synonyms(fetch_fn=_boom, rate_delay_s=0,
                               skip_test_prefix=False)
    # Row was queried (attempt counted) but nothing got stored.
    assert counts.queried >= 1
    assert _load_synonyms(mid) == []


def test_backfill_limit_caps_network_calls(app):
    """`limit` argument must cap the number of rows actually
    queried against PubChem."""
    from orgchem.db.backfill_synonyms import backfill_synonyms
    # Insert two fresh rows (both empty, both have InChIKeys).
    _insert_test_row(f"Tutor-test-cap-a-{_uuid8()}",
                     smiles="O=N", inchikey="MWUXSHHQAYIFBG-UHFFFAOYSA-N")
    _insert_test_row(f"Tutor-test-cap-b-{_uuid8()}",
                     smiles="O=S=O", inchikey="RAHZWNYVWXNFOC-UHFFFAOYSA-N")

    calls = []
    def _fake_fetch(key):
        calls.append(key)
        return []

    counts = backfill_synonyms(fetch_fn=_fake_fetch,
                               rate_delay_s=0, limit=1,
                               skip_test_prefix=False)
    assert counts.queried == 1
    assert len(calls) == 1
