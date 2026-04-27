"""Phase CB-3.0 (round 224) — tests for the Cell Bio Studio
tutorial-curriculum expansion (1 → 13 lessons).
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_12_lessons():
    """The CB-3.0 expansion brings cellbio from 1 lesson to
    13+ across all 4 tiers."""
    from cellbio.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 12


def test_curriculum_covers_all_four_tiers():
    from cellbio.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 1


def test_every_lesson_path_exists():
    from cellbio.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_has_a_title():
    from cellbio.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["title"].strip()


def test_every_lesson_loads_via_loader():
    from cellbio.tutorial.curriculum import CURRICULUM
    from cellbio.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_lessons_reference_signalling_or_cell_concepts():
    """Every cellbio lesson should reference a cell-biology
    or signalling concept somewhere in the body."""
    from cellbio.tutorial.curriculum import CURRICULUM
    keywords = (
        "cell", "signal", "receptor", "kinase", "pathway",
        "ligand", "protein", "membrane",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any cell-biology keyword")
