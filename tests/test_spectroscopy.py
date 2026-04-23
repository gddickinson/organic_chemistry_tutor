"""Tests for Phase 4 — IR band prediction."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")


# ---- Core predictor -------------------------------------------------

def test_acetic_acid_shows_carboxylic_acid_bands():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CC(=O)O")
    groups = [b["group"] for b in r["bands"]]
    # should hit the COOH C=O and the broad H-bonded OH
    assert any("carboxylic acid" in g for g in groups)
    assert any("C=O carboxylic acid" in g for g in groups)


def test_acetic_acid_does_not_trigger_alcohol_oh():
    """Carboxylic acid's OH should route to the COOH-specific band only,
    not fire the alcohol/phenol SMARTS as well."""
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CC(=O)O")
    groups = [b["group"] for b in r["bands"]]
    assert not any("alcohol/phenol" in g for g in groups)


def test_ethanol_shows_alcohol_oh_and_co():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CCO")
    groups = [b["group"] for b in r["bands"]]
    assert any("alcohol/phenol" in g for g in groups)
    assert any("C–O" in g for g in groups)


def test_acetone_vs_acetaldehyde_distinguished_by_aldehyde_doublet():
    """Aldehydes show a diagnostic ~2720-2820 C-H doublet; ketones don't."""
    from orgchem.core.spectroscopy import predict_bands
    ald = predict_bands("CC=O")
    ket = predict_bands("CC(=O)C")
    assert any("Aldehyde" in b["group"] for b in ald["bands"])
    assert not any("Aldehyde" in b["group"] for b in ket["bands"])
    assert any("ketone" in b["group"].lower() for b in ket["bands"])


def test_nitrile_strong_2200_band():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CC#N")
    hits = [b for b in r["bands"] if "C≡N" in b["group"]]
    assert hits
    lo, hi = hits[0]["range_cm1"]
    assert 2200 <= lo <= hi <= 2260


def test_nitro_group_shows_two_bands_note():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("[O-][N+](=O)c1ccccc1")
    hits = [b for b in r["bands"] if "N=O" in b["group"]]
    assert hits
    assert "two bands" in hits[0]["mode"].lower()


def test_aromatic_and_ring_bands():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("c1ccccc1")
    groups = [b["group"] for b in r["bands"]]
    assert any("Aromatic C–H" in g for g in groups)
    assert any("Aromatic C=C" in g for g in groups)


def test_alkane_shows_only_sp3_ch():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CCCCCC")   # hexane
    groups = [b["group"] for b in r["bands"]]
    assert any("Aliphatic C–H" in g for g in groups)
    assert not any("C=O" in g for g in groups)
    assert not any("O–H" in g for g in groups)


def test_bad_smiles_returns_error():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("not a molecule")
    assert "error" in r


def test_bands_sorted_high_to_low():
    from orgchem.core.spectroscopy import predict_bands
    r = predict_bands("CC(=O)NCC(=O)OCC")   # amide + ester on ethyl carbamate-ish
    # Each successive band's range_cm1 upper bound should be ≤ previous.
    highs = [max(b["range_cm1"]) for b in r["bands"]]
    assert highs == sorted(highs, reverse=True)


# ---- Renderer -------------------------------------------------------

def test_export_ir_png_and_svg(tmp_path):
    from orgchem.render.draw_ir import export_ir_spectrum
    p_png = export_ir_spectrum("CC(=O)O", tmp_path / "acetic.png")
    p_svg = export_ir_spectrum("CC(=O)O", tmp_path / "acetic.svg")
    assert p_png.exists() and p_png.stat().st_size > 5_000
    txt = p_svg.read_text()
    assert "<svg" in txt


def test_render_bad_smiles_raises(tmp_path):
    from orgchem.render.draw_ir import export_ir_spectrum
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_ir_spectrum("not a molecule", tmp_path / "bad.png")


def test_render_unsupported_format(tmp_path):
    from orgchem.render.draw_ir import export_ir_spectrum
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_ir_spectrum("CCO", tmp_path / "x.pdf")


# ---- Agent actions --------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_predict_ir_bands_action(app):
    r = app.call("predict_ir_bands", smiles="CC(=O)O")
    assert "error" not in r
    assert r["bands"]


def test_export_ir_action(app, tmp_path):
    r = app.call("export_ir_spectrum",
                 smiles="CC(=O)O",
                 path=str(tmp_path / "acetic.png"))
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 5_000


def test_predict_ir_error_path(app):
    r = app.call("predict_ir_bands", smiles="not a molecule")
    assert "error" in r


def test_export_ir_error_path(app, tmp_path):
    r = app.call("export_ir_spectrum",
                 smiles="bad smiles xyz",
                 path=str(tmp_path / "bad.png"))
    assert "error" in r
