"""Tests for Phase 26a — glossary example-figure schema (round 32)."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_glossary_model_has_figure_columns():
    from orgchem.db.models import GlossaryTerm
    cols = {c.name for c in GlossaryTerm.__table__.columns}
    assert "example_smiles" in cols
    assert "example_figure_path" in cols


def test_seed_version_bumped_to_three():
    from orgchem.db.seed_glossary import SEED_VERSION
    assert SEED_VERSION >= 3


def test_seed_rows_carry_example_smiles_for_anchors():
    """Round-32 anchor terms must have example_smiles seeded."""
    from orgchem.db.seed_glossary import _GLOSSARY
    by_term = {row["term"]: row for row in _GLOSSARY}
    anchors = ["Aromaticity", "Carbocation",
               "Diels-Alder reaction", "Aldol reaction"]
    for anchor in anchors:
        assert anchor in by_term, anchor
        assert by_term[anchor].get("example_smiles"), \
            f"{anchor} should carry example_smiles in round 32"


def test_seed_rows_without_example_smiles_stay_none():
    """Legacy rows keep a None default — the schema is additive."""
    from orgchem.db.seed_glossary import _GLOSSARY
    # Pick one we deliberately leave unannotated because it's a
    # concept without a canonical SMILES.
    by_term = {row["term"]: row for row in _GLOSSARY}
    assert by_term["Transition state"].get("example_smiles") \
        in (None, "", False)


def test_seed_writes_example_smiles_into_db(tmp_path, monkeypatch):
    """Full round-trip: init_db → seed_glossary → read back."""
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.seed_glossary import seed_glossary_if_empty
    from orgchem.db.models import GlossaryTerm
    cfg = AppConfig()
    cfg.db_path = tmp_path / "test.db"
    init_db(cfg)
    seed_glossary_if_empty(force=True)
    with session_scope() as s:
        row = s.query(GlossaryTerm).filter(
            GlossaryTerm.term == "Aromaticity").one_or_none()
        assert row is not None
        assert row.example_smiles == "c1ccccc1"


def test_additive_migration_adds_columns_on_legacy_db(tmp_path):
    """If an existing DB predates the schema change, the migration hook
    must add the new columns without destroying the table."""
    import sqlite3
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db

    db_path = tmp_path / "legacy.db"
    # Simulate a pre-26a database: create glossary_terms without the
    # new columns, then init_db should upgrade in place.
    conn = sqlite3.connect(db_path)
    conn.executescript(
        "CREATE TABLE glossary_terms ("
        "  id INTEGER PRIMARY KEY, "
        "  term VARCHAR(200) NOT NULL UNIQUE, "
        "  aliases_json TEXT, "
        "  definition_md TEXT NOT NULL, "
        "  category VARCHAR(80), "
        "  see_also_json TEXT, "
        "  example_ids_json TEXT, "
        "  created_at DATETIME"
        ");"
    )
    conn.commit()
    conn.close()

    cfg = AppConfig()
    cfg.db_path = db_path
    init_db(cfg)

    # After init_db, the migration step should have added the new
    # columns.
    conn = sqlite3.connect(db_path)
    cols = {row[1] for row in conn.execute(
        "PRAGMA table_info(glossary_terms)").fetchall()}
    conn.close()
    assert "example_smiles" in cols
    assert "example_figure_path" in cols
