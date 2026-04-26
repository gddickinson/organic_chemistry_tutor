"""Tests for Phase 11 — glossary / dictionary of terms."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- Seed ---------------------------------------------------------------

def test_glossary_seeded_with_at_least_40_terms(app):
    rows = app.call("list_glossary")
    assert len(rows) >= 40, f"expected ≥40 glossary terms, got {len(rows)}"


def test_phase_48a_isomer_terms_present(app):
    """Round 170 / Phase 48a — 7 new isomer-vocabulary terms
    seeded into the glossary as part of the isomers exploration
    tool's 4-pronged integration."""
    rows = app.call("list_glossary")
    names = {r["term"] for r in rows}
    for expected in ("Isomerism", "Stereoisomer", "Conformer",
                     "Tautomer", "Atropisomer",
                     "Cis-trans isomerism", "Optical activity"):
        assert expected in names, \
            f"isomer-vocabulary term {expected!r} missing"


def test_expected_core_terms_present(app):
    rows = app.call("list_glossary")
    names = {r["term"] for r in rows}
    for expected in ("SN1", "SN2", "E1", "E2", "Nucleophile",
                     "Electrophile", "Carbocation", "Enantiomer",
                     "R/S configuration", "Aromaticity",
                     "Atom economy", "Diels-Alder reaction",
                     "Transition state", "Curved arrow"):
        assert expected in names, f"missing glossary term: {expected!r}"


def test_categories_cover_syllabus(app):
    rows = app.call("list_glossary")
    cats = {r["category"] for r in rows}
    for expected in ("fundamentals", "stereochemistry", "mechanism",
                     "reactions", "spectroscopy", "synthesis",
                     "lab-technique"):
        assert expected in cats, f"no glossary entries in category {expected!r}"


# ---- define() ---------------------------------------------------------

def test_define_exact_match(app):
    r = app.call("define", term="SN2")
    assert "error" not in r
    assert r["term"] == "SN2"
    assert "backside" in r["definition_md"].lower()
    assert "SN1" in r["see_also"]


def test_define_case_insensitive(app):
    r = app.call("define", term="sn2")
    assert "error" not in r
    assert r["term"] == "SN2"


def test_define_by_alias(app):
    """Looking up 'nucleus-loving' shouldn't work but 'σ bond' should find Sigma bond."""
    # 'σ bond' is aliased to 'Sigma bond'
    r = app.call("define", term="σ bond")
    assert "error" not in r
    assert r["term"] == "Sigma bond"


def test_define_missing_term_returns_error(app):
    r = app.call("define", term="no such term")
    assert "error" in r


# ---- list_glossary() / search_glossary() ------------------------------

def test_list_glossary_filter_by_category(app):
    rows = app.call("list_glossary", category="mechanism")
    assert rows
    for r in rows:
        assert r["category"] == "mechanism"


def test_search_glossary_finds_by_definition_content(app):
    """Searching 'carbocation' should find SN1, E1, and Carbocation itself."""
    hits = app.call("search_glossary", query="carbocation")
    names = {h["term"] for h in hits}
    assert "Carbocation" in names
    assert "SN1" in names


def test_search_glossary_empty_query_returns_empty(app):
    assert app.call("search_glossary", query="") == []


def test_search_glossary_no_match_returns_empty(app):
    rows = app.call("search_glossary", query="x" * 40)
    assert rows == []


# ---- Glossary GUI panel --------------------------------------------

def test_show_term_focuses_tab(app):
    """show_term action should switch to the Glossary tab."""
    r = app.call("show_term", term="SN2")
    assert "error" not in r
    assert r["term"] == "SN2"
    win = app.window
    # Glossary tab should now be current
    current = win.tabs.tabText(win.tabs.currentIndex())
    assert current == "Glossary"


def test_glossary_panel_populates_and_filters(app):
    """Smoke test: the panel reloads when filtered and shows a definition."""
    win = app.window
    panel = win.glossary
    # Focus on a specific term; internal state should change
    found = panel.focus_term("SN2")
    assert found is True
    # Filter-based narrowing
    panel.filter.setText("Nucleo")
    panel._reload()
    count = panel.model.rowCount()
    assert count >= 1


def test_show_term_missing(app):
    r = app.call("show_term", term="xxxxxx no such")
    assert "error" in r
