"""Phase BC-1.0 (round 213) — enzyme catalogue (EC-class indexed).

The flagship Biochem Studio catalogue.  ~ 30 enzymes spanning
all 7 EC classes (1 = oxidoreductase, 2 = transferase, 3 =
hydrolase, 4 = lyase, 5 = isomerase, 6 = ligase, 7 = translocase
— class 7 added by IUBMB in 2018).  Each entry carries the full
EC number, mechanism class, substrates / products / cofactors /
regulators, disease associations, drug targets, and **typed
cross-references to OrgChem molecules + OrgChem metabolic
pathways + Cell Bio signalling pathways** — the core of the
multi-studio link audit.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# EC-class taxonomy
# ----------------------------------------------------------------
EC_CLASSES: Tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7)

EC_CLASS_NAMES: Dict[int, str] = {
    1: "Oxidoreductase",
    2: "Transferase",
    3: "Hydrolase",
    4: "Lyase",
    5: "Isomerase",
    6: "Ligase",
    7: "Translocase",
}

EC_CLASS_DESCRIPTIONS: Dict[int, str] = {
    1: "Catalyse oxidation-reduction reactions; transfer "
       "electrons / hydrogens / oxygen between substrates.",
    2: "Transfer a functional group (methyl, acyl, "
       "phosphoryl, glycosyl) between substrates.",
    3: "Catalyse hydrolysis (cleavage by water): proteases, "
       "nucleases, esterases, glycosidases, ATPases.",
    4: "Cleave bonds non-hydrolytically + non-oxidatively; "
       "often produce a double bond or ring (decarboxylases, "
       "dehydratases, cyclases).",
    5: "Catalyse intramolecular rearrangements: racemases, "
       "epimerases, cis/trans isomerases, mutases.",
    6: "Couple ATP / GTP hydrolysis to bond formation: "
       "aminoacyl-tRNA synthetases, carboxylases, ubiquitin "
       "ligases.",
    7: "Catalyse vectorial transport across a biological "
       "membrane coupled to chemistry — newest IUBMB class "
       "(2018) carved out from class 3 (ATPases) + class 5 "
       "(transporters).",
}


# ----------------------------------------------------------------
# Enzyme dataclass
# ----------------------------------------------------------------
@dataclass(frozen=True)
class Enzyme:
    """One enzyme entry in the BC-1.0 catalogue."""
    id: str
    name: str
    ec_number: str                  # e.g. "3.4.21.1"
    ec_class: int                   # 1..7
    mechanism_class: str            # "serine protease", "Zn metalloenzyme", …
    substrates: Tuple[str, ...]
    products: Tuple[str, ...]
    cofactors: Tuple[str, ...]
    regulators: Tuple[str, ...]
    disease_associations: Tuple[str, ...]
    drug_targets: Tuple[Tuple[str, str], ...]   # (drug, target)
    structural_family: str          # "TIM barrel", "α/β hydrolase fold", …
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    cross_reference_pathway_ids: Tuple[str, ...]
    # ↑ ids in orgchem.core.metabolic_pathways
    cross_reference_signaling_pathway_ids: Tuple[str, ...]
    # ↑ ids in cellbio.core.cell_signaling
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _enzyme_list() -> List[Enzyme]:
    """Lazy import of the 30-entry data so the dataclass file +
    its data file can each stay under the 500-line cap."""
    from biochem.core.enzymes_data import ENZYMES
    return ENZYMES


def list_enzymes(
    ec_class: Optional[int] = None,
) -> List[Enzyme]:
    """Return enzymes, optionally filtered by EC class (1-7)."""
    out = list(_enzyme_list())
    if ec_class is not None:
        out = [e for e in out if e.ec_class == ec_class]
    return out


def get_enzyme(enzyme_id: str) -> Optional[Enzyme]:
    """Return one enzyme by id, or ``None`` if unknown."""
    for e in _enzyme_list():
        if e.id == enzyme_id:
            return e
    return None


def find_enzymes(needle: str) -> List[Enzyme]:
    """Case-insensitive substring search across id + name +
    EC number + mechanism class + substrates + products +
    cofactors + disease associations + drug-target rows."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[Enzyme] = []
    for e in _enzyme_list():
        parts = [e.id, e.name, e.ec_number, e.mechanism_class,
                 e.structural_family]
        parts.extend(e.substrates)
        parts.extend(e.products)
        parts.extend(e.cofactors)
        parts.extend(e.disease_associations)
        for drug, tgt in e.drug_targets:
            parts.append(drug)
            parts.append(tgt)
        if n in " ".join(parts).lower():
            out.append(e)
    return out


def enzymes_for_ec_class(ec_class: int) -> List[Enzyme]:
    """All enzymes of a given EC class."""
    return list_enzymes(ec_class=ec_class)


def ec_class_of(e: Enzyme) -> str:
    """Human name for an enzyme's EC class."""
    return EC_CLASS_NAMES.get(e.ec_class, "Unknown")


def enzyme_to_dict(e: Enzyme) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(e)


def ec_class_names() -> Dict[int, str]:
    """Public access to the class-number → name map."""
    return dict(EC_CLASS_NAMES)


def ec_class_descriptions() -> Dict[int, str]:
    """Public access to the class-number → description map."""
    return dict(EC_CLASS_DESCRIPTIONS)
