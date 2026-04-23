"""Tests for Phase 19a — SAR series + matrix renderer."""
from __future__ import annotations
import os
from pathlib import Path
import pytest

pytest.importorskip("rdkit")


# ---- Core module ------------------------------------------------------

def test_library_seeded():
    from orgchem.core.sar import SAR_LIBRARY
    ids = {s.id for s in SAR_LIBRARY}
    assert "nsaid-cox" in ids
    assert "statin-hmgcoa" in ids


def test_get_series_returns_expected_fields():
    from orgchem.core.sar import get_series
    s = get_series("nsaid-cox")
    assert s is not None
    assert s.target.startswith("Cyclooxygenase")
    names = {v.name for v in s.variants}
    for expected in ("Aspirin", "Ibuprofen", "Naproxen", "Acetaminophen"):
        assert expected in names


def test_get_series_missing_returns_none():
    from orgchem.core.sar import get_series
    assert get_series("no-such-series") is None


def test_compute_descriptors_has_standard_columns():
    from orgchem.core.sar import get_series
    s = get_series("nsaid-cox")
    rows = s.compute_descriptors()
    assert len(rows) == 4
    for r in rows:
        for k in ("mw", "logp", "tpsa", "qed", "lipinski_violations"):
            assert k in r


def test_activity_values_merged_into_rows():
    from orgchem.core.sar import get_series
    rows = get_series("nsaid-cox").compute_descriptors()
    asp = next(r for r in rows if r["name"] == "Aspirin")
    # Aspirin COX-2 IC50 in the seeded data is ~280 µM
    assert asp["cox2_ic50_uM"] > 100


# ---- Renderer --------------------------------------------------------

def test_render_png_and_svg(tmp_path):
    from orgchem.core.sar import get_series
    from orgchem.render.draw_sar import export_sar_matrix
    s = get_series("nsaid-cox")
    png = export_sar_matrix(s, tmp_path / "nsaid.png")
    svg = export_sar_matrix(s, tmp_path / "nsaid.svg")
    assert png.exists() and png.stat().st_size > 10_000
    assert "<svg" in svg.read_text()


def test_render_unsupported_format_raises(tmp_path):
    from orgchem.core.sar import get_series
    from orgchem.render.draw_sar import export_sar_matrix
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        export_sar_matrix(get_series("nsaid-cox"), tmp_path / "x.pdf")


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_sar_series_action(app):
    rows = app.call("list_sar_series")
    ids = {r["id"] for r in rows}
    assert "nsaid-cox" in ids
    assert "statin-hmgcoa" in ids


def test_get_sar_series_action(app):
    r = app.call("get_sar_series", series_id="nsaid-cox")
    assert "error" not in r
    assert r["target"].startswith("Cyclo")
    assert len(r["rows"]) == 4


def test_get_sar_series_missing_returns_error(app):
    r = app.call("get_sar_series", series_id="nope")
    assert "error" in r


def test_export_sar_matrix_action(app, tmp_path):
    r = app.call("export_sar_matrix", series_id="statin-hmgcoa",
                 path=str(tmp_path / "statins.png"))
    assert "error" not in r
    assert Path(r["path"]).stat().st_size > 10_000


def test_export_sar_matrix_missing_series(app, tmp_path):
    r = app.call("export_sar_matrix", series_id="no-such",
                 path=str(tmp_path / "x.png"))
    assert "error" in r
