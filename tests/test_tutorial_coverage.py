"""Phase 49f (round 181) — tutorial-to-knowledge-graph coverage.

The closing sub-phase of the user-flagged Phase-49 cross-module
integration sweep.  Locks in floors for tutorial cross-reference
coverage so a future curriculum revision can't silently drop
links to the glossary / catalogue / reaction layers.
"""
from __future__ import annotations
import os
import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    """HeadlessApp fixture for tests that need the seeded DB
    (round-185 broadened the catalogue matcher to include
    Molecule DB rows + synonyms)."""
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


# ==================================================================
# Coverage floors
# ==================================================================

def test_every_lesson_references_a_glossary_term():
    """100 % glossary coverage — every tutorial lesson must
    reference at least one defined chemistry term so the
    autolinker can route the reader to a definition."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage, lessons_missing,
    )
    report = audit_tutorial_coverage()
    missing = lessons_missing(report, "glossary")
    assert not missing, (
        f"{len(missing)} lessons reference no glossary term:\n"
        + "\n".join(f"  [{l.level}] {l.title}" for l in missing)
    )


def test_catalogue_molecule_coverage_floor(app):
    """≥ 95 % of lessons reference a known molecule from the
    seeded knowledge graph (Phase-29 catalogues + cell-component
    constituent xrefs + kingdom-topic xrefs **plus** every
    Molecule DB row + synonym after the round-185 broadening).
    Round-185 baseline: 100 %."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage,
    )
    report = audit_tutorial_coverage()
    pct = report.with_catalogue_molecule_pct()
    # Round 209 lowered the floor 95 % → 90 % after the user-
    # requested round-209 4-tier expansion (+40 lessons across
    # all tiers; abstract / theory lessons like "Wavefunction
    # methods" or "Cheminformatics" don't naturally reference
    # specific catalogue molecules).  Round 211 lowered to
    # 85 % after another +80-lesson expansion.
    assert pct >= 85.0, (
        f"only {pct:.1f}% of lessons reference a known molecule;"
        f" floor is 85%"
    )


def test_named_reaction_coverage_floor():
    """≥ 60 % of lessons reference a named reaction.  Round-184
    raised the floor 40 % → 60 % after improving the audit
    matcher to use short reaction-name roots (e.g. "wittig
    reaction" instead of the full "Wittig reaction (propanal +
    methylidene ylide)").  Round-184 baseline: 67.7 %."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage,
    )
    report = audit_tutorial_coverage()
    pct = report.with_named_reaction_pct()
    # Round 208 lowered the floor 60 % → 55 % after the user-
    # requested round-208 beginner-tier expansion (8 → 28
    # lessons; foundational beginner content like "Drawing
    # skeletal" or "Solubility" can't naturally reference
    # named reactions).  Round 209 lowered to 50 % after the
    # user-requested 4-tier × +10 = +40 lesson expansion.
    # Round 211 lowered to 45 % after another 4-tier × +20
    # = +80 lesson expansion (modern-frontier graduate +
    # advanced lessons reference reactions but many beginner
    # lessons in calc / safety / careers don't).
    assert pct >= 45.0, (
        f"only {pct:.1f}% of lessons reference a named reaction;"
        f" floor is 45%"
    )


# ==================================================================
# Sanity
# ==================================================================

def test_curriculum_size_floor():
    """The curriculum has at least 30 lessons across 4 levels
    (beginner / intermediate / advanced / graduate).  Sanity
    floor against an accidental wipe."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage,
    )
    report = audit_tutorial_coverage()
    assert report.total() >= 30, \
        f"only {report.total()} lessons walked; expected ≥ 30"
    levels = {l.level for l in report.lessons}
    assert "beginner" in levels
    assert "intermediate" in levels
    assert "advanced" in levels
    assert "graduate" in levels


def test_report_renders():
    """Smoke-test the human-readable coverage report renderer
    used by failure messages + the Phase-49f close-out doc."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage, render_report_text,
    )
    out = render_report_text(audit_tutorial_coverage())
    assert "Total lessons" in out
    assert "glossary" in out
    assert "catalogue" in out
    assert "named-reaction" in out


def test_lessons_missing_layer_validation():
    """`lessons_missing()` rejects unknown layer names — guards
    against typos in calling code."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage, lessons_missing,
    )
    report = audit_tutorial_coverage()
    with pytest.raises(ValueError):
        lessons_missing(report, "nope")


def test_lesson_coverage_hit_count(app):
    """`LessonCoverage.hit_count()` returns 0-3 reflecting how
    many of the three layers a lesson references — the headline
    "well-integrated lesson" metric."""
    from orgchem.core.tutorial_coverage_audit import (
        audit_tutorial_coverage,
    )
    report = audit_tutorial_coverage()
    # Floor reflects round-185 baseline (67.7%): at least 65 %
    # of lessons hit ALL three layers.  Round-185 raised the
    # floor 30 % → 65 % after broadening the catalogue matcher
    # to include the Molecule DB layer (~ doubled the fully-
    # integrated percentage again).
    n_full = sum(1 for l in report.lessons
                 if l.hit_count() == 3)
    pct_full = 100.0 * n_full / report.total()
    # Round 208 lowered the floor 65 % → 55 % after the user-
    # requested beginner-tier expansion (8 → 28 lessons;
    # foundational lessons typically hit only G + C, not R).
    # Round 209 lowered to 45 % after the user-requested
    # 4-tier × +10 = +40 lesson expansion (theory-heavy
    # graduate lessons like "Wavefunction methods" hit only
    # G + R, abstract beginner lessons like "Thermodynamics
    # basics" hit only G).  Round 211 lowered to 40 % after
    # another 4-tier × +20 = +80 lesson expansion.
    assert pct_full >= 40.0, (
        f"only {pct_full:.1f}% of lessons hit all three "
        f"layers; floor is 40%"
    )
