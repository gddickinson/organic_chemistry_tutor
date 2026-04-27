"""Phase PH-1.0 (round 214) — drug-class catalogue.

The flagship Pharmacology Studio catalogue.  ~ 30 drug classes
indexed by **molecular target type** + **therapeutic area**.

Each entry carries: mechanism, molecular target, typical agents,
clinical use, side effects, contraindications, monitoring, and
**typed cross-references to OrgChem molecules + Biochem enzyme
ids + Cell Bio signalling-pathway ids** — the multi-hop link
layer that makes the cross-studio audit non-trivial.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Target-class taxonomy
# ----------------------------------------------------------------
TARGET_CLASSES: Tuple[str, ...] = (
    "GPCR",                 # β-adrenergic, AT1, opioid, 5-HT, dopamine, …
    "RTK",                  # EGFR, HER2, BCR-ABL, BTK, JAK
    "ion-channel",          # Ca²⁺ blockers, Na⁺ channels, GABA-A
    "NHR",                  # nuclear hormone receptor (steroid receptors)
    "enzyme",               # ACE, HMG-CoA reductase, COX, MAO, gyrase, β-lactamase
    "transporter",          # SGLT2, SERT, NET, DAT, P-gp
    "antibody-target",      # PD-1, CD20, TNF-α, IL-6, VEGF
    "nucleic-acid",         # NRTIs, alkylators, taxanes (microtubule-binders)
    "other",                # GLP-1 agonists, insulin (mixed), heparin (antithrombin enhancer)
)


THERAPEUTIC_AREAS: Tuple[str, ...] = (
    "cardiovascular",
    "metabolic",
    "neurology-psychiatry",
    "oncology",
    "infectious",
    "inflammation-immunology",
    "pulmonology",
    "endocrinology",
    "haematology",
    "gastrointestinal",
    "pain",
)


# ----------------------------------------------------------------
# DrugClass dataclass
# ----------------------------------------------------------------
@dataclass(frozen=True)
class DrugClass:
    """One drug-class entry in the PH-1.0 catalogue."""
    id: str
    name: str
    target_class: str               # one of TARGET_CLASSES
    therapeutic_areas: Tuple[str, ...]
    mechanism: str
    molecular_target: str
    typical_agents: Tuple[str, ...]
    clinical_use: Tuple[str, ...]
    side_effects: Tuple[str, ...]
    contraindications: Tuple[str, ...]
    monitoring: Tuple[str, ...]
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _drug_class_list() -> List[DrugClass]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from pharm.core.drug_classes_data import DRUG_CLASSES
    return DRUG_CLASSES


def list_drug_classes(
    target_class: Optional[str] = None,
    therapeutic_area: Optional[str] = None,
) -> List[DrugClass]:
    """Return drug classes, optionally filtered by molecular
    target class and/or therapeutic area."""
    out = list(_drug_class_list())
    if target_class:
        out = [d for d in out if d.target_class == target_class]
    if therapeutic_area:
        out = [d for d in out
               if therapeutic_area in d.therapeutic_areas]
    return out


def get_drug_class(class_id: str) -> Optional[DrugClass]:
    """Return one drug class by id, or ``None`` if unknown."""
    for d in _drug_class_list():
        if d.id == class_id:
            return d
    return None


def find_drug_classes(needle: str) -> List[DrugClass]:
    """Case-insensitive substring search across id + name +
    mechanism + molecular target + typical agents + clinical
    use + side effects + contraindications."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[DrugClass] = []
    for d in _drug_class_list():
        parts = [d.id, d.name, d.mechanism,
                 d.molecular_target]
        parts.extend(d.typical_agents)
        parts.extend(d.clinical_use)
        parts.extend(d.side_effects)
        parts.extend(d.contraindications)
        if n in " ".join(parts).lower():
            out.append(d)
    return out


def drug_classes_for_target(
    target_class: str,
) -> List[DrugClass]:
    """All drug classes hitting a given target type."""
    return list_drug_classes(target_class=target_class)


def drug_class_to_dict(d: DrugClass) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(d)


def target_classes() -> Tuple[str, ...]:
    return TARGET_CLASSES


def therapeutic_areas() -> Tuple[str, ...]:
    return THERAPEUTIC_AREAS
