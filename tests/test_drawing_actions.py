"""Phase 36h round 127 — tests for the drawing-tool agent actions.

``open_drawing_tool`` / ``drawing_to_smiles`` / ``drawing_export``
/ ``drawing_clear`` are the tutor + stdio-bridge surface for the
Phase-36g :class:`DrawingToolDialog`.  These tests drive them
through :func:`orgchem.agent.actions.invoke` just like a caller
would.
"""
from __future__ import annotations
import os

import pytest
from rdkit import Chem

pytest.importorskip("pytestqt", reason="pytest-qt not installed")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_singleton():
    from orgchem.gui.dialogs import drawing_tool as mod
    mod.DrawingToolDialog._instance = None
    yield
    mod.DrawingToolDialog._instance = None


# ---- registration -----------------------------------------------

def test_actions_registered_in_registry():
    from orgchem.agent.actions import registry
    names = {name for name, spec in registry().items()
             if spec.category == "drawing"}
    assert names == {
        "open_drawing_tool",
        "drawing_to_smiles",
        "drawing_export",
        "drawing_clear",
        "make_reaction_scheme",
    }


# ---- open_drawing_tool ------------------------------------------

def test_open_drawing_tool_creates_singleton(app):
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog
    res = invoke("open_drawing_tool")
    assert res["opened"] is True
    assert res["seeded_smiles"] is False
    assert res["current_smiles"] == ""
    assert DrawingToolDialog._instance is not None


def test_open_drawing_tool_with_seed_smiles(app):
    from orgchem.agent.actions import invoke
    res = invoke("open_drawing_tool", smiles="c1ccccc1")
    assert res["opened"] is True
    assert res["seeded_smiles"] is True
    assert Chem.CanonSmiles(res["current_smiles"]) == \
           Chem.CanonSmiles("c1ccccc1")


def test_open_drawing_tool_without_gui_returns_error(monkeypatch):
    """If the main-window pointer isn't set, the action must
    error-return cleanly rather than raising."""
    from orgchem.agent.actions import invoke
    import orgchem.agent.controller as controller_mod
    monkeypatch.setattr(controller_mod, "main_window",
                        lambda: None)
    res = invoke("open_drawing_tool")
    assert "error" in res
    assert "Main window" in res["error"]


# ---- drawing_to_smiles ------------------------------------------

def test_drawing_to_smiles_without_open_returns_error(app):
    from orgchem.agent.actions import invoke
    res = invoke("drawing_to_smiles")
    assert "error" in res
    assert "open_drawing_tool" in res["error"]


def test_drawing_to_smiles_returns_canvas_state(app):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool", smiles="CCO")
    res = invoke("drawing_to_smiles")
    assert Chem.CanonSmiles(res["smiles"]) == Chem.CanonSmiles("CCO")
    assert res["n_atoms"] == 3
    assert res["n_bonds"] == 2


def test_drawing_to_smiles_empty_canvas(app):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool")
    res = invoke("drawing_to_smiles")
    assert res["smiles"] == ""
    assert res["n_atoms"] == 0


# ---- drawing_export ---------------------------------------------

def test_drawing_export_without_open_returns_error(app, tmp_path):
    from orgchem.agent.actions import invoke
    res = invoke("drawing_export", path=str(tmp_path / "d.png"))
    assert "error" in res


def test_drawing_export_empty_canvas_returns_error(app, tmp_path):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool")
    res = invoke("drawing_export", path=str(tmp_path / "empty.png"))
    assert "error" in res
    assert "empty" in res["error"].lower()


def test_drawing_export_rejects_unknown_extension(app, tmp_path):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool", smiles="CCO")
    res = invoke("drawing_export", path=str(tmp_path / "d.xyz"))
    assert "error" in res
    assert "extension" in res["error"].lower()


def test_drawing_export_writes_mol_v2000(app, tmp_path):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool", smiles="CCO")
    out = tmp_path / "ethanol.mol"
    res = invoke("drawing_export", path=str(out))
    assert res.get("saved") is True
    assert res["format"] == "mol"
    assert out.exists()
    text = out.read_text()
    assert "V2000" in text and "M  END" in text


def test_drawing_export_writes_png(app, tmp_path):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool", smiles="CCO")
    out = tmp_path / "ethanol.png"
    res = invoke("drawing_export", path=str(out))
    assert res.get("saved") is True
    assert res["format"] == "png"
    assert out.exists() and out.stat().st_size > 0


# ---- drawing_clear ----------------------------------------------

def test_drawing_clear_without_open_returns_error(app):
    from orgchem.agent.actions import invoke
    res = invoke("drawing_clear")
    assert "error" in res


def test_drawing_clear_empties_canvas(app):
    from orgchem.agent.actions import invoke
    invoke("open_drawing_tool", smiles="CCO")
    assert invoke("drawing_to_smiles")["n_atoms"] == 3
    res = invoke("drawing_clear")
    assert res.get("cleared") is True
    after = invoke("drawing_to_smiles")
    assert after["n_atoms"] == 0
    assert after["smiles"] == ""


# ---- make_reaction_scheme (Phase 36f.1, round 131) -------------

def test_make_reaction_scheme_basic_round_trip(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="CCO", rhs_smiles="CC=O")
    assert "error" not in res
    assert res["reaction_smiles"] == "CCO>>CC=O"
    assert res["arrow"] == "forward"
    assert res["reagents"] == ""
    assert res["balanced"] is True


def test_make_reaction_scheme_with_reagents(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="CCO", rhs_smiles="CC=O",
                 reagents="[Cr]")
    assert res["reaction_smiles"] == "CCO>[Cr]>CC=O"
    assert res["reagents"] == "[Cr]"


def test_make_reaction_scheme_unbalanced_flag(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="CC", rhs_smiles="CCO")
    assert res["balanced"] is False


def test_make_reaction_scheme_garbage_smiles_returns_error(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="!!nope", rhs_smiles="C")
    assert "error" in res
    assert "parse" in res["error"].lower()


def test_make_reaction_scheme_invalid_arrow_rejected(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="C", rhs_smiles="C",
                 arrow="circular")
    assert "error" in res
    assert "arrow" in res["error"].lower()


def test_make_reaction_scheme_reversible_arrow_preserved(app):
    from orgchem.agent.actions import invoke
    res = invoke("make_reaction_scheme",
                 lhs_smiles="CCO", rhs_smiles="CC=O",
                 arrow="reversible")
    assert res["arrow"] == "reversible"


# ---- round trip ------------------------------------------------

def test_open_edit_export_roundtrip(app, tmp_path):
    """End-to-end: open the dialog with a seed, clear, build a
    new structure via the panel, export to mol-block, read back."""
    from orgchem.agent.actions import invoke
    from orgchem.gui.dialogs.drawing_tool import DrawingToolDialog

    invoke("open_drawing_tool", smiles="CCO")
    invoke("drawing_clear")
    # Replace canvas by driving the panel directly via singleton.
    DrawingToolDialog._instance.panel.set_structure_from_smiles(
        "c1ccncc1")  # pyridine
    out = tmp_path / "pyridine.mol"
    res = invoke("drawing_export", path=str(out))
    assert res.get("saved") is True
    # Read back via RDKit to confirm mol-block is sane.
    mol = Chem.MolFromMolFile(str(out))
    assert mol is not None
    assert Chem.CanonSmiles(Chem.MolToSmiles(mol)) == \
           Chem.CanonSmiles("c1ccncc1")
