"""Phase MB-1.0 (round 215) — microbe catalogue.

The flagship Microbiology Studio catalogue.  ~ 30 microbes
spanning the 5 microbial kingdoms (bacteria / archaea / fungi /
viruses / protists), each with cell-biology + drug-treatment +
enzyme cross-references.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
KINGDOMS: Tuple[str, ...] = (
    "bacteria",
    "archaea",
    "fungus",
    "virus",
    "protist",
)

GRAM_TYPES: Tuple[str, ...] = (
    "gram-positive",
    "gram-negative",
    "acid-fast",        # mycobacteria
    "atypical",         # Mycoplasma, Chlamydia, Treponema
    "not-applicable",   # archaea / fungi / viruses / protists
)

# Baltimore classification — viral genome organisation
BALTIMORE_CLASSES: Tuple[str, ...] = (
    "I",     # dsDNA
    "II",    # ssDNA
    "III",   # dsRNA
    "IV",    # +ssRNA
    "V",     # -ssRNA
    "VI",    # ssRNA-RT (retroviruses)
    "VII",   # dsDNA-RT (hepadnaviruses)
)


@dataclass(frozen=True)
class Microbe:
    """One microbe entry in the MB-1.0 catalogue."""
    id: str
    name: str
    full_taxonomic_name: str
    kingdom: str                            # one of KINGDOMS
    gram_type: str                          # one of GRAM_TYPES
    baltimore_class: str                    # one of BALTIMORE_CLASSES; "" if not virus
    morphology: str
    key_metabolism_or_replication: str
    pathogenesis_summary: str
    antibiotic_susceptibility: str          # phrases, not specific drugs
    genome_size_or_kb: str                  # "4.6 Mb" / "9.7 kb" / etc.
    ictv_or_bergey_reference: str
    # Cross-references (the multi-studio link layer)
    cross_reference_cell_component_ids: Tuple[str, ...]
    # ↑ ids in orgchem.core.cell_components
    cross_reference_pharm_drug_class_ids: Tuple[str, ...]
    # ↑ ids in pharm.core.drug_classes
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _microbe_list() -> List[Microbe]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from microbio.core.microbes_data import MICROBES
    return MICROBES


def list_microbes(
    kingdom: Optional[str] = None,
    gram_type: Optional[str] = None,
) -> List[Microbe]:
    """Return microbes, optionally filtered."""
    out = list(_microbe_list())
    if kingdom:
        out = [m for m in out if m.kingdom == kingdom]
    if gram_type:
        out = [m for m in out if m.gram_type == gram_type]
    return out


def get_microbe(microbe_id: str) -> Optional[Microbe]:
    """Return one microbe by id, or ``None``."""
    for m in _microbe_list():
        if m.id == microbe_id:
            return m
    return None


def find_microbes(needle: str) -> List[Microbe]:
    """Case-insensitive substring search across id + names +
    morphology + metabolism + pathogenesis + antibiotic
    susceptibility + reference."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[Microbe] = []
    for m in _microbe_list():
        parts = [m.id, m.name, m.full_taxonomic_name,
                 m.morphology, m.key_metabolism_or_replication,
                 m.pathogenesis_summary,
                 m.antibiotic_susceptibility,
                 m.ictv_or_bergey_reference]
        if n in " ".join(parts).lower():
            out.append(m)
    return out


def microbes_for_kingdom(kingdom: str) -> List[Microbe]:
    """All microbes in a given kingdom."""
    return list_microbes(kingdom=kingdom)


def microbe_to_dict(m: Microbe) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(m)


def kingdoms() -> Tuple[str, ...]:
    return KINGDOMS


def gram_types() -> Tuple[str, ...]:
    return GRAM_TYPES


def baltimore_classes() -> Tuple[str, ...]:
    return BALTIMORE_CLASSES
