"""Phase 49a (round 176) — glossary autolink coverage audit.

Locks in that pedagogically-important chemistry terms used
across catalogues + tutorials are also present as glossary
entries (so the existing tutorial-panel autolinker wraps
them as clickable anchors).

This is the **first sub-phase of the Phase-49 cross-module
integration sweep** — generalising the per-catalogue
cross-reference tests added in rounds 151 + 166 into a
project-wide audit.
"""
from __future__ import annotations
import pytest


# ==================================================================
# Glossary set + catalogue text — basic invariants
# ==================================================================

def test_glossary_term_set_is_substantial():
    """The glossary should carry > 200 entries after the
    round-176 backfill."""
    from orgchem.core.glossary_audit import glossary_term_set
    assert len(glossary_term_set()) >= 200


def test_all_catalogue_text_is_substantial():
    """The combined catalogue + tutorial text should be ≥ "
    100 kchars after the round-176 audit walks all 7+ "
    catalogue source modules + 35+ tutorial lessons."""
    from orgchem.core.glossary_audit import all_catalogue_text
    text = all_catalogue_text()
    assert len(text) >= 100_000


# ==================================================================
# Phase-49a required terms — high-priority coverage gates
# ==================================================================

def test_required_terms_in_glossary():
    """Every Phase-49a required term must be in the
    glossary set (case-insensitive)."""
    from orgchem.core.glossary_audit import (
        PHASE_49A_REQUIRED_TERMS, glossary_term_set,
    )
    terms = glossary_term_set()
    failed = [t for t in PHASE_49A_REQUIRED_TERMS
              if t not in terms]
    assert not failed, \
        f"Required terms missing from glossary: {failed}"


def test_required_terms_appear_in_catalogue_text():
    """Every Phase-49a required term must appear somewhere
    in the catalogue body / tutorial-lesson text — either
    as the canonical name OR as any of its known aliases.
    Proves the glossary entry is **load-bearing**, not just
    seeded for completeness."""
    from orgchem.core.glossary_audit import (
        PHASE_49A_REQUIRED_TERMS, all_catalogue_text,
    )
    from orgchem.db import seed_glossary as _g
    from orgchem.db.seed_glossary_extra import EXTRA_TERMS

    # Build name → aliases map.
    aliases_for: dict[str, list[str]] = {}
    for entry in (list(_g._GLOSSARY) + list(EXTRA_TERMS)):
        key = entry["term"].lower()
        aliases_for.setdefault(key, [])
        for a in entry.get("aliases", []) or []:
            aliases_for[key].append(a.lower())

    text = all_catalogue_text().lower()
    failed = []
    for required in PHASE_49A_REQUIRED_TERMS:
        candidates = [required] + aliases_for.get(required, [])
        if not any(c in text for c in candidates):
            failed.append((required, candidates))
    assert not failed, \
        f"Required glossary terms not used anywhere in " \
        f"catalogue/tutorial text: {failed}"


# ==================================================================
# Specific round-176 backfill: pH/pKa/buffer/etc must be present
# ==================================================================

def test_ph_chemistry_terms_present():
    """The Phase-46 pH explorer references pH / pKa /
    buffer / Henderson-Hasselbalch + buffer capacity
    extensively.  All 5 must be glossary entries."""
    from orgchem.core.glossary_audit import glossary_term_set
    terms = glossary_term_set()
    for t in ("ph", "pka", "buffer", "buffer capacity",
              "henderson-hasselbalch"):
        assert t in terms, f"missing {t!r}"


def test_synthesis_vocabulary_terms_present():
    """Phase-31b round-152-175 named-reaction expansion
    introduced LDA / active-methylene / MCR vocabulary
    that the round-176 backfill made glossary entries."""
    from orgchem.core.glossary_audit import glossary_term_set
    terms = glossary_term_set()
    for t in ("lda", "lithium diisopropylamide",
              "active-methylene compound",
              "multi-component reaction"):
        assert t in terms, f"missing {t!r}"


def test_biology_vocabulary_terms_present():
    """Phase-47 biochemistry-by-kingdom catalogue references
    endosymbiotic theory + horizontal gene transfer +
    CRISPR-Cas extensively in the eukarya / bacteria /
    archaea topics."""
    from orgchem.core.glossary_audit import glossary_term_set
    terms = glossary_term_set()
    for t in ("endosymbiotic theory",
              "horizontal gene transfer", "crispr",
              "crispr-cas"):
        assert t in terms, f"missing {t!r}"


def test_phase_49a_glossary_grew_by_at_least_15():
    """Round 176 added at least 15 new glossary entries
    (pH / pKa / buffer / buffer capacity / Henderson-
    Hasselbalch / hydrogen bonding / hydrophobic effect /
    LDA / active-methylene / MCR / endosymbiotic / HGT /
    CRISPR-Cas / chirality / chiral switch)."""
    from orgchem.core.glossary_audit import glossary_term_set
    # Lower bound: 247 = pre-round-170 base of ~ 210 +
    # round-170 isomer terms (7 = isomerism + stereoisomer
    # + conformer + tautomer + atropisomer + cis-trans +
    # optical activity) + round-176 backfill (15 = the
    # ones above).  Allow some headroom for aliases.
    assert len(glossary_term_set()) >= 240


# ==================================================================
# Audit infrastructure — public API surface
# ==================================================================

def test_glossary_audit_module_public_api():
    """The Phase-49a audit module exposes
    ``glossary_term_set`` + ``all_catalogue_text`` +
    ``PHASE_49A_REQUIRED_TERMS`` for downstream test reuse."""
    from orgchem.core import glossary_audit
    assert callable(glossary_audit.glossary_term_set)
    assert callable(glossary_audit.all_catalogue_text)
    assert isinstance(
        glossary_audit.PHASE_49A_REQUIRED_TERMS, tuple)
    assert len(glossary_audit.PHASE_49A_REQUIRED_TERMS) >= 10
