"""Tests for Phase 19c — bioisostere toolkit."""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


# ---- Catalogue -------------------------------------------------------

def test_catalogue_has_core_pairs():
    from orgchem.core.bioisosteres import BIOISOSTERES
    ids = {b.id for b in BIOISOSTERES}
    for required in ("cooh-to-tetrazole", "me-to-cf3",
                     "amide-to-sulfonamide", "phenyl-to-thiophene",
                     "o-to-ch2", "cl-to-f", "ester-to-amide"):
        assert required in ids


def test_list_bioisosteres_has_descriptions():
    from orgchem.core.bioisosteres import list_bioisosteres
    rows = list_bioisosteres()
    assert rows
    for r in rows:
        assert r["label"]
        # Forward templates have long descriptions; reverse templates
        # are allowed to just say "Reverse of X".
        assert r["description"] and len(r["description"]) >= 15


# ---- Engine ----------------------------------------------------------

def test_ibuprofen_cooh_to_tetrazole():
    """Ibuprofen → tetrazole variant is one of the archetypal drug
    optimisation moves; engine must surface it."""
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    assert "error" not in r
    tetrazole_hits = [v for v in r["variants"]
                      if v["template_id"] == "cooh-to-tetrazole"]
    assert tetrazole_hits
    # Tetrazole ring SMARTS should appear somewhere in the product
    assert any("nnn" in v["smiles"] for v in tetrazole_hits)


def test_aryl_chloride_to_fluoride():
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("Cc1ccc(Cl)cc1")
    hits = [v for v in r["variants"] if v["template_id"] == "cl-to-f"]
    assert hits
    assert any("F" in v["smiles"] for v in hits)


def test_cf3_swap_for_methyl_arene():
    """Toluene should gain a -CF3 variant from the CH3→CF3 template."""
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("Cc1ccccc1")
    hits = [v for v in r["variants"] if v["template_id"] == "me-to-cf3"]
    assert hits


def test_self_matches_excluded():
    """A molecule that the template matches against trivially shouldn't
    produce itself as a variant."""
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("CCO")
    for v in r["variants"]:
        assert v["smiles"] != r["target"]


def test_template_filter_narrows_output():
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r_all = suggest_bioisosteres("CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    r_sub = suggest_bioisosteres("CC(C)Cc1ccc(cc1)C(C)C(=O)O",
                                 template_ids=["cooh-to-tetrazole"])
    assert r_sub["n_variants"] < r_all["n_variants"]
    for v in r_sub["variants"]:
        assert v["template_id"] == "cooh-to-tetrazole"


def test_bad_smiles_returns_error():
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("not_a_molecule")
    assert "error" in r


def test_inert_molecule_has_few_or_no_variants():
    """Ethane doesn't have any of the handle groups our templates target."""
    from orgchem.core.bioisosteres import suggest_bioisosteres
    r = suggest_bioisosteres("CC")
    # Only the CH2↔O template could match but ethane has no in-chain CH2
    # between two carbons. Allow 0-1 variants depending on RDKit's SMARTS
    # interpretation — key property is we don't crash.
    assert r["n_variants"] <= 1


# ---- Agent actions ---------------------------------------------------

@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


def test_list_bioisosteres_action(app):
    rows = app.call("list_bioisosteres")
    assert len(rows) >= 8


def test_suggest_bioisosteres_action(app):
    r = app.call("suggest_bioisosteres",
                 smiles="CC(C)Cc1ccc(cc1)C(C)C(=O)O")
    assert "error" not in r
    assert r["n_variants"] >= 3


def test_suggest_bioisosteres_missing_smiles(app):
    r = app.call("suggest_bioisosteres", smiles="bogus")
    assert "error" in r
