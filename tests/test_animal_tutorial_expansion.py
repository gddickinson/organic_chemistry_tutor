"""Phase AB-3.0 (round 229) — tests for the Animal Biology
Studio tutorial-curriculum expansion.

Closes the -3 tutorial-expansion chain (rounds 224-229, CB-3.0
→ AB-3.0).  Animal curriculum grew from 2 starter lessons
(welcome + platform retrospective) to 14 across all 4 tiers.
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_12_lessons():
    """The AB-3.0 expansion brings animal from 2 lessons to
    14+ across all 4 tiers."""
    from animal.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 12


def test_curriculum_covers_all_four_tiers():
    from animal.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 1


def test_every_lesson_path_exists():
    from animal.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_has_a_title():
    from animal.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["title"].strip()


def test_every_lesson_loads_via_loader():
    from animal.tutorial.curriculum import CURRICULUM
    from animal.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_lessons_reference_animal_concepts():
    """Every animal lesson should reference an animal-biology
    concept somewhere in the body."""
    from animal.tutorial.curriculum import CURRICULUM
    keywords = (
        "animal", "vertebrate", "mammal", "neuron",
        "behaviour", "behavior", "evolution", "organ",
        "hormone", "immunity", "development", "species",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any animal-biology keyword")


def test_platform_retrospective_lesson_preserved():
    """AB-3.0 must NOT remove the platform-retrospective
    lesson from AB-1.0."""
    from animal.tutorial.curriculum import CURRICULUM
    titles = [lesson["title"]
              for lesson in CURRICULUM["beginner"]]
    assert any("retrospective" in t.lower() for t in titles)
