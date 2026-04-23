"""Tests for Phase 28d + 28e — filter-bar UI + agent actions."""
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


# ---- Query helper ----------------------------------------------------


def test_query_by_tags_returns_rows(app):
    """Unfiltered call matches the plain list_molecules count."""
    from orgchem.db.queries import query_by_tags, count_molecules
    rows = query_by_tags()
    assert len(rows) <= count_molecules()   # limited by default limit
    assert len(rows) > 0


def test_query_by_tags_filters_aromatic(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="functional_group", value_a="aromatic")
    assert rows
    # Every row's tag JSON should contain "aromatic".
    for r in rows:
        assert "aromatic" in (r.functional_group_tags_json or "")


def test_query_by_tags_size_small(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="size", value_a="small")
    for r in rows:
        assert r.heavy_atom_count is not None
        assert r.heavy_atom_count <= 12


def test_query_by_tags_charge_neutral_default(app):
    """Most seeded molecules are neutral."""
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="charge", value_a="neutral")
    assert rows
    for r in rows:
        assert r.formal_charge == 0


def test_query_by_tags_and_semantics(app):
    """Combining two axes AND-filters (small + aromatic)."""
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(
        axis_a="size", value_a="small",
        axis_b="functional_group", value_b="aromatic",
    )
    # Each row must satisfy both: size ≤ 12 AND aromatic tag.
    for r in rows:
        assert (r.heavy_atom_count or 0) <= 12
        assert "aromatic" in (r.functional_group_tags_json or "")


def test_query_by_tags_text_query(app):
    """Free-text substring combines with tag filters."""
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(
        axis_a="functional_group", value_a="aromatic",
        text_query="benzene",
    )
    # Benzene itself is aromatic and present in the seed set.
    names = {r.name.lower() for r in rows}
    assert any("benzene" in n for n in names)


def test_query_by_tags_ring_count(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="ring_count", value_a="acyclic")
    for r in rows:
        assert r.n_rings == 0


def test_query_by_tags_has_stereo_yes(app):
    from orgchem.db.queries import query_by_tags
    rows = query_by_tags(axis_a="has_stereo", value_a="yes")
    # Some seeded amino acids are chiral → has_stereo = True.
    assert rows
    for r in rows:
        assert r.has_stereo is True


# ---- Agent actions ---------------------------------------------------


def test_list_molecule_categories_action(app):
    r = app.call("list_molecule_categories")
    assert isinstance(r, dict)
    assert "functional_group" in r
    assert "carboxylic_acid" in r["functional_group"]


def test_filter_molecules_action(app):
    r = app.call("filter_molecules",
                 axis_a="functional_group", value_a="aromatic",
                 limit=10)
    assert isinstance(r, list)
    for row in r:
        assert "name" in row and "smiles" in row


# ---- GUI filter bar --------------------------------------------------


def test_molecule_browser_has_filter_bar(app):
    """Browser now exposes axis/value combos + clear button + count."""
    b = app.window.browser
    assert hasattr(b, "axis_a")
    assert hasattr(b, "axis_b")
    assert hasattr(b, "value_a")
    assert hasattr(b, "value_b")
    assert hasattr(b, "clear_btn")
    assert hasattr(b, "count_label")


def test_filter_bar_selecting_axis_populates_values(app):
    b = app.window.browser
    # Find the "functional_group" index on axis A and select it.
    for i in range(b.axis_a.count()):
        if b.axis_a.itemData(i) == "functional_group":
            b.axis_a.setCurrentIndex(i)
            break
    # Value-A combo should have grown well beyond just "(any)".
    assert b.value_a.count() > 5


def test_filter_bar_clears(app):
    b = app.window.browser
    # Set a filter, then clear.
    b.filter.setText("something")
    b._on_clear_filters()
    assert b.filter.text() == ""
    assert b.axis_a.currentData() in ("", None)


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
