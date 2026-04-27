"""Phase MB-2.0 (round 221) — GUI smoke tests for the new
Virulence-factors panel + the extended MicrobioMainWindow.
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


def test_virulence_panel_constructs(app):
    from microbio.gui.panels.virulence_factors_panel import (
        VirulenceFactorsPanel,
    )
    from microbio.core.virulence_factors import (
        list_virulence_factors,
    )
    panel = VirulenceFactorsPanel()
    assert panel.list_widget.count() == \
        len(list_virulence_factors())


def test_virulence_panel_select_by_id(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.virulence_factors_panel import (
        VirulenceFactorsPanel,
    )
    panel = VirulenceFactorsPanel()
    assert panel.select_factor("cholera-toxin")
    item = panel.list_widget.currentItem()
    assert item is not None
    assert item.data(Qt.UserRole) == "cholera-toxin"


def test_virulence_panel_filter_by_text(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.virulence_factors_panel import (
        VirulenceFactorsPanel,
    )
    panel = VirulenceFactorsPanel()
    panel.filter_edit.setText("botox")
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "botulinum-toxin" in ids


def test_virulence_panel_filter_by_class(app):
    from PySide6.QtCore import Qt
    from microbio.gui.panels.virulence_factors_panel import (
        VirulenceFactorsPanel,
    )
    panel = VirulenceFactorsPanel()
    for i in range(panel.class_combo.count()):
        if panel.class_combo.itemData(i) == "ab-toxin":
            panel.class_combo.setCurrentIndex(i)
            break
    ids = []
    for i in range(panel.list_widget.count()):
        ids.append(panel.list_widget.item(i).data(Qt.UserRole))
    assert "diphtheria-toxin" in ids
    assert "tsst-1" not in ids  # superantigen class


def test_microbio_main_window_has_virulence_tab(app):
    from microbio.gui.windows.microbio_main_window import (
        MicrobioMainWindow,
    )
    win = MicrobioMainWindow()
    labels = {win.tabs.tabText(i)
              for i in range(win.tabs.count())}
    assert "Microbes" in labels
    assert "Virulence factors" in labels
    assert "Antibiotic spectrum" in labels
    assert "Tutorials" in labels
    assert win.tabs.count() >= 4
    win.close()


def test_microbio_main_window_switch_to_virulence(app):
    from microbio.gui.windows.microbio_main_window import (
        MicrobioMainWindow,
    )
    win = MicrobioMainWindow()
    assert win.switch_to(MicrobioMainWindow.TAB_VIRULENCE)
    assert win.tabs.tabText(win.tabs.currentIndex()) == \
        "Virulence factors"
    win.close()


def test_open_microbio_virulence_tab_agent_action(app):
    from orgchem.agent.actions import invoke
    out = invoke("open_microbio_virulence_tab")
    assert isinstance(out, dict)
    assert out.get("opened") is True
    assert out.get("tab") == "Virulence factors"
