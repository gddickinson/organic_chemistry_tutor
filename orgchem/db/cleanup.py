"""Round 94 — housekeeping purge for the ``Tutor-test-*`` rows
left behind by the round-55 authoring-action tests.

Demo 15 (round 73) surfaced that a user's local DB was
accumulating ~165 polluted glossary rows from past test runs
— because the test SMILES / term / name strings intentionally
use ``Tutor-test-*`` prefixes with UUID suffixes to avoid
collisions, but no cleanup fixture removed them.

This module provides a **safe, idempotent** purge that:

- Targets ONLY rows whose name / term starts with
  ``Tutor-test-`` — the exact prefix the tests use; impossible
  to collide with real seeded content.
- Deletes cascading children where appropriate (pathway
  steps for pathway rows).
- Returns counts so callers can log + verify.

Callers: ``tests/conftest.py`` session-teardown fixture,
``scripts/cleanup_tutor_test_pollution.py`` one-shot CLI, and
any user who wants to clean their DB via the agent action.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict

log = logging.getLogger(__name__)


#: The prefix every round-55 authoring-action test uses
#: for its test-data names.  Canonical form is
#: ``Tutor-test-{kind}-{uuid8}`` (hyphen-separated); one
#: historical outlier (test_authoring_actions.py round-55
#: ``Tutor-test ester hydrolysis {uuid}``, since
#: fixed in round 97) used spaces.  Prefix is therefore
#: ``Tutor-test`` without a trailing separator so the purge
#: catches both styles and any future punctuation variants.
#: Still impossible to collide with real seeded content —
#: nothing in the canonical catalogue starts with the
#: literal string "Tutor-test".
TEST_NAME_PREFIX = "Tutor-test"


@dataclass
class PurgeCounts:
    molecules: int = 0
    reactions: int = 0
    glossary: int = 0
    pathways: int = 0
    pathway_steps: int = 0
    tutorials: int = 0

    def total(self) -> int:
        return (self.molecules + self.reactions + self.glossary
                + self.pathways + self.pathway_steps
                + self.tutorials)

    def __str__(self) -> str:
        return (f"PurgeCounts(molecules={self.molecules}, "
                f"reactions={self.reactions}, "
                f"glossary={self.glossary}, "
                f"pathways={self.pathways}, "
                f"pathway_steps={self.pathway_steps}, "
                f"tutorials={self.tutorials})")


def purge_tutor_test_pollution(prefix: str = TEST_NAME_PREFIX
                               ) -> PurgeCounts:
    """Delete every row across Molecule / Reaction / GlossaryTerm /
    SynthesisPathway (+ cascading SynthesisStep) / Tutorial whose
    name starts with *prefix*.  Safe, idempotent.

    Returns a :class:`PurgeCounts` with per-table deletion totals.
    """
    from sqlalchemy import delete, select

    from orgchem.db.models import (
        GlossaryTerm, Molecule, Reaction,
        SynthesisPathway, SynthesisStep,
    )
    from orgchem.db.session import session_scope

    pattern = f"{prefix}%"
    out = PurgeCounts()

    with session_scope() as s:
        # Molecules
        out.molecules = (
            s.execute(delete(Molecule)
                      .where(Molecule.name.like(pattern)))
            .rowcount or 0
        )
        # Reactions
        out.reactions = (
            s.execute(delete(Reaction)
                      .where(Reaction.name.like(pattern)))
            .rowcount or 0
        )
        # Glossary
        out.glossary = (
            s.execute(delete(GlossaryTerm)
                      .where(GlossaryTerm.term.like(pattern)))
            .rowcount or 0
        )
        # Pathways — cascade steps first.  Identify the ids up-front
        # so we can delete their steps before removing the parent.
        path_ids = [
            pid for (pid,) in s.execute(
                select(SynthesisPathway.id)
                .where(SynthesisPathway.name.like(pattern))
            ).all()
        ]
        if path_ids:
            out.pathway_steps = (
                s.execute(delete(SynthesisStep)
                          .where(SynthesisStep.pathway_id.in_(path_ids)))
                .rowcount or 0
            )
            out.pathways = (
                s.execute(delete(SynthesisPathway)
                          .where(SynthesisPathway.id.in_(path_ids)))
                .rowcount or 0
            )
        # Tutorials — add_tutorial_lesson writes markdown files
        # under content/, not the DB, so there's usually nothing
        # to purge here.  Defensive: purge by title in case a
        # future authoring action starts writing to the DB table.
        try:
            from orgchem.db.models import Tutorial
            out.tutorials = (
                s.execute(delete(Tutorial)
                          .where(Tutorial.title.like(pattern)))
                .rowcount or 0
            )
        except Exception:
            pass

    log.info("Tutor-test pollution purge: %s", out)
    return out
