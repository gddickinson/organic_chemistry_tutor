"""Phase GM-1.0 (round 230) — tests for the Genetics +
Molecular Biology Studio starter tutorial.

The deeper Genetics-specific curriculum is queued for a
future GM-3.0 expansion; GM-1.0 ships only the welcome
lesson.
"""
from __future__ import annotations
import pytest


def test_curriculum_has_a_welcome_lesson():
    from genetics.tutorial.curriculum import CURRICULUM
    titles = [lesson["title"]
              for lesson in CURRICULUM["beginner"]]
    assert any("welcome" in t.lower() for t in titles), \
        f"Welcome lesson missing; titles: {titles}"


def test_curriculum_covers_all_four_tier_keys():
    """All 4 tier keys must exist (some empty for GM-1.0)."""
    from genetics.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM


def test_every_lesson_path_exists():
    from genetics.tutorial.curriculum import CURRICULUM
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            assert lesson["path"].exists(), \
                f"missing {tier} lesson at {lesson['path']}"


def test_every_lesson_loads_via_loader():
    from genetics.tutorial.curriculum import CURRICULUM
    from genetics.tutorial.loader import load_lesson
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            md = load_lesson(lesson["path"])
            assert len(md) > 100, \
                f"lesson {lesson['title']!r} too short"


def test_welcome_lesson_references_seventh_sibling():
    from genetics.tutorial.curriculum import CURRICULUM
    from genetics.tutorial.loader import load_lesson
    welcome = CURRICULUM["beginner"][0]
    md = load_lesson(welcome["path"]).lower()
    assert "seventh" in md, \
        "Welcome lesson must mention the 7th-sibling context"


def test_welcome_lesson_references_techniques_catalogue():
    from genetics.tutorial.curriculum import CURRICULUM
    from genetics.tutorial.loader import load_lesson
    welcome = CURRICULUM["beginner"][0]
    md = load_lesson(welcome["path"]).lower()
    # Should mention major catalogue categories
    for keyword in ("pcr", "crispr", "sequencing"):
        assert keyword in md, \
            f"Welcome lesson missing keyword {keyword!r}"
