"""Tests for Phase 24k — nucleic-acid / ligand interaction analyser."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


def _intercalation_pdb() -> str:
    """Synthetic fixture: two stacked base pairs (DG-DC then DG-DC) with
    a planar aromatic ligand (6 carbons) sandwiched between the two
    stacked bases.

    Geometry: bases lie in z = 0 and z = 7 planes, the ligand ring at
    z = 3.5 — exactly halfway. That puts the ligand centroid ≤ 4.5 Å
    from both base centroids, at an angle close to 180°.
    """
    def lines() -> list[str]:
        out = ["TITLE     SYNTHETIC INTERCALATION FIXTURE"]
        serial = 1

        def add(name, resname, chain, seq, x, y, z, elem,
                hetatm=False):
            nonlocal serial
            record = "HETATM" if hetatm else "ATOM  "
            out.append(
                f"{record}{serial:>5d}  {name:<4s}{resname:>3s} "
                f"{chain}{seq:>4d}    "
                f"{x:>8.3f}{y:>8.3f}{z:>8.3f}  1.00 10.00           {elem}"
            )
            serial += 1

        # First pyrimidine-like base (use DC ring atoms) at z = 0
        base_atoms_pyr = [
            ("N1", 0.000, 0.000, 0.000, "N"),
            ("C2", 1.200, 0.000, 0.000, "C"),
            ("O2", 1.900, 1.000, 0.000, "O"),  # minor-groove
            ("N3", 1.800,-1.200, 0.000, "N"),  # minor-groove
            ("C4", 1.000,-2.300, 0.000, "C"),
            ("N4", 1.500,-3.500, 0.000, "N"),  # major-groove
            ("C5", -0.400,-2.300, 0.000, "C"),  # major-groove
            ("C6", -0.900,-1.100, 0.000, "C"),
            ("P",  -3.000, 0.000, 0.000, "P"),
            ("OP1",-4.000, 0.500, 0.000, "O"),
            ("OP2",-3.500,-1.000, 0.000, "O"),
        ]
        for name, x, y, z, elem in base_atoms_pyr:
            add(name, "DC", "A", 1, x, y, z, elem)

        # Second pyrimidine base at z = 7.0 (stacked above)
        for name, x, y, z, elem in base_atoms_pyr:
            add(name, "DC", "A", 2, x, y, z + 7.0, elem)

        # Intercalator ligand — 6-carbon planar ring at z = 3.5
        ring = [
            ("C1", 1.400, 0.000, 3.500, "C"),
            ("C2", 0.700, 1.200, 3.500, "C"),
            ("C3",-0.700, 1.200, 3.500, "C"),
            ("C4",-1.400, 0.000, 3.500, "C"),
            ("C5",-0.700,-1.200, 3.500, "C"),
            ("C6", 0.700,-1.200, 3.500, "C"),
            ("N1", 2.600, 0.000, 3.500, "N"),  # For phosphate / H-bond tests
        ]
        for name, x, y, z, elem in ring:
            add(name, "LIG", "A", 100, x, y, z, elem, hetatm=True)

        out.append("END")
        return out
    return "\n".join(lines())


def _minor_groove_pdb() -> str:
    """A single DC base + a ligand N at 3.0 Å from the minor-groove O2
    atom. Should produce exactly one minor-groove-hb contact."""
    out = ["TITLE     MINOR-GROOVE H-BOND FIXTURE"]
    serial = 1

    def add(name, resname, chain, seq, x, y, z, elem, hetatm=False):
        nonlocal serial
        record = "HETATM" if hetatm else "ATOM  "
        out.append(
            f"{record}{serial:>5d}  {name:<4s}{resname:>3s} "
            f"{chain}{seq:>4d}    "
            f"{x:>8.3f}{y:>8.3f}{z:>8.3f}  1.00 10.00           {elem}"
        )
        serial += 1

    # DC residue with O2 (minor) and N4 (major) atoms plus backbone P.
    add("N1", "DC", "A", 1, 0.000, 0.000, 0.000, "N")
    add("C2", "DC", "A", 1, 1.200, 0.000, 0.000, "C")
    add("O2", "DC", "A", 1, 1.900, 1.000, 0.000, "O")
    add("N3", "DC", "A", 1, 1.800,-1.200, 0.000, "N")
    add("C4", "DC", "A", 1, 1.000,-2.300, 0.000, "C")
    add("N4", "DC", "A", 1, 1.500,-3.500, 0.000, "N")
    add("C5", "DC", "A", 1,-0.400,-2.300, 0.000, "C")
    add("C6", "DC", "A", 1,-0.900,-1.100, 0.000, "C")
    add("P",  "DC", "A", 1,-3.000, 0.000, 0.000, "P")
    add("OP1","DC", "A", 1,-4.000, 0.500, 0.000, "O")
    add("OP2","DC", "A", 1,-3.500,-1.000, 0.000, "O")

    # Ligand N at 3.0 Å from O2 (1.9, 1.0, 0) → place at (1.9, 3.9, 0)
    add("N1", "LIG", "A", 100, 1.900, 3.900, 0.000, "N", hetatm=True)
    # And a ligand O near OP1 for phosphate-contact test (~2.5 Å)
    add("O1", "LIG", "A", 100,-4.500, 2.500, 0.000, "O", hetatm=True)

    out.append("END")
    return "\n".join(out)


# ---------------------------------------------------------------------

def test_intercalation_detected():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    protein = parse_pdb_text(_intercalation_pdb(), pdb_id="INT")
    report = analyse_na_binding(protein, "LIG")
    assert report.by_kind("intercalation"), \
        "ligand ring sandwiched between two bases should be intercalation"


def test_minor_groove_hbond_detected():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    protein = parse_pdb_text(_minor_groove_pdb(), pdb_id="MIN")
    report = analyse_na_binding(protein, "LIG")
    assert report.by_kind("minor-groove-hb"), \
        "N-O pair within 3.5 Å of O2 should be a minor-groove H-bond"


def test_phosphate_contact_detected():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    protein = parse_pdb_text(_minor_groove_pdb(), pdb_id="MIN")
    report = analyse_na_binding(protein, "LIG")
    assert report.by_kind("phosphate-contact"), \
        "ligand O near OP1/OP2 should be flagged as phosphate-contact"


def test_empty_report_for_no_nucleic_acid():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    pure_protein = """\
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 10.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 10.00           C
HETATM    3  C1  LIG A 100       1.000   1.000   1.000  1.00 10.00           C
END
"""
    protein = parse_pdb_text(pure_protein, pdb_id="PROT")
    report = analyse_na_binding(protein, "LIG")
    assert report.n_contacts == 0


def test_missing_ligand_is_empty():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    protein = parse_pdb_text(_minor_groove_pdb(), pdb_id="MIN")
    report = analyse_na_binding(protein, "NOPE")
    assert report.n_contacts == 0


def test_summary_dict_shape():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.na_interactions import analyse_na_binding
    protein = parse_pdb_text(_minor_groove_pdb(), pdb_id="MIN")
    report = analyse_na_binding(protein, "LIG")
    s = report.summary()
    for k in ("pdb_id", "ligand", "n_contacts", "by_kind", "contacts"):
        assert k in s


# ---- Agent action ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_analyse_na_binding_uncached_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("analyse_na_binding", pdb_id="NOPE", ligand_name="LIG")
    assert "error" in r


def test_analyse_na_binding_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "MIN.pdb").write_text(_minor_groove_pdb())
    r = app.call("analyse_na_binding", pdb_id="MIN", ligand_name="LIG")
    assert "error" not in r
    assert r["n_contacts"] >= 1
