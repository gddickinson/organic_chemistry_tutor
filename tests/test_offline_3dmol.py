"""Tests for Phase 20a — offline 3Dmol.js bundle."""
from __future__ import annotations
import pytest

pytest.importorskip("rdkit")


def test_build_3dmol_html_cdn_default(monkeypatch):
    """With no local bundle, `build_3dmol_html` should emit the CDN URL."""
    import orgchem.render.draw3d as draw3d
    # Force "no local bundle"
    monkeypatch.setattr(draw3d, "local_3dmol_available", lambda: False)
    html = draw3d.build_3dmol_html(["MOLBLOCK"], style="stick")
    assert "3dmol.org/build/3Dmol-min.js" in html
    assert "MOLBLOCK" in html


def test_build_3dmol_html_force_cdn_via_js_src():
    """Passing a custom ``js_src`` always takes the CDN template path."""
    from orgchem.render.draw3d import build_3dmol_html
    html = build_3dmol_html(["MB"], js_src="https://example.com/my-3dmol.js")
    assert "example.com/my-3dmol.js" in html


def test_build_3dmol_html_inlines_local_when_available(monkeypatch, tmp_path):
    """When a local asset exists, its contents are inlined into the HTML
    (making the page self-contained / offline-safe)."""
    import orgchem.render.draw3d as draw3d
    fake_asset = tmp_path / "3Dmol-min.js"
    fake_asset.write_text("// synthetic 3dmol stub\n" + "x" * 2000)
    monkeypatch.setattr(draw3d, "_LOCAL_3DMOL_JS", fake_asset)
    monkeypatch.setattr(draw3d, "local_3dmol_available", lambda: True)

    html = draw3d.build_3dmol_html(["MB"], style="stick")
    # Inlined content should appear; the CDN URL should NOT be in the
    # inline template.
    assert "synthetic 3dmol stub" in html
    assert "https://3dmol.org/build/3Dmol-min.js" not in html


def test_prefer_local_false_keeps_cdn_even_when_local_present(monkeypatch, tmp_path):
    import orgchem.render.draw3d as draw3d
    fake_asset = tmp_path / "3Dmol-min.js"
    fake_asset.write_text("// synthetic\n" + "y" * 2000)
    monkeypatch.setattr(draw3d, "_LOCAL_3DMOL_JS", fake_asset)
    monkeypatch.setattr(draw3d, "local_3dmol_available", lambda: True)

    html = draw3d.build_3dmol_html(["MB"], style="stick",
                                   prefer_local=False)
    assert "https://3dmol.org/build/3Dmol-min.js" in html
    assert "synthetic" not in html


def test_local_path_helper_returns_absolute():
    from orgchem.render.draw3d import local_3dmol_path
    p = local_3dmol_path()
    assert p.is_absolute()
    assert p.name == "3Dmol-min.js"
    # Unit test doesn't require the file to actually exist.
