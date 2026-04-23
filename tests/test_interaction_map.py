"""Tests for Phase 24c — 2D protein-ligand interaction map."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# Reuse the binding-contacts fixture PDB.
_FIXTURE_PDB = """\
TITLE     Contact-analyser fixture
ATOM      1  N   ASP A 102       0.000   1.500   0.000  1.00 10.00           N
ATOM      2  CA  ASP A 102       0.000   0.000   0.000  1.00 10.00           C
ATOM      3  C   ASP A 102       1.500   0.000   0.000  1.00 10.00           C
ATOM      4  O   ASP A 102       2.000   1.000   0.000  1.00 10.00           O
ATOM      5  CB  ASP A 102       0.000  -1.500   0.000  1.00 10.00           C
ATOM      6  CG  ASP A 102       0.500  -2.500   0.000  1.00 10.00           C
ATOM      7  OD1 ASP A 102       0.000  -3.500   0.000  1.00 10.00           O
ATOM      8  OD2 ASP A 102       1.500  -2.500   0.000  1.00 10.00           O
ATOM      9  N   ARG A 195       4.000   1.500   0.000  1.00 10.00           N
ATOM     10  CA  ARG A 195       4.000   0.000   0.000  1.00 10.00           C
ATOM     11  C   ARG A 195       5.500   0.000   0.000  1.00 10.00           C
ATOM     12  O   ARG A 195       6.000   1.000   0.000  1.00 10.00           O
ATOM     13  CB  ARG A 195       4.000  -1.500   0.000  1.00 10.00           C
ATOM     14  NE  ARG A 195       3.000  -2.000   0.000  1.00 10.00           N
ATOM     15  NH1 ARG A 195       2.000  -3.000   0.000  1.00 10.00           N
ATOM     16  NH2 ARG A 195       4.000  -3.000   0.000  1.00 10.00           N
ATOM     17  N   PHE A 168       7.000  -1.500   0.000  1.00 10.00           N
ATOM     18  CA  PHE A 168       7.000   0.000   0.000  1.00 10.00           C
ATOM     19  C   PHE A 168       8.500   0.000   0.000  1.00 10.00           C
ATOM     20  O   PHE A 168       9.000   1.000   0.000  1.00 10.00           O
ATOM     21  CB  PHE A 168       6.500  -0.500   1.500  1.00 10.00           C
ATOM     22  CG  PHE A 168       7.000   0.000   2.500  1.00 10.00           C
ATOM     23  CD1 PHE A 168       7.700   1.200   2.500  1.00 10.00           C
ATOM     24  CD2 PHE A 168       6.800  -0.700   3.700  1.00 10.00           C
ATOM     25  CE1 PHE A 168       8.200   1.700   3.700  1.00 10.00           C
ATOM     26  CE2 PHE A 168       7.300  -0.200   4.900  1.00 10.00           C
ATOM     27  CZ  PHE A 168       8.000   1.000   4.900  1.00 10.00           C
HETATM   30  N1  LIG B   1       1.000   0.000   0.000  1.00 10.00           N
HETATM   31  C1  LIG B   1       7.500   5.000   2.500  1.00 10.00           C
HETATM   32  C2  LIG B   1       6.500   4.500   2.500  1.00 10.00           C
HETATM   33  C3  LIG B   1       6.500   3.500   2.500  1.00 10.00           C
HETATM   34  C4  LIG B   1       7.500   3.000   2.500  1.00 10.00           C
HETATM   35  C5  LIG B   1       8.500   3.500   2.500  1.00 10.00           C
HETATM   36  C6  LIG B   1       8.500   4.500   2.500  1.00 10.00           C
END
"""


def test_render_interaction_map_png(tmp_path):
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    from orgchem.render.draw_interaction_map import export_interaction_map
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    out = export_interaction_map(report, tmp_path / "map.png")
    assert out.exists() and out.stat().st_size > 5_000


def test_render_interaction_map_svg(tmp_path):
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    from orgchem.render.draw_interaction_map import export_interaction_map
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    out = export_interaction_map(report, tmp_path / "map.svg")
    text = out.read_text()
    assert "<svg" in text
    # Ligand label + at least one residue label should appear
    assert "LIG" in text
    assert "ASP" in text or "ARG" in text or "PHE" in text


def test_render_empty_contacts_raises(tmp_path):
    from orgchem.core.binding_contacts import ContactReport
    from orgchem.render.draw_interaction_map import export_interaction_map
    from orgchem.messaging.errors import RenderError
    empty = ContactReport(pdb_id="X", ligand_name="NONE", contacts=[])
    with pytest.raises(RenderError):
        export_interaction_map(empty, tmp_path / "empty.png")


def test_render_bad_format_raises(tmp_path):
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    from orgchem.render.draw_interaction_map import export_interaction_map
    from orgchem.messaging.errors import RenderError
    protein = parse_pdb_text(_FIXTURE_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    with pytest.raises(RenderError):
        export_interaction_map(report, tmp_path / "bad.pdf")


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_export_interaction_map_action_with_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "TEST.pdb").write_text(_FIXTURE_PDB)
    r = app.call("export_interaction_map",
                 pdb_id="test", ligand_name="LIG",
                 path=str(tmp_path / "out.png"))
    assert "error" not in r
    assert r["n_contacts"] > 0
    assert Path(r["path"]).stat().st_size > 5_000


def test_export_interaction_map_missing_ligand(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "TEST.pdb").write_text(_FIXTURE_PDB)
    r = app.call("export_interaction_map",
                 pdb_id="test", ligand_name="NOPE",
                 path=str(tmp_path / "out.png"))
    assert "error" in r
