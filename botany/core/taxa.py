"""Phase BT-1.0 (round 216) — plant-taxa catalogue.

The flagship Botany Studio catalogue.  ~ 30 plant taxa spanning
the 6 major divisions (bryophyta / lycopodiophyta / pteridophyta
/ gymnosperm / angiosperm-monocot / angiosperm-eudicot), each
with metabolic-pathway + secondary-metabolite + drug-class
cross-references.

Pure-headless: no Qt, no DB.
"""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Tuple


# ----------------------------------------------------------------
# Taxonomy + traits
# ----------------------------------------------------------------
DIVISIONS: Tuple[str, ...] = (
    "bryophyta",            # mosses, liverworts, hornworts
    "lycopodiophyta",       # clubmosses, spikemosses, quillworts
    "pteridophyta",         # ferns + horsetails
    "gymnosperm",           # conifers, cycads, ginkgo, gnetophytes
    "angiosperm-monocot",   # grasses, lilies, orchids, palms
    "angiosperm-eudicot",   # most flowering plants
)

PHOTOSYNTHETIC_STRATEGIES: Tuple[str, ...] = (
    "C3",                # default — most plants
    "C4",                # maize, sugarcane, sorghum (PEP carboxylase)
    "CAM",               # crassulacean acid metabolism (cacti, aloe)
    "not-applicable",    # parasitic / mycoheterotrophic plants
)

LIFE_CYCLES: Tuple[str, ...] = (
    "annual",
    "biennial",
    "perennial",
    "not-applicable",    # holoparasites with weird life history
)


@dataclass(frozen=True)
class PlantTaxon:
    """One plant entry in the BT-1.0 catalogue."""
    id: str
    name: str                              # common name
    full_taxonomic_name: str               # binomial / cultivar
    division: str                          # one of DIVISIONS
    plant_class: str                       # liliopsida / magnoliopsida / pinopsida / etc.
    life_cycle: str                        # one of LIFE_CYCLES
    photosynthetic_strategy: str           # one of PHOTOSYNTHETIC_STRATEGIES
    reproductive_strategy: str
    ecological_role: str
    economic_importance: str
    model_organism: bool                   # is it a published model?
    genome_size_or_mb: str                 # "~125 Mb" / "~17 Gb" / etc.
    # Cross-references (the multi-studio link layer)
    cross_reference_molecule_names: Tuple[str, ...]
    # ↑ exact-name matches for orgchem.db.Molecule rows
    cross_reference_metabolic_pathway_ids: Tuple[str, ...]
    # ↑ ids in orgchem.core.metabolic_pathways
    cross_reference_pharm_drug_class_ids: Tuple[str, ...]
    # ↑ ids in pharm.core.drug_classes
    notes: str = ""


# ----------------------------------------------------------------
# Lookup helpers
# ----------------------------------------------------------------

def _taxon_list() -> List[PlantTaxon]:
    """Lazy import of the data file so each file stays under the
    500-line cap."""
    from botany.core.taxa_data import PLANT_TAXA
    return PLANT_TAXA


def list_plant_taxa(
    division: Optional[str] = None,
    photosynthetic_strategy: Optional[str] = None,
) -> List[PlantTaxon]:
    """Return plant taxa, optionally filtered."""
    out = list(_taxon_list())
    if division:
        out = [t for t in out if t.division == division]
    if photosynthetic_strategy:
        out = [t for t in out
               if t.photosynthetic_strategy
               == photosynthetic_strategy]
    return out


def get_plant_taxon(taxon_id: str) -> Optional[PlantTaxon]:
    """Return one plant taxon by id, or ``None``."""
    for t in _taxon_list():
        if t.id == taxon_id:
            return t
    return None


def find_plant_taxa(needle: str) -> List[PlantTaxon]:
    """Case-insensitive substring search across id + names +
    ecological role + economic importance + reproductive strategy
    + notes + cross-reference molecule names."""
    n = (needle or "").strip().lower()
    if not n:
        return []
    out: List[PlantTaxon] = []
    for t in _taxon_list():
        parts = [t.id, t.name, t.full_taxonomic_name,
                 t.plant_class, t.reproductive_strategy,
                 t.ecological_role, t.economic_importance,
                 t.notes]
        parts.extend(t.cross_reference_molecule_names)
        if n in " ".join(parts).lower():
            out.append(t)
    return out


def plant_taxa_for_division(division: str) -> List[PlantTaxon]:
    """All plant taxa in a given division."""
    return list_plant_taxa(division=division)


def plant_taxon_to_dict(t: PlantTaxon) -> Dict[str, object]:
    """JSON-friendly serialiser for agent actions."""
    return asdict(t)


def divisions() -> Tuple[str, ...]:
    return DIVISIONS


def photosynthetic_strategies() -> Tuple[str, ...]:
    return PHOTOSYNTHETIC_STRATEGIES


def life_cycles() -> Tuple[str, ...]:
    return LIFE_CYCLES
