"""Tests for Phase 24e — binding-contact analyser."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# A small fixture where we know the geometry by construction:
# - ASP102 side chain carboxylate at (0, 0, 0)
# - ARG195 guanidinium at (4, 0, 0)  → salt bridge (4.0 Å)
# - PHE168 ring centred near (7, 0, 0)  — aromatic
# - Ligand LIG (benzene-like 6-ring) centred at (7, 5, 0)   — π-stack
# - Ligand N atom at (1, 0, 0)  → H-bond to ASP-O (1.0 Å heavy-atom dist;
#   within the 3.5 Å cutoff)
_FIXTURE_CONTACTS_PDB = """\
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


def test_h_bond_detected():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    protein = parse_pdb_text(_FIXTURE_CONTACTS_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    hbonds = report.by_kind("h-bond")
    assert hbonds, "expected at least one H-bond between LIG N1 and ASP102-O"
    assert any(c.protein_residue == "ASP102" for c in hbonds)


def test_salt_bridge_detected():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    protein = parse_pdb_text(_FIXTURE_CONTACTS_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    # LIG N1 is close to ARG NH1 (~3 Å) — that's a salt-bridge-style contact
    sb = report.by_kind("salt-bridge")
    assert any(c.protein_residue == "ARG195" for c in sb)


def test_hydrophobic_detected_with_phe():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    protein = parse_pdb_text(_FIXTURE_CONTACTS_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    # Ligand ring C-atoms are near PHE168 aromatic carbons
    phobic = report.by_kind("hydrophobic")
    assert any(c.protein_residue == "PHE168" for c in phobic)


def test_missing_ligand_returns_empty_report():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    protein = parse_pdb_text(_FIXTURE_CONTACTS_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "NOPE")
    assert report.n_contacts == 0


def test_summary_dict_has_by_kind_counts():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.binding_contacts import analyse_binding
    protein = parse_pdb_text(_FIXTURE_CONTACTS_PDB, pdb_id="TEST")
    report = analyse_binding(protein, "LIG")
    s = report.summary()
    assert s["ligand"] == "LIG"
    assert s["n_contacts"] == len(s["contacts"])
    assert isinstance(s["by_kind"], dict)


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_analyse_binding_action_uncached_returns_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("analyse_binding", pdb_id="NONE", ligand_name="LIG")
    assert "error" in r


def test_analyse_binding_action_with_primed_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "TEST.pdb").write_text(_FIXTURE_CONTACTS_PDB)
    r = app.call("analyse_binding", pdb_id="test", ligand_name="lig")
    assert "error" not in r
    assert r["ligand"] == "LIG"
    assert r["n_contacts"] > 0
