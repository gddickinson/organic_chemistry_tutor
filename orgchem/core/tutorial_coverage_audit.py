"""Phase 49f (round 181) — tutorial-to-knowledge-graph coverage audit.

Test-time helper that walks every tutorial markdown lesson and
reports which knowledge-graph layers it references.  Three layers
audited:

1. **Glossary terms** — does the lesson reference any defined
   chemistry term so the autolinker can route the reader to a
   definition?
2. **Catalogue molecules** — does the lesson reference a
   molecule from any of the carbohydrate / lipid / nucleic-acid
   / SAR catalogues, the cell-component constituents, or the
   biochemistry-by-kingdom topic cross-references?
3. **Named reactions** — does the lesson reference a
   `seed_reactions._STARTER` named reaction (Diels-Alder /
   Wittig / SN2 / etc.)?

The audit reports per-lesson coverage flags + aggregate
coverage percentages.  Used by the Phase-49f tests to lock in
floors and guard against curriculum drift.

Pure-headless: no Qt imports.  Imports the tutorial loader +
the relevant catalogue modules lazily.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Set, Tuple


@dataclass
class LessonCoverage:
    """Coverage flags for one tutorial lesson."""
    level: str
    title: str
    path: str
    has_glossary_ref: bool = False
    has_catalogue_molecule_ref: bool = False
    has_named_reaction_ref: bool = False

    def hit_count(self) -> int:
        return (int(self.has_glossary_ref)
                + int(self.has_catalogue_molecule_ref)
                + int(self.has_named_reaction_ref))


@dataclass
class TutorialCoverageReport:
    """Aggregate coverage report across the whole curriculum."""
    lessons: List[LessonCoverage] = field(default_factory=list)

    def total(self) -> int:
        return len(self.lessons)

    def with_glossary_pct(self) -> float:
        if not self.lessons:
            return 0.0
        n = sum(1 for l in self.lessons if l.has_glossary_ref)
        return 100.0 * n / len(self.lessons)

    def with_catalogue_molecule_pct(self) -> float:
        if not self.lessons:
            return 0.0
        n = sum(1 for l in self.lessons
                if l.has_catalogue_molecule_ref)
        return 100.0 * n / len(self.lessons)

    def with_named_reaction_pct(self) -> float:
        if not self.lessons:
            return 0.0
        n = sum(1 for l in self.lessons
                if l.has_named_reaction_ref)
        return 100.0 * n / len(self.lessons)


# ----------------------------------------------------------------
# Lookup-set builders — pulled from the same modules the audit
# tests for cross-references.
# ----------------------------------------------------------------
def _glossary_terms(min_len: int = 4) -> Set[str]:
    """Lowercase glossary terms + aliases at least ``min_len``
    chars (single letters are too noisy)."""
    try:
        from orgchem.core.glossary_audit import glossary_term_set
        return {t for t in glossary_term_set() if len(t) >= min_len}
    except Exception:
        return set()


def _catalogue_molecule_names(min_len: int = 4) -> Set[str]:
    """Lowercase names from the seeded knowledge graph that a
    tutorial lesson can reference: lipids / carbohydrates /
    nucleic acids / SAR variants / cell-component constituents /
    kingdom-topic cross-refs **plus** every Molecule DB row
    name + synonym.

    Round-185 broadened the matcher from "narrow catalogues only"
    to "any molecule the user can address through the app".  The
    narrow Phase-29 catalogues only covered ~ 162 names; the
    broader knowledge-graph layer covers ~ 700.  Lessons referring
    to acetaldehyde / styrene / caffeine etc. now register
    correctly — same audit-accuracy principle as round 184's
    short-name reaction matcher.
    """
    import json
    out: Set[str] = set()
    try:
        from orgchem.core.lipids import LIPIDS
        out.update(l.name.lower() for l in LIPIDS)
    except Exception:
        pass
    try:
        from orgchem.core.carbohydrates import CARBOHYDRATES
        out.update(c.name.lower() for c in CARBOHYDRATES)
    except Exception:
        pass
    try:
        from orgchem.core.nucleic_acids import NUCLEIC_ACIDS
        out.update(n.name.lower() for n in NUCLEIC_ACIDS)
    except Exception:
        pass
    try:
        from orgchem.core.sar import SAR_LIBRARY
        for s in SAR_LIBRARY:
            for v in s.variants:
                out.add(v.name.lower())
    except Exception:
        pass
    try:
        from orgchem.core.cell_components import list_components
        for c in list_components():
            for m in c.constituents:
                if m.cross_reference_molecule_name:
                    out.add(
                        m.cross_reference_molecule_name.lower())
    except Exception:
        pass
    try:
        from orgchem.core.biochemistry_by_kingdom import (
            list_topics,
        )
        for t in list_topics():
            for n in t.cross_reference_molecule_names:
                out.add(n.lower())
    except Exception:
        pass
    # Round-185 broadening — pull every Molecule DB row + synonym
    # so lessons that reference DB-only molecules (acetaldehyde,
    # styrene, caffeine, …) register their catalogue coverage.
    # Lazy DB import — falls back gracefully if init_db hasn't run.
    try:
        from orgchem.db.queries import list_molecules
        for m in list_molecules():
            if m.name:
                out.add(m.name.lower())
            if m.synonyms_json:
                try:
                    for s in json.loads(m.synonyms_json) or []:
                        out.add(str(s).lower())
                except Exception:
                    pass
    except Exception:
        pass
    return {n for n in out if len(n) >= min_len}


def _named_reaction_names(min_len: int = 4) -> Set[str]:
    """Lowercase short reaction-name roots from the `_STARTER`
    seed, plus the full names for backwards compatibility.  The
    short root is everything before the first colon or
    parenthesis (e.g. ``"Wittig reaction (propanal + methylidene
    ylide)"`` → ``"wittig reaction"``), which matches the
    natural way tutorials reference reactions."""
    import re
    try:
        from orgchem.db.seed_reactions import _STARTER
    except Exception:
        return set()
    out: Set[str] = set()
    for e in _STARTER:
        full = e[0]
        if len(full) >= min_len:
            out.add(full.lower())
        short = re.split(r"[:(]", full, 1)[0].strip().lower()
        if len(short) >= min_len:
            out.add(short)
    return out


def _check_any_in(needles: Set[str], haystack: str) -> bool:
    """True iff any of the lowercased ``needles`` appears as a
    substring of ``haystack``."""
    return any(n in haystack for n in needles)


# ----------------------------------------------------------------
# Audit
# ----------------------------------------------------------------
def audit_tutorial_coverage() -> TutorialCoverageReport:
    """Walk every tutorial lesson and return a
    :class:`TutorialCoverageReport` of per-lesson coverage flags
    + aggregate percentages."""
    from orgchem.tutorial.curriculum import CURRICULUM

    gloss = _glossary_terms()
    mols = _catalogue_molecule_names()
    rxns = _named_reaction_names()

    report = TutorialCoverageReport()
    for level, lessons in CURRICULUM.items():
        for lesson in lessons:
            # Skip test-fixture lessons injected by authoring
            # tests — they're stubs with no chemistry content.
            title = lesson.get("title", "")
            if "test lesson" in title.lower():
                continue
            try:
                text = lesson["path"].read_text().lower()
            except Exception:
                continue
            cov = LessonCoverage(
                level=level,
                title=lesson["title"],
                path=str(lesson["path"]),
                has_glossary_ref=_check_any_in(gloss, text),
                has_catalogue_molecule_ref=_check_any_in(
                    mols, text),
                has_named_reaction_ref=_check_any_in(
                    rxns, text),
            )
            report.lessons.append(cov)
    return report


def lessons_missing(report: TutorialCoverageReport,
                    layer: str) -> List[LessonCoverage]:
    """Return the per-layer list of lessons missing a reference.
    ``layer`` ∈ ``{"glossary", "catalogue", "named-reaction"}``.
    """
    if layer == "glossary":
        return [l for l in report.lessons
                if not l.has_glossary_ref]
    if layer == "catalogue":
        return [l for l in report.lessons
                if not l.has_catalogue_molecule_ref]
    if layer == "named-reaction":
        return [l for l in report.lessons
                if not l.has_named_reaction_ref]
    raise ValueError(f"Unknown layer {layer!r}")


def render_report_text(report: TutorialCoverageReport) -> str:
    """Render the coverage report as a human-readable block.
    Used by the Phase-49f doc + failure messages."""
    rows = []
    rows.append("Tutorial-to-knowledge-graph coverage audit")
    rows.append("=" * 60)
    rows.append(f"Total lessons:                  {report.total()}")
    rows.append(
        f"Lessons with glossary ref:      "
        f"{report.with_glossary_pct():>5.1f} %"
    )
    rows.append(
        f"Lessons with catalogue ref:     "
        f"{report.with_catalogue_molecule_pct():>5.1f} %"
    )
    rows.append(
        f"Lessons with named-reaction ref:"
        f"{report.with_named_reaction_pct():>5.1f} %"
    )
    rows.append("=" * 60)
    return "\n".join(rows)
