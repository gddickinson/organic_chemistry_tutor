"""Tests for Phase 8 — synthesis pathways."""
from __future__ import annotations
import os
import pytest
from pathlib import Path

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- Seed / listing -----------------------------------------------------

def test_pathways_seeded(app):
    rows = app.call("list_pathways")
    names = {r["name"] for r in rows}
    assert len(rows) >= 12, f"expected at least 12 pathways, got {len(rows)}"
    for expected in ("Wöhler urea synthesis (1828)",
                     "Aspirin (acetylsalicylic acid)",
                     "Paracetamol (acetaminophen)",
                     "Ibuprofen — BHC green-chemistry process",
                     "Caffeine by N-methylation of theobromine",
                     "Aniline from benzene (2-step: nitration + reduction)",
                     "2-Methyl-2-butanol via Grignard (2-step)",
                     "Vanillin from eugenol (2-step via isoeugenol)"):
        assert expected in names, f"missing pathway: {expected!r}"
    # Phase 16a — SPPS
    assert any("SPPS" in n for n in names), \
        "expected a Fmoc SPPS pathway in the seed set"


def test_multistep_pathways_present(app):
    """At least 6 of the seeded pathways must be multi-step."""
    rows = app.call("list_pathways")
    multi = [r for r in rows if r["steps"] >= 2]
    assert len(multi) >= 6, (
        f"expected >=6 multi-step pathways, got {len(multi)}: "
        f"{[(r['name'], r['steps']) for r in multi]}"
    )


def test_bhc_is_three_steps(app):
    rows = app.call("list_pathways", filter="BHC")
    assert rows
    assert rows[0]["steps"] == 3, f"BHC should have 3 steps, got {rows[0]['steps']}"


def test_filter_by_category(app):
    rows = app.call("list_pathways", filter="Industrial")
    assert rows
    for r in rows:
        assert "Industrial" in r["category"] or "Industrial" in r["name"], r


# ---- Show / export ------------------------------------------------------

def test_show_pathway_substring(app):
    r = app.call("show_pathway", name_or_id="Wöhler")
    assert "error" not in r
    assert "Urea" in r["target"]


def test_show_pathway_missing(app):
    r = app.call("show_pathway", name_or_id="no such pathway xyz")
    assert "error" in r


def test_export_pathway_svg(app, tmp_path):
    rows = app.call("list_pathways", filter="Aspirin")
    assert rows
    out = app.call("export_pathway", pathway_id=rows[0]["id"],
                   path=str(tmp_path / "aspirin.svg"))
    assert "error" not in out
    text = Path(out["path"]).read_text()
    assert text.startswith("<svg")
    # Pathway SVG should contain the target name and at least one step
    assert "Aspirin" in text
    assert "Step 1" in text


def test_export_pathway_png(app, tmp_path):
    rows = app.call("list_pathways", filter="BHC")
    assert rows
    out = app.call("export_pathway", pathway_id=rows[0]["id"],
                   path=str(tmp_path / "bhc.png"))
    assert "error" not in out
    path = Path(out["path"])
    assert path.exists()
    # Non-trivial PNG
    assert path.stat().st_size > 5_000


# ---- Direct renderer ----------------------------------------------------

def test_render_pathway_svg_contains_all_steps(app):
    from orgchem.db.session import session_scope
    from orgchem.db.models import SynthesisPathway
    from orgchem.render.draw_pathway import build_svg
    with session_scope() as s:
        bhc = s.query(SynthesisPathway).filter(
            SynthesisPathway.name.ilike("%BHC%")).first()
        assert bhc is not None
        svg = build_svg(bhc)
    assert "Step 1" in svg
    assert "Step 2" in svg
    assert "Step 3" in svg
    # Each step's reagent string should appear somewhere
    assert "HF" in svg
    assert "Raney" in svg
    assert "Pd" in svg
