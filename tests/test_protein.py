"""Tests for Phase 24a — PDB ingestion + protein parser."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# A minimal PDB fixture: 2-residue dipeptide Ala-Gly on chain A,
# plus one HETATM waters and a ligand (formaldehyde as placeholder).
# Columns are kept exactly per PDB spec.
_FIXTURE_PDB = """\
HEADER    TEST PROTEIN                            01-JAN-26   TEST
TITLE     ALA-GLY DIPEPTIDE + FORMALDEHYDE LIGAND
ATOM      1  N   ALA A   1      -0.966   0.493   1.500  1.00 10.00           N
ATOM      2  CA  ALA A   1       0.257   0.418   0.692  1.00 10.00           C
ATOM      3  C   ALA A   1       1.208  -0.627   1.263  1.00 10.00           C
ATOM      4  O   ALA A   1       0.857  -1.809   1.234  1.00 10.00           O
ATOM      5  CB  ALA A   1       0.932   1.775   0.620  1.00 10.00           C
ATOM      6  N   GLY A   2       2.396  -0.247   1.802  1.00 10.00           N
ATOM      7  CA  GLY A   2       3.336  -1.215   2.319  1.00 10.00           C
ATOM      8  C   GLY A   2       4.756  -0.736   2.108  1.00 10.00           C
ATOM      9  O   GLY A   2       5.667  -1.481   1.738  1.00 10.00           O
HETATM   10  C   FOR B   1      10.000   0.000   0.000  1.00 10.00           C
HETATM   11  O   FOR B   1      11.200   0.000   0.000  1.00 10.00           O
HETATM   12  O   HOH B   2       5.000   5.000   5.000  1.00 30.00           O
END
"""


# ---- Parser --------------------------------------------------------

def test_parse_pdb_text_dipeptide():
    from orgchem.core.protein import parse_pdb_text
    p = parse_pdb_text(_FIXTURE_PDB, pdb_id="TEST")
    assert p.pdb_id == "TEST"
    assert "ALA-GLY" in p.title
    assert len(p.chains) == 1
    chain_a = p.get_chain("A")
    assert chain_a is not None
    assert len(chain_a.residues) == 2
    assert [r.name for r in chain_a.residues] == ["ALA", "GLY"]


def test_sequence_1_letter():
    from orgchem.core.protein import parse_pdb_text
    p = parse_pdb_text(_FIXTURE_PDB)
    assert p.get_chain("A").sequence == "AG"


def test_hetatm_classified_correctly():
    from orgchem.core.protein import parse_pdb_text
    p = parse_pdb_text(_FIXTURE_PDB)
    # HOH gets parked as hetatm but filtered out of ligand_residues
    ligand_names = {r.name for r in p.ligand_residues}
    assert "FOR" in ligand_names
    assert "HOH" not in ligand_names


def test_n_atoms_count():
    from orgchem.core.protein import parse_pdb_text
    p = parse_pdb_text(_FIXTURE_PDB)
    # 9 backbone/sidechain + 3 hetatm atoms
    assert p.n_atoms == 12


def test_summary_dict():
    from orgchem.core.protein import parse_pdb_text
    p = parse_pdb_text(_FIXTURE_PDB)
    s = p.summary()
    assert s["pdb_id"] == ""
    assert s["n_chains"] == 1
    assert "FOR" in s["ligands"]
    assert s["has_water"] is True


def test_infer_element_fallback():
    from orgchem.core.protein import _infer_element
    assert _infer_element("CA") == "C"
    assert _infer_element("OG1") == "O"


# ---- Seeded catalogue --------------------------------------------

def test_seeded_proteins_has_core_targets():
    from orgchem.core.protein import list_seeded_proteins, get_seeded_protein
    ids = {s["pdb_id"] for s in list_seeded_proteins()}
    for must_have in ("2YDO", "1EQG", "1HWK", "1HPV", "4INS", "1D12",
                      # Phase 31l expansion.
                      "1LYZ", "1MBN", "1EMA",
                      "1HHO",       # round 107
                      "1BL8",       # round 114
                      "1AOI",       # round 115 — nucleosome
                      "1IGT",       # round 115 — IgG
                      "5CHA",       # round 116 — chymotrypsin
                      "6LU7"):      # round 116 — SARS-CoV-2 Mpro
        assert must_have in ids
    # Phase 31l CLOSED at 15/15 in round 116.
    assert len(ids) >= 15, f"expected ≥15 seeded proteins, got {len(ids)}"
    assert get_seeded_protein("1EQG").ligand_name.startswith("IBP")
    assert get_seeded_protein("no_such_pdb") is None
    # 1HHO teaching story pairs pedagogically with myoglobin.
    hho = get_seeded_protein("1HHO")
    assert hho is not None
    assert "R-state" in hho.name or "haemoglobin" in hho.name.lower()
    assert "cooperativity" in hho.teaching_story.lower()
    # 1BL8 must reference the selectivity filter story — that's
    # the teaching-point invariant this entry exists for.
    kcsa = get_seeded_protein("1BL8")
    assert kcsa is not None
    assert "KcsA" in kcsa.name or "potassium" in kcsa.name.lower()
    assert "selectivity filter" in kcsa.teaching_story.lower() or \
           "selectivity" in kcsa.teaching_story.lower()
    # 1AOI — nucleosome — teaching story must mention histones
    # (the whole reason this structure is canonical teaching
    # material).
    nuc = get_seeded_protein("1AOI")
    assert nuc is not None
    assert "histone" in nuc.teaching_story.lower()
    # 1IGT — IgG — teaching story must mention CDR / antigen /
    # Fab so students know why this structure appears.
    igg = get_seeded_protein("1IGT")
    assert igg is not None
    story = igg.teaching_story.lower()
    assert "cdr" in story or "antigen" in story or "fab" in story


# ---- Cache layer (no network) -------------------------------------

def test_cached_pdb_path_formats():
    from orgchem.sources.pdb import cached_pdb_path
    p = cached_pdb_path("1abc")
    assert p.name == "1ABC.pdb"


def test_parse_from_cache_or_string_text_mode():
    from orgchem.sources.pdb import parse_from_cache_or_string
    p = parse_from_cache_or_string(_FIXTURE_PDB, treat_as_text=True)
    assert p is not None
    assert p.n_atoms == 12


def test_parse_from_cache_or_string_missing_returns_none(tmp_path, monkeypatch):
    """Point the cache at an empty dir so the lookup misses."""
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = pdb_mod.parse_from_cache_or_string("9XYZ")
    assert r is None


def test_fetch_pdb_rejects_bad_id():
    from orgchem.sources.pdb import fetch_pdb_text
    with pytest.raises(ValueError):
        fetch_pdb_text("not_a_code")


# ---- Agent actions (no network — uses in-memory fixture) ----------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_seeded_proteins_action(app):
    rows = app.call("list_seeded_proteins")
    assert len(rows) >= 6
    assert all("pdb_id" in r for r in rows)


def test_get_protein_info_uncached_returns_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("get_protein_info", pdb_id="9ZZZ")
    assert "error" in r


def test_get_protein_info_with_primed_cache(app, tmp_path, monkeypatch):
    """Seed an entry into a temp cache dir and verify the action returns a summary."""
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    # Prime the cache
    (tmp_path / "TEST.pdb").write_text(_FIXTURE_PDB)
    r = app.call("get_protein_info", pdb_id="test")
    assert "error" not in r
    assert r["n_chains"] == 1


def test_fetch_pdb_action_bad_id(app):
    r = app.call("fetch_pdb", pdb_id="not_a_code")
    assert "error" in r


def test_get_chain_sequence_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "TEST.pdb").write_text(_FIXTURE_PDB)
    r = app.call("get_protein_chain_sequence", pdb_id="test", chain_id="A")
    assert r["sequence"] == "AG"
    # Missing chain:
    r2 = app.call("get_protein_chain_sequence", pdb_id="test", chain_id="Z")
    assert "error" in r2
