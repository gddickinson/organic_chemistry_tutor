"""Phase 48c (round 172) — tests for the isomer agent
actions.
"""
from __future__ import annotations
import os

import pytest


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


@pytest.fixture(autouse=True)
def _reset_dialog_singleton():
    from orgchem.gui.dialogs import isomer_explorer as mod
    mod.IsomerExplorerDialog._instance = None
    yield
    mod.IsomerExplorerDialog._instance = None


# ==================================================================
# find_stereoisomers
# ==================================================================

def test_find_stereoisomers_two_centres(app):
    res = app.call("find_stereoisomers",
                   smiles="CC(O)C(O)CO")
    assert res["input_smiles"] == "CC(O)C(O)CO"
    assert len(res["canonical_smiles_list"]) == 4
    assert res["truncated"] is False


def test_find_stereoisomers_no_centres(app):
    res = app.call("find_stereoisomers", smiles="CCO")
    assert len(res["canonical_smiles_list"]) == 1
    assert res["truncated"] is False


def test_find_stereoisomers_max_results_truncates(app):
    res = app.call("find_stereoisomers",
                   smiles="CC(O)C(O)C(O)C(O)CO",
                   max_results=4)
    assert len(res["canonical_smiles_list"]) <= 4
    assert res["truncated"] is True


def test_find_stereoisomers_unparseable(app):
    res = app.call("find_stereoisomers", smiles="not-a-smiles")
    assert res["canonical_smiles_list"] == []
    assert res["truncated"] is False


# ==================================================================
# find_tautomers
# ==================================================================

def test_find_tautomers_acetone(app):
    res = app.call("find_tautomers", smiles="CC(=O)C")
    assert len(res["canonical_smiles_list"]) >= 2


def test_find_tautomers_pentanedione(app):
    res = app.call("find_tautomers", smiles="CC(=O)CC(=O)C")
    assert len(res["canonical_smiles_list"]) >= 5


def test_find_tautomers_unparseable(app):
    res = app.call("find_tautomers", smiles="not-a-smiles")
    assert res["canonical_smiles_list"] == []


# ==================================================================
# classify_isomer_pair — every classification branch
# ==================================================================

def test_classify_identical(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="CCO", smiles_b="CCO")
    assert r["relationship"] == "identical"
    assert r["formula_a"] == "C2H6O"
    assert r["formula_b"] == "C2H6O"


def test_classify_enantiomer(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="C[C@H](O)C(=O)O",
                 smiles_b="C[C@@H](O)C(=O)O")
    assert r["relationship"] == "enantiomer"


def test_classify_diastereomer(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="C[C@H](O)[C@H](O)C(=O)O",
                 smiles_b="C[C@H](O)[C@@H](O)C(=O)O")
    assert r["relationship"] == "diastereomer"


def test_classify_constitutional(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="CCC=O", smiles_b="CC(C)=O")
    assert r["relationship"] == "constitutional"


def test_classify_tautomer(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="CC(=O)C", smiles_b="CC(O)=C")
    assert r["relationship"] == "tautomer"


def test_classify_different_molecule(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="c1ccccc1", smiles_b="Cc1ccccc1")
    assert r["relationship"] == "different-molecule"


def test_classify_unparseable(app):
    r = app.call("classify_isomer_pair",
                 smiles_a="not-a-smiles", smiles_b="CCO")
    assert r["relationship"] == "different-molecule"


def test_classify_carries_formulas(app):
    """Every classify_isomer_pair result must carry both
    molecular formulas (or None for unparseable inputs)."""
    r = app.call("classify_isomer_pair",
                 smiles_a="C[C@H](O)C(=O)O",
                 smiles_b="C[C@@H](O)C(=O)O")
    assert r["formula_a"] == "C3H6O3"
    assert r["formula_b"] == "C3H6O3"


# ==================================================================
# open_isomer_explorer
# ==================================================================

def test_open_no_args(app):
    res = app.call("open_isomer_explorer")
    assert res["opened"] is True
    assert res["selected"] is False
    assert res["tab"] is None
    assert res["available_tabs"] == [
        "Stereoisomers", "Tautomers", "Classify pair"]


def test_open_with_tab(app):
    res = app.call("open_isomer_explorer", tab="Tautomers")
    assert res["opened"] is True
    assert res["selected"] is True


def test_open_with_unknown_tab(app):
    res = app.call("open_isomer_explorer",
                   tab="NotARealTab")
    assert res["opened"] is True
    assert res["selected"] is False


# ==================================================================
# Audit map registration
# ==================================================================

def test_audit_map_includes_all_four_isomer_actions():
    from orgchem.gui.audit import GUI_ENTRY_POINTS
    for name in ("find_stereoisomers", "find_tautomers",
                 "classify_isomer_pair",
                 "open_isomer_explorer"):
        assert name in GUI_ENTRY_POINTS, \
            f"{name} missing from GUI_ENTRY_POINTS"


def test_isomer_category_actions_registered():
    """All 4 actions live under the `isomer` category in the
    main action registry."""
    from orgchem.agent.actions import registry
    specs = registry()
    isomer_actions = {
        name for name, spec in specs.items()
        if getattr(spec, "category", None) == "isomer"
    }
    for name in ("find_stereoisomers", "find_tautomers",
                 "classify_isomer_pair",
                 "open_isomer_explorer"):
        assert name in isomer_actions, \
            f"{name} missing from `isomer` category; saw " \
            f"{sorted(isomer_actions)}"
