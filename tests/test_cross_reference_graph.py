"""Phase 49c (round 178) — cross-module reference graph audit.

Locks in that **every cross-reference declared by any catalogue
resolves to a real target** in the destination catalogue / DB.
Generalises the per-catalogue cross-reference tests added in:
- round 146 (Phase-44 microscopy → Phase-40a lab-analyser)
- round 151 (Phase-43 cell-component → Molecule DB)
- round 166 (Phase-47 kingdom-topic → Phase-43 + 42 + DB)

into a single project-wide audit driven by
``core.cross_reference_audit``.
"""
from __future__ import annotations
import os

import pytest

pytest.importorskip("rdkit")


@pytest.fixture(scope="module")
def app():
    os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
    from orgchem.agent.headless import HeadlessApp
    with HeadlessApp() as h:
        h.pump(5)
        yield h


# ==================================================================
# Walkers — surface raw counts so a regression here flags before the
# downstream broken-link test fires.
# ==================================================================

def test_gather_returns_at_least_50_cross_references(app):
    """The walker collects ≥ 100 cross-reference edges across all
    catalogues — sanity floor that catches "I deleted a catalogue"
    regressions.  Round-197 raised the floor 50 → 100 after the
    `metabolic-pathway → molecule` walker added 40 + edges in
    one go.  Now requires the `app` fixture so the DB-driven
    metabolic-pathway walker has a seeded DB to query."""
    from orgchem.core.cross_reference_audit import (
        gather_all_cross_references,
    )
    refs = gather_all_cross_references()
    assert len(refs) >= 100, \
        f"only {len(refs)} cross-refs gathered"


def test_metabolic_pathway_walker_uses_db_filter(app):
    """The Phase-42a pathway data references many molecule names
    (water, generic ions, enzyme co-substrates) that aren't in
    the seeded Molecule DB.  The new
    `metabolic-pathway → molecule` walker MUST filter by DB
    resolvability so it never emits unresolvable edges that
    `validate_cross_references` would flag as broken."""
    from orgchem.core.cross_reference_audit import (
        gather_all_cross_references, validate_cross_references,
    )
    refs = [r for r in gather_all_cross_references()
            if r.source_kind == "metabolic-pathway"]
    assert refs, "metabolic-pathway walker emitted no edges"
    report = validate_cross_references(refs)
    assert report.broken == [], (
        f"{len(report.broken)} unresolvable metabolic-pathway → "
        f"molecule edges leaked through the walker filter"
    )


def test_matrix_covers_every_declared_kind(app):
    """The matrix surfaces every (source, target) tuple in
    :data:`CROSS_REFERENCE_KINDS`, with non-zero edge counts.
    Requires `app` since the metabolic-pathway → molecule
    walker reads the DB."""
    from orgchem.core.cross_reference_audit import (
        CROSS_REFERENCE_KINDS, cross_reference_matrix,
    )
    matrix = cross_reference_matrix()
    for kind in CROSS_REFERENCE_KINDS:
        assert kind in matrix, (
            f"matrix missing declared kind {kind}"
        )
        assert matrix[kind] > 0, (
            f"declared cross-ref kind {kind} has 0 edges — "
            f"a catalogue lost its cross-references?"
        )


def test_matrix_renders_as_text(app):
    """Smoke-test the human-readable matrix renderer used by the
    Phase-49c doc + failure messages."""
    from orgchem.core.cross_reference_audit import (
        render_matrix_text,
    )
    out = render_matrix_text()
    assert "Source kind" in out
    assert "TOTAL" in out
    assert "cell-component" in out
    assert "kingdom-topic" in out


# ==================================================================
# Validation — every cross-ref resolves
# ==================================================================

def test_no_broken_cross_references(app):
    """Every cross-reference declared by any catalogue must resolve
    to a real target.  Failure surfaces the broken edges + a copy
    of the cross-module matrix for context."""
    from orgchem.core.cross_reference_audit import (
        validate_cross_references, render_matrix_text,
    )
    report = validate_cross_references()
    assert report.is_valid(), (
        f"{len(report.broken)} broken cross-references "
        f"(of {report.total} total).  First 10:\n"
        + "\n".join(
            f"  [{b.source_kind}:{b.source_id}] → "
            f"[{b.target_kind}:{b.target_id}]"
            for b in report.broken[:10])
        + "\n\nCurrent matrix:\n"
        + render_matrix_text()
    )


def test_per_kind_floors(app):
    """Each cross-reference kind has a sensible minimum edge count.
    A regression (e.g. someone strips all kingdom-topic →
    cell-component refs) surfaces immediately."""
    from orgchem.core.cross_reference_audit import (
        cross_reference_matrix,
    )
    matrix = cross_reference_matrix()
    # Floors set to current observed counts.  Tightening them as
    # the catalogues add cross-references is encouraged — going
    # below them surfaces a regression.  Round-183 raised the
    # cell-component → molecule + kingdom-topic → molecule
    # floors after the round-178 audit dashboard surfaced low
    # coverage in those two kinds.
    floors = {
        ("cell-component", "molecule"): 5,
        ("kingdom-topic", "cell-component"): 20,
        ("kingdom-topic", "metabolic-pathway"): 1,
        ("kingdom-topic", "molecule"): 30,
        ("microscopy-method", "lab-analyser"): 7,
        ("metabolic-pathway", "molecule"): 55,   # rounds 197 + 201 + 202
    }
    for kind, floor in floors.items():
        assert matrix.get(kind, 0) >= floor, (
            f"cross-ref kind {kind} has {matrix.get(kind, 0)} "
            f"edges; expected ≥ {floor}"
        )


# ==================================================================
# Internals
# ==================================================================

def test_cross_reference_dataclass_is_hashable():
    """``CrossRef`` rows are frozen dataclasses → safe to put in a
    set for de-duplication / diffing."""
    from orgchem.core.cross_reference_audit import CrossRef
    a = CrossRef("cell-component", "x", "molecule", "Y")
    b = CrossRef("cell-component", "x", "molecule", "Y")
    assert hash(a) == hash(b)
    assert {a, b} == {a}


def test_validate_accepts_explicit_refs_list(app):
    """``validate_cross_references`` can be called against a hand-
    rolled refs list — useful for testing one specific catalogue
    in isolation."""
    from orgchem.core.cross_reference_audit import (
        CrossRef, validate_cross_references,
    )
    refs = [
        CrossRef("kingdom-topic", "test", "cell-component",
                 "mitochondrion"),  # real id
        CrossRef("kingdom-topic", "test", "cell-component",
                 "made-up-organelle"),   # broken
    ]
    report = validate_cross_references(refs)
    assert report.total == 2
    assert len(report.broken) == 1
    assert report.broken[0].target_id == "made-up-organelle"
