"""Phase CB-4.0 (round 232) — tests for the Cell Biology
Studio tutorial-curriculum expansion v4 (13 → ~ 25 lessons).

Round 2 of the new -4 tutorial-expansion chain.  CB-3.0
(round 224, file `test_cellbio_tutorial_expansion.py`)
brought the curriculum to 13 lessons; CB-4.0 adds ~ 12
more for a total of 25.
"""
from __future__ import annotations
import pytest


def test_curriculum_has_at_least_24_lessons():
    """The CB-4.0 expansion brings cellbio from 13 to 24+
    lessons across all 4 tiers."""
    from cellbio.tutorial.curriculum import CURRICULUM
    total = sum(len(lessons)
                for lessons in CURRICULUM.values())
    assert total >= 24


def test_curriculum_covers_all_four_tiers():
    from cellbio.tutorial.curriculum import CURRICULUM
    for tier in ("beginner", "intermediate", "advanced",
                 "graduate"):
        assert tier in CURRICULUM
        assert len(CURRICULUM[tier]) >= 6


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


def test_lessons_reference_cellbio_concepts():
    """Every cellbio lesson should reference a cell-biology
    concept."""
    from cellbio.tutorial.curriculum import CURRICULUM
    keywords = (
        "cell", "organelle", "membrane", "signal",
        "cytoskeleton", "mitochondria", "cycle", "division",
        "receptor", "lipid", "channel",
    )
    for tier, lessons in CURRICULUM.items():
        for lesson in lessons:
            body = lesson["path"].read_text().lower()
            assert any(k in body for k in keywords), \
                (f"lesson {lesson['title']!r} doesn't "
                 f"mention any cellbio keyword")


def test_cb4_specific_lessons_present():
    """The 12 new CB-4.0 lessons must all appear."""
    from cellbio.tutorial.curriculum import CURRICULUM
    titles = []
    for lessons in CURRICULUM.values():
        for lesson in lessons:
            titles.append(lesson["title"].lower())
    needed = (
        "organelles deep-dive",
        "cytoskeleton + motility",
        "membrane lipids + rafts",
        "autophagy + ubiquitin-proteasome system",
        "cell-cell adhesion + extracellular matrix",
        "ion channels + electrical signalling",
        "calcium signalling",
        "cell migration + cancer invasion",
        "lysosomal degradation",
        "organelle contact sites",
        "oxidative stress + redox signalling",
        "intracellular ph",
    )
    for keyword in needed:
        assert any(keyword in t for t in titles), \
            f"CB-4.0 lesson with keyword {keyword!r} missing"
