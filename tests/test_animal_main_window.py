"""Phase AB-1.0 (round 217) — GUI smoke tests for the Animal
Biology Studio main window + Cell-signalling-bridge panel.
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


def test_animal_main_window_constructs(app):
    """Main window + inner tabs construct without crashing.
    AB-2.0 (round 223) added the Organ-systems tab, so the
    tab count is now 4 instead of the original 3."""
    from animal.gui.windows.animal_main_window import (
        AnimalMainWindow,
    )
    win = AnimalMainWindow()
    assert win.tabs.count() >= 4
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Animal taxa" in labels
    assert "Organ systems" in labels
    assert "Cell signalling bridge" in labels
    assert "Tutorials" in labels
    win.close()


def test_animal_taxa_panel_lists_all(app):
    from animal.gui.panels.animal_taxa_panel import (
        AnimalTaxaPanel,
    )
    from animal.core.taxa import list_animal_taxa
    panel = AnimalTaxaPanel()
    assert panel.list_widget.count() == len(list_animal_taxa())


def test_animal_taxa_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.animal_taxa_panel import (
        AnimalTaxaPanel,
    )
    panel = AnimalTaxaPanel()
    assert panel.select_taxon("homo-sapiens")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "homo-sapiens"


def test_animal_taxa_panel_filter_by_metabolite(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.animal_taxa_panel import (
        AnimalTaxaPanel,
    )
    panel = AnimalTaxaPanel()
    panel.filter_edit.setText("dopamine")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "homo-sapiens" in ids


def test_animal_taxa_panel_filter_by_phylum(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.animal_taxa_panel import (
        AnimalTaxaPanel,
    )
    panel = AnimalTaxaPanel()
    for i in range(panel.phylum_combo.count()):
        if panel.phylum_combo.itemData(i) == "arthropoda":
            panel.phylum_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "drosophila-melanogaster" in ids
    assert "homo-sapiens" not in ids  # chordata


def test_animal_taxa_panel_filter_by_body_plan(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.animal_taxa_panel import (
        AnimalTaxaPanel,
    )
    panel = AnimalTaxaPanel()
    for i in range(panel.body_combo.count()):
        if panel.body_combo.itemData(i) == "radial":
            panel.body_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "hydra-vulgaris" in ids
    assert "homo-sapiens" not in ids  # bilateral


def test_signalling_bridge_panel_constructs(app):
    """The bridge reads cellbio.core.cell_signaling directly
    — second sibling whose bridge does so."""
    from animal.gui.panels.cellbio_signaling_bridge_panel import (
        CellBioSignalingBridgePanel,
    )
    panel = CellBioSignalingBridgePanel()
    # Should list the 21-pathway curated animal subset.
    assert panel.list_widget.count() >= 15


def test_signalling_bridge_select_pathway(app):
    from PySide6.QtCore import Qt
    from animal.gui.panels.cellbio_signaling_bridge_panel import (
        CellBioSignalingBridgePanel,
    )
    panel = CellBioSignalingBridgePanel()
    assert panel.select_pathway("hedgehog")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "hedgehog"


def test_signalling_bridge_select_apoptosis(app):
    """Apoptosis pathways belong to the curated subset."""
    from PySide6.QtCore import Qt
    from animal.gui.panels.cellbio_signaling_bridge_panel import (
        CellBioSignalingBridgePanel,
    )
    panel = CellBioSignalingBridgePanel()
    assert panel.select_pathway("intrinsic-apoptosis")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "intrinsic-apoptosis"


def test_open_animal_studio_from_main_window(app):
    main = app.window
    win = main.open_animal_studio_window()
    assert win is not None
    assert main._animal_window is win
    win2 = main.open_animal_studio_window()
    assert win2 is win
    win.close()


def test_open_animal_studio_with_tab(app):
    main = app.window
    win = main.open_animal_studio_window(
        tab_label="Cell signalling bridge")
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Cell signalling bridge"
    win.close()


def test_open_animal_studio_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_animal_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_animal_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_animal_studio", tab="Animal taxa")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Animal taxa"
