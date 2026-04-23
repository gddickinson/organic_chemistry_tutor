"""Tests for Phase 28a+c — molecule-browser filter columns + auto-tagger."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


# ---- Auto-tagger ---------------------------------------------------


def test_aspirin_full_tagset():
    """Aspirin (CC(=O)Oc1ccccc1C(=O)O) should trip ester + carboxylic
    acid + aromatic + ring-containing categories."""
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("CC(=O)Oc1ccccc1C(=O)O")
    fg = set(t.functional_groups)
    assert "carboxylic_acid" in fg
    assert "ester" in fg
    assert "aromatic" in fg
    assert t.charge_category == "neutral"
    # Aspirin has 13 heavy atoms, which puts it in the medium band
    # (small = ≤ 12).
    assert t.size_band == "medium"
    assert t.ring_band == "one_to_two"
    assert t.n_rings == 1
    assert not t.has_stereo


def test_ethanol_has_alcohol_but_not_acid():
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("CCO")
    assert "alcohol" in t.functional_groups
    assert "carboxylic_acid" not in t.functional_groups
    assert t.size_band == "small"


def test_benzene_is_aromatic_and_acyclic_claim_false():
    """Benzene has exactly one ring → one_to_two."""
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("c1ccccc1")
    assert "aromatic" in t.functional_groups
    assert t.ring_band == "one_to_two"
    assert t.n_rings == 1


def test_lactate_is_chiral():
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("C[C@@H](O)C(=O)O")
    assert t.has_stereo


def test_amino_acid_is_zwitterion():
    """Zwitterionic glycine: H3N+-CH2-COO-."""
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("[NH3+]CC(=O)[O-]")
    assert t.charge_category == "zwitterion"


def test_carboxylate_anion():
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("CC(=O)[O-]")
    assert t.charge_category == "anion"
    assert t.formal_charge == -1


def test_ammonium_cation():
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("C[NH3+]")
    assert t.charge_category == "cation"


def test_halogen_composition_flag():
    from orgchem.core.molecule_tags import auto_tag
    t = auto_tag("Clc1ccccc1")
    assert "contains_halogen" in t.composition_flags
    assert "pure_organic" in t.composition_flags


def test_size_bands():
    from orgchem.core.molecule_tags import auto_tag
    # Small (10 heavy atoms)
    assert auto_tag("CCCCCCCCCC").size_band == "small"
    # Medium (~20)
    assert auto_tag("CCCCCCCCCCCCCCCCCCCC").size_band == "medium"
    # Large — hemoglobin-scale not needed; cholesterol (27 heavy),
    # let's use a 35-heavy-atom lipid ester.
    big = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC"
    assert auto_tag(big).size_band == "large"


def test_ring_bands():
    from orgchem.core.molecule_tags import auto_tag
    assert auto_tag("CCC").ring_band == "acyclic"
    assert auto_tag("c1ccccc1").ring_band == "one_to_two"
    assert auto_tag("c1ccc2ccccc2c1").ring_band == "one_to_two"
    # Pyrene has 4 fused rings.
    assert auto_tag("c1cc2ccc3cccc4ccc(c1)c2c34").ring_band \
        == "three_plus"


def test_filter_axes_enumeration_shape():
    from orgchem.core.molecule_tags import list_filter_axes
    axes = list_filter_axes()
    for key in ("functional_group", "composition", "charge",
                "size", "ring_count", "has_stereo"):
        assert key in axes
    assert "carboxylic_acid" in axes["functional_group"]
    assert "zwitterion" in axes["charge"]


def test_result_to_dict_shape():
    from orgchem.core.molecule_tags import auto_tag
    d = auto_tag("CCO").to_dict()
    for key in ("functional_groups", "composition_flags",
                "charge_category", "size_band", "ring_band",
                "heavy_atom_count", "formal_charge", "n_rings",
                "has_stereo"):
        assert key in d


# ---- DB schema + backfill ------------------------------------------


def test_model_has_new_columns():
    from orgchem.db.models import Molecule
    cols = {c.name for c in Molecule.__table__.columns}
    for c in ("source_tags_json", "functional_group_tags_json",
              "heavy_atom_count", "formal_charge", "n_rings",
              "has_stereo"):
        assert c in cols, c


def test_additive_migration_adds_molecule_tag_columns(tmp_path):
    """Simulate a pre-28a database and check init_db migrates it."""
    import sqlite3
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db

    db_path = tmp_path / "legacy.db"
    conn = sqlite3.connect(db_path)
    # Minimal pre-28a molecules table — just enough to trip the
    # migration path (we don't need a real orm_scope).
    conn.executescript(
        "CREATE TABLE molecules ("
        "  id INTEGER PRIMARY KEY, "
        "  name TEXT, smiles TEXT, inchi TEXT, inchikey TEXT, "
        "  formula TEXT, molblock_2d TEXT, molblock_3d TEXT, "
        "  properties_json TEXT, source TEXT, created_at DATETIME"
        ");"
    )
    conn.commit()
    conn.close()

    cfg = AppConfig()
    cfg.db_path = db_path
    init_db(cfg)

    conn = sqlite3.connect(db_path)
    cols = {row[1] for row in conn.execute(
        "PRAGMA table_info(molecules)").fetchall()}
    conn.close()
    for c in ("source_tags_json", "functional_group_tags_json",
              "heavy_atom_count", "formal_charge", "n_rings",
              "has_stereo"):
        assert c in cols, c


def test_backfill_populates_seeded_rows(tmp_path, monkeypatch):
    """After backfill, every seeded molecule has auto-tag columns set."""
    from orgchem.config import AppConfig
    from orgchem.db.session import init_db, session_scope
    from orgchem.db.seed import seed_if_empty
    from orgchem.db.models import Molecule
    cfg = AppConfig()
    cfg.db_path = tmp_path / "test.db"
    init_db(cfg)
    seed_if_empty(cfg)
    with session_scope() as s:
        rows = list(s.query(Molecule).limit(20).all())
    # At least the first 20 seeded rows are tagged.
    assert rows
    tagged = [r for r in rows
              if r.functional_group_tags_json is not None
              and r.heavy_atom_count is not None]
    assert len(tagged) == len(rows)
