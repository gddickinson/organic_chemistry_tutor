"""Phase 47b (round 167) — tests for the
Biochemistry-by-Kingdom window + per-kingdom subtab panel.
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
    """Each test gets a fresh BiochemistryByKingdomWindow so
    state from a previous test doesn't bleed in."""
    app.window._biochemistry_by_kingdom_window = None
    yield
    app.window._biochemistry_by_kingdom_window = None


# ==================================================================
# Per-kingdom subtab panel
# ==================================================================

def test_subtab_panel_constructs_for_each_kingdom(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    for kid in ("eukarya", "bacteria", "archaea", "viruses"):
        p = KingdomSubtabPanel(kingdom=kid)
        qtbot.addWidget(p)
        labels = p.subtab_labels()
        assert labels == ["Structure",
                          "Physiology + Development",
                          "Genetics + Evolution"]


def test_subtab_panel_lists_topics(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    # Each sub-pane lists its 5 eukarya topics.
    for sub_id in ("structure", "physiology", "genetics"):
        pane = p._panes[sub_id]
        assert pane._list.count() >= 4, \
            f"({sub_id}) pane has only {pane._list.count()} " \
            f"items"


def test_subtab_panel_select_topic(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    ok = p.select_topic(
        "genetics", "eukarya-genetics-endosymbiotic-origin")
    assert ok is True
    # Detail card should contain the topic title.
    pane = p._panes["genetics"]
    title = pane._title.text()
    assert "Endosymbiotic" in title or "endosymbiotic" \
        in title.lower()


def test_subtab_panel_select_unknown_topic(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    assert p.select_topic("genetics", "does-not-exist") is False


def test_subtab_panel_unknown_subtab(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    assert p.select_topic("not-a-subtab", "anything") is False


def test_subtab_panel_filter_narrows_results(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="bacteria")
    qtbot.addWidget(p)
    pane = p._panes["genetics"]
    n_before = pane._list.count()
    pane._filter_edit.setText("CRISPR")
    n_after = pane._list.count()
    assert n_after > 0
    assert n_after < n_before, \
        "filter should narrow the bacteria/genetics list"


def test_subtab_panel_detail_shows_cross_references(app, qtbot):
    """Topics that carry cross-references must show them in
    the detail card."""
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    p.select_topic(
        "genetics", "eukarya-genetics-endosymbiotic-origin")
    pane = p._panes["genetics"]
    html = pane._detail.toHtml()
    # mitochondrion + chloroplast are both cross-referenced
    # to Phase-43 cell-component ids.
    assert ("mitochondrion" in html.lower()
            or "chloroplast" in html.lower())


# ==================================================================
# Top-level window
# ==================================================================

def test_window_constructs(app, qtbot):
    from orgchem.gui.windows.biochemistry_by_kingdom_window import (
        BiochemistryByKingdomWindow,
    )
    win = BiochemistryByKingdomWindow(parent=app.window)
    qtbot.addWidget(win)
    assert win.tabs.count() == 4


def test_window_kingdom_labels_in_canonical_order(app, qtbot):
    from orgchem.gui.windows.biochemistry_by_kingdom_window import (
        BiochemistryByKingdomWindow,
    )
    win = BiochemistryByKingdomWindow(parent=app.window)
    qtbot.addWidget(win)
    assert win.kingdom_labels() == [
        "Eukarya", "Bacteria", "Archaea", "Viruses"]


def test_window_switch_to_kingdom(app, qtbot):
    from orgchem.gui.windows.biochemistry_by_kingdom_window import (
        BiochemistryByKingdomWindow,
    )
    win = BiochemistryByKingdomWindow(parent=app.window)
    qtbot.addWidget(win)
    assert win.switch_to_kingdom("archaea") is True
    assert win.switch_to_kingdom("not-a-kingdom") is False


def test_window_select_topic_round_trip(app, qtbot):
    from orgchem.gui.windows.biochemistry_by_kingdom_window import (
        BiochemistryByKingdomWindow,
    )
    win = BiochemistryByKingdomWindow(parent=app.window)
    qtbot.addWidget(win)
    ok = win.select_topic(
        "archaea", "genetics", "archaea-genetics-asgard-eocyte")
    assert ok is True
    # Outer tab should be on Archaea.
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Archaea"


def test_window_select_unknown_topic_returns_false(app, qtbot):
    from orgchem.gui.windows.biochemistry_by_kingdom_window import (
        BiochemistryByKingdomWindow,
    )
    win = BiochemistryByKingdomWindow(parent=app.window)
    qtbot.addWidget(win)
    assert win.select_topic(
        "archaea", "genetics", "does-not-exist") is False


def test_main_window_open_method_returns_window(app):
    """`MainWindow.open_biochemistry_by_kingdom_window()` should
    return a window instance + cache it on the main window."""
    win = app.window.open_biochemistry_by_kingdom_window()
    assert win is not None
    # Second call returns the same cached instance.
    win2 = app.window.open_biochemistry_by_kingdom_window()
    assert win is win2


def test_main_window_open_with_kingdom_focuses_tab(app):
    win = app.window.open_biochemistry_by_kingdom_window(
        kingdom="bacteria")
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Bacteria"


def test_main_window_open_with_full_path(app):
    win = app.window.open_biochemistry_by_kingdom_window(
        kingdom="viruses",
        subtab="genetics",
        topic_id="viruses-genetics-not-a-domain",
    )
    assert win is not None
    assert win.tabs.tabText(win.tabs.currentIndex()) == "Viruses"
    # The selected pane's detail card should mention ribosomes
    # (the headline reason viruses aren't classified as
    # living, encoded as a per-row teaching invariant in the
    # round-166 catalogue).
    panel = win.kingdom_panel("viruses")
    pane = panel._panes["genetics"]
    html = pane._detail.toHtml()
    assert "ribosome" in html.lower()


# ==================================================================
# Round 169 / Phase 47d — sub-domain combo on the Eukarya tab
# ==================================================================

def test_eukarya_panel_has_sub_domain_combo(app, qtbot):
    """The Eukarya (and other) per-kingdom panel must carry a
    sub-domain combo populated with that kingdom's
    pedagogically-meaningful sub-domains."""
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    assert p._sub_combo is not None
    items = [p._sub_combo.itemText(i)
             for i in range(p._sub_combo.count())]
    # First item is the "(all)" sentinel.
    assert items[0].startswith("(")
    for required in ("animal", "plant", "fungus", "protist"):
        assert required in items, \
            f"eukarya sub-domain combo missing {required!r}"


def test_panel_set_sub_domain_round_trip(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    assert p.set_sub_domain("plant") is True
    assert p.current_sub_domain() == "plant"


def test_panel_set_unknown_sub_domain_returns_false(app, qtbot):
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    assert p.set_sub_domain("not-a-sub-domain") is False


def test_panel_sub_domain_filter_narrows_pane_lists(app, qtbot):
    """Setting the sub-domain combo to 'plant' must narrow the
    sub-pane lists to plant-relevant topics + drop animal-only
    entries."""
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    p = KingdomSubtabPanel(kingdom="eukarya")
    qtbot.addWidget(p)
    # Before filtering — animal-tight-junctions topic is in the
    # structure pane.
    structure_pane = p._panes["structure"]
    n_unfiltered = structure_pane._list.count()
    visible_unfiltered = [
        structure_pane._list.item(i).text()
        for i in range(n_unfiltered)
    ]
    assert any("Animal cell-cell junctions" in t
               for t in visible_unfiltered)
    # After filter to plant — animal-tight-junctions must be
    # excluded.
    p.set_sub_domain("plant")
    visible_plant = [
        structure_pane._list.item(i).text()
        for i in range(structure_pane._list.count())
    ]
    assert not any("Animal cell-cell junctions" in t
                   for t in visible_plant)
    # But pan-eukaryotic topics + plant-specific topics must
    # still appear.
    assert any("Plant vascular tissue" in t
               for t in visible_plant)


def test_panel_sub_domain_combo_present_for_all_kingdoms(app, qtbot):
    """Every kingdom now carries a sub-domain combo (with
    domain-appropriate options)."""
    from orgchem.gui.panels.kingdom_subtab_panel import (
        KingdomSubtabPanel,
    )
    for kid in ("eukarya", "bacteria", "archaea", "viruses"):
        p = KingdomSubtabPanel(kingdom=kid)
        qtbot.addWidget(p)
        assert p._sub_combo is not None, \
            f"{kid} panel missing sub-domain combo"
