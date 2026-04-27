"""Phase BT-2.0 (round 222) — plant-hormones catalogue.

Additive deep-phase catalogue alongside the BT-1.0 plant-taxa
catalogue (`taxa.py`).  Covers the canonical plant-hormone
classes: auxins, cytokinins, gibberellins, abscisic acid,
ethylene, brassinosteroids, jasmonates, salicylic acid,
strigolactones, and peptide hormones.

Pure-headless: no Qt, no DB.

**Tuple-validation guard.** Same `__post_init__` validator
pattern that BC-2.0 (round 219) introduced — refuses plain
strings in tuple-typed fields, so the trailing-comma single-
element-tuple bug surfaces at construction time instead of
at test time.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
HORMONE_CLASSES: Tuple[str, ...] = (
    "auxin",
    "cytokinin",
    "gibberellin",
    "abscisic-acid",
    "ethylene",
    "brassinosteroid",
    "jasmonate",
    "salicylic-acid",
    "strigolactone",
    "peptide-hormone",
)


# Tuple-typed fields that must NEVER be plain strings.
_TUPLE_FIELDS: Tuple[str, ...] = (
    "biosynthesis_precursor",
    "perception_mechanism",
    "primary_physiological_effect",
    "antagonisms",
    "key_model_plants",
    "cross_reference_molecule_names",
    "cross_reference_plant_taxon_ids",
)


@dataclass(frozen=True)
class PlantHormone:
    """One plant-hormone entry in the BT-2.0 catalogue."""
    id: str
    name: str
    hormone_class: str                         # one of HORMONE_CLASSES
    structural_class: str                      # one-line chemistry
    biosynthesis_precursor: Tuple[str, ...]
    perception_mechanism: Tuple[str, ...]
    primary_physiological_effect: Tuple[str, ...]
    antagonisms: Tuple[str, ...]
    key_model_plants: Tuple[str, ...]          # free-text, names not ids
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    cross_reference_plant_taxon_ids: Tuple[str, ...]
    # ↑ ids in botany.core.taxa (plants where the hormone
    #   signalling was characterised or is most studied)
    notes: str = ""

    def __post_init__(self) -> None:
        """Reject plain strings in tuple-typed fields."""
        for fld in _TUPLE_FIELDS:
            value = getattr(self, fld)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"PlantHormone({self.id!r}): field "
                    f"{fld!r} must be a tuple, got "
                    f"{type(value).__name__} — add the "
                    f"trailing comma to single-element tuples "
                    f"(e.g. ('foo',) not ('foo')).")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _hormone_list() -> List[PlantHormone]:
    """Lazy import of the data file."""
    from botany.core.plant_hormones_data import PLANT_HORMONES
    return PLANT_HORMONES


def list_plant_hormones(
    hormone_class: Optional[str] = None,
) -> List[PlantHormone]:
    """Return plant hormones, optionally filtered by class."""
    out = list(_hormone_list())
    if hormone_class:
        out = [h for h in out
               if h.hormone_class == hormone_class]
    return out


def get_plant_hormone(
    hormone_id: str,
) -> Optional[PlantHormone]:
    """Return one hormone by id, or ``None``."""
    for h in _hormone_list():
        if h.id == hormone_id:
            return h
    return None


def find_plant_hormones(needle: str) -> List[PlantHormone]:
    """Case-insensitive substring search across id + name +
    structural class + precursor + perception + effect +
    antagonisms + model plants + notes + cross-reference
    molecule names."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[PlantHormone] = []
    for h in _hormone_list():
        parts = [h.id, h.name, h.hormone_class,
                 h.structural_class, h.notes]
        parts.extend(h.biosynthesis_precursor)
        parts.extend(h.perception_mechanism)
        parts.extend(h.primary_physiological_effect)
        parts.extend(h.antagonisms)
        parts.extend(h.key_model_plants)
        parts.extend(h.cross_reference_molecule_names)
        if n in " ".join(parts).lower():
            out.append(h)
    return out


def plant_hormones_for_class(
    hormone_class: str,
) -> List[PlantHormone]:
    """All plant hormones in a given class."""
    return list_plant_hormones(hormone_class=hormone_class)


def plant_hormone_to_dict(
    h: PlantHormone,
) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(h)


def hormone_classes() -> Tuple[str, ...]:
    return HORMONE_CLASSES
