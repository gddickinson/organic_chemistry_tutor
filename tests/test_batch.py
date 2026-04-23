"""Tests for Phase 20e — batch render."""
from __future__ import annotations
import csv
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# ---- Input parser ---------------------------------------------------

def test_parse_csv(tmp_path):
    from orgchem.core.batch import _parse_input
    p = tmp_path / "in.csv"
    p.write_text("name,smiles\nAspirin,CC(=O)Oc1ccccc1C(=O)O\nEthanol,CCO\n")
    rows = _parse_input(p)
    assert rows == [("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
                    ("Ethanol", "CCO")]


def test_parse_txt(tmp_path):
    from orgchem.core.batch import _parse_input
    p = tmp_path / "in.txt"
    p.write_text(
        "# a comment\n"
        "CCO   Ethanol\n"
        "\n"
        "c1ccccc1\n"            # no name → falls back to SMILES
        "CC(=O)O acetic_acid\n"
    )
    rows = _parse_input(p)
    assert len(rows) == 3
    assert rows[0] == ("Ethanol", "CCO")
    assert rows[1] == ("c1ccccc1", "c1ccccc1")
    assert rows[2] == ("acetic_acid", "CC(=O)O")


def test_parse_csv_missing_smiles_col_raises(tmp_path):
    from orgchem.core.batch import _parse_input
    p = tmp_path / "bad.csv"
    p.write_text("name,structure\nA,CCO\n")
    with pytest.raises(ValueError):
        _parse_input(p)


# ---- Core batch_render ----------------------------------------------

def test_batch_render_smoke(tmp_path):
    from orgchem.core.batch import batch_render
    entries = [("Aspirin", "CC(=O)Oc1ccccc1C(=O)O"),
               ("Ethanol", "CCO")]
    out = tmp_path / "out"
    result = batch_render(entries, out)

    assert result.n_input == 2
    assert result.n_failed == 0
    # Each molecule has 2D + IR artifacts.
    assert (out / "2d" / "Aspirin.png").stat().st_size > 1000
    assert (out / "2d" / "Ethanol.png").stat().st_size > 1000
    assert (out / "ir" / "Aspirin.png").stat().st_size > 1000

    # Descriptor CSV has a header and one row per molecule.
    with result.descriptor_csv.open() as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    assert len(rows) == 2
    assert all("mw" in r and "logp" in r for r in rows)

    # Markdown report exists and references at least the 2D images.
    report = result.report_md.read_text()
    assert "Aspirin" in report
    assert "2d/Aspirin.png" in report


def test_batch_render_handles_bad_smiles(tmp_path):
    from orgchem.core.batch import batch_render
    entries = [("Good", "CCO"),
               ("Bad", "not_a_molecule")]
    result = batch_render(entries, tmp_path / "out2")
    assert result.n_failed >= 1
    # Bad entry appears in failures but shouldn't stop the good one
    assert (tmp_path / "out2" / "2d" / "Good.png").exists()
    # No 2D file for the bad one
    assert not (tmp_path / "out2" / "2d" / "Bad.png").exists()


def test_batch_render_opt_out_of_renders(tmp_path):
    from orgchem.core.batch import batch_render
    result = batch_render([("A", "CCO")],
                          tmp_path / "d",
                          render_2d=False, render_ir=False,
                          write_report=False)
    assert not (tmp_path / "d" / "2d").exists()
    assert not (tmp_path / "d" / "ir").exists()
    # CSV still written
    assert result.descriptor_csv.exists()


# ---- File-entry shortcut --------------------------------------------

def test_batch_render_from_file(tmp_path):
    from orgchem.core.batch import batch_render_from_file
    infile = tmp_path / "in.csv"
    infile.write_text("name,smiles\nA,CCO\nB,c1ccccc1\n")
    result = batch_render_from_file(infile, tmp_path / "out")
    assert result.n_input == 2
    assert result.n_failed == 0


# ---- _safe_name -----------------------------------------------------

def test_safe_name_strips_bad_chars():
    from orgchem.core.batch import _safe_name
    assert _safe_name("Aspirin / 2") == "Aspirin_2"
    assert _safe_name("C#N") == "C_N"
    assert _safe_name("...") == "mol"
