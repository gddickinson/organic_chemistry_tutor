"""Phase 48e (round 174) — tests for the isomerism tutorial
lesson.
"""
from __future__ import annotations
from pathlib import Path

import pytest


def test_lesson_file_exists():
    """The new round-174 isomerism lesson markdown must exist
    on disk."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        (l for l in CURRICULUM["intermediate"]
         if "isomerism" in l["title"].lower()),
        None,
    )
    assert target is not None, \
        "Isomerism lesson missing from CURRICULUM"
    path = Path(target["path"])
    assert path.exists(), f"lesson file missing at {path}"


def test_lesson_registered_at_intermediate_level():
    """The new lesson must live under the 'intermediate'
    curriculum level + carry the canonical title pattern."""
    from orgchem.tutorial.curriculum import CURRICULUM
    titles = [l["title"] for l in CURRICULUM["intermediate"]]
    assert any("Isomerism" in t for t in titles), \
        f"Isomerism lesson missing from intermediate: {titles}"


def test_lesson_path_follows_convention():
    """Path is `intermediate/11_isomerism.md` — the next
    sequential number after the existing 10_protecting_groups."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    p = Path(target["path"])
    assert p.name == "11_isomerism.md"


# ---- Content invariants ------------------------------------------

def test_lesson_covers_all_seven_relationships():
    """The lesson should mention every entry in the canonical
    RELATIONSHIPS vocabulary so a reader gets the complete
    hierarchy."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    body = Path(target["path"]).read_text().lower()
    for rel in ("identical", "constitutional", "enantiomer",
                "diastereomer", "meso", "tautomer",
                "different molecule"):
        assert rel.lower() in body, \
            f"lesson body should mention {rel!r}"


def test_lesson_cross_links_to_isomer_explorer_dialog():
    """The lesson must point readers at the Phase-48b
    Tools → Isomer relationships… dialog (Ctrl+Shift+B) so
    the worked examples are reproducible."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    body = Path(target["path"]).read_text()
    assert "Isomer relationships" in body
    assert "Ctrl+Shift+B" in body


def test_lesson_cross_links_to_view_isomers_workspace_button():
    """The lesson must mention the Phase-48d round-173
    inline 'View isomers…' workspace button so readers
    discover the one-click entry path."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    body = Path(target["path"]).read_text()
    assert "View isomers" in body


def test_lesson_cross_links_to_round_170_glossary_terms():
    """The lesson must point readers at the 7 isomer-
    vocabulary glossary terms added in Phase 48a (round 170).
    Referencing them by name in the body is the documented
    cross-link mechanism — the autolinker will turn them into
    clickable anchors automatically when the tutorial-panel
    glossary autolink wraps them."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    body = Path(target["path"]).read_text()
    for term in ("Isomerism", "Stereoisomer", "Conformer",
                 "Tautomer", "Atropisomer",
                 "Cis-trans isomerism", "Optical activity"):
        assert term in body, \
            f"lesson should reference glossary term {term!r}"


def test_lesson_includes_worked_example_smiles():
    """The lesson should include at least 3 worked-example
    SMILES that the reader can paste into the dialog —
    proves the lesson has the kind of hands-on content the
    user-flagged design called for."""
    from orgchem.tutorial.curriculum import CURRICULUM
    target = next(
        l for l in CURRICULUM["intermediate"]
        if "isomerism" in l["title"].lower()
    )
    body = Path(target["path"]).read_text()
    expected_examples = [
        "CCCCO",                         # n-butanol
        "CC(C)(C)O",                     # tert-butanol
        "CCC=O",                         # propanal
        "CC(C)=O",                       # acetone
        "C[C@H](O)C(=O)O",               # (R)-lactic acid
        "C[C@@H](O)C(=O)O",              # (S)-lactic acid
        "CC(=O)CC(=O)C",                 # 2,4-pentanedione
    ]
    found = sum(1 for smi in expected_examples if smi in body)
    assert found >= 5, \
        f"only {found} of the worked-example SMILES found; " \
        f"expected ≥ 5"


def test_lesson_intermediate_count_increased_to_11():
    """Phase 48e expansion: the intermediate curriculum
    grew from 10 → 11 lessons."""
    from orgchem.tutorial.curriculum import CURRICULUM
    assert len(CURRICULUM["intermediate"]) >= 11
