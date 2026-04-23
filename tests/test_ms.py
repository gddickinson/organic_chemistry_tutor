"""Tests for Phase 4 MS predictor — monoisotopic mass + isotope pattern."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# ---- Monoisotopic mass -----------------------------------------------

def test_water_monoisotopic_mass():
    from orgchem.core.ms import monoisotopic_mass
    assert abs(monoisotopic_mass("O") - 18.0106) < 0.002


def test_ethanol_mass():
    from orgchem.core.ms import monoisotopic_mass
    assert abs(monoisotopic_mass("CCO") - 46.0419) < 0.002


def test_aspirin_mass():
    from orgchem.core.ms import monoisotopic_mass
    # HRMS reference: 180.0423
    assert abs(monoisotopic_mass("CC(=O)Oc1ccccc1C(=O)O") - 180.0423) < 0.003


def test_caffeine_mass():
    from orgchem.core.ms import monoisotopic_mass
    # HRMS reference: 194.0804
    assert abs(monoisotopic_mass("Cn1cnc2n(C)c(=O)n(C)c(=O)c12") - 194.0804) < 0.003


def test_bad_smiles_mass_is_zero():
    from orgchem.core.ms import monoisotopic_mass
    assert monoisotopic_mass("not_a_smiles") == 0.0


# ---- Isotope pattern -------------------------------------------------

def test_isotope_pattern_chlorobenzene_m_plus_2_near_33():
    """Diagnostic halogen pattern — Cl → M+2 ~33 % of M."""
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("Clc1ccccc1")
    assert "error" not in r
    m_plus_2 = next(p for p in r["peaks"] if p["label"] == "M+2")
    assert 0.28 < m_plus_2["intensity"] < 0.36


def test_isotope_pattern_bromobenzene_m_plus_2_near_100():
    """Br → M+2 ~97 % of M."""
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("Brc1ccccc1")
    m_plus_2 = next(p for p in r["peaks"] if p["label"] == "M+2")
    assert 0.90 < m_plus_2["intensity"] < 1.01


def test_isotope_pattern_dichloromethane_shows_m_plus_4():
    """Two Cl atoms → distinct M+4 peak at ~10 %."""
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("ClCCl")
    m_plus_4 = next((p for p in r["peaks"] if p["label"] == "M+4"), None)
    assert m_plus_4 is not None
    assert 0.05 < m_plus_4["intensity"] < 0.15


def test_isotope_pattern_m_plus_1_scales_with_carbon_count():
    """Each carbon contributes ~1.1 % to M+1 via 13C."""
    from orgchem.core.ms import isotope_pattern
    # Hexane has 6 C; expect ~6.6 % M+1
    r = isotope_pattern("CCCCCC")
    m_plus_1 = next(p for p in r["peaks"] if p["label"] == "M+1")
    assert 0.05 < m_plus_1["intensity"] < 0.09


def test_isotope_pattern_sorted_by_mz():
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("Clc1ccccc1")
    mzs = [p["mz"] for p in r["peaks"]]
    assert mzs == sorted(mzs)


def test_isotope_pattern_first_peak_is_M():
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("CCO")
    assert r["peaks"][0]["label"] == "M"


def test_isotope_pattern_includes_formula():
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("Clc1ccccc1")
    assert r["formula"] == "C6H5Cl"


def test_isotope_pattern_bad_smiles_returns_error():
    from orgchem.core.ms import isotope_pattern
    r = isotope_pattern("not_a_smiles")
    assert "error" in r


# ---- Renderer --------------------------------------------------------

def test_export_ms_spectrum_png_and_svg(tmp_path):
    from orgchem.render.draw_ms import export_ms_spectrum
    png = export_ms_spectrum("Brc1ccccc1", tmp_path / "ms.png")
    svg = export_ms_spectrum("CCO", tmp_path / "ms.svg")
    assert png.stat().st_size > 3_000
    assert "<svg" in svg.read_text()


def test_export_ms_bad_smiles_raises(tmp_path):
    from orgchem.render.draw_ms import export_ms_spectrum
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_ms_spectrum("bogus", tmp_path / "bad.png")


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_predict_ms_action(app):
    r = app.call("predict_ms", smiles="Brc1ccccc1")
    assert "error" not in r
    assert r["formula"] == "C6H5Br"
    assert r["peaks"]


def test_export_ms_action(app, tmp_path):
    r = app.call("export_ms_spectrum", smiles="CCO",
                 path=str(tmp_path / "ms.png"))
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 3_000
