"""Lessons must agree on the odours of the limonene and carvone enantiomers.

Beginner lesson 07 once said (S)-limonene smells of lemons while intermediate lesson 31 said pine, and it had the
carvone enantiomers swapped. The lessons now use: (R)-(+)-limonene = oranges / citrus, (S)-(−)-limonene = piney,
turpentine-like; (R)-(−)-carvone = spearmint, (S)-(+)-carvone = caraway.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LESSONS = sorted(p for p in ROOT.glob("*/tutorial/content/**/*.md"))


def _windows(word):
    """Each lesson line mentioning `word`, joined with the next line (sentences wrap)."""
    for p in LESSONS:
        lines = p.read_text(encoding="utf-8").splitlines()
        for i, line in enumerate(lines):
            if word in line.lower():
                yield p, " ".join(lines[i:i + 2]).lower()


def test_lessons_found():
    assert len(LESSONS) > 100


def test_no_lesson_says_s_limonene_smells_of_lemons():
    bad = [(str(p.relative_to(ROOT)), text) for p, text in _windows("limonene") if "lemon" in text]
    assert not bad, bad


def test_limonene_odour_table():
    rows = [t for p, t in _windows("limonene") if t.startswith("| limonene")]
    assert rows, "the beginner stereochemistry table lost its limonene row"
    for row in rows:
        cells = [c.strip() for c in row.split("|")[1:4]]
        assert "orange" in cells[1] and "turpentine" in cells[2], row


def test_carvone_odour_table():
    for _p, row in _windows("carvone"):
        if row.startswith("| carvone"):
            cells = [c.strip() for c in row.split("|")[1:4]]
            assert "spearmint" in cells[1] and "caraway" in cells[2], row  # (R) column, then (S) column
