"""Tests for Phase 4 NMR extension — ¹H + ¹³C shift predictor."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# ---- Core predictor ------------------------------------------------

def test_ethyl_acetate_h_nmr_has_three_environments():
    """EtOAc classical 3-peak ¹H NMR: OCH₂, acetyl CH₃, ethyl CH₃."""
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CCOC(C)=O", "H")
    envs = {p["environment"] for p in r["peaks"]}
    assert any("CH₂ next to O" in e for e in envs)
    assert any("α to carbonyl" in e for e in envs)


def test_aldehyde_downfield_proton():
    """Aldehyde H at 9-10 ppm is the most diagnostic ¹H NMR signature."""
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CC=O", "H")
    hits = [p for p in r["peaks"] if "Aldehyde" in p["environment"]]
    assert hits
    lo, hi = hits[0]["range_ppm"]
    assert lo >= 9.0 and hi <= 11.0


def test_aromatic_ch_range_6_to_8():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("c1ccccc1", "H")
    hits = [p for p in r["peaks"] if "Aromatic" in p["environment"]]
    assert hits
    lo, hi = hits[0]["range_ppm"]
    assert 6 <= lo and hi <= 9


def test_c13_ethyl_acetate_shows_ester_carbonyl():
    """EtOAc ¹³C at ~170 ppm for the ester C=O."""
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CCOC(C)=O", "C")
    hits = [p for p in r["peaks"] if "Ester" in p["environment"]]
    assert hits
    lo, hi = hits[0]["range_ppm"]
    assert 165 <= lo and hi <= 180


def test_c13_ketone_around_200():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CC(=O)C", "C")
    hits = [p for p in r["peaks"] if "Ketone" in p["environment"]]
    assert hits


def test_sorted_high_to_low_ppm():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CCOC(C)=O", "H")
    highs = [max(p["range_ppm"]) for p in r["peaks"]]
    assert highs == sorted(highs, reverse=True)


def test_bad_smiles_returns_error():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("not_a_molecule", "H")
    assert "error" in r


def test_unknown_nucleus_returns_error():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("CCO", "N")
    assert "error" in r


def test_methoxy_singlet_around_3_8():
    from orgchem.core.nmr import predict_shifts
    r = predict_shifts("COc1ccccc1", "H")
    hits = [p for p in r["peaks"] if "methoxy" in p["environment"].lower()]
    assert hits


# ---- Renderer --------------------------------------------------------

def test_render_nmr_png_and_svg(tmp_path):
    from orgchem.render.draw_nmr import export_nmr_spectrum
    png = export_nmr_spectrum("CCOC(C)=O", tmp_path / "etoac_h.png", "H")
    svg = export_nmr_spectrum("CCOC(C)=O", tmp_path / "etoac_c.svg", "C")
    assert png.stat().st_size > 5_000
    text = svg.read_text()
    assert "<svg" in text


def test_render_bad_smiles_raises(tmp_path):
    from orgchem.render.draw_nmr import export_nmr_spectrum
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_nmr_spectrum("bogus", tmp_path / "bad.png")


def test_render_bad_format_raises(tmp_path):
    from orgchem.render.draw_nmr import export_nmr_spectrum
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_nmr_spectrum("CCO", tmp_path / "x.pdf")


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_predict_nmr_shifts_action(app):
    r = app.call("predict_nmr_shifts", smiles="CCOC(C)=O", nucleus="H")
    assert "error" not in r
    assert r["peaks"]


def test_export_nmr_action(app, tmp_path):
    r = app.call("export_nmr_spectrum", smiles="CCOC(C)=O",
                 path=str(tmp_path / "nmr.png"), nucleus="H")
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 5_000


def test_export_nmr_error_path(app, tmp_path):
    r = app.call("export_nmr_spectrum", smiles="xyz bad",
                 path=str(tmp_path / "bad.png"))
    assert "error" in r
