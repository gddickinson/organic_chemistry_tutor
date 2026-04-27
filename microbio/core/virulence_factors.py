"""Phase MB-2.0 (round 221) — microbial virulence-factor +
toxin catalogue.

Additive deep-phase catalogue alongside the MB-1.0 microbe
catalogue (`microbes.py`).  Covers the canonical bacterial
virulence-factor classes: AB-toxins, pore-forming cytolysins,
superantigens, adhesins, capsules, secretion systems, immune-
evasion factors, biofilms, and endotoxin.

Pure-headless: no Qt, no DB.

**Tuple-validation guard.** Same `__post_init__` validator
pattern that BC-2.0 (round 219) introduced + PH-2.0 (round
220) re-used — refuses plain strings in tuple-typed fields,
so the trailing-comma single-element-tuple bug surfaces at
construction time instead of at test time.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
MECHANISM_CLASSES: Tuple[str, ...] = (
    "ab-toxin",            # AB-architecture (binding + active)
    "pore-forming",        # cytolysins / leukocidins
    "superantigen",        # bridge MHC-II / TCR non-specifically
    "adhesin",             # fimbriae / surface adhesins
    "capsule",             # polysaccharide / poly-aa capsules
    "secretion-system",    # T3SS / T4SS / T6SS injection systems
    "immune-evasion",      # IgA proteases / Protein A / Opa variation
    "biofilm",             # exopolysaccharide + quorum sensing
    "endotoxin",           # LPS / lipid A
)


# Tuple-typed fields that must NEVER be plain strings.
_TUPLE_FIELDS: Tuple[str, ...] = (
    "structural_notes",
    "target_tissue_or_cell",
    "mode_of_action",
    "clinical_syndrome",
    "vaccine_or_antitoxin",
    "cross_reference_microbe_ids",
    "cross_reference_enzyme_ids",
    "cross_reference_signaling_pathway_ids",
)


@dataclass(frozen=True)
class VirulenceFactor:
    """One virulence-factor entry in the MB-2.0 catalogue."""
    id: str
    name: str
    mechanism_class: str                       # one of MECHANISM_CLASSES
    structural_notes: Tuple[str, ...]
    target_tissue_or_cell: Tuple[str, ...]
    mode_of_action: Tuple[str, ...]
    clinical_syndrome: Tuple[str, ...]
    vaccine_or_antitoxin: Tuple[str, ...]
    # Cross-references (the multi-studio link layer)
    cross_reference_microbe_ids: Tuple[str, ...]
    # ↑ ids in microbio.core.microbes (source organisms)
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes (toxin IS an enzyme,
    #   or targets a host enzyme catalogued in BC-1.0)
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling (host pathways
    #   the factor hijacks or activates)
    notes: str = ""

    def __post_init__(self) -> None:
        """Reject plain strings in tuple-typed fields.

        Round-218 lesson; round-219 (BC-2.0) introduced the
        validator pattern; round-220 (PH-2.0) inherited it;
        MB-2.0 continues the pattern.
        """
        for fld in _TUPLE_FIELDS:
            value = getattr(self, fld)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"VirulenceFactor({self.id!r}): field "
                    f"{fld!r} must be a tuple, got "
                    f"{type(value).__name__} — add the "
                    f"trailing comma to single-element tuples "
                    f"(e.g. ('foo',) not ('foo')).")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _factor_list() -> List[VirulenceFactor]:
    """Lazy import of the data file so each file stays under
    the 500-line cap."""
    from microbio.core.virulence_factors_data import (
        VIRULENCE_FACTORS,
    )
    return VIRULENCE_FACTORS


def list_virulence_factors(
    mechanism_class: Optional[str] = None,
) -> List[VirulenceFactor]:
    """Return virulence factors, optionally filtered by
    mechanism class."""
    out = list(_factor_list())
    if mechanism_class:
        out = [f for f in out
               if f.mechanism_class == mechanism_class]
    return out


def get_virulence_factor(
    factor_id: str,
) -> Optional[VirulenceFactor]:
    """Return one virulence factor by id, or ``None``."""
    for f in _factor_list():
        if f.id == factor_id:
            return f
    return None


def find_virulence_factors(
    needle: str,
) -> List[VirulenceFactor]:
    """Case-insensitive substring search across id + name +
    mechanism class + structural notes + target tissue +
    mode of action + clinical syndrome + vaccine info +
    notes."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[VirulenceFactor] = []
    for f in _factor_list():
        parts = [f.id, f.name, f.mechanism_class, f.notes]
        parts.extend(f.structural_notes)
        parts.extend(f.target_tissue_or_cell)
        parts.extend(f.mode_of_action)
        parts.extend(f.clinical_syndrome)
        parts.extend(f.vaccine_or_antitoxin)
        if n in " ".join(parts).lower():
            out.append(f)
    return out


def virulence_factors_for_class(
    mechanism_class: str,
) -> List[VirulenceFactor]:
    """All virulence factors in a given mechanism class."""
    return list_virulence_factors(
        mechanism_class=mechanism_class)


def virulence_factor_to_dict(
    f: VirulenceFactor,
) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(f)


def mechanism_classes() -> Tuple[str, ...]:
    return MECHANISM_CLASSES
