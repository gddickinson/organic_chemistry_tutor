"""Phase GM-1.0 (round 230) — GUI smoke tests for
``TechniquesPanel``.
"""
from __future__ import annotations
import os
import pytest


pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_panel_constructs(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    assert panel.list_widget.count() >= 30


def test_filter_by_category_combo(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    full = panel.list_widget.count()
    # Pick the "crispr" category.
    for i in range(panel.category_combo.count()):
        if panel.category_combo.itemData(i) == "crispr":
            panel.category_combo.setCurrentIndex(i)
            break
    crispr_count = panel.list_widget.count()
    assert 0 < crispr_count < full


def test_text_filter_narrows_list(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    full = panel.list_widget.count()
    panel.filter_edit.setText("polymerase")
    narrowed = panel.list_widget.count()
    assert 0 < narrowed < full


def test_select_technique_focuses_row(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    assert panel.select_technique("crispr-cas9") is True
    current = panel.list_widget.currentItem()
    from PySide6.QtCore import Qt
    assert current.data(Qt.UserRole) == "crispr-cas9"


def test_select_unknown_returns_false(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    assert panel.select_technique("does-not-exist") is False


def test_detail_card_renders_with_cross_refs(app):
    from genetics.gui.panels.techniques_panel import (
        TechniquesPanel,
    )
    panel = TechniquesPanel()
    panel.select_technique("crispr-cas9")
    html = panel.detail.toHtml()
    # Should mention cross-references it carries.
    assert "p53" in html  # signalling-pathway xref
    assert "mus-musculus" in html  # animal-taxon xref
