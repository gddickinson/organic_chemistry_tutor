"""Phase PH-3.0 (round 226) — tests for the Pharm Studio
tutorial-curriculum expansion (1 → 13 lessons across all 4 tiers).
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_12_lessons():
    """The PH-3.0 expansion brings pharm from 1 lesson to
    13+ across all 4 tiers."""
    from pharm.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 12


def test_curriculum_covers_all_four_tiers():
    from pharm.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 1


def test_every_lesson_path_exists():
    from pharm.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_has_a_title():
    from pharm.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["title"].strip()


def test_every_lesson_loads_via_loader():
    from pharm.tutorial.curriculum import CURRICULUM
    from pharm.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_lessons_reference_pharm_concepts():
    """Every pharm lesson should reference a pharmacology
    concept somewhere in the body."""
    from pharm.tutorial.curriculum import CURRICULUM
    keywords = (
        "drug", "receptor", "agonist", "kinetics", "target",
        "dose", "clearance", "metabolism", "half-life",
        "pharmacology",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any pharm keyword")
