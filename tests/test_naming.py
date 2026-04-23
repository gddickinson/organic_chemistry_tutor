"""Tests for Phase 12a — IUPAC naming rule catalogue."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Core module ----------------------------------------------------

def test_catalogue_has_reasonable_size():
    from orgchem.naming import RULES
    assert len(RULES) >= 20


def test_every_rule_has_required_fields():
    from orgchem.naming import RULES
    for r in RULES:
        assert r.id and isinstance(r.id, str)
        assert r.title and isinstance(r.title, str)
        assert r.description_md and len(r.description_md) > 30
        assert r.category


def test_unique_rule_ids():
    from orgchem.naming import RULES
    ids = [r.id for r in RULES]
    assert len(ids) == len(set(ids)), "duplicate rule ids"


def test_categories_cover_core_classes():
    from orgchem.naming import rule_categories
    cats = rule_categories()
    for expected in ("alkanes", "alkenes", "alcohols", "carbonyls",
                     "acids", "amines", "aromatics", "heterocycles",
                     "stereochemistry", "general"):
        assert expected in cats, f"missing category {expected!r}"


def test_list_rules_filter_by_category():
    from orgchem.naming import list_rules
    alkanes = list_rules(category="alkanes")
    assert len(alkanes) >= 3
    assert all("alkane" in r["category"] for r in alkanes)


def test_list_rules_unfiltered_returns_all():
    from orgchem.naming import RULES, list_rules
    assert len(list_rules()) == len(RULES)


def test_get_rule_finds_known_id():
    from orgchem.naming import get_rule
    r = get_rule("alkane-parent")
    assert "error" not in r
    assert r["title"].startswith("Pick the longest")
    assert r["example_smiles"] == "CCCCC(C)C"
    assert r["example_iupac"] == "2-methylhexane"


def test_get_rule_missing_id_returns_error():
    from orgchem.naming import get_rule
    r = get_rule("no-such-rule")
    assert "error" in r


# ---- Rules that reference SMILES parse correctly --------------------

def test_all_example_smiles_parse():
    """Every rule's example SMILES should be RDKit-parseable."""
    from rdkit import Chem
    from orgchem.naming import RULES
    for r in RULES:
        if not r.example_smiles:
            continue
        m = Chem.MolFromSmiles(r.example_smiles)
        assert m is not None, \
            f"Rule {r.id!r} has unparseable example: {r.example_smiles!r}"


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_naming_rules_action(app):
    rows = app.call("list_naming_rules")
    assert len(rows) >= 20


def test_get_naming_rule_action(app):
    r = app.call("get_naming_rule", rule_id="alkene-ez")
    assert "error" not in r
    assert "E" in r["description_md"] and "Z" in r["description_md"]


def test_get_naming_rule_missing(app):
    r = app.call("get_naming_rule", rule_id="no-such")
    assert "error" in r


def test_naming_rule_categories_action(app):
    cats = app.call("naming_rule_categories")
    assert "alkanes" in cats
    assert "heterocycles" in cats
