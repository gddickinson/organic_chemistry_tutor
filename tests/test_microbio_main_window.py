"""Phase MB-1.0 (round 215) — GUI smoke tests for the
Microbiology Studio main window + Antibiotic-spectrum bridge.
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


def test_microbio_main_window_constructs(app):
    """Main window + inner tabs construct without crashing.
    MB-2.0 (round 221) added the Virulence-factors tab, so
    the tab count is now 4 instead of the original 3."""
    from microbio.gui.windows.microbio_main_window import (
        MicrobioMainWindow,
    )
    win = MicrobioMainWindow()
    assert win.tabs.count() >= 4
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Microbes" in labels
    assert "Virulence factors" in labels
    assert "Antibiotic spectrum" in labels
    assert "Tutorials" in labels
    win.close()


def test_microbes_panel_lists_all(app):
    from microbio.gui.panels.microbes_panel import MicrobesPanel
    from microbio.core.microbes import list_microbes
    panel = MicrobesPanel()
    assert panel.list_widget.count() == len(list_microbes())


def test_microbes_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.microbes_panel import MicrobesPanel
    panel = MicrobesPanel()
    assert panel.select_microbe("mycobacterium-tuberculosis")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "mycobacterium-tuberculosis"


def test_microbes_panel_filter_by_morphology(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.microbes_panel import MicrobesPanel
    panel = MicrobesPanel()
    panel.filter_edit.setText("tuberculosis")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "mycobacterium-tuberculosis" in ids


def test_microbes_panel_filter_by_kingdom(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.microbes_panel import MicrobesPanel
    panel = MicrobesPanel()
    for i in range(panel.kingdom_combo.count()):
        if panel.kingdom_combo.itemData(i) == "virus":
            panel.kingdom_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "hiv-1" in ids
    assert "escherichia-coli" not in ids


def test_microbes_panel_filter_by_gram_type(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.microbes_panel import MicrobesPanel
    panel = MicrobesPanel()
    for i in range(panel.gram_combo.count()):
        if panel.gram_combo.itemData(i) == "gram-positive":
            panel.gram_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "staphylococcus-aureus" in ids
    assert "escherichia-coli" not in ids  # gram-negative


def test_antibiotic_spectrum_panel_constructs(app):
    """The bridge reads pharm.core.drug_classes directly."""
    from microbio.gui.panels.antibiotic_spectrum_panel import (
        AntibioticSpectrumPanel,
    )
    panel = AntibioticSpectrumPanel()
    # Should list the 6 antimicrobial classes from PH-1.0.
    assert panel.list_widget.count() == 6


def test_antibiotic_spectrum_select_drug_class(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.antibiotic_spectrum_panel import (
        AntibioticSpectrumPanel,
    )
    panel = AntibioticSpectrumPanel()
    assert panel.select_drug_class("beta-lactams")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "beta-lactams"


def test_open_microbio_studio_from_main_window(app):
    main = app.window
    win = main.open_microbio_studio_window()
    assert win is not None
    assert main._microbio_window is win
    win2 = main.open_microbio_studio_window()
    assert win2 is win
    win.close()


def test_open_microbio_studio_with_tab(app):
    main = app.window
    win = main.open_microbio_studio_window(
        tab_label="Antibiotic spectrum")
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Antibiotic spectrum"
    win.close()


def test_open_microbio_studio_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_microbio_studio")
    assert isinstance(out, dict)
    assert out.get("opened") is True


def test_open_microbio_studio_agent_action_with_tab(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_microbio_studio", tab="Microbes")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Microbes"
