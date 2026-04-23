"""Tests for Phase 11a — enzyme-mechanism glossary additions (round 31)."""
from __future__ import annotations
import pytest


_EXPECTED_TERMS = [
    "Catalytic triad",
    "General acid-base catalysis",
    "Aspartic protease",
    "Oxyanion hole",
    "In-line phosphoryl transfer",
    "Covalent intermediate",
    "Schiff base",
    "Tetrahedral intermediate",
]


@pytest.mark.parametrize("term", _EXPECTED_TERMS)
def test_enzyme_glossary_term_present(term):
    from orgchem.db.seed_glossary import _GLOSSARY
    terms = {row["term"] for row in _GLOSSARY}
    assert term in terms, (
        f"Expected {term!r} in glossary seed after round 31")


def test_enzyme_mechanism_category_used():
    from orgchem.db.seed_glossary import _GLOSSARY
    cats = {row["category"] for row in _GLOSSARY
            if row["term"] in _EXPECTED_TERMS}
    assert cats == {"enzyme-mechanism"}


def test_seed_version_bumped():
    from orgchem.db.seed_glossary import SEED_VERSION
    assert SEED_VERSION >= 2


def test_all_new_terms_have_definition_and_see_also():
    from orgchem.db.seed_glossary import _GLOSSARY
    for row in _GLOSSARY:
        if row["term"] not in _EXPECTED_TERMS:
            continue
        assert row["definition_md"].strip(), row["term"]
        # Some see_also lists are intentionally empty, but most should
        # cross-link; check at least 5 of 8 have see_also entries.
    with_see = sum(1 for row in _GLOSSARY
                   if row["term"] in _EXPECTED_TERMS and row["see_also"])
    assert with_see >= 5
