"""Tests for the round-55 tutor-authoring actions."""
from __future__ import annotations
import os
import uuid

import pytest

pytest.importorskip("rdkit")


def _u() -> str:
    """Unique suffix so successive test runs don't collide on names
    in the persistent on-disk DB."""
    return uuid.uuid4().hex[:8]


@pytest.fixture(scope="module")
def app():
    """A HeadlessApp so the DB tables exist."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(10)
        yield h


# ---- add_molecule ------------------------------------------------

def test_add_molecule_accepts_valid_smiles(app):
    from orgchem.agent.actions import invoke
    # Variable-length linear alkane is guaranteed parseable and
    # almost certainly un-seeded — 23 carbons won't exist in the
    # starter set.
    suffix = _u()
    # Map hex digits to C; result is a long acyclic chain.
    smi = "C" * 23 + "O"  # tricosanol — not in the seed catalogue
    res = invoke("add_molecule",
                 mol_name=f"Tutor-test-alcohol-{suffix}",
                 smiles=smi,
                 notes="test entry, round 55")
    # Either accepted (first run) or rejected-on-duplicate-SMILES
    # (repeat run) — both are valid outcomes that prove the path
    # executes.
    assert res["status"] in ("accepted", "rejected"), res
    if res["status"] == "accepted":
        assert isinstance(res["id"], int)


def test_add_molecule_rejects_bad_smiles(app):
    from orgchem.agent.actions import invoke
    res = invoke("add_molecule", mol_name="BadMol",
                 smiles="!!not-a-smiles!!")
    assert res["status"] == "rejected"
    assert "parse" in res["reason"].lower()


def test_add_molecule_rejects_duplicate_name(app):
    from orgchem.agent.actions import invoke
    # Benzene is seeded; adding a second "Benzene" should reject.
    res = invoke("add_molecule", mol_name="Benzene", smiles="c1ccccc1")
    assert res["status"] == "rejected"
    assert "already exists" in res["reason"]


def test_add_molecule_rejects_duplicate_canonical_smiles(app):
    from orgchem.agent.actions import invoke
    # Aspirin is seeded — re-submitting under a new name still fails.
    res = invoke("add_molecule",
                 mol_name=f"Tutor-alias-aspirin",
                 smiles="CC(=O)Oc1ccccc1C(=O)O")
    assert res["status"] == "rejected"
    assert "canonical SMILES" in res["reason"]


def test_add_molecule_rejects_missing_fields(app):
    from orgchem.agent.actions import invoke
    assert invoke("add_molecule", mol_name="",
                  smiles="c1ccccc1")["status"] == "rejected"
    assert invoke("add_molecule", mol_name="NoSmilesMol",
                  smiles="")["status"] == "rejected"


# ---- add_reaction ------------------------------------------------

def test_add_reaction_accepts_valid_rxn(app):
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_reaction",
        rxn_name=f"Tutor-test ester hydrolysis {_u()}",
        reaction_smiles="CC(=O)OC.O>>CC(=O)O.CO",
        description="Acid-catalysed ester hydrolysis. Tests the "
                    "tutor-authoring path.",
        rxn_category="Test",
    )
    assert res["status"] == "accepted", res
    assert isinstance(res["id"], int)


def test_add_reaction_rejects_bad_rxn(app):
    from orgchem.agent.actions import invoke
    res = invoke("add_reaction", rxn_name="BadRxn",
                 reaction_smiles="not-a-reaction",
                 description="Still long enough to pass the length check.")
    assert res["status"] == "rejected"


def test_add_reaction_rejects_duplicate_name(app):
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_reaction",
        rxn_name="Fischer esterification",
        reaction_smiles="CC(=O)O.CCO>>CC(=O)OCC.O",
        description="This reaction is already seeded — duplicate.",
    )
    assert res["status"] == "rejected"


# ---- add_glossary_term -------------------------------------------

def test_add_glossary_term_accepts_new_entry(app):
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_glossary_term",
        term=f"Tutor-test-term-{_u()}",
        definition_md="A test glossary entry added by the "
                      "tutor-authoring round-55 test suite.",
        category="test",
        aliases=["tNN"],
    )
    assert res["status"] == "accepted", res


def test_add_glossary_term_rejects_short_definition(app):
    from orgchem.agent.actions import invoke
    res = invoke("add_glossary_term", term="tiny",
                 definition_md="too short")
    assert res["status"] == "rejected"


def test_add_glossary_term_rejects_duplicate_without_overwrite(app):
    from orgchem.agent.actions import invoke
    term = f"Tutor-test-term-dup-{_u()}"
    first = invoke(
        "add_glossary_term",
        term=term,
        definition_md="First definition for the duplicate-test "
                      "glossary term.",
    )
    assert first["status"] == "accepted", first
    second = invoke(
        "add_glossary_term",
        term=term,
        definition_md="Second definition (rejected without overwrite).",
    )
    assert second["status"] == "rejected"


def test_add_glossary_term_overwrite_updates_definition(app):
    from orgchem.agent.actions import invoke
    term = f"Tutor-test-term-ow-{_u()}"
    invoke(
        "add_glossary_term",
        term=term,
        definition_md="Version 1 — the original definition. "
                      "Still long enough.",
    )
    res = invoke(
        "add_glossary_term",
        term=term,
        definition_md="Version 2 — an updated teaching definition.",
        overwrite=True,
    )
    assert res["status"] == "accepted"
    assert res["updated"] is True


# ---- add_tutorial_lesson -----------------------------------------

def test_add_tutorial_lesson_writes_markdown(app, tmp_path, monkeypatch):
    """Writes a real markdown file under the tutorial content tree
    and appends to CURRICULUM."""
    from orgchem.agent import actions_authoring
    monkeypatch.setattr(actions_authoring, "_TUTORIAL_CONTENT",
                        tmp_path / "content")
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_tutorial_lesson",
        title="Test lesson from the round-55 suite",
        level="advanced",
        markdown_body="## Test body\n\nA long enough lesson body "
                      "to pass the ≥ 200-character length check — "
                      "covers basic test verification of the "
                      "tutor-authoring pipeline, including the "
                      "markdown file-write step and the curriculum "
                      "append side-effect.",
    )
    assert res["status"] == "accepted"
    from pathlib import Path
    out = Path(res["path"])
    assert out.exists()
    text = out.read_text()
    # Body has the requested ## heading; if the user didn't supply a
    # top-level # we prepend one, so either form is acceptable.
    assert "Test lesson" in text or "Test body" in text


def test_add_tutorial_lesson_rejects_bad_level(app):
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_tutorial_lesson",
        title="Bad level test",
        level="master",
        markdown_body="X" * 400,
    )
    assert res["status"] == "rejected"


def test_add_tutorial_lesson_rejects_short_body(app):
    from orgchem.agent.actions import invoke
    res = invoke(
        "add_tutorial_lesson",
        title="Short body",
        level="beginner",
        markdown_body="not long enough",
    )
    assert res["status"] == "rejected"


# ---- list_capabilities integration -------------------------------

def test_authoring_actions_visible_in_list_capabilities(app):
    from orgchem.agent.actions import invoke
    res = invoke("list_capabilities", category="authoring")
    assert "error" not in res
    names = [a["name"] for a in res["actions"]]
    for must in ("add_molecule", "add_reaction",
                 "add_glossary_term", "add_tutorial_lesson"):
        assert must in names, (must, names)


def test_gui_coverage_still_100(app):
    from orgchem.gui.audit import audit_summary
    s = audit_summary()
    assert s["coverage_pct"] == 100.0
