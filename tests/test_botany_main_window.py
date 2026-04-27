"""Phase BT-1.0 (round 216) — GUI smoke tests for the Botany
Studio main window + Plant-secondary-metabolites bridge.
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


def test_botany_main_window_constructs(app):
    """Main window + inner tabs construct without crashing.
    BT-2.0 (round 222) added the Plant-hormones tab, so the
    tab count is now 4 instead of the original 3."""
    from botany.gui.windows.botany_main_window import (
        BotanyMainWindow,
    )
    win = BotanyMainWindow()
    assert win.tabs.count() >= 4
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Plant taxa" in labels
    assert "Plant hormones" in labels
    assert "Plant secondary metabolites" in labels
    assert "Tutorials" in labels
    win.close()


def test_plant_taxa_panel_lists_all(app):
    from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
    from botany.core.taxa import list_plant_taxa
    panel = PlantTaxaPanel()
    assert panel.list_widget.count() == len(list_plant_taxa())


def test_plant_taxa_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
    panel = PlantTaxaPanel()
    assert panel.select_taxon("papaver-somniferum")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "papaver-somniferum"


def test_plant_taxa_panel_filter_by_metabolite(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
    panel = PlantTaxaPanel()
    panel.filter_edit.setText("morphine")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "papaver-somniferum" in ids


def test_plant_taxa_panel_filter_by_division(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
    panel = PlantTaxaPanel()
    for i in range(panel.division_combo.count()):
        if panel.division_combo.itemData(i) == "gymnosperm":
            panel.division_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "ginkgo-biloba" in ids
    assert "papaver-somniferum" not in ids  # eudicot


def test_plant_taxa_panel_filter_by_photosynthesis(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_taxa_panel import PlantTaxaPanel
    panel = PlantTaxaPanel()
    for i in range(panel.photo_combo.count()):
        if panel.photo_combo.itemData(i) == "C4":
            panel.photo_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "zea-mays" in ids
    assert "arabidopsis-thaliana" not in ids  # C3


def test_plant_metabolites_panel_constructs(app):
    """The bridge reads orgchem.db.Molecule rows directly."""
    from botany.gui.panels.plant_metabolites_panel import (
        PlantMetabolitesPanel,
    )
    panel = PlantMetabolitesPanel()
    # Default category = "(all plant-derived)" should
    # surface at least the natural-product (11) + terpene
    # (6) + alkaloid (3) + steroid (2) tagged rows, after
    # de-duplication by molecule.  Lower bound is loose:
    assert panel.list_widget.count() >= 10


def test_plant_metabolites_panel_alkaloid_filter(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_metabolites_panel import (
        PlantMetabolitesPanel,
    )
    panel = PlantMetabolitesPanel()
    # Switch combo to "Alkaloids".
    for i in range(panel.tag_combo.count()):
        if panel.tag_combo.itemData(i) == "alkaloid":
            panel.tag_combo.setCurrentIndex(i)
            break
    names = []
    for i in range(panel.list_widget.count()):
        names.append(panel.list_widget.item(i).text())
    # Morphine + Atropine + Quinine all carry the alkaloid
    # tag in the seeded DB.
    assert "Morphine" in names
    assert "Atropine" in names
    assert "Quinine" in names


def test_plant_metabolites_panel_text_filter(app):
    from PySide6.QtCore import Qt
    from botany.gui.panels.plant_metabolites_panel import (
        PlantMetabolitesPanel,
    )
    panel = PlantMetabolitesPanel()
    panel.filter_edit.setText("Caps")
    names = []
    for i in range(panel.list_widget.count()):
        names.append(panel.list_widget.item(i).text())
    assert "Capsaicin" in names


def test_open_botany_studio_from_main_window(app):
    main = app.window
    win = main.open_botany_studio_window()
    assert win is not None
    assert main._botany_window is win
    win2 = main.open_botany_studio_window()
    assert win2 is win
    win.close()


def test_open_botany_studio_with_tab(app):
    main = app.window
    win = main.open_botany_studio_window(
        tab_label="Plant secondary metabolites")
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Plant secondary metabolites"
    win.close()


def test_open_botany_studio_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_botany_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_botany_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_botany_studio", tab="Plant taxa")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Plant taxa"
