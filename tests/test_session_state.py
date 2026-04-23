"""Tests for Phase 20d — session save/restore."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def test_session_state_defaults():
    from orgchem.core.session_state import SessionState
    s = SessionState()
    assert s.name == "session"
    assert s.version == 1
    assert s.compare_smiles == []
    assert s.hrms_mass is None


def test_yaml_round_trip():
    from orgchem.core.session_state import SessionState
    orig = SessionState(
        name="demo",
        active_tab="Proteins",
        current_molecule_smiles="CC(=O)Oc1ccccc1C(=O)O",
        protein_pdb_id="2YDO",
        protein_ligand_name="CAF",
        compare_smiles=["c1ccccc1", "CCO"],
        hrms_mass=151.06333,
        hrms_ppm_tolerance=5.0,
        notes="debug",
    )
    text = orig.to_yaml()
    round_tripped = SessionState.from_yaml(text)
    assert round_tripped == orig


def test_save_load_round_trip(tmp_path):
    from orgchem.core.session_state import SessionState, save_session, load_session
    s = SessionState(name="hello", active_tab="Molecule Workspace")
    path = tmp_path / "hello.yaml"
    save_session(s, path)
    assert path.exists()
    loaded = load_session(path)
    assert loaded.name == "hello"
    assert loaded.active_tab == "Molecule Workspace"
    assert loaded.saved_at  # non-empty timestamp set on save


def test_unknown_yaml_keys_are_dropped():
    """Forwards-compat: unknown keys in the file should not blow up."""
    from orgchem.core.session_state import SessionState
    text = (
        "name: mystery\n"
        "active_tab: X\n"
        "future_feature: something\n"
        "weird_list: [1, 2, 3]\n"
    )
    s = SessionState.from_yaml(text)
    assert s.name == "mystery"
    assert s.active_tab == "X"


def test_load_missing_file_raises(tmp_path):
    from orgchem.core.session_state import load_session
    with pytest.raises(FileNotFoundError):
        load_session(tmp_path / "nope.yaml")


def test_list_sessions(tmp_path):
    from orgchem.core.session_state import (
        SessionState, save_session, list_sessions,
    )
    save_session(SessionState(name="A"), tmp_path / "A.yaml")
    save_session(SessionState(name="B"), tmp_path / "B.yaml")
    rows = list_sessions(tmp_path)
    assert len(rows) == 2
    assert {r["name"] for r in rows} == {"A", "B"}


def test_default_session_path_sanitises_name(tmp_path):
    from orgchem.core.session_state import default_session_path
    p = default_session_path("weird / name!", directory=tmp_path)
    # Only alnum / dash / underscore survive.
    assert p.name == "weird___name_.yaml"


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_save_then_load_action(app, tmp_path, monkeypatch):
    import orgchem.core.session_state as ss_mod
    monkeypatch.setattr(ss_mod, "sessions_dir", lambda: tmp_path)
    r = app.call("save_session_state",
                 session_name="roundtrip", active_tab="Proteins",
                 protein_pdb_id="2YDO")
    assert "error" not in r
    assert r["name"] == "roundtrip"

    loaded = app.call("load_session_state", path=r["path"])
    assert "error" not in loaded
    assert loaded["name"] == "roundtrip"
    assert loaded["protein_pdb_id"] == "2YDO"


def test_load_missing_action(app, tmp_path):
    r = app.call("load_session_state", path=str(tmp_path / "nope.yaml"))
    assert "error" in r


def test_list_sessions_action(app, tmp_path, monkeypatch):
    import orgchem.core.session_state as ss_mod
    monkeypatch.setattr(ss_mod, "sessions_dir", lambda: tmp_path)
    app.call("save_session_state", session_name="alpha")
    app.call("save_session_state", session_name="beta")
    rows = app.call("list_sessions")
    names = {r["name"] for r in rows}
    assert "alpha" in names and "beta" in names
