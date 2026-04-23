"""Unit tests for reaction rendering and seeding."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")

from orgchem.render.draw_reaction import render_svg, render_png_bytes, export_reaction
from orgchem.messaging.errors import RenderError


# ---- Rendering ------------------------------------------------------------

def test_render_svg_fischer_esterification():
    svg = render_svg("CC(=O)O.CCO>>CC(=O)OCC.O")
    assert svg.lstrip().startswith(("<?xml", "<svg"))
    assert len(svg) > 1000


def test_render_png_bytes_diels_alder():
    png = render_png_bytes("C=CC=C.C=C>>C1=CCCCC1", height=260)
    # PNG magic header
    assert png[:8] == b"\x89PNG\r\n\x1a\n"
    assert len(png) > 1000


def test_export_reaction_svg_and_png(tmp_path):
    svg_path = export_reaction("CBr.[OH-]>>CO.[Br-]", tmp_path / "sn2.svg")
    assert svg_path.exists() and svg_path.stat().st_size > 500

    png_path = export_reaction("CBr.[OH-]>>CO.[Br-]", tmp_path / "sn2.png")
    assert png_path.exists() and png_path.stat().st_size > 500


def test_invalid_reaction_rejected():
    with pytest.raises(RenderError):
        render_svg("not a reaction")


# ---- Seeded database ------------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_reactions_returns_seeded_set(app):
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for expected in ("Fischer esterification",
                     "SN2: methyl bromide + hydroxide",
                     "Diels-Alder: butadiene + ethene",
                     "NaBH4 reduction of acetone"):
        assert expected in names


def test_reactions_includes_phase6_expansion(app):
    """The 2026-04-22 expansion added 10 more named reactions."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    for expected in ("Wittig reaction (propanal + methylidene ylide)",
                     "Claisen condensation (ethyl acetate)",
                     "Suzuki coupling (bromobenzene + phenylboronic acid)",
                     "Michael addition (acetone enolate + methyl vinyl ketone)",
                     "Pinacol rearrangement (pinacol → pinacolone)"):
        assert expected in names, f"missing {expected!r}"
    assert len(rows) >= 26   # 16 Phase-2a + 10 Phase-6 expansion


def test_enzyme_reactions_seeded(app):
    """Phase 16d — at least 2 enzyme reactions present."""
    rows = app.call("list_reactions")
    names = {r["name"] for r in rows}
    assert any("Chymotrypsin" in n for n in names), \
        "Chymotrypsin enzyme reaction missing"
    assert any("Aldolase" in n for n in names), \
        "Aldolase enzyme reaction missing"


def test_show_reaction_by_substring(app):
    result = app.call("show_reaction", name_or_id="Fischer")
    assert "id" in result
    assert "Fischer" in result["name"]


def test_export_reaction_by_id(app, tmp_path):
    rows = app.call("list_reactions", filter="Diels")
    assert rows
    rid = rows[0]["id"]
    out = app.call("export_reaction_by_id",
                   reaction_id=rid, path=str(tmp_path / "da.svg"))
    assert Path(out["path"]).exists()
    assert out["size_bytes"] > 500
