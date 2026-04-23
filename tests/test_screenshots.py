"""Headless tests for the image-export + screenshot pipeline."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("PySide6")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- 2D export ------------------------------------------------------------

def test_export_molecule_2d_png(app, tmp_path):
    out = tmp_path / "caffeine.png"
    r = app.call("export_molecule_2d_by_id", molecule_id=7, path=str(out))
    assert "error" not in r
    assert Path(r["path"]).exists()
    assert r["format"] == "png"
    assert r["size_bytes"] > 1000


def test_export_molecule_2d_svg(app, tmp_path):
    out = tmp_path / "caffeine.svg"
    r = app.call("export_molecule_2d_by_id", molecule_id=7, path=str(out))
    assert "error" not in r
    content = Path(r["path"]).read_text()
    assert content.startswith("<?xml") or "<svg" in content


def test_export_unknown_extension_rejected(app, tmp_path):
    out = tmp_path / "caffeine.xyz"
    with pytest.raises(Exception):
        app.call("export_molecule_2d_by_id", molecule_id=7, path=str(out))


# ---- Screenshots ----------------------------------------------------------

def test_screenshot_main_window(app, tmp_path):
    out = tmp_path / "win.png"
    r = app.call("screenshot_window", path=str(out), settle_ms=100)
    assert "error" not in r
    assert Path(r["path"]).exists()
    assert r["size_bytes"] > 5_000


def test_screenshot_panel_browser(app, tmp_path):
    out = tmp_path / "browser.png"
    r = app.call("screenshot_panel", panel_name="browser", path=str(out), settle_ms=100)
    assert r["resolved"] == "browser"
    assert r["size_bytes"] > 500


def test_screenshot_panel_aliases_work(app, tmp_path):
    r = app.call("screenshot_panel", panel_name="2d", path=str(tmp_path / "a.png"), settle_ms=50)
    assert r["resolved"] == "viewer_2d"
    r = app.call("screenshot_panel", panel_name="properties", path=str(tmp_path / "b.png"), settle_ms=50)
    assert r["resolved"] == "props"


def test_screenshot_unknown_panel_returns_error(app, tmp_path):
    r = app.call("screenshot_panel", panel_name="nope", path=str(tmp_path / "x.png"))
    assert "error" in r
