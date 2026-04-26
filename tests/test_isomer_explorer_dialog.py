"""Phase 48b (round 171) — tests for the isomer-relationships
dialog.
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
def _reset_singleton():
    from orgchem.gui.dialogs import isomer_explorer as mod
    mod.IsomerExplorerDialog._instance = None
    yield
    mod.IsomerExplorerDialog._instance = None


# ==================================================================
# Construction + singleton
# ==================================================================

def test_dialog_constructs(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.tab_labels() == [
        "Stereoisomers", "Tautomers", "Classify pair"]


def test_dialog_singleton(app):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    a = IsomerExplorerDialog.singleton(parent=app.window)
    b = IsomerExplorerDialog.singleton(parent=app.window)
    assert a is b


def test_select_tab(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    assert d.select_tab("Tautomers") is True
    assert d.select_tab("Classify pair") is True
    assert d.select_tab("NotARealTab") is False


# ==================================================================
# Stereoisomers tab
# ==================================================================

def test_stereo_tab_runs(app, qtbot):
    """Two unassigned stereocentres → 4 isomers in the list."""
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._stereo_smiles.setText("CC(O)C(O)CO")
    d._on_stereo_run()
    assert d._stereo_list.count() == 4
    meta = d._stereo_meta.text()
    assert "Stereoisomers found:" in meta
    assert "Formula:" in meta


def test_stereo_tab_truncation(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    # 4-stereocentre molecule.
    d._stereo_smiles.setText("CC(O)C(O)C(O)C(O)CO")
    d._stereo_max.setValue(4)
    d._on_stereo_run()
    assert d._stereo_list.count() <= 4
    assert "truncated" in d._stereo_meta.text().lower()


def test_stereo_tab_empty_input(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._stereo_smiles.setText("")
    d._on_stereo_run()
    assert d._stereo_list.count() == 0
    assert "enter a smiles" in d._stereo_meta.text().lower()


def test_stereo_tab_unparseable_input(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._stereo_smiles.setText("not-a-smiles")
    d._on_stereo_run()
    assert d._stereo_list.count() == 0
    # Meta line should mention the unparseable formula.
    assert "unparseable" in d._stereo_meta.text().lower()


# ==================================================================
# Tautomers tab
# ==================================================================

def test_taut_tab_acetone(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._taut_smiles.setText("CC(=O)C")
    d._on_taut_run()
    # Acetone has at least 2 tautomers (keto + enol).
    assert d._taut_list.count() >= 2


def test_taut_tab_pentanedione(app, qtbot):
    """2,4-pentanedione is the textbook keto/enol example —
    RDKit's enumerator finds at least 5 tautomers."""
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._taut_smiles.setText("CC(=O)CC(=O)C")
    d._on_taut_run()
    assert d._taut_list.count() >= 5


def test_taut_tab_empty_input(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._taut_smiles.setText("")
    d._on_taut_run()
    assert d._taut_list.count() == 0


# ==================================================================
# Classify-pair tab
# ==================================================================

def test_classify_tab_enantiomers(app, qtbot):
    """(R)/(S)-lactic acid → enantiomer."""
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("C[C@H](O)C(=O)O")
    d._cls_b.setText("C[C@@H](O)C(=O)O")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "enantiomer" in html.lower()
    assert "mirror" in html.lower()


def test_classify_tab_identical(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("CCO")
    d._cls_b.setText("CCO")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "identical" in html.lower()


def test_classify_tab_constitutional(app, qtbot):
    """Propanal + acetone share C3H6O but differ in
    connectivity — constitutional isomers."""
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("CCC=O")
    d._cls_b.setText("CC(C)=O")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "constitutional" in html.lower()


def test_classify_tab_tautomer(app, qtbot):
    """Acetone keto + enol → tautomer."""
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("CC(=O)C")
    d._cls_b.setText("CC(O)=C")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "tautomer" in html.lower()


def test_classify_tab_different_molecule(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("c1ccccc1")
    d._cls_b.setText("Cc1ccccc1")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "different" in html.lower() and "isomer" in html.lower()


def test_classify_tab_empty_input(app, qtbot):
    from orgchem.gui.dialogs.isomer_explorer import (
        IsomerExplorerDialog,
    )
    d = IsomerExplorerDialog(parent=app.window)
    qtbot.addWidget(d)
    d._cls_a.setText("")
    d._cls_b.setText("CCO")
    d._on_classify_run()
    html = d._cls_result.toHtml()
    assert "enter both" in html.lower()


# ==================================================================
# Main-window slot
# ==================================================================

def test_main_window_open_slot(app):
    """`MainWindow._on_isomer_explorer()` should open the
    singleton dialog."""
    from orgchem.gui.dialogs import isomer_explorer as mod
    app.window._on_isomer_explorer()
    assert mod.IsomerExplorerDialog._instance is not None
