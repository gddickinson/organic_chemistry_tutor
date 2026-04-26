"""Phase 47c (round 168) — tests for the
biochemistry-by-kingdom agent actions.
"""
from __future__ import annotations
import os

import pytest


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_window(app):
    """Each test gets a fresh BiochemistryByKingdomWindow."""
    app.window._biochemistry_by_kingdom_window = None
    yield
    app.window._biochemistry_by_kingdom_window = None


# ==================================================================
# list_kingdom_topics
# ==================================================================

def test_list_topics_unfiltered(app):
    rows = app.call("list_kingdom_topics")
    assert len(rows) >= 60


def test_list_topics_by_kingdom(app):
    rows = app.call("list_kingdom_topics", kingdom="archaea")
    assert all(r["kingdom"] == "archaea" for r in rows)
    assert len(rows) >= 10


def test_list_topics_by_subtab(app):
    rows = app.call("list_kingdom_topics", subtab="genetics")
    assert all(r["subtab"] == "genetics" for r in rows)
    assert len(rows) >= 15


def test_list_topics_by_kingdom_and_subtab(app):
    rows = app.call("list_kingdom_topics",
                    kingdom="viruses", subtab="genetics")
    for r in rows:
        assert r["kingdom"] == "viruses"
        assert r["subtab"] == "genetics"
    assert len(rows) >= 4


def test_list_topics_unknown_kingdom(app):
    rows = app.call("list_kingdom_topics", kingdom="bogus")
    assert "error" in rows[0]


def test_list_topics_unknown_subtab(app):
    rows = app.call("list_kingdom_topics", subtab="bogus")
    assert "error" in rows[0]


def test_list_topics_by_sub_domain(app):
    """Round 169 / Phase 47d — sub-domain kwarg."""
    rows = app.call("list_kingdom_topics",
                    kingdom="eukarya", sub_domain="plant")
    ids = {r["id"] for r in rows}
    assert "eukarya-physiology-photosynthesis" in ids
    assert "eukarya-structure-plant-vascular-tissue" in ids
    # Animal-only must NOT appear.
    assert "eukarya-physiology-animal-nervous-system" not in ids


def test_list_topics_unknown_sub_domain(app):
    rows = app.call("list_kingdom_topics",
                    sub_domain="not-a-sub-domain")
    assert "error" in rows[0]


def test_get_topic_includes_sub_domain_field(app):
    """Round 169 — agent action's get_kingdom_topic must
    surface the new sub_domain field."""
    r = app.call(
        "get_kingdom_topic",
        topic_id="eukarya-physiology-photosynthesis")
    assert r["sub_domain"] == "plant"


# ==================================================================
# get_kingdom_topic
# ==================================================================

def test_get_topic_known_id(app):
    r = app.call(
        "get_kingdom_topic",
        topic_id="eukarya-genetics-endosymbiotic-origin")
    assert "error" not in r
    assert r["kingdom"] == "eukarya"
    assert r["subtab"] == "genetics"
    # Cross-references must serialise as list / tuple of strings.
    assert "mitochondrion" in (
        r["cross_reference_cell_component_ids"])


def test_get_topic_unknown_id(app):
    r = app.call("get_kingdom_topic", topic_id="bogus")
    assert "error" in r


# ==================================================================
# find_kingdom_topics
# ==================================================================

def test_find_topics(app):
    rows = app.call("find_kingdom_topics", needle="CRISPR")
    ids = {r["id"] for r in rows}
    # CRISPR appears in both bacteria + archaea genetics topics.
    assert any("crispr" in tid for tid in ids)


def test_find_topics_walks_cross_references(app):
    """A find for a Phase-43 cell-component id should land on
    topics that cross-reference it (not just topics that
    mention the id in body text)."""
    rows = app.call("find_kingdom_topics",
                    needle="mitochondrion")
    ids = {r["id"] for r in rows}
    assert "eukarya-genetics-endosymbiotic-origin" in ids


def test_find_empty(app):
    rows = app.call("find_kingdom_topics", needle="")
    assert rows == []


# ==================================================================
# open_biochemistry_by_kingdom
# ==================================================================

def test_open_no_args(app):
    res = app.call("open_biochemistry_by_kingdom")
    assert res["opened"] is True
    assert res["selected"] is False
    assert res["kingdom"] is None


def test_open_with_kingdom(app):
    res = app.call("open_biochemistry_by_kingdom",
                   kingdom="bacteria")
    assert res["opened"] is True
    assert res["selected"] is True
    assert res["kingdom"] == "bacteria"
    # Verify the window's outer tab actually moved.
    win = app.window._biochemistry_by_kingdom_window
    assert win is not None
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Bacteria"


def test_open_with_full_path(app):
    res = app.call(
        "open_biochemistry_by_kingdom",
        kingdom="archaea", subtab="genetics",
        topic_id="archaea-genetics-asgard-eocyte",
    )
    assert res["opened"] is True
    assert res["selected"] is True
    assert res["topic_id"] == "archaea-genetics-asgard-eocyte"
    win = app.window._biochemistry_by_kingdom_window
    assert win is not None
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Archaea"


def test_open_with_unknown_topic(app):
    res = app.call(
        "open_biochemistry_by_kingdom",
        kingdom="archaea", subtab="genetics",
        topic_id="does-not-exist",
    )
    assert res["opened"] is True
    # Unknown topic id → selected=False, but window opens.
    assert res["selected"] is False


# ==================================================================
# Audit map registration
# ==================================================================

def test_audit_map_includes_all_four_kingdom_actions():
    """Round 168 wired all four `kingdom`-category actions into
    `gui/audit.py::GUI_ENTRY_POINTS` so future regression of
    any one surfaces immediately."""
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("list_kingdom_topics",
                 "get_kingdom_topic",
                 "find_kingdom_topics",
                 "open_biochemistry_by_kingdom"):
        assert name in GUI_ENTRY_POINTS, \
            f"{name} missing from GUI_ENTRY_POINTS"


def test_kingdom_category_actions_registered():
    """All 4 actions live under the `kingdom` category in the
    main action registry."""
    from orgchem.agent.actions import registry
    specs = registry()
    kingdom_actions = {
        name for name, spec in specs.items()
        if getattr(spec, "category", None) == "kingdom"
    }
    for name in ("list_kingdom_topics", "get_kingdom_topic",
                 "find_kingdom_topics",
                 "open_biochemistry_by_kingdom"):
        assert name in kingdom_actions, \
            f"{name} missing from `kingdom`-category action " \
            f"registry; kingdom-tagged actions: " \
            f"{sorted(kingdom_actions)}"
