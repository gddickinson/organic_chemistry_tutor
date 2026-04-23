"""Tests for Phase 28b (source taxonomy) + 29a (carbohydrate data)."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- Phase 28b — curated source taxonomy ---------------------------


def test_curated_map_has_known_entries():
    from orgchem.db.seed_source_tags import _BY_NAME
    # NSAIDs / statins / antibiotics should all be present.
    for name in ("Aspirin", "Atorvastatin", "Penicillin G",
                 "Testosterone", "Dopamine"):
        assert name in _BY_NAME, name


def test_aspirin_tags_include_nsaid():
    from orgchem.db.seed_source_tags import _BY_NAME
    assert "NSAID" in _BY_NAME["Aspirin"]


def test_list_source_tag_values_covers_common_families():
    from orgchem.db.seed_source_tags import list_source_tag_values
    tags = set(list_source_tag_values())
    for required in ("NSAID", "statin", "alkaloid", "hormone",
                     "steroid", "antibiotic", "beta-lactam",
                     "antidiabetic"):
        assert required in tags, required


def test_filter_axes_exposes_source_axis():
    from orgchem.core.molecule_tags import list_filter_axes
    axes = list_filter_axes()
    assert "source" in axes
    assert "NSAID" in axes["source"]
    assert "statin" in axes["source"]


def test_backfill_source_tags_writes_column(app):
    """After the normal seed chain, source_tags_json is populated."""
    import json
    from orgchem.db.session import session_scope
    from orgchem.db.models import Molecule
    with session_scope() as s:
        row = s.query(Molecule).filter(
            Molecule.name == "Aspirin").one_or_none()
        assert row is not None
        assert row.source_tags_json, "source_tags_json should be set"
        tags = json.loads(row.source_tags_json)
        assert "NSAID" in tags
        # Aspirin's hand-curated list also includes the
        # prostaglandin-synthesis-inhibitor marker.
        assert "prostaglandin-synthesis-inhibitor" in tags


def test_filter_by_source_nsaid_hits_aspirin(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="source", value_a="NSAID")
    names = {r.name for r in rows}
    assert "Aspirin" in names


def test_filter_by_source_statin(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="source", value_a="statin")
    names = {r.name for r in rows}
    for s in ("Atorvastatin", "Simvastatin", "Lovastatin"):
        assert s in names


# ---- Phase 29a — carbohydrate data ----------------------------------


def test_catalogue_covers_all_families():
    from orgchem.core.carbohydrates import CARBOHYDRATES
    fams = {c.family for c in CARBOHYDRATES}
    for f in ("monosaccharide", "disaccharide", "polysaccharide"):
        assert f in fams


def test_glucose_anomers_present():
    from orgchem.core.carbohydrates import CARBOHYDRATES
    names = {c.name for c in CARBOHYDRATES}
    assert "α-D-Glucopyranose" in names
    assert "β-D-Glucopyranose" in names
    assert "D-Glucose (open chain)" in names


def test_all_smiles_parse_via_rdkit():
    from rdkit import Chem
    from orgchem.core.carbohydrates import CARBOHYDRATES
    for c in CARBOHYDRATES:
        mol = Chem.MolFromSmiles(c.smiles)
        assert mol is not None, c.name


def test_list_and_filter_helpers():
    from orgchem.core.carbohydrates import (
        list_carbohydrates, get_carbohydrate, families,
    )
    all_rows = list_carbohydrates()
    assert len(all_rows) >= 14
    assert {f for f in families()} == {
        "monosaccharide", "disaccharide", "polysaccharide",
    }
    assert get_carbohydrate("Sucrose") is not None
    assert get_carbohydrate("sucrose") is not None   # case-insensitive
    assert get_carbohydrate("not-a-sugar") is None
    mono = list_carbohydrates(family="monosaccharide")
    assert mono and all(
        r["family"] == "monosaccharide" for r in mono)


# ---- Agent actions ---------------------------------------------------


def test_list_carbohydrates_action(app):
    rows = app.call("list_carbohydrates")
    assert len(rows) >= 14


def test_get_carbohydrate_action_ok(app):
    r = app.call("get_carbohydrate", carb_name="Sucrose")
    assert "error" not in r
    assert r["family"] == "disaccharide"


def test_get_carbohydrate_action_error(app):
    r = app.call("get_carbohydrate", carb_name="Zzz")
    assert "error" in r


def test_carbohydrate_families_action(app):
    r = app.call("carbohydrate_families")
    assert set(r) == {"monosaccharide", "disaccharide", "polysaccharide"}


# ---- Coverage still 100 % -----------------------------------------


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
