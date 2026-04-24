"""Round 94 — regression tests for the ``Tutor-test-*`` pollution
purge helper that prevents authoring-action tests from
accumulating garbage in the user's local DB across runs."""
from __future__ import annotations

import uuid

import pytest


@pytest.fixture(scope="module")
def _app():
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as app:
        yield app


def test_purge_targets_only_Tutor_test_prefix(_app):
    """Real seeded rows must survive the purge unscathed.
    Round-94 invariant: cleanup only touches names starting with
    the literal ``Tutor-test-`` prefix."""
    from orgchem.db.cleanup import purge_tutor_test_pollution
    from orgchem.db.models import GlossaryTerm, Molecule
    from orgchem.db.session import session_scope

    with session_scope() as s:
        caffeine_before = s.query(Molecule).filter(
            Molecule.name.like("Caffeine%")).count()
        sn2_before = s.query(GlossaryTerm).filter(
            GlossaryTerm.term == "SN2").count()

    purge_tutor_test_pollution()   # safe; idempotent

    with session_scope() as s:
        caffeine_after = s.query(Molecule).filter(
            Molecule.name.like("Caffeine%")).count()
        sn2_after = s.query(GlossaryTerm).filter(
            GlossaryTerm.term == "SN2").count()

    assert caffeine_after == caffeine_before
    assert sn2_after == sn2_before


def test_purge_is_idempotent(_app):
    from orgchem.db.cleanup import purge_tutor_test_pollution
    # First call may remove something; second must be a no-op.
    _ = purge_tutor_test_pollution()
    counts = purge_tutor_test_pollution()
    assert counts.total() == 0


def test_purge_removes_newly_inserted_Tutor_test_row(_app):
    """Insert a fresh ``Tutor-test-*`` glossary row, purge, and
    check it's gone — while real content stays."""
    from orgchem.agent.actions import invoke
    from orgchem.db.cleanup import purge_tutor_test_pollution
    from orgchem.db.models import GlossaryTerm
    from orgchem.db.session import session_scope

    term = f"Tutor-test-purge-{uuid.uuid4().hex[:8]}"
    res = invoke(
        "add_glossary_term",
        term=term,
        definition_md=(
            "A teaching-term entry created solely to exercise "
            "the round-94 pollution-purge.  Should vanish after "
            "this test finishes."
        ),
        category="test",
    )
    assert "error" not in res, res

    with session_scope() as s:
        before = s.query(GlossaryTerm).filter_by(term=term).count()
    assert before == 1

    counts = purge_tutor_test_pollution()
    assert counts.glossary >= 1

    with session_scope() as s:
        after = s.query(GlossaryTerm).filter_by(term=term).count()
    assert after == 0


def test_purge_counts_stringify_cleanly():
    """PurgeCounts should have a readable repr for log output."""
    from orgchem.db.cleanup import PurgeCounts
    c = PurgeCounts(molecules=3, glossary=12)
    s = str(c)
    assert "molecules=3" in s
    assert "glossary=12" in s
    assert c.total() == 15


def test_purge_tolerates_custom_prefix():
    """Explicit prefix arg must override the default — used in
    future cleanup variants or for testing safety."""
    from orgchem.db.cleanup import purge_tutor_test_pollution
    counts = purge_tutor_test_pollution(prefix="__surely-no-row__")
    assert counts.total() == 0


def test_purge_catches_space_suffix_reaction(_app):
    """Round 97 — regression: the round-94 prefix was ``Tutor-test-``
    (hyphen-terminated), which missed the one historical outlier
    test that used a space (``Tutor-test ester hydrolysis {uuid}``).
    58 such polluted reactions survived in the user's DB until the
    round-97 broadening.  Insert a space-suffixed reaction + confirm
    the current prefix catches it."""
    from orgchem.agent.actions import invoke
    from orgchem.db.cleanup import purge_tutor_test_pollution
    from orgchem.db.models import Reaction
    from orgchem.db.session import session_scope

    name = f"Tutor-test space-suffixed rxn {uuid.uuid4().hex[:8]}"
    res = invoke(
        "add_reaction",
        rxn_name=name,
        reaction_smiles="CC(=O)OC.O>>CC(=O)O.CO",
        description="Regression fixture for the round-97 broader "
                    "prefix catch — must be purged by the default "
                    "Tutor-test prefix.",
        rxn_category="Test",
    )
    assert res["status"] == "accepted", res

    with session_scope() as s:
        before = s.query(Reaction).filter_by(name=name).count()
    assert before == 1

    counts = purge_tutor_test_pollution()
    assert counts.reactions >= 1

    with session_scope() as s:
        after = s.query(Reaction).filter_by(name=name).count()
    assert after == 0
