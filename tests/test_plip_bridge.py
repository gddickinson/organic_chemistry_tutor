"""Tests for Phase 24i — optional PLIP integration with graceful fallback."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


_FIXTURE_PDB = """\
TITLE     PLIP ADAPTER FIXTURE
ATOM      1  N   ASP A 102       0.000   0.000   0.000  1.00 10.00           N
ATOM      2  CA  ASP A 102       1.000   0.000   0.000  1.00 10.00           C
ATOM      3  CB  ASP A 102       1.500   1.000   0.500  1.00 10.00           C
ATOM      4  CG  ASP A 102       2.500   1.500   0.500  1.00 10.00           C
ATOM      5  OD1 ASP A 102       2.800   1.200   1.700  1.00 10.00           O
ATOM      6  OD2 ASP A 102       3.100   2.300   0.000  1.00 10.00           O
HETATM    7  N1  LIG A 500       5.800   0.000   1.700  1.00 10.00           N
HETATM    8  C1  LIG A 500       5.000   0.500   1.000  1.00 10.00           C
HETATM    9  C2  LIG A 500       4.000   1.000   1.500  1.00 10.00           C
HETATM   10  C3  LIG A 500       3.200   0.800   1.300  1.00 10.00           C
HETATM   11  N2  LIG A 500       3.100   0.300   0.800  1.00 10.00           N
END
"""


# ---------------------------------------------------------------------

def test_plip_available_without_install(monkeypatch):
    """When neither the Python API nor the CLI is present, the probe
    must return False."""
    from orgchem.core import plip_bridge
    import builtins

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "plip" or name.startswith("plip."):
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    monkeypatch.setattr(plip_bridge, "_find_plip_cli", lambda: None)
    assert plip_bridge.plip_available() is False


def test_capabilities_shape(monkeypatch):
    """`capabilities()` always returns the same set of keys."""
    from orgchem.core import plip_bridge
    caps = plip_bridge.capabilities()
    for k in ("available", "python_api", "cli"):
        assert k in caps


def test_fallback_to_builtin_without_plip(monkeypatch):
    """When PLIP is missing and ``require_plip=False``, the adapter
    must fall back to the built-in analyser (engine='builtin')."""
    from orgchem.core import plip_bridge
    from orgchem.core.protein import parse_pdb_text
    import builtins

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "plip" or name.startswith("plip."):
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    monkeypatch.setattr(plip_bridge, "_find_plip_cli", lambda: None)
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="FIX")
    result = plip_bridge.analyse_binding_plip(protein, "LIG")
    assert result.engine == "builtin"
    assert result.report.pdb_id == "FIX"


def test_require_plip_returns_unavailable(monkeypatch):
    """With ``require_plip=True`` the adapter does NOT run the
    fallback — it returns an empty report tagged engine='unavailable'."""
    from orgchem.core import plip_bridge
    from orgchem.core.protein import parse_pdb_text
    import builtins

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "plip" or name.startswith("plip."):
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    monkeypatch.setattr(plip_bridge, "_find_plip_cli", lambda: None)
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="FIX")
    result = plip_bridge.analyse_binding_plip(protein, "LIG",
                                              require_plip=True)
    assert result.engine == "unavailable"
    assert result.report.n_contacts == 0


def test_summary_carries_engine_field(monkeypatch):
    from orgchem.core import plip_bridge
    from orgchem.core.protein import parse_pdb_text
    import builtins

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "plip" or name.startswith("plip."):
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    monkeypatch.setattr(plip_bridge, "_find_plip_cli", lambda: None)
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="FIX")
    s = plip_bridge.analyse_binding_plip(protein, "LIG").summary()
    assert s["engine"] == "builtin"
    assert "notes" in s


# ---------------------------------------------------------------------
# Agent action integration — monkeypatches the cache so no network hit.

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_plip_capabilities_action(app):
    r = app.call("plip_capabilities")
    assert "available" in r
    assert isinstance(r["available"], bool)


def test_analyse_binding_plip_action_fallback(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    from orgchem.core import plip_bridge
    import builtins

    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "FIX.pdb").write_text(_FIXTURE_PDB)

    real_import = builtins.__import__

    def blocked_import(name, *args, **kwargs):
        if name == "plip" or name.startswith("plip."):
            raise ImportError("blocked")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", blocked_import)
    monkeypatch.setattr(plip_bridge, "_find_plip_cli", lambda: None)

    r = app.call("analyse_binding_plip", pdb_id="FIX", ligand_name="LIG")
    assert "error" not in r
    assert r["engine"] in ("builtin", "plip", "plip-cli")


def test_analyse_binding_plip_action_uncached_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("analyse_binding_plip", pdb_id="NOPE", ligand_name="LIG")
    assert "error" in r
