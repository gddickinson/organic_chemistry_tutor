"""Tests for stereochemistry helpers (cross-cutting — 2026-04-22)."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")


# ---- Core API --------------------------------------------------------

def test_l_alanine_is_S():
    """Standard L-alanine (N[C@@H](C)C(=O)O) has one S stereocentre."""
    from orgchem.core.stereo import assign_rs
    rs = assign_rs("N[C@@H](C)C(=O)O")
    assert len(rs) == 1
    assert next(iter(rs.values())) == "S"


def test_d_alanine_is_R():
    """Flipping L to D gives an R centre."""
    from orgchem.core.stereo import assign_rs
    rs = assign_rs("N[C@H](C)C(=O)O")
    assert next(iter(rs.values())) == "R"


def test_cis_trans_2_butene():
    """trans is E, cis is Z."""
    from orgchem.core.stereo import assign_ez
    assert list(assign_ez("C/C=C/C").values()) == ["E"]
    assert list(assign_ez(r"C/C=C\C").values()) == ["Z"]
    # No stereo specified → no descriptor
    assert assign_ez("CC=CC") == {}


def test_enantiomer_inverts_all_centres():
    """R,R-tartaric acid's enantiomer is S,S-tartaric acid (not meso)."""
    from orgchem.core.stereo import enantiomer_of, assign_rs
    # 2,3-dihydroxysuccinic acid — two stereocentres, not meso-symmetric by
    # charge/heterotopic environment. We use a Br-containing variant to avoid
    # the meso ambiguity: (2R,3R)-3-bromo-butane-2-ol and its enantiomer.
    orig = "O[C@@H](C)[C@H](C)Br"
    orig_rs = assign_rs(orig)
    ent = enantiomer_of(orig)
    ent_rs = assign_rs(ent)
    assert len(orig_rs) == len(ent_rs) == 2
    # Every descriptor should have flipped
    flipped = {"R": "S", "S": "R"}
    for idx, v in orig_rs.items():
        # The enantiomer's canonical SMILES may re-number atoms, so
        # compare multisets of values rather than per-atom.
        pass
    assert sorted(flipped[v] for v in orig_rs.values()) == \
        sorted(ent_rs.values())


def test_flip_single_stereocentre():
    """Flipping one atom only inverts that one."""
    from orgchem.core.stereo import flip_stereocentre, assign_rs
    orig = "O[C@@H](C)[C@@H](C)O"
    before = assign_rs(orig)
    atom_indices = list(before.keys())
    first = atom_indices[0]
    new_smi = flip_stereocentre(orig, first)
    after = assign_rs(new_smi)
    # Total count unchanged; at least one descriptor must have flipped
    assert len(before) == len(after)
    assert sorted(after.values()) != sorted(before.values())


def test_flip_nonstereo_atom_raises():
    from orgchem.core.stereo import flip_stereocentre
    with pytest.raises(ValueError):
        flip_stereocentre("CCO", 0)


def test_summarise_achiral_molecule():
    """Benzene has no stereocentres."""
    from orgchem.core.stereo import summarise
    r = summarise("c1ccccc1")
    assert r["n_stereocentres"] == 0
    assert r["is_chiral"] is False
    assert r["rs"] == {}
    assert r["ez"] == []


def test_summarise_unassigned_centres_counted():
    """A SMILES with a stereo-able atom but no wedge gets counted as
    unassigned, not as a null descriptor."""
    from orgchem.core.stereo import summarise
    # 2-chlorobutane without stereo marker — one potential centre
    r = summarise("CC(Cl)CC")
    assert r["n_stereocentres"] == 1
    assert r["unassigned_stereocentres"] == [1]
    assert r["rs"] == {}


# ---- 2D renderer with stereo labels ----------------------------------

def test_render_svg_with_stereo_labels_contains_cip_class():
    """RDKit draws annotation text as paths tagged with ``class='CIP_Code'``."""
    from rdkit import Chem
    from orgchem.render.draw2d import render_svg
    m = Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")
    svg = render_svg(m, show_stereo_labels=True)
    assert svg.startswith(("<?xml", "<svg"))
    # When addStereoAnnotation is on, RDKit emits a CIP_Code-classed path group
    assert "CIP_Code" in svg


def test_render_svg_without_stereo_labels_absent_class():
    from rdkit import Chem
    from orgchem.render.draw2d import render_svg
    m = Chem.MolFromSmiles("CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")
    svg = render_svg(m, show_stereo_labels=False)
    assert "CIP_Code" not in svg


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_assign_stereodescriptors_by_smiles(app):
    r = app.call("assign_stereodescriptors",
                 smiles="CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")
    assert "error" not in r
    assert r["is_chiral"] is True
    assert r["n_stereocentres"] == 1
    (value,) = r["rs"].values()
    assert value in ("R", "S")


def test_assign_stereodescriptors_missing_input(app):
    r = app.call("assign_stereodescriptors")
    assert "error" in r


def test_enantiomer_of_ibuprofen(app):
    r = app.call("enantiomer_of",
                 smiles="CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O")
    assert "error" not in r
    assert r["enantiomer_smiles"] != r["original_smiles"]
    # Both should have exactly one stereocentre
    assert r["n_stereocentres"] == 1


def test_enantiomer_of_by_db_id(app):
    # First find a chiral seeded molecule
    mols = app.call("list_all_molecules")
    # L-Alanine is seeded
    alas = [m for m in mols if "Alanine" in m["name"]]
    assert alas, "L-Alanine should be in seeded set"
    r = app.call("enantiomer_of", molecule_id=alas[0]["id"])
    assert "error" not in r
    assert r["is_chiral"] is True


def test_export_molecule_2d_stereo_svg(app, tmp_path):
    r = app.call("export_molecule_2d_stereo",
                 smiles="CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O",
                 path=str(tmp_path / "r_ibu.svg"))
    assert "error" not in r
    text = Path(r["path"]).read_text()
    assert "CIP_Code" in text


def test_export_molecule_2d_stereo_png(app, tmp_path):
    r = app.call("export_molecule_2d_stereo",
                 smiles="C/C=C/C(=O)O",
                 path=str(tmp_path / "crotonic.png"))
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 3_000


def test_flip_stereocentre_action(app):
    r = app.call("flip_stereocentre",
                 smiles="CC(C)Cc1ccc(cc1)[C@@H](C)C(=O)O",
                 atom_index=10)
    assert "error" not in r
    assert r["original_smiles"] != r["new_smiles"]


def test_flip_invalid_atom_returns_error(app):
    r = app.call("flip_stereocentre",
                 smiles="CCO", atom_index=0)
    assert "error" in r
