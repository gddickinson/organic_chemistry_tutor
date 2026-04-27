"""Phase AB-2.0 (round 223) — animal organ-systems catalogue.

Additive deep-phase catalogue alongside the AB-1.0 animal-taxa
catalogue (`taxa.py`).  Covers the 11 canonical mammalian organ
systems + a comparative-anatomy class for non-mammalian body
plans (open vs closed circulation, gills vs tracheae vs air
sacs, regeneration outliers, eye evolution, etc.).

Pure-headless: no Qt, no DB.

**Tuple-validation guard.** Same `__post_init__` validator
pattern that BC-2.0 (round 219) introduced — refuses plain
strings in tuple-typed fields.

This is the FINAL catalogue of the -2 deep-phase chain.  See
`SESSION_LOG.md` round 223 for the chain-wide retrospective.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
SYSTEM_CATEGORIES: Tuple[str, ...] = (
    "cardiovascular",
    "respiratory",
    "digestive",
    "urinary",
    "nervous",
    "endocrine",
    "immune",
    "musculoskeletal",
    "integumentary",
    "reproductive-female",
    "reproductive-male",
    "lymphatic",
    "comparative-anatomy",   # cross-phyla evolutionary notes
)


# Tuple-typed fields that must NEVER be plain strings.
_TUPLE_FIELDS: Tuple[str, ...] = (
    "representative_organs",
    "key_cell_types",
    "functional_anatomy",
    "evolutionary_origin",
    "characteristic_disorders",
    "cross_reference_molecule_names",
    "cross_reference_signaling_pathway_ids",
    "cross_reference_enzyme_ids",
    "cross_reference_animal_taxon_ids",
)


@dataclass(frozen=True)
class OrganSystem:
    """One organ-system entry in the AB-2.0 catalogue."""
    id: str
    name: str
    system_category: str                       # one of SYSTEM_CATEGORIES
    short_summary: str                         # one-paragraph description
    representative_organs: Tuple[str, ...]
    key_cell_types: Tuple[str, ...]
    functional_anatomy: Tuple[str, ...]
    evolutionary_origin: Tuple[str, ...]
    characteristic_disorders: Tuple[str, ...]
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    cross_reference_animal_taxon_ids: Tuple[str, ...]
    # ↑ ids in animal.core.taxa
    notes: str = ""

    def __post_init__(self) -> None:
        """Reject plain strings in tuple-typed fields."""
        for fld in _TUPLE_FIELDS:
            value = getattr(self, fld)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"OrganSystem({self.id!r}): field "
                    f"{fld!r} must be a tuple, got "
                    f"{type(value).__name__} — add the "
                    f"trailing comma to single-element tuples "
                    f"(e.g. ('foo',) not ('foo')).")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _system_list() -> List[OrganSystem]:
    """Lazy import of the data file."""
    from animal.core.organ_systems_data import ORGAN_SYSTEMS
    return ORGAN_SYSTEMS


def list_organ_systems(
    system_category: Optional[str] = None,
) -> List[OrganSystem]:
    """Return organ systems, optionally filtered by category."""
    out = list(_system_list())
    if system_category:
        out = [s for s in out
               if s.system_category == system_category]
    return out


def get_organ_system(
    system_id: str,
) -> Optional[OrganSystem]:
    """Return one organ system by id, or ``None``."""
    for s in _system_list():
        if s.id == system_id:
            return s
    return None


def find_organ_systems(needle: str) -> List[OrganSystem]:
    """Case-insensitive substring search across id + name +
    summary + representative organs + cell types + functional
    anatomy + evolutionary origin + disorders + notes."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[OrganSystem] = []
    for s in _system_list():
        parts = [s.id, s.name, s.system_category,
                 s.short_summary, s.notes]
        parts.extend(s.representative_organs)
        parts.extend(s.key_cell_types)
        parts.extend(s.functional_anatomy)
        parts.extend(s.evolutionary_origin)
        parts.extend(s.characteristic_disorders)
        if n in " ".join(parts).lower():
            out.append(s)
    return out


def organ_systems_for_category(
    system_category: str,
) -> List[OrganSystem]:
    """All organ-system entries in a given category."""
    return list_organ_systems(system_category=system_category)


def organ_system_to_dict(
    s: OrganSystem,
) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(s)


def system_categories() -> Tuple[str, ...]:
    return SYSTEM_CATEGORIES
