"""Phase 49a (round 176) — glossary autolink coverage audit.

A test-time helper that walks every catalogue's body text +
every tutorial markdown lesson and checks that pedagogically-
important chemistry terms are covered by the glossary.

Usage from a test::

    from orgchem.core.glossary_audit import (
        glossary_term_set, all_catalogue_text,
    )

    terms = glossary_term_set()
    text = all_catalogue_text().lower()
    for required in ("hydrogen bonding", "henderson-hasselbalch"):
        assert required in text  # the term IS used somewhere
        assert required in terms  # AND the glossary covers it

The point is to make missing-glossary-term failures **visible
at test time** rather than silently slipping through to the
tutorial autolinker.

Pure-headless: no Qt imports.  No DB dependency — reads
glossary entries straight from the seed-file Python data
structures.
"""
from __future__ import annotations
from typing import Iterable, Set


def glossary_term_set() -> Set[str]:
    """Return the lowercase set of every glossary term + every
    alias, across both `seed_glossary._GLOSSARY` and
    `seed_glossary_extra.EXTRA_TERMS`."""
    from orgchem.db import seed_glossary as _g
    from orgchem.db.seed_glossary_extra import EXTRA_TERMS
    out: Set[str] = set()
    for entry in _g._GLOSSARY:
        out.add(entry["term"].lower())
        for a in entry.get("aliases", []) or []:
            out.add(a.lower())
    for entry in EXTRA_TERMS:
        out.add(entry["term"].lower())
        for a in entry.get("aliases", []) or []:
            out.add(a.lower())
    return out


def _catalogue_text_sources() -> Iterable[str]:
    """Walk every shipped catalogue + return its body /
    description text fields as raw strings.  Non-fatal if a
    catalogue isn't importable — yields nothing for that
    source."""
    # Phase-43 cell components
    try:
        from orgchem.core.cell_components import list_components
        for c in list_components():
            yield c.function
            yield c.notes
            for m in c.constituents:
                yield m.role
                yield m.notes
    except Exception:
        pass

    # Phase-42 metabolic pathways
    try:
        from orgchem.core.metabolic_pathways import list_pathways
        for p in list_pathways():
            yield p.overview
            for s in p.steps:
                yield s.notes
    except Exception:
        pass

    # Phase-44 microscopy
    try:
        from orgchem.core.microscopy import list_methods
        for m in list_methods():
            yield m.typical_uses
            yield m.notes
            yield m.contrast_mechanism
    except Exception:
        pass

    # Phase-45 lab reagents
    try:
        from orgchem.core.lab_reagents import list_reagents
        for r in list_reagents():
            yield r.typical_usage
            yield r.notes
            yield r.preparation_notes
    except Exception:
        pass

    # Phase-46 pH explorer (reference cards)
    try:
        from orgchem.core.ph_explorer import REFERENCE_CARDS
        for card in REFERENCE_CARDS:
            yield card.body
    except Exception:
        pass

    # Phase-47 biochemistry by kingdom
    try:
        from orgchem.core.biochemistry_by_kingdom import (
            list_topics,
        )
        for t in list_topics():
            yield t.body
            yield t.notes
    except Exception:
        pass

    # Phase-31k SAR series
    try:
        from orgchem.core.sar import SAR_LIBRARY
        for s in SAR_LIBRARY:
            for v in s.variants:
                yield v.notes
    except Exception:
        pass

    # Phase-31b named-reaction catalogue (seed_reactions._STARTER
    # is a list of (name, category, description, smiles) tuples).
    try:
        from orgchem.db.seed_reactions import _STARTER
        for entry in _STARTER:
            # Description is the third element.
            if len(entry) >= 3:
                yield entry[2]
    except Exception:
        pass


def _tutorial_text_sources() -> Iterable[str]:
    """Walk every registered tutorial lesson markdown + return
    the file body."""
    try:
        from orgchem.tutorial.curriculum import CURRICULUM
    except Exception:
        return
    for level, lessons in CURRICULUM.items():
        for lesson in lessons:
            try:
                yield lesson["path"].read_text()
            except Exception:
                continue


def all_catalogue_text() -> str:
    """Return the concatenated body text of every shipped
    catalogue + every tutorial lesson, separated by
    newlines.  Used by the round-176 coverage test to
    verify that pedagogically-important chemistry terms
    are both used + glossary-covered."""
    parts = list(_catalogue_text_sources()) + \
        list(_tutorial_text_sources())
    return "\n".join(p for p in parts if p)


# ----------------------------------------------------------------
# High-priority terms we expect to be both used AND covered.
# ----------------------------------------------------------------
def gather_catalogue_molecule_references():
    """Phase 49b (round 177) — return a list of
    ``(source, name, smiles)`` triples for every catalogue
    entry that carries a parseable molecule reference.  Used
    by the round-177 molecule-DB canonicalisation audit.

    Sources walked:
    - Phase-29 carbohydrate / lipid / nucleic-acid catalogues
      (each entry IS a molecule reference)
    - Phase-31k SAR series variants
    - Phase-43 cell-component constituents with
      ``cross_reference_molecule_name`` (no SMILES — pulled
      back via DB name lookup)
    - Phase-47 biochemistry-by-kingdom topics with
      ``cross_reference_molecule_names``
    """
    out = []
    try:
        from orgchem.core.carbohydrates import CARBOHYDRATES
        for c in CARBOHYDRATES:
            if c.smiles:
                out.append(("carbohydrate", c.name, c.smiles))
    except Exception:
        pass
    try:
        from orgchem.core.lipids import LIPIDS
        for l in LIPIDS:
            if l.smiles:
                out.append(("lipid", l.name, l.smiles))
    except Exception:
        pass
    try:
        from orgchem.core.nucleic_acids import NUCLEIC_ACIDS
        for na in NUCLEIC_ACIDS:
            if na.smiles:
                out.append(("nucleic-acid", na.name, na.smiles))
    except Exception:
        pass
    try:
        from orgchem.core.sar import SAR_LIBRARY
        for s in SAR_LIBRARY:
            for v in s.variants:
                if v.smiles:
                    out.append((f"sar-{s.id}", v.name, v.smiles))
    except Exception:
        pass
    try:
        from orgchem.core.cell_components import list_components
        for c in list_components():
            for m in c.constituents:
                if m.cross_reference_molecule_name:
                    out.append((
                        f"cell-component:{c.id}",
                        m.cross_reference_molecule_name,
                        "",  # no SMILES — name-only ref
                    ))
    except Exception:
        pass
    try:
        from orgchem.core.biochemistry_by_kingdom import (
            list_topics,
        )
        for t in list_topics():
            for n in t.cross_reference_molecule_names:
                out.append((
                    f"kingdom-topic:{t.id}", n, "",
                ))
    except Exception:
        pass
    return out


#: Terms that the round-176 audit specifically locks in as
#: covered.  Each term must appear in the catalogue text + in
#: the glossary set.  Future audit rounds (49b-f) extend this
#: list as more cross-module integration shows up.
PHASE_49A_REQUIRED_TERMS = (
    # Foundational physical chemistry — referenced everywhere
    "ph", "pka", "buffer", "hydrogen bonding",
    # Synthesis vocabulary referenced by the round-152-175
    # named-reaction expansion
    "lithium diisopropylamide", "active-methylene compound",
    "multi-component reaction",
    # Biochemistry vocabulary referenced by Phase-47
    "endosymbiotic theory", "horizontal gene transfer",
    "crispr",
    # Stereochemistry vocabulary — round 170 + foundational
    "chirality", "chiral switch",
)
