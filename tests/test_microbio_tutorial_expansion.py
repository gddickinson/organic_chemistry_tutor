"""Phase MB-3.0 (round 227) — tests for the Microbiology Studio
tutorial-curriculum expansion (1 → 13 lessons across all 4 tiers).
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_12_lessons():
    """The MB-3.0 expansion brings microbio from 1 lesson to
    13+ across all 4 tiers."""
    from microbio.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 12


def test_curriculum_covers_all_four_tiers():
    from microbio.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 1


def test_every_lesson_path_exists():
    from microbio.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_has_a_title():
    from microbio.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["title"].strip()


def test_every_lesson_loads_via_loader():
    from microbio.tutorial.curriculum import CURRICULUM
    from microbio.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_lessons_reference_microbio_concepts():
    """Every microbio lesson should reference a microbiology
    concept somewhere in the body."""
    from microbio.tutorial.curriculum import CURRICULUM
    keywords = (
        "bacteria", "virus", "fungus", "antibiotic",
        "infection", "microbe", "pathogen", "immunity",
        "resistance", "microbiome", "phage", "antimicrobial",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any microbio keyword")
