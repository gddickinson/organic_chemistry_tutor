"""Phase CB-2.0 (round 218) — eukaryotic cell-cycle catalogue.

Additive deep-phase catalogue alongside the CB-1.0 signalling
catalogue (`cell_signaling.py`).  Covers the canonical cell-
cycle phases, checkpoints, cyclin-CDK pairs, CDK inhibitors,
mitotic regulators, and DNA-damage-response kinases that sit
upstream of all of them.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
CATEGORIES: Tuple[str, ...] = (
    "phase",                  # G1 / S / G2 / M / G0
    "checkpoint",             # G1/S restriction, G2/M, SAC, intra-S
    "cyclin-cdk",             # cyclin / CDK pairs
    "cdk-inhibitor",          # CKIs (CIP/KIP family + INK4)
    "pocket-protein",         # Rb + E2F axis
    "mitotic-regulator",      # APC/C, separase, Aurora, Plk, SAC
    "dna-damage-response",    # ATM, ATR, Chk1, Chk2, BRCA1/2
)


@dataclass(frozen=True)
class CellCycleEntry:
    """One entry in the CB-2.0 cell-cycle catalogue."""
    id: str
    name: str
    category: str                              # one of CATEGORIES
    phase_or_role: str                         # short tag, e.g. "G1/S", "M phase"
    summary: str                               # one-paragraph description
    key_components: Tuple[str, ...]            # the proteins / complexes
    function: str                              # what it does
    activated_by: Tuple[str, ...]              # upstream activators (free text)
    inhibited_by: Tuple[str, ...]              # upstream inhibitors (free text)
    disease_associations: Tuple[str, ...]      # cancer / DNA-repair syndromes
    # Cross-references (the multi-studio link layer)
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    cross_reference_pharm_drug_class_ids: Tuple[str, ...]
    # ↑ ids in pharm.core.drug_classes
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows; left empty
    #   for v0.1 — future round can backfill cyclins / kinases.
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _entry_list() -> List[CellCycleEntry]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from cellbio.core.cell_cycle_data import CELL_CYCLE_ENTRIES
    return CELL_CYCLE_ENTRIES


def list_cell_cycle_entries(
    category: Optional[str] = None,
) -> List[CellCycleEntry]:
    """Return cell-cycle entries, optionally filtered by category."""
    out = list(_entry_list())
    if category:
        out = [e for e in out if e.category == category]
    return out


def get_cell_cycle_entry(
    entry_id: str,
) -> Optional[CellCycleEntry]:
    """Return one entry by id, or ``None``."""
    for e in _entry_list():
        if e.id == entry_id:
            return e
    return None


def find_cell_cycle_entries(needle: str) -> List[CellCycleEntry]:
    """Case-insensitive substring search across id + name +
    summary + function + components + disease associations +
    activator / inhibitor lists + notes."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[CellCycleEntry] = []
    for e in _entry_list():
        parts = [e.id, e.name, e.phase_or_role, e.summary,
                 e.function, e.notes]
        parts.extend(e.key_components)
        parts.extend(e.activated_by)
        parts.extend(e.inhibited_by)
        parts.extend(e.disease_associations)
        if n in " ".join(parts).lower():
            out.append(e)
    return out


def cell_cycle_entries_for_category(
    category: str,
) -> List[CellCycleEntry]:
    """All cell-cycle entries in a given category."""
    return list_cell_cycle_entries(category=category)


def cell_cycle_entry_to_dict(
    e: CellCycleEntry,
) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(e)


def categories() -> Tuple[str, ...]:
    return CATEGORIES
