"""Tests for the static 3D side-by-side reaction renderer (Phase 2c.1)."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")
pytest.importorskip("matplotlib")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def _find(app, substring):
    for r in app.call("list_reactions"):
        if substring in r["name"]:
            return r
    raise AssertionError(f"No reaction matching {substring!r}")


def test_export_reaction_3d_sn2(app, tmp_path):
    row = _find(app, "SN2: methyl bromide")
    out = app.call("export_reaction_3d",
                   reaction_id=row["id"], path=str(tmp_path / "sn2_3d.png"))
    assert "error" not in out, out
    p = Path(out["path"])
    assert p.exists()
    assert p.stat().st_size > 5_000


def test_export_reaction_3d_pcc(app, tmp_path):
    row = _find(app, "PCC oxidation")
    out = app.call("export_reaction_3d",
                   reaction_id=row["id"], path=str(tmp_path / "pcc_3d.png"))
    assert "error" not in out, out
    assert Path(out["path"]).exists()


def test_export_reaction_3d_without_mapping_returns_error(app, tmp_path):
    # Friedel-Crafts isn't in _MAPPED so reaction_smarts_mapped should be NULL
    row = _find(app, "Friedel-Crafts alkylation")
    out = app.call("export_reaction_3d",
                   reaction_id=row["id"], path=str(tmp_path / "fc_3d.png"))
    assert "error" in out
    assert "atom-mapped" in out["error"].lower() or "mapped" in out["error"].lower()


def test_render_png_direct(tmp_path):
    from orgchem.render.draw_reaction_3d import render_png
    out = render_png(
        "[C:1][Br:2].[OH:3]>>[C:1][O:3].[Br:2]",
        tmp_path / "direct.png",
    )
    assert out.exists()


def test_render_png_rejects_unmapped(tmp_path):
    from orgchem.render.draw_reaction_3d import render_png
    from orgchem.messaging.errors import RenderError
    with pytest.raises(RenderError):
        render_png("CC(=O)O.CCO>>CC(=O)OCC.O",  # no atom maps
                   tmp_path / "x.png")
