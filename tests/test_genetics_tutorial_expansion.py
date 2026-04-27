"""Phase GM-3.0 (round 231) — tests for the Genetics +
Molecular Biology Studio tutorial-curriculum expansion
(1 → 14 lessons across all 4 tiers).

Brings genetics's tutorial scaffold up to par with the
other 6 siblings post the -3 chain.
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_12_lessons():
    """The GM-3.0 expansion brings genetics from 1 lesson to
    14+ across all 4 tiers."""
    from genetics.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 12


def test_curriculum_covers_all_four_tiers():
    from genetics.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 1


def test_every_lesson_path_exists():
    from genetics.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_has_a_title():
    from genetics.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["title"].strip()


def test_every_lesson_loads_via_loader():
    from genetics.tutorial.curriculum import CURRICULUM
    from genetics.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_lessons_reference_genetics_concepts():
    """Every genetics lesson should reference a genetics
    concept somewhere in the body."""
    from genetics.tutorial.curriculum import CURRICULUM
    keywords = (
        "dna", "rna", "gene", "genome", "sequence",
        "crispr", "pcr", "variant", "allele", "chromosome",
        "molecular", "protein",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any genetics keyword")


def test_welcome_lesson_preserved():
    """GM-3.0 must NOT remove the GM-1.0 Welcome lesson."""
    from genetics.tutorial.curriculum import CURRICULUM
    titles = [lesson["title"]
              for lesson in CURRICULUM["beginner"]]
    assert any("welcome" in t.lower() for t in titles)
