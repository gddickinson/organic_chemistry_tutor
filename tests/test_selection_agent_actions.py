"""Phase 34f round 119 — tests for the selection-aware agent
actions (`select_residues`, `get_selection`, `clear_selection`)."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("pytestqt", reason="pytest-qt not installed")


_FIXTURE = """\
HEADER    TEST                                     01-JAN-26   1TST
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 20.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 20.00           C
ATOM      3  CA  HIS A   3       7.600   0.000   0.000  1.00 20.00           C
ATOM      4  CA  ASP A   4      11.400   0.000   0.000  1.00 20.00           C
ATOM      5  CA  SER A   5      15.200   0.000   0.000  1.00 20.00           C
END
"""


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


@pytest.fixture
def _seed_protein_panel(app, tmp_path, monkeypatch):
    """Prime a PDB cache + populate the Proteins-tab sequence panel
    so the agent actions have something to target."""
    import orgchem.sources.pdb as pdb_mod
    cache = tmp_path / "pdb_cache"
    cache.mkdir()
    (cache / "1TST.pdb").write_text(_FIXTURE)
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: cache)

    win = app.window
    proteins = getattr(win, "proteins", None)
    if proteins is None:
        pytest.skip("Proteins panel not instantiated in this build.")
    if not hasattr(proteins, "sequence_panel"):
        pytest.skip("Sequence panel absent — no WebEngine support.")
    proteins._current_pdb = "1TST"
    proteins._last_pockets = None
    proteins._last_contacts = None
    proteins._refresh_sequence_bar()
    return proteins


# ---- select_residues -------------------------------------------

def test_select_residues_sets_bar_selection(_seed_protein_panel, app):
    res = app.call("select_residues", pdb_id="1TST",
                   chain_id="A", start=2, end=4)
    assert res.get("status") == "ok", res
    app.pump(10)
    sel = _seed_protein_panel.sequence_panel.bar.selection()
    assert sel == ("A", 2, 4)


def test_select_residues_swaps_reversed_bounds(_seed_protein_panel, app):
    res = app.call("select_residues", pdb_id="1TST",
                   chain_id="A", start=5, end=2)
    assert res.get("status") == "ok", res
    assert res["start"] == 2 and res["end"] == 5
    app.pump(10)
    sel = _seed_protein_panel.sequence_panel.bar.selection()
    assert sel == ("A", 2, 5)


def test_select_residues_single_residue(_seed_protein_panel, app):
    res = app.call("select_residues", pdb_id="1TST",
                   chain_id="A", start=3, end=3)
    assert res.get("status") == "ok", res
    app.pump(10)
    sel = _seed_protein_panel.sequence_panel.bar.selection()
    assert sel == ("A", 3, 3)


# ---- get_selection ---------------------------------------------

def test_get_selection_returns_current(_seed_protein_panel, app):
    app.call("select_residues", pdb_id="1TST",
             chain_id="A", start=2, end=4)
    app.pump(10)
    got = app.call("get_selection", pdb_id="1TST")
    assert "error" not in got
    assert got["chain_id"] == "A"
    assert got["start"] == 2
    assert got["end"] == 4


def test_get_selection_empty_errors(_seed_protein_panel, app):
    # Clear first, then query.
    _seed_protein_panel.sequence_panel.bar.clear_selection()
    app.pump(10)
    got = app.call("get_selection", pdb_id="1TST")
    assert "error" in got
    assert "No active selection" in got["error"]


# ---- clear_selection --------------------------------------------

def test_clear_selection_empties_bar(_seed_protein_panel, app):
    app.call("select_residues", pdb_id="1TST",
             chain_id="A", start=1, end=5)
    app.pump(10)
    res = app.call("clear_selection", pdb_id="1TST")
    assert res.get("status") == "ok", res
    app.pump(10)
    assert _seed_protein_panel.sequence_panel.bar.selection() is None


# ---- headless / unavailable GUI --------------------------------

def test_select_residues_without_gui_returns_error(app, monkeypatch):
    """If the Proteins panel isn't reachable (e.g. running headless
    but trying to use a missing branch), the action must error
    cleanly rather than crash."""
    from orgchem.agent.controller import main_window as _real_mw
    import orgchem.agent.actions_protein as ap
    monkeypatch.setattr(ap, "_get_sequence_panel", lambda: None)
    res = app.call("select_residues", pdb_id="1TST",
                   chain_id="A", start=1, end=3)
    assert "error" in res


def test_get_selection_without_gui_returns_error(app, monkeypatch):
    import orgchem.agent.actions_protein as ap
    monkeypatch.setattr(ap, "_get_sequence_panel", lambda: None)
    res = app.call("get_selection")
    assert "error" in res


def test_clear_selection_without_gui_returns_error(app, monkeypatch):
    import orgchem.agent.actions_protein as ap
    monkeypatch.setattr(ap, "_get_sequence_panel", lambda: None)
    res = app.call("clear_selection")
    assert "error" in res
