"""Phase BC-2.0 (round 219) — biochem cofactors / coenzymes
catalogue.

Additive deep-phase catalogue alongside the BC-1.0 enzyme
catalogue (`enzymes.py`).  Covers the canonical electron
carriers (nicotinamide + flavin), acyl-transfer carriers, methyl
donors, phosphate-energy currency, vitamin-derived prosthetic
groups (biotin / TPP / PLP / lipoate / cobalamin / folate),
metal cofactors, quinone electron carriers, and redox-buffer
small molecules.

Pure-headless: no Qt, no DB.

**Tuple-validation guard.**  The dataclass `__post_init__`
raises `TypeError` if any tuple-typed field comes in as a
plain `str`.  This kills the trailing-comma single-element-
tuple bug class that bit on round 218 (CB-2.0 cell-cycle
catalogue) — instead of silently coercing, we fail loudly
at import time so the test-suite or even a `python -c
"import biochem"` immediately surfaces the typo.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
COFACTOR_CLASSES: Tuple[str, ...] = (
    "nicotinamide",          # NAD+/H, NADP+/H
    "flavin",                # FAD/H2, FMN
    "acyl-carrier",          # CoA, acetyl-CoA, ACP
    "methyl-donor",          # SAM / SAH
    "phosphate-energy",      # ATP, ADP, AMP, GTP, creatine~P
    "biotin-vitamin",        # B7
    "tpp-vitamin",           # B1
    "plp-vitamin",           # B6
    "lipoate",               # lipoic acid
    "cobalamin-vitamin",     # B12
    "folate",                # B9 / tetrahydrofolate family
    "metal-cluster",         # heme, Fe-S, Mg, Mn, Zn
    "quinone",               # Q10 / plastoquinone / menaquinone
    "redox-buffer",          # glutathione / ascorbate / thioredoxin
)


# Tuple-typed fields that must NEVER be plain strings.  Listed
# explicitly so the post-init validator catches every one.
_TUPLE_FIELDS: Tuple[str, ...] = (
    "key_features",
    "primary_role",
    "carriers_or_substrates",
    "vitamin_origin",
    "deficiency_disease",
    "cross_reference_enzyme_ids",
    "cross_reference_metabolic_pathway_ids",
    "cross_reference_molecule_names",
)


@dataclass(frozen=True)
class Cofactor:
    """One cofactor entry in the BC-2.0 catalogue."""
    id: str
    name: str
    cofactor_class: str                        # one of COFACTOR_CLASSES
    chemical_summary: str                      # one-line chemistry
    primary_role: Tuple[str, ...]              # short role tags
    carriers_or_substrates: Tuple[str, ...]    # what it carries / transfers
    key_features: Tuple[str, ...]              # diagnostic facts
    vitamin_origin: Tuple[str, ...]            # B-vitamin link if any
    deficiency_disease: Tuple[str, ...]        # human deficiency syndromes
    # Cross-references (the multi-studio link layer)
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    cross_reference_metabolic_pathway_ids: Tuple[str, ...]
    # ↑ ids in orgchem.core.metabolic_pathways
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    notes: str = ""

    def __post_init__(self) -> None:
        """Reject plain strings in tuple-typed fields.

        Round-218 lesson: a single-element tuple needs a trailing
        comma — otherwise ``("foo")`` is just the string ``"foo"``.
        We refuse that quietly-corrupt input here so the bug
        surfaces at import time instead of at test time.
        """
        for fld in _TUPLE_FIELDS:
            value = getattr(self, fld)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"Cofactor({self.id!r}): field {fld!r} must "
                    f"be a tuple, got {type(value).__name__} — "
                    f"add the trailing comma to single-element "
                    f"tuples (e.g. ('foo',) not ('foo')).")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _cofactor_list() -> List[Cofactor]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from biochem.core.cofactors_data import COFACTORS
    return COFACTORS


def list_cofactors(
    cofactor_class: Optional[str] = None,
) -> List[Cofactor]:
    """Return cofactors, optionally filtered by class."""
    out = list(_cofactor_list())
    if cofactor_class:
        out = [c for c in out
               if c.cofactor_class == cofactor_class]
    return out


def get_cofactor(cofactor_id: str) -> Optional[Cofactor]:
    """Return one cofactor by id, or ``None``."""
    for c in _cofactor_list():
        if c.id == cofactor_id:
            return c
    return None


def find_cofactors(needle: str) -> List[Cofactor]:
    """Case-insensitive substring search across id + name +
    chemistry summary + role / substrate / feature lists +
    vitamin-origin tags + deficiency diseases + notes +
    cross-reference molecule names."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[Cofactor] = []
    for c in _cofactor_list():
        parts = [c.id, c.name, c.cofactor_class,
                 c.chemical_summary, c.notes]
        parts.extend(c.primary_role)
        parts.extend(c.carriers_or_substrates)
        parts.extend(c.key_features)
        parts.extend(c.vitamin_origin)
        parts.extend(c.deficiency_disease)
        parts.extend(c.cross_reference_molecule_names)
        if n in " ".join(parts).lower():
            out.append(c)
    return out


def cofactors_for_class(
    cofactor_class: str,
) -> List[Cofactor]:
    """All cofactors in a given class."""
    return list_cofactors(cofactor_class=cofactor_class)


def cofactor_to_dict(c: Cofactor) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(c)


def cofactor_classes() -> Tuple[str, ...]:
    return COFACTOR_CLASSES
