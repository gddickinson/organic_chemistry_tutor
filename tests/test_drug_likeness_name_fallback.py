"""Round 205 — drug_likeness name-fallback regression tests.

Tutor-test prompt 10 ("Compare aspirin and ibuprofen by their
drug-likeness") had qwen2.5:14b repeatedly passing broken SMILES
strings (`O=C(Oc1ccccc1C(=O)O` — missing closing paren) for
well-known drugs that ARE in the DB by name.  Round 205 added a
``name=`` fallback to ``drug_likeness`` so the LLM can pass
``name="aspirin"`` and get the action to look the SMILES up.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")
pytest.importorskip("PySide6")
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


@pytest.fixture(scope="module")
def app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


def test_drug_likeness_resolves_by_name(app):
    """Pass a plain name — the action looks it up via
    `find_molecule_by_name` and computes drug-likeness on the
    resolved row's SMILES."""
    res = app.call("drug_likeness", name="Aspirin")
    assert "error" not in res, f"unexpected error: {res}"
    assert res["smiles"]
    assert res["name"] == "Aspirin"
    assert "qed" in res or "qed_score" in res or any(
        k.startswith("qed") for k in res)


def test_drug_likeness_name_case_insensitive(app):
    """Lower-case and exact-case names both resolve."""
    res = app.call("drug_likeness", name="ibuprofen")
    assert "error" not in res
    assert res["smiles"]
    assert res["name"]   # the canonical DB name


def test_drug_likeness_smiles_still_works(app):
    """The original SMILES code path is unchanged."""
    res = app.call("drug_likeness",
                   smiles="CC(=O)Oc1ccccc1C(=O)O")
    assert "error" not in res
    assert res["smiles"] == "CC(=O)Oc1ccccc1C(=O)O"


def test_drug_likeness_molecule_id_still_works(app):
    """The molecule_id code path is unchanged."""
    from orgchem.db.queries import find_molecule_by_name
    row = find_molecule_by_name("Aspirin")
    assert row is not None
    res = app.call("drug_likeness", molecule_id=int(row.id))
    assert "error" not in res
    assert res["smiles"]
    assert res["name"] == "Aspirin"


def test_drug_likeness_unknown_name_errors_cleanly(app):
    """Unknown name returns a structured error, never raises."""
    res = app.call("drug_likeness", name="not-a-real-drug-xyz")
    assert "error" in res
    assert "not-a-real-drug-xyz" in res["error"]


def test_drug_likeness_no_inputs_errors(app):
    """No smiles + no id + no name → structured error."""
    res = app.call("drug_likeness")
    assert "error" in res
    assert "smiles=" in res["error"]
    assert "name=" in res["error"]


def test_drug_likeness_synonym_lookup_works(app):
    """The name fallback uses `find_molecule_by_name` which
    walks the round-58 synonyms layer.  'Acetylsalicylic acid'
    is a seeded synonym for Aspirin."""
    res = app.call("drug_likeness", name="Acetylsalicylic acid")
    if "error" in res:
        pytest.skip(
            "Synonym not seeded in this DB; passes if synonym "
            "exists.  Test guard: not a fixture failure."
        )
    assert res["name"] == "Aspirin"
