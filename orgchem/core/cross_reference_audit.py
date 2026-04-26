"""Phase 49c (round 178) — cross-module reference graph audit.

Test-time helper that walks every cross-reference relationship
across the catalogue layer and reports broken links.  The Phase-49
integration sweep flagged that catalogues, the molecule DB, the
glossary, and the agent registry can drift apart silently — this
module unifies the per-catalogue cross-reference tests added in
rounds 151 (Phase-43 → Molecule DB) and 166 (Phase-47 → Phase-43 +
Phase-42 + Molecule DB) and 146 (Phase-44 → Phase-40a) into a
single project-wide audit + a renderable matrix doc.

Five cross-reference relationships are audited:

1. ``Phase-43 cell-component → Molecule DB``
   (``MolecularConstituent.cross_reference_molecule_name`` →
   ``Molecule.name``)
2. ``Phase-47 kingdom-topic → Phase-43 cell-component``
   (``KingdomTopic.cross_reference_cell_component_ids`` →
   ``CellComponent.id``)
3. ``Phase-47 kingdom-topic → Phase-42 metabolic-pathway``
   (``KingdomTopic.cross_reference_pathway_ids`` →
   ``Pathway.id``)
4. ``Phase-47 kingdom-topic → Molecule DB``
   (``KingdomTopic.cross_reference_molecule_names`` →
   ``Molecule.name``)
5. ``Phase-44 microscopy-method → Phase-40a lab-analyser``
   (``MicroscopyMethod.cross_reference_lab_analyser_ids`` →
   ``LabAnalyser.id``)

Pure-headless: no Qt imports.  Lazy DB import so the gather walker
can run without a seeded database (broken-name detection then
becomes unavailable for that one kind, but the structural walks
still produce the matrix).
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


# ----------------------------------------------------------------
# Cross-reference kinds — canonical (source_kind, target_kind) tuples.
# ----------------------------------------------------------------
CROSS_REFERENCE_KINDS: Tuple[Tuple[str, str], ...] = (
    ("cell-component", "molecule"),
    ("kingdom-topic", "cell-component"),
    ("kingdom-topic", "metabolic-pathway"),
    ("kingdom-topic", "molecule"),
    ("microscopy-method", "lab-analyser"),
    ("metabolic-pathway", "molecule"),   # round 197
)


@dataclass(frozen=True)
class CrossRef:
    """One cross-reference edge in the cross-module graph."""
    source_kind: str
    source_id: str
    target_kind: str
    target_id: str


@dataclass
class CrossRefReport:
    """Result of a cross-reference audit run."""
    total: int = 0
    broken: List[CrossRef] = field(default_factory=list)
    by_kind: Dict[Tuple[str, str], int] = field(default_factory=dict)

    def is_valid(self) -> bool:
        return not self.broken


# ----------------------------------------------------------------
# Target-id resolvers — lazy lookup of valid ids per target kind.
# Each resolver returns a set of strings.  Lookups against
# ``molecule`` use the DB so they require a seeded database; all
# other lookups are pure-Python from catalogue modules.
# ----------------------------------------------------------------
def _cell_component_ids() -> Set[str]:
    try:
        from orgchem.core.cell_components import list_components
        return {c.id for c in list_components()}
    except Exception:
        return set()


def _metabolic_pathway_ids() -> Set[str]:
    try:
        from orgchem.core.metabolic_pathways import list_pathways
        return {p.id for p in list_pathways()}
    except Exception:
        return set()


def _lab_analyser_ids() -> Set[str]:
    try:
        from orgchem.core.lab_analysers import list_analysers
        return {a.id for a in list_analysers()}
    except Exception:
        return set()


def _molecule_names() -> Optional[Set[str]]:
    """Return the set of canonical molecule names + every synonym
    in the seeded DB.  Returns ``None`` if the DB isn't reachable
    so callers can skip molecule-name validation gracefully."""
    try:
        import json
        from orgchem.db.queries import list_molecules
        from orgchem.core.identity import normalise_name
        out: Set[str] = set()
        for m in list_molecules():
            if m.name:
                out.add(normalise_name(m.name))
            if m.synonyms_json:
                try:
                    for alt in json.loads(m.synonyms_json) or []:
                        out.add(normalise_name(str(alt)))
                except Exception:
                    pass
        return out
    except Exception:
        return None


# ----------------------------------------------------------------
# Walkers — gather cross-references per source catalogue.
# ----------------------------------------------------------------
def _walk_cell_component_xrefs() -> List[CrossRef]:
    out: List[CrossRef] = []
    try:
        from orgchem.core.cell_components import list_components
        for c in list_components():
            for m in c.constituents:
                target = (m.cross_reference_molecule_name or "").strip()
                if target:
                    out.append(CrossRef(
                        source_kind="cell-component",
                        source_id=c.id,
                        target_kind="molecule",
                        target_id=target,
                    ))
    except Exception:
        pass
    return out


def _walk_kingdom_topic_xrefs() -> List[CrossRef]:
    out: List[CrossRef] = []
    try:
        from orgchem.core.biochemistry_by_kingdom import list_topics
        for t in list_topics():
            for cid in t.cross_reference_cell_component_ids:
                out.append(CrossRef(
                    source_kind="kingdom-topic", source_id=t.id,
                    target_kind="cell-component", target_id=cid,
                ))
            for pid in t.cross_reference_pathway_ids:
                out.append(CrossRef(
                    source_kind="kingdom-topic", source_id=t.id,
                    target_kind="metabolic-pathway", target_id=pid,
                ))
            for n in t.cross_reference_molecule_names:
                out.append(CrossRef(
                    source_kind="kingdom-topic", source_id=t.id,
                    target_kind="molecule", target_id=n,
                ))
    except Exception:
        pass
    return out


def _walk_microscopy_xrefs() -> List[CrossRef]:
    out: List[CrossRef] = []
    try:
        from orgchem.core.microscopy import list_methods
        for m in list_methods():
            for aid in m.cross_reference_lab_analyser_ids:
                out.append(CrossRef(
                    source_kind="microscopy-method",
                    source_id=m.id,
                    target_kind="lab-analyser",
                    target_id=aid,
                ))
    except Exception:
        pass
    return out


def _walk_metabolic_pathway_xrefs() -> List[CrossRef]:
    """Round 197 — derive `metabolic-pathway → molecule` edges
    from the seeded Phase-42a pathway data.  Each edge connects
    a pathway to the canonical name of every substrate / product
    its steps reference that ALSO resolves to a Molecule DB row.

    Filters out unresolvable names (water, generic ions, enzyme
    names) at the walker level — only emits edges for names that
    map to actual DB rows so the validator never reports them as
    broken.  De-duplicates per (pathway, molecule) so the same
    pathway-and-molecule pair only contributes one edge regardless
    of how many steps mention it."""
    out: List[CrossRef] = []
    try:
        from orgchem.core.metabolic_pathways import list_pathways
        from orgchem.db.queries import find_molecule_by_name
    except Exception:
        return out
    seen: set = set()

    def _try_lookup(raw: str):
        try:
            return find_molecule_by_name(raw)
        except Exception:
            return None

    for p in list_pathways():
        # Walk substrates + products first so they take
        # priority in the dedup set.
        for step in p.steps:
            for raw in (list(step.substrates)
                        + list(step.products)):
                row = _try_lookup(raw)
                if row is None:
                    continue
                key = (p.id, row.name)
                if key in seen:
                    continue
                seen.add(key)
                out.append(CrossRef(
                    source_kind="metabolic-pathway",
                    source_id=p.id,
                    target_kind="molecule",
                    target_id=row.name,
                ))
        # Round 201 — also walk regulatory_effectors.  Captures
        # cross-pathway regulator molecules that AREN'T in the
        # pathway's substrate/product flow (e.g. Citrate as the
        # PFK inhibitor of glycolysis from the TCA cycle;
        # Cyanide as the Complex-IV inhibitor of ox-phos).
        # Dedup with the substrate/product set so a molecule
        # that's both a substrate AND a regulator only
        # contributes one edge.
        for step in p.steps:
            for eff in step.regulatory_effectors:
                row = _try_lookup(eff.name)
                if row is None:
                    continue
                key = (p.id, row.name)
                if key in seen:
                    continue
                seen.add(key)
                out.append(CrossRef(
                    source_kind="metabolic-pathway",
                    source_id=p.id,
                    target_kind="molecule",
                    target_id=row.name,
                ))
    return out


def gather_all_cross_references() -> List[CrossRef]:
    """Walk every catalogue and return every declared cross-ref
    edge as a flat list.  Order is stable: cell-component refs,
    then kingdom-topic refs, then microscopy refs, then
    metabolic-pathway refs."""
    out: List[CrossRef] = []
    out.extend(_walk_cell_component_xrefs())
    out.extend(_walk_kingdom_topic_xrefs())
    out.extend(_walk_microscopy_xrefs())
    out.extend(_walk_metabolic_pathway_xrefs())
    return out


def validate_cross_references(
    refs: Optional[List[CrossRef]] = None,
) -> CrossRefReport:
    """Resolve every cross-reference target and report broken
    links.  Pass an explicit ``refs`` list to validate a subset;
    omit to walk the whole graph."""
    if refs is None:
        refs = gather_all_cross_references()

    target_lookups = {
        "cell-component": _cell_component_ids(),
        "metabolic-pathway": _metabolic_pathway_ids(),
        "lab-analyser": _lab_analyser_ids(),
    }
    molecule_names = _molecule_names()   # may be None

    report = CrossRefReport(total=len(refs))
    for r in refs:
        report.by_kind[(r.source_kind, r.target_kind)] = (
            report.by_kind.get(
                (r.source_kind, r.target_kind), 0) + 1
        )
        if r.target_kind == "molecule":
            if molecule_names is None:
                continue   # DB unavailable — skip
            from orgchem.core.identity import normalise_name
            if normalise_name(r.target_id) not in molecule_names:
                report.broken.append(r)
            continue
        valid = target_lookups.get(r.target_kind)
        if valid is None:
            # Unknown target kind — treat as broken.
            report.broken.append(r)
            continue
        if r.target_id not in valid:
            report.broken.append(r)
    return report


# ----------------------------------------------------------------
# Reporting — human-readable matrix for the cross-module doc.
# ----------------------------------------------------------------
def cross_reference_matrix() -> Dict[Tuple[str, str], int]:
    """Return a ``{(source_kind, target_kind): edge_count}`` dict
    spanning every relationship declared in
    :data:`CROSS_REFERENCE_KINDS`.  Useful for the Phase-49c
    living matrix doc + as a regression floor."""
    refs = gather_all_cross_references()
    out: Dict[Tuple[str, str], int] = {
        kind: 0 for kind in CROSS_REFERENCE_KINDS
    }
    for r in refs:
        key = (r.source_kind, r.target_kind)
        out[key] = out.get(key, 0) + 1
    return out


def render_matrix_text(matrix: Optional[Dict[Tuple[str, str], int]] = None) -> str:
    """Render the cross-reference matrix as a left-aligned plain-
    text table.  Used by the Phase-49c doc generator + by failure
    messages in the audit test suite."""
    if matrix is None:
        matrix = cross_reference_matrix()
    rows = []
    rows.append("Source kind          → Target kind         | Edges")
    rows.append("-" * 60)
    for (s, t), n in matrix.items():
        rows.append(f"{s:<20} → {t:<20} | {n:>5}")
    rows.append("-" * 60)
    rows.append(f"{'TOTAL':<43} | {sum(matrix.values()):>5}")
    return "\n".join(rows)
