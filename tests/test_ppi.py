"""Tests for Phase 24j — protein-protein interface analyser."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---------------------------------------------------------------------
# Synthetic two-chain PDB fixtures. Each builder places residues on
# specific chains at known geometry so each contact kind is hit by
# construction.

def _make_two_chain_pdb() -> str:
    """Two chains whose interface has one H-bond, one salt bridge,
    one π-stacking pair, and one hydrophobic contact. All geometry
    is picked so the built-in 3.5 / 4.5 / 5.5 / 4.5 Å cutoffs trip.
    """
    lines = ["TITLE     SYNTHETIC TWO-CHAIN INTERFACE"]
    serial = 1

    def add(atom_name, resname, chain, seq, x, y, z, elem):
        nonlocal serial
        lines.append(
            f"ATOM  {serial:>5d}  {atom_name:<3s} {resname} {chain}{seq:>4d}    "
            f"{x:>8.3f}{y:>8.3f}{z:>8.3f}  1.00 10.00           {elem}"
        )
        serial += 1

    # --- Chain A ---------------------------------------------------
    # ASP10 carboxylate — pairs with ARG20 on chain B (salt bridge).
    add("N",   "ASP", "A", 10,  0.000, 0.000, 0.000, "N")
    add("CA",  "ASP", "A", 10,  1.000, 0.000, 0.000, "C")
    add("CB",  "ASP", "A", 10,  1.500, 1.000, 0.500, "C")
    add("CG",  "ASP", "A", 10,  2.500, 1.500, 0.500, "C")
    add("OD1", "ASP", "A", 10,  2.800, 1.200, 1.700, "O")
    add("OD2", "ASP", "A", 10,  3.100, 2.300, 0.000, "O")

    # SER11 hydroxyl — H-bond acceptor pair with chain B backbone N.
    add("N",  "SER", "A", 11,  5.000, 0.000, 0.000, "N")
    add("CA", "SER", "A", 11,  6.000, 0.000, 0.000, "C")
    add("CB", "SER", "A", 11,  6.500, 1.000, 0.500, "C")
    add("OG", "SER", "A", 11,  7.000, 1.800, 1.000, "O")

    # PHE12 — aromatic ring for π-stacking with chain B TYR.
    add("N",   "PHE", "A", 12,  10.000, 0.000, 0.000, "N")
    add("CA",  "PHE", "A", 12,  11.000, 0.000, 0.000, "C")
    add("CB",  "PHE", "A", 12,  11.500, 1.000, 0.500, "C")
    add("CG",  "PHE", "A", 12,  12.500, 1.000, 0.500, "C")
    add("CD1", "PHE", "A", 12,  13.200, 1.900, 0.500, "C")
    add("CD2", "PHE", "A", 12,  13.200, 0.100, 0.500, "C")
    add("CE1", "PHE", "A", 12,  14.500, 1.900, 0.500, "C")
    add("CE2", "PHE", "A", 12,  14.500, 0.100, 0.500, "C")
    add("CZ",  "PHE", "A", 12,  15.200, 1.000, 0.500, "C")

    # LEU13 side-chain carbon — hydrophobic vs chain B LEU.
    add("N",   "LEU", "A", 13,  20.000, 0.000, 0.000, "N")
    add("CA",  "LEU", "A", 13,  21.000, 0.000, 0.000, "C")
    add("CB",  "LEU", "A", 13,  21.500, 1.000, 0.000, "C")
    add("CG",  "LEU", "A", 13,  22.500, 1.000, 0.000, "C")
    add("CD1", "LEU", "A", 13,  23.000, 1.500, 1.000, "C")
    add("CD2", "LEU", "A", 13,  23.000, 1.500,-1.000, "C")

    # --- Chain B ---------------------------------------------------
    # ARG20 guanidinium — salt bridge with ASP10-OD1 (~3.0 Å).
    add("N",   "ARG", "B", 20,  5.800, 0.000, 1.700, "N")
    add("CA",  "ARG", "B", 20,  5.500, 1.000, 1.700, "C")
    add("CB",  "ARG", "B", 20,  5.000, 1.500, 2.500, "C")
    add("CG",  "ARG", "B", 20,  4.500, 2.000, 2.500, "C")
    add("CD",  "ARG", "B", 20,  4.000, 2.500, 2.200, "C")
    add("NE",  "ARG", "B", 20,  3.500, 3.000, 2.000, "N")
    add("NH1", "ARG", "B", 20,  3.000, 1.500, 2.000, "N")
    add("NH2", "ARG", "B", 20,  3.200, 1.800, 2.800, "N")

    # Backbone N at 3.0 Å from SER-OG → H-bond acceptor pair.
    add("N",  "ALA", "B", 21,  7.200, 4.500, 2.500, "N")  # far – padding
    add("CA", "ALA", "B", 21,  8.200, 4.500, 2.500, "C")
    # Put GLN22 carbonyl oxygen close to SER-OG so we definitely get a
    # heavy-atom N/O within 3.5 Å (≥1 N-O pair).
    add("N",  "GLN", "B", 22,  7.600, 2.200, 1.500, "N")
    add("CA", "GLN", "B", 22,  8.600, 2.200, 1.500, "C")

    # TYR30 — aromatic ring ~4.5 Å from chain A PHE centroid.
    add("N",   "TYR", "B", 30,  14.000, 3.500, 0.500, "N")
    add("CA",  "TYR", "B", 30,  14.500, 4.500, 0.500, "C")
    add("CB",  "TYR", "B", 30,  14.700, 5.500, 0.500, "C")
    add("CG",  "TYR", "B", 30,  14.000, 5.000, 0.500, "C")
    add("CD1", "TYR", "B", 30,  13.300, 5.900, 0.500, "C")
    add("CD2", "TYR", "B", 30,  13.300, 4.100, 0.500, "C")
    add("CE1", "TYR", "B", 30,  12.000, 5.900, 0.500, "C")
    add("CE2", "TYR", "B", 30,  12.000, 4.100, 0.500, "C")
    add("CZ",  "TYR", "B", 30,  11.300, 5.000, 0.500, "C")
    add("OH",  "TYR", "B", 30,  10.000, 5.000, 0.500, "O")

    # LEU40 side-chain carbon close to chain A LEU → hydrophobic.
    add("N",   "LEU", "B", 40,  22.500, 3.500, 0.500, "N")
    add("CA",  "LEU", "B", 40,  22.500, 4.500, 0.500, "C")
    add("CB",  "LEU", "B", 40,  22.500, 3.500, 0.500, "C")
    add("CG",  "LEU", "B", 40,  23.000, 3.500, 1.500, "C")
    add("CD1", "LEU", "B", 40,  23.500, 4.000, 2.000, "C")
    add("CD2", "LEU", "B", 40,  24.000, 3.000, 1.500, "C")

    lines.append("END")
    return "\n".join(lines)


def _make_single_chain_pdb() -> str:
    return """\
ATOM      1  CA  ALA A   1       0.000   0.000   0.000  1.00 10.00           C
ATOM      2  CA  GLY A   2       3.800   0.000   0.000  1.00 10.00           C
END
"""


# ---------------------------------------------------------------------
# Core tests

def test_analyse_ppi_detects_all_kinds():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi
    pdb = _make_two_chain_pdb()
    protein = parse_pdb_text(pdb, pdb_id="IFACE")
    interfaces = analyse_ppi(protein)
    assert len(interfaces) == 1
    iface = interfaces[0]
    assert (iface.chain_a, iface.chain_b) == ("A", "B")
    kinds = {c.kind for c in iface.contacts}
    assert "salt-bridge" in kinds
    assert "pi-stacking" in kinds
    assert "hydrophobic" in kinds


def test_ppi_is_empty_for_single_chain():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi
    protein = parse_pdb_text(_make_single_chain_pdb(), pdb_id="MINI")
    assert analyse_ppi(protein) == []


def test_analyse_ppi_pair_labels_residues():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi_pair
    protein = parse_pdb_text(_make_two_chain_pdb(), pdb_id="IFACE")
    iface = protein  # type: ignore[var-annotated]
    iface = analyse_ppi_pair(protein, "A", "B")
    assert iface.n_contacts >= 3
    # Interface-residue sets are labelled with 3-letter + seq id
    assert any(r.startswith("ASP") for r in iface.residues_a)
    assert any(r.startswith("ARG") for r in iface.residues_b)


def test_analyse_ppi_pair_missing_chain_is_empty():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi_pair
    protein = parse_pdb_text(_make_two_chain_pdb(), pdb_id="IFACE")
    iface = analyse_ppi_pair(protein, "A", "Z")
    assert iface.n_contacts == 0


def test_ppi_summary_shape():
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi, ppi_summary
    protein = parse_pdb_text(_make_two_chain_pdb(), pdb_id="IFACE")
    summary = ppi_summary(analyse_ppi(protein))
    assert summary["n_interfaces"] == 1
    assert summary["total_contacts"] >= 3
    iface0 = summary["interfaces"][0]
    for key in ("chain_a", "chain_b", "by_kind",
                "interface_residues_a", "interface_residues_b",
                "contacts"):
        assert key in iface0


def test_ppi_contacts_are_cross_chain():
    """Every reported PPI contact must span two different chains."""
    from orgchem.core.protein import parse_pdb_text
    from orgchem.core.ppi import analyse_ppi
    protein = parse_pdb_text(_make_two_chain_pdb(), pdb_id="IFACE")
    for iface in analyse_ppi(protein):
        for c in iface.contacts:
            assert c.chain_a != c.chain_b


# ---------------------------------------------------------------------
# Agent actions

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_analyse_ppi_action_uncached_error(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    r = app.call("analyse_ppi", pdb_id="NOPE")
    assert "error" in r


def test_analyse_ppi_action_with_cache(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "IFACE.pdb").write_text(_make_two_chain_pdb())
    r = app.call("analyse_ppi", pdb_id="IFACE")
    assert "error" not in r
    assert r["n_interfaces"] == 1
    assert r["total_contacts"] >= 3


def test_analyse_ppi_pair_action(app, tmp_path, monkeypatch):
    import orgchem.sources.pdb as pdb_mod
    monkeypatch.setattr(pdb_mod, "_pdb_cache_dir", lambda: tmp_path)
    (tmp_path / "IFACE.pdb").write_text(_make_two_chain_pdb())
    r = app.call("analyse_ppi_pair", pdb_id="IFACE",
                 chain_a="A", chain_b="B")
    assert "error" not in r
    assert r["n_contacts"] >= 3
    assert r["chain_a"] == "A"
    assert r["chain_b"] == "B"
