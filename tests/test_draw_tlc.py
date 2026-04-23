"""Tests for the Phase 15b TLC-plate renderer (round 53)."""
from __future__ import annotations
import os
from pathlib import Path

import pytest

pytest.importorskip("rdkit")
pytest.importorskip("matplotlib")


def test_render_figure_returns_matplotlib_figure():
    from orgchem.core.chromatography import simulate_tlc
    from orgchem.render.draw_tlc import render_figure
    data = simulate_tlc(["CC(=O)O", "c1ccccc1", "CCO"],
                        solvent="hexane:ethyl_acetate:1:1")
    fig = render_figure(data)
    import matplotlib.pyplot as plt
    assert fig is not None
    # Should have drawn something — at least one axes with patches.
    ax = fig.axes[0]
    assert len(ax.patches) >= 3, ax.patches
    plt.close(fig)


def test_export_tlc_plate_png(tmp_path):
    from orgchem.core.chromatography import simulate_tlc
    from orgchem.render.draw_tlc import export_tlc_plate
    data = simulate_tlc(["CC(=O)O", "c1ccccc1", "Oc1ccccc1C(=O)O"])
    out = tmp_path / "plate.png"
    export_tlc_plate(data, out)
    assert out.exists()
    assert out.stat().st_size > 4000   # real render, not a 1-pixel blank


def test_export_tlc_plate_svg(tmp_path):
    from orgchem.core.chromatography import simulate_tlc
    from orgchem.render.draw_tlc import export_tlc_plate
    data = simulate_tlc(["CCO", "c1ccccc1"])
    out = tmp_path / "plate.svg"
    export_tlc_plate(data, out)
    # SVG produced by matplotlib always contains the xmlns declaration.
    text = out.read_text()
    assert "<svg" in text and "xmlns" in text


def test_render_figure_tolerates_error_rows():
    """If simulate_tlc returns a row with `error` (bad SMILES), the
    renderer must not crash — it skips the bad row cleanly."""
    from orgchem.render.draw_tlc import render_figure
    data = {
        "solvent": "hexane:ethyl_acetate:1:1",
        "solvent_polarity": 0.23,
        "compounds": [
            {"smiles": "CCO", "rf": 0.42, "logp": -0.14},
            {"smiles": "!!!broken!!!", "error": "invalid SMILES"},
        ],
    }
    import matplotlib.pyplot as plt
    fig = render_figure(data)
    plt.close(fig)   # no assertion — just has to not raise


def test_agent_action_export_tlc_plate(tmp_path):
    from orgchem.agent.actions import invoke
    out = tmp_path / "agent.png"
    res = invoke(
        "export_tlc_plate",
        smiles_list=["CC(=O)O", "c1ccccc1", "CCO"],
        path=str(out),
        solvent="hexane:ethyl_acetate:1:1",
    )
    assert "error" not in res
    assert Path(res["path"]).exists()
    assert res["compound_count"] == 3
    assert res["rf_table"] and all("rf" in r for r in res["rf_table"])


def test_agent_action_audit_entry_wired():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    entry = GUI_ENTRY_POINTS.get("export_tlc_plate", "")
    assert "Lab techniques" in entry and "TLC" in entry


def test_gui_coverage_still_100():
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0


# ---- GUI wiring --------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_lab_dialog_has_save_plate_button(app, tmp_path, monkeypatch):
    """Opening the Lab-techniques dialog exposes the new Save plate
    button on the TLC tab, and clicking it writes a file."""
    from orgchem.gui.dialogs.lab_techniques import LabTechniquesDialog
    dlg = LabTechniquesDialog(app.window)
    dlg.tlc_smiles.setPlainText("CCO\nc1ccccc1")
    out = tmp_path / "plate-from-dialog.png"
    # Patch QFileDialog so the test doesn't open a modal picker.
    from PySide6.QtWidgets import QFileDialog
    monkeypatch.setattr(
        QFileDialog, "getSaveFileName",
        lambda *a, **k: (str(out), "PNG image (*.png)"),
    )
    # Patch QMessageBox.information + .critical so the dialog doesn't
    # block the test with a modal.
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "information",
                        lambda *a, **k: None)
    monkeypatch.setattr(QMessageBox, "critical",
                        lambda *a, **k: None)
    dlg._on_tlc_save_plate()
    assert out.exists()
    assert out.stat().st_size > 3000
