"""Phase PH-2.0 (round 220) — receptor pharmacology catalogue.

Additive deep-phase catalogue alongside the PH-1.0 drug-class
catalogue (`drug_classes.py`).  Covers the major drug-target
receptor superfamilies: GPCRs (aminergic + peptide + other),
nuclear hormone receptors, receptor tyrosine kinases, voltage-
+ ligand-gated ion channels, and small-molecule transporters.

Pure-headless: no Qt, no DB.

**Tuple-validation guard.** Same `__post_init__` validator
pattern that BC-2.0 (round 219) introduced for the cofactors
catalogue — refuses plain strings in tuple-typed fields, so
the trailing-comma single-element-tuple bug surfaces at
construction time instead of at test time.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy
# ----------------------------------------------------------------
RECEPTOR_FAMILIES: Tuple[str, ...] = (
    "gpcr-aminergic",         # adrenergic / muscarinic / dopaminergic / etc.
    "gpcr-peptide",           # opioid / angiotensin / GLP-1 / glucagon
    "gpcr-other",             # cannabinoid / sphingosine-1-P / chemokine
    "nhr-steroid",            # GR / ER / AR / PR / MR
    "nhr-other",              # TR / VDR / RAR-RXR / PPAR / FXR
    "rtk",                    # EGFR / HER2 / VEGFR / insulin / IGF-1R / MET
    "ion-channel-vg",         # voltage-gated Na+ / K+ / Ca2+
    "ion-channel-lg",         # ligand-gated nAChR / GABA-A / NMDA / AMPA
    "transporter-monoamine",  # SERT / NET / DAT
    "transporter-other",      # SGLT2 / MCT / P-glycoprotein
)


# Tuple-typed fields that must NEVER be plain strings.
_TUPLE_FIELDS: Tuple[str, ...] = (
    "endogenous_ligands",
    "signalling_output",
    "tissue_distribution",
    "clinical_relevance",
    "cross_reference_drug_class_ids",
    "cross_reference_signaling_pathway_ids",
    "cross_reference_enzyme_ids",
    "cross_reference_molecule_names",
)


@dataclass(frozen=True)
class Receptor:
    """One receptor entry in the PH-2.0 catalogue."""
    id: str
    name: str
    receptor_family: str                       # one of RECEPTOR_FAMILIES
    receptor_subtype: str                      # short label, e.g. "β1", "M3", "Nav1.7"
    structural_summary: str                    # 1-line architecture
    endogenous_ligands: Tuple[str, ...]
    signalling_output: Tuple[str, ...]         # G-protein / ion / second messenger
    tissue_distribution: Tuple[str, ...]
    clinical_relevance: Tuple[str, ...]        # diseases + therapeutic uses
    # Cross-references (the multi-studio link layer)
    cross_reference_drug_class_ids: Tuple[str, ...]
    # ↑ ids in pharm.core.drug_classes
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    cross_reference_enzyme_ids: Tuple[str, ...]
    # ↑ ids in biochem.core.enzymes (where the receptor IS an enzyme)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    notes: str = ""

    def __post_init__(self) -> None:
        """Reject plain strings in tuple-typed fields.

        Round-218 lesson: a single-element tuple needs a
        trailing comma — otherwise ``("foo")`` is just the
        string ``"foo"``.  Round-219 (BC-2.0) introduced this
        validator pattern; PH-2.0 inherits it.
        """
        for fld in _TUPLE_FIELDS:
            value = getattr(self, fld)
            if not isinstance(value, tuple):
                raise TypeError(
                    f"Receptor({self.id!r}): field {fld!r} must "
                    f"be a tuple, got {type(value).__name__} — "
                    f"add the trailing comma to single-element "
                    f"tuples (e.g. ('foo',) not ('foo')).")


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _receptor_list() -> List[Receptor]:
    """Lazy import of the data file so each file stays under
    the 500-line cap."""
    from pharm.core.receptors_data import RECEPTORS
    return RECEPTORS


def list_receptors(
    family: Optional[str] = None,
) -> List[Receptor]:
    """Return receptors, optionally filtered by family."""
    out = list(_receptor_list())
    if family:
        out = [r for r in out if r.receptor_family == family]
    return out


def get_receptor(receptor_id: str) -> Optional[Receptor]:
    """Return one receptor by id, or ``None``."""
    for r in _receptor_list():
        if r.id == receptor_id:
            return r
    return None


def find_receptors(needle: str) -> List[Receptor]:
    """Case-insensitive substring search across id + name +
    subtype + structural summary + ligands + signalling +
    tissue distribution + clinical relevance + notes +
    cross-reference molecule names."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[Receptor] = []
    for r in _receptor_list():
        parts = [r.id, r.name, r.receptor_subtype,
                 r.structural_summary, r.notes]
        parts.extend(r.endogenous_ligands)
        parts.extend(r.signalling_output)
        parts.extend(r.tissue_distribution)
        parts.extend(r.clinical_relevance)
        parts.extend(r.cross_reference_molecule_names)
        if n in " ".join(parts).lower():
            out.append(r)
    return out


def receptors_for_family(family: str) -> List[Receptor]:
    """All receptors in a given family."""
    return list_receptors(family=family)


def receptor_to_dict(r: Receptor) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(r)


def receptor_families() -> Tuple[str, ...]:
    return RECEPTOR_FAMILIES
